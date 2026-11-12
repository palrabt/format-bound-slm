# suite_20261029_gen2: tournament games

tournament run, backend gpu; 1998 answers per model and condition; training corpus `training/corpus/training_data_synct_15000_llm.txt`; evaluated 2026-11-12 13:12. Shares in brackets are 95% Wilson intervals.

## Overview

| condition | model | answers | schema-valid | legal | reference-correct | accept gap useful−useless | avoidable harvests |
|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 1271 | 52% [50–55] | 92% [91–94] | 44% [41–47] | -46 | 82% |
| base_verbose | granite-4.2-3b | 945 | 100% [100–100] | 98% [97–99] | 46% [43–50] | – | 86% |
| base_verbose | gemma-4-E2B | 1778 | 100% [100–100] | 98% [98–99] | 59% [56–61] | +79 | 66% |
| lora_verbose | LFM2.5-1.2B | 1276 | 100% [100–100] | 100% [99–100] | 50% [48–53] | -11 | 79% |
| lora_verbose | granite-4.2-3b | 1325 | 100% [100–100] | 96% [95–97] | 74% [72–77] | +19 | 17% |
| lora_verbose | gemma-4-E2B | 1223 | 100% [100–100] | 84% [81–86] | 57% [54–59] | +71 | 23% |
| lora_compact | LFM2.5-1.2B | 1606 | 100% [100–100] | 99% [98–99] | 83% [81–84] | +0 | 1% |
| lora_compact | granite-4.2-3b | 1998 | 100% [100–100] | 99% [98–99] | 91% [90–92] | +100 | 2% |
| lora_compact | gemma-4-E2B | 1554 | 100% [100–100] | 100% [100–100] | 84% [82–85] | +0 | 3% |
| base_grammar | LFM2.5-1.2B | 1288 | 97% [96–98] | 80% [77–82] | 23% [21–26] | +0 | 61% |
| base_grammar | granite-4.2-3b | 1030 | 100% [100–100] | 100% [99–100] | 33% [30–36] | – | 64% |
| base_grammar | gemma-4-E2B | 1931 | 100% [100–100] | 90% [89–91] | 47% [45–49] | +73 | 64% |

## Schema validity (valid@1)

Is the whole answer one JSON value that matches its message type's schema, game/schemas/output/<phase>.schema.json?

| condition | model | valid | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | main failures |
|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 665/1271 (52%) | 96% | 97% | 5% | 30% | 29% | wrapped 581, schema:enum 22, not_json 3 |
| base_verbose | granite-4.2-3b | 945/945 (100%) | 100% | 100% | 100% | 100% | – | – |
| base_verbose | gemma-4-E2B | 1777/1778 (100%) | 100% | 100% | 100% | 100% | 100% | schema:maxItems 1 |
| lora_verbose | LFM2.5-1.2B | 1276/1276 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_verbose | granite-4.2-3b | 1325/1325 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_verbose | gemma-4-E2B | 1223/1223 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | LFM2.5-1.2B | 1604/1606 (100%) | 100% | 100% | 100% | 100% | 100% | schema:enum 2 |
| lora_compact | granite-4.2-3b | 1998/1998 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | gemma-4-E2B | 1554/1554 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | LFM2.5-1.2B | 1252/1288 (97%) | 98% | 100% | 92% | 100% | 100% | schema:minItems 30, schema:maxItems 6 |
| base_grammar | granite-4.2-3b | 1030/1030 (100%) | 100% | 100% | 100% | 100% | – | – |
| base_grammar | gemma-4-E2B | 1931/1931 (100%) | 100% | 100% | 100% | 100% | 100% | – |

## Legality

Would the game carry out the answer as the model wrote it?

