# ── Family: the temporal / citation complex (X_cite) — OUTSIDE core/complex/ (A4, isolation) ──
# OBJECT:    the deterministic, embedder-independent citation complex — 0-cells notes, 1-cells the
#            corpus→corpus citation edges (reference_edges.sqlite), assembled at one commit.
# INVARIANT: read-only (no store write handle); no model, no network; the citation backbone A_cite
#            (E_geom, undirected) is NEVER mixed with the directed supersession D-arrows (E_disp) —
#            a single L₁ over the union is a type error (A5). This module reuses core/complex/hodge
#            (the safe import direction) but NOTHING here ever reaches build_complex / A_signed.
"""The citation complex X_cite — the topological half of dn-temporal-retrieval-algebra §3 (bp-032).

`X_cite` is the flag complex of the doc→doc citation graph read from `ReferenceEdgeStore`
(`direction="corpus_to_corpus"`, bp-026): 0-cells are notes, 1-cells are citation edges, and the
symmetrized binary backbone `A_cite` feeds the degree-1 Hodge machinery UNCHANGED from
`core/complex/hodge` (the note §2.4: "shared mathematics, never shared state"). It is
**embedder-independent by construction** — a deterministic parse of stored references, no embedding
read — which is the hinge of the A7 signal/noise discriminator.

The combinatorial v1 (unweighted) object: `A_cite` is binary (edge or no edge), matching `hodge`'s
v1 inner product; the `(β,z)` weighted retrieval curve is TA-a/bp-034+, out of scope. The directed
supersession D-arrows live in `boundary.py` and are NEVER symmetrized into `A_cite` (A5 — `E_disp`
is acyclic/directed, `E_geom` undirected; a mixed `L₁` conflates incompatible metrics).

Zone A: reads `reference_edges` only, holds no write handle, imports `core/complex/hodge` (the safe
direction — `core/complex/**` never imports THIS module; pinned by test_temporal_isolation.py).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import scipy.sparse as sp

from core.complex.hodge import boundary_1, boundary_2, edge_index, harmonic_basis
from core.stores.reference_edges import ReferenceEdgeStore


@dataclass(frozen=True)
class CitationComplex:
    """The assembled citation complex at one commit — a pure function of the store contents.

    `nodes` is the deterministic 0-cell ordering (sorted note ids); `node_index` maps a note id to
    its row in `A_cite`; `edges` are the 1-cells as `(u, v)` index pairs with `u < v`, sorted;
    `A_cite` is the binary symmetric backbone (csr, zero diagonal) fed to the Hodge machinery."""

    nodes: tuple[str, ...]
    node_index: dict[str, int]
    edges: tuple[tuple[int, int], ...]
    A_cite: sp.csr_matrix

    @property
    def n_nodes(self) -> int:
        return len(self.nodes)

    @property
    def n_edges(self) -> int:
        return len(self.edges)


def build_citation_complex(ref_store: ReferenceEdgeStore, *,
                           commit: str | None = None) -> CitationComplex:
    """Assemble `X_cite` from the doc→doc citation edges — deterministic, run-to-run byte-identical
    on the same store (node/edge ordering is sorted, never dict-iteration-dependent).

    0-cells = the sorted set of note ids appearing as either endpoint of a `corpus_to_corpus` edge;
    1-cells = the undirected, de-duplicated citation pairs (a self-citation `u==u` is dropped — no
    1-cell). `A_cite` is binary (combinatorial v1). Reads only; no store mutation.

    `commit` is the OPTIONAL anchor (dn-core-query-protocol §3 Q2; bp-037/`TemporalView`): edges are
    per-commit (`commit_sha` is part of edge identity — `reference_edges.py`), so `commit=None`
    (default) assembles over the ALL-HISTORY union of citation edges — the original behaviour, kept
    bit-for-bit — while `commit=<sha>` filters to that anchor, giving β₁ "as of" one commit rather
    than a union that can count threads across citations that never co-existed. A pure-Python filter
    over already-read rows: no new import, no store-API change, isolation untouched (§2.4)."""
    citations = ref_store.all(direction="corpus_to_corpus")
    if commit is not None:
        citations = [e for e in citations if e.commit_sha == commit]

    node_set: set[str] = set()
    for e in citations:
        node_set.add(e.source_ref)
        node_set.add(e.target_ref)
    nodes = tuple(sorted(node_set))
    node_index = {name: i for i, name in enumerate(nodes)}

    edge_set: set[tuple[int, int]] = set()
    for e in citations:
        u, v = node_index[e.source_ref], node_index[e.target_ref]
        if u == v:
            continue                                   # a self-citation is not a 1-cell
        edge_set.add((u, v) if u < v else (v, u))      # undirected backbone (A5: E_geom)
    edges = tuple(sorted(edge_set))

    n = len(nodes)
    if edges:
        rows = np.array([u for u, _ in edges] + [v for _, v in edges], dtype=np.int64)
        cols = np.array([v for _, v in edges] + [u for u, _ in edges], dtype=np.int64)
        data = np.ones(2 * len(edges), dtype=np.float64)
        A_cite = sp.csr_matrix((data, (rows, cols)), shape=(n, n))
    else:
        A_cite = sp.csr_matrix((n, n))

    return CitationComplex(nodes=nodes, node_index=node_index, edges=edges, A_cite=A_cite)


def dim_ker_L1(cx: CitationComplex) -> int:
    """β₁ of the citation flag complex — the number of independent citation "threads" (1-cycles not
    bounding a filled 2-simplex), computed as `dim ker L₁` via `hodge.harmonic_basis` (dense SVD
    null space, deterministic; inherits `hodge`'s `_MAX_DENSE_EDGES` guard). The Item-7 falsifier
    cross-checks this against an INDEPENDENT ripser β₁ (`citation_distance_matrix` + ripser)."""
    if cx.n_edges == 0:
        return 0
    return int(harmonic_basis(cx.A_cite).shape[1])


def citation_distance_matrix(cx: CitationComplex) -> np.ndarray:
    """The ripser input for the independent β₁ oracle: a dense distance matrix with `distance = 0`
    on a citation edge, `1` on a non-edge, `0` on the diagonal. Rips at threshold `t = 0` IS the
    flag complex of the (binary) citation graph, so ripser's H₁ alive at `t = 0` equals
    `dim ker L₁` (note §2.4/§2.7 Rule 2). Deterministic, symmetric."""
    n = cx.n_nodes
    D = np.ones((n, n), dtype=np.float64)
    np.fill_diagonal(D, 0.0)
    for u, v in cx.edges:
        D[u, v] = 0.0
        D[v, u] = 0.0
    return D


def flag_boundary_composition_is_zero(cx: CitationComplex) -> bool:
    """`∂₁∂₂ = 0` on `A_cite` — the fundamental chain-complex identity, reused from `hodge` (any
    sign error in the citation backbone's incidence would break it). Confirmed as an Item-6
    acceptance leg alongside the `δ_D² = 0` supersession check in `boundary.py`."""
    d1 = boundary_1(cx.A_cite)
    d2 = boundary_2(cx.A_cite)
    if d2.shape[1] == 0:
        return True                                    # no 2-cells ⇒ trivially zero
    comp = (d1 @ d2).tocoo()
    # edge_index is consumed to keep the reuse honest (same C₁ basis both boundaries key on).
    _ = edge_index(cx.A_cite)
    return bool(np.allclose(comp.data, 0.0))
