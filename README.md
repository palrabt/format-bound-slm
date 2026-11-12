# Format-bound competence of fine-tuned small language models in a card game

Code, data and run logs behind the paper of the same title (submitted to *Pollack Periodica*). Three
small language models (LFM2.5-1.2B, Granite-4.2-3B, Gemma-4-E2B), each with and without a LoRA
adapter trained on a rule-based teacher, play a simplified three-player Bohnanza under four prompt
styles. They are scored on 992 fixed game states (the replay) and in 30 seeded games per player
(the tournaments). An earlier generation (TinyLlama-1.1B, Qwen2.5-3B, Gemma-2B), trained and scored
the same way, serves as the replication.

## Check the paper's numbers (no GPU, no model, about a minute)

```bash
pip install -r requirements.txt
python3 paper/paper_numbers.py --rescore
```

`--rescore` does the following:

1. Unpacks every run's raw logs (`runs/*.tar.xz`) into `work/`.
2. Scores every logged answer again with `eval/evaluate.py`, checking each result
   against the shipped `runs/<run>/metrics.json`.
3. Rebuilds Tables 1–5 of `paper/paper.md`, together with the in-text numbers.
4. Lists every cell or number that differs from the paper.

It also scores the three baselines that need no model on the replay corpus: the reference bot, the
random bot and the fixed rule. Without `--rescore` the script skips steps 1–2 and reads the
shipped metrics. The exit status is 0 when everything matches.

## Contents

| Path | What it is |
|---|---|
| `game/` | The game: deck server, player servers, the LLM player (`game/player/llm.py`), the four prompt styles (`game/player/prompts/`), the answer schemas (`game/schemas/`) and the reference and random bots (`game/player/bots.py`) |
| `bohnanza.py`, `player.py`, `start_game.sh` | Entry points of the deck and player servers, and their launcher |
| `replay.py` | Asks every condition about every state of the replay corpus |
| `tournament.py` | The seeded tournaments: game g uses deck seed g and seat (g − 1) mod 3 |
| `train_adapters.py` | Trains the LoRA adapters and converts them to GGUF |
| `run_experiment.py` | Runs the steps above in order, unattended, and evaluates the results |
| `eval/` | Scoring: schema validity, legality, the reference rules (`reference.py`), avoidable harvests (`state_sensitivity.py`), agreement, paired tests (`effects.py`, `stats.py`), coins (`game_outcomes.py`); `evaluate.py` runs them all |
| `eval/replay_corpus.json` | The 992 replay states: 500 from earlier games, balanced per message type on what the decision turns on, and 492 held-out teacher states with the teacher's answers. The file is the record; the script that selected the states, and the game logs it drew on, are not included |
| `training/generate_data/` | The teacher (`synth.py`, which shares its message rules with the hand-entry tool `cli.py`) and the Phi-4 rewording of the free text (`llm_text.py`) |
| `training/corpus/` | The training corpus (15,000 examples), the held-out teacher states of the replay's training slice, and 445 human-written entries (`training_data.txt`) that `llm_text.py` shows Phi-4 as style examples |
| `training/records/` | Each adapter's training record: configuration, loss curve, trainer state, final losses |
| `config/experiment.json` | The one configuration: models, adapters, the 2 × 4 conditions, the training recipe, the tournament |
| `config/experiment_gen1.json` | The same configuration for the earlier generation |
| `config/chat_templates/` | The chat template of each model, used both in training and by llama-server |
| `runs/` | The six runs the paper reports, each as raw logs (`<run>.tar.xz`) plus their `metrics.md`, `metrics.json` and `run.json` |
| `weights.json` | Every model file the runs used, with Hugging Face source, size and sha256, and the data files' checksums |
| `paper/` | The paper source (`paper.md`, `references.bib`), its Word build (`build_docx.py`, needing python-docx), and `paper_numbers.py` |

### The runs

| Run | What | Paper |
|---|---|---|
| `replay_20261029_gen2` | Replay, main study, 8 conditions × 3 models × 992 states | Tables 1, 2, 4, 5 |
| `suite_20261029_gen2` | Tournament, main study, against two reference bots | Tables 3, 5 |
| `suite_20261030_gen2_vsrandom` | Tournament, main study, against two random bots | Tables 3, 5 |
| `replay_20261006_2x4` | Replay, earlier generation | Table 5 |
| `suite_20261102_phase1_fixed` | Tournament, earlier generation, against two reference bots | Table 5 |
| `suite_20261102_phase1_fixed_vsrandom` | Tournament, earlier generation, against two random bots | Table 5 |

