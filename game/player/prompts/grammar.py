"""Grammar-constrained prompt strategy.

Pairs a short prompt with a GBNF grammar attached to the llamacpp request
body's "grammar" field of the /v1/chat/completions endpoint — llama-server masks
the sampled token distribution at every step so only grammar-legal
continuations are possible.

A generic grammar only guarantees *shape* (valid JSON, valid card names) —
not semantic correctness. That gap is real: an early smoke test showed
tinyllama, told in prose "plant hand[0], hand[1] is optional", instead
planting its *entire* hand across the three fields every time. Since
temperature=0.0 is fully greedy, every retry reproduced the identical wrong
answer, so PlantingAction.is_valid()'s downstream check could never pass —
the player's hand only grew turn after turn and the game ran out the clock.

For planting/forced-planting specifically, the set of valid answers is small
and fully enumerable at prompt-build time (see PlantingAction.is_valid() /
NewCardPlantingAction.is_valid() in messages.py), so build_planting_prompt
and build_forced_prompt construct a per-call grammar whose only alternatives
*are* the valid placements — turning "shape guaranteed" into "shape and
correctness guaranteed" for these two phases. Offer/reply/considering keep a
shape-only grammar (their valid-answer space includes a free-text reason and
isn't practically enumerable).

ws/string productions are copied from llama.cpp's own reference
grammars/json.gbnf rather than hand-derived, to avoid subtly wrong escaping.
"""

import json
from itertools import product
from typing import Any

from ..messages import VALID_CARDS, Cards
from . import common
from .spec import PromptSpec

SYSTEM_PROMPT = (
    "You are a Bohnanza decision engine. Respond with the JSON object the "
    "grammar requires — choose values that make good Bohnanza strategic "
    "sense."
)

STRATEGY_BRIEF = (
    "Bohnanza: each of your 3 fields holds one bean type. Harvesting a field "
    "earns coins — more beans of one type harvested together pays more per "
    "card. Rare beans (Fire, Garden, Broad, Red, Black-eyed) pay off in "
    "small stacks; common beans (Coffee, Wax, Blue, Chili, Runner, Soy) need "
    "bigger stacks to be worth harvesting."
)

# ── GBNF fragments ──────────────────────────────────────────────────────────────
# ws/string productions copied from llama.cpp/grammars/json.gbnf. Convention
# (per that file): ws is applied *after* literal tokens, not before.

_WS = r'''ws ::= | " " | "\n" [ \t]{0,20}'''

_STRING = r'''string ::=
  "\"" (
    [^"\\\x7F\x00-\x1F] |
    "\\" (["\\bfnrt] | "u" [0-9a-fA-F]{4}) # escapes
  )* "\"" ws'''

_CARD_ALT = " | ".join(f'"\\"{c}\\""' for c in sorted(VALID_CARDS))
_CARD = f'card ::= ({_CARD_ALT}) ws'
_CARD_LIST = 'card-list ::= "[" ws ( card ("," ws card)* )? "]" ws'
_BOOL = 'bool ::= ("true" | "false") ws'

FIELD_ASSIGNMENT_GRAMMAR = "\n".join([
    'root ::= "{" ws "\\"field1\\":" ws card-list "," ws "\\"field2\\":" ws card-list '
    '"," ws "\\"field3\\":" ws card-list "}" ws',
    _CARD, _CARD_LIST, _WS,
])
# Fallback only — used when a planting/forced-planting call falls outside the
# enumerable case below (empty hand; more new_cards than _MAX_ENUMERATED_NEW_CARDS).

_FIELDS = ("field1", "field2", "field3")
_MAX_ENUMERATED_NEW_CARDS = 4   # 3**4 = 81 alternatives; keeps the grammar small


def _gbnf_literal(text: str) -> str:
    """A GBNF string-literal token that matches `text` verbatim."""
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _enumerated_grammar(placements: list[dict[str, list[str]]]) -> str:
    """A grammar whose only legal outputs are the given field-assignment dicts,
    rendered in the same compact style _append_to_log_file/training data use."""
    alts = [_gbnf_literal(json.dumps(p, separators=(", ", ": "))) for p in placements]
    return "\n".join([f'root ::= ({" | ".join(alts)}) ws', _WS])


def _planting_placements(card0: str, card1: str) -> list[dict[str, list[str]]]:
    """Every field-assignment PlantingAction.is_valid() accepts: card0 alone
    in one field, or — if hand[1] exists — card0 and card1 each independently
    placed (possibly in the same field) — messages.py:PlantingAction.is_valid()
    requires exactly {card0} or exactly {card0, card1} planted, nothing else."""
    placements = [{name: ([card0] if name == f else []) for name in _FIELDS} for f in _FIELDS]
    if card1:
        for f0, f1 in product(_FIELDS, repeat=2):
            d = {name: [] for name in _FIELDS}
            d[f0] = d[f0] + [card0]
            d[f1] = d[f1] + [card1]
            placements.append(d)
    return placements


def _planting_grammar(card0: str, card1: str) -> str:
    if not card0:
        return FIELD_ASSIGNMENT_GRAMMAR   # defensive fallback: hand was empty
    return _enumerated_grammar(_planting_placements(card0, card1))


