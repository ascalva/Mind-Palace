# Cross-strata & multi-scale dreamers

> Brainstorm topic: should some dreamer see the graph *as a whole* — across all strata, at multiple
> scales and clocks — and thereby build the connections that unify the strata? Seeded 2026-07-16 by
> the owner off the back of the first live dual-dreamer A/B RUN (dream_v2 over **13 authored notes /
> 4 edges** — a small authored substrate while the sensor strata grow constantly). Awaiting a **fable
> design pass** to graduate into a design note (full design, scope, goals; the firewall reconciliation
> made explicit). Design only; no build authorized by this brainstorm.

## 2026-07-16T15:31:54Z

```capsule
topic: cross-strata-and-multiscale-dreamers
date: 2026-07-16

decisions:
  - The idea splits into TWO threads that land very differently against the mirror firewall, and
    separating them is the point. IDEA A (multi-scale dreamers over the AUTHORED graph — local
    dreamers finding micro-patterns on a local clock, macro dreamers finding macro-patterns on a
    global clock) is FIREWALL-COMPATIBLE and a near-term thread; it is pure scope/scale on authored
    data. IDEA B (a dreamer that sees the WHOLE STRATA and builds connections BETWEEN layers to unify
    them) is the ambitious direction and hits the mirror firewall head-on; it needs a deliberate
    firewall-scope decision and must travel the artifact chain, never a casual build.
  - Idea A is expressible with machinery that already exists — the synchronic/diachronic axis is the
    design's spine (dream_v2 = synchronic/topological over one snapshot; DD-1 = diachronic across
    time, a different clock); "local vs global clock" IS Rule CLOCK (a Rate(κ) carries its clock in
    its type, capability-scope-algebra §2.3); "local vs macro scope" is expressible via the scope
    algebra's meet/join. So the multi-scale/multi-clock dreamer family is a NEW-DREAMERS question,
    not a new-boundary question.
  - The firewall-reconciliation PRINCIPLE for Idea B (the load-bearing insight): the mirror firewall
    (MIRROR_READABLE = {authored-solo, authored-dialogue}) protects WHAT GETS REFLECTED BACK AS
    AUTHORED INSIGHT — not necessarily what a subsystem may READ. A cross-strata / macro dreamer is
    therefore a DISTINCT `interpreted`-tier subsystem (NOT the mirror's reflective dreamer): it reads
    a COMPOSED / union scope (ObservedView ⊕ ReferenceView ⊕ … , not MirrorView), and everything it
    emits is `interpreted`-provenance, structurally unforgeable as authored (firewall ideal
    `s ⊓ ι = ⊥`). The strata get UNIFIED the safe way: the cross-strata dreamer PROPOSES connections
    as candidates; the ONLY sanctioned crossing into authored/mirror is OWNER RATIFICATION
    (observed/interpreted → owner authors → mirror). The system finds the connections; the owner
    decides which are actually part of their thought. This is a feature, not a limitation — it keeps
    the mirror trustworthy (a dream can never launder machine/third-party exhaust into what looks
    like the owner's insight, I5/I6) while still letting the whole strata inform discovery.
  - Owner intent (2026-07-16): capture the full spirit + rigor now; a FABLE PASS later to fully work
    out design, scope, and goals (design/gates tier per context-economy); then continue the harness
    build in the next session.

parked:
  - decision: The firewall-scope fork — does the mirror firewall forbid observed/non-authored data
      from seeding ANY dream, or ONLY the MIRROR dreamer's dreams (leaving room for a distinct
      cross-strata `interpreted`-tier dreamer)?
    default: the current firewall stands as written — MIRROR_READABLE = {authored-solo,
      authored-dialogue}; the mirror/reflective dreamer + contradiction scan are authored-only
      (core/mirror.py; "third-party observed exhaust can never seed a dream").
    re_entry: the fable design-note pass decides it deliberately and logs it — this sits NEAR an
      inviolable non-negotiable (the mirror firewall / fixed points are sacred), so the decision is
      human-only, deliberate, and recorded, not slipped into a build.

open_questions:
  - Is a COMPOSED cross-strata scope (a "union View" over authored ⊕ observed ⊕ reference ⊕ …)
    expressible under the scope algebra's firewall ideals, or does composing authored ⊕ observed
    collapse to ⊥ (`s ⊓ ι = ⊥`)? This grounds the whole feasibility of a cross-strata READ — the
    fable pass must settle it against capability-scope-algebra + core/scope.py.
  - What is the clock taxonomy for multi-scale dreamers — how do "local clock" and "global clock" map
    onto Rate(κ), and how do local-scope and macro-scope dreamers compose (do a local dreamer's
    micro-findings roll up as inputs to a macro dreamer, or are they independent lenses)?
  - How do cross-strata candidate-links surface for owner RATIFICATION? Is this the correlator's
    channel (Track D, ObservedView seam), the review-probe channel (E6/bp-048), or a new one? Is the
    macro/cross-strata dreamer a GENERALIZATION of the correlator, or a distinct subsystem beside it?
  - Does `authored-dialogue` actually flow into the mirror the dreamer reads TODAY? It is
    mirror-readable, so capturing owner↔Ambassador dialogue into the mirror is a firewall-RESPECTING
    substrate-growth lever available now — the φ_conversation-sensor brainstorm is exactly this thread.
  - Relationship to the existing dreamer roadmap: synchronic (dream_v2, built), diachronic (DD-1,
    design-only) — where do "local/macro scope" and "cross-strata" sit as axes alongside
    synchronic/diachronic? Is the full family a 3-axis space (temporal: synchronic/diachronic ×
    scope: local/macro × strata: mirror-only/cross-strata)?

next_steps:
  - A FABLE design pass (claude-fable-5, design/gates tier) to graduate this brainstorm into a design
    note: define the multi-scale / cross-strata dreamer FAMILY; state the firewall reconciliation
    explicitly (union-scope reads, `interpreted` output, ratification as the only authored crossing);
    resolve the firewall-scope fork; ground the scope-algebra feasibility; relate to the ratified
    notes (evaluation-harness, capability-scope-algebra, velocity-instruments, temporal-geometry,
    observed-data-and-the-assistant-tier, recursive-strata) and the correlator (Track D).
  - MEANWHILE (this is why the brainstorm is captured, not built): continue the harness build — the
    blessed build wave (bp-047 E3a-2 + bp-048 E6), then graduate E3a-1 (bp-046) against the resolved
    σ-fork. Idea A's multi-scale-over-authored thread is a near-term candidate once the harness lands
    (it measures dreamers; a new dreamer family wants the harness to evaluate it).

references:
  - core/mirror.py — MirrorView, the π_MR projection, the structural authored-only firewall ("the
    wrong state cannot be built"); the dreamer's current substrate.
  - core/provenance.py — the six provenance classes; MIRROR_READABLE = {authored-solo,
    authored-dialogue}; curated / interpreted / derived-stratum / observed all EXCLUDED.
  - core/sensing.py (ObservedView), core/reference_view.py (ReferenceView), core/temporal_view.py
    (TemporalView), core/dreams_view.py, core/ops_view.py — the sibling typed Views over other strata.
  - core/scope.py + docs/design-notes/capability-scope-algebra.md — scope meet/join, firewall ideals
    (`s ⊓ ι = ⊥`), Rule CLOCK (Rate(κ) carries its clock) — the algebra a union-scope must satisfy.
  - docs/design-notes/velocity-instruments.md, docs/design-notes/temporal-geometry-and-drives.md —
    Rate(κ)+clock; the diachronic frame (local vs global clock).
  - docs/design-notes/evaluation-harness.md — synchronic dream_v2; DD-1 (diachronic, consumes catalog
    instruments); the harness that would evaluate any new dreamer family.
  - docs/design-notes/observed-data-and-the-assistant-tier.md — the provenance-spectrum growth path
    (§1); the observed/assistant-tier boundary.
  - docs/design-notes/recursive-strata.md — DERIVED_STRATUM; depth-carrying derived; owner-verdict as
    the firewall crossing.
  - Track D correlator (ObservedView seam) — the existing "reads observed strata" subsystem the
    cross-strata dreamer may generalize; φ_conversation-sensor brainstorm — authored-dialogue capture.
  - The first live dual-dreamer A/B RUN (data/reports/2026-07-16-dreamer-ab/): dream_v2 over 13
    authored nodes / 4 edges — the concrete motivation (small authored substrate; sensor strata grow).
```
