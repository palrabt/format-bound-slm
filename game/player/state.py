"""Shared player game state, config, and locking."""

import functools
import inspect
import threading
from typing import Any, Callable, TypeVar

from game.deck.cards import coins_for

F = TypeVar("F", bound=Callable[..., tuple[bool, dict[str, Any]]])

# ── Shared state ───────────────────────────────────────────────────────────────

lock = threading.Lock()

class Field:
    """A bean field whose coin value is always derived from its current cards."""
    def __init__(self) -> None:
        self.cards: list[str] = []

    @property
    def value(self) -> int:
        if not self.cards:
            return 0
        return coins_for(self.cards[0], len(self.cards))

    def to_dict(self) -> dict[str, Any]:
        return {"cards": list(self.cards), "value": self.value}


class PlayerState:
    """Typed game state for a single player."""

    def __init__(self) -> None:
        self.new_cards: list[str] = []   # up to 2 cards just drawn from the deck
        self.hand:      list[str] = []   # ordered list; new items pushed to back
        self.field1:    Field     = Field()
        self.field2:    Field     = Field()
        self.field3:    Field     = Field()
        self.coins:        int       = 0
        self.penalty:      int       = 0    # incremented each time retries are exhausted with no valid LLM response
        self.identity:     str       = ""   # player's name or ID, for logging and trade offers

    def to_dict(self) -> dict[str, Any]:
        return {
            "new_cards": list(self.new_cards),
            "hand":      list(self.hand),
            "field1":    self.field1.to_dict(),
            "field2":    self.field2.to_dict(),
            "field3":    self.field3.to_dict(),
            "coins":       self.coins,
            "penalty":     self.penalty,
            "identity":    self.identity,
        }

    @property
    def print(self) -> str:
        return(
            "\n"
            f"Hand: {self.hand}; New: {self.new_cards}; Coins: {self.coins}; Penalty: {self.penalty}\n"
            f"Field1: {self.field1.cards}\n"
            f"Field2: {self.field2.cards}\n"
            f"Field3: {self.field3.cards}\n"
        )

state = PlayerState()

CONFIG: dict[str, Any] = {}

game_index: int = 0   # bumped on every /init — splits the LLM log into one file per game

# ── Logging ────────────────────────────────────────────────────────────────────

LOG_LEVEL: str = "info"   # "err" | "info" | "debug"

NBR_OF_RETRIES: int = 3
NBR_OF_TRADING: int = 3

_LEVELS: dict[str, int] = {"err": 0, "warn": 1, "info": 2, "debug": 3}


def log(msg: str, level: str = "info") -> None:
    if _LEVELS.get(level, 2) > _LEVELS.get(LOG_LEVEL, 2):
        return
    identity = CONFIG.get("identity") or state.identity or "unknown"
    caller = inspect.stack()[1 if level == "info" else 2].function
    print(f"[{identity}][{level.upper()}][{caller}] {msg}")

def debug(msg: str) -> None:
    log(msg, "debug")

def warn(msg: str) -> None:
    log(msg, "warn")

def err(msg: str) -> None:
    log(msg, "err")





# ── Decision module ────────────────────────────────────────────────────────────


def decision_module():
    """Return the active decision module for this player: human, a rule-based bot, or LLM.

    The imports are deferred: llm, human and bots all import this module, so a
    top-level import would be circular.
    """
    kind = CONFIG.get("llm_type")
    if kind == "human":
        from . import human
        return human
    if kind and kind.startswith("bot_"):
        from . import bots
        return bots.bot(kind)
    from . import llm
    return llm


# ── Peer addressing ────────────────────────────────────────────────────────────


def ip_to_index(ip: str, default: str = "") -> str:
    """Map a peer's base URL to the "0"/"1" index used in prompts and training data.

    `default` is what an unrecognised address maps to: llm.py needs a usable
    peer index ("0") so a trade offer always has a target, while human.py
    records "" so an unknown address is not silently written into the
    training corpus as player 0.
    """
    if ip == CONFIG.get("player1_ip"):
        return "0"
    if ip == CONFIG.get("player2_ip"):
        return "1"
    return default


# ── Decorator ──────────────────────────────────────────────────────────────────


def catch_errors(fn: F) -> F:
    """Catch any exception and return (False, {"error": ...}) instead of raising."""
    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> tuple[bool, dict[str, Any]]:
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            return False, {"error": str(e)}
    return wrapper  # type: ignore[return-value]
