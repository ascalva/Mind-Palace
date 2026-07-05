---
type: design-note
id: dn-agent-workflow
status: draft
created: 2026-07-05
updated: 2026-07-05
links:
  - docs/design-notes/supersession-lifecycle.md
  - docs/research/security-planes.md
  - docs/design-notes/sacred-boundary/ (write-channel properties)
  - docs/findings/finding-0001.md (warrant, amendment A2)
  - docs/findings/finding-0003.md (warrant, amendment A1)
supersedes: null
warrant: null
amendments: [A1 (finding-0003), A2 (finding-0001)]
---

# Agent Workflow: Brainstorm → Design → Build → Reflection

## 1. Purpose and scope

This note specifies the process machinery by which ideas move from brainstorm sessions (Claude chat, project context) through ratified design notes into session-scoped build plans executed by builder agents (Claude Code, Opus 4.8, max effort), with findings routed back for reflection. It defines the artifact taxonomy, state machines, repository layout, role contracts, enforcement hooks, and the owner's interaction surface.

Design goal: the owner's required touch points reduce to (a) brainstorming, (b) two blessing gates, and (c) answering a single questions file. Everything else is delegated, mechanical, or both. Starting `claude` at the repo root must land a fully oriented session every time, with no per-session configuration.

Out of scope: CI enforcement of artifact schemas (parked, §14), full migration of brainstorming into Claude Code (parked, §14), any automation of ratification (excluded permanently, §10).

## 2. Principles

The workflow applies existing store doctrine to the process layer itself:

1. **Everything is a typed file with a state machine.** No decision, question, or state lives only in a chat transcript or a session's context window. Front-matter carries `type`, `id`, `status`; state is greppable, so orchestrator sweeps are `grep`-cheap.
2. **The plan is a capability, not a suggestion.** A build plan's `write_scope` is mechanically enforced (pre-hoc deny + post-hoc audit), not merely steered. This is the security-planes move — object capabilities at the boundary — applied to the workflow.
3. **Write-channel properties apply to agent state.** Journals and findings are attributable (per-plan, per-session), append-only in spirit (committed, never rewritten), and typed-and-promotion-gated (findings promote into design notes only via supersession with warrant).
4. **Blessing gates are manual and raw.** Ratifying a design note and approving a plan split are owner-only front-matter flips. No command wraps them; automating a blessing gate would put an expected-value step inside a bright line.
5. **Zone isolation between sessions.** Builder sessions do not share context with the orchestrator or each other. The findings inbox is the only asynchronous channel. Session-sized plans run as independent sessions, not subagents, so no context bleeds across the boundary.

## 3. Artifact taxonomy and state machines

| Artifact | Location | States | Terminal |
|---|---|---|---|
| Brainstorm note | `docs/brainstorms/<topic>.md` | living (append-only) | — |
| Design note | `docs/design-notes/<slug>.md` | draft → ratified → superseded | superseded |
| Build plan | `docs/build-plans/<id>/plan.md` | proposed → ready → in-progress → complete \| parked \| superseded | complete, superseded |
| Journal | `docs/build-plans/<id>/journal.md` | alive → sealed | sealed |
| Finding | `docs/findings/<id>.md` | open → routed → resolved \| promoted | resolved, promoted |
| Owner questions | `docs/inbox/owner-questions.md` | living (entries: open → answered → swept) | — |
| Session capsule | fenced block in chat → appended to brainstorm note | — | — |
| Book (design manual) | `docs/book/` (LaTeX) | living; edition-tagged syncs | — |

State transitions that matter:

