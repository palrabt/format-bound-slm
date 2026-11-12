"""Generate Bohnanza LLM training data via guided interactive prompts."""

import argparse
import json
import random
import sys
from typing import Any, Callable, cast

from game.deck.cards import coins_for, make_deck

PLAYER_INDICES = ["0", "1"]

# ── ANSI helpers ───────────────────────────────────────────────────────────────

def _bold(s: str) -> str:   return f"\033[1m{s}\033[0m"
def _dim(s: str) -> str:    return f"\033[2m{s}\033[0m"
def _cyan(s: str) -> str:   return f"\033[36m{s}\033[0m"
def _yellow(s: str) -> str: return f"\033[33m{s}\033[0m"
def _green(s: str) -> str:  return f"\033[32m{s}\033[0m"
def _red(s: str) -> str:    return f"\033[31m{s}\033[0m"

# ── Input helpers ──────────────────────────────────────────────────────────────

def _ask(prompt: str, choices: list[str] | None = None) -> str:
    """Prompt until the user enters a valid choice (or any non-empty string if no choices)."""
    hint = f" [{'/'.join(choices)}]" if choices else ""
    while True:
        raw = input(_cyan(f"  {prompt}{hint}: ")).strip()
        if choices:
            if raw in choices:
                return raw
            print(_red(f"  ✗ Enter one of: {', '.join(choices)}"))
        else:
            if raw:
                return raw
            print(_red("  ✗ Cannot be empty."))


def _pick_field(label: str) -> str:
    v = _ask(label, ["1", "2", "3"])
    return f"field{v}"


def _pick_indices(label: str, cards: list[str], required: bool = False) -> list[int]:
    """Ask for space-separated indices into `cards`. Shows a numbered card list."""
    for i, c in enumerate(cards):
        print(_dim(f"    [{i}] {c}"))
    hint = "indices e.g. 0 2" if cards else "no cards available"
    while True:
        raw = input(_cyan(f"  {label} ({hint}): ")).strip()
        if not raw:
            if required:
                print(_red("  ✗ At least one index required."))
                continue
            return []
        try:
            indices = [int(x) for x in raw.split()]
            if all(0 <= i < len(cards) for i in indices):
                return indices
            print(_red(f"  ✗ Valid range: 0–{len(cards)-1}"))
        except ValueError:
            print(_red("  ✗ Enter space-separated numbers."))

# ── State generators ───────────────────────────────────────────────────────────

def _draw(deck: list[str], n: int) -> list[str]:
    drawn = deck[:n]
    del deck[:n]
    return drawn


def _size(typical: tuple[int, int], most: int, tail: float) -> int:
    """Usually a size in the `typical` range; with probability `tail`, anything
    above it up to `most`. Game states have long tails — hands keep growing and
    penalties pile up — so the corpus must cover them, not just the typical case."""
    lo, hi = typical
    if most > hi and random.random() < tail:
        return random.randint(hi + 1, most)
    return random.randint(lo, hi)


def _penalty() -> int:
    return _size((0, 30), 180, 0.4)


def _draw_field(deck: list[str]) -> dict:
    """Draw a homogeneous field (one bean type) from the deck, or empty."""
    if not deck or random.random() < 0.35:
        return {"cards": [], "value": 0}
    bean_type = deck[0]
    available = sum(1 for c in deck if c == bean_type)
    count = min(available, _size((1, 4), 8, 0.15))
    taken = 0
    i = 0
    while taken < count and i < len(deck):
        if deck[i] == bean_type:
            deck.pop(i)
            taken += 1
        else:
            i += 1
    cards = [bean_type] * count
    return {"cards": cards, "value": coins_for(bean_type, count)}


def _draw_fields(deck: list[str]) -> dict[str, dict]:
    return {
        "field1": _draw_field(deck),
        "field2": _draw_field(deck),
        "field3": _draw_field(deck),
    }


