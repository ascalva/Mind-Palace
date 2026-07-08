---
type: build-plan
id: bp-005
status: ready
design_ref: []
contract: builder
write_scope:
  - "docs/design-notes/**"
  - "docs/research/**"
  - "docs/build-plans/bp-005/**"
  - "docs/findings/**"
session_budget: 1
depends_on: []
parallelizable_with: []
created: 2026-07-07
updated: 2026-07-07
re_entry: null
supersedes: null
superseded_by: null
warrant: null
---

# Build Plan — Convert remaining design/research notes to front-matter format

## 1. Objective

Every design/research note not already carrying machine front-matter gets the
template block prepended, landing at `status: draft`. Front-matter only — prose
untouched. No archives (owner ruling: zero physical archives). No `ratified` or
`superseded` may be written — done or owner-only.

## 5. Write scope

As front-matter. Out of scope: docs/audits/\*\*, docs/PROGRESS.md, any status
transition to ratified/superseded, any prose edit.