- **Design note ratification** (draft → ratified): owner-only, by hand. `/graduate` refuses drafts.
- **Plan readiness** (proposed → ready): owner-only, by hand. This is the split-approval gate. `/build` refuses any plan whose status is not `ready`.
- **Plan supersession** is three-place: (P, P′, warrant), where the warrant is a `spec-defect` finding. A defect never edits a plan in place; graduation mints P′ citing the finding, P flips to `superseded` with a `superseded_by` link. Same relation as claim supersession (see `supersession-lifecycle.md`), same reason: the discredited plan must remain inspectable, and P′ must ground on the warrant, not on P.
- **Parked** requires a `re_entry` field. A plan or criterion without a re-entry condition cannot enter `parked`.
- **Finding promotion**: a `discovery` or `spec-defect` finding that changes design mints a design-note supersession (or amendment) citing the finding as warrant, then flips to `promoted`.
- **Book editions**: the book is a *derived projection* of the ratified record and the codebase — design notes remain authoritative for design, the repo for implementation. It synthesizes and asserts nothing without citing a source: an artifact id, or code by path plus git ref. Code snippets are included wherever they genuinely aid understanding; each is a copy annotated `source: path@ref`, so drift is detectable rather than silent. A scribe run ends by updating the sync marker (`docs/book/SYNC.md`: git ref + artifact ids incorporated); the commit is the edition. Draft notes never enter the book; parked decisions populate the future-work chapter verbatim with their re-entry conditions; superseded material may be retained as marked design-evolution remarks, warrant-linked — provenance as pedagogy.

### Front-matter schemas

Shared: `type, id, status, created, updated, links`.

Build plan adds: `objective` (one sentence), `contract: builder | scribe` (defaults to builder), `design_ref`, `write_scope` (glob list — the capability), `context_manifest` (ordered read list), `acceptance` (runnable criteria), `non_goals`, `stop_conditions`, `session_budget: 1`, `re_entry` (if parked), `supersedes`/`superseded_by` + `warrant` (if applicable).

Finding adds: `ftype: blocker | spec-defect | question | discovery`, `origin_plan`, `route: orchestrator | builder`, `resolution` (link or text on close).

Design note adds: `supersedes`/`superseded_by`, `warrant`.

## 4. Repository layout

```
CLAUDE.md                      # constitution, ~1 page, auto-loaded
.claude/
  settings.json                # hook registrations, permissions
  hooks/                       # 6 small shell scripts (§6)
  agents/
    builder.md                 # subagent variant for small scoped delegations only
    scribe.md                  # subagent variant (single-figure / single-section fixes)
  commands/
    capture.md  graduate.md  build.md  resume.md  triage.md  scribe.md
  skills/
    graduate/  build-plan/  finding/  checkpoint/  book/
  state/                       # gitignored; per-worktree active-plan pointer
docs/
  book/                        # main.tex, preamble.tex, notation.tex, chapters/, figures/, SYNC.md
  brainstorms/
  design-notes/
  build-plans/<id>/plan.md, journal.md
  findings/
  inbox/owner-questions.md
  templates/
    design-note.md  build-plan.md  finding.md  capsule.md
  PROGRESS.md
```

**Worktree isolation is a hard invariant, not merely a parallelism convenience — the Stop-gate scope audit depends on it for soundness.** That audit (§6) cannot distinguish a builder's out-of-scope Bash write from an owner's legitimate parallel untracked file: to git, both are uncommitted, untracked, out-of-scope paths, and no attribution separates them. A dedicated worktree removes the ambiguity — every uncommitted delta in it is the session's own, so "out-of-scope change present" and "the session violated scope" become the same proposition. `.claude/state/active-plan` and `.claude/state/session-baseline` are worktree-local, so concurrent sessions never collide on enforcement state. The one place the invariant cannot hold is bootstrap (BP-000), which necessarily runs in the main worktree; §12 records the consequence and the reconciliation.

## 5. Roles and write discipline

**CLAUDE.md is a persona-neutral constitution** (~one page): artifact chain, routing rule, note-taking obligation, never-block-on-owner rule, pointer to commands. Depth (templates, scoping heuristics, register) lives in skills and loads only when invoked.

