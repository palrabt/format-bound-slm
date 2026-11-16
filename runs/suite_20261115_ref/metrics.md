# suite_20261115_ref: tournament games

tournament run, backend gpu; 2435 answers per model and condition; training corpus `training/corpus/training_data_reference_15000.txt`; evaluated 2026-11-16 15:28. Shares in brackets are 95% Wilson intervals.

## Overview

| condition | model | answers | schema-valid | legal | valid play | reference-correct | accept gap useful−useless | avoidable harvests |
|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 1271 | 52% [50–55] | 92% [91–94] | 44% [41–47] | 7% [6–8] | -46 | 82% |
| base_verbose | granite-4.2-3b | 945 | 100% [100–100] | 98% [97–99] | 46% [43–50] | 7% [6–9] | – | 86% |
| base_verbose | gemma-4-E2B | 1778 | 100% [100–100] | 98% [98–99] | 59% [56–61] | 3% [2–4] | +79 | 66% |
| lora_verbose | LFM2.5-1.2B | 1457 | 100% [100–100] | 96% [94–96] | 46% [44–49] | 14% [13–16] | +8 | 62% |
| lora_verbose | granite-4.2-3b | 1371 | 99% [99–100] | 85% [83–87] | 69% [66–71] | 34% [31–36] | +75 | 28% |
| lora_verbose | gemma-4-E2B | 1590 | 99% [98–99] | 87% [85–88] | 58% [55–60] | 28% [26–31] | +47 | 38% |
| lora_compact | LFM2.5-1.2B | 2435 | 98% [97–99] | 97% [96–97] | 89% [88–91] | 67% [66–69] | +70 | 0% |
| lora_compact | granite-4.2-3b | 2177 | 100% [100–100] | 100% [100–100] | 98% [98–99] | 79% [77–80] | +100 | 0% |
| lora_compact | gemma-4-E2B | 2179 | 100% [100–100] | 100% [100–100] | 97% [96–98] | 77% [76–79] | +100 | 1% |
| base_grammar | LFM2.5-1.2B | 1288 | 97% [96–98] | 80% [77–82] | 23% [21–26] | 4% [3–5] | +0 | 61% |
| base_grammar | granite-4.2-3b | 1030 | 100% [100–100] | 100% [99–100] | 33% [30–36] | 6% [5–8] | – | 64% |
| base_grammar | gemma-4-E2B | 1931 | 100% [100–100] | 90% [89–91] | 47% [45–49] | 6% [5–7] | +73 | 64% |

## Schema validity (valid@1)

Is the whole answer one JSON value that matches its message type's schema, game/schemas/output/<phase>.schema.json?

| condition | model | valid | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | main failures |
|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 665/1271 (52%) | 96% | 97% | 5% | 30% | 29% | wrapped 581, schema:enum 22, not_json 3 |
| base_verbose | granite-4.2-3b | 945/945 (100%) | 100% | 100% | 100% | 100% | – | – |
| base_verbose | gemma-4-E2B | 1777/1778 (100%) | 100% | 100% | 100% | 100% | 100% | schema:maxItems 1 |
| lora_verbose | LFM2.5-1.2B | 1457/1457 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_verbose | granite-4.2-3b | 1363/1371 (99%) | 99% | 100% | 99% | 100% | 100% | schema:type 5, schema:maxItems 3 |
| lora_verbose | gemma-4-E2B | 1571/1590 (99%) | 94% | 100% | 100% | 100% | 100% | schema:maxItems 19 |
| lora_compact | LFM2.5-1.2B | 2388/2435 (98%) | 100% | 89% | 100% | 100% | 100% | schema:enum 47 |
| lora_compact | granite-4.2-3b | 2177/2177 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | gemma-4-E2B | 2179/2179 (100%) | 100% | 100% | 100% | 100% | 100% | – |
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
| lora_verbose | LFM2.5-1.2B | 1392/1457 (96%) | 96% | 83% | 93% | 100% | 100% | 100% | rules 65 |
| lora_verbose | granite-4.2-3b | 1169/1371 (85%) | 85% | 47% | 73% | 99% | 100% | 100% | rules 197, unknown_player 5 |
| lora_verbose | gemma-4-E2B | 1381/1590 (87%) | 87% | 58% | 57% | 98% | 100% | 100% | rules 198, cards_not_held 11 |
| lora_compact | LFM2.5-1.2B | 2359/2435 (97%) | 97% | 100% | 84% | 99% | 100% | 100% | parser 47, rules 22, cards_not_held 7 |
| lora_compact | granite-4.2-3b | 2177/2177 (100%) | 100% | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | gemma-4-E2B | 2175/2179 (100%) | 100% | 100% | 99% | 100% | 100% | 100% | rules 3, cards_not_held 1 |
| base_grammar | LFM2.5-1.2B | 1026/1288 (80%) | 80% | 89% | 90% | 87% | 49% | 51% | cards_not_held 170, rules 62, no_cards 30 |
| base_grammar | granite-4.2-3b | 1028/1030 (100%) | 100% | 100% | 100% | 100% | 99% | – | cards_not_held 2 |
| base_grammar | gemma-4-E2B | 1739/1931 (90%) | 90% | 100% | 92% | 100% | 86% | 66% | cards_not_held 164, rules 28 |

