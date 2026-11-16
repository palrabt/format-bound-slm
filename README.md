# Format-bound competence of fine-tuned small language models in a card game

Code, data and run logs behind the paper of the same title (submitted to *Pollack Periodica*). Three
small language models (LFM2.5-1.2B, Granite-4.2-3B, Gemma-4-E2B), each with and without a LoRA
adapter, play a simplified three-player Bohnanza under four prompt styles. The adapters are trained on
the decisions of a deterministic rule-based teacher, the reference bot. The models are scored on 992
fixed game states (the replay) and in 30 seeded games per player against reference bots and against
random bots (the tournaments).

## Check the paper's numbers (no GPU, no model, about a minute)

```bash
pip install -r requirements.txt
python3 paper/paper_numbers.py --rescore
```

`--rescore` does the following:

1. Unpacks every run's raw logs (`runs/*.tar.xz`) into `work/`.
2. Scores every logged answer again with `eval/evaluate.py`, checking each result against the
   shipped `runs/<run>/metrics.json`.
3. Rebuilds Tables 1–4 of `paper/paper.md`, together with the in-text numbers.
4. Lists every cell or number that differs from the paper.

It also scores the two baselines that need no model on the replay corpus: the random bot and the
fixed rule. Without `--rescore` the script skips steps 1–2 and reads the shipped metrics. The exit
status is 0 when everything matches.

## Contents

