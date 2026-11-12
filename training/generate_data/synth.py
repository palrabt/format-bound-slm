#!/usr/bin/env python3
"""Fully automated synthetic Bohnanza training data generator.

Usage:
    python3 -m training.generate_data.synth [--count N] [--output FILE] [--seed S]

Generates N entries per phase (PLANTING, FORCED, TRADING, REPLY, CONSIDERING)
using rule-based response generation and template natural language.
"""

import argparse
import json
import random
from collections import Counter
from pathlib import Path

from game.deck.cards import BEANS, coins_for
from training.generate_data.cli import MAKERS, REJECT_REASONS, bean_list

CARDS = list(BEANS.keys())

# ── Natural language templates ─────────────────────────────────────────────────

_TRADE_ASK = [
    "I have {card}, looking to trade for {want}.",
    "Anyone interested in swapping {card} for {want}?",
    "I can offer {card} — I'm hoping for {want} in return.",
    "Trading {card}, would love {want}.",
    "{card} up for grabs. Anyone have {want}?",
    "I'll give you {card} if you can spare {want}.",
    "Does anyone have {want}? I can offer {card}.",
    "I'd trade {card} for {want} if you're interested.",
    "Can anyone offer {want}? I have {card} to give.",
    "Offering {card} in exchange for {want}.",
]

_REPLY_ACCEPT_WITH_RETURN = [
    "Sure, I can give you {cards} in return.",
    "Deal! Here are {cards}.",
    "Yes, I'll take that. Have {cards}.",
    "That works for me — here's {cards}.",
    "Happy to trade, here is {cards}.",
    "I can do that, offering {cards}.",
    "Sounds good, {cards} on my end.",
    "I'll swap, giving you {cards}.",
    "Works for me. {cards} coming your way.",
    "Great offer! I can give {cards}.",
]

_REPLY_ACCEPT_NO_RETURN = [
    "Sure, sounds good!",
    "Yes, I'll take it.",
    "Deal!",
    "Works for me!",
    "Absolutely, happy to trade.",
    "Fine by me.",
    "That works.",
    "I'm in.",
]

# Rejecting with a counter-offer: the cards are the replier's own, what they
# could give instead; the beans they want can only be named in the text.
_REPLY_COUNTER = [
    "Not for {offered}, but I could give you {cards} for {want}.",
    "I'd rather not take {offered}. I can offer {cards} if you have {want}.",
    "How about {cards} for {want} instead?",
    "{offered} doesn't fit, but {cards} for {want} would work for me.",
    "Not this deal — I'd give {cards} for {want}.",
]

_CONSIDERING_ACCEPT = [
    "Deal, that works for me.",
    "Alright, I'll accept.",
    "That's fair, let's do it.",
    "Agreed!",
    "Sounds good, I'll take it.",
    "That works, accepted.",
    "Fine, I'll go with that.",
    "Great, let's trade.",
    "I'm happy with that offer.",
    "Accepted.",
]

_CONSIDERING_REJECT = [
    "Sorry, that doesn't work for me.",
    "I'll pass on this one.",
    "No thanks.",
    "That's not helpful to me right now.",
    "I'd rather decline.",
    "Not interested, sorry.",
    "That offer doesn't fit my needs.",
    "I can't accept that.",
    "No deal.",
    "I'll sit this one out.",
]

_CONSIDERING_COUNTER = [
    "How about {cards} instead?",
    "Could you do {cards} instead?",
    "I'd prefer to offer {cards}, would that work?",
    "What if I give you {cards} instead?",
    "I can offer {cards} — does that work for you?",
]


# ── Field helpers ──────────────────────────────────────────────────────────────

def _field_cards(f) -> list[str]:
    if isinstance(f, dict):
        return f.get("cards", [])
    return list(f) if f else []


def _field_type(f) -> str | None:
    cards = _field_cards(f)
    return cards[0] if cards else None


def _find_field_for(card: str, fields: dict) -> str | None:
    """Return field name that already holds this bean type, then empty, then None."""
    empty = None
    for fname in ["field1", "field2", "field3"]:
        t = _field_type(fields[fname])
        if t == card:
            return fname
        if t is None and empty is None:
            empty = fname
    return empty


# ── Rule-based response generators ────────────────────────────────────────────

def _auto_planting(state: dict) -> dict:
    hand   = state["hand"]
    fields = state["fields"]
    result: dict[str, list[str]] = {"field1": [], "field2": [], "field3": []}

    for i, card in enumerate(hand[:2]):
        target = _find_field_for(card, fields)
        if i == 0:
            target = target or "field1"
            result[target].append(card)
            fields = {k: ({"cards": _field_cards(v) + [card], "value": coins_for(card, len(_field_cards(v)) + 1)}
                          if k == target else v)
                      for k, v in fields.items()}
        elif target and random.random() < 0.55:
            result[target].append(card)
            fields = {k: ({"cards": _field_cards(v) + [card], "value": coins_for(card, len(_field_cards(v)) + 1)}
                          if k == target else v)
                      for k, v in fields.items()}
    return result


