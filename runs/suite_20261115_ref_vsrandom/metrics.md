# suite_20261115_ref_vsrandom: tournament games

tournament run, backend gpu; 1944 answers per model and condition; training corpus `training/corpus/training_data_reference_15000.txt`; evaluated 2026-11-16 15:29. Shares in brackets are 95% Wilson intervals.

## Overview

| condition | model | answers | schema-valid | legal | valid play | reference-correct | accept gap useful−useless | avoidable harvests |
|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 1390 | 54% [52–57] | 95% [94–96] | 44% [42–47] | 15% [13–17] | -15 | 85% |
| base_verbose | granite-4.2-3b | 1067 | 100% [100–100] | 97% [95–98] | 46% [43–49] | 8% [6–10] | +4 | 85% |
| base_verbose | gemma-4-E2B | 1843 | 100% [99–100] | 96% [95–97] | 53% [51–55] | 3% [3–4] | +31 | 64% |
| lora_verbose | LFM2.5-1.2B | 1722 | 100% [100–100] | 96% [95–97] | 60% [58–63] | 32% [30–34] | +0 | 62% |
| lora_verbose | granite-4.2-3b | 1408 | 99% [98–99] | 86% [84–88] | 71% [68–73] | 46% [43–48] | +49 | 26% |
| lora_verbose | gemma-4-E2B | 1362 | 99% [98–99] | 83% [81–85] | 58% [56–61] | 39% [37–42] | +12 | 46% |
| lora_compact | LFM2.5-1.2B | 1944 | 98% [97–98] | 97% [96–97] | 91% [89–92] | 68% [66–70] | +68 | 0% |
| lora_compact | granite-4.2-3b | 1911 | 100% [100–100] | 100% [100–100] | 98% [97–98] | 75% [73–77] | +100 | 0% |
| lora_compact | gemma-4-E2B | 1865 | 100% [100–100] | 99% [99–100] | 96% [95–97] | 73% [71–75] | +100 | 1% |
| base_grammar | LFM2.5-1.2B | 1334 | 99% [98–99] | 82% [80–84] | 24% [21–26] | 5% [4–6] | +1 | 56% |
| base_grammar | granite-4.2-3b | 1090 | 100% [100–100] | 99% [99–100] | 39% [36–42] | 7% [6–9] | +0 | 65% |
| base_grammar | gemma-4-E2B | 1934 | 100% [100–100] | 97% [96–98] | 56% [54–58] | 8% [7–9] | +11 | 63% |

## Schema validity (valid@1)

Is the whole answer one JSON value that matches its message type's schema, game/schemas/output/<phase>.schema.json?

| condition | model | valid | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | main failures |
|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 756/1390 (54%) | 98% | 96% | 11% | 56% | 3% | wrapped 617, schema:enum 17 |
| base_verbose | granite-4.2-3b | 1067/1067 (100%) | 100% | 100% | 100% | 100% | – | – |
| base_verbose | gemma-4-E2B | 1838/1843 (100%) | 98% | 100% | 100% | 100% | 100% | schema:maxItems 5 |
| lora_verbose | LFM2.5-1.2B | 1722/1722 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_verbose | granite-4.2-3b | 1391/1408 (99%) | 98% | 100% | 97% | 100% | 100% | schema:type 12, schema:maxItems 5 |
| lora_verbose | gemma-4-E2B | 1345/1362 (99%) | 94% | 100% | 100% | 100% | 100% | schema:maxItems 17 |
| lora_compact | LFM2.5-1.2B | 1904/1944 (98%) | 100% | 89% | 100% | 100% | 100% | schema:enum 40 |
| lora_compact | granite-4.2-3b | 1911/1911 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | gemma-4-E2B | 1865/1865 (100%) | 100% | 100% | 100% | 100% | 100% | – |
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
| lora_verbose | LFM2.5-1.2B | 1651/1722 (96%) | 96% | 83% | 91% | 100% | 100% | 100% | rules 71 |
| lora_verbose | granite-4.2-3b | 1213/1408 (86%) | 86% | 59% | 68% | 97% | 100% | 100% | rules 183, unknown_player 12 |
| lora_verbose | gemma-4-E2B | 1127/1362 (83%) | 83% | 51% | 48% | 98% | 100% | 100% | rules 227, cards_not_held 8 |
| lora_compact | LFM2.5-1.2B | 1878/1944 (97%) | 97% | 100% | 85% | 98% | 100% | 100% | parser 40, rules 16, cards_not_held 10 |
| lora_compact | granite-4.2-3b | 1911/1911 (100%) | 100% | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | gemma-4-E2B | 1855/1865 (99%) | 99% | 100% | 97% | 100% | 100% | 100% | rules 10 |
| base_grammar | LFM2.5-1.2B | 1092/1334 (82%) | 82% | 86% | 82% | 88% | 67% | 72% | cards_not_held 129, rules 96, no_cards 17 |
| base_grammar | granite-4.2-3b | 1084/1090 (99%) | 99% | 100% | 100% | 100% | 98% | – | cards_not_held 6 |
| base_grammar | gemma-4-E2B | 1877/1934 (97%) | 97% | 100% | 98% | 100% | 96% | 90% | cards_not_held 50, rules 7 |