One category is exempt from the thinness rule: **safety-critical non-negotiables stay inline, never behind a pointer.** The domain bright lines — the mind-palace kernel digest, the sacred-boundary constraints, the never-cross rules — remain in the auto-loaded surface, because a guardrail that is not in context at the moment it is relevant is not a guardrail. A skill that must be invoked to be seen is fine for a template and unacceptable for a constraint. This is the standing resolution of oq-0001 (warrant: finding-0001): replacing the operational CLAUDE.md must not demote the non-negotiables digest to pointer-only; the digest is re-homed into the workflow constitution's always-loaded body. Every *other* constitution token is paid on every turn and is justified by review, not hope — but guardrails are not on that ledger.

**Orchestrator** is the default posture of a bare `claude` session at root. Duties: run `/graduate`, spawn/resume builders, run `/triage` sweeps, maintain `owner-questions.md`, write PROGRESS.md checkpoints, flip plan status on completion. Single-writer set: `PROGRESS.md`, `docs/inbox/owner-questions.md`, plan front-matter status fields, `docs/findings/` (triage annotations).

**Builder** is a session contract layered by `/build <id>` or `/resume <id>`. Concerns: the codebase, spec fidelity, raising rather than resolving design questions. Writable surfaces are exactly three: the plan's `write_scope`, its own `journal.md`, and new files in `docs/findings/`. Everything else is denied (§6).

**Scribe** is the third contract, selected by a plan's `contract: scribe` field, minted by `/scribe`, executed by `/build` like any plan. Sole concern: exposition. It maintains `docs/book/`, a LaTeX design manual — the philosophy, the architecture, the mathematics (the coboundary framing and its derived instruments get their canonical write-up here), and the intuition connecting them. Figures are TikZ/pgfplots: text, diffable, versioned like everything else. Notation is defined once in `notation.tex` and used everywhere. Writable surfaces mirror the builder's: `docs/book/**`, its own journal, new findings. Grounding rule: every claim is checkable against a cited source — an artifact id for design, code by path plus git ref for implementation — and snippets carry their `source: path@ref` annotation. Accuracy outranks every other goal, stylistic or expository: a beautiful sentence about a false mechanism is a defect, not prose. When writing exposes a gap or contradiction in the design record — and it will; explanation is an audit pass — the scribe files a finding and routes it. It cannot edit a design note, and no new hook is needed to guarantee that: scope-guard already enforces the plan's write scope.

**Routing rule** (constitution text): findings typed `design | math | direction` → route `orchestrator`, who batches to `owner-questions.md` if owner input is needed. Findings typed `codebase | spec-fidelity` → builder resolves, annotates journal and finding, continues.

**Never-block-on-owner**: a builder facing an owner-level question parks that criterion with a re-entry condition and proceeds with remaining criteria. Only a `blocker` finding ends a session early — and the Stop gate still demands a fresh journal on the way out.

## 6. Enforcement: hook contracts

Hooks are shell scripts; they cannot compel prose, so each is placed where a mechanical check has teeth. Registered in `.claude/settings.json`:

| Hook | Event / matcher | Contract |
|---|---|---|
| `scope-guard` | PreToolUse: Edit\|Write\|MultiEdit | Read active plan id from `.claude/state/active-plan`; parse `write_scope` globs from plan front-matter; deny out-of-scope `file_path` with a reason string fed back to the agent. A global foundation-file denylist applies beneath any plan, in every session, orchestrator included. |
| `gate-guard` | PreToolUse: Edit\|Write\|MultiEdit on `docs/design-notes/` and `docs/build-plans/*/plan.md` | Deny any edit performing a blessing transition — setting `status: ratified`, or `proposed → ready` — in every session, every role. Deny reason states: blessing transitions are owner-manual, made by hand outside a session. All other status transitions (`ready → in-progress → complete \| parked \| superseded`) pass. |
| `session-brief` | SessionStart | Emit world-state to context: plans by status, unswept findings count, open owner questions, active worktree's plan if any. Record HEAD into `.claude/state/session-baseline` for the close-of-session audit. This is what makes bare `claude` land oriented. |
| `journal-gate` | Stop | Block session end (decision: block, with reason) if (a) journal mtime predates the last commit in the worktree; (b) the session's uncommitted delta contains any path outside the plan's `write_scope`; or (c) the working tree contains an *uncommitted* blessing transition relative to `HEAD`. (a) and (b) apply when a plan is active; (c) applies to every session. (b) and (c) are the post-hoc audit that catches Bash-mediated writes the pre-hoc guards cannot see. See the two clarifications below. |
| `staleness-nudge` | UserPromptSubmit | If journal is stale relative to HEAD, inject a one-line reminder into context. Advisory only. |
| `compaction-marker` | PreCompact | Append a mechanical marker line (timestamp, event) to the journal so the post-compaction turn knows a compaction occurred and re-verifies state against the journal rather than trusting the summary. |

