"""Persisted minted-agent registry (BUILD-SPEC §8, §10).

Minted agents are ephemeral by default — spun up, used, discarded. The owner may PROMOTE a
useful one to a persistent named agent recorded here (SQLite, the transactional store for
the agent registry per CONVENTIONS). Phase 5 records identity + resolved scope; per-agent
memory grows in later phases.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class PersistedAgent:
    name: str
    role: str
    scope: frozenset[str]
    tier: str
    created_at: str


_DDL = """
CREATE TABLE IF NOT EXISTS persisted_agents (
    name       TEXT PRIMARY KEY,
    role       TEXT NOT NULL,
    scope      TEXT NOT NULL,      -- JSON array of tool ids
    tier       TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


def _utcnow() -> str:
    return datetime.now(UTC).replace(tzinfo=None).isoformat(timespec="seconds")


@dataclass
class AgentRegistry:
    path: Path

    def __post_init__(self) -> None:
        if str(self.path) != ":memory:":
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.path))
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_DDL)
        self._conn.commit()

    def promote(self, name: str, role: str, scope: frozenset[str], tier: str) -> PersistedAgent:
        rec = PersistedAgent(name=name, role=role, scope=frozenset(scope), tier=tier,
                             created_at=_utcnow())
        self._conn.execute(
            "INSERT OR REPLACE INTO persisted_agents VALUES (?, ?, ?, ?, ?)",
            [rec.name, rec.role, json.dumps(sorted(rec.scope)), rec.tier, rec.created_at],
        )
        self._conn.commit()
        return rec

    def get(self, name: str) -> PersistedAgent | None:
        r = self._conn.execute(
            "SELECT * FROM persisted_agents WHERE name = ?", [name]
        ).fetchone()
        return self._row(r) if r else None

    def list(self) -> list[PersistedAgent]:
        rows = self._conn.execute("SELECT * FROM persisted_agents ORDER BY name").fetchall()
        return [self._row(r) for r in rows]

    @staticmethod
    def _row(r: sqlite3.Row) -> PersistedAgent:
        return PersistedAgent(name=r["name"], role=r["role"],
                              scope=frozenset(json.loads(r["scope"])),
                              tier=r["tier"], created_at=r["created_at"])

    def close(self) -> None:
        self._conn.close()
