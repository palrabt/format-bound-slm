---
title: Format-bound competence of fine-tuned small language models in a card game
authors: Laszlo Paksi*
affiliation: Roska Tamás Doctoral School of Sciences and Technology, Faculty of Information Technology and Bionics, Pázmány Péter Catholic University, Práter u. 50/A, H-1083 Budapest, Hungary
email: [e-mail]
abstract: Small language models with low-rank adapters are candidate negotiating agents on edge devices. Three recent models, each with and without an adapter trained on a rule-based teacher, were evaluated under four prompt styles in a three-player trading card game, on 992 fixed states and in 30 seeded games. In the training format, 68–90% of the adapted models' decisions followed a rule-based reference, 16–29 points above a verbose prompt, and in play their coins did not differ significantly from a rule-based player's. Under other prompts, two adapters fell to the level of random play. Grammar-constrained base models were 97–100% valid, yet only 24–41% of their decisions were correct. Two prompts rarely led a model to the same decision. An earlier model generation showed the same main patterns.
keywords: small language models, low-rank adaptation, prompt format, negotiation, game-based evaluation, decision quality
data: Code, prompts, answer schemas, the decoding grammar, seeds, run logs and the scripts behind every number are available at https://github.com/palrabt/format-bound-slm.git.
---

# Introduction

Edge devices with limited resources are expected to take on agentic roles in multi-agent systems, where an agent that negotiates well with its peers secures better local outcomes [@belcak2025slm]. Devices of this class cannot host large models, so it is worth asking whether small language models can provide any sort of benefits in these environments.

Low-rank adaptation (LoRA) [@hu2022lora] is the usual way to specialize a small model without changing its base weights. Fine-tuned small models can call functions on the device itself [@erdogan2024tinyagent]. For tool-calling agents, LoRA-based supervised fine-tuning was the strongest in-distribution method in 15 of 18 settings [@laskar2026sftrl].

Staged recipes first make 2-billion-parameter models playable in dialogue games and then improve their decisions [@huq2026playable], while targeted repairs raise in-domain scores but leave out-of-domain scores low [@li2026acquire]. These studies vary the training. An adapter, however, is trained on one input format, and comparing a base model under one prompt with its adapter under another changes the weights and the prompt at once. The prompt format is not a cosmetic detail: formatting alone can move accuracy by tens of points [@sclar2024format], the choice of template changes the conclusions of comparisons [@voronov2024mindyourformat], and evaluation with a single prompt is unreliable [@mizrahi2024stateofwhatart]. Requesting structured output can degrade reasoning while the structure stays correct [@tam2024format], although grammar-constrained decoding has also been found to raise accuracy slightly [@geng2025jsonschemabench]. Agentic benchmarks, finally, need trivial-agent baselines to show what a score is worth [@zhu2025abc].

This study holds each adapter fixed and varies the prompt it is used with. Three recent base models, each with and without a LoRA adapter trained on the decisions of a rule-based teacher, are crossed with four prompt styles in a simplified three-player version of Bohnanza, a bean-trading card game in which every move is a structured answer and every trade carries a free-text message. Decisions are scored against a rule-based reference on 992 fixed game states and in seeded games against bot opponents, and are compared with a fixed rule that ignores every offer. An earlier generation of three models, run with the same corpus, recipe and evaluation, serves as a replication. The results show that every adapter does significantly better in the training format, although how much competence survives outside it depends on the model; that structural validity does not predict decision quality; that the prompt changes the decision itself rather than its phrasing; that the lead over the fixed rule ranges from negligible to large; and that in play the adapters earn as much as the rule-based reference player but no more. The study is descriptive: it makes no claim of general strategic reasoning, nor of results for other teachers, games or model families.

# Materials and methods

## The game

Bohnanza is a card game in which players earn coins by harvesting fields of matching beans. The deck holds bean types with 6 (Garden Bean) to 24 (Coffee Bean) copies, and rarer beans need fewer cards per coin. Each player has three fields, each growing one bean type. Due to the built in mandatory planting the players must trade for the beans they need and for giving away the ones that would break their strategies. 

