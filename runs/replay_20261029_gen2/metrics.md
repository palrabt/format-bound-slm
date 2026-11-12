# replay_20261029_gen2: game states

replay run, backend gpu; 500 answers per model and condition; training corpus `training/corpus/training_data_synct_15000_llm.txt`; evaluated 2026-11-12 13:11. Shares in brackets are 95% Wilson intervals.

## Overview

| condition | model | answers | schema-valid | legal | reference-correct | accept gap useful−useless | avoidable harvests |
|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 500 | 52% [47–56] | 75% [71–79] | 34% [30–39] | +3 | 62% |
| base_verbose | granite-4.2-3b | 500 | 100% [99–100] | 85% [82–88] | 45% [40–49] | +2 | 42% |
| base_verbose | gemma-4-E2B | 500 | 100% [99–100] | 95% [93–97] | 42% [38–46] | +13 | 43% |
| lora_verbose | LFM2.5-1.2B | 500 | 100% [99–100] | 99% [98–100] | 49% [45–54] | +10 | 41% |
| lora_verbose | granite-4.2-3b | 500 | 100% [99–100] | 98% [96–99] | 74% [70–78] | +44 | 17% |
| lora_verbose | gemma-4-E2B | 500 | 100% [99–100] | 88% [85–91] | 45% [41–50] | +6 | 39% |
| base_verbose2 | LFM2.5-1.2B | 500 | 96% [94–98] | 71% [67–75] | 32% [28–36] | +0 | 45% |
| base_verbose2 | granite-4.2-3b | 500 | 100% [99–100] | 89% [86–92] | 42% [38–47] | +1 | 28% |
| base_verbose2 | gemma-4-E2B | 500 | 100% [99–100] | 87% [84–89] | 43% [39–48] | +3 | 50% |
| lora_verbose2 | LFM2.5-1.2B | 500 | 100% [99–100] | 99% [98–100] | 42% [38–46] | +0 | 57% |
| lora_verbose2 | granite-4.2-3b | 500 | 100% [99–100] | 94% [92–96] | 63% [59–67] | +35 | 27% |
| lora_verbose2 | gemma-4-E2B | 500 | 97% [95–98] | 89% [86–91] | 49% [44–53] | +14 | 38% |
| base_compact | LFM2.5-1.2B | 500 | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| base_compact | granite-4.2-3b | 500 | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| base_compact | gemma-4-E2B | 500 | 0% [0–1] | 18% [15–22] | 10% [7–12] | +0 | – |
| lora_compact | LFM2.5-1.2B | 500 | 100% [99–100] | 99% [98–100] | 78% [75–82] | +35 | 3% |
| lora_compact | granite-4.2-3b | 500 | 100% [99–100] | 100% [99–100] | 90% [87–93] | +98 | 4% |
| lora_compact | gemma-4-E2B | 500 | 100% [99–100] | 100% [99–100] | 68% [64–72] | +0 | 10% |
| base_grammar | LFM2.5-1.2B | 500 | 97% [95–98] | 81% [78–84] | 24% [21–28] | +1 | 62% |
| base_grammar | granite-4.2-3b | 500 | 100% [99–100] | 93% [90–95] | 41% [37–45] | +3 | 59% |
| base_grammar | gemma-4-E2B | 500 | 100% [99–100] | 95% [92–96] | 37% [33–41] | +5 | 62% |
| lora_grammar | LFM2.5-1.2B | 500 | 94% [91–96] | 93% [91–95] | 44% [40–49] | +4 | 45% |
| lora_grammar | granite-4.2-3b | 500 | 97% [95–98] | 97% [95–98] | 74% [70–78] | +54 | 13% |
| lora_grammar | gemma-4-E2B | 500 | 80% [76–83] | 80% [76–83] | 27% [24–31] | +0 | 50% |

## Effects

How much do the adapter and the prompt style change an outcome, item by item?

Rows marked * stay significant after the Holm correction.

### schema-valid

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| LFM2.5-1.2B | adapter at verbose | 500 | 52% | 100% | +48 [+44, +53] | 0 / 242 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at verbose2 | 500 | 96% | 100% | +4 [+2, +5] | 1 / 19 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at compact | 500 | 0% | 100% | +100 [+100, +100] | 0 / 500 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at grammar | 500 | 97% | 94% | -3 [-5, -1] | 18 / 3 | 0.001 | 0.019 * |
| LFM2.5-1.2B | base: verbose2 vs verbose | 500 | 52% | 96% | +45 [+40, +49] | 19 / 242 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: compact vs verbose | 500 | 52% | 0% | -52 [-56, -47] | 258 / 0 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: grammar vs verbose | 500 | 52% | 97% | +45 [+41, +50] | 3 / 229 | <0.001 | <0.001 * |
| LFM2.5-1.2B | lora: verbose2 vs verbose | 500 | 100% | 100% | -0 [-1, +0] | 1 / 0 | 1.000 | 1.000 |
| LFM2.5-1.2B | lora: compact vs verbose | 500 | 100% | 100% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| LFM2.5-1.2B | lora: grammar vs verbose | 500 | 100% | 94% | -6 [-8, -4] | 31 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at verbose | 500 | 100% | 100% | +0 [+0, +1] | 0 / 1 | 1.000 | 1.000 |
| granite-4.2-3b | adapter at verbose2 | 500 | 100% | 100% | -0 [-1, +0] | 2 / 1 | 1.000 | 1.000 |
| granite-4.2-3b | adapter at compact | 500 | 0% | 100% | +100 [+100, +100] | 0 / 500 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at grammar | 500 | 100% | 97% | -3 [-5, -2] | 16 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | base: verbose2 vs verbose | 500 | 100% | 100% | +0 [-1, +1] | 1 / 1 | 1.000 | 1.000 |
| granite-4.2-3b | base: compact vs verbose | 500 | 100% | 0% | -100 [-100, -99] | 499 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | base: grammar vs verbose | 500 | 100% | 100% | +0 [+0, +1] | 0 / 1 | 1.000 | 1.000 |
| granite-4.2-3b | lora: verbose2 vs verbose | 500 | 100% | 100% | -0 [-1, +0] | 2 / 0 | 0.500 | 1.000 |
| granite-4.2-3b | lora: compact vs verbose | 500 | 100% | 100% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| granite-4.2-3b | lora: grammar vs verbose | 500 | 100% | 97% | -3 [-5, -2] | 16 / 0 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at verbose | 500 | 100% | 100% | +0 [+0, +1] | 0 / 1 | 1.000 | 1.000 |
| gemma-4-E2B | adapter at verbose2 | 500 | 100% | 97% | -3 [-5, -1] | 17 / 2 | <0.001 | 0.010 * |
| gemma-4-E2B | adapter at compact | 500 | 0% | 100% | +100 [+100, +100] | 0 / 500 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at grammar | 500 | 100% | 80% | -20 [-24, -17] | 100 / 0 | <0.001 | <0.001 * |
| gemma-4-E2B | base: verbose2 vs verbose | 500 | 100% | 100% | -0 [-1, +0] | 2 / 1 | 1.000 | 1.000 |
| gemma-4-E2B | base: compact vs verbose | 500 | 100% | 0% | -100 [-100, -99] | 499 / 0 | <0.001 | <0.001 * |
| gemma-4-E2B | base: grammar vs verbose | 500 | 100% | 100% | +0 [+0, +1] | 0 / 1 | 1.000 | 1.000 |
| gemma-4-E2B | lora: verbose2 vs verbose | 500 | 100% | 97% | -3 [-5, -2] | 17 / 0 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: compact vs verbose | 500 | 100% | 100% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| gemma-4-E2B | lora: grammar vs verbose | 500 | 100% | 80% | -20 [-24, -17] | 100 / 0 | <0.001 | <0.001 * |

### legal

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| LFM2.5-1.2B | adapter at verbose | 500 | 75% | 99% | +24 [+20, +28] | 1 / 121 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at verbose2 | 500 | 71% | 99% | +28 [+24, +32] | 2 / 143 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at compact | 500 | 0% | 99% | +99 [+99, +100] | 0 / 497 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at grammar | 500 | 81% | 93% | +12 [+9, +16] | 15 / 76 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: verbose2 vs verbose | 500 | 75% | 71% | -4 [-10, +0] | 95 / 73 | 0.105 | 0.734 |
| LFM2.5-1.2B | base: compact vs verbose | 500 | 75% | 0% | -75 [-79, -71] | 376 / 0 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: grammar vs verbose | 500 | 75% | 81% | +6 [+2, +10] | 46 / 76 | 0.008 | 0.086 |
| LFM2.5-1.2B | lora: verbose2 vs verbose | 500 | 99% | 99% | -0 [-1, +1] | 4 / 3 | 1.000 | 1.000 |
| LFM2.5-1.2B | lora: compact vs verbose | 500 | 99% | 99% | +0 [-1, +1] | 2 / 3 | 1.000 | 1.000 |
| LFM2.5-1.2B | lora: grammar vs verbose | 500 | 99% | 93% | -6 [-8, -4] | 33 / 4 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at verbose | 500 | 85% | 98% | +13 [+10, +16] | 8 / 72 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at verbose2 | 500 | 89% | 94% | +5 [+1, +8] | 23 / 47 | 0.006 | 0.067 |
| granite-4.2-3b | adapter at compact | 500 | 0% | 100% | +100 [+99, +100] | 0 / 498 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at grammar | 500 | 93% | 97% | +4 [+1, +7] | 16 / 36 | 0.008 | 0.086 |
| granite-4.2-3b | base: verbose2 vs verbose | 500 | 85% | 89% | +4 [+0, +8] | 38 / 58 | 0.052 | 0.415 |
| granite-4.2-3b | base: compact vs verbose | 500 | 85% | 0% | -85 [-88, -82] | 426 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | base: grammar vs verbose | 500 | 85% | 93% | +7 [+5, +10] | 9 / 46 | <0.001 | <0.001 * |
| granite-4.2-3b | lora: verbose2 vs verbose | 500 | 98% | 94% | -4 [-7, -2] | 29 / 9 | 0.002 | 0.022 * |
| granite-4.2-3b | lora: compact vs verbose | 500 | 98% | 100% | +2 [+0, +3] | 2 / 10 | 0.039 | 0.347 |
| granite-4.2-3b | lora: grammar vs verbose | 500 | 98% | 97% | -1 [-3, +1] | 17 / 10 | 0.248 | 1.000 |
| gemma-4-E2B | adapter at verbose | 500 | 95% | 88% | -7 [-10, -4] | 57 / 22 | <0.001 | 0.002 * |
| gemma-4-E2B | adapter at verbose2 | 500 | 87% | 89% | +2 [-1, +5] | 25 / 34 | 0.298 | 1.000 |
| gemma-4-E2B | adapter at compact | 500 | 18% | 100% | +82 [+78, +85] | 0 / 410 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at grammar | 500 | 95% | 80% | -15 [-19, -11] | 101 / 26 | <0.001 | <0.001 * |
| gemma-4-E2B | base: verbose2 vs verbose | 500 | 95% | 87% | -9 [-12, -5] | 59 / 16 | <0.001 | <0.001 * |
| gemma-4-E2B | base: compact vs verbose | 500 | 95% | 18% | -77 [-81, -73] | 394 / 7 | <0.001 | <0.001 * |
| gemma-4-E2B | base: grammar vs verbose | 500 | 95% | 95% | -1 [-3, +2] | 18 / 15 | 0.728 | 1.000 |
| gemma-4-E2B | lora: verbose2 vs verbose | 500 | 88% | 89% | +0 [-4, +4] | 44 / 45 | 1.000 | 1.000 |
| gemma-4-E2B | lora: compact vs verbose | 500 | 88% | 100% | +12 [+9, +14] | 0 / 58 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: grammar vs verbose | 500 | 88% | 80% | -9 [-14, -4] | 101 / 58 | <0.001 | 0.011 * |

