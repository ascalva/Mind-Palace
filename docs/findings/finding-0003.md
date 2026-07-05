---
type: finding
id: finding-0003
status: routed
created: 2026-07-05
updated: 2026-07-05
links:
  - .claude/hooks/_lib.py
  - docs/design-notes/agent-workflow.md
ftype: spec-defect
origin_plan: bp-000
route: orchestrator
resolution: null
---

# journal-gate (b) over-flags a shared worktree's foundation changes

## What
On the first live Stop event after BP-000 registered its hooks, `journal-gate`
blocked session close, flagging two design notes as modified foundation files:
`docs/design-notes/agent-workflow.md` (the owner's uncommitted hand-ratification,
draft→ratified — also caught by (c)) and `docs/design-notes/core-integrity.md` (a
new, untracked `draft` note the owner filed via the chat-side protocol §8 during
the session). **Neither was written by the session.** The gate cannot attribute
them, so it blocks.

Two coupled causes:
1. **Implementation broadened the spec.** §6 specifies `git diff --name-only` for
   check (b) — which lists **tracked modifications only**. `_lib.py._changed_files`
   uses `git status --porcelain -uall`, which also lists **untracked** files. That
   broadening is deliberate and load-bearing: it is what lets (b) catch an
   untracked Bash-created write (criterion 2's probe). But the same breadth flags
   a legitimate untracked draft note, and any out-of-scope file the owner is
   editing in a **shared** worktree.
2. **Shared worktree during bootstrap.** §4 has parallel work in separate git
   worktrees; a builder's worktree would not contain the owner's chat-side drafts.
   The collision here is an artifact of everyone sharing one worktree with nothing
   committed.

## Why it matters
`spec-fidelity`-adjacent but it bears on the workflow's usability, so it routes to
the owner. Left as-is, any uncommitted draft note or owner edit anywhere in a
shared worktree hard-blocks every session's close — too aggressive for steady
state, though harmless once §4 separate worktrees and prompt commits are in play.

## Re-entry condition
Owner picks a resolution (below), or a real builder session hits this block
outside the bootstrap.

## Options (owner/orchestrator to decide)
- **(a) Steady state — rely on §4 separate worktrees + commit foundation changes
  promptly.** A builder's worktree won't hold the owner's drafts; a ratification
  is a deliberate logged §10 act that gets committed. The bootstrap block clears
  the moment the owner commits their design-note work. *No code change.*
- **(b) Degrade untracked out-of-scope/foundation files to a loud WARN, keep the
  hard BLOCK for tracked-modified ones.** Preserves the untracked-Bash-write
  signal as a warning without hard-blocking legitimate new drafts. Trade-off: a
  rogue untracked Bash write would warn, not block.
- **(c) Scope (b) strictly to `.claude/state/session-baseline`.** Reduces to (b)
  in practice, since untracked files have no baseline delta.

Recommendation: (a) now; consider (b) as a refinement so the shared-worktree case
degrades to a warning. **Not blocking** — BP-000's acceptance stands; this is the
reflection loop reporting on the machinery it just built.

## Addendum — (c) blocks on a *committed* blessing until the baseline re-anchors
Observed minutes later: after the owner committed the ratification (commit
`0b21de6`, an accountable, logged §10 act), check (c) kept firing. Cause: (c) is
`git diff <session-baseline> -- docs/design-notes docs/build-plans`, and the
baseline is pinned to SessionStart HEAD (`a096f3c`, pre-commit). `git diff <old
commit>` spans the intervening commits, so a blessing **committed mid-session**
still shows in the diff and keeps blocking — even though it is now in history and
fully accountable.

Reconciled operationally by re-anchoring `.claude/state/session-baseline` to HEAD
(what a fresh session records at SessionStart anyway); the gate then passed.

Refinement to consider alongside the (b) options: **(c) should diff against
`HEAD`, not the stale session baseline** — i.e., flag an *uncommitted* working-tree
blessing (`git diff HEAD`), since a committed one is already accountable in
history. That also makes long-lived sessions behave like fresh ones. Trade-off:
none obvious — a committed blessing is exactly the "deliberate, logged" §10 state
the gate wants to permit.

## Routing
`spec-defect` → `route: orchestrator`. A design-changing fix would mint an
`agent-workflow.md` amendment warrant-linked here; a pure code refinement is a
one-plan builder change to `_lib.py` (both (b) `-uall` breadth and (c) baseline-vs-HEAD).
