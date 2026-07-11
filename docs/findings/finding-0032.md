---
type: finding
id: finding-0032
status: routed
ftype: direction
origin_plan: bp-008
route: orchestrator
created: 2026-07-11
updated: 2026-07-11
links:
  - docs/build-plans/bp-008/journal.md   # Entry 4: the demo-branch episode
  - .gitlab-ci.yml                        # type-gate and ratchet jobs (lint stage)
resolution: null
---

# finding-0032 — Should CI gates (`type-gate`, `ratchet`) run via `needs: []`, independent of the `.pre` stage?

## What

While demonstrating bp-008's falsifiers on the throwaway `bp-008-falsifier-demo`
branch, the builder hit a stage-sequencing snag: the `.pre`-stage `next-version` job
(from the external `pipeline-fragments` semantic-release template — not ours to edit)
**failed** on that non-main branch, and GitLab's default stage ordering then
**skipped** the later `lint`-stage `type-gate` job entirely. The builder added
`needs: []` to `type-gate` (commit `aef6e86`, which lives ONLY in the discarded demo
history) to decouple it from stage order — it then ran immediately regardless of
`.pre`. The builder argued in its journal that this is a *permanent* improvement, not
a demo-only workaround.

At seal, the orchestrator **did not merge** `needs: []` into main: it arrived on a
demo commit, main's `next-version` succeeds normally (that is how releases are cut),
so the decoupling is not *required* for correctness on main, and matching the sibling
`ratchet` job's shape (no `needs:`) is the conservative default. main's `type-gate`
therefore mirrors `ratchet` exactly, as bp-008 Item 9 was authored.

## Why it matters

The robustness argument is real and general: if `.pre`/release tooling ever goes red
on main (it has — cf. `9bca225`, "403 turned cut releases red"), the current
stage-sequenced layout means the **type gate silently does not run** for that push.
A gate that stops firing exactly when the pipeline is already unhealthy is a weak
gate. But the fix is not `type-gate`-specific — the identical exposure applies to
`ratchet` (same `lint` stage, same implicit dependence on `.pre` succeeding). So this
is a CI-topology decision about *all* the code gates, not a one-job tweak, which is
why it is routed rather than quietly adopted.

## Recommended direction (route: orchestrator → owner)

Decide as a policy for the code gates together: add `needs: []` to **both**
`type-gate` and `ratchet` (decouple the code gates from release/`.pre` tooling so
they always run on a code change), OR consciously keep them stage-sequenced and
accept that a red `.pre` suppresses them. If adopted, land it in one small
CI-scoped plan touching both jobs, with a note in `.gitlab-ci.yml` explaining why the
code gates carry `needs: []` and the release jobs do not.

## Re-entry

Parked for the next CI-scoped plan (or fold into a broader `.gitlab-ci.yml` revision).
Trigger that reopens immediately: any push to main where a `.pre`/release failure is
observed to have skipped `type-gate` or `ratchet`.