**Two-layer write enforcement, stated honestly.** The pre-hoc guard covers Edit/Write tools only; a builder can write files through Bash. Pre-hoc Bash pattern-denial is brittle and is parked (§14). The `journal-gate` audit is the backstop: any out-of-scope change blocks session close with a reason, forcing revert-or-finding before the session can end. Pre-hoc porous, post-hoc tight.

**Clarification on (b) — untracked-inclusive, and why (warrant: finding-0003).** The delta must be computed untracked-inclusive: `git status --porcelain -uall` filtered against `write_scope` (equivalently `git diff --name-only` unioned with `git ls-files --others --exclude-standard`). Plain `git diff` omits new files entirely, and plain `--porcelain` collapses a wholly-new directory to a single entry that won't match a deeper scope glob — so `-uall` (file-granular, untracked-inclusive) is required. This is load-bearing: a Bash-written file is *untracked*, and it is precisely the write the pre-hoc guard cannot see, so an audit that ignored untracked paths could not satisfy §12 criterion 2. The check is sound only under the worktree-isolation invariant (§4): there, every uncommitted path is the session's own, so a flagged out-of-scope path is a genuine violation rather than someone else's parallel work.

**Clarification on (c) — diff against `HEAD`, not the session baseline (warrant: finding-0003).** The blessing detector compares the working tree to `HEAD`, flagging only an *uncommitted* `→ ratified` or `proposed → ready` flip. The reason is that a committed blessing is already accountable — attributable to its commit author, which is exactly §10's "deliberate, logged." Diffing against the session baseline (HEAD-at-start) instead made a blessing *committed mid-session* keep firing until the baseline was manually re-anchored — a spurious block on an already-accountable act. Anchoring to `HEAD` makes a committed blessing self-clear with no re-anchoring, while still catching an in-flight flip that has not yet been recorded. `session-baseline` is retained only for the SessionStart brief's "what changed this session" narration; enforcement does not depend on it.

**Failure posture: fail open, fail loud.** Claude Code hooks fail open on script error; that platform behavior is not configurable. The compensating contract: every script runs under an error trap that emits a conspicuous `HOOK-FAILURE <name>: <detail> — enforcement NOT applied` line to stderr, surfaced in the transcript, and appends a marker line to the journal. Every script is dual-mode — hook invocation via stdin JSON, standalone invocation via file arguments — so "rerun the hook" is a literal instruction: on a flagged failure, the owner tells the session to re-invoke the script manually and reconcile before proceeding. Scripts stay trivial (a glob match, an mtime compare, a diff) so the trap path is the rare path, and the Stop-gate audit remains the catch-all beneath it.

## 7. Commands and skills

| Command | Action |
|---|---|
| `/capture <topic>` | Append a pasted session capsule (or tolerate raw paste) to `docs/brainstorms/<topic>.md`, timestamped. |
| `/graduate <design-note>` | Refuse unless `status: ratified`. Invoke graduate skill: decompose into one-session build plans against the template, emit as `status: proposed`, cross-link to design note. |
| `/build <plan-id>` | Refuse unless `status: ready`. Write worktree state pointer, flip plan to `in-progress`, load the plan's contract (per its `contract` field) + context manifest, begin. |
| `/resume <plan-id>` | Load plan + journal + context-manifest delta into a fresh session under the plan's contract. Must pass the fresh-agent test (§9). |
| `/scribe` | Compute book debt — ratified or superseded design notes and promoted findings newer than `docs/book/SYNC.md` — and mint a sync plan (`contract: scribe`, `write_scope: docs/book/**`, the delta as context manifest) as `status: proposed`. Fixed acceptance on every sync plan: whole-book review, every snippet and code citation re-verified against HEAD, clean compile (latexmk or tectonic; default recorded on first run), zero undefined references, sync marker updated. Execution flows through `/build`. |
| `/triage` | Sweep findings: route, batch owner questions, propose promotions (as supersessions with warrant), seal journals of completed plans, write PROGRESS checkpoint entries, sweep answered owner questions back to their origin artifacts. This is the reflection stage made mechanical. |

