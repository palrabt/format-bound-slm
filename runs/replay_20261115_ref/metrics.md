# replay_20261115_ref: game states

replay run, backend gpu; 500 answers per model and condition; training corpus `training/corpus/training_data_reference_15000.txt`; evaluated 2026-11-17 09:25. Shares in brackets are 95% Wilson intervals.

## Overview

| condition | model | answers | schema-valid | legal | valid play | reference-correct | accept gap useful−useless | avoidable harvests |
|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 500 | 52% [47–56] | 75% [71–79] | 34% [30–39] | 9% [7–12] | +3 | 62% |
| base_verbose | granite-4.2-3b | 500 | 100% [99–100] | 85% [82–88] | 45% [40–49] | 14% [12–18] | +2 | 42% |
| base_verbose | gemma-4-E2B | 500 | 100% [99–100] | 95% [93–97] | 42% [38–46] | 7% [5–9] | +13 | 43% |
| lora_verbose | LFM2.5-1.2B | 500 | 100% [99–100] | 94% [92–96] | 42% [38–46] | 24% [20–28] | +0 | 57% |
| lora_verbose | granite-4.2-3b | 500 | 98% [96–99] | 91% [88–93] | 70% [66–74] | 54% [49–58] | +46 | 19% |
| lora_verbose | gemma-4-E2B | 500 | 100% [99–100] | 87% [83–89] | 44% [40–49] | 32% [28–36] | +5 | 33% |
| base_verbose2 | LFM2.5-1.2B | 500 | 96% [94–98] | 71% [67–75] | 32% [28–36] | 21% [17–25] | +0 | 45% |
| base_verbose2 | granite-4.2-3b | 500 | 100% [99–100] | 89% [86–92] | 42% [38–47] | 9% [7–12] | +1 | 28% |
| base_verbose2 | gemma-4-E2B | 500 | 100% [99–100] | 87% [84–89] | 43% [39–48] | 11% [8–14] | +3 | 50% |
| lora_verbose2 | LFM2.5-1.2B | 500 | 100% [99–100] | 97% [96–98] | 43% [38–47] | 23% [20–27] | +0 | 60% |
| lora_verbose2 | granite-4.2-3b | 500 | 98% [97–99] | 88% [85–91] | 67% [63–71] | 47% [42–51] | +55 | 30% |
| lora_verbose2 | gemma-4-E2B | 500 | 81% [77–84] | 72% [68–76] | 27% [23–31] | 12% [10–16] | -6 | 44% |
| base_compact | LFM2.5-1.2B | 500 | 0% [0–1] | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| base_compact | granite-4.2-3b | 500 | 0% [0–1] | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| base_compact | gemma-4-E2B | 500 | 0% [0–1] | 18% [15–22] | 10% [7–12] | 10% [7–12] | +0 | – |
| lora_compact | LFM2.5-1.2B | 500 | 100% [99–100] | 100% [99–100] | 86% [83–89] | 80% [76–83] | +56 | 0% |
| lora_compact | granite-4.2-3b | 500 | 100% [99–100] | 100% [99–100] | 97% [95–98] | 91% [88–93] | +99 | 0% |
| lora_compact | gemma-4-E2B | 500 | 100% [99–100] | 100% [99–100] | 94% [92–96] | 87% [84–90] | +99 | 2% |
| base_grammar | LFM2.5-1.2B | 500 | 97% [95–98] | 81% [78–84] | 24% [21–28] | 2% [1–4] | +1 | 62% |
| base_grammar | granite-4.2-3b | 500 | 100% [99–100] | 93% [90–95] | 41% [37–45] | 12% [9–15] | +3 | 59% |
| base_grammar | gemma-4-E2B | 500 | 100% [99–100] | 95% [92–96] | 37% [33–41] | 6% [4–9] | +5 | 62% |
| lora_grammar | LFM2.5-1.2B | 500 | 88% [85–91] | 87% [84–90] | 34% [30–38] | 25% [22–29] | +0 | 56% |
| lora_grammar | granite-4.2-3b | 500 | 93% [91–95] | 93% [91–95] | 71% [67–75] | 55% [51–60] | +67 | 27% |
| lora_grammar | gemma-4-E2B | 500 | 81% [78–84] | 81% [77–84] | 32% [28–37] | 26% [22–30] | +18 | 47% |

## Effects

How much do the adapter and the prompt style change an outcome, item by item?

Rows marked * stay significant after the Holm correction.

### schema-valid

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| LFM2.5-1.2B | adapter at verbose | 500 | 52% | 100% | +48 [+44, +53] | 0 / 242 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at verbose2 | 500 | 96% | 100% | +4 [+2, +6] | 0 / 19 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at compact | 500 | 0% | 100% | +100 [+100, +100] | 0 / 500 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at grammar | 500 | 97% | 88% | -9 [-12, -6] | 49 / 6 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: verbose2 vs verbose | 500 | 52% | 96% | +45 [+40, +49] | 19 / 242 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: compact vs verbose | 500 | 52% | 0% | -52 [-56, -47] | 258 / 0 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: grammar vs verbose | 500 | 52% | 97% | +45 [+41, +50] | 3 / 229 | <0.001 | <0.001 * |
| LFM2.5-1.2B | lora: verbose2 vs verbose | 500 | 100% | 100% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| LFM2.5-1.2B | lora: compact vs verbose | 500 | 100% | 100% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| LFM2.5-1.2B | lora: grammar vs verbose | 500 | 100% | 88% | -12 [-15, -9] | 59 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at verbose | 500 | 100% | 98% | -2 [-3, -1] | 11 / 1 | 0.006 | 0.070 |
| granite-4.2-3b | adapter at verbose2 | 500 | 100% | 98% | -1 [-3, -0] | 8 / 1 | 0.039 | 0.391 |
| granite-4.2-3b | adapter at compact | 500 | 0% | 100% | +100 [+100, +100] | 0 / 500 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at grammar | 500 | 100% | 93% | -7 [-9, -4] | 33 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | base: verbose2 vs verbose | 500 | 100% | 100% | +0 [-1, +1] | 1 / 1 | 1.000 | 1.000 |
| granite-4.2-3b | base: compact vs verbose | 500 | 100% | 0% | -100 [-100, -99] | 499 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | base: grammar vs verbose | 500 | 100% | 100% | +0 [+0, +1] | 0 / 1 | 1.000 | 1.000 |
| granite-4.2-3b | lora: verbose2 vs verbose | 500 | 98% | 98% | +1 [-1, +2] | 7 / 10 | 0.629 | 1.000 |
| granite-4.2-3b | lora: compact vs verbose | 500 | 98% | 100% | +2 [+1, +4] | 0 / 11 | <0.001 | 0.012 * |
| granite-4.2-3b | lora: grammar vs verbose | 500 | 98% | 93% | -4 [-7, -2] | 29 / 7 | <0.001 | 0.004 * |
| gemma-4-E2B | adapter at verbose | 500 | 100% | 100% | +0 [+0, +1] | 0 / 1 | 1.000 | 1.000 |
| gemma-4-E2B | adapter at verbose2 | 500 | 100% | 81% | -19 [-22, -15] | 95 / 2 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at compact | 500 | 0% | 100% | +100 [+100, +100] | 0 / 500 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at grammar | 500 | 100% | 81% | -19 [-22, -15] | 94 / 0 | <0.001 | <0.001 * |
| gemma-4-E2B | base: verbose2 vs verbose | 500 | 100% | 100% | -0 [-1, +0] | 2 / 1 | 1.000 | 1.000 |
| gemma-4-E2B | base: compact vs verbose | 500 | 100% | 0% | -100 [-100, -99] | 499 / 0 | <0.001 | <0.001 * |
| gemma-4-E2B | base: grammar vs verbose | 500 | 100% | 100% | +0 [+0, +1] | 0 / 1 | 1.000 | 1.000 |
| gemma-4-E2B | lora: verbose2 vs verbose | 500 | 100% | 81% | -19 [-23, -15] | 95 / 0 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: compact vs verbose | 500 | 100% | 100% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| gemma-4-E2B | lora: grammar vs verbose | 500 | 100% | 81% | -19 [-22, -15] | 94 / 0 | <0.001 | <0.001 * |

### legal

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| LFM2.5-1.2B | adapter at verbose | 500 | 75% | 94% | +19 [+15, +23] | 12 / 108 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at verbose2 | 500 | 71% | 97% | +27 [+23, +31] | 3 / 136 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at compact | 500 | 0% | 100% | +100 [+99, +100] | 0 / 499 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at grammar | 500 | 81% | 87% | +6 [+2, +10] | 47 / 76 | 0.011 | 0.113 |
| LFM2.5-1.2B | base: verbose2 vs verbose | 500 | 75% | 71% | -4 [-10, +0] | 95 / 73 | 0.105 | 0.525 |
| LFM2.5-1.2B | base: compact vs verbose | 500 | 75% | 0% | -75 [-79, -71] | 376 / 0 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: grammar vs verbose | 500 | 75% | 81% | +6 [+2, +10] | 46 / 76 | 0.008 | 0.092 |
| LFM2.5-1.2B | lora: verbose2 vs verbose | 500 | 94% | 97% | +3 [+1, +5] | 10 / 25 | 0.017 | 0.150 |
| LFM2.5-1.2B | lora: compact vs verbose | 500 | 94% | 100% | +5 [+3, +7] | 0 / 27 | <0.001 | <0.001 * |
| LFM2.5-1.2B | lora: grammar vs verbose | 500 | 94% | 87% | -7 [-11, -4] | 65 / 28 | <0.001 | 0.002 * |
| granite-4.2-3b | adapter at verbose | 500 | 85% | 91% | +6 [+2, +10] | 40 / 70 | 0.005 | 0.065 |
| granite-4.2-3b | adapter at verbose2 | 500 | 89% | 88% | -1 [-5, +3] | 48 / 44 | 0.755 | 1.000 |
| granite-4.2-3b | adapter at compact | 500 | 0% | 100% | +100 [+99, +100] | 0 / 498 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at grammar | 500 | 93% | 93% | +1 [-3, +4] | 33 / 36 | 0.810 | 1.000 |
| granite-4.2-3b | base: verbose2 vs verbose | 500 | 85% | 89% | +4 [+0, +8] | 38 / 58 | 0.052 | 0.363 |
| granite-4.2-3b | base: compact vs verbose | 500 | 85% | 0% | -85 [-88, -82] | 426 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | base: grammar vs verbose | 500 | 85% | 93% | +7 [+5, +10] | 9 / 46 | <0.001 | <0.001 * |
| granite-4.2-3b | lora: verbose2 vs verbose | 500 | 91% | 88% | -3 [-6, +0] | 35 / 21 | 0.081 | 0.489 |
| granite-4.2-3b | lora: compact vs verbose | 500 | 91% | 100% | +8 [+6, +11] | 1 / 43 | <0.001 | <0.001 * |
| granite-4.2-3b | lora: grammar vs verbose | 500 | 91% | 93% | +2 [-1, +5] | 29 / 39 | 0.275 | 1.000 |
| gemma-4-E2B | adapter at verbose | 500 | 95% | 87% | -9 [-12, -5] | 63 / 19 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at verbose2 | 500 | 87% | 72% | -15 [-19, -10] | 107 / 33 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at compact | 500 | 18% | 100% | +82 [+78, +85] | 0 / 410 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at grammar | 500 | 95% | 81% | -14 [-18, -10] | 96 / 26 | <0.001 | <0.001 * |
| gemma-4-E2B | base: verbose2 vs verbose | 500 | 95% | 87% | -9 [-12, -5] | 59 / 16 | <0.001 | <0.001 * |
| gemma-4-E2B | base: compact vs verbose | 500 | 95% | 18% | -77 [-81, -73] | 394 / 7 | <0.001 | <0.001 * |
| gemma-4-E2B | base: grammar vs verbose | 500 | 95% | 95% | -1 [-3, +2] | 18 / 15 | 0.728 | 1.000 |
| gemma-4-E2B | lora: verbose2 vs verbose | 500 | 87% | 72% | -15 [-20, -10] | 125 / 52 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: compact vs verbose | 500 | 87% | 100% | +13 [+10, +16] | 0 / 67 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: grammar vs verbose | 500 | 87% | 81% | -6 [-11, -1] | 90 / 61 | 0.022 | 0.179 |

