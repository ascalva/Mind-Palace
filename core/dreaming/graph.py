r"""The mirror graph G_MR — the shared substrate every interpreter reads (R0; §6/§8).

Built ONCE from a `MirrorView` (authored-only, Invariant 6 — structural firewall) and handed to
each method-specialist, so the panel computes note centroids + the σ-thresholded adjacency a
single time. Fully deterministic and **model-free** (NumPy cosine only): the §9 deterministic
floor. The graph is $G=(V,E)$ with $E_{\text{sim}}=\{(u,v):\cos\ge\sigma\}$ over note centroids.

This is read-only structure; the interpreters (`interpreters.py`) derive claims from it and the
adjudicator (`adjudicator.py`) ranks them. Nothing here touches a model or the network.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from core.dreaming.cluster import NoteVector, note_centroids, similarity_matrix
from core.kernel.mirror import MirrorView


@dataclass(frozen=True)
class MirrorGraph:
    """Note-level similarity graph over the authored mirror. `sim` is the full cosine matrix;
    edges are pairs with `sim >= sigma`. Deterministic given the MirrorView's row order."""

    notes: tuple[NoteVector, ...]
    sim: np.ndarray
    sigma: float
    _adj: np.ndarray            # boolean adjacency (sim >= sigma, no self-loops)

    @classmethod
    def build(cls, view: MirrorView, *, sigma: float) -> MirrorGraph:
        """π_MR → centroids → σ-adjacency. Input is a `MirrorView`, so the graph is provably
        over authored notes only (a non-authored node is unrepresentable upstream)."""
        notes = tuple(note_centroids(view.rows()))
        sim = similarity_matrix(list(notes))
        n = len(notes)
        adj = (sim >= sigma) & ~np.eye(n, dtype=bool) if n else np.zeros((0, 0), dtype=bool)
        return cls(notes=notes, sim=sim, sigma=sigma, _adj=adj)

    @property
    def n(self) -> int:
        return len(self.notes)

    def digest(self, i: int) -> str:
        return self.notes[i].digest

    def title(self, i: int) -> str:
        return self.notes[i].title

    def neighbors(self, i: int) -> list[int]:
        """Indices j != i with cos(i, j) >= sigma — deterministic ascending order."""
        return [int(j) for j in np.flatnonzero(self._adj[i])]

    def degree(self, i: int) -> int:
        return int(self._adj[i].sum())

    def local_clustering(self, i: int) -> float:
        """Clustering coefficient of node i: fraction of its neighbour pairs that are themselves
        adjacent. LOW clustering at a high-degree node = a structural hole / bridge (Burt): the
        neighbours form separate groups this node holds together. Degree<2 => undefined => 0.0."""
        nb = self.neighbors(i)
        k = len(nb)
        if k < 2:
            return 0.0
        sub = self._adj[np.ix_(nb, nb)]
        edges = int(sub.sum()) // 2                 # symmetric; count unordered pairs
        return edges / (k * (k - 1) / 2)

    def digests_for(self, indices: list[int]) -> tuple[str, ...]:
        """The authored content digests for a set of node indices — the evidence refs (G1)."""
        return tuple(self.notes[i].digest for i in indices)

    def titles_for(self, indices: list[int]) -> tuple[str, ...]:
        return tuple(self.notes[i].title for i in indices)
