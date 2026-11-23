---
title: Format-bound competence of fine-tuned small language models in a card game
authors: Laszlo Paksi*
affiliation: Roska Tamás Doctoral School of Sciences and Technology, Faculty of Information Technology and Bionics, Pázmány Péter Catholic University, Práter u. 50/A, H-1083 Budapest, Hungary
email: [e-mail]
abstract: Small language models with low-rank adapters are candidate negotiating agents on edge devices. Three recent models, with and without an adapter trained on a deterministic rule-based teacher, were tested under four prompts in a three-player trading card game, on 1,000 fixed states and 30 seeded games. In the training format, the adapted models made the teacher's decision on 80–91% of game states and 87–95% of held-out states, 37–56 points more often than under a verbose prompt, and in play their coins did not differ significantly from the teacher's. Under the verbose prompt, no adapted model out-earned random play. Grammar-constrained base models were 97–100% valid, yet matched the teacher on only 2–12% of game states, below random play. Two prompts rarely led a model to the same decision.
keywords: small language models, low-rank adaptation, prompt format, negotiation, game-based evaluation, decision quality
data: Code, prompts, answer schemas, the decoding grammar, seeds, run logs and the scripts behind every number are available at https://github.com/palrabt/format-bound-slm.git.
---

# Introduction

Edge devices with limited resources are expected to take on agentic roles in multi-agent systems, where an agent that negotiates well with its peers secures better local outcomes [@belcak2025slm]. Devices of this class cannot host large models, so it is worth asking whether small language models can provide any sort of benefits in these environments.

Low-rank adaptation (LoRA) [@hu2022lora] is the usual way to specialize a small model without changing its base weights. Fine-tuned small models can call functions on the device itself [@erdogan2024tinyagent]. For tool-calling agents, LoRA-based supervised fine-tuning was the strongest in-distribution method in 15 of 18 settings [@laskar2026sftrl].

Staged recipes first make 2-billion-parameter models playable in dialogue games and then improve their decisions [@huq2026playable], while targeted repairs raise in-domain scores but leave out-of-domain scores low [@li2026acquire]. These studies vary the training. An adapter, however, is trained on one input format, and comparing a base model under one prompt with its adapter under another changes the weights and the prompt at once. The prompt format is not a cosmetic detail: formatting alone can move accuracy by tens of points [@sclar2024format], the choice of template changes the conclusions of comparisons [@voronov2024mindyourformat], and evaluation with a single prompt is unreliable [@mizrahi2024stateofwhatart]. Requesting structured output can degrade reasoning while the structure stays correct [@tam2024format], although grammar-constrained decoding has also been found to raise accuracy slightly [@geng2025jsonschemabench]. Agentic benchmarks, finally, need trivial-agent baselines to show what a score is worth [@zhu2025abc].

This study holds each adapter fixed and varies the prompt it is used with. Three recent base models, each with and without a LoRA adapter trained on the decisions of a deterministic rule-based teacher, are crossed with four prompt styles in a simplified three-player version of Bohnanza, a bean-trading card game in which every move is a structured answer and every trade carries a free-text message. Decisions are scored against the teacher on 1,000 fixed game states and in seeded games against bot opponents, and are compared with a fixed rule that rejects every offer. The results show that every adapter does significantly better in the training format, where it makes the teacher's own decision on most states, although how much competence survives outside it depends on the model; that structural validity does not predict decision quality; that the prompt changes the decision itself rather than its phrasing; that in the training format the adapters lead the fixed rule by 31–43 points; and that in play the adapters' coins do not differ significantly from their teacher's. The study is descriptive: it makes no claim of general strategic reasoning, nor of results for other teachers, games or model families.

# Materials and methods

## The game

Bohnanza is a card game in which players earn coins by harvesting fields of matching beans. The deck holds bean types with 6 (Garden Bean) to 24 (Coffee Bean) copies, and rarer beans need fewer cards per coin. Each player has three fields, each growing one bean type. Due to the built-in mandatory planting the players must trade for the beans it needs and for giving away the ones that would break their strategies. 

