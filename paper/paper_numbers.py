#!/usr/bin/env python3
"""Every table and number of the paper, recomputed, and checked against paper/paper.md.

    python3 paper/paper_numbers.py            # from the runs' metrics (runs/<run>/metrics.json)
    python3 paper/paper_numbers.py --rescore  # first re-score every run from its raw logs

--rescore unpacks runs/<run>.tar.xz into work/, deletes the archived metrics, scores the raw answers
again with eval/evaluate.py (no GPU, no model needed), checks that the result equals
runs/<run>/metrics.json, and then builds the tables from the re-scored metrics.

Sources:
    runs/replay_20261029_gen2             replay, LFM2.5 / Granite / Gemma 4       Tables 1, 2, 4, 5
    runs/suite_20261029_gen2              tournament, reference-bot opponents      Tables 3, 5
    runs/suite_20261030_gen2_vsrandom     tournament, random-bot opponents         Tables 3, 5
    runs/replay_20261006_2x4              replay, TinyLlama / Qwen2.5 / Gemma-2B   Table 5
    runs/suite_20261102_phase1_fixed(_vsrandom)   the earlier generation's tournaments   Table 5
    eval/replay_corpus.json               the baselines that need no model: the reference bot,
                                          the random bot and the fixed rule (Tables 1, 4, 5)

Shares of states and games are rounded as the metrics.md files round them (half to even);
means, differences and p-values half up. Each table is printed in the paper's layout; a cell that differs
from paper.md is listed under the table, and the run ends with the in-text numbers that were not
found in paper.md. Exit status 1 if anything differs.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tarfile
from collections import defaultdict
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from eval import legality, reference, state_sensitivity  # noqa: E402
from eval.evaluate import TEACHER_STYLE  # noqa: E402
from game.player import bots  # noqa: E402
from game.player import state as game_state  # noqa: E402
from replay import ASK, ask_arguments  # noqa: E402

PAPER = REPO / "paper" / "paper.md"
RUNS, WORK = REPO / "runs", REPO / "work"
REPLAY, REPLAY_GEN1 = "replay_20261029_gen2", "replay_20261006_2x4"
SUITES = {"reference": "suite_20261029_gen2", "random": "suite_20261030_gen2_vsrandom"}
SUITES_GEN1 = {"reference": "suite_20261102_phase1_fixed", "random": "suite_20261102_phase1_fixed_vsrandom"}
ALL_RUNS = [REPLAY, *SUITES.values(), REPLAY_GEN1, *SUITES_GEN1.values()]
# identity -> the model name the metrics use, in the paper's order
MODELS = {"gen2": {"Alpha": "LFM2.5-1.2B", "Beta": "granite-4.2-3b", "Gamma": "gemma-4-E2B"},
          "gen1": {"Alpha": "TinyLlama-1.1B", "Beta": "Qwen2.5-3B", "Gamma": "gemma-2b"}}
IDS = ("Alpha", "Beta", "Gamma")
PHASES = ("PLANTING", "FORCED", "TRADING", "REPLY", "CONSIDERING")
FIELDS = ("field1", "field2", "field3")
CONDITIONS = ("lora_compact", "lora_verbose", "lora_verbose2", "lora_grammar",
              "base_compact", "base_verbose", "base_verbose2", "base_grammar")
AGREEMENT_ORDER = ("base_verbose", "lora_verbose", "base_verbose2", "lora_verbose2", "lora_compact",
                   "base_grammar", "lora_grammar")
TEACHER_ORDER = ("base_verbose", "lora_verbose", "base_verbose2", "lora_verbose2", "base_compact",
                 "lora_compact", "base_grammar", "lora_grammar")
TOURNAMENT_ORDER = ("lora_compact", "bot_reference", "bot_random", "base_grammar", "lora_verbose", "base_verbose")
MINUS = "−"
problems: list[str] = []


# ── formatting ────────────────────────────────────────────────────────────────

def half_up(x: float, places: int = 0) -> Decimal:
    return Decimal(repr(x)).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


def pct(k: float, n: float) -> int:
    """A share in %, rounded as eval/tables.py rounds it in every metrics.md (half to even: 62.5 -> 62)."""
    return int(f"{100 * k / n:.0f}")


def signed(x, places: int = 0) -> str:
    v = half_up(float(x), places)
    return ("+" if v >= 0 else MINUS) + f"{abs(v):.{places}f}"


def coins(x: float) -> str:
    return f"{half_up(x, 2):.2f}"


def p_text(p: float) -> str:
    """A Holm p as the paper writes it: "< 0.001", "0.031", "0.15", "1.0"."""
    if p < 0.001:
        return "< 0.001"
    if half_up(p, 2) >= Decimal("1.00"):
        return "1.0"
    return str(half_up(p, 3 if p < 0.1 else 2))


def three(values) -> str:
    return " / ".join(str(v) for v in values)


def p_note(ps: list[float], ns_words: bool) -> str:
    if all(p < 0.001 for p in ps):
        return "(p < 0.001)"
    if ns_words and all(p >= 0.05 for p in ps):
        return "(both n.s.)"
    return "(p = " + ", ".join(p_text(p) for p in ps) + ")"


# ── inputs ────────────────────────────────────────────────────────────────────

def rescore() -> None:
    """Score every run again from its raw logs, and compare with the shipped metrics."""
    WORK.mkdir(exist_ok=True)
    for run in ALL_RUNS:
        target = WORK / run
        if target.exists():
            shutil.rmtree(target)
        with tarfile.open(RUNS / f"{run}.tar.xz") as tar:
            tar.extractall(WORK, filter="data") if hasattr(tarfile, "data_filter") else tar.extractall(WORK)
        for name in ("metrics.json", "metrics.md"):
            (target / name).unlink(missing_ok=True)
        print(f"re-scoring {run} ...", flush=True)
        done = subprocess.run([sys.executable, "eval/evaluate.py", str(target.relative_to(REPO))],
                              cwd=REPO, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if done.returncode:
            sys.exit(f"eval/evaluate.py failed on {run}:\n{done.stderr[-2000:]}")
        diffs = differences(json.loads((RUNS / run / "metrics.json").read_text()),
                            json.loads((target / "metrics.json").read_text()))
        print(f"   {run}: {'identical to runs/' + run + '/metrics.json' if not diffs else f'{len(diffs)} differences'}")
        problems.extend(f"re-scored {run}: {d}" for d in diffs[:20])


def differences(a, b, path="") -> list[str]:
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            if k == "evaluated_at":
                continue
            out += differences(a.get(k), b.get(k), f"{path}/{k}") if k in a and k in b else [f"{path}/{k}: only in one"]
        return out
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [f"{path}: {len(a)} vs {len(b)} entries"]
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in differences(x, y, f"{path}[{i}]")]
    if isinstance(a, float) or isinstance(b, float):
        return [] if abs(float(a) - float(b)) <= 1e-9 * max(1.0, abs(float(a))) else [f"{path}: {a} vs {b}"]
    return [] if a == b else [f"{path}: {a!r} vs {b!r}"]


def load(run: str, base: Path) -> dict:
    return json.loads((base / run / "metrics.json").read_text())


# ── the baselines that need no model ─────────────────────────────────────────

def fixed_rule(state: dict) -> str:
    """Always pass; accept every offer and counter-offer, giving nothing; plant each card on a field
    of the same bean, else on an empty field, else on field 1."""
    phase = state["phase"]
    if phase == "TRADING":
        return "null"
    if phase in ("REPLY", "CONSIDERING"):
        return json.dumps({"accepted": True, "offer": [], "reason": ""})
    current = {f: list(state["fields"][f]["cards"]) for f in FIELDS}
    plan = {f: [] for f in FIELDS}
    for card in state["hand"][:1] if phase == "PLANTING" else state["new_cards"]:
        field = next((f for f in FIELDS if current[f] and current[f][0] == card), None) \
            or next((f for f in FIELDS if not current[f]), "field1")
        if current[field] and current[field][0] != card:
            current[field] = []
        current[field].append(card)
        plan[field].append(card)
    return json.dumps(plan)


def bot_answer(message, phase: str, peers: dict) -> str:
    """A bot's game message as the JSON answer a model gives in the compact style."""
    if phase in ("PLANTING", "FORCED"):
        return json.dumps({f: list(message.fields[f]) for f in FIELDS})
    if phase == "TRADING":
        index = {peers["player1_ip"]: "0", peers["player2_ip"]: "1"}
        return json.dumps({"offered_cards": list(message.offered_cards or []),
                           "to": index.get(str(message.to), "") if message.to else "", "ask": message.ask or ""})
    return json.dumps({"accepted": bool(message.accepted), "offer": list(message.offer), "reason": message.reason or ""})


