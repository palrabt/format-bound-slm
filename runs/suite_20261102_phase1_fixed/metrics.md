# suite_20261102_phase1_fixed: tournament games

tournament run, backend gpu; 1863 answers per model and condition; training corpus `training/corpus/training_data_synct_15000_llm.txt`; evaluated 2026-11-12 13:12. Shares in brackets are 95% Wilson intervals.

## Overview

| condition | model | answers | schema-valid | legal | reference-correct | accept gap useful−useless | avoidable harvests |
|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 546 | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| base_verbose | Qwen2.5-3B | 1224 | 100% [100–100] | 94% [93–95] | 42% [39–44] | -41 | 67% |
| base_verbose | gemma-2b | 744 | 100% [99–100] | 57% [54–61] | 25% [22–29] | +0 | 51% |
| lora_verbose | TinyLlama-1.1B | 1026 | 74% [71–77] | 96% [95–97] | 50% [47–53] | +0 | 63% |
| lora_verbose | Qwen2.5-3B | 798 | 100% [100–100] | 70% [67–73] | 47% [44–51] | +0 | 32% |
| lora_verbose | gemma-2b | 1076 | 100% [99–100] | 89% [87–91] | 48% [45–51] | +0 | 49% |
| lora_compact | TinyLlama-1.1B | 1582 | 100% [100–100] | 98% [97–98] | 78% [76–80] | +0 | 0% |
| lora_compact | Qwen2.5-3B | 1489 | 100% [100–100] | 99% [98–99] | 82% [80–84] | +0 | 0% |
| lora_compact | gemma-2b | 1573 | 100% [100–100] | 95% [94–96] | 81% [79–83] | +0 | 0% |
| base_grammar | TinyLlama-1.1B | 1290 | 96% [94–97] | 85% [83–87] | 22% [19–24] | +0 | 62% |
| base_grammar | Qwen2.5-3B | 1863 | 100% [100–100] | 100% [99–100] | 46% [44–48] | +0 | 64% |
| base_grammar | gemma-2b | 1473 | 100% [100–100] | 83% [81–85] | 33% [31–36] | +68 | 65% |

## Schema validity (valid@1)

Is the whole answer one JSON value that matches its message type's schema, game/schemas/output/<phase>.schema.json?

| condition | model | valid | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | main failures |
|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 0/546 (0%) | 0% | 0% | 0% | 0% | – | not_json 546 |
| base_verbose | Qwen2.5-3B | 1224/1224 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_verbose | gemma-2b | 743/744 (100%) | 100% | 99% | 100% | 100% | 100% | schema:enum 1 |
| lora_verbose | TinyLlama-1.1B | 760/1026 (74%) | 100% | 100% | 3% | 100% | 100% | schema:additionalProperties 266 |
| lora_verbose | Qwen2.5-3B | 798/798 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_verbose | gemma-2b | 1075/1076 (100%) | 100% | 100% | 100% | 100% | 100% | schema:maxItems 1 |
| lora_compact | TinyLlama-1.1B | 1582/1582 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | Qwen2.5-3B | 1487/1489 (100%) | 100% | 100% | 100% | 99% | 100% | not_json 2 |
| lora_compact | gemma-2b | 1573/1573 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | TinyLlama-1.1B | 1232/1290 (96%) | 100% | 100% | 95% | 81% | 100% | not_json 58 |
| base_grammar | Qwen2.5-3B | 1863/1863 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | gemma-2b | 1473/1473 (100%) | 100% | 100% | 100% | 100% | 100% | – |

## Legality

Would the game carry out the answer as the model wrote it?

