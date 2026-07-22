"""Two-slot model loader (BUILD-SPEC §5).

The model lifecycle's executor: it loads, swaps, and evicts weights while enforcing the
hardware ceiling (Invariant 8). The router *decides* tier/window; this code *does* the
load — model advises, code acts.

Two slots, never more:
  * Slot 1 — the pinned tiny model (router + watchdog), kept warm indefinitely.
  * Slot 2 — a single swappable worker. Loading a worker evicts the prior worker.
A stretch model that declares `evicts_pinned` also evicts the pinned model and runs as
the sole resident for its duration (the documented §5 tradeoff).

The ceiling is checked BEFORE any Ollama call, so breaching work is refused, not
half-applied. The `warm` flag lets the eviction/accounting logic be unit-tested
without a live server.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from core.kernel.config import Config, ModelConfig
from core.models.ollama_client import OllamaClient
from core.models.registry import MemoryCeilingError, Registry


@dataclass
class TwoSlotLoader:
    config: Config
    client: OllamaClient
    registry: Registry
    _resident: dict[str, ModelConfig] = field(default_factory=dict)
    last_load_seconds: float = 0.0

    # --- inspection --------------------------------------------------------------
    def resident_models(self) -> list[str]:
        return list(self._resident)

    def resident_gb(self) -> float:
        return sum(m.resident_gb for m in self._resident.values())

    # --- accounting (pure-ish, no Ollama calls) ----------------------------------
    def _prospective(self, candidate: ModelConfig) -> dict[str, ModelConfig]:
        """The resident set after loading `candidate`, applying the two-slot rules."""
        pinned_name = self.registry.pinned.name
        new = dict(self._resident)
        if candidate.evicts_pinned:
            new.pop(pinned_name, None)
        if not candidate.pinned:
            # Slot 2 holds exactly one worker: drop any existing non-pinned model.
            for name in [n for n in new if n != pinned_name]:
                del new[name]
        new[candidate.name] = candidate
        return new

    def _check_ceiling(self, prospective: dict[str, ModelConfig]) -> None:
        budget = self.config.resources.usable_ram_gb
        max_n = self.config.resources.max_resident_models
        if len(prospective) > max_n:
            raise MemoryCeilingError(
                f"would hold {len(prospective)} models > max {max_n}: {list(prospective)}"
            )
        total = sum(m.resident_gb for m in prospective.values())
        if total > budget:
            raise MemoryCeilingError(
                f"would use {total:.1f} GB > usable budget {budget:.1f} GB "
                f"({', '.join(prospective)})"
            )

    # --- load / swap -------------------------------------------------------------
    def ensure(self, name: str, *, warm: bool = True) -> ModelConfig:
        """Make `name` resident, swapping/evicting as the two-slot rules require.
        Refuses (raises MemoryCeilingError) before touching Ollama if it would breach
        the ceiling."""
        candidate = self.registry.by_name(name)
        if name in self._resident:
            return candidate

        prospective = self._prospective(candidate)
        self._check_ceiling(prospective)  # refuse breaching work up front

        for gone in [n for n in self._resident if n not in prospective]:
            if warm:
                self.client.unload(gone)
            del self._resident[gone]

        keep_alive: str | int = -1 if candidate.pinned else self.config.ollama.default_keep_alive
        t0 = time.monotonic()
        if warm:
            self.client.load(candidate.name, num_ctx=candidate.num_ctx, keep_alive=keep_alive)
        self.last_load_seconds = time.monotonic() - t0
        self._resident[name] = candidate
        return candidate

    def ensure_tier(self, tier: str, *, warm: bool = True) -> ModelConfig:
        return self.ensure(self.registry.by_tier(tier).name, warm=warm)

    def ensure_pinned(self, *, warm: bool = True) -> ModelConfig:
        return self.ensure(self.registry.pinned.name, warm=warm)