def baselines() -> dict:
    """The fixed rule, the reference bot and the random bot on the replay corpus. The random bot is
    seeded by the state and its identity ("Alpha"), so its score is one draw of a random player."""
    items = json.loads((REPO / "eval" / "replay_corpus.json").read_text())
    game_state.CONFIG["identity"] = "Alpha"
    players = {"fixed rule": None, "reference bot": bots.Reference(), "random bot": bots.Random()}
    out = {}
    for name, player in players.items():
        agg = defaultdict(lambda: defaultdict(int))
        for item in items:
            state, peers, slice_ = item["state"], item["peers"], item.get("slice", "game")
            phase = state["phase"]
            if player is None:
                verdict = legality.check(state, fixed_rule(state), TEACHER_STYLE, peers)
            else:
                game_state.CONFIG.update(peers)
                message = getattr(player, ASK[phase])(*ask_arguments(state, peers))
                verdict = legality.check(state, bot_answer(message, phase, peers), "compact", peers)
            for key in (slice_, "all"):
                a = agg[key]
                a["n"] += 1
                a["legal"] += verdict.legal
                a["correct"] += reference.check(state, verdict)["correct"]
                if phase in ("PLANTING", "FORCED") and verdict.legal:
                    a["plantings"] += 1
                    a["avoidable"] += state_sensitivity.facts(state, verdict.message)["avoidable_harvest"]
            if item.get("teacher"):
                taught = legality.check(state, item["teacher"], TEACHER_STYLE, peers)
                same = verdict.decision is not None and verdict.decision == taught.decision
                a = agg["teacher"]
                a[f"n {phase}"] += 1
                a[f"match {phase}"] += same
                a["n"] += 1
                a["match"] += same
        out[name] = agg
    return out


