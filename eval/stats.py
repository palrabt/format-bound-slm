"""Confidence intervals and paired tests for the report's rates.

Every rate in the report is a share of items, and the conditions of a replay answer the same
items, so differences between conditions are paired:
    wilson            95% Wilson score interval of a share
    mcnemar           exact two-sided McNemar test: of the items where two settings differ, are
                      the changes in one direction more often than chance?
    paired_bootstrap  95% interval of a paired difference of shares, resampling items
    holm              Holm–Bonferroni adjustment over a family of tests
"""

from math import sqrt

import numpy as np
from scipy.stats import binomtest

Z95 = 1.959963984540054
BOOTSTRAP_REPS = 2000


def wilson(k: int, n: int, z: float = Z95) -> tuple[float, float] | None:
    if not n:
        return None
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def mcnemar(b: int, c: int) -> float:
    """b: items only the first setting got right; c: only the second."""
    return 1.0 if b + c == 0 else float(binomtest(b, b + c, 0.5).pvalue)


def paired_bootstrap(x: list[bool], y: list[bool], reps: int = BOOTSTRAP_REPS, seed: int = 0) -> tuple[float, float]:
    """95% interval of share(y) − share(x) over paired items."""
    if not x:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    a, b = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    idx = rng.integers(0, len(a), size=(reps, len(a)))
    diffs = (b[idx] - a[idx]).mean(axis=1)
    return float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))


def holm(pvalues: list[float]) -> list[float]:
    """Holm-adjusted p-values, in the order given."""
    m = len(pvalues)
    adjusted = [1.0] * m
    running = 0.0
    for rank, i in enumerate(sorted(range(m), key=lambda j: pvalues[j])):
        running = max(running, min(1.0, (m - rank) * pvalues[i]))
        adjusted[i] = running
    return adjusted
