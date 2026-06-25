"""Model registry + memory-ceiling accounting (BUILD-SPEC §5).

Agents are not models. This is the *model* lifecycle's reference data: the configured
lineup keyed by tier/name, plus the rule for what may be resident at once. The router
decides which tier to use; this code only describes and accounts for the weights.
"""

from __future__ import annotations

from dataclasses import dataclass

from config.loader import Config, ModelConfig, get_config


class MemoryCeilingError(RuntimeError):
    """Raised when a requested load would breach the two-slot / usable-RAM budget
    (Invariant 8). The scheduler refuses breaching work rather than crashing."""


@dataclass(frozen=True)
class Registry:
    config: Config

    def by_name(self, name: str) -> ModelConfig:
        for m in self.config.models:
            if m.name == name:
                return m
        raise KeyError(f"unknown model {name!r}")

    def by_tier(self, tier: str) -> ModelConfig:
        return self.config.model_for_tier(tier)

    @property
    def pinned(self) -> ModelConfig:
        return self.config.pinned_model


def get_registry() -> Registry:
    return Registry(get_config())
