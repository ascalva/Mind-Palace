"""A1 — the §15 alignment drift gauge D(t) = d(μ(s_t), B) (eval/drift.py).

Pure, deterministic checks of the gauge contract: one-sided deterioration (healthy improvement is
NOT drift), per-axis tolerance normalization, L2 aggregation, the Θ band, and the Constitution-
fingerprint hard trip. No model, no stores — profiles in, report out.
"""

from __future__ import annotations

import math

import pytest

from eval.drift import (
    DriftConfig,
    Profile,
    constitution_intact,
    drift,
    drift_from_report,
    load_drift_config,
    measure_drift,
    profile_from_report,
)
from eval.golden import GoldenReport, QueryResult, load_baseline, load_golden_set

# A self-contained anchor + config so the unit tests don't depend on the blessed file's values.
_B = {"recall_at_k": 1.0, "overlap": 0.40, "mean_distance": 0.60}
_CFG = DriftConfig(recall_tol=0.10, overlap_tol=0.10, distance_tol=0.05, theta=1.0,
                   blessed_fingerprint=None)   # None ⇒ conformance not checked here


def _p(recall=1.0, overlap=0.40, distance=0.60, intact=True) -> Profile:
    return Profile(recall_at_k=recall, overlap=overlap, mean_distance=distance,
                   constitution_intact=intact)


def test_at_baseline_is_zero_drift():
    r = drift(_p(), _B, _CFG)
    assert r.drift == 0.0
    assert r.within_tolerance and r.constitution_intact


def test_healthy_improvement_is_not_drift():
    # recall up, overlap up, distance down (all better) ⇒ one-sided ⇒ D = 0.
    r = drift(_p(recall=1.0, overlap=0.9, distance=0.1), _B, _CFG)
    assert r.drift == 0.0
    assert r.per_axis == {"recall_at_k": 0.0, "overlap": 0.0, "mean_distance": 0.0}


def test_one_tolerance_unit_is_the_band_edge():
    # recall drops by exactly one tolerance-unit ⇒ that axis = 1.0 ⇒ D = 1.0 = Θ ⇒ still within (≤).
    r = drift(_p(recall=0.90), _B, _CFG)
    assert r.per_axis["recall_at_k"] == pytest.approx(1.0)
    assert r.drift == pytest.approx(1.0)
    assert r.within_tolerance


def test_past_the_band_is_out_of_tolerance():
    r = drift(_p(recall=0.79), _B, _CFG)   # 2.1 tolerance-units
    assert r.drift > _CFG.theta
    assert not r.within_tolerance


def test_axes_combine_by_l2():
    # recall −0.10 (1.0 unit) and distance +0.05 (1.0 unit) ⇒ D = sqrt(1²+1²) = √2.
    r = drift(_p(recall=0.90, distance=0.65), _B, _CFG)
    assert r.drift == pytest.approx(math.sqrt(2.0))
    assert not r.within_tolerance        # √2 > 1.0


def test_mean_distance_direction_is_lower_is_better():
    worse = drift(_p(distance=0.70), _B, _CFG)   # rose 0.10 = 2 tol ⇒ deterioration
    better = drift(_p(distance=0.50), _B, _CFG)  # fell ⇒ improvement ⇒ 0
    assert worse.per_axis["mean_distance"] == pytest.approx(2.0)
    assert better.per_axis["mean_distance"] == 0.0


def test_constitution_breach_hard_trips_regardless_of_capability():
    # Perfect-and-better capability, but the fixed point itself moved ⇒ categorically out of band.
    r = drift(_p(recall=1.0, overlap=1.0, distance=0.0, intact=False), _B, _CFG)
    assert r.drift == math.inf
    assert not r.within_tolerance and not r.constitution_intact
    assert r.per_axis == {"constitution": math.inf}


def test_zero_tolerance_with_real_deterioration_is_infinite():
    cfg0 = DriftConfig(recall_tol=0.0, overlap_tol=0.1, distance_tol=0.05, theta=1.0)
    r = drift(_p(recall=0.99), _B, cfg0)
    assert r.per_axis["recall_at_k"] == math.inf
    assert not r.within_tolerance


# --- conformance check -----------------------------------------------------------------------

def test_constitution_intact_matches_blessed_fingerprint():
    from core.constitution import constitution_fingerprint
    real = constitution_fingerprint()
    assert constitution_intact(DriftConfig(blessed_fingerprint=real)) is True
    assert constitution_intact(DriftConfig(blessed_fingerprint="deadbeef")) is False


def test_no_blessed_fingerprint_does_not_false_trip():
    # Honest: an unconfigured anchor reads intact rather than failing closed on missing config.
    assert constitution_intact(DriftConfig(blessed_fingerprint=None)) is True


# --- blessed file + end-to-end ----------------------------------------------------------------

def test_load_drift_config_reads_the_blessed_baseline():
    cfg = load_drift_config()
    assert cfg.theta == 1.0                      # Θ blessed in baseline.json
    assert cfg.blessed_fingerprint               # the frozen-anchor Constitution identity is set
    assert cfg.distance_tol == 0.05


def _stub(mapping):
    return lambda q, k: list(mapping.get(q, []))


def test_measure_drift_perfect_retriever_is_within_tolerance():
    golden = load_golden_set()
    perfect = _stub({gq.query: [{"title": t} for t in gq.expected] for gq in golden})
    r = measure_drift(perfect, golden=golden, baseline=load_baseline())
    assert r.within_tolerance and r.constitution_intact


