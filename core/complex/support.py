"""Noisy-OR message passing on the derivation DAG — exact multi-path support (§6.1; H8).

When a claim is supported through several independent paths, the principled combination is a
noisy-OR over path strengths:

    Pr[supported] = 1 − Π_p (1 − s_p)

On a **polytree** (singly-connected DAG) this is exact and linear (Pearl, BP on polytrees); the
derivation structure is depth-1 today, so it is exact now, and the acyclicity guard + bounded
depth keep it tractable as recursion deepens.

The adjudicator feed (`grounding_with_support`) generalizes `core.selfcheck.grounding_score`
WITHOUT changing the confidence law (R1's clamp stays THE single definition):

  * per evidence ref, a **path strength**: 1.0 for an authored leaf, the DAG-combined noisy-OR
    for an interpreted node, 0.0 for an unresolvable ref;
  * the claim's g = the **mean** of those strengths — exactly `grounding_score` when every ref is
    authored-or-junk (today's only live case; proven by property test), and a defensible partial
    credit for interpreted parents once recursion exists. The mean (not a noisy-OR) at the
    evidence level keeps the anti-fabrication gate strict: one good citation cannot carry nine
    junk ones ("adjudication not voting" — §6.1's discipline, held).

Deterministic; no model; no network. Bayesian machinery organizes the *graph*, never certifies a
*thought* (§6.3): these are support strengths for ranking, not truth probabilities.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping


def noisy_or(paths: Iterable[float]) -> float:
    """1 − Π(1 − s_p) over independent path strengths, each clamped to [0, 1]. Empty ⇒ 0.0."""
    prod = 1.0
    for s in paths:
        prod *= 1.0 - min(1.0, max(0.0, s))
    return 1.0 - prod


def support_scores(refs_of: Mapping[str, tuple[str, ...]],
                   authored: set[str]) -> dict[str, float]:
    """Path-combined support s(κ) for every node in the derivation map (§6.1).

    s(authored leaf) = 1.0; s(node) = noisy-OR over its refs' strengths (an unresolvable ref —
    neither authored nor a known node — contributes 0). A memoized topological sweep: exact on
    the polytree, linear, deterministic. Cycles are impossible at the source (`DerivedStore`
    refuses them at insert), but the sweep guards defensively (a revisit on the path scores 0
    rather than recursing forever)."""
    memo: dict[str, float] = {}

    def strength(ref: str, on_path: frozenset[str]) -> float:
        if ref in authored:
            return 1.0
        if ref not in refs_of:
            return 0.0                          # unresolvable — contributes nothing
        if ref in memo:
            return memo[ref]
        if ref in on_path:                      # defensive; inserts prevent cycles
            return 0.0
        s = noisy_or(strength(t, on_path | {ref}) for t in refs_of[ref])
        memo[ref] = s
        return s

    return {node: strength(node, frozenset()) for node in refs_of}


def grounding_with_support(evidence: Iterable[str],
                           refs_of: Mapping[str, tuple[str, ...]],
                           authored: set[str]) -> float:
    """The adjudicator's g, generalized to multi-path support: the MEAN per-ref path strength
    over a claim's direct evidence (authored → 1, interpreted node → its DAG noisy-OR,
    unresolvable → 0). Empty evidence is ungrounded (0.0).

    Equals `grounding_score(evidence, authored)` exactly whenever no ref is an interpreted node
    (the current live case) — the strict resolvability gate is preserved, not weakened."""
    refs = list(evidence)
    if not refs:
        return 0.0
    scores = support_scores(refs_of, authored)
    total = 0.0
    for r in refs:
        if r in authored:
            total += 1.0
        else:
            total += scores.get(r, 0.0)
    return total / len(refs)
