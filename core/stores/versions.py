# ── Family 1 boundary · the provenance layer (version history, NOT the semantic edge graph) ──
# OBJECT:    the append-only version-history store — note-version supersession as PRIMARY
#            provenance, keyed on version identity (ingest-identity-and-amendment.md §4A).
# INVARIANT: append-only; version identity = (doc_id, monotonic version_seq), NOT content digest
#            (C1: a revert stays linear, no cycle); the balance math cannot read this store (C2:
#            version history never enters the signed-edge projection — there is no code handle).
# ENFORCED:  structural — append + reads only (no update/delete) on every machine/runtime path; a
#            store distinct from EdgeStore, so no consumer of the signed graph (build_complex takes
#            an EdgeStore, not this) can reach a version row. Ordering is by version_seq, never by
#            walking edges (§4A). ONE owner-gated exception (bp-034; oq-0019 B; §11 ruling
#            2026-07-14): migrate_rekey_doc_id RELABELS doc_id — an identity migration
#            (source_path → minted id::), never a history rewrite: every row's
#            (version_seq, digest, at) is preserved byte-for-byte, chain merges are refused,
#            old==new / no-rows are no-ops, and the write requires a verified OwnerDeclaration
#            (authored_supersession's capability) — a machine caller is refused at this boundary.
#            The label moves; the sequence, contents, and order never do.
"""Append-only note-version history (ingest-identity-and-amendment.md §4A; build plan Item 6).

A note edited over time is a sequence of VERSIONS, and "v2 supersedes v1" is a PRIMARY provenance
fact — distinct from the semantic support/contradiction edges the balance math consumes. It lives
HERE, not in the `EdgeStore`, for two reasons the shipped implementation got wrong (§4A C1–C2):

  * **Keyed on version identity, not content digest.** Endpoints are `(doc_id, version_seq)`, so a
    revert (v1 → v2 → back to v1's exact bytes) is v3 at seq 3 — distinct from v1 even though the
    digest repeats. The chain stays linear; NO cycle-guard is wanted (rejecting the revert would
    refuse truthful history and break append-only). Content-hash stays the key for the vector
    projection; version-seq is the key here — two layers, two identities.
  * **The balance math cannot read it.** A version relation must never enter the signed-edge graph
    (a placeholder `sign` corrupts λ_min / frustration). `build_complex` takes an `EdgeStore` and
    has no handle to this store, so the exclusion is structural — not a rel-type-filter discipline
    every consumer must remember (the prior design was excluded only *accidentally*; see Q8).

Append-only: each version is one row, `version_seq` monotonic per `doc_id`. The current version is
`max(version_seq)`; supersession is the consecutive-seq relation — both DERIVED from the ordered
sequence, never from edge topology (§4A Ordering authority). Zone A, no network.

One owner-gated identity migration is admitted (bp-034; §11 ruling 2026-07-14):
`migrate_rekey_doc_id` relabels which `doc_id` a chain is filed under — needed exactly once per
identity switch (the id:: mint) so the switch does not FORK lineage, which is the outcome
append-only exists to prevent. `doc_id` is the RESOLVED identity label (provisional
`== source_path` until diverged — see the DDL note), not historical content: the relabel preserves
every row's (version_seq, digest, at) exactly, refuses to merge two chains, and is fail-closed on
owner authority. Runtime paths remain append + reads only.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from core.kernel.config import Config
from core.stores.authored_supersession import OwnerDeclaration, verify_owner_declaration


class RekeyRefusedError(RuntimeError):
    """An owner-gated `doc_id` re-key was refused by a safety gate — a bad/empty key, or a request
    that would MERGE two live lineages onto one id (`old` and `new` both hold rows). The
    `PurgeRefusedError` pattern: fail-closed, named, never a silent merge or partial write. Owner
    authority is refused separately, via `MachineAuthorityRefused` at the same boundary."""


def _utcnow() -> str:
    return datetime.now(UTC).replace(tzinfo=None).isoformat(timespec="seconds")


@dataclass(frozen=True)
class Version:
    doc_id: str
    version_seq: int
    digest: str
    at: str


_DDL = """
CREATE TABLE IF NOT EXISTS versions (
    doc_id      TEXT NOT NULL,        -- stable document identity resolved by sync via the catalog
                                      -- (bp-031: == source_path until a mechanism diverges it — a
                                      -- rename carries this forward, so the chain does not fork)
    version_seq INTEGER NOT NULL,     -- monotonic per doc_id (1,2,3,…) — the VERSION identity
    digest      TEXT NOT NULL,        -- content digest of THIS version (may repeat on a revert)
    at          TEXT NOT NULL,        -- when this version was recorded
    PRIMARY KEY (doc_id, version_seq)
);
CREATE INDEX IF NOT EXISTS versions_doc ON versions(doc_id, version_seq);
"""


@dataclass
class VersionStore:
    path: Path

    def __post_init__(self) -> None:
        if str(self.path) != ":memory:":
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.path))
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_DDL)
        self._conn.commit()

    def current(self, doc_id: str) -> Version | None:
        """The current (highest-seq) version of a document, or None if never recorded."""
        row = self._conn.execute(
            "SELECT * FROM versions WHERE doc_id = ? ORDER BY version_seq DESC LIMIT 1", [doc_id]
        ).fetchone()
        return _row(row) if row else None

    def record(self, doc_id: str, digest: str) -> Version:
        """Append the next version of `doc_id` at `digest` (version_seq = current + 1, or 1). A
        revert to an earlier version's bytes is a NEW version at a higher seq — never a cycle, never
        a merge (§4A C1). Append-only: no prior row is mutated."""
        cur = self.current(doc_id)
        seq = (cur.version_seq + 1) if cur is not None else 1
        v = Version(doc_id=doc_id, version_seq=seq, digest=digest, at=_utcnow())
        self._conn.execute("INSERT INTO versions VALUES (?, ?, ?, ?)",
                           [v.doc_id, v.version_seq, v.digest, v.at])
        self._conn.commit()
        return v

    def history(self, doc_id: str) -> list[Version]:
        """Every version of a document in version-seq order (the append-only chain)."""
        return [_row(r) for r in self._conn.execute(
            "SELECT * FROM versions WHERE doc_id = ? ORDER BY version_seq", [doc_id]).fetchall()]

    def supersessions(self, doc_id: str) -> list[tuple[int, int]]:
        """The `(superseded_seq, superseding_seq)` pairs — consecutive versions, DERIVED from the
        ordered sequence (never from edge topology, §4A Ordering authority)."""
        seqs = [v.version_seq for v in self.history(doc_id)]
        return list(zip(seqs, seqs[1:], strict=False))

    def migrate_rekey_doc_id(self, old: str, new: str, *, declaration: OwnerDeclaration) -> int:
        """Owner-gated identity migration: relabel a chain's `doc_id` from `old` to `new`, keeping
        every row's `(version_seq, digest, at)` byte-for-byte (bp-034; §11 ruling 2026-07-14). A
        RELABEL, never a history rewrite — the label moves, the sequence/contents/order never do;
        the ONE admitted write to this append-only store, needed once per id:: mint so an identity
        switch does not fork lineage. Returns rows relabeled.

        Fail-closed on owner authority (`verify_owner_declaration` — a machine caller refused here).
        CHECK ORDER matters — the no-op cases are decided BEFORE the merge refusal, so a partial run
        (the note re-keyed but interrupted before the next store) converges on re-run instead of
        raising:
          (i)   old == new                 → no-op (0): nothing to relabel.
          (ii)  old holds NO rows          → no-op (0): nothing to move — this is what makes a
                                             re-run of an already-migrated chain converge.
          (iii) old AND new both hold rows → REFUSE (RekeyRefusedError): never merge two lineages.
          (iv)  else                       → relabel (one UPDATE, one statement, one txn)."""
        verify_owner_declaration(declaration)                 # (1) owner authority, fail-closed
        if not old or not new:                                # (4) input sanity
            raise RekeyRefusedError("re-key refused: empty doc_id (old/new must be non-empty)")
        if old == new:                                        # (i) no-op
            return 0
        if self.current(old) is None:                         # (ii) old empty → no-op (converge)
            return 0
        if self.current(new) is not None:                     # (iii) both populated → REFUSE
            raise RekeyRefusedError(
                f"re-key refused: doc_id {new!r} already holds a version chain — relabeling "
                f"{old!r} onto it would MERGE two lineages. Append-only history is never merged."
            )
        cur = self._conn.execute(                             # (iv) relabel — the ONLY UPDATE
            "UPDATE versions SET doc_id = ? WHERE doc_id = ?", [new, old])
        self._conn.commit()
        return cur.rowcount

    def count(self) -> int:
        row = self._conn.execute("SELECT count(*) FROM versions").fetchone()
        return int(row[0]) if row else 0

    def close(self) -> None:
        self._conn.close()


def _row(r: sqlite3.Row) -> Version:
    return Version(doc_id=r["doc_id"], version_seq=r["version_seq"], digest=r["digest"], at=r["at"])


def open_version_store(config: Config | None = None) -> VersionStore:
    from core.kernel.config import get_config

    cfg = config or get_config()
    return VersionStore(cfg.paths.derived_store.parent / "versions.sqlite")