| condition | model | legal | valid & legal | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | why not legal |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 1172/1271 (92%) | 49% | 93% | 86% | 100% | 95% | 65% | rules 44, cards_not_held 30, parser 22, no_json 3 |
| base_verbose | granite-4.2-3b | 924/945 (98%) | 98% | 98% | 94% | 100% | 100% | – | rules 21 |
| base_verbose | gemma-4-E2B | 1751/1778 (98%) | 98% | 95% | 97% | 100% | 100% | 99% | rules 23, cards_not_held 4 |
| lora_verbose | LFM2.5-1.2B | 1272/1276 (100%) | 100% | 100% | 99% | 100% | 100% | 100% | rules 4 |
| lora_verbose | granite-4.2-3b | 1276/1325 (96%) | 96% | 88% | 94% | 100% | 100% | 100% | rules 49 |
| lora_verbose | gemma-4-E2B | 1023/1223 (84%) | 84% | 48% | 70% | 100% | 100% | 100% | rules 200 |
| lora_compact | LFM2.5-1.2B | 1587/1606 (99%) | 99% | 99% | 96% | 100% | 100% | 100% | rules 17, parser 2 |
| lora_compact | granite-4.2-3b | 1975/1998 (99%) | 99% | 100% | 96% | 100% | 100% | 100% | rules 20, cards_not_held 3 |
| lora_compact | gemma-4-E2B | 1552/1554 (100%) | 100% | 100% | 100% | 100% | 100% | 100% | rules 2 |
| base_grammar | LFM2.5-1.2B | 1026/1288 (80%) | 80% | 89% | 90% | 87% | 49% | 51% | cards_not_held 170, rules 62, no_cards 30 |
| base_grammar | granite-4.2-3b | 1028/1030 (100%) | 100% | 100% | 100% | 100% | 99% | – | cards_not_held 2 |
| base_grammar | gemma-4-E2B | 1739/1931 (90%) | 90% | 100% | 92% | 100% | 86% | 66% | cards_not_held 164, rules 28 |

## Reference decisions

Does the answer make the decision a simple, value-aware rule set makes?

| condition | model | correct (95% CI) | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | teacher match |
|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 44% [41–47] | 20% | 11% | 89% | 38% | 9% | – |
| base_verbose | granite-4.2-3b | 46% [43–50] | 21% | 1% | 100% | 89% | – | – |
| base_verbose | gemma-4-E2B | 59% [56–61] | 15% | 4% | 73% | 99% | 85% | – |
| lora_verbose | LFM2.5-1.2B | 50% [48–53] | 20% | 8% | 90% | 87% | 14% | – |
| lora_verbose | granite-4.2-3b | 74% [72–77] | 45% | 63% | 96% | 100% | 39% | – |
| lora_verbose | gemma-4-E2B | 57% [54–59] | 21% | 22% | 71% | 86% | 76% | – |
| lora_compact | LFM2.5-1.2B | 83% [81–84] | 70% | 84% | 99% | 95% | 29% | – |
| lora_compact | granite-4.2-3b | 91% [90–92] | 75% | 90% | 99% | 82% | 100% | – |
| lora_compact | gemma-4-E2B | 84% [82–85] | 71% | 90% | 100% | 88% | 28% | – |
| base_grammar | LFM2.5-1.2B | 23% [21–26] | 12% | 13% | 53% | 10% | 3% | – |
| base_grammar | granite-4.2-3b | 33% [30–36] | 12% | 8% | 100% | 0% | – | – |
| base_grammar | gemma-4-E2B | 47% [45–49] | 14% | 9% | 77% | 38% | 54% | – |
| teacher | training corpus | 83% [83–84] | 88% | 99% | 97% | 70% | 62% | – |

Each rule on its own (partial credit):

| condition | model | PLANT: first card placed | PLANT: second card without harvest | FORCE: no avoidable harvest | FORCE: least valuable stack lost | TRADI: keeps growing beans | REPLY: accepts iff useful | REPLY: keeps growing beans | CONSI: accepts iff useful |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 20% | 92% | 12% | 84% | 89% | 49% | 63% | 9% |
| base_verbose | granite-4.2-3b | 21% | 98% | 7% | 88% | 100% | 89% | 97% | – |
| base_verbose | gemma-4-E2B | 17% | 72% | 52% | 48% | 73% | 99% | 100% | 85% |
| lora_verbose | LFM2.5-1.2B | 21% | 99% | 22% | 84% | 90% | 87% | 100% | 14% |
| lora_verbose | granite-4.2-3b | 62% | 58% | 93% | 64% | 96% | 100% | 100% | 39% |
| lora_verbose | gemma-4-E2B | 28% | 36% | 66% | 26% | 71% | 86% | 97% | 76% |
| lora_compact | LFM2.5-1.2B | 71% | 98% | 95% | 85% | 99% | 100% | 95% | 29% |
| lora_compact | granite-4.2-3b | 78% | 95% | 96% | 90% | 99% | 100% | 82% | 100% |
| lora_compact | gemma-4-E2B | 75% | 95% | 99% | 91% | 100% | 100% | 88% | 28% |
| base_grammar | LFM2.5-1.2B | 24% | 21% | 54% | 50% | 53% | 49% | 10% | 3% |
| base_grammar | granite-4.2-3b | 24% | 25% | 59% | 49% | 100% | 1% | 70% | – |
| base_grammar | gemma-4-E2B | 26% | 26% | 51% | 49% | 77% | 81% | 42% | 54% |
| teacher | training corpus | 89% | 99% | 100% | 100% | 97% | 75% | 95% | 62% |