def _make_planting() -> dict:
    deck = make_deck()
    return {
        "phase": "PLANTING",
        "hand": _draw(deck, _size((1, 12), 35, 0.45)),
        "fields": _draw_fields(deck),
        "coins": random.randint(0, 15),
        "penalty": _penalty(),
    }


def _make_FORCED() -> dict:
    deck = make_deck()
    return {
        "phase": "FORCED",
        "new_cards": _draw(deck, _size((1, 2), 6, 0.25)),
        "fields": _draw_fields(deck),
        "coins": random.randint(0, 15),
        "penalty": _penalty(),
    }


# What a player says when rejecting an offer: why it doesn't fit and which
# beans they want instead. Shown to the proposer as TRADING's `reason`, and
# used by synth.py for REPLY rejections.
REJECT_REASONS = [
    "No thanks, {offered} doesn't fit my fields — I need {want}.",
    "Sorry, I'm collecting {want}, not {offered}.",
    "I'll pass on {offered}. Do you have {want}?",
    "{offered} is no use to me right now; I'm looking for {want}.",
    "Not this time — I'd trade for {want}, but not {offered}.",
    "I can't use {offered}. Any {want}?",
    "My fields need {want}, so I'll pass on {offered}.",
    "No deal for {offered}, sorry. I'd take {want} though.",
    "That doesn't work for me — I need {want}.",
    "I'd rather keep my cards unless you have {want}.",
]


def bean_list(cards: list[str]) -> str:
    """'Wax Bean and Soy Bean' — each bean type named once."""
    return " and ".join(dict.fromkeys(cards))


def _make_TRADING() -> dict:
    deck = make_deck()
    other_players = {idx: _draw_fields(deck) for idx in PLAYER_INDICES}
    new_cards = _draw(deck, _size((1, 2), 6, 0.15))
    hand = _draw(deck, _size((0, 8), 34, 0.35))
    # The game's first round has no history. In a later round previous_offers
    # is the rejected offer — cards the player still holds — and the rejecting
    # player's reason and optional counter-offer come with it.
    previous_offers, counter_offer, reason = [], [], ""
    if random.random() < 0.5:
        pool = hand + new_cards
        previous_offers = random.sample(pool, k=min(_size((1, 2), 5, 0.1), len(pool)))
        if random.random() < 0.3:
            counter_offer = _draw(deck, _size((1, 2), 4, 0.1))
        if random.random() < 0.9:
            want = random.choice([c for c in deck if c not in previous_offers] or deck)
            reason = random.choice(REJECT_REASONS).format(offered=bean_list(previous_offers), want=want)
    return {
        "phase": "TRADING",
        "new_cards": new_cards,
        "hand": hand,
        "fields": _draw_fields(deck),
        "coins": random.randint(0, 15),
        "penalty": _penalty(),
        "other_players": other_players,
        "previous_offers": previous_offers,
        "counter_offer": counter_offer,
        "reason": reason,
    }


def _make_REPLY() -> dict:
    deck = make_deck()
    return {
        "phase": "REPLY",
        "offered_cards": _draw(deck, _size((1, 3), 12, 0.08)),
        "from_player": random.choice(PLAYER_INDICES),
        "asking_for": random.choice(["I need chili beans.", "Can you give me a soy bean?", ""]),
        "hand": _draw(deck, _size((0, 10), 35, 0.4)),
        "fields": _draw_fields(deck),
        "penalty": _penalty(),
    }


MY_OFFER_REASONS = [
    "I can offer these, what do you have in return",
    "These don't fit my fields well.",
    "I have too many of these already.",
    "Trading these away helps me focus on my fields.",
    "These aren't useful to me right now.",
]


