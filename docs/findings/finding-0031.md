---
type: finding
id: finding-0031
status: routed
ftype: discovery
origin_plan: bp-007
route: orchestrator
created: 2026-07-11
updated: 2026-07-11
links:
  - docs/build-plans/bp-007/journal.md      # the episode (documented workaround)
  - .claude/skills/delegate/SKILL.md        # the mode this infrastructure serves
resolution: null
---

# finding-0031 — Enforcement state bleeds across worktrees: the active-plan pointer is not worktree-local in practice

## What

During the first PARALLEL delegated builds (bp-007 building while the orchestrator ran
bp-010 in the main checkout), bp-007's builder found its Edit/Write tool calls being
denied against **bp-010's** write_scope: the main checkout's `.claude/state/active-plan`
pointer governed the WORKTREE session's enforcement. Root cause: hook wrappers resolve
`ROOT` as `${CLAUDE_PROJECT_DIR:-git toplevel}`, and the harness sets
`CLAUDE_PROJECT_DIR` to the MAIN project directory even for worktree-isolated agents —
so `active_plan_path()` reads main's pointer, not the worktree's. The design intent
("the pointer is worktree-local … concurrent worktrees never collide on enforcement
state", `_lib.py` docstring) holds for the file layout but not for the env resolution.

The builder worked around it via Bash-mediated writes (in-scope by eye, documented in
its journal); the condition self-resolved when the orchestrator's bp-010 session
cleared the pointer.

## Why it matters

The delegate mode (owner rule 2026-07-11) makes parallel worktree builders the normal
case. Cross-bleed means: (a) a builder can be wrongly DENIED (this episode — friction,
Bash workarounds erode the pre-hoc layer's value), and (b) potentially wrongly ALLOWED
(a main-checkout pointer with a broad scope would loosen a worktree builder — the unsafe
direction). The pre-hoc guard's per-plan capability model silently degrades to
whichever checkout wrote the pointer last.

## Recommended direction (route: orchestrator)

Make ROOT resolution worktree-aware in the hook wrappers: prefer the PROCESS's actual
working tree (`git rev-parse --show-toplevel` from CWD) over the inherited
`CLAUDE_PROJECT_DIR` when they disagree AND `.claude/state/` exists in the working tree;
or have the Agent-tool spawn set `CLAUDE_PROJECT_DIR` to the worktree path. Small,
hooks-scoped fix (bp-010's surface family); verify with a two-worktree harness case.

## Re-entry

Parked until the next hooks-scoped plan (or fold into A7's implementation plan). Trigger
that reopens immediately: any parallel-builder denial or allowance traceable to a
pointer outside its own worktree.
