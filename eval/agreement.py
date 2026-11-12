"""Agreement: given the same item, do two settings make the same decision?

The settings are the conditions of one replay run (prompt style, adapter on or off) and, across
runs, the same condition run twice (e.g. on the GPU and on the CPU). The decision is what
legality.py reads from the answer — the planting plan; a pass, or the cards offered and to whom;
accept or reject and the cards given — whether or not it is legal. Items where either answer
cannot be read are left out; the number of compared items says how many remain.

Only replay runs share items: every tournament condition plays its own games.
"""

from eval.tables import ci, markdown

PHASES = ("PLANTING", "FORCED", "TRADING", "REPLY", "CONSIDERING")


def decisions(records) -> dict[str, tuple[str, tuple | None]]:
    """records: (item key, phase, decision) -> {item key: (phase, decision)}. evaluate.py keys an
    answer by its replay item's id, or — in tournaments — by its state and occurrence."""
    return {key: (phase, decision) for key, phase, decision in records}


def compare(a: dict, b: dict) -> dict:
    """Share of shared, readable items on which the two decision maps agree, overall and per phase."""
    phases = {phase: {"n": 0, "same": 0} for phase in PHASES}
    for key in a.keys() & b.keys():
        (phase, da), (_, db) = a[key], b[key]
        if da is None or db is None:
            continue
        phases[phase]["n"] += 1
        phases[phase]["same"] += da == db
    return {"n": sum(p["n"] for p in phases.values()), "same": sum(p["same"] for p in phases.values()),
            "phases": phases}


def table(model: str, labels: list[str], pairs: dict[tuple[str, str], dict]) -> list[str]:
    """One model's agreement matrix over `labels` (conditions, or runs)."""
    body = []
    for a in labels:
        row = [a]
        for b in labels:
            r = pairs.get((a, b)) or pairs.get((b, a))
            row.append("·" if a == b else (f"{ci(r['same'], r['n'])} ({r['n']})" if r else "–"))
        body.append(row)
    return markdown([model, *labels], body)
