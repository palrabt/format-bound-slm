# replay_20261006_2x4: game states

replay run, backend gpu; 500 answers per model and condition; training corpus `training/corpus/training_data_synct_15000_llm.txt`; evaluated 2026-11-12 13:12. Shares in brackets are 95% Wilson intervals.

## Overview

| condition | model | answers | schema-valid | legal | reference-correct | accept gap useful−useless | avoidable harvests |
|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 500 | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| base_verbose | Qwen2.5-3B | 500 | 100% [99–100] | 94% [92–96] | 44% [40–48] | +0 | 44% |
| base_verbose | gemma-2b | 500 | 99% [98–100] | 79% [75–82] | 37% [33–42] | +0 | 49% |
| lora_verbose | TinyLlama-1.1B | 500 | 80% [76–83] | 92% [90–94] | 46% [41–50] | +0 | 40% |
| lora_verbose | Qwen2.5-3B | 500 | 100% [99–100] | 85% [82–88] | 45% [40–49] | +0 | 36% |
| lora_verbose | gemma-2b | 500 | 100% [99–100] | 97% [95–98] | 44% [40–48] | +0 | 52% |
| base_verbose2 | TinyLlama-1.1B | 500 | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| base_verbose2 | Qwen2.5-3B | 500 | 98% [96–99] | 91% [88–93] | 38% [33–42] | +0 | 60% |
| base_verbose2 | gemma-2b | 500 | 97% [95–98] | 69% [65–73] | 32% [28–36] | +0 | 46% |
| lora_verbose2 | TinyLlama-1.1B | 500 | 79% [76–83] | 89% [86–91] | 49% [45–53] | +0 | 38% |
| lora_verbose2 | Qwen2.5-3B | 500 | 98% [96–99] | 94% [92–96] | 43% [39–47] | +0 | 39% |
| lora_verbose2 | gemma-2b | 500 | 98% [97–99] | 86% [83–89] | 39% [34–43] | +0 | 52% |
| base_compact | TinyLlama-1.1B | 500 | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| base_compact | Qwen2.5-3B | 500 | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| base_compact | gemma-2b | 500 | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| lora_compact | TinyLlama-1.1B | 500 | 100% [99–100] | 99% [97–99] | 69% [65–73] | +0 | 2% |
| lora_compact | Qwen2.5-3B | 500 | 100% [99–100] | 100% [99–100] | 75% [71–79] | +19 | 1% |
| lora_compact | gemma-2b | 500 | 100% [99–100] | 100% [99–100] | 73% [69–77] | +15 | 4% |
| base_grammar | TinyLlama-1.1B | 500 | 96% [94–98] | 83% [80–86] | 22% [19–26] | +0 | 66% |
| base_grammar | Qwen2.5-3B | 500 | 100% [99–100] | 98% [97–99] | 37% [33–42] | +1 | 64% |
| base_grammar | gemma-2b | 500 | 100% [99–100] | 86% [83–89] | 30% [27–35] | +0 | 62% |
| lora_grammar | TinyLlama-1.1B | 500 | 100% [99–100] | 97% [96–98] | 40% [36–44] | +0 | 51% |
| lora_grammar | Qwen2.5-3B | 500 | 100% [99–100] | 99% [98–100] | 50% [45–54] | +0 | 37% |
| lora_grammar | gemma-2b | 500 | 97% [95–98] | 97% [95–98] | 39% [35–44] | +1 | 61% |

## Effects

How much do the adapter and the prompt style change an outcome, item by item?

Rows marked * stay significant after the Holm correction.

### schema-valid

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| TinyLlama-1.1B | adapter at verbose | 500 | 0% | 80% | +80 [+76, +83] | 0 / 400 | <0.001 | <0.001 * |
| TinyLlama-1.1B | adapter at verbose2 | 500 | 0% | 79% | +79 [+76, +83] | 0 / 397 | <0.001 | <0.001 * |
| TinyLlama-1.1B | adapter at compact | 500 | 0% | 100% | +100 [+100, +100] | 0 / 500 | <0.001 | <0.001 * |
| TinyLlama-1.1B | adapter at grammar | 500 | 96% | 100% | +3 [+2, +5] | 1 / 17 | <0.001 | 0.003 * |
| TinyLlama-1.1B | base: verbose2 vs verbose | 500 | 0% | 0% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| TinyLlama-1.1B | base: compact vs verbose | 500 | 0% | 0% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| TinyLlama-1.1B | base: grammar vs verbose | 500 | 0% | 96% | +96 [+95, +98] | 0 / 482 | <0.001 | <0.001 * |
| TinyLlama-1.1B | lora: verbose2 vs verbose | 500 | 80% | 79% | -1 [-1, +0] | 3 / 0 | 0.250 | 1.000 |
| TinyLlama-1.1B | lora: compact vs verbose | 500 | 80% | 100% | +20 [+17, +24] | 0 / 100 | <0.001 | <0.001 * |
| TinyLlama-1.1B | lora: grammar vs verbose | 500 | 80% | 100% | +20 [+16, +23] | 0 / 98 | <0.001 | <0.001 * |
| Qwen2.5-3B | adapter at verbose | 500 | 100% | 100% | +0 [+0, +1] | 0 / 2 | 0.500 | 1.000 |
| Qwen2.5-3B | adapter at verbose2 | 500 | 98% | 98% | -0 [-2, +1] | 12 / 10 | 0.832 | 1.000 |
| Qwen2.5-3B | adapter at compact | 500 | 0% | 100% | +100 [+100, +100] | 0 / 500 | <0.001 | <0.001 * |
| Qwen2.5-3B | adapter at grammar | 500 | 100% | 100% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| Qwen2.5-3B | base: verbose2 vs verbose | 500 | 100% | 98% | -2 [-3, -0] | 10 / 2 | 0.039 | 0.540 |
| Qwen2.5-3B | base: compact vs verbose | 500 | 100% | 0% | -100 [-100, -99] | 498 / 0 | <0.001 | <0.001 * |
| Qwen2.5-3B | base: grammar vs verbose | 500 | 100% | 100% | +0 [+0, +1] | 0 / 2 | 0.500 | 1.000 |
| Qwen2.5-3B | lora: verbose2 vs verbose | 500 | 100% | 98% | -2 [-4, -1] | 12 / 0 | <0.001 | 0.008 * |
| Qwen2.5-3B | lora: compact vs verbose | 500 | 100% | 100% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| Qwen2.5-3B | lora: grammar vs verbose | 500 | 100% | 100% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| gemma-2b | adapter at verbose | 500 | 99% | 100% | +0 [-0, +1] | 1 / 3 | 0.625 | 1.000 |
| gemma-2b | adapter at verbose2 | 500 | 97% | 98% | +1 [-1, +3] | 9 / 14 | 0.405 | 1.000 |
| gemma-2b | adapter at compact | 500 | 0% | 100% | +100 [+100, +100] | 0 / 500 | <0.001 | <0.001 * |
| gemma-2b | adapter at grammar | 500 | 100% | 97% | -3 [-5, -2] | 16 / 0 | <0.001 | <0.001 * |
| gemma-2b | base: verbose2 vs verbose | 500 | 99% | 97% | -2 [-4, -1] | 14 / 3 | 0.013 | 0.204 |
| gemma-2b | base: compact vs verbose | 500 | 99% | 0% | -99 [-100, -99] | 497 / 0 | <0.001 | <0.001 * |
| gemma-2b | base: grammar vs verbose | 500 | 99% | 100% | +1 [+0, +1] | 0 / 3 | 0.250 | 1.000 |
| gemma-2b | lora: verbose2 vs verbose | 500 | 100% | 98% | -2 [-3, -0] | 9 / 1 | 0.021 | 0.322 |
| gemma-2b | lora: compact vs verbose | 500 | 100% | 100% | +0 [+0, +1] | 0 / 1 | 1.000 | 1.000 |
| gemma-2b | lora: grammar vs verbose | 500 | 100% | 97% | -3 [-5, -2] | 16 / 1 | <0.001 | 0.005 * |

### legal

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| TinyLlama-1.1B | adapter at verbose | 500 | 0% | 92% | +92 [+90, +94] | 0 / 462 | <0.001 | <0.001 * |
| TinyLlama-1.1B | adapter at verbose2 | 500 | 0% | 89% | +89 [+86, +91] | 0 / 443 | <0.001 | <0.001 * |
| TinyLlama-1.1B | adapter at compact | 500 | 0% | 99% | +99 [+98, +99] | 0 / 493 | <0.001 | <0.001 * |
| TinyLlama-1.1B | adapter at grammar | 500 | 83% | 97% | +14 [+11, +18] | 9 / 79 | <0.001 | <0.001 * |
| TinyLlama-1.1B | base: verbose2 vs verbose | 500 | 0% | 0% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| TinyLlama-1.1B | base: compact vs verbose | 500 | 0% | 0% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| TinyLlama-1.1B | base: grammar vs verbose | 500 | 0% | 83% | +83 [+80, +87] | 0 / 417 | <0.001 | <0.001 * |
| TinyLlama-1.1B | lora: verbose2 vs verbose | 500 | 92% | 89% | -4 [-7, -0] | 51 / 32 | 0.048 | 0.285 |
| TinyLlama-1.1B | lora: compact vs verbose | 500 | 92% | 99% | +6 [+4, +9] | 5 / 36 | <0.001 | <0.001 * |
| TinyLlama-1.1B | lora: grammar vs verbose | 500 | 92% | 97% | +5 [+2, +8] | 11 / 36 | <0.001 | 0.003 * |
| Qwen2.5-3B | adapter at verbose | 500 | 94% | 85% | -9 [-12, -6] | 60 / 15 | <0.001 | <0.001 * |
| Qwen2.5-3B | adapter at verbose2 | 500 | 91% | 94% | +3 [+0, +6] | 14 / 29 | 0.032 | 0.221 |
| Qwen2.5-3B | adapter at compact | 500 | 0% | 100% | +100 [+99, +100] | 0 / 498 | <0.001 | <0.001 * |
| Qwen2.5-3B | adapter at grammar | 500 | 98% | 99% | +1 [+0, +2] | 1 / 7 | 0.070 | 0.320 |
| Qwen2.5-3B | base: verbose2 vs verbose | 500 | 94% | 91% | -3 [-7, -0] | 41 / 25 | 0.064 | 0.320 |
| Qwen2.5-3B | base: compact vs verbose | 500 | 94% | 0% | -94 [-96, -92] | 472 / 0 | <0.001 | <0.001 * |
| Qwen2.5-3B | base: grammar vs verbose | 500 | 94% | 98% | +4 [+2, +6] | 8 / 27 | 0.002 | 0.015 * |
| Qwen2.5-3B | lora: verbose2 vs verbose | 500 | 85% | 94% | +9 [+5, +12] | 14 / 58 | <0.001 | <0.001 * |
| Qwen2.5-3B | lora: compact vs verbose | 500 | 85% | 100% | +14 [+11, +17] | 0 / 71 | <0.001 | <0.001 * |
| Qwen2.5-3B | lora: grammar vs verbose | 500 | 85% | 99% | +14 [+11, +17] | 3 / 73 | <0.001 | <0.001 * |
| gemma-2b | adapter at verbose | 500 | 79% | 97% | +18 [+14, +22] | 7 / 97 | <0.001 | <0.001 * |
| gemma-2b | adapter at verbose2 | 500 | 69% | 86% | +17 [+13, +21] | 14 / 98 | <0.001 | <0.001 * |
| gemma-2b | adapter at compact | 500 | 0% | 100% | +100 [+100, +100] | 0 / 500 | <0.001 | <0.001 * |
| gemma-2b | adapter at grammar | 500 | 86% | 97% | +10 [+7, +14] | 9 / 61 | <0.001 | <0.001 * |
| gemma-2b | base: verbose2 vs verbose | 500 | 79% | 69% | -9 [-14, -5] | 92 / 45 | <0.001 | <0.001 * |
| gemma-2b | base: compact vs verbose | 500 | 79% | 0% | -79 [-82, -75] | 394 / 0 | <0.001 | <0.001 * |
| gemma-2b | base: grammar vs verbose | 500 | 79% | 86% | +7 [+3, +12] | 44 / 81 | 0.001 | 0.011 * |
| gemma-2b | lora: verbose2 vs verbose | 500 | 97% | 86% | -11 [-14, -8] | 63 / 10 | <0.001 | <0.001 * |
| gemma-2b | lora: compact vs verbose | 500 | 97% | 100% | +3 [+2, +5] | 0 / 16 | <0.001 | <0.001 * |
| gemma-2b | lora: grammar vs verbose | 500 | 97% | 97% | -0 [-2, +2] | 17 / 16 | 1.000 | 1.000 |

