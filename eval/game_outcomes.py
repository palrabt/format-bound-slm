"""Game outcomes: how many coins does a player earn against the same opponents and decks?

tournament.py has every evaluated player — an LLM under a condition, or a baseline bot — play the
same seeded games against two opponent bots (tournament.opponents: the reference rules or a random
legal player), in every seat, and writes one row per game (tournament_<player>.csv: seed, seat,
coins, penalty, the opponents' coins). Per player:
    coins           mean per game, with a 95% bootstrap interval over games
    opponents       the two opponents' mean coins in the same games
    wins            games where it earned more than both opponents
    penalty         invalid answers the game had to replace, per game
Each player is compared with the two baseline bots (bots.py) that played the same seeds and seats:
    vs reference    the paired difference in coins from the reference bot — the rule player's coins
                    are the bar
    vs random       the paired difference from the random legal player — the floor
each with a 95% bootstrap interval, the Wilcoxon signed-rank p and the Holm-adjusted p over every
comparison in its column (one family per baseline and run). "all models" pools a condition's
models: per game, their mean coins against the baseline's coins on the same seed (a game is the
unit, so the baseline's game is not counted three times).
Runs from before (all three LLMs in every game, tournament_*.csv with <identity>_coins columns) are
summarized per identity, and a `note` column, if a CSV has one (e.g. outcomes reconstructed after
the fact), is carried into the report.
"""

import csv
from pathlib import Path

import numpy as np
from scipy.stats import wilcoxon

from eval.stats import holm, paired_bootstrap
from eval.tables import markdown, pct

REFERENCE = "bot_reference"
RANDOM = "bot_random"
BASELINES = (REFERENCE, RANDOM)
ALL_MODELS = "all models"


def _bootstrap_mean(xs: list[float], reps: int = 2000, seed: int = 0) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    a = np.asarray(xs, dtype=float)
    means = a[rng.integers(0, len(a), size=(reps, len(a)))].mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def summarize(csv_paths: list[Path], identities: list[str]) -> dict:
    with open(csv_paths[0], newline="") as f:
        header = next(csv.reader(f), [])
    return _players(csv_paths) if "player" in header else _identities(csv_paths, identities)


def _players(csv_paths: list[Path]) -> dict:
    """Per evaluated player: its games (seed -> coins etc.) and their summary."""
    games: dict[str, dict[int, dict]] = {}
    for path in csv_paths:
        with open(path, newline="") as f:
            for row in csv.DictReader(f):
                if row.get("coins") in (None, ""):
                    continue
                opponents = [int(c) for c in row.get("opponent_coins", "").split(";") if c]
                games.setdefault(row["player"], {})[int(row["game"])] = {
                    "seat": int(row["seat"]), "finished": row.get("finished") == "True", "coins": int(row["coins"]),
                    "penalty": int(row["penalty_delta"] or 0), "opponents": opponents}
    players = {}
    for player, by_seed in games.items():
        coins = [g["coins"] for g in by_seed.values()]
        opp = [np.mean(g["opponents"]) for g in by_seed.values() if g["opponents"]]
        players[player] = {
            "games": len(by_seed), "finished": sum(g["finished"] for g in by_seed.values()),
            "coins": float(np.mean(coins)), "coins_ci": _bootstrap_mean(coins),
            "opponents": float(np.mean(opp)) if opp else None,
            "wins": sum(1 for g in by_seed.values() if g["opponents"] and g["coins"] > max(g["opponents"])),
            "penalty": float(np.mean([g["penalty"] for g in by_seed.values()])),
            "by_seed": {seed: g["coins"] for seed, g in by_seed.items()}}
    return {"format": "players", "players": players}


def _identities(csv_paths: list[Path], identities: list[str]) -> dict:
    """Old layout: every identity's coins in every game."""
    coins = {name: [] for name in identities}
    penalties = {name: [] for name in identities}
    games = finished = 0
    notes = set()
    for path in csv_paths:
        with open(path, newline="") as f:
            for row in csv.DictReader(f):
                games += 1
                finished += row.get("finished") == "True"
                if row.get("note"):
                    notes.add(row["note"])
                for name in identities:
                    c, p = row.get(f"{name}_coins"), row.get(f"{name}_penalty_delta")
                    if c not in (None, ""):
                        coins[name].append(int(c))
                    if p not in (None, ""):
                        penalties[name].append(int(p))
    mean = lambda xs: round(sum(xs) / len(xs), 2) if xs else None
    return {"format": "identities", "games": games, "finished": finished, "notes": sorted(notes),
            "players": {name: {"avg_coins": mean(coins[name]), "avg_penalty": mean(penalties[name])}
                        for name in identities}}