### valid-play

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| LFM2.5-1.2B | adapter at verbose | 500 | 34% | 42% | +8 [+3, +12] | 50 / 88 | 0.002 | 0.017 * |
| LFM2.5-1.2B | adapter at verbose2 | 500 | 32% | 43% | +11 [+8, +14] | 4 / 57 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at compact | 500 | 0% | 86% | +86 [+83, +89] | 0 / 432 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at grammar | 500 | 24% | 34% | +9 [+4, +15] | 76 / 123 | 0.001 | 0.013 * |
| LFM2.5-1.2B | base: verbose2 vs verbose | 500 | 34% | 32% | -2 [-7, +3] | 92 / 80 | 0.402 | 1.000 |
| LFM2.5-1.2B | base: compact vs verbose | 500 | 34% | 0% | -34 [-39, -30] | 172 / 0 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: grammar vs verbose | 500 | 34% | 24% | -10 [-14, -7] | 73 / 23 | <0.001 | <0.001 * |
| LFM2.5-1.2B | lora: verbose2 vs verbose | 500 | 42% | 43% | +1 [-2, +3] | 14 / 17 | 0.720 | 1.000 |
| LFM2.5-1.2B | lora: compact vs verbose | 500 | 42% | 86% | +44 [+39, +49] | 18 / 240 | <0.001 | <0.001 * |
| LFM2.5-1.2B | lora: grammar vs verbose | 500 | 42% | 34% | -8 [-12, -5] | 63 / 22 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at verbose | 500 | 45% | 70% | +25 [+20, +30] | 35 / 160 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at verbose2 | 500 | 42% | 67% | +25 [+19, +29] | 38 / 161 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at compact | 500 | 0% | 97% | +97 [+95, +98] | 0 / 483 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at grammar | 500 | 41% | 71% | +30 [+25, +35] | 36 / 187 | <0.001 | <0.001 * |
| granite-4.2-3b | base: verbose2 vs verbose | 500 | 45% | 42% | -3 [-7, +2] | 63 / 50 | 0.259 | 1.000 |
| granite-4.2-3b | base: compact vs verbose | 500 | 45% | 0% | -45 [-49, -40] | 224 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | base: grammar vs verbose | 500 | 45% | 41% | -4 [-7, -1] | 44 / 25 | 0.029 | 0.265 |
| granite-4.2-3b | lora: verbose2 vs verbose | 500 | 70% | 67% | -3 [-7, +1] | 61 / 46 | 0.176 | 1.000 |
| granite-4.2-3b | lora: compact vs verbose | 500 | 70% | 97% | +27 [+23, +31] | 2 / 136 | <0.001 | <0.001 * |
| granite-4.2-3b | lora: grammar vs verbose | 500 | 70% | 71% | +1 [-2, +5] | 41 / 48 | 0.525 | 1.000 |
| gemma-4-E2B | adapter at verbose | 500 | 42% | 44% | +2 [-2, +7] | 53 / 65 | 0.311 | 1.000 |
| gemma-4-E2B | adapter at verbose2 | 500 | 43% | 27% | -16 [-20, -12] | 107 / 27 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at compact | 500 | 10% | 94% | +85 [+81, +88] | 0 / 424 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at grammar | 500 | 37% | 32% | -5 [-9, +0] | 81 / 58 | 0.062 | 0.493 |
| gemma-4-E2B | base: verbose2 vs verbose | 500 | 42% | 43% | +1 [-3, +6] | 57 / 63 | 0.648 | 1.000 |
| gemma-4-E2B | base: compact vs verbose | 500 | 42% | 10% | -32 [-37, -27] | 187 / 25 | <0.001 | <0.001 * |
| gemma-4-E2B | base: grammar vs verbose | 500 | 42% | 37% | -5 [-9, -1] | 60 / 35 | 0.013 | 0.134 |
| gemma-4-E2B | lora: verbose2 vs verbose | 500 | 44% | 27% | -17 [-21, -13] | 104 / 18 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: compact vs verbose | 500 | 44% | 94% | +50 [+45, +54] | 8 / 258 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: grammar vs verbose | 500 | 44% | 32% | -12 [-16, -8] | 84 / 24 | <0.001 | <0.001 * |

### reference-correct

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| LFM2.5-1.2B | adapter at verbose | 500 | 9% | 24% | +15 [+11, +18] | 12 / 86 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at verbose2 | 500 | 21% | 23% | +3 [+1, +4] | 4 / 17 | 0.007 | 0.065 |
| LFM2.5-1.2B | adapter at compact | 500 | 0% | 80% | +80 [+76, +83] | 0 / 399 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at grammar | 500 | 2% | 25% | +23 [+19, +27] | 1 / 116 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: verbose2 vs verbose | 500 | 9% | 21% | +12 [+8, +16] | 25 / 84 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: compact vs verbose | 500 | 9% | 0% | -9 [-12, -7] | 45 / 0 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: grammar vs verbose | 500 | 9% | 2% | -7 [-9, -4] | 43 / 10 | <0.001 | <0.001 * |
| LFM2.5-1.2B | lora: verbose2 vs verbose | 500 | 24% | 23% | -0 [-2, +2] | 15 / 13 | 0.851 | 1.000 |
| LFM2.5-1.2B | lora: compact vs verbose | 500 | 24% | 80% | +56 [+51, +61] | 19 / 299 | <0.001 | <0.001 * |
| LFM2.5-1.2B | lora: grammar vs verbose | 500 | 24% | 25% | +2 [-1, +4] | 15 / 23 | 0.256 | 1.000 |
| granite-4.2-3b | adapter at verbose | 500 | 14% | 54% | +39 [+33, +45] | 51 / 247 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at verbose2 | 500 | 9% | 47% | +37 [+32, +42] | 28 / 215 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at compact | 500 | 0% | 91% | +91 [+88, +93] | 0 / 455 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at grammar | 500 | 12% | 55% | +44 [+38, +49] | 36 / 254 | <0.001 | <0.001 * |
| granite-4.2-3b | base: verbose2 vs verbose | 500 | 14% | 9% | -5 [-8, -2] | 43 / 17 | 0.001 | 0.012 * |
| granite-4.2-3b | base: compact vs verbose | 500 | 14% | 0% | -14 [-18, -11] | 72 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | base: grammar vs verbose | 500 | 14% | 12% | -3 [-5, -1] | 23 / 9 | 0.020 | 0.160 |
| granite-4.2-3b | lora: verbose2 vs verbose | 500 | 54% | 47% | -7 [-11, -3] | 81 / 46 | 0.002 | 0.024 * |
| granite-4.2-3b | lora: compact vs verbose | 500 | 54% | 91% | +37 [+33, +42] | 7 / 194 | <0.001 | <0.001 * |
| granite-4.2-3b | lora: grammar vs verbose | 500 | 54% | 55% | +2 [-2, +5] | 32 / 40 | 0.410 | 1.000 |
| gemma-4-E2B | adapter at verbose | 500 | 7% | 32% | +25 [+21, +29] | 6 / 131 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at verbose2 | 500 | 11% | 12% | +2 [-2, +5] | 40 / 49 | 0.397 | 1.000 |
| gemma-4-E2B | adapter at compact | 500 | 10% | 87% | +78 [+74, +81] | 0 / 389 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at grammar | 500 | 6% | 26% | +19 [+16, +23] | 11 / 108 | <0.001 | <0.001 * |
| gemma-4-E2B | base: verbose2 vs verbose | 500 | 7% | 11% | +4 [+1, +7] | 25 / 45 | 0.022 | 0.160 |
| gemma-4-E2B | base: compact vs verbose | 500 | 7% | 10% | +3 [-0, +6] | 33 / 48 | 0.119 | 0.716 |
| gemma-4-E2B | base: grammar vs verbose | 500 | 7% | 6% | -0 [-2, +2] | 16 / 14 | 0.856 | 1.000 |
| gemma-4-E2B | lora: verbose2 vs verbose | 500 | 32% | 12% | -19 [-23, -15] | 106 / 10 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: compact vs verbose | 500 | 32% | 87% | +56 [+51, +60] | 10 / 289 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: grammar vs verbose | 500 | 32% | 26% | -6 [-9, -3] | 40 / 10 | <0.001 | <0.001 * |

## Schema validity (valid@1)

Is the whole answer one JSON value that matches its message type's schema, game/schemas/output/<phase>.schema.json?

| condition | model | valid | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | main failures |
|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 258/500 (52%) | 99% | 99% | 12% | 44% | 4% | wrapped 238, not_json 2, schema:type 1 |
| base_verbose | granite-4.2-3b | 499/500 (100%) | 99% | 100% | 100% | 100% | 100% | schema:maxItems 1 |
| base_verbose | gemma-4-E2B | 499/500 (100%) | 99% | 100% | 100% | 100% | 100% | schema:maxItems 1 |
| lora_verbose | LFM2.5-1.2B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_verbose | granite-4.2-3b | 489/500 (98%) | 94% | 100% | 95% | 100% | 100% | schema:maxItems 6, schema:type 5 |
| lora_verbose | gemma-4-E2B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_verbose2 | LFM2.5-1.2B | 481/500 (96%) | 93% | 88% | 100% | 100% | 100% | schema:additionalProperties 12, schema:maxItems 7 |
| base_verbose2 | granite-4.2-3b | 499/500 (100%) | 99% | 100% | 100% | 100% | 100% | schema:maxItems 1 |
| base_verbose2 | gemma-4-E2B | 498/500 (100%) | 99% | 100% | 100% | 99% | 100% | schema:maxItems 1, not_json 1 |
| lora_verbose2 | LFM2.5-1.2B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_verbose2 | granite-4.2-3b | 492/500 (98%) | 92% | 100% | 100% | 100% | 100% | schema:maxItems 8 |
| lora_verbose2 | gemma-4-E2B | 405/500 (81%) | 78% | 100% | 27% | 100% | 100% | schema:type 73, schema:maxItems 22 |
| base_compact | LFM2.5-1.2B | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 500 |
| base_compact | granite-4.2-3b | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 500 |
| base_compact | gemma-4-E2B | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 374, schema:additionalProperties 125, schema:type 1 |
| lora_compact | LFM2.5-1.2B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | granite-4.2-3b | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | gemma-4-E2B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | LFM2.5-1.2B | 484/500 (97%) | 100% | 100% | 84% | 100% | 100% | schema:minItems 16 |
| base_grammar | granite-4.2-3b | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | gemma-4-E2B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_grammar | LFM2.5-1.2B | 441/500 (88%) | 100% | 100% | 41% | 100% | 100% | schema:minItems 59 |
| lora_grammar | granite-4.2-3b | 467/500 (93%) | 100% | 100% | 67% | 100% | 100% | schema:minItems 33 |
| lora_grammar | gemma-4-E2B | 406/500 (81%) | 100% | 100% | 6% | 100% | 100% | schema:minItems 94 |

## Legality

Would the game carry out the answer as the model wrote it?

