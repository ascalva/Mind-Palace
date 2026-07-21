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

## 2026-07-21T15:45Z — where it lives + ACTIVE vs PASSIVE sensors (owner, session-39)

Owner: *"where does it live? what type of agent is it? or is it just a sensor agent where its
sensor is the core itself — this actually brings up an interesting idea: sensors can be active or
passive. passive sensors just get data that needs to be parsed/interpreted/projected; active
sensors are the agent using its sensor(s) to investigate, like a microscope — the agent uses the
tool to understand and know how to act."*

### Where the reference sensor lives (the direct answer)

**A PASSIVE sensor, in `ops/`, model-free, trough-tier scheduled — and yes, its instrument is the
core itself.** It sits beside `code_sensor` (φ_code) and `self_sensor`: the same shape — a standing
φ-projection with an `INTERPRETER_VERSION`, writing F-edges to X_cite, no model, no world reach
(scope signature = the sensor role: a stratum write, W_Σ, nothing else). Its instrument is the
corpus's own authored reference structure — the palace sensing the graph it wrote, kin to
self-sensing (the palace observing its own code/state). "A sensor whose sensor is the core itself"
is exactly right, and it is the passive kind.

### The active/passive distinction — the real idea (developed)

- **Passive sensor = a standing model-free projection of an incoming stream.** It does not choose
  what to sense; it interprets whatever arrives (commits → code_sensor; chat → chat_sensor;
  observations → self_sensor; references → the proposed reference sensor). Continuous, scheduled,
  undirected. This is the taxonomy's **sensor ROLE** (dn-agent-taxonomy §2.5) — an agent kind.
- **Active sensor = an agent DIRECTING an instrument to investigate — the microscope.** The agent
  chooses where to point (region, cut, fiber, magnification) in service of understanding and
  deciding how to act. Query-driven, purposeful, model-in-the-loop. This is not a role — it is a
  **CAPABILITY** (an instrument grant) that reader-roles wield.
- **The crisp mapping (the insight names structure the architecture already grew):** an INSTRUMENT
  (σ*, census, Forman curvature) is neither passive nor active by itself — it is a capability; the
  MODE is in the use. The palace ALREADY has both, unnamed until now:
  - *Passive* is the `ops/` sensors — standing φ-projections keeping strata fresh.
  - *Active* is **the DreamCharter's instrument grant (bp-079, just built)**: a dreamer is granted
    instruments and points them via the **materialization boundary** (`force(grant, cut)` = aim the
    microscope, on demand, budget-gated). The owner's distinction is the name for the seam bp-079
    built.
- **The real-sensing analogy makes it exact.** Passive = receive an ambient signal (thermometer,
  camera). Active = *emit a probe and measure the response* (radar, sonar, an illuminated
  microscope). And the palace's active-probe apparatus is already built too: **bp-082's influence
  machinery + the HYPOTHETICAL subspace ARE active sensing in the radar sense** — stage a
  counterfactual, measure the graph's response (the with/without differential). Perturb-and-read is
  the most active a sensor gets.
- **"Understand and know how to act" = active sensing is the PERCEPTION half of agency.** It closes
  toward the effector layer (Track G, the hands): perceive actively (direct instruments) → decide →
  act. Passive sensors maintain the substrate the active perceiver reads. The two are not rivals —
  passive keeps the world-model fresh; active interrogates it to choose an action.

```capsule
topic: active-passive-sensing
date: 2026-07-21

decisions:
  - Placement (owner Q answered): the reference sensor is a PASSIVE sensor — `ops/`, model-free,
    trough-tier scheduled, INTERPRETER_VERSION'd, instrument = the corpus's own reference structure
    (self-sensing kin). Scope signature = the sensor role (a stratum write, no model).
  - The distinction (owner seed): sensors are PASSIVE (standing φ-projection of an arriving stream;
    undirected; the sensor ROLE) or ACTIVE (an agent directing an instrument to investigate — the
    microscope; a CAPABILITY = an instrument grant that reader-roles wield). Seed + a proposed
    mapping; a taxonomy pass rules whether it is a new axis or a naming of existing structure.
  - Proposed reading (to test, not adopt): active/passive is NOT a new taxonomy axis — it decomposes
    into what exists: passive = the sensor role; active = the DreamCharter instrument-grant dispatch
    (bp-079) + the influence/subspace probe (bp-082). The owner's insight names the perception seam
    the architecture already grew.

open_questions:
  - Is active/passive a genuine new taxonomy axis, or (proposed) already expressible as
    sensor-role vs instrument-grant-on-a-reader-role? The dn-agent-taxonomy pass decides.
  - Governance: an active sensor has side effects (staging, compute) — already governed by the
    DreamCharter budget/refusal gate (bp-079 L3); a passive sensor is bounded by its schedule.
    Does anything about active sensing need governance the instrument grant doesn't already give?
  - Does "active sensing informs action" want an explicit perceive→decide→act loop typed across
    the sensor(active) → dreamer/query → effector (Track G) seam, or is that Track D/G territory?

next_steps:
  - The reference sensor (passive) proceeds on its own measure-first track (parent capsule) — it
    does NOT need the active/passive distinction resolved to be built.
  - The active/passive framing is a dn-agent-taxonomy design-pass candidate (fable) — it may be a
    clarifying refinement (name the seam) rather than new machinery; grounds on bp-079's instrument
    grant + bp-082's probe as the two worked examples of active sensing.

references:
  - docs/design-notes/agent-taxonomy.md              # §2.5 the sensor role; role = scope signature (the axis this may or may not extend)
  - docs/design-notes/synchronic-diachronic-dreamer.md  # §2.2 the DreamCharter instrument grant = active sensing; §2.4 force = aim the microscope
  - docs/build-plans/bp-082/plan.md                  # influence + subspace = active sensing (perturb-and-read, the radar mode)
  - docs/design-notes/self-sensing.md                # the passive-sensor precedent (core sensing itself)
  - docs/brainstorms/code-as-sensor-stream.md        # the passive φ-projection framing
  - docs/design-notes/hands-and-the-effector-layer.md  # Track G — where "know how to act" lands (perceive→act)
```