This experiment used a simplified implementation of the game, capturing the essence of the game in five simple structured messages. Each actions belongs to one of five message types:

- PLANTING: plant the first one or two cards of the hand;
- FORCED: plant every card received in a trade or drawn;
- TRADING: offer cards to one of the two other players, or pass;
- REPLY: accept or reject an offer, optionally proposing cards in return, with a free-text message;
- CONSIDERING: accept or reject the cards proposed in return.

The active player starts in the PLANTING phase. This is a forced action, they have to place at least one card into one of the fields. It is followed by TRADING, in this implementation the player has three attempts to give away cards or ask for new ones. Every trading messages is answered by a REPLY from the peer player it contains the acceptance or the rejection of the trade and possible cards offered in return. In case of a rejection the trading cycle is concluded and the active player initiate a new trading. When an afformative response is received the player enters into the CONSIDERING phase and evealuates whether the conter offer still suits its goals. After all trading is concluded the game enters into the FORCED phase when the player have to place all newly received cards into their fields.

Two properties make the game a controlled testbed. It is fully observable, so each decision can be checked against the information the player sees rather than against a subjective judgment. It is mixed-motive, each player maximizes its own coins but cannot do so without trading.

To mimic a mixed-agentic network, where models and target sotfwares co-exist all communication is conducted via structured JavaScript Object Notation (JSON). That measures the models capabilities threefold: generating a structured output format, playing the game by the rules, negotiating.

## Models and adapters

Three base models were served with the llama-server of llama.cpp [@gerganov2023llamacpp], all with 8-bit Q8_0 weights: LFM2.5-1.2B-Instruct [@liquid2026lfm], Granite 4.2 3B [@ibm2026granite] and Gemma 4 E2B [@gemma2026]. Each is served with its own chat template with thinking switched off, the template also used to render the training prompts. Each model has one LoRA adapter with rank 32, scaling factor 64 and dropout 0.05 on all linear layers, trained in bfloat16 for 2 epochs (422 updates) at a learning rate of 0.0001 with a cosine schedule, 5% warm-up, an effective batch size of 64 and sequences of up to 768 tokens, the recipe reported as best in-distribution in [@laskar2026sftrl]. The training corpus holds 15,000 examples, 3,000 per message type, split with seed 0 into 13,500 training and 1,500 validation sequences. The final validation loss was 0.357 for LFM2.5, 0.355 for Granite and 0.367 for Gemma 4. The teacher is partly random. It plants on field 1 when no field fits, plants its second card at random, picks its trading partner and whether to pass at random, and accepts about 40–45% of useless offers.

The prior study used an earlier generation trained on the same corpus with the same recipe and evaluated on the same states and seeds: TinyLlama-1.1B-Chat-v1.0 [@zhang2024tinyllama] served in 16-bit precision, Qwen2.5-3B-Instruct [@qwen2024] with 4-bit Q4_K_M weights, and Gemma-2B-it [@gemma2024] in 32-bit precision.

## Prompt conditions

Over the analysis the adapters were unchanged and the other conditions were changed. The adapter, absent or present, is crossed with four prompt styles, giving eight conditions per model, named `base_<style>` or `lora_<style>`:

- verbose: a system prompt with the game rules and an instruction to answer in JSON;
- verbose2: a reworded variant of verbose with the same information;
- compact: the bare game state in JSON, byte-identical to the user turn in training;
- grammar: the verbose prompt, with a JSON grammar constraining the decoding.

The sampling temperature is 0 in every condition.

## Replay corpus, metrics and baselines

The replay corpus holds 992 fixed states in two slices. The game slice has 500 states from earlier games, 100 per message type, balanced between a useful and a useless offer (REPLY, CONSIDERING) and between states where a harvest-free placement exists or not (PLANTING, FORCED). The training slice has 492 held-out teacher states with the teacher's own answers.

