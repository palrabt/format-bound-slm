"""Original (pre-redesign) verbose prompt strategy, kept for A/B comparison.

This is the verbose prompt exactly as it existed before the "verbose"
strategy's redesign earlier this session: the full ~32-line _STRATEGY
preamble (game structure + complete beanometer table) prepended to every
phase, each phase spelling out separate [RULES]/[CONSTRAINTS]/[RESPONSE
FORMAT] sections rather than the redesigned strategy's short brief +
[STATE]/[TASK]/[ANSWER FORMAT]. No system_prompt (old configs never set
llm.system_prompt, so none was ever actually sent) and no grammar.

Why this exists: comparing the currently-published paper tables (generated
from pre-session runs, which used this exact prompt) against the latest
post-fix run showed LoRA+Verbose/TinyLlama got WORSE under the redesigned
"verbose" strategy (75.8% -> 92.0% malformed) even though the redesign
helped every other Base/LoRA+Verbose cell. Registered as "verbose2" in
prompts/__init__.py (opt-in only, like "grammar" — never auto-selected) so
a condition can pin a player to this exact prompt and isolate whether the
redesign itself is the cause.

Changed since (2026-10-06): the message fields (`ask`, `reason`) are described in the output
schema's words (common.message_rule) — a message to the other player — instead of "explain your
decision", which had base models write analyses of their own position into the message.
"""

import json
from typing import Any

from ..messages import Cards
from . import common
from .spec import PromptSpec

_STRATEGY = """
You are an expert Bohnanza player. Bohnanza is a bean-planting card game where you earn
coins by harvesting full fields of matching beans. Here is how to play optimally:

══ GAME STRUCTURE ══════════════════════════════════════════════════════════════════════
Each turn has four phases in order:
  1. PLANTING   — plant or harvest from hand, then 2 new_cards are drawn (face-up for trading)
  2. TRADING    — trade new_cards or hand cards with other players (up to 3 negotiation rounds)
  3. FORCED PLANT — all new_cards must be planted; harvest a field first if no space exists
  4. CLOSING    — 3 more cards are dealt to your hand; the turn ends

══ FIELDS ══════════════════════════════════════════════════════════════════════════════
You have 3 fields. Each field can only hold ONE type of bean.
You may harvest a field at any time to earn coins and free up space.

══ THE BEANOMETER (coins earned per field) ══════════════════════════════════════════════
The beanometer lists how many beans of that type you need to earn 1, 2, 3, 4 coins.
Rarer beans (smaller deck count) earn coins with fewer cards.

  Bean             Count  1c   2c   3c   4c
  Coffee Bean        24    4    7   10   12   ← common, needs many to earn well
  Wax Bean           22    4    7    9   11
  Blue Bean          20    4    6    8   10
  Chili Bean         18    3    6    8    9
  Runner Bean        16    3    5    7    8
  Soy Bean           12    2    4    6    7
  Black-eyed Bean    10    2    4    5    6
  Red Bean            8    2    3    4    5
  Fire Bean           8    2    3    4    5
  Garden Bean         6    2    3    –    –   ← max 2 coins
  Broad Bean          6    1    2    3    4   ← always earns at least 1 coin

"""


