---
name: build-plan
description: Semantics of the build-plan template — write_scope as capability, context manifests, runnable acceptance, and pinning interfaces inline so a builder never infers design. Use when authoring or reviewing a build plan.
---

# build-plan — template semantics

A build plan is a **capability plus a contract**: it grants exactly the write
surface a session needs and tells a fresh agent everything it must know without
reading the design. Template: `docs/templates/build-plan.md`. Filled reference:
`docs/build-plans/bp-000/plan.md`.

## Field semantics

- **`write_scope` (the capability).** Glob list, least-privilege. This is
  mechanically enforced by `scope-guard` (pre-hoc deny) and the `journal-gate`
  audit (post-hoc, catches Bash writes) — not a suggestion (§2, §6). Grant the
  narrowest set of globs that lets the plan close. The plan's own `plan.md` and
  `journal.md`, and `docs/findings/**`, are always writable and need not be listed.
  Never include a foundation file (`CONSTITUTION.md`, `docs/design-notes/**`,
  `eval/golden/**`) — the denylist overrides write_scope regardless.
- **`context_manifest` (the read list).** Ordered. A fresh agent reads exactly
  these, in order, and can then build. If building needs a file not listed, that
  is a manifest defect — the journal records the delta and a richer resume/plan
  fixes it. Keep it minimal and sufficient.
- **`acceptance` (runnable).** Each criterion is checkable by a machine or a
  crisp observation: a test passes, a file parses, a command exits 0, a hook
  denies with the right reason. Avoid "works well." Each maps to a journal entry.
- **`non_goals` / `stop_conditions`.** Non-goals prevent scope creep; stop
  conditions name what ends the session early (a `blocker` finding; an
  irreversible scope breach). Both make the boundary explicit.
- **`session_budget: 1`.** Always one. Plans are session-sized by construction.

## Pin interfaces inline — the cardinal rule

Copy every signature, schema, invariant, and constant the builder must honor
**verbatim** into the plan's "Interfaces pinned inline" section. Never write "see
the design note" or "follow the existing pattern." The builder must be able to
build correctly with *only* the plan + manifest + journal in context. A plan that
forces the builder to infer design is defective — that inference is exactly where
drift enters. When in doubt, over-pin.

## Status lifecycle

`proposed → ready → in-progress → complete | parked | superseded`.
- `proposed→ready` is the owner's blessing (hand edit; `gate-guard` denies agents).
- `ready→in-progress` is `/build`. `in-progress→complete` is the orchestrator on
  acceptance. `→parked` **requires** a `re_entry` string. `→superseded` mints P′
  on a warrant finding (three-place, never edit-in-place).
