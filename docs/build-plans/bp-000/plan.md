---
type: build-plan
id: bp-000
status: complete
created: 2026-07-05
updated: 2026-07-05
links:
  - docs/design-notes/agent-workflow.md
objective: "Self-host the agent-workflow: build the constitution, hooks, commands, skills, and templates so every artifact after BP-000 flows through the machinery it built."
contract: builder
design_ref: "docs/design-notes/agent-workflow.md §12 (Bootstrap)"
write_scope:
  - "CLAUDE.md"
  - ".claude/**"
  - "docs/templates/**"
  - "docs/build-plans/bp-000/**"
  - "docs/findings/**"
  - "docs/inbox/**"
  - "docs/brainstorms/**"
context_manifest:
  - "docs/design-notes/agent-workflow.md   # the sole spec; §12 is the plan, §3/§6/§9 the schemas"
  - "CLAUDE.md (pre-BP-000)                 # the operational layer being replaced"
  - "CONSTITUTION.md                        # domain fixed point the new constitution points to"
  - "CONVENTIONS.md                         # engineering practice"
  - "docs/design-notes/supersession-lifecycle.md  # three-place (P,P',warrant); reused for plans"
  - "docs/research/security-planes.md       # capability-at-boundary; scope-guard/audit is its instance"
  - "docs/design-notes/the-sacred-boundary.md      # write-channel properties applied to agent state"
acceptance:
  - "1. Bare `claude` at root emits the session brief and behaves as orchestrator."
  - "2. On a toy plan: an out-of-scope Edit is denied pre-hoc with reason; an out-of-scope Bash write is caught by the Stop-gate audit and blocks close."
  - "3. Kill/resume round-trip on the toy plan passes the fresh-agent test."
  - "4. A stub capsule → /capture → hand-ratified stub note → /graduate yields a well-formed proposed plan."
  - "5. /triage on a synthetic finding routes it, drafts an owner-question entry, and writes a PROGRESS checkpoint."
  - "6. A blessing transition attempted by an agent is denied pre-hoc via the Edit path and caught by the close-of-session audit via the Bash path."
  - "7. A deliberately sabotaged hook script emits the HOOK-FAILURE line to the transcript and the journal marker, and its standalone re-invocation succeeds."
non_goals:
  - "docs/book/ — neither content nor scaffold; it is the first scribe plan through the finished machinery (§12)."
  - "CI/schema lint of front-matter (parked §14); pre-hoc Bash write-pattern denial (parked §14); brainstorm migration into Code (parked §14)."
  - "Editing design notes, CONSTITUTION.md, or the golden set; performing any blessing transition (draft→ratified, proposed→ready)."
  - "Appending to the canonical docs/PROGRESS.md — out of BP-000 write scope to protect the 1540-line build log; criterion 5 uses a toy PROGRESS target (see finding-0002)."
stop_conditions:
  - "The design note is not status: ratified — halt and tell the owner (front-matter check)."
  - "A `blocker` finding is filed (owner-level, no re-entry) — end the session after a fresh journal."
  - "An out-of-scope change cannot be reverted or converted to a finding."
session_budget: 1
re_entry: null
supersedes: null
superseded_by: null
warrant: null
---

# BP-000 — Bootstrap the agent-workflow machinery

## Bootstrap exception (why this plan is hand-minted at `in-progress`)

Every artifact *after* BP-000 flows through the machinery. BP-000 cannot: the
machinery that would `/graduate` and enforce the proposed→ready blessing gate on
it does not exist until this plan builds it. Per design-note §12 the ratified
note "graduates **by hand** into a single build plan." So this plan and its
journal are minted by hand from §12 and the §3 schema; they are the reference
examples the templates are then modeled on. The owner's instruction to execute
is the blessing. This is the last hand-built artifact; `gate-guard` did not exist
to gate it and is not active in the building session (hooks register at
SessionStart, already past). Status is `in-progress` because the plan is being
executed now; it flips to `complete` when criteria 1–7 pass.

## Deliverables (§12)

- `CLAUDE.md` — persona-neutral workflow constitution, ≤ 1 page (§5), pointing to
  the domain layer (`CONSTITUTION.md`/`BUILD-SPEC.md`/`CONVENTIONS.md`).
- `.claude/settings.json` + six hook scripts (§6), dual-mode, fail-open/fail-loud.
- Six commands (`capture`, `graduate`, `build`, `resume`, `triage`, `scribe`).
- Five skills (`graduate`, `build-plan`, `finding`, `checkpoint`, `book`).
- Four templates (`design-note`, `build-plan`, `finding`, `capsule`).
- Directory scaffolding; `.claude/state/` gitignored.
- `docs/inbox/owner-questions.md` initialized.

## Interfaces pinned inline

Per the build-plan skill, a plan copies the interfaces its builder must honor so
nothing is inferred. The interfaces this plan builds *to*:

**Artifact front-matter (§3).** Shared: `type, id, status, created, updated,
links`. Build plan adds `objective, contract(builder|scribe), design_ref,
write_scope, context_manifest, acceptance, non_goals, stop_conditions,
session_budget:1, re_entry, supersedes/superseded_by, warrant`. Finding adds
`ftype(blocker|spec-defect|question|discovery), origin_plan, route(orchestrator
|builder), resolution`. Design note adds `supersedes/superseded_by, warrant`.

**Active-plan pointer.** `.claude/state/active-plan` holds one line: the
repo-relative path to the active `plan.md` (a bare id like `bp-000` is also
tolerated). Worktree-local, gitignored.

**Hook I/O contract.** Each hook is dual-mode: hook invocation reads stdin JSON
(`tool_input.file_path`, `content`/`new_string`/`edits`); standalone invocation
takes `--standalone [args]`. PreToolUse deny = exit 2 with the reason on stderr.
Stop block = exit 2 with reason. SessionStart/UserPromptSubmit inject stdout into
context. On machinery error: emit `HOOK-FAILURE <name>: <detail> — enforcement
NOT applied` to stderr, append the same as a journal marker, and fail open.

**Scope decision.** Foundation denylist (`CONSTITUTION.md`, `docs/design-notes/**`,
`eval/golden/**`, `eval/golden.py`) is denied beneath every session. With a plan
active, the writable set is `write_scope ∪ {the plan's own plan.md, its
journal.md, docs/findings/**}`; everything else is denied. With no plan active
(orchestrator), everything non-denylisted is allowed.

## Acceptance evidence

Each criterion is demonstrated in `journal.md` (newest entry first) with the
exact command and its output. The hooks are exercised via their standalone path
because the building session predates their registration — which is also the
`HOOK-FAILURE` alarm test (criterion 7). Toy/stub/synthetic fixtures live under
`docs/build-plans/bp-000/acceptance/` so the evidence is committed and reproducible.
