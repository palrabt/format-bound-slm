#!/usr/bin/env python3
"""Rewrite the free-text fields of a synthetic corpus with a large LLM.

Usage:
    python3 -m training.generate_data.llm_text INPUT OUTPUT --server http://127.0.0.1:18600
        [--keep CURATED_FILE] [--cache CACHE.jsonl] [--workers 8] [--limit N]

The generator (synth.py) decides what every message says — accept or reject,
which cards, which bean is wanted — but words it with a few templates, and
adapters trained on it replay those templates verbatim. This keeps every
decision and has an LLM (served by llama-server, OpenAI-compatible API) say the
same thing in varied, table-talk wording.

Each line is checked before it is used: one short line, no markup; it names
only beans the message is about (or the speaker's own fields), names the ones
it must (e.g. the bean a rejection asks for), gives no card count that does not
match, and does not contradict the decision. A line that fails is resampled;
after --attempts failures the template text is kept and counted.

Rewritten fields:
  answers  TRADING ask, REPLY reason, CONSIDERING reason
  prompts  TRADING reason, REPLY asking_for, CONSIDERING my_reason / their_reason
The prompt fields are the other side of the same conversation (an ask, a
reply), so they get the same kinds of message, consistent with the state.
Entries found in --keep (hand-curated) are copied unchanged. Results are cached
by content, so a rerun only asks for what is missing.
"""

import argparse
import hashlib
import json
import random
import re
import threading
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from game.player.messages import VALID_CARDS

FIELDS = ("field1", "field2", "field3")
BEANS = sorted(VALID_CARDS)

# ── Bean mentions ──────────────────────────────────────────────────────────────

_WORD = {"black-eyed": "Black-eyed Bean", "blackeyed": "Black-eyed Bean", "black eyed": "Black-eyed Bean",
         "coffee": "Coffee Bean", "wax": "Wax Bean", "blue": "Blue Bean", "chili": "Chili Bean",
         "chilli": "Chili Bean", "chilis": "Chili Bean", "chilies": "Chili Bean", "chillies": "Chili Bean",
         "runner": "Runner Bean", "runners": "Runner Bean", "soy": "Soy Bean", "red": "Red Bean",
         "fire": "Fire Bean", "garden": "Garden Bean", "broad": "Broad Bean"}
_MENTION = re.compile(r"\b(" + "|".join(sorted(map(re.escape, _WORD), key=len, reverse=True)) + r")\b", re.I)
# "<word> bean(s)" where <word> is neither a bean type nor an ordinary modifier: "green beans", "stink bean".
_OK_MODIFIERS = {"a", "all", "any", "both", "cheap", "couple", "different", "extra", "few", "fewer", "five",
                 "four", "free", "fresh", "good", "great", "her", "his", "its", "less", "lone", "loose", "many",
                 "matching", "more", "my", "new", "nice", "no", "odd", "of", "old", "one", "other", "our", "own",
                 "right", "same", "single", "six", "some", "spare", "that", "the", "their", "these", "this",
                 "those", "three", "two", "useful", "what", "which", "your"}
_ANY_BEAN = re.compile(r"\b([a-z][a-z'-]*)\s+beans?\b", re.I)
_NUMBER = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "pair of": 2}
_COUNTED = re.compile(r"\b(\d+|one|two|three|four|five|six|pair of)\s+(?:(?:of\s+)?(?:my|your|the)\s+)?("
                      + "|".join(sorted(map(re.escape, _WORD), key=len, reverse=True)) + r")\b", re.I)


def mentions(text: str) -> set[str]:
    return {_WORD[m.group(1).lower()] for m in _MENTION.finditer(text)}


def full_mentions(text: str) -> list[str]:
    """Card names in a generator template, in order ("Wax Bean", ...)."""
    return re.findall("|".join(map(re.escape, sorted(BEANS, key=len, reverse=True))), text)


# ── Messages ───────────────────────────────────────────────────────────────────

def _cards(cards: list[str]) -> str:
    c = Counter(cards)
    parts = [f"{b} (x{n})" if n > 1 else b for b, n in c.items()]
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]


def _fields(fields: dict | None) -> str:
    if not fields:
        return ""
    grown = [f"{f['cards'][0]} ({len(f['cards'])})" for f in (fields[k] for k in FIELDS) if f["cards"]]
    return "Your own fields grow: " + (", ".join(grown) if grown else "nothing yet") + "."


ACCEPTING = {"accept_return", "accept_gift", "confirm"}
REJECTING = {"reject", "counter", "decline", "recounter"}