## Valid play

Does the answer keep every rule the teacher plays by?

| condition | model | valid play (95% CI) | PLANTING | FORCED | TRADING | REPLY | CONSIDERING |
|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 44% [41–47] | 20% | 11% | 89% | 38% | 9% |
| base_verbose | granite-4.2-3b | 46% [43–50] | 21% | 1% | 100% | 89% | – |
| base_verbose | gemma-4-E2B | 59% [56–61] | 15% | 4% | 73% | 99% | 85% |
| lora_verbose | LFM2.5-1.2B | 46% [44–49] | 19% | 12% | 77% | 9% | 83% |
| lora_verbose | granite-4.2-3b | 69% [66–71] | 22% | 53% | 86% | 87% | 86% |
| lora_verbose | gemma-4-E2B | 58% [55–60] | 22% | 10% | 77% | 65% | 77% |
| lora_compact | LFM2.5-1.2B | 89% [88–91] | 93% | 77% | 99% | 99% | 82% |
| lora_compact | granite-4.2-3b | 98% [98–99] | 94% | 95% | 100% | 100% | 100% |
| lora_compact | gemma-4-E2B | 97% [96–98] | 90% | 91% | 100% | 100% | 100% |
| base_grammar | LFM2.5-1.2B | 23% [21–26] | 12% | 13% | 53% | 10% | 3% |
| base_grammar | granite-4.2-3b | 33% [30–36] | 12% | 8% | 100% | 0% | – |
| base_grammar | gemma-4-E2B | 47% [45–49] | 14% | 9% | 77% | 38% | 54% |
| teacher | training corpus | 100% [100–100] | 100% | 100% | 100% | 100% | 100% |

Each rule on its own (partial credit):

| condition | model | PLANT: first card placed | PLANT: second card without harvest | FORCE: no avoidable harvest | FORCE: least valuable stack lost | TRADI: keeps growing beans | REPLY: accepts iff useful | REPLY: keeps growing beans | CONSI: accepts iff useful |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 20% | 92% | 12% | 84% | 89% | 49% | 63% | 9% |
| base_verbose | granite-4.2-3b | 21% | 98% | 7% | 88% | 100% | 89% | 97% | – |
| base_verbose | gemma-4-E2B | 17% | 72% | 52% | 48% | 73% | 99% | 100% | 85% |
| lora_verbose | LFM2.5-1.2B | 29% | 58% | 49% | 56% | 77% | 9% | 100% | 83% |
| lora_verbose | granite-4.2-3b | 39% | 26% | 69% | 57% | 86% | 87% | 100% | 86% |
| lora_verbose | gemma-4-E2B | 23% | 57% | 45% | 22% | 77% | 65% | 100% | 77% |
| lora_compact | LFM2.5-1.2B | 93% | 100% | 83% | 78% | 99% | 100% | 99% | 82% |
| lora_compact | granite-4.2-3b | 94% | 100% | 100% | 95% | 100% | 100% | 100% | 100% |
| lora_compact | gemma-4-E2B | 90% | 100% | 98% | 92% | 100% | 100% | 100% | 100% |
| base_grammar | LFM2.5-1.2B | 24% | 21% | 54% | 50% | 53% | 49% | 10% | 3% |
| base_grammar | granite-4.2-3b | 24% | 25% | 59% | 49% | 100% | 1% | 70% | – |
| base_grammar | gemma-4-E2B | 26% | 26% | 51% | 49% | 77% | 81% | 42% | 54% |
| teacher | training corpus | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |

## Reference-correctness

Does the answer make the decision the reference bot makes in the same state?

