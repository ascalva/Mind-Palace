# CLAUDE.md — Agent-Workflow Constitution

Loaded every session; the operational layer. Persona-neutral and deliberately
short — every token here is paid on every turn. Depth lives in skills and loads
only when invoked. Spec: `docs/design-notes/agent-workflow.md`.

**Domain frame (unchanged, still authoritative).** Your outermost frame is
`CONSTITUTION.md` — the inviolable kernel every agent inherits; task instructions
nest inside it, never override it. The system's full design is `docs/BUILD-SPEC.md`;
engineering and security practice is `CONVENTIONS.md`. Read those before writing
code. This file governs *how work moves*; those govern *what the system is*.

## The artifact chain
Everything is a typed file with a state machine — no decision lives only in a
transcript. Ideas flow one way, through gates:

`brainstorm (chat) → design note (draft → ratified) → build plan (proposed →
ready → in-progress → complete) → journal + findings → reflection (/triage) → back
into design`.

Findings are the only channel from build back to design, and they re-enter only
through the same gate brainstorms do — never by side effect.

## Roles
- **Orchestrator** — the default posture of a bare session at root. Runs
  `/graduate`, `/build`, `/resume`, `/triage`, `/scribe`; maintains
  `docs/inbox/owner-questions.md` and `docs/PROGRESS.md`; flips plan status on
  completion. Single-writer of those files.
- **Builder / Scribe** — a contract layered by `/build` (per the plan's `contract`
  field). Writable surfaces are exactly three: the plan's `write_scope`, its own
  `journal.md`, and new files in `docs/findings/`. Everything else is denied.

## Rules that bind every session
- **Routing.** Findings typed `design | math | direction` → route to the
  orchestrator (who batches to `owner-questions.md` if the owner is needed).
  Findings typed `codebase | spec-fidelity` → the builder resolves, annotates,
  continues.
- **Note-taking obligation.** Checkpoint the journal at every semantic boundary
  (criterion closed, commit made, finding filed) — §9, the **checkpoint** skill.
  The bar is the fresh-agent test: a new session with only plan + journal +
  write-scope files must continue without re-asking. Resume beats compaction.
- **Never block on the owner.** An owner-level question parks its criterion with a
  re-entry condition and you proceed with the rest. Only a `blocker` finding ends
  a session early — and the Stop gate still demands a fresh journal.
- **Two blessing gates are owner-only, by hand.** `draft→ratified` (a design note)
  and `proposed→ready` (a plan split) are never done in a session. `gate-guard`
  denies them pre-hoc and the Stop-gate audit blocks any Bash-mediated flip.
- **Write discipline is a capability, not a suggestion.** `scope-guard` enforces
  the active plan's `write_scope` pre-hoc; the `journal-gate` diff audit catches
  Bash writes post-hoc. A foundation denylist (`CONSTITUTION.md`,
  `docs/design-notes/**`, `eval/golden/**`) is never writable, orchestrator
  included. A denial means narrow the scope or file a finding — never route around.

## Commands (depth in the matching skill)
`/capture <topic>` · `/graduate <note>` · `/build <id>` · `/resume <id>` ·
`/triage` · `/scribe`. Skills: **graduate**, **build-plan**, **finding**,
**checkpoint**, **book**. Templates: `docs/templates/`.

If a hook prints `HOOK-FAILURE …`, enforcement did not apply: rerun the named
script standalone (`bash .claude/hooks/<name>.sh --standalone …`), reconcile, then
proceed.