def _forced_placements(new_cards: list[str]) -> list[dict[str, list[str]]]:
    """Every field-assignment NewCardPlantingAction.is_valid() accepts: each
    new card independently placed in one of the 3 fields (order within a
    field doesn't affect the Counter-based validity check)."""
    placements = []
    for field_choices in product(_FIELDS, repeat=len(new_cards)):
        d = {name: [] for name in _FIELDS}
        for card, field in zip(new_cards, field_choices):
            d[field] = d[field] + [card]
        placements.append(d)
    return placements


def _forced_grammar(new_cards: list[str]) -> str:
    if not new_cards or len(new_cards) > _MAX_ENUMERATED_NEW_CARDS:
        return FIELD_ASSIGNMENT_GRAMMAR   # defensive fallback: unexpectedly many new_cards
    return _enumerated_grammar(_forced_placements(new_cards))

REPLY_GRAMMAR = "\n".join([
    'root ::= "{" ws "\\"accepted\\":" ws bool "," ws "\\"offer\\":" ws card-list '
    '"," ws "\\"reason\\":" ws string "}" ws',
    _BOOL, _CARD, _CARD_LIST, _STRING, _WS,
])


def _offer_grammar(candidates: list[str]) -> str:
    """`to` is closed to the actual peer addresses available for *this*
    offer, not left as a free Address string — game/player/actions.py:253
    treats an offer.to that isn't exactly player1_ip/player2_ip as a hard,
    non-retryable failure (+1 penalty, trading aborted for the turn), and a
    free-text `to` that is merely IP/URL-*shaped* would pass TradeOffer's
    own validation but still hit that failure. offered_cards stays the
    static 11-card enum since it IS re-validated downstream as a subset
    check (actions.py:258)."""
    to_alt = " | ".join(f'"\\"{addr}\\""' for addr in candidates) or '"\\"\\""'
    to_value = f'to-value ::= ({to_alt}) ws'
    return "\n".join([
        'root ::= ("null" ws) | offer',
        'offer ::= "{" ws "\\"offered_cards\\":" ws card-list "," ws "\\"to\\":" ws to-value '
        '"," ws "\\"ask\\":" ws string "}" ws',
        to_value, _CARD, _CARD_LIST, _STRING, _WS,
    ])


# ── Prompt builders ────────────────────────────────────────────────────────────

def build_planting_prompt(s: dict[str, Any]) -> PromptSpec:
    hand = s["hand"]
    card0 = hand[0] if hand else ""
    card1 = hand[1] if len(hand) > 1 else ""
    task = f"Plant hand[0]='{card0}' this turn"
    task += f"; hand[1]='{card1}' is optional.\n" if card1 else " (it is your only card).\n"
    text = (
        f"{STRATEGY_BRIEF}\n\n"
        "[STATE]\n"
        f"hand: {hand}\n"
        f"{common.format_fields_block(s)}\n"
        f"coins: {s['coins']}  penalty: {s['penalty']}\n\n"
        f"[TASK] {task}"
        "Harvest a field first if you want to clear it before planting into it.\n\n"
        "Choose which field gets which card(s)."
    )
    return PromptSpec(text=text, system_prompt=SYSTEM_PROMPT, grammar=_planting_grammar(card0, card1))


def build_forced_prompt(s: dict[str, Any]) -> PromptSpec:
    new = s["new_cards"]
    text = (
        f"{STRATEGY_BRIEF}\n\n"
        "[STATE]\n"
        f"new_cards: {new}\n"
        f"{common.format_fields_block(s)}\n"
        f"coins: {s['coins']}  penalty: {s['penalty']}\n\n"
        "[TASK] ALL cards in new_cards must be planted this turn — none can "
        "be skipped; multiple new cards may go to the same field. Every "
        "card in new_cards must appear exactly once across the three "
        "fields.\n\n"
        "Choose which field gets which card(s)."
    )
    return PromptSpec(text=text, system_prompt=SYSTEM_PROMPT, grammar=_forced_grammar(new))


def build_offer_prompt(
    s: dict[str, Any],
    other_fields: dict[str, dict[str, Cards]],
    previous_offers: Cards,
    counter_offer: Cards,
    reason: str,
) -> PromptSpec:
    candidates = list(other_fields.keys())
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
        f"Don't repeat an offer already in previous_offers.\n\n"
        f"Choose the offer (or null). {common.message_rule('TRADING')}"
    )
    return PromptSpec(text=text, system_prompt=SYSTEM_PROMPT, grammar=_offer_grammar(candidates))


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
        f"Choose accepted/offer/reason. {common.message_rule('REPLY')}"
    )
    return PromptSpec(text=text, system_prompt=SYSTEM_PROMPT, grammar=REPLY_GRAMMAR)


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
        f"Choose accepted/offer/reason. {common.message_rule('CONSIDERING')}"
    )
    return PromptSpec(text=text, system_prompt=SYSTEM_PROMPT, grammar=REPLY_GRAMMAR)
