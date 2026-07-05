---
type: build-plan
id: <bp-NNN or slug>
status: proposed          # proposed → ready → in-progress → complete | parked | superseded
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
links:
  - <design-note or related artifact path>
objective: "<one sentence: what one session will make true>"
contract: builder        # builder | scribe  (defaults to builder)
design_ref: "<design-note path + section that authorizes this plan>"
write_scope:             # THE capability — mechanically enforced by scope-guard (§6). Least-privilege.
  - "<glob>"
context_manifest:        # ordered read list; a fresh agent reads exactly these, in order
  - "<path>   # why"
acceptance:              # runnable, checkable criteria — each demonstrated in journal.md
  - "1. <criterion>"
non_goals:               # what this plan deliberately does NOT do (prevents scope creep)
  - "<non-goal>"
stop_conditions:         # what ends the session early (blocker finding; irreversible scope breach)
  - "<condition>"
session_budget: 1        # always 1 — plans are session-sized; split at graduation, never mid-build
re_entry: null           # REQUIRED string if status becomes `parked` — the condition that reopens it
supersedes: null         # prior plan id, if this P′ replaces a defective P
superseded_by: null      # successor plan id, once superseded
warrant: null            # the spec-defect finding id grounding a supersession
---

# <Plan title>

## Objective
<One paragraph expanding the one-sentence objective. What is true when this closes.>

## Interfaces pinned inline
<Copy the signatures, schemas, and invariants the builder must honor — verbatim,
never by reference. The builder must never infer design. (build-plan skill.)>

## Steps / deliverables
<Ordered, each mapping to acceptance criteria.>

## Acceptance evidence
<How each criterion is demonstrated in journal.md. Keep the journal newest-first.>
