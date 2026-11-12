"""State sensitivity: does the decision depend on the game state?

A model that answers the same whatever the state — always accepts, always plants on field 1 —
passes every format and legality check, so these numbers look at what was decided, over the legal
answers:

    REPLY, CONSIDERING  accept rate when the cards on offer include a bean already growing in one
                        of the player's fields ("useful") and when they do not ("useless"); the gap
                        between the two is ~0 for a policy that ignores the offer
    PLANTING, FORCED    avoidable harvests: the answer replaces a field's bean although the cards
                        that had to be planted fit on empty or same-bean fields (in PLANTING only
                        the first card has to be planted, so harvesting for the second never has to
                        happen)
    TRADING             passes, and offers that give away a bean the player is growing

evaluate.py also scores the training corpus this way (the "teacher" row): the teacher's own
decisions are partly random, so they are the reference, not 100%.
"""

from itertools import permutations

from eval.tables import frac, markdown, pct

FIELDS = ("field1", "field2", "field3")


def _types(fields: dict) -> set[str]:
    """The beans growing in a player's fields."""
    return {fields[f]["cards"][0] for f in FIELDS if fields.get(f, {}).get("cards")}


def _harvests(fields: dict, plan: dict) -> int:
    """How many times planting `plan` (field -> cards, in order) replaces a field's bean."""
    current = {f: list(fields[f]["cards"]) for f in FIELDS}
    count = 0
    for f in FIELDS:
        for card in plan[f]:
            if current[f] and current[f][0] != card:
                count += 1
                current[f] = []
            current[f].append(card)
    return count


def _fits_without_harvest(fields: dict, beans: list[str]) -> bool:
    """Each bean type gets its own empty or same-bean field."""
    kinds = sorted(set(beans))
    fits = lambda bean, f: not fields[f]["cards"] or fields[f]["cards"][0] == bean
    return len(kinds) <= 3 and any(all(fits(b, f) for b, f in zip(kinds, order))
                                   for order in permutations(FIELDS, len(kinds)))


def facts(state: dict, message) -> dict:
    """What one legal answer shows; `message` is the parsed game message (None for a TRADING null)."""
    phase = state["phase"]
    if phase in ("REPLY", "CONSIDERING"):
        fields = state["fields"] if phase == "REPLY" else state["my_fields"]
        incoming = state["offered_cards"] if phase == "REPLY" else state["their_offers"]
        return {"useful": bool(set(incoming) & _types(fields)), "accepted": bool(message.accepted)}
    if phase in ("PLANTING", "FORCED"):
        fields, plan = state["fields"], message.fields
        if phase == "PLANTING":
            needed = 0 if _fits_without_harvest(fields, state["hand"][:1]) else 1
            return {"avoidable_harvest": _harvests(fields, plan) > needed}
        return {"avoidable_harvest": _fits_without_harvest(fields, state["new_cards"]) and _harvests(fields, plan) > 0}
    cards = list(message.offered_cards) if message is not None else []
    if not cards:
        return {"pass": True, "gives_own_type": False}
    return {"pass": False, "gives_own_type": bool(set(cards) & _types(state["fields"]))}


def summarize(records) -> dict:
    """records: (phase, facts) per legal answer."""
    s = {"REPLY": {"useful": 0, "useful_accepted": 0, "useless": 0, "useless_accepted": 0},
         "CONSIDERING": {"useful": 0, "useful_accepted": 0, "useless": 0, "useless_accepted": 0},
         "PLANTING": {"n": 0, "avoidable_harvest": 0}, "FORCED": {"n": 0, "avoidable_harvest": 0},
         "TRADING": {"n": 0, "pass": 0, "offers": 0, "gives_own_type": 0}}
    for phase, f in records:
        if phase in ("REPLY", "CONSIDERING"):
            kind = "useful" if f["useful"] else "useless"
            s[phase][kind] += 1
            s[phase][f"{kind}_accepted"] += f["accepted"]
        elif phase in ("PLANTING", "FORCED"):
            s[phase]["n"] += 1
            s[phase]["avoidable_harvest"] += f["avoidable_harvest"]
        else:
            s[phase]["n"] += 1
            s[phase]["pass"] += f["pass"]
            s[phase]["offers"] += not f["pass"]
            s[phase]["gives_own_type"] += f["gives_own_type"]
    return s


def accept_gap(s: dict) -> float | None:
    """Accept rate on useful minus useless offers, in points."""
    if not s["useful"] or not s["useless"]:
        return None
    return 100 * (s["useful_accepted"] / s["useful"] - s["useless_accepted"] / s["useless"])


def _gap(s: dict) -> str:
    gap = accept_gap(s)
    return "–" if gap is None else f"{gap:+.0f}"


def table(rows: list[tuple[list[str], dict]]) -> list[str]:
    body = []
    for cells, s in rows:
        r, c = s["REPLY"], s["CONSIDERING"]
        body.append(cells + [
            f"{pct(r['useful_accepted'], r['useful'])} / {pct(r['useless_accepted'], r['useless'])}", _gap(r),
            f"{pct(c['useful_accepted'], c['useful'])} / {pct(c['useless_accepted'], c['useless'])}", _gap(c),
            frac(s["PLANTING"]["avoidable_harvest"], s["PLANTING"]["n"]),
            frac(s["FORCED"]["avoidable_harvest"], s["FORCED"]["n"]),
            pct(s["TRADING"]["pass"], s["TRADING"]["n"]),
            frac(s["TRADING"]["gives_own_type"], s["TRADING"]["offers"])])
    return markdown(["condition", "model", "REPLY accepts useful / useless", "gap", "CONSIDERING accepts useful / useless",
                     "gap", "PLANTING avoidable harvests", "FORCED avoidable harvests", "TRADING passes",
                     "offers giving away a growing bean"], body)