def task(msg: dict) -> str:
    k = msg["kind"]
    if k == "ask":
        return (f"You want to give {_cards(msg['offered'])} to another player and get {msg['want']} from them "
                f"in return. Make the offer.")
    if k in ("reject", "counter", "accept_return", "accept_gift"):
        offer = f"Another player offers to give you {_cards(msg['offered'])}. "
        return offer + {
            "reject": lambda: f"You refuse: you don't want them. Say you would rather get {msg['want']}.",
            "counter": lambda: (f"You refuse that offer, but propose something else: you would give them "
                                f"{_cards(msg['cards'])} if they give you {msg['want']}."),
            "accept_return": lambda: f"You accept and take them, and in exchange you give them {_cards(msg['cards'])}.",
            "accept_gift": lambda: "You accept and take them. You give nothing back.",
        }[k]()
    got = f"and would give you {_cards(msg['their'])} in return" if msg["their"] else "and would give you nothing back"
    agreed = f"You offered to give {_cards(msg['mine'])} to another player. They accepted your offer {got}. "
    return agreed + {
        "confirm": lambda: "You are happy with that: confirm, the trade goes ahead.",
        "decline": lambda: "But you changed your mind: you cancel the trade and keep your cards.",
        "recounter": lambda: (f"But you changed your mind: cancel this trade and propose giving them "
                              f"{_cards(msg['cards'])} instead."),
    }[k]()


def required(msg: dict) -> list[set[str]]:
    """Each set must be mentioned at least once."""
    k = msg["kind"]
    need = []
    if k in ("ask", "reject", "counter"):
        need.append({msg["want"]})
    if k in ("counter", "accept_return", "recounter"):
        need.append(set(msg["cards"]))
    return need


def allowed(msg: dict) -> set[str]:
    beans = set(msg.get("offered", [])) | set(msg.get("cards", [])) | set(msg.get("mine", [])) | set(msg.get("their", []))
    if msg.get("want"):
        beans.add(msg["want"])
    for f in (msg.get("fields") or {}).values():
        beans.update(f["cards"][:1])
    return beans


_ACCEPT_WORDS = re.compile(r"\b(deal!|(it'?s a deal|agreed|accepted|you('ve)? got (a|yourself a) deal|sold)\b)", re.I)
_REJECT_WORDS = re.compile(r"\b(no thanks|no,? thank you|i'?ll pass|pass on|decline|reject|not interested|"
                           r"no deal|call (it|the trade|this) off|cancel|changed? my mind|nope|sorry|oops|"
                           r"mistake)\b", re.I)
# A refusal has to say so somewhere: "no", "not", "pass", "rather", "instead", "n't", ...
_REFUSAL_CUE = re.compile(r"(\b(no|not|nah|nope|pass|sorry|rather|instead|decline|cancel|off|skip|"
                          r"keep|hold|changed?|except|unless|but)\b|n't\b|n’t\b)", re.I)


_BEAN_WORD = "|".join(sorted(map(re.escape, _WORD), key=len, reverse=True))
_POSSESSED = re.compile(r"\b(my|your)\s+((?:[\w'-]+\s+){0,2}?)(" + _BEAN_WORD + r")\b(?:\s+beans?)?(\s+fields?)?", re.I)
# "Here's your Fire" hands a card over: after these words "your" means the recipient.
_GIVING = re.compile(r"(here['’]?s|here (is|are)|there['’]?s|there you go|enjoy|send(ing)?|giv(e|ing)|hand(ing)?|"
                     r"pass(ing)?|(^|[.!?,;:]\s*)take)\b[^.!?]*$", re.I)


def sides(msg: dict) -> tuple[set[str], set[str]]:
    """Beans the speaker gives, and beans the other player gives, in this message."""
    k = msg["kind"]
    if k == "ask":
        return set(msg["offered"]), {msg["want"]}
    if k == "reject":
        return set(), set(msg["offered"]) | {msg["want"]}
    if k == "counter":
        return set(msg["cards"]), set(msg["offered"]) | {msg["want"]}
    if k in ("accept_return", "accept_gift"):
        return set(msg.get("cards", [])), set(msg["offered"])
    return set(msg["mine"]) | set(msg.get("cards", [])), set(msg["their"])  # confirm, decline, recounter


