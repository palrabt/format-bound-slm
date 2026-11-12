"""Bohnanza player — game action functions and turn phase orchestration."""

import urllib.error
from typing import Any
from collections import Counter

from . import state as _state
from . import messages as m
from .http import http_get, http_post
from .state import (
    catch_errors, decision_module as _dm, lock, log, state, debug, warn, err,
    NBR_OF_RETRIES, NBR_OF_TRADING,
)

# ── Field helpers ──────────────────────────────────────────────────────────────


def _field_accepts(card: str, field: str) -> bool:
    """True if `field` is empty or already holds `card`'s bean type."""
    field_cards = getattr(state, field).cards
    if len(field_cards) == 0 or field_cards[0] == card:
        return True
    return False

# ── Action functions ───────────────────────────────────────────────────────────


@catch_errors
def do_plant(card_location: str, selected_card: str, field: str) -> tuple[bool, dict[str, Any]]:
    debug("do_plant: called")
    with lock:

        if card_location == "hand":
            if not state.hand:
                debug("do_plant: hand is empty")
                return False, {"error": "hand is empty"}
            selected_card = state.hand[0]
            if not _field_accepts(selected_card, field):
                debug(f"do_plant: {field} does not accept {selected_card!r}")
                return False, {"error": f"{field} does not accept {selected_card!r}"}

            state.hand.pop(0)
        elif card_location == "new_cards":
            if not _field_accepts(selected_card, field):
                debug(f"do_plant: {field} does not accept {selected_card!r}")
                return False, {"error": f"{field} does not accept {selected_card!r}"}

            state.new_cards.remove(selected_card)
        else:
            debug(f"do_plant: invalid card location {card_location!r}")
            return False, {"error": f"invalid card location: {card_location!r}"}

        getattr(state, field).cards.append(selected_card)
        snapshot = state.to_dict()
    debug(f"do_plant: planted {selected_card!r} on {field}")
    return True, {"action": "plant", "card": selected_card, "field": field, "state": snapshot}


@catch_errors
def do_harvest(fields: list[str]) -> tuple[bool, dict[str, Any]]:
    debug(f"do_harvest: called with fields={fields}")
    if not fields:
        debug("do_harvest: no fields specified")
        return False, {"error": "no fields specified"}
    with lock:
        for f in fields:
            if f not in ("field1", "field2", "field3"):
                debug(f"do_harvest: invalid field {f!r}")
                return False, {"error": f"invalid field: {f}"}
        to_return: list[str] = []
        for f in fields:
            to_return.extend(getattr(state, f).cards)
            getattr(state, f).cards = []
    debug(f"do_harvest: returning {to_return} to deck")
    result = http_post(f"{_state.CONFIG['deck_ip']}/return", {"cards": to_return})
    ret = m.ReturnResponse.from_dict(result)
    with lock:
        state.coins += ret.coins
        snapshot = state.to_dict()
    debug(f"do_harvest: earned {ret.coins} coins, total={state.coins}")
    return True, {"action": "harvest", "harvested": to_return, "coins_earned": ret.coins, "state": snapshot}


@catch_errors
def do_deal(num: int) -> tuple[bool, dict[str, Any]]:
    debug(f"do_deal: called with num={num}")
    result = http_get(f"{_state.CONFIG['deck_ip']}/deal{2 if num == 2 else 3}")
    deal = m.DealResponse.from_dict(result)
    dest = "new_cards" if num == 2 else "hand"
    debug(f"do_deal: received {deal.cards} → {dest}")
    with lock:
        getattr(state, dest).extend(deal.cards)
        snapshot = state.to_dict()
    return True, {"action": "deal", "new_cards": deal.cards, "state": snapshot}


def get_other_fields() -> dict[str, dict[str, list[str]]]:
    other_fields: dict[str, dict[str, list[str]]] = {}
    for key in ("player1_ip", "player2_ip"):
        ip: str = _state.CONFIG.get(key, "")
        if not ip:
            continue
        try:
            other_user_fields = http_get(f"{ip}/state")
            other_fields[ip] = {f: other_user_fields.get(f, {"cards": [], "value": 0}) for f in ("field1", "field2", "field3")}
            debug(f"{other_fields[ip]}")
        except Exception as e:
            other_fields[ip] = {"field1": {"cards": [], "value": 0}, "field2": {"cards": [], "value": 0}, "field3": {"cards": [], "value": 0}}
            debug(f"failed to fetch state from {ip}: {e}")
    return other_fields

