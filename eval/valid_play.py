"""Valid play: does the answer keep every rule the teacher plays by?

The reference bot (game/player/bots.py), the adapters' teacher, plays the deterministic rules of an
earlier, partly random teacher (training/generate_data/synth.py) with its random or arbitrary parts
replaced by value rules. Valid play asks whether an answer keeps these rules; reference-correctness
(reference.py) asks whether it makes the bot's exact decision. Where the rules allow several answers
(a tie, any spare bean, either partner, passing), each of them is valid play. In brackets, synth.py:

    PLANTING     the first card goes onto a field growing the same bean, else onto an empty field,
                 else onto the field with the least progress towards its next coin (ties: any).
                 The second card is optional, but never planted with a harvest.
                 [synth.py: field1 when nothing fits; plants the second card at random]
    FORCED       no harvest when the new cards fit without one; when one is unavoidable, the stacks
                 lost are worth no more than synth.py's choice (least progress towards the next
                 coin).                                       [synth.py: the same rule]
    TRADING      pass, or offer only beans the player is not growing (when it has any).
                 [synth.py: also passes at random, picks the partner at random]
    REPLY        accept exactly when the offered cards include a bean the player grows; the cards
                 given in return never include a bean the player grows.
                 [synth.py: accepts 40% of useless offers; may give back the bean it receives]
    CONSIDERING  accept exactly when the counter-offer includes a bean the player grows.
                 [synth.py: accepts 45% of useless counter-offers]

An answer is valid play when it is legal (legality.py) and keeps every rule of its message type; an
unreadable or illegal answer keeps no rule. Each rule is also counted on its own (partial credit).
"""

from eval.legality import FIELDS
from eval.state_sensitivity import _fits_without_harvest, _harvests, _types
from eval.tables import ci, markdown, pct
from training.generate_data.synth import _auto_forced, _progress_to_next_coin

PHASES = ("PLANTING", "FORCED", "TRADING", "REPLY", "CONSIDERING")
RULES = {
    "PLANTING": ("first card placed", "second card without harvest"),
    "FORCED": ("no avoidable harvest", "least valuable stack lost"),
    "TRADING": ("keeps growing beans",),
    "REPLY": ("accepts iff useful", "keeps growing beans"),
    "CONSIDERING": ("accepts iff useful",),
}


def _progress(field: dict) -> float:
    cards = field["cards"]
    return _progress_to_next_coin(cards[0], len(cards)) if cards else 0.0


def _stacks_lost(fields: dict, plan: dict) -> float:
    """Progress of the existing stacks a planting plan harvests: any bean planted on a field that
    grows another one harvests it, even after more of the field's own bean was added."""
    return sum(_progress(fields[f]) for f in FIELDS
               if fields[f]["cards"] and any(card != fields[f]["cards"][0] for card in plan[f]))


def _planting(state: dict, plan: dict) -> dict:
    fields, hand = state["fields"], state["hand"]
    first = hand[0]
    placed = next(f for f in FIELDS if first in plan[f])  # the field the game plants it on (exec_order)
    same = [f for f in FIELDS if fields[f]["cards"] and fields[f]["cards"][0] == first]
    empty = [f for f in FIELDS if not fields[f]["cards"]]
    if same or empty:
        ok_first = placed in (same or empty)
    else:
        least = min(_progress(fields[f]) for f in FIELDS)
        ok_first = _progress(fields[placed]) <= least + 1e-9
    second = [c for f in FIELDS for c in plan[f]]
    no_second_harvest = True
    if len(second) == 2:
        after = {f: list(fields[f]["cards"]) for f in FIELDS}
        after[placed] = after[placed] + [first] if after[placed] and after[placed][0] == first else [first]
        rest = {f: list(plan[f]) for f in FIELDS}
        rest[placed].remove(first)
        target = next(f for f in FIELDS if rest[f])
        no_second_harvest = not after[target] or after[target][0] == rest[target][0]
    return {"first card placed": ok_first, "second card without harvest": no_second_harvest}


def _forced(state: dict, plan: dict) -> dict:
    fields = state["fields"]
    if _fits_without_harvest(fields, state["new_cards"]):
        return {"no avoidable harvest": _harvests(fields, plan) == 0, "least valuable stack lost": True}
    teacher_loss = _stacks_lost(fields, _auto_forced(state))
    return {"no avoidable harvest": True, "least valuable stack lost": _stacks_lost(fields, plan) <= teacher_loss + 1e-9}


def check(state: dict, verdict) -> dict:
    """{"valid": bool, "rules": {rule: bool}} for one answer (legality.check's verdict)."""
    phase = state["phase"]
    if not verdict.legal:
        return {"valid": False, "rules": {rule: False for rule in RULES[phase]}}
    message = verdict.message
    if phase == "PLANTING":
        rules = _planting(state, message.fields)
    elif phase == "FORCED":
        rules = _forced(state, message.fields)
    elif phase == "TRADING":
        cards = list(message.offered_cards) if message is not None else []
        growing = _types(state["fields"])
        spare = [c for c in state.get("hand", []) + state.get("new_cards", []) if c not in growing]
        rules = {"keeps growing beans": not cards or not spare or not set(cards) & growing}
    elif phase == "REPLY":
        growing = _types(state["fields"])
        useful = bool(set(state["offered_cards"]) & growing)
        rules = {"accepts iff useful": bool(message.accepted) == useful,
                 "keeps growing beans": not set(message.offer) & growing}
    else:
        useful = bool(set(state["their_offers"]) & _types(state["my_fields"]))
        rules = {"accepts iff useful": bool(message.accepted) == useful}
    return {"valid": all(rules.values()), "rules": rules}


def summarize(records) -> dict:
    """records: (phase, check result) per answer."""
    phases = {phase: {"n": 0, "valid": 0, "rules": {rule: 0 for rule in RULES[phase]}} for phase in PHASES}
    for phase, result in records:
        p = phases[phase]
        p["n"] += 1
        p["valid"] += result["valid"]
        for rule, ok in result["rules"].items():
            p["rules"][rule] += ok
    return {"n": sum(p["n"] for p in phases.values()), "valid": sum(p["valid"] for p in phases.values()),
            "phases": phases}


def table(rows: list[tuple[list[str], dict]]) -> list[str]:
    body = [cells + [ci(s["valid"], s["n"])] + [pct(s["phases"][p]["valid"], s["phases"][p]["n"]) for p in PHASES]
            for cells, s in rows]
    return markdown(["condition", "model", "valid play (95% CI)", *PHASES], body)


def rules_table(rows: list[tuple[list[str], dict]]) -> list[str]:
    names = [(phase, rule) for phase in PHASES for rule in RULES[phase]]
    body = [cells + [pct(s["phases"][phase]["rules"][rule], s["phases"][phase]["n"]) for phase, rule in names]
            for cells, s in rows]
    return markdown(["condition", "model", *[f"{phase[:5]}: {rule}" for phase, rule in names]], body)