# ── the metrics ───────────────────────────────────────────────────────────────

def cell(m: dict, slice_: str, cond: str, identity: str) -> dict:
    return m["slices"][slice_]["conditions"][cond][identity]


def share(m: dict, cond: str, identity: str, metric: str, key: str, slices=("game",)) -> int:
    k = sum(cell(m, s, cond, identity)[metric][key] for s in slices)
    n = sum(cell(m, s, cond, identity)[metric]["n"] for s in slices)
    return pct(k, n)


def correct(m: dict, cond: str, identity: str, slice_: str = "game") -> int:
    return share(m, cond, identity, "reference", "correct", (slice_,))


def avoidable(m: dict, cond: str, identity: str) -> str:
    s = cell(m, "game", cond, identity)["state_sensitivity"]
    n = sum(s.get(p, {}).get("n", 0) for p in ("PLANTING", "FORCED"))
    k = sum(s.get(p, {}).get("avoidable_harvest", 0) for p in ("PLANTING", "FORCED"))
    return str(pct(k, n)) if n else "–"


def effect(m: dict, slice_: str, metric: str, contrast: str, model: str) -> dict:
    found = [e for e in m["slices"][slice_]["effects"][metric] if e["contrast"] == contrast and e["model"] == model]
    assert len(found) == 1, (slice_, metric, contrast, model)
    return found[0]


