"""Signed balance & frustration (companion III §2.3) — rigorous contradiction detection.

A signed graph is **balanced** when its nodes 2-color so every + edge stays within a color and
every − edge crosses — the tensions resolve into two coherent camps. When they can't, there is
**frustration**: irreducible dissonance. Two readings, both exact/cheap and model-free:

  * **global** — λ_min(L̄) of the signed Laplacian is a dissonance proxy: λ_min = 0 ⇔ balanced
    (Hou; Kunegis). It rises as the graph becomes harder to 2-color.
  * **local** — a triangle is frustrated **iff it has an odd number of − edges**; enumerating them
    localizes *which* commitments can't co-hold ("these three can't all be true — you keep circling
    this"). O(#triangles), exact.

This replaces the 0.1 draft's deferred contradiction judge with structure. Deterministic; no model,
no network. The signed adjacency comes from `build_complex` (persisted contradiction edges overlaid
on the similarity backbone); with no contradictions the graph is all-support and trivially balanced.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp

from core.complex.laplacian import signed_laplacian

_DENSE_MAX = 4


def signed_spectrum(A_signed: sp.spmatrix) -> float:
    """λ_min(L̄) — the smallest eigenvalue of the signed Laplacian (global dissonance proxy).
    0 ⇔ the signed graph is balanced; > 0 ⇔ frustration. Deterministic (fixed ARPACK start)."""
    n = A_signed.shape[0]
    if n < 2:
        return 0.0
    L = signed_laplacian(A_signed)
    if n <= _DENSE_MAX:
        vals = np.linalg.eigvalsh(L.toarray())
        return float(max(0.0, vals[0]))          # clamp tiny negative fp noise to 0
    from scipy.sparse.linalg import ArpackNoConvergence, eigsh
    v0 = np.ones(n) / np.sqrt(n)
    try:
        vals = eigsh(L.astype(float), k=1, which="SA", v0=v0, return_eigenvectors=False)
    except ArpackNoConvergence:                  # dense is exact when ARPACK stalls
        vals = np.linalg.eigvalsh(L.toarray())
    return float(max(0.0, vals[0]))


def is_balanced(A_signed: sp.spmatrix, *, tol: float = 1e-8) -> bool:
    """True iff the signed graph is balanced (λ_min(L̄) ≈ 0 within `tol`)."""
    return signed_spectrum(A_signed) <= tol


def frustrated_triangles(A_signed: sp.spmatrix) -> list[tuple[int, int, int]]:
    """Every frustrated triangle (i<j<k with all three edges present and an ODD number of −
    edges) — the specific unresolved tensions. Sorted, deterministic. O(#triangles)."""
    A = A_signed.tocsr()
    n = A.shape[0]
    # neighbor sets and signs (undirected; use upper info symmetrically)
    neighbors: list[set[int]] = [set() for _ in range(n)]
    coo = A.tocoo()
    sign: dict[tuple[int, int], int] = {}
    for i, j, v in zip(coo.row, coo.col, coo.data, strict=True):
        if i == j or v == 0.0:
            continue
        neighbors[i].add(int(j))
        a, b = (int(i), int(j)) if i < j else (int(j), int(i))
        sign[(a, b)] = 1 if v > 0 else -1
    out: list[tuple[int, int, int]] = []
    for i in range(n):
        for j in sorted(x for x in neighbors[i] if x > i):
            for k in sorted(x for x in (neighbors[i] & neighbors[j]) if x > j):
                s = sign[(i, j)] * sign[(j, k)] * sign[(i, k)]
                if s < 0:                        # odd number of negative edges
                    out.append((i, j, k))
    return out


def frustration(A_signed: sp.spmatrix) -> tuple[float, list[tuple[int, int, int]]]:
    """(λ_min(L̄), frustrated_triangles) — the global dissonance proxy plus the localized tensions
    (companion III §2.3 contract). Balanced graph ⇒ (0.0, [])."""
    return signed_spectrum(A_signed), frustrated_triangles(A_signed)
