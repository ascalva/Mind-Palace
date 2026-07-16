"""Theory-probe candidates — the `plausible`-verdict spillover (E6 Item 18, Track L §3 annex).

When the owner verdicts a claim `plausible` in the review REPL ("can't verify yet; interesting"),
the taxonomy names it a **probe candidate** (`core/verdict/taxonomy.py`; Track L §3 verdict table).
This module is the append-only record of those candidates — a small SQLite table beside the verdict
store (plan §11 parked default), so E7 / the report can later enumerate open probes and (out of
scope here) a demon protocol could execute them.

The schema is **grounded in the Track L §3 protocol annex, not invented**
(`docs/design-notes/live-adoption-and-longitudinal-harness.md:140-142`): a probe is
`probe(probe_id, hypothesis, expectation_kind, target_hints)`. Mapped onto a `plausible`-verdicted
claim (plan §3 Q4 — "claim_id + the probe question + provenance key"):

  * `probe_id`        = sha256(claim_id ‖ hypothesis) — makes idempotency-by-(claim_id, question)
                        structural (it IS the primary key), per the Item-18 acceptance test.
  * `claim_id`        = the verdict subject linkage (plan §3 Q2 — the content-addressed claim id).
  * `hypothesis`      = the probe question = the claim's `surface_text` (annex field).
  * `expectation_kind`= the claim's `kind` (annex field).
  * `target_hints`    = the claim's `support_json` (annex field).
  * `pipeline`        = provenance: which pipeline emitted the claim (plan §3 Q4 "provenance key").

Boundaries. Append-only (no update/delete) like the verdict + run stores. Probe *records* only —
NEVER a run trigger; probe execution (a dreamer-alone run) is catalog row 12, R-gated, owner-only
(plan §9, falsifier). Probe records are operational ground truth, ∉ `MIRROR_READABLE` — this store
is a fresh table under the derived-store dir, structurally outside any mirror-readable location, and
no read path here routes a probe into one. Zone A, no network, no model.
"""

from __future__ import annotations

import hashlib
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_DDL = """
CREATE TABLE IF NOT EXISTS probe_candidates (
    probe_id         TEXT PRIMARY KEY,   -- sha256(claim_id ‖ hypothesis); idempotent by (cid, q)
    claim_id         TEXT NOT NULL,      -- the verdict subject linkage (plan Q2; content-address)
    hypothesis       TEXT NOT NULL,      -- the probe question (annex field) = the claim surface
    expectation_kind TEXT NOT NULL,      -- annex field = the claim kind
    target_hints     TEXT NOT NULL,      -- annex field = the claim support set (JSON)
    pipeline         TEXT NOT NULL,      -- provenance: the pipeline that emitted the claim
    recorded_at      TEXT NOT NULL       -- audit (unsigned); when the store appended it
);
"""


def _utcnow() -> str:
    return datetime.now(UTC).replace(tzinfo=None).isoformat(timespec="seconds")


def _probe_id(claim_id: str, hypothesis: str) -> str:
    """Content-address the probe by (claim_id, question) so a re-verdict of the same claim maps to
    ONE probe — the append-only idempotency key (Item-18 acceptance test)."""
    return hashlib.sha256(f"{claim_id}‖{hypothesis}".encode()).hexdigest()


@dataclass(frozen=True)
class ProbeCandidate:
    """One recorded probe candidate — an annex-grounded `probe(...)` keyed to its source claim.

    `recorded_at` is left empty by `from_claim` (the store stamps it on append), so a candidate's
    identity (`probe_id`) never depends on wall-clock — two builds of the same candidate are equal
    and idempotent."""

    probe_id: str
    claim_id: str
    hypothesis: str
    expectation_kind: str
    target_hints: str
    pipeline: str
    recorded_at: str = ""

    @classmethod
    def from_claim(cls, claim: dict[str, Any], *, pipeline: str) -> ProbeCandidate:
        """Build a probe candidate from a `plausible`-verdicted run-ledger claim row. Maps the
        annex fields onto the claim (see module docstring). `hypothesis` = the claim's surface
        text — the thing "can't verify yet; interesting" points at."""
        claim_id = str(claim["claim_id"])
        hypothesis = str(claim["surface_text"])
        return cls(
            probe_id=_probe_id(claim_id, hypothesis),
            claim_id=claim_id,
            hypothesis=hypothesis,
            expectation_kind=str(claim["kind"]),
            target_hints=str(claim["support_json"]),
            pipeline=pipeline,
        )