def points(m: dict, slice_: str, contrast: str, model: str) -> int:
    e = effect(m, slice_, "reference-correct", contrast, model)
    return int(half_up(100 * (e["b"] - e["a"]) / e["n"]))


def agreement(m: dict, slice_: str, model: str) -> dict[tuple[str, str], float]:
    """Pairwise agreement in %, over the states where both conditions give a readable decision;
    base_compact is left out (it gives almost no readable decision), and so is a pair without any
    such state (TinyLlama's base_verbose gives none)."""
    pairs = {}
    for key, v in m["slices"][slice_]["agreement"][model].items():
        a, b = key.split("|")
        if "base_compact" not in (a, b) and v["n"]:
            pairs[(a, b)] = 100 * v["same"] / v["n"]
    return pairs


def mean_agreement(pairs: dict, cond: str | None = None) -> tuple[float, float, float]:
    shares = [v for (a, b), v in pairs.items() if cond is None or cond in (a, b)]
    return sum(shares) / len(shares), min(shares), max(shares)


def comparison(suite: dict, cond: str, player: str, baseline: str) -> dict:
    found = [c for c in suite["game_comparisons"] if c["condition"] == cond and c["player"] == player]
    assert len(found) == 1, (cond, player)
    return found[0]["vs"][baseline]


def player_games(suite: dict, cond: str, identity: str) -> dict:
    return suite["games"][cond]["players"][identity]


# ── paper.md ──────────────────────────────────────────────────────────────────

def paper_tables(text: str) -> dict[str, dict[str, list[str]]]:
    tables, current = {}, None
    for line in text.splitlines():
        m = re.match(r"Table: .*\{#tab:(\w+)\}", line)
        if m:
            current = tables.setdefault(m.group(1), {})
            continue
        if current is not None and line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                continue
            current[cells[0].strip("`")] = cells[1:]
        elif current is not None and line.strip() and not line.startswith("|"):
            current = None
    return tables


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("-", MINUS).replace("–", "–")).strip()


def show(tid: str, header: list[str], rows: list[tuple[str, list[str]]], paper: dict) -> None:
    print(f"\nTable {tid}")
    print("| " + " | ".join(header) + " |")
    print("|" + "---|" * len(header))
    for name, cells in rows:
        label = name if name in ("fixed rule", "random bot", "reference bot") or " " in name else f"`{name}`"
        print("| " + " | ".join([label, *cells]) + " |")
    theirs = paper.get(tid)
    if theirs is None:
        problems.append(f"tab:{tid} is not in paper.md")
        return
    for name, cells in rows:
        if name not in theirs:
            problems.append(f"tab:{tid}: row {name!r} not in paper.md")
            continue
        for col, (ours, their) in enumerate(zip(cells, theirs[name]), start=1):
            if norm(ours) != norm(their):
                problems.append(f"tab:{tid}, row {name!r}, column {header[col]!r}: computed {ours!r}, paper {their!r}")
    for name in theirs:
        if name not in dict(rows) and name not in (header[0],):
            problems.append(f"tab:{tid}: paper row {name!r} is not computed here")