### reference-correct

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| LFM2.5-1.2B | adapter at verbose | 500 | 34% | 49% | +15 [+11, +19] | 23 / 98 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at verbose2 | 500 | 32% | 42% | +10 [+7, +13] | 9 / 58 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at compact | 500 | 0% | 78% | +78 [+75, +82] | 0 / 392 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at grammar | 500 | 24% | 44% | +20 [+15, +25] | 45 / 144 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: verbose2 vs verbose | 500 | 34% | 32% | -2 [-7, +3] | 92 / 80 | 0.402 | 1.000 |
| LFM2.5-1.2B | base: compact vs verbose | 500 | 34% | 0% | -34 [-39, -30] | 172 / 0 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: grammar vs verbose | 500 | 34% | 24% | -10 [-14, -7] | 73 / 23 | <0.001 | <0.001 * |
| LFM2.5-1.2B | lora: verbose2 vs verbose | 500 | 49% | 42% | -8 [-13, -2] | 127 / 89 | 0.012 | 0.116 |
| LFM2.5-1.2B | lora: compact vs verbose | 500 | 49% | 78% | +29 [+24, +33] | 16 / 161 | <0.001 | <0.001 * |
| LFM2.5-1.2B | lora: grammar vs verbose | 500 | 49% | 44% | -5 [-11, +0] | 115 / 89 | 0.080 | 0.559 |
| granite-4.2-3b | adapter at verbose | 500 | 45% | 74% | +29 [+24, +35] | 46 / 192 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at verbose2 | 500 | 42% | 63% | +21 [+15, +27] | 81 / 185 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at compact | 500 | 0% | 90% | +90 [+87, +93] | 0 / 451 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at grammar | 500 | 41% | 74% | +33 [+27, +39] | 46 / 212 | <0.001 | <0.001 * |
| granite-4.2-3b | base: verbose2 vs verbose | 500 | 45% | 42% | -3 [-7, +2] | 63 / 50 | 0.259 | 1.000 |
| granite-4.2-3b | base: compact vs verbose | 500 | 45% | 0% | -45 [-49, -40] | 224 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | base: grammar vs verbose | 500 | 45% | 41% | -4 [-7, -1] | 44 / 25 | 0.029 | 0.236 |
| granite-4.2-3b | lora: verbose2 vs verbose | 500 | 74% | 63% | -11 [-15, -7] | 74 / 19 | <0.001 | <0.001 * |
| granite-4.2-3b | lora: compact vs verbose | 500 | 74% | 90% | +16 [+12, +20] | 13 / 94 | <0.001 | <0.001 * |
| granite-4.2-3b | lora: grammar vs verbose | 500 | 74% | 74% | +0 [-3, +4] | 43 / 44 | 1.000 | 1.000 |
| gemma-4-E2B | adapter at verbose | 500 | 42% | 45% | +3 [-1, +8] | 54 / 71 | 0.152 | 0.761 |
| gemma-4-E2B | adapter at verbose2 | 500 | 43% | 49% | +6 [+2, +10] | 30 / 58 | 0.004 | 0.041 * |
| gemma-4-E2B | adapter at compact | 500 | 10% | 68% | +59 [+53, +64] | 48 / 342 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at grammar | 500 | 37% | 27% | -10 [-16, -4] | 146 / 98 | 0.003 | 0.031 * |
| gemma-4-E2B | base: verbose2 vs verbose | 500 | 42% | 43% | +1 [-3, +6] | 57 / 63 | 0.648 | 1.000 |
| gemma-4-E2B | base: compact vs verbose | 500 | 42% | 10% | -32 [-37, -27] | 187 / 25 | <0.001 | <0.001 * |
| gemma-4-E2B | base: grammar vs verbose | 500 | 42% | 37% | -5 [-9, -1] | 60 / 35 | 0.013 | 0.120 |
| gemma-4-E2B | lora: verbose2 vs verbose | 500 | 45% | 49% | +3 [-0, +7] | 38 / 55 | 0.097 | 0.579 |
| gemma-4-E2B | lora: compact vs verbose | 500 | 45% | 68% | +23 [+17, +29] | 100 / 215 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: grammar vs verbose | 500 | 45% | 27% | -18 [-24, -12] | 181 / 91 | <0.001 | <0.001 * |

## Schema validity (valid@1)

Is the whole answer one JSON value that matches its message type's schema, game/schemas/output/<phase>.schema.json?

| condition | model | valid | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | main failures |
|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 258/500 (52%) | 99% | 99% | 12% | 44% | 4% | wrapped 238, not_json 2, schema:type 1 |
| base_verbose | granite-4.2-3b | 499/500 (100%) | 99% | 100% | 100% | 100% | 100% | schema:maxItems 1 |
| base_verbose | gemma-4-E2B | 499/500 (100%) | 99% | 100% | 100% | 100% | 100% | schema:maxItems 1 |
| lora_verbose | LFM2.5-1.2B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_verbose | granite-4.2-3b | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_verbose | gemma-4-E2B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_verbose2 | LFM2.5-1.2B | 481/500 (96%) | 93% | 88% | 100% | 100% | 100% | schema:additionalProperties 12, schema:maxItems 7 |
| base_verbose2 | granite-4.2-3b | 499/500 (100%) | 99% | 100% | 100% | 100% | 100% | schema:maxItems 1 |
| base_verbose2 | gemma-4-E2B | 498/500 (100%) | 99% | 100% | 100% | 99% | 100% | schema:maxItems 1, not_json 1 |
| lora_verbose2 | LFM2.5-1.2B | 499/500 (100%) | 99% | 100% | 100% | 100% | 100% | schema:maxItems 1 |
| lora_verbose2 | granite-4.2-3b | 498/500 (100%) | 98% | 100% | 100% | 100% | 100% | schema:maxItems 1, not_json 1 |
| lora_verbose2 | gemma-4-E2B | 483/500 (97%) | 96% | 99% | 99% | 100% | 89% | schema:additionalProperties 11, schema:maxItems 4, schema:type 1 |
| base_compact | LFM2.5-1.2B | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 500 |
| base_compact | granite-4.2-3b | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 500 |
| base_compact | gemma-4-E2B | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 374, schema:additionalProperties 125, schema:type 1 |
| lora_compact | LFM2.5-1.2B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | granite-4.2-3b | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | gemma-4-E2B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | LFM2.5-1.2B | 484/500 (97%) | 100% | 100% | 84% | 100% | 100% | schema:minItems 16 |
| base_grammar | granite-4.2-3b | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | gemma-4-E2B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_grammar | LFM2.5-1.2B | 469/500 (94%) | 100% | 100% | 69% | 100% | 100% | schema:minItems 31 |
| lora_grammar | granite-4.2-3b | 484/500 (97%) | 100% | 100% | 84% | 100% | 100% | schema:minItems 16 |
| lora_grammar | gemma-4-E2B | 400/500 (80%) | 100% | 100% | 0% | 100% | 100% | schema:minItems 100 |

## Legality

Would the game carry out the answer as the model wrote it?