def _progress_to_next_coin(bean: str, count: int) -> float:
    """How far a field of `count` beans is towards its next coin (0–1)."""
    for threshold in BEANS[bean]["beanometer"]:
        if count < threshold:
            return count / threshold
    return 1.0  # beanometer maxed out


def _auto_forced(state: dict) -> dict:
    """Plant every new card. A bean joins the field that already grows it; the
    other bean types take empty fields, most copies first. Beans left over all
    go onto one field: one started this turn if any (no existing stack is
    lost), else the untouched field with the least progress towards its next
    coin (ties: fewer cards), so fields close to paying out are protected. The
    most plentiful bean is listed last there, because only the last bean type
    planted in a field stays.

    The protection rule keeps the same stacks as 89% of the hand-curated FORCED
    answers in training_data_synct_5000_offered_forced_over2.txt."""
    fields = state["fields"]
    result: dict[str, list[str]] = {f: [] for f in ("field1", "field2", "field3")}
    copies = Counter(state["new_cards"])
    beans = sorted(copies, key=lambda b: -copies[b])  # stable: ties keep first-seen order

    unmatched = []
    for bean in beans:
        match = next((f for f in result if _field_type(fields[f]) == bean), None)
        if match:
            result[match] = [bean] * copies[bean]
        else:
            unmatched.append(bean)
    overflow = []
    for bean in unmatched:
        empty = next((f for f in result if not _field_cards(fields[f]) and not result[f]), None)
        if empty:
            result[empty] = [bean] * copies[bean]
        else:
            overflow.append(bean)
    if not overflow:
        return result

    def protection(f: str) -> tuple[float, int]:
        cards = _field_cards(fields[f])
        return (_progress_to_next_coin(cards[0], len(cards)), len(cards))

    # Cheapest first: a field started this turn loses no existing stack; then
    # the least valuable untouched field; a matched field only as a last resort.
    started = [f for f in result if result[f] and not _field_cards(fields[f])]
    untouched = [f for f in result if not result[f]]
    target = started[0] if started else min(untouched or list(result), key=protection)
    spill = [card for bean in reversed(overflow) for card in [bean] * copies[bean]]
    result[target] = spill + result[target]
    return result


def _auto_trading(state: dict) -> dict:
    pool    = state["new_cards"] + state["hand"]
    fields  = state["fields"]

    if not pool or random.random() < 0.25:
        return {"offered_cards": [], "to": "", "ask": ""}

    field_types = {_field_type(v) for v in fields.values() if _field_type(v)}
    extras = [c for c in pool if c not in field_types]
    offer_pool = extras if extras else pool

    # Big hands (they keep growing in the game) are worth trimming by more than two cards.
    n_offer = random.randint(1, min(4 if len(pool) > 8 else 2, len(offer_pool)))
    offered = random.sample(offer_pool, k=n_offer)

    players = list(state["other_players"].keys())
    target  = random.choice(players)

    # want: prefer beans the proposer is already collecting (grounds the ask in their own state).
    # sorted(), not list(): set iteration order varies with PYTHONHASHSEED, which
    # made the random.choice below ignore --seed and produce a different corpus
    # on every run.
    own_visible = sorted(field_types | set(pool))
    want_pool = [b for b in own_visible if b not in offered]
    if not want_pool:
        want_pool = own_visible or CARDS
    want = random.choice(want_pool)

    card_str = " and ".join(dict.fromkeys(offered))  # named, deduped
    ask = random.choice(_TRADE_ASK).format(card=card_str, want=want)

    return {"offered_cards": offered, "to": target, "ask": ask}


def _reply_reject(offered: list[str], hand: list[str], field_types: set[str]) -> dict:
    """A rejection that says which beans the replier wants — preferably one they
    already grow — and sometimes counter-offers spare cards from their hand."""
    want_pool = (sorted(field_types - set(offered)) or sorted(set(hand) - set(offered))
                 or [c for c in CARDS if c not in offered])
    want = random.choice(want_pool)
    spare = [c for c in hand if c not in field_types and c != want and c not in offered]
    if spare and random.random() < 0.35:
        counter = random.sample(spare, k=random.randint(1, min(2, len(spare))))
        reason = random.choice(_REPLY_COUNTER).format(offered=bean_list(offered), cards=bean_list(counter), want=want)
        return {"accepted": False, "offer": counter, "reason": reason}
    reason = random.choice(REJECT_REASONS).format(offered=bean_list(offered), want=want)
    return {"accepted": False, "offer": [], "reason": reason}


