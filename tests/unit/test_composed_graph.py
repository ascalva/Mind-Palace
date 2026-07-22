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

import pytest

from core.dreaming.graph import MirrorGraph
from core.graph.composed import (
    E_PROVEN,
    E_SIM,
    E_STAGED,
    ComposedGraph,
    StagedGrantRequired,
    compose,
    compose_staged,
)
from core.graph.conductance import CONDUCTANCE_THRESH, effective_conductance, sigma_t_profile
from core.graph.sigma_star import build_max_spanning_tree, pairwise_sigma_star, sigma_star
from core.kernel.scope import (
    Authority,
    Clock,
    EdgeScope,
    Scope,
    Stratum,
    StratumScope,
    Tier,
    TimeScope,
    Window,
)


def _hyp_grant() -> Scope:
    """A grant that NAMES HYPOTHETICAL beside a durable stratum — a valid multi-stratum composed
    grant (COMMIT clock supplies the cut, so SLICE is satisfied)."""
    return Scope(
        StratumScope.of(Stratum.MIRROR_AUTHORED, Stratum.HYPOTHETICAL),
        EdgeScope.bottom(),
        TimeScope(Clock.COMMIT, Window.point("deadbeef")),
        Authority.read_only(),
        tier=Tier.STATIC_GUARD,
    )


def _durable_only_grant() -> Scope:
    """A durable-only grant — does NOT name HYPOTHETICAL (single-stratum, so no SLICE)."""
    return Scope(
        StratumScope.of(Stratum.MIRROR_AUTHORED),
        EdgeScope.bottom(),
        TimeScope(Clock.COMMIT, Window.point("deadbeef")),
        Authority.read_only(),
        tier=Tier.STATIC_GUARD,
    )

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


# ── H-1 Item 9 (dn-synchronic-diachronic-dreamer §2.6-4) — the staged overlay at ASSEMBLY ─────────
# `compose_staged` adds E_STAGED as a THIRD class at assembly (never a store merge), gated by a
# grant naming HYPOTHETICAL. The existing guard tests above are UNMODIFIED — a staged-free
# composition is bit-identical to `compose` (the additive-extension falsifier).
def test_staged_free_compose_staged_is_bit_identical_to_compose():
    """With NO staged edges, `compose_staged` (under a HYPOTHETICAL grant) reproduces `compose`
    bit-identically — same weight matrix, same class attribution. The staged class is opt-in."""
    plain = compose(_NODES, _SIM_EDGES, [("b", "c", 1.0)])
    staged_empty = compose_staged(_NODES, _SIM_EDGES, [("b", "c", 1.0)], [], grant=_hyp_grant())
    assert (staged_empty.sim == plain.sim).all()
    assert staged_empty.edge_classes == plain.edge_classes
    assert staged_empty.nodes == plain.nodes


def test_staged_overlay_presents_the_mirror_surface_and_runs_the_math():
    """A staged overlay presents through the same MirrorGraph surface, so the REAL σ*/conductance
    run over it unchanged: a staged bridge b—c joins the two similarity components exactly as a
    proven bridge does (weight 1.0 present at every grid σ)."""
    g = compose_staged(_NODES, _SIM_EDGES, [], [("b", "c", 1.0)], grant=_hyp_grant())
    forest = build_max_spanning_tree(_as_mirror(g))
    reading = sigma_star(forest, "a", "d", grid=_GRID)
    assert reading.sigma_star == 0.9                          # connected via the staged bridge
    assert reading.chain == ("a", "b", "c", "d")
    c1 = effective_conductance(_as_mirror(g), "a", "d", sigma=0.5, thresh=CONDUCTANCE_THRESH)
    assert c1 > 0.0                                           # conductance math consumes it too


def test_staged_class_is_retained_in_attribution():
    """Per-class attribution keeps E_STAGED — a pair carried by the staged class only tags E_staged,
    and a pair carried by sim AND staged keeps both (the influence-attribution surface, bp-082)."""
    g = compose_staged(_NODES, [("a", "b", 0.6)], [], [("a", "b", 1.0), ("c", "d", 0.8)],
                       grant=_hyp_grant())
    assert g.classes_of("a", "b") == frozenset({E_SIM, E_STAGED})   # both classes
    assert g.classes_of("c", "d") == frozenset({E_STAGED})          # staged only
    ia, ib = g.nodes.index("a"), g.nodes.index("b")
    assert g.sim[ia, ib] == 1.0                                     # max(0.6, 1.0)


def test_staged_overlay_unconstructable_without_a_hypothetical_grant():
    """The falsifier tooth: a staged row reaching assembly WITHOUT a HYPOTHETICAL-naming grant is
    unconstructable — `compose_staged` refuses at assembly (`StagedGrantRequired`). A durable-only
    grant (however it is otherwise shaped) cannot see staged rows (Σ-visibility capability test)."""
    with pytest.raises(StagedGrantRequired):
        compose_staged(_NODES, _SIM_EDGES, [], [("b", "c", 1.0)], grant=_durable_only_grant())
    # a grant that DOES name HYPOTHETICAL admits the very same overlay
    g = compose_staged(_NODES, _SIM_EDGES, [], [("b", "c", 1.0)], grant=_hyp_grant())
    assert g.classes_of("b", "c") == frozenset({E_STAGED})