def build_planting_prompt(s: dict[str, Any]) -> PromptSpec:
    hand = s["hand"]
    card0 = hand[0] if hand else ""
    card1 = hand[1] if len(hand) > 1 else ""
    prompt = (
        f"{_STRATEGY}\n\n"
        "[PLANTING PHASE]\n"
        f"  hand    : {hand}\n"
        f"  field1  : {s['field1']['cards'] or 'empty'} (value: {s['field1']['value']})\n"
        f"  field2  : {s['field2']['cards'] or 'empty'} (value: {s['field2']['value']})\n"
        f"  field3  : {s['field3']['cards'] or 'empty'} (value: {s['field3']['value']})\n"
        f"  coins   : {s['coins']}\n"
        f"  penalty : {s['penalty']}\n\n"
        "[RULES]\n"
        "- Each field holds ONE bean type only.\n"
        f"- hand[0] = '{card0}' MUST be planted this turn.\n"
    )
    if card1:
        prompt += f"- hand[1] = '{card1}' may optionally also be planted.\n"
    prompt += (
        "- You may harvest a field first to clear it, then plant into it in the same turn.\n"
        "- Harvesting earns coins: more beans in the field = more coins.\n\n"
        "[CONSTRAINTS]\n"
        "- Use the exact card names shown in 'hand'.\n"
        f"- '{card0}' must appear exactly once across ALL fields.\n"
    )
    if card1:
        prompt += f"- '{card1}' may appear at most once across ALL fields.\n"
    prompt += (
        "- If a card is placed into a field with a non-matching bean type, that field is harvested first.\n"
        "- An empty list [] means no card is planted into that field.\n\n"
        "[RESPONSE FORMAT]\n"
        "Reply with ONLY a JSON object. No explanation, no markdown, no extra keys.\n"
        "Each field maps to a list of card names to plant there.\n\n"
        "Examples:\n"
        f'  Plant only hand[0] into field1:\n'
        f'    {{"field1": ["{card0}"], "field2": [], "field3": []}}\n\n'
    )
    if card1:
        prompt += (
            f'  Plant hand[0] into field2, hand[1] into field3:\n'
            f'    {{"field1": [], "field2": ["{card0}"], "field3": ["{card1}"]}}\n\n'
            f'  Plant both cards into field1:\n'
            f'    {{"field1": ["{card0}", "{card1}"], "field2": [], "field3": []}}\n\n'
        )
    prompt += "Your answer:\n"
    return PromptSpec(text=prompt)


def build_forced_prompt(s: dict[str, Any]) -> PromptSpec:
    new = s["new_cards"]
    prompt = (
        f"{_STRATEGY}\n\n"
        "[FORCED PLANTING PHASE]\n"
        f"  new_cards : {new}\n"
        f"  field1    : {s['field1']['cards'] or 'empty'} (value: {s['field1']['value']})\n"
        f"  field2    : {s['field2']['cards'] or 'empty'} (value: {s['field2']['value']})\n"
        f"  field3    : {s['field3']['cards'] or 'empty'} (value: {s['field3']['value']})\n"
        f"  coins     : {s['coins']}\n"
        f"  penalty   : {s['penalty']}\n\n"

        "[RULES]\n"
        "- Each field holds ONE bean type only.\n"
        "- ALL cards in new_cards must be planted this turn — none can be skipped.\n"
        "- You may assign multiple new cards to the same field.\n"
        "- If a card does not match the bean type already in a field, that field is\n"
        "  automatically harvested first, then the card is planted there.\n"
        "- Prefer planting into fields that already match the bean type to avoid\n"
        "  unwanted harvests. Only force a harvest if it earns good coins.\n\n"

        "[CONSTRAINTS]\n"
        "- Use the exact card names from new_cards.\n"
        "- Each field gets a list of card names to plant there, or [] if none.\n"
        "- You MUST assign ALL cards from new_cards exactly once.\n"
        f"- Use ONLY these card names: {new}\n\n"

        "[RESPONSE FORMAT]\n"
        "Reply with ONLY a JSON object. No explanation, no markdown, no extra keys.\n"
    )
    if len(new) >= 2:
        prompt += (
            f"Examples (new_cards = {new}):\n"
            f'  Plant all into field1:\n'
            f'    {{"field1": {json.dumps(new)}, "field2": [], "field3": []}}\n\n'
            f'  Split across fields:\n'
            f'    {{"field1": {json.dumps([new[0]])}, "field2": {json.dumps([new[1]])}, "field3": []}}\n\n'
            "Not good answers:\n"
            f'  {{"field1": [], "field2": [], "field3": []}}\n\n'
            f'  {{"field1": {json.dumps([new[0]])}, "field2": [], "field3": []}}\n\n'
        )
    elif new:
        prompt += (
            f"Example:\n"
            f'  Plant into field1:\n'
            f'    {{"field1": {json.dumps(new)}, "field2": [], "field3": []}}\n\n'
        )
    prompt += "Your answer:\n"
    return PromptSpec(text=prompt)


