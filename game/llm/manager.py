#!/usr/bin/env python3
"""Manage LLM server instances (ollama or llama.cpp) for a multi-player game."""

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path

# ── config ────────────────────────────────────────────────────────────────────
HOME    = Path.home()
TMP     = Path(os.environ.get("TMPDIR", "/tmp"))

LOG_DIR = TMP / "ollama-logs"
PID_DIR = TMP / "ollama-pids"

def _find_cfg_path() -> Path:
    # Early scan for --config / -c before argparse runs, so config is available at module load
    args = sys.argv[1:]
    for flag in ("--config", "-c"):
        if flag in args:
            i = args.index(flag)
            if i + 1 < len(args):
                return Path(args[i + 1])
    if Path("config/llm-network.json").exists():
        return Path("config/llm-network.json")
    if Path("llm-network.json").exists():
        return Path("llm-network.json")
    return HOME / ".llm-network.json"


def _find_player_paths() -> list[str]:
    """Early scan for --players before argparse runs."""
    args = sys.argv[1:]
    if "--players" not in args:
        return []
    i = args.index("--players")
    players = []
    j = i + 1
    while j < len(args) and not args[j].startswith("-"):
        players.append(args[j])
        j += 1
    return players


_cfg_path = _find_cfg_path()
_cfg: dict = json.loads(_cfg_path.read_text()) if _cfg_path.exists() else {}

OLLAMA_MODEL = _cfg.get("default_ollama_model", "llama3.2")   # model name for ollama pull/serve
DEFAULT_GGUF = _cfg.get("default_gguf", "")                   # fallback .gguf path for llama.cpp instances

