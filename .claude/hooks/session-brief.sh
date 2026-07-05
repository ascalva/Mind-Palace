#!/usr/bin/env bash
# session-brief — SessionStart: emit world-state into context and record the
# close-of-session audit baseline. This is what makes a bare `claude` at root
# land oriented as orchestrator (design-note §6): plans by status, unswept
# findings, open owner questions, the active worktree's plan, book debt.
#
# Dual-mode:  hook (SessionStart)  |  --standalone
# Fail posture: fail-open, fail-loud (§6). Never blocks; stdout joins context.
NAME="session-brief"
ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
LIB="$ROOT/.claude/hooks/_lib.py"
HOOK_INTENTIONAL=0

fail_loud() {
  printf 'HOOK-FAILURE %s: %s — enforcement NOT applied\n' "$NAME" "$1" >&2
  python3 "$LIB" marker "HOOK-FAILURE $NAME: $1 — enforcement NOT applied" >/dev/null 2>&1 || true
}
trap 'rc=$?; [ "$HOOK_INTENTIONAL" = 1 ] || fail_loud "unexpected exit rc=$rc"' EXIT

[ "${1:-}" = "--standalone" ] && shift

python3 "$LIB" brief; rc=$?
# Record HEAD for the Stop-gate (c) blessing-diff audit.
mkdir -p "$ROOT/.claude/state"
git -C "$ROOT" rev-parse HEAD > "$ROOT/.claude/state/session-baseline" 2>/dev/null || true

if [ "$rc" != 0 ]; then fail_loud "brief error (rc=$rc)"; fi
HOOK_INTENTIONAL=1
exit 0
