---
type: build-plan
id: bp-demo
status: proposed
created: 2026-07-05
updated: 2026-07-05
links:
  - docs/design-notes/agent-workflow.md
objective: "Add a /status command that prints the current session brief on demand."
contract: builder
design_ref: "docs/design-notes/agent-workflow.md §6 (session-brief) — graduated for the criterion-4 positive path"
write_scope:
  - ".claude/commands/status.md"
context_manifest:
  - ".claude/hooks/session-brief.sh   # the brief this command re-emits"
  - ".claude/hooks/_lib.py            # brief subcommand"
acceptance:
  - "1. `/status` prints the session brief (plans by status, unswept findings, open owner questions, active plan)."
non_goals:
  - "Changing the brief's content or the SessionStart hook."
stop_conditions:
  - "A blocker finding."
session_budget: 1
re_entry: null
supersedes: null
superseded_by: null
warrant: null
---

# bp-demo — /status command  (BP-000 acceptance demonstration)

**Synthetic.** This plan exists only to demonstrate criterion 4's positive path:
`/graduate` run against a genuinely ratified note (`dn-agent-workflow`) emits a
**well-formed `proposed` plan** — every required front-matter field present,
least-privilege `write_scope`, ordered `context_manifest`, runnable `acceptance`,
interfaces pinned. It is not a scheduled plan; the owner readies real plans by
hand. Safe to delete after BP-000.

## Interfaces pinned inline
`/status` re-emits `bash .claude/hooks/session-brief.sh --standalone` output as a
slash command (`.claude/commands/status.md`, front-matter `description`).
