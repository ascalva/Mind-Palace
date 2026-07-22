"""The hard feature-flag boundary for the dream-phase R&D track (design-notes/
dream-phase-rnd-charter.md).

The interpreter panel (R0) and the evidence-based adjudicator (R1) are RESEARCH, behind a flag
that is **OFF by default**. They are deliberately NOT wired into the live dream path —
`scheduler/cron.py` runs the Phase-7 `Dreamer`, never this. As a second line of defense, every
R&D entry point calls `require_rnd_enabled(config)` and raises if the flag is off, so even a
direct import-and-call cannot run the R&D engine in a normal session. To exercise it you must
explicitly construct a config with `[dream_rnd] enabled = true` — a conscious R&D act.

This keeps the riskiest layer (the one place the system reasons over its own outputs, once R3
lands) gated by construction, not by remembering to be careful.
"""

from __future__ import annotations

from core.kernel.config import Config, DreamRnDConfig, get_config


class DreamRnDDisabledError(RuntimeError):
    """An R&D dream entry point was called while the feature flag is OFF (the default).

    This is the boundary: the interpreter panel / adjudicator never run unless
    `[dream_rnd] enabled = true` is set deliberately. Not reachable from the live path."""


def rnd_config(config: Config | None = None) -> DreamRnDConfig:
    return (config or get_config()).dream_rnd


def require_rnd_enabled(config: Config | None = None) -> DreamRnDConfig:
    """Fail closed unless the R&D flag is explicitly on. Called by every R0/R1 entry point."""
    cfg = rnd_config(config)
    if not cfg.enabled:
        raise DreamRnDDisabledError(
            "dream-phase R&D (interpreter panel / adjudicator) is flag-OFF; set "
            "[dream_rnd] enabled = true to run it deliberately (it is never wired into the "
            "live dream path — see design-notes/dream-phase-rnd-charter.md)"
        )
    return cfg
