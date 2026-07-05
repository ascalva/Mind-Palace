---
name: checkpoint
description: The journal contract — semantic-boundary triggers, the required section shape, and the fresh-agent test that makes context disposable. Use when writing a journal entry or deciding whether to resume vs compact.
---

# checkpoint — the journal contract (§9)

The journal is the deliverable of the note-taking obligation: it makes context
disposable. `docs/build-plans/<id>/journal.md`, alive while `in-progress`, sealed
by `/triage` on completion. **Committed** — history, not scratch.

## When to write — semantic boundaries, not a feeling

Write at every semantic boundary:
- an acceptance criterion closed,
- a commit made,
- a finding filed.

Do **not** rely on "context feels high." Boundaries plus the Stop gate make
staleness structurally bounded to one criterion. If a compaction fires mid-
criterion, the `compaction-marker` line tells the next turn to re-verify against
the journal, not the summary.

## Required sections — newest entry first

1. **Status line** — one sentence, the current truth.
2. **Completed** — per criterion, with commit refs.
3. **In-flight** — what is mid-motion and its exact state.
4. **Next action** — single and concrete enough to execute without thought.
5. **Open questions** — typed and routed (or finding-linked).
6. **Context-manifest delta** — files read beyond the manifest; files that proved
   irrelevant.
7. **Markers** — mechanical lines appended by hooks (compactions, audits,
   HOOK-FAILUREs). Keep these in a `## Markers` section at the file's end where
   hooks append.

## The fresh-agent test — the acceptance bar

A new session given **only** `plan.md` + this journal + the write-scope files must
continue **without asking anything already answered**. If it would have to ask,
the journal is under-specified — enrich the Next action and In-flight before you
stop.

When this holds, **resume strictly dominates compaction**: the journal is
audited, committed, reviewable; a compaction summary is lossy and unreviewable.
Norm: kill sessions freely between criteria and resume fresh (`/resume`);
compaction is the mid-criterion fallback only.

## On the way out

The Stop gate (`journal-gate`) blocks close if the journal predates the last
commit, if the worktree holds out-of-scope changes, or if the diff since baseline
contains a blessing transition. So the last act before stopping is always a fresh,
truthful journal entry.
