---
type: finding
id: finding-0027
status: routed
ftype: discovery
origin_plan: bp-006
route: orchestrator
created: 2026-07-11
updated: 2026-07-11
links:
  - docs/design-notes/type-system-as-core-audit.md   # PD-4, the re-entry this feeds
  - docs/build-plans/bp-006/journal.md               # the triage table (the evidence)
resolution: null
---

# finding-0027 — Tier-1 strict audit found ZERO latent defects (T1=0): PD-4 evidence

## What

bp-006's full strict-mypy audit of `core/` (183 errors triaged, every one classified)
produced **zero T1s** — no error corresponded to a reachable incorrect behavior. The
inventory was dominated by T2 (representability: untyped `dict` shapes crossing
boundaries, duck-typed `object` params hiding real interfaces) with T3 friction at ~6%.
One near-miss worth naming: `core/complex/balance.py` reused numpy loop variables as
Python loop variables — harmless today, exactly the pattern that becomes a real defect
under refactoring; the checker surfaced it as five type errors that were one shadowing.

## Why it matters (the pre-written re-entry)

`type-system-as-core-audit.md` PD-4 wired B-1's outcome into the parked Rust/PyO3
privileged-path record: *"if strict typing plus wrappers closes the T1 class on
privileged paths, the split's security motivation weakens to performance-only."* That
condition is now measured fact. The Rust split's remaining case is performance, and
CONVENTIONS already says don't prematurely optimize.

Secondary: PD-2's re-entry (runtime validation) did NOT fire — T1s did not cluster at
the ingestion boundary because there were no T1s. PD-2 stays parked with this recorded.

## Routing

`discovery` → orchestrator. Promotion path: annotate the parked Rust/PyO3 record with
this evidence at its next owner-touched revision (warrant: this finding). No new note
needed; no build licensed. Re-entry — a future T1 on a privileged path reopens the
security half of the split's case.
