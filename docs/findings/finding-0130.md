---
type: finding
id: finding-0130
status: open
created: 2026-07-21
updated: 2026-07-21
links:
  - docs/build-plans/bp-081/plan.md
  - ops/staging_sweep.py
  - scheduler/cron.py
ftype: spec-defect
origin_plan: bp-081
route: builder
resolution: null
---

# bp-081 Item 10: staging sweep trough-registration needs scheduler internals (Q3 stop-and-raise)

## What
Plan bp-081 Item 10 lands the HYPOTHETICAL-staging expiry sweep as a "trough-tier generation
sweep". Registering it as an actual trough job requires editing `scheduler/cron.py`
(a `SWEEP_KIND` constant, a `sweep_handler`, an `enqueue_sweep` helper, and adding the handler to
`cron_handlers`), and almost certainly `scheduler/router.py` (`_PINNED_KINDS`, since the sweep is
model-free housekeeping like `chat_events`/`integrate`) plus a launcher cadence entry
(`ops/lifecycle/launcher.py`). NONE of those files is in bp-081's `write_scope`
(`core/scope.py`, `core/stores/staging.py`, `core/graph/composed.py`, `ops/staging_sweep.py`, and
the five test files).

Per the plan's own Q3 / §10 stop-and-raise, I did NOT widen scope. `ops/staging_sweep.py` landed as
a **callable** — `run_sweep(store, *, now_wall, dry_run=True)` — fully tested (expiry, tombstone,
generation advance, interval-valued ambiguity-widening wall→generation resolution). The trough
**wiring** is parked.

## Why it matters
Without wiring, expired staged rows are not swept automatically — they remain live in `read_at()`
until some caller invokes `run_sweep`. This is harmless today (nothing stages rows yet; the overlay
is flag-off and not wired at any tier — the H-family influence dispatch is bp-082, gated), but the
housekeeping cadence must be wired before HYPOTHETICAL is used in a live dispatch, or the TTL clock
does not actually expire anything.

## Re-entry condition
A plan whose `write_scope` includes the scheduler surface (`scheduler/cron.py`,
`scheduler/router.py`, `ops/lifecycle/launcher.py`) wires `run_sweep` as a pinned trough job —
sourced from a background/model-free plan like `chat_events` (bp-069 Item 3) / `integrate`
(bp-071 Item 2). Natural home: the bp-082 influence plan (which first makes staged rows live), or a
dedicated small wiring plan. Until then the sweep is caller-invoked only.

## Routing
- `spec-defect` — the plan under-specified the registration seam at graduation (plan §3 Q3
  explicitly anticipated this and instructed stop-and-raise). The builder resolved by landing the
  callable and parking the wiring; the orchestrator batches the wiring into a scheduler-scoped plan.
  No design change — the sweep's shape is settled; only the scheduler edit is deferred.