The following metrics were used to measure the adapters' effectiveness:

- schema validity: the answer matches the JSON schema of its message type.
- legality: the game's own parser and rules accept the answer as it is, e.g. offered cards are present, they can be traded.
- reference-correctness: the answer is legal and keeps every rule of a reference, which is the teacher's deterministic rules with its random choices replaced by value rules.
- teacher match (training slice): the decision equals the teacher's own answer, a share capped below 100% by the teacher's randomness.
- avoidable harvests: the share of plantings that harvest a field although the cards fitted on empty or same-bean fields.
- agreement: for two conditions, the share of states on which a model makes the identical decision.


The baseline is set by two players that do not learn: the reference bot and the random bot. The reference bot plays the reference, so on the replay corpus it is reference-correct by definition. It serves as the player to match in the tournaments. The random bot plays a uniformly random legal move and is a baseline in both the replay and the tournaments. A fixed rule serves as a third, trivial baseline on the replay corpus only: it always passes in TRADING, accepts every offer and every counter-offer while giving nothing in return and plants on the first available location.

Shares carry Wilson 95% intervals. Differences between conditions on the same states are tested with exact McNemar tests and paired bootstrap intervals (2,000 resamples, seed 0), with Holm correction within each family of tests.

## Tournaments

To assess the models and the adapters in a more realistic setting, a tournament environment was created in which three players play 30 seeded games. Each table consists of two bots of one kind, either reference bots or random bots, and one evaluated player: a model in one of four conditions (`lora_compact`, `base_grammar`, `lora_verbose`, `base_verbose`) or one of the two baseline bots. Game g uses deck seed g and seat (g − 1) mod 3, so the seat rotates from game to game and every evaluated player meets the same card sequences in the same seats. Coins per game are compared with each baseline bot on the same seed and seat, with Wilcoxon signed-rank tests, Holm correction and bootstrap intervals over games. A game counts as won when the player earns strictly more coins than both opponents. Per-model and pooled figures are reported side by side, because pooling across models that behave differently can reverse the apparent direction of an effect [@prost2022simpson].

# Results and discussion

## Competence is largest in the training format

Table: Replay results by condition: schema validity and legality on the 992 states, reference-correctness and avoidable harvests on the game slice, in %; three values are LFM2.5 / Granite / Gemma 4. The baselines do not depend on the model, and the random bot's row is one seeded draw; – marks a value that does not apply. {#tab:replay}
| Player | Schema-valid | Legal | Correct | Avoidable harvests |
|---|---|---|---|---|
| `lora_compact` | 100 / 100 / 100 | 99 / 100 / 100 | 78 / 90 / 68 | 3 / 4 / 10 |
| `lora_verbose` | 100 / 100 / 100 | 99 / 98 / 88 | 49 / 74 / 45 | 41 / 17 / 39 |
| `lora_verbose2` | 100 / 100 / 97 | 99 / 94 / 89 | 42 / 63 / 49 | 57 / 27 / 38 |
| `lora_grammar` | 94 / 97 / 80 | 93 / 97 / 80 | 44 / 74 / 27 | 45 / 13 / 50 |
| `base_compact` | 0 / 0 / 0 | 0 / 0 / 18 | 0 / 0 / 10 | – |
| `base_verbose` | 52 / 100 / 100 | 75 / 85 / 95 | 34 / 45 / 42 | 62 / 42 / 43 |
| `base_verbose2` | 96 / 100 / 100 | 71 / 89 / 87 | 32 / 42 / 43 | 45 / 28 / 50 |
| `base_grammar` | 97 / 100 / 100 | 81 / 93 / 95 | 24 / 41 / 37 | 62 / 59 / 62 |
| fixed rule | – | 100 | 67 | 0 |
| random bot | – | 100 | 44 | – |

