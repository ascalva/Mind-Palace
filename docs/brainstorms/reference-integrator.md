# Brainstorm — the reference integrator: keeping the F-fiber (X_cite) fresh

> Captured by the orchestrator from owner chat (2026-07-21 ~15:35Z, session-39). Owner, on the
> heels of the fiber-geometry synthesis formalizing F = citation: *"maybe creating a reference
> integrator that keeps things up to date could be nice."* A freshness-keeper for the citation
> edge layer, which the owner's work exercises heavily (the artifact chain is dense with
> cross-references — front-matter `links`/`design_ref`/`warrant`, inline `docs/…` refs,
> `[[wikilinks]]`).

## 2026-07-21T15:35Z (session-39)

### The seed, grounded

**What already exists (so the idea is a keeper, not a green field):** the F-fiber has a built,
populated store — `core/stores/reference_edges.py` (X_cite), commit-keyed, symmetric
`(source_kind, source_ref) → (target_kind, target_ref)` over `{code, corpus}`. Extraction runs
today at two seams: **`ops/code_sensor.py` (φ_code)** for code↔corpus references (a model-less
sensor over the commit stream — `docs/brainstorms/code-as-sensor-stream.md`), and the **note
ingest** (`core/ingest/logseq.py` — the `[[…]]` regex + front-matter parse) for corpus links.
`ReferenceView` (bp-035) and the census (bp-080) read it. So references ARE extracted; the seed
is about *continuous freshness*, not first capture.

### Orchestrator chew

- **It is a SENSOR, not an integrator (a naming caution, like the census's).** In
  dn-agent-taxonomy the roles split by scope-signature: an **integrator** does witnessed
  *reasoning* (it mints C-edges — proven causal production — model-in-the-loop); a **sensor** is
  model-free deterministic extraction (φ_code is one). Reference extraction is deterministic
  parse-and-record — no model, no judgment — so the honest name is a **reference sensor** (the
  F-fiber's φ, sibling to code_sensor's code↔corpus φ). Worth pinning before the name sticks: F is
  recorded, not reasoned; calling its keeper an "integrator" would blur the sensor/integrator line
  the taxonomy draws. (The owner's word "integrator" = the intent "keep it current"; the taxonomy
  word is "sensor".)
- **The real content is FRESHNESS + RECONCILIATION, and neither is extraction (DRY).** The
  extraction logic exists twice (code_sensor, note ingest); a reference sensor should NOT
  re-implement it — it should *schedule* and *reconcile* it: (a) **incremental re-extraction** on
  corpus change — a scheduled model-free job in the trough tier, the `chat_events`/`vault_sync`
  pattern (single-writer, cheap); (b) **retirement of removed references** — a ref deleted from a
  note must retire its F-edge. The store is commit-keyed / per-commit re-minted, so "current" =
  the latest-commit set (the July census saw ~234 distinct pairs under a 76k row count precisely
  because rows accumulate per-commit); the keeper's job is to maintain a clean **current-view**
  (latest-commit, de-duped) so consumers don't re-derive it each read.
- **Why it matters — stale F is a stale reasoning graph.** F feeds: the census (bp-080's directed
  structure), the S↔F mismatch field (fiber-geometry M2 — citations without resemblance =
  cross-domain import), ReferenceView, and any future grammar/reasoning-path work (a citation move
  in a chain). If X_cite lags the corpus, every one of those reads a stale graph. So the keeper's
  value is proportional to how much the corpus changes — which, for this owner, is a lot.
- **Coverage is the adjacent question (an ingest gap, not the keeper's job).** The extractor
  captures front-matter relations + inline note-citation + `[[wikilink]]`. Whether **bare `docs/…`
  path references written in prose** (not front-matter) are captured is worth a check — if they're
  not, that's an extraction-coverage gap the keeper would faithfully keep *empty*. Fix coverage in
  the extractor first, then the keeper keeps the complete set fresh.
- **Measure-first (the house discipline): quantify the staleness gap before building.** How far
  does live X_cite lag the current corpus today? (Count references in the current tree vs edges in
  the store's latest-commit view.) If the daemon's ingest already re-extracts on each commit, the
  gap may be small and the keeper is a reconciliation/current-view convenience; if extraction is
  manual/lagging, the keeper is load-bearing. The number decides the plan's size.

```capsule
topic: reference-integrator
date: 2026-07-21

decisions:
  - The seed (owner): a component that keeps the F-fiber (X_cite / reference_edges) current as the
    corpus evolves. Seed only — no design decisions taken.
  - Naming caution the chew proposes: it is a reference SENSOR (model-free, deterministic — F is
    recorded, not reasoned), not an integrator (integrators mint C-edges via witnessed reasoning,
    dn-agent-taxonomy §2.5). Pin before the name sticks.

parked:
  - decision: new component vs scheduling+reconciling the existing extraction
    default: DO NOT re-implement extraction (code_sensor + note ingest already do it); the keeper
      is a trough-tier scheduled job (chat_events/vault_sync pattern) + a clean current-view
    re_entry: the measured staleness gap (below) shows extraction itself lags, not just the view

open_questions:
  - The staleness gap, measured: how far does live X_cite lag the current corpus (references in
    tree vs latest-commit edge set)? Small ⇒ a reconciliation/current-view convenience; large ⇒
    load-bearing.
  - Coverage: are bare prose `docs/…` path references extracted, or only front-matter + wikilink +
    inline? (An ingest-extractor question; fix before the keeper.)
  - Deletion semantics: is per-commit re-minting + a latest-commit current-view sufficient to
    retire removed refs, or is an explicit tombstone needed (kin to the staging sweep)?
  - Does it fold into the existing φ_code sensor (extend to corpus↔corpus refs) or stand as a
    sibling reference-φ? (DRY audit at the design pass.)

next_steps:
  - MEASURE the staleness gap first (read-only, cheap) — it sizes the whole thing.
  - If warranted, a small design pass / plan: the reference sensor as a trough-tier scheduled
    reconciler over the built extraction, maintaining a current-view; NOT new extraction.
  - Cross-ref the fiber-geometry measure-first battery (M2 consumes fresh X_cite) — a fresh F-layer
    is a precondition for the S↔F mismatch reading to mean anything.

references:
  - core/stores/reference_edges.py                  # X_cite — the F store (commit-keyed, symmetric)
  - ops/code_sensor.py                              # φ_code — the model-free sensor precedent (code↔corpus refs)
  - core/ingest/logseq.py                           # the [[…]] + front-matter extractor (corpus refs)
  - docs/brainstorms/code-as-sensor-stream.md       # the sensor framing this mirrors
  - docs/design-notes/agent-taxonomy.md             # §2.5 sensor vs integrator (the naming ruling)
  - docs/design-notes/fiber-geometry.md             # F = citation; M2 (S↔F mismatch) consumes fresh X_cite
  - docs/design-notes/self-sensing.md               # φ versioning (INTERPRETER_VERSION) discipline the sensor inherits
```