This experiment used a simplified implementation of the game, capturing the essence of the game in five simple structured messages. Each action belongs to one of five message types:

- PLANTING: plant the first one or two cards of the hand;
- FORCED: plant every card received in a trade or drawn;
- TRADING: offer cards to one of the two other players, or pass;
- REPLY: accept or reject an offer, optionally proposing cards in return, with a free-text message;
- CONSIDERING: accept or reject the cards proposed in return.

The active player starts in the PLANTING phase. This is a forced action, they have to place at least one card into one of the fields. It is followed by TRADING, in this implementation the player has three attempts to give away cards or ask for new ones. Every trading messages is answered by a REPLY from the peer player, it contains the acceptance or the rejection of the trade and possible cards offered in return. In case of a rejection the trading cycle is concluded and the active player initiates a new trading. When an affirmative response is received the player enters into the CONSIDERING phase and evaluates whether the counter-offer still suits its goals. After all trading is concluded the game enters into the FORCED phase when the player have to place all newly received cards into their fields.

Two properties make the game a controlled testbed. It is fully observable, so each decision can be checked against the information the player sees rather than against a subjective judgment. It is mixed-motive, each player maximizes its own coins but cannot do so without trading.

To mimic a mixed-agentic network, where models and target softwares co-exist all communication is conducted via structured JavaScript Object Notation (JSON). That measures the models capabilities threefold: generating a structured output format, playing the game by the rules, negotiating.

## Models and adapters

Three base models were served with the llama-server of llama.cpp [@gerganov2023llamacpp], all with 8-bit Q8_0 weights: LFM2.5-1.2B-Instruct [@liquid2026lfm], Granite 4.2 3B [@ibm2026granite] and Gemma-4 E2B [@gemma2026]. Each is served with its own chat template with thinking switched off, the template also used to render the training prompts. Each model has one LoRA adapter with rank 32, scaling factor 64 and dropout 0.05 on all linear layers, trained in bfloat16 for 2 epochs (422 updates) at a learning rate of 0.0001 with a cosine schedule, 5% warm-up, an effective batch size of 64 and sequences of up to 768 tokens, the recipe reported as best in-distribution in [@laskar2026sftrl]. The training corpus holds 15000 examples, 3000 per message type, split with seed 0 into 13500 training and 1500 validation sequences. Its game states were drawn by a synthetic generator, and the free text a player receives in them was reworded by Phi-4, a 14-billion-parameter model. Every state is answered by the teacher, the reference bot described below, and the free text of its answers is worded with fixed templates. The final validation loss was 0.056 for LFM2.5, 0.052 for Granite and 0.054 for Gemma-4.

## Prompt conditions

Over the analysis the adapters were unchanged but the prompt styles were. The adapter, absent or present, is crossed with four prompt styles, giving eight conditions per model, named `base_<style>` or `lora_<style>`:

- verbose: a system prompt with the game rules and an instruction to answer in JSON;
- verbose2: a reworded variant of verbose with the same information;
- compact: the bare game state in JSON, byte-identical to the user turn in training;
- grammar: the verbose prompt, with a JSON grammar constraining the decoding.

The sampling temperature is 0 in every condition.

## Replay corpus, metrics and baselines

The replay corpus holds 1,000 fixed states in two slices. The game slice has 500 states from earlier games, 100 per message type, balanced between a useful and a useless offer (REPLY, CONSIDERING) and between states where a harvest-free placement exists or not (PLANTING, FORCED). The training slice has 500 held-out states from the generator of the training corpus, also 100 per message type.

The following metrics were used to measure the adapters' effectiveness:

- schema validity: the answer matches the JSON schema of its message type.
- legality: the game's own parser and rules accept the answer as it is, e.g. offered cards are present, they can be traded.
- reference-correctness: the answer is legal and makes the decision the teacher makes in the same state: the same planting plan, the same pass, or the same cards offered to the same player, the same acceptance or rejection with the same cards given in return. The free text is not compared.
- valid play: the answer is legal and follows a basic greedy strategy. The reference bot's rules are one deterministic instance of this strategy.
- avoidable harvests: the share of plantings that harvest a field although the cards fitted on empty or same-bean fields.
- agreement: for two conditions of one model, the share of states on which both make the same decision, legal or not, among the states where both answers can be read. Reasonings are not compared.

Adapters capabilities are evaluated against a random player that valid and legal decision, two deterministic players: a trivial player and the reference bot. Prior is used to set the baseline. This player always passes, rejects every offer and counter-offer, and plants on a field of the same bean, else on an empty field, else on field 1.

The reference player plays a slightly more complex strategy, it plants a card on a field of the same bean, else on an empty field, else on the field with the least progress towards its next coin, and never harvests when the cards fit without it. It offers only beans it does not grow, to the player who grows most of them, and passes otherwise. It accepts exactly the offers and counter-offers that include a bean it grows, giving back a bean it does not grow. 

Shares carry Wilson 95% intervals. Differences between conditions on the same states are tested with exact McNemar tests and Holm correction within each family of tests.

## Tournaments

To assess the models and the adapters in a more realistic setting, a tournament environment was created in which three players play 30 seeded games. Each table consists of two bots of one kind, either reference bots or random bots, and one evaluated player: a model in one of four conditions (`lora_compact`, `base_grammar`, `lora_verbose`, `base_verbose`) or one of the two baseline bots. Game g uses deck seed g and seat (g − 1) mod 3, so the seat rotates from game to game and every evaluated player meets the same card sequences in the same seats. Coins per game are compared with each baseline bot on the same seed and seat, with Wilcoxon signed-rank tests, Holm correction and bootstrap intervals over games. A game counts as won when the player earns strictly more coins than both opponents. Per-model and pooled figures are reported side by side, because pooling across models that behave differently can reverse the apparent direction of an effect [@prost2022simpson].

# Results and discussion

## Competence is largest in the training format

Table: Replay results by condition on the game slice (500 states), in %; three values are LFM2.5 / Granite / Gemma-4. The baselines do not depend on the model, and the random bot's row is one seeded draw; – marks a value that does not apply. {#tab:replay}
| Player | Schema-valid | Legal | Valid play | Reference-correct | Avoidable harvests |
|---|---|---|---|---|---|
| `lora_compact` | 100 / 100 / 100 | 100 / 100 / 100 | 86 / 97 / 94 | 80 / 91 / 87 | 0 / 0 / 2 |
| `lora_verbose` | 100 / 98 / 100 | 94 / 91 / 87 | 42 / 70 / 44 | 24 / 54 / 32 | 57 / 19 / 33 |
| `lora_verbose2` | 100 / 98 / 81 | 97 / 88 / 72 | 43 / 67 / 27 | 23 / 47 / 12 | 60 / 30 / 44 |
| `lora_grammar` | 88 / 93 / 81 | 87 / 93 / 81 | 34 / 71 / 32 | 25 / 55 / 26 | 56 / 27 / 47 |
| `base_compact` | 0 / 0 / 0 | 0 / 0 / 18 | 0 / 0 / 10 | 0 / 0 / 10 | – |
| `base_verbose` | 52 / 100 / 100 | 75 / 85 / 95 | 34 / 45 / 42 | 9 / 14 / 7 | 62 / 42 / 43 |
| `base_verbose2` | 96 / 100 / 100 | 71 / 89 / 87 | 32 / 42 / 43 | 21 / 9 / 11 | 45 / 28 / 50 |
| `base_grammar` | 97 / 100 / 100 | 81 / 93 / 95 | 24 / 41 / 37 | 2 / 12 / 6 | 62 / 59 / 62 |
| fixed rule | – | 100 | 67 | 48 | 0 |
| random bot | – | 100 | 44 | 18 | – |

