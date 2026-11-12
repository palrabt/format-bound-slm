#!/usr/bin/env python3
"""Play the tournament: each player against two fixed bots, on the same seeded games.

    python3 tournament.py                  # the config's "tournament" section, on the GPU
    python3 tournament.py --games 3        # a smoke test
    python3 tournament.py --cpu            # llama.cpp's CPU build instead of the CUDA one
    python3 tournament.py --run-id ID      # resume logs/suite_<ID>/ (finished blocks are kept)
    python3 tournament.py --only lora_compact:Beta,bot_reference   # only these players
    python3 tournament.py --opponents bot_random   # against random bots instead of the config's

The evaluated players are every model under every condition in tournament.conditions, and the
baseline bots in tournament.baselines (game/player/bots.py: the reference rules, a random legal
player). Each plays tournament.games games against two tournament.opponents bots: game g uses deck
seed g, so every player plays the same card sequences, and seat (g - 1) % 3, so each plays every
seat equally often. A block — one player in one seat — starts its servers (start_game.sh), plays its
games and stops them. The LLM answers once per decision (llm_max_retries 1: at temperature 0 a retry
repeats the answer). A game ends when the deck runs out; TIMEOUT_S is only a safety net, and a game
that hits it is marked unfinished. Nothing is scored here: eval/evaluate.py scores a finished run.

Output, read by eval/evaluate.py:
    logs/suite_<id>/run.json                              kind, the experiment config, finished blocks
      <condition>/seat<k>/configs/<player>/player{1,2,3}_config.json
      <condition>/seat<k>/<identity>/game_<seed>.log      the LLM player's own log, one file per game
      <condition>/seat<k>/tournament_<player>.csv         per game: seed, seat, coins, penalty,
                                                           the opponents' coins
      <condition>/seat<k>/<player>_deck.log, _player{1,2,3}.log
A baseline bot's <condition> is its kind (bot_reference or bot_random).

GPU by default: every llama-server this starts is <llama_cpp>/build-cuda/bin/llama-server; --cpu
uses <llama_cpp>/llama-server.
"""

import argparse
import csv
import json
import os
import shutil
import subprocess
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent
LOGS_DIR = REPO_ROOT / "logs"
EXPERIMENT_FILE = REPO_ROOT / "config" / "experiment.json"

EXPERIMENT: dict = json.loads(EXPERIMENT_FILE.read_text())
CONDITIONS: list[str] = list(EXPERIMENT["conditions"])
MODELS: list[dict] = EXPERIMENT["models"]
SLOT_COUNT = 3
IDENTITIES: list[str] = [m["identity"] for m in MODELS]
BOT_KINDS = ("bot_reference", "bot_random")  # game/player/bots.py BOTS

DECK = "http://localhost:8765"
PLAYERS = [f"http://localhost:{8765 + slot}" for slot in range(1, SLOT_COUNT + 1)]
GAME_TIMEOUT_S = 2700   # safety net only: a game ends when the deck runs out
POLL_INTERVAL_S = 5     # how often to check the deck log for game_over
POST_GAME_SETTLE = 5    # seconds to wait after game_over before reading final state
GAME_LOG_FILES = ["deck.log", "player1.log", "player2.log", "player3.log"]

if len(MODELS) != SLOT_COUNT:
    raise SystemExit(f"{EXPERIMENT_FILE}: needs {SLOT_COUNT} models (one per player), found {len(MODELS)}")


def info(msg: str) -> None: print(f"\033[0;36m[run]\033[0m {msg}", flush=True)
def success(msg: str) -> None: print(f"\033[0;32m[run]\033[0m {msg}", flush=True)
def warn(msg: str) -> None: print(f"\033[0;33m[run]\033[0m {msg}", flush=True)


# ── Experiment setup (shared with replay.py) ──────────────────────────────────

