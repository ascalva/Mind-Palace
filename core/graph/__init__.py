"""core/graph — the σ-connectivity instruments (dn-core-graph-instruments P2).

The σ/temporal connectivity mathematics over `MirrorGraph` + `Spine`: σ*/MST (`sigma_star`),
the (σ,t) conductance-profile family (`conductance` — lands with bp-065 item 2; bridges and
helix follow on their re-mints). Distinct from `core/complex/` (the ReasoningComplex math) but
built on its primitives — ONE Laplacian (P3). This package imports core substrate and stdlib/
NumPy/SciPy ONLY — never `eval` (the P1 boundary tooth, `tests/unit/test_graph_boundary.py`);
the eval harness imports *us* and keeps the instrument layer (readings, evidence, gates).
"""

from core.graph.sigma_star import (
    ConnIndex,
    CrossingEdgeError,
    MaxSpanningForest,
    SigmaStar,
    acquire_mirror_cut,
    build_max_spanning_tree,
    cut_fingerprint,
    pairwise_sigma_star,
    sigma_star,
)

__all__ = [
    "ConnIndex",
    "CrossingEdgeError",
    "MaxSpanningForest",
    "SigmaStar",
    "acquire_mirror_cut",
    "build_max_spanning_tree",
    "cut_fingerprint",
    "pairwise_sigma_star",
    "sigma_star",
]
