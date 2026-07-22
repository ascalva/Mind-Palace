"""H8 — noisy-OR multi-path support on the derivation DAG (core/complex/support.py; §6.1).

Proves: the noisy-OR combination is exact on the polytree; the adjudicator feed
(`grounding_with_support`) equals the flat `grounding_score` whenever no evidence ref is an
interpreted node (behavior-preserving on every current live input); interpreted parents earn
partial credit through their own DAG support; determinism; the defensive cycle guard.
"""

from __future__ import annotations

import pytest

from core.kernel.complex.support import grounding_with_support, noisy_or, support_scores
from core.kernel.selfcheck import grounding_score

AUTHORED = {"a1", "a2", "a3", "a4"}


def test_noisy_or_math():
    assert noisy_or([]) == 0.0
    assert noisy_or([1.0]) == 1.0
    assert noisy_or([0.5, 0.5]) == pytest.approx(0.75)          # 1 − 0.5·0.5
    assert noisy_or([0.3, 0.4]) == pytest.approx(1 - 0.7 * 0.6)
    assert noisy_or([2.0, -1.0]) == 1.0                          # clamped to [0, 1]


def test_support_scores_exact_on_the_polytree():
    # art ← {a1, a2}: two sure paths ⇒ s = 1 − (1−1)(1−1) = 1. mid ← {a1}; top ← {mid, a2}.
    refs = {"art": ("a1", "a2"), "mid": ("a1",), "top": ("mid", "a2")}
    s = support_scores(refs, AUTHORED)
    assert s["art"] == 1.0
    assert s["mid"] == 1.0
    assert s["top"] == 1.0                                       # both paths sure ⇒ sure


def test_unresolvable_refs_contribute_nothing():
    refs = {"art": ("ghost",), "half": ("a1", "ghost")}
    s = support_scores(refs, AUTHORED)
    assert s["art"] == 0.0                                       # no path to ground
    assert s["half"] == 1.0                                      # noisy-OR: one sure path suffices


def test_grounding_with_support_equals_flat_score_without_interpreted_refs():
    # The current live case: evidence = authored digests and/or junk. Must match grounding_score
    # exactly (the strict resolvability gate is preserved, not weakened).
    refs_of: dict[str, tuple[str, ...]] = {}
    for evidence in (["a1", "a2"], ["a1", "ghost"], ["ghost"], [], ["a1", "a2", "a3", "junk"]):
        assert grounding_with_support(evidence, refs_of, AUTHORED) == pytest.approx(
            grounding_score(evidence, AUTHORED)
        )


def test_interpreted_parent_earns_partial_credit():
    # An interpreted ref contributes its own DAG-combined support — the generalization beyond
    # the flat score (which scores any non-authored ref 0).
    refs_of = {"parent": ("a1", "ghost")}          # parent has one sure path ⇒ s(parent) = 1
    g = grounding_with_support(["a1", "parent"], refs_of, AUTHORED)
    assert g == pytest.approx(1.0)                 # mean(1.0, 1.0)
    assert grounding_score(["a1", "parent"], AUTHORED) == pytest.approx(0.5)  # the flat view
    # a parent with NO path to ground stays worthless — support cannot be manufactured
    refs_bad = {"parent": ("ghost",)}
    assert grounding_with_support(["a1", "parent"], refs_bad, AUTHORED) == pytest.approx(0.5)


def test_mean_gate_holds_against_citation_padding():
    # One good citation cannot carry junk ones (adjudication, not voting): the evidence-level
    # aggregation is a mean, not a noisy-OR.
    refs_of: dict[str, tuple[str, ...]] = {}
    g = grounding_with_support(["a1", "ghost1", "ghost2", "ghost3"], refs_of, AUTHORED)
    assert g == pytest.approx(0.25)


def test_deterministic_and_cycle_defensive():
    refs = {"x": ("y",), "y": ("x",)}              # impossible at the source; guarded anyway
    s1 = support_scores(refs, AUTHORED)
    s2 = support_scores(refs, AUTHORED)
    assert s1 == s2 == {"x": 0.0, "y": 0.0}        # a closed loop grounds nothing
