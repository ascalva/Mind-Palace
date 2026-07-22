"""Purge-raw — deliberate, owner-gated TRUE deletion (design-notes/vault-sync-and-capture.md).

The watcher never deletes raw: a vault delete only TOMBSTONES (derived dropped, raw kept) so
nothing is lost and a re-add dedups. But for genuine privacy deletion the owner must be able
to destroy the source bytes too. That is this action — and it is deliberately NOT the
watcher's default, mirroring the propose/approve posture of the self-modification gate
(Invariant 4): destroying ground truth is consequential and irreversible, so it requires an
explicit owner act and refuses to fire on content still in use.

Two gates, both fail-closed:
  1. `confirm=True` must be passed explicitly (no accidental purge).
  2. the digest must have **zero active references** — an active note still holds this content,
     so tombstone/delete it from the vault first. (Purge operates on already-tombstoned data.)

On success it drops derived rows, removes the raw blob, and deletes the tombstoned catalog
rows for that digest. `scripts/purge_raw.py` is the owner-facing entry.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.kernel.stores.rawstore import RawStore
from core.stores.catalog import VaultCatalog
from core.stores.vectorstore import VectorStore


class PurgeRefusedError(RuntimeError):
    """The purge was refused by a safety gate (no confirm, or content still referenced)."""


@dataclass(frozen=True)
class PurgeResult:
    digest: str
    raw_removed: bool
    paths_removed: tuple[str, ...]


def purge_raw(
    digest: str,
    *,
    raw: RawStore,
    store: VectorStore,
    catalog: VaultCatalog,
    confirm: bool = False,
) -> PurgeResult:
    """Permanently remove a note's raw bytes + derived rows. Owner-gated; see module docstring."""
    if not confirm:
        raise PurgeRefusedError(
            "purge_raw is owner-gated and irreversible — pass confirm=True to proceed"
        )
    if catalog.active_refs(digest) > 0:
        raise PurgeRefusedError(
            f"digest {digest[:12]}… is still held by an active note; delete it from the vault "
            "(tombstone) before purging its raw bytes"
        )

    paths = tuple(catalog.paths_for_digest(digest))   # all tombstoned at this point
    store.delete(digest=digest)                        # derived (idempotent; usually already gone)
    raw_removed = raw.delete(digest)                   # the irreversible step
    catalog.remove_digest(digest)
    return PurgeResult(digest=digest, raw_removed=raw_removed, paths_removed=paths)
