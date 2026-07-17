r"""CN-2: σ*, the abstraction ultrametric, via one maximum spanning tree per certified cut.

The keystone of the connectivity-instruments family (`docs/design-notes/connectivity-instruments.md`
CN-1 + CN-2; RATIFIED — math held verbatim, never re-derived here). A derived-tier, read-only,
**model-free** instrument: NumPy cosine + a union-find MST, no model import, no LLM call. It reads a
`MirrorView` (Invariant-6 authored-only firewall) and a certified cut, and writes only new keyed
readings into the eval store.

**σ* — the abstraction ultrametric (CN-2).** `σ*(A,B) = sup{σ : A ∼ B in G_σ(cut)}` — the strictest
abstraction threshold at which two thoughts still share a component. It is the single-linkage /
maximin-cosine path value, and **one maximum spanning tree over the loosest-grid graph yields all
pairwise σ* and the realizing chain** (the bottleneck edge of the unique MST path). σ* is
**grid-relative** (the fibers discipline): computed against the declared σ-grid, the MST built at
the loosest grid threshold `min(grid)`, the grid pinned in every reading's evidence; a pair
unconnected there reports **"not connected within grid"** (`sigma_star=None`) — an honest bounded
answer, never an extrapolation.

**The CN-1 index discipline.** Every instrument in this family is indexed by a point in (σ, t, cut)
space and DECLARES which axes it uses. σ* uses **(σ-grid, cut)** — no walk, hence no t. The cut is
the corpus-history coordinate; "the graph at a moment" exists only at a **certified** cut (GC-3),
and wall-clock indexes nothing (Law C4 — this module reads no clock, stamps no time). `ConnIndex`
and `ConnEvidence` are the shared scaffolding bp-060 (conductance) / bp-061 (bridges) / bp-062
(helix) import; get their surface right — it is load-bearing for the family.

**The cut gap (cross-reference-on-extension, plan §4 — NOT a correction).** `MirrorGraph.build`
(`core/dreaming/graph.py`) takes **no cut**; `MirrorView` has **no downset/at-cut surface**. The
dreamer never needed a cut, so this is not a bug there. This family *supplies* the cut index
externally: v1 builds the graph over the CURRENT `MirrorView` and records the LATEST certified cut
(`spine.cut_at(strata=frozenset({"mirror"}))`) in `ConnEvidence` as its history coordinate.
Historical / cut-restricted graphs are PARKED (plan §11): a future `core/` plan adding a
`MirrorView` downset filter, with its own warrant — never a mid-build core edit here.

**Registration (fibers precedent, plan §4).** `EvalResultsStore.put()` does NOT gate on
registration (`store.py` imports no registry), and `registry.py` is out of this plan's write_scope.
So — exactly as FB-1 wrote `sigma_persistence.*` before bp-054 registered them (`fibers.py`
head-note) — this instrument emits `sigma_star.*` readings with `type_tag="SigmaStar"` now;
registering the names + the tag vocabulary is a separate future act (a bp-054-style companion).
Recorded here so it never reads as a violation.

**Not a recall signal (finding-0096).** σ* reports thresholds + chains; it does NOT feed
golden_recall or claim a σ-discriminating recall improvement. finding-0096 established golden_recall
saturates at this corpus scale — σ*'s falsifiers are the ultrametric inequality and MST≡union-find
agreement, both scale-free STRUCTURAL checks, never a recall booster.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass, field
from statistics import mean, median

from core.dreaming.graph import MirrorGraph
from core.mirror import MirrorView
from core.temporal.spine import CertifiedCut, Spine
from eval.harness.store import EvalKey, EvalResultsStore, Reading

# --- family constants ---------------------------------------------------------------------------
_INSTRUMENT = "connectivity/v1"           # the spec_hash instrument tag (id + version)
_TYPE_TAG = "SigmaStar"                    # the result-typing tag (unregistered; see head-note)
_MIRROR_STRATUM = frozenset({"mirror"})    # σ* cuts the mirror stratum (versions/catalog → COMMIT)

# The grid-snap tolerance: a raw bottleneck cosine that equals a grid point up to float noise must
# snap TO that point, not to the one below it. Cosines and grid values are both float64.
_SNAP_EPS = 1e-12

# The aggregate metric names (σ* distribution over the pairwise summary). Unregistered by design
# (see head-note); a bp-054-style companion registers them later.
METRIC_MEAN = "sigma_star.mean"
METRIC_P50 = "sigma_star.p50"
METRIC_MAX = "sigma_star.max"
METRIC_FRAC_CONNECTED = "sigma_star.frac_connected"
METRIC_N_PAIRS = "sigma_star.n_pairs"


class CrossingEdgeError(RuntimeError):
    """The acquired cut has crossing generator edges (`spine.crossing_edges(cut) != []`) — an event
    inside the down-set reading from one outside it. The cut is not sound; refuse (the CN-1 legality
    tooth, plan §7 item-1). Never emit a reading at an unsound cut (fail-closed)."""


# ── the CN-1 index object + the family evidence pin ─────────────────────────────────────────────


@dataclass(frozen=True)
class ConnIndex:
    """The CN-1 connectivity index — the coordinate every reading in this family carries. Each
    instrument declares WHICH of (σ-grid, t, cut) it uses; **σ* uses (grid, cut) — no t** (no walk).
    Shared scaffolding: bp-060/061/062 reuse this object and the latest-cut acquisition below."""

    grid: tuple[float, ...]            # the declared σ-grid (ascending; loosest = grid[0])
    cut: CertifiedCut                  # the corpus-history coordinate (latest certified cut, v1)


@dataclass(frozen=True)
class ConnEvidence:
    """The reconstruction pins recorded in every reading's `evidence_ref` (the `FibersEvidence`
    pattern, copied verbatim): the declared grid, the caller's base fingerprint (config/embedding
    regime), and the certified cut's content fingerprint. Serialized so the number stays
    independently recoverable and a later grid / cut drift is detectable."""

    grid: tuple[float, ...]
    base_fingerprint: str
    cut_fingerprint: str

    def as_ref(self) -> str:
        return json.dumps(
            {
                "instrument": _INSTRUMENT,
                "grid": list(self.grid),
                "base_fingerprint": self.base_fingerprint,
                "cut_fingerprint": self.cut_fingerprint,
            },
            sort_keys=True,
            separators=(",", ":"),
        )


@dataclass(frozen=True)
class SigmaStar:
    """One pair's σ* reading. `sigma_star` is the **grid-snapped** bottleneck cosine (the largest
    grid σ ≤ the maximin-path bottleneck), or **None** ⇒ "not connected within grid" (the pair's
    components split at the loosest grid threshold). `chain` is the realizing MST path (note
    digests, A→B inclusive); `()` when unconnected."""

    a: str
    b: str
    sigma_star: float | None
    chain: tuple[str, ...]


# ── the maximum spanning forest (CN-2) ──────────────────────────────────────────────────────────


@dataclass(frozen=True)
class MaxSpanningForest:
    """The maximum spanning tree of the loosest-grid graph — a FOREST when that graph is
    disconnected (one tree per component). `tree_adj[i]` are node i's tree neighbours with the edge
    cosine; `component[i]` is i's component root (equal roots ⇔ a maximin path exists ⇔ σ* is not
    None). Built ONCE (Kruskal, O(E log V)); per-pair σ* walks the prebuilt tree — never re-searches
    the MST (plan §7 item-2 invariant)."""

    digests: tuple[str, ...]                      # node index -> content digest
    index_of: dict[str, int]                      # digest -> node index
    tree_adj: dict[int, list[tuple[int, float]]]  # node -> [(tree-neighbour, edge cosine)]
    component: tuple[int, ...]                     # node -> component root id


def build_max_spanning_tree(graph: MirrorGraph) -> MaxSpanningForest:
    """One maximum spanning tree over the graph's σ-adjacency (built at the loosest grid threshold —
    the caller passes `MirrorGraph.build(view, sigma=min(grid))`). Edges are the pairs `graph`
    admits at its σ (`graph.neighbors`), weighted by the cosine `graph.sim[i,j]`; Kruskal
    descending on weight (ties broken by `(i, j)` for determinism) yields the maximum spanning
    FOREST. O(E log V) — built once; `sim`/`_adj` are never mutated."""
    n = graph.n
    digests = tuple(graph.digest(i) for i in range(n))
    index_of = {d: i for i, d in enumerate(digests)}
    # Distinct undirected edges present at graph.sigma, weighted by cosine.
    edges: list[tuple[float, int, int]] = []
    for i in range(n):
        for j in graph.neighbors(i):
            if j > i:
                edges.append((float(graph.sim[i, j]), i, j))
    edges.sort(key=lambda e: (-e[0], e[1], e[2]))     # descending weight, deterministic tie-break

    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    tree_adj: dict[int, list[tuple[int, float]]] = {i: [] for i in range(n)}
    for w, i, j in edges:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[max(ri, rj)] = min(ri, rj)
            tree_adj[i].append((j, w))
            tree_adj[j].append((i, w))
    component = tuple(find(x) for x in range(n))
    return MaxSpanningForest(
        digests=digests, index_of=index_of, tree_adj=tree_adj, component=component
    )


def _tree_path_bottleneck(
    forest: MaxSpanningForest, ia: int, ib: int
) -> tuple[list[int], float] | None:
    """The unique tree path `ia → ib` and its **bottleneck** (minimum edge cosine along it), or
    None if the two nodes are in different components (no maximin path within the loosest grid). A
    DFS over the prebuilt tree adjacency — O(V), no MST re-search."""
    if forest.component[ia] != forest.component[ib]:
        return None
    # DFS from ia, recording each node's parent AND the cosine of the edge to that parent, so the
    # path and its bottleneck reconstruct in O(V) without a separate weight lookup.
    prev: dict[int, int] = {ia: ia}
    pw: dict[int, float] = {ia: float("inf")}          # edge cosine to parent (ia has none)
    stack = [ia]
    while stack:
        u = stack.pop()
        if u == ib:
            break
        for v, w in forest.tree_adj[u]:
            if v not in prev:
                prev[v] = u
                pw[v] = w
                stack.append(v)
    # Reconstruct the path ib → ia, then reverse; the bottleneck is the min edge cosine on it.
    path: list[int] = [ib]
    while path[-1] != ia:
        path.append(prev[path[-1]])
    bottleneck = min(pw[node] for node in path[:-1])   # every node except ia carries a parent edge
    path.reverse()
    return path, float(bottleneck)


def _grid_snap(value: float, grid: Sequence[float]) -> float:
    """The largest grid σ ≤ `value` (grid-relativity: σ* is snapped to the declared grid, never
    extrapolated). `value` is a raw path-bottleneck cosine ≥ grid[0] for any connected pair, so the
    result is always ≥ grid[0]. A small tolerance keeps a bottleneck that equals a grid point from
    snapping to the point below it under float noise."""
    snapped = grid[0]
    for g in grid:
        if g <= value + _SNAP_EPS:
            snapped = g
        else:
            break
    return float(snapped)


def sigma_star(
    forest: MaxSpanningForest, a: str, b: str, *, grid: Sequence[float]
) -> SigmaStar:
    """`σ*(A,B)` and its realizing MST chain, read off the prebuilt forest. Grid-snapped bottleneck
    + the tree path (digests, A→B inclusive) for a connected pair; `sigma_star=None, chain=()` for a
    pair whose components split at the loosest grid ("not connected within grid")."""
    ia, ib = forest.index_of[a], forest.index_of[b]
    walked = _tree_path_bottleneck(forest, ia, ib)
    if walked is None:
        return SigmaStar(a=a, b=b, sigma_star=None, chain=())
    path, bottleneck = walked
    chain = tuple(forest.digests[k] for k in path)
    return SigmaStar(a=a, b=b, sigma_star=_grid_snap(bottleneck, grid), chain=chain)


# ── the cut acquisition + evidence pins (CN-1) ──────────────────────────────────────────────────


def cut_fingerprint(cut: CertifiedCut) -> str:
    """A deterministic content hash of the certified cut — its frontier, the certificates it
    composed, and their evidence (the sourced observables, never wall-time). Rides in `ConnEvidence`
    so the history coordinate a reading measured stays independently recoverable and cut drift is
    detectable."""
    payload = json.dumps(
        {
            "frontier": [list(pair) for pair in cut.frontier],
            "certificates": sorted(c.value for c in cut.certificates),
            "evidence": list(cut.evidence),
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def acquire_mirror_cut(spine: Spine) -> CertifiedCut:
    """The latest certified cut over the mirror stratum — the family's history coordinate (v1). Lets
    `CutCertificateError` propagate (fail-closed: a cut with no COMMIT certificate REFUSES; we never
    fabricate one). Asserts the CN-1 legality tooth (`crossing_edges == []`): an unsound cut raises
    `CrossingEdgeError`, never emits a reading."""
    cut = spine.cut_at(strata=_MIRROR_STRATUM)
    crossings = spine.crossing_edges(cut)
    if crossings:
        raise CrossingEdgeError(
            f"the acquired mirror cut has {len(crossings)} crossing generator edge(s) "
            f"{crossings[:3]}… — an event inside the down-set reads from one outside it, so the "
            "cut is not sound (CN-1 legality tooth). Refusing to emit a reading at an unsound cut."
        )
    return cut


def _corpus_ref(forest: MaxSpanningForest) -> str:
    """The corpus coordinate (the store's corpus-growth confound key): a content digest of the node
    set the reading measured. Deterministic — the sorted note digests hashed. Distinct corpora key
    distinctly; the same notes re-read key identically (idempotent-by-key writes)."""
    payload = "‖".join(sorted(forest.digests))
    return "conn:" + hashlib.sha256(payload.encode()).hexdigest()


def _spec_hash(grid: Sequence[float]) -> str:
    """`spec_hash = sha256(instrument ‖ grid-descriptor)` — instrument id+version, then the
    declared grid (the battery param, `store.py:32`). A different grid keys DISTINCTLY (the Res(π)
    discipline — comparisons across unacknowledged rulers cannot collapse)."""
    descriptor = json.dumps({"grid": list(grid)}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(f"{_INSTRUMENT}‖{descriptor}".encode()).hexdigest()


# ── the entry point + the pairwise summary + readings (item 3) ──────────────────────────────────


@dataclass
class ConnResult:
    """The instrument's verdict. `index` is the CN-1 (grid, cut) coordinate; `evidence` the pins;
    the `pairs` are the full pairwise σ* summary (report artifact); `aggregates` the distribution
    readings written; `readings_written` counts NEW eval-store rows (a re-run yields 0 — the store
    dedups by key). `notes` records every coverage gap (no silent caps)."""

    index: ConnIndex
    evidence: ConnEvidence
    corpus_ref: str
    spec_hash: str
    pairs: tuple[SigmaStar, ...]
    aggregates: dict[str, float]
    readings_written: int
    notes: tuple[str, ...] = field(default_factory=tuple)


def _aggregate(pairs: Sequence[SigmaStar]) -> tuple[dict[str, float], tuple[str, ...]]:
    """The σ* distribution summary over the pairwise readings. mean/p50/max are over CONNECTED pairs
    only (σ* not None); `frac_connected` and `n_pairs` are always present. Returns (aggregates,
    coverage-notes)."""
    connected = [p.sigma_star for p in pairs if p.sigma_star is not None]
    notes: list[str] = []
    agg: dict[str, float] = {
        METRIC_N_PAIRS: float(len(pairs)),
        METRIC_FRAC_CONNECTED: (len(connected) / len(pairs)) if pairs else 0.0,
    }
    if connected:
        agg[METRIC_MEAN] = float(mean(connected))
        agg[METRIC_P50] = float(median(connected))
        agg[METRIC_MAX] = float(max(connected))
    else:
        notes.append(
            "no pair connects within the grid — mean/p50/max omitted "
            "(only frac_connected=0 + n_pairs written)."
        )
    return agg, tuple(notes)


def pairwise_sigma_star(
    forest: MaxSpanningForest, *, grid: Sequence[float]
) -> tuple[SigmaStar, ...]:
    """Every distinct pair's σ*, read off the single prebuilt forest (strongest first, id-stable).
    O(V²) tree walks over ONE MST — no per-pair MST re-search (plan §7 item-2 invariant)."""
    digests = forest.digests
    out = [
        sigma_star(forest, digests[i], digests[j], grid=grid)
        for i in range(len(digests))
        for j in range(i + 1, len(digests))
    ]
    out.sort(key=lambda s: (s.sigma_star is not None, s.sigma_star or 0.0, s.a, s.b), reverse=True)
    return tuple(out)


def run_connectivity(
    *,
    view: MirrorView,
    spine: Spine,
    grid: Sequence[float],
    eval_store: EvalResultsStore,
    base_fingerprint: str,
) -> ConnResult:
    """Build the σ-graph over the CURRENT MirrorView at the loosest grid threshold, acquire the
    latest certified mirror cut (fail-closed), compute the pairwise σ* summary, and write the
    aggregate readings keyed with the `ConnEvidence` ref. Reads only the view + spine; writes only
    additive, idempotent-by-key eval Readings (never re-keys, never overwrites). n≤1 corpora emit
    no readings and note it (a sanctioned empty outcome, plan §10)."""
    grid = tuple(sorted(float(g) for g in grid))
    if not grid:
        raise ValueError("run_connectivity: empty σ-grid — an instrument must declare its grid")

    cut = acquire_mirror_cut(spine)                       # fail-closed BEFORE any graph work
    evidence = ConnEvidence(
        grid=grid, base_fingerprint=base_fingerprint, cut_fingerprint=cut_fingerprint(cut)
    )
    index = ConnIndex(grid=grid, cut=cut)

    graph = MirrorGraph.build(view, sigma=grid[0])        # loosest grid = densest edges
    if graph.n <= 1:
        return ConnResult(
            index=index, evidence=evidence,
            corpus_ref=_corpus_ref(build_max_spanning_tree(graph)),
            spec_hash=_spec_hash(grid), pairs=(), aggregates={}, readings_written=0,
            notes=(f"corpus n={graph.n} ≤ 1: no pairs — no readings emitted (plan §10).",),
        )

    forest = build_max_spanning_tree(graph)
    pairs = pairwise_sigma_star(forest, grid=grid)
    aggregates, agg_notes = _aggregate(pairs)
    corpus_ref = _corpus_ref(forest)
    spec_hash = _spec_hash(grid)

    key = EvalKey(spec_hash=spec_hash, corpus_ref=corpus_ref,
                  config_fingerprint=base_fingerprint, seed=0)
    ref = evidence.as_ref()
    written = 0
    for name, value in aggregates.items():
        if eval_store.put(
            Reading(key=key, metric_name=name, value=float(value),
                    type_tag=_TYPE_TAG, evidence_ref=ref)
        ):
            written += 1

    return ConnResult(
        index=index, evidence=evidence, corpus_ref=corpus_ref, spec_hash=spec_hash,
        pairs=pairs, aggregates=aggregates, readings_written=written, notes=agg_notes,
    )
