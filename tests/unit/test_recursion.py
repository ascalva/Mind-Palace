"""Recursion-decay bound c ≤ γ^d·g (Invariant 10) and the single clamped confidence definition
c = min{1, γ^d·g·(1+λ(|Agr|−1))} (Prompt R1). Deterministic checks; the monotonicity and
c∈[0,1] properties over arbitrary inputs are in test_properties.py."""

import pytest

from core.recursion import DEFAULT_GAMMA, DEFAULT_LAMBDA, claim_confidence, decay_bound


def test_authored_leaf_is_undiscounted():
    assert decay_bound(0, grounding=1.0) == 1.0          # depth 0: c ≤ g


def test_depth_strictly_discounts():
    assert decay_bound(1) == DEFAULT_GAMMA               # γ^1
    assert decay_bound(2) == DEFAULT_GAMMA ** 2
    assert decay_bound(3) == pytest.approx(0.125)        # depth-3 is clearly subordinate (G7)


def test_grounding_scales_the_ceiling():
    assert decay_bound(2, grounding=0.4) == pytest.approx((DEFAULT_GAMMA ** 2) * 0.4)


def test_gamma_must_contract():
    with pytest.raises(ValueError):
        decay_bound(1, gamma=1.0)                         # γ=1 would not decay
    with pytest.raises(ValueError):
        decay_bound(1, gamma=0.0)


# --- claim_confidence: the single clamped definition (Prompt R1) ----------------

def test_claim_confidence_equals_unclamped_on_current_inputs():
    # Behavior-preserving: on everything the R0/R1 panel produces today (d=1, small agreement,
    # g∈[0,1]) the raw product is < 1, so the clamp is a no-op — c matches the old assembly
    # decay_bound(1, g)·(1+λ(a−1)) exactly.
    for g in (0.0, 0.5, 1.0):
        for a in (1, 2, 3, 4):
            raw = decay_bound(1, grounding=g) * (1 + DEFAULT_LAMBDA * (a - 1))
            assert raw <= 1.0                             # the premise: no clamp needed today
            assert claim_confidence(1, grounding=g, agreement=a) == pytest.approx(raw)


def test_claim_confidence_clamps_above_one():
    # Force the raw product past 1 (many agreeing methods at low decay) — the clamp holds c at 1.
    c = claim_confidence(0, grounding=1.0, agreement=40, gamma=0.9, lam=1.0)
    assert c == 1.0


def test_agreement_is_a_multiplier_not_a_vote():
    # g=0 ⇒ c=0 regardless of how many methods agree (agreement can't manufacture confidence).
    assert claim_confidence(1, grounding=0.0, agreement=10) == 0.0
    # more agreement never lowers confidence (bonus ≥ 1, monotone in |Agr|)
    assert (claim_confidence(1, grounding=0.5, agreement=3)
            >= claim_confidence(1, grounding=0.5, agreement=1))


def test_claim_confidence_rejects_illegal_inputs():
    with pytest.raises(ValueError):
        claim_confidence(1, agreement=0)                  # a claim is found by ≥1 method
    with pytest.raises(ValueError):
        claim_confidence(1, lam=-0.1)                     # corroboration bonus must be ≥ 0