| condition | model | legal | valid & legal | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | why not legal |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 376/500 (75%) | 36% | 75% | 55% | 99% | 84% | 63% | rules 68, cards_not_held 52, parser 2, no_json 2 |
| base_verbose | granite-4.2-3b | 426/500 (85%) | 85% | 97% | 78% | 100% | 84% | 67% | cards_not_held 49, rules 25 |
| base_verbose | gemma-4-E2B | 477/500 (95%) | 95% | 96% | 96% | 100% | 92% | 93% | cards_not_held 15, rules 8 |
| lora_verbose | LFM2.5-1.2B | 472/500 (94%) | 94% | 87% | 85% | 100% | 100% | 100% | rules 28 |
| lora_verbose | granite-4.2-3b | 456/500 (91%) | 91% | 69% | 92% | 95% | 100% | 100% | rules 39, unknown_player 5 |
| lora_verbose | gemma-4-E2B | 433/500 (87%) | 87% | 90% | 48% | 95% | 100% | 100% | rules 62, cards_not_held 5 |
| base_verbose2 | LFM2.5-1.2B | 354/500 (71%) | 71% | 2% | 53% | 99% | 100% | 100% | rules 145, cards_not_held 1 |
| base_verbose2 | granite-4.2-3b | 446/500 (89%) | 89% | 85% | 80% | 100% | 83% | 98% | rules 35, cards_not_held 19 |
| base_verbose2 | gemma-4-E2B | 434/500 (87%) | 87% | 57% | 95% | 100% | 82% | 100% | rules 48, cards_not_held 17, no_json 1 |
| lora_verbose2 | LFM2.5-1.2B | 487/500 (97%) | 97% | 94% | 93% | 100% | 100% | 100% | rules 13 |
| lora_verbose2 | granite-4.2-3b | 442/500 (88%) | 88% | 43% | 99% | 100% | 100% | 100% | rules 58 |
| lora_verbose2 | gemma-4-E2B | 360/500 (72%) | 72% | 39% | 96% | 27% | 98% | 100% | unknown_player 73, rules 65, cards_not_held 2 |
| base_compact | LFM2.5-1.2B | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | 0% | no_json 500 |
| base_compact | granite-4.2-3b | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | 0% | no_json 500 |
| base_compact | gemma-4-E2B | 90/500 (18%) | 0% | 0% | 0% | 0% | 85% | 5% | no_json 374, rules 35, parser 1 |
| lora_compact | LFM2.5-1.2B | 499/500 (100%) | 100% | 100% | 99% | 100% | 100% | 100% | rules 1 |
| lora_compact | granite-4.2-3b | 498/500 (100%) | 100% | 98% | 100% | 100% | 100% | 100% | rules 2 |
| lora_compact | gemma-4-E2B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | LFM2.5-1.2B | 406/500 (81%) | 81% | 100% | 98% | 79% | 64% | 65% | cards_not_held 76, no_cards 16, rules 2 |
| base_grammar | granite-4.2-3b | 463/500 (93%) | 93% | 100% | 98% | 100% | 87% | 78% | cards_not_held 35, rules 2 |
| base_grammar | gemma-4-E2B | 474/500 (95%) | 95% | 100% | 100% | 100% | 85% | 89% | cards_not_held 26 |
| lora_grammar | LFM2.5-1.2B | 435/500 (87%) | 87% | 100% | 98% | 37% | 100% | 100% | no_cards 59, cards_not_held 4, rules 2 |
| lora_grammar | granite-4.2-3b | 466/500 (93%) | 93% | 100% | 99% | 67% | 100% | 100% | no_cards 33, rules 1 |
| lora_grammar | gemma-4-E2B | 404/500 (81%) | 81% | 100% | 98% | 6% | 100% | 100% | no_cards 94, rules 2 |

## Valid play

Does the answer keep every rule the teacher plays by?

| condition | model | valid play (95% CI) | PLANTING | FORCED | TRADING | REPLY | CONSIDERING |
|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 34% [30–39] | 20% | 1% | 82% | 39% | 30% |
| base_verbose | granite-4.2-3b | 45% [40–49] | 40% | 9% | 100% | 41% | 34% |
| base_verbose | gemma-4-E2B | 42% [38–46] | 33% | 3% | 75% | 48% | 51% |
| lora_verbose | LFM2.5-1.2B | 42% [38–46] | 20% | 7% | 83% | 50% | 50% |
| lora_verbose | granite-4.2-3b | 70% [66–74] | 36% | 80% | 87% | 69% | 77% |
| lora_verbose | gemma-4-E2B | 44% [40–49] | 39% | 8% | 70% | 55% | 50% |
| base_verbose2 | LFM2.5-1.2B | 32% [28–36] | 0% | 2% | 58% | 50% | 50% |
| base_verbose2 | granite-4.2-3b | 42% [38–47] | 36% | 24% | 65% | 36% | 50% |
| base_verbose2 | gemma-4-E2B | 43% [39–48] | 23% | 7% | 100% | 35% | 51% |
| lora_verbose2 | LFM2.5-1.2B | 43% [38–47] | 21% | 5% | 87% | 50% | 50% |
| lora_verbose2 | granite-4.2-3b | 67% [63–71] | 25% | 61% | 93% | 85% | 70% |
| lora_verbose2 | gemma-4-E2B | 27% [23–31] | 19% | 7% | 26% | 40% | 44% |
| base_compact | LFM2.5-1.2B | 0% [0–1] | 0% | 0% | 0% | 0% | 0% |
| base_compact | granite-4.2-3b | 0% [0–1] | 0% | 0% | 0% | 0% | 0% |
| base_compact | gemma-4-E2B | 10% [7–12] | 0% | 0% | 0% | 45% | 3% |
| lora_compact | LFM2.5-1.2B | 86% [83–89] | 82% | 96% | 100% | 98% | 56% |
| lora_compact | granite-4.2-3b | 97% [95–98] | 85% | 99% | 100% | 100% | 99% |
| lora_compact | gemma-4-E2B | 94% [92–96] | 84% | 89% | 100% | 100% | 99% |
| base_grammar | LFM2.5-1.2B | 24% [21–28] | 22% | 6% | 48% | 15% | 31% |
| base_grammar | granite-4.2-3b | 41% [37–45] | 22% | 7% | 100% | 37% | 39% |
| base_grammar | gemma-4-E2B | 37% [33–41] | 20% | 6% | 74% | 38% | 47% |
| lora_grammar | LFM2.5-1.2B | 34% [30–38] | 25% | 15% | 29% | 50% | 50% |
| lora_grammar | granite-4.2-3b | 71% [67–75] | 41% | 81% | 67% | 83% | 84% |
| lora_grammar | gemma-4-E2B | 32% [28–37] | 29% | 9% | 6% | 68% | 50% |
| teacher | training corpus | 100% [100–100] | 100% | 100% | 100% | 100% | 100% |

Each rule on its own (partial credit):

| condition | model | PLANT: first card placed | PLANT: second card without harvest | FORCE: no avoidable harvest | FORCE: least valuable stack lost | TRADI: keeps growing beans | REPLY: accepts iff useful | REPLY: keeps growing beans | CONSI: accepts iff useful |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 31% | 52% | 19% | 37% | 82% | 45% | 71% | 30% |
| base_verbose | granite-4.2-3b | 40% | 97% | 34% | 53% | 100% | 44% | 73% | 34% |
| base_verbose | gemma-4-E2B | 38% | 80% | 50% | 49% | 75% | 54% | 86% | 51% |
| lora_verbose | LFM2.5-1.2B | 34% | 51% | 45% | 47% | 83% | 50% | 100% | 50% |
| lora_verbose | granite-4.2-3b | 53% | 45% | 87% | 85% | 87% | 69% | 100% | 77% |
| lora_verbose | gemma-4-E2B | 39% | 89% | 27% | 29% | 70% | 55% | 100% | 50% |
| base_verbose2 | LFM2.5-1.2B | 0% | 2% | 30% | 25% | 58% | 50% | 100% | 50% |
| base_verbose2 | granite-4.2-3b | 37% | 84% | 56% | 48% | 65% | 44% | 63% | 50% |
| base_verbose2 | gemma-4-E2B | 32% | 33% | 51% | 51% | 100% | 43% | 73% | 51% |
| lora_verbose2 | LFM2.5-1.2B | 40% | 49% | 47% | 51% | 87% | 50% | 100% | 50% |
| lora_verbose2 | granite-4.2-3b | 33% | 31% | 69% | 91% | 93% | 85% | 100% | 70% |
| lora_verbose2 | gemma-4-E2B | 27% | 28% | 51% | 52% | 26% | 50% | 78% | 44% |
| base_compact | LFM2.5-1.2B | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| base_compact | granite-4.2-3b | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| base_compact | gemma-4-E2B | 0% | 0% | 0% | 0% | 0% | 45% | 85% | 3% |
| lora_compact | LFM2.5-1.2B | 82% | 100% | 99% | 96% | 100% | 100% | 98% | 56% |
| lora_compact | granite-4.2-3b | 85% | 98% | 100% | 99% | 100% | 100% | 100% | 99% |
| lora_compact | gemma-4-E2B | 84% | 100% | 95% | 94% | 100% | 100% | 100% | 99% |
| base_grammar | LFM2.5-1.2B | 42% | 29% | 52% | 52% | 48% | 32% | 39% | 31% |
| base_grammar | granite-4.2-3b | 36% | 34% | 53% | 52% | 100% | 47% | 65% | 39% |
| base_grammar | gemma-4-E2B | 40% | 28% | 54% | 52% | 74% | 47% | 68% | 47% |
| lora_grammar | LFM2.5-1.2B | 44% | 40% | 58% | 55% | 29% | 50% | 100% | 50% |
| lora_grammar | granite-4.2-3b | 71% | 58% | 97% | 83% | 67% | 83% | 100% | 84% |
| lora_grammar | gemma-4-E2B | 45% | 73% | 55% | 52% | 6% | 68% | 100% | 50% |
| teacher | training corpus | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |

## Reference-correctness

Does the answer make the decision the reference bot makes in the same state?

| condition | model | correct (95% CI) | PLANTING | FORCED | TRADING | REPLY | CONSIDERING |
|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 9% [7–12] | 19% | 1% | 0% | 25% | 0% |
| base_verbose | granite-4.2-3b | 14% [12–18] | 31% | 8% | 29% | 0% | 4% |
| base_verbose | gemma-4-E2B | 7% [5–9] | 27% | 3% | 1% | 1% | 1% |
| lora_verbose | LFM2.5-1.2B | 24% [20–28] | 13% | 5% | 2% | 49% | 50% |
| lora_verbose | granite-4.2-3b | 54% [49–58] | 23% | 80% | 38% | 50% | 77% |
| lora_verbose | gemma-4-E2B | 32% [28–36] | 31% | 7% | 20% | 50% | 50% |
| base_verbose2 | LFM2.5-1.2B | 21% [17–25] | 0% | 1% | 3% | 50% | 50% |
| base_verbose2 | granite-4.2-3b | 9% [7–12] | 27% | 18% | 1% | 0% | 0% |
| base_verbose2 | gemma-4-E2B | 11% [8–14] | 9% | 7% | 25% | 1% | 11% |
| lora_verbose2 | LFM2.5-1.2B | 23% [20–27] | 3% | 5% | 9% | 50% | 50% |
| lora_verbose2 | granite-4.2-3b | 47% [42–51] | 22% | 51% | 39% | 51% | 70% |
| lora_verbose2 | gemma-4-E2B | 12% [10–16] | 7% | 7% | 1% | 4% | 43% |
| base_compact | LFM2.5-1.2B | 0% [0–1] | 0% | 0% | 0% | 0% | 0% |
| base_compact | granite-4.2-3b | 0% [0–1] | 0% | 0% | 0% | 0% | 0% |
| base_compact | gemma-4-E2B | 10% [7–12] | 0% | 0% | 0% | 45% | 3% |
| lora_compact | LFM2.5-1.2B | 80% [76–83] | 73% | 94% | 78% | 98% | 56% |
| lora_compact | granite-4.2-3b | 91% [88–93] | 80% | 95% | 81% | 100% | 99% |
| lora_compact | gemma-4-E2B | 87% [84–90] | 77% | 88% | 73% | 100% | 99% |
| base_grammar | LFM2.5-1.2B | 2% [1–4] | 6% | 5% | 1% | 0% | 0% |
| base_grammar | granite-4.2-3b | 12% [9–15] | 21% | 7% | 29% | 1% | 0% |
| base_grammar | gemma-4-E2B | 6% [4–9] | 14% | 6% | 3% | 1% | 7% |
| lora_grammar | LFM2.5-1.2B | 25% [22–29] | 7% | 13% | 7% | 50% | 50% |
| lora_grammar | granite-4.2-3b | 55% [51–60] | 30% | 75% | 35% | 52% | 84% |
| lora_grammar | gemma-4-E2B | 26% [22–30] | 23% | 8% | 1% | 46% | 50% |
| teacher | training corpus | 100% [100–100] | 100% | 100% | 100% | 100% | 100% |