The `metrics.*` files were written by this repository's `eval/evaluate.py` from the raw logs.
Every metric in them equals the one written when the runs were made. The sections the paper
doesn't use are left out: the free-text analysis, the trade counts and a comparison with bots
outside this study.

The free text the players write (their reasons and messages) is in the logs, but neither the paper
nor this code analyzes it.

## Reproduce the runs

The runs were made on one NVIDIA L4 (24 GB) with Python 3.10.12 and llama.cpp at commit
`e583f3b4f5dabf9a6e987772d4e4daf121858707` (version 8918). The configuration expects that
checkout at `../llama.cpp`, built with CUDA into `build-cuda/bin/llama-server`; `--cpu` uses
`../llama.cpp/llama-server`.

1. **Models.** Put the files listed in `weights.json` at their paths under `artifacts/`:
   - **Base models:** convert each from the Hugging Face model named in `weights.json` with
     llama.cpp's `convert_hf_to_gguf.py`. The main study's models are Q8_0. In the earlier
     generation, TinyLlama is F16, Qwen2.5 is Q4_K_M and Gemma-2B is F32.
   - **Adapters:** download them from the location given in `weights.json`, or retrain them
     (step 2).

   The sha256 values identify the exact files used. A fresh conversion may differ in its bytes.
2. **Adapters (optional).** `pip install -r training/requirements.txt`, then
   `python3 train_adapters.py`. This trains the adapter of every model in `config/experiment.json`
   on `training/corpus/training_data_synct_15000_llm.txt` and converts it to GGUF. An adapter that
   already exists is skipped. The recipe:
   - rank 32, alpha 64, dropout 0.05, all linear layers;
   - 2 epochs, learning rate 1e-4 with a cosine schedule and 5% warm-up;
   - effective batch size 64, sequences of up to 768 tokens;
   - split seed 0.

   `training/records/` holds the losses each adapter reached.
3. **Main study.**

   ```bash
   python3 run_experiment.py --id gen2                    # adapters (if missing), replay, tournament vs reference bots, evaluation
   python3 run_experiment.py --id gen2_vsrandom --tournament-only --opponents bot_random
   ```

   The output goes to `logs/replay_gen2/`, `logs/suite_gen2/` and `logs/suite_gen2_vsrandom/`,
   each with its `metrics.md`. To check the new runs with `paper/paper_numbers.py`, copy them into
   `runs/` under the names in the table above.
4. **Earlier generation.** Copy `config/experiment_gen1.json` over `config/experiment.json` and
   repeat step 3.

Decoding is greedy (temperature 0). The random bot is seeded by the state it is asked about, and
the tournaments by deck seed and seat, so reruns meet the same states and card sequences.
Differences between GPU and CPU builds, or between llama.cpp versions, can still change individual
answers.

The earlier generation's replay was made on 2026-10-06. The phase-1 record of the original
repository (commit `6e10a58` there) lists it as produced by that commit's code. The prompts,
schemas, replay code, chat templates and replay corpus are unchanged since then, and re-scoring
its raw logs with this code gives its logged metrics exactly. The earlier generation's
tournaments were rerun on 2026-11-02 with this code.

## The training corpus

The teacher is partly random:
- it plants on field 1 when no field fits, and plants its second card at random;
- it picks its trading partner, and whether to pass, at random;
- it accepts about 40–45% of useless offers.

The reference bot plays the teacher's deterministic rules, with the random and arbitrary choices
replaced by value rules (`eval/reference.py`).

To regenerate the corpus:
1. `python3 -m training.generate_data.synth --count 3000` generates the decisions.
2. `python3 -m training.generate_data.llm_text` rewords the free text with Phi-4, served by
   llama-server, using the human-written lines of `training/corpus/training_data.txt` as style
   examples.

The exact seeds of the shipped corpus are not recorded. The shipped corpus is therefore the record;
its checksum is in `weights.json`.
