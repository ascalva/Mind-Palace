# BP-000 — Build journal

Alive while the plan is `in-progress`; sealed by `/triage` on completion.
Committed — this is history, not scratch (§9). Narrative entries are newest-first
below the header; the `## Markers` section at the file's end receives the
mechanical lines hooks append (compactions, audits, HOOK-FAILUREs).

Convention: this journal is the reference example for the journal contract (§9).
A fresh session given only `plan.md` + this journal + the write-scope files must
continue without re-asking anything already answered (the fresh-agent test).

---

## Entry — 2026-07-05 — acceptance criteria 1–7 all pass; BP-000 complete

**Status.** BP-000 complete. All deliverables built; acceptance criteria 1–7
demonstrated green by `docs/build-plans/bp-000/acceptance/run.sh` (PASS=13,
FAIL=0). Plan flipped `in-progress → complete`; this journal is sealed below.

**Completed (per criterion, each demonstrated in run.sh).**
- **C1 — brief + orchestrator.** `session-brief.sh --standalone` emits world-state
  (plans by status, unswept findings, open owner questions, active plan, book
  debt) and declares orchestrator posture. PASS.
- **C2 — pre-hoc scope deny + post-hoc Bash catch.** `scope-guard.sh --standalone
  core/secret.py` under toy-plan → deny rc=2 with reason; an in-scope path → allow
  rc=0. A Bash-written `core/_bp000_audit_probe.txt` under the bp-000 plan →
  `journal-gate.sh --standalone` blocks (rc=2), reason names the probe. PASS.
- **C3 — fresh-agent test.** `toy-plan/journal.md` carries every §9 section and a
  single concrete Next action (`src/hello.txt` = one line `hello`) — resume-
  sufficient without re-asking. PASS. (Round-trip shown by journal sufficiency;
  no process restart, no subagent spawned.)
- **C4 — capture → note → graduate.** capsule captured to
  `docs/brainstorms/bp-000-acceptance.md`; `/graduate`'s status gate refuses the
  draft stub (status=draft ≠ ratified); on the owner-ratified `agent-workflow.md`
  the emitted proposed plan (`demo-graduated-plan.md`) is schema-complete. PASS.
- **C5 — triage.** synthetic `finding-9001` routed (open→routed); owner-question
  `oq-9001` drafted (toy inbox); PROGRESS checkpoint written (toy PROGRESS). Real
  `docs/PROGRESS.md` is out of BP-000 scope by design (finding-0002). PASS.
- **C6 — blessing denied + caught.** `gate-guard` denies design-note→ratified and
  plan→ready pre-hoc (rc=2 each); `journal-gate` detects a blessing in a crafted
  diff (rc=2) and, live, in the real worktree diff (the owner's uncommitted
  ratification). PASS.
- **C7 — alarm tested.** a sabotaged `scope-guard` copy (forced rc=77) emits
  `HOOK-FAILURE scope-guard: … enforcement NOT applied` to stderr AND appends a
  journal marker (see Markers); the fixed real script re-invoked standalone
  succeeds (rc=0, clean). PASS.

**In-flight.** None.

**Next action (orchestrator, post-BP-000).** Commit the BP-000 machinery (owner's
call — I do not commit unprompted). Then real work flows through it: `/capture`
brainstorms → owner ratifies notes by hand → `/graduate` → owner readies →
`/build`; the first scribe plan mints `docs/book/`. Note: the Stop gate flags the
owner's **uncommitted** `agent-workflow.md` ratification — commit that blessing
(deliberate + logged, §10) so future sessions close clean.

**Open questions.** `finding-0001` (CLAUDE.md domain digest → `oq-0001`, routed to
owner, not blocking); `finding-0002` (PROGRESS scope, resolved in-plan).

**Context-manifest delta.** Acceptance added no new manifest reads. Discovered and
fixed: `git status --porcelain` collapses wholly-new directories, which would
mis-flag files under a deep `write_scope`; fixed with `-uall` in
`_lib.py._changed_files`.

**Seal.** Sealed 2026-07-05 as the final BP-000 act (in normal operation `/triage`
seals a completed plan's journal; BP-000 is the hand-built bootstrap). Narrative
entries end here; the `## Markers` section still receives mechanical hook lines.

---

## Entry — 2026-07-05 — machinery scaffolded; acceptance pending

**Status.** BP-000 in-progress. The enforcement layer (`_lib.py` + six hooks) is
built and unit-tested; scaffolding, plan, and this journal are minted. Building
the remaining deliverables (templates, commands, skills, agents, constitution,
owner-questions), then running acceptance criteria 1–7.

**Completed.**
- Confirmed `docs/design-notes/agent-workflow.md` front-matter is `status:
  ratified` (line 4) — the stop-gate at the top of §12 passes.
- Directory scaffolding created (`.claude/{hooks,commands,skills,agents,state}`,
  `docs/{brainstorms,findings,inbox,templates,build-plans/bp-000}`).
- `.claude/hooks/_lib.py` — shared decision logic (glob matcher with correct
  `**` vs `*`, front-matter parser, scope/gate/audit/brief/marker). Unit-tested:
  22/22 assertions green (glob semantics, denylist, block+flow front-matter,
  classification, gate transitions, blessing-in-diff scan).
- Six hooks (`scope-guard`, `gate-guard`, `session-brief`, `journal-gate`,
  `staleness-nudge`, `compaction-marker`) — dual-mode, fail-open/fail-loud.
  Standalone smoke tests green (denylist deny, blessing deny, allow paths, brief).
- `.claude/settings.json` (hook registrations + shared allowlist);
  `.claude/state/.gitignore`.
- `docs/build-plans/bp-000/plan.md` minted by hand (bootstrap exception documented).

**In-flight.** None mid-motion; at a clean boundary.

**Next action.** Write the four templates (design-note, build-plan, finding,
capsule), then the six commands, five skills, two agents, then `CLAUDE.md` and
`docs/inbox/owner-questions.md`. Then execute acceptance 1–7, prepending a
journal entry per closed criterion.

**Open questions.**
- CLAUDE.md replaces the pre-BP-000 operational layer; the domain non-negotiables
  digest it carried is dropped in favor of a pointer to `CONSTITUTION.md`/
  `BUILD-SPEC.md`/`CONVENTIONS.md`. Surfaced as `docs/findings/finding-0001.md`
  (direction), parked — not blocking.
- Criterion 5's PROGRESS checkpoint vs BP-000 write scope (excludes
  `docs/PROGRESS.md`). Surfaced as `docs/findings/finding-0002.md`, resolved
  in-plan by demonstrating against a toy PROGRESS target — not blocking.

**Context-manifest delta.** Read beyond the manifest: `.claude/settings.local.json`
(to avoid clobbering the existing local permissions), `.gitignore` (state-ignore
approach), `eval/golden/` (denylist path). Manifest item `the-sacred-boundary.md`
consulted only lightly (write-channel properties are already internalized in §2.3).

---

## Markers
- [2026-07-05T19:09:38Z] HOOK-FAILURE scope-guard: unexpected exit rc=77 — enforcement NOT applied
- [2026-07-05T19:17:04Z] Live Stop-gate fired (hooks now active): blocked on owner's uncommitted design-note changes (agent-workflow.md ratification + new core-integrity.md draft) — not session writes; filed finding-0003.
- [2026-07-05T19:20:15Z] Reconciled: owner committed the blessing (0b21de6, accountable §10); re-anchored session-baseline to HEAD; Stop-gate now passes (rc=0). (c) stale-baseline facet added to finding-0003.
