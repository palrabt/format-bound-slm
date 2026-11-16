"""Rule-based players: the opponents and baselines of the tournament.

A bot answers the same five calls as llm.py and human.py (state.decision_module picks it by
llm.type): "bot_reference" plays the reference rules below — the adapters' teacher, an earlier teacher's
deterministic rules with its random parts replaced by value rules — and "bot_random" plays a
uniformly random legal move, the floor. A bot needs no LLM server and writes no LLM log.

    planting     first card on a field growing that bean, else an empty field, else harvest the
                 field with the least progress towards its next coin; the second card only onto a
                 field already growing it
    forced       the teacher's rule (synth._auto_forced): no harvest when the new cards fit, the
                 least valuable stack when one is unavoidable
    trading      offer up to two spare beans (not growing in its own fields) to the player growing
                 most of them; pass when no one grows any, or when that offer was just refused
    reply        accept exactly when the offer includes a bean it grows, giving back one spare bean
    considering  accept exactly when the cards given back include a bean it grows

The random bot draws from a generator seeded by the state it is asked about, so the same state
always gets the same answer — runs stay paired and reproducible.
"""

import hashlib
import json
import os
import random
from typing import Any

from training.generate_data.synth import _auto_forced, _progress_to_next_coin

from . import state as _state
from .messages import (Address, Cards, ConsideringReply, NewCardPlantingAction, OfferReply, PlantingAction,
                       TradeOffer)

FIELDS = ("field1", "field2", "field3")


def _cards(field) -> list[str]:
    return list(field.get("cards", [])) if isinstance(field, dict) else list(field or [])


def _fields(s: dict[str, Any]) -> dict[str, list[str]]:
    return {f: _cards(s.get(f)) for f in FIELDS}


def _growing(s: dict[str, Any]) -> set[str]:
    return {cards[0] for cards in _fields(s).values() if cards}


def _spare(s: dict[str, Any], pool: list[str]) -> list[str]:
    growing = _growing(s)
    return [c for c in pool if c not in growing]


def llm_log_path() -> str:
    """The /llm_log endpoint's file: bots keep none."""
    return os.path.join("logs", f"{_state.CONFIG.get('identity', 'bot')}_bot.log")


class Reference:
    """The reference rules (the module docstring), deterministic: the adapters' teacher."""

    llm_log_path = staticmethod(llm_log_path)

    def get_planting_action(self, s: dict[str, Any]) -> PlantingAction:
        hand, fields = list(s.get("hand", [])), _fields(s)
        plan = {f: [] for f in FIELDS}
        if not hand:
            return PlantingAction()
        first = hand[0]
        same = [f for f in FIELDS if fields[f] and fields[f][0] == first]
        empty = [f for f in FIELDS if not fields[f]]
        if same or empty:
            target = (same or empty)[0]
        else:
            target = min(FIELDS, key=lambda f: (_progress_to_next_coin(fields[f][0], len(fields[f])), len(fields[f])))
        plan[target].append(first)
        after = dict(fields)
        after[target] = (fields[target] + [first]) if fields[target] and fields[target][0] == first else [first]
        if len(hand) > 1:
            second = hand[1]
            grows = [f for f in FIELDS if after[f] and after[f][0] == second]
            if grows:
                plan[grows[0]].append(second)
        return PlantingAction(**{f: Cards(plan[f]) for f in FIELDS})

    def get_new_card_action(self, s: dict[str, Any]) -> NewCardPlantingAction:
        state = {"fields": {f: {"cards": c} for f, c in _fields(s).items()}, "new_cards": list(s.get("new_cards", []))}
        plan = _auto_forced(state)
        return NewCardPlantingAction(**{f: Cards(plan[f]) for f in FIELDS})

    def get_trade_offer(self, s, other_fields, previous_offers, in_return, reason) -> TradeOffer:
        spare = _spare(s, list(s.get("new_cards", [])) + list(s.get("hand", [])))
        best, best_cards = None, []
        for ip, fields in other_fields.items():
            theirs = {cards[0] for cards in (_cards(v) for v in fields.values()) if cards}
            cards = [c for c in spare if c in theirs][:2]
            if len(cards) > len(best_cards):
                best, best_cards = ip, cards
        if not best or sorted(best_cards) == sorted(previous_offers or []):
            return TradeOffer()
        names = " and ".join(dict.fromkeys(best_cards))
        return TradeOffer(offered_cards=Cards(best_cards), to=Address(best),
                          ask=f"{names} would fit your field — anything you can spare in return?")

    def get_REPLY(self, s, cards, from_ip, ask) -> OfferReply:
        if set(cards) & _growing(s):
            back = _spare(s, list(s.get("hand", [])))[:1]
            return OfferReply(accepted=True, offer=Cards(back), reason="Deal, that fits my field.")
        return OfferReply(accepted=False, offer=Cards([]), reason="Sorry, that doesn't fit my fields.")

    def get_considering_reply(self, s, my_offer, my_reason, their_offer, their_reason, their_fields,
                              from_ip) -> ConsideringReply:
        if set(their_offer) & _growing(s):
            return ConsideringReply(accepted=True, offer=Cards([]), reason="Deal.")
        return ConsideringReply(accepted=False, offer=Cards([]), reason="No thanks, that doesn't fit my fields.")