In the training format, `lora_compact` is reference-correct on 78/90/68% of the game slice and 77/91/71% of the training slice (LFM2.5/Granite/Gemma 4 throughout; Table @tab:replay). The same adapters under the verbose prompt reach 49/74/45%: within the adapted models, compact against verbose is worth +29/+16/+23 points on the game slice and +28/+22/+15 on the training slice, with Holm-corrected p < 0.001 in all six comparisons. Attaching the adapter at the verbose prompt depends strongly on the model, LFM2.5 gains 15 points and Granite 29 (both Holm p < 0.001), while Gemma 4 gains 3 (Holm p = 0.76). The compact format is not an instruction to a base model, `base_compact` is never schema-valid, and only Gemma 4 gives any legal answers (18%).

Granite is the exception for the format-bound competence. Its adapter keeps 63–74% reference-correctness under the three other prompts, above the fixed rule's 67% in two of them, whereas the adapters of LFM2.5 and Gemma 4 fall to 42–49% and 27–49%. Competence is therefore not bound to the training format in the same degree for every model, and this study does not identify why. The same training recipe and data yield an adapter effect at the verbose prompt that ranges from not significant to 29 points depending on the base model, in line with prompt-format effects that correlate only weakly across models [@sclar2024format]. An adapter can also harm outside its format. Under the grammar, the adapter lowers Gemma 4 by 10 points (Holm p = 0.031). This qualifies the view of LoRA as a conservative change [@biderman2024lora].

## A well-formed answer is not a good decision

`base_grammar` is 97–100% schema-valid, yet only 24–41% of its decisions are reference-correct, and 59–62% of its plantings make an avoidable harvest. Grammar-constrained decoding does not guarantee validity either for instance `lora_grammar` of Gemma 4 is 80% valid, because all its TRADING answers fall short of the number of items the schema requires. The grammar lowered the decisions of all three base models against the verbose prompt, by 10/4/5 points, significantly only for LFM2.5 (Holm p < 0.001), whose verbose answers are valid only 52% of the time. Against random-bot opponents `base_grammar` earns no more than the random bot (pooled difference −0.09 coins, Holm p = 1.0). Validity and decision quality are separable, a guarantee of valid structure says nothing about the decision inside it. This agrees with format restrictions degrading reasoning [@tam2024format] and contrasts with the small gains reported for grammar-constrained decoding [@geng2025jsonschemabench].

## The prompt changes most decisions