Skills carry the depth the constitution omits: **graduate** (decomposition rules, session-sizing heuristics, split-at-graduation-never-mid-build), **build-plan** (template semantics, especially: interfaces pinned inline — signatures, schemas, invariants copied into the plan, never referenced — so the builder never infers design), **finding** (typing and routing), **checkpoint** (journal contract §9, semantic-boundary triggers, fresh-agent test), and **book** (chapter map, voice and register, TikZ conventions, notation-registry discipline, citation scheme — artifact ids and code `path@ref` — snippet provenance, sync semantics).

## 8. Chat-side protocol

The brainstorm surface stays in Claude chat with project context. Changes:

- The filesystem MCP is demoted to read-only reference. The chat agent never writes files.
- Every session ends with a **session capsule** in a fenced block: `decisions`, `parked` (each with re-entry condition), `open_questions`, `next_steps`, `references`. Owner pastes it into `/capture <topic>`.
- When an idea finalizes, the chat agent drafts the design note in-chat against `docs/templates/design-note.md`. Owner files it as `draft`; ratification is a hand edit; `/graduate` takes it from there.

Capsule loss (a chat that ends without one) is tolerated: `/capture` accepts raw pasted conversation excerpts and the orchestrator restructures on append. Lossy capture beats no capture.

## 9. Journal contract

`docs/build-plans/<id>/journal.md`, alive while the plan is in-progress, sealed by `/triage` on completion. Committed — journals are history, not scratch. Written at every semantic boundary: an acceptance criterion closed, a commit made, a finding filed. The threshold trigger ("context feels high") is not relied upon; boundaries plus the Stop gate make staleness structurally bounded to one criterion.

Required sections, newest entry first:

1. **Status line** — one sentence, current truth.
2. **Completed** — per criterion, with commit refs.
3. **In-flight** — what is mid-motion and its exact state.
4. **Next action** — single and concrete enough to execute without thought.
5. **Open questions** — typed and routed (or finding-linked).
6. **Context-manifest delta** — files read beyond the manifest, files that proved irrelevant.
7. **Markers** — mechanical lines appended by hooks (compactions, audits).

