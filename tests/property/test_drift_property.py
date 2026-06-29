"""Property-based checks for the §15 drift gauge (eval/drift.py; Track A, A1).

Hypothesis over arbitrary profiles, asserting the gauge's load-bearing invariants rather than
hand-picked points:

  * D ≥ 0 always, and D = 0 exactly when no axis has deteriorated.
  * one-sided: a profile at-or-better than baseline on every axis has D = 0 (healthy growth is
    never flagged as drift).
  * monotonic: deteriorating an axis further never decreases D.
  * within_tolerance ⇔ D ≤ Θ (when the Constitution is intact).
"""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

from eval.drift import DriftConfig, Profile, drift

_B = {"recall_at_k": 1.0, "overlap": 0.40, "mean_distance": 0.60}
_CFG = DriftConfig(recall_tol=0.10, overlap_tol=0.10, distance_tol=0.05, theta=1.0,
                   blessed_fingerprint=None)

_rate = st.floats(min_value=0.0, max_value=1.0, allow_nan=False)
_dist = st.floats(min_value=0.0, max_value=2.0, allow_nan=False)


def _profile(recall, overlap, distance) -> Profile:
    return Profile(recall_at_k=recall, overlap=overlap, mean_distance=distance,
                   constitution_intact=True)


@given(_rate, _rate, _dist)
@settings(max_examples=200)
def test_drift_is_nonnegative_and_within_iff_below_theta(recall, overlap, distance):
    r = drift(_profile(recall, overlap, distance), _B, _CFG)
    assert r.drift >= 0.0
    assert r.within_tolerance == (r.drift <= _CFG.theta)


@given(_rate, _rate, _dist)
@settings(max_examples=200)
def test_at_or_better_than_baseline_is_zero_drift(recall, overlap, distance):
    # Force every axis to at-least-baseline (rates up, distance down) ⇒ one-sided ⇒ D = 0.
    p = _profile(max(recall, _B["recall_at_k"]),
                 max(overlap, _B["overlap"]),
                 min(distance, _B["mean_distance"]))
    assert drift(p, _B, _CFG).drift == 0.0


@given(_rate, _rate, _dist, st.floats(min_value=0.0, max_value=1.0, allow_nan=False))
@settings(max_examples=200)
def test_more_deterioration_never_decreases_drift(recall, overlap, distance, drop):
    base = drift(_profile(recall, overlap, distance), _B, _CFG)
    worse = drift(_profile(recall - drop, overlap, distance), _B, _CFG)   # recall can only fall
    assert worse.drift >= base.drift - 1e-9