def do_prepare_offer(other_fields: dict[str, dict[str, m.Cards]], previous_offers: m.Cards, in_return: m.Cards, reason: str) -> m.TradeOffer:
    with lock:
        snapshot = state.to_dict()
    
    is_offer_correct = False
    retries = 0
    offer: m.TradeOffer = m.TradeOffer()
    while( not is_offer_correct and retries < NBR_OF_RETRIES):
        try:
            offer = _dm().get_trade_offer(snapshot, other_fields, previous_offers, in_return, reason)
            debug(f"do_prepare_offer: prepared offer {offer}")
            if not offer.to:
                debug("Nothing offered, skip offering")
                is_offer_correct = True
                break

            if (Counter(offer.offered_cards) <= Counter(state.hand + state.new_cards)):
                is_offer_correct = True
            else:
                retries += 1
                warn(f"Offered cards are not a real subset: {offer.offered_cards} not in {state.hand + state.new_cards}, retry {retries}")
        except Exception as e:
            warn(f"Offer creation error: {e}, retry {retries + 1}")
            retries += 1
    if not is_offer_correct:
        err("No valid offer, setting empty offer")
        state.penalty += 1
        offer = m.TradeOffer()

    return offer

def send_offer(offer: m.TradeOffer) -> m.OfferReply:
    req = m.OfferRequest(cards=offer.offered_cards, from_ip=_state.CONFIG.get("self_ip", ""), ask=offer.ask)
    debug(f"send_offer: sending offer to {offer.to}: {req.cards}, ask: {req.ask}")
    try:
        result = http_post(f"{offer.to}/offer", req.to_dict(), timeout=120)
    except urllib.error.HTTPError as e:
        warn(f"send_offer: {offer.to} rejected offer with {e.code}, treating as no deal")
        return m.OfferReply()
    reply = m.OfferReply.from_dict(result)
    debug(f"send_offer: received response: accepted={reply.accepted} offer={reply.offer}, reason={reply.reason!r}")
    return reply

def do_consider_offer(
        my_offer: list[str],
        my_reason: str,
        their_offer: list[str],
        their_reason: str,
        their_fields: dict[str, list[str]],
        from_ip: str) -> m.ConsideringReply:
    with lock:
        snapshot = state.to_dict()
    reply: m.ConsideringReply = _dm().get_considering_reply(snapshot, my_offer, my_reason, their_offer, their_reason, their_fields, from_ip)
    debug(f"do_consider_offer: accepted={reply.accepted}, offer={reply.offer}, reason={reply.reason!r}")
    return reply

def do_exchange(sending_cards: m.Cards, receiving_cards: m.Cards, partner_ip: str) -> tuple[bool, dict[str, Any]]:
    debug(f"do_exchange: executing trade with {partner_ip}, sending {sending_cards}, receiving {receiving_cards}")
    req = m.TradeRequest(
        getting=sending_cards,
        sending=receiving_cards,
        from_ip=_state.CONFIG.get("self_ip", ""),
    )

    result = http_post(f"{partner_ip}/trade", req.to_dict())
    resp = m.TradeResponse.from_dict(result)
    if not resp.success:
        err(f"do_exchange: trade execution failed: {resp.error or 'unknown error'}")
        return False, {"error": f"trade execution failed: {resp.error or 'unknown error'}"}

    debug("response received")

    with lock:
        for c in sending_cards:
            if c in state.new_cards:
                state.new_cards.remove(c)
            elif c in state.hand:
                state.hand.remove(c)
            else:
                err(f"{c} is not in my deck")

        state.new_cards.extend(receiving_cards)
        snapshot = state.to_dict()

    log(f"do_exchange: trade complete — sent {sending_cards}, received {receiving_cards}")
    return True, {"action": "trade", "offered": sending_cards, "received": receiving_cards, "state": snapshot}

# ── Game phase functions ───────────────────────────────────────────────────────


def plant_from_hand() -> tuple[bool, dict[str, Any]]:
    debug("plant_from_hand: asking LLM for planting action")
    got_valid_action = False
    actions: m.PlantingAction = m.PlantingAction()
    retries = 0
    while(not got_valid_action and retries < NBR_OF_RETRIES):
        with lock:
            snap = state.to_dict()
        actions = _dm().get_planting_action(snap)

        got_valid_action = actions.is_valid(state.hand)

        if not got_valid_action:
            retries += 1
            warn(f"plant_from_hand: LLM returned no valid action, retry {retries}")
            continue

    if not got_valid_action:
        state.penalty += 1
        err(f"MAJOR ERROR hand:{state.hand}, set of actions: {actions.fields}")
        return False, {"error": "no valid planting action"}
    else:
        for selected_field in actions.exec_order(state.hand):
            success, result = do_plant("hand", state.hand[0], selected_field)
            if not success:
                success, result = do_harvest([selected_field])
                success, result = do_plant("hand", state.hand[0], selected_field)

            debug(f"{result}")

    return do_deal(2)