| condition | model | legal | valid & legal | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | why not legal |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 0/546 (0%) | 0% | 0% | 0% | 0% | 0% | – | no_json 546 |
| base_verbose | Qwen2.5-3B | 1152/1224 (94%) | 94% | 88% | 85% | 100% | 100% | 100% | rules 72 |
| base_verbose | gemma-2b | 426/744 (57%) | 57% | 22% | 56% | 100% | 82% | 100% | rules 279, cards_not_held 38, parser 1 |
| lora_verbose | TinyLlama-1.1B | 986/1026 (96%) | 70% | 97% | 92% | 100% | 96% | 100% | rules 31, cards_not_held 9 |
| lora_verbose | Qwen2.5-3B | 561/798 (70%) | 70% | 32% | 73% | 100% | 100% | 100% | rules 237 |
| lora_verbose | gemma-2b | 958/1076 (89%) | 89% | 65% | 92% | 100% | 100% | 100% | rules 118 |
| lora_compact | TinyLlama-1.1B | 1548/1582 (98%) | 98% | 92% | 98% | 100% | 100% | 100% | rules 34 |
| lora_compact | Qwen2.5-3B | 1472/1489 (99%) | 99% | 99% | 100% | 97% | 99% | 100% | cards_not_held 11, rules 4, no_json 2 |
| lora_compact | gemma-2b | 1499/1573 (95%) | 95% | 100% | 84% | 100% | 100% | 100% | rules 74 |
| base_grammar | TinyLlama-1.1B | 1092/1290 (85%) | 85% | 100% | 99% | 84% | 39% | 95% | cards_not_held 135, no_json 58, rules 5 |
| base_grammar | Qwen2.5-3B | 1859/1863 (100%) | 100% | 100% | 100% | 99% | 100% | 100% | cards_not_held 4 |
| base_grammar | gemma-2b | 1229/1473 (83%) | 83% | 100% | 90% | 75% | 74% | 77% | cards_not_held 209, rules 35 |

## Reference decisions

Does the answer make the decision a simple, value-aware rule set makes?

| condition | model | correct (95% CI) | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | teacher match |
|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 0% [0–1] | 0% | 0% | 0% | 0% | – | – |
| base_verbose | Qwen2.5-3B | 42% [39–44] | 16% | 0% | 80% | 56% | 15% | – |
| base_verbose | gemma-2b | 25% [22–29] | 12% | 6% | 79% | 21% | 19% | – |
| lora_verbose | TinyLlama-1.1B | 50% [47–53] | 17% | 6% | 98% | 93% | 0% | – |
| lora_verbose | Qwen2.5-3B | 47% [44–51] | 15% | 21% | 66% | 100% | 17% | – |
| lora_verbose | gemma-2b | 48% [45–51] | 15% | 6% | 77% | 100% | 8% | – |
| lora_compact | TinyLlama-1.1B | 78% [76–80] | 62% | 82% | 93% | 83% | 32% | – |
| lora_compact | Qwen2.5-3B | 82% [80–84] | 76% | 93% | 97% | 71% | 32% | – |
| lora_compact | gemma-2b | 81% [79–83] | 73% | 74% | 100% | 96% | 30% | – |
| base_grammar | TinyLlama-1.1B | 22% [19–24] | 7% | 16% | 49% | 1% | 17% | – |
| base_grammar | Qwen2.5-3B | 46% [44–48] | 12% | 1% | 67% | 0% | 85% | – |
| base_grammar | gemma-2b | 33% [31–36] | 14% | 8% | 48% | 58% | 51% | – |
| teacher | training corpus | 83% [83–84] | 88% | 99% | 97% | 70% | 62% | – |

Each rule on its own (partial credit):

| condition | model | PLANT: first card placed | PLANT: second card without harvest | FORCE: no avoidable harvest | FORCE: least valuable stack lost | TRADI: keeps growing beans | REPLY: accepts iff useful | REPLY: keeps growing beans | CONSI: accepts iff useful |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 0% | 0% | 0% | 0% | 0% | 0% | 0% | – |
| base_verbose | Qwen2.5-3B | 17% | 70% | 43% | 43% | 80% | 56% | 100% | 15% |
| base_verbose | gemma-2b | 13% | 20% | 15% | 48% | 79% | 82% | 21% | 19% |
| lora_verbose | TinyLlama-1.1B | 17% | 97% | 51% | 47% | 98% | 96% | 93% | 0% |
| lora_verbose | Qwen2.5-3B | 20% | 22% | 59% | 35% | 66% | 100% | 100% | 17% |
| lora_verbose | gemma-2b | 23% | 37% | 68% | 30% | 77% | 100% | 100% | 8% |
| lora_compact | TinyLlama-1.1B | 63% | 91% | 98% | 82% | 93% | 100% | 83% | 32% |
| lora_compact | Qwen2.5-3B | 76% | 99% | 100% | 93% | 97% | 99% | 71% | 32% |
| lora_compact | gemma-2b | 73% | 100% | 83% | 74% | 100% | 100% | 96% | 30% |
| base_grammar | TinyLlama-1.1B | 43% | 21% | 65% | 49% | 49% | 39% | 1% | 17% |
| base_grammar | Qwen2.5-3B | 20% | 21% | 59% | 42% | 67% | 0% | 100% | 85% |
| base_grammar | gemma-2b | 26% | 23% | 49% | 49% | 48% | 74% | 58% | 51% |
| teacher | training corpus | 89% | 99% | 100% | 100% | 97% | 75% | 95% | 62% |

