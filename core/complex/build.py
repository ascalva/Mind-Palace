"""build_complex(view) — assemble the reasoning complex 𝔎 from a MirrorView (companion III §1).

The *object* the strong Dreamer reasons over, regenerated per trough pass (never a long-lived
global, §1.3):

  * **nodes** — one per authored note (its digest), from a `MirrorView` only, so a non-authored
    complex is unrepresentable (Invariant 6, structural firewall — the constructor's type IS the
    proof);
  * **A** — the weighted similarity backbone (cosine over note centroids, negatives/self zeroed);
  * **A_signed** — the signed adjacency: A with polarity overlaid from any persisted typed edges
    (`EdgeStore`; contradiction ⇒ −w). With no persisted edges it equals A (pure support), so the
    similarity backbone is a balanced signed graph until a contradiction is asserted;
  * **hyper** — the derivation B-arcs (tail set → head) touching these nodes, from the
    `DerivedStore` junction (companion III §1.3); empty for a pure authored view.

Deterministic (fixed embeddings ⇒ fixed graph), model-free, Zone A (no network).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np
import scipy.sparse as sp

from core.mirror import MirrorView
from core.provenance import Provenance

if TYPE_CHECKING:  # annotation-only; the runtime import is lazy (see build_complex) to break
    from core.dreaming.cluster import NoteVector  # the package-init cycle with core.dreaming

# Stable provenance → integer layer code (companion III §1.1: layers are provenance strata).
_LAYER_CODE = {p.value: i for i, p in enumerate(Provenance)}


@dataclass(frozen=True)
class ReasoningComplex:
    """𝔎|_MR — the introspective reasoning complex over authored notes (companion III §1.5).

    A small immutable snapshot: the node list + index, the weighted (`A`) and signed (`A_signed`)
    adjacencies, the derivation hyperedges, and per-node layer/creation arrays for §5.4 temporal
    tracking. Assembled by `build_complex` from a `MirrorView`; the Laplacian/spectral/balance
    modules consume it. Never mutated — a fresh pass rebuilds it (regenerable)."""

    nodes: tuple[str, ...]                     # authored note digests, MirrorView-filtered
    idx: dict[str, int]                        # digest -> matrix index
    A: sp.csr_matrix                           # weighted similarity backbone (w >= 0, sym, 0 diag)
    A_signed: sp.csr_matrix                    # signed adjacency (+w support / -w contradiction)
    hyper: tuple[tuple[frozenset[str], str], ...]  # derivation B-arcs (tail set, head)
    layers: np.ndarray                         # provenance code per node
    created: np.ndarray                        # creation timestamp (epoch float) per node
    titles: dict[str, str] = field(default_factory=dict)  # digest -> title (convenience, not spec)

    @property
    def n(self) -> int:
        return len(self.nodes)


def cosine_adjacency(vectors: np.ndarray, *, sim_floor: float = 0.0) -> sp.csr_matrix:
    """Weighted cosine-similarity adjacency: symmetric, zero diagonal, negatives clamped to 0,
    and entries below `sim_floor` dropped (denoising). Zero vectors sit at the origin (no edges).

    The similarity backbone A (companion III §2.2). Deterministic. For the lexical/semantic
    embeddings the Dreamer uses, orthogonal notes have 0 cosine, so A is naturally sparse."""
    if vectors.shape[0] == 0:
        return sp.csr_matrix((0, 0))
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0.0] = 1.0
    unit = vectors / norms
    sim = unit @ unit.T
    np.fill_diagonal(sim, 0.0)
    sim[sim < max(sim_floor, 0.0)] = 0.0
    sim[sim < 0.0] = 0.0                        # cosine can be negative; the backbone is w >= 0
    sim = np.maximum(sim, sim.T)                # exact symmetry (guard fp asymmetry)
    return sp.csr_matrix(sim)


def _note_matrix(notes: list[NoteVector]) -> np.ndarray:
    if not notes:
        return np.zeros((0, 0))
    return np.asarray([n.vector for n in notes], dtype=np.float64)


def _created_epoch(rows: list[dict], nodes: tuple[str, ...]) -> np.ndarray:
    """Per-node creation time (epoch seconds) for the §5.4 temporal index; 0.0 when unknown."""
    from datetime import datetime
    seen: dict[str, float] = {}
    for r in rows:
        d = r.get("digest")
        if d in seen:
            continue
        ts = r.get("created_at") or r.get("timestamp") or r.get("created")
        val = 0.0
        if isinstance(ts, int | float):
            val = float(ts)
        elif isinstance(ts, str) and ts:
            try:
                val = datetime.fromisoformat(ts).timestamp()
            except ValueError:
                val = 0.0
        seen[d] = val
    return np.asarray([seen.get(d, 0.0) for d in nodes], dtype=np.float64)


def build_complex(view: MirrorView, *, edges=None, derived=None,
                  sim_floor: float = 0.0) -> ReasoningComplex:
    """Assemble 𝔎|_MR from a `MirrorView` (Invariant 6: authored-only is structural — the input
    type cannot hold a non-authored row).

    `edges` (optional `EdgeStore`): persisted typed/signed edges overlaid onto A_signed, so an
    asserted contradiction flips a pair's polarity to −w. `derived` (optional `DerivedStore`): the
    derivation hyperedges whose tails touch these authored nodes. Both default None (pure
    similarity backbone, no hyperedges), keeping the introspective pass self-contained."""
    # Lazy: core.dreaming's eager __init__ imports the panel, which imports core.complex —
    # importing its cluster module at OUR module load would close that cycle. The dependency
    # direction is panel → instruments; this keeps the instruments importable standalone.
    from core.dreaming.cluster import note_centroids

    rows = view.rows()
    notes = note_centroids(rows)
    nodes = tuple(nv.digest for nv in notes)
    idx = {d: i for i, d in enumerate(nodes)}
    titles = {nv.digest: nv.title for nv in notes}

    A = cosine_adjacency(_note_matrix(notes), sim_floor=sim_floor)
    A_signed = _overlay_signed(A, idx, edges)
    hyper = _hyperedges_touching(nodes, derived)

    prov_by_digest = {r["digest"]: r.get("provenance", "") for r in rows}
    layers = np.asarray([_LAYER_CODE.get(prov_by_digest.get(d, ""), -1) for d in nodes],
                        dtype=np.int64)
    created = _created_epoch(rows, nodes)

    return ReasoningComplex(nodes=nodes, idx=idx, A=A, A_signed=A_signed, hyper=hyper,
                            layers=layers, created=created, titles=titles)


def _overlay_signed(A: sp.csr_matrix, idx: dict[str, int], edges) -> sp.csr_matrix:
    """A_signed = A (all support) with any persisted typed edges overlaid: an edge (u,v) present in
    the store sets the pair to sign·w (contradiction ⇒ −w). Both endpoints must be nodes here."""
    if edges is None or A.shape[0] == 0:
        return A.copy()
    signed = A.tolil()
    for e in edges.all():
        i, j = idx.get(e.u), idx.get(e.v)
        if i is None or j is None:
            continue
        val = float(int(e.sign)) * float(e.w)
        signed[i, j] = val
        signed[j, i] = val
    return signed.tocsr()


def _hyperedges_touching(nodes: tuple[str, ...], derived) -> tuple[tuple[frozenset[str], str], ...]:
    """Derivation B-arcs (tail set, head) whose tail set intersects these authored nodes."""
    if derived is None:
        return ()
    node_set = set(nodes)
    out = []
    for he in derived.hyperedges():
        tails = he.tails & node_set
        if tails:
            out.append((frozenset(tails), he.head))
    return tuple(out)
