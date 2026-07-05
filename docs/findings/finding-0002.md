---
type: finding
id: finding-0002
status: resolved
created: 2026-07-05
updated: 2026-07-05
links:
  - docs/build-plans/bp-000/plan.md
  - docs/design-notes/agent-workflow.md
ftype: question
origin_plan: bp-000
route: builder
resolution: "Criterion 5 is demonstrated against a toy PROGRESS target under docs/build-plans/bp-000/acceptance/. The canonical docs/PROGRESS.md append is the orchestrator's post-BP-000 single-writer action (§7, §11), deliberately outside BP-000's write scope to protect the 1540-line build log. No spec change needed."
---

# Criterion 5's PROGRESS checkpoint vs BP-000's write scope

## What
Acceptance criterion 5 requires `/triage` to "write a PROGRESS checkpoint." The
canonical target is `docs/PROGRESS.md` (§7, §11). BP-000's granted `write_scope`
deliberately excludes `docs/PROGRESS.md` (a 1540-line existing build log). So the
criterion cannot append to the canonical file within scope.

## Why it matters
A `spec-fidelity` concern the builder can settle against the spec — not an owner
question. The criteria are exercised on **synthetic** fixtures ("a synthetic
finding," "a toy plan"); the PROGRESS write is likewise demonstrable against a toy
PROGRESS target, proving the mechanism without touching the real log. The
orchestrator writes the real checkpoint post-BP-000 as its normal single-writer
action (§11: "Completed plans get a PROGRESS.md checkpoint entry, orchestrator-
written").

## Re-entry condition
None required — resolved in-plan. If the owner later wants BP-000's own completion
checkpoint appended to the canonical `docs/PROGRESS.md`, that is a one-line
orchestrator action outside this plan's scope.

## Routing
`spec-fidelity` → builder resolves, annotates here + journal, continues. Not
escalated.
