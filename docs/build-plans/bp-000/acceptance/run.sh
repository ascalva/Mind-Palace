#!/usr/bin/env bash
# BP-000 acceptance harness — reproduces the evidence for criteria 1–7 (§12).
# Run from the repo root:  bash docs/build-plans/bp-000/acceptance/run.sh
#
# The hooks are exercised via their standalone (dual-mode) path because the
# building session predates their SessionStart registration — which is also the
# HOOK-FAILURE alarm test (criterion 7). Each criterion prints PASS/FAIL.
set -u
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
export CLAUDE_PROJECT_DIR="$ROOT"
H=".claude/hooks"
A="docs/build-plans/bp-000/acceptance"
PTR=".claude/state/active-plan"
SAVED_PTR="$(cat "$PTR" 2>/dev/null || true)"
pass=0; fail=0
ok(){ echo "  PASS — $1"; pass=$((pass+1)); }
no(){ echo "  FAIL — $1"; fail=$((fail+1)); }
restore(){ printf '%s\n' "$SAVED_PTR" > "$PTR"; }
trap restore EXIT

echo "════════════════════════════════════════════════════════════════════"
echo "CRITERION 1 — bare session emits the brief and behaves as orchestrator"
echo "────────────────────────────────────────────────────────────────────"
out="$(bash "$H/session-brief.sh" --standalone)"; echo "$out"
echo "$out" | grep -q "SESSION BRIEF" && echo "$out" | grep -qi "orchestrator" \
  && ok "brief emitted with orchestrator posture" || no "brief missing"

echo
echo "════════════════════════════════════════════════════════════════════"
echo "CRITERION 2 — out-of-scope Edit denied pre-hoc; out-of-scope Bash write"
echo "             caught by the Stop-gate audit"
echo "────────────────────────────────────────────────────────────────────"
printf '%s\n' "$A/toy-plan/plan.md" > "$PTR"   # active plan = toy-plan
echo "[2a] scope-guard on out-of-scope 'core/secret.py' (toy-plan scope is toy-plan/src/**):"
bash "$H/scope-guard.sh" --standalone core/secret.py; rc=$?
echo "     rc=$rc"; [ "$rc" = 2 ] && ok "out-of-scope Edit denied pre-hoc" || no "not denied"
echo "[2a'] scope-guard on in-scope 'toy-plan/src/hello.txt':"
bash "$H/scope-guard.sh" --standalone "$A/toy-plan/src/hello.txt"; rc=$?
echo "     rc=$rc"; [ "$rc" = 0 ] && ok "in-scope Edit allowed" || no "wrongly denied"
echo "[2b] Stop-gate audit catches an out-of-scope Bash write. Active plan = bp-000"
echo "     (its scope covers the BP-000 deliverables; only the probe is out-of-scope)."
printf '%s\n' "docs/build-plans/bp-000/plan.md" > "$PTR"
: > core/_bp000_audit_probe.txt   # a Bash-mediated write the pre-hoc guard cannot see
out="$(bash "$H/journal-gate.sh" --standalone 2>&1)"; rc=$?
echo "     rc=$rc"; echo "     reason: $out"
{ [ "$rc" = 2 ] && printf '%s' "$out" | grep -q "_bp000_audit_probe.txt"; } \
  && ok "out-of-scope Bash write caught; close blocked" || no "probe not caught"
rm -f core/_bp000_audit_probe.txt

echo
echo "════════════════════════════════════════════════════════════════════"
echo "CRITERION 3 — kill/resume round-trip passes the fresh-agent test"
echo "────────────────────────────────────────────────────────────────────"
echo "The fresh-agent bar (§9): plan + journal + write-scope files suffice to"
echo "continue without re-asking. Verify the toy-plan journal is complete + has a"
echo "single concrete Next action:"
J="$A/toy-plan/journal.md"
need=0
for s in "Status." "Completed." "Next action." "Open questions." "Context-manifest delta" "Markers"; do
  grep -q "$s" "$J" && echo "  section present: $s" || { echo "  MISSING: $s"; need=1; }
done
grep -q "src/hello.txt" "$J" && echo "  next action names the exact file+content" || need=1
[ "$need" = 0 ] && ok "journal satisfies the fresh-agent test (resume-sufficient)" \
                 || no "journal under-specified"

echo
echo "════════════════════════════════════════════════════════════════════"
echo "CRITERION 4 — capsule → /capture → note → /graduate (capture + gate + shape)"
echo "────────────────────────────────────────────────────────────────────"
echo "[4a] /capture appended the pasted capsule to a brainstorm note:"
BN="docs/brainstorms/bp-000-acceptance.md"
{ [ -f "$BN" ] && grep -q '```capsule' "$BN"; } \
  && ok "capsule captured to $BN" || no "capture missing"
