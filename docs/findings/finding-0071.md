---
type: finding
id: finding-0071
status: resolved
created: 2026-07-13
updated: 2026-07-13
links:
  - docs/build-plans/bp-028/plan.md
  - ops/lifecycle/launcher.py
ftype: spec-defect
origin_plan: bp-028
route: orchestrator
resolution: >
  Owner hand-added the three §7 test paths AND ops/lifecycle/launcher.py to bp-028's
  write_scope (2026-07-13). Both halves addressed in-plan: (1) the acceptance tests for
  Items 23–25 were authored (test_research_{driver,cron,foreground}.py, all green);
  (2) the production activation was done in launcher.py — RESEARCH_KIND registered in the
  supervisor handler map + build_task_delegation now receives the librarian, so the daemon
  runs the airlock. Not parked. bp-028 SEALED complete.
---

# bp-028 write_scope omits the §7 test paths (blocks acceptance) + the production handler registration is out of scope

## What

Two grounding gaps surfaced on opening the bp-028 build (both discovered from the code, not
inferred):

1. **The `write_scope` cannot satisfy its own §7 acceptance criteria.** bp-028's
   `write_scope` is `scheduler/**`, `agents/ambassador/**`, `docs/BUILD-SPEC.md` (plus the
   auto-granted journal + `docs/findings/**`). It lists **no test paths**. Every §7 item
   (23/24/25) mandates a unit/integration **acceptance test**, and every sibling code-build
   plan (bp-021/022/024/025/026) explicitly enumerates its test files in `write_scope`. As
   written, the acceptance tests for Items 23–25 cannot be authored — `scope-guard` denies
   any write under `tests/**`. This is a graduation oversight, not a design decision.

   Concretely, the tests the items call for:
   - `tests/integration/test_research_driver.py` (Item 23 — already drafted, denied by scope-guard)
   - `tests/integration/test_research_cron.py` (Item 24 — routing + drain of the research job)
   - a delegate-routing + Ambassador test for Item 25 (extend `test_ambassador_conversation.py`
     or a new `tests/integration/test_research_foreground.py`)

2. **The production daemon handler map + delegate are assembled OUTSIDE `write_scope`.** The
   running daemon builds its handlers dict and the task-delegation closure in
   `ops/lifecycle/launcher.py:193` and `:188` — not under `scheduler/**`. To ACTIVATE the
   airlock in the live daemon, `RESEARCH_KIND` must be registered there and
   `build_task_delegation(...)` must be passed a `librarian` (for the foreground research
   route). Both are one-line wiring changes, but `ops/**` is out of this plan's scope. The
   in-scope `ConversationRuntime` (`scheduler/interface.py`) gives the in-process end-to-end
   proof; the launcher registration is the deploy-facing activation.

## Why it matters

Item 26 (the BUILD-SPEC §16 banner) is in scope and completable. But the plan's CORE
deliverable — a wired, TESTED `emit → collect → rank → surface` chain (Items 23–25) — is
blocked on (1): an invariant-adjacent subsystem (Inv 2/7/11, the outbound airlock) must not
land untested. Correcting the `write_scope` is a capability-surface change to an owner-blessed,
invariant-adjacent plan, so it is owner-gated ("never route around" a scope denial; blessings
owner-by-hand). And without (2), the machinery is built + tested but the live daemon never
runs it.

## Re-entry condition

The owner adds the test paths above to `bp-028`'s `write_scope` (a graduation-oversight fix),
and — optionally, to activate in the daemon — adds `ops/lifecycle/launcher.py` (the two
one-line registrations) or defers that to a follow-up. On write_scope correction, resume
bp-028: author the §7 acceptance tests for Items 23–25, run the five-leg gate, seal.

## Routing

`spec-defect` bearing on an owner-blessed plan's capability surface → orchestrator surfaces
to the owner (this session). Item 23's driver code (`scheduler/research.py`) and Item 26 are
delivered in-scope; Items 24/25 code + all acceptance tests park on the re-entry condition.