All conditions answered both slices of the replay corpus. The training slice gives the same picture as the game slice: its reference-correct shares are within −4 to +11 points of the game slice's (Table @tab:teacher, Overall). Competence shows in the valid-play and reference-correct columns. The players fall into four groups: those that cannot play, and three at the level of a baseline, the random bot, the fixed rule and the reference bot. The reference bot scores 100% in both columns by definition and is not shown in Table @tab:replay.

The compact prompt is not an instruction to a base model: `base_compact` is never schema-valid, and only Gemma-4 gives any legal answers (18%). Under the verbose prompts the base models play mostly below the level of the random bot: 24–45% of their moves are valid play and 2–21% of their decisions reference-correct, against the random bot's 44% and 18%, and 5–29% of their answers are illegal.

Attaching the adapter at the verbose prompt helps every model, by amounts that depend strongly on the model: LFM2.5 gains 15 points, Granite 39 and Gemma-4 25 (all Holm p < 0.001). This brings Granite to the level of the fixed rule: its adapter keeps 47–55% reference-correctness under the three other prompts, above the fixed rule's 48% in two of them, whereas the adapters of LFM2.5 and Gemma-4 fall to 23–25% and 12–32%, below the fixed rule, closer to the random bot. Competence is therefore not bound to the training format in the same degree for every model, and this study does not identify why. Outside its format an adapter can also add almost nothing: under the reworded verbose prompt, the adapter of Gemma-4 gains 2 points (Holm p = 1.0), largely because 73% of its TRADING answers write a pass with null fields, which the schema does not allow.

The training format is the best condition for every model. `lora_compact` is reference-correct on 80/91/87% of the game slice and 87/95/94% of the training slice (LFM2.5/Granite/Gemma-4 throughout), ahead of the fixed rule's 48% and 56% by 31–43 and 31–39 points (Holm p < 0.001 for every model on both slices). The same adapters under the verbose prompt reach 24/54/32%: within the adapted models, compact against verbose is worth +56/+37/+56 points on the game slice and +59/+45/+57 on the training slice, with Holm-corrected p < 0.001 in all six comparisons.

## A well-formed answer is not a good decision

Once a model is given the answer schema, by the prompt, the grammar or the adapter, at least four of its answers in five are schema-valid (81–100% of the game slice, Table @tab:replay). The one exception is LFM2.5's `base_verbose`, valid only 52% of the time, almost always because it wraps the JSON in prose (238 of its 242 failures). Under `base_compact`, which gives no schema, no answer is valid.

Legality follows schema validity but runs up to 25 points below it (`base_verbose2`), because a well-formed answer can still break a rule of the game or offer cards the player does not hold.

Eight condition–model pairs are schema-valid on all 500 game states. Their answers are 87–100% legal, yet only 37–97% of their moves are valid play and 6–91% of their decisions reference-correct. In the tournaments, the player with the most coins (Granite's `lora_compact`) and the one with the fewest (Gemma-4's `lora_verbose`) are both among the eight (Table @tab:coins).

Neither a well-formed answer, which almost every condition achieves, nor the adapter guarantees a good decision. This agrees with structured output degrading reasoning while the structure stays correct [@tam2024format]. The slight gains reported for grammar-constrained decoding [@geng2025jsonschemabench] do not appear here: against the verbose prompt, the grammar lowered the decisions of LFM2.5 and Granite by 7 and 3 points, significantly only for LFM2.5 (Holm p < 0.001), and left Gemma-4 unchanged.

## The prompt changes most decisions