| condition | model | legal | valid & legal | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | why not legal |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 376/500 (75%) | 36% | 75% | 55% | 99% | 84% | 63% | rules 68, cards_not_held 52, parser 2, no_json 2 |
| base_verbose | granite-4.2-3b | 426/500 (85%) | 85% | 97% | 78% | 100% | 84% | 67% | cards_not_held 49, rules 25 |
| base_verbose | gemma-4-E2B | 477/500 (95%) | 95% | 96% | 96% | 100% | 92% | 93% | cards_not_held 15, rules 8 |
| lora_verbose | LFM2.5-1.2B | 496/500 (99%) | 99% | 100% | 96% | 100% | 100% | 100% | rules 4 |
| lora_verbose | granite-4.2-3b | 490/500 (98%) | 98% | 96% | 94% | 100% | 100% | 100% | rules 10 |
| lora_verbose | gemma-4-E2B | 442/500 (88%) | 88% | 80% | 62% | 100% | 100% | 100% | rules 58 |
| base_verbose2 | LFM2.5-1.2B | 354/500 (71%) | 71% | 2% | 53% | 99% | 100% | 100% | rules 145, cards_not_held 1 |
| base_verbose2 | granite-4.2-3b | 446/500 (89%) | 89% | 85% | 80% | 100% | 83% | 98% | rules 35, cards_not_held 19 |
| base_verbose2 | gemma-4-E2B | 434/500 (87%) | 87% | 57% | 95% | 100% | 82% | 100% | rules 48, cards_not_held 17, no_json 1 |
| lora_verbose2 | LFM2.5-1.2B | 495/500 (99%) | 99% | 99% | 97% | 99% | 100% | 100% | rules 4, cards_not_held 1 |
| lora_verbose2 | granite-4.2-3b | 470/500 (94%) | 94% | 70% | 100% | 100% | 100% | 100% | rules 29, no_json 1 |
| lora_verbose2 | gemma-4-E2B | 443/500 (89%) | 86% | 44% | 100% | 99% | 100% | 100% | rules 56, unknown_player 1 |
| base_compact | LFM2.5-1.2B | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | 0% | no_json 500 |
| base_compact | granite-4.2-3b | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | 0% | no_json 500 |
| base_compact | gemma-4-E2B | 90/500 (18%) | 0% | 0% | 0% | 0% | 85% | 5% | no_json 374, rules 35, parser 1 |
| lora_compact | LFM2.5-1.2B | 497/500 (99%) | 99% | 100% | 97% | 100% | 100% | 100% | rules 3 |
| lora_compact | granite-4.2-3b | 498/500 (100%) | 100% | 100% | 100% | 98% | 100% | 100% | cards_not_held 2 |
| lora_compact | gemma-4-E2B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | LFM2.5-1.2B | 406/500 (81%) | 81% | 100% | 98% | 79% | 64% | 65% | cards_not_held 76, no_cards 16, rules 2 |
| base_grammar | granite-4.2-3b | 463/500 (93%) | 93% | 100% | 98% | 100% | 87% | 78% | cards_not_held 35, rules 2 |
| base_grammar | gemma-4-E2B | 474/500 (95%) | 95% | 100% | 100% | 100% | 85% | 89% | cards_not_held 26 |
| lora_grammar | LFM2.5-1.2B | 467/500 (93%) | 93% | 100% | 98% | 69% | 100% | 100% | no_cards 31, rules 2 |
| lora_grammar | granite-4.2-3b | 483/500 (97%) | 97% | 100% | 99% | 84% | 100% | 100% | no_cards 16, rules 1 |
| lora_grammar | gemma-4-E2B | 399/500 (80%) | 80% | 100% | 99% | 0% | 100% | 100% | no_cards 100, rules 1 |

## Reference decisions

Does the answer make the decision a simple, value-aware rule set makes?

| condition | model | correct (95% CI) | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | teacher match |
|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 34% [30–39] | 20% | 1% | 82% | 39% | 30% | – |
| base_verbose | granite-4.2-3b | 45% [40–49] | 40% | 9% | 100% | 41% | 34% | – |
| base_verbose | gemma-4-E2B | 42% [38–46] | 33% | 3% | 75% | 48% | 51% | – |
| lora_verbose | LFM2.5-1.2B | 49% [45–54] | 39% | 15% | 83% | 60% | 50% | – |
| lora_verbose | granite-4.2-3b | 74% [70–78] | 50% | 79% | 97% | 94% | 50% | – |
| lora_verbose | gemma-4-E2B | 45% [41–50] | 30% | 10% | 82% | 55% | 50% | – |
| base_verbose2 | LFM2.5-1.2B | 32% [28–36] | 0% | 2% | 58% | 50% | 50% | – |
| base_verbose2 | granite-4.2-3b | 42% [38–47] | 36% | 24% | 65% | 36% | 50% | – |
| base_verbose2 | gemma-4-E2B | 43% [39–48] | 23% | 7% | 100% | 35% | 51% | – |
| lora_verbose2 | LFM2.5-1.2B | 42% [38–46] | 25% | 7% | 77% | 50% | 50% | – |
| lora_verbose2 | granite-4.2-3b | 63% [59–67] | 42% | 50% | 88% | 83% | 52% | – |
| lora_verbose2 | gemma-4-E2B | 49% [44–53] | 21% | 14% | 95% | 63% | 51% | – |
| base_compact | LFM2.5-1.2B | 0% [0–1] | 0% | 0% | 0% | 0% | 0% | – |
| base_compact | granite-4.2-3b | 0% [0–1] | 0% | 0% | 0% | 0% | 0% | – |
| base_compact | gemma-4-E2B | 10% [7–12] | 0% | 0% | 0% | 45% | 3% | – |
| lora_compact | LFM2.5-1.2B | 78% [75–82] | 72% | 90% | 99% | 81% | 50% | – |
| lora_compact | granite-4.2-3b | 90% [87–93] | 65% | 96% | 98% | 94% | 98% | – |
| lora_compact | gemma-4-E2B | 68% [64–72] | 65% | 84% | 100% | 43% | 50% | – |
| base_grammar | LFM2.5-1.2B | 24% [21–28] | 22% | 6% | 48% | 15% | 31% | – |
| base_grammar | granite-4.2-3b | 41% [37–45] | 22% | 7% | 100% | 37% | 39% | – |
| base_grammar | gemma-4-E2B | 37% [33–41] | 20% | 6% | 74% | 38% | 47% | – |
| lora_grammar | LFM2.5-1.2B | 44% [40–49] | 31% | 29% | 57% | 56% | 48% | – |
| lora_grammar | granite-4.2-3b | 74% [70–78] | 64% | 69% | 84% | 88% | 66% | – |
| lora_grammar | gemma-4-E2B | 27% [24–31] | 29% | 8% | 0% | 50% | 50% | – |
| teacher | training corpus | 83% [83–84] | 88% | 99% | 97% | 70% | 62% | – |

Each rule on its own (partial credit):

| condition | model | PLANT: first card placed | PLANT: second card without harvest | FORCE: no avoidable harvest | FORCE: least valuable stack lost | TRADI: keeps growing beans | REPLY: accepts iff useful | REPLY: keeps growing beans | CONSI: accepts iff useful |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 31% | 52% | 19% | 37% | 82% | 45% | 71% | 30% |
| base_verbose | granite-4.2-3b | 40% | 97% | 34% | 53% | 100% | 44% | 73% | 34% |
| base_verbose | gemma-4-E2B | 38% | 80% | 50% | 49% | 75% | 54% | 86% | 51% |
| lora_verbose | LFM2.5-1.2B | 40% | 96% | 51% | 60% | 83% | 60% | 100% | 50% |
| lora_verbose | granite-4.2-3b | 68% | 68% | 90% | 83% | 97% | 94% | 100% | 50% |
| lora_verbose | gemma-4-E2B | 41% | 58% | 38% | 34% | 82% | 56% | 99% | 50% |
| base_verbose2 | LFM2.5-1.2B | 0% | 2% | 30% | 25% | 58% | 50% | 100% | 50% |
| base_verbose2 | granite-4.2-3b | 37% | 84% | 56% | 48% | 65% | 44% | 63% | 50% |
| base_verbose2 | gemma-4-E2B | 32% | 33% | 51% | 51% | 100% | 43% | 73% | 51% |
| lora_verbose2 | LFM2.5-1.2B | 43% | 60% | 51% | 53% | 77% | 50% | 100% | 50% |
| lora_verbose2 | granite-4.2-3b | 53% | 51% | 75% | 75% | 88% | 83% | 100% | 52% |
| lora_verbose2 | gemma-4-E2B | 24% | 32% | 62% | 52% | 95% | 63% | 100% | 51% |
| base_compact | LFM2.5-1.2B | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| base_compact | granite-4.2-3b | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| base_compact | gemma-4-E2B | 0% | 0% | 0% | 0% | 0% | 45% | 85% | 3% |
| lora_compact | LFM2.5-1.2B | 72% | 99% | 93% | 94% | 99% | 85% | 96% | 50% |
| lora_compact | granite-4.2-3b | 72% | 92% | 100% | 96% | 98% | 100% | 94% | 98% |
| lora_compact | gemma-4-E2B | 72% | 92% | 89% | 95% | 100% | 50% | 93% | 50% |
| base_grammar | LFM2.5-1.2B | 42% | 29% | 52% | 52% | 48% | 32% | 39% | 31% |
| base_grammar | granite-4.2-3b | 36% | 34% | 53% | 52% | 100% | 47% | 65% | 39% |
| base_grammar | gemma-4-E2B | 40% | 28% | 54% | 52% | 74% | 47% | 68% | 47% |
| lora_grammar | LFM2.5-1.2B | 61% | 53% | 61% | 66% | 57% | 56% | 100% | 48% |
| lora_grammar | granite-4.2-3b | 74% | 82% | 92% | 76% | 84% | 88% | 100% | 66% |
| lora_grammar | gemma-4-E2B | 45% | 61% | 55% | 52% | 0% | 50% | 100% | 50% |
| teacher | training corpus | 89% | 99% | 100% | 100% | 97% | 75% | 95% | 62% |

## State sensitivity

Does the decision depend on the game state?

