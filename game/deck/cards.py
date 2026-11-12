"""Bohnanza bean definitions and deck utilities."""

import random
from typing import Any

# beanometer: cards needed to earn [1, 2, 3, 4] coins respectively
BEANS: dict[str, dict[str, Any]] = {
    "Coffee Bean":     {"count": 24, "beanometer": [4, 7, 10, 12]},
    "Wax Bean":        {"count": 22, "beanometer": [4, 7,  9, 11]},
    "Blue Bean":       {"count": 20, "beanometer": [4, 6,  8, 10]},
    "Chili Bean":      {"count": 18, "beanometer": [3, 6,  8,  9]},
    "Runner Bean":     {"count": 16, "beanometer": [3, 5,  7,  8]},
    "Soy Bean":        {"count": 12, "beanometer": [2, 4,  6,  7]},
    "Black-eyed Bean": {"count": 10, "beanometer": [2, 4,  5,  6]},
    "Red Bean":        {"count":  8, "beanometer": [2, 3,  4,  5]},
    "Fire Bean":       {"count":  8, "beanometer": [2, 3,  4,  5]},
    "Garden Bean":     {"count":  6, "beanometer": [2, 3]},
    "Broad Bean":      {"count":  6, "beanometer": [1, 2,  3,  4]},
}


def card(name: str) -> dict:
    b = BEANS[name]["beanometer"]
    return {
        "name":       name,
        "total":      BEANS[name]["count"],
        "beanometer": b,
        "max_coins":  len(b),
    }


def make_deck(seed: int | None = None) -> list[str]:
    """A shuffled deck; the same seed always gives the same order (paired tournament games)."""
    deck = [name for name, info in BEANS.items() for _ in range(info["count"])]
    (random.Random(seed) if seed is not None else random).shuffle(deck)
    return deck


def coins_for(bean: str, count: int) -> int:
    """Coins for harvesting `count` beans: the highest beanometer tier reached. Never decreases with count."""
    return sum(1 for threshold in BEANS[bean]["beanometer"] if count >= threshold)
