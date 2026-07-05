---
type: build-plan
id: toy-plan
status: proposed
created: 2026-07-05
updated: 2026-07-05
links:
  - docs/build-plans/bp-000/plan.md
objective: "BP-000 acceptance fixture: a minimal plan for exercising the hooks and the fresh-agent test."
contract: builder
design_ref: "docs/build-plans/bp-000/plan.md (acceptance criteria 2, 3, 6)"
write_scope:
  - "docs/build-plans/bp-000/acceptance/toy-plan/src/**"
context_manifest:
  - "docs/build-plans/bp-000/acceptance/toy-plan/plan.md"
  - "docs/build-plans/bp-000/acceptance/toy-plan/journal.md"
acceptance:
  - "1. Create src/hello.txt containing exactly one line: hello."
non_goals:
  - "Any write outside toy-plan/src/**."
stop_conditions:
  - "A blocker finding."
session_budget: 1
re_entry: null
supersedes: null
superseded_by: null
warrant: null
---

# toy-plan — BP-000 acceptance fixture

Deliberately trivial. Exercises `scope-guard` (out-of-scope Edit deny), the
`journal-gate` audit (out-of-scope Bash write catch), `gate-guard`
(proposed→ready deny), and the fresh-agent test (§9). Not a real plan; safe to
delete after BP-000.

## Interfaces pinned inline
The single deliverable is `src/hello.txt` — exactly one line: `hello`.