# Up to 3 llama.cpp instances (one per player) run concurrently during a
# game, so each gets a quarter of the machine's cores rather than a fixed
# small number — a hardcoded "4" left a 40-core box running each instance at
# 12/40 cores total, which was slow enough that single-game tournament runs
# were consistently eating their whole 900s-per-game timeout on inference
# alone, not on any game-logic bug.
LLAMACPP_THREADS = max(4, (os.cpu_count() or 4) // 4)

# Set properly by check_deps() before any start command runs
DEFAULT_BACKEND  = "ollama"
LLAMA_SERVER_BIN = "llama-server"


@dataclass
class Instance:
    num: int
    port: int
    data_dir: Path
    backend: str = ""   # "ollama" | "llama.cpp" | "" (use DEFAULT_BACKEND)
    gguf: str = ""      # path to .gguf file (llama.cpp only)
    lora: str = ""
    chat_template_file: str = ""   # Jinja chat template to apply instead of the GGUF's own

    @property
    def resolved_backend(self) -> str:
        return self.backend or DEFAULT_BACKEND

    @property
    def pid_file(self) -> Path:
        return PID_DIR / f"instance-{self.num}.pid"

    @property
    def log_file(self) -> Path:
        return LOG_DIR / f"instance-{self.num}.log"

    def read_pid(self) -> int | None:
        if self.pid_file.exists():
            try:
                return int(self.pid_file.read_text().strip())
            except ValueError:
                pass
        return None

    def is_running(self, pid: int | None = None) -> bool:
        if pid is None:
            pid = self.read_pid()
        if pid is None:
            return False
        try:
            os.kill(pid, 0)
            return True
        except (ProcessLookupError, PermissionError):
            return False

    def prepare_start(self) -> bool:
        """Return False (and warn) if already running; clear stale pid otherwise."""
        pid = self.read_pid()
        if pid is not None:
            if self.is_running(pid):
                warn(f"Instance {self.num} already running (pid {pid}) on port {self.port} — skipping")
                return False
            self.pid_file.unlink(missing_ok=True)
        return True

    def resolve_model_file(self) -> str | None:
        candidates = [p for p in [
            Path(self.gguf) if self.gguf else None,
            Path(DEFAULT_GGUF) if DEFAULT_GGUF else None,
        ] if p]
        llamacpp_models = (
            HOME / "llama.cpp" / "models" if (HOME / "llama.cpp" / "models").is_dir()
            else HOME / "paksi" / "llama.cpp" / "models"
        )
        if llamacpp_models.is_dir():
            candidates += sorted(p for p in llamacpp_models.glob("*.gguf") if "vocab" not in p.name)
        for p in candidates:
            if p.exists():
                return str(p)
        return None

    def ollama_model_present(self) -> bool:
        manifest_root = self.data_dir / "models" / "manifests" / "registry.ollama.ai" / "library"
        return manifest_root.exists() and any(manifest_root.iterdir())


def _instances_from_players(paths: list[str]) -> list[Instance]:
    instances = []
    default_ports = [11434, 11435, 11436]
    for n, path in enumerate(paths, start=1):  # numbered by player slot, so start and stop agree
        raw = json.loads(Path(path).read_text())
        llm = raw.get("llm", raw)  # fall back to flat format
        llm_type = llm.get("type", "")
        if llm_type == "human" or llm_type.startswith("bot_"):
            continue  # needs no LLM server
        if llm_type == "llamacpp":
            backend = "llama.cpp"
        elif llm_type == "ollama":
            backend = "ollama"
        else:
            backend = llm.get("backend", "")
        instances.append(Instance(
            num=n,
            port=llm.get("port", default_ports[n - 1]),
            data_dir=HOME / f".ollama-instance-{n}",
            backend=backend,
            gguf=llm.get("gguf", ""),
            lora=llm.get("lora", ""),
            chat_template_file=llm.get("chat_template_file", ""),
        ))
    return instances


_player_paths = _find_player_paths()
if _player_paths:
    INSTANCES = _instances_from_players(_player_paths)
else:
    _inst_cfgs = {e["num"]: e for e in _cfg.get("instances", []) if "num" in e}
    INSTANCES = [
        Instance(
            num=n,
            port=_inst_cfgs.get(n, {}).get("port", base_port),
            data_dir=HOME / f".ollama-instance-{n}",
            backend=_inst_cfgs.get(n, {}).get("backend", ""),
            gguf=_inst_cfgs.get(n, {}).get("gguf", ""),
            lora=_inst_cfgs.get(n, {}).get("lora", ""),
            chat_template_file=_inst_cfgs.get(n, {}).get("chat_template_file", ""),
        )
        for n, base_port in [(1, 11434), (2, 11435), (3, 11436)]
    ]
# ──────────────────────────────────────────────────────────────────────────────

# ANSI colours
R = "\033[0;31m"
G = "\033[0;32m"
Y = "\033[0;33m"
C = "\033[0;36m"
B = "\033[1m"
X = "\033[0m"

def log(msg):  print(f"{C}[ollama]{X} {msg}", file=sys.stderr)
def ok(msg):   print(f"{G}[ollama]{X} {msg}", file=sys.stderr)
def warn(msg): print(f"{Y}[ollama]{X} {msg}", file=sys.stderr)
def err(msg):  print(f"{R}[ollama]{X} {msg}", file=sys.stderr)


def check_deps():
    """Detect available backends; set DEFAULT_BACKEND and LLAMA_SERVER_BIN."""
    global DEFAULT_BACKEND, LLAMA_SERVER_BIN

    ollama_ok = bool(shutil.which("ollama"))

    # LLAMA_SERVER_BIN picks the build (tournament.py / replay.py point it at
    # the CUDA build unless --cpu); otherwise the llama-server on PATH
    llama_server = os.environ.get("LLAMA_SERVER_BIN") or shutil.which("llama-server") or (
        str(HOME / "llama.cpp" / "llama-server")
        if (HOME / "llama.cpp" / "llama-server").exists() else None
    )

    if not ollama_ok and not llama_server:
        err("Neither ollama nor llama-server found.")
        err("  Install ollama from https://ollama.com")
        err("  OR llama.cpp from https://github.com/ggerganov/llama.cpp")
        sys.exit(1)

    if llama_server:
        LLAMA_SERVER_BIN = llama_server

    DEFAULT_BACKEND = "ollama" if ollama_ok else "llama.cpp"

    available = []
    if ollama_ok:
        available.append("ollama")
    if llama_server:
        available.append(f"llama.cpp ({llama_server})")
    log(f"Available backends: {', '.join(available)}  (default: {DEFAULT_BACKEND})")

    # Validate that every instance's requested backend is actually available
    for inst in INSTANCES:
        b = inst.backend
        if b == "ollama" and not ollama_ok:
            err(f"Instance {inst.num} requests ollama but ollama is not installed.")
            sys.exit(1)
        if b == "llama.cpp" and not llama_server:
            err(f"Instance {inst.num} requests llama.cpp but llama-server is not found.")
            sys.exit(1)
        if b and b not in ("ollama", "llama.cpp"):
            err(f"Instance {inst.num}: unknown backend '{b}' (use 'ollama' or 'llama.cpp')")
            sys.exit(1)


def wait_for_port(port: int, timeout: int = 20) -> bool:
    url = f"http://127.0.0.1:{port}/"
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(url, timeout=1)
            return True
        except Exception:
            time.sleep(1)
    return False


# ── commands ──────────────────────────────────────────────────────────────────

def cmd_start():
    check_deps()
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    PID_DIR.mkdir(parents=True, exist_ok=True)
    print()

    for inst in INSTANCES:
        if inst.resolved_backend == "ollama":
            _start_one_ollama(inst)
        else:
            _start_one_llamacpp(inst)

    # Pull model into ollama instances that need it
    ollama_instances = [i for i in INSTANCES if i.resolved_backend == "ollama"]
    if ollama_instances:
        print()
        log(f"Pulling {B}{OLLAMA_MODEL}{X} into ollama instances (skipped if already present)...")
        print()
        for inst in ollama_instances:
            if inst.ollama_model_present():
                log(f"Instance {inst.num}: model already present, skipping pull")
                continue
            log(f"Instance {inst.num}: pulling {OLLAMA_MODEL} ...")
            env = {
                **os.environ,
                "OLLAMA_HOST":   f"127.0.0.1:{inst.port}",
                "OLLAMA_MODELS": str(inst.data_dir / "models"),
            }
            result = subprocess.run(["ollama", "pull", OLLAMA_MODEL], env=env)
            if result.returncode == 0:
                ok(f"Instance {inst.num}: {OLLAMA_MODEL} ready")
            else:
                err(f"Instance {inst.num}: pull failed (exit {result.returncode})")

    print()
    ok("All instances running:")
    for inst in INSTANCES:
        print(f"    Instance {inst.num}  [{inst.resolved_backend}]  →  http://127.0.0.1:{inst.port}")
    print()
    print(f"  Logs:  {LOG_DIR}/")
    print(f"  Stop:  python3 {sys.argv[0]} stop")


def _spawn_and_wait(inst: Instance, cmd: list[str], env: dict | None = None):
    """Launch `cmd` as instance `inst`'s server process, persist its pid, and
    block until it's answering on its port (or report the failure)."""
    with open(inst.log_file, "a") as lf:
        proc = subprocess.Popen(cmd, env=env, stdout=lf, stderr=lf, start_new_session=True)

    inst.pid_file.write_text(str(proc.pid))

    if wait_for_port(inst.port):
        ok(f"Instance {inst.num} ready  →  http://127.0.0.1:{inst.port}  (pid {proc.pid})")
    else:
        err(f"Instance {inst.num} failed to start. Check: {inst.log_file}")


def _start_one_ollama(inst: Instance):
    if not inst.prepare_start():
        return

    inst.data_dir.mkdir(parents=True, exist_ok=True)

    env = {
        **os.environ,
        "OLLAMA_HOST":             f"127.0.0.1:{inst.port}",
        "OLLAMA_MODELS":           str(inst.data_dir / "models"),
        "OLLAMA_NUM_PARALLEL":     "1",
        "OLLAMA_MAX_LOADED_MODELS": "1",
        "OLLAMA_ORIGINS":          "*",
    }

    log(f"Starting instance {inst.num} (ollama) on port {inst.port} ...")
    _spawn_and_wait(inst, ["ollama", "serve"], env=env)

def _start_one_llamacpp(inst: Instance):
    model_file = inst.resolve_model_file()
    if not model_file:
        err(f"Instance {inst.num}: model file not found")
        err(f"  Add 'gguf' (global) or per-instance 'gguf' for instance {inst.num} in {_cfg_path}")
        sys.exit(1)

    if inst.lora and not Path(inst.lora).exists():
        err(f"Instance {inst.num}: LoRA adapter not found: {inst.lora}")
        sys.exit(1)

    if inst.chat_template_file and not Path(inst.chat_template_file).exists():
        err(f"Instance {inst.num}: chat template not found: {inst.chat_template_file}")
        sys.exit(1)

    if not inst.prepare_start():
        return

    inst.data_dir.mkdir(parents=True, exist_ok=True)

    label = Path(model_file).name
    if inst.lora:
        label += f" + {Path(inst.lora).name}"
    log(f"Starting instance {inst.num} (llama.cpp) on port {inst.port}  [{label}] ...")

    cmd = [
        LLAMA_SERVER_BIN,
        "-m", model_file,
        "--host", "127.0.0.1",
        "--port", str(inst.port),
        "--threads", str(LLAMACPP_THREADS),
        "--threads-batch", str(LLAMACPP_THREADS),
        "--ctx-size", "4096",
        "--parallel", "1",
        # apply the model's own chat template, matching how the adapter was
        # trained; without this /v1/chat/completions falls back to a generic
        # format and the prompt no longer looks like the training data
        "--jinja",
    ]
    if inst.chat_template_file:
        # The template the adapter was trained with (gemma-2b-it's GGUF ships none, and llama-server
        # would fall back to ChatML). A file, not --chat-template NAME: after --jinja that flag takes
        # template text, so a built-in name would itself become the prompt.
        cmd += ["--chat-template-file", inst.chat_template_file]
    if inst.lora:
        cmd += ["--lora", inst.lora]

    _spawn_and_wait(inst, cmd)


def cmd_stop():
    log("Stopping all instances...")
    stopped = 0
    for inst in INSTANCES:
        pid = inst.read_pid()
        if pid is None:
            warn(f"Instance {inst.num} — no pid file found")
            continue
        if inst.is_running(pid):
            os.kill(pid, signal.SIGTERM)
            ok(f"Stopped instance {inst.num} (pid {pid})")
            stopped += 1
        else:
            warn(f"Instance {inst.num} pid {pid} not running (stale pid file)")
        inst.pid_file.unlink(missing_ok=True)
    if stopped == 0:
        warn("No instances were running")


def cmd_status():
    print()
    print(f"  {'Instance':<12} {'Port':<10} {'PID':<12} Status")
    print(f"  {'-'*8:<12} {'-'*4:<10} {'-'*3:<12} {'------'}")
    for inst in INSTANCES:
        pid = inst.read_pid()
        if pid is None:
            status, pid_str = f"{Y}stopped{X}", "-"
        elif inst.is_running(pid):
            status, pid_str = f"{G}running{X}", str(pid)
        else:
            status, pid_str = f"{R}dead{X}", f"{pid} (stale)"
        print(f"  {str(inst.num):<12} {str(inst.port):<10} {pid_str:<12} {status}")
    print()


def cmd_ports():
    """Print the LLM port for each player slot (space-separated, one per player)."""
    print(" ".join(str(inst.port) for inst in INSTANCES))


def cmd_backends():
    """Print the llm_type string for each player slot (space-separated, one per player)."""
    check_deps()
    def _llm_type(inst: Instance) -> str:
        return "llamacpp" if inst.resolved_backend == "llama.cpp" else "ollama"
    print(" ".join(_llm_type(inst) for inst in INSTANCES))


def cmd_restart():
    cmd_stop()
    time.sleep(1)
    cmd_start()


def cmd_logs():
    files = [str(inst.log_file) for inst in INSTANCES if inst.log_file.exists()]
    if not files:
        warn(f"No log files found in {LOG_DIR}")
        sys.exit(1)
    try:
        subprocess.run(["tail", "-f", *files])
    except KeyboardInterrupt:
        pass


# ── entrypoint ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Manage 3 isolated Ollama or llama.cpp instances.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Global config file (JSON)  —  defaults/fallbacks only:\n"
            f"  default path: {_cfg_path}\n"
            '    {\n'
            '      "default_ollama_model": "llama3.2",\n'
            '      "default_gguf": "~/models/base.gguf"\n'
            '    }\n\n'
            "  default_ollama_model   model pulled/served by ollama instances\n"
            "  default_gguf           .gguf used when a player config leaves gguf blank\n\n"
            "Player config file (JSON)  —  per-player llm section:\n"
            '    { "llm": { "type": "llamacpp|ollama", "port": 11434,\n'
            '               "gguf": "", "lora": "" } }\n\n'
            "Examples:\n"
            f"  python3 {sys.argv[0]} start --players config/player{{1,2,3}}_config.json\n"
            f"  python3 {sys.argv[0]} --config my-config.json start --players p1.json p2.json p3.json\n"
            f"  python3 {sys.argv[0]} status\n"
            f"  python3 {sys.argv[0]} stop --players config/player{{1,2,3}}_config.json\n"
        ),
    )
    # --config/--players are declared here only so --help documents them and
    # argparse doesn't reject them as unrecognized — args.config/args.players
    # are never read. The values that actually take effect were already
    # resolved by _find_cfg_path()/_find_player_paths()'s own sys.argv scan
    # at module-import time (above), since INSTANCES and friends need a
    # config before any command function can be defined. Don't "fix" this by
    # wiring args.config/args.players through instead — that would parse the
    # config twice via two different mechanisms; edit the early-scan
    # functions if the parsing behavior needs to change.
    parser.add_argument(
        "--config", "-c",
        metavar="FILE",
        default=str(_cfg_path),
        help=f"Global config JSON file (default: {_cfg_path})",
    )
    parser.add_argument(
        "--players",
        nargs="+",
        metavar="FILE",
        help="Player config files in player order (overrides 'instances' in config)",
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="start",
        choices=["start", "stop", "status", "restart", "logs", "ports", "backends"],
        help=(
            "start    Start LLM instance(s) + pull model\n"
            "stop     Stop all running instances\n"
            "status   Show status of each instance\n"
            "restart  Stop then start\n"
            "logs     Tail logs from all instances\n"
            "ports    Print LLM port per player slot (for scripting)\n"
            "backends Print llm_type per player slot (for scripting)"
        ),
    )
    args = parser.parse_args()

    commands = {
        "start":    cmd_start,
        "stop":     cmd_stop,
        "status":   cmd_status,
        "restart":  cmd_restart,
        "logs":     cmd_logs,
        "ports":    cmd_ports,
        "backends": cmd_backends,
    }
    commands[args.command]()


if __name__ == "__main__":
    main()
