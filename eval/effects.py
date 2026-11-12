"""Effects: how much do the adapter and the prompt style change an outcome, item by item?

All conditions of a replay answer the same items, so an effect is a paired difference: the share
of items where an outcome holds in one condition minus another, for one model —
    adapter effect   lora_<prompt> − base_<prompt>, for each prompt style
    prompt effect    <prompt> − verbose, for each of base model and adapter
for three outcomes: schema-valid (valid@1), legal, and reference-correct (reference.py). Each
difference comes with a 95% paired-bootstrap interval (resampling items), the exact McNemar p of
the items where the two conditions disagree, and that p Holm-adjusted over its table (one family:
one outcome, one slice, all models and contrasts).
"""

from eval.stats import holm, mcnemar, paired_bootstrap
from eval.tables import markdown, pct

OUTCOMES = ("schema-valid", "legal", "reference-correct")
BASELINE_PROMPT = "verbose"


def contrasts(conditions: list[str]) -> list[tuple[str, str, str]]:
    """(label, condition A, condition B) for the effects the run's conditions allow."""
    pairs = []
    prompts = [c.split("_", 1)[1] for c in conditions if c.startswith("base_") and f"lora_{c[5:]}" in conditions]
    for prompt in prompts:
        pairs.append((f"adapter at {prompt}", f"base_{prompt}", f"lora_{prompt}"))
    for adapter in ("base", "lora"):
        for prompt in [c.split("_", 1)[1] for c in conditions if c.startswith(f"{adapter}_")]:
            if prompt != BASELINE_PROMPT and f"{adapter}_{BASELINE_PROMPT}" in conditions:
                pairs.append((f"{adapter}: {prompt} vs {BASELINE_PROMPT}", f"{adapter}_{BASELINE_PROMPT}",
                              f"{adapter}_{prompt}"))
    return pairs


def compare(a: dict[str, bool], b: dict[str, bool]) -> dict:
    """a, b: {item key: outcome} of two conditions. Items both answered are paired."""
    keys = sorted(a.keys() & b.keys())
    x, y = [a[k] for k in keys], [b[k] for k in keys]
    only_a = sum(1 for i, j in zip(x, y) if i and not j)
    only_b = sum(1 for i, j in zip(x, y) if j and not i)
    low, high = paired_bootstrap(x, y)
    return {"n": len(keys), "a": sum(x), "b": sum(y), "only_a": only_a, "only_b": only_b,
            "delta": (sum(y) - sum(x)) / len(keys) if keys else None, "ci": (low, high), "p": mcnemar(only_a, only_b)}


def effects(outcomes: dict[str, dict[str, dict[str, dict[str, bool]]]], conditions: list[str],
            models: list[str] | None = None) -> dict:
    """outcomes[condition][model][outcome] = {item key: bool} -> {outcome: [row, ...]} with Holm p.
    Rows follow `models` (default: sorted)."""
    result = {}
    models = models or sorted({m for by_model in outcomes.values() for m in by_model})
    for outcome in OUTCOMES:
        rows = []
        for model in models:
            for label, ca, cb in contrasts(conditions):
                a = outcomes.get(ca, {}).get(model, {}).get(outcome)
                b = outcomes.get(cb, {}).get(model, {}).get(outcome)
                if a is not None and b is not None:
                    rows.append({"model": model, "contrast": label, "a": ca, "b": cb, **compare(a, b)})
        for row, adjusted in zip(rows, holm([r["p"] for r in rows])):
            row["p_holm"] = adjusted
        result[outcome] = rows
    return result


def _p(p: float) -> str:
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def table(rows: list[dict]) -> list[str]:
    body = []
    for r in rows:
        if not r["n"]:
            continue
        mark = " *" if r["p_holm"] < 0.05 else ""
        body.append([r["model"], r["contrast"], r["n"], pct(r["a"], r["n"]), pct(r["b"], r["n"]),
                     f"{100 * r['delta']:+.0f} [{100 * r['ci'][0]:+.0f}, {100 * r['ci'][1]:+.0f}]",
                     f"{r['only_a']} / {r['only_b']}", _p(r["p"]), _p(r["p_holm"]) + mark])
    return markdown(["model", "effect", "items", "A", "B", "B − A in points [95% CI]", "only A / only B",
                     "McNemar p", "Holm p"], body)
