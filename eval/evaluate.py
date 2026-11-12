#!/usr/bin/env python3
"""Evaluate replay and tournament runs: every metric, one command.

    python3 eval/evaluate.py logs/replay_<id>               # one run
    python3 eval/evaluate.py logs/replay_A logs/replay_B    # several runs, plus run against run
    python3 eval/evaluate.py RUN --training-corpus PATH     # another corpus than the run's own

Metrics, one file each in eval/:
    schema_validity.py    the whole answer matches the message type's JSON schema (valid@1)
    legality.py           the game would carry out the answer as written
    reference.py          the decision a value-aware rule set makes; the teacher's own answer
    state_sensitivity.py  the decision depends on the state; the teacher's decisions as reference
    agreement.py          the same item gets the same decision across conditions and runs
    effects.py            adapter and prompt effects on paired items, with intervals and tests (stats.py)
    game_outcomes.py      coins and penalties (tournament runs)

A replay's items come in slices (eval/replay_corpus.json): "game"
states from tournament logs and "training" states held out from the adapters' generator. Each
slice is a chapter of its own; a tournament is one chapter. Condition names of runs from before
the 2 x 4 design are mapped to the current ones (ALIASES).

Reads the layout replay.py and tournament.py write:
    <run>/run.json                                   kind, backend, the experiment config
    <run>/<condition>/configs/player{1,2,3}_config.json
    <run>/<condition>/<identity>/game_NNNN.log       the player's own log
    <run>/<condition>/tournament_*.csv               tournament runs
Runs from before run.json are read from report.json, and from <identity>_llm.log when the
per-game logs are missing.

Writes <run>/metrics.json and <run>/metrics.md (also printed), and with several runs
<first run>/comparison.json/.md. Needs no model: it scores the answers the logs hold.
"""

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import tournament as T  # noqa: E402  (the experiment config)
from eval import (agreement, corpus, effects, game_outcomes, legality, reference,  # noqa: E402
                  schema_validity, state_sensitivity)
from eval.stats import mcnemar  # noqa: E402
from eval.tables import ci, markdown, pct  # noqa: E402

# The training corpus names the two other players "0"/"1", like the compact prompt; any two
# addresses let legality.py map them.
TEACHER_STYLE = "compact"
TEACHER_PEERS = {"player1_ip": "http://teacher-peer-0", "player2_ip": "http://teacher-peer-1"}
# Condition names before the 2 x 4 design (adapter x prompt style).
ALIASES = {"no_lora": "base_verbose", "with_lora": "lora_compact", "with_lora_verbose": "lora_verbose",
           "grammar": "base_grammar", "with_lora_verbose2": "lora_verbose2", "no_lora_verbose2": "base_verbose2"}
SLICES = {"game": "game states", "training": "held-out training states", "games": "tournament games",
          "unmatched": "states not in the replay corpus"}


def info(msg: str) -> None:
    print(f"\033[0;36m[eval]\033[0m {msg}", file=sys.stderr, flush=True)


# ── Runs ───────────────────────────────────────────────────────────────────────

@dataclass
class Player:
    identity: str
    model: str                # short model name for the tables
    style: str                # prompt style
    peers: dict[str, str]     # player1_ip / player2_ip
    logs: Path                # the directory holding <identity>/game_*.log


@dataclass
class Condition:
    name: str                 # base_<prompt> or lora_<prompt> (or a baseline bot's kind)
    dir: Path
    backend: str
    players: list[Player]     # LLM players; one per seat they played in a tournament

    @property
    def models(self) -> dict[str, str]:
        """{identity: model name} of its LLM players, in order."""
        return {p.identity: p.model for p in self.players}


@dataclass
class Run:
    dir: Path
    kind: str                 # "replay" or "tournament"
    experiment: dict
    conditions: list[Condition] = field(default_factory=list)
    corpus_path: Path | None = None   # the training corpus (the teacher's own rows)
    date: str = ""                    # when it ran (YYYY-MM-DD)

    @property
    def name(self) -> str:
        return self.dir.name

    @property
    def label(self) -> str:
        """The run with its backend and date, e.g. "replay_x (gpu, 2026-10-05)"."""
        backends = ", ".join(sorted({c.backend for c in self.conditions})) or "?"
        return f"{self.name} ({backends}" + (f", {self.date})" if self.date else ")")


