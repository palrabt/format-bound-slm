#!/usr/bin/env python3
"""Run every condition of config/experiment.json against the replay corpus.

    python3 replay.py                  # on the GPU
    python3 replay.py --cpu            # llama.cpp's CPU build instead of the CUDA one
    python3 replay.py --run-id ID      # resume logs/replay_<ID>/ (finished conditions are kept)
    python3 replay.py --corpus FILE    # another corpus than the config's (e.g. a few items, as a smoke test)

The corpus (eval/replay_corpus.json) holds game states taken
from tournament logs and held-out states of the adapters' training generator, 100 per message type
each, with the peer addresses the prompts print. Per condition the three LLM servers are
started exactly as in the tournament (the same player configs: the condition's adapter and prompt
style, the same llama-server flags), and every player answers every item through the game's own
code — game/player/llm.py builds the prompt, calls its server, parses the answer and logs it — with
one attempt per item. No game is played; the states come from the corpus, so all conditions and
models answer the same questions and the results are directly comparable.

Output — the tournament's layout (tournament.py), read by eval/evaluate.py:
    logs/replay_<id>/run.json                   kind, the experiment config, backend per condition
      <condition>/configs/player{1,2,3}_config.json
      <condition>/<identity>/game_0001.log      the player's own log: one answer per item
Nothing is scored here: eval/evaluate.py scores a finished run.
"""

import argparse
import json
import multiprocessing
import os
import shutil
import socket
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import tournament as T
from eval import corpus

CORPUS = T.REPO_ROOT / T.EXPERIMENT["replay"]["corpus"]
MANAGER = [sys.executable, "game/llm/manager.py", "--config", "config/llm-network.json"]

# The player function that asks the LLM for each message type (game/player/llm.py).
ASK = {
    "PLANTING": "get_planting_action",
    "FORCED": "get_new_card_action",
    "TRADING": "get_trade_offer",
    "REPLY": "get_REPLY",
    "CONSIDERING": "get_considering_reply",
}


def _player_state(state: dict[str, Any], fields_key: str = "fields") -> dict[str, Any]:
    fields = state.get(fields_key, {})
    empty = {"cards": [], "value": 0}
    return {"hand": state.get("hand", []), "new_cards": state.get("new_cards", []),
            "field1": fields.get("field1", empty), "field2": fields.get("field2", empty),
            "field3": fields.get("field3", empty), "coins": state.get("coins", 0),
            "penalty": state.get("penalty", 0)}


def ask_arguments(state: dict[str, Any], peers: dict[str, str]) -> tuple:
    """The arguments the player's ASK function was called with in the game, recovered from the
    state object it logged (game/player/prompts/common.*_state_obj). States name the two peers
    "0"/"1"; the item's peer addresses map them back."""
    phase = state["phase"]
    ip = {"0": peers.get("player1_ip", ""), "1": peers.get("player2_ip", "")}
    if phase in ("PLANTING", "FORCED"):
        return (_player_state(state),)
    if phase == "TRADING":
        other = {ip[k]: v for k, v in state.get("other_players", {}).items()}
        return (_player_state(state), other, state.get("previous_offers", []),
                state.get("counter_offer", []), state.get("reason", ""))
    if phase == "REPLY":
        return (_player_state(state), state.get("offered_cards", []),
                ip.get(state.get("from_player", ""), ""), state.get("asking_for", ""))
    if phase == "CONSIDERING":
        return (_player_state(state, "my_fields"), state.get("my_offers", []), state.get("my_reason", ""),
                state.get("their_offers", []), state.get("their_reason", ""),
                state.get("their_fields", {}), ip.get(state.get("from_player", ""), ""))
    raise ValueError(f"unknown phase {phase!r}")


def answer_items(config_path: str, items: list[dict]) -> None:
    """One player, in its own process: answer every item as the player would in a game."""
    from game.player import llm, state
    from game.player.server import load_config
    state.LOG_LEVEL = "err"
    state.CONFIG.clear()
    state.CONFIG.update(load_config(config_path))
    state.CONFIG["llm_max_retries"] = 1  # one answer per item
    state.game_index = 1                 # everything goes to <identity>/game_0001.log
    for item in items:
        state.CONFIG.update(item["peers"])  # the addresses the prompt showed in the game
        getattr(llm, ASK[item["state"]["phase"]])(*ask_arguments(item["state"], item["peers"]))


def check_log(log: Path, items: list[dict]) -> None:
    """Every item answered once, in order, with the state it was asked about."""
    expected = [item["state"] for item in items]
    # The log's own reader: a state line opens each entry, so an answer that echoes a state (base
    # models given the bare state, as in compact) is not mistaken for one.
    logged = [entry.state for entry in corpus.read(log)] if log.exists() else []
    if logged != expected:
        first = next((i for i, (a, b) in enumerate(zip(logged, expected)) if a != b), min(len(logged), len(expected)))
        T.warn(f"{log}: {len(logged)} of {len(expected)} items logged as asked (first difference at item {first})")


def run_condition(run_dir: Path, condition: str, items: list[dict]) -> None:
    cond_dir = run_dir / condition
    shutil.rmtree(cond_dir, ignore_errors=True)  # whatever an interrupted attempt left behind
    configs = T.write_condition_configs(cond_dir / "configs", condition, scenario=f"{run_dir.name}/{condition}")
    T.info(f"=== {condition}: {len(items)} items x {len(configs)} players ===")
    subprocess.run(MANAGER + ["start", "--players", *map(str, configs)], cwd=T.REPO_ROOT, check=True)
    try:
        T.wait_for_llms(configs)
        players = [multiprocessing.Process(target=answer_items, args=(str(c), items)) for c in configs]
        for p in players:
            p.start()
        for p in players:
            p.join()
    finally:
        subprocess.run(MANAGER + ["stop", "--players", *map(str, configs)], cwd=T.REPO_ROOT, check=False)
    for identity in T.IDENTITIES:
        check_log(cond_dir / identity / "game_0001.log", items)
    T.success(f"{condition} done -> {cond_dir}")


def ports_free() -> bool:
    ports = [11433 + slot for slot in range(1, T.SLOT_COUNT + 1)]
    for port in ports:
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", port)) == 0:
                T.warn(f"port {port} is in use — is a game or another replay running? (./start_game.sh stop)")
                return False
    return True


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--run-id", help="resume logs/replay_<run-id>/ (finished conditions are kept)")
    p.add_argument("--cpu", action="store_true", help="run llama.cpp on the CPU instead of the GPU")
    p.add_argument("--corpus", type=Path, default=CORPUS, help="replay corpus (default: the config's)")
    args = p.parse_args()

    os.chdir(T.REPO_ROOT)  # the players write their logs relative to the repo root
    backend = T.use_backend(args.cpu)
    T.check_adapters()
    if not ports_free():
        sys.exit(1)
    items = json.loads(args.corpus.read_text())
    run_dir = T.LOGS_DIR / f"replay_{args.run_id or f'{datetime.now():%Y%m%d_%H%M%S}'}"
    run_dir.mkdir(parents=True, exist_ok=True)
    T.check_resumable(run_dir)
    T.info(f"{len(T.CONDITIONS)} conditions x {len(items)} items on the {backend} -> {run_dir}")

    for condition in T.CONDITIONS:
        if T.condition_finished(run_dir, condition):
            T.info(f"{condition}: already finished, kept")
            continue
        run_condition(run_dir, condition, items)
        T.record_condition(run_dir, "replay", condition, backend)
    T.success(f"Done. Score it with: python3 eval/evaluate.py {run_dir.relative_to(T.REPO_ROOT)}")


if __name__ == "__main__":
    main()
