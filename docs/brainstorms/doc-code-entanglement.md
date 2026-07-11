# doc-code-entanglement

Owner morning musings (2026-07-11, chat), restructured on append (§8, lossy capture beats
no capture). One train of thought: how meaning crosses representations — chunk grain,
docs↔code entanglement, docstrings as the Rosetta stone.

## 2026-07-11T09:30:00Z (captured)

```capsule
topic: doc-code-entanglement
date: 2026-07-11

decisions: []   # directions, not decisions — nothing ratified here

open_questions:
  - SMEAR: different chunk sizes resolve the same document differently — "a smear of
    resolution along the embedded vector space." Multi-scale embedding as an ensemble of
    grains per document. NOTE the collision: the source-set work (2026-07-03) deliberately
    confirmed single-scale-at-chunk-grain; this thought is supersession-shaped against
    that decision and needs evidence, not enthusiasm.
  - ENTANGLEMENT: theory/design docs and code reference each other — "entangled ... not in
    the same embedding region but there's a latent connection." Cosine proximity cannot
    see it; the connection is REFERENTIAL, not distributional. Which layer carries it?
  - ROSETTA: "notes and dialogue can more easily latch on to code semantics through ...
    well formed documentation wrapping the code." Docstrings as the translation layer
    between owner-language and code semantics. Standardize docstrings? Enforced how?
  - EDGES: "that might need to be edges that we help form or at least guide" — the first
    legitimate fiber-minting use case: today NOTHING mints E_geom fibers (2026-07-10
    survey; balance math runs on recomputed cosine only). Doc↔code reference edges are
    observer-independent and deterministic (AST + explicit citations), which is exactly
    the class the-edge-model.md §2 assigns to deterministic ingest, geometry authority —
    no Dreamer judgment, no blessing gate needed.

parked:
  - decision: multi-scale ("smear") embedding vs the standing single-scale-at-chunk-grain
      decision
    default: single-scale stands (2026-07-03 source-set decision; k× storage + retrieval
      fusion complexity not yet paid for)
    re_entry: a measured retrieval failure attributable to grain mismatch (query resolves
      at document grain, corpus embedded at chunk grain, or inverse) — the founding corpus
      + eval harness can run this as a CHEAP offline experiment (embed at 2-3 grains,
      measure hit overlap + rank divergence) before any store change
  - decision: docstring standard (format, required sections, why-not-what discipline)
    default: CONVENTIONS "comment the why" only; no format standard
    re_entry: the doc↔code edge experiment shows extraction quality gated on docstring
      form; or A8 lands and the orchestrator drafts the convention as a design note for
      owner ratification

next_steps:
  - Cheap, deterministic, additive — docstring extraction into the code-snapshot ledger
    (ops/code_snapshot.py already parses every AST; a docstrings column/table gives the
    Rosetta layer a queryable home + a per-commit doc-coverage metric for the evolution
    study). DEFERRED until bp-007 merges (it owns ops/** right now — collision).
  - Reference-edge inventory (read-only experiment): walk docstrings + design notes for
    explicit cross-references (path:symbol mentions, design-notes/*.md citations,
    [[note]] links) and count the latent edge set before deciding to mint any.
  - The smear experiment per the park re-entry above.
  - When drafted (post-A8 or owner hand): a design note tying this to the edge model —
    doc↔code reference edges as deterministic E_geom fibers, provenance-aware (code is a
    sensed stream per code-as-sensor-stream ruling; docstrings are its English shadow).

references:
  - docs/brainstorms/code-as-sensor-stream.md        # code = sensed stream; docstrings are its prose face
  - docs/design-notes/the-edge-model.md              # §2: deterministic ingest lays fibers
  - core/stores/sourceset.py                         # the single-scale decision this smear idea presses on
  - docs/findings/finding-0021.md                    # code as external corroboration — entanglement, evidenced
  - ops/code_snapshot.py                             # the AST walk the docstring layer rides on
  - scripts/ingest_self_knowledge.py                 # docs-as-curated; the bridge's other bank
```
