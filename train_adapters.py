#!/usr/bin/env python3
"""Train the LoRA adapters of config/experiment.json and convert them for llama.cpp.

    python3 train_adapters.py            # every model in the config
    python3 train_adapters.py Beta       # only these identities
    python3 train_adapters.py --corpus FILE --adapters NAME   # another corpus, as its own adapter set

For each model: tokenise the training corpus ("training" in the config) with the model's chat
template from the config (the file llama-server is given), fine-tune a LoRA adapter on it, and
convert the adapter to GGUF with llama.cpp's convert_lora_to_gguf.py. Output, per model, named
after the config's "adapters":

    artifacts/<name>/<name>_<adapters>/          adapter, tokenizer, checkpoints,
                                                 loss_curve.csv, training_meta.json
    artifacts/<name>/<name>_<adapters>.gguf      what replay.py and tournament.py load

A model whose .gguf already exists is skipped — delete it, or name a new set in "adapters", to
train again. Building a corpus is separate: training/generate_data/bot_corpus.py. Needs:
pip install -r training/requirements.txt.
"""

import os

# Long sequences fragment CUDA memory; Qwen ran out at batch 4 without this.
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import argparse  # noqa: E402
import csv  # noqa: E402
import inspect  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
import traceback  # noqa: E402
from pathlib import Path  # noqa: E402

import torch  # noqa: E402
from datasets import Dataset  # noqa: E402
from peft import LoraConfig, get_peft_model  # noqa: E402
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent
EXPERIMENT = json.loads((REPO_ROOT / "config" / "experiment.json").read_text())
TRAINING = EXPERIMENT["training"]

RESPONSE_MARKER = "[JSON]"
DTYPES = {"float32": torch.float32, "float16": torch.float16, "bfloat16": torch.bfloat16}
GGUF_OUTTYPE = {"float32": "f32", "float16": "f16", "bfloat16": "bf16"}
# Which weight matrices get a LoRA update. Llama-style names cover Granite and Gemma 4; LFM2 calls
# its MLP w1/w2/w3 and the input/output projections of its conv blocks (and its attention output)
# in_proj/out_proj, which no other model uses. lm_head is never targeted — most of these models tie
# it to the input embeddings, which llama.cpp's converter rejects.
TARGET_MODULE_PRESETS = {
    "attention_qv": ["q_proj", "v_proj"],
    "all_linear": ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj",
                   "in_proj", "out_proj", "w1", "w2", "w3"],
}
# Gemma 4 loads with its vision and audio encoders, whose layers reuse those names: the game sends
# text only, and llama.cpp's adapter converter maps text-model tensors only.
EXCLUDED_MODULES = r".*\.(vision_tower|audio_tower)\..*"
CURVE_FIELDS = ("step", "epoch", "loss", "eval_loss", "learning_rate", "grad_norm")
LOGGING_STEPS = 50   # at most; fewer optimiser steps log more often (see train)
EVAL_STEPS = 200     # likewise
VAL_FRACTION = 0.1   # held out for the eval curve
SPLIT_SEED = 0       # fixed so every adapter is trained on the same split


def target_modules() -> list[str]:
    targets = TRAINING["lora"]["target_modules"]
    if isinstance(targets, str):
        if targets not in TARGET_MODULE_PRESETS:
            raise SystemExit(f"unknown target_modules preset {targets!r}; known: {sorted(TARGET_MODULE_PRESETS)}")
        return TARGET_MODULE_PRESETS[targets]
    return list(targets)


def check_dependencies() -> None:
    """Fail before the base model is downloaded, not after: apply_chat_template renders the
    model's template with Jinja, and transformers does not install jinja2 itself — without this
    the run dies on the first corpus entry, having already pulled several GB of weights."""
    try:
        import jinja2
    except ImportError:
        raise SystemExit("jinja2 is required to apply the chat template.\n  pip install 'jinja2>=3.1.0'")
    major, minor, *_ = (jinja2.__version__.split(".") + ["0", "0"])[:3]
    if (int(major), int(minor)) < (3, 1):
        raise SystemExit(f"jinja2 {jinja2.__version__} is too old for apply_chat_template.\n"
                         f"  pip install -U 'jinja2>=3.1.0'")


