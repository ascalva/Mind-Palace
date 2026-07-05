#!/usr/bin/env bash
# compaction-marker — PreCompact: append a mechanical marker line to the active
# journal so the post-compaction turn knows a compaction occurred and re-verifies
# state against the journal rather than trusting the (lossy) summary (§6).
#
# Dual-mode:  hook (PreCompact)  |  --standalone [marker text]
# Fail posture: fail-open, fail-loud (§6).
NAME="compaction-marker"
ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
LIB="$ROOT/.claude/hooks/_lib.py"
HOOK_INTENTIONAL=0

fail_loud() {
  printf 'HOOK-FAILURE %s: %s — enforcement NOT applied\n' "$NAME" "$1" >&2
  python3 "$LIB" marker "HOOK-FAILURE $NAME: $1 — enforcement NOT applied" >/dev/null 2>&1 || true
}
trap 'rc=$?; [ "$HOOK_INTENTIONAL" = 1 ] || fail_loud "unexpected exit rc=$rc"' EXIT

[ "${1:-}" = "--standalone" ] && shift
TEXT="${*:-compaction event — re-verify state against this journal, not the summary (§6)}"

python3 "$LIB" marker "$TEXT"; rc=$?
if [ "$rc" != 0 ]; then fail_loud "lib error (rc=$rc)"; fi
HOOK_INTENTIONAL=1
exit 0
