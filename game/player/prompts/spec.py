"""Uniform return type for every build_* prompt function in every strategy module."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PromptSpec:
    """text          — the full user-turn prompt string.
    system_prompt — optional system-turn content; "" means no system turn is
                    added.
    grammar       — optional GBNF grammar string; None means the "grammar"
                    key is omitted from the llamacpp request body.
    """
    text: str
    system_prompt: str = ""
    grammar: str | None = None