## State sensitivity

Does the decision depend on the game state?

| condition | model | REPLY accepts useful / useless | gap | CONSIDERING accepts useful / useless | gap | PLANTING avoidable harvests | FORCED avoidable harvests | TRADING passes | offers giving away a growing bean |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 49% / 42% | +7 | 100% / 100% | +0 | 45/75 (60%) | 36/55 (65%) | 0% | 17/99 (17%) |
| base_verbose | granite-4.2-3b | 28% / 25% | +3 | 12% / 9% | +3 | 29/97 (30%) | 44/78 (56%) | 100% | – |
| base_verbose | gemma-4-E2B | 51% / 34% | +17 | 38% / 29% | +9 | 37/96 (39%) | 46/96 (48%) | 0% | 25/100 (25%) |
| lora_verbose | LFM2.5-1.2B | 2% / 2% | +0 | 0% / 0% | +0 | 58/87 (67%) | 40/85 (47%) | 0% | 17/100 (17%) |
| lora_verbose | granite-4.2-3b | 38% / 0% | +38 | 56% / 2% | +54 | 26/69 (38%) | 5/92 (5%) | 7% | 8/88 (9%) |
| lora_verbose | gemma-4-E2B | 10% / 0% | +10 | 0% / 0% | +0 | 25/90 (28%) | 21/48 (44%) | 1% | 25/94 (27%) |
| base_verbose2 | LFM2.5-1.2B | 0% / 0% | +0 | 0% / 0% | +0 | 2/2 (100%) | 23/53 (43%) | 0% | 41/99 (41%) |
| base_verbose2 | granite-4.2-3b | 2% / 0% | +2 | 0% / 0% | +0 | 22/85 (26%) | 24/80 (30%) | 0% | 35/100 (35%) |
| base_verbose2 | gemma-4-E2B | 17% / 12% | +5 | 12% / 10% | +2 | 32/57 (56%) | 44/95 (46%) | 90% | 0/10 (0%) |
| lora_verbose2 | LFM2.5-1.2B | 0% / 0% | +0 | 0% / 0% | +0 | 66/94 (70%) | 46/93 (49%) | 43% | 13/57 (23%) |
| lora_verbose2 | granite-4.2-3b | 72% / 2% | +70 | 40% / 0% | +40 | 13/43 (30%) | 30/99 (30%) | 44% | 7/56 (12%) |
| lora_verbose2 | gemma-4-E2B | 0% / 0% | +0 | 6% / 18% | -12 | 14/39 (36%) | 45/96 (47%) | 0% | 1/27 (4%) |
| base_compact | LFM2.5-1.2B | – / – | – | – / – | – | – | – | – | – |
| base_compact | granite-4.2-3b | – / – | – | – / – | – | – | – | – | – |
| base_compact | gemma-4-E2B | 0% / 0% | +0 | 0% / 0% | +0 | – | – | – | – |
| lora_compact | LFM2.5-1.2B | 100% / 0% | +100 | 48% / 36% | +12 | 0/100 (0%) | 0/99 (0%) | 26% | 0/74 (0%) |
| lora_compact | granite-4.2-3b | 100% / 0% | +100 | 100% / 2% | +98 | 0/98 (0%) | 0/100 (0%) | 26% | 0/74 (0%) |
| lora_compact | gemma-4-E2B | 100% / 0% | +100 | 100% / 2% | +98 | 0/100 (0%) | 5/100 (5%) | 26% | 0/74 (0%) |
| base_grammar | LFM2.5-1.2B | 100% / 100% | +0 | 100% / 97% | +3 | 77/100 (77%) | 46/98 (47%) | 0% | 31/79 (39%) |
| base_grammar | granite-4.2-3b | 2% / 2% | +0 | 10% / 5% | +4 | 72/100 (72%) | 45/98 (46%) | 100% | – |
| base_grammar | gemma-4-E2B | 10% / 4% | +6 | 7% / 2% | +5 | 79/100 (79%) | 46/100 (46%) | 0% | 26/100 (26%) |
| lora_grammar | LFM2.5-1.2B | 0% / 0% | +0 | 0% / 0% | +0 | 70/100 (70%) | 40/98 (41%) | 0% | 8/37 (22%) |
| lora_grammar | granite-4.2-3b | 68% / 2% | +66 | 70% / 2% | +68 | 52/100 (52%) | 2/99 (2%) | 0% | 0/67 (0%) |
| lora_grammar | gemma-4-E2B | 44% / 8% | +36 | 0% / 0% | +0 | 50/100 (50%) | 43/98 (44%) | 0% | 0/6 (0%) |
| teacher | training corpus | 100% / 0% | +100 | 100% / 0% | +100 | 0/3000 (0%) | 0/3000 (0%) | 43% | 0/1712 (0%) |

## Agreement

Given the same item, do two settings make the same decision?

Same decision on the same item (95% CI; compared items in brackets).

| LFM2.5-1.2B | base_verbose | lora_verbose | base_verbose2 | lora_verbose2 | base_compact | lora_compact | base_grammar | lora_grammar |
|---|---|---|---|---|---|---|---|---|
| base_verbose | · | 39% [35–44] (496) | 12% [10–15] (496) | 17% [14–20] (496) | – (0) | 10% [8–13] (496) | 26% [23–30] (496) | 13% [10–16] (496) |
| lora_verbose | 39% [35–44] (496) | · | 45% [41–50] (500) | 55% [51–60] (500) | – (0) | 26% [23–30] (500) | 9% [7–12] (500) | 49% [45–54] (500) |
| base_verbose2 | 12% [10–15] (496) | 45% [41–50] (500) | · | 46% [42–51] (500) | – (0) | 22% [19–26] (500) | 10% [7–13] (500) | 44% [40–48] (500) |
| lora_verbose2 | 17% [14–20] (496) | 55% [51–60] (500) | 46% [42–51] (500) | · | – (0) | 24% [21–28] (500) | 18% [15–22] (500) | 57% [52–61] (500) |
| base_compact | – (0) | – (0) | – (0) | – (0) | · | – (0) | – (0) | – (0) |
| lora_compact | 10% [8–13] (496) | 26% [23–30] (500) | 22% [19–26] (500) | 24% [21–28] (500) | – (0) | · | 2% [1–3] (500) | 26% [22–30] (500) |
| base_grammar | 26% [23–30] (496) | 9% [7–12] (500) | 10% [7–13] (500) | 18% [15–22] (500) | – (0) | 2% [1–3] (500) | · | 26% [23–30] (500) |
| lora_grammar | 13% [10–16] (496) | 49% [45–54] (500) | 44% [40–48] (500) | 57% [52–61] (500) | – (0) | 26% [22–30] (500) | 26% [23–30] (500) | · |

| granite-4.2-3b | base_verbose | lora_verbose | base_verbose2 | lora_verbose2 | base_compact | lora_compact | base_grammar | lora_grammar |
|---|---|---|---|---|---|---|---|---|
| base_verbose | · | 8% [6–11] (500) | 29% [26–34] (500) | 18% [15–21] (500) | – (0) | 12% [9–15] (500) | 43% [39–48] (500) | 6% [4–8] (500) |
| lora_verbose | 8% [6–11] (500) | · | 10% [7–12] (500) | 53% [49–58] (500) | – (0) | 54% [50–58] (500) | 6% [4–9] (500) | 65% [61–69] (500) |
| base_verbose2 | 29% [26–34] (500) | 10% [7–12] (500) | · | 8% [6–10] (500) | – (0) | 8% [6–10] (500) | 11% [8–14] (500) | 6% [4–8] (500) |
| lora_verbose2 | 18% [15–21] (500) | 53% [49–58] (500) | 8% [6–10] (500) | · | – (0) | 47% [43–52] (500) | 15% [12–19] (500) | 52% [48–57] (500) |
| base_compact | – (0) | – (0) | – (0) | – (0) | · | – (0) | – (0) | – (0) |
| lora_compact | 12% [9–15] (500) | 54% [50–58] (500) | 8% [6–10] (500) | 47% [43–52] (500) | – (0) | · | 10% [8–13] (500) | 56% [51–60] (500) |
| base_grammar | 43% [39–48] (500) | 6% [4–9] (500) | 11% [8–14] (500) | 15% [12–19] (500) | – (0) | 10% [8–13] (500) | · | 8% [6–11] (500) |
| lora_grammar | 6% [4–8] (500) | 65% [61–69] (500) | 6% [4–8] (500) | 52% [48–57] (500) | – (0) | 56% [51–60] (500) | 8% [6–11] (500) | · |

| gemma-4-E2B | base_verbose | lora_verbose | base_verbose2 | lora_verbose2 | base_compact | lora_compact | base_grammar | lora_grammar |
|---|---|---|---|---|---|---|---|---|
| base_verbose | · | 22% [18–26] (500) | 30% [26–34] (499) | 15% [12–19] (500) | 0% [0–3] (125) | 7% [5–10] (500) | 45% [40–49] (500) | 23% [20–27] (500) |
| lora_verbose | 22% [18–26] (500) | · | 10% [8–13] (499) | 29% [25–33] (500) | 69% [60–76] (125) | 33% [29–37] (500) | 15% [12–18] (500) | 54% [50–58] (500) |
| base_verbose2 | 30% [26–34] (499) | 10% [8–13] (499) | · | 23% [19–27] (499) | 2% [0–6] (124) | 10% [7–13] (499) | 30% [26–34] (499) | 18% [15–22] (499) |
| lora_verbose2 | 15% [12–19] (500) | 29% [25–33] (500) | 23% [19–27] (499) | · | 13% [8–20] (125) | 14% [11–17] (500) | 17% [14–21] (500) | 34% [30–38] (500) |
| base_compact | 0% [0–3] (125) | 69% [60–76] (125) | 2% [0–6] (124) | 13% [8–20] (125) | · | 38% [30–47] (125) | 0% [0–3] (125) | 57% [48–65] (125) |
| lora_compact | 7% [5–10] (500) | 33% [29–37] (500) | 10% [7–13] (499) | 14% [11–17] (500) | 38% [30–47] (125) | · | 5% [4–8] (500) | 26% [22–30] (500) |
| base_grammar | 45% [40–49] (500) | 15% [12–18] (500) | 30% [26–34] (499) | 17% [14–21] (500) | 0% [0–3] (125) | 5% [4–8] (500) | · | 20% [17–24] (500) |
| lora_grammar | 23% [20–27] (500) | 54% [50–58] (500) | 18% [15–22] (499) | 34% [30–38] (500) | 57% [48–65] (125) | 26% [22–30] (500) | 20% [17–24] (500) | · |

# replay_20261115_ref: held-out training states

replay run, backend gpu; 500 answers per model and condition; training corpus `training/corpus/training_data_reference_15000.txt`; evaluated 2026-11-17 09:25. Shares in brackets are 95% Wilson intervals.

## Overview

