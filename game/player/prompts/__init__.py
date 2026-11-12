"""Interchangeable prompt strategies for LLM players.

select_strategy() replaces the old boolean _use_trained_prompt() with a
dispatch over these modules, each implementing the same 5 build_*
functions (one per phase) and returning a PromptSpec.
"""

from types import ModuleType

from .. import state as _state
from . import compact, grammar, verbose, verbose2
from .spec import PromptSpec

STRATEGIES: dict[str, ModuleType] = {
    "compact": compact,
    "verbose": verbose,
    "grammar": grammar,
    "verbose2": verbose2,
}

# Earlier names still accepted in configs: "compact" used to be "trained".
ALIASES: dict[str, str] = {"trained": "compact"}

_REQUIRED_FUNCTIONS = (
    "build_planting_prompt",
    "build_forced_prompt",
    "build_offer_prompt",
    "build_reply_prompt",
    "build_considering_prompt",
)

for _name, _module in STRATEGIES.items():
    for _fn in _REQUIRED_FUNCTIONS:
        assert hasattr(_module, _fn), f"prompts.{_name} is missing {_fn}()"


def select_strategy() -> ModuleType:
    """Replacement for the old llm.py:_use_trained_prompt().

    Configurable via llm.prompt_style in the player config:
      "compact"  → always use the compact prompt: the state as one JSON line,
                   the format the LoRA corpus trains on ("trained" also works)
      "verbose"  → always use the redesigned strategy-guide prompt
      "grammar"  → always use grammar-constrained decoding
      "verbose2" → always use the original (pre-redesign) strategy-guide
                   prompt, kept for A/B comparison against "verbose"
      (absent)   → auto-detect: compact iff llm.lora is set, else verbose.
                   "grammar"/"verbose2" are never auto-selected — they're
                   opt-in only, since there's no prior behavior to preserve
                   for "grammar", and "verbose2" exists specifically to be
                   pinned deliberately for comparison, not fallen into.
    """
    llm_section = _state.CONFIG.get("llm_section", {})
    style = ALIASES.get(llm_section.get("prompt_style", ""), llm_section.get("prompt_style", ""))
    if style in STRATEGIES:
        return STRATEGIES[style]
    if style:
        _state.warn(f"Unknown llm.prompt_style {style!r} — falling back to auto-detect")
    return compact if llm_section.get("lora", "") else verbose


__all__ = ["ALIASES", "PromptSpec", "STRATEGIES", "select_strategy"]
