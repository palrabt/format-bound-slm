"""Schema validity (valid@1): is the whole answer one JSON value that matches its message type's
schema, game/schemas/output/<phase>.schema.json?

The schema checks the keys (all required, none extra), the types, the card names, at most two
cards per field when planting, and the player a trade goes to; TRADING may also be null or an
empty offer (a pass). Nothing is extracted or repaired: an answer with text around the JSON fails.
Every answer counts, so this is the share of first attempts the game could use without help.

Failure types:
    empty       nothing was written
    wrapped     JSON object inside other text (prose, code fences) — the game's parser would find it
    not_json    no JSON object at all
    schema:<k>  JSON that breaks the schema; <k> is the rule (required, additionalProperties,
                type, enum, maxItems, ...)
"""

import json
from collections import Counter
from pathlib import Path

from jsonschema import Draft7Validator
from jsonschema.exceptions import best_match

from eval.tables import frac, markdown, pct
from game.player.prompts.common import extract_json

PHASES = ("PLANTING", "FORCED", "TRADING", "REPLY", "CONSIDERING")
SCHEMA_DIR = Path(__file__).resolve().parent.parent / "game" / "schemas" / "output"
_VALIDATORS = {phase: Draft7Validator(json.loads((SCHEMA_DIR / f"{phase.lower()}.schema.json").read_text()))
               for phase in PHASES}


def check(phase: str, raw: str) -> str | None:
    """None when the answer is schema-valid, otherwise its failure type."""
    text = raw.strip()
    if not text:
        return "empty"
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        return "wrapped" if extract_json(text) else "not_json"
    error = best_match(_VALIDATORS[phase].iter_errors(value))
    return None if error is None else f"schema:{error.validator}"


def summarize(records) -> dict:
    """records: (phase, failure type or None) per answer."""
    phases = {phase: {"n": 0, "valid": 0} for phase in PHASES}
    failures = Counter()
    for phase, failure in records:
        phases[phase]["n"] += 1
        phases[phase]["valid"] += failure is None
        if failure:
            failures[failure] += 1
    return {"n": sum(p["n"] for p in phases.values()), "valid": sum(p["valid"] for p in phases.values()),
            "phases": phases, "failures": dict(failures.most_common())}


def table(rows: list[tuple[list[str], dict]]) -> list[str]:
    """rows: (leading cells, summary)."""
    body = []
    for cells, s in rows:
        failures = ", ".join(f"{k} {v}" for k, v in list(s["failures"].items())[:3]) or "–"
        body.append(cells + [frac(s["valid"], s["n"])]
                    + [pct(s["phases"][p]["valid"], s["phases"][p]["n"]) for p in PHASES] + [failures])
    return markdown(["condition", "model", "valid", *PHASES, "main failures"], body)