def _eval_arg_name() -> str:
    """`evaluation_strategy` was renamed `eval_strategy` in transformers 4.41 and removed in 4.46;
    pick whichever this install accepts, so the run does not die after the model has loaded."""
    params = inspect.signature(TrainingArguments.__init__).parameters
    return "eval_strategy" if "eval_strategy" in params else "evaluation_strategy"


def _group_by_length_kwargs() -> dict:
    """`group_by_length=True` became `train_sampling_strategy="group_by_length"` in transformers 5
    (needed for Gemma 4); same choice as _eval_arg_name, so either install trains."""
    params = inspect.signature(TrainingArguments.__init__).parameters
    if "train_sampling_strategy" in params:
        return {"train_sampling_strategy": "group_by_length"}
    return {"group_by_length": True}


def _pick_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


# ── Corpus → training examples ────────────────────────────────────────────────

def tokenize_entries(tok, model_name: str, corpus: Path) -> list[tuple[list, list]]:
    """Tokenize each corpus entry — a state line, then "[JSON] <response>" — into
    (prompt_ids, response_ids).

    The state becomes a user turn and the response an assistant turn, in the base model's own
    template: that gives the format three things raw text cannot express — where the input ends,
    where the output ends, and that this is one self-contained exchange — and the game serves the
    adapters through the same chat endpoint. The prompt is rendered with add_generation_prompt=True,
    exactly the string inference sends, and the response is the content plus an explicit EOS. The
    response is not derived by subtracting the prompt from a two-turn rendering: TinyLlama's
    template emits different whitespace in the two cases, so the split would land in the wrong place.
    """
    def encode(text):
        return tok(text, add_special_tokens=False, truncation=False, verbose=False)["input_ids"]

    if tok.eos_token_id is None:
        raise SystemExit(f"{model_name} has no eos_token_id. Training without an end-of-response "
                         f"token is what produces truncated output; set tok.eos_token first.")
    has_template = bool(getattr(tok, "chat_template", None))
    if not has_template:
        print(f"WARNING: {model_name} has no chat template, falling back to the raw '{RESPONSE_MARKER}' "
              f"format. The game still posts to the chat endpoint, so training and inference formats "
              f"will NOT match — pick an instruction-tuned base or set llm.chat_template.")

    entries = []
    for chunk in corpus.read_text(encoding="utf-8").strip().split("\n\n"):
        lines = [line for line in chunk.split("\n") if line.strip()]
        if len(lines) < 2 or not lines[1].startswith(RESPONSE_MARKER):
            continue
        state, response = lines[0], lines[1][len(RESPONSE_MARKER):].strip()
        if has_template:
            prompt = tok.apply_chat_template([{"role": "user", "content": state}],
                                             tokenize=False, add_generation_prompt=True)
            prompt_ids = encode(prompt)
        else:
            prompt_ids = encode(state + "\n" + RESPONSE_MARKER + " ")
        # explicit EOS: the one token that teaches the model to stop
        entries.append((prompt_ids, encode(response) + [tok.eos_token_id]))
    return entries


def build_examples(entries, max_len: int) -> tuple[list, list]:
    """One training example per corpus entry: the whole state, then the response.

    Variable-length lists — the collator pads each batch to its own longest member, so a short
    entry never pays for a long one. labels are -100 across the prompt, so the loss covers only the
    response, while the model still reads the entire state it has to copy card names from.
    Entries longer than max_len are dropped, not truncated: truncating would cut either the
    response being scored or the state it copies from.
    """
    ids, labels, dropped = [], [], 0
    for prompt_ids, response_ids in entries:
        if len(prompt_ids) + len(response_ids) > max_len:
            dropped += 1
            continue
        ids.append(prompt_ids + response_ids)
        labels.append([-100] * len(prompt_ids) + response_ids)
    if dropped:
        print(f"Dropped {dropped} of {len(entries)} entries longer than sequence_length={max_len}; "
              f"raise it to keep them.")
    return ids, labels


