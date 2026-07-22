---
type: finding
id: finding-0160
status: open             # open → routed → resolved | promoted
created: 2026-07-22
updated: 2026-07-22
links:
  - tests/unit/test_provenance_tags.py
  - tests/unit/provenance_fixture.py
  - docs/build-plans/bp-098/plan.md      # surfaced by bp-098's green-gate run (NOT its cause)
ftype: spec-defect       # a gate-health defect: the full green-gate is red on main
origin_plan: bp-098
route: orchestrator      # bears on the deploy gate broadly (mypy pinning / gate health) — an owner/orchestrator call
resolution: null
---

# The provenance-tag type-error tests are RED on main under mypy 2.2.0 (deploy gate broken)

## What

Three tests in `tests/unit/test_provenance_tags.py` fail on a CLEAN `main` (HEAD `7eb127f`),
independent of any working change:

- `test_promotion_without_capability_is_a_type_error`
- `test_subclass_laundering_is_a_type_error`
- `test_mirror_bypass_is_a_type_error`

Each shells out to `mypy` over `tests/unit/provenance_fixture.py` and asserts an EXACT set of
`error:`-line numbers. Under the installed **mypy 2.2.0** the emitted diagnostics no longer match
the pinned expectations:
- the two "route/laundering" tests emit the expected line set PLUS/at shifted lines (the exact-set
  assertion is brittle to any diagnostic drift);
- `test_mirror_bypass_is_a_type_error` collects **0** errors where it expects **2** (`{14, 15}`),
  i.e. mypy 2.2.0 no longer flags the mirror-bypass at those lines at all — the more concerning
  case, since it means the *structural provenance guard these tests assert* may not be enforced by
  this mypy version the way the suite believes.

**Proven pre-existing / not bp-098:** stashing all of bp-098's changes and running the three on
clean HEAD reproduces the failures identically. bp-098 touches only `core/kernel/config/loader.py`,
`ops/lifecycle/launcher.py`, `scripts/palace.py`, `config/defaults.toml`, and a new test — none
imported by `test_provenance_tags.py`. The full green-gate run for bp-098 was **1907 passed, 3
failed (these), 8 skipped, 21 deselected**; the 3 failures are this finding.

## Why it matters

The full green-gate suite is the DEPLOY gate (`Launcher.gate_cmd`) and the local-ci-gate every
seal/push honors. It is currently RED on `main` — so a strict reading blocks `palace deploy` and
muddies every builder's "is the suite green?" signal. Worse, the mirror-bypass case failing at 0
errors is not just a fixture-line drift: it may indicate mypy 2.2.0 changed how `@final` /
overload-based provenance guards are checked, i.e. a real weakening of the type-level MIRROR
guarantee (dn-provenance-tags). That needs a human eye, not a blind line-number bump.

## Re-entry condition

N/A to bp-098 (no bp-098 criterion is parked on this — bp-098's own acceptance is fully met and its
5 new tests are green). This is a standalone gate-health defect for the orchestrator to triage into
its own fix session.

## Routing

`spec-defect` bearing on the deploy gate + a possible type-guard regression → **orchestrator**.
Decision surface for the fix session:
1. **Diagnose the mirror-bypass 0-errors case FIRST** — is the provenance MIRROR guard still enforced
   under mypy 2.2.0, or did the version regress it? (Falsifier before cosmetics.) If regressed, that
   is a real structural finding, not a test edit.
2. Then decide the test's robustness posture: pin mypy to the version these expectations were
   written against, OR make the assertion drift-tolerant (assert the guard *fires on the bypass
   lines* rather than an exact whole-file error-line set). The exact-set assertion is the fragility.
3. Until fixed, the green-gate is red on main for a reason ORTHOGONAL to any new build — sealing
   bp-098 is correct (its work is green); this is logged so the redness is not mistaken for it.
