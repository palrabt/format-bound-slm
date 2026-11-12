"""Formatting shared by the metrics' report tables."""

from eval.stats import wilson


def pct(part: int, whole: int) -> str:
    """'95%' — or '–' when there is nothing to divide by."""
    return f"{100 * part / whole:.0f}%" if whole else "–"


def frac(part: int, whole: int) -> str:
    """'19/20 (95%)'."""
    return f"{part}/{whole} ({pct(part, whole)})" if whole else "–"


def ci(part: int, whole: int) -> str:
    """'95% [76–99]': the share with its 95% Wilson interval."""
    interval = wilson(part, whole)
    if interval is None:
        return "–"
    return f"{100 * part / whole:.0f}% [{100 * interval[0]:.0f}–{100 * interval[1]:.0f}]"


def markdown(header: list[str], rows: list[list[str]]) -> list[str]:
    """A Markdown table, one line per row."""
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return lines
