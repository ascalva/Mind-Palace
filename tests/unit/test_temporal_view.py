"""`TemporalView` — the commit-anchored β₁ read surface (bp-037 / CQ-wire, Item 2).

Proves the single-snapshot reads over in-memory fixtures with KNOWN topology (4-cycle → β₁=1, filled
triangle → β₁=0), that the anchor scopes to one commit (never the all-history union), that an empty
anchor is honest, and that no store/mutator surface is reachable through the frozen view (the scope
guard — mirrors `test_reference_view.py`). Deterministic; no model, no network.
"""

from __future__ import annotations

from pathlib import Path

from core.stores.reference_edges import ReferenceEdge, ReferenceEdgeStore
from core.temporal_view import TemporalView


def _cite_store(tmp_path: Path, edges: list[tuple[str, str, str]]) -> ReferenceEdgeStore:
    """A citation store of `(source, target, commit_sha)` doc→doc (`corpus_to_corpus`) edges."""
    store = ReferenceEdgeStore(tmp_path / "reference_edges.sqlite")
    store.add_batch([
        ReferenceEdge.mint(source_kind="corpus", source_ref=u, target_kind="corpus",
                           target_ref=v, ref_type="design-ref", commit_sha=c, source_line=i + 1)
        for i, (u, v, c) in enumerate(edges)
    ])
    return store


def test_citation_threads_counts_beta1_at_the_anchor(tmp_path):
    # A chordless 4-cycle a—b—c—d—a at c1 → β₁ = 1 (no triangle fills it).
    store = _cite_store(tmp_path, [
        ("a", "b", "c1"), ("b", "c", "c1"), ("c", "d", "c1"), ("d", "a", "c1"),
    ])
    view = TemporalView.over(store, commit="c1")
    assert view.commit == "c1"
    assert view.citation_threads() == 1
    assert view.boundary_composition_is_zero() is True
    assert view.n_nodes == 4
    assert view.n_edges == 4


def test_filled_triangle_has_no_thread(tmp_path):
    store = _cite_store(tmp_path, [("a", "b", "c1"), ("b", "c", "c1"), ("a", "c", "c1")])
    view = TemporalView.over(store, commit="c1")
    assert view.citation_threads() == 0        # the flag complex fills the triangle
    assert view.n_nodes == 3 and view.n_edges == 3


def test_anchor_scopes_to_one_commit(tmp_path):
    # The falsifier: an extra edge at c2 must not enter the c1 view (the all-history-union bug).
    store = _cite_store(tmp_path, [
        ("a", "b", "c1"), ("b", "c", "c1"), ("c", "d", "c1"), ("d", "a", "c1"),
        ("e", "f", "c2"),
    ])
    at_c1 = TemporalView.over(store, commit="c1")
    assert at_c1.n_nodes == 4 and at_c1.n_edges == 4    # no e/f leaked in
    assert at_c1.citation_threads() == 1
    at_c2 = TemporalView.over(store, commit="c2")
    assert at_c2.n_nodes == 2 and at_c2.n_edges == 1
    assert at_c2.citation_threads() == 0


def test_empty_anchor_is_honest(tmp_path):
    # A commit with no citation edges → the empty complex: β₁ = 0, ∂₁∂₂=0 trivially, not a crash.
    store = _cite_store(tmp_path, [("a", "b", "c1")])
    view = TemporalView.over(store, commit="nonesuch")
    assert view.n_nodes == 0 and view.n_edges == 0
    assert view.citation_threads() == 0
    assert view.boundary_composition_is_zero() is True


def test_no_store_or_mutator_reachable_through_the_view(tmp_path):
    # The scope guard (§2.1): the frozen view names reads only — no store handle, no mutator.
    store = _cite_store(tmp_path, [("a", "b", "c1")])
    view = TemporalView.over(store, commit="c1")
    for forbidden in ("add_batch", "_conn", "store", "_store", "all", "for_commit"):
        assert not hasattr(view, forbidden), f"scope leak: {forbidden} reachable via TemporalView"
    # The only fields are the frozen complex + the anchor commit — no live store reference retained.
    assert set(vars(view)) == {"_complex", "commit"}