def test_measure_drift_empty_retriever_breaches_recall():
    golden = load_golden_set()
    r = measure_drift(_stub({}), golden=golden, baseline=load_baseline())
    assert r.drift > r.theta
    assert not r.within_tolerance
    assert r.per_axis["recall_at_k"] > 0.0


def test_drift_from_report_reuses_a_report():
    report = GoldenReport(per_query=(
        QueryResult(id="q", retrieved=(), recall_at_k=0.5, overlap=0.40, mean_distance=0.60),
    ))
    # recall 0.5 vs baseline 1.0 ⇒ 5 tolerance-units ⇒ way past Θ. intact overridden True.
    r = drift_from_report(report, _B, _CFG, intact=True)
    assert r.per_axis["recall_at_k"] == pytest.approx(5.0)
    assert not r.within_tolerance


def test_profile_from_report_maps_metrics():
    report = GoldenReport(per_query=(
        QueryResult(id="q", retrieved=(), recall_at_k=0.8, overlap=0.3, mean_distance=0.7),
    ))
    p = profile_from_report(report, constitution_intact=True)
    assert (p.recall_at_k, p.overlap, p.mean_distance) == (0.8, 0.3, 0.7)
    assert p.constitution_intact is True


# --- A2: the structural axes (H6) — additive, never rewiring ----------------------------------

_B_STRUCT = {**_B, "frustration": 0.05, "min_conductance": 0.30}


def test_structural_axes_absent_leaves_drift_exactly_pre_a2():
    # A profile without the A2 fields, even against a baseline that HAS them, produces exactly
    # the original three axes — the extension is additive (Axis is a data change, not a rewrite).
    r = drift(_p(recall=0.90), _B_STRUCT, _CFG)
    assert set(r.per_axis) == {"recall_at_k", "overlap", "mean_distance"}
    assert r.drift == pytest.approx(1.0)


def test_structural_axes_appear_when_supplied():
    p = Profile(recall_at_k=1.0, overlap=0.40, mean_distance=0.60, constitution_intact=True,
                frustration=0.05, min_conductance=0.30)
    r = drift(p, _B_STRUCT, _CFG)
    assert set(r.per_axis) == {"recall_at_k", "overlap", "mean_distance",
                               "frustration", "min_conductance"}
    assert r.drift == 0.0                               # at baseline on every axis


def test_rising_frustration_is_deterioration():
    # frustration up 0.25 = one tolerance-unit (frustration_tol=0.25); capability at baseline.
    p = Profile(recall_at_k=1.0, overlap=0.40, mean_distance=0.60, constitution_intact=True,
                frustration=0.30, min_conductance=0.30)
    r = drift(p, _B_STRUCT, _CFG)
    assert r.per_axis["frustration"] == pytest.approx(1.0)
    assert r.per_axis["min_conductance"] == 0.0
    assert r.drift == pytest.approx(1.0)


def test_falling_conductance_is_deterioration_and_rising_is_not():
    worse = Profile(recall_at_k=1.0, overlap=0.40, mean_distance=0.60, constitution_intact=True,
                    frustration=0.05, min_conductance=0.20)    # fell 0.10 = 1 unit (echo chamber)
    better = Profile(recall_at_k=1.0, overlap=0.40, mean_distance=0.60, constitution_intact=True,
                     frustration=0.0, min_conductance=0.50)    # both axes improved
    assert drift(worse, _B_STRUCT, _CFG).per_axis["min_conductance"] == pytest.approx(1.0)
    assert drift(better, _B_STRUCT, _CFG).drift == 0.0         # one-sided: improvement ≠ drift


def test_profile_from_report_carries_structural_axes():
    report = GoldenReport(per_query=(
        QueryResult(id="q", retrieved=(), recall_at_k=0.8, overlap=0.3, mean_distance=0.7),
    ))
    p = profile_from_report(report, constitution_intact=True,
                            structural={"frustration": 0.1, "min_conductance": 0.4})
    assert (p.frustration, p.min_conductance) == (0.1, 0.4)
    # and omitted ⇒ None ⇒ the axes stay off (pre-A2 behavior)
    p0 = profile_from_report(report, constitution_intact=True)
    assert p0.frustration is None and p0.min_conductance is None


def test_alignment_snapshot_feeds_the_drift_profile():
    # End to end: complex → alignment_snapshot → Profile → drift. Balanced all-support backbone
    # at the blessed baseline ⇒ zero structural drift.
    import numpy as np

    from core.complex.build import build_complex
    from core.complex.cut import alignment_snapshot
    from core.mirror import MirrorView
    rng = np.random.default_rng(0)
    rows = []
    for i in range(4):
        rows.append({"digest": f"p{i}", "title": f"p{i}", "provenance": "authored-solo",
                     "vector": list(np.array([1.0, 0, 0, 0]) + rng.normal(0, .02, 4))})
    for i in range(4):
        rows.append({"digest": f"s{i}", "title": f"s{i}", "provenance": "authored-solo",
                     "vector": list(np.array([0.0, 0, 1.0, 0]) + rng.normal(0, .02, 4))})
    snap = alignment_snapshot(build_complex(MirrorView(_rows=tuple(rows))))
    assert snap["frustration"] == pytest.approx(0.0, abs=1e-6)   # no contradiction ⇒ balanced
    assert 0.0 <= snap["min_conductance"] <= 1.0
    baseline = {**_B, **snap}
    p = Profile(recall_at_k=1.0, overlap=0.40, mean_distance=0.60, constitution_intact=True,
                frustration=snap["frustration"], min_conductance=snap["min_conductance"])
    r = drift(p, baseline, _CFG)
    assert r.drift == 0.0
    assert {"frustration", "min_conductance"} <= set(r.per_axis)
