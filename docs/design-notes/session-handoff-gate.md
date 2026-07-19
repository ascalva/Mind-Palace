---
type: design-note
id: dn-session-handoff-gate
status: ratified            # draft → ratified → superseded.  draft→ratified is an OWNER-ONLY hand edit.
created: 2026-07-19
updated: 2026-07-19
links:
  - docs/brainstorms/handoff-automation.md
  - docs/design-notes/agent-workflow.md          # §6 — the enforcement contract this extends
  - .claude/hooks/journal-gate.sh                 # the Stop gate this clause joins
  - .claude/hooks/session-brief.sh                # writes both halves of the freshness signal
  - .claude/skills/context-economy                # the resume-brief discipline being enforced
supersedes: null
superseded_by: null
warrant: null
---

# The session-handoff gate — enforcing a fresh resume brief on Stop

> Filed by the chat agent as `draft` (chat-side protocol, §8). Ratification is a
> hand edit by the owner — no command performs it, and `gate-guard` denies any
> agent attempt (§10). `/graduate` refuses this note until `status: ratified`.

## 1. Purpose and scope

Close the one weak link in the session-handoff loop (brainstorm
`handoff-automation`, 2026-07-19). The loop is seal → brief → (kill) → resume.
The *resume* half is already automated — SessionStart auto-loads
`.claude/state/resume-brief.md` (`session-brief.sh:46-47`). The *kill* is one
owner keystroke, deliberately manual. The brief is the gap: authored by habit,
enforced by nothing. This note decides the enforcement — a Stop-audit clause
that refuses to close an orchestrator session which committed work but left the
resume brief stale.

**In scope:** the block condition, its scope key, the freshness signal, failure
posture, and where the clause lives. **Out of scope:** judging brief *quality*
(machine-checking "is this prose sufficient?" is not trusted — the gate checks
that a fresh brief EXISTS, not that it is good); any seal→brief cockpit
keystroke (parked below); any change to authorship or re-entry, which remain
deliberate acts.

## 2. Decision

### 2.1 The clause — stop-audit (e), orchestrator handoff

Extend `cmd_stop_audit` (`.claude/hooks/_lib.py`) with clause **(e)**, joining
(a) journal staleness, (b/b2) scope + immutability, (c) blessing transitions,
(d) cross-checkout bleed. No new hook script and no new Stop entry:
`journal-gate.sh`'s contract is already "Stop: block session close on an
unfinished obligation," and a stale handoff brief is exactly that. A separate
`brief-gate.sh` would duplicate the worktree-aware ROOT preamble and trap
plumbing for zero separation benefit (owner DRY rule).

### 2.2 The block condition

With **no active plan** (orchestrator posture — the same `plan is None` branch
that already exists at `_lib.py:617`):

```
BLOCK  iff  HEAD ≠ content(.claude/state/session-baseline)     # commits happened THIS session
       and  mtime(.claude/state/resume-brief.md) < last-commit time (git log -1 %ct)
```

(a missing `resume-brief.md` counts as infinitely stale — it blocks whenever
commits happened.)

The block reason is the automation: it instructs the agent to write the brief
(per the context-economy skill's resume-brief shape) and close again — the same
nudge mechanics journal-gate (a) already uses on builders. The owner never
thinks about it; the agent is refused until the handoff artifact exists.

### 2.3 The freshness signal — already built

The brainstorm's gating open question (the brief is gitignored, so
"newer than the last commit" does not transfer directly) dissolves against
existing machinery: `session-brief.sh:52` writes
`.claude/state/session-baseline` at every SessionStart. Its **content** (HEAD
at session start) yields "did this session commit?" — the guard that keeps
pure-chat sessions from ever blocking. The last-commit **timestamp** yields
"is the brief fresher than the last unit of committed work?" — identical to
journal-gate (a)'s test, and it encodes the natural ceremony order (seal
commits first, brief last: the brief cites final commit hashes, so it is
necessarily authored after them). No new sentinel; no relocation of the brief
into the committed tree.

### 2.4 Scope key — absence of `active-plan`