**Fresh-agent test** (the checkpoint skill's acceptance bar): a new session given only plan + journal + write-scope files must continue without asking anything already answered. When this holds, resume strictly dominates compaction — the journal is an audited, committed artifact; a compaction summary is lossy and unreviewable. Norm: kill sessions freely between criteria and resume fresh; compaction is the mid-criterion fallback only. The journal makes context disposable; that is the deliverable of the note-taking obligation.

## 10. Owner interaction surface

Three touch points, by construction:

1. **Brainstorming** — unchanged, in chat.
2. **Two blessing gates** — ratify a design note (draft → ratified), approve a plan split (proposed → ready). Both are raw front-matter edits by the owner, made by hand outside any agent session. The exclusion is permanent and mechanically enforced, not steered: `gate-guard` denies the transitions pre-hoc in every session and role, and the Stop-gate audit blocks close on any Bash-mediated flip (§6). The gates bound the feasible set of everything downstream, so they live in the hook layer with the same standing as the foundation-file denylist — a bright line built as a hard constraint, never left as instruction text.
3. **`docs/inbox/owner-questions.md`** — the one file the owner answers. Orchestrator-maintained. Entry fields: id, origin link, question, blocking (bool), and `default_if_unanswered` with a park condition — so an unanswered question degrades to a parked item with re-entry, never to a stalled builder.

## 11. Reflection loop

Reflection is `/triage` plus the promotion path. Builder findings of type `discovery` or `spec-defect` that bear on design are proposed by the orchestrator as design-note supersessions or amendments, warrant-linked to the finding — the owner ratifies or declines at the same gate as any design change. Completed plans get a PROGRESS.md checkpoint entry (orchestrator-written) and a sealed journal. The loop closes: build output re-enters design through the same typed, gated channel brainstorms do, never by side effect.

Milestones close a second, slower loop. `/triage` surfaces book debt in the session brief and runs `/scribe` to mint a proposed sync plan whenever a design note has been ratified or superseded since the last edition; the owner's ready-flip is the milestone confirmation — the existing gate, reused, no new ceremony. The scribe then feeds back through the same findings channel: the book sits downstream of design, but writing it audits design.

## 12. Bootstrap (BP-000)

The system self-hosts. This note, once ratified, graduates by hand into a single build plan whose deliverables are the machinery itself:

- CLAUDE.md (constitution, ≤ 1 page)
- `.claude/settings.json` + the six hook scripts
- Six commands, five skills, four templates
- Directory scaffolding, `.claude/state/` gitignored
- `docs/inbox/owner-questions.md` initialized

Acceptance criteria for BP-000:

1. Bare `claude` at root emits the session brief and behaves as orchestrator.
2. On a toy plan: an out-of-scope Edit is denied pre-hoc with reason; an out-of-scope Bash write — untracked, invisible to the pre-hoc guard — is caught by the Stop-gate untracked-inclusive audit (§6b) and blocks close.
3. Kill/resume round-trip on the toy plan passes the fresh-agent test.
4. A stub capsule → `/capture` → hand-ratified stub note → `/graduate` yields a well-formed `proposed` plan.
5. `/triage` on a synthetic finding routes it, drafts an owner-question entry, and writes a PROGRESS checkpoint.
6. A blessing transition attempted by an agent is denied pre-hoc via the Edit path and caught by the close-of-session audit via the Bash path.
7. A deliberately sabotaged hook script (forced error) emits the `HOOK-FAILURE` line to the transcript and the journal marker, and its standalone re-invocation succeeds — the alarm is tested, not just the lock.

One session of work, cleanly scoped. Every artifact after BP-000 flows through the machinery it built. The book is deliberately excluded from BP-000: its scaffold and first edition are the first scribe plans through the finished machinery — split by chapter cluster if the seeding pass exceeds one session, per the standard rule.

**Bootstrap worktree caveat.** BP-000 runs in the main worktree, not a dedicated one, so the isolation invariant (§4) does not hold *during bootstrap only*. If the owner is drafting or ratifying design notes in parallel (the chat-side path, §8), those uncommitted changes will trip the Stop-gate scope audit (§6b) and blessing audit (§6c) — the builder sees out-of-scope untracked files and an uncommitted ratification it did not make. This is expected behavior, not a defect: it is the fail-loud → owner-reconcile protocol (§6) exercising itself on live state, and the correct response is exactly what it prescribes — the builder surfaces the state and refuses to touch the owner's notes or to weaken its own audit; the owner reconciles by committing the parallel work (a ratification wants committing anyway, §10), after which the audits read clean. The builder must not "fix" the block by editing the hook or by committing the owner's design notes on their behalf; both are recorded as prohibited responses. Every plan after BP-000 runs isolated and never meets this case.

## 13. Failure modes and mitigations

| Failure | Mitigation |
|---|---|
| Bash write (untracked) escapes pre-hoc scope guard | Stop-gate untracked-inclusive audit blocks close (§6b); sound under worktree isolation (§4) |
| Committed blessing keeps firing the Stop gate (re-anchor loop) | (c) diffs against `HEAD`, not the session baseline — committed = accountable, self-clears (§6c) |
| Owner's parallel untracked work trips the scope audit | Only possible in a shared worktree; isolation (§4) removes it; bootstrap is the one documented exception (§12) |
| Safety non-negotiables orphaned from context | Kept inline in the auto-loaded constitution, exempt from the thinness rule (§5) |
| Journal staleness | Semantic-boundary discipline + Stop gate + staleness nudge |
| Compaction mid-criterion loses nuance | PreCompact marker forces post-compaction re-verification against journal; resume-over-compact norm shrinks the exposure window |
| Capsule never emitted | `/capture` tolerates raw paste; orchestrator restructures |
| Constitution bloat | Hard budget (~1 page); depth exiled to skills; reviewed at each triage that touches CLAUDE.md |
| Hook script error fails open | Error trap emits loud `HOOK-FAILURE` line to transcript + journal marker; owner-directed standalone re-run; audit layer as catch-all |
| Agent attempts a blessing transition | `gate-guard` pre-hoc deny; close-of-session audit blocks Bash-mediated flips |
| Review fatigue at owner gates | `default_if_unanswered` + park semantics on every question; findings batched by `/triage`, never dripped |
| Book drifts from the record | Sync marker + book-debt line in session brief; every claim cites a source (artifact id or code ref); draft notes barred |
| Code snippets rot as the repo moves | Every snippet annotated `source: path@ref`; sync acceptance re-verifies all snippets and code citations against HEAD |
| Scribe "fixes" design in prose | Write scope excludes design notes; gaps exit as findings, not edits |
| Compile rot | Fixed acceptance on every sync plan: clean compile, zero undefined references, sync marker updated |

## 14. Parked decisions

| Decision | Default recorded | Re-entry condition |
|---|---|---|
| Full brainstorm migration into Claude Code | Stay hybrid (chat + capsule) | After 5 graduations, compare capsule fidelity against a trial run of in-Code brainstorm sessions |
| CI/schema lint of artifact front-matter | Manual + hook-level only | First observed state-machine violation in practice, or ≥ 3 artifact types churning schema |
| Pre-hoc Bash write-pattern denial | Post-hoc audit only | Stop-gate audit catches ≥ 1 real escape |
| Subagent decomposition pass inside `/graduate` | Single-context graduation | A multi-plan split ships with a scoping defect traced to decomposition quality |
| PDF edition publishing cadence (tagged builds, committed PDFs) | Source-only commits; PDF built locally | First complete edition compiles clean end-to-end |

## 15. Cross-references

- `docs/design-notes/supersession-lifecycle.md` — three-place supersession; reused verbatim for plans and design-note promotion.
- `docs/research/security-planes.md` — capability enforcement at boundaries; the scope-guard/audit pair is its workflow-plane instance. Foundation-file denylist originates there.
- Sacred Boundary design set — the four write-channel properties; §2.3 applies them to agent state.
- `docs/PROGRESS.md` — receives a checkpoint entry when this note is filed, and per completed plan thereafter.

## 16. Amendment log

Amendments to a ratified note are warranted by findings and re-ratified by hand (defect patches amend in place; substantive pivots supersede — the same distinction the store draws between amendment and supersession). Each entry records the warrant and the change.

- **A1** — warrant: finding-0003 (surfaced by BP-000, first live run). §6(b) specified untracked-inclusive (`git status -uall`) rather than `git diff --name-only`, because a Bash write is untracked and criterion 2 could not otherwise be satisfied; the soundness dependency on worktree isolation (§4) is made explicit. §6(c) re-anchored from the session baseline to `HEAD`, so a mid-session *committed* blessing self-clears instead of forcing a manual re-anchor. §12 gains the bootstrap-worktree caveat. Both changes eliminate the two reconciliation loops observed on day one while preserving every enforcement guarantee.
- **A2** — warrant: finding-0001 / oq-0001. §5 exempts safety-critical non-negotiables from the constitution thinness rule: the domain bright-line digest stays inline in the auto-loaded surface rather than demoted to a pointer, on the principle that an out-of-context guardrail is not a guardrail.
