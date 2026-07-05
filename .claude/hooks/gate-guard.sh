#!/usr/bin/env bash
# gate-guard — PreToolUse(Edit|Write|MultiEdit): deny blessing transitions.
# The two blessing gates — design-note draft→ratified and plan proposed→ready —
# are owner-manual, made by hand outside any agent session (design-note §10).
# This hook denies either transition pre-hoc, in every session and every role.
# All other status transitions (ready→in-progress→complete|parked|superseded)
# pass. Only fires on files under docs/design-notes/ and docs/build-plans/**/plan.md.
#
# Dual-mode:  hook (stdin JSON)  |  --standalone <file_path> <intended_status>
# Fail posture: fail-open, fail-loud (§6).
NAME="gate-guard"
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
  out="$(python3 "$LIB" gate-check "${1:-}" "${2:-}")"; rc=$?
else
  out="$(python3 "$LIB" gate-check-hook)"; rc=$?
fi

if [ "$rc" != 0 ]; then fail_loud "lib error (rc=$rc)"; HOOK_INTENTIONAL=1; exit 0; fi
case "$out" in
  ALLOW*) HOOK_INTENTIONAL=1; exit 0 ;;
  DENY:*) HOOK_INTENTIONAL=1; printf '%s\n' "${out#DENY: }" >&2; exit 2 ;;
  *)      fail_loud "unrecognized decision: $out"; HOOK_INTENTIONAL=1; exit 0 ;;
esac