### reference-correct

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| TinyLlama-1.1B | adapter at verbose | 500 | 0% | 46% | +46 [+41, +50] | 0 / 229 | <0.001 | <0.001 * |
| TinyLlama-1.1B | adapter at verbose2 | 500 | 0% | 49% | +49 [+44, +53] | 0 / 245 | <0.001 | <0.001 * |
| TinyLlama-1.1B | adapter at compact | 500 | 0% | 69% | +69 [+65, +73] | 0 / 346 | <0.001 | <0.001 * |
| TinyLlama-1.1B | adapter at grammar | 500 | 22% | 40% | +17 [+13, +21] | 14 / 101 | <0.001 | <0.001 * |
| TinyLlama-1.1B | base: verbose2 vs verbose | 500 | 0% | 0% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| TinyLlama-1.1B | base: compact vs verbose | 500 | 0% | 0% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| TinyLlama-1.1B | base: grammar vs verbose | 500 | 0% | 22% | +22 [+19, +26] | 0 / 112 | <0.001 | <0.001 * |
| TinyLlama-1.1B | lora: verbose2 vs verbose | 500 | 46% | 49% | +3 [+1, +5] | 5 / 21 | 0.002 | 0.030 * |
| TinyLlama-1.1B | lora: compact vs verbose | 500 | 46% | 69% | +23 [+19, +28] | 14 / 131 | <0.001 | <0.001 * |
| TinyLlama-1.1B | lora: grammar vs verbose | 500 | 46% | 40% | -6 [-10, -2] | 64 / 34 | 0.003 | 0.035 * |
| Qwen2.5-3B | adapter at verbose | 500 | 44% | 45% | +1 [-3, +4] | 47 / 51 | 0.762 | 1.000 |
| Qwen2.5-3B | adapter at verbose2 | 500 | 38% | 43% | +5 [-1, +11] | 113 / 139 | 0.115 | 0.755 |
| Qwen2.5-3B | adapter at compact | 500 | 0% | 75% | +75 [+72, +79] | 0 / 376 | <0.001 | <0.001 * |
| Qwen2.5-3B | adapter at grammar | 500 | 37% | 50% | +12 [+6, +18] | 103 / 164 | <0.001 | 0.004 * |
| Qwen2.5-3B | base: verbose2 vs verbose | 500 | 44% | 38% | -6 [-11, -1] | 104 / 72 | 0.019 | 0.173 |
| Qwen2.5-3B | base: compact vs verbose | 500 | 44% | 0% | -44 [-49, -40] | 220 / 0 | <0.001 | <0.001 * |
| Qwen2.5-3B | base: grammar vs verbose | 500 | 44% | 37% | -7 [-12, -2] | 97 / 64 | 0.011 | 0.114 |
| Qwen2.5-3B | lora: verbose2 vs verbose | 500 | 45% | 43% | -2 [-5, +1] | 32 / 22 | 0.220 | 0.881 |
| Qwen2.5-3B | lora: compact vs verbose | 500 | 45% | 75% | +30 [+26, +35] | 10 / 162 | <0.001 | <0.001 * |
| Qwen2.5-3B | lora: grammar vs verbose | 500 | 45% | 50% | +5 [+2, +8] | 15 / 39 | 0.001 | 0.021 * |
| gemma-2b | adapter at verbose | 500 | 37% | 44% | +7 [+4, +9] | 8 / 41 | <0.001 | <0.001 * |
| gemma-2b | adapter at verbose2 | 500 | 32% | 39% | +7 [+1, +12] | 81 / 114 | 0.022 | 0.174 |
| gemma-2b | adapter at compact | 500 | 0% | 73% | +73 [+69, +77] | 0 / 366 | <0.001 | <0.001 * |
| gemma-2b | adapter at grammar | 500 | 30% | 39% | +9 [+3, +14] | 78 / 122 | 0.002 | 0.030 * |
| gemma-2b | base: verbose2 vs verbose | 500 | 37% | 32% | -5 [-8, -3] | 38 / 12 | <0.001 | 0.005 * |
| gemma-2b | base: compact vs verbose | 500 | 37% | 0% | -37 [-41, -33] | 186 / 0 | <0.001 | <0.001 * |
| gemma-2b | base: grammar vs verbose | 500 | 37% | 30% | -7 [-10, -3] | 60 / 26 | <0.001 | 0.005 * |
| gemma-2b | lora: verbose2 vs verbose | 500 | 44% | 39% | -5 [-11, +1] | 134 / 108 | 0.108 | 0.755 |
| gemma-2b | lora: compact vs verbose | 500 | 44% | 73% | +29 [+25, +34] | 8 / 155 | <0.001 | <0.001 * |
| gemma-2b | lora: grammar vs verbose | 500 | 44% | 39% | -5 [-10, +1] | 125 / 102 | 0.144 | 0.755 |

## Schema validity (valid@1)

Is the whole answer one JSON value that matches its message type's schema, game/schemas/output/<phase>.schema.json?

| condition | model | valid | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | main failures |
|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 500 |
| base_verbose | Qwen2.5-3B | 498/500 (100%) | 98% | 100% | 100% | 100% | 100% | schema:maxItems 2 |
| base_verbose | gemma-2b | 497/500 (99%) | 100% | 97% | 100% | 100% | 100% | schema:enum 3 |
| lora_verbose | TinyLlama-1.1B | 400/500 (80%) | 100% | 100% | 0% | 100% | 100% | schema:additionalProperties 100 |
| lora_verbose | Qwen2.5-3B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_verbose | gemma-2b | 499/500 (100%) | 99% | 100% | 100% | 100% | 100% | schema:maxItems 1 |
| base_verbose2 | TinyLlama-1.1B | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 500 |
| base_verbose2 | Qwen2.5-3B | 490/500 (98%) | 98% | 100% | 92% | 100% | 100% | schema:enum 8, schema:maxItems 2 |
| base_verbose2 | gemma-2b | 486/500 (97%) | 98% | 88% | 100% | 100% | 100% | wrapped 12, schema:maxItems 2 |
| lora_verbose2 | TinyLlama-1.1B | 397/500 (79%) | 97% | 100% | 0% | 100% | 100% | schema:additionalProperties 101, schema:maxItems 2 |
| lora_verbose2 | Qwen2.5-3B | 488/500 (98%) | 100% | 88% | 100% | 100% | 100% | wrapped 12 |
| lora_verbose2 | gemma-2b | 491/500 (98%) | 91% | 100% | 100% | 100% | 100% | schema:maxItems 9 |
| base_compact | TinyLlama-1.1B | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 500 |
| base_compact | Qwen2.5-3B | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 500 |
| base_compact | gemma-2b | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 500 |
| lora_compact | TinyLlama-1.1B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | Qwen2.5-3B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | gemma-2b | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | TinyLlama-1.1B | 482/500 (96%) | 100% | 100% | 98% | 85% | 99% | not_json 18 |
| base_grammar | Qwen2.5-3B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | gemma-2b | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_grammar | TinyLlama-1.1B | 498/500 (100%) | 100% | 100% | 98% | 100% | 100% | schema:minItems 2 |
| lora_grammar | Qwen2.5-3B | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_grammar | gemma-2b | 484/500 (97%) | 100% | 100% | 84% | 100% | 100% | schema:minItems 16 |

## Legality

Would the game carry out the answer as the model wrote it?

