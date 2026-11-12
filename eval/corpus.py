"""Reader for the prompt/response format shared by the players' logs and the training corpus.

Every file is a sequence of blank-line separated entries::

    {"phase": "REPLY", "hand": [...], ...}
    [JSON] {"accepted": false, "offer": [], "reason": "..."}

One Entry per message, whatever the response looks like: each metric decides for itself what it
can score, so all metrics count over the same answers.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

_MARKER = "[JSON]"


@dataclass
class Entry:
    """One prompt/response pair from a log or training file."""

    state: dict[str, Any]   # the state the player was asked about
    raw: str                # the answer as written, unparsed

    @property
    def phase(self) -> str:
        return self.state.get("phase", "")


def _strip_timestamp(line: str) -> str:
    """Drop an old-format 'YYYY-MM-DD HH:MM:SS % ' prefix, if present."""
    return line.split(" % ", 1)[1] if " % " in line else line


def read(path: Path | str) -> Iterator[Entry]:
    """Yield one Entry per message, malformed responses included."""
    text = Path(path).read_text(encoding="utf-8")
    for chunk in text.strip().split("\n\n"):
        lines = [l for l in chunk.strip().split("\n") if l.strip()]
        if len(lines) < 2 or not lines[1].startswith(_MARKER):
            continue
        try:
            state = json.loads(_strip_timestamp(lines[0]))
        except json.JSONDecodeError:
            continue
        if not isinstance(state, dict) or "phase" not in state:
            continue
        # The harness keeps multi-line answers intact (e.g. pretty-printed JSON), so the response
        # is everything after the marker, not just the marker's own line.
        raw = "\n".join([lines[1][len(_MARKER):]] + lines[2:]).strip()
        yield Entry(state, raw)


def state_key(state: dict[str, Any]) -> str:
    """The same state, written the same way — for matching an answer to its corpus item."""
    return json.dumps(state, sort_keys=True)