def build_offer_prompt(
    s: dict[str, Any],
    other_fields: dict[str, dict[str, Cards]],
    previous_offers: Cards,
    counter_offer: Cards,
    reason: str,
) -> PromptSpec:
    others = ""
    for ip, types in other_fields.items():
        others += f" {ip}: "
        for k, field in types.items():
            cards = field["cards"]
            others += f"{k} [{', '.join(cards)}] (value: {field['value']}) " if cards else f"{k} [] "

    prompt = (
        f"{_STRATEGY}\n\n"
        "[INITIAL OFFER]\n"
        f"  new_cards       : {s['new_cards']}\n"
        f"  hand            : {s['hand']}\n"
        f"  field1          : {s['field1']['cards'] or 'empty'} (value: {s['field1']['value']})\n"
        f"  field2          : {s['field2']['cards'] or 'empty'} (value: {s['field2']['value']})\n"
        f"  field3          : {s['field3']['cards'] or 'empty'} (value: {s['field3']['value']})\n"
        f"  coins           : {s['coins']}\n"
        f"  penalty         : {s['penalty']}\n"
        f"  previous_offers : {previous_offers or 'none'}\n"
        f"  counter_offer   : {counter_offer or 'none'}\n\n"

        "[OTHER PLAYERS]\n"
        f"{others}\n\n"

        "[RULES]\n"
        "- You make exactly ONE offer to ONE player, or no offer at all.\n"
        "- You may offer cards from new_cards, hand, or both.\n"
        "- A good trade gives away beans that don't fit your fields and gets back\n"
        "  beans that match your existing fields or help build a new one.\n"
        "- Check other players' fields — offer them beans they are already growing.\n"
        "- Do NOT repeat an offer that appears in previous_offers.\n"
        "- If a counter_offer exists, respond to it: accept, modify, or decline.\n"
        "- Reply with null if no worthwhile trade exists.\n\n"

        f"[OFFER REJECTED REASON]\n  {reason}\n\n"

        "[CONSTRAINTS]\n"
        f"- IMPORTANT: You may ONLY offer cards from this exact list (these are ALL the cards you have): {s['hand'] + s['new_cards']}\n"
        "- No card can appear more times in 'offered_cards' than it appears in that list.\n"
        f"- 'to' must be exactly one of: {list(other_fields.keys())}.\n"
        f"- {common.message_rule('TRADING')}\n"
        "- 'offered_cards' MUST NOT include cards that you need for your own fields.\n"
        "- 'offered_cards' MUST NOT include cards that are already planted in your fields.\n\n"

        "[RESPONSE FORMAT]\n"
        "Reply with ONLY a JSON object. No explanation, no markdown, no extra keys.\n"
        "The offer has exactly these keys: offered_cards, to, ask.\n\n"
        f"Examples:\n"
        f'  Offer from new_cards only:\n'
        f'    {{"offered_cards": ["{s["new_cards"][0] if s["new_cards"] else ""}"], "to": "{list(other_fields.keys())[0] if other_fields else "player_ip"}", "ask": "I need wax beans."}}\n\n'
        f'  Offer from hand only:\n'
        f'    {{"offered_cards": ["{s["hand"][0] if s["hand"] else ""}"], "to": "{list(other_fields.keys())[0] if other_fields else "player_ip"}", "ask": "I need blue beans."}}\n\n'
        f'  Offer from both hand and new_cards:\n'
        f'    {{"offered_cards": ["{s["new_cards"][0] if s["new_cards"] else ""}", "{s["hand"][0] if s["hand"] else ""}"], "to": "{list(other_fields.keys())[0] if other_fields else "player_ip"}", "ask": "I need coffee beans."}}\n\n'
        '  No good trade:\n'
        '    null\n\n'
        "Your answer:\n"
    )
    return PromptSpec(text=prompt)


