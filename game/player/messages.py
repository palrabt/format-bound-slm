"""Typed dataclasses for HTTP request/response bodies and LLM responses."""

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

VALID_CARDS = {
    "Coffee Bean", "Wax Bean", "Blue Bean", "Chili Bean", "Runner Bean",
    "Soy Bean", "Black-eyed Bean", "Red Bean", "Fire Bean", "Garden Bean", "Broad Bean"
}



class Cards(list[str]):
    def __init__(self, iterable=None):
        super().__init__(iterable or [])
        self.validate()

    def validate(self):
        if not all(card in VALID_CARDS for card in self):
            raise ValueError(f"Invalid card names: {list(self)}")


_IP_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}(:\d+)?$")


class Address(str):
    """A validated IP address or HTTP(S) URL string."""

    def __new__(cls, value: str = "") -> "Address":
        instance = super().__new__(cls, value)
        if value and not value.startswith(("http://", "https://")) and not _IP_RE.match(value):
            raise ValueError(f"Invalid address {value!r}: must start with http(s):// or be an IP address")
        return instance


# ── Player ↔ Player ────────────────────────────────────────────────────────────

@dataclass
class OfferRequest:
    cards: Cards
    from_ip: Address
    ask: str = ""

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "OfferRequest":
        return cls(cards=Cards(d["cards"]), from_ip=Address(d.get("from", "")), ask=d.get("ask", ""))

    def to_dict(self) -> dict[str, Any]:
        return {"cards": self.cards, "from": self.from_ip, "ask": self.ask}



@dataclass
class TradeRequest:
    getting: Cards
    sending: Cards
    from_ip: Address = field(default_factory=Address)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "TradeRequest":
        return cls(
            getting=Cards(d["getting"]),
            sending=Cards(d["sending"]),
            from_ip=Address(d.get("from", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {"getting": self.getting, "sending": self.sending, "from": self.from_ip}


@dataclass
class TradeResponse:
    success: bool
    sending: Cards = field(default_factory=Cards)
    getting: Cards = field(default_factory=Cards)
    state: dict[str, Any] = field(default_factory=dict)
    error: str = ""

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "TradeResponse":
        return cls(
            success=d.get("success", False),
            sending=d.get("sending", []),
            getting=d.get("getting", []),
            state=d.get("state", {}),
            error=d.get("error", ""),
        )

    def to_dict(self) -> dict[str, Any]:
        if self.error:
            return {"success": False, "error": self.error}
        return {"success": True, "sending": self.sending, "getting": self.getting, "state": self.state}


# ── Player → Deck ──────────────────────────────────────────────────────────────


@dataclass
class DealResponse:
    cards: Cards
    start: bool = False

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "DealResponse":
        return cls(
            cards=[c["name"] for c in d.get("cards", [])],
            start=d.get("start", False),
        )


@dataclass
class ReturnResponse:
    coins: int

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "ReturnResponse":
        return cls(coins=d.get("coins", 0))


@dataclass
class EndTurnResponse:
    game_over: bool

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "EndTurnResponse":
        return cls(game_over=d.get("game_over", False))


# ── LLM Responses ──────────────────────────────────────────────────────────────

@dataclass
class _FieldAssignment:
    """Shared shape of both planting responses: which cards go to which field.

    The two phases differ only in what counts as valid — see is_valid on each.
    """
    field1: Cards = field(default_factory=Cards)
    field2: Cards = field(default_factory=Cards)
    field3: Cards = field(default_factory=Cards)

    @property
    def fields(self) -> dict[str, Cards]:
        return {"field1": self.field1, "field2": self.field2, "field3": self.field3}

    @property
    def actions(self) -> list[str]:
        return list(self.field1) + list(self.field2) + list(self.field3)

    @classmethod
    def from_dict(cls, d: dict[str, Any]):
        return cls(
            field1=Cards(d.get("field1", [])),
            field2=Cards(d.get("field2", [])),
            field3=Cards(d.get("field3", [])),
        )


@dataclass
class PlantingAction(_FieldAssignment):
    """LLM response for the from-hand planting phase."""

    def is_valid(self, hand: list[str]) -> bool:
        """Plants 1-2 cards, and exactly the ones at the front of the hand."""
        cards = self.actions
        n = len(cards)
        if n < 1 or n > min(2, len(hand)):
            return False
        return Counter(cards) == Counter(hand[:n])

    def exec_order(self, hand: list[str]) -> list[str]:
        """Return fields in the order their assigned cards appear in hand."""
        result = []
        remaining = {name: list(cards) for name, cards in self.fields.items()}
        for card in hand[:2]:
            for field_name, field_cards in remaining.items():
                if card in field_cards:
                    result.append(field_name)
                    field_cards.remove(card)
                    break
        return result


@dataclass
class NewCardPlantingAction(_FieldAssignment):
    """LLM response for the forced new-card planting phase."""

    def is_valid(self, new_cards: list[str]) -> bool:
        """Every new card must be placed, exactly once."""
        return Counter(self.actions) == Counter(new_cards)


@dataclass
class TradeOffer:
    """LLM-proposed trade offer (null from LLM becomes None in Python)."""
    offered_cards: Cards = field(default_factory=Cards)
    to: Address = field(default_factory=Address)
    ask: str = ""


    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "TradeOffer":
        return cls(
            offered_cards=Cards(d.get("offered_cards", [])),
            to=Address(d.get("to", "")),
            ask=d.get("ask", ""),
        )


@dataclass
class OfferReply:
    """LLM response when receiving an offer — what to offer in return."""
    accepted: bool = False
    offer: Cards = field(default_factory=Cards)
    reason: str = ""

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "OfferReply":
        return cls(accepted=d.get("accepted", False), offer=Cards(d.get("offer", [])), reason=d.get("reason", ""))

    def to_dict(self) -> dict[str, Any]:
        return {"accepted": self.accepted, "offer": self.offer, "reason": self.reason}


@dataclass
class ConsideringReply:
    """LLM response when deciding whether to accept a counter-offer."""
    accepted: bool
    offer: Cards = field(default_factory=Cards)
    reason: str = ""

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "ConsideringReply":
        return cls(
            accepted=d.get("accepted", False),
            offer=Cards(d.get("offer", [])),
            reason=d.get("reason", ""),
        )
