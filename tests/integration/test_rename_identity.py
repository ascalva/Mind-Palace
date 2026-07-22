"""Rename-stable document identity — bp-031 Item 3, the falsifiable A6 proof
(temporal-retrieval-algebra.md §2.4). A file rename must NOT fork the version-history lineage: the
note's history stays ONE chain under ONE doc_id (no orphaned seq-1 chain). This is the hard
prerequisite the diachronic reader / Result-1 H1 / β*-over-lineage rely on.

Also the acceptance surface for Item 2 (doc_id resolution): an existing `id::` is the stable
identity across a rename, and an exact-content rename carries the doc_id forward without minting
anything into the vault. Deterministic — a fake embedder, real stores; no network, no model.
"""

from __future__ import annotations

from pathlib import Path

from core.ingest.sync import VaultSync
from core.kernel.stores.rawstore import RawStore
from core.stores.catalog import VaultCatalog
from core.stores.vectorstore import VectorStore
from core.stores.versions import VersionStore
from tests.fixtures.embedding import DIM, FakeEmbedder


def _sync(tmp_path: Path) -> VaultSync:
    vault = tmp_path / "vault"
    vault.mkdir()
    return VaultSync(
        vault=vault,
        raw=RawStore(tmp_path / "raw"),
        store=VectorStore(tmp_path / "v.lance", dim=DIM),
        catalog=VaultCatalog(tmp_path / "catalog.sqlite"),
        embedder=FakeEmbedder(),  # type: ignore[arg-type]  # test fixture duck-types Embedder
        version_store=VersionStore(tmp_path / "versions.sqlite"),
    )


def test_pure_rename_keeps_one_continuous_version_chain(tmp_path):
    # The A6 payoff: ingest at A (v1, v2), rename A -> B (content unchanged), rescan -> ONE
    # continuous chain v1,v2,v3 under ONE doc_id. The fork the A6 ruling exists to kill is an orphan
    # seq-1 chain under path B; its absence is the proof.
    sync = _sync(tmp_path)
    assert sync.version_store is not None
    a = sync.vault / "a.md"
    a.write_text("first content", encoding="utf-8")
    sync.rescan()                                          # v1
    a.write_text("second content", encoding="utf-8")
    sync.rescan()                                          # v2
    doc_id = sync.catalog.doc_id_for(str(a))
    assert [v.version_seq for v in sync.version_store.history(doc_id)] == [1, 2]

    b = sync.vault / "b.md"
    a.rename(b)                                            # rename on disk, content unchanged
    sync.rescan()                                          # v3 — the re-appearance at the new path

    # doc_id carried forward; B resolves to the SAME identity; the chain is one continuous run.
    assert sync.catalog.doc_id_for(str(b)) == doc_id
    assert [v.version_seq for v in sync.version_store.history(doc_id)] == [1, 2, 3]
    # NO fork: no seq-1 chain was opened under path B's own name; the store holds exactly one chain.
    assert sync.version_store.history(str(b)) == []
    assert sync.version_store.count() == 3
    # Resolution did NOT mutate the vault (falsifier: an id was minted into the file).
    assert b.read_text(encoding="utf-8") == "second content"


def test_existing_id_property_is_the_stable_identity_across_rename(tmp_path):
    # Item 2 resolution: a note carrying `id:: X` keeps doc_id == X across a source_path change —
    # the id::, not the path, is the identity, and it survives the rename with the chain intact.
    sync = _sync(tmp_path)
    assert sync.version_store is not None
    a = sync.vault / "a.md"
    a.write_text("id:: note-xyz\ncontent about gardening", encoding="utf-8")
    sync.rescan()                                          # v1 under doc_id note-xyz
    assert sync.catalog.doc_id_for(str(a)) == "note-xyz"   # the id::, not the path

    b = sync.vault / "renamed.md"
    a.rename(b)
    sync.rescan()                                          # v2 — carried by the id::
    assert sync.catalog.doc_id_for(str(b)) == "note-xyz"
    assert [v.version_seq for v in sync.version_store.history("note-xyz")] == [1, 2]
    assert sync.version_store.history(str(b)) == []        # never a path-keyed chain
    # The id:: was READ, not written — the file is byte-for-byte what the owner authored.
    assert b.read_text(encoding="utf-8").startswith("id:: note-xyz")


def test_rename_with_edit_falls_back_to_new_lineage(tmp_path):
    # The parked ambiguity (§11): a rename that ALSO edits content can't be matched by exact digest,
    # so it degrades to a fresh identity — no worse than today, and no FALSE carry-forward. This is
    # the deliberate no-regression floor, not the payoff.
    sync = _sync(tmp_path)
    a = sync.vault / "a.md"
    a.write_text("original", encoding="utf-8")
    sync.rescan()
    old_doc_id = sync.catalog.doc_id_for(str(a))

    b = sync.vault / "b.md"
    a.rename(b)
    b.write_text("original but now edited", encoding="utf-8")   # content changed during the move
    sync.rescan()

    new_doc_id = sync.catalog.doc_id_for(str(b))
    assert new_doc_id != old_doc_id           # exact-content match missed → distinct lineage
    assert new_doc_id == str(b)                            # defaulted to the path (no id::)


def test_ambiguous_shared_content_rename_does_not_misattribute(tmp_path):
    # Dedup edge: two vanished paths held identical bytes, so a new path matching that digest has no
    # single predecessor. The rename index drops the ambiguous digest → fresh identity, never a
    # coin-flip carry-forward to the wrong lineage.
    sync = _sync(tmp_path)
    a = sync.vault / "a.md"
    b = sync.vault / "b.md"
    a.write_text("identical twins", encoding="utf-8")
    b.write_text("identical twins", encoding="utf-8")
    sync.rescan()
    a.unlink()
    b.unlink()
    c = sync.vault / "c.md"
    c.write_text("identical twins", encoding="utf-8")     # matches BOTH gone paths' digest
    sync.rescan()

    assert sync.catalog.doc_id_for(str(c)) == str(c)      # ambiguous → defaulted, no misattribution
