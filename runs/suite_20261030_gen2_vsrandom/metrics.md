# suite_20261030_gen2_vsrandom: tournament games

tournament run, backend gpu; 1939 answers per model and condition; training corpus `training/corpus/training_data_synct_15000_llm.txt`; evaluated 2026-11-12 13:12. Shares in brackets are 95% Wilson intervals.

## Overview

| condition | model | answers | schema-valid | legal | reference-correct | accept gap useful−useless | avoidable harvests |
|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 1390 | 54% [52–57] | 95% [94–96] | 44% [42–47] | -15 | 85% |
| base_verbose | granite-4.2-3b | 1067 | 100% [100–100] | 97% [95–98] | 46% [43–49] | +4 | 85% |
| base_verbose | gemma-4-E2B | 1843 | 100% [99–100] | 96% [95–97] | 53% [51–55] | +31 | 64% |
| lora_verbose | LFM2.5-1.2B | 1696 | 100% [100–100] | 97% [96–98] | 53% [50–55] | +51 | 84% |
| lora_verbose | granite-4.2-3b | 1435 | 100% [99–100] | 96% [94–96] | 72% [70–75] | +57 | 15% |
| lora_verbose | gemma-4-E2B | 1320 | 100% [100–100] | 86% [84–88] | 57% [54–59] | +5 | 22% |
| lora_compact | LFM2.5-1.2B | 1735 | 100% [100–100] | 99% [98–99] | 86% [84–87] | +83 | 1% |
| lora_compact | granite-4.2-3b | 1939 | 100% [100–100] | 100% [99–100] | 93% [92–94] | +100 | 3% |
| lora_compact | gemma-4-E2B | 1820 | 100% [100–100] | 100% [100–100] | 81% [79–83] | +50 | 2% |
| base_grammar | LFM2.5-1.2B | 1334 | 99% [98–99] | 82% [80–84] | 24% [21–26] | +1 | 56% |
| base_grammar | granite-4.2-3b | 1090 | 100% [100–100] | 99% [99–100] | 39% [36–42] | +0 | 65% |
| base_grammar | gemma-4-E2B | 1934 | 100% [100–100] | 97% [96–98] | 56% [54–58] | +11 | 63% |

## Schema validity (valid@1)

Is the whole answer one JSON value that matches its message type's schema, game/schemas/output/<phase>.schema.json?

| condition | model | valid | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | main failures |
|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 756/1390 (54%) | 98% | 96% | 11% | 56% | 3% | wrapped 617, schema:enum 17 |
| base_verbose | granite-4.2-3b | 1067/1067 (100%) | 100% | 100% | 100% | 100% | – | – |
| base_verbose | gemma-4-E2B | 1838/1843 (100%) | 98% | 100% | 100% | 100% | 100% | schema:maxItems 5 |
| lora_verbose | LFM2.5-1.2B | 1696/1696 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_verbose | granite-4.2-3b | 1431/1435 (100%) | 99% | 100% | 100% | 100% | 100% | schema:maxItems 4 |
| lora_verbose | gemma-4-E2B | 1320/1320 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | LFM2.5-1.2B | 1733/1735 (100%) | 100% | 99% | 100% | 100% | 100% | schema:enum 2 |
| lora_compact | granite-4.2-3b | 1939/1939 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | gemma-4-E2B | 1820/1820 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | LFM2.5-1.2B | 1316/1334 (99%) | 100% | 100% | 96% | 100% | 100% | schema:minItems 17, schema:maxItems 1 |
| base_grammar | granite-4.2-3b | 1090/1090 (100%) | 100% | 100% | 100% | 100% | – | – |
| base_grammar | gemma-4-E2B | 1934/1934 (100%) | 100% | 100% | 100% | 100% | 100% | – |

## Legality

Would the game carry out the answer as the model wrote it?

