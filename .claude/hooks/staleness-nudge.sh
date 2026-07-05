#!/usr/bin/env bash
# staleness-nudge — UserPromptSubmit: if the active journal is stale relative to
# HEAD, inject a one-line reminder into context (design-note §6). Advisory only:
# it never blocks. The Stop-gate is the hard backstop; this is the soft nudge
# that keeps staleness bounded to one criterion between semantic boundaries.
#
# Dual-mode:  hook (UserPromptSubmit)  |  --standalone
# Fail posture: fail-open, fail-loud (§6).
NAME="staleness-nudge"
ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
LIB="$ROOT/.claude/hooks/_lib.py"
HOOK_INTENTIONAL=0

fail_loud() {
  printf 'HOOK-FAILURE %s: %s — enforcement NOT applied\n' "$NAME" "$1" >&2
  python3 "$LIB" marker "HOOK-FAILURE $NAME: $1 — enforcement NOT applied" >/dev/null 2>&1 || true
}
trap 'rc=$?; [ "$HOOK_INTENTIONAL" = 1 ] || fail_loud "unexpected exit rc=$rc"' EXIT

[ "${1:-}" = "--standalone" ] && shift

python3 "$LIB" staleness; rc=$?
if [ "$rc" != 0 ]; then fail_loud "lib error (rc=$rc)"; fi
HOOK_INTENTIONAL=1
exit 0