Table: Agreement by condition on the game slice: the share of states on which a model gives the same decision as under each other condition, averaged over the six comparable pairs, mean % [range]. `base_compact` gives almost no readable decision and is left out. {#tab:agreement}
| Condition | LFM2.5 | Granite | Gemma-4 |
|---|---|---|---|
| `base_verbose` | 20 [10–39] | 19 [6–43] | 24 [7–45] |
| `lora_verbose` | 37 [9–55] | 33 [6–65] | 27 [10–54] |
| `base_verbose2` | 30 [10–46] | 12 [6–29] | 20 [10–30] |
| `lora_verbose2` | 36 [17–57] | 32 [8–53] | 22 [14–34] |
| `lora_compact` | 18 [2–26] | 31 [8–56] | 16 [5–33] |
| `base_grammar` | 15 [2–26] | 16 [6–43] | 22 [5–45] |
| `lora_grammar` | 36 [13–57] | 32 [6–65] | 29 [18–54] |

On the game slice, two conditions of the same model agree on only 28/25/23% of the states on average, and pairs that include `lora_compact` on 18/31/16% (range 2–56%), the training slice gives 29/24/26%. Table @tab:agreement shows that the adapter does not make a model consistent across prompts in general. Even Granite, the model that keeps most of its competence, reaches at most 65% between two conditions, and that only between the verbose and grammar prompts with the adapter. The prompt therefore changes which decision a model makes on an identical state, not only how the answer is phrased. This extends the finding that formatting moves accuracy [@sclar2024format] from an aggregate score to the individual decision, within a single fine-tuned model.

## Coins and wins against bot opponents

Table: Mean coins per game (30 games each) and the share of games won, in %, by opponent suite; coins with three values are LFM2.5 / Granite / Gemma-4, and wins are pooled over the three models. {#tab:coins}
| Player | Coins, reference-bot opponents | Coins, random-bot opponents | Wins, reference-bot opponents | Wins, random-bot opponents |
|---|---|---|---|---|
| `lora_compact` | 7.43 / 8.37 / 8.00 | 5.33 / 5.70 / 5.67 | 30 | 84 |
| reference bot | 8.33 | 5.57 | 23 | 83 |
| random bot | 2.20 | 2.40 | 0 | 37 |
| `base_grammar` | 2.77 / 2.53 / 3.10 | 1.90 / 2.53 / 2.50 | 1 | 33 |
| `lora_verbose` | 1.77 / 2.20 / 1.30 | 1.63 / 2.60 / 1.10 | 1 | 22 |
| `base_verbose` | 2.60 / 1.57 / 1.83 | 1.50 / 1.63 / 1.93 | 0 | 16 |


`lora_compact` earns 7.43/8.37/8.00 coins per game against reference-bot opponents and 5.33/5.70/5.67 against random-bot opponents, while its teacher, the reference bot, earns 8.33 and 5.57 and the random bot 2.20 and 2.40 (Table @tab:coins). Paired by seed and seat, it does not differ significantly from the reference bot (pooled differences of −0.40 [−1.08, +0.31] and +0.00 [−0.66, +0.67] coins, Holm p = 0.70 and 1.0), so it is not shown to exceed its teacher. It wins 30% of its games against reference-bot opponents, against the reference bot's 23%, and 84% against random-bot opponents, against 83%.

Every other player earns significantly less than the reference bot, and none of them earns significantly more than the random bot. Several earn significantly less than the random bot, among them Gemma-4's `lora_verbose` in both suites (−0.90 and −1.30 coins) and, against random-bot opponents, the pooled `lora_verbose` (−0.62 coins) and the pooled `base_verbose` (−0.71 coins). Granite's `lora_verbose`, the adapter that keeps most of its competence outside the training format, does not differ significantly from the random bot (+0.00 and +0.20 coins).

The opponents set the level of coins a competent player can reach. The reference bot earns 8.33 coins per game against two reference bots but 5.57 against two random bots, 2.77 fewer in the same seeded games, and lora_compact loses about as much (2.10/2.67/2.33 coins; Wilcoxon p < 0.001 in all four cases). Players near the random bot's level change by at most 1.1 coins.

## The adapter follows its teacher

Table: Reference-correctness by condition and message type on the 500 held-out training states: the share of states on which the decision equals the teacher's, in %; three values are LFM2.5 / Granite / Gemma-4. The teacher is the reference bot, which is correct on every state by definition; the random bot's row is one seeded draw. {#tab:teacher}
| Condition | PLANTING | FORCED | TRADING | REPLY | CONSIDERING | Overall |
|---|---|---|---|---|---|---|
| `base_verbose` | 7 / 23 / 9 | 7 / 11 / 17 | 0 / 44 / 1 | 26 / 0 / 6 | 0 / 1 / 0 | 8 / 16 / 7 |
| `lora_verbose` | 8 / 28 / 21 | 18 / 60 / 27 | 1 / 29 / 22 | 50 / 50 / 50 | 65 / 83 / 65 | 28 / 50 / 37 |
| `base_verbose2` | 3 / 13 / 3 | 1 / 16 / 26 | 0 / 0 / 42 | 50 / 0 / 0 | 65 / 0 / 11 | 24 / 6 / 16 |
| `lora_verbose2` | 4 / 20 / 9 | 23 / 58 / 27 | 15 / 34 / 3 | 50 / 50 / 11 | 65 / 76 / 66 | 31 / 48 / 23 |
| `base_compact` | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 29 | 0 / 0 / 0 | 0 / 0 / 6 |
| `lora_compact` | 89 / 92 / 93 | 82 / 88 / 84 | 96 / 95 / 96 | 95 / 100 / 98 | 74 / 100 / 98 | 87 / 95 / 94 |
| `base_grammar` | 9 / 11 / 6 | 20 / 20 / 24 | 1 / 47 / 1 | 2 / 0 / 1 | 0 / 0 / 29 | 6 / 16 / 12 |
| `lora_grammar` | 8 / 34 / 24 | 36 / 72 / 37 | 10 / 40 / 4 | 50 / 53 / 50 | 65 / 92 / 65 | 34 / 58 / 36 |
| fixed rule | 55 | 65 | 47 | 50 | 65 | 56 |
| random bot | 12 | 11 | 28 | 18 | 50 | 24 |

By message type (Table @tab:teacher), `lora_compact` makes the teacher's own decision on 87/95/94% of the held-out training states overall, far above the fixed rule (56%) and the random bot (24%). It does so on 95–100% of TRADING and REPLY states, and least often in FORCED (82–88%) and, for LFM2.5, in CONSIDERING (74%), although the teacher's rules there are as deterministic as in the other message types. Under the other prompts the same adapters make the teacher's decision on only 23–58% of these states, and the base models on 0–24%. A deterministic teacher is thus followed closely, but only in the format it was taught in.

## Limitations

The teacher is a fixed rule set, so competence here means making its decisions, not optimal play, and the teacher's own coins are the level the adapters are measured against. The three models belong to different families and differ in size, so differences between them cannot be attributed to any single factor. Each adapter was trained with one seed and one configuration, so the difference between Granite and the other two models may partly reflect training variation. With 30 games per player, the tournaments cannot rule out differences of about one coin per game. The game is simplified and short, about 9 turns per player.

# Conclusion

Within the prompt format it was trained on, a low-rank adapter makes a small language model follow its deterministic teacher closely: it makes the teacher's own decision on 87–95% of held-out states, and in play its coins do not differ significantly from the teacher's. Every adapter does significantly better in that format, but how much competence survives outside it depends on the model. Two of the three adapters then make the teacher's decision on only 12–32% of states, below a trivial fixed rule, while one keeps about half of them, yet under the verbose prompt none of them out-earns random play. Structural validity does not indicate decision quality: grammar-constrained base models are almost always well formed and mostly wrong. Evaluations of fine-tuned negotiation agents should therefore vary and report the prompt format together with the adapter, test more than one base model, and compare the agents with trivial baselines.

# Data availability {-}

{{data}}


# Acknowledgements {-}

[Grants and technical help to be added.]
