"""A trivial agent that inherits the Constitution (Phase 0 inheritance stub).

Every agent — static, scheduled, or minted by the factory (Phase 5) — is built this
way: the Constitution is its outermost frame and the role/task nest inside it
(Invariant 6). The factory will extend this with tool scope, tiers, and the scope
ceiling; here we prove the inheritance + self-evaluation seam end to end.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.constitution import Message, frame_context
from core.models import ModelServer


@dataclass(frozen=True)
class SelfCheck:
    """Result of the Constitution pre-return check (BUILD-SPEC §4 self-evaluation
    mandate)."""

    passed: bool
    notes: tuple[str, ...] = ()


def self_evaluate(output: str) -> SelfCheck:
    """Phase 0 stub of the self-evaluation mandate.

    The seam exists so no agent can return without passing through the Constitution
    check. Phase 2 fills this in: deterministic checks first (e.g. verify cited
    identifiers resolve), then a small-model judge for subjective cases — always A/B'd
    against a baseline snapshot, never scored cold (§4, §15).
    """
    return SelfCheck(passed=True, notes=("phase0-stub",))


@dataclass
class Agent:
    name: str
    role_prompt: str
    tier: str = "routine"
    server: ModelServer | None = None

    def build_context(self, task: str, *, history: list[Message] | None = None) -> list[Message]:
        """The agent's context, Constitution outermost (Invariant 6)."""
        return frame_context(self.role_prompt, task, history=history)

    def respond(self, task: str, *, history: list[Message] | None = None,
                think: bool | None = None) -> tuple[str, SelfCheck]:
        if self.server is None:
            raise RuntimeError(f"agent {self.name!r} has no model server bound")
        output = self.server.chat(self.tier, self.build_context(task, history=history), think=think)
        return output, self_evaluate(output)
