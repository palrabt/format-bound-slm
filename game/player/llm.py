"""Bohnanza player — LLM communication helpers.

Prompt construction lives in game/player/prompts/ (three interchangeable
strategies: compact/verbose/grammar/verbose2 — see prompts/__init__.py:select_strategy).
This module is orchestration only: sending the request, logging, parsing the
response, and retrying.
"""

import json
import os
from typing import Any, Protocol, TypeVar

from . import state as _state
from .http import http_post
from .messages import ConsideringReply, NewCardPlantingAction, OfferReply, PlantingAction, TradeOffer, Cards
from .prompts import PromptSpec, select_strategy
from .prompts import common as _common


# ── Typing ─────────────────────────────────────────────────────────────────────

class _Parseable(Protocol):
    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "_Parseable": ...

T = TypeVar("T", bound=_Parseable)


# ── Infrastructure ─────────────────────────────────────────────────────────────

def llm_log_path() -> str:
    """One file per game: logs/[{scenario}/]{identity}/game_{n:04d}.log.

    `scenario` is an optional free-text field on the player config (e.g.
    "no_lora"/"with_lora") so runs are grouped by scenario from the moment
    they're written, rather than relying on a post-hoc move that a crash
    mid-run could skip."""
    identity = _state.CONFIG.get("identity") or _state.state.identity or "player"
    game_index = _state.game_index or 1
    scenario = _state.CONFIG.get("scenario")
    base = os.path.join("logs", scenario, identity) if scenario else os.path.join("logs", identity)
    return os.path.join(base, f"game_{game_index:04d}.log")


def _append_to_log_file(state_obj: dict[str, Any], response: str) -> None:
    """Write one entry in the same format as training_data.txt: a compact
    JSON state line, followed by '[JSON] <response>', regardless of what
    prompt style was actually sent to the LLM."""
    path = llm_log_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(state_obj, separators=(", ", ": ")))
        f.write("\n[JSON] ")
        f.write(response.strip())
        f.write("\n\n")


def _ask_llm(spec: PromptSpec, state_obj: dict[str, Any]) -> str:
    """Send one decision prompt as a chat turn.

    The adapters are trained with the base model's chat template — state as a
    user turn, response as an assistant turn ending in EOS — so inference has
    to go through the chat endpoint too. A model trained with the template and
    prompted without it does worse than either consistent choice.

    Because the response now ends at a real EOS token, there is no stop-string
    and no first-line scraping: a multi-line JSON answer survives intact
    instead of being truncated at the first newline.
    """
    llm_type = _state.CONFIG.get("llm_type", "ollama")
    llm_section = _state.CONFIG.get("llm_section", {})

    # An operator-set llm.system_prompt wins if present; otherwise fall back
    # to the strategy's own system_prompt (verbose/grammar set one, compact
    # doesn't — matches its compact training-corpus format).
    system = llm_section.get("system_prompt", "") or spec.system_prompt
    messages: list[dict[str, str]] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": spec.text})

    if llm_type == "llamacpp":
        url  = f"{_state.CONFIG['llm_ip']}/v1/chat/completions"
        body: dict[str, Any] = {
            "messages": messages,
            "max_tokens": llm_section.get("max_tokens", 256),
            "stream": False,
            "temperature": llm_section.get("temperature", 0.0),
        }
        if spec.grammar:
            body["grammar"] = spec.grammar
        result = http_post(url, body, timeout=120)
        response = result["choices"][0]["message"]["content"].strip()
    else:
        # ollama /api/chat: no grammar support, no max_tokens/temperature —
        # the grammar strategy is only ever paired with llamacpp in practice.
        url  = f"{_state.CONFIG['llm_ip']}/api/chat"
        body = {
            "model": _state.CONFIG.get("llm_model", "llama3.2"),
            "messages": messages,
            "stream": False,
        }
        result = http_post(url, body, timeout=120)
        response = (result.get("message") or {}).get("content", "").strip()
    _append_to_log_file(state_obj, response)
    return response


