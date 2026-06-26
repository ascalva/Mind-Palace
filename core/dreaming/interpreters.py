"""R0 — the interpreter panel (design-notes/dreaming-v2-interpreter-panel.md; §6/§8).

Generalizes the Phase-7 single clusterer into a REGISTRY of deterministic interpreters — the
"workers", specialists by METHOD (not source). Each is a different lens on the *same* authored
mirror graph and emits candidate pattern-claims plus the authored graph evidence that supports
them:

    φ_i : G_MR → 2^K,   κ = (statement, support ⊆ authored notes)

All are model-free (NumPy over the σ-graph) — the §9 deterministic floor; the model is earned
only for narration/judging, which R0 does NOT do. No adjudication here (that is R1): R0 just
produces the raw claims. Inputs are a `MirrorView`, so every claim's support is authored
(Invariant 6, structural) — observed exhaust can never seed a claim.

Interpreters today: community (connected components), centrality (degree hubs), bridge
(structural holes), density (cores + explicit noise). Change-point is a registered but DEFERRED
seam — it needs a per-note temporal axis the MirrorView does not yet carry, so it returns
nothing rather than fake a trend (the honest-seam pattern, like the §4 judge / contradiction
detector). The registry is the extension point: a modularity community method (Leiden/Louvain),
once it can be done dependency-free in the sealed core, is a drop-in.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from config.loader import Config, DreamRnDConfig
from core.dreaming.cluster import cluster_notes
from core.dreaming.graph import MirrorGraph
from core.dreaming.rnd import require_rnd_enabled
from core.mirror import MirrorView

# Method names (the discriminator carried on every claim).
COMMUNITY = "community"
CENTRALITY = "centrality"
BRIDGE = "bridge"
DENSITY = "density"
CHANGE_POINT = "change_point"   # deferred seam


@dataclass(frozen=True)
class Claim:
    """A candidate pattern-claim from one interpreter. `support` is the set of authored note
    digests the claim rests on — content-addressed evidence (G1), and the LEAVES that ground it
    (G2). `data` is method-specific. No confidence here; ranking is the adjudicator's job (R1)."""

    method: str
    statement: str
    support: tuple[str, ...]
    data: dict = field(default_factory=dict)


# An interpreter is a deterministic map from the mirror graph (+ tunables) to claims.
Interpreter = Callable[[MirrorGraph, DreamRnDConfig], "list[Claim]"]


def community_interpreter(graph: MirrorGraph, cfg: DreamRnDConfig) -> list[Claim]:
    """Connected components over the σ-graph — thematic groups (the Phase-7 lens, as one of
    many). Each component of >=2 notes is a theme; support = the component's notes."""
    clusters = cluster_notes(list(graph.notes), threshold=cfg.sigma, min_size=2)
    return [
        Claim(method=COMMUNITY,
              statement=f"{c.size} notes group into a theme",
              support=c.digests,
              data={"size": c.size})
        for c in clusters
    ]


def centrality_interpreter(graph: MirrorGraph, cfg: DreamRnDConfig) -> list[Claim]:
    """Degree centrality — which notes are load-bearing hubs. The top-k highest-degree notes
    (degree >= min_degree); support = the hub plus the notes it links."""
    ranked = sorted(range(graph.n), key=lambda i: (-graph.degree(i), graph.title(i)))
    claims: list[Claim] = []
    for i in ranked[: cfg.centrality_top_k]:
        deg = graph.degree(i)
        if deg < cfg.min_degree:
            break                      # ranked desc — once below the floor, all the rest are too
        support = graph.digests_for([i, *graph.neighbors(i)])
        claims.append(Claim(
            method=CENTRALITY,
            statement=f"'{graph.title(i)}' is a hub linking {deg} related notes",
            support=support,
            data={"degree": deg, "focus": graph.digest(i)},
        ))
    return claims


def bridge_interpreter(graph: MirrorGraph, cfg: DreamRnDConfig) -> list[Claim]:
    """Structural holes (Burt): a node of degree>=2 whose neighbours are poorly connected to
    each other (local clustering <= ceiling) holds otherwise-separate notes together. Support =
    the bridge plus what it connects. Deterministic; no community partition required."""
    claims: list[Claim] = []
    for i in range(graph.n):
        if graph.degree(i) < 2:
            continue
        clustering = graph.local_clustering(i)
        if clustering <= cfg.bridge_clustering_max:
            support = graph.digests_for([i, *graph.neighbors(i)])
            claims.append(Claim(
                method=BRIDGE,
                statement=(f"'{graph.title(i)}' bridges otherwise-separate notes "
                           f"(clustering {clustering:.2f})"),
                support=support,
                data={"clustering": round(clustering, 4), "degree": graph.degree(i),
                      "focus": graph.digest(i)},
            ))
    return claims


def density_interpreter(graph: MirrorGraph, cfg: DreamRnDConfig) -> list[Claim]:
    """Density split (the HDBSCAN-style contribution): notes with >= min_degree neighbours are
    'core'; notes with no σ-neighbour are explicit NOISE/outliers. Emits a core-region claim
    and, distinctively, an outliers claim — the signal the connected-components lens hides."""
    cores = [i for i in range(graph.n) if graph.degree(i) >= cfg.min_degree]
    noise = [i for i in range(graph.n) if graph.degree(i) == 0]
    claims: list[Claim] = []
    if len(cores) >= 2:
        claims.append(Claim(
            method=DENSITY,
            statement=f"a dense region of {len(cores)} closely-related notes",
            support=graph.digests_for(cores),
            data={"core_count": len(cores)},
        ))
    if noise:
        claims.append(Claim(
            method=DENSITY,
            statement=f"{len(noise)} note(s) stand apart from any theme (outliers)",
            support=graph.digests_for(noise),
            data={"outlier_count": len(noise)},
        ))
    return claims


def change_point_interpreter(graph: MirrorGraph, cfg: DreamRnDConfig) -> list[Claim]:
    """DEFERRED seam: temporal change-point detection needs a per-note timestamp, which the
    MirrorView does not yet carry. Returns nothing rather than fabricate a trend — the same
    honest-seam discipline as the §4 judge and the contradiction detector. Wire it when an
    authored temporal axis lands on the mirror rows."""
    return []


# The registry — the panel. Order is the run order; the adjudicator re-ranks by confidence.
INTERPRETERS: dict[str, Interpreter] = {
    COMMUNITY: community_interpreter,
    CENTRALITY: centrality_interpreter,
    BRIDGE: bridge_interpreter,
    DENSITY: density_interpreter,
    CHANGE_POINT: change_point_interpreter,
}


def run_panel(view: MirrorView, *, config: Config | None = None) -> list[Claim]:
    """Run every registered interpreter over the mirror graph and return all candidate claims
    (R0 — no adjudication). Refuses unless the R&D flag is on (hard boundary)."""
    cfg = require_rnd_enabled(config)
    graph = MirrorGraph.build(view, sigma=cfg.sigma)
    claims: list[Claim] = []
    for interpret in INTERPRETERS.values():
        claims.extend(interpret(graph, cfg))
    return claims
