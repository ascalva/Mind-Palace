"""The human gate — seam for routing privileged requests (BUILD-SPEC §10, §14; Invariant 5).

When the factory is asked for capability beyond an agent's scope ceiling, it routes the
request HERE instead of minting a privileged agent (§10). This is the Phase-5 seam: it
records the request as PENDING so nothing privileged ever happens unattended (Invariant 5,
Constitution §II.4). The full propose → approve → execute → validate → rollback ledger is
Phase 10; this module is its inbox, kept deliberately small.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum


class GateStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"


@dataclass(frozen=True)
class GateRequest:
    id: int
    kind: str             # "privileged_mint" | "out_of_scope_tool" | ...
    detail: str
    status: GateStatus
    created_at: str
    agent: str | None = None


def _utcnow() -> str:
    return datetime.now(UTC).replace(tzinfo=None).isoformat(timespec="seconds")


@dataclass
class HumanGate:
    """Records routed requests. Nothing is auto-approved — approval is a human act
    (Phase 10 wires the durable SQLite ledger + the approve/execute/validate/rollback loop)."""

    _requests: list[GateRequest] = field(default_factory=list)

    def submit(self, kind: str, detail: str, *, agent: str | None = None) -> GateRequest:
        req = GateRequest(
            id=len(self._requests) + 1,
            kind=kind,
            detail=detail,
            status=GateStatus.PENDING,
            created_at=_utcnow(),
            agent=agent,
        )
        self._requests.append(req)
        return req

    def pending(self) -> list[GateRequest]:
        return [r for r in self._requests if r.status is GateStatus.PENDING]

    def all(self) -> list[GateRequest]:
        return list(self._requests)
