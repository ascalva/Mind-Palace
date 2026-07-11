#!/usr/bin/env bash
# BP-010 acceptance harness — the A8 status-aware design-note guard, six cases with
# non-vacuous controls (plan §7 Item 13). Isolated temp repo (bp-000/bp-002 pattern);
# exercises the hooks standalone with CLAUDE_PROJECT_DIR pointed at the fixture repo,
# so the REAL repo is never touched. Run from the repo root:
#   bash docs/build-plans/bp-010/acceptance/run.sh
#
# NON-VACUITY: against pre-A8 _lib.py, cases (a) and (e) MUST FAIL (the location
# denylist denies draft writes) — run once before Item 12 lands and record the RED in
# the journal.
set -u
REPO="$(git rev-parse --show-toplevel)"
pass=0; fail=0
ok(){ echo "  PASS — $1"; pass=$((pass+1)); }
no(){ echo "  FAIL — $1"; fail=$((fail+1)); }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
export CLAUDE_PROJECT_DIR="$TMP"

# ── fixture repo ─────────────────────────────────────────────────────────────
cd "$TMP"
git init -q -b main
git config user.email t@t; git config user.name t
mkdir -p .claude/hooks .claude/state docs/design-notes eval/golden
cp "$REPO"/.claude/hooks/*.py "$REPO"/.claude/hooks/*.sh .claude/hooks/
: > .claude/state/active-plan                       # orchestrator posture (no plan)
printf 'kernel\n' > CONSTITUTION.md
printf 'golden\n' > eval/golden/anchor.txt
printf -- '---\nstatus: draft\n---\n\n# draft note\nbody\n'      > docs/design-notes/draft-note.md
printf -- '---\nstatus: ratified\n---\n\n# ratified note\nbody\n' > docs/design-notes/ratified-note.md
printf -- '---\nstatus: superseded\n---\n\n# old note\nbody\n'    > docs/design-notes/superseded-note.md
git add -A && git commit -qm "fixture: notes at draft/ratified/superseded"

SG=".claude/hooks/scope-guard.sh"
JG=".claude/hooks/journal-gate.sh"
scope(){ bash "$SG" --standalone "$1" >/dev/null 2>&1; echo $?; }
stop_audit(){ git diff HEAD > "$TMP/d.diff"; bash "$JG" --standalone --diff-file "$TMP/d.diff" >/dev/null 2>&1; echo $?; }
clean(){ git checkout -q -- . ; git clean -qfd docs eval 2>/dev/null || true; }

echo "═══ A8 acceptance — status-aware design-note guard ═══"

# (a) draft-note write ALLOWS (pre-hoc)
[ "$(scope docs/design-notes/draft-note.md)" = 0 ] \
  && ok "(a) draft note Edit/Write ALLOWED" || no "(a) draft note write denied"

# (b) ratified body-only write DENIES (pre-hoc, content guard — Correction 1)
[ "$(scope docs/design-notes/ratified-note.md)" = 2 ] \
  && ok "(b) ratified note write DENIED pre-hoc" || no "(b) ratified note write allowed"

# (b2) superseded is immutable historical record too
[ "$(scope docs/design-notes/superseded-note.md)" = 2 ] \
  && ok "(b2) superseded note write DENIED pre-hoc" || no "(b2) superseded note write allowed"

# (e) NEW note at draft ALLOWS (no on-disk status yet)
[ "$(scope docs/design-notes/brand-new-note.md)" = 0 ] \
  && ok "(e) new-note creation ALLOWED" || no "(e) new-note creation denied"

# (f1) hard denylist untouched
[ "$(scope CONSTITUTION.md)" = 2 ] && [ "$(scope eval/golden/anchor.txt)" = 2 ] \
  && ok "(f1) CONSTITUTION.md + eval/golden still DENY" || no "(f1) hard denylist regressed"

# (c1) Bash body-only edit of a ratified note BLOCKS at Stop (HEAD-keyed — Correction 2)
echo "tampered" >> docs/design-notes/ratified-note.md
[ "$(stop_audit)" = 2 ] && ok "(c1) Bash body edit of ratified BLOCKS at Stop" \
                        || no "(c1) Bash body edit escaped the Stop audit"
clean

# (c2) Bash DELETION of a ratified note BLOCKS at Stop
rm docs/design-notes/ratified-note.md
[ "$(stop_audit)" = 2 ] && ok "(c2) deletion of ratified BLOCKS at Stop" \
                        || no "(c2) deletion escaped the Stop audit"
clean

# (d) laundering: flip ratified→draft then edit — pre-hoc reads on-disk (still ratified)
#     and the Bash form must be caught by the HEAD comparison regardless of tree status
[ "$(scope docs/design-notes/ratified-note.md)" = 2 ] || no "(d-pre) pre-hoc missed"
python3 - <<PY
from pathlib import Path
p = Path("docs/design-notes/ratified-note.md")
p.write_text(p.read_text().replace("status: ratified", "status: draft") + "laundered\n")
PY
[ "$(stop_audit)" = 2 ] && ok "(d) ratified→draft laundering BLOCKS at Stop (HEAD-keyed)" \
                        || no "(d) laundering escaped — the exact Correction-2 hole"
clean

# (d2) comment-evasion parity (A5): laundering to 'draft   # x' must still block
python3 - <<PY
from pathlib import Path
p = Path("docs/design-notes/ratified-note.md")
p.write_text(p.read_text().replace("status: ratified", "status: draft   # totally a draft"))
PY
[ "$(stop_audit)" = 2 ] && ok "(d2) comment-evasion laundering BLOCKS (A5 parity on HEAD read)" \
                        || no "(d2) comment evasion slipped the HEAD comparison"
clean

# (f2) A3 regression: Bash-minted UNTRACKED note at status: ratified still blocks
printf -- '---\nstatus: ratified\n---\n\n# forged blessing\n' > docs/design-notes/forged.md
[ "$(stop_audit)" = 2 ] && ok "(f2) untracked Bash-minted ratified note BLOCKS (A3 intact)" \
                        || no "(f2) untracked blessing regression"
rm -f docs/design-notes/forged.md

# (g) control: a clean tree does NOT block (the gate must not become noise)
[ "$(stop_audit)" = 0 ] && ok "(g) clean tree passes the Stop audit (no false block)" \
                        || no "(g) clean tree blocked — gate is noise"

echo "──────────────────────────────────────────────────────"
echo "PASS=$pass FAIL=$fail"
[ "$fail" = 0 ]
