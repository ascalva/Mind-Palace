"""Property tests for the reasoning complex (H1–H3; companion III §2, BUILD §6.1).

  * Determinism    — a fixed input yields an identical clustering (fixed seed, no RNG leakage).
  * Spectral stability — a small vector perturbation moves cluster labels within a Hamming
    tolerance (a chaotic clusterer would reshuffle memberships).
  * Frustration correctness — a balanced signed graph has λ_min(L̄) ≈ 0 and no frustrated
    triangles; a planted frustrated triangle is enumerated.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp
from hypothesis import given, settings
from hypothesis import strategies as st

from core.complex.spectral import diffusion_cluster_notes
from core.dreaming.cluster import NoteVector
from core.kernel.complex.balance import frustrated_triangles, frustration, signed_spectrum


def _notes(seed: int, n: int, dim: int = 8) -> list[NoteVector]:
    rng = np.random.default_rng(seed)
    return [NoteVector(digest=f"d{i}", title=f"t{i}", vector=tuple(rng.random(dim)))
            for i in range(n)]


def _partition(notes: list[NoteVector]) -> list[tuple[str, ...]]:
    return [tuple(sorted(c.digests))
            for c in diffusion_cluster_notes(notes, threshold=0.5, min_size=2)]


# --- determinism: identical input ⇒ identical clustering -------------------------

@settings(deadline=None, max_examples=30)
@given(seed=st.integers(min_value=0, max_value=2**20), n=st.integers(min_value=2, max_value=24))
def test_diffusion_clustering_is_deterministic(seed, n):
    notes = _notes(seed, n)
    assert _partition(notes) == _partition(notes)          # eigsh (fixed v0) + kmeans (fixed seed)


# --- spectral stability: a small perturbation keeps memberships ------------------

def _clustered_notes() -> list[NoteVector]:
    """Two well-separated blobs in token space: notes 0-5 share bank A, 6-11 share bank B."""
    a = np.array([1.0, 1, 1, 1, 0, 0, 0, 0])
    b = np.array([0.0, 0, 0, 0, 1, 1, 1, 1])
    rng = np.random.default_rng(0)
    out = []
    for i in range(6):
        out.append(NoteVector(f"a{i}", f"a{i}", tuple(a + rng.normal(0, 0.05, 8))))
    for i in range(6):
        out.append(NoteVector(f"b{i}", f"b{i}", tuple(b + rng.normal(0, 0.05, 8))))
    return out


def _membership(notes):
    m: dict[str, frozenset[str]] = {}
    for c in diffusion_cluster_notes(notes, threshold=0.5, min_size=2):
        s = frozenset(c.digests)
        for d in c.digests:
            m[d] = s
    return m


def test_spectral_clustering_is_stable_under_small_perturbation():
    base = _clustered_notes()
    rng = np.random.default_rng(1)
    perturbed = [NoteVector(n.digest, n.title,
                            tuple(np.asarray(n.vector) + rng.normal(0, 1e-3, len(n.vector))))
                 for n in base]
    mb, mp = _membership(base), _membership(perturbed)
    shared = [d for d in mb if d in mp]
    stable = sum(1 for d in shared if mb[d] == mp[d]) / max(len(shared), 1)
    assert stable >= 0.9, f"clusterer is chaotic: only {stable:.0%} of memberships stable"


# --- frustration correctness (companion III §2.3) --------------------------------

def _balanced_signed_graph(colors: list[int], seed: int) -> sp.csr_matrix:
    """Edges between many pairs, signed +1 within a color / −1 across (balanced by construction)."""
    n = len(colors)
    A = np.zeros((n, n))
    rng = np.random.default_rng(seed)
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < 0.6:
                s = 1.0 if colors[i] == colors[j] else -1.0
                A[i, j] = A[j, i] = s
    return sp.csr_matrix(A)


@settings(deadline=None, max_examples=30)
@given(bits=st.lists(st.integers(min_value=0, max_value=1), min_size=4, max_size=10),
       seed=st.integers(min_value=0, max_value=2**16))
def test_balanced_signed_graph_has_no_frustration(bits, seed):
    A = _balanced_signed_graph(bits, seed)
    assert signed_spectrum(A) <= 1e-6            # λ_min(L̄) = 0 ⇔ balanced (Hou/Kunegis)
    assert frustrated_triangles(A) == []         # a 2-colorable graph has no odd-negative triangle


def test_planted_frustrated_triangle_is_enumerated():
    # nodes 0,1,2 form a frustrated triangle (+,+,−); 2,3,4 a clean (+,+,+) triangle.
    A = np.zeros((5, 5))
    for i, j, s in [(0, 1, 1), (1, 2, 1), (0, 2, -1), (2, 3, 1), (3, 4, 1), (2, 4, 1)]:
        A[i, j] = A[j, i] = s
    lam, tris = frustration(sp.csr_matrix(A))
    assert (0, 1, 2) in tris                      # the odd-negative triangle is localized
    assert (2, 3, 4) not in tris                  # the balanced triangle is not
    assert lam > 1e-6                             # global proxy registers the dissonance