| condition | model | REPLY accepts useful / useless | gap | CONSIDERING accepts useful / useless | gap | PLANTING avoidable harvests | FORCED avoidable harvests | TRADING passes | offers giving away a growing bean |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 49% / 42% | +7 | 100% / 100% | +0 | 45/75 (60%) | 36/55 (65%) | 0% | 17/99 (17%) |
| base_verbose | granite-4.2-3b | 28% / 25% | +3 | 12% / 9% | +3 | 29/97 (30%) | 44/78 (56%) | 100% | – |
| base_verbose | gemma-4-E2B | 51% / 34% | +17 | 38% / 29% | +9 | 37/96 (39%) | 46/96 (48%) | 0% | 25/100 (25%) |
| lora_verbose | LFM2.5-1.2B | 84% / 64% | +20 | 94% / 94% | +0 | 35/100 (35%) | 45/96 (47%) | 0% | 17/100 (17%) |
| lora_verbose | granite-4.2-3b | 90% / 2% | +88 | 100% / 100% | +0 | 29/96 (30%) | 4/94 (4%) | 0% | 3/100 (3%) |
| lora_verbose | gemma-4-E2B | 14% / 2% | +12 | 2% / 2% | +0 | 32/80 (40%) | 24/62 (39%) | 14% | 18/86 (21%) |
| base_verbose2 | LFM2.5-1.2B | 0% / 0% | +0 | 0% / 0% | +0 | 2/2 (100%) | 23/53 (43%) | 0% | 41/99 (41%) |
| base_verbose2 | granite-4.2-3b | 2% / 0% | +2 | 0% / 0% | +0 | 22/85 (26%) | 24/80 (30%) | 0% | 35/100 (35%) |
| base_verbose2 | gemma-4-E2B | 17% / 12% | +5 | 12% / 10% | +2 | 32/57 (56%) | 44/95 (46%) | 90% | 0/10 (0%) |
| lora_verbose2 | LFM2.5-1.2B | 0% / 0% | +0 | 0% / 0% | +0 | 66/99 (67%) | 46/97 (47%) | 0% | 22/99 (22%) |
| lora_verbose2 | granite-4.2-3b | 80% / 14% | +66 | 98% / 94% | +4 | 21/70 (30%) | 25/100 (25%) | 0% | 12/100 (12%) |
| lora_verbose2 | gemma-4-E2B | 54% / 28% | +26 | 8% / 6% | +2 | 17/44 (39%) | 38/100 (38%) | 84% | 4/16 (25%) |
| base_compact | LFM2.5-1.2B | – / – | – | – / – | – | – | – | – | – |
| base_compact | granite-4.2-3b | – / – | – | – / – | – | – | – | – | – |
| base_compact | gemma-4-E2B | 0% / 0% | +0 | 0% / 0% | +0 | – | – | – | – |
| lora_compact | LFM2.5-1.2B | 100% / 30% | +70 | 100% / 100% | +0 | 1/100 (1%) | 4/97 (4%) | 0% | 1/100 (1%) |
| lora_compact | granite-4.2-3b | 100% / 0% | +100 | 98% / 2% | +96 | 8/100 (8%) | 0/100 (0%) | 0% | 0/98 (0%) |
| lora_compact | gemma-4-E2B | 100% / 100% | +0 | 100% / 100% | +0 | 8/100 (8%) | 11/100 (11%) | 0% | 0/100 (0%) |
| base_grammar | LFM2.5-1.2B | 100% / 100% | +0 | 100% / 97% | +3 | 77/100 (77%) | 46/98 (47%) | 0% | 31/79 (39%) |
| base_grammar | granite-4.2-3b | 2% / 2% | +0 | 10% / 5% | +4 | 72/100 (72%) | 45/98 (46%) | 100% | – |
| base_grammar | gemma-4-E2B | 10% / 4% | +6 | 7% / 2% | +5 | 79/100 (79%) | 46/100 (46%) | 0% | 26/100 (26%) |
| lora_grammar | LFM2.5-1.2B | 12% / 0% | +12 | 44% / 48% | -4 | 53/100 (53%) | 37/98 (38%) | 0% | 12/69 (17%) |
| lora_grammar | granite-4.2-3b | 98% / 22% | +76 | 100% / 68% | +32 | 19/100 (19%) | 7/99 (7%) | 0% | 0/84 (0%) |
| lora_grammar | gemma-4-E2B | 100% / 100% | +0 | 88% / 88% | +0 | 56/100 (56%) | 44/99 (44%) | – | – |
| teacher | training corpus | 100% / 41% | +59 | 100% / 45% | +55 | 26/3000 (1%) | 9/3000 (0%) | 23% | 132/2309 (6%) |

## Agreement

Given the same item, do two settings make the same decision?

Same decision on the same item (95% CI; compared items in brackets).

| LFM2.5-1.2B | base_verbose | lora_verbose | base_verbose2 | lora_verbose2 | base_compact | lora_compact | base_grammar | lora_grammar |
|---|---|---|---|---|---|---|---|---|
| base_verbose | · | 31% [27–35] (496) | 12% [10–15] (496) | 20% [16–23] (496) | – (0) | 4% [3–6] (496) | 26% [23–30] (496) | 11% [9–15] (496) |
| lora_verbose | 31% [27–35] (496) | · | 11% [9–14] (500) | 21% [18–25] (500) | – (0) | 32% [28–36] (500) | 6% [4–9] (500) | 25% [21–29] (500) |
| base_verbose2 | 12% [10–15] (496) | 11% [9–14] (500) | · | 49% [44–53] (500) | – (0) | 8% [6–11] (500) | 10% [7–13] (500) | 34% [30–38] (500) |
| lora_verbose2 | 20% [16–23] (496) | 21% [18–25] (500) | 49% [44–53] (500) | · | – (0) | 11% [8–14] (500) | 14% [11–17] (500) | 41% [37–45] (500) |
| base_compact | – (0) | – (0) | – (0) | – (0) | · | – (0) | – (0) | – (0) |
| lora_compact | 4% [3–6] (496) | 32% [28–36] (500) | 8% [6–11] (500) | 11% [8–14] (500) | – (0) | · | 4% [3–6] (500) | 26% [23–30] (500) |
| base_grammar | 26% [23–30] (496) | 6% [4–9] (500) | 10% [7–13] (500) | 14% [11–17] (500) | – (0) | 4% [3–6] (500) | · | 16% [13–19] (500) |
| lora_grammar | 11% [9–15] (496) | 25% [21–29] (500) | 34% [30–38] (500) | 41% [37–45] (500) | – (0) | 26% [23–30] (500) | 16% [13–19] (500) | · |

| granite-4.2-3b | base_verbose | lora_verbose | base_verbose2 | lora_verbose2 | base_compact | lora_compact | base_grammar | lora_grammar |
|---|---|---|---|---|---|---|---|---|
| base_verbose | · | 8% [6–11] (500) | 29% [26–34] (500) | 7% [5–9] (499) | – (0) | 10% [8–13] (500) | 43% [39–48] (500) | 9% [7–12] (500) |
| lora_verbose | 8% [6–11] (500) | · | 9% [7–12] (500) | 52% [47–56] (499) | – (0) | 42% [38–47] (500) | 6% [4–8] (500) | 63% [58–67] (500) |
| base_verbose2 | 29% [26–34] (500) | 9% [7–12] (500) | · | 9% [7–12] (499) | – (0) | 12% [9–15] (500) | 11% [8–14] (500) | 10% [7–13] (500) |
| lora_verbose2 | 7% [5–9] (499) | 52% [47–56] (499) | 9% [7–12] (499) | · | – (0) | 36% [32–40] (499) | 11% [9–15] (499) | 53% [49–57] (499) |
| base_compact | – (0) | – (0) | – (0) | – (0) | · | – (0) | – (0) | – (0) |
| lora_compact | 10% [8–13] (500) | 42% [38–47] (500) | 12% [9–15] (500) | 36% [32–40] (499) | – (0) | · | 2% [1–4] (500) | 49% [44–53] (500) |
| base_grammar | 43% [39–48] (500) | 6% [4–8] (500) | 11% [8–14] (500) | 11% [9–15] (499) | – (0) | 2% [1–4] (500) | · | 7% [5–10] (500) |
| lora_grammar | 9% [7–12] (500) | 63% [58–67] (500) | 10% [7–13] (500) | 53% [49–57] (499) | – (0) | 49% [44–53] (500) | 7% [5–10] (500) | · |

| gemma-4-E2B | base_verbose | lora_verbose | base_verbose2 | lora_verbose2 | base_compact | lora_compact | base_grammar | lora_grammar |
|---|---|---|---|---|---|---|---|---|
| base_verbose | · | 18% [15–22] (500) | 30% [26–34] (499) | 20% [17–24] (500) | 0% [0–3] (125) | 8% [6–11] (500) | 45% [40–49] (500) | 28% [24–32] (500) |
| lora_verbose | 18% [15–22] (500) | · | 18% [15–22] (499) | 45% [40–49] (500) | 56% [47–64] (125) | 13% [10–16] (500) | 18% [15–21] (500) | 26% [22–30] (500) |
| base_verbose2 | 30% [26–34] (499) | 18% [15–22] (499) | · | 38% [34–42] (499) | 2% [0–6] (124) | 7% [5–10] (499) | 30% [26–34] (499) | 21% [18–25] (499) |
| lora_verbose2 | 20% [17–24] (500) | 45% [40–49] (500) | 38% [34–42] (499) | · | 41% [33–50] (125) | 8% [6–10] (500) | 21% [17–24] (500) | 30% [26–34] (500) |
| base_compact | 0% [0–3] (125) | 56% [47–64] (125) | 2% [0–6] (124) | 41% [33–50] (125) | · | 0% [0–3] (125) | 0% [0–3] (125) | 0% [0–3] (125) |
| lora_compact | 8% [6–11] (500) | 13% [10–16] (500) | 7% [5–10] (499) | 8% [6–10] (500) | 0% [0–3] (125) | · | 3% [2–5] (500) | 24% [21–28] (500) |
| base_grammar | 45% [40–49] (500) | 18% [15–21] (500) | 30% [26–34] (499) | 21% [17–24] (500) | 0% [0–3] (125) | 3% [2–5] (500) | · | 21% [18–25] (500) |
| lora_grammar | 28% [24–32] (500) | 26% [22–30] (500) | 21% [18–25] (499) | 30% [26–34] (500) | 0% [0–3] (125) | 24% [21–28] (500) | 21% [18–25] (500) | · |

# replay_20261029_gen2: held-out training states

replay run, backend gpu; 492 answers per model and condition; training corpus `training/corpus/training_data_synct_15000_llm.txt`; evaluated 2026-11-12 13:11. Shares in brackets are 95% Wilson intervals.

## Overview

