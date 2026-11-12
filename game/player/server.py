"""Bohnanza player HTTP server."""

import json
import os
import sys
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from collections import Counter

from . import state as lib
from . import actions as actions
from .state import decision_module as _dm
from .messages import DealResponse, OfferRequest, TradeRequest, TradeResponse, OfferReply

# ── Config ─────────────────────────────────────────────────────────────────────


def load_config(path: str) -> dict[str, Any]:
    with open(path) as f:
        raw = json.load(f)
    # Structured format: player / connectivity / llm sections
    if any(k in raw for k in ("player", "connectivity", "llm")):
        cfg: dict[str, Any] = {}
        cfg.update(raw.get("player", {}))
        cfg.update(raw.get("connectivity", {}))
        llm = raw.get("llm", {})
        cfg.setdefault("llm_type", llm.get("type", ""))
        cfg["llm_section"] = llm
    else:
        cfg = raw
    required = ("player1_ip", "player2_ip", "llm_ip", "deck_ip", "identity")
    for key in required:
        if key not in cfg:
            lib.debug(f"config missing required field '{key}'", "err")
            sys.exit(1)
    return cfg

# ── HTTP handler ───────────────────────────────────────────────────────────────


class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        if getattr(self, "path", None) in ("/llm_log", "/state"):
            return
        lib.debug(f"{self.address_string()}  {fmt % args}")

    def send_body(self, code: int, body: bytes, content_type: str, extra_headers: dict[str, str] | None = None):
        self.send_response(code)
        self.send_header("Content-Type",   content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        for name, value in (extra_headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        try:
            self.wfile.write(body)
        except BrokenPipeError:
            pass

    def send_json(self, code: int, data: dict[str, Any]):
        self.send_body(code, json.dumps(data, indent=2).encode(), "application/json")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        routes = {
            "/state":    self.handle_state,
            "/init":     self.handle_init,
            "/yourturn": self.handle_yourturn,
            "/llm_log":  self.handle_llm_log,
            "/pending":  self.handle_pending,
            "/human":    self.handle_human_ui,
        }
        handler = routes.get(urllib.parse.urlparse(self.path).path)
        if handler:
            handler()
        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):
        routes = {
            "/offer":  self.handle_offer,
            "/trade":  self.handle_trade,
            "/submit": self.handle_submit,
        }
        handler = routes.get(urllib.parse.urlparse(self.path).path)
        if handler:
            handler()
        else:
            self.send_json(404, {"error": "not found"})

    def read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length))

    # ── GET /state ─────────────────────────────────────────────────────────────

    def handle_state(self):
        with lib.lock:
            self.send_json(200, lib.state.to_dict())

    # ── GET /llm_log ───────────────────────────────────────────────────────────

    def handle_llm_log(self):
        path = _dm().llm_log_path()
        if not os.path.exists(path):
            self.send_json(404, {"error": "no llm log yet"})
            return
        filename = os.path.basename(path)
        with open(path, "rb") as f:
            body = f.read()
        self.send_body(200, body, "text/plain; charset=utf-8",
                        {"Content-Disposition": f'attachment; filename="{filename}"'})

    # ── GET /init ──────────────────────────────────────────────────────────────
    # Draws a starting hand and plants the first card onto field1.

    def handle_init(self):
        lib.debug("GET /init")
        from .http import http_get
        self_ip = urllib.parse.quote(lib.CONFIG.get("self_ip", ""), safe="")
        url     = f"{lib.CONFIG['deck_ip']}/init" + (f"?ip={self_ip}" if self_ip else "")
        try:
            result = http_get(url)
        except Exception as e:
            self.send_json(502, {"error": f"deck server unreachable: {e}"})
            return

        init = DealResponse.from_dict(result)
        # /init?game=N numbers this game N (a tournament passes its deck seed); otherwise the next number
        game = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get("game", [""])[0]
        with lib.lock:
            lib.game_index = int(game) if game.isdigit() else lib.game_index + 1
            lib.state.hand           = init.cards
            lib.state.new_cards      = []
            lib.state.field1.cards   = []
            lib.state.field2.cards   = []
            lib.state.field3.cards   = []
            lib.state.coins          = 0
            lib.state.identity       = lib.CONFIG.get("identity", "")
            snapshot = lib.state.to_dict()

        self.send_json(200, {
            "message":      "initialized",
            "state":        snapshot,
        })

        if init.start:
            threading.Thread(target=actions.start_new_turn, daemon=True).start()

    # ── GET /yourturn ──────────────────────────────────────────────────────────

    def handle_yourturn(self):
        lib.debug("GET /yourturn")
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "game_over" in params:
            lib.err(f"Game over received\nPenalties: {lib.state.penalty}\nCoins: {lib.state.coins}")
            self.send_json(200, {"message": "game over acknowledged, cashing out the fields"})
            # after answering: the deck is still inside /endturn and serves one request at a time
            threading.Thread(target=actions.cash_out, daemon=True).start()
            return
        self.send_json(200, {"message": "starting turn"})
        threading.Thread(target=actions.start_new_turn, daemon=True).start()

    # ── POST /offer ────────────────────────────────────────────────────────────

    def handle_offer(self):
        lib.debug("received POST /offer")
        try:
            req = OfferRequest.from_dict(self.read_json())
            if not req.cards:
                raise ValueError
        except Exception:
            lib.debug("bad request — could not parse body")
            self.send_json(400, {"error": 'expected {"cards":[...],"from":"...","ask":"..."}'})
            return

        lib.debug(f"from={req.from_ip!r}  cards={req.cards}")

        with lib.lock:
            snapshot = lib.state.to_dict()

        retries = 0
        reply: OfferReply = OfferReply()
        while retries < lib.NBR_OF_RETRIES:
            lib.debug(f"hand before decision: {snapshot.get('hand')}")
            reply = _dm().get_REPLY(snapshot, req.cards, req.from_ip, req.ask)
            lib.debug(f"response: offer={reply.offer}, reason={reply.reason!r}")

            if Counter(reply.offer) <= Counter(lib.state.hand):
                break
            else:
                lib.warn(f"Invalid offer response: {reply.offer}, retry {retries + 1}")
                retries += 1
                continue

        if not (Counter(reply.offer) <= Counter(lib.state.hand)):
            lib.err("No valid offer reply after retries, sending empty reply")
            lib.state.penalty += 1
            reply = OfferReply()

        self.send_json(200, reply.to_dict())
        lib.debug(f"response sent")

    # ── POST /trade ────────────────────────────────────────────────────────────

    def handle_trade(self):
        lib.debug("POST /trade")
        try:
            req = TradeRequest.from_dict(self.read_json())
            lib.debug(f"sending={req.sending}  getting={req.getting}")
        except Exception as e:
            lib.err(f"bad request — could not parse body :: {e}")
            self.send_json(400, {"error": 'expected {"getting":[...],"sending":[...]}'})
            return

        with lib.lock:
            missing = [c for c in req.sending if c not in lib.state.hand]
            if missing:
                resp = TradeResponse(success=True, error=f"cards not in hand: {missing}")
                lib.err(f"In hand: {lib.state.hand},  Missing {missing}")
            else:
                for card in req.sending:
                    lib.state.hand.remove(card)
                lib.state.new_cards.extend(req.getting)
                snapshot = lib.state.to_dict()
                resp = TradeResponse(success=True, sending=req.sending, getting=req.getting, state=snapshot)

        self.send_json(200 if resp.success else 400, resp.to_dict())

        lib.debug("Execute forced planting")
        actions.forced_planting()

    # ── GET /pending ───────────────────────────────────────────────────────────
    # Returns the current pending human decision, or {"pending": false}.

    def handle_pending(self):
        if lib.CONFIG.get("llm_type") != "human":
            self.send_json(404, {"error": "not a human player"})
            return
        from . import human as h
        pending = h.get_pending()
        if pending is None:
            self.send_json(200, {"pending": False})
        else:
            self.send_json(200, {"pending": True, **pending})

    # ── POST /submit ───────────────────────────────────────────────────────────
    # Body: the human's decision dict (shape depends on decision type).

    def handle_submit(self):
        if lib.CONFIG.get("llm_type") != "human":
            self.send_json(404, {"error": "not a human player"})
            return
        from . import human as h
        try:
            data = self.read_json()
        except Exception:
            self.send_json(400, {"error": "invalid JSON body"})
            return
        ok = h.submit_response(data)
        if ok:
            self.send_json(200, {"ok": True})
        else:
            self.send_json(409, {"error": "no decision pending"})

    # ── GET /human ─────────────────────────────────────────────────────────────
    # Serves the human-player web UI HTML file.

    def handle_human_ui(self):
        import pathlib
        html_path = pathlib.Path(__file__).parent.parent.parent / "training" / "generate_data" / "human_player.html"
        if not html_path.exists():
            self.send_json(404, {"error": "human_player.html not found"})
            return
        self.send_body(200, html_path.read_bytes(), "text/html; charset=utf-8")


# ── Entry point ────────────────────────────────────────────────────────────────

def run(config_path: str, log_level: str = "info"):
    lib.LOG_LEVEL = log_level
    lib.CONFIG = load_config(config_path)
    port = int(lib.CONFIG.get("port", 8766))

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Player server  →  http://127.0.0.1:{port}")
    print(f"  deck_ip        : {lib.CONFIG['deck_ip']}")
    print(f"  llm_ip         : {lib.CONFIG['llm_ip']}")
    print(f"  player1        : {lib.CONFIG['player1_ip']}")
    print(f"  player2        : {lib.CONFIG['player2_ip']}")
    print()
    print("  GET  /state      current player state")
    print("  GET  /init       draw starting hand, auto-plant first card")
    print("  GET  /yourturn   run this player's turn (LLM-driven)")
    print("  GET  /llm_log    log of all LLM prompts and responses")
    print('  POST /offer      {"card":[...],"from":"..."} — LLM decides to accept')
    print('  POST /trade      {"buyer":[...],"seller":[...]} — execute a trade')
    print()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