| condition | model | answers | schema-valid | legal | valid play | reference-correct | accept gap useful−useless | avoidable harvests |
|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 500 | 51% [47–56] | 66% [61–70] | 30% [27–35] | 8% [6–11] | +0 | 73% |
| base_verbose | granite-4.2-3b | 500 | 99% [98–100] | 78% [74–81] | 43% [38–47] | 16% [13–19] | -6 | 43% |
| base_verbose | gemma-4-E2B | 500 | 95% [93–97] | 86% [82–89] | 38% [34–43] | 7% [5–9] | +5 | 39% |
| lora_verbose | LFM2.5-1.2B | 500 | 100% [99–100] | 92% [90–94] | 47% [43–51] | 28% [25–33] | +1 | 57% |
| lora_verbose | granite-4.2-3b | 500 | 99% [98–100] | 90% [87–93] | 71% [66–74] | 50% [46–54] | +51 | 20% |
| lora_verbose | gemma-4-E2B | 500 | 100% [99–100] | 88% [85–90] | 46% [42–50] | 37% [33–41] | +1 | 30% |
| base_verbose2 | LFM2.5-1.2B | 500 | 92% [89–94] | 66% [62–70] | 35% [31–39] | 24% [20–28] | +0 | 32% |
| base_verbose2 | granite-4.2-3b | 500 | 97% [95–98] | 82% [78–85] | 40% [36–45] | 6% [4–8] | +0 | 39% |
| base_verbose2 | gemma-4-E2B | 500 | 99% [97–99] | 82% [78–85] | 47% [43–52] | 16% [13–20] | -2 | 37% |
| lora_verbose2 | LFM2.5-1.2B | 500 | 100% [99–100] | 94% [91–96] | 48% [44–52] | 31% [27–36] | +0 | 56% |
| lora_verbose2 | granite-4.2-3b | 500 | 97% [95–98] | 85% [82–88] | 68% [64–72] | 48% [43–52] | +52 | 11% |
| lora_verbose2 | gemma-4-E2B | 500 | 93% [91–95] | 79% [75–82] | 43% [38–47] | 23% [20–27] | +4 | 30% |
| base_compact | LFM2.5-1.2B | 500 | 0% [0–1] | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| base_compact | granite-4.2-3b | 500 | 0% [0–1] | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| base_compact | gemma-4-E2B | 500 | 0% [0–1] | 11% [9–14] | 6% [4–8] | 6% [4–8] | +0 | – |
| lora_compact | LFM2.5-1.2B | 500 | 100% [99–100] | 98% [96–99] | 89% [86–91] | 87% [84–90] | +72 | 1% |
| lora_compact | granite-4.2-3b | 500 | 100% [99–100] | 100% [99–100] | 97% [95–98] | 95% [93–97] | +100 | 1% |
| lora_compact | gemma-4-E2B | 500 | 100% [99–100] | 100% [99–100] | 96% [94–98] | 94% [91–96] | +98 | 1% |
| base_grammar | LFM2.5-1.2B | 500 | 100% [99–100] | 76% [72–79] | 24% [20–28] | 6% [5–9] | -2 | 63% |
| base_grammar | granite-4.2-3b | 500 | 100% [99–100] | 90% [87–92] | 42% [38–46] | 16% [13–19] | -2 | 62% |
| base_grammar | gemma-4-E2B | 500 | 100% [99–100] | 93% [91–95] | 37% [33–42] | 12% [10–15] | +5 | 56% |
| lora_grammar | LFM2.5-1.2B | 500 | 87% [84–90] | 84% [80–87] | 39% [35–43] | 34% [30–38] | +0 | 52% |
| lora_grammar | granite-4.2-3b | 500 | 91% [88–93] | 90% [87–93] | 71% [67–75] | 58% [54–62] | +71 | 24% |
| lora_grammar | gemma-4-E2B | 500 | 82% [78–85] | 79% [76–83] | 42% [37–46] | 36% [32–40] | +22 | 40% |

## Effects

How much do the adapter and the prompt style change an outcome, item by item?

Rows marked * stay significant after the Holm correction.

### schema-valid

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| LFM2.5-1.2B | adapter at verbose | 500 | 51% | 100% | +49 [+44, +53] | 0 / 244 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at verbose2 | 500 | 92% | 100% | +8 [+6, +11] | 1 / 41 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at compact | 500 | 0% | 100% | +100 [+100, +100] | 0 / 500 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at grammar | 500 | 100% | 87% | -13 [-16, -10] | 64 / 0 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: verbose2 vs verbose | 500 | 51% | 92% | +41 [+35, +46] | 35 / 238 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: compact vs verbose | 500 | 51% | 0% | -51 [-56, -47] | 256 / 0 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: grammar vs verbose | 500 | 51% | 100% | +49 [+44, +53] | 0 / 243 | <0.001 | <0.001 * |
| LFM2.5-1.2B | lora: verbose2 vs verbose | 500 | 100% | 100% | -0 [-1, +0] | 1 / 0 | 1.000 | 1.000 |
| LFM2.5-1.2B | lora: compact vs verbose | 500 | 100% | 100% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| LFM2.5-1.2B | lora: grammar vs verbose | 500 | 100% | 87% | -13 [-16, -10] | 65 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at verbose | 500 | 99% | 99% | +0 [-1, +1] | 4 / 5 | 1.000 | 1.000 |
| granite-4.2-3b | adapter at verbose2 | 500 | 97% | 97% | +0 [-2, +2] | 13 / 13 | 1.000 | 1.000 |
| granite-4.2-3b | adapter at compact | 500 | 0% | 100% | +100 [+100, +100] | 0 / 500 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at grammar | 500 | 100% | 91% | -9 [-12, -7] | 47 / 1 | <0.001 | <0.001 * |
| granite-4.2-3b | base: verbose2 vs verbose | 500 | 99% | 97% | -2 [-4, -1] | 13 / 3 | 0.021 | 0.170 |
| granite-4.2-3b | base: compact vs verbose | 500 | 99% | 0% | -99 [-100, -98] | 495 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | base: grammar vs verbose | 500 | 99% | 100% | +1 [+0, +2] | 1 / 5 | 0.219 | 1.000 |
| granite-4.2-3b | lora: verbose2 vs verbose | 500 | 99% | 97% | -2 [-4, -1] | 14 / 3 | 0.013 | 0.115 |
| granite-4.2-3b | lora: compact vs verbose | 500 | 99% | 100% | +1 [+0, +2] | 0 / 4 | 0.125 | 0.875 |
| granite-4.2-3b | lora: grammar vs verbose | 500 | 99% | 91% | -9 [-11, -6] | 45 / 2 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at verbose | 500 | 95% | 100% | +5 [+3, +7] | 0 / 23 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at verbose2 | 500 | 99% | 93% | -5 [-8, -3] | 32 / 6 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at compact | 500 | 0% | 100% | +100 [+100, +100] | 0 / 500 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at grammar | 500 | 100% | 82% | -18 [-21, -15] | 90 / 0 | <0.001 | <0.001 * |
| gemma-4-E2B | base: verbose2 vs verbose | 500 | 95% | 99% | +3 [+1, +5] | 4 / 20 | 0.002 | 0.015 * |
| gemma-4-E2B | base: compact vs verbose | 500 | 95% | 0% | -95 [-97, -93] | 477 / 0 | <0.001 | <0.001 * |
| gemma-4-E2B | base: grammar vs verbose | 500 | 95% | 100% | +4 [+2, +6] | 2 / 23 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: verbose2 vs verbose | 500 | 100% | 93% | -7 [-9, -4] | 33 / 0 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: compact vs verbose | 500 | 100% | 100% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| gemma-4-E2B | lora: grammar vs verbose | 500 | 100% | 82% | -18 [-22, -15] | 92 / 0 | <0.001 | <0.001 * |

### legal

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| LFM2.5-1.2B | adapter at verbose | 500 | 66% | 92% | +27 [+23, +31] | 5 / 139 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at verbose2 | 500 | 66% | 94% | +28 [+24, +32] | 9 / 148 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at compact | 500 | 0% | 98% | +98 [+96, +99] | 0 / 489 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at grammar | 500 | 76% | 84% | +8 [+3, +12] | 56 / 95 | 0.002 | 0.021 * |
| LFM2.5-1.2B | base: verbose2 vs verbose | 500 | 66% | 66% | +0 [-5, +5] | 82 / 84 | 0.938 | 1.000 |
| LFM2.5-1.2B | base: compact vs verbose | 500 | 66% | 0% | -66 [-70, -61] | 328 / 0 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: grammar vs verbose | 500 | 66% | 76% | +10 [+6, +15] | 43 / 94 | <0.001 | <0.001 * |
| LFM2.5-1.2B | lora: verbose2 vs verbose | 500 | 92% | 94% | +1 [-1, +4] | 18 / 25 | 0.360 | 1.000 |
| LFM2.5-1.2B | lora: compact vs verbose | 500 | 92% | 98% | +5 [+3, +8] | 6 / 33 | <0.001 | <0.001 * |
| LFM2.5-1.2B | lora: grammar vs verbose | 500 | 92% | 84% | -9 [-13, -5] | 74 / 30 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at verbose | 500 | 78% | 90% | +12 [+8, +17] | 36 / 98 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at verbose2 | 500 | 82% | 85% | +3 [-1, +8] | 52 / 69 | 0.145 | 1.000 |
| granite-4.2-3b | adapter at compact | 500 | 0% | 100% | +100 [+99, +100] | 0 / 499 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at grammar | 500 | 90% | 90% | +1 [-3, +4] | 48 / 51 | 0.841 | 1.000 |
| granite-4.2-3b | base: verbose2 vs verbose | 500 | 78% | 82% | +4 [+0, +8] | 46 / 67 | 0.059 | 0.512 |
| granite-4.2-3b | base: compact vs verbose | 500 | 78% | 0% | -78 [-81, -74] | 389 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | base: grammar vs verbose | 500 | 78% | 90% | +12 [+8, +16] | 23 / 82 | <0.001 | <0.001 * |
| granite-4.2-3b | lora: verbose2 vs verbose | 500 | 90% | 85% | -5 [-8, -1] | 48 / 24 | 0.006 | 0.063 |
| granite-4.2-3b | lora: compact vs verbose | 500 | 90% | 100% | +10 [+7, +12] | 1 / 49 | <0.001 | <0.001 * |
| granite-4.2-3b | lora: grammar vs verbose | 500 | 90% | 90% | +0 [-4, +4] | 45 / 45 | 1.000 | 1.000 |
| gemma-4-E2B | adapter at verbose | 500 | 86% | 88% | +2 [-2, +6] | 42 / 52 | 0.353 | 1.000 |
| gemma-4-E2B | adapter at verbose2 | 500 | 82% | 79% | -3 [-7, +1] | 56 / 41 | 0.155 | 1.000 |
| gemma-4-E2B | adapter at compact | 500 | 11% | 100% | +89 [+86, +92] | 0 / 445 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at grammar | 500 | 93% | 79% | -14 [-18, -10] | 97 / 28 | <0.001 | <0.001 * |
| gemma-4-E2B | base: verbose2 vs verbose | 500 | 86% | 82% | -4 [-8, +0] | 60 / 40 | 0.057 | 0.512 |
| gemma-4-E2B | base: compact vs verbose | 500 | 86% | 11% | -75 [-79, -71] | 381 / 7 | <0.001 | <0.001 * |
| gemma-4-E2B | base: grammar vs verbose | 500 | 86% | 93% | +7 [+4, +11] | 26 / 63 | <0.001 | 0.001 * |
| gemma-4-E2B | lora: verbose2 vs verbose | 500 | 88% | 79% | -9 [-13, -5] | 80 / 35 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: compact vs verbose | 500 | 88% | 100% | +12 [+9, +15] | 0 / 61 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: grammar vs verbose | 500 | 88% | 79% | -8 [-13, -4] | 86 / 44 | <0.001 | 0.003 * |

