"""Human player decision module — serves decisions via web UI instead of an LLM.

Every completed decision is appended to training_data.txt in the same compact
prompt/response format used by the existing LLM training pipeline.

Flow:
  1. A game action calls one of the public get_* functions.
  2. The function stores a pending decision dict and blocks on a threading.Event.
  3. The web UI polls GET /pending and renders the appropriate decision form.
  4. The human submits a choice via POST /submit.
  5. submit_response() stores the result, fires the event, and logs the example.
"""

import json
import os
import threading
from pathlib import Path
from typing import Any

from . import state as _state
from .messages import (
    Address, Cards,
    ConsideringReply, NewCardPlantingAction,
    OfferReply, PlantingAction, TradeOffer,
)

# ── Shared pending-decision state ─────────────────────────────────────────────

_lock    = threading.Lock()
_pending: dict | None = None
_response: dict | None = None
_event   = threading.Event()

DECISION_TIMEOUT  = 600   # seconds the human has to respond
TRAINING_DATA_PATH = Path("training/corpus/training_data.txt")


# ── Internal helpers ──────────────────────────────────────────────────────────

def _to_list(v: Any) -> list:
    if v is None:
        return []
    if isinstance(v, dict) and "cards" in v:
        return list(v["cards"])
    return list(v)


def _ip_to_index(ip: str) -> str:
    return _state.ip_to_index(ip)


def _fields_dict(s: dict) -> dict:
    return {
        "field1": s.get("field1", {}),
        "field2": s.get("field2", {}),
        "field3": s.get("field3", {}),
    }