def adapter_path(model: dict) -> str:
    """The model's adapter in the configured set: artifacts/<name>/<name>_<adapters>.gguf."""
    return f"artifacts/{model['name']}/{model['name']}_{EXPERIMENT['adapters']}.gguf"


def check_adapters() -> None:
    """Fail before any server starts if a condition needs an adapter that was never trained."""
    if not any(spec["lora"] for spec in EXPERIMENT["conditions"].values()):
        return
    missing = [adapter_path(m) for m in MODELS if not (REPO_ROOT / adapter_path(m)).exists()]
    if missing:
        raise SystemExit("adapters not found (train them with train_adapters.py, or change \"adapters\" in "
                         f"{EXPERIMENT_FILE.relative_to(REPO_ROOT)}):\n  " + "\n  ".join(missing))


def use_backend(cpu: bool) -> str:
    """Point every llama-server this process starts (the players' LLMs) at one llama.cpp build
    (game/llm/manager.py reads LLAMA_SERVER_BIN)."""
    llama_cpp = (REPO_ROOT / EXPERIMENT["llama_cpp"]).resolve()
    binary = llama_cpp / "llama-server" if cpu else llama_cpp / "build-cuda" / "bin" / "llama-server"
    if not binary.exists():
        raise SystemExit(f"llama-server not found: {binary}" + ("" if cpu else " (or run with --cpu)"))
    os.environ["LLAMA_SERVER_BIN"] = str(binary)
    return "cpu" if cpu else "gpu"


def player_config(slot: int, condition: str, scenario: str) -> dict:
    """The player config of one slot under one condition. Ports follow the slot: player 8765+slot,
    its LLM 11433+slot, the deck 8765. `scenario` is where the player's logger writes
    (logs/<scenario>/<identity>/game_NNNN.log, see game/player/llm.py:llm_log_path)."""
    model, spec = MODELS[slot - 1], EXPERIMENT["conditions"][condition]
    peers = [s for s in range(1, SLOT_COUNT + 1) if s != slot]
    return {
        "player": {"self_ip": f"http://localhost:{8765 + slot}", "port": 8765 + slot,
                   "identity": model["identity"], "scenario": scenario},
        "connectivity": {"player1_ip": f"http://localhost:{8765 + peers[0]}",
                         "player2_ip": f"http://localhost:{8765 + peers[1]}",
                         "llm_ip": f"http://localhost:{11433 + slot}", "deck_ip": DECK},
        "llm": {"type": "llamacpp", "port": 11433 + slot, "backend": "", "gguf": model["gguf"],
                "lora": adapter_path(model) if spec["lora"] else "", "prompt_style": spec["prompt"],
                "chat_template_file": model.get("chat_template", "")},
    }


def write_condition_configs(dest_dir: Path, condition: str, scenario: str) -> list[Path]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for slot in range(1, SLOT_COUNT + 1):
        path = dest_dir / f"player{slot}_config.json"
        path.write_text(json.dumps(player_config(slot, condition, scenario), indent=2))
        paths.append(path)
    return paths


def wait_for_llms(config_paths: list[Path], timeout: int = 600) -> None:
    """llama-server answers 503 while it loads the model; a player asking then would fail its turn."""
    deadline = time.time() + timeout
    for path in config_paths:
        llm = json.loads(path.read_text())["llm"]
        if llm.get("type") != "llamacpp":
            continue  # a bot or a human: no server
        port = llm["port"]
        while True:
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=5) as r:
                    if json.loads(r.read()).get("status") == "ok":
                        break
            except Exception:
                pass
            if time.time() > deadline:
                raise RuntimeError(f"the LLM on port {port} did not become ready within {timeout} s")
            time.sleep(2)


# ── Run manifest (shared with replay.py) ──────────────────────────────────────

