"""HTTP helpers for the player."""

import json
import urllib.request
from typing import Any


def http_get(url: str) -> dict[str, Any]:
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.loads(resp.read())


def http_post(url: str, body: dict[str, Any], timeout: int = 10) -> dict[str, Any]:
    data = json.dumps(body).encode()
    req  = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())