| condition | model | correct (95% CI) | PLANTING | FORCED | TRADING | REPLY | CONSIDERING |
|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 7% [6–8] | 18% | 11% | 0% | 1% | 0% |
| base_verbose | granite-4.2-3b | 7% [6–9] | 19% | 1% | 5% | 0% | – |
| base_verbose | gemma-4-E2B | 3% [2–4] | 13% | 4% | 1% | 0% | 0% |
| lora_verbose | LFM2.5-1.2B | 14% [13–16] | 13% | 7% | 0% | 0% | 83% |
| lora_verbose | granite-4.2-3b | 34% [31–36] | 14% | 45% | 24% | 0% | 86% |
| lora_verbose | gemma-4-E2B | 28% [26–31] | 18% | 10% | 16% | 0% | 77% |
| lora_compact | LFM2.5-1.2B | 67% [66–69] | 90% | 76% | 29% | 99% | 82% |
| lora_compact | granite-4.2-3b | 79% [77–80] | 91% | 94% | 34% | 100% | 100% |
| lora_compact | gemma-4-E2B | 77% [76–79] | 88% | 88% | 35% | 99% | 100% |
| base_grammar | LFM2.5-1.2B | 4% [3–5] | 3% | 11% | 2% | 0% | 0% |
| base_grammar | granite-4.2-3b | 6% [5–8] | 11% | 5% | 7% | 0% | – |
| base_grammar | gemma-4-E2B | 6% [5–7] | 12% | 8% | 1% | 23% | 2% |
| teacher | training corpus | 100% [100–100] | 100% | 100% | 100% | 100% | 100% |

## State sensitivity

Does the decision depend on the game state?

| condition | model | REPLY accepts useful / useless | gap | CONSIDERING accepts useful / useless | gap | PLANTING avoidable harvests | FORCED avoidable harvests | TRADING passes | offers giving away a growing bean |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 51% / – | – | 100% / 100% | +0 | 204/261 (78%) | 238/278 (86%) | 0% | 53/473 (11%) |
| base_verbose | granite-4.2-3b | 89% / – | – | – / – | – | 217/275 (79%) | 240/259 (93%) | 100% | – |
| base_verbose | gemma-4-E2B | 99% / – | – | 2% / 1% | +1 | 226/267 (85%) | 120/261 (46%) | 0% | 183/689 (27%) |
| lora_verbose | LFM2.5-1.2B | 9% / – | – | 0% / 0% | +0 | 181/238 (76%) | 105/221 (48%) | 0% | 123/541 (23%) |
| lora_verbose | granite-4.2-3b | 87% / – | – | 31% / 0% | +30 | 63/142 (44%) | 5/105 (5%) | 1% | 45/362 (12%) |
| lora_verbose | gemma-4-E2B | 65% / – | – | 0% / 0% | +0 | 83/171 (49%) | 21/100 (21%) | 1% | 99/473 (21%) |
| lora_compact | LFM2.5-1.2B | 100% / – | – | 16% / 0% | +16 | 0/280 (0%) | 2/361 (1%) | 3% | 0/713 (0%) |
| lora_compact | granite-4.2-3b | 100% / – | – | 100% / 0% | +100 | 0/280 (0%) | 0/388 (0%) | 4% | 0/612 (0%) |
| lora_compact | gemma-4-E2B | 100% / – | – | 100% / 0% | +100 | 0/280 (0%) | 6/382 (2%) | 3% | 0/611 (0%) |
| base_grammar | LFM2.5-1.2B | 100% / – | – | 100% / 100% | +0 | 214/252 (85%) | 119/292 (41%) | 0% | 132/334 (40%) |
| base_grammar | granite-4.2-3b | 1% / – | – | – / – | – | 242/280 (86%) | 116/281 (41%) | 100% | – |
| base_grammar | gemma-4-E2B | 94% / – | – | 0% / 0% | +0 | 240/280 (86%) | 139/315 (44%) | 0% | 164/716 (23%) |
| teacher | training corpus | 100% / 0% | +100 | 100% / 0% | +100 | 0/3000 (0%) | 0/3000 (0%) | 43% | 0/1712 (0%) |

## Game outcomes

How many coins does a player earn against the same opponents and decks?

Opponents: two bot_reference bots in every game.