Clause (e) fires only when no `active-plan` pointer is set. This answers both
brainstorm scope questions at once:

- **Orchestrator-only by construction** — "bare session at root ⇒ orchestrator
  posture" (CLAUDE.md). Builder sessions have a plan active and are governed by
  journal-gate (a); their handoff artifact is the journal, not the brief.
- **Worktree-correct for free** — delegated builders always carry an
  `active-plan` in their worktree's own `.claude/state/` (the worktree-aware
  ROOT of bp-014), so (e) is silent there. A bare session in a worktree without
  a pointer is treated as orchestrator; acceptable, since (e) only ever asks
  for a resume brief in that worktree's own state dir.

### 2.5 Failure posture and standalone mode — inherited

(e) is a clause inside the existing audit, so it inherits journal-gate's
posture verbatim: fail-open, fail-loud (§6); `--standalone` re-runnable;
`HOOK-FAILURE` marker on unexpected exit. A missing or unreadable
`session-baseline` (first session, cleaned state) skips (e) — fail-open: the
signal cannot be evaluated, so no block.

### 2.6 Accepted porosity (invariants stated honestly)

- **mtime is launderable** by a Bash `touch` — the same porosity journal-gate
  (a) accepts for journals. Pre-hoc porous, post-hoc tight is the standing §6
  posture; the gate targets forgetting, not adversarial evasion.
- **Commit-less sessions can end briefless.** A pure design/chat session leaves
  no mechanical trace to key on; discipline (context-economy) covers that tail.
- **Session resume/clear rewrites the baseline**, so commits made before a
  mid-session compaction are forgotten by (e). Minor: the Stop that *precedes*
  the compaction already ran the audit.
- **Existence, not quality.** A one-line brief passes. Deliberate (brainstorm
  decision): authorship stays a judged act; the gate guarantees the artifact,
  the fresh-agent test judges the prose.

## 3. Consequences

- **One build plan** (papercut-sized, single session): clause (e) in
  `cmd_stop_audit` + integration tests in the established pattern
  (`tests/integration/test_worktree_enforcement.py` invokes `_lib.py
  stop-audit` in fixture repos): blocks on commits+stale-brief, allows on
  no-commits, allows on fresh brief, allows under an active plan, fail-open on
  missing baseline, worktree silence. `write_scope`: `.claude/hooks/**` and
  `tests/integration/**` (bare globs).
- **agent-workflow.md §6** gains clause (e) in its Stop-audit enumeration
  (amendment at build time, cited to this note).
- The handoff loop becomes guaranteed end-to-end: brief enforced (this gate) →
  kill (owner keystroke) → resume auto-loaded (existing SessionStart hook).

## Parked decisions

- **Cockpit seal-motion keybind** (`palace` verb or tmux bind running
  seal→brief as one motion). Default: the orchestrator performs the ceremony by
  hand at unit boundaries. Re-entry: the manual ceremony proves annoying in
  real cockpit use.
- **Brief-quality checking** (machine-judging prose sufficiency). Default:
  existence+freshness only. Re-entry: recurring fresh-but-useless briefs
  observed at resume time — i.e., the fresh-agent test fails despite the gate
  passing.
- **Commit-less-session enforcement.** Default: not enforceable, discipline
  covers it. Re-entry: a signal for "meaningful uncommitted work" emerges
  (e.g., artifact writes tracked by the harness).

## Cross-references

- Brainstorm: `docs/brainstorms/handoff-automation.md` (2026-07-19 capsule)
- Enforcement contract: `docs/design-notes/agent-workflow.md` §6
- Pattern mirrored: `.claude/hooks/journal-gate.sh` + `_lib.py:cmd_stop_audit`
  (clauses (a)–(d) at `_lib.py:571-708`)
- Freshness signal: `.claude/hooks/session-brief.sh:52` (baseline write),
  `:46-47` (brief auto-load)
- Discipline enforced: `.claude/skills/context-economy` (resume-brief shape),
  `.claude/skills/checkpoint` (the fresh-agent test)
- Test pattern: `tests/integration/test_worktree_enforcement.py`
