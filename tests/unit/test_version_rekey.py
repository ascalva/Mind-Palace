"""The owner-gated `doc_id` re-key primitive (bp-034 Item 14; oq-0019 B; §11 ruling 2026-07-14).

`migrate_rekey_doc_id` is the ONE admitted write to the append-only version store: it RELABELS a
chain's `doc_id` (`source_path -> minted id::`) so an identity switch does not fork lineage. It must
preserve every row's `(version_seq, digest, at)` byte-for-byte (a relabel, never a history rewrite),
be owner-gated (fail-closed), refuse to merge two lineages, and be idempotent under the §3 CHECK
ORDER (no-op cases decided BEFORE the merge refusal, so a partial-failure re-run converges). The
catalog twin carries the same gate plus the resolution-layer uniqueness refusal (`doc_id` has no
unique index). Deterministic, in-process; no network, no model.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from core.stores.authored_supersession import (
    MachineAuthorityRefused,
    OwnerDeclaration,
    owner_declaration,
)
from core.stores.catalog import VaultCatalog
from core.stores.versions import RekeyRefusedError, VersionStore


def _seed_chain(vs: VersionStore, doc_id: str, n: int) -> list[tuple[int, str, str]]:
    """Append `n` versions under `doc_id`; return the pre-migration (seq, digest, at) manifest."""
    for i in range(n):
        vs.record(doc_id, f"digest-{doc_id}-{i}")
    return [(v.version_seq, v.digest, v.at) for v in vs.history(doc_id)]


# ── versions store ───────────────────────────────────────────────────────────────────────────

def test_rekey_relabels_preserving_seq_digest_at(tmp_path: Path):
    # The acceptance surface: history moves old -> new byte-identical; the old key goes empty.
    vs = VersionStore(tmp_path / "versions.sqlite")
    before = _seed_chain(vs, "P", 3)
    assert [s for s, _, _ in before] == [1, 2, 3]

    moved = vs.migrate_rekey_doc_id("P", "X", declaration=owner_declaration())
    assert moved == 3
    after = [(v.version_seq, v.digest, v.at) for v in vs.history("X")]
    assert after == before                                    # seq, digest, AND at all preserved
    assert vs.history("P") == []                              # no orphaned source_path chain
    assert vs.count() == 3                                    # relabel, not append — count fixed


def test_rekey_refuses_without_owner_authority(tmp_path: Path):
    vs = VersionStore(tmp_path / "versions.sqlite")
    _seed_chain(vs, "P", 2)
    with pytest.raises(MachineAuthorityRefused):
        vs.migrate_rekey_doc_id("P", "X", declaration=None)  # type: ignore[arg-type]
    assert [v.version_seq for v in vs.history("P")] == [1, 2]  # nothing moved (fail-closed)


def test_rekey_refuses_forged_declaration(tmp_path: Path):
    # The getattr(_token) guard: a bypass-constructed declaration (no valid token) is refused.
    vs = VersionStore(tmp_path / "versions.sqlite")
    _seed_chain(vs, "P", 1)
    forged = object.__new__(OwnerDeclaration)                # skips __post_init__ / the token
    with pytest.raises(MachineAuthorityRefused):
        vs.migrate_rekey_doc_id("P", "X", declaration=forged)


def test_rekey_same_key_is_noop(tmp_path: Path):             # CHECK ORDER (i)
    vs = VersionStore(tmp_path / "versions.sqlite")
    _seed_chain(vs, "P", 2)
    assert vs.migrate_rekey_doc_id("P", "P", declaration=owner_declaration()) == 0
    assert [v.version_seq for v in vs.history("P")] == [1, 2]


def test_rekey_absent_old_is_noop_not_refusal(tmp_path: Path):  # CHECK ORDER (ii): convergence
    # A re-run of an already-migrated chain: old (P) is empty, new (X) is populated. This MUST be
    # the no-op case, NOT the merge-refusal case — a refuse-first impl breaks re-run idempotency.
    vs = VersionStore(tmp_path / "versions.sqlite")
    _seed_chain(vs, "X", 3)                                   # chain already lives under X
    assert vs.migrate_rekey_doc_id("P", "X", declaration=owner_declaration()) == 0
    assert [v.version_seq for v in vs.history("X")] == [1, 2, 3]  # untouched


def test_rekey_refuses_merging_two_live_chains(tmp_path: Path):  # CHECK ORDER (iii)
    vs = VersionStore(tmp_path / "versions.sqlite")
    _seed_chain(vs, "P", 2)
    _seed_chain(vs, "X", 2)                                   # BOTH populated
    with pytest.raises(RekeyRefusedError):
        vs.migrate_rekey_doc_id("P", "X", declaration=owner_declaration())
    assert [v.version_seq for v in vs.history("P")] == [1, 2]  # neither lineage disturbed
    assert [v.version_seq for v in vs.history("X")] == [1, 2]


def test_rekey_refuses_empty_key(tmp_path: Path):            # input sanity (guardrail 4)
    vs = VersionStore(tmp_path / "versions.sqlite")
    _seed_chain(vs, "P", 1)
    with pytest.raises(RekeyRefusedError):
        vs.migrate_rekey_doc_id("", "X", declaration=owner_declaration())
    with pytest.raises(RekeyRefusedError):
        vs.migrate_rekey_doc_id("P", "", declaration=owner_declaration())


def test_rekey_is_idempotent_on_rerun(tmp_path: Path):
    # The full acceptance re-run: (P, X) once relabels; (P, X) again no-ops via CHECK ORDER (ii).
    vs = VersionStore(tmp_path / "versions.sqlite")
    _seed_chain(vs, "P", 3)
    assert vs.migrate_rekey_doc_id("P", "X", declaration=owner_declaration()) == 3
    assert vs.migrate_rekey_doc_id("P", "X", declaration=owner_declaration()) == 0
    assert [v.version_seq for v in vs.history("X")] == [1, 2, 3]


# ── catalog twin ─────────────────────────────────────────────────────────────────────────────

def test_catalog_rekey_rebinds_doc_id(tmp_path: Path):
    cat = VaultCatalog(tmp_path / "catalog.sqlite")
    cat.record("/vault/a.md", "d1", "a")                     # doc_id defaults to source_path
    assert cat.doc_id_for("/vault/a.md") == "/vault/a.md"
    cat.migrate_rekey_doc_id("/vault/a.md", "id-X", declaration=owner_declaration())
    assert cat.doc_id_for("/vault/a.md") == "id-X"


def test_catalog_rekey_refuses_without_owner_authority(tmp_path: Path):
    cat = VaultCatalog(tmp_path / "catalog.sqlite")
    cat.record("/vault/a.md", "d1", "a")
    with pytest.raises(MachineAuthorityRefused):
        cat.migrate_rekey_doc_id("/vault/a.md", "id-X", declaration=None)  # type: ignore[arg-type]
    assert cat.doc_id_for("/vault/a.md") == "/vault/a.md"    # unchanged (fail-closed)


def test_catalog_rekey_refuses_doc_id_collision(tmp_path: Path):  # guardrail 5 (no unique index)
    cat = VaultCatalog(tmp_path / "catalog.sqlite")
    cat.record("/vault/a.md", "d1", "a", doc_id="id-shared")
    cat.record("/vault/b.md", "d2", "b")                     # doc_id == /vault/b.md
    with pytest.raises(RekeyRefusedError):                   # rebinding b onto a's id would merge
        cat.migrate_rekey_doc_id("/vault/b.md", "id-shared", declaration=owner_declaration())
    assert cat.doc_id_for("/vault/b.md") == "/vault/b.md"    # unchanged


def test_catalog_rekey_is_idempotent(tmp_path: Path):
    cat = VaultCatalog(tmp_path / "catalog.sqlite")
    cat.record("/vault/a.md", "d1", "a")
    decl = owner_declaration()
    cat.migrate_rekey_doc_id("/vault/a.md", "id-X", declaration=decl)
    cat.migrate_rekey_doc_id("/vault/a.md", "id-X", declaration=decl)  # re-run: no clash with self
    assert cat.doc_id_for("/vault/a.md") == "id-X"
