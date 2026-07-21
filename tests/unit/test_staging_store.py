"""The HYPOTHETICAL staging store (bp-081 Item 8; dn-synchronic-diachronic-dreamer §2.6-2/3/4).

The store is append-only and generation-clocked, records would-be stratum/provenance as ROW DATA,
and — THE SPINE INVARIANT — has NO promotion path to any durable store. The last is asserted
STRUCTURALLY by an API-surface scan (`test_no_promotion_path_exists_by_api_surface_scan`): the
module imports no durable-store writer, no method signature references a durable store, and no
method is named with a promotion verb. Its violation is the plan's immediate-stop falsifier.
"""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

import pytest

from core.provenance import Provenance
from core.scope import Stratum
from core.stores import staging as staging_mod
from core.stores.staging import (
    IllegalWouldBeStratum,
    StagedItem,
    StagingStore,
)


def _store() -> StagingStore:
    return StagingStore(Path(":memory:"))


def _item(digest: str = "d0", *, stratum: Stratum = Stratum.MIRROR_AUTHORED,
          prov: Provenance = Provenance.INTERPRETED) -> StagedItem:
    return StagedItem(would_be_stratum=stratum, would_be_provenance=prov, content_digest=digest)


# ── append advances the generation chain (monotone) ──────────────────────────────────────────────
def test_append_advances_generation_monotone():
    s = _store()
    assert s.current_generation() == 0                       # genesis
    b1 = s.stage("subspace-A", [_item("d1"), _item("d2")])
    b2 = s.stage("subspace-A", [_item("d3")])
    assert b1.generation == 1 and b2.generation == 2         # one admission = one tick
    assert s.current_generation() == 2
    gens = [g.generation for g in s.generations()]
    assert gens == sorted(gens) == [0, 1, 2]                 # monotone, gap-free


def test_one_admission_is_one_generation_shared_by_the_batch():
    s = _store()
    batch = s.stage("subspace-A", [_item("d1"), _item("d2"), _item("d3")])
    rows = s.read_at(batch.generation)
    assert {r.generation for r in rows} == {1}               # the whole batch shares generation 1
    assert len(batch.row_ids) == 3


# ── rows carry would-be stratum/provenance + content digest (stratum ≠ provenance) ───────────────
def test_rows_carry_would_be_stratum_provenance_and_digest():
    s = _store()
    s.stage("subspace-A",
            [StagedItem(would_be_stratum=Stratum.MIRROR_AUTHORED,
                        would_be_provenance=Provenance.AUTHORED_SOLO, content_digest="c1",
                        payload="a hypothesis")])
    (row,) = s.read_at()
    # stratum and provenance are INDEPENDENT row data (dn-agent-taxonomy §2.3)
    assert row.would_be_stratum is Stratum.MIRROR_AUTHORED
    assert row.would_be_provenance is Provenance.AUTHORED_SOLO
    assert row.content_digest == "c1" and row.payload == "a hypothesis"


def test_would_be_stratum_of_overlay_or_denylist_is_refused():
    """A staged row's would-be home is a DURABLE stratum — never the overlay class, never 𝔇."""
    s = _store()
    with pytest.raises(IllegalWouldBeStratum):
        s.stage("subspace-A", [_item("d1", stratum=Stratum.HYPOTHETICAL)])
    with pytest.raises(IllegalWouldBeStratum):
        s.stage("subspace-A", [_item("d1", stratum=Stratum.FOUNDATION)])


# ── reads are generation-addressed (reproducible as a record) ────────────────────────────────────
def test_reads_are_generation_addressed():
    s = _store()
    g1 = s.stage("subspace-A", [_item("d1")]).generation
    g2 = s.stage("subspace-A", [_item("d2")]).generation
    # a read AT g1 sees only what existed at g1 — reproducible regardless of later admissions
    assert {r.content_digest for r in s.read_at(g1)} == {"d1"}
    assert {r.content_digest for r in s.read_at(g2)} == {"d1", "d2"}
    # and pinning g1 stays stable after g2 is admitted (the record property)
    assert {r.content_digest for r in s.read_at(g1)} == {"d1"}


def test_subspace_at_projects_one_subspace():
    s = _store()
    s.stage("subspace-A", [_item("a1")])
    s.stage("subspace-B", [_item("b1")])
    assert {r.content_digest for r in s.subspace_at("subspace-A")} == {"a1"}
    assert {r.content_digest for r in s.subspace_at("subspace-B")} == {"b1"}


