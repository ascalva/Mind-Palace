---
type: finding
id: finding-0001
status: routed
created: 2026-07-05
updated: 2026-07-05
links:
  - CLAUDE.md
  - CONSTITUTION.md
  - docs/design-notes/agent-workflow.md
ftype: question
origin_plan: bp-000
route: orchestrator
resolution: null
---

# CLAUDE.md replaced the domain digest with a domain pointer — re-home any of it?

## What
BP-000 §12 delivers `CLAUDE.md` as the persona-neutral workflow constitution
(≤ 1 page, §5). The pre-BP-000 `CLAUDE.md` was a different document — the
mind-palace *operating rules* — carrying, on the auto-loaded surface: a 12-item
non-negotiables digest, the repo map, a "current phase" marker, the
build-session-budget guidance, and the live-verification directive. The new file
keeps only a **pointer** to the domain layer (`CONSTITUTION.md` / `BUILD-SPEC.md` /
`CONVENTIONS.md`). Nothing was lost from the repo — the non-negotiables live in
`BUILD-SPEC §3` and `CONSTITUTION.md`, and the old file is in git history — but the
*auto-loaded digest* is gone.

## Why it matters
This is a `direction` concern, so it routes to the owner (§5). The design note is
explicit that the constitution is persona-neutral and lean ("every constitution
token is paid on every turn"), which argues for the pointer-only form. But the
owner may want a subset (e.g. the four hardest non-negotiables) resident every
turn rather than one indirection away. That is a values call, not a mechanical one.

## Re-entry condition
Owner answers `oq-0001` in `docs/inbox/owner-questions.md`; or a later session
files a `direction` finding reporting that a dropped item caused a real miss.
Until then the default holds: pointer-only.

## Routing
`direction` → `route: orchestrator`; batched to `owner-questions.md` as `oq-0001`
with `default_if_unanswered: pointer-only`. Not blocking — BP-000 proceeds.
