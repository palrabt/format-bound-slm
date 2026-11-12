"""Bohnanza deck server — port 8765."""

import datetime
import json
import threading
import time
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

from .cards import BEANS, card, make_deck, coins_for

# ── Shared state ──────────────────────────────────────────────────────────────

_lock       = threading.Lock()
_main       = make_deck()   # draw pile
_new: list[str] = []        # returned cards accumulate here
_init_count = 0             # how many /init calls have been made (max 3)
_players: list[str] = []    # registered player base URLs in turn order
_turn_idx   = 0             # index into _players of the current turn

# ── Request log ───────────────────────────────────────────────────────────────

_req_log: list[dict] = []
_req_log_lock = threading.Lock()
_req_log_seq  = 0
_NO_LOG_PATHS = {"/status", "/log"}


def _append_log(method: str, path: str, caller: str, status: int, summary: str) -> None:
    global _req_log_seq
    with _req_log_lock:
        _req_log_seq += 1
        _req_log.append({
            "seq":    _req_log_seq,
            "ts":     datetime.datetime.now().isoformat(timespec="seconds"),
            "method": method,
            "path":   path,
            "caller": caller,
            "status": status,
            "summary": summary[:300],
        })
        if len(_req_log) > 500:
            _req_log.pop(0)

# ── HTTP handler ──────────────────────────────────────────────────────────────


