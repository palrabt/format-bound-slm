"""Redesigned verbose prompt strategy for base / non-fine-tuned models.

Replaces the old ~50-70-line-per-call prompt (30-line strategy preamble +
state + RULES + CONSTRAINTS + RESPONSE FORMAT, response format far from the
"answer now" cue) with a short brief + state + a handful of task bullets +
the answer format/example placed immediately before "Answer:". Also carries
a SYSTEM_PROMPT reinforcing "JSON only, never repeat this prompt" — unused by
every prior strategy since no config ever set llm.system_prompt.

This directly targets the observed failure in logs/no_lora/Alpha/game_0002.log,
where a base TinyLlama-1.1B given the old prompt echoed the [PLANTING PHASE]
state block or paraphrased the strategy preamble instead of answering in JSON.
"""

import json
from typing import Any

from ..messages import Cards
from . import common
from .spec import PromptSpec

SYSTEM_PROMPT = (
    "You are a Bohnanza decision engine. You output exactly one JSON object "
    "per turn and nothing else — no explanations, no markdown, no repeating "
    "this prompt. If unsure, make your best guess but still answer with "
    "valid JSON only."
)

STRATEGY_BRIEF = (
    "Bohnanza: each of your 3 fields holds one bean type. Harvesting a field "
    "earns coins — more beans of one type harvested together pays more per "
    "card. Rare beans (Fire, Garden, Broad, Red, Black-eyed) pay off in "
    "small stacks; common beans (Coffee, Wax, Blue, Chili, Runner, Soy) need "
    "bigger stacks to be worth harvesting."
)


def build_planting_prompt(s: dict[str, Any]) -> PromptSpec:
    hand = s["hand"]
    card0 = hand[0] if hand else ""
    card1 = hand[1] if len(hand) > 1 else ""
    task = f"hand[0]='{card0}' MUST be planted this turn"
    task += f"; hand[1]='{card1}' MAY optionally also be planted.\n" if card1 else " (it is your only card).\n"
    only_clause = (
        f'ONLY "{card0}" and "{card1}" may appear in your answer — nowhere else in hand '
        "is eligible this turn, even if hand has more cards.\n"
        if card1 else
        f'ONLY "{card0}" may appear in your answer — nowhere else in hand is eligible this turn, '
        "even if hand has more cards.\n"
    )
    text = (
        f"{STRATEGY_BRIEF}\n\n"
        "[STATE]\n"
        f"hand: {hand}\n"
        f"{common.format_fields_block(s)}\n"
        f"coins: {s['coins']}  penalty: {s['penalty']}\n\n"
        f"[TASK] {task}"
        f"{only_clause}"
        "You may harvest a field first (earns coins), then plant into it. "
        "A field holds one bean type — planting a mismatched card harvests "
        "that field automatically first.\n\n"
        "[ANSWER FORMAT] Output ONLY this JSON object, nothing else:\n"
        '  {"field1": [...], "field2": [...], "field3": [...]}\n'
        f'Example — plant "{card0}" into field1:\n'
        f'  {{"field1": ["{card0}"], "field2": [], "field3": []}}\n\n'
        "Do not repeat this prompt. Do not explain your answer. JSON only.\n"
        "Answer:"
    )
    return PromptSpec(text=text, system_prompt=SYSTEM_PROMPT)


def build_forced_prompt(s: dict[str, Any]) -> PromptSpec:
    new = s["new_cards"]
    text = (
        f"{STRATEGY_BRIEF}\n\n"
        "[STATE]\n"
        f"new_cards: {new}\n"
        f"{common.format_fields_block(s)}\n"
        f"coins: {s['coins']}  penalty: {s['penalty']}\n\n"
        "[TASK] ALL cards in new_cards must be planted this turn — none can "
        "be skipped. Multiple new cards may go to the same field. A field "
        "holds one bean type — planting a mismatched card harvests that "
        "field automatically first.\n\n"
        "[ANSWER FORMAT] Output ONLY this JSON object, nothing else:\n"
        '  {"field1": [...], "field2": [...], "field3": [...]}\n'
        f"Example — plant all of {new} into field1:\n"
        f'  {{"field1": {json.dumps(new)}, "field2": [], "field3": []}}\n\n'
        "Every card in new_cards must appear exactly once across the three "
        "lists. Do not repeat this prompt. Do not explain. JSON only.\n"
        "Answer:"
    )
    return PromptSpec(text=text, system_prompt=SYSTEM_PROMPT)


