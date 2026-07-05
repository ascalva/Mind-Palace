---
description: Resume an in-progress plan in a fresh session from its journal (fresh-agent test).
argument-hint: <plan-id>
---
Resume build plan `$1` in this fresh session under its contract.

The journal is an audited, committed artifact; a compaction summary is lossy and
unreviewable. Resume strictly dominates compaction when the journal holds (§9).

1. Confirm `docs/build-plans/$1/plan.md` is `in-progress` (if `ready`, use
   `/build`; if `complete`/`parked`/`superseded`, report and stop).
2. Set the worktree pointer: `printf '%s\n' "docs/build-plans/$1/plan.md" >
   .claude/state/active-plan`.
3. Load, in order: `plan.md`, then `journal.md` (newest entry first), then the
   context-manifest **delta** the journal records (files already read, files that
   proved irrelevant) — read the manifest minus what the journal says is done.
4. Adopt the plan's contract (builder/scribe), exactly as `/build` does.
5. **Fresh-agent test** (the checkpoint skill's bar): you must be able to state
   the single concrete Next action and continue **without asking anything the
   journal already answers**. If you cannot, the journal was under-specified —
   file a `spec-fidelity` finding noting what was missing and checkpoint richer,
   rather than guessing.
6. Execute the Next action; checkpoint at the next semantic boundary.