## Valid play

Does the answer keep every rule the teacher plays by?

| condition | model | valid play (95% CI) | PLANTING | FORCED | TRADING | REPLY | CONSIDERING |
|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 44% [42–47] | 19% | 5% | 92% | 66% | 6% |
| base_verbose | granite-4.2-3b | 46% [43–49] | 21% | 2% | 100% | 68% | – |
| base_verbose | gemma-4-E2B | 53% [51–55] | 14% | 6% | 70% | 66% | 88% |
| lora_verbose | LFM2.5-1.2B | 60% [58–63] | 18% | 13% | 77% | 66% | 93% |
| lora_verbose | granite-4.2-3b | 71% [68–73] | 31% | 55% | 85% | 80% | 97% |
| lora_verbose | gemma-4-E2B | 58% [56–61] | 19% | 9% | 74% | 77% | 94% |
| lora_compact | LFM2.5-1.2B | 91% [89–92] | 91% | 76% | 98% | 100% | 87% |
| lora_compact | granite-4.2-3b | 98% [97–98] | 91% | 94% | 100% | 100% | 100% |
| lora_compact | gemma-4-E2B | 96% [95–97] | 89% | 86% | 100% | 100% | 100% |
| base_grammar | LFM2.5-1.2B | 24% [21–26] | 12% | 15% | 53% | 3% | 11% |
| base_grammar | granite-4.2-3b | 39% [36–42] | 12% | 7% | 100% | 37% | – |
| base_grammar | gemma-4-E2B | 56% [54–58] | 15% | 7% | 77% | 57% | 84% |
| teacher | training corpus | 100% [100–100] | 100% | 100% | 100% | 100% | 100% |

Each rule on its own (partial credit):

| condition | model | PLANT: first card placed | PLANT: second card without harvest | FORCE: no avoidable harvest | FORCE: least valuable stack lost | TRADI: keeps growing beans | REPLY: accepts iff useful | REPLY: keeps growing beans | CONSI: accepts iff useful |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 19% | 94% | 9% | 86% | 92% | 68% | 95% | 6% |
| base_verbose | granite-4.2-3b | 21% | 99% | 8% | 88% | 100% | 77% | 83% | – |
| base_verbose | gemma-4-E2B | 17% | 67% | 48% | 44% | 70% | 72% | 89% | 88% |
| lora_verbose | LFM2.5-1.2B | 28% | 57% | 49% | 55% | 77% | 66% | 100% | 93% |
| lora_verbose | granite-4.2-3b | 49% | 35% | 64% | 59% | 85% | 80% | 100% | 97% |
| lora_verbose | gemma-4-E2B | 19% | 51% | 36% | 22% | 74% | 77% | 100% | 94% |
| lora_compact | LFM2.5-1.2B | 91% | 100% | 85% | 76% | 98% | 100% | 100% | 87% |
| lora_compact | granite-4.2-3b | 91% | 100% | 100% | 94% | 100% | 100% | 100% | 100% |
| lora_compact | gemma-4-E2B | 90% | 100% | 95% | 88% | 100% | 100% | 100% | 100% |
| base_grammar | LFM2.5-1.2B | 35% | 22% | 57% | 40% | 53% | 18% | 28% | 11% |
| base_grammar | granite-4.2-3b | 22% | 25% | 57% | 50% | 100% | 68% | 56% | – |
| base_grammar | gemma-4-E2B | 25% | 25% | 57% | 47% | 77% | 67% | 84% | 84% |
| teacher | training corpus | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |

## Reference-correctness

Does the answer make the decision the reference bot makes in the same state?

| condition | model | correct (95% CI) | PLANTING | FORCED | TRADING | REPLY | CONSIDERING |
|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 15% [13–17] | 18% | 5% | 1% | 61% | 0% |
| base_verbose | granite-4.2-3b | 8% [6–10] | 19% | 2% | 8% | 0% | – |
| base_verbose | gemma-4-E2B | 3% [3–4] | 13% | 6% | 1% | 0% | 0% |
| lora_verbose | LFM2.5-1.2B | 32% [30–34] | 14% | 7% | 0% | 66% | 93% |
| lora_verbose | granite-4.2-3b | 46% [43–48] | 22% | 45% | 26% | 63% | 97% |
| lora_verbose | gemma-4-E2B | 39% [37–42] | 15% | 9% | 17% | 73% | 94% |
| lora_compact | LFM2.5-1.2B | 68% [66–70] | 85% | 73% | 36% | 100% | 87% |
| lora_compact | granite-4.2-3b | 75% [73–77] | 88% | 92% | 37% | 100% | 100% |
| lora_compact | gemma-4-E2B | 73% [71–75] | 86% | 84% | 39% | 100% | 100% |
| base_grammar | LFM2.5-1.2B | 5% [4–6] | 4% | 14% | 2% | 0% | 1% |
| base_grammar | granite-4.2-3b | 7% [6–9] | 11% | 5% | 12% | 0% | – |
| base_grammar | gemma-4-E2B | 8% [7–9] | 12% | 6% | 0% | 0% | 25% |
| teacher | training corpus | 100% [100–100] | 100% | 100% | 100% | 100% | 100% |

## State sensitivity

Does the decision depend on the game state?

| condition | model | REPLY accepts useful / useless | gap | CONSIDERING accepts useful / useless | gap | PLANTING avoidable harvests | FORCED avoidable harvests | TRADING passes | offers giving away a growing bean |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 24% / 24% | +1 | 100% / 100% | +0 | 215/270 (80%) | 252/279 (90%) | 0% | 36/426 (8%) |
| base_verbose | granite-4.2-3b | 10% / 6% | +4 | – / – | – | 216/276 (78%) | 251/274 (92%) | 100% | – |
| base_verbose | gemma-4-E2B | 47% / 15% | +32 | 26% / 6% | +19 | 228/269 (85%) | 122/276 (44%) | 0% | 199/659 (30%) |
| lora_verbose | LFM2.5-1.2B | 0% / 0% | +0 | 0% / 0% | +0 | 182/236 (77%) | 99/215 (46%) | 0% | 140/601 (23%) |
| lora_verbose | granite-4.2-3b | 46% / 0% | +46 | 62% / 0% | +62 | 71/175 (41%) | 8/134 (6%) | 1% | 55/429 (13%) |
| lora_verbose | gemma-4-E2B | 14% / 0% | +14 | 0% / 0% | +0 | 85/152 (56%) | 20/77 (26%) | 0% | 101/408 (25%) |
| lora_compact | LFM2.5-1.2B | 100% / 0% | +100 | 16% / 2% | +15 | 0/280 (0%) | 0/322 (0%) | 4% | 6/622 (1%) |
| lora_compact | granite-4.2-3b | 100% / 0% | +100 | 100% / 0% | +100 | 0/280 (0%) | 0/374 (0%) | 4% | 0/619 (0%) |
| lora_compact | gemma-4-E2B | 100% / 0% | +100 | 100% / 0% | +100 | 1/280 (0%) | 6/343 (2%) | 5% | 0/619 (0%) |
| base_grammar | LFM2.5-1.2B | 100% / 100% | +0 | 100% / 97% | +3 | 202/246 (82%) | 83/266 (31%) | 0% | 144/359 (40%) |
| base_grammar | granite-4.2-3b | 0% / 0% | +0 | – / – | – | 243/280 (87%) | 120/280 (43%) | 100% | – |
| base_grammar | gemma-4-E2B | 15% / 7% | +8 | 8% / 1% | +7 | 239/280 (85%) | 120/291 (41%) | 0% | 164/718 (23%) |
| teacher | training corpus | 100% / 0% | +100 | 100% / 0% | +100 | 0/3000 (0%) | 0/3000 (0%) | 43% | 0/1712 (0%) |