def build_reply_prompt(s: dict[str, Any], card: Cards, from_ip: str, reason: str = "") -> PromptSpec:
    prompt = (
        f"{_STRATEGY}\n\n"
        "[FIRST RESPONSE]\n"
        f"  offered_cards   : {card}\n"
        f"  from_player     : {from_ip}\n"
        f"  asking_for      : {reason or 'none'}\n"
        f"  hand            : {s['hand']}\n"
        f"  field1          : {s['field1']['cards'] or 'empty'} (value: {s['field1']['value']})\n"
        f"  field2          : {s['field2']['cards'] or 'empty'} (value: {s['field2']['value']})\n"
        f"  field3          : {s['field3']['cards'] or 'empty'} (value: {s['field3']['value']})\n"
        f"  penalty         : {s['penalty']}\n\n"

        "[RULES]\n"
        "- Read 'asking_for' carefully — it may request specific cards from you or try to convince you\n"
        "  what the other player needs. Use this to craft a better counter-offer.\n"
        "- Consider if the offered cards match a bean type you are already growing\n"
        "  or help start a valuable new field.\n"
        "- Reject if the offered cards don't fit any of your fields and would force\n"
        "  an unwanted harvest when planted.\n"
        "- To swap, accept and put in 'offer' the cards from your hand you give\n"
        "  in return; the other player then confirms the trade.\n"
        "- To take the offered cards and give nothing back, accept with 'offer': [].\n"
        "- If you reject, you may still put in 'offer' cards you could give instead\n"
        "  (a counter-offer); nothing is exchanged, but they may make a new offer.\n"
        "- If 'asking_for' asks for a specific card and you have it, consider\n"
        "  including it in your 'offer' to make the deal more attractive.\n"
        "- Cards in 'offer' must exist in your actual hand.\n"
        f"- {common.message_rule('REPLY')} You may ask for specific cards\n"
        "  (e.g. 'Could you give me a Wax Bean instead?').\n\n"

        "[CONSTRAINTS]\n"
        f"- 'accepted' must be present - must be a boolean value\n"
        f"- 'offer' must be present - either [] or a list of cards of these types {s['hand']}. Use [] to give nothing.\n"
        "- 'offer' MUST NOT be the cards that you need\n"
        "- 'offer' MUST NOT be the cards that are in your fields\n"
        "- 'reason' must always be present — one or two sentences max.\n\n"

        "[RESPONSE FORMAT]\n"
        "Reply with ONLY a JSON object. No explanation, no markdown, no extra keys.\n\n"
        "Examples:\n"
        "  Accepting as offered, giving nothing back\n"
        '    {"accepted": true, "offer": [], "reason": "Chili beans fit my field1 perfectly, happy to help."}\n\n'
        "  Accepting and giving a card in return (a swap)\n"
        '    {"accepted": true, "offer": ["Soy Bean"], "reason": "Chili beans fit my field1 — you can have my soy bean."}\n\n'
        "  Countering with an explanation and a request:\n"
        '    {"accepted": false, "offer": ["Wax Bean"], "reason": "I have the wax bean you need — can you give me a red bean instead?"}\n\n'
        "  Bargaining\n"
        '    {"accepted": false, "offer": ["Coffee Bean", "Coffee Bean"], "reason": "I can offer two coffee beans if you give me an extra wax bean."}\n\n'
        "  Not interested in trading\n"
        '    {"accepted": false, "offer": [], "reason": "Sorry not interested"}\n\n'
        "Your answer:\n"
    )
    return PromptSpec(text=prompt)


