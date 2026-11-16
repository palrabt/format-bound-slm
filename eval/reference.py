"""Reference-correctness: does the answer make the decision the reference bot makes in the same state?

The reference bot (game/player/bots.py) is the adapters' teacher: it answered every state of their
training corpus (training/corpus/training_data_reference_15000.txt). Each answer is compared with the
bot's answer to the same state. The bot is asked through the call the game makes (replay.py's
ask_arguments recovers the call's arguments from the logged state) and its message is read like a
model's (legality.judge), so the two decisions compare as in agreement.py:

    PLANTING, FORCED  the planting plan: which cards go on which field
    TRADING           a pass, or the cards offered and the player they go to
    REPLY             accept or reject, and the cards given in return
    CONSIDERING       accept or reject, and the cards given in return (the bot gives none)

An answer is correct when it is legal (legality.py) and makes the bot's decision. Its free text is not
compared, and an unreadable or illegal answer is wrong.
"""

import json
from functools import lru_cache

from eval import legality
from eval.tables import ci, markdown, pct
from game.player.bots import bot
from replay import ASK, ask_arguments

PHASES = ("PLANTING", "FORCED", "TRADING", "REPLY", "CONSIDERING")
REFERENCE = "bot_reference"


@lru_cache(maxsize=None)
def _decision(state: str, peers: str):
    s, p = json.loads(state), json.loads(peers)
    return legality.judge(s, getattr(bot(REFERENCE), ASK[s["phase"]])(*ask_arguments(s, p)), p).decision


def decision(state: dict, peers: dict[str, str]):
    """The reference bot's decision in the state (one bot call per distinct state)."""
    return _decision(json.dumps(state, sort_keys=True), json.dumps(peers, sort_keys=True))


def check(state: dict, peers: dict[str, str], verdict: legality.Verdict) -> bool:
    """Is the answer (legality.check's verdict) legal and the reference bot's decision?"""
    return verdict.legal and verdict.decision is not None and verdict.decision == decision(state, peers)


def summarize(records) -> dict:
    """records: (phase, correct) per answer."""
    phases = {phase: {"n": 0, "correct": 0} for phase in PHASES}
    for phase, correct in records:
        phases[phase]["n"] += 1
        phases[phase]["correct"] += correct
    return {"n": sum(p["n"] for p in phases.values()), "correct": sum(p["correct"] for p in phases.values()),
            "phases": phases}


def table(rows: list[tuple[list[str], dict]]) -> list[str]:
    body = [cells + [ci(s["correct"], s["n"])] + [pct(s["phases"][p]["correct"], s["phases"][p]["n"]) for p in PHASES]
            for cells, s in rows]
    return markdown(["condition", "model", "correct (95% CI)", *PHASES], body)
