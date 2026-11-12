"""Legality: would the game carry out the answer as the model wrote it?

The answer goes through the game's own code: the prompt style's post-processing (the compact style
names the two other players "0"/"1" and maps them back to addresses), then the game's parser
(game/player/llm.py:parse_llm_response, which also accepts a JSON object wrapped in prose), then
the rules the game applies to that message type:

    PLANTING     plants 1–2 cards, exactly the front of the hand      PlantingAction.is_valid
    FORCED       places every new card exactly once                   NewCardPlantingAction.is_valid
    TRADING      a pass (null, or no cards and no player), or one or more cards the player holds
                 (hand + new cards) offered to one of the two other players
                                                                      game/player/actions.py:trading
    REPLY        the cards given in return are in the player's hand
    CONSIDERING  the cards proposed instead are in the player's hand or new cards

An answer the game cannot read is illegal, even where the game would fall back to a default (no
planting, a pass, a rejection): the fallback is the harness acting, not the model.

check() also returns the decision the answer makes, in a form two answers can be compared by;
the agreement and state-sensitivity metrics build on it.

Reasons an answer is illegal:
    no_json         no JSON object in the answer
    parser          JSON the game's message class rejects (wrong type, unknown card, bad address)
    rules           a planting that breaks the phase's rule
    unknown_player  an offer to nobody, or to an address that is not one of the two other players
    no_cards        an offer of no cards to a player
    cards_not_held  cards the player does not have
"""

import json
from collections import Counter
from dataclasses import dataclass
from typing import Any

from eval.tables import frac, markdown, pct
from game.player import state as game_state
from game.player.llm import parse_llm_response
from game.player.messages import (ConsideringReply, NewCardPlantingAction, OfferReply, PlantingAction,
                                  TradeOffer)
from game.player.prompts import ALIASES, STRATEGIES
from game.player.prompts.common import extract_json

PHASES = ("PLANTING", "FORCED", "TRADING", "REPLY", "CONSIDERING")
FIELDS = ("field1", "field2", "field3")
MESSAGE = {"PLANTING": PlantingAction, "FORCED": NewCardPlantingAction, "TRADING": TradeOffer,
           "REPLY": OfferReply, "CONSIDERING": ConsideringReply}


@dataclass
class Verdict:
    legal: bool
    reason: str | None = None      # why it is not legal (see the module docstring)
    decision: tuple | None = None  # comparable decision; None when the game cannot read the answer
    message: Any = None            # the parsed game message

    @property
    def text(self) -> str:
        """The free text the answer carries: a trade's ask, a reply's reason."""
        value = getattr(self.message, "ask", None) or getattr(self.message, "reason", None)
        return value if isinstance(value, str) else ""


def _postprocess(raw: str, style: str, peers: dict[str, str]) -> str:
    """The prompt style's own post-processing of a TRADING answer, as get_trade_offer applies it."""
    fn = getattr(STRATEGIES.get(ALIASES.get(style, style)), "postprocess_offer_response", None)
    if fn is None:
        return raw
    game_state.CONFIG.update(peers)  # index_to_ip reads the two other players from the player config
    return fn(raw)


def _is_null(raw: str) -> bool:
    try:
        return json.loads(raw.strip()) is None
    except json.JSONDecodeError:
        return False


def _cards(cards) -> tuple[str, ...]:
    return tuple(sorted(cards))


def _holds(cards, owned) -> bool:
    return not (Counter(cards) - Counter(owned))


def check(state: dict[str, Any], raw: str, style: str, peers: dict[str, str]) -> Verdict:
    """state: the logged state; style: the condition's prompt style; peers: player1_ip/player2_ip
    as the player's config (or the replay item) gave them."""
    phase = state["phase"]
    if phase == "TRADING":
        if _is_null(raw):
            return Verdict(True, decision=("pass",))
        raw = _postprocess(raw, style, peers)
    try:
        message, ok = parse_llm_response(raw, MESSAGE[phase])
    except AttributeError:  # a JSON value that is not an object (e.g. a list): the game's parser raises
        message, ok = None, False
    if not ok:
        try:
            json.loads(raw.strip())
            readable = True
        except json.JSONDecodeError:
            readable = extract_json(raw) is not None
        return Verdict(False, "parser" if readable else "no_json")
    return judge(state, message, peers)


def judge(state: dict[str, Any], message, peers: dict[str, str]) -> Verdict:
    """The verdict on a message the game has read — a parsed answer, or a bot's own message."""
    phase = state["phase"]
    if phase in ("PLANTING", "FORCED"):
        decision = ("plant",) + tuple((f, _cards(message.fields[f])) for f in FIELDS)
        legal = message.is_valid(state["hand"] if phase == "PLANTING" else state["new_cards"])
        return Verdict(legal, None if legal else "rules", decision, message)

    if phase == "TRADING":
        cards = list(message.offered_cards)
        if not message.to and not cards:
            return Verdict(True, decision=("pass",), message=message)
        target = {peers.get("player1_ip"): "0", peers.get("player2_ip"): "1"}.get(message.to) if message.to else None
        decision = ("offer", _cards(cards), target)
        if target is None:
            return Verdict(False, "unknown_player", decision, message)
        if not cards:
            return Verdict(False, "no_cards", decision, message)
        if not _holds(cards, state.get("hand", []) + state.get("new_cards", [])):
            return Verdict(False, "cards_not_held", decision, message)
        return Verdict(True, None, decision, message)

    # REPLY / CONSIDERING
    decision = ("accept" if message.accepted else "reject", _cards(message.offer))
    owned = state.get("hand", []) + (state.get("new_cards", []) if phase == "CONSIDERING" else [])
    legal = _holds(message.offer, owned)
    return Verdict(legal, None if legal else "cards_not_held", decision, message)


def summarize(records) -> dict:
    """records: (phase, Verdict, schema-valid?) per answer."""
    phases = {phase: {"n": 0, "legal": 0, "valid_and_legal": 0} for phase in PHASES}
    reasons = Counter()
    for phase, verdict, valid in records:
        phases[phase]["n"] += 1
        phases[phase]["legal"] += verdict.legal
        phases[phase]["valid_and_legal"] += verdict.legal and valid
        if verdict.reason:
            reasons[verdict.reason] += 1
    total = {k: sum(p[k] for p in phases.values()) for k in ("n", "legal", "valid_and_legal")}
    return {**total, "phases": phases, "reasons": dict(reasons.most_common())}


def table(rows: list[tuple[list[str], dict]]) -> list[str]:
    body = []
    for cells, s in rows:
        reasons = ", ".join(f"{k} {v}" for k, v in s["reasons"].items()) or "–"
        body.append(cells + [frac(s["legal"], s["n"]), pct(s["valid_and_legal"], s["n"])]
                    + [pct(s["phases"][p]["legal"], s["phases"][p]["n"]) for p in PHASES] + [reasons])
    return markdown(["condition", "model", "legal", "valid & legal", *PHASES, "why not legal"], body)
