"""The composed graph feeds the EXISTING σ*/conductance math unchanged (bp-070 D3).

D3's contract: an explicit node set × the edge union `E_sim ∪ E_proven`, flattened to the surface
σ-connectivity family already consumes off a `MirrorGraph` — with per-class attribution retained.
These tests are the guard: a sim-only composition reproduces single-class behaviour; a bridge proven
edge flips a cross-component σ* from None to a reading (and raises effective conductance); the class
tags survive the flatten; and the REAL `core.graph.sigma_star` / `core.graph.conductance` functions
are called on the composed graph directly — the whole point being that the math needs NO change.

The `cast(MirrorGraph, …)` at each call site is a static-type bridge ONLY: `ComposedGraph` presents
`MirrorGraph`'s exact runtime surface (`.n`, `.digest`, `.neighbors`, `.sim`), so the math runs
unchanged; the cast asserts that structural compatibility to mypy without touching the math modules.
"""

from __future__ import annotations

from typing import cast

from core.dreaming.graph import MirrorGraph
from core.graph.composed import E_PROVEN, E_SIM, ComposedGraph, compose
from core.graph.conductance import CONDUCTANCE_THRESH, effective_conductance, sigma_t_profile
from core.graph.sigma_star import build_max_spanning_tree, pairwise_sigma_star, sigma_star

_GRID = (0.5, 0.7, 0.9)

# Two similarity components: {a—b} and {c—d}, each internally strong, with NO sim edge between them.
_NODES = ("a", "b", "c", "d")
_SIM_EDGES = [("a", "b", 0.9), ("c", "d", 0.9)]


def _as_mirror(g: ComposedGraph) -> MirrorGraph:
    """Static bridge: ComposedGraph presents MirrorGraph's runtime surface (module docstring)."""
    return cast(MirrorGraph, g)


# ── a sim-only composition reproduces the single-class behaviour ──────────────────────────────
def test_sim_only_composition_has_two_components():
    """With only E_sim edges the composed graph IS the similarity graph: {a,b} and {c,d} are
    separate σ-components, so cross-component σ* is None and intra-component σ* reads the cosine."""
    g = compose(_NODES, _SIM_EDGES, [])
    forest = build_max_spanning_tree(_as_mirror(g))
    assert sigma_star(forest, "a", "b", grid=_GRID).sigma_star == 0.9      # connected within a pair
    assert sigma_star(forest, "a", "c", grid=_GRID).sigma_star is None     # not connected across
    assert g.classes_of("a", "b") == frozenset({E_SIM})
    assert g.classes_of("a", "c") == frozenset()                          # no edge at all


def test_pairwise_sigma_star_runs_on_the_composed_graph():
    """The real `pairwise_sigma_star` consumes the composed graph directly — 6 pairs over 4 nodes,
    the two intra-pair connected, the four cross-pair unconnected."""
    g = compose(_NODES, _SIM_EDGES, [])
    readings = pairwise_sigma_star(build_max_spanning_tree(_as_mirror(g)), grid=_GRID)
    assert len(readings) == 6
    connected = {(r.a, r.b) for r in readings if r.sigma_star is not None}
    assert connected == {("a", "b"), ("c", "d")}


# ── a bridge proven edge joins two σ-components (the DIRECTION the fixture encodes) ────────────
def test_proven_bridge_edge_joins_two_components():
    """Adding a single E_proven edge b—c (weight 1.0) bridges the two similarity components — a—d,
    unconnected under E_sim alone, becomes connected via the proven bridge. The proven weight 1.0 is
    present at every grid σ, so it links the components at the loosest grid."""
    without = compose(_NODES, _SIM_EDGES, [])
    with_bridge = compose(_NODES, _SIM_EDGES, [("b", "c", 1.0)])

    f0 = build_max_spanning_tree(_as_mirror(without))
    f1 = build_max_spanning_tree(_as_mirror(with_bridge))
    assert sigma_star(f0, "a", "d", grid=_GRID).sigma_star is None        # disconnected before
    reading = sigma_star(f1, "a", "d", grid=_GRID)
    assert reading.sigma_star == 0.9                          # connected after (bottleneck 0.9)
    assert reading.chain == ("a", "b", "c", "d")             # the realizing path uses the bridge
    assert with_bridge.classes_of("b", "c") == frozenset({E_PROVEN})


def test_proven_bridge_raises_effective_conductance():
    """The conductance math consumes the composed graph too: a—d has 0 effective conductance under
    E_sim alone (disconnected) and a positive reading once the proven bridge connects them — the
    Rayleigh-monotone direction (adding an edge never lowers conductance)."""
    without = compose(_NODES, _SIM_EDGES, [])
    with_bridge = compose(_NODES, _SIM_EDGES, [("b", "c", 1.0)])
    thr = CONDUCTANCE_THRESH
    c0 = effective_conductance(_as_mirror(without), "a", "d", sigma=0.5, thresh=thr)
    c1 = effective_conductance(_as_mirror(with_bridge), "a", "d", sigma=0.5, thresh=thr)
    assert c0 == 0.0
    assert c1 > 0.0


def test_sigma_t_profile_runs_on_the_composed_graph():
    """`sigma_t_profile` (the CN-3 (σ,t) profile) consumes the composed graph directly and emits a
    well-formed profile per pair with the degeneracy self-diagnostic present."""
    g = compose(_NODES, _SIM_EDGES, [("b", "c", 1.0)])
    profiles = sigma_t_profile(_as_mirror(g), sigma_grid=_GRID, t_grid=(1.0, 5.0))
    assert len(profiles) == 6                                             # every pair
    for p in profiles:
        assert p.sigma_grid == _GRID and p.t_grid == (1.0, 5.0)
        assert isinstance(p.degeneracy_diag, float)             # always present (never absent)


# ── per-class attribution survives the flatten (class tags not lost) ──────────────────────────
def test_both_class_tags_survive_when_a_pair_is_sim_and_proven():
    """A pair carried by BOTH classes keeps both tags, and the flattened weight is the max — the
    'class tags lost in composition' falsifier."""
    g = compose(_NODES, [("a", "b", 0.6)], [("a", "b", 1.0)])
    assert g.classes_of("a", "b") == frozenset({E_SIM, E_PROVEN})
    ia, ib = g.nodes.index("a"), g.nodes.index("b")
    assert g.sim[ia, ib] == 1.0                                           # max(0.6, 1.0)


def test_classes_of_is_order_independent_and_empty_for_non_edges():
    g = compose(_NODES, _SIM_EDGES, [("b", "c", 1.0)])
    assert g.classes_of("c", "b") == g.classes_of("b", "c") == frozenset({E_PROVEN})
    assert g.classes_of("a", "d") == frozenset()                         # no direct edge


# ── compose fails closed on bad input ─────────────────────────────────────────────────────────
def test_compose_rejects_unknown_node_and_self_loop():
    import pytest

    with pytest.raises(KeyError):
        compose(_NODES, [("a", "z", 0.9)], [])                            # 'z' is not a node
    with pytest.raises(ValueError):
        compose(_NODES, [("a", "a", 0.9)], [])                            # self-loop