## State sensitivity

Does the decision depend on the game state?

| condition | model | REPLY accepts useful / useless | gap | CONSIDERING accepts useful / useless | gap | PLANTING avoidable harvests | FORCED avoidable harvests | TRADING passes | offers giving away a growing bean |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | – / – | – | – / – | – | – | – | – | – |
| base_verbose | Qwen2.5-3B | 56% / – | – | 100% / 100% | +0 | 205/249 (82%) | 106/213 (50%) | 0% | 87/439 (20%) |
| base_verbose | gemma-2b | 100% / – | – | 100% / 100% | +0 | 25/68 (37%) | 33/45 (73%) | 0% | 26/124 (21%) |
| lora_verbose | TinyLlama-1.1B | 100% / – | – | – / 100% | – | 221/272 (81%) | 111/252 (44%) | 97% | 4/8 (50%) |
| lora_verbose | Qwen2.5-3B | 100% / – | – | 100% / 100% | +0 | 41/99 (41%) | 14/74 (19%) | 0% | 60/178 (34%) |
| lora_verbose | gemma-2b | 100% / – | – | 100% / 100% | +0 | 133/191 (70%) | 47/177 (27%) | 0% | 77/333 (23%) |
| lora_compact | TinyLlama-1.1B | 100% / – | – | 100% / 100% | +0 | 2/259 (1%) | 0/418 (0%) | 0% | 34/489 (7%) |
| lora_compact | Qwen2.5-3B | 100% / – | – | 100% / 100% | +0 | 0/277 (0%) | 0/379 (0%) | 0% | 2/427 (0%) |
| lora_compact | gemma-2b | 100% / – | – | 100% / 100% | +0 | 0/280 (0%) | 1/376 (0%) | 0% | 1/441 (0%) |
| base_grammar | TinyLlama-1.1B | 100% / – | – | 100% / 100% | +0 | 251/279 (90%) | 96/285 (34%) | 0% | 135/324 (42%) |
| base_grammar | Qwen2.5-3B | 0% / – | – | 0% / 0% | +0 | 246/280 (88%) | 115/280 (41%) | 0% | 240/739 (32%) |
| base_grammar | gemma-2b | 100% / – | – | 17% / 17% | -0 | 241/280 (86%) | 148/323 (46%) | 0% | 134/373 (36%) |
| teacher | training corpus | 100% / 41% | +59 | 100% / 45% | +55 | 26/3000 (1%) | 9/3000 (0%) | 23% | 132/2309 (6%) |

## Game outcomes

How many coins does a player earn against the same opponents and decks?

Opponents: two bot_reference bots in every game.

| condition | player | finished games | coins per game [95% CI] | opponents' coins | wins | penalty per game |
|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 30/30 | 0.23 [0.07, 0.43] | 8.35 | 0% | 10.07 |
| base_verbose | Qwen2.5-3B | 30/30 | 1.87 [1.47, 2.27] | 8.00 | 0% | 2.23 |
| base_verbose | gemma-2b | 30/30 | 0.57 [0.30, 0.87] | 7.98 | 0% | 10.73 |
| lora_verbose | TinyLlama-1.1B | 30/30 | 1.60 [1.17, 2.07] | 7.17 | 0% | 1.30 |
| lora_verbose | Qwen2.5-3B | 30/30 | 1.13 [0.73, 1.60] | 8.75 | 0% | 7.90 |
| lora_verbose | gemma-2b | 30/30 | 1.70 [1.20, 2.20] | 7.80 | 0% | 3.90 |
| lora_compact | TinyLlama-1.1B | 30/30 | 7.53 [6.40, 8.70] | 10.25 | 13% | 1.13 |
| lora_compact | Qwen2.5-3B | 30/30 | 7.57 [6.77, 8.40] | 8.92 | 7% | 0.40 |
| lora_compact | gemma-2b | 30/30 | 7.87 [7.00, 8.73] | 9.68 | 10% | 2.47 |
| base_grammar | TinyLlama-1.1B | 30/30 | 2.93 [2.43, 3.43] | 8.70 | 0% | 4.40 |
| base_grammar | Qwen2.5-3B | 30/30 | 2.20 [1.80, 2.63] | 7.25 | 0% | 0.13 |
| base_grammar | gemma-2b | 30/30 | 3.53 [3.00, 4.07] | 7.72 | 0% | 6.97 |
| bot_random | bot_random | 30/30 | 2.20 [1.80, 2.60] | 7.43 | 0% | 0.00 |
| bot_reference | bot_reference | 30/30 | 8.33 [7.43, 9.20] | 8.63 | 23% | 0.00 |

