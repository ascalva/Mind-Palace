"""Execution request/result types for the sandbox (BUILD-SPEC §11, Invariant 4).

Executed code is *powerless*: it gets no credentials, no network (unless an explicit,
logged, per-execution grant — not in Phase 4), and no access to the private vault. It
returns **data** (stdout/stderr/exit code), never actions on the system. Output is capped
so a result can never blow the context budget (§13).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

DEFAULT_TIMEOUT_S = 10
MAX_TIMEOUT_S = 120
MAX_OUTPUT_BYTES = 64 * 1024   # results are data; cap to protect the context budget (§13)


class Network(StrEnum):
    NONE = "none"   # the only mode Phase 4 runs. Scoped grants are a deliberate, logged
    #                 later extension (§11): per-execution, narrowly scoped, audited.


@dataclass(frozen=True)
class Limits:
    memory: str = "256m"   # podman --memory (also pins --memory-swap to forbid swap)
    cpus: float = 1.0
    pids: int = 128


@dataclass(frozen=True)
class ExecSpec:
    code: str
    language: str = "python"
    timeout_s: int = DEFAULT_TIMEOUT_S
    limits: Limits = field(default_factory=Limits)
    network: Network = Network.NONE
    env: dict[str, str] = field(default_factory=dict)   # NON-secret only (never secrets, §Secrets)

    def __post_init__(self) -> None:
        if not self.code.strip():
            raise ValueError("ExecSpec.code is empty")
        if not 0 < self.timeout_s <= MAX_TIMEOUT_S:
            raise ValueError(f"timeout_s must be in (0, {MAX_TIMEOUT_S}], got {self.timeout_s}")


@dataclass(frozen=True)
class ExecResult:
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool = False
    duration_s: float = 0.0
    truncated: bool = False

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and not self.timed_out