| condition | model | legal | valid & legal | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | why not legal |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | 0% | no_json 500 |
| base_verbose | Qwen2.5-3B | 472/500 (94%) | 94% | 98% | 74% | 100% | 100% | 100% | rules 28 |
| base_verbose | gemma-2b | 394/500 (79%) | 79% | 75% | 56% | 100% | 71% | 92% | rules 66, cards_not_held 37, parser 3 |
| lora_verbose | TinyLlama-1.1B | 462/500 (92%) | 72% | 99% | 89% | 100% | 77% | 97% | cards_not_held 26, rules 12 |
| lora_verbose | Qwen2.5-3B | 427/500 (85%) | 85% | 64% | 63% | 100% | 100% | 100% | rules 73 |
| lora_verbose | gemma-2b | 484/500 (97%) | 97% | 93% | 91% | 100% | 100% | 100% | rules 16 |
| base_verbose2 | TinyLlama-1.1B | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | 0% | no_json 500 |
| base_verbose2 | Qwen2.5-3B | 456/500 (91%) | 91% | 68% | 96% | 92% | 100% | 100% | rules 36, parser 8 |
| base_verbose2 | gemma-2b | 347/500 (69%) | 67% | 26% | 66% | 100% | 55% | 100% | rules 108, cards_not_held 45 |
| lora_verbose2 | TinyLlama-1.1B | 443/500 (89%) | 69% | 78% | 65% | 100% | 100% | 100% | rules 57 |
| lora_verbose2 | Qwen2.5-3B | 471/500 (94%) | 92% | 73% | 98% | 100% | 100% | 100% | rules 29 |
| lora_verbose2 | gemma-2b | 431/500 (86%) | 86% | 43% | 88% | 100% | 100% | 100% | rules 69 |
| base_compact | TinyLlama-1.1B | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | 0% | no_json 500 |
| base_compact | Qwen2.5-3B | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | 0% | no_json 500 |
| base_compact | gemma-2b | 0/500 (0%) | 0% | 0% | 0% | 0% | 0% | 0% | no_json 500 |
| lora_compact | TinyLlama-1.1B | 493/500 (99%) | 99% | 96% | 97% | 100% | 100% | 100% | rules 7 |
| lora_compact | Qwen2.5-3B | 498/500 (100%) | 100% | 98% | 100% | 100% | 100% | 100% | rules 2 |
| lora_compact | gemma-2b | 500/500 (100%) | 100% | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | TinyLlama-1.1B | 417/500 (83%) | 83% | 100% | 98% | 86% | 39% | 94% | cards_not_held 63, no_json 18, rules 2 |
| base_grammar | Qwen2.5-3B | 491/500 (98%) | 98% | 100% | 98% | 97% | 100% | 96% | cards_not_held 7, rules 2 |
| base_grammar | gemma-2b | 431/500 (86%) | 86% | 100% | 98% | 76% | 70% | 87% | cards_not_held 67, rules 2 |
| lora_grammar | TinyLlama-1.1B | 487/500 (97%) | 97% | 100% | 98% | 89% | 100% | 100% | cards_not_held 9, no_cards 2, rules 2 |
| lora_grammar | Qwen2.5-3B | 497/500 (99%) | 99% | 100% | 98% | 99% | 100% | 100% | rules 2, cards_not_held 1 |
| lora_grammar | gemma-2b | 483/500 (97%) | 97% | 100% | 99% | 84% | 100% | 100% | no_cards 16, rules 1 |

## Reference decisions

Does the answer make the decision a simple, value-aware rule set makes?

| condition | model | correct (95% CI) | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | teacher match |
|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 0% [0–1] | 0% | 0% | 0% | 0% | 0% | – |
| base_verbose | Qwen2.5-3B | 44% [40–48] | 35% | 3% | 82% | 50% | 50% | – |
| base_verbose | gemma-2b | 37% [33–42] | 28% | 4% | 83% | 24% | 47% | – |
| lora_verbose | TinyLlama-1.1B | 46% [41–50] | 40% | 5% | 100% | 35% | 49% | – |
| lora_verbose | Qwen2.5-3B | 45% [40–49] | 30% | 11% | 83% | 50% | 50% | – |
| lora_verbose | gemma-2b | 44% [40–48] | 26% | 10% | 83% | 50% | 50% | – |
| base_verbose2 | TinyLlama-1.1B | 0% [0–1] | 0% | 0% | 0% | 0% | 0% | – |
| base_verbose2 | Qwen2.5-3B | 38% [33–42] | 14% | 6% | 68% | 50% | 50% | – |
| base_verbose2 | gemma-2b | 32% [28–36] | 13% | 5% | 82% | 10% | 50% | – |
| lora_verbose2 | TinyLlama-1.1B | 49% [45–53] | 36% | 9% | 100% | 50% | 50% | – |
| lora_verbose2 | Qwen2.5-3B | 43% [39–47] | 30% | 15% | 69% | 50% | 50% | – |
| lora_verbose2 | gemma-2b | 39% [34–43] | 18% | 4% | 71% | 50% | 50% | – |
| base_compact | TinyLlama-1.1B | 0% [0–1] | 0% | 0% | 0% | 0% | 0% | – |
| base_compact | Qwen2.5-3B | 0% [0–1] | 0% | 0% | 0% | 0% | 0% | – |
| base_compact | gemma-2b | 0% [0–1] | 0% | 0% | 0% | 0% | 0% | – |
| lora_compact | TinyLlama-1.1B | 69% [65–73] | 68% | 87% | 96% | 45% | 50% | – |
| lora_compact | Qwen2.5-3B | 75% [71–79] | 70% | 96% | 100% | 60% | 50% | – |
| lora_compact | gemma-2b | 73% [69–77] | 73% | 84% | 99% | 60% | 50% | – |
| base_grammar | TinyLlama-1.1B | 22% [19–26] | 10% | 6% | 46% | 4% | 46% | – |
| base_grammar | Qwen2.5-3B | 37% [33–42] | 21% | 4% | 61% | 50% | 51% | – |
| base_grammar | gemma-2b | 30% [27–35] | 21% | 4% | 55% | 29% | 43% | – |
| lora_grammar | TinyLlama-1.1B | 40% [36–44] | 30% | 14% | 55% | 50% | 50% | – |
| lora_grammar | Qwen2.5-3B | 50% [45–54] | 35% | 25% | 88% | 50% | 50% | – |
| lora_grammar | gemma-2b | 39% [35–44] | 22% | 5% | 68% | 52% | 49% | – |
| teacher | training corpus | 83% [83–84] | 88% | 99% | 97% | 70% | 62% | – |

Each rule on its own (partial credit):

| condition | model | PLANT: first card placed | PLANT: second card without harvest | FORCE: no avoidable harvest | FORCE: least valuable stack lost | TRADI: keeps growing beans | REPLY: accepts iff useful | REPLY: keeps growing beans | CONSI: accepts iff useful |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| base_verbose | Qwen2.5-3B | 39% | 84% | 40% | 37% | 82% | 50% | 99% | 50% |
| base_verbose | gemma-2b | 29% | 72% | 20% | 40% | 83% | 33% | 55% | 47% |
| lora_verbose | TinyLlama-1.1B | 40% | 99% | 45% | 49% | 100% | 41% | 71% | 49% |
| lora_verbose | Qwen2.5-3B | 35% | 44% | 41% | 33% | 83% | 50% | 100% | 50% |
| lora_verbose | gemma-2b | 38% | 60% | 48% | 53% | 83% | 50% | 100% | 50% |
| base_verbose2 | TinyLlama-1.1B | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| base_verbose2 | Qwen2.5-3B | 24% | 19% | 50% | 52% | 68% | 50% | 99% | 50% |
| base_verbose2 | gemma-2b | 13% | 15% | 37% | 34% | 82% | 28% | 35% | 50% |
| lora_verbose2 | TinyLlama-1.1B | 36% | 78% | 34% | 40% | 100% | 50% | 100% | 50% |
| lora_verbose2 | Qwen2.5-3B | 31% | 68% | 57% | 56% | 69% | 50% | 100% | 50% |
| lora_verbose2 | gemma-2b | 24% | 19% | 45% | 47% | 71% | 50% | 100% | 50% |
| base_compact | TinyLlama-1.1B | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| base_compact | Qwen2.5-3B | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| base_compact | gemma-2b | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| lora_compact | TinyLlama-1.1B | 69% | 95% | 95% | 89% | 96% | 50% | 91% | 50% |
| lora_compact | Qwen2.5-3B | 70% | 97% | 100% | 96% | 100% | 69% | 91% | 50% |
| lora_compact | gemma-2b | 73% | 100% | 91% | 93% | 99% | 65% | 95% | 50% |
| base_grammar | TinyLlama-1.1B | 41% | 25% | 51% | 53% | 46% | 21% | 20% | 46% |
| base_grammar | Qwen2.5-3B | 40% | 31% | 50% | 52% | 61% | 50% | 100% | 51% |
| base_grammar | gemma-2b | 40% | 33% | 50% | 52% | 55% | 37% | 53% | 43% |
| lora_grammar | TinyLlama-1.1B | 56% | 46% | 60% | 52% | 55% | 50% | 100% | 50% |
| lora_grammar | Qwen2.5-3B | 44% | 71% | 70% | 53% | 88% | 50% | 100% | 50% |
| lora_grammar | gemma-2b | 38% | 34% | 52% | 52% | 68% | 52% | 100% | 49% |
| teacher | training corpus | 89% | 99% | 100% | 100% | 97% | 75% | 95% | 62% |

## State sensitivity

Does the decision depend on the game state?