| condition | player | finished games | coins per game [95% CI] | opponents' coins | wins | penalty per game |
|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 30/30 | 2.60 [1.97, 3.23] | 9.15 | 0% | 1.97 |
| base_verbose | granite-4.2-3b | 30/30 | 1.57 [1.23, 1.90] | 7.67 | 0% | 0.67 |
| base_verbose | gemma-4-E2B | 30/30 | 1.83 [1.43, 2.30] | 7.32 | 0% | 0.70 |
| lora_verbose | LFM2.5-1.2B | 30/30 | 1.77 [1.40, 2.17] | 7.33 | 0% | 2.17 |
| lora_verbose | granite-4.2-3b | 30/30 | 2.20 [1.53, 2.93] | 7.85 | 3% | 6.67 |
| lora_verbose | gemma-4-E2B | 30/30 | 1.30 [0.90, 1.73] | 7.23 | 0% | 6.87 |
| lora_compact | LFM2.5-1.2B | 30/30 | 7.43 [6.63, 8.17] | 7.92 | 27% | 1.00 |
| lora_compact | granite-4.2-3b | 30/30 | 8.37 [7.60, 9.13] | 8.65 | 30% | 0.00 |
| lora_compact | gemma-4-E2B | 30/30 | 8.00 [7.03, 8.87] | 8.63 | 33% | 0.13 |
| base_grammar | LFM2.5-1.2B | 30/30 | 2.77 [2.27, 3.33] | 9.05 | 0% | 6.30 |
| base_grammar | granite-4.2-3b | 30/30 | 2.53 [2.07, 3.00] | 7.40 | 0% | 0.07 |
| base_grammar | gemma-4-E2B | 30/30 | 3.10 [2.57, 3.73] | 7.57 | 3% | 1.83 |
| bot_random | bot_random | 30/30 | 2.20 [1.80, 2.60] | 7.43 | 0% | 0.00 |
| bot_reference | bot_reference | 30/30 | 8.33 [7.43, 9.20] | 8.63 | 23% | 0.00 |

Paired differences in coins per game from the baseline bots, on the same seeds and seats:

| condition | player | Δ coins vs reference bot [95% CI] | p | Holm p | Δ coins vs random bot [95% CI] | p | Holm p |
|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | -5.73 [-6.70, -4.80] | <0.001 | <0.001 | +0.40 [-0.30, +1.17] | 0.332 | 0.995 |
| base_verbose | granite-4.2-3b | -6.77 [-7.67, -5.73] | <0.001 | <0.001 | -0.63 [-1.00, -0.27] | 0.005 | 0.056 |
| base_verbose | gemma-4-E2B | -6.50 [-7.50, -5.43] | <0.001 | <0.001 | -0.37 [-0.77, +0.00] | 0.071 | 0.424 |
| lora_verbose | LFM2.5-1.2B | -6.57 [-7.53, -5.53] | <0.001 | <0.001 | -0.43 [-0.80, -0.07] | 0.040 | 0.282 |
| lora_verbose | granite-4.2-3b | -6.13 [-7.07, -5.13] | <0.001 | <0.001 | +0.00 [-0.77, +0.80] | 0.871 | 0.995 |
| lora_verbose | gemma-4-E2B | -7.03 [-7.93, -6.10] | <0.001 | <0.001 | -0.90 [-1.40, -0.43] | 0.002 | 0.022 |
| lora_compact | LFM2.5-1.2B | -0.90 [-1.60, -0.13] | 0.021 | 0.083 | +5.23 [+4.33, +6.13] | <0.001 | <0.001 |
| lora_compact | granite-4.2-3b | +0.03 [-0.83, +0.93] | 0.903 | 1.000 | +6.17 [+5.27, +7.03] | <0.001 | <0.001 |
| lora_compact | gemma-4-E2B | -0.33 [-1.10, +0.40] | 0.535 | 1.000 | +5.80 [+4.80, +6.80] | <0.001 | <0.001 |
| base_grammar | LFM2.5-1.2B | -5.57 [-6.57, -4.53] | <0.001 | <0.001 | +0.57 [+0.03, +1.10] | 0.071 | 0.424 |
| base_grammar | granite-4.2-3b | -5.80 [-6.70, -4.90] | <0.001 | <0.001 | +0.33 [-0.10, +0.80] | 0.165 | 0.660 |
| base_grammar | gemma-4-E2B | -5.23 [-6.23, -4.27] | <0.001 | <0.001 | +0.90 [+0.27, +1.63] | 0.011 | 0.111 |
| bot_random | bot_random | -6.13 [-7.10, -5.10] | <0.001 | <0.001 | – |  |  |
| bot_reference | bot_reference | – |  |  | +6.13 [+5.10, +7.10] | <0.001 | <0.001 |
| base_verbose | all models | -6.33 [-7.26, -5.37] | <0.001 | <0.001 | -0.20 [-0.61, +0.20] | 0.391 | 0.995 |
| lora_verbose | all models | -6.58 [-7.46, -5.68] | <0.001 | <0.001 | -0.44 [-0.82, -0.07] | 0.031 | 0.249 |
| lora_compact | all models | -0.40 [-1.08, +0.31] | 0.233 | 0.700 | +5.73 [+4.87, +6.61] | <0.001 | <0.001 |
| base_grammar | all models | -5.53 [-6.43, -4.64] | <0.001 | <0.001 | +0.60 [+0.19, +1.06] | 0.017 | 0.151 |


