# Builder Prompt — Edge Model & Supersession Lifecycle: Investigate, Reconcile, Plan

**Mode: INVESTIGATION AND PLANNING ONLY. Do not implement anything. Do not
create, edit, move, or delete any file in the repository except the single build
plan named in "Deliverable." Wait for explicit owner approval before any
implementation, and before applying any documentation banner or cross-reference.**

## Context

The supersession-edge work (Items 6, 2a, 2b) is committed-pending. It surfaced a
reclassification: **supersession is a reasoning path, not a knowledge edge**,
which the two new notes formalize. Two of the resulting points are **corrections
to committed code**, not just additions — treat them as such. Everything is
provisional until confirmed against the code; ground it, answer the open
questions with citations, and produce an implementation plan the owner can approve
item by item.

## Required reading (in this order)

New notes:

- `docs/design-notes/the-edge-model.md` — statics (edge taxonomy, assertion
  authority, the E_geom ⊔ E_disp partition and the `L = D − A_geom` restriction).
New notes:

- `docs/design-notes/the-edge-model.md` — statics (edge taxonomy, assertion
  authority, the E_geom ⊔ E_disp partition and the `L = D − A_geom` restriction).
- `docs/design-notes/supersession-lifecycle.md` — dynamics (proposed→certified,
  the authored-content gate, grounding maintenance, the depth / γ^d decay math).
- `docs/design-notes/recursive-strata-amendment.md` — the change-spec for
  `recursive-strata.md` (depth carries two components; edge-budget extension; I10
  clarification). Read this **with** the current `recursive-strata.md`.

Then the notes and code they refine:

- `docs/design-notes/the-sacred-boundary.md` (§2.3),
  `docs/design-notes/ingest-identity-and-amendment.md` (§4A),
  `docs/design-notes/dialogue-ingest-and-recursion.md` (§3–§4),
  `docs/design-notes/recursive-strata.md` — a **correction target**, not a stable
  reference: apply `recursive-strata-amendment.md` (depth / γ^d, edge budgets,
  I10) with banners vs cross-references decided from its current text;
- the committed edge/version/claim-op stores and the deterministic recursion core
  (`core/stores/versions.py`, `core/stores/edges.py`, `core/ingest/sync.py`,
  `core/recursion_ops.py`), the depth / γ^d application, and the signed-Laplacian
  / frustration / clustering / curvature code.

Read whole files before citing; re-establish the filesystem connection if it has
dropped.

## Part A — Answer the open questions (with `path:line` citations)

**Every claim about current state carries a `path:line` citation.** Where the code
does not settle a question, say so rather than inferring.

- **Q9 — confidence bound terms (answered by the file; confirm in code).** The
  file's Invariant 10 is `c ≤ γ^d · g`: `d` = stratum depth (I4, echo-chamber term),
  `g` = grounding ratio (§6, inference-distance term). Both risks are already
  covered; **do not add or swap a depth term.** Confirm in code: where `γ^d · g` is
  applied, that `d` is the mint-time stratum stamp, and that `g` is computed as the
  §6 transitive grounding ratio. Then confirm the two exclusions the reasoning-path
  work requires: (a) `d` is not graph-computed (so supersession edges cannot affect
  it), and (b) the **grounding-ratio walk does not traverse dispositional
  (supersession) edges** — cite the walk. If it does traverse them, that is a bug
  (a supersession is not cited support).
- **Q10 — grounding of a revision (correction to Item 2b).** Does a claim
  `supersede` mint the alternative with `derived_from=[C]`, or with the warrant's
  K₀-reaching anchors? Cite. Assess against `supersession-lifecycle.md` §4.2:
  `[C]` makes the revision cite the claim it discredits and makes its grounding
  ratio `g` **collapse when `C` is superseded**; the target is warrant-anchors. The
  "derived can't out-rank authored" guarantee is preserved by `γ^{d≥1}` (not by
  grounding on `C`) — confirm it holds under the corrected grounding.