| condition | model | REPLY accepts useful / useless | gap | CONSIDERING accepts useful / useless | gap | PLANTING avoidable harvests | FORCED avoidable harvests | TRADING passes | offers giving away a growing bean |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | – / – | – | – / – | – | – | – | – | – |
| base_verbose | Qwen2.5-3B | 28% / 28% | +0 | 100% / 100% | +0 | 42/98 (43%) | 34/74 (46%) | 0% | 18/100 (18%) |
| base_verbose | gemma-2b | 100% / 100% | +0 | 100% / 100% | +0 | 28/75 (37%) | 36/56 (64%) | 0% | 17/100 (17%) |
| lora_verbose | TinyLlama-1.1B | 100% / 100% | +0 | 100% / 100% | +0 | 32/99 (32%) | 44/89 (49%) | 100% | – |
| lora_verbose | Qwen2.5-3B | 100% / 100% | +0 | 100% / 100% | +0 | 24/64 (38%) | 22/63 (35%) | 0% | 17/100 (17%) |
| lora_verbose | gemma-2b | 100% / 100% | +0 | 100% / 100% | +0 | 52/93 (56%) | 43/91 (47%) | 0% | 17/100 (17%) |
| base_verbose2 | TinyLlama-1.1B | – / – | – | – / – | – | – | – | – | – |
| base_verbose2 | Qwen2.5-3B | 0% / 0% | +0 | 0% / 0% | +0 | 52/68 (76%) | 46/96 (48%) | 1% | 24/91 (26%) |
| base_verbose2 | gemma-2b | 100% / 100% | +0 | 100% / 100% | +0 | 13/26 (50%) | 29/66 (44%) | 0% | 18/100 (18%) |
| lora_verbose2 | TinyLlama-1.1B | 100% / 100% | +0 | 100% / 100% | +0 | 23/78 (29%) | 31/65 (48%) | 100% | – |
| lora_verbose2 | Qwen2.5-3B | 100% / 100% | +0 | 100% / 100% | +0 | 26/73 (36%) | 41/98 (42%) | 0% | 31/100 (31%) |
| lora_verbose2 | gemma-2b | 0% / 0% | +0 | 0% / 0% | +0 | 25/43 (58%) | 43/88 (49%) | 0% | 29/100 (29%) |
| base_compact | TinyLlama-1.1B | – / – | – | – / – | – | – | – | – | – |
| base_compact | Qwen2.5-3B | – / – | – | – / – | – | – | – | – | – |
| base_compact | gemma-2b | – / – | – | – / – | – | – | – | – | – |
| lora_compact | TinyLlama-1.1B | 100% / 100% | +0 | 100% / 100% | +0 | 1/96 (1%) | 2/97 (2%) | 0% | 4/100 (4%) |
| lora_compact | Qwen2.5-3B | 100% / 62% | +38 | 100% / 100% | +0 | 1/98 (1%) | 0/100 (0%) | 0% | 0/100 (0%) |
| lora_compact | gemma-2b | 100% / 70% | +30 | 100% / 100% | +0 | 0/100 (0%) | 9/100 (9%) | 0% | 1/100 (1%) |
| base_grammar | TinyLlama-1.1B | 100% / 100% | +0 | 100% / 100% | +0 | 83/100 (83%) | 47/98 (48%) | 0% | 40/86 (47%) |
| base_grammar | Qwen2.5-3B | 0% / 0% | +0 | 4% / 2% | +2 | 78/100 (78%) | 48/98 (49%) | 0% | 36/97 (37%) |
| base_grammar | gemma-2b | 100% / 100% | +0 | 95% / 95% | -0 | 75/100 (75%) | 48/98 (49%) | 0% | 21/76 (28%) |
| lora_grammar | TinyLlama-1.1B | 100% / 100% | +0 | 100% / 100% | +0 | 62/100 (62%) | 38/98 (39%) | 0% | 34/89 (38%) |
| lora_grammar | Qwen2.5-3B | 100% / 100% | +0 | 100% / 100% | +0 | 45/100 (45%) | 28/98 (29%) | 0% | 11/99 (11%) |
| lora_grammar | gemma-2b | 24% / 20% | +4 | 0% / 2% | -2 | 74/100 (74%) | 47/99 (47%) | 0% | 16/84 (19%) |
| teacher | training corpus | 100% / 41% | +59 | 100% / 45% | +55 | 26/3000 (1%) | 9/3000 (0%) | 23% | 132/2309 (6%) |

## Agreement

Given the same item, do two settings make the same decision?

Same decision on the same item (95% CI; compared items in brackets).

| TinyLlama-1.1B | base_verbose | lora_verbose | base_verbose2 | lora_verbose2 | base_compact | lora_compact | base_grammar | lora_grammar |
|---|---|---|---|---|---|---|---|---|
| base_verbose | · | – (0) | – (0) | – (0) | – (0) | – (0) | – (0) | – (0) |
| lora_verbose | – (0) | · | – (0) | 62% [58–67] (500) | – (0) | 16% [13–19] (500) | 20% [17–24] (482) | 28% [24–32] (500) |
| base_verbose2 | – (0) | – (0) | · | – (0) | – (0) | – (0) | – (0) | – (0) |
| lora_verbose2 | – (0) | 62% [58–67] (500) | – (0) | · | – (0) | 27% [23–31] (500) | 6% [4–8] (482) | 46% [42–50] (500) |
| base_compact | – (0) | – (0) | – (0) | – (0) | · | – (0) | – (0) | – (0) |
| lora_compact | – (0) | 16% [13–19] (500) | – (0) | 27% [23–31] (500) | – (0) | · | 3% [2–5] (482) | 27% [24–31] (500) |
| base_grammar | – (0) | 20% [17–24] (482) | – (0) | 6% [4–8] (482) | – (0) | 3% [2–5] (482) | · | 17% [14–21] (482) |
| lora_grammar | – (0) | 28% [24–32] (500) | – (0) | 46% [42–50] (500) | – (0) | 27% [24–31] (500) | 17% [14–21] (482) | · |

| Qwen2.5-3B | base_verbose | lora_verbose | base_verbose2 | lora_verbose2 | base_compact | lora_compact | base_grammar | lora_grammar |
|---|---|---|---|---|---|---|---|---|
| base_verbose | · | 55% [50–59] (500) | 30% [27–35] (492) | 40% [36–44] (500) | – (0) | 28% [24–32] (500) | 33% [29–37] (500) | 35% [31–39] (500) |
| lora_verbose | 55% [50–59] (500) | · | 12% [9–15] (492) | 51% [46–55] (500) | – (0) | 30% [26–34] (500) | 16% [13–19] (500) | 56% [51–60] (500) |
| base_verbose2 | 30% [27–35] (492) | 12% [9–15] (492) | · | 16% [13–20] (492) | – (0) | 3% [2–5] (492) | 41% [36–45] (492) | 11% [9–14] (492) |
| lora_verbose2 | 40% [36–44] (500) | 51% [46–55] (500) | 16% [13–20] (492) | · | – (0) | 32% [28–36] (500) | 16% [13–20] (500) | 55% [51–59] (500) |
| base_compact | – (0) | – (0) | – (0) | – (0) | · | – (0) | – (0) | – (0) |
| lora_compact | 28% [24–32] (500) | 30% [26–34] (500) | 3% [2–5] (492) | 32% [28–36] (500) | – (0) | · | 6% [4–8] (500) | 32% [28–36] (500) |
| base_grammar | 33% [29–37] (500) | 16% [13–19] (500) | 41% [36–45] (492) | 16% [13–20] (500) | – (0) | 6% [4–8] (500) | · | 21% [18–25] (500) |
| lora_grammar | 35% [31–39] (500) | 56% [51–60] (500) | 11% [9–14] (492) | 55% [51–59] (500) | – (0) | 32% [28–36] (500) | 21% [18–25] (500) | · |

| gemma-2b | base_verbose | lora_verbose | base_verbose2 | lora_verbose2 | base_compact | lora_compact | base_grammar | lora_grammar |
|---|---|---|---|---|---|---|---|---|
| base_verbose | · | 28% [24–32] (497) | 24% [20–28] (497) | 7% [5–10] (497) | – (0) | 7% [5–10] (497) | 28% [24–32] (497) | 4% [2–6] (497) |
| lora_verbose | 28% [24–32] (497) | · | 41% [37–45] (500) | 18% [15–21] (500) | – (0) | 25% [21–29] (500) | 15% [12–18] (500) | 19% [16–22] (500) |
| base_verbose2 | 24% [20–28] (497) | 41% [37–45] (500) | · | 19% [16–23] (500) | – (0) | 21% [18–25] (500) | 16% [13–20] (500) | 13% [10–16] (500) |
| lora_verbose2 | 7% [5–10] (497) | 18% [15–21] (500) | 19% [16–23] (500) | · | – (0) | 7% [5–9] (500) | 23% [20–27] (500) | 56% [52–60] (500) |
| base_compact | – (0) | – (0) | – (0) | – (0) | · | – (0) | – (0) | – (0) |
| lora_compact | 7% [5–10] (497) | 25% [21–29] (500) | 21% [18–25] (500) | 7% [5–9] (500) | – (0) | · | 5% [4–8] (500) | 9% [6–11] (500) |
| base_grammar | 28% [24–32] (497) | 15% [12–18] (500) | 16% [13–20] (500) | 23% [20–27] (500) | – (0) | 5% [4–8] (500) | · | 29% [26–34] (500) |
| lora_grammar | 4% [2–6] (497) | 19% [16–22] (500) | 13% [10–16] (500) | 56% [52–60] (500) | – (0) | 9% [6–11] (500) | 29% [26–34] (500) | · |

# replay_20261006_2x4: held-out training states

replay run, backend gpu; 492 answers per model and condition; training corpus `training/corpus/training_data_synct_15000_llm.txt`; evaluated 2026-11-12 13:12. Shares in brackets are 95% Wilson intervals.

## Overview

| condition | model | answers | schema-valid | legal | reference-correct | accept gap useful−useless | avoidable harvests |
|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 492 | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| base_verbose | Qwen2.5-3B | 492 | 98% [96–99] | 87% [83–89] | 39% [35–43] | -19 | 43% |
| base_verbose | gemma-2b | 492 | 99% [98–100] | 70% [66–74] | 29% [25–33] | +0 | 51% |
| lora_verbose | TinyLlama-1.1B | 492 | 79% [76–83] | 91% [89–94] | 47% [42–51] | +0 | 37% |
| lora_verbose | Qwen2.5-3B | 492 | 100% [99–100] | 86% [82–88] | 43% [39–48] | +0 | 33% |
| lora_verbose | gemma-2b | 492 | 100% [99–100] | 94% [92–96] | 42% [38–47] | +0 | 47% |
| base_verbose2 | TinyLlama-1.1B | 492 | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| base_verbose2 | Qwen2.5-3B | 492 | 98% [96–99] | 89% [86–91] | 42% [37–46] | +0 | 59% |
| base_verbose2 | gemma-2b | 492 | 86% [82–89] | 63% [59–68] | 28% [24–32] | -2 | 40% |
| lora_verbose2 | TinyLlama-1.1B | 492 | 78% [74–81] | 88% [85–91] | 47% [43–52] | +0 | 35% |
| lora_verbose2 | Qwen2.5-3B | 492 | 93% [90–95] | 94% [92–96] | 41% [37–46] | +0 | 36% |
| lora_verbose2 | gemma-2b | 492 | 98% [96–99] | 84% [80–87] | 45% [41–49] | +0 | 43% |
| base_compact | TinyLlama-1.1B | 492 | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| base_compact | Qwen2.5-3B | 492 | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| base_compact | gemma-2b | 492 | 0% [0–1] | 0% [0–1] | 0% [0–1] | – | – |
| lora_compact | TinyLlama-1.1B | 492 | 100% [99–100] | 98% [96–99] | 65% [61–69] | +0 | 2% |
| lora_compact | Qwen2.5-3B | 492 | 100% [99–100] | 99% [97–99] | 73% [69–77] | +18 | 1% |
| lora_compact | gemma-2b | 492 | 100% [99–100] | 99% [97–99] | 72% [68–76] | +14 | 1% |
| base_grammar | TinyLlama-1.1B | 492 | 96% [93–97] | 77% [73–81] | 24% [20–28] | +0 | 64% |
| base_grammar | Qwen2.5-3B | 492 | 99% [98–100] | 97% [95–98] | 45% [40–49] | -1 | 57% |
| base_grammar | gemma-2b | 492 | 100% [99–100] | 77% [73–81] | 25% [22–29] | +4 | 61% |
| lora_grammar | TinyLlama-1.1B | 492 | 99% [97–99] | 92% [89–94] | 38% [34–42] | +1 | 48% |
| lora_grammar | Qwen2.5-3B | 492 | 100% [99–100] | 98% [96–99] | 49% [44–53] | +0 | 40% |
| lora_grammar | gemma-2b | 492 | 93% [91–95] | 90% [87–93] | 45% [40–49] | +10 | 58% |

