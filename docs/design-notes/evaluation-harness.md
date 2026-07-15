---
type: design-note
id: dn-evaluation-harness
status: draft            # draft → ratified → superseded.  draft→ratified is an OWNER-ONLY hand edit.
implementation: not-built # the harness itself; §2.3 catalogs per-instrument reality (built-wired → design-only)
created: 2026-07-15
updated: 2026-07-15
links:
  - docs/brainstorms/evaluation-harness.md # THE WARRANT — consolidation synthesis + owner decisions 2026-07-15
  - docs/design-notes/capability-evaluation-harness.md # superseded on ratification; §5 batteries + V1–V5 carried as protocol annex
  - docs/design-notes/live-adoption-and-longitudinal-harness.md # superseded on ratification; L1–L5 shapes carried as protocol annex
  - docs/design-notes/holistic-testing.md # the taxonomy (attestation-as-oracle) this harness executes
  - docs/design-notes/test-organization.md # execution-profile homes (built-wired); longitudinal/ is this note's tenant
  - docs/design-notes/alignment-subsystem.md # the drift gauge frame; A2 axis-extensibility contract
  - docs/design-notes/dreamer-quality-suite-evaluation.md # F9 (built-wired); "thresholds are tuning, not code"
  - docs/design-notes/supersession-recovery-evaluation.md # instance #1 — protocol unchanged, first capability battery
  - docs/design-notes/velocity-instruments.md # ratified; RotationReport + alive/stale discriminator join the catalog
  - docs/design-notes/temporal-geometry-and-drives.md # ratified; demon-vs-source is an eval-harness item (§2.2 there)
  - docs/design-notes/capability-scope-algebra.md # §2.3 Inv/Rate(κ) — the catalog's typing discipline
supersedes: [dn-capability-evaluation-harness, dn-live-adoption-and-longitudinal-harness]
superseded_by: null
warrant: docs/brainstorms/evaluation-harness.md
---

# Design note — The evaluation harness: one subsystem for instruments, curves, benchmarks, and gated tuning

> Composed at **fable** (`claude-fable-5`, 2026-07-15, usage credits) from the consolidation
> warrant (`docs/brainstorms/evaluation-harness.md` — two Explore sweeps + owner decisions,
> 2026-07-15). Filed as `draft`; ratification is a hand edit by the owner — no command performs
> it, `gate-guard` denies any agent attempt, and `/graduate` refuses this note until
> `status: ratified`. **Design only; no build is authorized by this note.**

## 1. Purpose and scope

### 1.1 The question, and why now

The system now contains a unified query language (CQ-scope, live in v1.11.0), a second dreamer
(`dream_v2`, topological, about to replace the Phase-7 single-linkage pipeline), and a growing
family of dreaming instruments. Ad-hoc eval scripts stop scaling exactly here. This note defines
the **evaluation harness** as a first-class subsystem answering one compound question:

> **Which capabilities does the system demonstrably have, at what scale, attributable to which
> instrument — and are they holding, improving, or drifting over time, under which parameter
> settings?**

