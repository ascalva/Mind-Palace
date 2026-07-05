#!/usr/bin/env bash
# journal-gate — Stop: block session close on an unfinished obligation. This is
# the post-hoc backstop that catches the Bash-mediated writes the pre-hoc guards
# cannot see (design-note §6). Blocks close when, with a plan active: (a) the
# journal mtime predates the last commit, or (b) the worktree holds out-of-scope
# changes; and, in every session: (c) the diff since the session baseline
# contains a blessing transition. Pre-hoc porous, post-hoc tight.
#
# Dual-mode:  hook (Stop event)  |  --standalone [--diff-file <path>]
# Fail posture: fail-open, fail-loud (§6). A block is exit 2 with a reason.
NAME="journal-gate"
ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
LIB="$ROOT/.claude/hooks/_lib.py"
HOOK_INTENTIONAL=0

fail_loud() {
  printf 'HOOK-FAILURE %s: %s — enforcement NOT applied\n' "$NAME" "$1" >&2
  python3 "$LIB" marker "HOOK-FAILURE $NAME: $1 — enforcement NOT applied" >/dev/null 2>&1 || true
}
trap 'rc=$?; [ "$HOOK_INTENTIONAL" = 1 ] || fail_loud "unexpected exit rc=$rc"' EXIT

[ "${1:-}" = "--standalone" ] && shift
out="$(python3 "$LIB" stop-audit "$@")"; rc=$?

if [ "$rc" != 0 ]; then fail_loud "lib error (rc=$rc)"; HOOK_INTENTIONAL=1; exit 0; fi
case "$out" in
  ALLOW*)  HOOK_INTENTIONAL=1; exit 0 ;;
  BLOCK:*) HOOK_INTENTIONAL=1; printf '%s\n' "${out#BLOCK: }" >&2; exit 2 ;;
  *)       fail_loud "unrecognized decision: $out"; HOOK_INTENTIONAL=1; exit 0 ;;
esac