def _model_name(experiment: dict, identity: str) -> str:
    for m in experiment.get("models", []):
        if m["identity"] == identity:
            return re.sub(r"-(Chat-v1\.0|Instruct|it)$", "", m.get("hf", m["gguf"]).split("/")[-1])
    return identity


def load_run(run_dir: Path) -> Run:
    manifest = {}
    for name in ("run.json", "report.json"):
        if (run_dir / name).exists():
            manifest = json.loads((run_dir / name).read_text())
            break
    kind = manifest.get("kind") or ("replay" if run_dir.name.startswith("replay") else "tournament")
    experiment = manifest.get("experiment") or T.EXPERIMENT
    recorded = manifest.get("conditions") if isinstance(manifest.get("conditions"), dict) else {}
    date = min(filter(None, (c.get("finished", "") for c in recorded.values())),
               default=manifest.get("generated_at", ""))[:10]
    run = Run(run_dir, kind, experiment, date=date)
    order = list(T.EXPERIMENT["conditions"])
    for cond_dir in (d for d in sorted(run_dir.iterdir()) if d.is_dir()):
        # a replay's condition holds configs/; a tournament's holds seat<k>/configs/<player>/
        seat_dirs = [cond_dir] if (cond_dir / "configs").is_dir() else \
            [d for d in sorted(cond_dir.glob("seat*")) if (d / "configs").is_dir()]
        if not seat_dirs:
            continue
        name = ALIASES.get(cond_dir.name, cond_dir.name)
        spec = experiment.get("conditions", {}).get(cond_dir.name) or T.EXPERIMENT["conditions"].get(name, {})
        players = []
        for seat_dir in seat_dirs:
            for path in sorted((seat_dir / "configs").rglob("player*_config.json")):
                cfg = json.loads(path.read_text())
                if not cfg.get("llm", {}).get("type", "llamacpp").startswith(("llamacpp", "ollama")):
                    continue  # a bot or a human: no LLM answers to score
                identity = cfg["player"]["identity"]
                players.append(Player(identity, _model_name(experiment, identity),
                                      cfg["llm"].get("prompt_style") or spec.get("prompt", ""),
                                      {k: cfg["connectivity"][k] for k in ("player1_ip", "player2_ip")}, seat_dir))
        backend = next((v.get("backend") for k, v in recorded.items() if k.split("/")[0] == cond_dir.name), None)
        run.conditions.append(Condition(name, cond_dir, backend or manifest.get("backend", "?"), players))
    run.conditions.sort(key=lambda c: (order.index(c.name) if c.name in order else len(order), c.name))
    return run


def answer_files(cond_dir: Path, identity: str) -> list[Path]:
    games = sorted((cond_dir / identity).glob("game_*.log"))
    if games:
        return games
    combined = cond_dir / f"{identity}_llm.log"
    return [combined] if combined.exists() else []


def replay_items(run: Run) -> dict[str, dict]:
    """The replay corpus's items, keyed by state: id, slice, the peers the prompts showed, and for
    held-out training states the teacher's answer."""
    path = REPO_ROOT / run.experiment.get("replay", {}).get("corpus", T.EXPERIMENT["replay"]["corpus"])
    if run.kind != "replay" or not path.exists():
        return {}
    return {corpus.state_key(item["state"]): {**item, "slice": item.get("slice", "game")}
            for item in json.loads(path.read_text())}


# ── Scoring ────────────────────────────────────────────────────────────────────