## Effects

How much do the adapter and the prompt style change an outcome, item by item?

Rows marked * stay significant after the Holm correction.

### schema-valid

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| TinyLlama-1.1B | adapter at verbose | 492 | 0% | 79% | +79 [+76, +83] | 0 / 391 | <0.001 | <0.001 * |
| TinyLlama-1.1B | adapter at verbose2 | 492 | 0% | 78% | +78 [+74, +81] | 0 / 382 | <0.001 | <0.001 * |
| TinyLlama-1.1B | adapter at compact | 492 | 0% | 100% | +100 [+100, +100] | 0 / 492 | <0.001 | <0.001 * |
| TinyLlama-1.1B | adapter at grammar | 492 | 96% | 99% | +3 [+1, +5] | 4 / 20 | 0.002 | 0.022 * |
| TinyLlama-1.1B | base: verbose2 vs verbose | 492 | 0% | 0% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| TinyLlama-1.1B | base: compact vs verbose | 492 | 0% | 0% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| TinyLlama-1.1B | base: grammar vs verbose | 492 | 0% | 96% | +96 [+93, +97] | 0 / 470 | <0.001 | <0.001 * |
| TinyLlama-1.1B | lora: verbose2 vs verbose | 492 | 79% | 78% | -2 [-3, -1] | 11 / 2 | 0.022 | 0.247 |
| TinyLlama-1.1B | lora: compact vs verbose | 492 | 79% | 100% | +21 [+17, +24] | 0 / 101 | <0.001 | <0.001 * |
| TinyLlama-1.1B | lora: grammar vs verbose | 492 | 79% | 99% | +19 [+16, +23] | 3 / 98 | <0.001 | <0.001 * |
| Qwen2.5-3B | adapter at verbose | 492 | 98% | 100% | +2 [+1, +4] | 1 / 12 | 0.003 | 0.044 * |
| Qwen2.5-3B | adapter at verbose2 | 492 | 98% | 93% | -5 [-8, -2] | 35 / 11 | <0.001 | 0.008 * |
| Qwen2.5-3B | adapter at compact | 492 | 0% | 100% | +100 [+99, +100] | 0 / 491 | <0.001 | <0.001 * |
| Qwen2.5-3B | adapter at grammar | 492 | 99% | 100% | +1 [+0, +2] | 0 / 4 | 0.125 | 1.000 |
| Qwen2.5-3B | base: verbose2 vs verbose | 492 | 98% | 98% | +0 [-2, +2] | 9 / 10 | 1.000 | 1.000 |
| Qwen2.5-3B | base: compact vs verbose | 492 | 98% | 0% | -98 [-99, -96] | 480 / 0 | <0.001 | <0.001 * |
| Qwen2.5-3B | base: grammar vs verbose | 492 | 98% | 99% | +2 [+0, +3] | 4 / 12 | 0.077 | 0.691 |
| Qwen2.5-3B | lora: verbose2 vs verbose | 492 | 100% | 93% | -7 [-9, -5] | 35 / 1 | <0.001 | <0.001 * |
| Qwen2.5-3B | lora: compact vs verbose | 492 | 100% | 100% | +0 [-1, +1] | 1 / 1 | 1.000 | 1.000 |
| Qwen2.5-3B | lora: grammar vs verbose | 492 | 100% | 100% | +0 [+0, +1] | 0 / 1 | 1.000 | 1.000 |
| gemma-2b | adapter at verbose | 492 | 99% | 100% | +1 [-0, +2] | 1 / 4 | 0.375 | 1.000 |
| gemma-2b | adapter at verbose2 | 492 | 86% | 98% | +12 [+9, +15] | 5 / 63 | <0.001 | <0.001 * |
| gemma-2b | adapter at compact | 492 | 0% | 100% | +100 [+100, +100] | 0 / 492 | <0.001 | <0.001 * |
| gemma-2b | adapter at grammar | 492 | 100% | 93% | -7 [-9, -4] | 32 / 0 | <0.001 | <0.001 * |
| gemma-2b | base: verbose2 vs verbose | 492 | 99% | 86% | -13 [-16, -10] | 68 / 3 | <0.001 | <0.001 * |
| gemma-2b | base: compact vs verbose | 492 | 99% | 0% | -99 [-100, -98] | 487 / 0 | <0.001 | <0.001 * |
| gemma-2b | base: grammar vs verbose | 492 | 99% | 100% | +1 [+0, +2] | 0 / 5 | 0.062 | 0.625 |
| gemma-2b | lora: verbose2 vs verbose | 492 | 100% | 98% | -2 [-4, -1] | 12 / 2 | 0.013 | 0.155 |
| gemma-2b | lora: compact vs verbose | 492 | 100% | 100% | +0 [+0, +1] | 0 / 2 | 0.500 | 1.000 |
| gemma-2b | lora: grammar vs verbose | 492 | 100% | 93% | -6 [-9, -4] | 32 / 2 | <0.001 | <0.001 * |

### legal

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| TinyLlama-1.1B | adapter at verbose | 492 | 0% | 91% | +91 [+89, +94] | 0 / 450 | <0.001 | <0.001 * |
| TinyLlama-1.1B | adapter at verbose2 | 492 | 0% | 88% | +88 [+85, +91] | 0 / 433 | <0.001 | <0.001 * |
| TinyLlama-1.1B | adapter at compact | 492 | 0% | 98% | +98 [+96, +99] | 0 / 480 | <0.001 | <0.001 * |
| TinyLlama-1.1B | adapter at grammar | 492 | 77% | 92% | +15 [+11, +19] | 19 / 91 | <0.001 | <0.001 * |
| TinyLlama-1.1B | base: verbose2 vs verbose | 492 | 0% | 0% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| TinyLlama-1.1B | base: compact vs verbose | 492 | 0% | 0% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| TinyLlama-1.1B | base: grammar vs verbose | 492 | 0% | 77% | +77 [+73, +81] | 0 / 380 | <0.001 | <0.001 * |
| TinyLlama-1.1B | lora: verbose2 vs verbose | 492 | 91% | 88% | -3 [-7, +0] | 46 / 29 | 0.064 | 0.448 |
| TinyLlama-1.1B | lora: compact vs verbose | 492 | 91% | 98% | +6 [+4, +9] | 6 / 36 | <0.001 | <0.001 * |
| TinyLlama-1.1B | lora: grammar vs verbose | 492 | 91% | 92% | +0 [-3, +3] | 29 / 31 | 0.897 | 1.000 |
| Qwen2.5-3B | adapter at verbose | 492 | 87% | 86% | -1 [-4, +2] | 44 / 39 | 0.661 | 1.000 |
| Qwen2.5-3B | adapter at verbose2 | 492 | 89% | 94% | +5 [+2, +8] | 17 / 42 | 0.002 | 0.017 * |
| Qwen2.5-3B | adapter at compact | 492 | 0% | 99% | +98 [+97, +99] | 0 / 484 | <0.001 | <0.001 * |
| Qwen2.5-3B | adapter at grammar | 492 | 97% | 98% | +1 [-0, +3] | 4 / 10 | 0.180 | 1.000 |
| Qwen2.5-3B | base: verbose2 vs verbose | 492 | 87% | 89% | +2 [-1, +6] | 36 / 48 | 0.230 | 1.000 |
| Qwen2.5-3B | base: compact vs verbose | 492 | 87% | 0% | -86 [-89, -83] | 425 / 0 | <0.001 | <0.001 * |
| Qwen2.5-3B | base: grammar vs verbose | 492 | 87% | 97% | +10 [+7, +13] | 9 / 59 | <0.001 | <0.001 * |
| Qwen2.5-3B | lora: verbose2 vs verbose | 492 | 86% | 94% | +9 [+6, +12] | 14 / 56 | <0.001 | <0.001 * |
| Qwen2.5-3B | lora: compact vs verbose | 492 | 86% | 99% | +13 [+10, +16] | 4 / 68 | <0.001 | <0.001 * |
| Qwen2.5-3B | lora: grammar vs verbose | 492 | 86% | 98% | +12 [+9, +15] | 4 / 65 | <0.001 | <0.001 * |
| gemma-2b | adapter at verbose | 492 | 70% | 94% | +24 [+20, +28] | 7 / 124 | <0.001 | <0.001 * |
| gemma-2b | adapter at verbose2 | 492 | 63% | 84% | +20 [+16, +24] | 6 / 106 | <0.001 | <0.001 * |
| gemma-2b | adapter at compact | 492 | 0% | 99% | +99 [+98, +100] | 0 / 486 | <0.001 | <0.001 * |
| gemma-2b | adapter at grammar | 492 | 77% | 90% | +13 [+9, +17] | 25 / 90 | <0.001 | <0.001 * |
| gemma-2b | base: verbose2 vs verbose | 492 | 70% | 63% | -7 [-11, -3] | 76 / 42 | 0.002 | 0.022 * |
| gemma-2b | base: compact vs verbose | 492 | 70% | 0% | -70 [-74, -66] | 346 / 0 | <0.001 | <0.001 * |
| gemma-2b | base: grammar vs verbose | 492 | 70% | 77% | +7 [+2, +12] | 63 / 96 | 0.011 | 0.098 |
| gemma-2b | lora: verbose2 vs verbose | 492 | 94% | 84% | -10 [-14, -7] | 66 / 15 | <0.001 | <0.001 * |
| gemma-2b | lora: compact vs verbose | 492 | 94% | 99% | +5 [+3, +7] | 4 / 27 | <0.001 | <0.001 * |
| gemma-2b | lora: grammar vs verbose | 492 | 94% | 90% | -4 [-7, -1] | 43 / 24 | 0.027 | 0.217 |

### reference-correct

