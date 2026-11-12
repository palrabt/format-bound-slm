"""State-serialization and helper functions shared by all three prompt strategies.

These build the compact state dicts that `compact.py` dumps verbatim as JSON
and that `llm.py`'s `_append_to_log_file` always logs, regardless of which
strategy actually produced the prompt — the log format must stay stable
since it feeds the training corpus and the eval metrics scripts.
"""

import json
import re
from pathlib import Path
from typing import Any

from .. import state as _state
from ..messages import Cards


def ip_to_index(ip: str) -> str:
    return _state.ip_to_index(ip, default="0")


def index_to_ip(index: str) -> str:
    if index == "0":
        return _state.CONFIG.get("player1_ip", "")
    if index == "1":
        return _state.CONFIG.get("player2_ip", "")
    return ""


def plant_state_obj(s: dict[str, Any]) -> dict[str, Any]:
    return {
        "phase": "PLANTING",
        "hand": s["hand"],
        "fields": {"field1": s["field1"], "field2": s["field2"], "field3": s["field3"]},
        "coins": s["coins"],
        "penalty": s["penalty"],
    }


def forced_state_obj(s: dict[str, Any]) -> dict[str, Any]:
    return {
        "phase": "FORCED",
        "new_cards": s["new_cards"],
        "fields": {"field1": s["field1"], "field2": s["field2"], "field3": s["field3"]},
        "coins": s["coins"],
        "penalty": s["penalty"],
    }


def offer_state_obj(
    s: dict[str, Any],
    other_fields: dict[str, dict[str, "Cards"]],
    previous_offers: "Cards",
    counter_offer: "Cards",
    reason: str,
) -> dict[str, Any]:
    return {
        "phase": "TRADING",
        "new_cards": s["new_cards"],
        "hand": s["hand"],
        "fields": {"field1": s["field1"], "field2": s["field2"], "field3": s["field3"]},
        "coins": s["coins"],
        "penalty": s["penalty"],
        "other_players": {ip_to_index(ip): types for ip, types in other_fields.items()},
        "previous_offers": previous_offers,
        "counter_offer": counter_offer,
        "reason": reason,
    }


def recv_offer_state_obj(s: dict[str, Any], card: "Cards", from_ip: str, reason: str) -> dict[str, Any]:
    return {
        "phase": "REPLY",
        "offered_cards": card,
        "from_player": ip_to_index(from_ip),
        "asking_for": reason,
        "hand": s["hand"],
        "fields": {"field1": s["field1"], "field2": s["field2"], "field3": s["field3"]},
        "penalty": s["penalty"],
    }


def considering_state_obj(
    s: dict[str, Any],
    my_offers: "Cards",
    my_reason: str,
    their_offers: "Cards",
    their_reason: str,
    their_fields: dict[str, "Cards"],
    from_ip: str,
) -> dict[str, Any]:
    return {
        "phase": "CONSIDERING",
        "my_offers": my_offers,
        "my_reason": my_reason,
        "their_offers": their_offers,
        "their_reason": their_reason,
        "from_player": ip_to_index(from_ip),
        "hand": s["hand"],
        "new_cards": s["new_cards"],
        "my_fields": {"field1": s["field1"], "field2": s["field2"], "field3": s["field3"]},
        "their_fields": their_fields,
        "penalty": s["penalty"],
    }


def extract_json(response: str) -> str | None:
    """Extract the first JSON object from a free-text LLM response."""
    match = re.search(r'\{[^}]+\}', response, re.DOTALL)
    if match:
        candidate = match.group()
        try:
            json.loads(candidate)
            return candidate
        except json.JSONDecodeError:
            pass
    return None


# The free text of an answer — TRADING's `ask`, REPLY's and CONSIDERING's `reason` — is the message
# the other player receives (actions.py passes it on). Every prompt style describes it in the output
# schema's own words, so none asks for a justification instead.
_SCHEMAS = Path(__file__).resolve().parents[2] / "schemas" / "output"
MESSAGE_FIELD = {"TRADING": "ask", "REPLY": "reason", "CONSIDERING": "reason"}


def message_rule(phase: str) -> str:
    """"'reason' is your message to the other player: One short sentence to ...", from the schema."""
    schema = json.loads((_SCHEMAS / f"{phase.lower()}.schema.json").read_text())
    props = schema["anyOf"][0]["properties"] if "anyOf" in schema else schema["properties"]
    key = MESSAGE_FIELD[phase]
    return f"'{key}' is your message to the other player, who reads it. {props[key]['description']}"


def format_fields_block(s: dict[str, Any], indent: str = "") -> str:
    """Human-readable field1/field2/field3 dump, shared by verbose.py and grammar.py."""
    return "\n".join(
        f"{indent}{name}: {s[name]['cards'] or 'empty'} (value {s[name]['value']})"
        for name in ("field1", "field2", "field3")
    )


def format_others_block(other_fields: dict[str, dict[str, Any]]) -> str:
    """Human-readable per-peer field dump, shared by verbose.py and grammar.py."""
    lines = [
        f"  {ip}: " + " ".join(f"{k} {field['cards'] or []} (value {field['value']})" for k, field in types.items())
        for ip, types in other_fields.items()
    ]
    return "\n".join(lines) if lines else "  (none)"
