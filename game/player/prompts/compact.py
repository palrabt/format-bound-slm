"""Compact prompt strategy — exactly the LoRA fine-tuning input.

One line of `json.dumps(state)`, with no strategy preamble, rules, examples or
"[JSON]" marker: train_adapters.py puts the corpus's state line, and nothing
else, into the user turn (the marker only separates state from answer in the
corpus file). The state objects (common.*_state_obj) list their keys in the
corpus's order, so an adapter sees here the very string it was trained on.
"""

import json
from typing import Any

from ..messages import Cards
from . import common
from .spec import PromptSpec


def _prompt(state_obj: dict[str, Any]) -> PromptSpec:
    return PromptSpec(text=json.dumps(state_obj, separators=(", ", ": ")))


def build_planting_prompt(s: dict[str, Any]) -> PromptSpec:
    return _prompt(common.plant_state_obj(s))


def build_forced_prompt(s: dict[str, Any]) -> PromptSpec:
    return _prompt(common.forced_state_obj(s))


def build_offer_prompt(
    s: dict[str, Any],
    other_fields: dict[str, dict[str, Cards]],
    previous_offers: Cards,
    counter_offer: Cards,
    reason: str,
) -> PromptSpec:
    return _prompt(common.offer_state_obj(s, other_fields, previous_offers, counter_offer, reason))


def build_reply_prompt(s: dict[str, Any], card: Cards, from_ip: str, reason: str) -> PromptSpec:
    return _prompt(common.recv_offer_state_obj(s, card, from_ip, reason))


def build_considering_prompt(
    s: dict[str, Any],
    my_offers: Cards,
    my_reason: str,
    their_offers: Cards,
    their_reason: str,
    their_fields: dict[str, Cards],
    from_ip: str,
) -> PromptSpec:
    return _prompt(
        common.considering_state_obj(s, my_offers, my_reason, their_offers, their_reason, their_fields, from_ip)
    )


def postprocess_offer_response(raw: str) -> str:
    """The compact format's other_players/`to` are index-keyed ("0"/"1"), not
    IP-keyed — only compact.py's prompt teaches the model to answer with an
    index, so only compact.py needs to translate it back to a real IP before
    TradeOffer.from_dict() validates it as an Address."""
    try:
        text = common.extract_json(raw) or raw
        data = json.loads(text)
        if "to" in data:
            data["to"] = common.index_to_ip(str(data["to"]))
        return json.dumps(data)
    except Exception:
        return raw
