#!/usr/bin/env bash
# Start Ollama (or llama.cpp) instances, then start deck + player servers.
# LLM config is read directly from each player config file.
# Run:  ./start_game.sh --players p1.json p2.json p3.json
# Stop: ./start_game.sh stop

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
PID_FILE="$SCRIPT_DIR/.game_pids"
LLM_CONFIG="$SCRIPT_DIR/config/llm-network.json"

# Parse flags
STOP=false
NO_INIT=false   # --no-init: leave the players uninitialised (tournament.py resets and inits per game)
PLAYER_CONFIGS=()
args=("$@")
i=0
while [[ $i -lt ${#args[@]} ]]; do
    arg="${args[$i]}"
    if [[ "$arg" == "stop" ]]; then
        STOP=true
    elif [[ "$arg" == "--no-init" ]]; then
        NO_INIT=true
    elif [[ "$arg" == "--players" ]]; then
        i=$(( i + 1 ))
        while [[ $i -lt ${#args[@]} && "${args[$i]}" != --* ]]; do
            PLAYER_CONFIGS+=("${args[$i]}")
            i=$(( i + 1 ))
        done
        continue
    fi
    i=$(( i + 1 ))
done

# Read llm.port and llm.type from a player config file
player_llm_port() { python3 -c "import json,sys; c=json.load(open(sys.argv[1])); print(c['llm']['port'])" "$1"; }
player_llm_type() { python3 -c "import json,sys; c=json.load(open(sys.argv[1])); print(c['llm'].get('type',''))" "$1"; }

# One pass: port, type, and the subset that actually needs an LLM (not human)
LLM_PORTS=()
LLM_TYPES=()
LLM_PLAYER_CONFIGS=()
# ${arr[@]+...}: macOS bash 3.2 calls an empty array unbound under set -u (`stop` passes no configs)
for cfg in ${PLAYER_CONFIGS[@]+"${PLAYER_CONFIGS[@]}"}; do
    t="$(player_llm_type "$cfg")"
    LLM_PORTS+=("$(player_llm_port "$cfg")")
    LLM_TYPES+=("$t")
    [[ "$t" != "human" && "$t" != bot_* ]] && LLM_PLAYER_CONFIGS+=("$cfg")
done

# ── Helpers ───────────────────────────────────────────────────────────────────

info()    { printf "\033[0;36m[start]\033[0m %s\n" "$*"; }
success() { printf "\033[0;32m[start]\033[0m %s\n" "$*"; }
warn()    { printf "\033[0;33m[start]\033[0m %s\n" "$*"; }

# ── Stop ──────────────────────────────────────────────────────────────────────

stop_all() {
    info "Stopping game processes..."
    if [[ -f "$PID_FILE" ]]; then
        while IFS= read -r pid; do
            if kill -0 "$pid" 2>/dev/null; then
                kill "$pid" && info "  killed PID $pid"
            fi
        done < "$PID_FILE"
        rm -f "$PID_FILE"
    else
        warn "No PID file found — game processes may not be running."
    fi

    info "Stopping LLM instances (Ollama or llama.cpp)..."
    if [[ ${#PLAYER_CONFIGS[@]} -gt 0 ]]; then
        python3 "$SCRIPT_DIR/game/llm/manager.py" --config "$LLM_CONFIG" \
            stop --players "${PLAYER_CONFIGS[@]}" 2>/dev/null || true
    else
        python3 "$SCRIPT_DIR/game/llm/manager.py" --config "$LLM_CONFIG" \
            stop 2>/dev/null || true
    fi

    success "Done."
    exit 0
}

if $STOP; then stop_all; fi

port_in_use() {
    python3 -c "
import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sys.exit(0 if s.connect_ex(('127.0.0.1', int(sys.argv[1]))) == 0 else 1)
" "$1"
}

ALL_PORTS=(8765 8766 8767 8768 "${LLM_PORTS[@]}")
BUSY_PORTS=()
for p in "${ALL_PORTS[@]}"; do
    port_in_use "$p" && BUSY_PORTS+=("$p")
done
if [[ ${#BUSY_PORTS[@]} -gt 0 ]]; then
    echo "" >&2
    printf "\033[0;31m[start]\033[0m Port(s) already in use: %s\n" "${BUSY_PORTS[*]}" >&2
    printf "\033[0;31m[start]\033[0m Refusing to start — a leftover process from a previous run may still be listening,\n" >&2
    printf "\033[0;31m[start]\033[0m and this script cannot tell a stale server apart from a fresh one once it's bound.\n" >&2
    printf "\033[0;31m[start]\033[0m Run '%s stop' first, or find and stop whatever is bound to these ports.\n" "$0" >&2
    exit 1
fi

# ── Start ─────────────────────────────────────────────────────────────────────

mkdir -p "$LOG_DIR"
> "$PID_FILE"

# 1. Start the LLM instances — config comes from player config files
echo ""
info "=== Step 1 / 3 — Starting LLM instances (Ollama or llama.cpp) ==="
if [[ ${#LLM_PLAYER_CONFIGS[@]} -gt 0 ]]; then
    # every config: the manager skips human and bot players itself and numbers instances by slot,
    # exactly as `stop` (which gets every config) does
    python3 "$SCRIPT_DIR/game/llm/manager.py" --config "$LLM_CONFIG" \
        start --players "${PLAYER_CONFIGS[@]}"
else
    info "No LLM players — skipping LLM startup."
fi
echo ""

# 2. Start deck server + player servers
info "=== Step 2 / 3 — Starting game servers ==="

info "Starting deck server on :8765 ..."
python3 -u "$SCRIPT_DIR/bohnanza.py" > "$LOG_DIR/deck.log" 2>&1 &
echo $! >> "$PID_FILE"

# Give the deck server a moment to bind
sleep 5

for i in 1 2 3; do
    PORT=$((8765 + i))
    info "Starting player $i on :${PORT} (llm → :${LLM_PORTS[$((i-1))]}) ..."
    python3 -u "$SCRIPT_DIR/player.py" "${PLAYER_CONFIGS[$((i-1))]}" --log-level info \
         > "$LOG_DIR/player${i}.log" 2>&1 &
    echo $! >> "$PID_FILE"
done

# Wait for all player servers to be ready, then call /init on each
info "Waiting for player servers to come up..."
for i in 1 2 3; do
    PORT=$((8765 + i))
    for attempt in $(seq 1 20); do
        if curl -sf "http://localhost:${PORT}/" >/dev/null 2>&1; then
            break
        fi
        sleep 1
    done
done

echo ""
if $NO_INIT; then
    info "=== Step 3 / 3 — skipped (--no-init): players start uninitialised ==="
else
    info "=== Step 3 / 3 — Initialising players (GET /init) ==="
    for i in 1 2 3; do
        PORT=$((8765 + i))
        info "  Initialising player ${i} (port ${PORT}) ..."
        curl -sf "http://localhost:${PORT}/init" >/dev/null \
            && success "  Player ${i} initialised." \
            || warn    "  Player ${i} /init failed — check logs."
    done
fi

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
success "All processes started."
echo ""
echo "  Deck server     →  http://localhost:8765"
PORTS=(8766 8767 8768)
for i in 0 1 2; do
    port="${PORTS[$i]}"
    if [[ "${LLM_TYPES[$i]}" == "human" ]]; then
        echo "  Player $((i+1)) (YOU)  →  http://localhost:${port}/human   ← open this!"
    else
        echo "  Player $((i+1))        →  http://localhost:${port}   (llm :${LLM_PORTS[$i]})"
    fi
done
echo ""
echo "  Logs:      $LOG_DIR/"
echo ""
echo "  To stop everything:  $0 stop"
echo ""