def build_offer_prompt(
    s: dict[str, Any],
    other_fields: dict[str, dict[str, Cards]],
    previous_offers: Cards,
    counter_offer: Cards,
    reason: str,
) -> PromptSpec:
    candidates = list(other_fields.keys())
    example_ip = candidates[0] if candidates else "player_ip"
    example_card = (s["new_cards"] or s["hand"] or [""])[0]
    text = (
        f"{STRATEGY_BRIEF}\n\n"
        "[STATE]\n"
        f"new_cards: {s['new_cards']}\n"
        f"hand: {s['hand']}\n"
        f"{common.format_fields_block(s)}\n"
        f"coins: {s['coins']}  penalty: {s['penalty']}\n"
        f"previous_offers: {previous_offers or 'none'}\n"
        f"counter_offer: {counter_offer or 'none'}\n"
        f"{'rejected_reason: ' + reason if reason else ''}\n"
        "[OTHER PLAYERS]\n"
        f"{common.format_others_block(other_fields)}\n\n"
        "[TASK] Offer cards from hand/new_cards to exactly one player whose "
        "fields they'd fit, or answer null if no worthwhile trade exists. "
        f"You may only offer from: {s['hand'] + s['new_cards']}. Don't "
        f"repeat an offer already in previous_offers. 'to' must be exactly "
        f"one of {candidates}.\n\n"
        "[ANSWER FORMAT] Output ONLY this JSON object (keys: offered_cards, "
        "to, ask), or exactly null if no good trade:\n"
        f'  {{"offered_cards": ["{example_card}"], "to": "{example_ip}", "ask": "<your message to that player>"}}\n'
        f"{common.message_rule('TRADING')}\n\n"
        "Do not repeat this prompt. Do not explain. JSON only.\n"
        "Answer:"
    )
    return PromptSpec(text=text, system_prompt=SYSTEM_PROMPT)


def build_reply_prompt(s: dict[str, Any], card: Cards, from_ip: str, reason: str) -> PromptSpec:
    text = (
        f"{STRATEGY_BRIEF}\n\n"
        "[STATE]\n"
        f"offered_cards: {card}\n"
        f"from_player: {from_ip}\n"
        f"asking_for: {reason or 'none'}\n"
        f"hand: {s['hand']}\n"
        f"{common.format_fields_block(s)}\n"
        f"penalty: {s['penalty']}\n\n"
        "[TASK] Accept the offered cards if they fit your fields; otherwise "
        "decline, or counter with cards from your own hand you're willing "
        "to trade instead. Counter-offer cards must be in hand, must not be "
        "cards you need, and must not already be planted.\n\n"
        "[ANSWER FORMAT] Output ONLY this JSON object (keys: accepted, "
        "offer, reason):\n"
        '  {"accepted": true|false, "offer": [...], "reason": "<your message to the other player>"}\n'
        f"{common.message_rule('REPLY')}\n"
        "Examples:\n"
        '  Accept:  {"accepted": true, "offer": [], "reason": "Deal, the Chili fits my field nicely."}\n'
        '  Counter: {"accepted": false, "offer": ["Wax Bean"], "reason": "Can you give a Red Bean instead?"}\n'
        '  Decline: {"accepted": false, "offer": [], "reason": "Not interested."}\n\n'
        "Do not repeat this prompt. Do not explain. JSON only.\n"
        "Answer:"
    )
    return PromptSpec(text=text, system_prompt=SYSTEM_PROMPT)


def build_considering_prompt(
    s: dict[str, Any],
    my_offers: Cards,
    my_reason: str,
    their_offers: Cards,
    their_reason: str,
    their_fields: dict[str, Cards],
    from_ip: str,
) -> PromptSpec:
    text = (
        f"{STRATEGY_BRIEF}\n\n"
        "[STATE]\n"
        f"my_offers: {my_offers}  my_reason: {my_reason}\n"
        f"their_offers: {their_offers}  their_reason: {their_reason}\n"
        f"from_player: {from_ip}\n"
        f"hand: {s['hand']}  new_cards: {s['new_cards']}\n"
        f"{common.format_fields_block(s)}\n"
        f"penalty: {s['penalty']}\n"
        f"their_field1: {their_fields.get('field1', {}).get('cards') or 'empty'} "
        f"(value {their_fields.get('field1', {}).get('value', 0)})\n"
        f"their_field2: {their_fields.get('field2', {}).get('cards') or 'empty'} "
        f"(value {their_fields.get('field2', {}).get('value', 0)})\n"
        f"their_field3: {their_fields.get('field3', {}).get('cards') or 'empty'} "
        f"(value {their_fields.get('field3', {}).get('value', 0)})\n\n"
        "[TASK] Decide whether to accept their_offers in exchange for "
        "my_offers. Accept if the trade is still good for you; otherwise "
        "decline or propose new cards from hand/new_cards instead.\n\n"
        "[ANSWER FORMAT] Output ONLY this JSON object (keys: accepted, "
        "offer, reason):\n"
        '  {"accepted": true|false, "offer": [...], "reason": "<your message to the other player>"}\n'
        f"{common.message_rule('CONSIDERING')}\n"
        "Examples:\n"
        '  Accept:  {"accepted": true, "offer": [], "reason": "Deal, the Chili fits my field nicely."}\n'
        '  Decline: {"accepted": false, "offer": [], "reason": "Only what I have — anything else?"}\n'
        '  Counter: {"accepted": false, "offer": ["Wax Bean"], "reason": "I can give this instead."}\n\n'
        "Do not repeat this prompt. Do not explain. JSON only.\n"
        "Answer:"
    )
    return PromptSpec(text=text, system_prompt=SYSTEM_PROMPT)