## Game outcomes

How many coins does a player earn against the same opponents and decks?

Opponents: two bot_random bots in every game.

| condition | player | finished games | coins per game [95% CI] | opponents' coins | wins | penalty per game |
|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 30/30 | 1.50 [1.17, 1.83] | 2.13 | 7% | 1.20 |
| base_verbose | granite-4.2-3b | 30/30 | 1.63 [1.27, 2.00] | 1.87 | 17% | 1.10 |
| base_verbose | gemma-4-E2B | 30/30 | 1.93 [1.57, 2.33] | 1.88 | 23% | 2.23 |
| lora_verbose | LFM2.5-1.2B | 30/30 | 1.63 [1.23, 2.07] | 2.10 | 20% | 2.37 |
| lora_verbose | granite-4.2-3b | 30/30 | 2.60 [1.90, 3.27] | 2.07 | 37% | 6.53 |
| lora_verbose | gemma-4-E2B | 30/30 | 1.10 [0.73, 1.47] | 1.95 | 10% | 7.63 |
| lora_compact | LFM2.5-1.2B | 30/30 | 5.33 [4.77, 5.87] | 2.07 | 83% | 0.83 |
| lora_compact | granite-4.2-3b | 30/30 | 5.70 [5.07, 6.30] | 2.12 | 87% | 0.00 |
| lora_compact | gemma-4-E2B | 30/30 | 5.67 [5.07, 6.30] | 2.20 | 83% | 0.37 |
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
| base_verbose | gemma-4-E2B | -3.63 [-4.33, -2.90] | <0.001 | <0.001 | -0.47 [-0.87, -0.10] | 0.034 | 0.202 |
| lora_verbose | LFM2.5-1.2B | -3.93 [-4.70, -3.13] | <0.001 | <0.001 | -0.77 [-1.23, -0.33] | 0.004 | 0.029 |
| lora_verbose | granite-4.2-3b | -2.97 [-3.87, -2.07] | <0.001 | <0.001 | +0.20 [-0.53, +0.97] | 0.592 | 1.000 |
| lora_verbose | gemma-4-E2B | -4.47 [-5.13, -3.80] | <0.001 | <0.001 | -1.30 [-1.77, -0.83] | <0.001 | 0.001 |
| lora_compact | LFM2.5-1.2B | -0.23 [-1.03, +0.50] | 0.768 | 1.000 | +2.93 [+2.27, +3.63] | <0.001 | <0.001 |
| lora_compact | granite-4.2-3b | +0.13 [-0.57, +0.83] | 0.611 | 1.000 | +3.30 [+2.60, +3.97] | <0.001 | <0.001 |
| lora_compact | gemma-4-E2B | +0.10 [-0.77, +0.97] | 0.787 | 1.000 | +3.27 [+2.60, +3.97] | <0.001 | <0.001 |
| base_grammar | LFM2.5-1.2B | -3.67 [-4.47, -2.90] | <0.001 | <0.001 | -0.50 [-0.97, -0.07] | 0.061 | 0.303 |
| base_grammar | granite-4.2-3b | -3.03 [-3.63, -2.43] | <0.001 | <0.001 | +0.13 [-0.27, +0.57] | 0.695 | 1.000 |
| base_grammar | gemma-4-E2B | -3.07 [-3.77, -2.40] | <0.001 | <0.001 | +0.10 [-0.27, +0.43] | 0.683 | 1.000 |
| bot_random | bot_random | -3.17 [-3.90, -2.43] | <0.001 | <0.001 | – |  |  |
| bot_reference | bot_reference | – |  |  | +3.17 [+2.43, +3.90] | <0.001 | <0.001 |
| base_verbose | all models | -3.88 [-4.51, -3.24] | <0.001 | <0.001 | -0.71 [-1.04, -0.41] | <0.001 | 0.003 |
| lora_verbose | all models | -3.79 [-4.46, -3.14] | <0.001 | <0.001 | -0.62 [-1.00, -0.24] | 0.005 | 0.034 |
| lora_compact | all models | +0.00 [-0.66, +0.67] | 0.628 | 1.000 | +3.17 [+2.60, +3.72] | <0.001 | <0.001 |
| base_grammar | all models | -3.26 [-3.88, -2.62] | <0.001 | <0.001 | -0.09 [-0.40, +0.19] | 0.544 | 1.000 |


