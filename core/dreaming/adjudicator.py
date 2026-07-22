"""R1 — the evidence-based adjudicator (design-notes/dreaming-v2-interpreter-panel.md; §6/§8).

Ranks the panel's competing claims and logs a **confidence-ordered dream log**, each entry
carrying content-addressed authored evidence. The load-bearing rule: **evidence, not
persuasion**. The currency is *resolvable grounding* (`core.selfcheck.grounding_score`), never
rhetoric — no model scores argument quality here, so the most eloquent claim cannot win.

Confidence of a group κ (the single clamped definition, `core.recursion.claim_confidence`):

    c(κ) = min{1, γ^{d(κ)} · g(κ) · (1 + λ(|Agr(κ)| − 1))}

where g(κ) is the authored-grounding score (the gate: g=0 ⇒ c=0, so agreement can never
*manufacture* confidence from nothing — agreement is a **multiplier, not a vote**), |Agr(κ)| is
the number of DISTINCT interpreters that corroborate the claim, λ is the bounded corroboration
bonus (`core.recursion.DEFAULT_LAMBDA`), and γ^d is the recursion decay (`DEFAULT_GAMMA`).
d(κ)=1 here: every claim's support is authored leaves (R0 reads a MirrorView), so the chain
terminates in authored ground (Invariant 10) and depth is uniform — γ^d is order-preserving and
present for honesty (a first-order interpretation is γ·g, explicitly a hypothesis) and for R3
readiness. **Confidence is NOT a probability and never combined with utility** (a separate axis,
R2): `c` decides what to *believe*, utility decides what to *surface*; one scalar is forbidden.

Output is stored INTERPRETED-only (`DerivedStore`, no provenance parameter — structural §8) with
`derived_from` = the authored evidence digests (acyclic, depth-1 — G2). Reproducible and
tamper-evident: a dream log entry is pinned to sha256 evidence refs.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from core.dreaming.interpreters import Claim, run_panel
from core.dreaming.rnd import require_rnd_enabled
from core.kernel.config import Config, get_config
from core.kernel.mirror import MirrorView
from core.kernel.recursion import DEFAULT_GAMMA, DEFAULT_LAMBDA, claim_confidence
from core.kernel.selfcheck import grounding_score
from core.stores.derived import DREAM_LOG, DerivedStore

# All R0/R1 claims rest directly on authored leaves, so the derivation depth is 1 (an
# interpretation of ground truth, not of another interpretation). R3 would compute this from
# the support closure; until then it is a named constant, not a magic literal.
AUTHORED_LEAF_DEPTH = 1


@dataclass(frozen=True)
class DreamLogEntry:
    """One consensus group in the ranked dream log: a hypothesis, never a verdict."""

    statement: str
    methods: tuple[str, ...]        # the DISTINCT interpreters that corroborated it (Agr)
    evidence: tuple[str, ...]       # authored note digests — content-addressed refs (G1)
    grounding: float                # g(κ)
    agreement: int                  # |Agr(κ)| = number of distinct methods
    depth: int                      # d(κ)
    confidence: float               # c(κ) — a ranking score for BELIEF; never combined w/ utility
    terminates_in_authored: bool    # support closure bottoms out in authored ground (I10)
    members: tuple[Claim, ...] = field(default_factory=tuple)


def _jaccard(a: set[str], b: set[str]) -> float:
    union = a | b
    return len(a & b) / len(union) if union else 0.0


def _consensus_groups(claims: list[Claim], *, threshold: float) -> list[list[int]]:
    """Union-find over claims by support-set overlap: claims whose authored support has
    Jaccard >= threshold describe the *same* underlying pattern (corroboration). Deterministic."""
    n = len(claims)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    sets = [set(c.support) for c in claims]
    for i in range(n):
        for j in range(i + 1, n):
            if _jaccard(sets[i], sets[j]) >= threshold:
                ri, rj = find(i), find(j)
                if ri != rj:
                    parent[max(ri, rj)] = min(ri, rj)

    groups: dict[int, list[int]] = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return list(groups.values())


def adjudicate(claims: list[Claim], *, authored_digests: set[str],
               agreement_jaccard: float,
               gamma: float = DEFAULT_GAMMA,
               lam: float = DEFAULT_LAMBDA,
               support_of: Callable[[tuple[str, ...]], float] | None = None,
               ) -> list[DreamLogEntry]:
    """Rank claims into a confidence-ordered dream log (no model; grounding decides). Agreement
    across DISTINCT interpreters multiplies confidence; a claim found by one lens still appears
    (disagreement is information, not noise) — just lower.

    `support_of` (H8, §6.1): an optional multi-path grounding scorer — evidence refs → g via
    noisy-OR message passing on the derivation DAG (`core.complex.support.grounding_with_support`
    partially applied). None (the default) keeps the flat resolvability `grounding_score`; the two
    are numerically identical whenever no evidence ref is an interpreted node (property-tested),
    so the confidence law (R1's clamp) is untouched — only g's *computation* generalizes."""
    entries: list[DreamLogEntry] = []
    for idxs in _consensus_groups(claims, threshold=agreement_jaccard):
        members = tuple(claims[i] for i in idxs)
        methods = tuple(sorted({m.method for m in members}))      # DISTINCT methods, not a vote
        evidence = tuple(sorted({r for m in members for r in m.support}))
        g = (support_of(evidence) if support_of is not None
             else grounding_score(evidence, authored_digests))
        agreement = len(methods)
        # The corroboration bonus lifts grounded claims; g=0 keeps c=0 regardless of agreement.
        # The single clamped definition (core.recursion) — c = min{1, γ^d·g·(1+λ(|Agr|−1))}; this
        # callsite no longer assembles the bonus, so it cannot produce c>1 or a depth-rising c.
        confidence = claim_confidence(AUTHORED_LEAF_DEPTH, grounding=g, agreement=agreement,
                                      gamma=gamma, lam=lam)
        # Representative statement: the most comprehensive member (largest support), stable.
        rep = max(members, key=lambda m: (len(m.support), m.method, m.statement))
        entries.append(DreamLogEntry(
            statement=rep.statement,
            methods=methods,
            evidence=evidence,
            grounding=round(g, 4),
            agreement=agreement,
            depth=AUTHORED_LEAF_DEPTH,
            confidence=round(confidence, 4),
            terminates_in_authored=(g == 1.0),     # all evidence resolves to authored leaves
            members=members,
        ))
    # Confidence-ordered (belief rank); stable tie-break by evidence so the log is reproducible.
    entries.sort(key=lambda e: (-e.confidence, e.evidence))
    return entries


def run_dream_rnd(view: MirrorView, derived: DerivedStore, *,
                  config: Config | None = None) -> list[DreamLogEntry]:
    """R0+R1 end to end behind the flag: run the interpreter panel, adjudicate, and persist the
    confidence-ordered dream log as INTERPRETED artifacts. Refuses unless the R&D flag is on."""
    cfg = config or get_config()
    rnd = require_rnd_enabled(cfg)                 # hard boundary (run_panel re-checks too)
    rows = view.rows()
    authored = {r.get("digest", "") for r in rows}
    titles = {r.get("digest", ""): r.get("title", "") for r in rows}

    claims = run_panel(view, config=cfg)
    entries = adjudicate(claims, authored_digests=authored,
                         agreement_jaccard=rnd.agreement_jaccard)
    for e in entries:
        derived.add(
            kind=DREAM_LOG,
            summary=e.statement,
            subjects=tuple(titles.get(d, d) for d in e.evidence),
            data={
                "confidence": e.confidence,          # belief axis only — utility is separate (R2)
                "grounding": e.grounding,
                "agreement": e.agreement,
                "methods": list(e.methods),
                "depth": e.depth,
                "evidence": list(e.evidence),        # content-addressed authored refs
                "terminates_in_authored": e.terminates_in_authored,
            },
            derived_from=e.evidence,                 # authored leaves -> depth 1, acyclic (G2)
        )
    return entries