### valid-play

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| LFM2.5-1.2B | adapter at verbose | 500 | 30% | 47% | +17 [+12, +21] | 36 / 119 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at verbose2 | 500 | 35% | 48% | +13 [+10, +16] | 3 / 69 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at compact | 500 | 0% | 89% | +89 [+86, +92] | 0 / 445 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at grammar | 500 | 24% | 39% | +15 [+9, +21] | 72 / 147 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: verbose2 vs verbose | 500 | 30% | 35% | +4 [-1, +9] | 75 / 97 | 0.109 | 0.790 |
| LFM2.5-1.2B | base: compact vs verbose | 500 | 30% | 0% | -30 [-35, -26] | 152 / 0 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: grammar vs verbose | 500 | 30% | 24% | -7 [-10, -3] | 62 / 29 | <0.001 | 0.008 * |
| LFM2.5-1.2B | lora: verbose2 vs verbose | 500 | 47% | 48% | +1 [-2, +4] | 23 / 28 | 0.576 | 1.000 |
| LFM2.5-1.2B | lora: compact vs verbose | 500 | 47% | 89% | +42 [+37, +47] | 14 / 224 | <0.001 | <0.001 * |
| LFM2.5-1.2B | lora: grammar vs verbose | 500 | 47% | 39% | -8 [-12, -4] | 71 / 30 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at verbose | 500 | 43% | 71% | +28 [+23, +33] | 30 / 170 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at verbose2 | 500 | 40% | 68% | +28 [+24, +33] | 17 / 157 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at compact | 500 | 0% | 97% | +97 [+95, +98] | 0 / 484 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at grammar | 500 | 42% | 71% | +29 [+24, +35] | 54 / 200 | <0.001 | <0.001 * |
| granite-4.2-3b | base: verbose2 vs verbose | 500 | 43% | 40% | -2 [-6, +2] | 58 / 47 | 0.329 | 1.000 |
| granite-4.2-3b | base: compact vs verbose | 500 | 43% | 0% | -43 [-47, -38] | 213 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | base: grammar vs verbose | 500 | 43% | 42% | -1 [-5, +3] | 54 / 50 | 0.769 | 1.000 |
| granite-4.2-3b | lora: verbose2 vs verbose | 500 | 71% | 68% | -2 [-6, +2] | 54 / 43 | 0.310 | 1.000 |
| granite-4.2-3b | lora: compact vs verbose | 500 | 71% | 97% | +26 [+22, +30] | 1 / 132 | <0.001 | <0.001 * |
| granite-4.2-3b | lora: grammar vs verbose | 500 | 71% | 71% | +0 [-4, +4] | 50 / 52 | 0.921 | 1.000 |
| gemma-4-E2B | adapter at verbose | 500 | 38% | 46% | +8 [+4, +12] | 36 / 75 | <0.001 | 0.004 * |
| gemma-4-E2B | adapter at verbose2 | 500 | 47% | 43% | -5 [-9, -1] | 63 / 40 | 0.030 | 0.327 |
| gemma-4-E2B | adapter at compact | 500 | 6% | 96% | +91 [+88, +93] | 0 / 453 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at grammar | 500 | 37% | 42% | +4 [-1, +9] | 63 / 84 | 0.099 | 0.790 |
| gemma-4-E2B | base: verbose2 vs verbose | 500 | 38% | 47% | +9 [+5, +14] | 42 / 87 | <0.001 | 0.001 * |
| gemma-4-E2B | base: compact vs verbose | 500 | 38% | 6% | -32 [-37, -28] | 167 / 5 | <0.001 | <0.001 * |
| gemma-4-E2B | base: grammar vs verbose | 500 | 38% | 37% | -1 [-5, +3] | 55 / 51 | 0.771 | 1.000 |
| gemma-4-E2B | lora: verbose2 vs verbose | 500 | 46% | 43% | -3 [-7, +0] | 51 / 34 | 0.082 | 0.738 |
| gemma-4-E2B | lora: compact vs verbose | 500 | 46% | 96% | +50 [+46, +55] | 6 / 258 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: grammar vs verbose | 500 | 46% | 42% | -4 [-8, -0] | 65 / 43 | 0.043 | 0.428 |

### reference-correct

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| LFM2.5-1.2B | adapter at verbose | 500 | 8% | 28% | +20 [+17, +24] | 8 / 110 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at verbose2 | 500 | 24% | 31% | +8 [+5, +10] | 1 / 39 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at compact | 500 | 0% | 87% | +87 [+84, +90] | 0 / 436 | <0.001 | <0.001 * |
| LFM2.5-1.2B | adapter at grammar | 500 | 6% | 34% | +27 [+23, +32] | 11 / 148 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: verbose2 vs verbose | 500 | 8% | 24% | +16 [+12, +20] | 16 / 95 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: compact vs verbose | 500 | 8% | 0% | -8 [-10, -6] | 40 / 0 | <0.001 | <0.001 * |
| LFM2.5-1.2B | base: grammar vs verbose | 500 | 8% | 6% | -2 [-5, +1] | 35 / 27 | 0.374 | 1.000 |
| LFM2.5-1.2B | lora: verbose2 vs verbose | 500 | 28% | 31% | +3 [+1, +5] | 10 / 25 | 0.017 | 0.100 |
| LFM2.5-1.2B | lora: compact vs verbose | 500 | 28% | 87% | +59 [+54, +63] | 11 / 305 | <0.001 | <0.001 * |
| LFM2.5-1.2B | lora: grammar vs verbose | 500 | 28% | 34% | +5 [+3, +8] | 11 / 38 | <0.001 | 0.001 * |
| granite-4.2-3b | adapter at verbose | 500 | 16% | 50% | +34 [+28, +40] | 62 / 233 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at verbose2 | 500 | 6% | 48% | +42 [+37, +46] | 8 / 217 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at compact | 500 | 0% | 95% | +95 [+93, +97] | 0 / 475 | <0.001 | <0.001 * |
| granite-4.2-3b | adapter at grammar | 500 | 16% | 58% | +43 [+37, +48] | 49 / 262 | <0.001 | <0.001 * |
| granite-4.2-3b | base: verbose2 vs verbose | 500 | 16% | 6% | -10 [-13, -7] | 64 / 14 | <0.001 | <0.001 * |
| granite-4.2-3b | base: compact vs verbose | 500 | 16% | 0% | -16 [-19, -12] | 79 / 0 | <0.001 | <0.001 * |
| granite-4.2-3b | base: grammar vs verbose | 500 | 16% | 16% | -0 [-3, +2] | 23 / 22 | 1.000 | 1.000 |
| granite-4.2-3b | lora: verbose2 vs verbose | 500 | 50% | 48% | -2 [-7, +2] | 59 / 47 | 0.285 | 1.000 |
| granite-4.2-3b | lora: compact vs verbose | 500 | 50% | 95% | +45 [+41, +50] | 1 / 226 | <0.001 | <0.001 * |
| granite-4.2-3b | lora: grammar vs verbose | 500 | 50% | 58% | +8 [+5, +11] | 15 / 56 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at verbose | 500 | 7% | 37% | +30 [+26, +35] | 6 / 158 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at verbose2 | 500 | 16% | 23% | +7 [+2, +11] | 47 / 81 | 0.003 | 0.024 * |
| gemma-4-E2B | adapter at compact | 500 | 6% | 94% | +88 [+85, +91] | 0 / 440 | <0.001 | <0.001 * |
| gemma-4-E2B | adapter at grammar | 500 | 12% | 36% | +24 [+20, +28] | 4 / 123 | <0.001 | <0.001 * |
| gemma-4-E2B | base: verbose2 vs verbose | 500 | 7% | 16% | +10 [+6, +13] | 17 / 66 | <0.001 | <0.001 * |
| gemma-4-E2B | base: compact vs verbose | 500 | 7% | 6% | -1 [-4, +2] | 30 / 26 | 0.689 | 1.000 |
| gemma-4-E2B | base: grammar vs verbose | 500 | 7% | 12% | +6 [+3, +9] | 16 / 44 | <0.001 | 0.003 * |
| gemma-4-E2B | lora: verbose2 vs verbose | 500 | 37% | 23% | -14 [-18, -10] | 86 / 17 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: compact vs verbose | 500 | 37% | 94% | +57 [+52, +61] | 4 / 288 | <0.001 | <0.001 * |
| gemma-4-E2B | lora: grammar vs verbose | 500 | 37% | 36% | -1 [-4, +2] | 34 / 29 | 0.615 | 1.000 |

## Schema validity (valid@1)

Is the whole answer one JSON value that matches its message type's schema, game/schemas/output/<phase>.schema.json?

| condition | model | valid | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | main failures |
|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 256/500 (51%) | 87% | 90% | 11% | 31% | 37% | wrapped 217, schema:type 11, schema:maxItems 8 |
| base_verbose | granite-4.2-3b | 495/500 (99%) | 96% | 100% | 100% | 99% | 100% | schema:maxItems 4, schema:enum 1 |
| base_verbose | gemma-4-E2B | 477/500 (95%) | 77% | 100% | 100% | 100% | 100% | schema:maxItems 23 |
| lora_verbose | LFM2.5-1.2B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_verbose | granite-4.2-3b | 496/500 (99%) | 98% | 100% | 98% | 100% | 100% | schema:maxItems 2, schema:type 2 |
| lora_verbose | gemma-4-E2B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_verbose2 | LFM2.5-1.2B | 459/500 (92%) | 94% | 65% | 100% | 100% | 100% | schema:additionalProperties 35, schema:maxItems 6 |
| base_verbose2 | granite-4.2-3b | 485/500 (97%) | 85% | 100% | 100% | 100% | 100% | schema:maxItems 15 |
| base_verbose2 | gemma-4-E2B | 493/500 (99%) | 93% | 100% | 100% | 100% | 100% | schema:maxItems 7 |
| lora_verbose2 | LFM2.5-1.2B | 499/500 (100%) | 99% | 100% | 100% | 100% | 100% | schema:additionalProperties 1 |
| lora_verbose2 | granite-4.2-3b | 485/500 (97%) | 85% | 100% | 100% | 100% | 100% | schema:maxItems 15 |
| lora_verbose2 | gemma-4-E2B | 467/500 (93%) | 94% | 100% | 73% | 100% | 100% | schema:type 27, schema:maxItems 6 |
| base_compact | LFM2.5-1.2B | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 500 |
| base_compact | granite-4.2-3b | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 500 |
| base_compact | gemma-4-E2B | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 438, schema:additionalProperties 61, schema:type 1 |
| lora_compact | LFM2.5-1.2B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | granite-4.2-3b | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | gemma-4-E2B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | LFM2.5-1.2B | 499/500 (100%) | 100% | 100% | 99% | 100% | 100% | schema:minItems 1 |
| base_grammar | granite-4.2-3b | 499/500 (100%) | 100% | 100% | 100% | 99% | 100% | not_json 1 |
| base_grammar | gemma-4-E2B | 498/500 (100%) | 100% | 100% | 98% | 100% | 100% | schema:minItems 2 |
| lora_grammar | LFM2.5-1.2B | 435/500 (87%) | 100% | 100% | 35% | 100% | 100% | schema:minItems 65 |
| lora_grammar | granite-4.2-3b | 453/500 (91%) | 100% | 100% | 53% | 100% | 100% | schema:minItems 47 |
| lora_grammar | gemma-4-E2B | 408/500 (82%) | 100% | 100% | 8% | 100% | 100% | schema:minItems 92 |

## Legality

Would the game carry out the answer as the model wrote it?

