# ── Family: σ-connectivity instruments · the composed graph · docs/NOTATION.md ────────────────────
# OBJECT:    the cross-strata composed graph — EXPLICIT nodes × the edge union E_sim ∪ E_proven
#            (dn-agent-taxonomy §2.2 grounding law), flattened to the SAME adjacency/`sim` surface
#            the existing σ*/conductance math (`core.graph.sigma_star`, `.conductance`) consumes off
#            a `MirrorGraph`, with per-class edge attribution retained (E_sim vs E_proven).
# INVARIANT: pure and dependency-injected — it reads NO store and imports NO harness/View; the union
#            enters at ASSEMBLY, in core (the harness's `MirrorGraph` stays mirror-similarity-only —
#            dn-agent-taxonomy §3 Phase Α). The math is fed UNCHANGED (the surface is MirrorGraph's:
#            `.n`, `.digest(i)`, `.neighbors(i)`, `.sim[i,j]`); a proven edge is present at every
#            similarity threshold (weight ≥ any cosine grid σ), so it can join two σ-components.
# ENFORCED:  guard (tests/unit/test_composed_graph.py) — a sim-only composition reproduces
#            single-class behaviour; a bridge proven edge flips a cross-component σ* from None to a
#            reading; per-class tags survive; the real σ*/conductance functions are called on it.
r"""D3 — the composed-graph assembly (`E_sim ∪ E_proven`) over an explicit node set.

`dn-agent-taxonomy` §2.2 (the grounding law) answers oq-0031's connectivity saturation with a
SECOND, proven edge class: conductance/connectivity are measured over `E_proven ∪ E_sim`, not a
better σ. This module builds exactly that graph — an explicit node set and a union of two edge
classes — and presents it through the surface the σ-connectivity family already consumes off a
`MirrorGraph` (`build_max_spanning_tree`, `sigma_t_profile`, …). The math is fed UNCHANGED: this is
assembly, not new instruments.

**Why not extend `MirrorGraph`.** `core/dreaming/graph.py`'s `MirrorGraph.build` is
mirror-similarity-only by construction (built from a `MirrorView` — authored notes, cosine edges).
The cross-strata union is not a function of the mirror alone, so it cannot live there without
polluting the dreamer's substrate; it enters here, at core-side assembly (the self-containment rule:
math → core). A `ComposedGraph` is a structural stand-in — it exposes `.n`, `.digest(i)`,
`.neighbors(i)`, `.sim` exactly as `MirrorGraph` does, so a caller passes it wherever a
`MirrorGraph` is expected (a localized `cast` bridges the static type; the runtime surface matches).

**The union as a flattened weighted multigraph.** `E_sim` (cosine-weighted pairs) and `E_proven`
(integrator-witnessed pairs, weight 1.0 by default — plan §11) are merged into one symmetric weight
matrix by taking the **max** weight per pair (a proven edge, weight 1.0, dominates any cosine and is
thus present at every grid σ ∈ [0, 1] — it can bridge two similarity components). The per-class
attribution is kept beside the weights (`edge_classes`), so a Δ-phase reading can attribute
connectivity to `E_sim` vs `E_proven` — the falsifier oq-0031 needs. Pure/injected: fixtures in
tests now; real edge sets (sensor nodes, integrator proven edges) in Phase Δ.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np

# The edge-class tags carried in `edge_classes` (the per-class attribution retained through the
# flatten). Named constants so a Δ-phase reading and the tests agree on the strings.
E_SIM = "E_sim"          # cosine-similarity edges (the mirror family's E_sim)
E_PROVEN = "E_proven"    # integrator-witnessed proven edges (dn-agent-taxonomy §2.2 / fiber C)

# A weighted edge: (node-a digest, node-b digest, weight). Weights are cosines for E_sim, the proven
# weight (1.0 default) for E_proven.
WeightedEdge = tuple[str, str, float]

# The default weight of a proven edge when the caller supplies a bare pair (plan §11 parked default:
# weight 1.0 per witnessed edge; Δ-phase calibrates).
PROVEN_WEIGHT: float = 1.0


@dataclass(frozen=True)
class ComposedGraph:
    """An explicit node set × the flattened edge union `E_sim ∪ E_proven`, presenting the
    `MirrorGraph` surface. `sim` is the symmetric max-weight matrix (zero diagonal), `_adj` its
    boolean adjacency (any union edge present), `edge_classes` the per-class attribution keyed by
    the ordered index pair `(i, j)`, `i < j`. Deterministic given the node order."""

    nodes: tuple[str, ...]
    sim: np.ndarray
    _adj: np.ndarray
    edge_classes: dict[tuple[int, int], frozenset[str]]
    sigma: float = 0.0            # informational (the σ context the sim-edges were drawn at); the
    #                              consuming math re-thresholds via its own grid, never reads this.

    # ── the MirrorGraph surface the σ*/conductance math consumes ────────────────────────────────
    @property
    def n(self) -> int:
        return len(self.nodes)

    def digest(self, i: int) -> str:
        return self.nodes[i]

    def neighbors(self, i: int) -> list[int]:
        """Indices j != i joined to i by ANY union edge (E_sim or E_proven) — ascending order,
        matching `MirrorGraph.neighbors`."""
        return [int(j) for j in np.flatnonzero(self._adj[i])]

    # ── the per-class attribution query (the Δ-phase / oq-0031 falsifier) ───────────────────────
    def classes_of(self, a: str, b: str) -> frozenset[str]:
        """The edge classes joining nodes `a` and `b` (a subset of {E_sim, E_proven}); the empty set
        if the pair has no union edge. Order-independent."""
        ia, ib = self.nodes.index(a), self.nodes.index(b)
        return self.edge_classes.get((min(ia, ib), max(ia, ib)), frozenset())


def compose(
    nodes: Iterable[str],
    sim_edges: Iterable[WeightedEdge],
    proven_edges: Iterable[WeightedEdge],
    *,
    sigma: float = 0.0,
) -> ComposedGraph:
    """Assemble a `ComposedGraph` from an explicit node set and the two edge classes. Each edge is a
    `(a, b, weight)` triple over `nodes`; the union is flattened to one symmetric weight matrix by
    the **max** weight per pair (so a proven edge, weight 1.0, dominates and stays present at every
    grid σ). Per-class tags accumulate in `edge_classes` — a pair carried by BOTH classes keeps both
    tags. `sigma` is recorded for provenance only. Raises `KeyError` for an edge naming an unknown
    node and `ValueError` for a self-loop (a node is not a union edge to itself)."""
    node_tuple = tuple(nodes)
    index = {d: i for i, d in enumerate(node_tuple)}
    size = len(node_tuple)
    sim = np.zeros((size, size), dtype=np.float64)
    classes: dict[tuple[int, int], set[str]] = {}

    def _add(a: str, b: str, weight: float, tag: str) -> None:
        ia, ib = index[a], index[b]        # KeyError propagates for an unknown node (fail-closed)
        if ia == ib:
            raise ValueError(f"compose: self-loop on node {a!r} — a node is not an edge to itself")
        key = (min(ia, ib), max(ia, ib))
        w = float(weight)
        sim[ia, ib] = sim[ib, ia] = max(sim[ia, ib], w)   # flatten the multigraph via max weight
        classes.setdefault(key, set()).add(tag)

    for a, b, w in sim_edges:
        _add(a, b, w, E_SIM)
    for a, b, w in proven_edges:
        _add(a, b, w, E_PROVEN)

    adj = (sim > 0.0) & ~np.eye(size, dtype=bool) if size else np.zeros((0, 0), dtype=bool)
    edge_classes = {k: frozenset(v) for k, v in classes.items()}
    return ComposedGraph(
        nodes=node_tuple, sim=sim, _adj=adj, edge_classes=edge_classes, sigma=sigma
    )
