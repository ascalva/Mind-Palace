#!/usr/bin/env bash
# session-brief — SessionStart: emit world-state into context and record the
# close-of-session audit baseline. This is what makes a bare `claude` at root
# land oriented as orchestrator (design-note §6): plans by status, unswept
# findings, open owner questions, the active worktree's plan, book debt.
#
# Dual-mode:  hook (SessionStart)  |  --standalone
# Fail posture: fail-open, fail-loud (§6). Never blocks; stdout joins context.
NAME="session-brief"
# Worktree-aware ROOT (bp-014, warrant finding-0031): prefer the CWD worktree's own
# git toplevel over the inherited CLAUDE_PROJECT_DIR when they DIFFER and that toplevel
# carries its own .claude/state/ — so a hook firing inside a worktree reads THAT
# worktree's active-plan pointer, never the main checkout's (which the delegate harness
# sets CLAUDE_PROJECT_DIR to). Fail-closed: the worktree's own state governs its own
# writes; a broad main-checkout pointer never loosens a narrow worktree builder. Both
# sides realpath-normalized (pwd -P) so /tmp->/private/tmp symlink drift can't spoof the
# comparison. When they agree (or no .claude/state/), byte-identical to before. Kept in
# lock-step with _lib.py:repo_root().
_wt_norm() { [ -n "$1" ] && [ -d "$1" ] && (cd "$1" 2>/dev/null && pwd -P) || printf '%s' "$1"; }
_CWD_TOP="$(git rev-parse --show-toplevel 2>/dev/null)"; _CWD_TOP="$(_wt_norm "$_CWD_TOP")"
_ENV_TOP="$(_wt_norm "${CLAUDE_PROJECT_DIR:-}")"
if [ -n "$_CWD_TOP" ] && [ "$_CWD_TOP" != "$_ENV_TOP" ] && [ -d "$_CWD_TOP/.claude/state" ]; then
  ROOT="$_CWD_TOP"
else
  ROOT="${_ENV_TOP:-${_CWD_TOP:-$(pwd -P)}}"
fi
LIB="$ROOT/.claude/hooks/_lib.py"
HOOK_INTENTIONAL=0

fail_loud() {
  printf 'HOOK-FAILURE %s: %s — enforcement NOT applied\n' "$NAME" "$1" >&2
  python3 "$LIB" marker "HOOK-FAILURE $NAME: $1 — enforcement NOT applied" >/dev/null 2>&1 || true
}
trap 'rc=$?; [ "$HOOK_INTENTIONAL" = 1 ] || fail_loud "unexpected exit rc=$rc"' EXIT

[ "${1:-}" = "--standalone" ] && shift

# Auto-surface the orchestrator's self-resume brief (finding-0035, bp-014 Item 3):
# if the worktree-local .claude/state/resume-brief.md exists, emit it at the TOP of
# the SESSION BRIEF so a fresh session reads its own re-prompt FIRST, zero owner
# action. Resolved under the worktree-aware ROOT (above). Fail-open: a missing or
# unreadable brief never errors the hook — done Bash-side so _lib.py's cmd_brief
# stays pure, and the absent-file case is byte-identical to before (no marker, no
# leading blank line). Only the hook piece of finding-0035 lands here; the template
# + context-economy rule route at /triage (finding-0035 is partially-addressed).
_RB="$ROOT/.claude/state/resume-brief.md"
if [ -r "$_RB" ]; then cat "$_RB"; echo; fi

python3 "$LIB" brief; rc=$?
# Record HEAD for the Stop-gate (c) blessing-diff audit.
mkdir -p "$ROOT/.claude/state"
git -C "$ROOT" rev-parse HEAD > "$ROOT/.claude/state/session-baseline" 2>/dev/null || true

if [ "$rc" != 0 ]; then fail_loud "brief error (rc=$rc)"; fi
HOOK_INTENTIONAL=1
exit 0