| condition | model | legal | valid & legal | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | why not legal |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 328/500 (66%) | 32% | 63% | 36% | 99% | 74% | 56% | rules 86, cards_not_held 66, parser 14, no_json 6 |
| base_verbose | granite-4.2-3b | 389/500 (78%) | 78% | 95% | 52% | 99% | 74% | 69% | cards_not_held 57, rules 53, parser 1 |
| base_verbose | gemma-4-E2B | 429/500 (86%) | 86% | 67% | 82% | 100% | 91% | 89% | rules 51, cards_not_held 20 |
| lora_verbose | LFM2.5-1.2B | 462/500 (92%) | 92% | 86% | 76% | 100% | 100% | 100% | rules 38 |
| lora_verbose | granite-4.2-3b | 451/500 (90%) | 90% | 74% | 81% | 96% | 100% | 100% | rules 45, cards_not_held 2, unknown_player 2 |
| lora_verbose | gemma-4-E2B | 439/500 (88%) | 88% | 80% | 71% | 88% | 100% | 100% | rules 49, cards_not_held 12 |
| base_verbose2 | LFM2.5-1.2B | 330/500 (66%) | 65% | 9% | 22% | 99% | 100% | 100% | rules 169, cards_not_held 1 |
| base_verbose2 | granite-4.2-3b | 410/500 (82%) | 82% | 74% | 69% | 100% | 73% | 94% | rules 57, cards_not_held 33 |
| base_verbose2 | gemma-4-E2B | 409/500 (82%) | 82% | 45% | 86% | 100% | 79% | 99% | rules 69, cards_not_held 22 |
| lora_verbose2 | LFM2.5-1.2B | 469/500 (94%) | 94% | 86% | 83% | 100% | 100% | 100% | rules 31 |
| lora_verbose2 | granite-4.2-3b | 427/500 (85%) | 85% | 33% | 96% | 98% | 100% | 100% | rules 71, cards_not_held 2 |
| lora_verbose2 | gemma-4-E2B | 394/500 (79%) | 79% | 37% | 93% | 69% | 95% | 100% | rules 70, unknown_player 27, cards_not_held 9 |
| base_compact | LFM2.5-1.2B | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | 0% | no_json 500 |
| base_compact | granite-4.2-3b | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | 0% | no_json 500 |
| base_compact | gemma-4-E2B | 55/500 (11%) | 0% | 0% | 0% | 0% | 55% | 0% | no_json 438, rules 6, parser 1 |
| lora_compact | LFM2.5-1.2B | 489/500 (98%) | 98% | 100% | 89% | 100% | 100% | 100% | rules 11 |
| lora_compact | granite-4.2-3b | 499/500 (100%) | 100% | 100% | 99% | 100% | 100% | 100% | rules 1 |
| lora_compact | gemma-4-E2B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | LFM2.5-1.2B | 379/500 (76%) | 76% | 100% | 84% | 88% | 50% | 57% | cards_not_held 104, rules 16, no_cards 1 |
| base_grammar | granite-4.2-3b | 448/500 (90%) | 90% | 100% | 88% | 100% | 72% | 88% | cards_not_held 39, rules 12, no_json 1 |
| base_grammar | gemma-4-E2B | 466/500 (93%) | 93% | 100% | 94% | 98% | 87% | 87% | cards_not_held 26, rules 6, no_cards 2 |
| lora_grammar | LFM2.5-1.2B | 418/500 (84%) | 84% | 100% | 85% | 33% | 100% | 100% | no_cards 65, rules 15, cards_not_held 2 |
| lora_grammar | granite-4.2-3b | 451/500 (90%) | 90% | 100% | 99% | 52% | 100% | 100% | no_cards 47, rules 1, cards_not_held 1 |
| lora_grammar | gemma-4-E2B | 397/500 (79%) | 79% | 100% | 89% | 8% | 100% | 100% | no_cards 92, rules 11 |

## Valid play

Does the answer keep every rule the teacher plays by?

| condition | model | valid play (95% CI) | PLANTING | FORCED | TRADING | REPLY | CONSIDERING |
|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 30% [27–35] | 10% | 8% | 79% | 32% | 23% |
| base_verbose | granite-4.2-3b | 43% [38–47] | 29% | 16% | 95% | 32% | 41% |
| base_verbose | gemma-4-E2B | 38% [34–43] | 13% | 18% | 59% | 51% | 50% |
| lora_verbose | LFM2.5-1.2B | 47% [43–51] | 17% | 23% | 79% | 51% | 65% |
| lora_verbose | granite-4.2-3b | 71% [66–74] | 41% | 70% | 84% | 75% | 83% |
| lora_verbose | gemma-4-E2B | 46% [42–50] | 26% | 33% | 55% | 51% | 65% |
| base_verbose2 | LFM2.5-1.2B | 35% [31–39] | 4% | 3% | 52% | 50% | 65% |
| base_verbose2 | granite-4.2-3b | 40% [36–45] | 19% | 21% | 69% | 33% | 60% |
| base_verbose2 | gemma-4-E2B | 47% [43–52] | 10% | 30% | 100% | 34% | 62% |
| lora_verbose2 | LFM2.5-1.2B | 48% [44–52] | 13% | 26% | 86% | 50% | 65% |
| lora_verbose2 | granite-4.2-3b | 68% [64–72] | 26% | 69% | 88% | 83% | 76% |
| lora_verbose2 | gemma-4-E2B | 43% [38–47] | 18% | 34% | 53% | 40% | 68% |
| base_compact | LFM2.5-1.2B | 0% [0–1] | 0% | 0% | 0% | 0% | 0% |
| base_compact | granite-4.2-3b | 0% [0–1] | 0% | 0% | 0% | 0% | 0% |
| base_compact | gemma-4-E2B | 6% [4–8] | 0% | 0% | 0% | 29% | 0% |
| lora_compact | LFM2.5-1.2B | 89% [86–91] | 89% | 84% | 100% | 98% | 74% |
| lora_compact | granite-4.2-3b | 97% [95–98] | 92% | 92% | 100% | 100% | 100% |
| lora_compact | gemma-4-E2B | 96% [94–98] | 93% | 91% | 100% | 100% | 98% |
| base_grammar | LFM2.5-1.2B | 24% [20–28] | 12% | 22% | 58% | 5% | 22% |
| base_grammar | granite-4.2-3b | 42% [38–46] | 11% | 24% | 100% | 19% | 55% |
| base_grammar | gemma-4-E2B | 37% [33–42] | 9% | 28% | 63% | 30% | 57% |
| lora_grammar | LFM2.5-1.2B | 39% [35–43] | 16% | 39% | 24% | 50% | 65% |
| lora_grammar | granite-4.2-3b | 71% [67–75] | 48% | 82% | 50% | 83% | 92% |
| lora_grammar | gemma-4-E2B | 42% [37–46] | 27% | 40% | 8% | 68% | 65% |
| teacher | training corpus | 100% [100–100] | 100% | 100% | 100% | 100% | 100% |

Each rule on its own (partial credit):

| condition | model | PLANT: first card placed | PLANT: second card without harvest | FORCE: no avoidable harvest | FORCE: least valuable stack lost | TRADI: keeps growing beans | REPLY: accepts iff useful | REPLY: keeps growing beans | CONSI: accepts iff useful |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 15% | 45% | 14% | 30% | 79% | 41% | 63% | 23% |
| base_verbose | granite-4.2-3b | 29% | 95% | 32% | 36% | 95% | 35% | 60% | 41% |
| base_verbose | gemma-4-E2B | 13% | 62% | 56% | 44% | 59% | 52% | 86% | 50% |
| lora_verbose | LFM2.5-1.2B | 33% | 50% | 50% | 49% | 79% | 51% | 100% | 65% |
| lora_verbose | granite-4.2-3b | 60% | 51% | 77% | 74% | 84% | 75% | 100% | 83% |
| lora_verbose | gemma-4-E2B | 28% | 78% | 56% | 48% | 55% | 51% | 100% | 65% |
| base_verbose2 | LFM2.5-1.2B | 5% | 7% | 16% | 9% | 52% | 50% | 100% | 65% |
| base_verbose2 | granite-4.2-3b | 21% | 71% | 50% | 40% | 69% | 37% | 56% | 60% |
| base_verbose2 | gemma-4-E2B | 13% | 29% | 64% | 52% | 100% | 38% | 68% | 62% |
| lora_verbose2 | LFM2.5-1.2B | 29% | 44% | 57% | 52% | 86% | 50% | 100% | 65% |
| lora_verbose2 | granite-4.2-3b | 29% | 28% | 87% | 78% | 88% | 83% | 100% | 76% |
| lora_verbose2 | gemma-4-E2B | 26% | 25% | 69% | 58% | 53% | 49% | 71% | 68% |
| base_compact | LFM2.5-1.2B | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| base_compact | granite-4.2-3b | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| base_compact | gemma-4-E2B | 0% | 0% | 0% | 0% | 0% | 29% | 55% | 0% |
| lora_compact | LFM2.5-1.2B | 89% | 100% | 88% | 85% | 100% | 100% | 98% | 74% |
| lora_compact | granite-4.2-3b | 92% | 100% | 98% | 93% | 100% | 100% | 100% | 100% |
| lora_compact | gemma-4-E2B | 93% | 100% | 98% | 93% | 100% | 100% | 100% | 98% |
| base_grammar | LFM2.5-1.2B | 33% | 29% | 50% | 56% | 58% | 26% | 27% | 22% |
| base_grammar | granite-4.2-3b | 33% | 27% | 56% | 56% | 100% | 32% | 45% | 55% |
| base_grammar | gemma-4-E2B | 29% | 37% | 66% | 56% | 63% | 49% | 55% | 57% |
| lora_grammar | LFM2.5-1.2B | 32% | 47% | 66% | 58% | 24% | 50% | 100% | 65% |
| lora_grammar | granite-4.2-3b | 79% | 60% | 98% | 83% | 50% | 83% | 100% | 92% |
| lora_grammar | gemma-4-E2B | 41% | 70% | 72% | 57% | 8% | 68% | 100% | 65% |
| teacher | training corpus | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |

## Reference-correctness

Does the answer make the decision the reference bot makes in the same state?

| condition | model | correct (95% CI) | PLANTING | FORCED | TRADING | REPLY | CONSIDERING |
|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 8% [6–11] | 7% | 7% | 0% | 26% | 0% |
| base_verbose | granite-4.2-3b | 16% [13–19] | 23% | 11% | 44% | 0% | 1% |
| base_verbose | gemma-4-E2B | 7% [5–9] | 9% | 17% | 1% | 6% | 0% |
| lora_verbose | LFM2.5-1.2B | 28% [25–33] | 8% | 18% | 1% | 50% | 65% |
| lora_verbose | granite-4.2-3b | 50% [46–54] | 28% | 60% | 29% | 50% | 83% |
| lora_verbose | gemma-4-E2B | 37% [33–41] | 21% | 27% | 22% | 50% | 65% |
| base_verbose2 | LFM2.5-1.2B | 24% [20–28] | 3% | 1% | 0% | 50% | 65% |
| base_verbose2 | granite-4.2-3b | 6% [4–8] | 13% | 16% | 0% | 0% | 0% |
| base_verbose2 | gemma-4-E2B | 16% [13–20] | 3% | 26% | 42% | 0% | 11% |
| lora_verbose2 | LFM2.5-1.2B | 31% [27–36] | 4% | 23% | 15% | 50% | 65% |
| lora_verbose2 | granite-4.2-3b | 48% [43–52] | 20% | 58% | 34% | 50% | 76% |
| lora_verbose2 | gemma-4-E2B | 23% [20–27] | 9% | 27% | 3% | 11% | 66% |
| base_compact | LFM2.5-1.2B | 0% [0–1] | 0% | 0% | 0% | 0% | 0% |
| base_compact | granite-4.2-3b | 0% [0–1] | 0% | 0% | 0% | 0% | 0% |
| base_compact | gemma-4-E2B | 6% [4–8] | 0% | 0% | 0% | 29% | 0% |
| lora_compact | LFM2.5-1.2B | 87% [84–90] | 89% | 82% | 96% | 95% | 74% |
| lora_compact | granite-4.2-3b | 95% [93–97] | 92% | 88% | 95% | 100% | 100% |
| lora_compact | gemma-4-E2B | 94% [91–96] | 93% | 84% | 96% | 98% | 98% |
| base_grammar | LFM2.5-1.2B | 6% [5–9] | 9% | 20% | 1% | 2% | 0% |
| base_grammar | granite-4.2-3b | 16% [13–19] | 11% | 20% | 47% | 0% | 0% |
| base_grammar | gemma-4-E2B | 12% [10–15] | 6% | 24% | 1% | 1% | 29% |
| lora_grammar | LFM2.5-1.2B | 34% [30–38] | 8% | 36% | 10% | 50% | 65% |
| lora_grammar | granite-4.2-3b | 58% [54–62] | 34% | 72% | 40% | 53% | 92% |
| lora_grammar | gemma-4-E2B | 36% [32–40] | 24% | 37% | 4% | 50% | 65% |
| teacher | training corpus | 100% [100–100] | 100% | 100% | 100% | 100% | 100% |