def versus(player: dict | list[dict], baseline: dict) -> dict | None:
    """Paired difference in coins from a baseline bot on the seeds both played. A list of players
    (a condition's models) is compared by their mean coins per seed, on the seeds all of them played."""
    group = player if isinstance(player, list) else [player]
    seeds = sorted(set(baseline["by_seed"]).intersection(*(set(p["by_seed"]) for p in group)))
    if not seeds:
        return None
    a = [baseline["by_seed"][s] for s in seeds]
    b = [float(np.mean([p["by_seed"][s] for p in group])) for s in seeds]
    diffs = [y - x for x, y in zip(a, b)]
    low, high = paired_bootstrap(a, b)  # works on any paired numbers, not only 0/1 outcomes
    p = float(wilcoxon(diffs).pvalue) if any(diffs) else 1.0
    return {"n": len(seeds), "delta": float(np.mean(diffs)), "ci": (low, high), "p": p}


def comparisons(players: dict[tuple[str, str], dict]) -> list[dict]:
    """players[(condition, player)] = summary -> one row per player, and an "all models" row per
    condition with several, each compared with every baseline bot the run has (not with itself);
    Holm-adjusted per baseline over the rows."""
    groups: dict[str, list[dict]] = {}
    for (cond, player), s in players.items():
        if player not in BASELINES:
            groups.setdefault(cond, []).append(s)
    rows = [{"condition": cond, "player": player, "group": s} for (cond, player), s in players.items()]
    rows += [{"condition": cond, "player": ALL_MODELS, "group": group}
             for cond, group in groups.items() if len(group) > 1]
    for row in rows:
        row["vs"] = {b: (versus(row["group"], players[(b, b)]) if (b, b) in players and row["player"] != b else None)
                     for b in BASELINES}
    for b in BASELINES:
        tested = [row["vs"][b] for row in rows if row["vs"][b]]
        for result, adjusted in zip(tested, holm([r["p"] for r in tested])):
            result["holm"] = adjusted
    for row in rows:
        del row["group"]
    return rows


def table(rows: list[tuple[list[str], dict, str]]) -> list[str]:
    """Old layout. rows: (leading cells, condition summary, identity)."""
    shown = lambda v: "not in CSV" if v is None else v
    body = [cells + [f"{s['finished']}/{s['games']}", shown(s["players"][identity]["avg_coins"]),
                     shown(s["players"][identity]["avg_penalty"])] for cells, s, identity in rows]
    return markdown(["condition", "model", "finished games", "avg coins", "avg penalty"], body)


def _p(p: float) -> str:
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def player_table(rows: list[tuple[list[str], dict]]) -> list[str]:
    """rows: (leading cells, player summary)."""
    body = []
    for cells, s in rows:
        low, high = s["coins_ci"]
        body.append(cells + [f"{s['finished']}/{s['games']}", f"{s['coins']:.2f} [{low:.2f}, {high:.2f}]",
                             "–" if s["opponents"] is None else f"{s['opponents']:.2f}",
                             pct(s["wins"], s["games"]), f"{s['penalty']:.2f}"])
    return markdown(["condition", "player", "finished games", "coins per game [95% CI]", "opponents' coins",
                     "wins", "penalty per game"], body)


def comparison_table(rows: list[dict], names: dict[str, str]) -> list[str]:
    """comparisons()'s rows; `names` maps an identity to its model's name."""
    body = []
    for row in rows:
        cells = [row["condition"], names.get(row["player"], row["player"])]
        for b in BASELINES:
            vs = row["vs"][b]
            cells += ([f"{vs['delta']:+.2f} [{vs['ci'][0]:+.2f}, {vs['ci'][1]:+.2f}]", _p(vs["p"]), _p(vs["holm"])]
                      if vs else ["–", "", ""])
        body.append(cells)
    return markdown(["condition", "player", "Δ coins vs reference bot [95% CI]", "p", "Holm p",
                     "Δ coins vs random bot [95% CI]", "p", "Holm p"], body)