def parse_llm_response(response: str, cls: type[T], default: T | None = None) -> tuple[T | None, bool]:
    for text in (response, _common.extract_json(response)):
        if text is None:
            continue
        try:
            data = json.loads(text)
            if data is None:
                return default, False
            result = cls.from_dict(data)  # type: ignore[return-value]
            return result, True
        except ValueError as e:
            # Type validation error (e.g., invalid card names in Cards)
            _state.debug(f"Value {type[T]} validation error: {e}")
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            _state.debug(f"Parsing error: {e}")
    return default, False


def _parse_with_retry(
    prompt_fn: callable,
    cls: type[T],
    default: T | None = None,
    max_retries: int | None = None,
) -> T | None:

    if max_retries is None:
        max_retries = _state.CONFIG.get("llm_max_retries", 3)

    for attempt in range(max_retries):
        try:
            response = prompt_fn()
            result, success = parse_llm_response(response, cls, default=None)
            if success:
                return result
            else:
                _state.debug(f"Parsing error, will retry. Attempt: {attempt}")
        except Exception as e:
            _state.err(f"Parsing exception: {e}")

    # All retries exhausted
    return default


# ── Public interface ───────────────────────────────────────────────────────────

def get_planting_action(s: dict[str, Any]) -> PlantingAction:
    strategy = select_strategy()
    result = _parse_with_retry(
        lambda: _ask_llm(strategy.build_planting_prompt(s), _common.plant_state_obj(s)),
        PlantingAction)
    return result if result else PlantingAction()


def get_new_card_action(s: dict[str, Any]) -> NewCardPlantingAction:
    strategy = select_strategy()
    result = _parse_with_retry(
        lambda: _ask_llm(strategy.build_forced_prompt(s), _common.forced_state_obj(s)),
        NewCardPlantingAction
    )
    return result if result else NewCardPlantingAction()


def get_trade_offer(
    s: dict[str, Any],
    other_fields: dict[str, dict[str, Cards]],
    previous_offers: Cards,
    in_return: Cards,
    reason: str,
) -> TradeOffer:
    strategy = select_strategy()

    def _prompt() -> str:
        raw = _ask_llm(
            strategy.build_offer_prompt(s, other_fields, previous_offers, in_return, reason),
            _common.offer_state_obj(s, other_fields, previous_offers, in_return, reason),
        )
        postprocess = getattr(strategy, "postprocess_offer_response", None)
        return postprocess(raw) if postprocess else raw

    offer = _parse_with_retry(_prompt, TradeOffer)
    if offer and offer.to:
        return offer
    return TradeOffer()


def get_REPLY(s: dict[str, Any], cards: Cards, from_ip: str, ask: str) -> OfferReply:
    strategy = select_strategy()
    return _parse_with_retry(
        lambda: _ask_llm(strategy.build_reply_prompt(s, cards, from_ip, ask), _common.recv_offer_state_obj(s, cards, from_ip, ask)),
        OfferReply,
        default=OfferReply(reason="Could not parse response.")
    )  # type: ignore[return-value]


def get_considering_reply(
    s: dict[str, Any],
    my_offer: Cards,
    my_reason: str,
    their_offer: Cards,
    their_reason: str,
    their_fields: dict[str, Cards],
    from_ip: str,
) -> ConsideringReply:
    strategy = select_strategy()
    return _parse_with_retry(
        lambda: _ask_llm(
            strategy.build_considering_prompt(s, my_offer, my_reason, their_offer, their_reason, their_fields, from_ip),
            _common.considering_state_obj(s, my_offer, my_reason, their_offer, their_reason, their_fields, from_ip),
        ),
        ConsideringReply,
        default=ConsideringReply(accepted=False, reason="Could not parse response.")
    )  # type: ignore[return-value]