The testing story arrived in three waves that were never consolidated: the taxonomy wave
(`holistic-testing`, `test-organization`, `alignment-subsystem`), the executable-capability wave
(F9, supersession-recovery instance #1), and the two harness generalizations — the **offline
capability spine** (`dn-capability-evaluation-harness`: masked replay, a transformation algebra,
the r0→r8 ablation ladder, six batteries, an append-only eval-results store) and the
**operational/longitudinal spine** (`dn-live-adoption-and-longitudinal-harness`, "Track L":
shadow runner + run ledger, verdict store + review REPL, tuning manifest + gated apply,
longitudinal curves, continuous digest). Both spines declared shared machinery ("build it once");
neither was merged into one subsystem, and the newest ratified instruments (velocity pair,
temporal geometry) plus the self-sensor telemetry streams postdate both catalogs. The remaining
frontier — **automated parameter tuning** — was explicitly deferred by Track L §7. This note
fills the seam and designs that frontier.

### 1.2 Supersession decision, and the enumerated amendments

**This note SUPERSEDES both spine notes** (they are `draft` + `not-built`; no built code cites
them as authority). Rationale: the consolidation changes their content materially, and an
umbrella note over two amended drafts would leave three mutually-entangled authorities where the
artifact chain wants one. Their fine-grained protocol detail is **carried forward as the
protocol annex of record** — the capability note's §5 battery protocols, §7 candidate-instrument
menu, and §9 prerequisites/verification items (P1–P4, V1–V5); Track L's L1–L5 stage shapes and
builder-prompt scoping — valid as detail wherever this note does not amend them. The amendments,
enumerated so nothing changes silently:

- **A-1 (overnight thoroughness).** The owner runs the harness overnight; wall-clock is not a
  constraint. Every cost-constrained compromise in the spines is lifted — Track L §2's "3–5 σ
  values, cheap" becomes full-resolution grids; ladders run complete; curves run long (§2.8).
- **A-2 (bounded auto-apply exists).** Track L §7's "no verdict-driven automatic retuning" is
  revised by owner decision 2026-07-15: automated tuning is designed in BOTH modes —
  *measure+propose* (default) and *bounded auto-apply* (opt-in per lever) — under the §14 gate
  (§2.6). The prohibition survives as the default mode, not as the ceiling.
- **A-3 (catalog extended, typed).** The instrument catalog absorbs the ratified velocity pair,
  the structural A2 axes, effector drift, the coherence/rotation reports, and the adjudicator
  confidence panel, under the `Inv`/`Rate(κ)` typing discipline (§2.3) — all postdate the spines.
- **A-4 (backends decided).** Eval-results store → DuckDB (capability note Q5 closed: its access
  pattern is analytical group-by; append-only is a discipline, not a storage engine). Run ledger
  → SQLite/WAL (it is a ledger; the routing pin "telemetry/time-series → DuckDB; ledgers →
  SQLite" stands).
- **A-5 (shared machinery made literal).** ONE replay substrate, ONE run ledger, ONE
  eval-results store, ONE report generator, ONE scheduler serve both frames (§2.1–§2.2).

On ratification, the owner (or the orchestrator immediately after, as a non-blessing edit) stamps
`superseded_by: dn-evaluation-harness` in both spine notes.

### 1.3 Out of scope

No build (each §3 item is its own plan through the standard pipeline). No unparking of any
R-gated instrument (the ladder hosts unparking *vocabulary*, not decisions). No modification of
F9's protocol, its `THRESH` surface, or instance #1's fixture/answer-key/leak-check — both stay
canonical and become tenants. Not the diachronic dreamer (DD-1; it consumes catalog instruments).
No effector work — Track G stays unwired at every tier; **precision@review remains the
precondition for opening that boundary**, and this harness is what makes the number exist.

## 2. Principles / decision

### 2.1 The architecture: instrument → harness → report, over one substrate

- **An instrument** is a deterministic, read-only, erasure-invariant measurement producing one
  typed reading. No instrument holds a model in its measurement path.
- **The harness** schedules instruments, keys every reading, and turns readings into **curves**.
  The unit of evidence is a curve — an ablation curve across ladder rungs, a lever curve across a
  sweep grid, a longitudinal curve across time. Single readings are anecdotes.
- **A report** renders curves and verdict tables into local files. Reports never serve, never
  egress.

**The two frames are two corpus bindings of one engine**, not two subsystems:

| binding | corpus_ref | scores against | inherited from |
|---|---|---|---|
| **fixture-bound** (capability mode) | frozen transformed replay — `fixture:<hash>` | the mask / oracle / answer key | capability spine §1–§6 |
| **mirror-bound** (longitudinal mode) | live `MirrorView` snapshot digest, or the frozen control corpus | verdicts, drift, F9, structural axes | Track L L1–L5 |

Same run ledger, same eval-results store, same key, same report generator, same trough
scheduler. **The unified key:** every reading is keyed by

```
(spec_hash, corpus_ref, config_fingerprint, seed)
```

where `spec_hash` covers instrument id+version, pipeline identity, and battery parameters;
`corpus_ref` is a fixture hash (fixture-bound) or a Merkle corpus digest (mirror-bound);
`config_fingerprint` is the sha256 of the resolved tuning manifest. Curves are group-bys over
this key; the three confounds Track L named (corpus growth, config change, pipeline change) are
separable because each has its own key component.

### 2.2 The shared substrate

**Masked replay + the transformation algebra** — carried unchanged from the capability spine
(§1–§2 there, the protocol annex): an eval corpus is never a hand-mutated copy but a filtered,
transformed replay into a disposable scratch complex; variants are composable typed pipelines
(`subset / mask / scrub / inject / flip / permute / freeze`), deterministic given a seed; every
pipeline ends in `freeze`; every `mask`/`scrub` ships its leak check (a pattern hit fails the run
before the Dreamer sees anything); `mask` declares its metadata tier and the tier gap is itself a
reported measurement. Reset is free (discard scratch, replay); eval isolation is a soundness
invariant of the same rank as worktree isolation.

**The run ledger** — carried from Track L L1: append-only `dream_runs` + `dream_claims`
(SQLite/WAL, scheduler single-writer); claims content-addressed
(`claim_id = sha256(kind ‖ canonical(support_set) ‖ polarity)`, excluding surface wording and
confidence) so novelty, duplication, and verdict-carryover are well-defined across runs; `novel`
computed on insert; re-emitted claims inherit prior verdicts. **Build status (verified on disk
2026-07-15): NOT built** — no `core/stores/runledger.py`, no shadow runner. Track L's "Built:"
headers were spec, not reality; its `implementation: not-built` front-matter is the truth.

**The eval-results store** — new, the keystone: DuckDB (A-4), append-only discipline. A row is
`(key §2.1, metric_name, value, type_tag, interval_lo/hi?, evidence_ref)`. Non-promotable,
outside the complex, ∉ `MIRROR_READABLE`. Two properties fall out of append-only keying:
**resumability** (a keyed cell already present is skipped — an interrupted overnight sweep
resumes for free) and **honest longitudinal comparison** (every number knows exactly what state
it measured). Assertions over the store are regression-shaped first (§2.5). The drift suite's
frozen anchors (B, Θ) are explicitly not part of this store's lifecycle and are never derived
from it. `eval/metrics.py` (existing metric helpers) is absorbed into the registry at build time.

**The verdict store** — **already built** (`core/stores/verdicts.py`; Ed25519 signing in
`core/verdict/` per `verdict-authority`). The five-verdict taxonomy
(`novel_useful / true_known / plausible / wrong / noise`), the review REPL (`scripts/review.py`,
model-free display, keystroke verdicts, pipeline-labeled interleave = native A/B), and theory
probes carry unchanged from Track L §3. Verdicts are operational ground truth, not mirror
content.

**Three corpora, three lifecycles** — carried: the founding corpus (deliberately coherent; never
a control), the frozen control corpus (own `CURATED` graph; isolates pipeline/config effect from
corpus growth), and per-test eval fixtures (disposable, frozen per-run). Conflating any two
confounds the measurements built on them.

### 2.3 The instrument catalog and its typing discipline

Every catalog entry declares, at graduation into the catalog:

1. **Its result type** — `Inv` (depends only on the window's event set: counts, sets, booleans,
   subspace geometry) or `Rate(κ)` (a difference quotient against a declared clock; Rule CLOCK:
   a Rate carries its clock in its type and is never a bare number). Dedup is type-directed
   (X3): `Inv` readings may dedup across distinct-snapshot anchors; `Rate` readings never dedup
   — a plateau is data. Cross-anchor comparison of readings is a transport question governed by
   the type, never a subtraction of numbers from different slices.
2. **Its three clauses** (field-guide discipline): what it measures, its validity assumptions,
   and the observable that would show it is not earning its place. An instrument whose delta is
   indistinguishable from zero across the batteries is recorded as *no signal at this scale* and
   parked with a corpus-growth re-entry — never silently kept because the math is pretty.
3. **Its drift-axis registration**, where applicable — **A2 is the extensibility contract**: a
   new instrument enters the alignment picture as a new `Axis` that μ absorbs (capability rates ⊕
   conformance), so the catalog and the drift gauge grow together rather than forking.

Where an instrument reads the mirror-side weighted backbone, A7 binds: readings are taken at a
fixed interpreter version; a version boundary inside the window voids the reading (emit nothing).

**The catalog** (status verified against disk and the corpus audit, 2026-07-15):

| # | instrument | type | status | home | harness action |
|---|---|---|---|---|---|
| 1 | Golden-set recall (frozen queries vs `baseline.json`) | Inv | **built-wired** | `eval/golden.py`, `eval/golden/**` (SACRED) | consume as guardrail; never write near |
| 2 | A1 drift gauge `D(t)=d(μ(sₜ),B)` vs frozen B, tolerance Θ | Inv | **built-wired** (in the §14 validator) | `eval/drift.py` | guardrail + longitudinal curve |
| 3 | Attestation verification (chain completeness, signatures, Constitution fingerprint) | Inv | **built-wired** | `ops/attestation/**`, `scripts/verify_attestation.py` | the process oracle (§2.4) |
| 4 | Telemetry vitals + `context_usage` | Rate(wall) / Inv | **built-wired** | `core/stores/telemetry.py` (DuckDB) | cost + resource curves |
| 5 | F9 quality suite (apophenia, calibration, TF-IDF baseline, citation-ablation, decoy proxy) | statistical battery | **built-wired** | `tests/quality/` | objective components; `THRESH` joins the tuning surface |
| 6 | Structural snapshot axes (β₀, Fiedler, frustration, curvature, SBM, conductance, H₁) | Inv | **built, unwired** — SnapshotStore not passed by `build_dreamer`; written only in `dream_v2` | `core/complex/temporal.py` | **WIRE** (§3 E5); per-run rows |
| 7 | Effector drift | Inv | **built, detection-only, out of gate** | `eval/effector_drift.py` | catalog as report-only axis (Track G stays unwired) |
| 8 | CoherenceReport ‖[d,τ]‖ / β₁ citation instruments | Inv | **built, no live caller** | `core/temporal_view.py`, `core/temporal/complex.py` | **WIRE** as a replay-pair instrument |
| 9 | RotationReport (principal angles between harmonic subspaces at two anchors) | Inv | ratified, design-only | extends `core/temporal_view.py` | build via `dn-velocity-instruments` §3; catalog row reserved |
| 10 | Alive/stale hole discriminator ‖P_harm(Δw)‖ | Inv | ratified, design-only | `core/complex/hodge.py` projectors | ditto |
| 11 | Adjudicator confidence panel | Inv | **built, unwired** (`dream_rnd` lane) | dream_rnd adjudicator | wire into reports |
| 12 | Demon-vs-source protocol (V6 provenance-decomposed innovation over a dreamer-alone run) | Rate(κ) | design-only, R3/R4-gated | `dn-temporal-geometry` §2.2 | the harness hosts the protocol; the *run* is owner-gated |
| 13 | Capability batteries (structure recovery, edge proposal, polarity/negation, prediction, reasoning traces, metrology, RAG substrate) | per-battery | designed (protocol annex, capability §5) | `eval/capability/` | build (§3 E8); instance #1 first, unchanged |
| 14 | Longitudinal metrics (precision@review, novelty/duplication, grounding-defect rate, probe rates, confidence calibration) | Rate(run) / Inv | designed (protocol annex, Track L §5) | `eval/longitudinal.py` | build (§3 E7); **F4 lands here** |

**The ablation ladder r0→r8 is the attribution discipline** for every capability claim, carried
unchanged: a claimed capability is a claim about a *rung delta* on a named battery (r3 cosine is
the floor every reasoning claim must clear; r8 ≈ r3 means the machinery is a thesaurus).
Head-to-head slots host same-fixture bouts between instruments claiming the same capability; the
§7 candidate menu (magnetic Laplacian, Hodge decomposition, zigzag, GW alignment, conformal
prediction, PPR) enters only through ladder slots, three clauses attached.

### 2.4 Telemetry and audit: the harness's own evidence substrate

- **The harness is itself attested.** Every run emits an attestation
  (`action="eval-run"`, spec hash, corpus_ref, config fingerprint, seed, output hash); every
  tuning act (§2.6 — propose, bless, set, auto-set, rollback) is attested with old→new values,
  fingerprint before/after, and the evidence key of the sweep that justified it. The audit spine
  is the existing attestation store + the §14 proposal ledger + the run ledger.
- **Attestation-as-oracle is a battery, not a metaphor** (holistic-testing §1e, executable
  here): the process battery asserts over the chains a replay run generates — completeness,
  signature validity, Constitution fingerprint, input hashes resolving to authored records, no
  dreamer attestation referencing observed provenance. The system proves its own process on
  every harness run, not just on test runs.
- **The sensor streams are inputs:** φ_self (cost frontmatter → `AgentObservationStore`), φ_code
  (repo → `CodeObservationStore`), telemetry DuckDB (`vitals`, `context_usage`). The harness
  reads them; it does not write them.
- **The cost ledger closes a named gap** (no seal-cost store, no `/usage` view): a small
  cost/residency table in the telemetry DuckDB, written per harness run (wall-clock, models
  resident, cells completed), surfaced as the report's cost appendix (§2.7). Overnight capacity
  planning becomes measured, not guessed.

### 2.5 Metrics, benchmarks, and assertion shapes

**The metric registry** (`eval/harness/registry.py`) is the single namespace sweeps, batteries,
and reports may reference — no ad-hoc metrics. A registered metric declares: name; type
(`Inv`/`Rate(κ)`); source instrument (catalog row); comparability rule (which corpus_refs /
anchors it may be compared across — type-directed); assertion shape (`regression` | `absolute`);
and whether it is **guardrail-eligible**.

**Guardrails ≠ benchmarks.** The always-on guardrail set for any tuning act (§2.6) is:

1. golden-set recall unchanged against `baseline.json` (the frozen expectations);
2. drift `D(t)` within Θ (advisory until Θ is owner-blessed from calibrated curves — until then
   the harness reports, never trips);
3. grounding-defect rate ≈ 0 (a selfcheck failure, not a taste failure);
4. the integrity suite green (non-skippable, per `test-organization` §5).

**Benchmarks** are the golden set (fixed), the capability batteries (r-laddered), the F9 battery,
the RAG substrate battery (external corpora, scratch complexes only, subgraph-graded, no
LLM-judge), and the weekly control-corpus run.

**Assertion discipline:** regression-shaped first (no-worse-than the store's own history, with
agreed slack); a metric graduates to an absolute threshold only when its distribution stabilizes
— the `THRESH` lifecycle ("thresholds are tuning, not code"), applied family-wide. At n≤13,
owner-labeled batteries report intervals, not points; k-seed repetition reports per-case
agreement; nulls are recorded as no-signal-at-this-scale. B and Θ are excluded from this
lifecycle (frozen / owner-blessed).

### 2.6 The automated-tuning layer — the novel core

**The built surface this generalizes:** `ops/levers.py` — four bounded `[dreaming]` levers
(`dream_similarity_threshold` σ ∈ [0.55, 0.75], `dream_near_dup_threshold` ∈ [0.90, 0.99],
`dream_min_cluster_size` ∈ [2, 6], `dream_max_clusters` ∈ [4, 16]); the `config/levers.toml`
machine overlay (subordinate to `local.toml` — the human always wins); the §14 gate
(`ops/selfmod.py`: propose → approve → execute → validate-against-golden/drift →
keep-or-auto-rollback; fail-closed switches `[selfmod] enabled=false` and
`unattended_enabled=false`; `SAFE_LEVERS = {dream_max_clusters}`). Track L's L3 manifest
(`config/tuning.toml`, `scripts/tune.py show/set/history/--revert`, attested, fingerprinted) is
absorbed as the manifest layer over the same closed lever registry.

**The sweep spec** — declarative, versioned in-repo, the unit the optimizer executes:

```toml
[sweep.dreamer-sigma-ab]                       # the bp-040 instance, re-derived (§2.9)
levers      = { dream_similarity_threshold = "full" }  # "full" = manifest range at `resolution`, or an explicit list
resolution  = 21                               # grid points per lever
pipelines   = ["phase7", "dream_v2"]           # dual-dreamer A/B is native
corpus      = "mirror-snapshot"                # or "fixture:<hash>" | "control"
seeds       = 5
metrics     = ["f9_composite", "structural_axes", "golden_recall", "drift_D"]
objective   = "f9_composite"                   # a registry key; REQUIRED
guardrails  = []                               # additive only — the §2.5 defaults are always on
mode        = "propose"                        # can never exceed any touched lever's autonomy
```

**The optimizer is deterministic code — no model anywhere in the tuning loop.** A model may
annotate a report after the fact; it never selects a value, proposes a number, or applies one.
The curve is the adviser. Pipeline: evaluate the grid (per-cell rows into the eval-results store;
resumable by key) → assemble per-lever curves → **admissibility filter** (a cell failing any
guardrail is inadmissible regardless of objective score — guardrails are lexicographically
prior) → **selection rule**: prefer plateau centers over knife-edge maxima (stability beats
peak-chasing); tie-break toward least motion from the current value → emit a
`TuningProposal(lever, curve, selected_value, evidence_keys)`. Grid-first, not black-box
(Bayesian etc.): grids are auditable, resumable, and overnight-affordable; smarter search is
parked (EH-b).

**The two autonomy modes, per lever** (owner decision 2026-07-15 — locked):

- **`autonomy = "propose"`** — the DEFAULT, and the value when the field is absent. The
  optimizer measures and proposes; the proposal lands in the §14 proposal ledger and the owner
  inbox with its curve; **every `set` is an owner hand-blessing.**
- **`autonomy = "auto"`** — opt-in per lever, only by an owner hand-edit of the manifest (that
  edit is itself attested). Within `auto_band ⊆ range`, moving at most `auto_max_step` per
  application, at most once per `auto_cooldown_runs`; requires `[selfmod] enabled` AND
  `unattended_enabled` (the global kill switch freezes every auto lever at once);
  `SAFE_LEVERS` becomes **derived** — `{levers with autonomy = "auto"}` — generalizing the
  hardcoded frozenset. Every auto-`set` runs the full §14 validation (golden + drift) and
  auto-rolls-back on regression; every application is attested with its evidence key.

Per-lever manifest schema: `type, range, default, subsystem, autonomy` (+ for auto:
`auto_band, auto_max_step, auto_cooldown_runs`; optionally `objective` — the default registry
key this lever's sweeps optimize).

**The never-tunable fixed points are structurally unable to express either mode.** A manifest
key must resolve to a lever registered in `ops/levers.py`; the `Lever` constructor requires a
bounded range and a namespaced config-overlay path. The golden set (`eval/golden/**`),
`baseline.json` (B, Θ), `CONSTITUTION.md`, gate predicates, `MIRROR_READABLE`, and provenance
rules are not config-overlay values and have no lever constructor — **neither mode can name
them.** Backstops behind the structural exclusion: the foundation denylist; the loader
hard-failing on unknown keys; the gate refusing any proposal whose diff leaves the overlay.

**The objective function** (open question, decided): there is **no single global objective** —
the objective is a per-sweep declared registry key, with guardrails lexicographically prior.
Defaults by lever family: dreaming levers → `f9_composite` (apophenia + calibration +
beats-baseline delta + ablation survival, combined as *no-regression-on-all +
improvement-on-headline*, never as scalar weights — at 13-note scale scalar weights are
fiction); capability-instrument levers → the named battery's rung delta. **The designated
upgrade path:** once L2 verdicts accrue past a floor (set at E7 graduation),
**precision@review becomes the headline objective** and `f9_composite` demotes to a component —
owner judgment is the arbiter the whole apparatus exists to serve.

**The loop, closed:** sweep (overnight) → curves → proposal (or bounded auto-set) → §14
validation → ledger fingerprint boundary → the next runs' curves measure whether the tune
helped. Tuning efficacy is measured, not vibed — carried verbatim.

### 2.7 Report generation

`eval/harness/report.py` (+ a `scripts/` entry point) consumes the eval-results store, the run
ledger, the telemetry DuckDB, and attestation refs; it emits into
`data/reports/<YYYY-MM-DD>-<topic>/`:

- `report.md` (human) + `report.json` (machine) — same content, two renderings;
- **curves as terminal sparklines** + static markdown tables (HTML later, EH-g);
- **the drift study** — D(t) trajectory with per-axis decomposition (the A2 axes make the
  decomposition meaningful: *which* structural property moved);
- **sweep reports** — per-lever curve, admissibility overlay, the selected point, guardrail
  readouts, and the proposal's disposition (pending / blessed / auto-applied / rolled back);
- **A/B tables** — per-pipeline metric and verdict splits (Phase-7 vs `dream_v2`);
- **the cost appendix** — wall-clock, model residency, cells completed/skipped (§2.4).

**Every figure carries its key** `(spec_hash, corpus_ref, config_fingerprint, seed)` — no number
without provenance; every report is reproducible from the store. Generation is deterministic
templating — model-free. Reports are local files: no serving, no egress, ∉ `MIRROR_READABLE`.
The Voice's weekly digest (Track L §6, carried unchanged for later) narrates from the same
ledgers in the plain-language register; expected-update class, never an interruption.

### 2.8 The overnight-run profile

Design for **thoroughness, not cheapness** (owner mandate, 2026-07-15):

- full manifest-resolution grids (e.g. 21 points across σ's range, not 3–5);
- complete r0→r8 ladders per battery, per milestone;
- k-seed repetition for variance intervals on everything statistical;
- dual-pipeline everywhere the dreamer is touched;
- long replay horizons and weekly control runs for the longitudinal curves.

**What bounds a run:** the memory ceiling (≤ 2 resident models — the scheduler refuses breaching
work; model-heavy cells serialize; each sweep cell declares its residency); local compute; trough
scheduling at background priority. **What does not:** wall-clock (the night is the window) and
Claude budget (dream synthesis is the local 27b — an overnight sweep costs zero API tokens).

**Resumability is a requirement, not a nicety:** append-only keyed cells mean an interrupted
night resumes by skipping present keys. **No silent caps:** any run that bounds coverage
(sampled grid, truncated ladder, skipped battery) records what was dropped in the report — a
truncated sweep that reads as exhaustive is a lie in the evidence layer.

### 2.9 First passengers: testing the new machinery

**CQ-scope (bp-039, live).** The scope algebra gets property tests as first-class harness
tenants (`tests/property/` + `tests/integrity/`): lattice laws (idempotent, commutative,
associative, absorption) over `meet`/`join`/⊑; firewall ideals (`s ⊓ ι = ⊥` for every applicable
ι); Rule CLOCK (cross-clock meet raises at construction); delegation-exceeding-parent
unrepresentable (`minted = meet(parent, template)`); the declared-vs-actual scope audit per View
(the five inhabitants); and the typing layer's own falsifier — bit-identical reads. The harness
is also a *consumer* of the discipline: every harness read path is scope-typed (mirror-bound
runs read through `MirrorView` snapshots; eval stores are their own Σ, outside the mirror).

**The dual dreamers.** bp-040 `dream-calibrate` is re-derived as **the first sweep instance** —
`sweep.dreamer-sigma-ab` (§2.6): full σ grid × {Phase-7, `dream_v2`} × {F9 composite, structural
axes, golden, drift} × k seeds, on a mirror snapshot plus the control corpus. Its report is the
owner's first systematic sight of `dream_v2` output across σ (folds in oq-0024), and the
evidence base for the bp-041 wire-live decision. The A2 axes are first-class here: the
topological dreamer is measured in its own vocabulary (β₀, Fiedler, frustration, curvature, SBM,
conductance, H₁ per run). F9 binds both pipelines through the existing `DreamerAdapter` seam.
Track L §5's adoption criterion (precision@review ≥, grounding-defect ≤, novelty >, flat
control, sustained weeks) carries as the eventual verdict-based form of the flip decision —
computable as one pure function over the ledger.

### 2.10 Constraints honored (the binding table)

| constraint (BUILD-SPEC §3 + self-imposed) | binding form in this design |
|---|---|
| **Sacred fixed points** — golden set, B/Θ, Constitution never auto-modified | not lever-representable (§2.6, structural); `eval/golden/**` + `eval/golden.py` + `CONSTITUTION.md` on the foundation denylist, excluded from every grant; the harness measures against them, never writes near them; Θ owner-blessed, harness-advisory |
| **Eval isolation** — no eval run ingests or promotes anything, ever | scratch replay in the `dream_rnd` lane; eval outputs (proposals, dreams, scores) never ingest-eligible; external corpora → scratch complexes only; integrity test: no path from eval stores to ingest |
| **Mirror firewall** | verdicts, eval-results, shadow output, reports ∉ `MIRROR_READABLE`; control corpus in its own `CURATED` graph; integrity tests prove both |
| **Sealed core, zero egress** | reports are local files; no serving component exists; core import-lint unchanged |
| **The model advises; code acts** | instruments deterministic + read-only; review REPL display model-free; the optimizer model-free (§2.6 — the curve is the adviser); auto-apply is code under §14 |
| **Self-mod gate bounds all tuning** | every apply — hand or auto — transits §14; `unattended_enabled` is the global kill; `auto_band ⊆ range ⊆ registry bounds` |
| **Memory ceiling ≤ 2 models** | the scheduler's refusal binds sweep cells; per-cell residency declared; model-heavy cells serialize |
| **Control-corpus separation** | three artifacts, three lifecycles (§2.2) |
| **Regression-shaped at current scale** | registry assertion shapes (§2.5); absolute thresholds only on stabilized distributions |

## 3. Consequences — the build decomposition this note licenses (on ratification)

Session-sized plan candidates, blast-radius ordered. `/graduate` decides final splits; each plan
re-verifies the carried verification items (capability §9 V1–V5) that touch its scope, plus this
note's disk-status claims.

- **E1 — the eval-results store + metric registry.** DuckDB store with the §2.1 key, type tags,
  resumable keyed cells; `eval/harness/registry.py` with the built metrics registered
  (golden recall, drift, F9 components, telemetry). The keystone — everything else writes
  through it. Absorbs `eval/metrics.py`.
- **E2 — the run ledger + shadow runner** (Track L L1, carried): `core/stores/runledger.py`,
  `ShadowRunner` (both pipelines, one snapshot, one digest), trough wiring, content-addressed
  claims. Live surface provably unchanged.
- **E3 — the sweep engine + optimizer + tuning manifest.** Likely two plans: **E3a**
  measure+propose (sweep spec, grid evaluation, curves, admissibility, `TuningProposal` into the
  §14 proposal ledger; `config/tuning.toml` manifest + `scripts/tune.py`); **E3b** bounded
  auto-apply (per-lever `autonomy` field, derived `SAFE_LEVERS`, cooldowns, §14 unattended path
  generalized, rollback attestation).
- **E4 — the report generator + cost ledger** (§2.7, §2.4): `data/reports/` renderer, sparkline
  curves, the drift study, the cost appendix / usage view.
- **E5 — wire the flag-off instruments:** SnapshotStore into `build_dreamer` (per-run A2 rows);
  a live caller for CoherenceReport as a replay-pair instrument; the adjudicator confidence
  panel into reports; `effector_drift` as a report-only axis.
- **E6 — the review REPL + probes** (Track L L2, carried; the verdict store already exists).
- **E7 — longitudinal metrics + F4:** `eval/longitudinal.py`, the weekly control-corpus run,
  F9's two drift-deferred tests move into `tests/longitudinal/` (currently empty), the Θ
  calibration protocol (propose from p99 healthy inter-run variance after ~4 weeks; owner
  re-blesses), `adoption_ready(ledger) -> bool`.
- **E8 — the capability batteries** (`eval/capability/`, protocol annex): transformation algebra
  + ladder runner; instance #1 first, unchanged; P1 (codegraph extractor) its own plan;
  batteries gated on the carried prerequisites P1–P4.

**Sequencing:** E1 → {E2, E4} parallelizable; E3a needs E1; **the first overnight dual-dreamer
A/B needs E1 + E2 + E5(A2) + E4** — that run is bp-040 re-derived, and its report feeds bp-041
(wire `dream_v2` live). E3b follows E3a only after propose-mode has produced owner-blessed sets
(trust the loop before arming it). E6/E7 unlock the verdict objective (EH-c). The book gains the
harness chapter debt.

## Parked decisions

| id | decision | default recorded | re-entry condition |
|---|---|---|---|
| EH-a | supersession stamping of the two spine notes | `supersedes:` declared here; spines stamped `superseded_by` at ratification | owner ratifies this note |
| EH-b | optimizer search strategy | exhaustive grid (auditable, resumable, overnight-affordable) | a declared grid cannot finish in one night |
| EH-c | headline objective upgrade | `f9_composite` + guardrails | L2 verdict count ≥ floor (set at E7 graduation) → `precision@review` |
| EH-d | multi-lever joint sweeps | one-lever-at-a-time + explicit small joint grids | measured lever interaction (a lever's curve shifts across another's fixed values) |
| EH-e | Θ auto-calibration | harness proposes from p99 healthy variance after ~4 weeks; owner blesses in `baseline.json` | 4 weeks of longitudinal curves |
| EH-f | interval columns in the eval-results store | point value + optional CI lo/hi | first battery reporting intervals |
| EH-g | HTML reports | markdown + terminal sparklines v1 | owner asks for richer rendering |
| EH-h | external RAG corpus selection (capability Q4, carried) | unresolved | E8 graduation |
| EH-i | candidate-instrument menu (capability §7, carried) | menu only; none adopted | per ladder-slot entry, three clauses attached |
| EH-j | auto-apply beyond `[dreaming]` levers | dreaming-only | a second subsystem registers levers |
| EH-k | sweep-spec format (capability Q1, carried) | declarative TOML compiled to pytest-parametrized runs | a consumer the TOML cannot express |

## Cross-references

- `docs/brainstorms/evaluation-harness.md` — **the warrant**: the landscape (two Explore
  sweeps), the owner decisions (both autonomy modes per-lever; overnight thoroughness; bp-040
  subsumed; fable pass on credits).
- Superseded on ratification: `docs/design-notes/capability-evaluation-harness.md` (protocol
  annex: §1–§2 replay + algebra, §3 ground-truth taxonomy, §4 ladder, §5 batteries, §7 menu,
  §8 harness-quality/mutation testing, §9 P1–P4 + V1–V5); `docs/design-notes/live-adoption-and-
  longitudinal-harness.md` (protocol annex: L1–L5 stage shapes, verdict taxonomy, adoption
  criterion, digest/interruption policy).
- Frames: `holistic-testing.md` (taxonomy; attestation-as-oracle → §2.4);
  `test-organization.md` (built-wired; execution-profile homes — `integrity/` the non-skippable
  gate, `longitudinal/` this note's tenant); `alignment-subsystem.md` (drift frame; A2
  axis-extensibility → §2.3); `dreamer-quality-suite-evaluation.md` (F9, built-wired; the
  `THRESH` lifecycle → §2.5); `supersession-recovery-evaluation.md` (instance #1, protocol
  unchanged → E8).
- Instruments folded in: `velocity-instruments.md` (ratified; catalog rows 9–10, X1–X3 typing);
  `temporal-geometry-and-drives.md` (ratified; catalog row 12); `capability-scope-algebra.md`
  §2.3 (Inv/Rate(κ), Rule CLOCK → §2.3/§2.5) and §2.4 (the Views the harness reads through).
- Code (verified on disk 2026-07-15): `eval/golden.py` + `eval/golden/**`, `eval/drift.py`,
  `eval/effector_drift.py`, `eval/metrics.py`; `ops/levers.py` (the four `[dreaming]` levers),
  `ops/selfmod.py` (§14 gate, `SAFE_LEVERS`, fail-closed switches), `ops/ledger.py`,
  `ops/attestation/**`; `core/stores/telemetry.py`, `core/stores/verdicts.py` (+
  `core/verdict/`), `core/complex/temporal.py` (SnapshotStore), `core/temporal_view.py`,
  `core/temporal/complex.py`, `core/complex/hodge.py`; `tests/quality/` (F9),
  `tests/longitudinal/` (empty — E7's home). **Not on disk** (spec only, this note's
  deliverables): `core/stores/runledger.py`, `scripts/{tune,review,curves}.py`,
  `eval/longitudinal.py`, `eval/capability/`, `eval/harness/`.