# ── tombstone on expiry per SD-d default (removed from reads; record survives) ────────────────────
def test_tombstone_removes_from_reads_but_keeps_the_record():
    s = _store()
    b = s.stage("subspace-A", [_item("d1"), _item("d2")])
    live_before = s.read_at()
    assert len(live_before) == 2
    sweep_gen = s.tombstone([b.row_ids[0]])
    assert sweep_gen == 2                                     # the sweep is its own tick
    # gone from the current view …
    assert {r.content_digest for r in s.read_at()} == {"d2"}
    # … but the record survives in the audit view AND at the pre-tombstone generation
    assert len(s.all_rows()) == 2 and s.count() == 2
    assert {r.content_digest for r in s.read_at(b.generation)} == {"d1", "d2"}


def test_tombstone_is_idempotent_and_has_no_inverse():
    s = _store()
    b = s.stage("subspace-A", [_item("d1")])
    first = s.tombstone([b.row_ids[0]])
    (row_after_first,) = [r for r in s.all_rows() if r.row_id == b.row_ids[0]]
    assert row_after_first.tombstoned_at_gen == first
    s.tombstone([b.row_ids[0]])                               # re-tombstone: keeps original gen
    (row_after_second,) = [r for r in s.all_rows() if r.row_id == b.row_ids[0]]
    assert row_after_second.tombstoned_at_gen == first        # unchanged (idempotent)
    # there is no un-tombstone / promote method (the API scan below proves the absence structurally)
    assert not hasattr(s, "untombstone") and not hasattr(s, "promote")


# ── wall NEVER orders (Law C4) — reads are ordered by the event clock, not by `at` ────────────────
def test_wall_never_orders_reads():
    """Reads are ordered by (generation, row_id). Wall `at` bookmarks admission but never orders —
    even if two admissions share a wall second, the generation disambiguates and orders them."""
    s = _store()
    s.stage("subspace-A", [_item("d1")])
    s.stage("subspace-A", [_item("d2")])
    rows = s.read_at()
    assert [r.generation for r in rows] == [1, 2]             # monotone by the event clock
    # the store's read SQL orders by generation/row_id, not by `at`
    src = inspect.getsource(StagingStore.read_at)
    assert "ORDER BY generation" in src and "ORDER BY at" not in src


# ── THE SPINE INVARIANT — no promotion path exists (structural API-surface scan) ─────────────────
_DURABLE_STORE_MODULES = {
    "vectorstore", "derived", "versions", "catalog", "edges", "causal_edges",
    "reference_edges", "authored_supersession", "runledger", "chatlog", "chat_events",
    "observation_history", "agent_observations", "code_observations", "verdicts",
    "curated_store", "rawstore", "sourceset", "telemetry",
}
_PROMOTION_VERBS = {
    "promote", "persist", "publish", "ingest", "export", "commit_to", "durable",
    "to_durable", "write_durable", "flush_to", "materialize_durable", "graduate",
}


def test_no_promotion_path_exists_by_api_surface_scan():
    """The plan's spine: there is NO promotion path from HYPOTHETICAL to any durable store. Asserted
    THREE ways, structurally:

      (1) the module IMPORTS no durable-store module — so no writer is even reachable from here;
      (2) no public method is NAMED with a promotion verb; and
      (3) no public method's SIGNATURE references a durable-store type (nothing durable can be
          handed in to be written to).

    Any of these failing is the immediate-stop falsifier (a staged row copied durable-ward)."""
    # (1) import scan — parse the module AST, collect every imported module path
    source = Path(inspect.getfile(staging_mod)).read_text()
    tree = ast.parse(source)
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
            for alias in node.names:
                imported.add(f"{node.module}.{alias.name}")
        elif isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
    leaked = {m for m in imported for d in _DURABLE_STORE_MODULES
              if m.endswith(f"stores.{d}") or m.endswith(f".{d}") or m == d}
    assert not leaked, f"staging.py imports a durable store: {leaked}"

    # (2) + (3) method scan — no promotion verb; no signature references a durable-store type
    public = [name for name in dir(StagingStore) if not name.startswith("_")]
    for name in public:
        low = name.lower()
        assert not any(v in low for v in _PROMOTION_VERBS), f"{name!r} names a promotion verb"
        member = getattr(StagingStore, name)
        if not callable(member):
            continue
        sig = inspect.signature(member)
        for pname, param in sig.parameters.items():
            ann = str(param.annotation)
            assert "Store" not in ann or "StagingStore" in ann, (
                f"method {name!r} param {pname!r} references a store type: {ann}"
            )


def test_module_imports_only_core_and_stdlib():
    """The store is core machinery: it imports only stdlib + core (no ops/edge/scheduler/eval) — so
    it adds NO core→sibling edge to the finding-0103 ratchet."""
    source = Path(inspect.getfile(staging_mod)).read_text()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        mod = None
        if isinstance(node, ast.ImportFrom) and node.module:
            mod = node.module
        elif isinstance(node, ast.Import):
            mod = node.names[0].name
        if mod and mod.split(".")[0] in {"ops", "edge", "scheduler", "eval", "agents", "config"}:
            pytest.fail(f"staging.py reaches outside core: {mod}")