| condition | model | legal | valid & legal | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | why not legal |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 1321/1390 (95%) | 52% | 95% | 89% | 100% | 100% | 85% | rules 31, cards_not_held 21, parser 17 |
| base_verbose | granite-4.2-3b | 1032/1067 (97%) | 97% | 99% | 94% | 100% | 94% | – | rules 23, cards_not_held 12 |
| base_verbose | gemma-4-E2B | 1774/1843 (96%) | 96% | 96% | 86% | 100% | 95% | 99% | rules 56, cards_not_held 13 |
| lora_verbose | LFM2.5-1.2B | 1645/1696 (97%) | 97% | 99% | 87% | 100% | 100% | 100% | rules 51 |
| lora_verbose | granite-4.2-3b | 1371/1435 (96%) | 96% | 94% | 86% | 100% | 100% | 100% | rules 64 |
| lora_verbose | gemma-4-E2B | 1139/1320 (86%) | 86% | 55% | 72% | 100% | 100% | 100% | rules 181 |
| lora_compact | LFM2.5-1.2B | 1715/1735 (99%) | 99% | 99% | 95% | 100% | 100% | 100% | rules 18, parser 2 |
| lora_compact | granite-4.2-3b | 1930/1939 (100%) | 100% | 100% | 98% | 100% | 100% | 100% | rules 8, cards_not_held 1 |
| lora_compact | gemma-4-E2B | 1820/1820 (100%) | 100% | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | LFM2.5-1.2B | 1092/1334 (82%) | 82% | 86% | 82% | 88% | 67% | 72% | cards_not_held 129, rules 96, no_cards 17 |
| base_grammar | granite-4.2-3b | 1084/1090 (99%) | 99% | 100% | 100% | 100% | 98% | – | cards_not_held 6 |
| base_grammar | gemma-4-E2B | 1877/1934 (97%) | 97% | 100% | 98% | 100% | 96% | 90% | cards_not_held 50, rules 7 |

## Reference decisions

Does the answer make the decision a simple, value-aware rule set makes?

| condition | model | correct (95% CI) | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | teacher match |
|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 44% [42–47] | 19% | 5% | 92% | 66% | 6% | – |
| base_verbose | granite-4.2-3b | 46% [43–49] | 21% | 2% | 100% | 68% | – | – |
| base_verbose | gemma-4-E2B | 53% [51–55] | 14% | 6% | 70% | 66% | 88% | – |
| lora_verbose | LFM2.5-1.2B | 53% [50–55] | 21% | 6% | 93% | 65% | 63% | – |
| lora_verbose | granite-4.2-3b | 72% [70–75] | 50% | 63% | 96% | 98% | 35% | – |
| lora_verbose | gemma-4-E2B | 57% [54–59] | 24% | 27% | 68% | 72% | 87% | – |
| lora_compact | LFM2.5-1.2B | 86% [84–87] | 70% | 75% | 99% | 95% | 80% | – |
| lora_compact | granite-4.2-3b | 93% [92–94] | 70% | 91% | 99% | 96% | 100% | – |
| lora_compact | gemma-4-E2B | 81% [79–83] | 72% | 87% | 100% | 36% | 75% | – |
| base_grammar | LFM2.5-1.2B | 24% [21–26] | 12% | 15% | 53% | 3% | 11% | – |
| base_grammar | granite-4.2-3b | 39% [36–42] | 12% | 7% | 100% | 37% | – | – |
| base_grammar | gemma-4-E2B | 56% [54–58] | 15% | 7% | 77% | 57% | 84% | – |
| teacher | training corpus | 83% [83–84] | 88% | 99% | 97% | 70% | 62% | – |

Each rule on its own (partial credit):

| condition | model | PLANT: first card placed | PLANT: second card without harvest | FORCE: no avoidable harvest | FORCE: least valuable stack lost | TRADI: keeps growing beans | REPLY: accepts iff useful | REPLY: keeps growing beans | CONSI: accepts iff useful |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 19% | 94% | 9% | 86% | 92% | 68% | 95% | 6% |
| base_verbose | granite-4.2-3b | 21% | 99% | 8% | 88% | 100% | 77% | 83% | – |
| base_verbose | gemma-4-E2B | 17% | 67% | 48% | 44% | 70% | 72% | 89% | 88% |
| lora_verbose | LFM2.5-1.2B | 21% | 99% | 10% | 83% | 93% | 65% | 100% | 63% |
| lora_verbose | granite-4.2-3b | 68% | 63% | 86% | 63% | 96% | 98% | 100% | 35% |
| lora_verbose | gemma-4-E2B | 31% | 41% | 70% | 30% | 68% | 72% | 100% | 87% |
| lora_compact | LFM2.5-1.2B | 70% | 97% | 95% | 76% | 99% | 95% | 99% | 80% |
| lora_compact | granite-4.2-3b | 75% | 94% | 98% | 91% | 99% | 100% | 96% | 100% |
| lora_compact | gemma-4-E2B | 75% | 95% | 99% | 87% | 100% | 38% | 98% | 75% |
| base_grammar | LFM2.5-1.2B | 35% | 22% | 57% | 40% | 53% | 18% | 28% | 11% |
| base_grammar | granite-4.2-3b | 22% | 25% | 57% | 50% | 100% | 68% | 56% | – |
| base_grammar | gemma-4-E2B | 25% | 25% | 57% | 47% | 77% | 67% | 84% | 84% |
| teacher | training corpus | 89% | 99% | 100% | 100% | 97% | 75% | 95% | 62% |

