# suite_20261102_phase1_fixed_vsrandom: tournament games

tournament run, backend gpu; 1961 answers per model and condition; training corpus `training/corpus/training_data_synct_15000_llm.txt`; evaluated 2026-11-12 13:12. Shares in brackets are 95% Wilson intervals.

## Overview

| condition | model | answers | schema-valid | legal | reference-correct | accept gap useful−useless | avoidable harvests |
|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 663 | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| base_verbose | Qwen2.5-3B | 1259 | 100% [100–100] | 94% [92–95] | 41% [39–44] | -12 | 69% |
| base_verbose | gemma-2b | 986 | 99% [99–100] | 56% [53–60] | 19% [17–22] | +0 | 50% |
| lora_verbose | TinyLlama-1.1B | 1212 | 77% [75–80] | 88% [86–90] | 32% [30–35] | +0 | 63% |
| lora_verbose | Qwen2.5-3B | 1146 | 100% [100–100] | 70% [67–72] | 28% [26–31] | +0 | 30% |
| lora_verbose | gemma-2b | 1299 | 100% [99–100] | 87% [85–88] | 33% [30–35] | +0 | 49% |
| lora_compact | TinyLlama-1.1B | 1707 | 100% [100–100] | 98% [97–98] | 74% [72–76] | +38 | 0% |
| lora_compact | Qwen2.5-3B | 1485 | 100% [100–100] | 99% [99–99] | 77% [75–79] | +23 | 0% |
| lora_compact | gemma-2b | 1727 | 100% [100–100] | 95% [94–96] | 77% [75–79] | +41 | 0% |
| base_grammar | TinyLlama-1.1B | 1353 | 97% [96–98] | 83% [81–85] | 22% [20–24] | +0 | 63% |
| base_grammar | Qwen2.5-3B | 1961 | 100% [100–100] | 100% [99–100] | 54% [52–56] | +0 | 64% |
| base_grammar | gemma-2b | 1627 | 100% [100–100] | 83% [81–85] | 32% [30–35] | +53 | 60% |

## Schema validity (valid@1)

Is the whole answer one JSON value that matches its message type's schema, game/schemas/output/<phase>.schema.json?

| condition | model | valid | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | main failures |
|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 0/663 (0%) | 0% | 0% | 0% | 0% | – | not_json 663 |
| base_verbose | Qwen2.5-3B | 1259/1259 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_verbose | gemma-2b | 980/986 (99%) | 99% | 99% | 100% | 100% | 100% | schema:enum 6 |
| lora_verbose | TinyLlama-1.1B | 938/1212 (77%) | 100% | 100% | 0% | 100% | – | schema:additionalProperties 274 |
| lora_verbose | Qwen2.5-3B | 1146/1146 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_verbose | gemma-2b | 1296/1299 (100%) | 99% | 100% | 100% | 100% | 100% | schema:maxItems 3 |
| lora_compact | TinyLlama-1.1B | 1707/1707 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | Qwen2.5-3B | 1484/1485 (100%) | 100% | 100% | 100% | 100% | 100% | not_json 1 |
| lora_compact | gemma-2b | 1727/1727 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | TinyLlama-1.1B | 1308/1353 (97%) | 100% | 99% | 99% | 84% | 100% | not_json 45 |
| base_grammar | Qwen2.5-3B | 1961/1961 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | gemma-2b | 1627/1627 (100%) | 100% | 100% | 100% | 100% | 100% | – |

## Legality

Would the game carry out the answer as the model wrote it?