| condition | model | answers | schema-valid | legal | reference-correct | accept gap useful−useless | avoidable harvests |
|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 492 | 51% [47–56] | 66% [62–70] | 30% [26–34] | -2 | 73% |
| base_verbose | granite-4.2-3b | 492 | 99% [98–100] | 78% [74–82] | 43% [39–48] | -6 | 43% |
| base_verbose | gemma-4-E2B | 492 | 95% [93–97] | 86% [82–88] | 39% [34–43] | +7 | 39% |
| lora_verbose | LFM2.5-1.2B | 492 | 100% [99–100] | 97% [95–98] | 49% [45–53] | +14 | 41% |
| lora_verbose | granite-4.2-3b | 492 | 100% [99–100] | 97% [95–98] | 69% [64–73] | +36 | 21% |
| lora_verbose | gemma-4-E2B | 492 | 100% [99–100] | 95% [93–97] | 56% [51–60] | +8 | 35% |
| base_verbose2 | LFM2.5-1.2B | 492 | 92% [89–94] | 65% [61–70] | 35% [31–40] | +0 | 32% |
| base_verbose2 | granite-4.2-3b | 492 | 97% [95–98] | 82% [78–85] | 41% [37–45] | +0 | 39% |
| base_verbose2 | gemma-4-E2B | 492 | 99% [97–99] | 82% [78–85] | 48% [44–52] | -2 | 37% |
| lora_verbose2 | LFM2.5-1.2B | 492 | 100% [99–100] | 96% [94–98] | 46% [42–50] | +0 | 55% |
| lora_verbose2 | granite-4.2-3b | 492 | 99% [98–100] | 94% [92–96] | 64% [60–69] | +37 | 16% |
| lora_verbose2 | gemma-4-E2B | 492 | 98% [97–99] | 88% [85–90] | 60% [55–64] | +21 | 19% |
| base_compact | LFM2.5-1.2B | 492 | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| base_compact | granite-4.2-3b | 492 | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| base_compact | gemma-4-E2B | 492 | 0% [0–1] | 11% [9–14] | 6% [4–8] | +0 | – |
| lora_compact | LFM2.5-1.2B | 492 | 100% [99–100] | 99% [97–99] | 77% [73–80] | +37 | 0% |
| lora_compact | granite-4.2-3b | 492 | 100% [99–100] | 100% [99–100] | 91% [88–93] | +90 | 1% |
| lora_compact | gemma-4-E2B | 492 | 100% [99–100] | 100% [99–100] | 71% [66–74] | +4 | 2% |
| base_grammar | LFM2.5-1.2B | 492 | 100% [99–100] | 76% [72–80] | 23% [20–27] | -2 | 63% |
| base_grammar | granite-4.2-3b | 492 | 100% [99–100] | 90% [87–92] | 42% [38–47] | -3 | 62% |
| base_grammar | gemma-4-E2B | 492 | 100% [99–100] | 93% [90–95] | 38% [34–42] | +6 | 56% |
| lora_grammar | LFM2.5-1.2B | 492 | 96% [93–97] | 93% [90–95] | 51% [46–55] | +14 | 43% |
| lora_grammar | granite-4.2-3b | 492 | 96% [94–97] | 95% [93–97] | 68% [63–72] | +32 | 13% |
| lora_grammar | gemma-4-E2B | 492 | 80% [76–83] | 79% [75–82] | 32% [28–36] | +14 | 46% |

## Effects

How much do the adapter and the prompt style change an outcome, item by item?

Rows marked * stay significant after the Holm correction.

### schema-valid

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| LFM2.5-1.2B | adapter at verbose | 492 | 51% | 100% | +49 [+45, +53] | 0 / 240 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at verbose2 | 492 | 92% | 100% | +8 [+6, +10] | 1 / 40 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at compact | 492 | 0% | 100% | +100 [+100, +100] | 0 / 492 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at grammar | 492 | 100% | 96% | -4 [-6, -3] | 21 / 0 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: verbose2 vs verbose | 492 | 51% | 92% | +40 [+35, +46] | 35 / 234 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: compact vs verbose | 492 | 51% | 0% | -51 [-55, -47] | 252 / 0 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: grammar vs verbose | 492 | 51% | 100% | +49 [+44, +53] | 0 / 239 | <0.001 | <0.001 * |
| LFM2.5-1.2B | lora: verbose2 vs verbose | 492 | 100% | 100% | -0 [-1, +0] | 2 / 0 | 0.500 | 1.000 |
| LFM2.5-1.2B | lora: compact vs verbose | 492 | 100% | 100% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| LFM2.5-1.2B | lora: grammar vs verbose | 492 | 100% | 96% | -4 [-7, -3] | 22 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at verbose | 492 | 99% | 100% | +1 [+0, +2] | 0 / 5 | 0.062 | 0.500 |
| granite-4.2-3b | adapter at verbose2 | 492 | 97% | 99% | +2 [+1, +4] | 3 / 14 | 0.013 | 0.140 |
| granite-4.2-3b | adapter at compact | 492 | 0% | 100% | +100 [+100, +100] | 0 / 492 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at grammar | 492 | 100% | 96% | -4 [-6, -2] | 20 / 1 | <0.001 | <0.001 * |
| granite-4.2-3b | base: verbose2 vs verbose | 492 | 99% | 97% | -2 [-4, -1] | 13 / 3 | 0.021 | 0.213 |
| granite-4.2-3b | base: compact vs verbose | 492 | 99% | 0% | -99 [-100, -98] | 487 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | base: grammar vs verbose | 492 | 99% | 100% | +1 [-0, +2] | 1 / 5 | 0.219 | 1.000 |
| granite-4.2-3b | lora: verbose2 vs verbose | 492 | 100% | 99% | -1 [-2, -0] | 4 / 0 | 0.125 | 0.875 |
| granite-4.2-3b | lora: compact vs verbose | 492 | 100% | 100% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| granite-4.2-3b | lora: grammar vs verbose | 492 | 100% | 96% | -4 [-6, -2] | 20 / 0 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at verbose | 492 | 95% | 100% | +4 [+3, +7] | 1 / 23 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at verbose2 | 492 | 99% | 98% | -0 [-2, +1] | 8 / 7 | 1.000 | 1.000 |
| gemma-4-E2B | adapter at compact | 492 | 0% | 100% | +100 [+100, +100] | 0 / 492 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at grammar | 492 | 100% | 80% | -20 [-23, -16] | 98 / 0 | <0.001 | <0.001 * |
| gemma-4-E2B | base: verbose2 vs verbose | 492 | 95% | 99% | +3 [+1, +5] | 4 / 20 | 0.002 | 0.019 * |
| gemma-4-E2B | base: compact vs verbose | 492 | 95% | 0% | -95 [-97, -93] | 469 / 0 | <0.001 | <0.001 * |
| gemma-4-E2B | base: grammar vs verbose | 492 | 95% | 100% | +4 [+2, +6] | 2 / 23 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: verbose2 vs verbose | 492 | 100% | 98% | -1 [-3, -0] | 8 / 1 | 0.039 | 0.352 |
| gemma-4-E2B | lora: compact vs verbose | 492 | 100% | 100% | +0 [+0, +1] | 0 / 1 | 1.000 | 1.000 |
| gemma-4-E2B | lora: grammar vs verbose | 492 | 100% | 80% | -20 [-24, -17] | 100 / 1 | <0.001 | <0.001 * |

### legal

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| LFM2.5-1.2B | adapter at verbose | 492 | 66% | 97% | +31 [+27, +35] | 1 / 154 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at verbose2 | 492 | 65% | 96% | +31 [+27, +35] | 2 / 154 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at compact | 492 | 0% | 99% | +99 [+98, +100] | 0 / 486 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at grammar | 492 | 76% | 93% | +17 [+13, +21] | 18 / 102 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: verbose2 vs verbose | 492 | 66% | 65% | -0 [-6, +4] | 82 / 80 | 0.937 | 1.000 |
| LFM2.5-1.2B | base: compact vs verbose | 492 | 66% | 0% | -66 [-70, -62] | 324 / 0 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: grammar vs verbose | 492 | 66% | 76% | +10 [+5, +15] | 43 / 93 | <0.001 | <0.001 * |
| LFM2.5-1.2B | lora: verbose2 vs verbose | 492 | 97% | 96% | -1 [-3, +1] | 15 / 12 | 0.701 | 1.000 |
| LFM2.5-1.2B | lora: compact vs verbose | 492 | 97% | 99% | +2 [+1, +3] | 0 / 9 | 0.004 | 0.027 * |
| LFM2.5-1.2B | lora: grammar vs verbose | 492 | 97% | 93% | -4 [-6, -2] | 26 / 7 | 0.001 | 0.012 * |
| granite-4.2-3b | adapter at verbose | 492 | 78% | 97% | +18 [+14, +22] | 10 / 100 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at verbose2 | 492 | 82% | 94% | +12 [+9, +16] | 20 / 81 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at compact | 492 | 0% | 100% | +100 [+99, +100] | 0 / 491 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at grammar | 492 | 90% | 95% | +5 [+2, +8] | 20 / 46 | 0.002 | 0.015 * |
| granite-4.2-3b | base: verbose2 vs verbose | 492 | 78% | 82% | +3 [-1, +8] | 46 / 63 | 0.125 | 0.500 |
| granite-4.2-3b | base: compact vs verbose | 492 | 78% | 0% | -78 [-82, -75] | 385 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | base: grammar vs verbose | 492 | 78% | 90% | +12 [+8, +15] | 23 / 80 | <0.001 | <0.001 * |
| granite-4.2-3b | lora: verbose2 vs verbose | 492 | 97% | 94% | -2 [-5, +0] | 26 / 14 | 0.081 | 0.403 |
| granite-4.2-3b | lora: compact vs verbose | 492 | 97% | 100% | +3 [+2, +5] | 0 / 16 | <0.001 | <0.001 * |
| granite-4.2-3b | lora: grammar vs verbose | 492 | 97% | 95% | -1 [-4, +1] | 23 / 16 | 0.337 | 1.000 |
| gemma-4-E2B | adapter at verbose | 492 | 86% | 95% | +10 [+6, +13] | 17 / 64 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at verbose2 | 492 | 82% | 88% | +6 [+2, +10] | 25 / 56 | <0.001 | 0.008 * |
| gemma-4-E2B | adapter at compact | 492 | 11% | 100% | +89 [+86, +92] | 0 / 437 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at grammar | 492 | 93% | 79% | -14 [-19, -10] | 102 / 31 | <0.001 | <0.001 * |
| gemma-4-E2B | base: verbose2 vs verbose | 492 | 86% | 82% | -4 [-8, +0] | 60 / 40 | 0.057 | 0.341 |
| gemma-4-E2B | base: compact vs verbose | 492 | 86% | 11% | -74 [-78, -70] | 373 / 7 | <0.001 | <0.001 * |
| gemma-4-E2B | base: grammar vs verbose | 492 | 86% | 93% | +8 [+4, +11] | 26 / 63 | <0.001 | 0.001 * |
| gemma-4-E2B | lora: verbose2 vs verbose | 492 | 95% | 88% | -7 [-11, -4] | 52 / 16 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: compact vs verbose | 492 | 95% | 100% | +5 [+3, +7] | 0 / 24 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: grammar vs verbose | 492 | 95% | 79% | -16 [-21, -12] | 103 / 22 | <0.001 | <0.001 * |