@dataclass
class ProbeStore:
    """Append-only SQLite store of probe candidates. Exposes `record` + reads only — no update/
    delete (corrections are not a concept here; a probe is a standing candidate). `path` accepts
    `":memory:"` for tests as well as a real on-disk `Path`."""

    path: Path | str
    _conn: sqlite3.Connection = None  # type: ignore[assignment]  # set in __post_init__

    def __post_init__(self) -> None:
        if str(self.path) != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.path))
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_DDL)
        self._conn.commit()

    def record(self, candidate: ProbeCandidate) -> ProbeCandidate:
        """Append one probe candidate, idempotent by `probe_id` (= sha256(claim_id ‖ hypothesis)).
        A second record of the same (claim_id, question) is a no-op — the first row (with its
        original `recorded_at`) stands. Returns the stored record (the existing one on a repeat)."""
        stored = self.get(candidate.probe_id)
        if stored is not None:
            return stored
        rec = ProbeCandidate(
            probe_id=candidate.probe_id, claim_id=candidate.claim_id,
            hypothesis=candidate.hypothesis, expectation_kind=candidate.expectation_kind,
            target_hints=candidate.target_hints, pipeline=candidate.pipeline,
            recorded_at=candidate.recorded_at or _utcnow(),
        )
        # ON CONFLICT DO NOTHING is the structural backstop against a concurrent double-insert.
        self._conn.execute(
            "INSERT INTO probe_candidates (probe_id, claim_id, hypothesis, expectation_kind, "
            "target_hints, pipeline, recorded_at) VALUES (?, ?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(probe_id) DO NOTHING",
            [rec.probe_id, rec.claim_id, rec.hypothesis, rec.expectation_kind,
             rec.target_hints, rec.pipeline, rec.recorded_at],
        )
        self._conn.commit()
        got = self.get(rec.probe_id)
        return got if got is not None else rec

    def get(self, probe_id: str) -> ProbeCandidate | None:
        row = self._conn.execute(
            "SELECT * FROM probe_candidates WHERE probe_id = ?", [probe_id]
        ).fetchone()
        return _row(row) if row is not None else None

    def open_probes(self) -> list[ProbeCandidate]:
        """Enumerate the recorded probe candidates (the reader E7 / the report joins on). Ordered by
        `recorded_at` then `probe_id` for a stable listing. (All recorded probes are "open" — this
        plan records candidates only; execution/resolution is out of scope.)"""
        rows = self._conn.execute(
            "SELECT * FROM probe_candidates ORDER BY recorded_at, probe_id"
        ).fetchall()
        return [_row(r) for r in rows]

    def count(self) -> int:
        row = self._conn.execute("SELECT count(*) FROM probe_candidates").fetchone()
        return int(row[0]) if row else 0

    def close(self) -> None:
        self._conn.close()


def _row(r: sqlite3.Row) -> ProbeCandidate:
    return ProbeCandidate(
        probe_id=r["probe_id"], claim_id=r["claim_id"], hypothesis=r["hypothesis"],
        expectation_kind=r["expectation_kind"], target_hints=r["target_hints"],
        pipeline=r["pipeline"], recorded_at=r["recorded_at"],
    )


def open_probe_store(config: Any = None) -> ProbeStore:
    """Open the configured probe store — its SQLite file lives beside the verdict store + run
    ledger (the plan §11 parked backend). Import of `config.loader` is lazy so this module stays
    dependency-light (and importable without a live config in unit tests)."""
    from config.loader import get_config

    config = config or get_config()
    path: Path = config.paths.derived_store.parent / "probes.sqlite"
    return ProbeStore(path)


__all__ = ["ProbeCandidate", "ProbeStore", "open_probe_store"]


# Idempotency helper is also useful to a caller building a candidate by hand.
def probe_id_for(claim_id: str, hypothesis: str) -> str:
    return _probe_id(claim_id, hypothesis)