## State sensitivity

Does the decision depend on the game state?

| condition | model | REPLY accepts useful / useless | gap | CONSIDERING accepts useful / useless | gap | PLANTING avoidable harvests | FORCED avoidable harvests | TRADING passes | offers giving away a growing bean |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 24% / 24% | +1 | 100% / 100% | +0 | 215/270 (80%) | 252/279 (90%) | 0% | 36/426 (8%) |
| base_verbose | granite-4.2-3b | 10% / 6% | +4 | – / – | – | 216/276 (78%) | 251/274 (92%) | 100% | – |
| base_verbose | gemma-4-E2B | 47% / 15% | +32 | 26% / 6% | +19 | 228/269 (85%) | 122/276 (44%) | 0% | 199/659 (30%) |
| lora_verbose | LFM2.5-1.2B | 86% / 39% | +48 | 100% / 38% | +62 | 220/278 (79%) | 292/330 (88%) | 0% | 38/524 (7%) |
| lora_verbose | granite-4.2-3b | 95% / 1% | +95 | 100% / 76% | +24 | 81/264 (31%) | 1/295 (0%) | 0% | 18/425 (4%) |
| lora_verbose | gemma-4-E2B | 7% / 1% | +6 | 3% / 1% | +3 | 59/163 (36%) | 5/126 (4%) | 7% | 124/363 (34%) |
| lora_compact | LFM2.5-1.2B | 100% / 7% | +93 | 100% / 21% | +79 | 4/276 (1%) | 1/328 (0%) | 0% | 4/579 (1%) |
| lora_compact | granite-4.2-3b | 100% / 0% | +100 | 100% / 0% | +100 | 18/280 (6%) | 0/356 (0%) | 0% | 3/680 (0%) |
| lora_compact | gemma-4-E2B | 100% / 95% | +5 | 100% / 27% | +73 | 15/280 (5%) | 3/480 (1%) | 0% | 0/577 (0%) |
| base_grammar | LFM2.5-1.2B | 100% / 100% | +0 | 100% / 97% | +3 | 202/246 (82%) | 83/266 (31%) | 0% | 144/359 (40%) |
| base_grammar | granite-4.2-3b | 0% / 0% | +0 | – / – | – | 243/280 (87%) | 120/280 (43%) | 100% | – |
| base_grammar | gemma-4-E2B | 15% / 7% | +8 | 8% / 1% | +7 | 239/280 (85%) | 120/291 (41%) | 0% | 164/718 (23%) |
| teacher | training corpus | 100% / 41% | +59 | 100% / 45% | +55 | 26/3000 (1%) | 9/3000 (0%) | 23% | 132/2309 (6%) |

## Game outcomes

How many coins does a player earn against the same opponents and decks?

Opponents: two bot_random bots in every game.

| condition | player | finished games | coins per game [95% CI] | opponents' coins | wins | penalty per game |
|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 30/30 | 1.50 [1.17, 1.83] | 2.13 | 7% | 1.20 |
| base_verbose | granite-4.2-3b | 30/30 | 1.63 [1.27, 2.00] | 1.87 | 17% | 1.10 |
| base_verbose | gemma-4-E2B | 30/30 | 1.93 [1.57, 2.33] | 1.88 | 23% | 2.23 |
| lora_verbose | LFM2.5-1.2B | 30/30 | 2.03 [1.70, 2.37] | 2.05 | 23% | 1.70 |
| lora_verbose | granite-4.2-3b | 30/30 | 4.63 [4.03, 5.27] | 2.07 | 67% | 2.03 |
| lora_verbose | gemma-4-E2B | 30/30 | 1.60 [1.13, 2.13] | 2.03 | 23% | 5.90 |
| lora_compact | LFM2.5-1.2B | 30/30 | 4.80 [4.17, 5.37] | 2.07 | 77% | 0.60 |
| lora_compact | granite-4.2-3b | 30/30 | 5.43 [4.73, 6.20] | 2.03 | 87% | 0.30 |
| lora_compact | gemma-4-E2B | 30/30 | 5.60 [4.97, 6.23] | 2.40 | 73% | 0.00 |
| base_grammar | LFM2.5-1.2B | 30/30 | 1.90 [1.47, 2.43] | 2.40 | 17% | 6.40 |
| base_grammar | granite-4.2-3b | 30/30 | 2.53 [2.07, 3.07] | 1.92 | 43% | 0.20 |
| base_grammar | gemma-4-E2B | 30/30 | 2.50 [2.10, 2.93] | 1.87 | 40% | 0.47 |
| bot_random | bot_random | 30/30 | 2.40 [2.03, 2.80] | 1.97 | 37% | 0.00 |
| bot_reference | bot_reference | 30/30 | 5.57 [5.00, 6.13] | 2.27 | 83% | 0.00 |