### reference-correct

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| LFM2.5-1.2B | adapter at verbose | 492 | 30% | 49% | +19 [+15, +23] | 22 / 115 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at verbose2 | 492 | 35% | 46% | +11 [+8, +14] | 8 / 60 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at compact | 492 | 0% | 77% | +77 [+73, +80] | 0 / 377 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at grammar | 492 | 23% | 51% | +27 [+22, +33] | 45 / 180 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: verbose2 vs verbose | 492 | 30% | 35% | +5 [+0, +10] | 71 / 97 | 0.053 | 0.481 |
| LFM2.5-1.2B | base: compact vs verbose | 492 | 30% | 0% | -30 [-34, -26] | 148 / 0 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: grammar vs verbose | 492 | 30% | 23% | -7 [-11, -3] | 62 / 28 | <0.001 | 0.005 * |
| LFM2.5-1.2B | lora: verbose2 vs verbose | 492 | 49% | 46% | -3 [-9, +2] | 120 / 105 | 0.351 | 1.000 |
| LFM2.5-1.2B | lora: compact vs verbose | 492 | 49% | 77% | +28 [+23, +32] | 16 / 152 | <0.001 | <0.001 * |
| LFM2.5-1.2B | lora: grammar vs verbose | 492 | 49% | 51% | +2 [-4, +7] | 102 / 110 | 0.631 | 1.000 |
| granite-4.2-3b | adapter at verbose | 492 | 43% | 69% | +25 [+20, +31] | 59 / 184 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at verbose2 | 492 | 41% | 64% | +23 [+17, +29] | 73 / 188 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at compact | 492 | 0% | 91% | +91 [+88, +93] | 0 / 446 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at grammar | 492 | 42% | 68% | +25 [+19, +32] | 70 / 195 | <0.001 | <0.001 * |
| granite-4.2-3b | base: verbose2 vs verbose | 492 | 43% | 41% | -2 [-6, +2] | 58 / 47 | 0.329 | 1.000 |
| granite-4.2-3b | base: compact vs verbose | 492 | 43% | 0% | -43 [-48, -39] | 213 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | base: grammar vs verbose | 492 | 43% | 42% | -1 [-5, +3] | 54 / 49 | 0.694 | 1.000 |
| granite-4.2-3b | lora: verbose2 vs verbose | 492 | 69% | 64% | -4 [-8, -1] | 52 / 31 | 0.028 | 0.275 |
| granite-4.2-3b | lora: compact vs verbose | 492 | 69% | 91% | +22 [+18, +26] | 8 / 116 | <0.001 | <0.001 * |
| granite-4.2-3b | lora: grammar vs verbose | 492 | 69% | 68% | -1 [-5, +3] | 50 / 45 | 0.682 | 1.000 |
| gemma-4-E2B | adapter at verbose | 492 | 39% | 56% | +17 [+13, +22] | 26 / 111 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at verbose2 | 492 | 48% | 60% | +12 [+8, +16] | 25 / 82 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at compact | 492 | 6% | 71% | +65 [+60, +70] | 24 / 342 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at grammar | 492 | 38% | 32% | -6 [-12, +0] | 136 / 106 | 0.062 | 0.497 |
| gemma-4-E2B | base: verbose2 vs verbose | 492 | 39% | 48% | +9 [+5, +14] | 41 / 87 | <0.001 | <0.001 * |
| gemma-4-E2B | base: compact vs verbose | 492 | 39% | 6% | -33 [-37, -29] | 166 / 5 | <0.001 | <0.001 * |
| gemma-4-E2B | base: grammar vs verbose | 492 | 39% | 38% | -1 [-5, +3] | 54 / 51 | 0.845 | 1.000 |
| gemma-4-E2B | lora: verbose2 vs verbose | 492 | 56% | 60% | +4 [-1, +8] | 48 / 66 | 0.111 | 0.777 |
| gemma-4-E2B | lora: compact vs verbose | 492 | 56% | 71% | +15 [+9, +22] | 105 / 177 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: grammar vs verbose | 492 | 56% | 32% | -24 [-30, -18] | 188 / 70 | <0.001 | <0.001 * |

## Schema validity (valid@1)

Is the whole answer one JSON value that matches its message type's schema, game/schemas/output/<phase>.schema.json?

| condition | model | valid | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | main failures |
|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 252/492 (51%) | 87% | 90% | 11% | 31% | 36% | wrapped 213, schema:type 11, schema:maxItems 8 |
| base_verbose | granite-4.2-3b | 487/492 (99%) | 96% | 100% | 100% | 99% | 100% | schema:maxItems 4, schema:enum 1 |
| base_verbose | gemma-4-E2B | 469/492 (95%) | 77% | 100% | 100% | 100% | 100% | schema:maxItems 23 |
| lora_verbose | LFM2.5-1.2B | 492/492 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_verbose | granite-4.2-3b | 492/492 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_verbose | gemma-4-E2B | 491/492 (100%) | 99% | 100% | 100% | 100% | 100% | schema:maxItems 1 |
| base_verbose2 | LFM2.5-1.2B | 451/492 (92%) | 94% | 65% | 100% | 100% | 100% | schema:additionalProperties 35, schema:maxItems 6 |
| base_verbose2 | granite-4.2-3b | 477/492 (97%) | 85% | 100% | 100% | 100% | 100% | schema:maxItems 15 |
| base_verbose2 | gemma-4-E2B | 485/492 (99%) | 93% | 100% | 100% | 100% | 100% | schema:maxItems 7 |
| lora_verbose2 | LFM2.5-1.2B | 490/492 (100%) | 98% | 100% | 100% | 100% | 100% | schema:maxItems 2 |
| lora_verbose2 | granite-4.2-3b | 488/492 (99%) | 96% | 100% | 100% | 100% | 100% | schema:maxItems 4 |
| lora_verbose2 | gemma-4-E2B | 484/492 (98%) | 95% | 99% | 100% | 100% | 98% | schema:maxItems 5, schema:additionalProperties 2, schema:required 1 |
| base_compact | LFM2.5-1.2B | 0/492 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 492 |
| base_compact | granite-4.2-3b | 0/492 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 492 |
| base_compact | gemma-4-E2B | 0/492 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 430, schema:additionalProperties 61, schema:type 1 |
| lora_compact | LFM2.5-1.2B | 492/492 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | granite-4.2-3b | 492/492 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | gemma-4-E2B | 492/492 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | LFM2.5-1.2B | 491/492 (100%) | 100% | 100% | 99% | 100% | 100% | schema:minItems 1 |
| base_grammar | granite-4.2-3b | 491/492 (100%) | 100% | 100% | 100% | 99% | 100% | not_json 1 |
| base_grammar | gemma-4-E2B | 490/492 (100%) | 100% | 100% | 98% | 100% | 100% | schema:minItems 2 |
| lora_grammar | LFM2.5-1.2B | 470/492 (96%) | 100% | 100% | 78% | 100% | 100% | schema:minItems 22 |
| lora_grammar | granite-4.2-3b | 472/492 (96%) | 100% | 100% | 80% | 100% | 100% | schema:minItems 20 |
| lora_grammar | gemma-4-E2B | 392/492 (80%) | 100% | 100% | 0% | 100% | 100% | schema:minItems 100 |

## Legality

Would the game carry out the answer as the model wrote it?

| condition | model | legal | valid & legal | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | why not legal |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 324/492 (66%) | 32% | 63% | 36% | 99% | 74% | 57% | rules 86, cards_not_held 62, parser 14, no_json 6 |
| base_verbose | granite-4.2-3b | 385/492 (78%) | 78% | 95% | 52% | 99% | 74% | 71% | rules 53, cards_not_held 53, parser 1 |
| base_verbose | gemma-4-E2B | 421/492 (86%) | 86% | 67% | 82% | 100% | 91% | 88% | rules 51, cards_not_held 20 |
| lora_verbose | LFM2.5-1.2B | 477/492 (97%) | 97% | 99% | 86% | 100% | 100% | 100% | rules 15 |
| lora_verbose | granite-4.2-3b | 475/492 (97%) | 97% | 92% | 91% | 100% | 100% | 100% | rules 17 |
| lora_verbose | gemma-4-E2B | 468/492 (95%) | 95% | 90% | 86% | 100% | 100% | 100% | rules 24 |
| base_verbose2 | LFM2.5-1.2B | 322/492 (65%) | 65% | 9% | 22% | 99% | 100% | 100% | rules 169, cards_not_held 1 |
| base_verbose2 | granite-4.2-3b | 402/492 (82%) | 82% | 74% | 69% | 100% | 73% | 93% | rules 57, cards_not_held 33 |
| base_verbose2 | gemma-4-E2B | 401/492 (82%) | 82% | 45% | 86% | 100% | 79% | 99% | rules 69, cards_not_held 22 |
| lora_verbose2 | LFM2.5-1.2B | 474/492 (96%) | 96% | 91% | 91% | 100% | 100% | 100% | rules 18 |
| lora_verbose2 | granite-4.2-3b | 463/492 (94%) | 94% | 71% | 100% | 100% | 100% | 100% | rules 29 |
| lora_verbose2 | gemma-4-E2B | 432/492 (88%) | 87% | 43% | 97% | 100% | 100% | 100% | rules 60 |
| base_compact | LFM2.5-1.2B | 0/492 (0%) | 0% | 0% | 0% | 0% | 0% | 0% | no_json 492 |
| base_compact | granite-4.2-3b | 0/492 (0%) | 0% | 0% | 0% | 0% | 0% | 0% | no_json 492 |
| base_compact | gemma-4-E2B | 55/492 (11%) | 0% | 0% | 0% | 0% | 55% | 0% | no_json 430, rules 6, parser 1 |
| lora_compact | LFM2.5-1.2B | 486/492 (99%) | 99% | 100% | 94% | 100% | 100% | 100% | rules 6 |
| lora_compact | granite-4.2-3b | 491/492 (100%) | 100% | 100% | 99% | 100% | 100% | 100% | rules 1 |
| lora_compact | gemma-4-E2B | 492/492 (100%) | 100% | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | LFM2.5-1.2B | 374/492 (76%) | 76% | 100% | 84% | 88% | 50% | 57% | cards_not_held 101, rules 16, no_cards 1 |
| base_grammar | granite-4.2-3b | 442/492 (90%) | 90% | 100% | 88% | 100% | 72% | 89% | cards_not_held 37, rules 12, no_json 1 |
| base_grammar | gemma-4-E2B | 458/492 (93%) | 93% | 100% | 94% | 98% | 87% | 86% | cards_not_held 26, rules 6, no_cards 2 |
| lora_grammar | LFM2.5-1.2B | 458/492 (93%) | 93% | 100% | 89% | 77% | 100% | 100% | no_cards 22, rules 11, cards_not_held 1 |
| lora_grammar | granite-4.2-3b | 468/492 (95%) | 95% | 100% | 96% | 80% | 100% | 100% | no_cards 20, rules 4 |
| lora_grammar | gemma-4-E2B | 387/492 (79%) | 79% | 100% | 95% | 0% | 100% | 100% | no_cards 100, rules 5 |