def _append_training(state_obj: dict, response_obj: dict | None) -> None:
    """Write one prompt/response pair to training_data.txt."""
    try:
        prompt_line   = json.dumps(state_obj, separators=(", ", ": "))
        response_line = "null" if response_obj is None else json.dumps(response_obj, separators=(", ", ": "))
        with open(TRAINING_DATA_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n{prompt_line}\n[JSON] {response_line}\n")
        _state.debug(f"human: training example saved ({state_obj['phase']})")
    except Exception as e:
        _state.warn(f"human: failed to save training example: {e}")


def _request(decision_type: str, context: dict) -> dict:
    """Block until the web UI posts a response."""
    global _pending, _response
    with _lock:
        _pending  = {"type": decision_type, "context": context}
        _response = None
        _event.clear()

    timed_out = not _event.wait(timeout=DECISION_TIMEOUT)

    with _lock:
        result    = _response or {}
        _pending  = None
        _response = None

    if timed_out:
        _state.warn(f"human: decision timed out for {decision_type}")
    return result


# ── Public API (called by the player server) ──────────────────────────────────

def get_pending() -> dict | None:
    with _lock:
        return _pending


def submit_response(response: dict) -> bool:
    """Called by POST /submit.  Returns False if no decision is pending."""
    global _response
    with _lock:
        if _pending is None:
            return False
        _response = response
    _event.set()
    return True


# ── Decision functions (same signatures as llm.py) ────────────────────────────

def llm_log_path() -> str:
    identity = _state.CONFIG.get("identity") or _state.state.identity or "human"
    return os.path.join("logs", f"{identity}_human.log")


def get_planting_action(s: dict[str, Any]) -> PlantingAction:
    ctx = {
        "hand":    _to_list(s.get("hand")),
        "field1":  _to_list(s.get("field1")),
        "field2":  _to_list(s.get("field2")),
        "field3":  _to_list(s.get("field3")),
        "coins":   s.get("coins", 0),
        "penalty": s.get("penalty", 0),
    }
    result = _request("planting", ctx)
    try:
        action = PlantingAction.from_dict(result)
    except Exception:
        return PlantingAction()

    if action.is_valid(ctx["hand"]):
        _append_training(
            state_obj={
                "phase":   "PLANTING",
                "hand":    ctx["hand"],
                "fields":  _fields_dict(ctx),
                "coins":   ctx["coins"],
                "penalty": ctx["penalty"],
            },
            response_obj={
                "field1": list(action.field1),
                "field2": list(action.field2),
                "field3": list(action.field3),
            },
        )
    return action


def get_new_card_action(s: dict[str, Any]) -> NewCardPlantingAction:
    ctx = {
        "new_cards": _to_list(s.get("new_cards")),
        "field1":    _to_list(s.get("field1")),
        "field2":    _to_list(s.get("field2")),
        "field3":    _to_list(s.get("field3")),
        "coins":     s.get("coins", 0),
        "penalty":   s.get("penalty", 0),
    }
    result = _request("forced_planting", ctx)
    try:
        action = NewCardPlantingAction.from_dict(result)
    except Exception:
        return NewCardPlantingAction()

    if action.is_valid(ctx["new_cards"]):
        _append_training(
            state_obj={
                "phase":     "FORCED",
                "new_cards": ctx["new_cards"],
                "fields":    _fields_dict(ctx),
                "coins":     ctx["coins"],
                "penalty":   ctx["penalty"],
            },
            response_obj={
                "field1": list(action.field1),
                "field2": list(action.field2),
                "field3": list(action.field3),
            },
        )
    return action


def get_trade_offer(
    s: dict[str, Any],
    other_fields: dict[str, dict[str, Any]],
    previous_offers: Cards,
    in_return: Cards,
    reason: str,
) -> TradeOffer:
    serialised_others = {
        ip: {f: _to_list(v) for f, v in fields.items()}
        for ip, fields in other_fields.items()
    }
    ctx = {
        "hand":            _to_list(s.get("hand")),
        "new_cards":       _to_list(s.get("new_cards")),
        "field1":          _to_list(s.get("field1")),
        "field2":          _to_list(s.get("field2")),
        "field3":          _to_list(s.get("field3")),
        "coins":           s.get("coins", 0),
        "penalty":         s.get("penalty", 0),
        "other_fields":    serialised_others,
        "previous_offers": _to_list(previous_offers),
        "in_return":       _to_list(in_return),
        "reason":          reason,
    }
    result = _request("trade_offer", ctx)

    try:
        offer = TradeOffer(
            offered_cards=Cards(result.get("offered_cards", [])),
            to=Address(result.get("to", "")),
            ask=result.get("ask", ""),
        )
    except Exception:
        return TradeOffer()

    _append_training(
        state_obj={
            "phase":           "TRADING",
            "new_cards":       ctx["new_cards"],
            "hand":            ctx["hand"],
            "fields":          _fields_dict(ctx),
            "coins":           ctx["coins"],
            "penalty":         ctx["penalty"],
            "other_players":   {_ip_to_index(ip): {f: _to_list(v) for f, v in flds.items()}
                                for ip, flds in other_fields.items()},
            "previous_offers": ctx["previous_offers"],
            "counter_offer":   ctx["in_return"],
            "reason":          reason,
        },
        response_obj={
            "offered_cards": list(offer.offered_cards),
            "to":            _ip_to_index(str(offer.to)),
            "ask":           offer.ask,
        },
    )
    return offer


def get_REPLY(s: dict[str, Any], cards: Cards, from_ip: str, ask: str) -> OfferReply:
    ctx = {
        "hand":          _to_list(s.get("hand")),
        "field1":        _to_list(s.get("field1")),
        "field2":        _to_list(s.get("field2")),
        "field3":        _to_list(s.get("field3")),
        "coins":         s.get("coins", 0),
        "offered_cards": _to_list(cards),
        "from_ip":       from_ip,
        "ask":           ask,
    }
    result = _request("incoming_offer", ctx)
    try:
        reply = OfferReply(
            accepted=result.get("accepted", False),
            offer=result.get("offer", []),
            reason=result.get("reason", ""),
        )
    except Exception:
        return OfferReply()

    _append_training(
        state_obj={
            "phase":         "REPLY",
            "offered_cards": ctx["offered_cards"],
            "from_player":   _ip_to_index(from_ip),
            "asking_for":    ask,
            "hand":          ctx["hand"],
            "fields":        _fields_dict(ctx),
            "penalty":       s.get("penalty", 0),
        },
        response_obj={
            "accepted": reply.accepted,
            "offer": list(reply.offer),
            "reason":    reply.reason,
        },
    )
    return reply


def get_considering_reply(
    s: dict[str, Any],
    my_offer: Cards,
    my_reason: str,
    their_offer: Cards,
    their_reason: str,
    their_fields: dict[str, Any],
    from_ip: str,
) -> ConsideringReply:
    ctx = {
        "hand":         _to_list(s.get("hand")),
        "new_cards":    _to_list(s.get("new_cards")),
        "field1":       _to_list(s.get("field1")),
        "field2":       _to_list(s.get("field2")),
        "field3":       _to_list(s.get("field3")),
        "coins":        s.get("coins", 0),
        "my_offer":     _to_list(my_offer),
        "my_reason":    my_reason,
        "their_offer":  _to_list(their_offer),
        "their_reason": their_reason,
        "their_fields": {f: _to_list(v) for f, v in their_fields.items()},
        "from_ip":      from_ip,
    }
    result = _request("considering", ctx)
    try:
        reply = ConsideringReply(
            accepted=bool(result.get("accepted", False)),
            offer=Cards(result.get("offer", [])),
            reason=result.get("reason", ""),
        )
    except Exception:
        return ConsideringReply(accepted=False, reason="error")

    _append_training(
        state_obj={
            "phase":       "CONSIDERING",
            "my_offers":   ctx["my_offer"],
            "my_reason":   my_reason,
            "their_offers": ctx["their_offer"],
            "their_reason": their_reason,
            "from_player": _ip_to_index(from_ip),
            "hand":        ctx["hand"],
            "new_cards":   ctx["new_cards"],
            "my_fields":   _fields_dict(ctx),
            "penalty":     s.get("penalty", 0),
            "their_fields": ctx["their_fields"],
        },
        response_obj={
            "accepted":  reply.accepted,
            "offer": list(reply.offer),
            "reason":    reply.reason,
        },
    )
    return reply