def score_answers(entries, player: Player, items: dict, kind: str) -> list[dict]:
    """Per answer: its item and slice, schema failure, legality verdict, reference check and teacher
    match."""
    answers, seen, previous = [], Counter(), None
    for e in entries:
        key = corpus.state_key(e.state)
        if kind == "tournament" and key == previous:
            continue  # a retry of the same decision: only its first attempt counts
        previous = key
        item = items.get(key)
        peers = item["peers"] if item else player.peers
        verdict = legality.check(e.state, e.raw, player.style, peers)
        if item:
            slice_, item_key = item["slice"], item["id"]
        else:
            seen[key] += 1
            slice_, item_key = ("games" if kind == "tournament" else "unmatched"), f"{key}#{seen[key]}"
        teacher_match = None
        if item and item.get("teacher"):
            taught = legality.check(e.state, item["teacher"], TEACHER_STYLE, peers)
            teacher_match = verdict.decision is not None and verdict.decision == taught.decision
        answers.append({"state": e.state, "peers": peers, "phase": e.phase, "item": item_key, "slice": slice_,
                        "schema": schema_validity.check(e.phase, e.raw), "verdict": verdict,
                        "reference": reference.check(e.state, verdict), "teacher_match": teacher_match})
    return answers


def summaries(answers: list[dict]) -> dict:
    """Every metric's summary of one model's answers in one condition and slice."""
    legal = [a for a in answers if a["verdict"].legal]
    return {
        "answers": len(answers),
        "schema_validity": schema_validity.summarize([(a["phase"], a["schema"]) for a in answers]),
        "legality": legality.summarize([(a["phase"], a["verdict"], a["schema"] is None) for a in answers]),
        "reference": reference.summarize([(a["phase"], a["reference"], a["teacher_match"]) for a in answers]),
        "state_sensitivity": state_sensitivity.summarize(
            [(a["phase"], state_sensitivity.facts(a["state"], a["verdict"].message)) for a in legal]),
    }


def outcomes(answers: list[dict]) -> dict[str, dict[str, bool]]:
    """Per outcome, {item: holds?} — what effects.py and run-vs-run tests pair on."""
    return {"schema-valid": {a["item"]: a["schema"] is None for a in answers},
            "legal": {a["item"]: a["verdict"].legal for a in answers},
            "reference-correct": {a["item"]: a["reference"]["correct"] for a in answers}}


def teacher_rows(corpus_path: Path) -> dict:
    """State sensitivity and reference decisions of the training corpus's own answers."""
    sensitivity, ref = [], []
    for e in corpus.read(corpus_path):
        verdict = legality.check(e.state, e.raw, TEACHER_STYLE, TEACHER_PEERS)
        ref.append((e.phase, reference.check(e.state, verdict), None))
        if verdict.legal:
            sensitivity.append((e.phase, state_sensitivity.facts(e.state, verdict.message)))
    return {"state_sensitivity": state_sensitivity.summarize(sensitivity), "reference": reference.summarize(ref)}


# ── Report ─────────────────────────────────────────────────────────────────────

def _section(module) -> list[str]:
    """A heading and its question, from the first paragraph of the metric module's docstring."""
    para = " ".join(module.__doc__.strip().split("\n\n")[0].split())
    title, _, question = para.partition(": ")
    return [f"## {title}", "", question[:1].upper() + question[1:], ""]


def headline(s: dict) -> dict:
    """One model's headline numbers in one condition: a share as (part, whole), the accept gap in
    points (REPLY and CONSIDERING pooled)."""
    sv, lg, rf, ss = s["schema_validity"], s["legality"], s["reference"], s["state_sensitivity"]
    pooled = {k: ss["REPLY"][k] + ss["CONSIDERING"][k] for k in ss["REPLY"]}
    return {
        "schema-valid": (sv["valid"], sv["n"]),
        "legal": (lg["legal"], lg["n"]),
        "reference-correct": (rf["correct"], rf["n"]),
        "accept gap useful−useless": state_sensitivity.accept_gap(pooled),
        "avoidable harvests": (ss["PLANTING"]["avoidable_harvest"] + ss["FORCED"]["avoidable_harvest"],
                               ss["PLANTING"]["n"] + ss["FORCED"]["n"]),
    }


WITH_CI = ("schema-valid", "legal", "reference-correct")


def _shown(value, with_ci: bool = False) -> str:
    if isinstance(value, tuple):
        return ci(*value) if with_ci else pct(*value)
    return "–" if value is None else f"{value:+.0f}"


