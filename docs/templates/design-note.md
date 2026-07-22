---
type: design-note
id: dn-<slug>
track: <slug>            # the board coordinate — dn-track-board-and-deskcheck-gate (D1); MUST equal a docs/tracks/<slug>.md manifest
status: draft            # draft → ratified → superseded.  draft→ratified is an OWNER-ONLY hand edit.
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
links:
  - <related design note / research / brainstorm path>
supersedes: null         # prior design-note id this one replaces (three-place: P, P′, warrant)
superseded_by: null      # successor design-note id, once superseded
warrant: null            # the finding id (discovery | spec-defect) grounding a supersession/amendment
---

# <Design note title>

> Filed by the chat agent as `draft` (chat-side protocol, §8). Ratification is a
> hand edit by the owner — no command performs it, and `gate-guard` denies any
> agent attempt (§10). `/graduate` refuses this note until `status: ratified`.

## 1. Purpose and scope
<What this note decides. What is out of scope.>

## 2. Principles / decision
<The substance. State invariants explicitly.>

## 3. Consequences
<What downstream artifacts (plans, code, book chapters) this note licenses.>

## 4. Wiring & enablement
<!-- REQUIRED, ALWAYS PRESENT. A tool is useless until it is wired and ready to use — or at least
ready to flip on. Every design note states how the capability it designs becomes RUNNABLE; the ON
switch is never left as an unstated "later step" (finding-0159 — the code-ingest lane shipped
un-runnable: inert flag, no daemon enqueue, no CLI). Present even when there is nothing to do. -->

**How it wires:** <the connective tissue a plan must build so this can actually run — config
schema, daemon enqueue / CLI, the switch itself. Name the surfaces; it is IN-SCOPE, never a
deferred afterthought.>

**What it takes to flip it on:** <exactly one of —
- `N/A — no enable step: a fix / live on merge (a behavior change, not a new capability).`  (blank
  but present), OR
- the concrete steps: (a) the wiring a build must add, then (b) how the owner turns it on — e.g.
  "set `[x].enabled=true`", "run `palace <cmd>`", "flip the flag + the owner-visible seed run".>

## Parked decisions
<Each with a recorded default and a re-entry condition, so nothing is lost.>

## Cross-references
<Artifact ids and code `path@ref`. Everything asserted must cite a source.>