Paired differences in coins per game from the baseline bots, on the same seeds and seats:

| condition | player | Δ coins vs reference bot [95% CI] | p | Holm p | Δ coins vs random bot [95% CI] | p | Holm p |
|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | -8.10 [-8.93, -7.20] | <0.001 | <0.001 | -1.97 [-2.37, -1.57] | <0.001 | <0.001 |
| base_verbose | Qwen2.5-3B | -6.47 [-7.43, -5.50] | <0.001 | <0.001 | -0.33 [-0.70, +0.03] | 0.104 | 0.313 |
| base_verbose | gemma-2b | -7.77 [-8.63, -6.87] | <0.001 | <0.001 | -1.63 [-2.10, -1.17] | <0.001 | <0.001 |
| lora_verbose | TinyLlama-1.1B | -6.73 [-7.67, -5.70] | <0.001 | <0.001 | -0.60 [-1.03, -0.23] | 0.007 | 0.031 |
| lora_verbose | Qwen2.5-3B | -7.20 [-8.10, -6.27] | <0.001 | <0.001 | -1.07 [-1.63, -0.47] | 0.002 | 0.015 |
| lora_verbose | gemma-2b | -6.63 [-7.73, -5.47] | <0.001 | <0.001 | -0.50 [-1.13, +0.10] | 0.143 | 0.313 |
| lora_compact | TinyLlama-1.1B | -0.80 [-2.13, +0.43] | 0.251 | 1.000 | +5.33 [+4.20, +6.43] | <0.001 | <0.001 |
| lora_compact | Qwen2.5-3B | -0.77 [-2.00, +0.47] | 0.357 | 1.000 | +5.37 [+4.60, +6.17] | <0.001 | <0.001 |
| lora_compact | gemma-2b | -0.47 [-1.63, +0.73] | 0.452 | 1.000 | +5.67 [+4.87, +6.47] | <0.001 | <0.001 |
| base_grammar | TinyLlama-1.1B | -5.40 [-6.57, -4.23] | <0.001 | <0.001 | +0.73 [+0.30, +1.17] | 0.005 | 0.031 |
| base_grammar | Qwen2.5-3B | -6.13 [-7.10, -5.10] | <0.001 | <0.001 | +0.00 [-0.40, +0.40] | 1.000 | 1.000 |
| base_grammar | gemma-2b | -4.80 [-5.77, -3.80] | <0.001 | <0.001 | +1.33 [+0.80, +1.90] | <0.001 | 0.002 |
| bot_random | bot_random | -6.13 [-7.10, -5.10] | <0.001 | <0.001 | – |  |  |
| bot_reference | bot_reference | – |  |  | +6.13 [+5.10, +7.10] | <0.001 | <0.001 |
| base_verbose | all models | -7.44 [-8.29, -6.54] | <0.001 | <0.001 | -1.31 [-1.66, -0.99] | <0.001 | <0.001 |
| lora_verbose | all models | -6.86 [-7.78, -5.88] | <0.001 | <0.001 | -0.72 [-1.16, -0.31] | 0.006 | 0.031 |
| lora_compact | all models | -0.68 [-1.69, +0.34] | 0.274 | 1.000 | +5.46 [+4.86, +6.06] | <0.001 | <0.001 |
| base_grammar | all models | -5.44 [-6.41, -4.43] | <0.001 | <0.001 | +0.69 [+0.36, +1.03] | 0.002 | 0.015 |