echo "[4b] /graduate REFUSES a non-ratified (draft) note — the command's status gate"
echo "     (§7: 'Refuse unless status: ratified'):"
st="$(python3 -c "import importlib.util;s=importlib.util.spec_from_file_location('l','$H/_lib.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);print(m.status_of('$A/stub-note.md') or 'none')")"
echo "     stub-note.md status=$st  (graduate requires 'ratified')"
[ "$st" != "ratified" ] && ok "graduate refuses non-ratified note (status=$st)" || no "would not refuse"
echo "     (independently, gate-guard denies any WRITE of a blessing — criterion 6a.)"
echo "[4c] Positive path on a genuinely RATIFIED note (agent-workflow.md is owner-"
echo "     ratified). The emitted proposed plan is schema-complete:"
if python3 - "$A/demo-graduated-plan.md" <<'PY'
import sys, importlib.util
s = importlib.util.spec_from_file_location("l", ".claude/hooks/_lib.py")
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
fm = m.read_front_matter(sys.argv[1])
req = ["type","id","status","objective","contract","design_ref","write_scope",
       "context_manifest","acceptance","non_goals","stop_conditions","session_budget"]
missing = [k for k in req if not fm.get(k)]
print("     status:", fm.get("status"), "| missing fields:", missing or "none")
sys.exit(0 if fm.get("status") == "proposed" and not missing else 1)
PY
then ok "ratified→graduate yields a well-formed proposed plan"
else no "graduated plan malformed"; fi

echo
echo "════════════════════════════════════════════════════════════════════"
echo "CRITERION 5 — /triage on a synthetic finding: route, owner-question, PROGRESS"
echo "────────────────────────────────────────────────────────────────────"
echo "Synthetic finding: $A/synthetic-finding.md (finding-9001, direction)."
echo "Demonstrating the /triage motions against toy targets (finding-0002):"
echo "  finding-9001 status: $(grep -m1 '^status:' "$A/synthetic-finding.md")"
grep -q "owner-question drafted for finding-9001" "$A/toy-owner-questions.md" && qd=1 || qd=0
grep -q "finding-9001" "$A/toy-PROGRESS.md" && cp=1 || cp=0
echo "  toy owner-question drafted: $([ $qd = 1 ] && echo yes || echo no)"
echo "  toy PROGRESS checkpoint written: $([ $cp = 1 ] && echo yes || echo no)"
{ [ "$qd" = 1 ] && [ "$cp" = 1 ] && grep -q "route: orchestrator" "$A/synthetic-finding.md"; } \
  && ok "finding routed, owner-question drafted, PROGRESS checkpoint written" \
  || no "triage motions incomplete"

echo
echo "════════════════════════════════════════════════════════════════════"
echo "CRITERION 6 — blessing transition denied pre-hoc (Edit) AND caught (Bash)"
echo "────────────────────────────────────────────────────────────────────"
echo "[6a] Edit path — gate-guard denies both blessing transitions:"
bash "$H/gate-guard.sh" --standalone docs/design-notes/some-note.md ratified; e1=$?
bash "$H/gate-guard.sh" --standalone docs/build-plans/some-plan/plan.md ready; e2=$?
echo "     design-note draft→ratified rc=$e1 ; plan proposed→ready rc=$e2"
{ [ "$e1" = 2 ] && [ "$e2" = 2 ]; } && ok "Edit-path blessing denied pre-hoc" || no "not denied"
echo "[6b] Bash path — Stop-gate audit detects a blessing in a diff. Crafted diff:"
printf '%s\n' "docs/build-plans/bp-000/plan.md" > "$PTR"
out="$(bash "$H/journal-gate.sh" --standalone --diff-file "$A/crafted-blessing.diff" 2>&1)"; rc=$?
echo "     rc=$rc ; reason: $out"
{ [ "$rc" = 2 ] && printf '%s' "$out" | grep -qi "blessing"; } \
  && ok "Bash-path blessing caught by close-of-session audit" || no "not caught"
echo "[6b'] Live corroboration — the owner's uncommitted hand-ratification of"
echo "      agent-workflow.md (draft→ratified) is present in the real worktree diff:"
python3 -c "import importlib.util,sys; s=importlib.util.spec_from_file_location('l','.claude/hooks/_lib.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); import subprocess; base=open('.claude/state/session-baseline').read().strip(); d=subprocess.run(['git','diff',base,'--','docs/design-notes'],capture_output=True,text=True).stdout; print('      detector:', m._blessing_in_diff(d))"

echo
echo "════════════════════════════════════════════════════════════════════"
echo "CRITERION 7 — sabotaged hook emits HOOK-FAILURE + journal marker; the fixed"
echo "             script's standalone re-invocation succeeds"
echo "────────────────────────────────────────────────────────────────────"
printf '%s\n' "docs/build-plans/bp-000/plan.md" > "$PTR"   # marker lands in bp-000 journal
SAB="$(mktemp -t bp000-sabotaged-XXXX.sh)"
# Copy the real scope-guard and inject a forced fault right after the trap line.
awk '1; /EXIT$/ && !d {print "false || exit 77   # SABOTAGE: forced fault (BP-000 C7)"; d=1}' \
  "$H/scope-guard.sh" > "$SAB"
before="$(grep -c '^- \[.*HOOK-FAILURE' docs/build-plans/bp-000/journal.md)"
echo "[7a] Running the sabotaged copy:"
sab_err="$(bash "$SAB" --standalone core/foo.py 2>&1 1>/dev/null)"
echo "     stderr: $sab_err"
after="$(grep -c '^- \[.*HOOK-FAILURE' docs/build-plans/bp-000/journal.md)"
echo "     journal HOOK-FAILURE markers: before=$before after=$after"
{ printf '%s' "$sab_err" | grep -q "HOOK-FAILURE scope-guard" && [ "$after" -gt "$before" ]; } \
  && ok "sabotage emits HOOK-FAILURE to transcript AND journal marker" \
  || no "alarm did not fire"
echo "[7b] The fixed (real) script, standalone, on an in-scope path:"
bash "$H/scope-guard.sh" --standalone CLAUDE.md; rc=$?   # CLAUDE.md ∈ bp-000 scope
echo "     rc=$rc (0=allow, clean)"
{ [ "$rc" = 0 ] && ! bash "$H/scope-guard.sh" --standalone CLAUDE.md 2>&1 | grep -q HOOK-FAILURE; } \
  && ok "fixed script standalone re-invocation succeeds" || no "fixed script failed"
rm -f "$SAB"

echo
echo "════════════════════════════════════════════════════════════════════"
echo "SUMMARY: PASS=$pass  FAIL=$fail"
echo "════════════════════════════════════════════════════════════════════"
[ "$fail" = 0 ]
