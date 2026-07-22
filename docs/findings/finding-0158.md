---
type: finding
id: finding-0158
status: routed           # open → routed → resolved | promoted
created: 2026-07-22
updated: 2026-07-22
links:
  - docs/build-plans/bp-094/plan.md
  - docs/design-notes/code-ingest-pipeline.md
  - core/stores/reference_edges.py
ftype: spec-defect       # blocker | spec-defect | question | discovery | direction
origin_plan: bp-094      # discovered building CI-3's paired-§ resolver
route: builder           # resolved in-scope with a documented v1 choice; design confirms the shape
resolution: v1 overloads target_detail for the §-anchor (paired-section gated OFF); design to confirm or add a field
---

# The `reference_edges` store has no section-anchor field for the paired-`§` rule (§2.4-2)

## What

`dn-code-ingest-pipeline` §2.4-2 rules that a `§N` token in a code docstring, when PAIRED
(the docstring cites exactly one resolvable note), mints an edge "to that note with
`source_detail` carrying the section anchor." But the v2 `ReferenceEdge` schema
(`core/stores/reference_edges.py`) has NO slot whose documented meaning is a section anchor:

- `source_detail` on a `code` endpoint IS the **qualname** (load-bearing — the code reading's
  coordinate; `_edge_id` and the finding-0063 v1 read-compat properties both key on it). It
  cannot also carry a `§` anchor without corrupting the code endpoint.
- `target_detail` on a `corpus` endpoint is documented `'' | digest`, and `corpus_kind`
  derives `"digest" if detail else "path"` — a non-empty `§` anchor there makes `corpus_kind`
  report `"digest"`, a wrong answer for the v1 read surface.

So the design's pinned interface (§6 REF_TYPES adds `dn-slug`/`finding-id`/`inherits`/`calls`
but NO section type, and the note says `source_detail`) is under-specified for where the anchor
lives. This is a §-interface disagreement, surfaced at build (per the plan's stop-and-raise).

## Why it matters

Without a clean home, the anchor either overloads a load-bearing field (source_detail) or a
type-derived one (target_detail → corpus_kind). Neither is free. The paired-`§` pattern is also
the most speculative of CI-3's resolvers (968 tokens, precision-first, PD-F parks unpaired) and
ships DISABLED behind `ENABLED_L2B_PATTERNS` until its M-C6 sample clears — so nothing mints
today, and the field decision can be made deliberately before the pattern is enabled.

## Resolution (v1, in-scope) + the design question

CI-3 implements paired-`§` minting `ref_type="note-citation"` (it IS a citation, to a section
of the note) with the anchor in **`target_detail`** — the *corpus* endpoint's refinement slot,
the least-wrong choice (it refines the target, not the code coordinate). The `corpus_kind`
caveat is real but inert: `corpus_kind` is a finding-0063 v1 read-compat property only exercised
by legacy `code_to_corpus`/`corpus_to_code` tests over the OLD patterns, never over a paired-`§`
edge. The pattern is gated OFF, so no such edge exists in any store yet.

**For design to confirm at enable-time (M-C6 / a future amendment):** either (a) accept the
`target_detail` overload and relax `corpus_kind`'s doc/derivation to exclude anchored corpus
targets, or (b) add a first-class `section_anchor` column (a genuine schema field, additive) so
the anchor is not overloaded onto an endpoint-detail slot. (b) is cleaner if paired-`§` clears
its precision bar and stays; (a) suffices if it lands narrow. The choice rides the pattern's
own enable gate, not this session.

## Routing

`spec-fidelity` → the builder resolved the in-scope half (a documented v1 `target_detail`
choice, pattern gated off, no data at risk) and routes the schema-shape confirmation to design
via the pattern's M-C6/enable gate (Item 2). Not a blocker: CI-3's other three patterns
(`dn-slug`/`finding-id`/`inherits`/`calls`) are unaffected and the paired rule is dormant.