def _make_considering() -> dict:
    deck = make_deck()
    hand = _draw(deck, _size((0, 9), 33, 0.35))
    new_cards = _draw(deck, _size((0, 2), 6, 0.2))
    if not hand + new_cards:  # the offer that is being considered came from somewhere
        hand = _draw(deck, 1)
    pool = hand + new_cards
    my_offers = random.sample(pool, k=min(_size((1, 2), 5, 0.15), len(pool)))
    # In the game, CONSIDERING follows an accepted reply, which often gives
    # nothing back.
    their_offers = [] if random.random() < 0.5 else _draw(deck, _size((1, 2), 10, 0.1))
    return {
        "phase": "CONSIDERING",
        "my_offers": my_offers,
        "my_reason": random.choice(MY_OFFER_REASONS),
        "their_offers": their_offers,
        "their_reason": "I can offer these instead.",
        "from_player": random.choice(PLAYER_INDICES),
        "hand": hand,
        "new_cards": new_cards,
        "my_fields": _draw_fields(deck),
        "their_fields": _draw_fields(deck),
        "penalty": _penalty(),
    }

# ── Response collectors ────────────────────────────────────────────────────────

def _collect_planting(state: dict[str, Any]) -> dict[str, Any]:
    hand = state["hand"]
    print(_bold(f"\n  hand: {hand}"))
    for fname, fdata in state['fields'].items():
        cards, value = fdata['cards'], fdata['value']
        print(_bold(f"  {fname}: {cards or 'empty'}" + (_yellow(f" → {value} coins if harvested") if cards else "")))

    first_field = _pick_field(f"Plant FIRST card ({hand[0]}) into field")
    result = {"field1": [], "field2": [], "field3": []}
    result[first_field].append(hand[0])

    if len(hand) >= 2:
        choice = _ask(f"Plant SECOND card ({hand[1]}) into a field?", ["1", "2", "3", "skip"])
        if choice != "skip":
            result[f"field{choice}"].append(hand[1])

    return result


def _collect_FORCED(state: dict[str, Any]) -> dict[str, Any]:
    new_cards = state["new_cards"]
    print(_bold(f"\n  new_cards: {new_cards}"))
    for fname, fdata in state['fields'].items():
        cards, value = fdata['cards'], fdata['value']
        print(_bold(f"  {fname}: {cards or 'empty'}" + (_yellow(f" → {value} coins if harvested") if cards else "")))

    result: dict[str, list[str]] = {"field1": [], "field2": [], "field3": []}
    for i, card in enumerate(cast(list[str], new_cards)):
        field = _pick_field(f"Card [{i}] ({card}) → field")
        result[field].append(card)

    return result


def _collect_TRADING(state: dict[str, Any]) -> dict[str, Any]:
    pool = state["new_cards"] + state["hand"]
    print(_bold(f"\n  hand: {state['hand']}"))
    print(_bold(f"  new_cards: {state['new_cards']}"))
    print(_bold(f"  fields: {state['fields']}"))
    print(_bold(f"  other_players: {list(state['other_players'].keys())}"))

    skip = _ask("Skip trade (no offer)?", ["y", "n"])
    if skip == "y":
        return {"offered_cards": [], "to": "", "ask": ""}

    print("  Offer cards from hand+new_cards:")
    indices = _pick_indices("Offer card indices", pool, required=True)
    offered = [pool[i] for i in indices]

    players = list(state["other_players"].keys())
    for i, p in enumerate(players):
        print(_dim(f"    [{i+1}] player {p}"))
    target_idx = int(_ask("Target player", [str(i+1) for i in range(len(players))])) - 1
    target = players[target_idx]  # already an index "0"/"1"

    ask_msg = _ask("Ask message")

    return {"offered_cards": offered, "to": target, "ask": ask_msg}


