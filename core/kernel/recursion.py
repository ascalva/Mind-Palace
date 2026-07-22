"""Recursion-decay bound for interpreted artifacts (Invariant 10; BUILD-SPEC §8 analogy).

*Interpretation is hypothesis; tame the recursion; evidence decides, not persuasion.*

An interpreted artifact's confidence may not compound with derivational distance from ground
truth — it must **decay**. With derivation depth `d(κ)` (0 = an authored leaf; computed by
`DerivedStore.depth`, well-defined because the derivation graph is acyclic by construction —
gap G2) and a base grounding score `g(κ) ∈ [0, 1]`, the bound is

        c(κ) ≤ γ^{d(κ)} · g(κ),     γ ∈ (0, 1).

Because γ < 1, a self-referential loop loses potency every pass instead of amplifying — the
formal shape of taming "the stack-overflow of a mind thinking only about itself". This module
is the small, pure home of that bound: depth + γ + g make `c` *computable*.

`decay_bound` is the depth-decay **ceiling** γ^d·g. The full, clamped confidence a claim actually
carries — `c = min{1, γ^d · g · (1 + λ(|Agr| − 1))}` — is `claim_confidence`, the **single**
definition the adjudicator calls (companion III §5.3/§7.2). The min{1,·} clamp + the γ^d factor
make `c ∈ [0,1]` and non-increasing in depth *by construction*: a c>1 or a depth-rising c is
unrepresentable because no caller assembles the bonus itself.

γ bound (gap G7): γ is held small enough that a depth-3 artifact is *clearly subordinate* to
ground truth — at the default γ = 0.5, depth-3 confidence is capped at 0.125·g (an eighth),
so third-order interpretation cannot out-rank a first-order reading of the same evidence. It
is a declared constant here, not a magic number scattered at call sites; calibrate on the real
corpus before the adjudicator ships.
"""

from __future__ import annotations

# γ ∈ (0,1): the per-depth confidence discount (gap G7). Small enough that depth-3 (γ³=0.125)
# is plainly subordinate to ground truth. A single declared bound, not a scattered literal.
DEFAULT_GAMMA: float = 0.5

# λ ≥ 0: the corroboration bonus in the base confidence c₀(κ) = g·(1 + λ(|Agr(κ)|-1)) — each
# additional *independent* agreeing source nudges confidence up (gap G7). BOUND: small, λ ≤ 0.25,
# so corroboration tilts a tie but never lets agreement masquerade as ground truth — the hard
# ceiling c ≤ γ^d·g still dominates. A declared constant awaiting calibration on the real corpus
# (the adjudicator that consumes it is a later phase); not a magic number at a call site.
DEFAULT_LAMBDA: float = 0.1


def decay_bound(depth: int, *, grounding: float = 1.0, gamma: float = DEFAULT_GAMMA) -> float:
    """The confidence ceiling c ≤ γ^depth · g for an artifact at derivation `depth` with base
    grounding `g` (Invariant 10). Non-increasing in depth for γ ∈ (0,1) and g ≥ 0 — confidence
    strictly decays away from authored ground, never compounds."""
    if not 0.0 < gamma < 1.0:
        raise ValueError(f"gamma must be in (0,1) for the decay to contract, got {gamma}")
    if depth < 0:
        raise ValueError(f"depth must be >= 0, got {depth}")
    if grounding < 0.0:
        raise ValueError(f"grounding must be >= 0, got {grounding}")
    return (gamma ** depth) * grounding


def claim_confidence(depth: int, *, grounding: float = 1.0, agreement: int = 1,
                     gamma: float = DEFAULT_GAMMA, lam: float = DEFAULT_LAMBDA) -> float:
    """THE single definition of an interpreted claim's confidence (companion III §5.3/§7.2):

        c = min{1, γ^d · g · (1 + λ(|Agr| − 1))}.

    `decay_bound` is the depth-decay *ceiling* γ^d·g (Invariant 10); this multiplies in the
    bounded corroboration bonus `(1 + λ(|Agr|−1))` — agreement across |Agr| distinct methods is a
    *multiplier, not a vote* (g=0 ⇒ c=0) — and applies the **min{1,·} clamp**. Together the clamp
    and the γ^d factor guarantee, for every admissible input:

      * **c ∈ [0, 1]** — no path can produce c > 1 (closes the companion III §7.2 clamp tension);
      * **c is non-increasing in depth d** for fixed (g, |Agr|) — belief decays away from authored
        ground, never compounds.

    This is the *only* place confidence is assembled; callers (the adjudicator) must not multiply
    the bonus in themselves, so an out-of-range or depth-rising c is unrepresentable at source."""
    if agreement < 1:
        raise ValueError(f"agreement must be >= 1 (found by >=1 method), got {agreement}")
    if lam < 0.0:
        raise ValueError(f"lambda (corroboration bonus) must be >= 0, got {lam}")
    # decay_bound validates depth/gamma/grounding and returns the γ^d·g ceiling; the clamp then
    # holds c ≤ 1 even if the bonus (or an out-of-range grounding) would push the product past 1.
    ceiling = decay_bound(depth, grounding=grounding, gamma=gamma)
    return min(1.0, ceiling * (1.0 + lam * (agreement - 1)))