def wrong_direction(text: str, msg: dict) -> str | None:
    """A line that swaps who gives what: "your X" for a card the speaker gives
    (unless handing it over: "here's your X"), or "my X" for one the other
    player gives (unless it is the speaker's field). "A for B" is left alone —
    players use it both ways ("Coffee for soy, deal?" when accepting)."""
    give, get = sides(msg)
    only_give, only_get = give - get, get - give
    own_fields = {f["cards"][0] for f in (msg.get("fields") or {}).values() if f["cards"]}
    for m in _POSSESSED.finditer(text):
        owner, bean, is_field = m.group(1).lower(), _WORD[m.group(3).lower()], m.group(4)
        if owner == "your" and bean in only_give and not _GIVING.search(text[:m.start()]):
            return f"direction {m.group(0)!r}"
        if owner == "my" and bean in only_get and not is_field and bean not in own_fields:
            return f"direction {m.group(0)!r}"
    return None


def check(text: str, msg: dict) -> str | None:
    """Why `text` is not a valid line for `msg`, or None if it is."""
    if not text or "\n" in text:
        return "not one line"
    words = text.split()
    if len(words) > 30:
        return "too long"
    if (re.search(r'[{}\[\]"*#<>]|^\s*[-•]|^\W*(line|player|answer)\b\s*:', text, re.I)
            or any(ord(c) > 0x2FFF for c in text)):
        return "markup"
    for m in _ANY_BEAN.finditer(text):
        w = m.group(1).lower()
        if w not in _WORD and w not in _OK_MODIFIERS and w != "eyed" and not w.startswith(("black-eyed", "chil")):
            return f"unknown bean {m.group(0)!r}"
    named = mentions(text)
    if named - allowed(msg):
        return f"names {sorted(named - allowed(msg))}"
    for group in required(msg):
        if not named & group:
            return f"misses {sorted(group)}"
    counts = Counter(msg.get("offered", [])) | Counter(msg.get("cards", [])) | Counter(msg.get("mine", [])) | Counter(msg.get("their", []))
    field_counts = {f["cards"][0]: len(f["cards"]) for f in (msg.get("fields") or {}).values() if f["cards"]}
    for m in _COUNTED.finditer(text):
        n = int(m.group(1)) if m.group(1).isdigit() else _NUMBER[m.group(1).lower()]
        bean = _WORD[m.group(2).lower()]
        if bean != msg.get("want") and n not in (counts.get(bean, 0), field_counts.get(bean, 0)):
            return f"count {m.group(0)!r}"
    direction = wrong_direction(text, msg)
    if direction:
        return direction
    if msg["kind"] in ACCEPTING and _REJECT_WORDS.search(text):
        return "sounds like a rejection"
    if msg["kind"] in REJECTING and _ACCEPT_WORDS.search(text):
        return "sounds like an acceptance"
    # A counter-offer ("How about Runner for Chili?") refuses by proposing something
    # else; a plain refusal has to say no.
    if msg["kind"] in ("reject", "decline") and not _REFUSAL_CUE.search(text):
        return "does not refuse"
    if msg["kind"] == "accept_gift" and re.search(r"\b(in return|here'?s|give you|for you)\b", text, re.I):
        return "gives something back"
    return None


# ── Prompting ──────────────────────────────────────────────────────────────────

SYSTEM = """You write one line of table talk for a player in Bohnanza, the bean-trading card game. Players plant beans in fields, cash a field in for coins once it holds enough beans of one kind, and trade cards to grow their fields. Your line is sent to another player together with a trade decision, and must say what that decision says - nothing else.

Rules:
- One line: a short phrase or one to two short sentences. No quotation marks, no emojis, no lists.
- Name only the beans given in the task (or the ones in your fields). Short forms like "wax" or "Chilis" are fine.
- Do not state a number of cards unless it matches the cards listed in the task.
- Sound like a real player at the table: casual, brief, and different every time. Do not always start the same way.

Reply with the line only."""

TONES = ["friendly", "blunt", "playful", "businesslike", "polite", "casual", "enthusiastic", "hesitant",
         "dry", "haggling", "curt", "cheerful", "confident", "apologetic", "laid-back", "matter-of-fact"]
LENGTHS = [("very short: 2 to 6 words", 0.35), ("short: 6 to 12 words", 0.45),
           ("one or two short sentences, at most 20 words", 0.20)]


def load_style_examples(path: Path) -> dict[str, list[str]]:
    """Human-written lines from the annotated corpus, by message family."""
    ex: dict[str, set[str]] = {"ask": set(), "reply": set()}
    for chunk in path.read_text(encoding="utf-8").strip().split("\n\n"):
        lines = [l for l in chunk.split("\n") if l.strip()]
        if len(lines) < 2 or not lines[1].startswith("[JSON]"):
            continue
        try:
            state, resp = json.loads(lines[0].split(" % ")[-1]), json.loads(lines[1][6:])
        except json.JSONDecodeError:
            continue
        for fam, text in [("ask", state.get("asking_for")), ("ask", state.get("my_reason")),
                          ("ask", resp.get("ask") if isinstance(resp, dict) else None),
                          ("reply", state.get("their_reason")), ("reply", state.get("reason")),
                          ("reply", resp.get("reason") if isinstance(resp, dict) else None)]:
            if isinstance(text, str) and 1 < len(text.split()) <= 20:
                ex[fam].add(text.strip())
    return {k: sorted(v) for k, v in ex.items()}


