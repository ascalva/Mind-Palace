"""Ops — the human gate, safe levers, rollback (BUILD-SPEC §10, §14).

Phase 5 ships the gate *seam* (`HumanGate`): the factory routes privileged, beyond-scope
requests here as PENDING rather than minting a privileged agent (Invariant 5). The full
propose → approve → execute → validate → rollback ledger + safe levers land in Phase 10.
"""

from ops.gate import GateRequest, GateStatus, HumanGate

__all__ = ["GateRequest", "GateStatus", "HumanGate"]