def trading() -> bool:
    debug("trading: starting trading phase")
    other_fields: dict[str, dict[str, list[str]]] = get_other_fields()
    previous_offers: list[str] = []
    in_return: list[str] = []
    reason = ""
    rounds = 0

    while rounds < NBR_OF_TRADING:  # limit to 3 rounds of offers/counteroffers to avoid infinite loops
        debug(f"<<ROUND {rounds} >>")
        offer: m.TradeOffer = do_prepare_offer(other_fields, previous_offers, in_return, reason)

        if not offer.to:
            break

        if offer.to not in [_state.CONFIG.get("player1_ip"), _state.CONFIG.get("player2_ip")]:
            err(f"Invalid IP: {offer.to}")
            _state.state.penalty += 1
            return False

        if not (Counter(offer.offered_cards) <= Counter(state.hand + state.new_cards)):
            rounds += 1
            continue

        receiver_fields = other_fields.get(offer.to, {})

        answer: m.OfferReply = send_offer(offer)
        debug(f"raw answer >> {answer}")

        if not answer.accepted:
            debug("No interested in this offer")
            previous_offers = offer.offered_cards
            in_return = answer.offer
            reason = answer.reason
            rounds += 1
            continue

        accepting: m.ConsideringReply = do_consider_offer(
            my_offer=offer.offered_cards,
            my_reason=offer.ask,
            their_offer=answer.offer,
            their_reason=answer.reason,
            their_fields=receiver_fields,
            from_ip=offer.to,
        )
        debug(f"My offer {offer.offered_cards} | Their offer {answer.offer}")
        if accepting.accepted:
            debug("trading: offer accepted, executing exchange")
            do_exchange(
                sending_cards=offer.offered_cards,
                receiving_cards=answer.offer,
                partner_ip=offer.to,
            )
            break
        else:
            debug("trading: offer rejected or no response, preparing next offer")
            previous_offers = offer.offered_cards
            in_return = answer.offer
            reason = answer.reason
            rounds += 1
    debug("trading: done")
    return True


def forced_planting() -> int:
    debug("FORCED: starting forced planting phase")
    with lock:
        if not state.new_cards:
            debug("FORCED: no new cards, skipping")
            return 0
    retries = 0
    actions: m.NewCardPlantingAction = m.NewCardPlantingAction()
    while not actions.is_valid(state.new_cards) and retries < NBR_OF_RETRIES:
        with lock:
            snap = state.to_dict()
        actions = _dm().get_new_card_action(snap)

        if not actions.is_valid(state.new_cards):
            warn(f"FORCED: LLM returned no valid action, retry {retries + 1}")
            retries += 1
            continue

    mapped_cards: dict[str, m.Cards]
    if not actions.is_valid(state.new_cards):
        state.penalty += 1
        err(f"Still no valid action after retries: {actions.fields} new_cards: {state.new_cards}")
        mapped_cards = {
            "field1": m.Cards([v for ind, v in enumerate(state.new_cards) if ind % 3 == 0]),
            "field2": m.Cards([v for ind, v in enumerate(state.new_cards) if ind % 3 == 1]),
            "field3": m.Cards([v for ind, v in enumerate(state.new_cards) if ind % 3 == 2]),
        }
    else:
        mapped_cards = {k: m.Cards(v) for k, v in actions.fields.items()}

    for field in mapped_cards:
        for card in mapped_cards[field]:
            if not _field_accepts(card, field):
                do_harvest([field])  # try to make space by harvesting first

            success, result = do_plant("new_cards", card, field)
            if not success:
                err(f"FORCED: failed to plant {card!r} on {field}: {result.get('error', 'unknown error')}")
            else:
                log(f"FORCED: planted {card!r} on {field} as suggested by LLM")

    if len(state.new_cards) > 0:
        err(f"Forced planting failed, remaining cards: {state.new_cards}")
    debug("FORCED: done")
    return retries

def closing_turn() -> bool:
    """Returns True if the game continues, False if the deck is exhausted."""
    debug("closing_turn: dealing 3 cards and ending turn")

    do_deal(3)
    result = http_get(f"{_state.CONFIG['deck_ip']}/endturn")
    end = m.EndTurnResponse.from_dict(result)
    if end.game_over:
        err(f"GAME OVER: the deck is exhausted\nPenalties: {state.penalty}\nCoins: {state.coins}")
        return False
    debug("closing_turn: done")
    return True


def cash_out() -> None:
    """Game over: harvest every standing field, so no stack is lost with the deck. One /return per
    field (the deck counts beans per request), all under the lock, so /state answers only once the
    coins are in."""
    try:
        with lock:
            for f in ("field1", "field2", "field3"):
                cards = getattr(state, f).cards
                if not cards:
                    continue
                result = http_post(f"{_state.CONFIG['deck_ip']}/return", {"cards": list(cards)})
                state.coins += m.ReturnResponse.from_dict(result).coins
                getattr(state, f).cards = []
            coins = state.coins
        log(f"GAME OVER: fields cashed out, coins={coins}")
    except Exception as e:
        err(f"cash_out failed: {e}")


def start_new_turn() -> None:
    to_continue: bool = True
    log(f"START {state.print}")
    if state.new_cards:
        forced_planting()
    to_continue, _ = plant_from_hand()
    
    if to_continue:
        trading()
        forced_planting()
    closing_turn()
    log(f"END {state.print}")