- **Q11 — the demotion (blessing) gate.** Does `superseded()` remove **blessed**
  content — authored (K₀) **or promoted-derived** (both retrievable) — from the
  active projection without a verdict, or is that gated (defeater + unpromoted
  derived alternative + verdict recommendation, blessed claim stays contested)?
  Cite. Free removal of **unpromoted** derived (not retrievable) is fine; silent
  removal of anything blessed is the gap (`supersession-lifecycle.md` §3). Confirm
  the indexing policy already makes unpromoted `DERIVED_STRATUM` non-retrievable
  (`recursive-strata.md` I5 → `security-planes.md` §6).
- **Q12 — disposition authority.** Does the active-projection disposition record
  **which authority** removed a claim (`owner-verdict` vs `dialogue-op` vs
  `decay`)? Cite.
- **Q13 — proposed/certified + candidate surfacing.** Is there a
  `proposed → certified` state on a claim `supersede`, or a single type? Cite. Is
  any unasserted-supersession candidate surfacing wired, or is the frustration /
  curvature machinery available to point at it (§6)? Cite the instruments.
- **Q14 — secondary.** Confirm (a) rename behaviour: does `doc_id = source_path`
  fork a version thread on file rename (§7)? and (b) no-op re-save: is a re-ingest
  of unchanged bytes logged as an **occurrence** rather than a phantom version
  (`ingest-identity-and-amendment.md` §2)? Cite both.
- **Q15 — promotion vs depth cap.** Does a `promote` verdict lift a derived
  claim's weight *within* the `γ^d·g` ceiling, or **re-anchor its stratum depth**
  so the ceiling rises? Cite the promotion path and whether it writes depth. If it
  only lifts weight within the ceiling, a good insight reached late stays capped by
  `γ^d` — flag for the §10 open-decision list (`supersession-lifecycle.md` §4.5).

Then list any **additional questions or risks** discovered during reading.

## Part B — Reconciliation proposal (propose only; do not apply)

For each affected doc, quote the passage this design corrects or extends and
propose a cross-reference **or** a partially-superseded banner (banner on
correction, cross-reference on extension; never silent replacement). In
particular, `dialogue-ingest-and-recursion.md` §4 / `recursion_ops.py` and
`the-edge-model.md` describe `derived_from` differently from the committed code —
that is a **correction**, so it takes a banner on the relevant note plus a code
change in the plan, not a silent edit. Present as proposed diffs.

## Part C — Build plan

Phased, each item independently approvable, each with an acceptance test and a
named falsifier. Respect the ordering in `the-sacred-boundary.md` §4 (verdict
store → close the loop → study) and phase by blast radius. **Mark each item
parallelizable or not, with explicit dependency edges.** Continue the item
numbering from the prior plan.

- **Item 7 — edge assertion-authority typing + structural E_geom/E_disp
  partition.** Add the `authority ∈ {geometry, dreamer-proposed,
  verdict-certified}` typing to the edge model; make the exclusion of
  dispositional edges from `A_geom`/`L` **structural** (dispositional edges in
  stores the balance math has no handle to — already true for the version and
  claim-op stores per Items 6/2b; state it as an invariant and verify no
  dispositional edge is ever assembled into `A_geom`).
  *Acceptance / falsifier:* clustering, frustration, and curvature results are
  **invariant** under adding or removing any dispositional edge; if one changes,
  `E_disp` has leaked into `A_geom`.
- **Item 8 — supersession lifecycle: gate + states + disposition authority.**
  Implement the **blessing gate** (Q11: superseding blessed content — authored or
  promoted-derived — records defeater + unpromoted alternative + verdict
  recommendation and leaves the blessed claim contested; superseding unpromoted
  derived is free), the `proposed → certified` two-state path with the verdict
  transition (Q13), and disposition-authority recording (Q12). Depends on the
  verdict store; leans on the existing indexing policy (unpromoted derived not
  retrievable).
  *Acceptance:* no blessed claim is removed from the active projection without an
  owner verdict; superseding unpromoted derived stays free; the proposed→certified
  transition **is** a verdict event; every removal record names its authority
  (`owner-verdict` / `dialogue-op` / `decay`).