## Reference decisions

Does the answer make the decision a simple, value-aware rule set makes?

| condition | model | correct (95% CI) | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | teacher match |
|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 30% [26–34] | 10% | 8% | 79% | 32% | 21% | 7% [5–9] |
| base_verbose | granite-4.2-3b | 43% [39–48] | 29% | 16% | 95% | 32% | 45% | 17% [14–21] |
| base_verbose | gemma-4-E2B | 39% [34–43] | 13% | 18% | 59% | 51% | 53% | 12% [10–16] |
| lora_verbose | LFM2.5-1.2B | 49% [45–53] | 33% | 28% | 83% | 63% | 37% | 30% [27–35] |
| lora_verbose | granite-4.2-3b | 69% [64–73] | 46% | 77% | 95% | 91% | 32% | 39% [35–44] |
| lora_verbose | gemma-4-E2B | 56% [51–60] | 34% | 38% | 85% | 56% | 67% | 25% [21–29] |
| base_verbose2 | LFM2.5-1.2B | 35% [31–40] | 4% | 3% | 52% | 50% | 71% | 11% [8–14] |
| base_verbose2 | granite-4.2-3b | 41% [37–45] | 19% | 21% | 69% | 33% | 65% | 10% [8–13] |
| base_verbose2 | gemma-4-E2B | 48% [44–52] | 10% | 30% | 100% | 34% | 67% | 14% [11–17] |
| lora_verbose2 | LFM2.5-1.2B | 46% [42–50] | 13% | 27% | 71% | 50% | 71% | 16% [13–20] |
| lora_verbose2 | granite-4.2-3b | 64% [60–69] | 40% | 63% | 93% | 88% | 36% | 36% [31–40] |
| lora_verbose2 | gemma-4-E2B | 60% [55–64] | 28% | 45% | 97% | 55% | 74% | 27% [23–31] |
| base_compact | LFM2.5-1.2B | 0% [0–1] | 0% | 0% | 0% | 0% | 0% | 0% [0–1] |
| base_compact | granite-4.2-3b | 0% [0–1] | 0% | 0% | 0% | 0% | 0% | 0% [0–1] |
| base_compact | gemma-4-E2B | 6% [4–8] | 0% | 0% | 0% | 29% | 0% | 2% [1–4] |
| lora_compact | LFM2.5-1.2B | 77% [73–80] | 78% | 84% | 99% | 87% | 32% | 50% [46–54] |
| lora_compact | granite-4.2-3b | 91% [88–93] | 78% | 92% | 100% | 96% | 87% | 52% [47–56] |
| lora_compact | gemma-4-E2B | 71% [66–74] | 78% | 90% | 99% | 53% | 29% | 48% [43–52] |
| base_grammar | LFM2.5-1.2B | 23% [20–27] | 12% | 22% | 58% | 5% | 18% | 7% [5–9] |
| base_grammar | granite-4.2-3b | 42% [38–47] | 11% | 24% | 100% | 19% | 59% | 11% [9–14] |
| base_grammar | gemma-4-E2B | 38% [34–42] | 9% | 28% | 63% | 30% | 62% | 11% [8–14] |
| lora_grammar | LFM2.5-1.2B | 51% [46–55] | 31% | 37% | 61% | 62% | 63% | 23% [19–26] |
| lora_grammar | granite-4.2-3b | 68% [63–72] | 66% | 73% | 80% | 81% | 36% | 41% [37–46] |
| lora_grammar | gemma-4-E2B | 32% [28–36] | 24% | 39% | 0% | 53% | 45% | 28% [24–32] |
| teacher | training corpus | 83% [83–84] | 88% | 99% | 97% | 70% | 62% | – |

Each rule on its own (partial credit):

| condition | model | PLANT: first card placed | PLANT: second card without harvest | FORCE: no avoidable harvest | FORCE: least valuable stack lost | TRADI: keeps growing beans | REPLY: accepts iff useful | REPLY: keeps growing beans | CONSI: accepts iff useful |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 15% | 45% | 14% | 30% | 79% | 41% | 63% | 21% |
| base_verbose | granite-4.2-3b | 29% | 95% | 32% | 36% | 95% | 35% | 60% | 45% |
| base_verbose | gemma-4-E2B | 13% | 62% | 56% | 44% | 59% | 52% | 86% | 53% |
| lora_verbose | LFM2.5-1.2B | 33% | 98% | 53% | 61% | 83% | 63% | 100% | 37% |
| lora_verbose | granite-4.2-3b | 70% | 60% | 87% | 81% | 95% | 91% | 100% | 32% |
| lora_verbose | gemma-4-E2B | 40% | 71% | 68% | 56% | 85% | 57% | 98% | 67% |
| base_verbose2 | LFM2.5-1.2B | 5% | 7% | 16% | 9% | 52% | 50% | 100% | 71% |
| base_verbose2 | granite-4.2-3b | 21% | 71% | 50% | 40% | 69% | 37% | 56% | 65% |
| base_verbose2 | gemma-4-E2B | 13% | 29% | 64% | 52% | 100% | 38% | 68% | 67% |
| lora_verbose2 | LFM2.5-1.2B | 31% | 48% | 64% | 54% | 71% | 50% | 100% | 71% |
| lora_verbose2 | granite-4.2-3b | 49% | 53% | 93% | 70% | 93% | 88% | 100% | 36% |
| lora_verbose2 | gemma-4-E2B | 31% | 34% | 85% | 57% | 97% | 55% | 100% | 74% |
| base_compact | LFM2.5-1.2B | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| base_compact | granite-4.2-3b | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| base_compact | gemma-4-E2B | 0% | 0% | 0% | 0% | 0% | 29% | 55% | 0% |
| lora_compact | LFM2.5-1.2B | 78% | 100% | 94% | 84% | 99% | 90% | 96% | 32% |
| lora_compact | granite-4.2-3b | 78% | 99% | 99% | 92% | 100% | 100% | 96% | 87% |
| lora_compact | gemma-4-E2B | 78% | 99% | 98% | 92% | 99% | 55% | 98% | 29% |
| base_grammar | LFM2.5-1.2B | 33% | 29% | 50% | 56% | 58% | 26% | 27% | 18% |
| base_grammar | granite-4.2-3b | 33% | 27% | 56% | 56% | 100% | 32% | 45% | 59% |
| base_grammar | gemma-4-E2B | 29% | 37% | 66% | 56% | 63% | 49% | 55% | 62% |
| lora_grammar | LFM2.5-1.2B | 62% | 50% | 66% | 60% | 61% | 62% | 100% | 63% |
| lora_grammar | granite-4.2-3b | 84% | 80% | 94% | 75% | 80% | 81% | 100% | 36% |
| lora_grammar | gemma-4-E2B | 45% | 57% | 75% | 59% | 0% | 53% | 100% | 45% |
| teacher | training corpus | 89% | 99% | 100% | 100% | 97% | 75% | 95% | 62% |