def build_prompt(msg: dict, rng: random.Random, style: dict[str, list[str]]) -> str:
    fam = "ask" if msg["kind"] == "ask" else "reply"
    length = rng.choices([l for l, _ in LENGTHS], weights=[w for _, w in LENGTHS])[0]
    examples = "\n".join(f"- {e}" for e in rng.sample(style[fam], min(4, len(style[fam]))))
    facts = _fields(msg.get("fields"))
    return (f"Task: {task(msg)}\n" + (f"{facts}\n" if facts else "")
            + f"Tone: {rng.choice(TONES)}. Length: {length}.\n"
            f"How players talk (style only; their beans do not apply here):\n{examples}\n\nLine:")


def ask_llm(server: str, prompt: str, seed: int) -> str:
    body = {"messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
            "temperature": 1.0, "top_p": 0.95, "max_tokens": 60, "seed": seed, "cache_prompt": True}
    req = urllib.request.Request(f"{server}/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        text = json.loads(resp.read())["choices"][0]["message"]["content"]
    return text.strip().strip('"').strip("'").strip()


# ── Which messages an entry holds ──────────────────────────────────────────────

def _want(template_text: str, exclude: list[str], fallback: list[str], rng: random.Random) -> str:
    named = [b for b in full_mentions(template_text) if b not in exclude]
    if named:
        return named[-1]
    pool = [b for b in fallback if b not in exclude] or [b for b in BEANS if b not in exclude]
    return rng.choice(pool)


def _field_types(fields: dict) -> list[str]:
    return sorted({fields[f]["cards"][0] for f in FIELDS if fields[f]["cards"]})


def messages_of(state: dict, response, rng: random.Random) -> list[tuple[str, str, dict | None]]:
    """(where, key, message) for every free-text field of an entry; message None = leave empty."""
    ph, out = state["phase"], []
    if ph == "TRADING":
        if state["previous_offers"] and state["reason"]:
            prev, counter = state["previous_offers"], state["counter_offer"]
            want = _want(state["reason"], prev + counter, BEANS, rng)
            msg = ({"kind": "counter", "offered": prev, "cards": counter, "want": want} if counter
                   else {"kind": "reject", "offered": prev, "want": want})
            out.append(("state", "reason", msg))
        if response and response.get("ask"):
            offered = response["offered_cards"]
            want = _want(response["ask"], offered, _field_types(state["fields"]), rng)
            out.append(("response", "ask", {"kind": "ask", "offered": offered, "want": want, "fields": state["fields"]}))
    elif ph == "REPLY":
        offered = state["offered_cards"]
        if rng.random() < 0.03:  # in the game ~2% of offers come without a message
            out.append(("state", "asking_for", None))
        else:
            want = rng.choice([b for b in BEANS if b not in offered])
            out.append(("state", "asking_for", {"kind": "ask", "offered": offered, "want": want}))
        r, fields = response, state["fields"]
        if r["accepted"]:
            msg = ({"kind": "accept_return", "offered": offered, "cards": r["offer"]} if r["offer"]
                   else {"kind": "accept_gift", "offered": offered})
        else:
            want = _want(r["reason"], offered + r["offer"], _field_types(fields), rng)
            msg = ({"kind": "counter", "offered": offered, "cards": r["offer"], "want": want} if r["offer"]
                   else {"kind": "reject", "offered": offered, "want": want})
        out.append(("response", "reason", {**msg, "fields": fields}))
    elif ph == "CONSIDERING":
        mine, their = state["my_offers"], state["their_offers"]
        want = rng.choice([b for b in _field_types(state["my_fields"]) if b not in mine]
                          or [b for b in BEANS if b not in mine])
        out.append(("state", "my_reason", {"kind": "ask", "offered": mine, "want": want, "fields": state["my_fields"]}))
        their_msg = ({"kind": "accept_return", "offered": mine, "cards": their} if their
                     else {"kind": "accept_gift", "offered": mine})
        out.append(("state", "their_reason", {**their_msg, "fields": state["their_fields"]}))
        r = response
        kind = "confirm" if r["accepted"] else ("recounter" if r["offer"] else "decline")
        msg = {"kind": kind, "mine": mine, "their": their, "fields": state["my_fields"]}
        if kind == "recounter":
            msg["cards"] = r["offer"]
        out.append(("response", "reason", msg))
    return out


# ── Driver ─────────────────────────────────────────────────────────────────────

def _key(entry_text: str, where: str, field: str) -> str:
    return hashlib.sha1(f"{entry_text}|{where}.{field}".encode()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--server", default="http://127.0.0.1:18600")
    p.add_argument("--keep", type=Path, help="Corpus of hand-curated entries to copy unchanged")
    p.add_argument("--style", type=Path, default=Path("training/corpus/training_data.txt"),
                   help="Human-written corpus used for style examples")
    p.add_argument("--cache", type=Path, help="JSONL cache of generated lines (default: OUTPUT.cache.jsonl)")
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--attempts", type=int, default=5)
    p.add_argument("--limit", type=int, help="Only rewrite the first N messages (pilot run)")
    args = p.parse_args()

    style = load_style_examples(args.style)
    keep = set()
    if args.keep:
        keep = {c.strip() for c in args.keep.read_text(encoding="utf-8").strip().split("\n\n")}
    chunks = [c.strip() for c in args.input.read_text(encoding="utf-8").strip().split("\n\n")]

    cache_path = args.cache or args.output.with_suffix(".cache.jsonl")
    cache: dict[str, dict] = {}
    if cache_path.exists():
        for line in cache_path.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            cache[row["key"]] = row
    lock = threading.Lock()

    # Plan every message first so the pool can run them concurrently.
    entries, jobs, planned = [], [], set()
    for chunk in chunks:
        state_line, response_line = chunk.split("\n")
        state, response = json.loads(state_line), json.loads(response_line[len("[JSON] "):])
        slots = []
        if chunk not in keep:
            rng = random.Random(hashlib.sha1(chunk.encode()).hexdigest())
            for where, field, msg in messages_of(state, response, rng):
                key = _key(chunk, where, field)
                slots.append((where, field, msg, key))
                if msg is not None and key not in cache and key not in planned:
                    planned.add(key)  # a duplicate entry reuses the same line
                    jobs.append((key, msg, (state if where == "state" else response)[field]))
        entries.append((state, response, slots))
    if args.limit is not None:  # the corpus is ordered by phase; a pilot should see every kind
        jobs = random.Random(0).sample(jobs, min(args.limit, len(jobs)))
    print(f"{len(chunks)} entries, {sum(1 for c in chunks if c in keep)} kept as curated; "
          f"{len(jobs)} lines to generate ({len(cache)} cached)")

    stats = Counter()

    def run(job):
        key, msg, template_text = job
        rng = random.Random(key)
        reasons = []
        for attempt in range(args.attempts):
            try:
                text = ask_llm(args.server, build_prompt(msg, rng, style), seed=rng.randrange(2 ** 31))
            except Exception as e:  # one failed request must not end a long run
                reasons.append(f"error: {e}")
                continue
            problem = check(text, msg)
            if problem is None:
                row = {"key": key, "kind": msg["kind"], "text": text, "attempts": attempt + 1}
                if reasons:
                    row["problems"] = reasons
                break
            reasons.append(problem)
        else:
            row = {"key": key, "kind": msg["kind"], "text": template_text, "attempts": args.attempts,
                   "fallback": True, "problems": reasons}
        with lock:
            cache[key] = row
            with open(cache_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(row) + "\n")
            stats["fallback" if row.get("fallback") else "ok"] += 1
            done = stats["ok"] + stats["fallback"]
            if done % 250 == 0 or done == len(jobs):
                print(f"  {done}/{len(jobs)} lines, {stats['fallback']} kept template text", flush=True)

    with ThreadPoolExecutor(args.workers) as pool:
        list(pool.map(run, jobs))

    missing = 0
    with open(args.output, "w", encoding="utf-8") as out:
        for state, response, slots in entries:
            for where, field, msg, key in slots:
                target = state if where == "state" else response
                if msg is None:
                    target[field] = ""
                elif key in cache:
                    target[field] = cache[key]["text"]
                else:
                    missing += 1
            out.write(f"\n{json.dumps(state, separators=(', ', ': '))}\n"
                      f"[JSON] {json.dumps(response, separators=(', ', ': '))}\n")
    print(f"Written → {args.output}" + (f" ({missing} lines not generated yet kept their template text)" if missing else ""))


if __name__ == "__main__":
    main()