class Random:
    """A uniformly random legal move, seeded by the state."""

    llm_log_path = staticmethod(llm_log_path)

    @staticmethod
    def _rng(*parts) -> random.Random:
        key = json.dumps(parts, sort_keys=True, default=list) + str(_state.CONFIG.get("identity", ""))
        return random.Random(int(hashlib.sha256(key.encode()).hexdigest()[:16], 16))

    def get_planting_action(self, s: dict[str, Any]) -> PlantingAction:
        hand = list(s.get("hand", []))
        rng = self._rng("plant", s)
        plan = {f: [] for f in FIELDS}
        for card in hand[:1 + (len(hand) > 1 and rng.random() < 0.5)]:
            plan[rng.choice(FIELDS)].append(card)
        return PlantingAction(**{f: Cards(plan[f]) for f in FIELDS})

    def get_new_card_action(self, s: dict[str, Any]) -> NewCardPlantingAction:
        rng = self._rng("forced", s)
        plan = {f: [] for f in FIELDS}
        for card in s.get("new_cards", []):
            plan[rng.choice(FIELDS)].append(card)
        return NewCardPlantingAction(**{f: Cards(plan[f]) for f in FIELDS})

    def get_trade_offer(self, s, other_fields, previous_offers, in_return, reason) -> TradeOffer:
        rng = self._rng("trade", s, other_fields, previous_offers, in_return)
        pool = list(s.get("new_cards", [])) + list(s.get("hand", []))
        if not pool or not other_fields or rng.random() < 0.5:
            return TradeOffer()
        cards = rng.sample(pool, k=min(len(pool), rng.randint(1, 2)))
        return TradeOffer(offered_cards=Cards(cards), to=Address(rng.choice(sorted(other_fields))),
                          ask="Would you take these?")

    def get_REPLY(self, s, cards, from_ip, ask) -> OfferReply:
        rng = self._rng("reply", s, cards)
        hand = list(s.get("hand", []))
        back = rng.sample(hand, k=1) if hand and rng.random() < 0.5 else []
        accepted = rng.random() < 0.5
        return OfferReply(accepted=accepted, offer=Cards(back), reason="Deal." if accepted else "No thanks.")

    def get_considering_reply(self, s, my_offer, my_reason, their_offer, their_reason, their_fields,
                              from_ip) -> ConsideringReply:
        accepted = self._rng("considering", s, my_offer, their_offer).random() < 0.5
        return ConsideringReply(accepted=accepted, offer=Cards([]), reason="Deal." if accepted else "No thanks.")


BOTS = {"bot_reference": Reference, "bot_random": Random}
_instances: dict[str, object] = {}


def bot(kind: str):
    """The bot for an llm.type, one instance per process."""
    if kind not in _instances:
        _instances[kind] = BOTS[kind]()
    return _instances[kind]