def _overview(rows) -> list[str]:
    body = [cells + [s["answers"], *[_shown(v, k in WITH_CI) for k, v in headline(s).items()]] for cells, s in rows]
    names = list(headline(rows[0][1])) if rows else []
    return markdown(["condition", "model", "answers", *names], body)


def render_slice(run: Run, slice_: str, results: dict, teacher: dict | None, pairs: dict, eff: dict) -> list[str]:
    rows = [([cond.name, model], results[cond.name][identity])
            for cond in run.conditions for identity, model in cond.models.items() if identity in results.get(cond.name, {})]
    items = max((s["answers"] for _, s in rows), default=0)
    backends = sorted({c.backend for c in run.conditions})
    corpus_name = run.corpus_path.relative_to(REPO_ROOT) if run.corpus_path else "none"
    lines = [f"# {run.name}: {SLICES.get(slice_, slice_)}", "",
             f"{run.kind} run, backend {', '.join(backends)}; {items} answers per model and condition; training "
             f"corpus `{corpus_name}`; evaluated {datetime.now():%Y-%m-%d %H:%M}. "
             "Shares in brackets are 95% Wilson intervals.", "",
             "## Overview", "", *_overview(rows), ""]
    if any(eff.values()):
        lines += [*_section(effects), "Rows marked * stay significant after the Holm correction.", ""]
        for outcome, effect_rows in eff.items():
            lines += [f"### {outcome}", "", *effects.table(effect_rows), ""]
    lines += [*_section(schema_validity), *schema_validity.table([(c, s["schema_validity"]) for c, s in rows]), ""]
    lines += [*_section(legality), *legality.table([(c, s["legality"]) for c, s in rows]), ""]
    ref_rows = [(c, s["reference"]) for c, s in rows] + ([(["teacher", "training corpus"], teacher["reference"])]
                                                         if teacher else [])
    lines += [*_section(reference), *reference.table(ref_rows), "", "Each rule on its own (partial credit):", "",
              *reference.rules_table(ref_rows), ""]
    by_phase = reference.teacher_table([(c, s["reference"]) for c, s in rows])
    if by_phase:
        lines += ["Teacher match per message type (the decision equals the teacher's held-out answer):", "",
                  *by_phase, ""]
    sens_rows = [(c, s["state_sensitivity"]) for c, s in rows] + ([(["teacher", "training corpus"],
                                                                    teacher["state_sensitivity"])] if teacher else [])
    lines += [*_section(state_sensitivity), *state_sensitivity.table(sens_rows), ""]
    if pairs:
        lines += [*_section(agreement), "Same decision on the same item (95% CI; compared items in brackets).", ""]
        for model, model_pairs in pairs.items():
            lines += [*agreement.table(model, [c.name for c in run.conditions], model_pairs), ""]
    return lines