Teacher match per message type (the decision equals the teacher's held-out answer):

| condition | model | teacher match (95% CI) | PLANTING | FORCED | TRADING | REPLY | CONSIDERING |
|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 7% [5–9] | 8% | 7% | 7% | 10% | 0% |
| base_verbose | granite-4.2-3b | 17% [14–21] | 42% | 11% | 25% | 4% | 2% |
| base_verbose | gemma-4-E2B | 12% [10–16] | 28% | 17% | 4% | 12% | 0% |
| lora_verbose | LFM2.5-1.2B | 30% [27–35] | 44% | 21% | 6% | 27% | 57% |
| lora_verbose | granite-4.2-3b | 39% [35–44] | 38% | 68% | 7% | 27% | 59% |
| lora_verbose | gemma-4-E2B | 25% [21–29] | 32% | 33% | 6% | 22% | 32% |
| base_verbose2 | LFM2.5-1.2B | 11% [8–14] | 4% | 1% | 0% | 21% | 29% |
| base_verbose2 | granite-4.2-3b | 10% [8–13] | 28% | 16% | 4% | 2% | 0% |
| base_verbose2 | gemma-4-E2B | 14% [11–17] | 12% | 26% | 25% | 2% | 4% |
| lora_verbose2 | LFM2.5-1.2B | 16% [13–20] | 8% | 21% | 2% | 21% | 29% |
| lora_verbose2 | granite-4.2-3b | 36% [31–40] | 32% | 49% | 8% | 34% | 57% |
| lora_verbose2 | gemma-4-E2B | 27% [23–31] | 14% | 39% | 21% | 24% | 39% |
| base_compact | LFM2.5-1.2B | 0% [0–1] | 0% | 0% | 0% | 0% | 0% |
| base_compact | granite-4.2-3b | 0% [0–1] | 0% | 0% | 0% | 0% | 0% |
| base_compact | gemma-4-E2B | 2% [1–4] | 0% | 0% | 0% | 11% | 0% |
| lora_compact | LFM2.5-1.2B | 50% [46–54] | 73% | 80% | 7% | 28% | 63% |
| lora_compact | granite-4.2-3b | 52% [47–56] | 73% | 89% | 7% | 31% | 59% |
| lora_compact | gemma-4-E2B | 48% [43–52] | 74% | 84% | 4% | 16% | 61% |
| base_grammar | LFM2.5-1.2B | 7% [5–9] | 10% | 20% | 2% | 1% | 0% |
| base_grammar | granite-4.2-3b | 11% [9–14] | 8% | 20% | 26% | 0% | 1% |
| base_grammar | gemma-4-E2B | 11% [8–14] | 12% | 24% | 5% | 2% | 10% |
| lora_grammar | LFM2.5-1.2B | 23% [19–26] | 21% | 32% | 3% | 24% | 34% |
| lora_grammar | granite-4.2-3b | 41% [37–46] | 46% | 66% | 3% | 33% | 60% |
| lora_grammar | gemma-4-E2B | 28% [24–32] | 18% | 34% | 0% | 29% | 60% |

## State sensitivity

Does the decision depend on the game state?

| condition | model | REPLY accepts useful / useless | gap | CONSIDERING accepts useful / useless | gap | PLANTING avoidable harvests | FORCED avoidable harvests | TRADING passes | offers giving away a growing bean |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 41% / 30% | +11 | 100% / 100% | +0 | 50/63 (79%) | 22/36 (61%) | 0% | 23/99 (23%) |
| base_verbose | granite-4.2-3b | 6% / 15% | -10 | 5% / 7% | -2 | 43/95 (45%) | 20/52 (38%) | 95% | 4/5 (80%) |
| base_verbose | gemma-4-E2B | 30% / 19% | +11 | 29% / 26% | +3 | 32/67 (48%) | 26/82 (32%) | 0% | 44/100 (44%) |
| lora_verbose | LFM2.5-1.2B | 84% / 58% | +26 | 100% / 89% | +11 | 43/99 (43%) | 33/86 (38%) | 0% | 20/100 (20%) |
| lora_verbose | granite-4.2-3b | 92% / 10% | +82 | 100% / 97% | +3 | 34/92 (37%) | 4/91 (4%) | 0% | 8/100 (8%) |
| lora_verbose | gemma-4-E2B | 18% / 4% | +14 | 7% / 8% | -0 | 43/90 (48%) | 18/86 (21%) | 26% | 15/74 (20%) |
| base_verbose2 | LFM2.5-1.2B | 0% / 0% | +0 | 0% / 0% | +0 | 4/9 (44%) | 6/22 (27%) | 0% | 50/99 (51%) |
| base_verbose2 | granite-4.2-3b | 0% / 0% | +0 | 0% / 0% | +0 | 37/74 (50%) | 19/69 (28%) | 0% | 34/100 (34%) |
| base_verbose2 | gemma-4-E2B | 5% / 5% | -0 | 0% / 5% | -5 | 27/45 (60%) | 22/86 (26%) | 91% | 1/9 (11%) |
| lora_verbose2 | LFM2.5-1.2B | 0% / 0% | +0 | 0% / 0% | +0 | 73/91 (80%) | 27/91 (30%) | 0% | 32/100 (32%) |
| lora_verbose2 | granite-4.2-3b | 96% / 20% | +76 | 96% / 89% | +7 | 20/71 (28%) | 7/100 (7%) | 0% | 10/100 (10%) |
| lora_verbose2 | gemma-4-E2B | 52% / 42% | +10 | 26% / 6% | +20 | 14/43 (33%) | 12/97 (12%) | 84% | 3/16 (19%) |
| base_compact | LFM2.5-1.2B | – / – | – | – / – | – | – | – | – | – |
| base_compact | granite-4.2-3b | – / – | – | – / – | – | – | – | – | – |
| base_compact | gemma-4-E2B | 0% / 0% | +0 | – / – | – | – | – | – | – |
| lora_compact | LFM2.5-1.2B | 100% / 20% | +80 | 100% / 97% | +3 | 0/100 (0%) | 0/94 (0%) | 1% | 3/99 (3%) |
| lora_compact | granite-4.2-3b | 100% / 0% | +100 | 100% / 18% | +82 | 1/100 (1%) | 0/99 (0%) | 2% | 1/98 (1%) |
| lora_compact | gemma-4-E2B | 100% / 90% | +10 | 100% / 100% | +0 | 1/100 (1%) | 2/100 (2%) | 4% | 1/96 (1%) |
| base_grammar | LFM2.5-1.2B | 100% / 100% | +0 | 94% / 100% | -6 | 82/100 (82%) | 34/84 (40%) | 0% | 33/88 (38%) |
| base_grammar | granite-4.2-3b | 3% / 9% | -6 | 25% / 17% | +8 | 84/100 (84%) | 32/88 (36%) | 100% | – |
| base_grammar | gemma-4-E2B | 12% / 4% | +8 | 0% / 0% | +0 | 81/100 (81%) | 28/94 (30%) | 0% | 37/98 (38%) |
| lora_grammar | LFM2.5-1.2B | 24% / 0% | +24 | 37% / 26% | +11 | 59/100 (59%) | 23/89 (26%) | 0% | 17/77 (22%) |
| lora_grammar | granite-4.2-3b | 100% / 38% | +62 | 100% / 91% | +9 | 23/100 (23%) | 2/96 (2%) | 0% | 0/80 (0%) |
| lora_grammar | gemma-4-E2B | 100% / 94% | +6 | 96% / 77% | +19 | 69/100 (69%) | 20/95 (21%) | – | – |
| teacher | training corpus | 100% / 41% | +59 | 100% / 45% | +55 | 26/3000 (1%) | 9/3000 (0%) | 23% | 132/2309 (6%) |

## Agreement

Given the same item, do two settings make the same decision?

Same decision on the same item (95% CI; compared items in brackets).

| LFM2.5-1.2B | base_verbose | lora_verbose | base_verbose2 | lora_verbose2 | base_compact | lora_compact | base_grammar | lora_grammar |
|---|---|---|---|---|---|---|---|---|
| base_verbose | · | 30% [26–34] (472) | 13% [10–16] (472) | 21% [18–25] (472) | – (0) | 7% [5–9] (472) | 31% [27–35] (472) | 12% [9–15] (472) |
| lora_verbose | 30% [26–34] (472) | · | 12% [10–15] (492) | 22% [19–26] (492) | – (0) | 35% [31–39] (492) | 12% [10–16] (492) | 28% [24–32] (492) |
| base_verbose2 | 13% [10–16] (472) | 12% [10–15] (492) | · | 46% [41–50] (492) | – (0) | 10% [8–13] (492) | 6% [4–9] (492) | 35% [30–39] (492) |
| lora_verbose2 | 21% [18–25] (472) | 22% [19–26] (492) | 46% [41–50] (492) | · | – (0) | 16% [13–20] (492) | 13% [10–16] (492) | 40% [35–44] (492) |
| base_compact | – (0) | – (0) | – (0) | – (0) | · | – (0) | – (0) | – (0) |
| lora_compact | 7% [5–9] (472) | 35% [31–39] (492) | 10% [8–13] (492) | 16% [13–20] (492) | – (0) | · | 6% [4–8] (492) | 28% [24–32] (492) |
| base_grammar | 31% [27–35] (472) | 12% [10–16] (492) | 6% [4–9] (492) | 13% [10–16] (492) | – (0) | 6% [4–8] (492) | · | 11% [8–14] (492) |
| lora_grammar | 12% [9–15] (472) | 28% [24–32] (492) | 35% [30–39] (492) | 40% [35–44] (492) | – (0) | 28% [24–32] (492) | 11% [8–14] (492) | · |

| granite-4.2-3b | base_verbose | lora_verbose | base_verbose2 | lora_verbose2 | base_compact | lora_compact | base_grammar | lora_grammar |
|---|---|---|---|---|---|---|---|---|
| base_verbose | · | 8% [6–11] (491) | 31% [27–35] (491) | 6% [4–9] (491) | – (0) | 11% [9–14] (491) | 37% [33–41] (490) | 8% [6–10] (491) |
| lora_verbose | 8% [6–11] (491) | · | 9% [7–12] (492) | 55% [51–60] (492) | – (0) | 38% [34–43] (492) | 9% [6–11] (491) | 58% [54–62] (492) |
| base_verbose2 | 31% [27–35] (491) | 9% [7–12] (492) | · | 9% [7–12] (492) | – (0) | 11% [8–14] (492) | 8% [6–10] (491) | 8% [6–10] (492) |
| lora_verbose2 | 6% [4–9] (491) | 55% [51–60] (492) | 9% [7–12] (492) | · | – (0) | 36% [32–40] (492) | 8% [6–11] (491) | 51% [47–56] (492) |
| base_compact | – (0) | – (0) | – (0) | – (0) | · | – (0) | – (0) | – (0) |
| lora_compact | 11% [9–14] (491) | 38% [34–43] (492) | 11% [8–14] (492) | 36% [32–40] (492) | – (0) | · | 6% [4–9] (491) | 45% [40–49] (492) |
| base_grammar | 37% [33–41] (490) | 9% [6–11] (491) | 8% [6–10] (491) | 8% [6–11] (491) | – (0) | 6% [4–9] (491) | · | 8% [6–11] (491) |
| lora_grammar | 8% [6–10] (491) | 58% [54–62] (492) | 8% [6–10] (492) | 51% [47–56] (492) | – (0) | 45% [40–49] (492) | 8% [6–11] (491) | · |

| gemma-4-E2B | base_verbose | lora_verbose | base_verbose2 | lora_verbose2 | base_compact | lora_compact | base_grammar | lora_grammar |
|---|---|---|---|---|---|---|---|---|
| base_verbose | · | 16% [13–20] (492) | 28% [24–32] (492) | 12% [9–15] (492) | 7% [3–16] (61) | 12% [10–15] (492) | 31% [27–35] (492) | 18% [15–21] (492) |
| lora_verbose | 16% [13–20] (492) | · | 24% [20–28] (492) | 46% [42–51] (492) | 66% [53–76] (61) | 20% [17–24] (492) | 22% [19–26] (492) | 34% [30–39] (492) |
| base_verbose2 | 28% [24–32] (492) | 24% [20–28] (492) | · | 33% [29–37] (492) | 0% [0–6] (61) | 10% [7–13] (492) | 26% [22–30] (492) | 18% [15–21] (492) |
| lora_verbose2 | 12% [9–15] (492) | 46% [42–51] (492) | 33% [29–37] (492) | · | 49% [37–61] (61) | 18% [15–22] (492) | 18% [15–22] (492) | 31% [27–35] (492) |
| base_compact | 7% [3–16] (61) | 66% [53–76] (61) | 0% [0–6] (61) | 49% [37–61] (61) | · | 8% [4–18] (61) | 0% [0–6] (61) | 5% [2–13] (61) |
| lora_compact | 12% [10–15] (492) | 20% [17–24] (492) | 10% [7–13] (492) | 18% [15–22] (492) | 8% [4–18] (61) | · | 8% [6–11] (492) | 29% [25–33] (492) |
| base_grammar | 31% [27–35] (492) | 22% [19–26] (492) | 26% [22–30] (492) | 18% [15–22] (492) | 0% [0–6] (61) | 8% [6–11] (492) | · | 18% [15–22] (492) |
| lora_grammar | 18% [15–21] (492) | 34% [30–39] (492) | 18% [15–21] (492) | 31% [27–35] (492) | 5% [2–13] (61) | 29% [25–33] (492) | 18% [15–22] (492) | · |

