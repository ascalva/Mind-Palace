# bp-000-acceptance

Brainstorm note seeded by the criterion-4 `/capture` demonstration. This is what
`/capture bp-000-acceptance` produces when the owner pastes a session capsule:
the capsule is appended verbatim under a timestamped heading. Safe to delete
after BP-000.

## 2026-07-05T00:00:00Z (captured)

```capsule
topic: bp-000-acceptance
date: 2026-07-05

decisions:
  - The BP-000 acceptance criteria are exercised via the hooks' standalone path
    and toy/stub/synthetic fixtures under docs/build-plans/bp-000/acceptance/.

parked:
  - decision: whether BP-000's own completion checkpoint lands in the canonical
      docs/PROGRESS.md
    default: toy PROGRESS target for the demo; canonical append is a post-BP-000
      orchestrator action
    re_entry: owner asks for the canonical checkpoint (finding-0002)

open_questions:
  - Should CLAUDE.md re-home any of the pre-BP-000 domain digest? (oq-0001)

next_steps:
  - Run docs/build-plans/bp-000/acceptance/run.sh and record results in the journal.

references:
  - docs/design-notes/agent-workflow.md
  - docs/build-plans/bp-000/plan.md
```