def record_condition(run_dir: Path, kind: str, condition: str, backend: str) -> None:
    """run.json: the kind of run, the experiment config it started with, and for every finished
    condition its backend and finishing time. eval/evaluate.py reads it; a resumed run skips the
    conditions it lists."""
    path = run_dir / "run.json"
    manifest = json.loads(path.read_text()) if path.exists() else \
        {"kind": kind, "experiment": EXPERIMENT, "conditions": {}}
    manifest["conditions"][condition] = {"backend": backend, "finished": datetime.now().isoformat(timespec="seconds")}
    path.write_text(json.dumps(manifest, indent=2))


def condition_finished(run_dir: Path, condition: str) -> bool:
    path = run_dir / "run.json"
    return path.exists() and condition in json.loads(path.read_text()).get("conditions", {})


def check_resumable(run_dir: Path) -> None:
    """A run directory written before run.json existed has no record of its finished conditions;
    resuming it would delete and redo them all."""
    if any(run_dir.iterdir()) and not (run_dir / "run.json").exists():
        raise SystemExit(f"{run_dir} has no run.json (an older run): resume refused, use a new --run-id")


# ── Game servers ──────────────────────────────────────────────────────────────

def start_servers(config_paths: list[Path]) -> None:
    info("Starting game servers...")
    # --no-init: start_game.sh would otherwise deal a startup game that player 1 begins playing,
    # only for play_games to reset it — its stray turns would land in the logs
    subprocess.run(["./start_game.sh", "--no-init", "--players", *[str(p) for p in config_paths]],
                   cwd=REPO_ROOT, check=True, timeout=600)
    deadline = time.time() + 60
    while True:
        try:
            with urllib.request.urlopen(f"{DECK}/status", timeout=5):
                break
        except Exception:
            if time.time() > deadline:
                raise RuntimeError("Deck server did not become reachable after start_game.sh")
            time.sleep(2)
    wait_for_llms(config_paths)


def stop_servers() -> None:
    info("Stopping game servers...")
    subprocess.run(["./start_game.sh", "stop"], cwd=REPO_ROOT, check=False, timeout=60)
    time.sleep(5)


# ── Games ─────────────────────────────────────────────────────────────────────

def _get(url: str, timeout: int = 30) -> dict[str, Any]:
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read())