def build_considering_prompt(
    s: dict[str, Any],
    my_offers: Cards,
    my_reason: str,
    their_offers: Cards,
    their_reason: str,
    their_fields: dict[str, Cards],
    from_ip: str,
) -> PromptSpec:
    prompt = (
        f"{_STRATEGY}\n\n"
        "[CONSIDERING PHASE]\n"
        f"  my_offers           : {my_offers}\n"
        f"  my_reason           : {my_reason}\n"
        f"  their_offers        : {their_offers}\n"
        f"  their_reason        : {their_reason}\n"
        f"  from_player         : {from_ip}\n"
        f"  hand                : {s['hand']}\n"
        f"  new_cards           : {s['new_cards']}\n"
        f"  my_field1           : {s['field1']['cards'] or 'empty'} (value: {s['field1']['value']})\n"
        f"  my_field2           : {s['field2']['cards'] or 'empty'} (value: {s['field2']['value']})\n"
        f"  my_field3           : {s['field3']['cards'] or 'empty'} (value: {s['field3']['value']})\n"
        f"  penalty             : {s['penalty']}\n\n"
        f"  their_field1        : {their_fields.get('field1', {}).get('cards') or 'empty'} (value: {their_fields.get('field1', {}).get('value', 0)})\n"
        f"  their_field2        : {their_fields.get('field2', {}).get('cards') or 'empty'} (value: {their_fields.get('field2', {}).get('value', 0)})\n"
        f"  their_field3        : {their_fields.get('field3', {}).get('cards') or 'empty'} (value: {their_fields.get('field3', {}).get('value', 0)})\n\n"

        "[RULES]\n"
        "- Read 'asking_for' carefully — it may request specific cards from you or try to convince you\n"
        "  what the other player needs. Use this to craft a better counter-offer.\n"
        "- Consider if the offered cards match a bean type you are already growing\n"
        "  or help start a valuable new field.\n"
        "- Reject if the offered cards don't fit any of your fields and would force\n"
        "  an unwanted harvest when planted.\n"
        "- You may propose a counter-offer: different cards from your hand that\n"
        "  you are willing to give in exchange for the offered cards.\n"
        "- If 'asking_for' asks for a specific card and you have it, consider\n"
        "  including it in your counter-offer to make the deal more attractive.\n"
        "- Counter-offer cards must exist in your actual hand.\n"
        f"- {common.message_rule('CONSIDERING')} You may ask for specific cards\n"
        "  (e.g. 'Could you give me a Wax Bean instead?').\n\n"

        "[CONSTRAINTS]\n"
        f"- 'accepted' must be present - must be a boolean value\n"
        "- if 'accepted' is true, 'offer' must be [].\n"
        f"- 'offer' must be present - either [] or a list of cards of these types {set(s['hand'] + s['new_cards'])}. Use [] to simply decline.\n"
        "- 'reason' must always be present — one or two sentences max.\n\n"

        "[RESPONSE FORMAT]\n"
        "Reply with ONLY a JSON object. No explanation, no markdown, no extra keys.\n\n"
        "Examples:\n"
        "  Accepting offer as-is, with an explanation\n"
        '    {"accepted": true, "offer": [], "reason": "Chili beans fit my field1 perfectly, happy to help."}\n\n'
        "  Rejecting offer, without new offer:\n"
        '    {"accepted": false, "offer": [], "reason": "I can only offer what I have. Do you have any other cards?"}\n\n'
        "  Rejecting offer, with new offer for orginal offering:\n"
        '    {"accepted": false, "offer": ["Wax Bean", "Stink Bean"], "reason": "I can give these instead."}\n\n'
        "  Rejecting offer, with new offer, with asking for specific cards:\n"
        '    {"accepted": false, "offer": ["Wax Bean", "Stink Bean"], "reason": "I can give these instead. If you have any other cards, I\'m open to trading."}\n\n'
        "Your answer:\n"
    )
    return PromptSpec(text=prompt)