## State sensitivity

Does the decision depend on the game state?

| condition | model | REPLY accepts useful / useless | gap | CONSIDERING accepts useful / useless | gap | PLANTING avoidable harvests | FORCED avoidable harvests | TRADING passes | offers giving away a growing bean |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 51% / – | – | 100% / 100% | +0 | 204/261 (78%) | 238/278 (86%) | 0% | 53/473 (11%) |
| base_verbose | granite-4.2-3b | 89% / – | – | – / – | – | 217/275 (79%) | 240/259 (93%) | 100% | – |
| base_verbose | gemma-4-E2B | 99% / – | – | 2% / 1% | +1 | 226/267 (85%) | 120/261 (46%) | 0% | 183/689 (27%) |
| lora_verbose | LFM2.5-1.2B | 87% / – | – | 100% / 100% | +0 | 222/280 (79%) | 215/276 (78%) | 0% | 52/509 (10%) |
| lora_verbose | granite-4.2-3b | 100% / – | – | 100% / 81% | +19 | 82/249 (33%) | 2/234 (1%) | 0% | 16/413 (4%) |
| lora_verbose | gemma-4-E2B | 86% / – | – | 0% / 0% | +0 | 52/144 (36%) | 5/101 (5%) | 9% | 97/308 (31%) |
| lora_compact | LFM2.5-1.2B | 100% / – | – | 100% / 100% | +0 | 5/279 (2%) | 4/439 (1%) | 0% | 8/454 (2%) |
| lora_compact | granite-4.2-3b | 100% / – | – | 100% / 0% | +100 | 15/280 (5%) | 0/439 (0%) | 0% | 5/633 (1%) |
| lora_compact | gemma-4-E2B | 100% / – | – | 100% / 100% | +0 | 14/279 (5%) | 4/418 (1%) | 0% | 0/455 (0%) |
| base_grammar | LFM2.5-1.2B | 100% / – | – | 100% / 100% | +0 | 214/252 (85%) | 119/292 (41%) | 0% | 132/334 (40%) |
| base_grammar | granite-4.2-3b | 1% / – | – | – / – | – | 242/280 (86%) | 116/281 (41%) | 100% | – |
| base_grammar | gemma-4-E2B | 94% / – | – | 0% / 0% | +0 | 240/280 (86%) | 139/315 (44%) | 0% | 164/716 (23%) |
| teacher | training corpus | 100% / 41% | +59 | 100% / 45% | +55 | 26/3000 (1%) | 9/3000 (0%) | 23% | 132/2309 (6%) |

## Game outcomes

How many coins does a player earn against the same opponents and decks?

Opponents: two bot_reference bots in every game.

| condition | player | finished games | coins per game [95% CI] | opponents' coins | wins | penalty per game |
|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 30/30 | 2.60 [1.97, 3.23] | 9.15 | 0% | 1.97 |
| base_verbose | granite-4.2-3b | 30/30 | 1.57 [1.23, 1.90] | 7.67 | 0% | 0.67 |
| base_verbose | gemma-4-E2B | 30/30 | 1.83 [1.43, 2.30] | 7.32 | 0% | 0.70 |
| lora_verbose | LFM2.5-1.2B | 30/30 | 2.47 [2.03, 2.97] | 8.78 | 0% | 0.13 |
| lora_verbose | granite-4.2-3b | 30/30 | 4.00 [3.47, 4.53] | 7.90 | 0% | 1.60 |
| lora_verbose | gemma-4-E2B | 30/30 | 1.40 [0.97, 1.90] | 7.35 | 0% | 6.57 |
| lora_compact | LFM2.5-1.2B | 30/30 | 8.73 [7.83, 9.60] | 8.95 | 30% | 0.57 |
| lora_compact | granite-4.2-3b | 30/30 | 8.40 [7.37, 9.47] | 8.23 | 40% | 0.73 |
| lora_compact | gemma-4-E2B | 30/30 | 7.93 [7.03, 8.83] | 9.35 | 23% | 0.07 |
| base_grammar | LFM2.5-1.2B | 30/30 | 2.77 [2.27, 3.33] | 9.05 | 0% | 6.30 |
| base_grammar | granite-4.2-3b | 30/30 | 2.53 [2.07, 3.00] | 7.40 | 0% | 0.07 |
| base_grammar | gemma-4-E2B | 30/30 | 3.10 [2.57, 3.73] | 7.57 | 3% | 1.83 |
| bot_random | bot_random | 30/30 | 2.20 [1.80, 2.60] | 7.43 | 0% | 0.00 |
| bot_reference | bot_reference | 30/30 | 8.33 [7.43, 9.20] | 8.63 | 23% | 0.00 |