| condition | model | legal | valid & legal | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | why not legal |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 0/663 (0%) | 0% | 0% | 0% | 0% | 0% | – | no_json 663 |
| base_verbose | Qwen2.5-3B | 1178/1259 (94%) | 94% | 90% | 80% | 100% | 100% | 100% | rules 81 |
| base_verbose | gemma-2b | 557/986 (56%) | 56% | 30% | 36% | 100% | 78% | 85% | rules 361, cards_not_held 62, parser 6 |
| lora_verbose | TinyLlama-1.1B | 1068/1212 (88%) | 66% | 97% | 79% | 100% | 80% | – | rules 98, cards_not_held 46 |
| lora_verbose | Qwen2.5-3B | 799/1146 (70%) | 70% | 43% | 49% | 100% | 100% | 100% | rules 347 |
| lora_verbose | gemma-2b | 1125/1299 (87%) | 87% | 74% | 74% | 100% | 100% | 100% | rules 174 |
| lora_compact | TinyLlama-1.1B | 1669/1707 (98%) | 98% | 91% | 97% | 100% | 100% | 100% | rules 37, cards_not_held 1 |
| lora_compact | Qwen2.5-3B | 1472/1485 (99%) | 99% | 100% | 99% | 98% | 100% | 100% | cards_not_held 9, rules 3, no_json 1 |
| lora_compact | gemma-2b | 1646/1727 (95%) | 95% | 100% | 82% | 100% | 100% | 100% | rules 81 |
| base_grammar | TinyLlama-1.1B | 1129/1353 (83%) | 83% | 98% | 89% | 93% | 38% | 96% | cards_not_held 142, no_json 45, rules 37 |
| base_grammar | Qwen2.5-3B | 1956/1961 (100%) | 100% | 100% | 100% | 100% | 100% | 100% | cards_not_held 5 |
| base_grammar | gemma-2b | 1350/1627 (83%) | 83% | 100% | 86% | 82% | 52% | 91% | cards_not_held 223, rules 54 |

## Reference decisions

Does the answer make the decision a simple, value-aware rule set makes?

| condition | model | correct (95% CI) | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | teacher match |
|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 0% [0–1] | 0% | 0% | 0% | 0% | – | – |
| base_verbose | Qwen2.5-3B | 41% [39–44] | 17% | 5% | 75% | 77% | 7% | – |
| base_verbose | gemma-2b | 19% [17–22] | 12% | 9% | 76% | 10% | 6% | – |
| lora_verbose | TinyLlama-1.1B | 32% [30–35] | 17% | 5% | 100% | 21% | – | – |
| lora_verbose | Qwen2.5-3B | 28% [26–31] | 20% | 17% | 66% | 26% | 11% | – |
| lora_verbose | gemma-2b | 33% [30–35] | 17% | 16% | 76% | 27% | 10% | – |
| lora_compact | TinyLlama-1.1B | 74% [72–76] | 62% | 77% | 96% | 35% | 64% | – |
| lora_compact | Qwen2.5-3B | 77% [75–79] | 74% | 88% | 98% | 62% | 14% | – |
| lora_compact | gemma-2b | 77% [75–79] | 75% | 71% | 99% | 48% | 65% | – |
| base_grammar | TinyLlama-1.1B | 22% [20–24] | 7% | 22% | 50% | 0% | 10% | – |
| base_grammar | Qwen2.5-3B | 54% [52–56] | 12% | 1% | 65% | 70% | 88% | – |
| base_grammar | gemma-2b | 32% [30–35] | 11% | 6% | 56% | 12% | 74% | – |
| teacher | training corpus | 83% [83–84] | 88% | 99% | 97% | 70% | 62% | – |

Each rule on its own (partial credit):

| condition | model | PLANT: first card placed | PLANT: second card without harvest | FORCE: no avoidable harvest | FORCE: least valuable stack lost | TRADI: keeps growing beans | REPLY: accepts iff useful | REPLY: keeps growing beans | CONSI: accepts iff useful |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 0% | 0% | 0% | 0% | 0% | 0% | 0% | – |
| base_verbose | Qwen2.5-3B | 19% | 75% | 36% | 49% | 75% | 77% | 100% | 7% |
| base_verbose | gemma-2b | 13% | 28% | 16% | 29% | 76% | 21% | 64% | 6% |
| lora_verbose | TinyLlama-1.1B | 17% | 97% | 41% | 43% | 100% | 22% | 78% | – |
| lora_verbose | Qwen2.5-3B | 32% | 27% | 40% | 26% | 66% | 26% | 100% | 11% |
| lora_verbose | gemma-2b | 28% | 40% | 50% | 41% | 76% | 27% | 100% | 10% |
| lora_compact | TinyLlama-1.1B | 62% | 91% | 97% | 77% | 96% | 38% | 95% | 64% |
| lora_compact | Qwen2.5-3B | 74% | 100% | 99% | 88% | 98% | 68% | 93% | 14% |
| lora_compact | gemma-2b | 75% | 100% | 82% | 72% | 99% | 49% | 99% | 65% |
| base_grammar | TinyLlama-1.1B | 37% | 24% | 58% | 52% | 50% | 9% | 24% | 10% |
| base_grammar | Qwen2.5-3B | 20% | 20% | 59% | 42% | 65% | 70% | 100% | 88% |
| base_grammar | gemma-2b | 25% | 23% | 53% | 39% | 56% | 17% | 43% | 74% |
| teacher | training corpus | 89% | 99% | 100% | 100% | 97% | 75% | 95% | 62% |