def make_collator(pad_token_id: int):
    """Pad each batch to its own longest example, preserving masked labels. Not
    DataCollatorForLanguageModeling: with mlm=False it overwrites labels with input_ids, silently
    undoing the prompt masking. Pad positions get label -100 and attention 0."""
    def collate(features: list[dict]) -> dict:
        longest = max(len(f["input_ids"]) for f in features)
        out = {"input_ids": [], "labels": [], "attention_mask": []}
        for f in features:
            pad = longest - len(f["input_ids"])
            out["input_ids"].append(list(f["input_ids"]) + [pad_token_id] * pad)
            out["labels"].append(list(f["labels"]) + [-100] * pad)
            out["attention_mask"].append([1] * len(f["input_ids"]) + [0] * pad)
        return {k: torch.tensor(v, dtype=torch.long) for k, v in out.items()}
    return collate


def split_train_eval(dataset):
    """Hold out a deterministic slice for the eval curve (none if the corpus is too small)."""
    n_val = int(len(dataset) * VAL_FRACTION)
    if n_val < 1 or len(dataset) - n_val < 1:
        print(f"Dataset has {len(dataset)} sequences — too few to hold out {VAL_FRACTION:.0%}; "
              f"training without an eval curve.")
        return dataset, None
    split = dataset.train_test_split(test_size=VAL_FRACTION, seed=SPLIT_SEED)
    print(f"Split {len(dataset)} sequences → {len(split['train'])} train / {len(split['test'])} eval "
          f"(seed {SPLIT_SEED})")
    return split["train"], split["test"]


# ── Training ──────────────────────────────────────────────────────────────────

