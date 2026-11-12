#!/usr/bin/env python3
"""Run the whole experiment unattended: adapters, replay, tournament, evaluation.

    python3 run_experiment.py                  # everything on the GPU, the config's games per condition
    python3 run_experiment.py --games 5        # a shorter tournament
    python3 run_experiment.py --cpu            # llama.cpp's CPU build for every server
    python3 run_experiment.py --id ID          # resume: finished steps are skipped
    python3 run_experiment.py --tournament-only    # tournament and its evaluation
    python3 run_experiment.py --tournament-only --opponents bot_random --only lora_compact,bot_reference
                                               # some players only, against random bots
    python3 run_experiment.py --cpu --replay-only --include-experiment GPU_ID
                                               # a CPU replay, compared item by item with an earlier
                                               # experiment's replay

To keep it running after logout:
    setsid nohup python3 run_experiment.py --id ID > /dev/null 2>&1 &

Each step is one of the project's scripts; a failed step is recorded and the later steps still
run on whatever exists:
    1  train_adapters.py               trains only the adapters that do not exist yet
    2  replay.py --run-id ID           logs/replay_<ID>/
    3  tournament.py --run-id ID       logs/suite_<ID>/
    4  eval/evaluate.py                the replay, with the newest earlier replay of the same models
                                       and adapters (run-to-run agreement)
    5  eval/evaluate.py                the tournament
--cpu applies to the replay and the tournament.

Progress and output: logs/experiment_<ID>/status.json and output.log.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
LOGS_DIR = REPO_ROOT / "logs"


def same_models(run_dir: Path) -> bool:
    """Whether an earlier run served the models and adapter set the config names now: evaluate.py
    pairs players by identity, so a run of other models would be compared slot against slot."""
    served = lambda e: (e.get("adapters"), [m.get("gguf") for m in e.get("models", [])])
    then = json.loads((run_dir / "run.json").read_text()).get("experiment", {})
    return served(then) == served(json.loads((REPO_ROOT / "config" / "experiment.json").read_text()))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--id", default=f"{datetime.now():%Y%m%d_%H%M%S}", help="run id (resume with the same id)")
    p.add_argument("--games", type=int, help="tournament games per condition (default: the config's)")
    p.add_argument("--cpu", action="store_true", help="llama.cpp's CPU build instead of the CUDA one")
    p.add_argument("--replay-only", action="store_true", help="no tournament")
    p.add_argument("--tournament-only", action="store_true", help="no replay")
    p.add_argument("--opponents", help="the tournament's opponent bots (default: the config's)")
    p.add_argument("--only", help="only these tournament players (tournament.py --only)")
    p.add_argument("--compare-with", type=Path, metavar="RUN_DIR",
                   help="the earlier replay to compare with (default: the newest evaluated one of the same models)")
    p.add_argument("--include-experiment", metavar="ID",
                   help="an earlier experiment: its replay is the one compared with")
    args = p.parse_args()

    exp_dir = LOGS_DIR / f"experiment_{args.id}"
    exp_dir.mkdir(parents=True, exist_ok=True)
    status_path, log_path = exp_dir / "status.json", exp_dir / "output.log"
    status = json.loads(status_path.read_text()) if status_path.exists() else {"id": args.id, "steps": {}}
    replay_dir, suite_dir = LOGS_DIR / f"replay_{args.id}", LOGS_DIR / f"suite_{args.id}"
    earlier = sorted((d for d in LOGS_DIR.glob("replay_*") if d.is_dir() and d != replay_dir
                      and (d / "metrics.json").exists() and (d / "run.json").exists() and same_models(d)),
                     key=lambda d: d.stat().st_mtime)
    backend = ["--cpu"] if args.cpu else []
    py = sys.executable
    rel = lambda path: str(path.relative_to(REPO_ROOT))
    other = args.include_experiment
    compare = ([args.compare_with.resolve()] if args.compare_with
               else [LOGS_DIR / f"replay_{other}"] if other else earlier[-1:])

    steps = [
        ("adapters", [py, "train_adapters.py"]),
        ("replay", [py, "replay.py", "--run-id", args.id, *backend]),
        ("tournament", [py, "tournament.py", "--run-id", args.id, *backend]
         + (["--games", str(args.games)] if args.games else [])
         + (["--opponents", args.opponents] if args.opponents else [])
         + (["--only", args.only] if args.only else [])),
        ("evaluate replay", [py, "eval/evaluate.py", rel(replay_dir), *map(rel, compare)]),
        ("evaluate tournament", [py, "eval/evaluate.py", rel(suite_dir)]),
    ]
    if args.replay_only:
        steps = [step for step in steps if step[0] not in ("tournament", "evaluate tournament")]
    if args.tournament_only:
        steps = [step for step in steps if step[0] not in ("replay", "evaluate replay")]
    for name, cmd in steps:
        if status["steps"].get(name, {}).get("exit") == 0:
            continue
        record = {"command": " ".join(cmd), "started": datetime.now().isoformat(timespec="seconds")}
        status["steps"][name] = record
        status_path.write_text(json.dumps(status, indent=2))
        with open(log_path, "a") as log:
            log.write(f"\n===== {name}: {record['command']} ({record['started']}) =====\n")
            log.flush()
            record["exit"] = subprocess.run(cmd, cwd=REPO_ROOT, stdout=log, stderr=subprocess.STDOUT).returncode
        record["finished"] = datetime.now().isoformat(timespec="seconds")
        status_path.write_text(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
