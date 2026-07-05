---
type: finding
id: finding-<NNNN>
status: open             # open → routed → resolved | promoted
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
links:
  - <artifact this finding bears on>
ftype: question          # blocker | spec-defect | question | discovery
origin_plan: <plan id that raised it, or "orchestrator">
route: orchestrator      # orchestrator (design|math|direction) | builder (codebase|spec-fidelity)
resolution: null         # link or text, set on close
---

# <One-line finding title>

## What
<The gap, contradiction, question, or discovery — stated concretely.>

## Why it matters
<Consequence if unresolved. For a `blocker`: why the session cannot proceed.>

## Re-entry condition
<REQUIRED when the raising criterion is parked: the exact condition under which
work resumes. A parked item without a re-entry condition is not allowed (§3).>

## Routing
- `codebase | spec-fidelity` → the builder resolves, annotates here + journal, continues.
- `design | math | direction` → the orchestrator batches to `owner-questions.md`
  if owner input is needed; a design-changing `discovery`/`spec-defect` is proposed
  as a design-note supersession (or amendment) warrant-linked to this finding, then
  this flips to `promoted` (§11).
