---
type: finding
id: finding-0084
status: resolved
created: 2026-07-15
updated: 2026-07-15
links:
  - docs/build-plans/bp-039/plan.md
  - core/reference_view.py
  - tests/unit/test_reference_view.py
  - tests/integrity/test_ops_view.py
ftype: spec-fidelity
origin_plan: bp-039
route: builder
resolution: >-
  Resolved in-session (bp-039 Item 3). The public `SCOPE` ClassVar is the correct,
  layering-respecting design (EffectView.SCOPE must live in ops/effects.py, so a core-side
  registry is impossible without inverting ops→core). test_reference_view.py:82's exact-set
  assertion is more brittle than its sibling test_ops_view.py:34 (which checks
  `public & FORBIDDEN == ∅` and is robust to read-only additions). Fixed by acknowledging
  `SCOPE` in the expected set — the no-mutator guarantee is preserved unchanged, and every
  read-VALUE assertion in the file passes untouched (reads are bit-identical). The plan's
  write_scope was widened by ONE file (tests/unit/test_reference_view.py) with this finding as
  warrant, recorded in the journal and the plan diff.
---

# bp-039's public `SCOPE` retrofit trips test_reference_view.py's exact-public-surface assertion

## What
bp-039 Item 3 retrofits a public `SCOPE: ClassVar[Scope]` declaration onto each of the five Views.
`test_reference_view.py:82` asserts the EXACT public surface:
`public == {"references_to", "references_from", "connected_set", "commit", "over"}`. The new
read-only `SCOPE` constant appears in `dir(view)`, so this exact-set assertion fails — even though
(a) every READ is bit-identical (all value assertions in the file pass unchanged), and (b) `SCOPE`
is a read-only declaration, not a mutator, so the test's real guarantee ("reads and only reads — no
mutator reachable") still holds.

The sibling test `tests/integrity/test_ops_view.py:34` expresses the SAME intent robustly —
`leaked = public & _FORBIDDEN; assert leaked == set()` — and passed unmodified with `OpsView.SCOPE`
present. So the ReferenceView test is over-specified relative to both its sibling and the guarantee
it means to enforce.

## Why it matters
The plan's whole-plan falsifier was "every existing View test stays green, unmodified — bit-identical
reads." The reads ARE bit-identical; what changed is the public-surface ENUMERATION (a read-only
constant appeared). The graduation drew the write_scope one file too tight: it did not anticipate
that adding a public constant legitimately changes an exact-surface enumeration test while leaving
reads untouched. The layering-correct design (a class attribute, since EffectView.SCOPE must live
ops-side) requires the public constant, so the constant is not the defect — the exact-set assertion
+ the omitted write_scope entry are.

## Resolution
1. Widen bp-039's write_scope by one file — `tests/unit/test_reference_view.py` — warrant: this
   finding.
2. Add `"SCOPE"` to the expected public set at `:82` with a comment noting it is the read-only
   capability declaration (not a mutator); the no-mutator asserts (`add_batch`/`_conn`/`close`
   absent) are untouched.
3. No source read path changes; every read-value assertion passes unmodified (the bit-identical
   proof, now precisely "bit-identical reads" rather than "byte-identical public surface").

## Re-entry condition
None — resolved in-session. A future hardening (optional, not owed): migrate `:82` to the
`public & FORBIDDEN == ∅` pattern its sibling uses, so read-only additions never trip it. Recorded
here; not done now (minimal change preferred).

## Routing
`spec-fidelity` → builder resolves, annotates, continues (CLAUDE.md routing rule).