def save_loss_curve(trainer, model: dict, out_dir: Path, n_train: int, n_eval: int,
                    logging_steps: int, eval_steps: int | None) -> None:
    """Keep the loss curve next to the adapter. With report_to="none", log_history otherwise only
    lives inside checkpoint-*/trainer_state.json. Writes loss_curve.csv (one row per logged step),
    trainer_state.json and training_meta.json (the recipe actually used)."""
    trainer.save_state()
    adapter = out_dir.name
    rows = [{"adapter": adapter, **{k: record.get(k) for k in CURVE_FIELDS}}
            for record in trainer.state.log_history if "loss" in record or "eval_loss" in record]
    with (out_dir / "loss_curve.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=("adapter", *CURVE_FIELDS))
        writer.writeheader()
        writer.writerows(rows)

    peft_cfg = trainer.model.peft_config["default"]
    args = trainer.args
    meta = {
        "adapter": adapter,
        "base_model": model["hf"],
        "epochs": trainer.state.epoch,
        "batch_size": model["batch_size"],
        "seq_len": TRAINING["sequence_length"],
        "dtype": model["dtype"],
        "lora": {"r": peft_cfg.r, "alpha": peft_cfg.lora_alpha, "dropout": peft_cfg.lora_dropout,
                 "target_modules": sorted(peft_cfg.target_modules),
                 "trainable_parameters": sum(p.numel() for p in trainer.model.parameters() if p.requires_grad)},
        "training": {
            "learning_rate": args.learning_rate,
            "lr_scheduler": str(getattr(args.lr_scheduler_type, "value", args.lr_scheduler_type)),
            "warmup_ratio": args.warmup_ratio,
            "gradient_accumulation_steps": args.gradient_accumulation_steps,
            "effective_batch_size": model["batch_size"] * args.gradient_accumulation_steps,
            "bf16_mixed_precision": args.bf16,
            "optimizer_steps": trainer.state.global_step,
        },
        "train_file": TRAINING["corpus"],
        "train_sequences": n_train,
        "eval_sequences": n_eval,
        "split_seed": SPLIT_SEED if n_eval else None,
        "logging_steps": logging_steps,
        "eval_steps": eval_steps,
        "logged_points": len(rows),
        "final_train_loss": next((r["loss"] for r in reversed(rows) if r["loss"] is not None), None),
        "final_eval_loss": next((r["eval_loss"] for r in reversed(rows) if r["eval_loss"] is not None), None),
    }
    (out_dir / "training_meta.json").write_text(json.dumps(meta, indent=2))
    print(f"Saved loss curve ({len(rows)} points) to {out_dir / 'loss_curve.csv'}")


def train(model: dict, out_dir: Path) -> None:
    """Fine-tune one base model on the training corpus, writing the adapter to out_dir."""
    check_dependencies()
    device = _pick_device()
    batch = model["batch_size"]
    effective = TRAINING["effective_batch_size"] or batch
    if effective % batch:
        raise SystemExit(f"effective_batch_size {effective} is not a multiple of {model['identity']}'s batch_size {batch}")
    accumulation = effective // batch
    bf16 = TRAINING["mixed_precision"] == "bf16"
    if bf16 and not (device.type == "cuda" and torch.cuda.is_bf16_supported()):
        print(f"WARNING: bf16 mixed precision needs a CUDA GPU with bf16 support; training on {device} in the model's dtype")
        bf16 = False
    lora, max_len, epochs = TRAINING["lora"], TRAINING["sequence_length"], TRAINING["epochs"]
    print(f"-----\n>> TRAINING {model['identity']} <<\nModel: {model['hf']} on {device}\n"
          f"Max Length: {max_len}\nDType: {model['dtype']}{' + bf16 mixed precision' if bf16 else ''}\n"
          f"Batch Size: {batch} x {accumulation} accumulation = {effective}\n"
          f"LoRA: r={lora['r']} alpha={lora['alpha']} targets={target_modules()}\n"
          f"LR: {TRAINING['learning_rate']} {TRAINING['lr_scheduler']}, warmup {TRAINING['warmup_ratio']:.0%}\n-----")

    tok = AutoTokenizer.from_pretrained(model["hf"])
    # The served template, not the tokenizer's own: Granite's thinks unless told not to, and the
    # adapter must learn the exact prompt llama-server renders from --chat-template-file.
    tok.chat_template = (REPO_ROOT / model["chat_template"]).read_text()
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    base = AutoModelForCausalLM.from_pretrained(model["hf"], dtype=DTYPES[model["dtype"]])
    base.to(device)

    corpus = REPO_ROOT / TRAINING["corpus"]
    entries = tokenize_entries(tok, model["hf"], corpus)
    sequences, labels = build_examples(entries, max_len)
    if not sequences:
        raise SystemExit(f"{corpus} produced no training examples from {len(entries)} entries at "
                         f"sequence_length={max_len}: wrong format, or every entry is too long.")
    real = sum(map(len, sequences))
    scored = sum(label != -100 for seq in labels for label in seq)
    print(f"{len(entries)} corpus entries -> {len(sequences)} training examples, {real:,} tokens, "
          f"{scored:,} scored ({scored / real:.1%})")
    ds_train, ds_eval = split_train_eval(Dataset.from_dict({"input_ids": sequences, "labels": labels}))

    # only where there is something to exclude: peft warns about a pattern that matches nothing
    exclude = EXCLUDED_MODULES if any(re.fullmatch(EXCLUDED_MODULES, n) for n, _ in base.named_modules()) else None
    peft_model = get_peft_model(base, LoraConfig(r=lora["r"], lora_alpha=lora["alpha"], target_modules=target_modules(),
                                                 exclude_modules=exclude,
                                                 lora_dropout=lora["dropout"], bias="none"))
    # The base model is frozen, so the recomputed forward inside each checkpointed layer has no
    # requires_grad tensor unless forced here — without it backward can't reach the adapters.
    peft_model.enable_input_require_grads()
    peft_model.print_trainable_parameters()

    # Logging and evaluation count optimiser steps, so with gradient accumulation there are far
    # fewer: aim for ~50 loss points and ~10 evaluations per run.
    total_steps = math.ceil(len(ds_train) / effective) * math.ceil(epochs)
    logging_steps = min(LOGGING_STEPS, max(1, total_steps // 50))
    eval_steps = min(EVAL_STEPS, max(1, total_steps // 10)) if ds_eval is not None else None
    eval_kwargs = {_eval_arg_name(): "steps", "eval_steps": eval_steps,
                   "per_device_eval_batch_size": batch * 2} if ds_eval is not None else {}

    trainer = Trainer(
        model=peft_model,
        args=TrainingArguments(
            output_dir=str(out_dir),
            per_device_train_batch_size=batch,
            gradient_accumulation_steps=accumulation,
            num_train_epochs=epochs,
            learning_rate=TRAINING["learning_rate"],
            lr_scheduler_type=TRAINING["lr_scheduler"],
            warmup_ratio=TRAINING["warmup_ratio"],
            logging_steps=logging_steps,
            save_steps=200,
            bf16=bf16,                     # only on CUDA: MPS + bf16/fp16 can be finicky
            report_to="none",
            dataloader_pin_memory=False,
            gradient_checkpointing=True,
            gradient_checkpointing_kwargs={"use_reentrant": False},
            **_group_by_length_kwargs(),   # similar lengths together: dynamic padding adds almost nothing
            **eval_kwargs,
        ),
        data_collator=make_collator(tok.pad_token_id),
        train_dataset=ds_train,
        eval_dataset=ds_eval,
    )
    trainer.train()

    trainer.model.save_pretrained(str(out_dir))
    tok.save_pretrained(str(out_dir))
    print(f"Saved LoRA adapter to {out_dir}/")
    save_loss_curve(trainer, model, out_dir, len(ds_train), len(ds_eval) if ds_eval is not None else 0,
                    logging_steps, eval_steps)


def convert_to_gguf(model: dict, out_dir: Path, gguf: Path) -> None:
    converter = (REPO_ROOT / EXPERIMENT["llama_cpp"]).resolve() / "convert_lora_to_gguf.py"
    subprocess.run([sys.executable, str(converter), str(out_dir), "--outfile", str(gguf),
                    "--outtype", GGUF_OUTTYPE[model["dtype"]]], check=True)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("identities", nargs="*", help="only these models (default: all)")
    p.add_argument("--corpus", help="train on this corpus instead of the config's training.corpus (needs --adapters)")
    p.add_argument("--adapters", help="name of the adapter set to write instead of the config's adapters")
    args = p.parse_args()
    if args.corpus and not args.adapters:
        p.error("--corpus needs --adapters: the config's adapter set was trained on the config's corpus")
    if args.corpus:
        if not (REPO_ROOT / args.corpus).is_file():
            p.error(f"corpus not found: {args.corpus}")
        TRAINING["corpus"] = args.corpus
    if args.adapters:
        EXPERIMENT["adapters"] = args.adapters
    known = [m["identity"] for m in EXPERIMENT["models"]]
    unknown = set(args.identities) - set(known)
    if unknown:
        p.error(f"unknown identities {sorted(unknown)}; known: {known}")
    models = [m for m in EXPERIMENT["models"] if not args.identities or m["identity"] in args.identities]

    failed = []
    for model in models:
        out_dir = REPO_ROOT / "artifacts" / model["name"] / f"{model['name']}_{EXPERIMENT['adapters']}"
        gguf = out_dir.with_name(out_dir.name + ".gguf")
        if gguf.exists():
            print(f"{model['identity']}: {gguf.relative_to(REPO_ROOT)} exists — skipped "
                  f"(delete it, or name a new set in \"adapters\", to train again)")
            continue
        started = time.time()
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
            train(model, out_dir)
            convert_to_gguf(model, out_dir, gguf)
            print(f"{model['identity']}: done in {(time.time() - started) / 60:.0f} min -> {gguf.relative_to(REPO_ROOT)}")
        except Exception as e:
            traceback.print_exc()
            failed.append(f"{model['identity']}: {type(e).__name__}: {e}")
    if failed:
        sys.exit("failed:\n  " + "\n  ".join(failed))


if __name__ == "__main__":
    main()
