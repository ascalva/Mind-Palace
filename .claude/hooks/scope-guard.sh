#!/usr/bin/env bash
# scope-guard — PreToolUse(Edit|Write|MultiEdit): deny out-of-scope file writes.
# The pre-hoc half of the two-layer write enforcement (design-note §6). Reads the
# active plan's write_scope capability; denies anything outside it (+ the plan's
# own journal, + docs/findings/**), and enforces the foundation-file denylist
# beneath every session, orchestrator included.
#
# Dual-mode:  hook (stdin JSON)  |  --standalone <file_path>
# Fail posture: fail-open, fail-loud — on machinery error, emit a conspicuous
# HOOK-FAILURE line + journal marker and let the write proceed (§6).
NAME="scope-guard"
ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
LIB="$ROOT/.claude/hooks/_lib.py"
HOOK_INTENTIONAL=0

fail_loud() {
  printf 'HOOK-FAILURE %s: %s — enforcement NOT applied\n' "$NAME" "$1" >&2
  python3 "$LIB" marker "HOOK-FAILURE $NAME: $1 — enforcement NOT applied" >/dev/null 2>&1 || true
}
trap 'rc=$?; [ "$HOOK_INTENTIONAL" = 1 ] || fail_loud "unexpected exit rc=$rc"' EXIT

if [ "${1:-}" = "--standalone" ]; then
  shift
  out="$(python3 "$LIB" scope-check "${1:-}")"; rc=$?
else
  out="$(python3 "$LIB" scope-check-hook)"; rc=$?
fi

if [ "$rc" != 0 ]; then fail_loud "lib error (rc=$rc)"; HOOK_INTENTIONAL=1; exit 0; fi
case "$out" in
  ALLOW*) HOOK_INTENTIONAL=1; exit 0 ;;
  DENY:*) HOOK_INTENTIONAL=1; printf '%s\n' "${out#DENY: }" >&2; exit 2 ;;
  *)      fail_loud "unrecognized decision: $out"; HOOK_INTENTIONAL=1; exit 0 ;;
esac