def _auto_reply(state: dict) -> dict:
    offered = state["offered_cards"]
    hand    = state["hand"]
    fields  = state["fields"]

    field_types = {_field_type(v) for v in fields.values() if _field_type(v)}
    useful  = any(c in field_types for c in offered)
    accept  = useful or random.random() < 0.40

    if not accept:
        return _reply_reject(offered, hand, field_types)

    field_types_return = field_types - set(offered)
    extras = [c for c in hand if c not in field_types_return]
    if extras and random.random() < 0.65:
        n = random.randint(1, min(2, len(extras)))
        in_return = random.sample(extras, k=n)
        cards_str = ", ".join(in_return)
        reason = random.choice(_REPLY_ACCEPT_WITH_RETURN).format(cards=cards_str)
        return {"accepted": True, "offer": in_return, "reason": reason}

    return {
        "accepted": True,
        "offer": [],
        "reason": random.choice(_REPLY_ACCEPT_NO_RETURN),
    }


def _auto_considering(state: dict) -> dict:
    their_offers  = state["their_offers"]
    my_fields     = state["my_fields"]
    pool          = state["hand"] + state["new_cards"]

    field_types = {_field_type(v) for v in my_fields.values() if _field_type(v)}
    useful = any(c in field_types for c in their_offers)
    accept = useful or random.random() < 0.45

    if accept:
        return {
            "accepted": True,
            "offer": [],
            "reason": random.choice(_CONSIDERING_ACCEPT),
        }

    if pool and random.random() < 0.40:
        extras = [c for c in pool if c not in field_types]
        counter_pool = extras if extras else pool
        n = random.randint(1, min(2, len(counter_pool)))
        new_offer = random.sample(counter_pool, k=n)
        cards_str = ", ".join(new_offer)
        reason = random.choice(_CONSIDERING_COUNTER).format(cards=cards_str)
        return {"accepted": False, "offer": new_offer, "reason": reason}

    return {
        "accepted": False,
        "offer": [],
        "reason": random.choice(_CONSIDERING_REJECT),
    }


AUTO_RESPONDERS = {
    "PLANTING":    _auto_planting,
    "FORCED":      _auto_forced,
    "TRADING":     _auto_trading,
    "REPLY":       _auto_reply,
    "CONSIDERING": _auto_considering,
}

# ── Writer ─────────────────────────────────────────────────────────────────────

def _read_curated(path: Path, phases: list[str]) -> dict[str, list[str]]:
    """Hand-curated entries of the given phases, each as its two-line text."""
    curated: dict[str, list[str]] = {}
    for chunk in path.read_text(encoding="utf-8").strip().split("\n\n"):
        state_line, response_line = chunk.strip().split("\n")
        phase = json.loads(state_line)["phase"]
        if phase in phases:
            curated.setdefault(phase, []).append(f"{state_line}\n{response_line}")
    return curated


def generate(count_per_phase: int, output: Path, seed: int | None = None,
             curated: Path | None = None, curated_phases: list[str] | None = None) -> int:
    """Write count_per_phase entries per phase. Entries from `curated` (of
    `curated_phases`, default all) take the place of generated ones, so each
    phase still has count_per_phase entries."""
    if seed is not None:
        random.seed(seed)

    phases = list(MAKERS.keys())
    fixed = _read_curated(curated, curated_phases or phases) if curated else {}
    total  = 0
    with open(output, "w", encoding="utf-8") as f:
        for phase in phases:
            maker   = MAKERS[phase]
            respond = AUTO_RESPONDERS[phase]
            kept = fixed.get(phase, [])[:count_per_phase]
            for _ in range(count_per_phase - len(kept)):
                state    = maker()
                response = respond(state)
                state_line    = json.dumps(state,    separators=(", ", ": "))
                response_line = json.dumps(response, separators=(", ", ": "))
                f.write(f"\n{state_line}\n[JSON] {response_line}\n")
                total += 1
            for entry in kept:
                f.write(f"\n{entry}\n")
                total += 1
    return total


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic Bohnanza training data.")
    parser.add_argument("--count",  type=int, default=1000, help="Entries per phase (default 1000 → 5000 total)")
    parser.add_argument("--output", default="training/corpus/training_data_synct_5000.txt",
                        help="Output file path")
    parser.add_argument("--seed",   type=int, default=None)
    parser.add_argument("--curated", type=Path, default=None,
                        help="Corpus of hand-curated entries that replace generated ones of the same phase")
    parser.add_argument("--curated-phases", nargs="+", default=None,
                        help="Only take these phases from --curated (default: all)")
    args = parser.parse_args()

    out   = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    total = generate(args.count, out, seed=args.seed, curated=args.curated, curated_phases=args.curated_phases)
    print(f"Written {total} entries ({args.count} per phase) → {out}")


if __name__ == "__main__":
    main()
