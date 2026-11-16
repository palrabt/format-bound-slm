#!/usr/bin/env python3
"""The training corpus: the states of a corpus, answered by a rule-based bot (game/player/bots.py).

    python3 -m training.generate_data.bot_corpus --bot bot_reference \
        --states training/corpus/training_data_reference_15000.txt --output /tmp/check.txt

Every state line of --states is copied byte for byte and only its answer is replaced by the bot's.
The shipped corpus (training/corpus/training_data_reference_15000.txt) was made this way from the
15,000 states of an earlier, partly random teacher's corpus (synth.py's states, 3,000 per message
type, their free-text fields reworded by Phi-4); its states are kept in it, so relabelling it again
with the reference bot and seed 0 gives the same file.

The bot decides; the text of its answer is worded with synth.py's templates (one of them picked by a
generator of its own, seeded by --seed), naming the bean the bot wants. Message by message:
    PLANTING     the bot's planting
    FORCED       the bot's forced planting
    TRADING      the bot's offer (or a pass); the ask names the cards and the bean wanted: its
                 field closest to its next coin, else a bean of its hand or new cards
    REPLY        the bot's accept, with the cards it gives back, or a rejection naming the bean it
                 wants; the bots never counter-offer
    CONSIDERING  the bot's accept or reject; the bots never propose other cards
"""

import argparse
import json
import random
from pathlib import Path

from game.player import bots
from training.generate_data.cli import REJECT_REASONS, bean_list
from training.generate_data.synth import (_CONSIDERING_ACCEPT, _CONSIDERING_REJECT, _REPLY_ACCEPT_NO_RETURN,
                                          _REPLY_ACCEPT_WITH_RETURN, _TRADE_ASK, CARDS, _progress_to_next_coin)

FIELDS = ("field1", "field2", "field3")
PEER = {"0": "http://player0", "1": "http://player1"}  # the corpus names the other players "0"/"1"
INDEX = {ip: i for i, ip in PEER.items()}


def _player(fields: dict, **rest) -> dict:
    """A corpus state in the shape the game hands a bot (player.state.to_dict)."""
    return {"hand": [], "new_cards": [], **{f: fields[f] for f in FIELDS}, "coins": 0, "penalty": 0, **rest}


def _want(fields: dict, pool: list[str], exclude: list[str], rng: random.Random) -> str:
    """The bean to ask for: the own field closest to its next coin, else a bean held, else any."""
    growing = [fields[f]["cards"] for f in FIELDS if fields[f]["cards"] and fields[f]["cards"][0] not in exclude]
    if growing:
        best = max(growing, key=lambda c: _progress_to_next_coin(c[0], len(c)))
        return best[0]
    return rng.choice(sorted(set(pool) - set(exclude)) or [c for c in CARDS if c not in exclude])


def answer(bot, state: dict, rng: random.Random) -> dict:
    """The bot's answer to one corpus state, in the corpus's JSON shape."""
    phase = state["phase"]
    if phase in ("PLANTING", "FORCED"):
        s = _player(state["fields"], hand=state.get("hand", []), new_cards=state.get("new_cards", []))
        action = bot.get_planting_action(s) if phase == "PLANTING" else bot.get_new_card_action(s)
        return {f: list(action.fields[f]) for f in FIELDS}

    if phase == "TRADING":
        s = _player(state["fields"], hand=state["hand"], new_cards=state["new_cards"])
        others = {PEER[i]: fields for i, fields in state["other_players"].items()}
        offer = bot.get_trade_offer(s, others, state["previous_offers"], state["counter_offer"], state["reason"])
        if not offer.to:
            return {"offered_cards": [], "to": "", "ask": ""}
        cards = list(offer.offered_cards)
        want = _want(state["fields"], state["hand"] + state["new_cards"], cards, rng)
        return {"offered_cards": cards, "to": INDEX[offer.to],
                "ask": rng.choice(_TRADE_ASK).format(card=bean_list(cards), want=want)}

    if phase == "REPLY":
        s = _player(state["fields"], hand=state["hand"])
        reply = bot.get_REPLY(s, state["offered_cards"], PEER[state["from_player"]], state["asking_for"])
        back = list(reply.offer)
        if reply.accepted:
            reason = (rng.choice(_REPLY_ACCEPT_WITH_RETURN).format(cards=", ".join(back)) if back
                      else rng.choice(_REPLY_ACCEPT_NO_RETURN))
            return {"accepted": True, "offer": back, "reason": reason}
        want = _want(state["fields"], state["hand"], state["offered_cards"], rng)
        return {"accepted": False, "offer": [],
                "reason": rng.choice(REJECT_REASONS).format(offered=bean_list(state["offered_cards"]), want=want)}

    if phase == "CONSIDERING":
        s = _player(state["my_fields"], hand=state["hand"], new_cards=state["new_cards"])
        reply = bot.get_considering_reply(s, state["my_offers"], state["my_reason"], state["their_offers"],
                                          state["their_reason"], state["their_fields"], PEER[state["from_player"]])
        return {"accepted": reply.accepted, "offer": [],
                "reason": rng.choice(_CONSIDERING_ACCEPT if reply.accepted else _CONSIDERING_REJECT)}

    raise ValueError(f"unknown phase {phase!r}")


def relabel(kind: str, states: Path, output: Path, seed: int = 0) -> int:
    """Every entry of the corpus `states`, its state line kept as written, answered by bot `kind`."""
    rng = random.Random(f"text-{seed}")  # the wording
    bot = bots.BOTS[kind]()
    total = 0
    with open(output, "w", encoding="utf-8") as f:
        for chunk in states.read_text(encoding="utf-8").strip().split("\n\n"):
            lines = [line for line in chunk.strip().split("\n") if line.strip()]
            if len(lines) < 2 or not lines[1].startswith("[JSON]"):
                continue
            response = answer(bot, json.loads(lines[0]), rng)
            f.write(f"\n{lines[0]}\n[JSON] {json.dumps(response, separators=(', ', ': '))}\n")
            total += 1
    return total


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--bot", choices=list(bots.BOTS), default="bot_reference", help="the bot that decides")
    parser.add_argument("--states", type=Path, required=True, help="the corpus whose states are answered")
    parser.add_argument("--output", type=Path, required=True, help="output file")
    parser.add_argument("--seed", type=int, default=0, help="the wording's seed (default 0)")
    args = parser.parse_args()
    total = relabel(args.bot, args.states, args.output, seed=args.seed)
    print(f"{args.bot}: written {total} entries, the states of {args.states} -> {args.output}")


if __name__ == "__main__":
    main()