| model | effect | items | A | B | B − A in points [95% CI] | only A / only B | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|---|
| TinyLlama-1.1B | adapter at verbose | 492 | 0% | 47% | +47 [+42, +51] | 0 / 229 | <0.001 | <0.001 * |
| TinyLlama-1.1B | adapter at verbose2 | 492 | 0% | 47% | +47 [+43, +51] | 0 / 232 | <0.001 | <0.001 * |
| TinyLlama-1.1B | adapter at compact | 492 | 0% | 65% | +65 [+61, +70] | 0 / 321 | <0.001 | <0.001 * |
| TinyLlama-1.1B | adapter at grammar | 492 | 24% | 38% | +14 [+10, +18] | 27 / 96 | <0.001 | <0.001 * |
| TinyLlama-1.1B | base: verbose2 vs verbose | 492 | 0% | 0% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| TinyLlama-1.1B | base: compact vs verbose | 492 | 0% | 0% | +0 [+0, +0] | 0 / 0 | 1.000 | 1.000 |
| TinyLlama-1.1B | base: grammar vs verbose | 492 | 0% | 24% | +24 [+20, +27] | 0 / 117 | <0.001 | <0.001 * |
| TinyLlama-1.1B | lora: verbose2 vs verbose | 492 | 47% | 47% | +1 [-1, +3] | 12 / 15 | 0.701 | 1.000 |
| TinyLlama-1.1B | lora: compact vs verbose | 492 | 47% | 65% | +19 [+15, +23] | 12 / 104 | <0.001 | <0.001 * |
| TinyLlama-1.1B | lora: grammar vs verbose | 492 | 47% | 38% | -9 [-13, -5] | 71 / 28 | <0.001 | <0.001 * |
| Qwen2.5-3B | adapter at verbose | 492 | 39% | 43% | +4 [+1, +9] | 42 / 64 | 0.041 | 0.490 |
| Qwen2.5-3B | adapter at verbose2 | 492 | 42% | 41% | -0 [-6, +6] | 117 / 115 | 0.948 | 1.000 |
| Qwen2.5-3B | adapter at compact | 492 | 0% | 73% | +73 [+69, +77] | 0 / 357 | <0.001 | <0.001 * |
| Qwen2.5-3B | adapter at grammar | 492 | 45% | 49% | +4 [-2, +11] | 120 / 140 | 0.239 | 1.000 |
| Qwen2.5-3B | base: verbose2 vs verbose | 492 | 39% | 42% | +3 [-3, +8] | 80 / 93 | 0.362 | 1.000 |
| Qwen2.5-3B | base: compact vs verbose | 492 | 39% | 0% | -39 [-43, -35] | 191 / 0 | <0.001 | <0.001 * |
| Qwen2.5-3B | base: grammar vs verbose | 492 | 39% | 45% | +6 [+0, +11] | 68 / 96 | 0.035 | 0.451 |
| Qwen2.5-3B | lora: verbose2 vs verbose | 492 | 43% | 41% | -2 [-5, +1] | 31 / 20 | 0.161 | 1.000 |
| Qwen2.5-3B | lora: compact vs verbose | 492 | 43% | 73% | +29 [+25, +34] | 8 / 152 | <0.001 | <0.001 * |
| Qwen2.5-3B | lora: grammar vs verbose | 492 | 43% | 49% | +5 [+2, +8] | 15 / 41 | <0.001 | 0.010 * |
| gemma-2b | adapter at verbose | 492 | 29% | 42% | +13 [+10, +17] | 1 / 67 | <0.001 | <0.001 * |
| gemma-2b | adapter at verbose2 | 492 | 28% | 45% | +17 [+12, +22] | 50 / 135 | <0.001 | <0.001 * |
| gemma-2b | adapter at compact | 492 | 0% | 72% | +72 [+68, +76] | 0 / 355 | <0.001 | <0.001 * |
| gemma-2b | adapter at grammar | 492 | 25% | 45% | +19 [+13, +24] | 59 / 153 | <0.001 | <0.001 * |
| gemma-2b | base: verbose2 vs verbose | 492 | 29% | 28% | -1 [-4, +2] | 28 / 22 | 0.480 | 1.000 |
| gemma-2b | base: compact vs verbose | 492 | 29% | 0% | -29 [-33, -25] | 142 / 0 | <0.001 | <0.001 * |
| gemma-2b | base: grammar vs verbose | 492 | 29% | 25% | -3 [-7, +0] | 56 / 39 | 0.100 | 1.000 |
| gemma-2b | lora: verbose2 vs verbose | 492 | 42% | 45% | +3 [-4, +9] | 111 / 124 | 0.434 | 1.000 |
| gemma-2b | lora: compact vs verbose | 492 | 42% | 72% | +30 [+26, +34] | 3 / 150 | <0.001 | <0.001 * |
| gemma-2b | lora: grammar vs verbose | 492 | 42% | 45% | +2 [-4, +8] | 113 / 124 | 0.516 | 1.000 |

## Schema validity (valid@1)

Is the whole answer one JSON value that matches its message type's schema, game/schemas/output/<phase>.schema.json?

| condition | model | valid | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | main failures |
|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 0/492 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 492 |
| base_verbose | Qwen2.5-3B | 480/492 (98%) | 88% | 100% | 100% | 100% | 100% | schema:maxItems 12 |
| base_verbose | gemma-2b | 487/492 (99%) | 95% | 100% | 100% | 100% | 100% | schema:maxItems 5 |
| lora_verbose | TinyLlama-1.1B | 391/492 (79%) | 100% | 100% | 1% | 98% | 100% | schema:additionalProperties 99, not_json 2 |
| lora_verbose | Qwen2.5-3B | 491/492 (100%) | 99% | 100% | 100% | 100% | 100% | schema:maxItems 1 |
| lora_verbose | gemma-2b | 490/492 (100%) | 98% | 100% | 100% | 100% | 100% | schema:maxItems 2 |
| base_verbose2 | TinyLlama-1.1B | 0/492 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 492 |
| base_verbose2 | Qwen2.5-3B | 481/492 (98%) | 93% | 100% | 100% | 100% | 96% | schema:maxItems 7, schema:enum 4 |
| base_verbose2 | gemma-2b | 422/492 (86%) | 64% | 66% | 100% | 100% | 100% | schema:maxItems 34, wrapped 33, schema:enum 2 |
| lora_verbose2 | TinyLlama-1.1B | 382/492 (78%) | 90% | 100% | 0% | 100% | 100% | schema:additionalProperties 110 |
| lora_verbose2 | Qwen2.5-3B | 457/492 (93%) | 100% | 65% | 100% | 100% | 100% | wrapped 35 |
| lora_verbose2 | gemma-2b | 480/492 (98%) | 88% | 100% | 100% | 100% | 100% | schema:maxItems 12 |
| base_compact | TinyLlama-1.1B | 0/492 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 492 |
| base_compact | Qwen2.5-3B | 0/492 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 491, wrapped 1 |
| base_compact | gemma-2b | 0/492 (0%) | 0% | 0% | 0% | 0% | 0% | not_json 492 |
| lora_compact | TinyLlama-1.1B | 492/492 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_compact | Qwen2.5-3B | 491/492 (100%) | 100% | 100% | 99% | 100% | 100% | not_json 1 |
| lora_compact | gemma-2b | 492/492 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| base_grammar | TinyLlama-1.1B | 470/492 (96%) | 100% | 100% | 97% | 82% | 99% | not_json 22 |
| base_grammar | Qwen2.5-3B | 488/492 (99%) | 100% | 98% | 98% | 100% | 100% | not_json 4 |
| base_grammar | gemma-2b | 492/492 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_grammar | TinyLlama-1.1B | 486/492 (99%) | 100% | 100% | 98% | 97% | 99% | not_json 4, schema:minItems 2 |
| lora_grammar | Qwen2.5-3B | 492/492 (100%) | 100% | 100% | 100% | 100% | 100% | – |
| lora_grammar | gemma-2b | 460/492 (93%) | 100% | 100% | 68% | 100% | 100% | schema:minItems 32 |

## Legality

Would the game carry out the answer as the model wrote it?

| condition | model | legal | valid & legal | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | why not legal |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 0/492 (0%) | 0% | 0% | 0% | 0% | 0% | 0% | no_json 492 |
| base_verbose | Qwen2.5-3B | 426/492 (87%) | 87% | 83% | 51% | 100% | 100% | 100% | rules 66 |
| base_verbose | gemma-2b | 346/492 (70%) | 70% | 63% | 38% | 100% | 61% | 91% | rules 99, cards_not_held 47 |
| lora_verbose | TinyLlama-1.1B | 450/492 (91%) | 71% | 98% | 77% | 100% | 84% | 99% | rules 25, cards_not_held 15, no_json 2 |
| lora_verbose | Qwen2.5-3B | 421/492 (86%) | 86% | 56% | 73% | 100% | 100% | 100% | rules 71 |
| lora_verbose | gemma-2b | 463/492 (94%) | 94% | 87% | 84% | 100% | 100% | 100% | rules 29 |
| base_verbose2 | TinyLlama-1.1B | 0/492 (0%) | 0% | 0% | 0% | 0% | 0% | 0% | no_json 492 |
| base_verbose2 | Qwen2.5-3B | 438/492 (89%) | 89% | 72% | 80% | 100% | 98% | 96% | rules 48, parser 4, cards_not_held 2 |
| base_verbose2 | gemma-2b | 312/492 (63%) | 57% | 15% | 57% | 99% | 50% | 99% | rules 125, cards_not_held 52, parser 3 |
| lora_verbose2 | TinyLlama-1.1B | 433/492 (88%) | 68% | 71% | 70% | 100% | 100% | 100% | rules 59 |
| lora_verbose2 | Qwen2.5-3B | 463/492 (94%) | 87% | 74% | 97% | 100% | 100% | 100% | rules 29 |
| lora_verbose2 | gemma-2b | 412/492 (84%) | 84% | 31% | 89% | 100% | 100% | 100% | rules 80 |
| base_compact | TinyLlama-1.1B | 0/492 (0%) | 0% | 0% | 0% | 0% | 0% | 0% | no_json 492 |
| base_compact | Qwen2.5-3B | 1/492 (0%) | 0% | 0% | 0% | 1% | 0% | 0% | no_json 491 |
| base_compact | gemma-2b | 0/492 (0%) | 0% | 0% | 0% | 0% | 0% | 0% | no_json 492 |
| lora_compact | TinyLlama-1.1B | 480/492 (98%) | 98% | 98% | 91% | 99% | 100% | 100% | rules 11, cards_not_held 1 |
| lora_compact | Qwen2.5-3B | 485/492 (99%) | 99% | 100% | 96% | 97% | 100% | 100% | rules 4, cards_not_held 2, no_json 1 |
| lora_compact | gemma-2b | 486/492 (99%) | 99% | 100% | 94% | 100% | 100% | 100% | rules 6 |
| base_grammar | TinyLlama-1.1B | 380/492 (77%) | 77% | 100% | 84% | 81% | 32% | 90% | cards_not_held 74, no_json 22, rules 16 |
| base_grammar | Qwen2.5-3B | 476/492 (97%) | 97% | 100% | 88% | 98% | 98% | 100% | rules 10, no_json 4, cards_not_held 2 |
| base_grammar | gemma-2b | 379/492 (77%) | 77% | 100% | 84% | 64% | 59% | 78% | cards_not_held 97, rules 16 |
| lora_grammar | TinyLlama-1.1B | 452/492 (92%) | 92% | 100% | 85% | 79% | 97% | 99% | cards_not_held 19, rules 15, no_json 4, no_cards 2 |
| lora_grammar | Qwen2.5-3B | 482/492 (98%) | 98% | 100% | 91% | 99% | 100% | 100% | rules 9, cards_not_held 1 |
| lora_grammar | gemma-2b | 444/492 (90%) | 90% | 100% | 85% | 67% | 100% | 100% | no_cards 32, rules 15, cards_not_held 1 |

