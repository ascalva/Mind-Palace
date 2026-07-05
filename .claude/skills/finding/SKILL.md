---
name: finding
description: Type and route a finding. Use when filing or triaging a finding — the ftype taxonomy, the routing rule, park-with-re-entry, and the promotion path into design notes.
---

# finding — typing and routing

A finding is the **only asynchronous channel** between sessions (§2.5). It is a
typed file in `docs/findings/`, attributable and committed. Template:
`docs/templates/finding.md`. Getting the type right determines where it goes.

## The `ftype` taxonomy

- **`blocker`** — the session cannot proceed and there is no re-entry that lets
  remaining work continue. Rare. Ends the session early (the Stop gate still
  demands a fresh journal on the way out). Everything that *can* be parked is not
  a blocker.
- **`spec-defect`** — the design record is wrong, contradictory, or
  under-specified in a way that changes what should be built. Warrant-grade: can
  ground a design-note supersession/amendment or a plan supersession.
- **`discovery`** — building revealed something new that bears on design (a better
  structure, a missed case, an emergent property). May promote into design.
- **`question`** — needs a decision or input, typically the owner's.

## The routing rule (constitution text, §5)

- **`codebase | spec-fidelity`** (a `question`/`spec-defect` the builder can
  settle against the code and spec) → **the builder resolves it**, annotates the
  finding and the journal, and continues. Do not escalate what you can settle.
- **`design | math | direction`** → **route `orchestrator`**. The orchestrator
  batches to `owner-questions.md` if owner input is needed. Never block: park the
  raising criterion with a re-entry condition and proceed with the rest (§5).

## Park with re-entry — always

When a finding parks a criterion, the finding **must** carry a re-entry condition
(the exact trigger that reopens it). A parked item without one is disallowed (§3).
Pair it, when owner input is needed, with an `owner-questions.md` entry whose
`default_if_unanswered` degrades to that same parked state — so an unanswered
question never stalls a builder (§10).

## Promotion path (§11)

A `discovery` or `spec-defect` that changes design does not get edited into a
note. The orchestrator proposes a design-note **supersession or amendment**,
warrant-linked to the finding (three-place: P, P′, warrant). The owner ratifies
or declines at the design blessing gate. On acceptance the finding flips
`routed → promoted`. Build output thus re-enters design through the same typed,
gated channel brainstorms do — never by side effect.

## Lifecycle

`open → routed → resolved | promoted`. Set `resolution` (link or text) on close.