## State sensitivity

Does the decision depend on the game state?

| condition | model | REPLY accepts useful / useless | gap | CONSIDERING accepts useful / useless | gap | PLANTING avoidable harvests | FORCED avoidable harvests | TRADING passes | offers giving away a growing bean |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | – / – | – | – / – | – | – | – | – | – |
| base_verbose | Qwen2.5-3B | 21% / 5% | +16 | 100% / 100% | +0 | 208/256 (81%) | 116/211 (55%) | 0% | 99/399 (25%) |
| base_verbose | gemma-2b | 100% / 100% | +0 | 100% / 100% | +0 | 41/92 (45%) | 48/86 (56%) | 0% | 34/141 (24%) |
| lora_verbose | TinyLlama-1.1B | 100% / 100% | +0 | – / – | – | 223/273 (82%) | 159/335 (47%) | 100% | – |
| lora_verbose | Qwen2.5-3B | 100% / 100% | +0 | 100% / 100% | +0 | 59/133 (44%) | 31/166 (19%) | 0% | 70/206 (34%) |
| lora_verbose | gemma-2b | 100% / 100% | +0 | 100% / 100% | +0 | 151/216 (70%) | 93/285 (33%) | 0% | 80/328 (24%) |
| lora_compact | TinyLlama-1.1B | 100% / 100% | +0 | 100% / 41% | +59 | 1/258 (0%) | 0/423 (0%) | 0% | 21/535 (4%) |
| lora_compact | Qwen2.5-3B | 100% / 54% | +46 | 100% / 98% | +2 | 0/280 (0%) | 0/400 (0%) | 0% | 0/433 (0%) |
| lora_compact | gemma-2b | 100% / 95% | +5 | 100% / 40% | +60 | 0/280 (0%) | 1/374 (0%) | 0% | 8/540 (1%) |
| base_grammar | TinyLlama-1.1B | 100% / 100% | +0 | 100% / 100% | +0 | 250/274 (91%) | 91/264 (34%) | 0% | 172/372 (46%) |
| base_grammar | Qwen2.5-3B | 0% / 0% | +0 | 0% / 0% | +0 | 246/280 (88%) | 115/280 (41%) | 0% | 256/727 (35%) |
| base_grammar | gemma-2b | 100% / 100% | +0 | 71% / 18% | +53 | 244/280 (87%) | 132/342 (39%) | 0% | 133/413 (32%) |
| teacher | training corpus | 100% / 41% | +59 | 100% / 45% | +55 | 26/3000 (1%) | 9/3000 (0%) | 23% | 132/2309 (6%) |

## Game outcomes

How many coins does a player earn against the same opponents and decks?

Opponents: two bot_random bots in every game.

| condition | player | finished games | coins per game [95% CI] | opponents' coins | wins | penalty per game |
|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 30/30 | 0.23 [0.07, 0.43] | 2.30 | 0% | 10.07 |
| base_verbose | Qwen2.5-3B | 30/30 | 1.70 [1.37, 2.07] | 2.02 | 10% | 2.73 |
| base_verbose | gemma-2b | 30/30 | 0.83 [0.57, 1.13] | 2.42 | 0% | 14.87 |
| lora_verbose | TinyLlama-1.1B | 30/30 | 1.87 [1.47, 2.30] | 1.78 | 23% | 4.80 |
| lora_verbose | Qwen2.5-3B | 30/30 | 1.63 [1.13, 2.17] | 2.12 | 13% | 11.97 |
| lora_verbose | gemma-2b | 30/30 | 1.73 [1.40, 2.10] | 2.22 | 13% | 5.93 |
| lora_compact | TinyLlama-1.1B | 30/30 | 5.13 [4.60, 5.70] | 2.33 | 73% | 1.27 |
| lora_compact | Qwen2.5-3B | 30/30 | 5.67 [5.17, 6.20] | 2.17 | 90% | 0.33 |
| lora_compact | gemma-2b | 30/30 | 5.67 [4.97, 6.33] | 2.30 | 73% | 2.67 |
| base_grammar | TinyLlama-1.1B | 30/30 | 2.23 [1.83, 2.63] | 2.48 | 20% | 5.73 |
| base_grammar | Qwen2.5-3B | 30/30 | 2.17 [1.77, 2.60] | 1.97 | 30% | 0.10 |
| base_grammar | gemma-2b | 30/30 | 2.63 [2.20, 3.10] | 2.05 | 37% | 8.57 |
| bot_random | bot_random | 30/30 | 2.40 [2.03, 2.80] | 1.97 | 37% | 0.00 |
| bot_reference | bot_reference | 30/30 | 5.57 [5.00, 6.13] | 2.27 | 83% | 0.00 |