## Reference decisions

Does the answer make the decision a simple, value-aware rule set makes?

| condition | model | correct (95% CI) | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | teacher match |
|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 0% [0–1] | 0% | 0% | 0% | 0% | 0% | 0% [0–1] |
| base_verbose | Qwen2.5-3B | 39% [35–43] | 22% | 18% | 79% | 46% | 29% | 27% [23–31] |
| base_verbose | gemma-2b | 29% [25–33] | 14% | 9% | 77% | 17% | 27% | 7% [5–9] |
| lora_verbose | TinyLlama-1.1B | 47% [42–51] | 32% | 24% | 100% | 46% | 29% | 29% [25–33] |
| lora_verbose | Qwen2.5-3B | 43% [39–48] | 23% | 35% | 79% | 50% | 29% | 27% [24–32] |
| lora_verbose | gemma-2b | 42% [38–47] | 19% | 31% | 81% | 50% | 29% | 27% [23–31] |
| base_verbose2 | TinyLlama-1.1B | 0% [0–1] | 0% | 0% | 0% | 0% | 0% | 0% [0–1] |
| base_verbose2 | Qwen2.5-3B | 42% [37–46] | 7% | 23% | 67% | 45% | 68% | 17% [14–20] |
| base_verbose2 | gemma-2b | 28% [24–32] | 3% | 20% | 78% | 8% | 29% | 17% [14–21] |
| lora_verbose2 | TinyLlama-1.1B | 47% [43–52] | 24% | 31% | 100% | 50% | 29% | 33% [29–37] |
| lora_verbose2 | Qwen2.5-3B | 41% [37–46] | 25% | 33% | 68% | 50% | 29% | 29% [25–33] |
| lora_verbose2 | gemma-2b | 45% [41–49] | 4% | 28% | 74% | 50% | 71% | 17% [14–20] |
| base_compact | TinyLlama-1.1B | 0% [0–1] | 0% | 0% | 0% | 0% | 0% | 0% [0–1] |
| base_compact | Qwen2.5-3B | 0% [0–1] | 0% | 0% | 1% | 0% | 0% | 0% [0–1] |
| base_compact | gemma-2b | 0% [0–1] | 0% | 0% | 0% | 0% | 0% | 0% [0–1] |
| lora_compact | TinyLlama-1.1B | 65% [61–69] | 76% | 77% | 94% | 47% | 29% | 45% [40–49] |
| lora_compact | Qwen2.5-3B | 73% [69–77] | 77% | 88% | 97% | 69% | 29% | 48% [43–52] |
| lora_compact | gemma-2b | 72% [68–76] | 78% | 87% | 98% | 65% | 29% | 48% [44–53] |
| base_grammar | TinyLlama-1.1B | 24% [20–28] | 12% | 28% | 52% | 0% | 27% | 6% [4–9] |
| base_grammar | Qwen2.5-3B | 45% [40–49] | 13% | 27% | 67% | 49% | 70% | 13% [10–16] |
| base_grammar | gemma-2b | 25% [22–29] | 12% | 26% | 43% | 20% | 26% | 7% [5–9] |
| lora_grammar | TinyLlama-1.1B | 38% [34–42] | 26% | 33% | 53% | 47% | 29% | 26% [23–30] |
| lora_grammar | Qwen2.5-3B | 49% [44–53] | 36% | 40% | 87% | 50% | 29% | 30% [26–34] |
| lora_grammar | gemma-2b | 45% [40–49] | 11% | 33% | 57% | 53% | 71% | 21% [17–25] |
| teacher | training corpus | 83% [83–84] | 88% | 99% | 97% | 70% | 62% | – |

Each rule on its own (partial credit):

| condition | model | PLANT: first card placed | PLANT: second card without harvest | FORCE: no avoidable harvest | FORCE: least valuable stack lost | TRADI: keeps growing beans | REPLY: accepts iff useful | REPLY: keeps growing beans | CONSI: accepts iff useful |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| base_verbose | Qwen2.5-3B | 26% | 70% | 39% | 30% | 79% | 46% | 100% | 29% |
| base_verbose | gemma-2b | 15% | 60% | 23% | 24% | 77% | 30% | 45% | 27% |
| lora_verbose | TinyLlama-1.1B | 32% | 98% | 54% | 47% | 100% | 46% | 84% | 29% |
| lora_verbose | Qwen2.5-3B | 30% | 38% | 56% | 52% | 79% | 50% | 100% | 29% |
| lora_verbose | gemma-2b | 26% | 62% | 60% | 55% | 81% | 50% | 100% | 29% |
| base_verbose2 | TinyLlama-1.1B | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| base_verbose2 | Qwen2.5-3B | 18% | 18% | 51% | 52% | 67% | 48% | 93% | 68% |
| base_verbose2 | gemma-2b | 3% | 13% | 39% | 38% | 78% | 26% | 30% | 29% |
| lora_verbose2 | TinyLlama-1.1B | 24% | 69% | 52% | 49% | 100% | 50% | 100% | 29% |
| lora_verbose2 | Qwen2.5-3B | 26% | 66% | 72% | 58% | 68% | 50% | 100% | 29% |
| lora_verbose2 | gemma-2b | 6% | 17% | 62% | 55% | 74% | 50% | 100% | 71% |
| base_compact | TinyLlama-1.1B | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| base_compact | Qwen2.5-3B | 0% | 0% | 0% | 0% | 1% | 0% | 0% | 0% |
| base_compact | gemma-2b | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| lora_compact | TinyLlama-1.1B | 76% | 98% | 88% | 80% | 94% | 50% | 96% | 29% |
| lora_compact | Qwen2.5-3B | 78% | 99% | 95% | 89% | 97% | 71% | 98% | 29% |
| lora_compact | gemma-2b | 78% | 100% | 93% | 88% | 98% | 66% | 99% | 29% |
| base_grammar | TinyLlama-1.1B | 39% | 28% | 52% | 60% | 52% | 16% | 16% | 27% |
| base_grammar | Qwen2.5-3B | 35% | 39% | 59% | 56% | 67% | 49% | 98% | 70% |
| base_grammar | gemma-2b | 38% | 32% | 55% | 55% | 43% | 31% | 39% | 26% |
| lora_grammar | TinyLlama-1.1B | 55% | 51% | 61% | 57% | 53% | 47% | 97% | 29% |
| lora_grammar | Qwen2.5-3B | 46% | 74% | 69% | 62% | 87% | 50% | 100% | 29% |
| lora_grammar | gemma-2b | 36% | 38% | 60% | 58% | 57% | 53% | 100% | 71% |
| teacher | training corpus | 89% | 99% | 100% | 100% | 97% | 75% | 95% | 62% |

