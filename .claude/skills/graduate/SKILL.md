---
name: graduate
description: Decompose a ratified design note into session-sized build plans. Use when running /graduate — decomposition rules, session-sizing heuristics, and the split-at-graduation-never-mid-build discipline.
---

# graduate — turning a ratified note into build plans

A design note is a *decision*; a build plan is a *session*. Graduation is the
translation, and it is where scope is set. Do it once, deliberately, from a
single context that holds the whole note.

## The one discipline: split at graduation, never mid-build

All plan boundaries are decided here, with the entire note in view. A builder
mid-session that discovers its plan is too big does **not** re-split — it files a
`spec-defect` finding and parks; the orchestrator re-graduates. This keeps
session boundaries a property of the design, not of a tiring builder's context.
(Subagent-assisted decomposition is parked, §14 — graduate in a single context.)

## Session-sizing heuristic

One plan = one session of an Opus builder at max effort that lands with:
- a single coherent objective statable in one sentence;
- a `write_scope` a reviewer can hold in their head (a handful of globs);
- acceptance criteria that are *runnable* — a test passes, a file exists and
  parses, a command exits 0 — not "looks good";
- interfaces it depends on already pinned (see below), so it reads no design.

Split when any of these breaks: the objective needs an "and"; the write_scope
sprawls across zones (`core/` **and** `edge/`); acceptance can't be checked
without a human judgment call; or the context manifest exceeds what a fresh agent
can read and still build. Prefer more, smaller plans — resume is cheap, oversized
sessions are not.

## Pin interfaces inline (delegates to the build-plan skill)

Every plan copies the signatures, schemas, and invariants its builder must honor
**verbatim** into the plan — never "see the design note." A builder must never
infer design. This is the single most common decomposition defect; get it right
here. (Details: build-plan skill.)

## Procedure

1. Verify `status: ratified` (the command already gated; re-confirm).
2. Read the whole note. List the atomic units of work it licenses.
3. Cluster units into session-sized plans by the heuristic above. Order them by
   dependency; note cross-plan ordering in each plan's body.
4. For each: instantiate `docs/templates/build-plan.md` → `status: proposed`,
   least-privilege `write_scope`, ordered `context_manifest`, runnable
   `acceptance`, explicit `non_goals`/`stop_conditions`, `session_budget: 1`,
   interfaces pinned inline. Create the plan's `journal.md` (alive).
5. Cross-link every plan to the note (`design_ref`, `links`).
6. Emit `proposed` only. The proposed→ready blessing is the owner's, by hand.

## Supersession, not editing

If a plan is later found defective, do not edit it in place. Mint P′ that grounds
on the `spec-defect` warrant finding; flip P to `superseded` with `superseded_by`.
Same three-place relation as claim supersession (`supersession-lifecycle.md`) —
the discredited plan stays inspectable.
