"""The alignment drift gauge D(t) = d(μ(s_t), B) (BUILD-SPEC §15; Track A, item A1; gap G4).

The Voigt-Kampff analog of `alignment-subsystem.md` §2: a periodic, deterministic measure of
how far the system's *behavioral profile* μ(s_t) has drifted from the **frozen anchor** B. This
is the detection conjunct the gate already names but until now only proxied — `ops.gate` specifies

    G_now(Δ,s) = approved(Δ) ∧ golden(Δ·s) ≥ golden(B) ∧ D(Δ·s) ≤ Θ          (G5)

and `D(Δ·s) ≤ Θ` was a stand-in ("no rolling-baseline regression") until this module made it real.
**Detection only — this gauge alters nothing.** It is consumed by the gate's validate step
(`ops.selfmod.build_golden_validator`), by the longitudinal harness (Track F / F4 trajectory
asserts), and later by the alignment report (A2).

The profile (μ) — "rates ⊕ conformance" (G4)
---------------------------------------------
μ(s_t) is the mixed profile G4 calls for: the golden-set **capability rates** (recall↑, overlap↑,
mean_distance↓ — `eval.golden.GoldenReport`) ⊕ the **Constitution conformance** signal (the
`core.constitution` fingerprint vs the blessed one). A2 extends μ with structural axes (min-cut to
authored, community/echo-chamber, depth/grounding distributions) — `Axis` is a flat, additive
record precisely so that is a data change, not a rewrite.

The metric (d) — one-sided L2 deterioration distance  [owner decision, 2026-06-29]
----------------------------------------------------------------------------------
Each axis contributes only its **bad-direction** deviation past baseline, normalized by a blessed
per-axis tolerance (one "tolerance-unit"); the axes combine by L2:

    det_i   = max(0, deterioration_of_axis_i) / tolerance_i
    D       = sqrt( Σ_i det_i² )

So **D = 0 whenever every axis is at-or-better than baseline** — healthy improvement (recall
rising as the corpus grows) is *not* counted as drift, matching the design note's "some drift is
healthy; deterioration is not." A **Constitution fingerprint mismatch is a categorical breach of
the fixed point**, not one more axis to average: it hard-trips (D = ∞, out of band) regardless of
capability — you cannot be "a little" off the Constitution.

Θ — the tolerance band  [owner decision: Θ = 1.0, blessed + F4-calibrated]
--------------------------------------------------------------------------
With per-tolerance-unit normalization, Θ = 1.0 means "no single tolerance-unit of aggregate
deterioration." Θ is a **human-set, frozen fixed point** (alignment-subsystem.md §5): it is
excluded from the self-mod lever set (levers tune only `[dreaming]` knobs, never this), lives in
the owner-blessed `eval/golden/baseline.json` beside the golden anchor (Invariant 9 — edited only
by the owner, on purpose, logged), and is calibrated against observed curves by the F4 harness and
then re-blessed. This module never writes it.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

from eval.golden import (
    BASELINE_PATH,
    GoldenReport,
    Retriever,
    evaluate,
    load_baseline,
    load_golden_set,
)


@dataclass(frozen=True)
class Axis:
    """One profile dimension and its blessed anchor + scale. Additive: A2 appends structural
    axes (min-cut, community, depth/grounding) without touching the metric."""

    name: str
    value: float           # μ_i(s_t) — the measured value now
    baseline: float        # B_i — the blessed frozen-anchor value
    tolerance: float       # one "tolerance-unit" of deterioration on this axis
    higher_is_better: bool  # direction; mean_distance is False (closer = lower = better)

    def deterioration(self) -> float:
        """One-sided, tolerance-normalized deterioration. 0 when at-or-better than baseline; a
        non-positive tolerance with real deterioration is treated as ∞ (an unscaled regression
        cannot be 'within' anything)."""
        bad = (self.baseline - self.value) if self.higher_is_better \
            else (self.value - self.baseline)
        if bad <= 0.0:
            return 0.0
        return bad / self.tolerance if self.tolerance > 0.0 else math.inf


@dataclass(frozen=True)
class DriftConfig:
    """The blessed drift fixed points (from baseline.json `drift`). Owner-only, frozen (§15)."""

    recall_tol: float = 0.10
    overlap_tol: float = 0.10
    distance_tol: float = 0.05
    theta: float = 1.0                          # Θ — the tolerance band
    blessed_fingerprint: str | None = None      # the frozen-anchor Constitution identity


@dataclass(frozen=True)
class Profile:
    """μ(s_t): the behavioral profile — capability rates ⊕ Constitution conformance (G4)."""

    recall_at_k: float
    overlap: float
    mean_distance: float
    constitution_intact: bool


@dataclass(frozen=True)
class DriftReport:
    """The gauge reading. `within_tolerance` is the gate's D(Δ·s) ≤ Θ conjunct (also requires the
    Constitution intact — a breach is out of band by construction)."""

    drift: float                  # D(t)
    theta: float                  # Θ in force
    within_tolerance: bool        # D ≤ Θ AND constitution intact
    constitution_intact: bool
    per_axis: dict[str, float]    # axis name -> deterioration (tolerance-units); for the report/F4


def drift(profile: Profile, baseline_metrics: dict[str, float], cfg: DriftConfig) -> DriftReport:
    """D(t) = d(μ, B): one-sided L2 deterioration distance, with a Constitution-breach hard trip."""
    if not profile.constitution_intact:
        # The fixed point itself moved — categorically out of band, dominates every rate axis.
        return DriftReport(drift=math.inf, theta=cfg.theta, within_tolerance=False,
                           constitution_intact=False, per_axis={"constitution": math.inf})
    axes = (
        Axis("recall_at_k", profile.recall_at_k, baseline_metrics["recall_at_k"],
             cfg.recall_tol, higher_is_better=True),
        Axis("overlap", profile.overlap, baseline_metrics["overlap"],
             cfg.overlap_tol, higher_is_better=True),
        Axis("mean_distance", profile.mean_distance, baseline_metrics["mean_distance"],
             cfg.distance_tol, higher_is_better=False),
    )
    per_axis = {a.name: a.deterioration() for a in axes}
    d = math.sqrt(sum(v * v for v in per_axis.values()))
    return DriftReport(drift=d, theta=cfg.theta, within_tolerance=(d <= cfg.theta),
                       constitution_intact=True, per_axis=per_axis)


def profile_from_report(report: GoldenReport, *, constitution_intact: bool) -> Profile:
    m = report.as_metrics()
    return Profile(recall_at_k=m["recall_at_k"], overlap=m["overlap"],
                   mean_distance=m["mean_distance"], constitution_intact=constitution_intact)


def constitution_intact(cfg: DriftConfig) -> bool:
    """True iff the live Constitution matches the blessed fingerprint. No blessed fingerprint ⇒
    intact (we do not false-trip on an unconfigured anchor — honest, not silently failing closed
    on missing config; the owner blesses the fingerprint to turn the conformance axis on)."""
    if not cfg.blessed_fingerprint:
        return True
    from core.constitution import constitution_fingerprint
    return constitution_fingerprint() == cfg.blessed_fingerprint


def drift_from_report(report: GoldenReport, baseline_metrics: dict[str, float], cfg: DriftConfig,
                      *, intact: bool | None = None) -> DriftReport:
    """Gauge from an already-computed golden report (so the validator evaluates once). `intact`
    overrides the conformance check (tests pass it explicitly); None computes it from `cfg`."""
    is_intact = constitution_intact(cfg) if intact is None else intact
    return drift(profile_from_report(report, constitution_intact=is_intact), baseline_metrics, cfg)


def load_drift_config(path: Path = BASELINE_PATH) -> DriftConfig:
    """Read the blessed `drift` section of baseline.json. Defaults apply if it is absent, so the
    gauge degrades gracefully on an un-extended baseline (Θ=1.0, no conformance check)."""
    data = json.loads(path.read_text(encoding="utf-8"))
    d = data.get("drift", {})
    return DriftConfig(
        recall_tol=float(d.get("recall_tol", 0.10)),
        overlap_tol=float(d.get("overlap_tol", 0.10)),
        distance_tol=float(d.get("distance_tol", 0.05)),
        theta=float(d.get("drift_tolerance", 1.0)),
        blessed_fingerprint=d.get("constitution_fingerprint"),
    )


def measure_drift(retriever: Retriever, *, golden=None, baseline: dict[str, float] | None = None,
                  cfg: DriftConfig | None = None, intact: bool | None = None) -> DriftReport:
    """High-level entry: run the golden set through `retriever` and report D(t). Used standalone by
    the alignment report (A2) and the F4 trajectory harness; the gate uses `drift_from_report` to
    avoid re-evaluating. Mirrors `eval.golden.evaluate`'s injectable-retriever seam."""
    golden = golden or load_golden_set()
    baseline = baseline or load_baseline()
    cfg = cfg or load_drift_config()
    report = evaluate(golden, retriever)
    return drift_from_report(report, baseline, cfg, intact=intact)