Paired differences in coins per game from the baseline bots, on the same seeds and seats:

| condition | player | Δ coins vs reference bot [95% CI] | p | Holm p | Δ coins vs random bot [95% CI] | p | Holm p |
|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | -5.73 [-6.70, -4.80] | <0.001 | <0.001 | +0.40 [-0.30, +1.17] | 0.332 | 0.722 |
| base_verbose | granite-4.2-3b | -6.77 [-7.67, -5.73] | <0.001 | <0.001 | -0.63 [-1.00, -0.27] | 0.005 | 0.056 |
| base_verbose | gemma-4-E2B | -6.50 [-7.50, -5.43] | <0.001 | <0.001 | -0.37 [-0.77, +0.00] | 0.071 | 0.424 |
| lora_verbose | LFM2.5-1.2B | -5.87 [-6.77, -4.90] | <0.001 | <0.001 | +0.27 [-0.10, +0.63] | 0.241 | 0.722 |
| lora_verbose | granite-4.2-3b | -4.33 [-5.27, -3.33] | <0.001 | <0.001 | +1.80 [+1.20, +2.43] | <0.001 | <0.001 |
| lora_verbose | gemma-4-E2B | -6.93 [-7.90, -5.93] | <0.001 | <0.001 | -0.80 [-1.33, -0.30] | 0.007 | 0.069 |
| lora_compact | LFM2.5-1.2B | +0.40 [-0.63, +1.43] | 0.444 | 1.000 | +6.53 [+5.70, +7.40] | <0.001 | <0.001 |
| lora_compact | granite-4.2-3b | +0.07 [-1.30, +1.47] | 0.909 | 1.000 | +6.20 [+5.23, +7.27] | <0.001 | <0.001 |
| lora_compact | gemma-4-E2B | -0.40 [-1.53, +0.83] | 0.604 | 1.000 | +5.73 [+4.87, +6.60] | <0.001 | <0.001 |
| base_grammar | LFM2.5-1.2B | -5.57 [-6.57, -4.53] | <0.001 | <0.001 | +0.57 [+0.03, +1.10] | 0.071 | 0.424 |
| base_grammar | granite-4.2-3b | -5.80 [-6.70, -4.90] | <0.001 | <0.001 | +0.33 [-0.10, +0.80] | 0.165 | 0.660 |
| base_grammar | gemma-4-E2B | -5.23 [-6.23, -4.27] | <0.001 | <0.001 | +0.90 [+0.27, +1.63] | 0.011 | 0.100 |
| bot_random | bot_random | -6.13 [-7.10, -5.10] | <0.001 | <0.001 | – |  |  |
| bot_reference | bot_reference | – |  |  | +6.13 [+5.10, +7.10] | <0.001 | <0.001 |
| base_verbose | all models | -6.33 [-7.26, -5.37] | <0.001 | <0.001 | -0.20 [-0.61, +0.20] | 0.391 | 0.722 |
| lora_verbose | all models | -5.71 [-6.54, -4.78] | <0.001 | <0.001 | +0.42 [+0.09, +0.77] | 0.039 | 0.274 |
| lora_compact | all models | +0.02 [-1.06, +1.10] | 0.770 | 1.000 | +6.16 [+5.47, +6.87] | <0.001 | <0.001 |
| base_grammar | all models | -5.53 [-6.43, -4.64] | <0.001 | <0.001 | +0.60 [+0.19, +1.06] | 0.017 | 0.134 |