## State sensitivity

Does the decision depend on the game state?

| condition | model | REPLY accepts useful / useless | gap | CONSIDERING accepts useful / useless | gap | PLANTING avoidable harvests | FORCED avoidable harvests | TRADING passes | offers giving away a growing bean |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | LFM2.5-1.2B | 41% / 30% | +11 | 100% / 100% | +0 | 50/63 (79%) | 22/36 (61%) | 0% | 23/99 (23%) |
| base_verbose | granite-4.2-3b | 6% / 15% | -10 | 4% / 7% | -3 | 43/95 (45%) | 20/52 (38%) | 95% | 4/5 (80%) |
| base_verbose | gemma-4-E2B | 30% / 19% | +11 | 25% / 26% | -1 | 32/67 (48%) | 26/82 (32%) | 0% | 44/100 (44%) |
| lora_verbose | LFM2.5-1.2B | 2% / 0% | +2 | 0% / 0% | +0 | 66/86 (77%) | 26/76 (34%) | 0% | 24/100 (24%) |
| lora_verbose | granite-4.2-3b | 50% / 0% | +50 | 51% / 0% | +51 | 27/74 (36%) | 4/81 (5%) | 1% | 15/95 (16%) |
| lora_verbose | gemma-4-E2B | 2% / 0% | +2 | 0% / 0% | +0 | 30/80 (38%) | 15/71 (21%) | 1% | 36/87 (41%) |
| base_verbose2 | LFM2.5-1.2B | 0% / 0% | +0 | 0% / 0% | +0 | 4/9 (44%) | 6/22 (27%) | 0% | 50/99 (51%) |
| base_verbose2 | granite-4.2-3b | 0% / 0% | +0 | 0% / 0% | +0 | 37/74 (50%) | 19/69 (28%) | 0% | 34/100 (34%) |
| base_verbose2 | gemma-4-E2B | 5% / 5% | -0 | 0% / 5% | -5 | 27/45 (60%) | 22/86 (26%) | 91% | 1/9 (11%) |
| lora_verbose2 | LFM2.5-1.2B | 0% / 0% | +0 | 0% / 0% | +0 | 68/86 (79%) | 26/83 (31%) | 26% | 15/74 (20%) |
| lora_verbose2 | granite-4.2-3b | 66% / 0% | +66 | 34% / 2% | +33 | 5/33 (15%) | 9/96 (9%) | 31% | 11/68 (16%) |
| lora_verbose2 | gemma-4-E2B | 0% / 0% | +0 | 14% / 3% | +11 | 15/37 (41%) | 24/93 (26%) | 0% | 19/69 (28%) |
| base_compact | LFM2.5-1.2B | – / – | – | – / – | – | – | – | – | – |
| base_compact | granite-4.2-3b | – / – | – | – / – | – | – | – | – | – |
| base_compact | gemma-4-E2B | 0% / 0% | +0 | – / – | – | – | – | – | – |
| lora_compact | LFM2.5-1.2B | 100% / 0% | +100 | 54% / 15% | +39 | 0/100 (0%) | 1/89 (1%) | 47% | 0/53 (0%) |
| lora_compact | granite-4.2-3b | 100% / 0% | +100 | 100% / 0% | +100 | 0/100 (0%) | 1/99 (1%) | 47% | 0/53 (0%) |
| lora_compact | gemma-4-E2B | 100% / 0% | +100 | 97% / 2% | +96 | 0/100 (0%) | 2/100 (2%) | 47% | 0/53 (0%) |
| base_grammar | LFM2.5-1.2B | 100% / 100% | +0 | 96% / 100% | -4 | 82/100 (82%) | 34/84 (40%) | 0% | 33/88 (38%) |
| base_grammar | granite-4.2-3b | 3% / 9% | -6 | 23% / 17% | +6 | 84/100 (84%) | 32/88 (36%) | 100% | – |
| base_grammar | gemma-4-E2B | 12% / 4% | +8 | 0% / 0% | +0 | 81/100 (81%) | 28/94 (30%) | 0% | 37/98 (38%) |
| lora_grammar | LFM2.5-1.2B | 0% / 0% | +0 | 0% / 0% | +0 | 77/100 (77%) | 19/85 (22%) | 0% | 9/33 (27%) |
| lora_grammar | granite-4.2-3b | 68% / 2% | +66 | 77% / 0% | +77 | 46/100 (46%) | 1/99 (1%) | 0% | 2/52 (4%) |
| lora_grammar | gemma-4-E2B | 40% / 4% | +36 | 0% / 0% | +0 | 59/100 (59%) | 17/89 (19%) | 0% | 0/8 (0%) |
| teacher | training corpus | 100% / 0% | +100 | 100% / 0% | +100 | 0/3000 (0%) | 0/3000 (0%) | 43% | 0/1712 (0%) |

## Agreement

Given the same item, do two settings make the same decision?

Same decision on the same item (95% CI; compared items in brackets).

| LFM2.5-1.2B | base_verbose | lora_verbose | base_verbose2 | lora_verbose2 | base_compact | lora_compact | base_grammar | lora_grammar |
|---|---|---|---|---|---|---|---|---|
| base_verbose | · | 41% [37–46] (480) | 13% [10–16] (480) | 19% [16–22] (480) | – (0) | 9% [6–11] (480) | 31% [27–36] (480) | 14% [11–17] (480) |
| lora_verbose | 41% [37–46] (480) | · | 44% [39–48] (500) | 59% [54–63] (500) | – (0) | 30% [26–34] (500) | 15% [12–19] (500) | 51% [46–55] (500) |
| base_verbose2 | 13% [10–16] (480) | 44% [39–48] (500) | · | 46% [41–50] (500) | – (0) | 25% [22–29] (500) | 6% [4–9] (500) | 43% [39–47] (500) |
| lora_verbose2 | 19% [16–22] (480) | 59% [54–63] (500) | 46% [41–50] (500) | · | – (0) | 33% [29–38] (500) | 13% [11–16] (500) | 56% [52–60] (500) |
| base_compact | – (0) | – (0) | – (0) | – (0) | · | – (0) | – (0) | – (0) |
| lora_compact | 9% [6–11] (480) | 30% [26–34] (500) | 25% [22–29] (500) | 33% [29–38] (500) | – (0) | · | 7% [5–10] (500) | 36% [32–40] (500) |
| base_grammar | 31% [27–36] (480) | 15% [12–19] (500) | 6% [4–9] (500) | 13% [11–16] (500) | – (0) | 7% [5–10] (500) | · | 15% [12–18] (500) |
| lora_grammar | 14% [11–17] (480) | 51% [46–55] (500) | 43% [39–47] (500) | 56% [52–60] (500) | – (0) | 36% [32–40] (500) | 15% [12–18] (500) | · |

| granite-4.2-3b | base_verbose | lora_verbose | base_verbose2 | lora_verbose2 | base_compact | lora_compact | base_grammar | lora_grammar |
|---|---|---|---|---|---|---|---|---|
| base_verbose | · | 5% [4–8] (499) | 31% [27–35] (499) | 11% [9–14] (499) | – (0) | 16% [13–19] (499) | 37% [33–41] (498) | 4% [2–6] (499) |
| lora_verbose | 5% [4–8] (499) | · | 9% [7–12] (500) | 56% [51–60] (500) | – (0) | 51% [47–56] (500) | 7% [5–9] (499) | 65% [61–69] (500) |
| base_verbose2 | 31% [27–35] (499) | 9% [7–12] (500) | · | 9% [7–12] (500) | – (0) | 5% [4–8] (500) | 8% [6–11] (499) | 5% [3–7] (500) |
| lora_verbose2 | 11% [9–14] (499) | 56% [51–60] (500) | 9% [7–12] (500) | · | – (0) | 48% [44–52] (500) | 11% [9–15] (499) | 53% [48–57] (500) |
| base_compact | – (0) | – (0) | – (0) | – (0) | · | – (0) | – (0) | – (0) |
| lora_compact | 16% [13–19] (499) | 51% [47–56] (500) | 5% [4–8] (500) | 48% [44–52] (500) | – (0) | · | 16% [13–20] (499) | 58% [54–63] (500) |
| base_grammar | 37% [33–41] (498) | 7% [5–9] (499) | 8% [6–11] (499) | 11% [9–15] (499) | – (0) | 16% [13–20] (499) | · | 9% [7–12] (499) |
| lora_grammar | 4% [2–6] (499) | 65% [61–69] (500) | 5% [3–7] (500) | 53% [48–57] (500) | – (0) | 58% [54–63] (500) | 9% [7–12] (499) | · |

| gemma-4-E2B | base_verbose | lora_verbose | base_verbose2 | lora_verbose2 | base_compact | lora_compact | base_grammar | lora_grammar |
|---|---|---|---|---|---|---|---|---|
| base_verbose | · | 21% [18–25] (500) | 28% [24–32] (500) | 19% [15–22] (500) | 7% [3–16] (61) | 7% [5–9] (500) | 31% [27–35] (500) | 16% [13–20] (500) |
| lora_verbose | 21% [18–25] (500) | · | 18% [15–22] (500) | 39% [34–43] (500) | 89% [78–94] (61) | 37% [33–41] (500) | 23% [20–27] (500) | 55% [50–59] (500) |
| base_verbose2 | 28% [24–32] (500) | 18% [15–22] (500) | · | 25% [22–29] (500) | 0% [0–6] (61) | 17% [14–20] (500) | 26% [22–30] (500) | 17% [14–21] (500) |
| lora_verbose2 | 19% [15–22] (500) | 39% [34–43] (500) | 25% [22–29] (500) | · | 21% [13–33] (61) | 24% [20–28] (500) | 26% [22–30] (500) | 35% [31–39] (500) |
| base_compact | 7% [3–16] (61) | 89% [78–94] (61) | 0% [0–6] (61) | 21% [13–33] (61) | · | 48% [36–60] (61) | 0% [0–6] (61) | 77% [65–86] (61) |
| lora_compact | 7% [5–9] (500) | 37% [33–41] (500) | 17% [14–20] (500) | 24% [20–28] (500) | 48% [36–60] (61) | · | 12% [10–15] (500) | 36% [32–40] (500) |
| base_grammar | 31% [27–35] (500) | 23% [20–27] (500) | 26% [22–30] (500) | 26% [22–30] (500) | 0% [0–6] (61) | 12% [10–15] (500) | · | 26% [22–30] (500) |
| lora_grammar | 16% [13–20] (500) | 55% [50–59] (500) | 17% [14–21] (500) | 35% [31–39] (500) | 77% [65–86] (61) | 36% [32–40] (500) | 26% [22–30] (500) | · |