Table: Agreement by condition on the game slice: the share of states on which a model gives the same decision as under each other condition, averaged over the six comparable pairs, mean % [range]. `base_compact` gives almost no readable decision and is left out. {#tab:agreement}
| Condition | LFM2.5 | Granite | Gemma 4 |
|---|---|---|---|
| `base_verbose` | 17 [4–31] | 18 [7–43] | 25 [8–45] |
| `lora_verbose` | 21 [6–32] | 30 [6–63] | 23 [13–45] |
| `base_verbose2` | 21 [8–49] | 13 [9–29] | 24 [7–38] |
| `lora_verbose2` | 26 [11–49] | 28 [7–53] | 27 [8–45] |
| `lora_compact` | 14 [4–32] | 25 [2–49] | 11 [3–24] |
| `base_grammar` | 13 [4–26] | 13 [2–43] | 23 [3–45] |
| `lora_grammar` | 26 [11–41] | 32 [7–63] | 25 [21–30] |

On the game slice, two conditions of the same model agree on only 20/23/22% of the states on average, and pairs that include `lora_compact` on 14/25/11% (range 2–49%); the training slice gives 21/22/22%. Table @tab:agreement shows that the adapter does not make a model consistent across prompts in general: even Granite, the model that keeps most of its competence, reaches at most 63% between two conditions, and that only between the verbose and grammar prompts with the adapter. The prompt therefore changes which decision a model makes on an identical state, not only how the answer is phrased. This extends the finding that formatting moves accuracy [@sclar2024format] from an aggregate score to the individual decision, within a single fine-tuned model.

## Coins and wins against bot opponents

Table: Mean coins per game (30 games each) and the share of games won, in %, by opponent suite; coins with three values are LFM2.5 / Granite / Gemma 4, and wins are pooled over the three models. {#tab:coins}
| Player | Coins, reference-bot opponents | Coins, random-bot opponents | Wins, reference-bot opponents | Wins, random-bot opponents |
|---|---|---|---|---|
| `lora_compact` | 8.73 / 8.40 / 7.93 | 4.80 / 5.43 / 5.60 | 31 | 79 |
| reference bot | 8.33 | 5.57 | 23 | 83 |
| random bot | 2.20 | 2.40 | 0 | 37 |
| `base_grammar` | 2.77 / 2.53 / 3.10 | 1.90 / 2.53 / 2.50 | 1 | 33 |
| `lora_verbose` | 2.47 / 4.00 / 1.40 | 2.03 / 4.63 / 1.60 | 0 | 38 |
| `base_verbose` | 2.60 / 1.57 / 1.83 | 1.50 / 1.63 / 1.93 | 0 | 16 |


`lora_compact` earns 8.73/8.40/7.93 coins per game against reference-bot opponents and 4.80/5.43/5.60 against random-bot opponents, while the reference bot earns 8.33 and 5.57 and the random bot 2.20 and 2.40 (Table @tab:coins). Paired by seed and seat, it earns as much as the reference bot (pooled differences of +0.02 and −0.29 coins, Holm p = 1.0) but is not shown to exceed it. It wins 31% of its games against reference-bot opponents, against the reference bot's 23%, and 79% against random-bot opponents, against 83%.

Every other player earns significantly less than the reference bot, except Granite's `lora_verbose` against random-bot opponents (−0.93 coins, Holm p = 0.15). Most do not differ significantly from the random bot. The exceptions are Granite's `lora_verbose`, which out-earns it by 1.80 and 2.23 coins, and `base_verbose`, which earns 0.71 coins less than it against random-bot opponents. 


## Behavior matching

Table: Teacher match by condition and message type on the 492 held-out training states: the share of states on which the decision equals the teacher's own answer, in %; three values are LFM2.5 / Granite / Gemma 4. The teacher decides partly at random, so no deterministic player matches it on every state; the random bot's row is one seeded draw. {#tab:teacher}
| Condition | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | Overall |
|---|---|---|---|---|---|---|
| `base_verbose` | 8 / 42 / 28 | 7 / 11 / 17 | 7 / 25 / 4 | 10 / 4 / 12 | 0 / 2 / 0 | 7 / 17 / 12 |
| `lora_verbose` | 44 / 38 / 32 | 21 / 68 / 33 | 6 / 7 / 6 | 27 / 27 / 22 | 57 / 59 / 32 | 30 / 39 / 25 |
| `base_verbose2` | 4 / 28 / 12 | 1 / 16 / 26 | 0 / 4 / 25 | 21 / 2 / 2 | 29 / 0 / 4 | 11 / 10 / 14 |
| `lora_verbose2` | 8 / 32 / 14 | 21 / 49 / 39 | 2 / 8 / 21 | 21 / 34 / 24 | 29 / 57 / 39 | 16 / 36 / 27 |
| `base_compact` | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 11 | 0 / 0 / 0 | 0 / 0 / 2 |
| `lora_compact` | 73 / 73 / 74 | 80 / 89 / 84 | 7 / 7 / 4 | 28 / 31 / 16 | 63 / 59 / 61 | 50 / 52 / 48 |
| `base_grammar` | 10 / 8 / 12 | 20 / 20 / 24 | 2 / 26 / 5 | 1 / 0 / 2 | 0 / 1 / 10 | 7 / 11 / 11 |
| `lora_grammar` | 21 / 46 / 18 | 32 / 66 / 34 | 3 / 3 / 0 | 24 / 33 / 29 | 34 / 60 / 60 | 23 / 41 / 28 |
| reference bot | 61 | 100 | 9 | 33 | 59 | 52 |
| random bot | 13 | 11 | 20 | 18 | 40 | 20 |

Overall, `lora_compact` matches the teacher about as often as the reference bot (52%), which replaces the teacher's random and arbitrary choices with value rules, and in PLANTING more often (73–74% against 61%), where the teacher plants on field 1 when no field fits and the reference bot does not

The match is highest where the teacher's rules are deterministic, which suggests that an adapter would follow a fully deterministic teacher more closely.

## Replication in an earlier model generation

Table: The same measures in the two model generations. Three values are TinyLlama / Qwen / Gemma-2B for the earlier generation and LFM2.5 / Granite / Gemma 4 for the main study; coin differences give the suites against reference-bot / random-bot opponents, with the Holm-corrected p where it matters. Decision measures are in % on the game slice. {#tab:replication}
| Measure | Earlier generation | Main study |
|---|---|---|
| Correct, `lora_compact` | 69 / 75 / 73 | 78 / 90 / 68 |
| Correct, `lora_verbose` | 46 / 45 / 44 | 49 / 74 / 45 |
| Compact over verbose, adapted, points | +23 / +30 / +29 | +29 / +16 / +23 |
| Adapter at verbose, points | +46 / +1 / +7 | +15 / +29 / +3 |
| Schema-valid, `base_grammar` | 96 / 100 / 100 | 97 / 100 / 100 |
| Correct, `base_grammar` | 22 / 37 / 30 | 24 / 41 / 37 |
| Agreement between conditions | 25 / 29 / 20 | 20 / 23 / 22 |
| Lead over the fixed rule, points | +2 / +8 / +6 | +11 / +23 / +1 |
| `lora_compact` vs reference bot, coins | −0.68 / −0.08 (both n.s.) | +0.02 / −0.29 (both n.s.) |
| `lora_compact` vs random bot, coins | +5.46 / +3.09 (p < 0.001) | +6.16 / +2.88 (p < 0.001) |
| `lora_verbose` vs random bot, coins | −0.72 / −0.66 (p = 0.031, 0.044) | +0.42 / +0.36 (p = 0.27, 0.24) |

Most findings hold across the two generations, which share no model (Table @tab:replication). In both, every adapter is significantly better in the compact format than under the verbose prompt (Holm p < 0.001), `lora_compact` earns as much as the reference bot and far more than the random bot, grammar-constrained base models are almost always valid and mostly wrong, and two conditions of a model rarely agree. Two results do not carry over. In the earlier generation, every adapter under the verbose prompt stayed at 44–46% and the adapted players earned significantly less than random legal play. In the main study, Granite's adapter works at 74% and the pooled adapted players are level with the random bot. Newer models did not bring uniform gains Gemma 4 scores below Gemma-2B in the training format (68% against 73%), although the coin results show no such loss.

## Limitations

The reference is derived from the teacher's deterministic rules, so competence here means imitating this partly random teacher, not optimal play. The six models belong to different families, and the two generations were served at different precisions, so differences between generations cannot be attributed to any single factor. Each adapter was trained with one seed and one configuration, so the difference between Granite and the other two models may partly reflect training variation. The game is simplified and short, about 9 turns per player.

# Conclusion

Within the prompt format it was trained on, a low-rank adapter for a small language model largely reproduces the teacher's handling of deterministic decisions. Every adapter does significantly better in that format, but how much competence survives outside it depends on the model. Two of the three adapters fall to about the level of a random player, while one keeps most of its decisions and still out-earns random play, though not the reference bot. Structural validity does not indicate decision quality, grammar-constrained base models are almost always well formed and mostly wrong. Evaluations of fine-tuned negotiation agents should therefore vary and report the prompt format together with the adapter, test more than one base model, and compare the agents with trivial baselines.

# Data availability {-}

{{data}}


# Acknowledgements {-}

[Grants and technical help to be added.]