# ── the tables ────────────────────────────────────────────────────────────────

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--rescore", action="store_true", help="re-score every run from its raw logs first")
    args = p.parse_args()
    if args.rescore:
        rescore()
    base = WORK if args.rescore else RUNS
    rep, rep1 = load(REPLAY, base), load(REPLAY_GEN1, base)
    suites = {k: load(v, base) for k, v in SUITES.items()}
    suites1 = {k: load(v, base) for k, v in SUITES_GEN1.items()}
    names, names1 = MODELS["gen2"], MODELS["gen1"]
    text = PAPER.read_text()
    paper = paper_tables(text)
    print("baselines on the replay corpus ...", flush=True)
    bl = baselines()
    claims: list[tuple[str, str]] = []  # (what, the text paper.md should contain)

    # Table 1 — the replay
    rows = []
    for c in CONDITIONS:
        rows.append((c, [three(share(rep, c, i, "schema_validity", "valid") for i in IDS),
                         three(share(rep, c, i, "legality", "legal") for i in IDS),
                         three(correct(rep, c, i) for i in IDS),
                         "–" if all(avoidable(rep, c, i) == "–" for i in IDS) else three(avoidable(rep, c, i) for i in IDS)]))
    fr, rb = bl["fixed rule"], bl["random bot"]
    fixed_correct = pct(fr["game"]["correct"], fr["game"]["n"])
    rows.append(("fixed rule", ["–", str(pct(fr["game"]["legal"], fr["game"]["n"])), str(fixed_correct),
                                str(pct(fr["game"]["avoidable"], fr["game"]["plantings"]))]))
    rows.append(("random bot", ["–", str(pct(rb["game"]["legal"], rb["game"]["n"])),
                                str(pct(rb["game"]["correct"], rb["game"]["n"])), "–"]))
    show("replay", ["Player", "Schema-valid", "Legal", "Correct", "Avoidable harvests"], rows, paper)
    print("   (every share is on the game slice, the 500 states)")
    print(f"   (the random bot's avoidable harvests, not in the table: "
          f"{pct(rb['game']['avoidable'], rb['game']['plantings'])}%)")

    lc = [correct(rep, "lora_compact", i) for i in IDS]
    lc_train = [correct(rep, "lora_compact", i, "training") for i in IDS]
    cv = {s: [points(rep, s, "lora: compact vs verbose", names[i]) for i in IDS] for s in ("game", "training")}
    cv_p = [effect(rep, s, "reference-correct", "lora: compact vs verbose", names[i])["p_holm"]
            for s in ("game", "training") for i in IDS]
    av = [points(rep, "game", "adapter at verbose", names[i]) for i in IDS]
    av_p = [effect(rep, "game", "reference-correct", "adapter at verbose", names[i])["p_holm"] for i in IDS]
    claims += [
        ("lora_compact, game slice", f"{'/'.join(map(str, lc))}% of the game slice"),
        ("lora_compact, training slice", f"{'/'.join(map(str, lc_train))}% of the training slice"),
        ("compact over verbose, adapted, game", "/".join(signed(x) for x in cv["game"])),
        ("compact over verbose, adapted, training", "/".join(signed(x) for x in cv["training"])),
        ("... all six Holm p < 0.001" if max(cv_p) < 0.001 else f"... max Holm p {max(cv_p):.3g}",
         "p < 0.001 in all six comparisons" if max(cv_p) < 0.001 else "(not < 0.001 in all six)"),
        ("adapter at verbose, LFM2.5 and Granite", f"LFM2.5 gains {av[0]} points and Granite {av[1]} "
         f"({'both Holm p < 0.001' if max(av_p[:2]) < 0.001 else 'Holm p = ' + p_text(av_p[0]) + ', ' + p_text(av_p[1])})"),
        ("adapter at verbose, Gemma 4", f"Gemma 4 gains {av[2]} (Holm p = {p_text(av_p[2])})"),
        ("base_compact legal, Gemma 4", f"({share(rep, 'base_compact', 'Gamma', 'legality', 'legal')}%)"),
    ]
    others = {i: [correct(rep, c, i) for c in ("lora_verbose", "lora_verbose2", "lora_grammar")] for i in IDS}
    above = sum(x > fixed_correct for x in others["Beta"])
    ag = effect(rep, "game", "reference-correct", "adapter at grammar", names["Gamma"])
    claims += [
        ("Granite's adapter under the three other prompts", f"{min(others['Beta'])}–{max(others['Beta'])}% reference-correctness"),
        ("... above the fixed rule in", f"above the fixed rule's {fixed_correct}% in {['none', 'one', 'two', 'all three'][above]} of them"),
        ("LFM2.5 and Gemma 4 adapters under the other prompts",
         f"{min(others['Alpha'])}–{max(others['Alpha'])}% and {min(others['Gamma'])}–{max(others['Gamma'])}%"),
        ("adapter at grammar, Gemma 4", f"lowers Gemma 4 by {-points(rep, 'game', 'adapter at grammar', names['Gamma'])} "
                                        f"points (Holm p = {p_text(ag['p_holm'])})"),
    ]
    bg_valid = [share(rep, "base_grammar", i, "schema_validity", "valid") for i in IDS]
    bg_correct = [correct(rep, "base_grammar", i) for i in IDS]
    bg_avoid = [int(avoidable(rep, "base_grammar", i)) for i in IDS]
    gv = [-points(rep, "game", "base: grammar vs verbose", names[i]) for i in IDS]
    gv_p = [effect(rep, "game", "reference-correct", "base: grammar vs verbose", names[i])["p_holm"] for i in IDS]
    bg_rand = comparison(suites["random"], "base_grammar", "all models", "bot_random")
    claims += [
        ("base_grammar schema-valid", f"{min(bg_valid)}–{max(bg_valid)}% schema-valid"),
        ("base_grammar correct", f"only {min(bg_correct)}–{max(bg_correct)}% of its decisions are reference-correct"),
        ("base_grammar avoidable harvests", f"{min(bg_avoid)}–{max(bg_avoid)}% of its plantings"),
        ("lora_grammar Gemma 4 schema-valid", f"is {share(rep, 'lora_grammar', 'Gamma', 'schema_validity', 'valid')}% valid"),
        ("grammar vs verbose, base models", f"by {'/'.join(map(str, gv))} points"),
        ("... Holm p per model", f"significantly only for LFM2.5 (Holm p {p_text(gv_p[0]) if gv_p[0] < 0.001 else '= ' + p_text(gv_p[0])})"
         if gv_p[0] < 0.05 and min(gv_p[1:]) >= 0.05 else f"Holm p = {', '.join(p_text(x) for x in gv_p)}"),
        ("base_verbose LFM2.5 schema-valid", f"valid only {share(rep, 'base_verbose', 'Alpha', 'schema_validity', 'valid')}% of the time"),
        ("base_grammar vs random bot, random-bot opponents, pooled",
         f"pooled difference {signed(bg_rand['delta'], 2)} coins, Holm p = {p_text(bg_rand['holm'])}"),
    ]

    # Table 2 — agreement
    pairs = {i: agreement(rep, "game", names[i]) for i in IDS}
    rows = []
    for c in AGREEMENT_ORDER:
        stats = [mean_agreement(pairs[i], c) for i in IDS]
        rows.append((c, [f"{half_up(mu)} [{half_up(lo)}–{half_up(hi)}]" for mu, lo, hi in stats]))
    show("agreement", ["Condition", "LFM2.5", "Granite", "Gemma 4"], rows, paper)
    overall = [int(half_up(mean_agreement(pairs[i])[0])) for i in IDS]
    with_lc = [mean_agreement(pairs[i], "lora_compact") for i in IDS]
    pairs_t = {i: agreement(rep, "training", names[i]) for i in IDS}
    best = max(pairs["Beta"].items(), key=lambda kv: kv[1])
    claims += [
        ("agreement, game slice", f"{'/'.join(map(str, overall))}% of the states on average"),
        ("... pairs with lora_compact", f"{'/'.join(str(half_up(x[0])) for x in with_lc)}% "
                                        f"(range {half_up(min(x[1] for x in with_lc))}–{half_up(max(x[2] for x in with_lc))}%)"),
        ("agreement, training slice", f"the training slice gives {'/'.join(str(half_up(mean_agreement(pairs_t[i])[0])) for i in IDS)}%"),
        (f"Granite's highest pair ({best[0][0]} | {best[0][1]})", f"reaches at most {half_up(best[1])}%"),
    ]

    # Table 3 — coins and wins
    def wins(suite, cond):
        ps = suite["games"][cond]["players"].values()
        return pct(sum(x["wins"] for x in ps), sum(x["games"] for x in ps))

    def mean_coins(suite, cond, ids):
        return [coins(player_games(suite, cond, i)["coins"]) for i in ids]

    rows = []
    for c in TOURNAMENT_ORDER:
        ids = [c] if c.startswith("bot_") else IDS
        label = {"bot_reference": "reference bot", "bot_random": "random bot"}.get(c, c)
        rows.append((label, [three(mean_coins(suites["reference"], c, ids)), three(mean_coins(suites["random"], c, ids)),
                             str(wins(suites["reference"], c)), str(wins(suites["random"], c))]))
    show("coins", ["Player", "Coins, reference-bot opponents", "Coins, random-bot opponents",
                   "Wins, reference-bot opponents", "Wins, random-bot opponents"], rows, paper)
    vs_ref = [comparison(suites[s], "lora_compact", "all models", "bot_reference") for s in ("reference", "random")]
    claims += [
        ("lora_compact coins, reference-bot opponents", "/".join(mean_coins(suites["reference"], "lora_compact", IDS))),
        ("lora_compact coins, random-bot opponents", "/".join(mean_coins(suites["random"], "lora_compact", IDS))),
        ("reference bot coins", f"{coins(player_games(suites['reference'], 'bot_reference', 'bot_reference')['coins'])} and "
                                f"{coins(player_games(suites['random'], 'bot_reference', 'bot_reference')['coins'])}"),
        ("random bot coins", f"{coins(player_games(suites['reference'], 'bot_random', 'bot_random')['coins'])} and "
                             f"{coins(player_games(suites['random'], 'bot_random', 'bot_random')['coins'])}"),
        ("lora_compact vs reference bot, pooled", f"{signed(vs_ref[0]['delta'], 2)} and {signed(vs_ref[1]['delta'], 2)} coins, "
                                                  f"Holm p = {p_text(max(x['holm'] for x in vs_ref))}"),
    ]
    print("\n   95% bootstrap intervals, lora_compact minus the reference bot, pooled: " + "; ".join(
        f"{s}-bot opponents {signed(x['delta'], 2)} [{signed(x['ci'][0], 2)}, {signed(x['ci'][1], 2)}]"
        for s, x in zip(("reference", "random"), vs_ref)))
    print("   Comparisons with Holm p >= 0.05 against the reference bot, and with Holm p < 0.05 against the random bot:")
    for s, suite in suites.items():
        for c in suite["game_comparisons"]:
            if c["condition"] == "lora_compact" or c["condition"].startswith("bot_"):
                continue
            who = "pooled" if c["player"] == "all models" else names[c["player"]]
            r, q = c["vs"].get("bot_reference"), c["vs"].get("bot_random")
            if r and r["holm"] >= 0.05:
                print(f"      {s}-bot opponents: {c['condition']} {who} vs reference bot "
                      f"{signed(r['delta'], 2)}, Holm p = {p_text(r['holm'])}")
            if q and q["holm"] < 0.05:
                print(f"      {s}-bot opponents: {c['condition']} {who} vs random bot "
                      f"{signed(q['delta'], 2)}, Holm p = {p_text(q['holm'])}")

    # Table 4 — teacher match on the training slice
    def teacher(cond, identity, phase=None):
        ref = cell(rep, "training", cond, identity)["reference"]
        t = ref["phases"][phase]["teacher"] if phase else ref["teacher"]
        return pct(t["match"], t["n"])

    rows = [(c, [three(teacher(c, i, ph) for i in IDS) for ph in PHASES] + [three(teacher(c, i) for i in IDS)])
            for c in TEACHER_ORDER]
    for name in ("reference bot", "random bot"):
        t = bl[name]["teacher"]
        rows.append((name, [str(pct(t[f"match {ph}"], t[f"n {ph}"])) for ph in PHASES] + [str(pct(t["match"], t["n"]))]))
    show("teacher", ["Condition", *PHASES, "Overall"], rows, paper)
    t = bl["fixed rule"]["teacher"]
    by_type = ", ".join(f"{ph} {pct(t['match ' + ph], t['n ' + ph])}" for ph in PHASES)
    print(f"   (the fixed rule, not in the table: {by_type}, overall {pct(t['match'], t['n'])})")
    rt = bl["reference bot"]["teacher"]
    lcp = [teacher("lora_compact", i, "PLANTING") for i in IDS]
    claims += [
        ("reference bot teacher match, overall", f"as often as the reference bot ({pct(rt['match'], rt['n'])}%)"),
        ("lora_compact vs reference bot, PLANTING",
         f"({min(lcp)}–{max(lcp)}% against {pct(rt['match PLANTING'], rt['n PLANTING'])}%)"),
    ]

    # Table 5 — the two generations
    def gen_rows(m, nm, su):
        cvg = [points(m, "game", "lora: compact vs verbose", nm[i]) for i in IDS]
        avg = [points(m, "game", "adapter at verbose", nm[i]) for i in IDS]
        agree = [int(half_up(mean_agreement(agreement(m, "game", nm[i]))[0])) for i in IDS]

        def coin_row(cond, baseline, ns_words):
            cs = [comparison(su[s], cond, "all models", baseline) for s in ("reference", "random")]
            return f"{signed(cs[0]['delta'], 2)} / {signed(cs[1]['delta'], 2)} {p_note([c['holm'] for c in cs], ns_words)}"

        return {
            "Correct, `lora_compact`": three(correct(m, "lora_compact", i) for i in IDS),
            "Correct, `lora_verbose`": three(correct(m, "lora_verbose", i) for i in IDS),
            "Compact over verbose, adapted, points": three(signed(x) for x in cvg),
            "Adapter at verbose, points": three(signed(x) for x in avg),
            "Schema-valid, `base_grammar`": three(share(m, "base_grammar", i, "schema_validity", "valid") for i in IDS),
            "Correct, `base_grammar`": three(correct(m, "base_grammar", i) for i in IDS),
            "Agreement between conditions": three(agree),
            "Lead over the fixed rule, points": three(signed(correct(m, "lora_compact", i) - fixed_correct) for i in IDS),
            "`lora_compact` vs reference bot, coins": coin_row("lora_compact", "bot_reference", True),
            "`lora_compact` vs random bot, coins": coin_row("lora_compact", "bot_random", False),
            "`lora_verbose` vs random bot, coins": coin_row("lora_verbose", "bot_random", False),
        }

    g1, g2 = gen_rows(rep1, names1, suites1), gen_rows(rep, names, suites)
    show("replication", ["Measure", "Earlier generation", "Main study"],
         [(k.replace("`", ""), [g1[k], g2[k]]) for k in g1],
         {"replication": {k.replace("`", ""): v for k, v in paper.get("replication", {}).items()}})
    lv1 = [correct(rep1, "lora_verbose", i) for i in IDS]
    claims += [
        ("earlier generation, lora_verbose", f"stayed at {min(lv1)}–{max(lv1)}%"),
        ("main study, Granite lora_verbose", f"Granite's adapter works at {correct(rep, 'lora_verbose', 'Beta')}%"),
        ("Gemma 4 vs Gemma-2B, lora_compact", f"({correct(rep, 'lora_compact', 'Gamma')}% against "
                                              f"{correct(rep1, 'lora_compact', 'Gamma')}%)"),
    ]

    # the abstract
    claims += [
        ("abstract: lora_compact correct", f"{min(lc)}–{max(lc)}% of the adapted models' decisions"),
        ("abstract: compact over verbose", f"{min(cv['game'])}–{max(cv['game'])} points"),
        ("abstract: base_grammar valid / correct", f"{min(bg_valid)}–{max(bg_valid)}% valid, yet only "
                                                   f"{min(bg_correct)}–{max(bg_correct)}%"),
    ]

    print("\nIn-text numbers (each is searched for in paper.md):")
    flat = norm(text.replace("\n", " "))
    for what, expected in claims:
        found = norm(expected) in flat
        print(f"   {'ok     ' if found else 'MISSING'} {what}: {expected}")
        if not found:
            problems.append(f"text: {what}: {expected!r} not found")

    print(f"\n{len(problems)} difference(s) from paper.md" + (":" if problems else "."))
    for line in problems:
        print("   " + line)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