def _post(url: str, data: dict | None = None, timeout: int = 30) -> dict[str, Any]:
    req = urllib.request.Request(url, data=json.dumps(data or {}).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def _reset_and_init(seed: int) -> dict[str, int]:
    """Deal game `seed` and re-initialise all players (their logs number the game `seed`). Returns
    {player_url: penalty at game start}, for per-game penalty increments (/init keeps the penalty)."""
    _post(f"{DECK}/reset", {"seed": seed})
    time.sleep(1)
    start_penalties: dict[str, int] = {}
    for url in PLAYERS:
        try:
            _get(f"{url}/init?game={seed}", timeout=30)
            time.sleep(0.5)
            start_penalties[url] = _get(f"{url}/state").get("penalty", 0)
        except Exception as e:
            print(f"  [warn] /init failed for {url}: {e}")
            start_penalties[url] = 0
    return start_penalties


def _wait_game_over(timeout: int = GAME_TIMEOUT_S) -> bool:
    """Poll the deck /log until a game_over=true entry appears (the deck writes it into the
    /endturn response once the main deck is exhausted)."""
    seq = 0
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            data = _get(f"{DECK}/log?since={seq}", timeout=10)
            seq = data.get("seq", seq)
            for entry in data.get("entries", []):
                if '"game_over": true' in entry.get("summary", ""):
                    return True
        except Exception:
            pass
        time.sleep(POLL_INTERVAL_S)
    return False


def _final_state(start_penalties: dict[str, int]) -> dict[str, tuple[int | None, int | None]]:
    """{player_url: (coins, penalty increment)} once a game is over."""
    time.sleep(POST_GAME_SETTLE)
    out = {}
    for url in PLAYERS:
        try:
            s = _get(f"{url}/state")
            out[url] = (s.get("coins", 0), s.get("penalty", 0) - start_penalties.get(url, 0))
        except Exception as e:
            print(f"  [warn] state collection failed for {url}: {e}")
            out[url] = (None, None)
    return out


# ── Blocks: one evaluated player in one seat ─────────────────────────────────

def opponents() -> str:
    return EXPERIMENT["tournament"].get("opponents", "bot_reference")


def bot_config(slot: int, kind: str, identity: str, scenario: str) -> dict:
    """A rule-based player (game/player/bots.py) in one slot; the llm port is only a placeholder."""
    peers = [s for s in range(1, SLOT_COUNT + 1) if s != slot]
    return {
        "player": {"self_ip": f"http://localhost:{8765 + slot}", "port": 8765 + slot, "identity": identity,
                   "scenario": scenario},
        "connectivity": {"player1_ip": f"http://localhost:{8765 + peers[0]}",
                         "player2_ip": f"http://localhost:{8765 + peers[1]}",
                         "llm_ip": f"http://localhost:{11433 + slot}", "deck_ip": DECK},
        "llm": {"type": kind, "port": 11433 + slot},
    }


def block_configs(dest: Path, seat: int, condition: str, model: dict | None, kind: str | None,
                  scenario: str) -> tuple[list[Path], str]:
    """Configs of one block: the evaluated player (an LLM `model` under `condition`, or a `kind` of
    bot) in slot seat + 1, opponent bots elsewhere. Returns (paths, the evaluated player's identity)."""
    dest.mkdir(parents=True, exist_ok=True)
    slot = seat + 1
    if model is not None:
        cfg = player_config(1, condition, scenario)  # slot-1 template, moved to its slot below
        peers = [s for s in range(1, SLOT_COUNT + 1) if s != slot]
        cfg["player"].update({"self_ip": f"http://localhost:{8765 + slot}", "port": 8765 + slot,
                              "identity": model["identity"], "llm_max_retries": 1})
        cfg["connectivity"].update({"player1_ip": f"http://localhost:{8765 + peers[0]}",
                                    "player2_ip": f"http://localhost:{8765 + peers[1]}",
                                    "llm_ip": f"http://localhost:{11433 + slot}"})
        spec = EXPERIMENT["conditions"][condition]
        cfg["llm"].update({"port": 11433 + slot, "gguf": model["gguf"], "lora": adapter_path(model) if spec["lora"] else "",
                           "chat_template_file": model.get("chat_template", "")})
        player, identity = cfg, model["identity"]
    else:
        identity = kind
        player = bot_config(slot, kind, identity, scenario)
    paths = []
    for s in range(1, SLOT_COUNT + 1):
        cfg = player if s == slot else bot_config(s, opponents(), f"opponent{s}", scenario)
        path = dest / f"player{s}_config.json"
        path.write_text(json.dumps(cfg, indent=2))
        paths.append(path)
    return paths, identity


def play_block(seat_dir: Path, configs: list[Path], identity: str, seat: int, seeds: list[int]) -> Path:
    """Play the block's games and write one CSV row per game."""
    csv_path = seat_dir / f"tournament_{identity}.csv"
    rows = []
    for seed in seeds:
        print(f"  {identity} seat {seat + 1} game {seed:3d}  ", end="", flush=True)
        start_penalties = _reset_and_init(seed)
        finished = _wait_game_over()
        final = _final_state(start_penalties)
        me = PLAYERS[seat]
        others = [final[u][0] for u in PLAYERS if u != me]
        coins, penalty = final[me]
        rows.append({"game": seed, "seat": seat + 1, "player": identity, "finished": finished,
                     "coins": coins, "penalty_delta": penalty,
                     "opponent_coins": ";".join("" if c is None else str(c) for c in others)})
        print(f"[{'OK     ' if finished else 'TIMEOUT'}]  {coins}c +{penalty}p  opponents {others}", flush=True)
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return csv_path


def run_block(run_dir: Path, condition: str, model: dict | None, kind: str | None, seat: int, seeds: list[int]) -> None:
    seat_dir = run_dir / condition / f"seat{seat + 1}"
    name = model["identity"] if model else kind
    configs, identity = block_configs(seat_dir / "configs" / name, seat, condition, model, kind,
                                      scenario=f"{run_dir.name}/{condition}/seat{seat + 1}")
    for old in (seat_dir / identity).glob("game_*.log") if (seat_dir / identity).exists() else []:
        old.unlink()  # whatever an interrupted attempt left behind
    info(f"=== {condition}: {identity} in seat {seat + 1}, games {seeds[0]}..{seeds[-1]} ===")
    try:
        start_servers(configs)
        play_block(seat_dir, configs, identity, seat, seeds)
    finally:
        stop_servers()
    for log in GAME_LOG_FILES:  # start_game.sh writes these to logs/
        if (LOGS_DIR / log).exists():
            shutil.move(str(LOGS_DIR / log), str(seat_dir / f"{identity}_{log}"))


def blocks(games: int, only: set[str] = frozenset()) -> list[tuple[str, dict | None, str | None, int, list[int]]]:
    """(condition, model, bot kind, seat, seeds) for every block the config asks for — or, with
    `only`, for the players named there ("condition", "condition:identity" or a bot kind)."""
    t = EXPERIMENT["tournament"]
    players = [(c, m, None) for c in t["conditions"] for m in MODELS] + [(k, None, k) for k in t.get("baselines", [])]
    players += [(k, None, k) for k in BOT_KINDS if k in only and k not in t.get("baselines", [])]
    if only:
        players = [(c, m, k) for c, m, k in players if c in only or (m and f"{c}:{m['identity']}" in only)]
    out = []
    for condition, model, kind in players:
        for seat in range(SLOT_COUNT):
            seeds = [g for g in range(1, games + 1) if (g - 1) % SLOT_COUNT == seat]
            if seeds:
                out.append((condition, model, kind, seat, seeds))
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--games", type=int, default=EXPERIMENT["tournament"]["games"], help="games per player")
    p.add_argument("--run-id", help="resume logs/suite_<run-id>/ (finished blocks are kept)")
    p.add_argument("--cpu", action="store_true", help="run llama.cpp on the CPU instead of the GPU")
    p.add_argument("--only", default="", help="only these players: condition, condition:identity or bot kind "
                                              "(any of BOT_KINDS, baseline or not)")
    p.add_argument("--opponents", choices=BOT_KINDS, default=opponents(),
                   help="the opponent bots' kind (default: the config's tournament.opponents)")
    args = p.parse_args()
    EXPERIMENT["tournament"]["opponents"] = args.opponents  # run.json records the config the run played

    os.chdir(REPO_ROOT)  # the players write their logs relative to the repo root
    todo = blocks(args.games, set(filter(None, args.only.split(","))))
    if any(model for _, model, _, _, _ in todo):
        backend = use_backend(args.cpu)
        check_adapters()
    else:
        backend = "none"  # bots only: no llama-server, no adapters
    run_dir = LOGS_DIR / f"suite_{args.run_id or f'{datetime.now():%Y%m%d_%H%M%S}'}"
    run_dir.mkdir(parents=True, exist_ok=True)
    check_resumable(run_dir)
    if (run_dir / "run.json").exists():
        played = json.loads((run_dir / "run.json").read_text())["experiment"]["tournament"].get("opponents")
        if played != args.opponents:
            raise SystemExit(f"{run_dir} was played against {played}: resume with --opponents {played}")
    info(f"{len(todo)} blocks, {args.games} games per player, against {opponents()} -> {run_dir}")
    for condition, model, kind, seat, seeds in todo:
        block = f"{condition}/seat{seat + 1}/{model['identity'] if model else kind}"
        if condition_finished(run_dir, block):
            info(f"{block}: already finished, kept")
            continue
        run_block(run_dir, condition, model, kind, seat, seeds)
        record_condition(run_dir, "tournament", block, backend)
    success(f"Done. Score it with: python3 eval/evaluate.py {run_dir.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
