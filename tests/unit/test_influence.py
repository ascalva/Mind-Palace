"""Overlay influence v1 (bp-082 Items 11–12; dn-synchronic-diachronic-dreamer §2.7 SD-7).

Item 11 — the INTEGER family (exact recompute-diff, CN-3 leave-one-out attribution):
  * a staged bridge edge flips a two-component σ* from None to a reading, and the influence claim
    names EXACTLY that staged edge (leave-one-out confirmed);
  * a staged arc that closes a directed cycle appears in Δcensus with its witness;
  * an empty overlay ⇒ zero influence (every pair unchanged; no new census claims);
  * the falsifier is structurally impossible — attribution names only leave-one-out-confirmed edges.

Item 12 — the SMOOTH family (the Rayleigh first-order estimator + the finite-difference check):
  * on a synthetic Laplacian, a small Δ agrees with the exact recompute-diff within the second-order
    bound and declares "perturbative"; a large Δ switches to exact and declares "recomputed, not
    perturbative" (F-SD7a);
  * the one-sided addition law is structural — pure addition is signed non-negative, and an
    edit/removal overlay is refused up front (SD-e parked).
"""

from __future__ import annotations

import numpy as np
import pytest

from core.graph.census import INFLUENCE_LOOP, Arc
from core.graph.composed import StagedGrantRequired
from core.graph.influence import (
    NegativeAdditiveInfluenceError,
    NonAdditiveOverlayError,
    census_influence,
    rayleigh_influence,
    sigma_star_influence,
)
from core.scope import (
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
from core.temporal.spine import Certificate, CertifiedCut


# ── grants (the HYPOTHETICAL capability gates the whole influence op) ─────────────────────────────
def _hyp_grant() -> Scope:
    """A grant naming HYPOTHETICAL beside a durable stratum — a valid multi-stratum composed grant
    (COMMIT clock supplies the cut, so SLICE is satisfied)."""
    return Scope(
        StratumScope.of(Stratum.MIRROR_AUTHORED, Stratum.HYPOTHETICAL),
        EdgeScope.bottom(),
        TimeScope(Clock.COMMIT, Window.point("deadbeef")),
        Authority.read_only(),
        tier=Tier.STATIC_GUARD,
    )


def _durable_only_grant() -> Scope:
    """A durable-only grant — does NOT name HYPOTHETICAL, so it cannot see staged rows."""
    return Scope(
        StratumScope.of(Stratum.MIRROR_AUTHORED),
        EdgeScope.bottom(),
        TimeScope(Clock.COMMIT, Window.point("deadbeef")),
        Authority.read_only(),
        tier=Tier.STATIC_GUARD,
    )


def _cut() -> CertifiedCut:
    return CertifiedCut(
        frontier=(("versions:noteA", 3),),
        certificates=frozenset({Certificate.COMMIT}),
        evidence=("deadbeef",),
    )


_GRID = (0.5, 0.7, 0.9)
# Two similarity components {a—b}, {c—d}, no sim edge between them.
_NODES = ("a", "b", "c", "d")
_SIM_EDGES = [("a", "b", 0.9), ("c", "d", 0.9)]


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Item 11 — integer family: σ* component-structure influence + CN-3 attribution
# ═══════════════════════════════════════════════════════════════════════════════════════════════


def test_staged_bridge_flips_sigma_star_and_names_exactly_that_edge():
    """A staged bridge b—c joins the two similarity components: a—d, unconnected without the
    overlay, reads σ*=0.9 with it, and the influence claim names EXACTLY that one staged edge
    (leave-one-out confirmed)."""
    staged = [("b", "c", 1.0)]
    infl = sigma_star_influence(_NODES, _SIM_EDGES, [], staged, grant=_hyp_grant(), grid=_GRID)
    by_pair = {(i.a, i.b): i for i in infl}
    ad = by_pair[("a", "d")]
    assert ad.before is None                       # disconnected without the overlay
    assert ad.after == 0.9                          # connected via the staged bridge
    assert ad.changed
    assert ad.attributed == (("b", "c", 1.0),)      # exactly that staged edge, LOO-confirmed


def test_empty_overlay_is_zero_influence_sigma_star():
    """An empty overlay moves nothing — every pair's σ* is unchanged (before == after), so no pair
    is `changed` and no attribution is minted."""
    infl = sigma_star_influence(_NODES, _SIM_EDGES, [], [], grant=_hyp_grant(), grid=_GRID)
    assert len(infl) == 6                            # every pair over 4 nodes
    assert all(not i.changed for i in infl)
    assert all(i.attributed == () for i in infl)
    assert all(i.before == i.after for i in infl)


def test_attribution_is_leave_one_out_confirmed_not_decorative():
    """With TWO staged edges where only one is load-bearing for a pair, attribution names the
    load-bearing edge alone — the CN-3 falsifier (naming an element whose removal does NOT change
    the reading) is structurally avoided. b—c bridges a—d; c—d already exists in sim, so a staged
    duplicate c—d is NOT the reconnecting edge for a—d."""
    staged = [("b", "c", 1.0), ("c", "d", 1.0)]     # c—d duplicates an existing sim edge
    infl = sigma_star_influence(_NODES, _SIM_EDGES, [], staged, grant=_hyp_grant(), grid=_GRID)
    ad = {(i.a, i.b): i for i in infl}[("a", "d")]
    assert ad.attributed == (("b", "c", 1.0),)  # only the bridge; the c—d duplicate is not named


def test_one_sided_law_holds_for_pure_addition():
    """A pure-addition overlay can only RAISE σ*: no pair ever reads `after < before` (None as the
    floor). The op returns without raising `NegativeAdditiveInfluenceError`."""
    staged = [("b", "c", 1.0), ("a", "c", 0.7)]
    infl = sigma_star_influence(_NODES, _SIM_EDGES, [], staged, grant=_hyp_grant(), grid=_GRID)
    for i in infl:
        before = float("-inf") if i.before is None else i.before
        after = float("-inf") if i.after is None else i.after
        assert after >= before                      # non-decreasing, structurally


def test_influence_refuses_without_a_hypothetical_grant():
    """The whole influence op is gated by the HYPOTHETICAL capability — a durable-only grant cannot
    reach the staged overlay, so `compose_staged` refuses at assembly (fail-closed)."""
    with pytest.raises(StagedGrantRequired):
        sigma_star_influence(
            _NODES, _SIM_EDGES, [], [("b", "c", 1.0)], grant=_durable_only_grant(), grid=_GRID
        )


# ── the census (arrow-aware) influence: Δcensus over staged arcs ──────────────────────────────────


def test_staged_arc_closes_a_cycle_appears_in_delta_census_with_witness():
    """A staged arc c→a closes the directed cycle a→b→c→a that the base arcs alone do not: it
    appears in Δcensus as a NEW influence-loop claim carrying its exact witness, attributed to that
    staged arc leave-one-out."""
    base = [Arc("a", "b", "e1"), Arc("b", "c", "e2")]
    staged = [Arc("c", "a", "s1")]
    infl = census_influence(base, staged, {}, _cut())
    assert len(infl) == 1
    (loop,) = infl
    assert loop.claim.kind == INFLUENCE_LOOP
    assert loop.claim.members == ("a", "b", "c")
    assert loop.claim.witness == ("e1", "e2", "s1")   # the staged arc closes the loop, in-witness
    assert loop.attributed == (Arc("c", "a", "s1"),)  # LOO-confirmed


def test_empty_overlay_is_zero_influence_census():
    """No staged arcs ⇒ no NEW claims ⇒ zero influence (the census over base is unchanged)."""
    base = [Arc("a", "b", "e1"), Arc("b", "c", "e2"), Arc("c", "a", "e3")]  # already a loop
    assert census_influence(base, [], {}, _cut()) == ()


def test_census_influence_excludes_claims_already_present_without_the_overlay():
    """A claim the base already carries is NOT the overlay's influence — only genuinely new claims
    are reported."""
    base = [Arc("a", "b", "e1"), Arc("b", "c", "e2"), Arc("c", "a", "e3")]  # loop without overlay
    staged = [Arc("c", "a", "s1")]  # a parallel arc that does not mint a NEW distinct loop claim
    infl = census_influence(base, staged, {}, _cut())
    # The base loop (witness e1,e2,e3) is not the overlay's; any reported claim is strictly new.
    for ci in infl:
        assert "e3" not in ci.claim.witness


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Item 12 — smooth family: the Rayleigh estimator + the finite-difference check (F-SD7a)
# ═══════════════════════════════════════════════════════════════════════════════════════════════


def _path_adjacency(weights: dict[tuple[int, int], float], n: int = 4) -> np.ndarray:
    """A symmetric weighted adjacency (zero diagonal) over n nodes from an {(i,j): w} edge map."""
    w = np.zeros((n, n), dtype=np.float64)
    for (i, j), val in weights.items():
        w[i, j] = w[j, i] = val
    return w


_BASE_PATH = {(0, 1): 1.0, (1, 2): 1.0, (2, 3): 1.0}   # a 4-node path


def test_small_delta_agrees_within_bound_and_declares_perturbative():
    """A small pure-addition Δ keeps the first-order estimator inside its validity domain: the
    estimate agrees with the exact recompute-diff within the second-order bound, the reading
    declares 'perturbative', and its value is the cheap estimate."""
    w_base = _path_adjacency(_BASE_PATH)
    w_over = _path_adjacency({**_BASE_PATH, (0, 1): 1.0 + 1e-2})   # nudge one edge weight
    infl = rayleigh_influence(w_base, w_over, index=1)
    assert infl.perturbative
    assert infl.mode == "perturbative"
    assert abs(infl.estimate - infl.exact) <= infl.bound + 1e-9   # the finite-difference check
    assert infl.value == infl.estimate
    assert infl.estimate >= 0.0 and infl.exact >= 0.0             # one-sided (ΔL PSD)


def test_large_delta_switches_to_exact_and_declares_recomputed():
    """A large Δ (a strong new long-range edge) pushes ‖ΔL‖ past its Weyl-bracketed validity: the
    reading switches to exact and declares 'recomputed, not perturbative' — F-SD7a's declared
    switch, never a silent disagreement."""
    w_base = _path_adjacency(_BASE_PATH)
    w_over = _path_adjacency({**_BASE_PATH, (0, 3): 5.0})          # a strong new bridge edge
    infl = rayleigh_influence(w_base, w_over, index=1)
    assert not infl.perturbative
    assert infl.mode == "recomputed, not perturbative"
    assert infl.value == infl.exact
    assert infl.exact >= 0.0                                       # one-sided still holds


def test_perturbative_flag_never_disagrees_beyond_bound():
    """The invariant behind F-SD7a: whenever the reading declares 'perturbative', the estimate and
    the exact diff agree within the second-order bound. Swept over a range of Δ magnitudes."""
    w_base = _path_adjacency(_BASE_PATH)
    for delta in (1e-3, 1e-2, 0.1, 0.5, 2.0, 5.0):
        w_over = _path_adjacency({**_BASE_PATH, (0, 1): 1.0 + delta})
        infl = rayleigh_influence(w_base, w_over, index=1)
        if infl.perturbative:
            assert abs(infl.estimate - infl.exact) <= infl.bound + 1e-9


def test_removal_overlay_is_refused_up_front():
    """An edit/removal overlay (a decreased edge weight) is NOT addition-only v1 — it is the
    opposite one-sided law, parked (SD-e). `rayleigh_influence` refuses it up front, never
    conflating the two families."""
    w_base = _path_adjacency(_BASE_PATH)
    w_over = _path_adjacency({**_BASE_PATH, (1, 2): 0.5})  # weakened edge — a removal-ward Δ
    with pytest.raises(NonAdditiveOverlayError):
        rayleigh_influence(w_base, w_over, index=1)


def test_negative_additive_influence_is_a_bug_that_raises():
    """The one-sided law fails the suite, never surfaces as a finding: a hand-forged negative
    reading (an impossible pure-addition outcome) trips `_assert_one_sided_smooth`. Exercised
    directly via the guard so the structural tooth is covered."""
    from core.graph.influence import _assert_one_sided_smooth

    _assert_one_sided_smooth(0.5, 0.4, 1)                          # non-negative: no raise
    with pytest.raises(NegativeAdditiveInfluenceError):
        _assert_one_sided_smooth(-1.0, 0.4, 1)