Paired differences in coins per game from the baseline bots, on the same seeds and seats:

| condition | player | Δ coins vs reference bot [95% CI] | p | Holm p | Δ coins vs random bot [95% CI] | p | Holm p |
|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | -4.07 [-4.70, -3.50] | <0.001 | <0.001 | -0.90 [-1.33, -0.50] | <0.001 | 0.006 |
| base_verbose | granite-4.2-3b | -3.93 [-4.60, -3.20] | <0.001 | <0.001 | -0.77 [-1.17, -0.40] | 0.002 | 0.018 |
| base_verbose | gemma-4-E2B | -3.63 [-4.33, -2.90] | <0.001 | <0.001 | -0.47 [-0.87, -0.10] | 0.034 | 0.236 |
| lora_verbose | LFM2.5-1.2B | -3.53 [-4.13, -2.97] | <0.001 | <0.001 | -0.37 [-0.87, +0.13] | 0.109 | 0.435 |
| lora_verbose | granite-4.2-3b | -0.93 [-1.67, -0.17] | 0.030 | 0.151 | +2.23 [+1.67, +2.80] | <0.001 | <0.001 |
| lora_verbose | gemma-4-E2B | -3.97 [-4.60, -3.30] | <0.001 | <0.001 | -0.80 [-1.37, -0.23] | 0.016 | 0.125 |
| lora_compact | LFM2.5-1.2B | -0.77 [-1.73, +0.13] | 0.233 | 0.933 | +2.40 [+1.80, +3.00] | <0.001 | <0.001 |
| lora_compact | granite-4.2-3b | -0.13 [-1.23, +0.93] | 0.761 | 1.000 | +3.03 [+2.27, +3.87] | <0.001 | <0.001 |
| lora_compact | gemma-4-E2B | +0.03 [-0.90, +0.93] | 0.870 | 1.000 | +3.20 [+2.47, +3.90] | <0.001 | <0.001 |
| base_grammar | LFM2.5-1.2B | -3.67 [-4.47, -2.90] | <0.001 | <0.001 | -0.50 [-0.97, -0.07] | 0.061 | 0.303 |
| base_grammar | granite-4.2-3b | -3.03 [-3.63, -2.43] | <0.001 | <0.001 | +0.13 [-0.27, +0.57] | 0.695 | 1.000 |
| base_grammar | gemma-4-E2B | -3.07 [-3.77, -2.40] | <0.001 | <0.001 | +0.10 [-0.27, +0.43] | 0.683 | 1.000 |
| bot_random | bot_random | -3.17 [-3.90, -2.43] | <0.001 | <0.001 | – |  |  |
| bot_reference | bot_reference | – |  |  | +3.17 [+2.43, +3.90] | <0.001 | <0.001 |
| base_verbose | all models | -3.88 [-4.51, -3.24] | <0.001 | <0.001 | -0.71 [-1.04, -0.41] | <0.001 | 0.003 |
| lora_verbose | all models | -2.81 [-3.34, -2.28] | <0.001 | <0.001 | +0.36 [-0.03, +0.70] | 0.037 | 0.236 |
| lora_compact | all models | -0.29 [-1.19, +0.58] | 0.703 | 1.000 | +2.88 [+2.34, +3.44] | <0.001 | <0.001 |
| base_grammar | all models | -3.26 [-3.88, -2.62] | <0.001 | <0.001 | -0.09 [-0.40, +0.19] | 0.544 | 1.000 |


