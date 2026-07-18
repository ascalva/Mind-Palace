---
type: finding
id: finding-0107
status: open
created: 2026-07-18
updated: 2026-07-18
links:
  - ops/lifecycle/launcher.py                      # _report_snapshot builds OpsView WITHOUT a drift provider
  - core/ops_view.py                               # snapshot(): None when _drift is None (":69 not measured")
  - ops/lifecycle/snapshot.py                      # build_status carries the two health fields
re_entry: builder — make `status` show the last MEASURED drift/constitution (or label it "not measured"), not a bare None
ftype: codebase
origin_plan: orchestrator
route: builder
resolution: null
---

# `palace status` always prints `drift/constitution: None` — the drift provider is never wired

## What
`Launcher._report_snapshot` (the `status` command) builds its read-only view as
`OpsView.over(open_attestation_store(cfg), open_ledger(cfg))` — it does NOT pass the optional
`drift=` provider. So `OpsView.drift_report()` returns `None` (`core/ops_view.py:136`), and
`snapshot()` sets BOTH `drift_within_tolerance=None` and `constitution_intact=None`
(`ops_view.py:144-145`; the field comment: *"None = not measured this session"*). Therefore `status`
ALWAYS prints:

    drift within tolerance: None   constitution intact: None

regardless of the daemon's actual health — it is structural, not a live signal. (The dormant
`Components.snapshot` hook is a no-op since the edge monitor was retired, so nothing else populates it
either.)

## Why it matters
A bare `None` beside "constitution intact" reads to a human as "unknown / possibly broken" and caused
real worry (owner, 2026-07-18) during the recovery. The ACTUAL Constitution-integrity check is green
and already shown in preflight (`✓ constitution: matches blessed anchor …`); this second field is a
different, runtime conformance/drift measurement that `status` simply never computes. The display
conflates "not measured" with a health verdict.

## Fix (builder, low priority)
One of:
- Have `status` READ the last persisted drift/eval report (if the system keeps one) and show that
  measured value with its timestamp ("constitution intact: yes (as of <t>)").
- Or render the unmeasured state honestly — e.g. "drift/constitution: not measured this session (run
  `mind-palace eval`)" — so `None` never masquerades as a verdict.
- Optionally wire the `drift=` provider through `_report_snapshot` if a cheap read of the latest
  report is available (do NOT trigger a full golden-set eval from `status`).

## Routing
`codebase` → builder (status/tooling). Surfaced by the recovery-incident diagnosis; sibling to
finding-0106 (the wrapper-verb gap). NOT a health defect — a display-honesty defect.