Paired differences in coins per game from the baseline bots, on the same seeds and seats:

| condition | player | Δ coins vs reference bot [95% CI] | p | Holm p | Δ coins vs random bot [95% CI] | p | Holm p |
|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | -5.33 [-5.87, -4.80] | <0.001 | <0.001 | -2.17 [-2.60, -1.77] | <0.001 | <0.001 |
| base_verbose | Qwen2.5-3B | -3.87 [-4.50, -3.27] | <0.001 | <0.001 | -0.70 [-1.13, -0.27] | 0.005 | 0.044 |
| base_verbose | gemma-2b | -4.73 [-5.37, -4.13] | <0.001 | <0.001 | -1.57 [-2.10, -1.03] | <0.001 | 0.002 |
| lora_verbose | TinyLlama-1.1B | -3.70 [-4.33, -3.03] | <0.001 | <0.001 | -0.53 [-0.93, -0.17] | 0.015 | 0.102 |
| lora_verbose | Qwen2.5-3B | -3.93 [-4.67, -3.20] | <0.001 | <0.001 | -0.77 [-1.43, -0.07] | 0.039 | 0.193 |
| lora_verbose | gemma-2b | -3.83 [-4.53, -3.20] | <0.001 | <0.001 | -0.67 [-1.17, -0.20] | 0.019 | 0.115 |
| lora_compact | TinyLlama-1.1B | -0.43 [-1.13, +0.23] | 0.322 | 1.000 | +2.73 [+2.17, +3.33] | <0.001 | <0.001 |
| lora_compact | Qwen2.5-3B | +0.10 [-0.80, +0.93] | 0.758 | 1.000 | +3.27 [+2.67, +3.87] | <0.001 | <0.001 |
| lora_compact | gemma-2b | +0.10 [-0.77, +0.97] | 0.849 | 1.000 | +3.27 [+2.60, +3.90] | <0.001 | <0.001 |
| base_grammar | TinyLlama-1.1B | -3.33 [-4.13, -2.53] | <0.001 | <0.001 | -0.17 [-0.50, +0.20] | 0.252 | 0.755 |
| base_grammar | Qwen2.5-3B | -3.40 [-4.13, -2.70] | <0.001 | <0.001 | -0.23 [-0.67, +0.17] | 0.298 | 0.755 |
| base_grammar | gemma-2b | -2.93 [-3.67, -2.20] | <0.001 | <0.001 | +0.23 [-0.13, +0.60] | 0.166 | 0.665 |
| bot_random | bot_random | -3.17 [-3.90, -2.43] | <0.001 | <0.001 | – |  |  |
| bot_reference | bot_reference | – |  |  | +3.17 [+2.43, +3.90] | <0.001 | <0.001 |
| base_verbose | all models | -4.64 [-5.23, -4.11] | <0.001 | <0.001 | -1.48 [-1.89, -1.07] | <0.001 | <0.001 |
| lora_verbose | all models | -3.82 [-4.41, -3.26] | <0.001 | <0.001 | -0.66 [-1.06, -0.24] | 0.005 | 0.044 |
| lora_compact | all models | -0.08 [-0.76, +0.57] | 0.891 | 1.000 | +3.09 [+2.71, +3.50] | <0.001 | <0.001 |
| base_grammar | all models | -3.22 [-3.92, -2.53] | <0.001 | <0.001 | -0.06 [-0.36, +0.22] | 0.856 | 0.856 |