class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f"  {self.address_string()}  {fmt % args}")

    # ── helpers ───────────────────────────────────────────────────────────────

    def send_json(self, code: int, data: dict[str, Any]):
        self._resp_code    = code
        self._resp_summary = json.dumps(data)
        body = json.dumps(data, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length))

    # ── CORS pre-flight ───────────────────────────────────────────────────────

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # ── GET routes ────────────────────────────────────────────────────────────

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        self._query    = urllib.parse.parse_qs(parsed.query)
        self._resp_code    = 0
        self._resp_summary = ""
        routes = {"/deal2": self.deal2,
                  "/deal3": self.deal3,
                  "/status": self.handle_status,
                  "/init": self.handle_init,
                  "/endturn": self.handle_endturn,
                  "/log": self.handle_log}
        handler = routes.get(parsed.path)
        if handler:
            handler()
        else:
            self.send_json(404, {"error": "not found"})
        if parsed.path not in _NO_LOG_PATHS:
            _append_log("GET", parsed.path, self.client_address[0],
                        self._resp_code, self._resp_summary)

    # ── POST routes ───────────────────────────────────────────────────────────

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        self._resp_code    = 0
        self._resp_summary = ""
        routes = {"/return": self.handle_return,
                  "/reset": self.handle_reset}
        handler = routes.get(parsed.path)
        if handler:
            handler()
        else:
            self.send_json(404, {"error": "not found"})
        if parsed.path not in _NO_LOG_PATHS:
            _append_log("POST", parsed.path, self.client_address[0],
                        self._resp_code, self._resp_summary)

    # ── /init ─────────────────────────────────────────────────────────────────
    # 1st call → 3 cards, 2nd → 4 cards, 3rd → 5 cards. Max 3 calls per reset.
    # Optional query param: ?ip=http://10.0.0.2:8766  registers the player.

    def handle_init(self):
        global _init_count, _players
        ip = (self._query.get("ip") or [None])[0]
        print(f"[deck][init] request from {self.client_address[0]}, ip={ip}")
        with _lock:
            if _init_count >= 3:
                print(f"[deck][init] rejected — init limit reached")
                self.send_json(403, {"error": "init limit reached (3 players max) — POST /reset to start over"})
                return
            _init_count += 1
            n     = _init_count + 2          # 1→3, 2→4, 3→5
            n     = min(n, len(_main))
            cards: list[dict[str, Any]] = [card(_main.pop()) for _ in range(n)]
            size  = len(_main)
            if ip and ip not in _players:
                _players.append(ip)

        print(f"[deck][init] player={_init_count}, dealt={[c['name'] for c in cards]}, deck_size={size}, players={_players}")
        self.send_json(200, {
            "player":     _init_count,
            "cards":      cards,
            "deck_size":  size,
            "registered": ip,
            # No player starts on its own /init: the first one would play before the others are
            # registered, and the turn would come back to it alone (fast players such as bots did).
            "start": False,
        })
        if _init_count == 3 and _players:
            threading.Thread(target=self._start_game, daemon=True).start()

    @staticmethod
    def _start_game():
        """Once all three players are dealt in, give the first registered player its turn."""
        time.sleep(0.5)  # let the third player finish its own /init
        first = _players[0]
        print(f"[deck][init] all players in, starting {first}")
        try:
            urllib.request.urlopen(f"{first}/yourturn", timeout=5)
        except Exception as e:
            print(f"[deck][init] could not start {first}: {e}")

    # ── /deal ─────────────────────────────────────────────────────────────────

    def handle_deal(self, num_cards=2):
        global _main
        with _lock:
            n     = min(num_cards, len(_main))
            cards: list[dict[str, Any]] = [card(_main.pop()) for _ in range(n)]
            size  = len(_main)

        print(f"[deck][deal{num_cards}] dealt={[c['name'] for c in cards]}, deck_size={size}")
        self.send_json(200, {"cards": cards})

    def deal2(self):
        self.handle_deal(2)

    def deal3(self):
        self.handle_deal(3)

    # ── /return ───────────────────────────────────────────────────────────────
    # Body: {"cards": ["Coffee Bean", "Coffee Bean", "Blue Bean", ...]}

    def handle_return(self):
        global _new
        try:
            data  = self.read_json()
            cards = data["cards"]
            if not isinstance(cards, list):
                raise ValueError
        except Exception:
            self.send_json(400, {"error": 'expected {"cards": ["Bean Name", ...]}'})
            return

        print(f"[deck][return] from={self.client_address[0]}, cards={cards}")
        unknown = [c for c in cards if c not in BEANS]
        if unknown:
            print(f"[deck][return] rejected — unknown beans: {unknown}")
            self.send_json(400, {"error": f"unknown beans: {unknown}",
                                 "valid": list(BEANS.keys())})
            return

        counts: dict[str, int] = {}
        for c in cards:
            counts[c] = counts.get(c, 0) + 1

        total_coins = 0
        with _lock:
            for bean, count in counts.items():
                c = coins_for(bean, count)
                print(f"[deck][return]   {bean} x{count} → {c} coins")
                total_coins += c
                _new.extend([bean] * count)

        print(f"[deck][return] total_coins={total_coins}, new_deck_size={len(_new)}")
        self.send_json(200, {"coins": total_coins})

    # ── /status ───────────────────────────────────────────────────────────────

    def handle_status(self):
        with _lock:
            self.send_json(200, {
                "main_deck_size": len(_main),
                "new_deck_size":  len(_new),
                "total_in_play":  len(_main) + len(_new),
                "players":        list(_players),
            })

    # ── /log ──────────────────────────────────────────────────────────────────

    def handle_log(self):
        since = int((self._query.get("since") or ["0"])[0])
        with _req_log_lock:
            entries = [e for e in _req_log if e["seq"] > since]
            seq     = _req_log_seq
        self.send_json(200, {"entries": entries, "seq": seq})

    # ── /endturn ──────────────────────────────────────────────────────────────

    def handle_endturn(self):
        global _turn_idx
        print(f"[deck][endturn] request from {self.client_address[0]}")
        with _lock:
            if not _players:
                print(f"[deck][endturn] rejected — no players registered")
                self.send_json(400, {"error": "no players registered"})
                return
            if len(_main) == 0:
                print(f"[deck][endturn] game over — main deck exhausted")
                self.send_json(200, {"game_over": True, "message": "main deck exhausted — game over"})
                for ip in _players:
                    try:
                        urllib.request.urlopen(f"{ip}/yourturn?game_over=true", timeout=5)
                        print(f"[deck][endturn] notified {ip} of game over")
                    except Exception as e:
                        print(f"[deck][endturn] failed to notify {ip} of game over: {e}")
                return
            _turn_idx = (_turn_idx + 1) % len(_players)
            next_ip   = _players[_turn_idx]

        print(f"[deck][endturn] turn_idx={_turn_idx}, notifying {next_ip}")
        try:
            urllib.request.urlopen(f"{next_ip}/yourturn", timeout=100)
            print(f"[deck][endturn] {next_ip} acknowledged")
            self.send_json(200, {"next_player": next_ip})
        except Exception as e:
            print(f"[deck][endturn] failed to reach {next_ip}: {e}")
            self.send_json(502, {"error": f"could not reach {next_ip}, turn_idx {_turn_idx}: {e}"})

    # ── /reset ────────────────────────────────────────────────────────────────

    def handle_reset(self):
        """POST /reset, optionally {"seed": N}: the same seed deals the same game."""
        global _main, _new, _init_count, _players, _turn_idx, _req_log, _req_log_seq
        print(f"[deck][reset] request from {self.client_address[0]}")
        try:
            seed = (self.read_json() or {}).get("seed")
        except (ValueError, AttributeError):
            seed = None
        with _lock:
            _main       = make_deck(seed)
            _new        = []
            _init_count = 0
            _players    = []   # re-registered by /init, in order: the first one starts
            _turn_idx   = 0
            size        = len(_main)
        with _req_log_lock:
            _req_log     = []
            _req_log_seq = 0
        print(f"[deck][reset] deck shuffled, size={size}, seed={seed}")
        self.send_json(200, {"message": "deck reset", "deck_size": size, "seed": seed})


# ── Entry point ───────────────────────────────────────────────────────────────

def run(port: int = 8765):
    server = HTTPServer(("127.0.0.1", port), Handler)
    total  = sum(v["count"] for v in BEANS.values())
    print(f"Bohnanza server  →  http://127.0.0.1:{port}")
    print(f"  {total} cards across {len(BEANS)} bean types")
    print()
    print("  GET  /init              deal starting hand (3/4/5 cards, max 3 players)")
    print("  GET  /deal2             draw 2 cards")
    print("  GET  /deal3             draw 3 cards")
    print('  POST /return            {"cards":["Bean Name",...]}  →  coins earned')
    print("  GET  /status            deck sizes")
    print("  GET  /endturn           advance turn and call next player's /yourturn")
    print("  POST /reset             reshuffle a fresh deck ({\"seed\": N} for a fixed order)")
    print()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    run()
