# ── Family: σ-connectivity instruments · overlay influence (the perturbation term) · NOTATION.md ──
# OBJECT:    the influence of a staged overlay — the per-instrument with/without differential
#            `infl_R(Δ) = R(G ∪ Δ) − R(G)` (dn-synchronic-diachronic-dreamer §2.7 SD-7). Two
#            families: INTEGER (census, σ* component structure — exact recompute-diff, delta-local;
#            integers do not perturb) and SMOOTH (Rayleigh/spectral — the first-order eigenvalue
#            estimator `x*ΔL x` with its finite-difference check). Every changed reading is
#            attributed leave-one-out over the staged elements (CN-3, generalized verbatim §2.7).
# INVARIANT: v1 is ADDITION-ONLY (SD-e parks edit/removal overlays). The one-sided law is
#            STRUCTURAL, not measured: a pure-addition overlay can only RAISE σ*/conductance/
#            Laplacian eigenvalues (weighted Rayleigh + D5 growth monotonicity), so a NEGATIVE
#            additive influence is an implementation BUG that must fail the suite — never a finding.
#            Read-only over assembly; the staged overlay reaches the read ONLY under a HYPOTHETICAL
#            grant (`compose_staged` fail-closed). No store import, no clock (Law C4), no eval (P1).
# ENFORCED:  guard (tests/unit/test_influence.py) — a staged bridge flips a σ* None→reading and the
#            claim names exactly that staged edge leave-one-out; a staged arc closing a cycle shows
#            in Δcensus with its witness; empty overlay ⇒ zero influence; the estimator agrees with
#            the exact diff within the second-order bound for small Δ and declares recompute past
#            it; a negative additive influence raises; a non-HYPOTHETICAL grant refuses at assembly.
r"""Overlay influence v1 — the perturbation term of a staged hypothesis (§2.7 SD-7).

Influence is the differential of an instrument reading along the overlay direction: for a staged
perturbation Δ (the HYPOTHETICAL overlay's added edges/arcs) and a reading R,

    infl_R(Δ) = R(G ∪ Δ) − R(G).

Computed two ways by family, which agree where both apply:

  * **integer family** (σ* component structure; the arrow-aware census) — integers do not perturb,
    so influence is the EXACT recompute-diff over the composed assembly (`core/graph/composed.py`),
    delta-local where the combinatorics allow (a staged bridge that flips a two-component σ* from
    None to a reading; a staged arc that closes a directed cycle in the census). Reused, not
    re-implemented: the σ* diff runs the real `build_max_spanning_tree`/`pairwise_sigma_star`, the
    census diff the real `core.graph.census` families;
  * **smooth family** (Rayleigh/spectral — conductance, heat-kernel eigenvalues) — the first-order
    term IS the definition: for a simple eigenpair (λ, x), `infl_λ(Δ) ≈ x*ΔL x` (the
    Rayleigh-quotient directional derivative, `[FROM MEMORY — verify; standard first-order
    eigenvalue perturbation]`). The EXACT recompute-diff `λ(L+ΔL) − λ(L)` is its finite-difference
    check; when ‖ΔL‖ is not small vs the spectral gap (Weyl-bracketed, `[FROM MEMORY — verify]`)
    OR the estimate disagrees with the exact diff beyond the second-order bound, the reading
    switches to exact and declares "recomputed, not perturbative" (F-SD7a).

**The one-sided law is STRUCTURAL (the honesty anchor, §2.7).** A pure-addition overlay can only
raise σ*, conductance, and the Laplacian eigenvalues — weighted Rayleigh + D5 growth monotonicity;
adding a non-negative edge weight makes ΔL positive-semidefinite, so `x*ΔL x ≥ 0` and every exact
eigenvalue shift is ≥ 0. A negative additive influence is therefore an IMPLEMENTATION BUG, and this
module raises on it (`NegativeAdditiveInfluenceError`) rather than ever surfacing it as a finding.
Edit/removal overlays ("what if this note were gone") are a v2 with the OPPOSITE one-sided law,
parked (SD-e) — a non-addition perturbation is refused up front, never silently conflated.

**Attribution is CN-3, generalized verbatim (§2.7).** The Δ-elements are exactly the staged items;
every influence claim names the staged element(s) it verified leave-one-out — the same
single-element revert-and-recompute the reconnection rider uses (`conductance.reconnection_scan`):
an element whose removal erases the change is named, never a guess.

PURE-CORE: imports core substrate + NumPy/SciPy only — never `eval` (P1), never a clock (Law C4).
The Laplacian is THE core primitive (`core/complex/laplacian`, P3) — never re-derived here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import numpy as np
import scipy.sparse as sp

from core.dreaming.graph import MirrorGraph
from core.graph.census import (
    DEFAULT_MAX_LEN,
    Arc,
    CensusClaim,
    FirstAuthorship,
    census,
)
from core.graph.composed import WeightedEdge, compose_staged
from core.graph.sigma_star import build_max_spanning_tree, pairwise_sigma_star
from core.kernel.complex.laplacian import laplacian as _combinatorial_laplacian
from core.kernel.scope import Scope
from core.temporal.spine import CertifiedCut

# ‖ΔL‖₂ below this fraction of the spectral gap keeps the first-order eigenvalue estimator inside
# its Weyl-bracketed validity domain (`[FROM MEMORY — verify]`; the finite-difference fixture, not
# this constant, is the acceptance ground — Q4). A tolerance, not a tunable magnitude.
_VALIDITY_FRACTION: float = 0.5

# Float-noise thresholds. `_ONE_SIDED_EPS`: a reading below −this is a genuine sign violation (a
# bug), not rounding. `_GAP_EPS`: a spectral gap at or below this is a (near-)degenerate eigenpair —
# the simple-eigenpair premise fails, so the estimator is not perturbative there.
_ONE_SIDED_EPS: float = 1e-9
_GAP_EPS: float = 1e-12


def _as_mirror(graph: object) -> MirrorGraph:
    """Static bridge: a `ComposedGraph` presents the `MirrorGraph` runtime surface (`.n`, `.digest`,
    `.neighbors`, `.sim`), so the real σ* math runs over it unchanged (the D3 contract). The cast
    asserts that structural compatibility to mypy without touching the math modules."""
    return cast(MirrorGraph, graph)


class NegativeAdditiveInfluenceError(AssertionError):
    """A pure-addition overlay produced a NEGATIVE influence reading — structurally impossible
    (weighted Rayleigh + D5 growth monotonicity, §2.7), hence an implementation bug. Raised so it
    FAILS THE SUITE; a negative additive influence is never surfaced as a finding (the one-sided
    law is the honesty anchor)."""


class NonAdditiveOverlayError(ValueError):
    """A smooth-family overlay decreased an edge weight — an edit/removal, not a pure addition. v1
    is addition-only; edit/removal overlays are the opposite one-sided law, parked (SD-e). Refused
    up front so the two families are never conflated."""


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Integer family (Item 11) — exact recompute-diff, CN-3 leave-one-out attribution
# ═══════════════════════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class SigmaStarInfluence:
    """One pair's σ*-component-structure influence: `before`/`after` are the pair's σ* WITHOUT and
    WITH the staged overlay (None ⇒ "not connected within grid"). `attributed` are the staged edges
    whose leave-one-out removal reverts `after` back to `before` — the CN-3 Δ-elements, verified,
    never guessed. `changed` iff the overlay moved the reading."""

    a: str
    b: str
    before: float | None
    after: float | None
    attributed: tuple[WeightedEdge, ...]

    @property
    def changed(self) -> bool:
        return self.before != self.after


def _sigma_key(value: float | None) -> float:
    """Order σ* readings with None as "less than any grid value" (unconnected is the floor), so the
    one-sided law (addition ⇒ non-decreasing) is a plain `after >= before` comparison."""
    return float("-inf") if value is None else value


def _pairwise_sigma_map(
    nodes: tuple[str, ...],
    sim_edges: list[WeightedEdge],
    proven_edges: list[WeightedEdge],
    staged_edges: list[WeightedEdge],
    *,
    grant: Scope,
    grid: tuple[float, ...],
) -> dict[tuple[str, str], float | None]:
    """Every pair's σ* over the composed assembly `E_sim ∪ E_proven ∪ E_staged`, keyed by the
    ordered `(a, b)` pair. Routes through `compose_staged` (fail-closed: a non-HYPOTHETICAL grant
    refuses at assembly) and the REAL σ*/MST math — assembly, never a new instrument."""
    graph = compose_staged(nodes, sim_edges, proven_edges, staged_edges, grant=grant)
    forest = build_max_spanning_tree(_as_mirror(graph))
    return {(s.a, s.b): s.sigma_star for s in pairwise_sigma_star(forest, grid=grid)}


def sigma_star_influence(
    nodes: tuple[str, ...],
    sim_edges: list[WeightedEdge],
    proven_edges: list[WeightedEdge],
    staged_edges: list[WeightedEdge],
    *,
    grant: Scope,
    grid: tuple[float, ...],
) -> tuple[SigmaStarInfluence, ...]:
    """The integer-family σ* influence of the staged overlay: the EXACT recompute-diff of every
    pair's σ* WITHOUT vs WITH `staged_edges`, with CN-3 leave-one-out attribution on every changed
    pair. Both reads go through `compose_staged` under `grant` (so the whole influence op is gated
    by the HYPOTHETICAL capability — a durable-only grant refuses). Integers do not perturb: this is
    an exact diff, never an estimate.

    The one-sided law is enforced structurally: a pure-addition overlay can only raise σ*, so
    `after >= before` (None as the floor) holds for every pair — a violation raises
    `NegativeAdditiveInfluenceError` (a bug, never a finding). Empty overlay ⇒ every pair unchanged
    (zero influence)."""
    before_map = _pairwise_sigma_map(nodes, sim_edges, proven_edges, [], grant=grant, grid=grid)
    after_map = _pairwise_sigma_map(
        nodes, sim_edges, proven_edges, staged_edges, grant=grant, grid=grid
    )
    out: list[SigmaStarInfluence] = []
    for pair, after in after_map.items():
        before = before_map[pair]
        if _sigma_key(after) < _sigma_key(before) - _ONE_SIDED_EPS:
            raise NegativeAdditiveInfluenceError(
                f"σ* influence for {pair} fell from {before} to {after} under a pure-addition "
                f"overlay — impossible (D5 growth monotonicity, §2.7); an implementation bug"
            )
        attributed: tuple[WeightedEdge, ...] = ()
        if before != after:
            attributed = _attribute_sigma(
                nodes, sim_edges, proven_edges, staged_edges, pair, before,
                grant=grant, grid=grid,
            )
        out.append(SigmaStarInfluence(pair[0], pair[1], before, after, attributed))
    return tuple(out)


def _attribute_sigma(
    nodes: tuple[str, ...],
    sim_edges: list[WeightedEdge],
    proven_edges: list[WeightedEdge],
    staged_edges: list[WeightedEdge],
    pair: tuple[str, str],
    before: float | None,
    *,
    grant: Scope,
    grid: tuple[float, ...],
) -> tuple[WeightedEdge, ...]:
    """CN-3 leave-one-out attribution (generalized verbatim): for the changed `pair`, revert each
    staged edge in isolation and recompute its σ*; a staged edge whose removal reverts σ* to
    `before` is a CONFIRMED Δ-element (its removal erases the change). Reports only confirmed edges
    — the falsifier (an element whose leave-one-out removal does NOT change the reading) is
    structurally impossible."""
    a, b = pair
    confirmed: list[WeightedEdge] = []
    for k in range(len(staged_edges)):
        loo = staged_edges[:k] + staged_edges[k + 1 :]
        reverted = _pairwise_sigma_map(
            nodes, sim_edges, proven_edges, loo, grant=grant, grid=grid
        )[(a, b)]
        if reverted == before:
            confirmed.append(staged_edges[k])
    return tuple(confirmed)


# ── the census (arrow-aware) influence: Δcensus over staged arcs ──────────────────────────────────


@dataclass(frozen=True)
class CensusInfluence:
    """One NEW census claim introduced by the staged overlay (present WITH the staged arcs, absent
    WITHOUT), plus the staged arcs whose leave-one-out removal erases it — the CN-3 Δ-elements. The
    claim already carries its own witness (arc ids); `attributed` names which STAGED arcs are
    load-bearing for it."""

    claim: CensusClaim
    attributed: tuple[Arc, ...]


def _claim_key(claim: CensusClaim) -> tuple[str, tuple[str, ...], tuple[str, ...]]:
    """A hashable identity for a census claim — (kind, members, witness). `detail` is excluded (it
    is an unhashable dict and derivable from the other three); two claims with the same key are the
    same fact."""
    return (claim.kind, claim.members, claim.witness)


def census_influence(
    base_arcs: list[Arc],
    staged_arcs: list[Arc],
    authorship: dict[str, FirstAuthorship],
    cut: CertifiedCut,
    *,
    max_len: int = DEFAULT_MAX_LEN,
) -> tuple[CensusInfluence, ...]:
    """The integer-family census influence: the EXACT set-diff of the census over `base_arcs` vs
    over `base_arcs ∪ staged_arcs` at one certified cut — the NEW witnessed claims the overlay
    introduces (a staged arc closing a directed cycle, minting an asymmetry, or a reach-back). Each
    new claim is attributed leave-one-out over the staged arcs (revert one, recompute; a staged arc
    whose removal erases the claim is confirmed). Empty overlay ⇒ no new claims (zero influence)."""
    without = {
        _claim_key(c) for c in census(base_arcs, authorship, cut, max_len=max_len).claims
    }
    with_claims = census([*base_arcs, *staged_arcs], authorship, cut, max_len=max_len).claims
    out: list[CensusInfluence] = []
    for claim in with_claims:
        if _claim_key(claim) in without:
            continue  # already present without the overlay — not the overlay's influence
        attributed: list[Arc] = []
        for k in range(len(staged_arcs)):
            loo = staged_arcs[:k] + staged_arcs[k + 1 :]
            keys = {
                _claim_key(c)
                for c in census([*base_arcs, *loo], authorship, cut, max_len=max_len).claims
            }
            if _claim_key(claim) not in keys:  # removing this arc erases the claim — confirmed
                attributed.append(staged_arcs[k])
        out.append(CensusInfluence(claim, tuple(attributed)))
    return tuple(out)


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Smooth family (Item 12) — the Rayleigh first-order estimator + its finite-difference check
# ═══════════════════════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class RayleighInfluence:
    """One eigenvalue's smooth-family influence under the overlay. `estimate` is the first-order
    Rayleigh term `x*ΔL x`; `exact` is the finite-difference recompute-diff `λ(L+ΔL) − λ(L)`;
    `bound` is the second-order remainder that brackets their agreement. `perturbative` is True iff
    the estimator is inside its Weyl validity domain AND agrees with the exact diff within `bound`;
    then `mode == "perturbative"` and `value` is the cheap estimate. Otherwise the reading switches
    to exact: `mode == "recomputed, not perturbative"` and `value` is `exact` (F-SD7a)."""

    index: int
    estimate: float
    exact: float
    bound: float
    perturbative: bool

    @property
    def mode(self) -> str:
        return "perturbative" if self.perturbative else "recomputed, not perturbative"

    @property
    def value(self) -> float:
        """The honest reading: the first-order estimate when perturbative, else the exact diff."""
        return self.estimate if self.perturbative else self.exact


def _laplacian_of(w: np.ndarray) -> np.ndarray:
    """`L = D − W` via THE core primitive (`core/complex/laplacian`, P3 — one Laplacian; never
    re-derived). Dense for `eigh`/`eigvalsh` (corpus scale is small — finding-0096)."""
    return np.asarray(_combinatorial_laplacian(sp.csr_matrix(w)).toarray(), dtype=np.float64)


def _spectral_gap(vals: np.ndarray, index: int) -> float:
    """The distance from eigenvalue `index` to its nearest neighbour in the spectrum — the simple-
    eigenpair gap the first-order estimator's validity is bracketed by (Weyl). 0 (within noise) ⇒ a
    (near-)degenerate eigenpair, so the estimator is not perturbative there."""
    gaps = [abs(vals[index] - vals[j]) for j in range(len(vals)) if j != index]
    return min(gaps) if gaps else float("inf")


def rayleigh_influence(
    w_base: np.ndarray,
    w_overlay: np.ndarray,
    *,
    index: int,
) -> RayleighInfluence:
    r"""The smooth-family influence of the overlay on eigenvalue `index` of the combinatorial
    Laplacian. `w_base`/`w_overlay` are symmetric weighted adjacencies (zero diagonal) of the graph
    WITHOUT / WITH the overlay — v1 requires `w_overlay >= w_base` elementwise (pure addition;
    edit/removal is SD-e, refused with `NonAdditiveOverlayError`).

    Returns the first-order estimate `x*ΔL x` (x the eigenvector of `L(w_base)` at `index`), the
    exact finite-difference diff `λ_index(L(w_overlay)) − λ_index(L(w_base))`, the second-order
    bound bracketing them, and whether the estimator is perturbatively valid. The one-sided law is
    structural: pure addition makes ΔL PSD, so BOTH `estimate` and `exact` are ≥ 0 — a negative
    reading raises `NegativeAdditiveInfluenceError` (a bug, never a finding).

    The perturbative flag never lies: it is claimed only when ‖ΔL‖₂ is inside its Weyl-bracketed
    validity fraction of the spectral gap AND `|estimate − exact| ≤ bound`. Past either, the reading
    declares recompute (F-SD7a): the finite-difference check IS the estimator's validity gate."""
    w_base = np.asarray(w_base, dtype=np.float64)
    w_overlay = np.asarray(w_overlay, dtype=np.float64)
    if np.any(w_overlay < w_base - _ONE_SIDED_EPS):
        raise NonAdditiveOverlayError(
            "rayleigh_influence: the overlay decreases an edge weight — an edit/removal, not a "
            "pure addition. v1 is addition-only; edit/removal overlays are parked (SD-e)"
        )
    lap_base = _laplacian_of(w_base)
    lap_over = _laplacian_of(w_overlay)
    delta_lap = lap_over - lap_base

    vals, vecs = np.linalg.eigh(lap_base)
    x = vecs[:, index]
    estimate = float(x @ delta_lap @ x)
    # The finite-difference check: the exact eigenvalue shift, recomputed (not perturbative).
    exact = float(np.linalg.eigvalsh(lap_over)[index] - vals[index])

    _assert_one_sided_smooth(estimate, exact, index)

    gap = _spectral_gap(vals, index)
    delta_norm = float(np.linalg.norm(delta_lap, 2))
    # Kato-style second-order remainder for a simple eigenvalue: ‖ΔL‖²/gap `[FROM MEMORY — verify]`.
    bound = delta_norm**2 / gap if gap > _GAP_EPS else float("inf")
    weyl_valid = gap > _GAP_EPS and delta_norm <= _VALIDITY_FRACTION * gap
    perturbative = weyl_valid and abs(estimate - exact) <= bound + _ONE_SIDED_EPS
    return RayleighInfluence(
        index=index, estimate=estimate, exact=exact, bound=bound, perturbative=perturbative
    )


def _assert_one_sided_smooth(estimate: float, exact: float, index: int) -> None:
    """The structural one-sided law for the smooth family: a pure-addition overlay makes ΔL
    positive-semidefinite, so `x*ΔL x ≥ 0` (Rayleigh) and every exact eigenvalue shift ≥ 0 (Weyl).
    A negative reading is impossible — an implementation bug that must fail the suite, never a
    finding."""
    if estimate < -_ONE_SIDED_EPS or exact < -_ONE_SIDED_EPS:
        raise NegativeAdditiveInfluenceError(
            f"smooth influence on eigenvalue {index} is negative (estimate={estimate}, "
            f"exact={exact}) under a pure-addition overlay — impossible (ΔL is PSD, §2.7); a bug"
        )