Teacher match per message type (the decision equals the teacher's held-out answer):

| condition | model | teacher match (95% CI) | PLANTING | FORCED | TRADING | REPLY | CONSIDERING |
|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | 0% [0–1] | 0% | 0% | 0% | 0% | 0% |
| base_verbose | Qwen2.5-3B | 27% [23–31] | 29% | 15% | 7% | 24% | 61% |
| base_verbose | gemma-2b | 7% [5–9] | 21% | 4% | 7% | 1% | 0% |
| lora_verbose | TinyLlama-1.1B | 29% [25–33] | 43% | 22% | 26% | 25% | 29% |
| lora_verbose | Qwen2.5-3B | 27% [24–32] | 16% | 30% | 5% | 28% | 61% |
| lora_verbose | gemma-2b | 27% [23–31] | 25% | 20% | 7% | 28% | 59% |
| base_verbose2 | TinyLlama-1.1B | 0% [0–1] | 0% | 0% | 0% | 0% | 0% |
| base_verbose2 | Qwen2.5-3B | 17% [14–20] | 10% | 20% | 10% | 18% | 27% |
| base_verbose2 | gemma-2b | 17% [14–21] | 2% | 17% | 7% | 2% | 61% |
| lora_verbose2 | TinyLlama-1.1B | 33% [29–37] | 29% | 22% | 26% | 28% | 61% |
| lora_verbose2 | Qwen2.5-3B | 29% [25–33] | 27% | 28% | 5% | 28% | 61% |
| lora_verbose2 | gemma-2b | 17% [14–20] | 5% | 23% | 7% | 21% | 29% |
| base_compact | TinyLlama-1.1B | 0% [0–1] | 0% | 0% | 0% | 0% | 0% |
| base_compact | Qwen2.5-3B | 0% [0–1] | 0% | 0% | 0% | 0% | 0% |
| base_compact | gemma-2b | 0% [0–1] | 0% | 0% | 0% | 0% | 0% |
| lora_compact | TinyLlama-1.1B | 45% [40–49] | 73% | 70% | 6% | 15% | 61% |
| lora_compact | Qwen2.5-3B | 48% [43–52] | 77% | 79% | 10% | 13% | 61% |
| lora_compact | gemma-2b | 48% [44–53] | 75% | 81% | 10% | 15% | 61% |
| base_grammar | TinyLlama-1.1B | 6% [4–9] | 7% | 21% | 3% | 0% | 0% |
| base_grammar | Qwen2.5-3B | 13% [10–16] | 13% | 21% | 5% | 21% | 3% |
| base_grammar | gemma-2b | 7% [5–9] | 8% | 22% | 1% | 2% | 0% |
| lora_grammar | TinyLlama-1.1B | 26% [23–30] | 20% | 28% | 0% | 26% | 61% |
| lora_grammar | Qwen2.5-3B | 30% [26–34] | 29% | 30% | 5% | 28% | 61% |
| lora_grammar | gemma-2b | 21% [17–25] | 13% | 28% | 6% | 28% | 29% |

## State sensitivity

Does the decision depend on the game state?

| condition | model | REPLY accepts useful / useless | gap | CONSIDERING accepts useful / useless | gap | PLANTING avoidable harvests | FORCED avoidable harvests | TRADING passes | offers giving away a growing bean |
|---|---|---|---|---|---|---|---|---|---|
| base_verbose | TinyLlama-1.1B | – / – | – | – / – | – | – | – | – | – |
| base_verbose | Qwen2.5-3B | 26% / 34% | -8 | 100% / 100% | +0 | 46/83 (55%) | 12/51 (24%) | 0% | 24/100 (24%) |
| base_verbose | gemma-2b | 100% / 100% | +0 | 100% / 100% | +0 | 37/63 (59%) | 15/38 (39%) | 0% | 26/100 (26%) |
| lora_verbose | TinyLlama-1.1B | 100% / 100% | +0 | 100% / 100% | +0 | 42/98 (43%) | 23/77 (30%) | 99% | 0/1 (0%) |
| lora_verbose | Qwen2.5-3B | 100% / 100% | +0 | 100% / 100% | +0 | 25/56 (45%) | 17/73 (23%) | 0% | 24/100 (24%) |
| lora_verbose | gemma-2b | 100% / 100% | +0 | 100% / 100% | +0 | 56/87 (64%) | 24/84 (29%) | 0% | 22/100 (22%) |
| base_verbose2 | TinyLlama-1.1B | – / – | – | – / – | – | – | – | – | – |
| base_verbose2 | Qwen2.5-3B | 0% / 0% | +0 | 0% / 0% | +0 | 61/72 (85%) | 29/80 (36%) | 0% | 36/100 (36%) |
| base_verbose2 | gemma-2b | 96% / 100% | -4 | 100% / 100% | +0 | 11/15 (73%) | 18/57 (32%) | 0% | 24/99 (24%) |
| lora_verbose2 | TinyLlama-1.1B | 100% / 100% | +0 | 100% / 100% | +0 | 31/71 (44%) | 18/70 (26%) | 100% | – |
| lora_verbose2 | Qwen2.5-3B | 100% / 100% | +0 | 100% / 100% | +0 | 36/74 (49%) | 25/97 (26%) | 0% | 35/100 (35%) |
| lora_verbose2 | gemma-2b | 0% / 0% | +0 | 0% / 0% | +0 | 25/31 (81%) | 27/89 (30%) | 0% | 29/100 (29%) |
| base_compact | TinyLlama-1.1B | – / – | – | – / – | – | – | – | – | – |
| base_compact | Qwen2.5-3B | – / – | – | – / – | – | – | – | 100% | – |
| base_compact | gemma-2b | – / – | – | – / – | – | – | – | – | – |
| lora_compact | TinyLlama-1.1B | 100% / 100% | +0 | 100% / 100% | +0 | 0/98 (0%) | 3/91 (3%) | 0% | 8/99 (8%) |
| lora_compact | Qwen2.5-3B | 100% / 58% | +42 | 100% / 100% | +0 | 1/100 (1%) | 1/96 (1%) | 0% | 3/97 (3%) |
| lora_compact | gemma-2b | 100% / 68% | +32 | 100% / 100% | +0 | 0/100 (0%) | 1/94 (1%) | 1% | 4/99 (4%) |
| base_grammar | TinyLlama-1.1B | 100% / 100% | +0 | 100% / 100% | +0 | 85/100 (85%) | 32/84 (38%) | 0% | 32/81 (40%) |
| base_grammar | Qwen2.5-3B | 0% / 0% | +0 | 0% / 2% | -2 | 79/100 (79%) | 29/88 (33%) | 0% | 34/98 (35%) |
| base_grammar | gemma-2b | 100% / 100% | +0 | 100% / 94% | +6 | 84/100 (84%) | 29/84 (35%) | 0% | 22/64 (34%) |
| lora_grammar | TinyLlama-1.1B | 100% / 100% | +0 | 100% / 98% | +2 | 64/100 (64%) | 24/85 (28%) | 0% | 28/79 (35%) |
| lora_grammar | Qwen2.5-3B | 100% / 100% | +0 | 100% / 100% | +0 | 55/100 (55%) | 22/91 (24%) | 0% | 15/99 (15%) |
| lora_grammar | gemma-2b | 36% / 30% | +6 | 0% / 0% | +0 | 82/100 (82%) | 25/85 (29%) | 0% | 12/67 (18%) |
| teacher | training corpus | 100% / 41% | +59 | 100% / 45% | +55 | 26/3000 (1%) | 9/3000 (0%) | 23% | 132/2309 (6%) |

## Agreement

Given the same item, do two settings make the same decision?

Same decision on the same item (95% CI; compared items in brackets).

| TinyLlama-1.1B | base_verbose | lora_verbose | base_verbose2 | lora_verbose2 | base_compact | lora_compact | base_grammar | lora_grammar |
|---|---|---|---|---|---|---|---|---|
| base_verbose | · | – (0) | – (0) | – (0) | – (0) | – (0) | – (0) | – (0) |
| lora_verbose | – (0) | · | – (0) | 69% [64–73] (490) | – (0) | 23% [19–27] (490) | 17% [14–20] (469) | 36% [32–40] (487) |
| base_verbose2 | – (0) | – (0) | · | – (0) | – (0) | – (0) | – (0) | – (0) |
| lora_verbose2 | – (0) | 69% [64–73] (490) | – (0) | · | – (0) | 31% [27–35] (492) | 11% [9–15] (470) | 47% [43–52] (488) |
| base_compact | – (0) | – (0) | – (0) | – (0) | · | – (0) | – (0) | – (0) |
| lora_compact | – (0) | 23% [19–27] (490) | – (0) | 31% [27–35] (492) | – (0) | · | 6% [4–8] (470) | 31% [27–36] (488) |
| base_grammar | – (0) | 17% [14–20] (469) | – (0) | 11% [9–15] (470) | – (0) | 6% [4–8] (470) | · | 14% [11–17] (468) |
| lora_grammar | – (0) | 36% [32–40] (487) | – (0) | 47% [43–52] (488) | – (0) | 31% [27–36] (488) | 14% [11–17] (468) | · |

| Qwen2.5-3B | base_verbose | lora_verbose | base_verbose2 | lora_verbose2 | base_compact | lora_compact | base_grammar | lora_grammar |
|---|---|---|---|---|---|---|---|---|
| base_verbose | · | 51% [46–55] (492) | 24% [20–28] (488) | 38% [33–42] (492) | 0% [0–79] (1) | 29% [25–33] (491) | 32% [28–36] (488) | 35% [31–39] (492) |
| lora_verbose | 51% [46–55] (492) | · | 13% [11–17] (488) | 55% [51–60] (492) | 0% [0–79] (1) | 31% [27–36] (491) | 20% [17–24] (488) | 55% [51–59] (492) |
| base_verbose2 | 24% [20–28] (488) | 13% [11–17] (488) | · | 17% [14–20] (488) | 0% [0–79] (1) | 8% [6–11] (487) | 38% [33–42] (484) | 12% [9–15] (488) |
| lora_verbose2 | 38% [33–42] (492) | 55% [51–60] (492) | 17% [14–20] (488) | · | 0% [0–79] (1) | 34% [30–38] (491) | 18% [15–21] (488) | 59% [55–63] (492) |
| base_compact | 0% [0–79] (1) | 0% [0–79] (1) | 0% [0–79] (1) | 0% [0–79] (1) | · | 0% [0–79] (1) | 0% [0–79] (1) | 0% [0–79] (1) |
| lora_compact | 29% [25–33] (491) | 31% [27–36] (491) | 8% [6–11] (487) | 34% [30–38] (491) | 0% [0–79] (1) | · | 10% [7–13] (487) | 37% [33–41] (491) |
| base_grammar | 32% [28–36] (488) | 20% [17–24] (488) | 38% [33–42] (484) | 18% [15–21] (488) | 0% [0–79] (1) | 10% [7–13] (487) | · | 19% [16–23] (488) |
| lora_grammar | 35% [31–39] (492) | 55% [51–59] (492) | 12% [9–15] (488) | 59% [55–63] (492) | 0% [0–79] (1) | 37% [33–41] (491) | 19% [16–23] (488) | · |

| gemma-2b | base_verbose | lora_verbose | base_verbose2 | lora_verbose2 | base_compact | lora_compact | base_grammar | lora_grammar |
|---|---|---|---|---|---|---|---|---|
| base_verbose | · | 32% [28–36] (492) | 30% [26–34] (489) | 11% [9–14] (492) | – (0) | 5% [3–7] (492) | 20% [17–24] (492) | 5% [4–8] (492) |
| lora_verbose | 32% [28–36] (492) | · | 47% [42–51] (489) | 23% [19–27] (492) | – (0) | 28% [24–32] (492) | 13% [11–16] (492) | 23% [20–27] (492) |
| base_verbose2 | 30% [26–34] (489) | 47% [42–51] (489) | · | 21% [18–25] (489) | – (0) | 23% [19–27] (489) | 15% [12–18] (489) | 11% [9–15] (489) |
| lora_verbose2 | 11% [9–14] (492) | 23% [19–27] (492) | 21% [18–25] (489) | · | – (0) | 10% [8–13] (492) | 17% [14–20] (492) | 52% [47–56] (492) |
| base_compact | – (0) | – (0) | – (0) | – (0) | · | – (0) | – (0) | – (0) |
| lora_compact | 5% [3–7] (492) | 28% [24–32] (492) | 23% [19–27] (489) | 10% [8–13] (492) | – (0) | · | 7% [5–10] (492) | 12% [9–15] (492) |
| base_grammar | 20% [17–24] (492) | 13% [11–16] (492) | 15% [12–18] (489) | 17% [14–20] (492) | – (0) | 7% [5–10] (492) | · | 23% [20–27] (492) |
| lora_grammar | 5% [4–8] (492) | 23% [20–27] (492) | 11% [9–15] (489) | 52% [47–56] (492) | – (0) | 12% [9–15] (492) | 23% [20–27] (492) | · |