def _jsonable(value):
    if isinstance(value, dict):
        return {("|".join(k) if isinstance(k, tuple) else k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    if isinstance(value, tuple):
        return [_jsonable(v) for v in value]
    return value


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("runs", nargs="+", type=Path, help="run directories (logs/replay_<id>, logs/suite_<id>)")
    p.add_argument("--training-corpus", type=Path, help="the teacher's rows from this corpus instead of the run's own")
    args = p.parse_args()

    runs = [load_run(d) for d in dict.fromkeys(d.resolve() for d in args.runs)]
    teachers: dict[Path, dict] = {}
    scored = {}  # run name -> condition -> identity -> answers
    for run in runs:
        corpus_path = (args.training_corpus or REPO_ROOT / run.experiment["training"]["corpus"]).resolve()
        if not corpus_path.exists():
            info(f"{run.name}: training corpus {corpus_path} not found — no teacher rows")
            corpus_path = None
        elif corpus_path not in teachers:
            info(f"Reading the training corpus {corpus_path.name}...")
            teachers[corpus_path] = teacher_rows(corpus_path)
        run.corpus_path = corpus_path
        items = replay_items(run)
        scored[run.name] = {}
        for cond in run.conditions:
            scored[run.name][cond.name] = {}
            for player in cond.players:  # a tournament player once per seat it played
                files = answer_files(player.logs, player.identity)
                if not files:
                    info(f"{run.name}/{cond.name}: no logs for {player.identity} in {player.logs.name}")
                    continue
                entries = [e for f in files for e in corpus.read(f)]
                scored[run.name][cond.name].setdefault(player.identity, []).extend(score_answers(
                    entries, player, items, run.kind))
        answers = [a for c in scored[run.name].values() for ans in c.values() for a in ans]
        info(f"{run.name}: {len(answers)} answers scored " + str(dict(Counter(a["slice"] for a in answers))))
        if any(a["slice"] == "unmatched" for a in answers):
            info(f"{run.name}: some states are not in the replay corpus — scored as slice 'unmatched'")

    all_results = {}
    for run in runs:
        by_slice: dict[str, dict] = {}
        for cond, by_id in scored[run.name].items():
            for identity, answers in by_id.items():
                for a in answers:
                    by_slice.setdefault(a["slice"], {}).setdefault(cond, {}).setdefault(identity, []).append(a)
        order = [s for s in SLICES if s in by_slice]
        results, slice_data, lines = {}, {}, []
        teacher = teachers.get(run.corpus_path)
        for slice_ in order:
            answers_of = by_slice[slice_]
            results[slice_] = {cond: {identity: summaries(ans) for identity, ans in by_id.items()}
                               for cond, by_id in answers_of.items()}
            pairs, eff = {}, {}
            if run.kind == "replay":
                models = {p.identity: p.model for c in run.conditions for p in c.players}
                for identity, model in models.items():
                    decisions = {c: agreement.decisions([(a["item"], a["phase"], a["verdict"].decision)
                                                         for a in answers_of.get(c, {}).get(identity, [])])
                                 for c in answers_of}
                    names = [c.name for c in run.conditions if c.name in decisions]
                    pairs[model] = {(a, b): agreement.compare(decisions[a], decisions[b])
                                    for i, a in enumerate(names) for b in names[i + 1:]}
                eff = effects.effects({c: {models[i]: outcomes(ans) for i, ans in by_id.items()}
                                       for c, by_id in answers_of.items()}, [c.name for c in run.conditions],
                                      list(dict.fromkeys(models.values())))
            slice_data[slice_] = {"conditions": results[slice_], "agreement": pairs, "effects": eff}
            lines += render_slice(run, slice_, results[slice_], teacher, pairs, eff)
        games, compared = {}, []
        if run.kind == "tournament":
            for cond in run.conditions:
                csvs = sorted(cond.dir.rglob("tournament_*.csv"))
                if csvs:
                    games[cond.name] = game_outcomes.summarize(csvs, list(cond.models))
        if games:
            lines += _section(game_outcomes)
            old_style = {c: g for c, g in games.items() if g["format"] == "identities"}
            if old_style:
                lines += [*game_outcomes.table([([cond.name, model], games[cond.name], identity)
                                                for cond in run.conditions if cond.name in old_style
                                                for identity, model in cond.models.items()]), ""]
            new_style = {c: g for c, g in games.items() if g["format"] == "players"}
            if new_style:
                against = run.experiment.get("tournament", {}).get("opponents")
                lines += [f"Opponents: two {against} bots in every game.", ""] if against else []
                names = {i: m for c in run.conditions for i, m in c.models.items()}
                players = {(cond, player): s for cond, g in new_style.items() for player, s in g["players"].items()}
                lines += [*game_outcomes.player_table([([cond, names.get(player, player)], s)
                                                       for (cond, player), s in players.items()]), ""]
                compared = game_outcomes.comparisons(players)
                lines += ["Paired differences in coins per game from the baseline bots, on the same seeds and seats:", "",
                          *game_outcomes.comparison_table(compared, names), ""]
            lines += [f"Note: {note}." for note in sorted({n for g in games.values() for n in g.get("notes", [])})]
            lines.append("")
        all_results[run.name] = results
        report = "\n".join(lines)
        (run.dir / "metrics.md").write_text(report + "\n")
        (run.dir / "metrics.json").write_text(json.dumps(_jsonable({
            "run": run.name, "kind": run.kind, "evaluated_at": datetime.now().isoformat(timespec="seconds"),
            "training_corpus": str(run.corpus_path.relative_to(REPO_ROOT)) if run.corpus_path else None,
            "slices": slice_data, "teacher": teacher, "games": games,
            "game_comparisons": compared}), indent=1))
        print(report)
        info(f"Written {run.dir / 'metrics.md'} and metrics.json")

    if len(runs) > 1:
        compare_runs(runs, scored, all_results)


def compare_runs(runs: list[Run], scored: dict, results: dict) -> None:
    """Run against run, for every pair of runs and every slice, condition and model both have —
    e.g. the same replay on two backends: the share of items decided the same (agreement.py), and
    the overview's numbers of both runs side by side, with the exact McNemar p of the paired items
    for schema-valid, legal and reference-correct."""
    lines = ["# Run against run", "", *_section(agreement)[2:]]
    data = {}
    for i, ra in enumerate(runs):
        for rb in runs[i + 1:]:
            for slice_ in [s for s in SLICES if s in results[ra.name] and s in results[rb.name]]:
                rows, names = [], []
                for cond in ra.conditions:
                    if cond.name not in results[rb.name][slice_] or cond.name not in results[ra.name][slice_]:
                        continue
                    for player in {p.identity: p for p in cond.players}.values():
                        sa = results[ra.name][slice_][cond.name].get(player.identity)
                        sb = results[rb.name][slice_][cond.name].get(player.identity)
                        if not sa or not sb:
                            continue
                        a = [x for x in scored[ra.name][cond.name][player.identity] if x["slice"] == slice_]
                        b = [x for x in scored[rb.name][cond.name][player.identity] if x["slice"] == slice_]
                        r = agreement.compare(
                            agreement.decisions([(x["item"], x["phase"], x["verdict"].decision) for x in a]),
                            agreement.decisions([(x["item"], x["phase"], x["verdict"].decision) for x in b]))
                        ha, hb = headline(sa), headline(sb)
                        oa, ob = outcomes(a), outcomes(b)
                        side = []
                        for k in ha:
                            cell = _shown(ha[k]) if _shown(ha[k]) == _shown(hb[k]) else f"{_shown(ha[k])} → {_shown(hb[k])}"
                            if k in oa and _shown(ha[k]) != _shown(hb[k]):
                                keys = oa[k].keys() & ob[k].keys()
                                p = mcnemar(sum(oa[k][x] and not ob[k][x] for x in keys),
                                            sum(ob[k][x] and not oa[k][x] for x in keys))
                                cell += f" (p {'<0.001' if p < 0.001 else f'{p:.2f}'})"
                            side.append(cell)
                        names = list(ha)
                        data[f"{ra.name}|{rb.name}|{slice_}|{cond.name}|{player.identity}"] = {
                            "agreement": r, "a": ha, "b": hb}
                        rows.append([cond.name, player.model, r["n"], ci(r["same"], r["n"]), *side])
                if rows:
                    lines += [f"## {ra.name} vs {rb.name}: {SLICES.get(slice_, slice_)}", "",
                              f"A = {ra.label}, B = {rb.label}. Same decision: the share of the items both runs "
                              "answered (compared items) decided the same, with its 95% interval. Other columns: the "
                              "overview's numbers — one value where the runs agree, A → B where they differ, with the "
                              "exact McNemar p of the paired items for schema-valid, legal and reference-correct.", "",
                              *markdown(["condition", "model", "compared items", "same decision", *names], rows), ""]
    md = "\n".join(lines)
    (runs[0].dir / "comparison.md").write_text(md + "\n")
    (runs[0].dir / "comparison.json").write_text(json.dumps(_jsonable(data), indent=1))
    print(md)
    info(f"Written {runs[0].dir / 'comparison.md'} and .json")


if __name__ == "__main__":
    main()