| Path | What it is |
|---|---|
| `game/` | The game: deck server, player servers, the LLM player (`game/player/llm.py`), the four prompt styles (`game/player/prompts/`), the answer schemas (`game/schemas/`) and the reference and random bots (`game/player/bots.py`) |
| `bohnanza.py`, `player.py`, `start_game.sh` | Entry points of the deck and player servers, and their launcher |
| `replay.py` | Asks every condition about every state of the replay corpus |
| `tournament.py` | The seeded tournaments: game g uses deck seed g and seat (g − 1) mod 3 |
| `train_adapters.py` | Trains the LoRA adapters and converts them to GGUF |
| `run_experiment.py` | Runs the steps above in order, unattended, and evaluates the results |
| `eval/` | Scoring: schema validity, legality, valid play (`valid_play.py`: the answer keeps every rule the teacher plays by), reference-correctness (`reference.py`: the reference bot's decision in the same state), avoidable harvests (`state_sensitivity.py`), agreement, paired tests (`effects.py`, `stats.py`), coins (`game_outcomes.py`); `evaluate.py` runs them all |
| `eval/replay_corpus.json` | The 992 replay states: 500 from earlier games, balanced per message type on what the decision turns on, and 492 held-out states from the training corpus's generator. The file is the record. Its training-slice items also carry an earlier teacher's answers, which nothing here uses |
| `training/generate_data/` | `bot_corpus.py` answers a corpus's states with the reference bot; `synth.py` holds the states' generator, the answer templates and the earlier, partly random teacher whose rules the reference bot cleans up; `cli.py` its shared message rules |
| `training/corpus/training_data_reference_15000.txt` | The training corpus: 15,000 states, 3,000 per message type, each answered by the reference bot |
| `training/records/` | Each adapter's training record: configuration, loss curve, trainer state, final losses |
| `config/experiment.json` | The one configuration: models, adapters, the 2 × 4 conditions, the training recipe, the tournament |
| `config/chat_templates/` | The chat template of each model, used both in training and by llama-server |
| `runs/` | The three runs the paper reports, each as raw logs (`<run>.tar.xz`) plus their `metrics.md`, `metrics.json` and `run.json` |
| `weights.json` | Every model file the runs used, with Hugging Face source, size and sha256, and the data files' checksums |
| `paper/` | The paper source (`paper.md`, `references.bib`), its Word build (`build_docx.py`, needing python-docx), and `paper_numbers.py` |

### The runs

| Run | What | Paper |
|---|---|---|
| `replay_20261115_ref` | Replay, 8 conditions × 3 models × 992 states | Tables 1, 2, 4 |
| `suite_20261115_ref` | Tournament against two reference bots | Table 3 |
| `suite_20261115_ref_vsrandom` | Tournament against two random bots | Table 3 |

The conditions with the adapter were run on 2026-11-15. The conditions without it, and the two
baseline bots in the tournaments, don't depend on the adapter. They were run once, on 2026-10-29/30,
with the same code, models, prompts, states and seeds, and copied into these runs; each run's
`run.json` names where every condition came from.

The `metrics.*` files were written by this repository's `eval/evaluate.py` from the raw logs.
Reference-correctness compares every answer's decision with the one the reference bot, the adapters' teacher, makes in
the same state.
The free text the players write (their reasons and messages) is in the logs, but neither the paper
nor this code analyzes it.

## Reproduce the runs

The runs were made on one NVIDIA L4 (24 GB) with Python 3.10.12 and llama.cpp at commit
`e583f3b4f5dabf9a6e987772d4e4daf121858707` (version 8918). The configuration expects that
checkout at `../llama.cpp`, built with CUDA into `build-cuda/bin/llama-server`; `--cpu` uses
`../llama.cpp/llama-server`.

1. **Models.** Put the files listed in `weights.json` at their paths under `artifacts/`:
   - **Base models:** convert each from the Hugging Face model named in `weights.json` with
     llama.cpp's `convert_hf_to_gguf.py`, quantized to Q8_0.
   - **Adapters:** download them from the location given in `weights.json`, or retrain them
     (step 2).

   The sha256 values identify the exact files used. A fresh conversion may differ in its bytes.
2. **Adapters (optional).** `pip install -r training/requirements.txt`, then
   `python3 train_adapters.py`. This trains the adapter of every model in `config/experiment.json`
   on `training/corpus/training_data_reference_15000.txt` and converts it to GGUF. An adapter that
   already exists is skipped. The recipe:
   - rank 32, alpha 64, dropout 0.05, all linear layers;
   - 2 epochs, learning rate 1e-4 with a cosine schedule and 5% warm-up;
   - effective batch size 64, sequences of up to 768 tokens;
   - split seed 0.

   Training took 0.75 h for LFM2.5, 3.1 h for Granite and 6.2 h for Gemma 4. `training/records/`
   holds the losses each adapter reached.
3. **The experiment.**

   ```bash
   python3 run_experiment.py --id ref                    # adapters (if missing), replay, tournament vs reference bots, evaluation
   python3 run_experiment.py --id ref_vsrandom --tournament-only --opponents bot_random
   ```

   The output goes to `logs/replay_ref/`, `logs/suite_ref/` and `logs/suite_ref_vsrandom/`, each
   with its `metrics.md`. A fresh run plays every condition, including those without the adapter.
   To check the new runs with `paper/paper_numbers.py`, copy them into `runs/` under the names in
   the table above.

Decoding is greedy (temperature 0). The random bot is seeded by the state it is asked about, and
the tournaments by deck seed and seat, so reruns meet the same states and card sequences.
Differences between GPU and CPU builds, or between llama.cpp versions, can still change individual
answers.

## The training corpus

The teacher is the reference bot (`game/player/bots.py`, which lists its rules): the deterministic
rules of an earlier, partly random teacher (`synth.py`), with its random and arbitrary choices
replaced by value rules. The corpus keeps the 15,000 states of that earlier teacher's corpus:
synth.py's states, the free text a player receives in them reworded by Phi-4. Only the answers are
the reference bot's, their free text worded with synth.py's templates. Every answer is legal and,
by construction, valid play and reference-correct (`eval/evaluate.py` checks both on the corpus: 15,000 of
15,000).

The states are kept in the corpus itself, so it can be regenerated from them, byte for byte:

```bash
python3 -m training.generate_data.bot_corpus --states training/corpus/training_data_reference_15000.txt --output /tmp/check.txt
cmp /tmp/check.txt training/corpus/training_data_reference_15000.txt
```
