# ── Family: the counterfactual overlay · the HYPOTHETICAL staging substrate · docs/NOTATION.md ────
# OBJECT:    the staging store — append-only, generation-clocked rows that hold STAGED hypotheses.
#            A staged row carries its WOULD-BE stratum/provenance as ROW DATA (stratum ≠ provenance,
#            dn-agent-taxonomy §2.3), lives at the overlay stratum HYPOTHETICAL for visibility, and
#            is addressed by generation N_hyp (its per-stratum event clock; ticks = generations).
# INVARIANT: append-only; generations MONOTONE; wall NEVER orders (Law C4 — `at` is a bookmark, the
#            generation orders); expiry is TOMBSTONE (SD-d default); and — THE SPINE INVARIANT —
#            there is NO promotion path from HYPOTHETICAL to any durable store. This module imports
#            no durable-store writer and exposes no method whose signature could write a staged row
#            durable-ward; `test_staging_store.py`'s API-surface scan proves it structurally.
# ENFORCED:  structural — the store's only handle is its OWN sqlite connection (no durable store is
#            reachable from here); the no-promotion property is a scan over this class's methods,
#            not a convention. Zone A, no network. Machinery (outer ring — rings classify imports).
"""The HYPOTHETICAL staging store (dn-synchronic-diachronic-dreamer §2.6-2/3/4; bp-081 H-1).

Staged hypotheses live ONLY here — never in a durable store. The design is laundering-proof by
CONSTRUCTION, not by a gate: **there is no promotion path from HYPOTHETICAL to anything** (note
§2.6-3). A hypothesis the owner comes to believe enters the corpus the way everything does — the
owner authors it, or its real source ingests through the normal pipeline. So this store has no
`promote`, no `commit_to`, no durable-store handle; it can only *append* staged rows, *read* them
by generation, and *tombstone* them on expiry. That absence is the whole invariant, and the API
surface scan in the tests asserts it structurally (the plan's spine).

**The clock (§2.6-2).** Admission and expiry are append events on the store's OWN chain — a
per-stratum event clock `N_hyp` whose ticks are GENERATIONS. Every write (a `stage` admission, a
sweep tombstone tick) advances the generation by one and logs a bookmark in `staging_generations`.
Reads are GENERATION-ADDRESSED (`read_at(g)`), so a dream report that pinned generation `g` stays
reproducible AS A RECORD even after the rows expire. Wall time (`at`, `ttl_wall`) is a COORDINATE
CHART for owner-convenience lookup only — it NEVER orders anything (Law C4); the wall→generation
resolution the sweep does is interval-valued and ambiguity-widening (D8), and lives sweep-side.

**Stratum ≠ provenance.** A staged row records its *would-be* stratum (where it would live if it
were real — mirror, interpreted, …) AND its *would-be* provenance, both as ROW DATA. The row's
overlay stratum is always HYPOTHETICAL (implicit — that is the visibility class). A would-be
stratum of HYPOTHETICAL or FOUNDATION is refused: the overlay is not a promotion target and the
denylist is never a home.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from core.config import Config
from core.provenance import Provenance
from core.scope import Stratum

# A would-be stratum that is never a legitimate home for a staged row: the overlay itself (a staged
# row's would-be identity is a DURABLE stratum, never "hypothetical") and the denylist (𝔇 is never a
# home). Refused at admission — keeps "would-be stratum" honest.
_ILLEGAL_WOULD_BE: frozenset[Stratum] = frozenset({Stratum.HYPOTHETICAL, Stratum.FOUNDATION})


class IllegalWouldBeStratum(ValueError):
    """A staged row named a would-be stratum that is not a durable home (HYPOTHETICAL / FOUNDATION).
    A staged row's would-be identity is where it WOULD live if real — never the overlay class, never
    the denylist. Refused at admission (fail-closed)."""


def _utcnow() -> str:
    return datetime.now(UTC).replace(tzinfo=None).isoformat(timespec="seconds")


@dataclass(frozen=True)
class StagedItem:
    """One hypothesis to admit: its would-be stratum + provenance (ROW DATA — stratum ≠ provenance),
    its content digest (the content address the conditioning law's `derives` tails cite), and an
    opaque payload. No generation here — the store assigns it at `stage`."""

    would_be_stratum: Stratum
    would_be_provenance: Provenance
    content_digest: str
    payload: str = ""


@dataclass(frozen=True)
class StagedRow:
    """A staged row as stored: its identity (`row_id`), the `subspace_id` it belongs to, the
    `generation` it was admitted at, its would-be stratum/provenance + content digest, its opaque
    payload, an optional wall-denominated TTL (`ttl_wall` — owner convenience, resolved to a
    generation at sweep; NEVER an ordering key), the generation a sweep tombstoned it at
    (`tombstoned_at_gen`, None while live), and the wall `at` bookmark of its admission."""

    row_id: int
    subspace_id: str
    generation: int
    would_be_stratum: Stratum
    would_be_provenance: Provenance
    content_digest: str
    payload: str
    ttl_wall: str | None
    tombstoned_at_gen: int | None
    at: str


@dataclass(frozen=True)
class StagedBatch:
    """The result of one `stage` admission: the generation the batch was admitted at and the ids of
    the rows appended (so a caller can pin the (subspace, generation) it staged)."""

    generation: int
    row_ids: tuple[int, ...]


@dataclass(frozen=True)
class GenerationEvent:
    """One tick of `N_hyp` — a bookmark in the generation chain. `kind` ∈ {genesis, admission,
    sweep}; `at` is the wall bookmark (lookup only — never orders). The sweep's wall→generation
    resolver reads these to bracket a wall time into a generation interval (D8)."""

    generation: int
    at: str
    kind: str


_DDL = """
CREATE TABLE IF NOT EXISTS staging_generations (
    generation  INTEGER PRIMARY KEY,     -- the N_hyp tick (monotone; the ONLY ordering key)
    at          TEXT NOT NULL,           -- wall bookmark of the tick (lookup only; never orders)
    kind        TEXT NOT NULL            -- genesis | admission | sweep
);
CREATE TABLE IF NOT EXISTS staged_rows (
    row_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    subspace_id        TEXT NOT NULL,
    generation         INTEGER NOT NULL,          -- admission tick (-> staging_generations)
    would_be_stratum   TEXT NOT NULL,             -- ROW DATA: where it WOULD live (stratum ≠ prov)
    would_be_provenance TEXT NOT NULL,            -- ROW DATA: its would-be provenance label
    content_digest     TEXT NOT NULL,             -- content address (the conditioning-law tail)
    payload            TEXT NOT NULL DEFAULT '',
    ttl_wall           TEXT,                      -- optional wall TTL (owner convenience; no order)
    tombstoned_at_gen  INTEGER,                   -- sweep tick that tombstoned it (NULL = live)
    at                 TEXT NOT NULL              -- wall bookmark of admission (lookup only)
);
CREATE INDEX IF NOT EXISTS staged_rows_subspace ON staged_rows(subspace_id);
CREATE INDEX IF NOT EXISTS staged_rows_generation ON staged_rows(generation);
"""


def _row_to_staged(r: sqlite3.Row) -> StagedRow:
    return StagedRow(
        row_id=int(r["row_id"]),
        subspace_id=r["subspace_id"],
        generation=int(r["generation"]),
        would_be_stratum=Stratum(r["would_be_stratum"]),
        would_be_provenance=Provenance(r["would_be_provenance"]),
        content_digest=r["content_digest"],
        payload=r["payload"],
        ttl_wall=r["ttl_wall"],
        tombstoned_at_gen=None if r["tombstoned_at_gen"] is None else int(r["tombstoned_at_gen"]),
        at=r["at"],
    )


@dataclass
class StagingStore:
    """Append-only, generation-clocked staging for the HYPOTHETICAL overlay.

    The store's ONLY handle is its own sqlite connection — no durable store is reachable from here,
    which is what makes "a staged row reaches a durable store" unrepresentable rather than forbidden
    (the no-promotion spine invariant, note §2.6-3). Generations are monotone and owned here; wall
    time is a bookmark, never an ordering key."""

    path: Path

    def __post_init__(self) -> None:
        if str(self.path) != ":memory:":
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.path))
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_DDL)
        # Genesis tick: generation 0 exists before any admission, so `current_generation` is total.
        if self._conn.execute("SELECT count(*) FROM staging_generations").fetchone()[0] == 0:
            self._conn.execute(
                "INSERT INTO staging_generations VALUES (?, ?, ?)", [0, _utcnow(), "genesis"]
            )
        self._conn.commit()

    # ── the N_hyp clock ──────────────────────────────────────────────────────────────────────────
    def current_generation(self) -> int:
        """The latest `N_hyp` tick — the generation a bare read is addressed at."""
        row = self._conn.execute("SELECT max(generation) AS g FROM staging_generations").fetchone()
        return int(row["g"]) if row and row["g"] is not None else 0

    def _tick(self, kind: str) -> tuple[int, str]:
        """Advance `N_hyp` by one, log the bookmark, return `(generation, at)`. MONOTONE by the
        PRIMARY KEY + `max+1`; the ONLY place a generation is minted."""
        at = _utcnow()
        gen = self.current_generation() + 1
        self._conn.execute("INSERT INTO staging_generations VALUES (?, ?, ?)", [gen, at, kind])
        return gen, at

    def generations(self) -> list[GenerationEvent]:
        """The `N_hyp` chain — the generation bookmarks the sweep's wall→generation resolver reads
        (D8). Ordered by generation (never by wall)."""
        return [GenerationEvent(int(r["generation"]), r["at"], r["kind"])
                for r in self._conn.execute(
                    "SELECT * FROM staging_generations ORDER BY generation")]

    # ── admission (append-only) ──────────────────────────────────────────────────────────────────
    def stage(self, subspace_id: str, items: list[StagedItem], *,
              ttl_wall: str | None = None) -> StagedBatch:
        """Admit a batch of staged items under `subspace_id`. ONE admission = ONE generation tick
        (an append event on `N_hyp`); every row in the batch shares that generation. Append-only —
        rows are never mutated after admission except a sweep's tombstone stamp.

        Refuses (fail-closed) a would-be stratum that is not a durable home
        (HYPOTHETICAL/FOUNDATION, `IllegalWouldBeStratum`). Returns the generation + the appended
        row ids so the caller can pin the (subspace, generation) it staged."""
        for it in items:
            if it.would_be_stratum in _ILLEGAL_WOULD_BE:
                raise IllegalWouldBeStratum(
                    f"staged row would-be stratum {it.would_be_stratum.value!r} is not a durable "
                    f"home — the overlay class and 𝔇 are never promotion targets (note §2.6-3)"
                )
        gen, at = self._tick("admission")
        row_ids: list[int] = []
        for it in items:
            cur = self._conn.execute(
                "INSERT INTO staged_rows (subspace_id, generation, would_be_stratum, "
                "would_be_provenance, content_digest, payload, ttl_wall, tombstoned_at_gen, at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?)",
                [subspace_id, gen, it.would_be_stratum.value, it.would_be_provenance.value,
                 it.content_digest, it.payload, ttl_wall, at],
            )
            row_ids.append(int(cur.lastrowid or 0))
        self._conn.commit()
        return StagedBatch(generation=gen, row_ids=tuple(row_ids))

    # ── generation-addressed reads ───────────────────────────────────────────────────────────────
    def read_at(self, generation: int | None = None) -> list[StagedRow]:
        """The staged rows VISIBLE at `generation` (default: the current tick) — admitted at or
        before `generation` and NOT tombstoned as of it. Generation-addressed and reproducible: the
        same `generation` always yields the same rows, so an expired dream stays a record. Ordered
        by (generation, row_id) — by the event clock, NEVER by wall (Law C4)."""
        g = self.current_generation() if generation is None else generation
        rows = self._conn.execute(
            "SELECT * FROM staged_rows WHERE generation <= ? "
            "AND (tombstoned_at_gen IS NULL OR tombstoned_at_gen > ?) "
            "ORDER BY generation, row_id",
            [g, g],
        )
        return [_row_to_staged(r) for r in rows]

    def subspace_at(self, subspace_id: str, generation: int | None = None) -> list[StagedRow]:
        """The visible rows of one subspace at `generation` — the counterfactual overlay a composed
        read consumes (its digests are the conditioning law's `derives` tails)."""
        return [r for r in self.read_at(generation) if r.subspace_id == subspace_id]

    def all_rows(self) -> list[StagedRow]:
        """EVERY staged row, tombstoned or not — the audit view (append-only, so history is whole).
        Ordered by (generation, row_id)."""
        return [_row_to_staged(r) for r in self._conn.execute(
            "SELECT * FROM staged_rows ORDER BY generation, row_id")]

    # ── expiry (tombstone; sweep-driven — read/tombstone-only, NEVER promotion) ───────────────────
    def tombstone(self, row_ids: list[int]) -> int:
        """Advance `N_hyp` by one (a sweep tick) and TOMBSTONE `row_ids` at that generation — the
        SD-d default disposition (append-only discipline; the row leaves every read_at(g') for
        g' ≥ the tick, but the record survives). Idempotent on already-tombstoned rows (they keep
        their original tombstone generation). Returns the sweep tick's generation.

        This is the ONLY mutation after admission, and it is read/tombstone-only: it moves NO row
        anywhere — least of all durable-ward. There is deliberately no inverse (no un-tombstone,
        no promote)."""
        gen, _ = self._tick("sweep")
        if row_ids:
            marks = ",".join("?" for _ in row_ids)
            self._conn.execute(
                f"UPDATE staged_rows SET tombstoned_at_gen = ? "
                f"WHERE row_id IN ({marks}) AND tombstoned_at_gen IS NULL",
                [gen, *row_ids],
            )
        self._conn.commit()
        return gen

    def count(self) -> int:
        """Total rows ever staged (append-only; tombstoned rows still count as records)."""
        row = self._conn.execute("SELECT count(*) FROM staged_rows").fetchone()
        return int(row[0]) if row else 0

    def close(self) -> None:
        self._conn.close()


def open_staging_store(config: Config | None = None) -> StagingStore:
    """Open the staging store beside the other core stores (the store-layer house pattern).
    Sqlite-backed (parked engine default: sqlite, not in-memory — reading records must outlive the
    process)."""
    from core.config import get_config

    cfg = config or get_config()
    path = cfg.paths.derived_store.parent / "staging.sqlite"
    return StagingStore(path)
