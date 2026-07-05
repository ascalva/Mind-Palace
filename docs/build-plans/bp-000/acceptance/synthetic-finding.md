---
type: finding
id: finding-9001
status: routed
created: 2026-07-05
updated: 2026-07-05
links:
  - docs/design-notes/agent-workflow.md
ftype: question
origin_plan: toy-plan
route: orchestrator
resolution: null
triage: "2026-07-05 /triage — routed to orchestrator; owner-question drafted in toy-owner-questions.md; checkpoint written to toy-PROGRESS.md."
---

# (Synthetic) Should the session brief show per-plan write_scope inline?

## What
BP-000 acceptance fixture for criterion 5. A `direction` question: should the
`session-brief` list each in-progress plan's `write_scope` inline, or is the plan
id enough? Synthetic — safe to delete after BP-000.

## Why it matters
A `direction` concern, so it routes to the orchestrator, who drafts an owner
question and (on completion) a PROGRESS checkpoint — the exact `/triage` motion
criterion 5 checks.

## Re-entry condition
Owner answers the drafted question; default: plan id only.

## Routing
`direction` → `route: orchestrator`.