- **Item 9 — revision grounding correction + grounding maintenance.** Re-ground
  claim `supersede` on the **warrant's K₀ anchors**, not `[C]` (Q10), with a test
  that the `γ^{d≥1}` guarantee (can't out-rank authored) still holds, and ensure
  the grounding-ratio walk skips dispositional edges. Implement `Stale(C)` =
  grounding-descendant closure, **flag-for-re-examination** (not cascade), and a
  Dreamer grounding-maintenance pass that emits **proposals**; surface `|Stale(C)|`
  backlog in the digest.
  *Acceptance / falsifier:* along a revision thread ordered by op-seq, a sequence
  of strictly-improving revisions does **not** show a falling grounding ratio `g`
  (the §4.4 falsifier — falling `g` means the revisions cite predecessors / build
  the tower rather than K₀ anchors); `Stale(C)` is the grounding-descendant
  closure; maintenance emits proposals, never silent edits.
  *Note:* corrects committed Item 2b but touches no stored data while the analyzer
  is no-op — sequence before a real `DialogueAnalyzer` is wired.
- **Item 10 — unasserted-supersession candidate surfacing (instrument).** As an
  **application of existing instruments** (signed Laplacian / frustration /
  Ollivier-Ricci), implement the candidate score `s(C,D)` and the blind-
  adjudication falsification experiment (§6). **Gated** on the Ollivier-Ricci
  re-entry condition (Track L shadow runner live + verdict taxonomy ratified); if
  unmet, record as parked with that re-entry condition rather than building now.
- **Item 11 — confidence-bound confirmation and exclusions** (`recursive-strata.md`
  Invariant 10, `recursive-strata-amendment.md` §0). The bound is **already**
  `c ≤ γ^d · g` — `γ^d` (stratum depth, echo-chamber) × `g` (grounding ratio,
  inference-distance). **No new depth term; no swap.** Verify both are wired (Q9),
  and enforce the two exclusions: `d` stays a mint-time stratum stamp (not
  graph-computed), and the grounding-ratio walk skips dispositional edges.
  *Acceptance:* adding or removing a dispositional edge changes neither `d` nor `g`
  for any node.
- **Item 12 — promotion vs depth cap (open decision, may be parked).** Resolve
  Q15: whether `promote` lifts weight within the `γ^d·g` ceiling or re-anchors
  stratum depth. If the decision is deferred, record it in `recursive-strata.md`
  §10 with the default and a re-entry condition; do not change promotion behaviour
  without owner ratification.

**Math to carry into the plan explicitly**, each with its field-guide clause from
the notes: the `L = D − A_geom` restriction to `E_geom`, derived *citation* edges
included and down-weighted by `layer_weight`, dispositional edges excluded (Item 7);
the `c ≤ γ^d · g` bound with `d` = stratum stamp and `g` = transitive grounding
ratio, both excluding dispositional edges (Item 11); the grounding-ratio-along-a-
thread reading as the tower/undulation diagnostic (Item 9 falsifier);
`Stale(C)` closure and its backlog load (Item 9); the candidate score `s(C,D)` and
adjudication experiment (Item 10).

**Dependency edges** (state and extend in the plan): Item 7 underpins Items 8–10.
Item 8 requires the verdict store. Item 9 is a correction to committed Item 2b —
sequence it ahead of any real analyzer; it composes with Item 8 (the gate decides
whether a supersede executes or is proposed; the grounding rule decides how `C′`
is minted when it does). Item 10 inherits the Ollivier-Ricci gate. Item 11 is
conditional on Q9. For every deferred decision use the parked-decisions protocol
(default, rejected alternatives with reasons, explicit re-entry condition).

Each item specifies: files to create or change (changed or new only), the
acceptance test, the invariant(s) it must not violate, and whether it touches
stored data.

## Deliverable

Write the build plan to a **single file**:

`docs/design-notes/build-plans/edge-and-supersession-build-plan.md`
(use the established build-plans location if one exists, and say so).

Contents, in order: (A) answered questions with citations and any new risks;
(B) the reconciliation proposal as proposed diffs, including the `derived_from`
correction; (C) the phased, parallelizable-marked build plan with acceptance
tests, the explicit math items, and parked-decision records.

Then **stop and wait for owner approval.** Implement nothing, and apply no
documentation change, until the owner approves — item by item is acceptable.
