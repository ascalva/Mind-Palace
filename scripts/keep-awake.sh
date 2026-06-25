#!/usr/bin/env bash
# keep-awake.sh — prevent the Mac from sleeping during long builds / runtime.
# Safe for clamshell mode on AC power. Screen lock, screensaver, and display
# sleep still work normally — only *system* sleep is blocked, so compute keeps
# running.
#
# Usage:
#   ./scripts/keep-awake.sh             # keep the system awake until Ctrl-C
#   ./scripts/keep-awake.sh -- <cmd>    # keep awake only while <cmd> runs
#
# Note: clamshell needs AC power + an external display/input connected.
# For an unattended setup you can instead hard-disable AC sleep with:
#   sudo pmset -c disablesleep 1   (revert: sudo pmset -c disablesleep 0)

set -euo pipefail

# Flags: -i no idle sleep, -m no disk sleep, -s no system sleep (AC only).
# Display sleep is intentionally left alone.
FLAGS="-ims"

if [[ "${1:-}" == "--" ]]; then
  shift
  [[ $# -gt 0 ]] || { echo "error: no command given after --" >&2; exit 1; }
  exec caffeinate $FLAGS "$@"
fi

echo "Keeping this Mac awake (no idle/disk/system sleep). Press Ctrl-C to stop."
echo "Clamshell reminder: needs AC power + an external display/input attached."
exec caffeinate $FLAGS