def _collect_REPLY(state: dict[str, Any]) -> dict[str, Any]:
    hand: list[str] = cast(list[str], state["hand"])
    print(_bold(f"\n  offered_cards: {state['offered_cards']}"))
    print(_bold(f"  from: {state['from_player']}  asking: {state.get('asking_for', '')}"))

    print(_bold(f"  hand: {hand}"))
    print(_bold(f"  fields: {state['fields']}"))

    accept = _ask("Accept as offered?", ["y", "n"])
    if accept == "y":
        reason = _ask("Reason")
        return {"accepted": True, "offer": [], "reason": reason}

    offered = cast(list[str], state["offered_cards"])
    print("  Cards to return from hand (empty = flat reject):")
    while True:
        indices = _pick_indices("Return card indices (empty = nothing)", hand)
        counter_offer = [hand[i] for i in indices]
        overlap = set(counter_offer) & set(offered)
        if overlap:
            print(_red(f"  ✗ Don't return cards already offered to you: {sorted(overlap)}"))
            continue
        break

    reason = _ask("Reason")
    return {"accepted": False, "offer": counter_offer, "reason": reason}


def _collect_considering(state: dict[str, Any]) -> dict[str, Any]:
    pool = state["hand"] + state["new_cards"]
    print(_bold(f"\n  my_offers: {state['my_offers']}  ({state['my_reason']})"))
    print(_bold(f"  their_offers: {state['their_offers']}  ({state['their_reason']})"))
    print(_bold(f"  hand: {state['hand']}  new_cards: {state['new_cards']}"))
    print(_bold(f"  my_fields: {state['my_fields']}"))
    print(_bold(f"  their_fields: {state['their_fields']}"))

    accept = _ask("Accept offer?", ["y", "n"])
    if accept == "y":
        reason = _ask("Reason")
        return {"accepted": True, "offer": [], "reason": reason}

    pool_typed: list[str] = cast(list[str], pool)
    print("  New offer cards from hand+new_cards:")
    indices = _pick_indices("New offer indices (empty = decline)", pool_typed)
    new_offer = [pool_typed[i] for i in indices]
    reason = _ask("Reason")
    return {"accepted": False, "offer": new_offer, "reason": reason}


MAKERS: dict[str, Callable[[], dict[str, Any]]] = {
    "PLANTING":      _make_planting,
    "FORCED":  _make_FORCED,
    "TRADING": _make_TRADING,
    "REPLY":   _make_REPLY,
    "CONSIDERING":   _make_considering,
}

COLLECTORS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "PLANTING":      _collect_planting,
    "FORCED":  _collect_FORCED,
    "TRADING": _collect_TRADING,
    "REPLY":   _collect_REPLY,
    "CONSIDERING":   _collect_considering,
}

# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Bohnanza LLM training data.")
    parser.add_argument("--output", default="training/corpus/training_data.txt", help="Output file path")
    parser.add_argument("--count",  type=int, default=10, help="Samples per phase")
    parser.add_argument("--phases", nargs="+", default=list(MAKERS), choices=list(MAKERS),
                        help="Which phases to generate (default: all)")
    parser.add_argument("--seed",   type=int, default=None, help="Random seed for reproducibility")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    total = len(args.phases) * args.count
    written = 0

    with open(args.output, "a", encoding="utf-8") as f:
        for phase in args.phases:
            print(_yellow(f"\n{'='*60}\nPhase: {phase}  ({args.count} samples)\n{'='*60}"))
            for i in range(args.count):
                print(_bold(f"\n[{phase}] Sample {i+1}/{args.count}"))
                try:
                    state = MAKERS[phase]()
                    response = COLLECTORS[phase](state)
                    response_str = json.dumps(response)
                    print(_green(f"  ✓ {response_str}"))
                    f.write(f"\n{json.dumps(state)}\n[JSON] {response_str}\n")
                    f.flush()
                    written += 1
                except (KeyboardInterrupt, EOFError):
                    print(_red("\nInterrupted — partial data saved."))
                    sys.exit(0)
                except Exception as e:
                    print(_red(f"  ✗ ERROR: {e}"))

    print(_green(f"\nDone. {written}/{total} samples written to '{args.output}'."))


if __name__ == "__main__":
    main()
