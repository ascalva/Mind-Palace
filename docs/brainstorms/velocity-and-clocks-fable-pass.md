# velocity-and-clocks-fable-pass — the rigorous pass over the two open brainstorm threads

> Fable rigorous pass (`claude-fable-5`, 2026-07-15, usage tokens — same session as
> `cq-scope-fable-pass.md`, owner-directed: "a proper, rigorous pass through the two other
> brainstorm documents"). Inputs read IN FULL: `edge-dynamics-vector-field.md` (the six
> `novel_objects`, all `~mine`/ungraded) and `temporal-clocks-and-strata.md` (all three capsules:
> clocks/relativity, velocity-conformal curvature, driven-dissipative). Held to consistency with
> the ratified frames: `dn-edge-dynamics` (R-ladder §2.5, Hodge §2.2, inversion), `dn-temporal-
> retrieval-algebra` (γ-contraction R6, σ_*/π_active, Sz.-Nagy R5, kernel-vs-topology R4), and
> this session's `cq-scope-fable-pass.md` (Rate/Inv typing, SLICE rule, clock poset). Grades:
> `[ESTABLISHED]` (external, named — flagged for verification) / `[DERIVED]` (proven here at
> fable) / `[SKETCH]` (defined, not proven) / `[REFUTED]` (the claim as stated is wrong; repair
> given). The two threads converge on ONE object — the velocity 1-cochain `ẇ` is both the
> vector-field program's substrate and the clocks thread's curvature source — so this is one
> pass in three parts: cross-cutting repairs (X), the vector-field objects (V), the
> clocks/geometry objects (T).

## 2026-07-15T18:17:22Z — the pass

## Part X — cross-cutting repairs (these bind every object below)

### X1. ẇ is a `Rate(κ)`-typed cochain on the common-edge restriction — birth/death are separate axes

`[DERIVED]` The velocity 1-cochain is used everywhere below, so pin its type first. Between
snapshots the edge set itself changes, so "d/dt of edge strength" is well-defined only where the
edge persists: `Δw` lives on the **common-edge restriction** (the bp-038 `_restrict` pattern,
lifted from citations to weights), with **edge birth and edge death as separate axes, never folded
into the derivative** (exactly as `CoherenceReport` keeps `nodes_added/dropped` out of
`coherence_norm`). And the difference quotient divides by a clock increment — so by CQ-scope rule
CLOCK, **ẇ is `Rate(κ)`: the clock is part of the object**, declared, never implicit. "Velocity
per commit" ≠ "velocity per event" ≠ "velocity per wall-day"; an undeclared-clock velocity is
ill-typed. Everything downstream (covariance, spectra, the J-field, the conformal geometry)
inherits κ.

### X2. The measurement/interpretation line: exact one-step differences are NOT R-ladder-gated

`[DERIVED — a genuine unlock]` The R-ladder (`dn-edge-dynamics` §2.5) gates **continuous fits**
(splines, spectra, operators) on sample depth, because a fit is an interpretation. But under the
inversion, the discrete record is the reality — so the exact one-step difference `Δw` on the
common restriction is **not an estimate of an underlying trajectory; it IS the record's own
increment.** It is measurement-class, like β₁ and ‖[d,τ]‖ — and indeed bp-038 already shipped a
two-snapshot instrument (‖[d,τ]‖) with no R1 clearance, correctly. **Rule: instruments consuming
exact per-step differences are available NOW (measurement-class); the ladder gates only smooth/
fitted readings of the series.** This un-parks the two-snapshot grain of several V-objects below
(and gives DD-1's corpus-structural tier exact objects to consume without waiting for R1). The
R1 gate stands unchanged for anything claiming a *trajectory* (a trend, a derivative-as-function,
a forecast).

### X3. The dedup question (clocks capsule 1, open q 1) is answered by the typing: it is type-directed

`[DERIVED]` "Raw ledger-append position or distinct-snapshot index?" — the general rule falls out
of X1 + CQ-scope S4: **`Inv` instruments may use either clock** (deduplicating byte-identical
states removes only plateaus, and an Inv value depends only on the event set — the answer is
unchanged); **`Rate` instruments must use the declared raw clock and must NOT silently dedup** —
a plateau is *data* for a rate (six commits with one identical snapshot is a rate observation:
zero change per six commit-ticks). bp-038's distinct-snapshot choice was right *because*
‖[d,τ]‖-as-count is Inv; the first Rate instrument must make the opposite choice on purpose.

## Part V — the vector-field `novel_objects`, graded

### V1. Velocity Hodge decomposition — well-defined, and it SPLITS into two instruments

`[DERIVED, with a repair]` Apply `P_grad ⊕ P_curl ⊕ P_harm` (built, `hodge.py`) to ẇ:

- **Fixed complex over the window** (common restriction): the projectors are constant linear
  maps, so they commute with the difference — `P_harm(Δw) = Δ(P_harm w)`. "Harmonic velocity" =
  the rate of change of the circulating component. Well-defined, exact at the two-snapshot grain
  (X2). ✓
- **Changing complex:** the projectors are themselves time-dependent, and the product rule
  forces a **connection term**: `Δ(P_harm w) = P_harm(Δw) + (ΔP_harm)(w)`. These are *different
  measurements*: (i) `P_harm Δw` — flow within the current topology; (ii) `(ΔP_harm) w` — the
  **rotation of the harmonic subspace itself**. The brainstorm's single "harmonic velocity"
  conflates them; the split is forced, and (ii) is exactly TRA Result 4 made measurable — chain
  maps transport homology but not kernels, so the harmonic *subspace* drifts even when β₁ is
  constant. **New instrument (measurement-class, two-snapshot, exact): the harmonic-subspace
  rotation** — principal angles between `H_n` and the common-restriction pullback of `H_{n+1}`.
  It is the metric-coherence complement of ‖[d,τ]‖: ‖[d,τ]‖ counts *topological* severing;
  the principal-angle spectrum measures *kernel* drift below the topological threshold.
- **The falsifier, sharpened.** As stated ("nonzero harmonic-velocity coincides with an open
  `hole` gap") it is near-tautological: `P_harm ẇ ≠ 0` requires `ker L₁ ≠ 0` requires β₁ > 0 —
  a hole exists *by construction* at matching scale. `[REFUTED as an empirical test; trivially a
  theorem one way.]` The real content is **dynamical: the alive/stale hole discriminator** — a
  hole whose carrying cycle has sustained nonzero harmonic velocity is being actively orbited
  (knowledge sloshing, unconverged); a hole with `P_harm ẇ ≈ 0` is abandoned structure. That is
  a genuine, falsifiable claim type for the THREAD/hole lens family, available at the
  two-snapshot grain per X2.

### V2. Velocity-covariance / "Koopman-lite" — PSD ✓; the Koopman identification is REFUTED; POD is the honest name

- `C_ij = cos(ẇ_i, ẇ_j)` over aligned samples is a Gram matrix of normalized vectors — PSD,
  trivially. `[DERIVED]` Eigenmodes = the **empirical orthogonal functions / POD modes** of the
  velocity field.
- **"Koopman-lite" `[REFUTED as identification; repaired as sequencing]`:** POD modes are
  energy-ranked spatial patterns; Koopman/DMD modes are eigenvectors of the fitted evolution
  operator. They coincide only for **normal** operators — and here the transport is generically
  **non-normal by structure**: σ_* is supported on the supersession strict partial order, hence
  upper-triangular in any linearization of the poset, and triangular-not-diagonal ⇒ non-normal.
  The operator is normal only in the no-supersession (diagonal decay) degenerate case — so **POD
  ≠ Koopman precisely when history matters** (when supersession is active), which is exactly
  when the diachronic program cares. The honest statement: POD is *the spatial half of the DMD
  algorithm* (DMD = project onto the POD basis, then eigendecompose the projected propagator),
  so the covariance object is a legitimate **R1-stage precursor that DMD (R3) reuses wholesale**
  — one rung early as *infrastructure*, never as *spectrum*. `[ESTABLISHED frame: POD/DMD
  relationship — from memory, verify: Schmid 2010 (DMD); Rowley et al. 2009 (Koopman spectral
  analysis).]`
- **Market-beta split** `ẇ_e = β_e ẇ̄ + ε_e`: an orthogonal projection onto the span of the mean
  series — standard, well-defined, and it is the **rank-1 case** of the nested hierarchy in V6.
  `[DERIVED]`
- **Anti-correlation = substitution — one confound to pin.** `[DERIVED caveat]` If the weight
  field is ever normalized (per-node or globally), velocities live on a simplex and **negative
  correlations are forced by closure** (the compositional-data artifact `[ESTABLISHED — verify:
  Aitchison 1986]`). Today's cosine-similarity backbone is not closure-normalized, so the
  fingerprint is admissible — but the instrument must carry "no compositional closure on w" as a
  standing hypothesis, checked, or substitution claims are artifacts.

### V3. Joint space×time spectrum — well-defined after ONE repair (eigenspace, not eigenvector)

`[DERIVED, with a determinism repair]` Project the series onto a **fixed** L₁ eigenbasis over
the window, per-mode series `a_k(t) = ⟨w_t, ψ_k⟩`, Lomb–Scargle per mode (R2 machinery,
irregular sampling — ✓note). The repair: **L₁ spectra carry degeneracies** (symmetric complexes
produce repeated eigenvalues), and within a degenerate eigenspace the eigenbasis is
arbitrary-up-to-rotation — per-eigenVECTOR series are then non-deterministic run-to-run,
violating the house determinism invariant. **Fix: track per-eigenSPACE projections** (the norm
of the projection onto each eigenspace) — basis-invariant, deterministic. "A thread that pulses"
= the harmonic-subspace projection (an eigenspace: `ker L₁`) with a significant L-S peak — the
cleanest instance, since the harmonic space is canonically defined. Gated R2 (needs series);
the object is now specified precisely enough to graduate when the gate opens.

### V4. Distant-correlation ⟺ low-frequency duality — HALF a theorem; the converse is false

- **Forward `[DERIVED]`:** if the velocity field decomposes over L₁ modes with uncorrelated
  amplitudes, `Cov(ẇ_e, ẇ_{e'}) = Σ_k σ_k² ψ_k(e) ψ_k(e')`; a dominant low-eigenvalue mode is
  smooth/delocalized, so its σ² spreads coherent correlation across graph-distant edge pairs.
  Dominant-low-frequency ⇒ long-range correlation. ✓
- **Converse `[REFUTED]`:** long-range correlation implies a *delocalized* dominant mode — and
  delocalization does **not** imply low frequency (high-frequency eigenvectors of sparse graphs
  are generically delocalized too; localization is the exception, not the rule). The duality as
  an iff is false; as stated ("links Q4 and Q5 into one statement") it survives only
  one-directionally. The cheap empirical test stands and is worth running when series exist:
  measure both and see *which* modes actually carry the long-range correlation.

### V5. Normal-to-velocity = transverse stability — a conflation, split

`[DERIVED — the split; the stability object ESTABLISHED-frame]` The brainstorm's two readings
are different objects and must not share a name: **(i)** stability transverse to the trajectory —
attractor-vs-saddle — is the real-part spectrum of the *linearized evolution operator* (Lyapunov/
Floquet), an R3/Koopman deliverable, correctly gated there; **(ii)** "normal in cochain space =
curl+harmonic by Hodge orthogonality" is not about the trajectory at all — it is the static Hodge
complement of the gradient part, i.e. V1 restated. Keep (i) as the stability instrument at R3;
delete (ii) as a separate object.

### V6. Prediction-residual as creative signal — the deepest object, and it lands PROVEN-conditional

`[DERIVED, conditional; the frame ESTABLISHED]` Formal home: the **innovations process** of
filtering theory (the part of `w_{t+1}` the fitted autonomous model cannot predict —
`[ESTABLISHED — verify: Kalman 1960; innovations representation]`). The tie to the algebra is
now a corollary chain, not a metaphor:

1. TRA R6 (unconditional theorem): the autonomous belief-view transport is a strict
   γ-contraction **except at owner promotions**.
2. Therefore IF the fitted `T̂` (R3 DMD / R4 gradient flow) consistently estimates the
   contraction, the residual `r_{t+1} = w_{t+1} − T̂(w_t)` is supported **exactly on the
   injection events** — the residual doesn't *correlate with* creativity, it *is* the injection
   channel, by R6. (Conditional on estimator consistency — an R3/R4-gated statistical question,
   honestly.)
3. **The system can do the attribution physics cannot.** `[DERIVED — the pass's best new
   result]` With the two-prime-movers correction (temporal-clocks coda 3), the injection has two
   channels — owner promotions and dreamer outputs — and **the architecture labels every event
   with its provenance already** (owner-verdict events vs `provenance='interpreted'` dream
   events). So the innovation decomposes **by construction**: `r = r_owner + r_dreamer`, no
   blind-source separation needed. The Maxwell's-demon question (T4) thereby becomes measurable:
   the dreamer is a *genuine source* iff `r_dreamer` maintains positive innovation against the
   frozen-corpus baseline over a dreamer-alone run; it is a *demon/heat-engine* iff its
   innovation decays to zero as it exhausts the owner's deposited gradients.
4. Birth/death events (X1's separate axes) are unpredicted by any fixed-complex `T̂` —
   creation is structurally the un-modeled part, consistent with the matter-creation reading
   (T3/T4).
5. The **nesting**: V2's market-beta residual is this same object under a rank-1 `T̂`
   (everything predicted by the global tempo); DMD is rank-k; the innovation hierarchy is
   ordered by model class, and each rung's residual is the next rung's target. One object,
   graded by the ladder.

## Part T — the clocks/geometry objects, graded

### T1. Causal-set / proper time — formal, small, and exact in this system

`[DERIVED; the frame ESTABLISHED — verify BLMS 1987]` In causal-set theory, proper time between
two events ≈ the length of the longest chain between them. Here each stratum's event set is
**totally ordered** (per-store sequences: op-seq, version_seq, RunLedger), so a stratum's
worldline between two cuts has longest-chain length = event count exactly — **"proper time =
N_s-increment" is not an approximation in this system; it is an identity.** The causal-set
subtlety only activates for the *unified* cross-store partial order (CQ-scope CS-a/CS-b, not yet
materialized), where longest-chain gives the canonical frame-free duration between two
antichains (cuts). Typing: chain-length duration is `Inv`; coordinate durations (per-commit,
per-wall-day) are the `Rate`-adjacent reparametrizations. This slots directly into the TRA §2
anchor question as its formal answer — **the ledger is a causal set; anchors are cuts; durations
are chain lengths; commit is the consistent cut for repo-backed strata** (CQ-scope S3). The
SR/GR shell stays evocative only (preferred frame exists; no boost group) — unchanged from the
brainstorm's own honest assessment.

### T2. The locally-clocked superconnection — DEFINED, with the reduction theorem; the gauge theory stays a sketch

The brainstorm's genuinely-new object, now given a precise form:

- **Definition.** `[DERIVED]` Work in the version bundle (the ledger/dilation space): objects =
  (note, version), morphisms = supersession steps (well-founded, op-seq). A **clock field** is
  `n : V → ℕ` — advance each note by its own number of local steps. **Admissibility:** the
  target family `{σ^{n(v)} v}` must be a **consistent cut** (an antichain in the version causal
  order) — the CQ-scope SLICE rule reappearing as the admissibility condition, which is the
  formal content of "a cross-stratum scope needs a consistent slice." The **locally-clocked
  transport** `τ(n)` carries an edge `{u,v}` to `{σ^{n(u)}u, σ^{n(v)}v}`, evaluated in the
  target cut's complex; the **curvature** is the holonomy of composing sheared transports
  around a graph loop that crosses regions of different clock rate — does the citation structure
  return to itself?
- **Reduction theorem.** `[DERIVED]` A constant clock field `n ≡ k` targets a global snapshot,
  and `τ(n)` reduces to the k-step global transport — for k=1, exactly the current two-snapshot
  `[d,τ]`. The brainstorm's consistency check ("does it reduce in the flat/global limit?") is
  answered **YES**.
- **Gauge.** `[DERIVED, one step]` The uniform part of a clock field is pure gauge (advancing
  every region equally is a global re-anchoring, not curvature) — consistent with the
  brainstorm's "a uniform rate can be reparametrized away." Only the *contrast* of n across
  space can source holonomy.
- **The rest is `[SKETCH]`**, and honestly data-gated: on the young corpus, version chains are
  almost all length ≤ 1, so every admissible non-constant clock field is trivially close to
  constant — the shear has nothing to shear. The full gauge theory (when are two non-constant
  fields equivalent; the holonomy group; the relation to diamond/merge structure TA-c) waits
  for per-note event depth. Parked with its existing re-entry (per-stratum N_s + R1 data).

### T3. The velocity-conformal geometry — three repairs make it computable; one over-reach refuted

- **Mean-centering is automatic — "global rate is gauge" is a theorem-let of the built
  machinery.** `[DERIVED]` `Φ = L⁺J`: the pseudoinverse annihilates constants (`L⁺𝟙 = 0` on a
  connected component), so Φ responds only to the **fluctuation of activity around its mean** —
  the uniform part of J (a global clock speed-up) sources nothing, exactly matching the
  brainstorm's own "uniformly-varying rate is FLAT." The intuition and the operator agree with
  no extra construction.
- **The source must be typed and placed.** `[DERIVED]` The settled source is `|ẇ|` (rate of
  CHANGE, the coda) — which by X1 is `Rate(κ)`: **the conformal geometry is clock-relative**;
  declare κ or the "curvature" is ill-typed. (The natural v1 declaration: per-event N_corpus —
  churn per unit of corpus activity — with wall-time as the alternative for physical-tempo
  questions. The two give genuinely different geometries; that is a feature, typed.) Placement:
  `|ẇ|` lives on edges; the GR-shaped picture wants a node density — pin v1 as node-aggregated
  `J(v) = Σ_{e∋v} |ẇ_e|`, the natural divergence-like marginal.
- **The concrete first instrument exists in known machinery.** `[DERIVED; ESTABLISHED — verify:
  Coifman & Lafon 2006]` The diffusion-maps α-normalization deforms the kernel by a density
  estimate `q^{−α}`; substituting the **activity field J for the density q** gives the
  activity-conformal diffusion `K_J = K/(J(x)J(y))^α` — a one-parameter instrument family where
  α dials how strongly churn bends the retrieval geometry. The "does activity attract or repel"
  sign question is then literally the sign of the empirical effect on geodesics — measurable,
  R1-gated (needs the J field, needs series), unchanged as an open empirical.
- **`ẅ` / the radiation reading — `[REFUTED for now]`.** The induction/radiation analogy
  ("changing sources produce radiated fields; true radiation is sourced by the second
  derivative") has **no formal home here**: radiation requires a wave equation — a metric
  signature and finite propagation speed — and the corpus has neither. `ẇ` sourcing a
  quasi-static deformation per window is coherent; `ẅ`-sourced "gravitational waves in the
  corpus" is vocabulary without an equation. Keep ẇ; park ẅ with the already-logged "which
  order of change" open question, now with the reason pinned.
- The coupling `f(Φ)` stays posited/measured (no principle selects it) — unchanged, honest.

### T4. Driven-dissipative / two prime movers — heat death is a corollary; the FDT question gets a real formula

- **Heat death is the Banach fixed-point theorem.** `[DERIVED]` TRA R6: the autonomous
  belief-view transport is a strict γ-contraction. Without injections, iterates converge
  geometrically to the unique fixed point; `|ẇ| → 0`; the velocity-conformal geometry (T3) goes
  flat. The brainstorm's "heat death" is not a metaphor — it is the contraction-mapping theorem
  applied to R6. Rate: gap closes as `γ^t` (the system's own γ names the cooling rate).
- **The two-mover reconciliation, sharpened one step further than the coda.** `[DERIVED]` In
  the **belief view there is exactly ONE injection channel** — owner promotions (R6 stands
  unweakened). The dreamer never appears as a second term in the belief dynamics; it **modulates
  the rate and quality of the single promotion channel** by keeping the queue full. The
  two-mover picture is exact in the **two-layer state space**: the INTERPRETED layer has its own
  dynamics driven continuously by the dreamer, one-way coupled into the belief layer through the
  promotion gate. (A skew-product system: dreamer drives upstairs; the gate samples downstairs.)
  This is the precise form of the coda's "two tiers coupled by the promotion gate" — and it
  makes the §2.5 erratum's wording checkable: γ-contraction for BELIEF, dreamer drives
  INTERPRETED, coupling = the gate. ✓ consistent.
- **The fluctuation-dissipation question has a concrete first formula.** `[DERIVED as a model
  statement; calibration R1-gated]` For a contraction driven by stochastic injections, the
  steady-state variance solves the discrete Lyapunov equation `Σ = T̂ Σ T̂ᵀ + Q`; in the scalar
  caricature, `σ² = q/(1 − γ²)` — the **corpus temperature**: injection variance q (dreamer-fed
  promotion stream) over dissipation `1 − γ²`. This is the promised FDT-flavored relation:
  measurable once R1 series exist, and it *predicts* what a "healthy fluctuating corpus" looks
  like quantitatively rather than rhetorically. The demon-vs-source question resolves through
  V6.3 (provenance-decomposed innovation; dreamer-alone run).
- **Third mover (DD-1)** — unchanged: a driver that feeds on ẇ and injects into the temporal
  layer; its formal slot is a second upstairs-layer in the same skew-product.

### T5. The unification candidate — one curvature, two faces `[SKETCH]`

The clocks capsule asked whether the activity-conformal curvature (#3) and the superconnection
`[d,τ]` (#2) are "two faces of one curvature 2-form on the space×time bicomplex." There is a
concrete candidate object: let the activity potential Φ (T3) **conformally weight the citation
coboundary** — `d_Φ = e^{−Φ} d e^{Φ}` (the standard conjugated/weighted differential) — and form
the superconnection `𝔸_Φ = d_Φ + τ`. Its curvature `[d_Φ, τ]` carries BOTH: the τ-side severing
obstruction (the current ‖[d,τ]‖, recovered at Φ ≡ const by the gauge fact in T3) and the
Φ-gradient coupling (how the transport interacts with the activity landscape). Flatness of 𝔸_Φ
is then a single coherence condition: *citations carry forward AND churn does not twist the
carry-forward*. Defined; not proven to be the right object; data-gated twice over (needs J and
per-note depth). The four-curvatures taxonomy (Forman / [d,τ] / activity-conformal /
Ollivier-bridge) stands — this candidate would *relate* #2 and #3, never conflate them with #1.

## What changed in the ledgers (the honest delta)

- The five VF-* objects now have **formalization DONE** (this pass); their **data gates are
  unchanged** (R1/R2/R3 as before) — except the two-snapshot grain of V1 (both instruments) and
  V6's provenance-attribution *design*, which X2 makes measurement-class and buildable now.
- T1 (causal set) and T4's reconciliation are ready to be **stated in a design note** (the TRA
  §2 anchor answer + the §2.5 erratum wording) — TRA is ratified/A8, so both ride the planned
  post-reset TRA revision (with the owner's erratum), for which this pass is now the warrant.
- T2's definition + reduction theorem and T5's candidate are **banked** for the revision note
  too; their empirical programs stay parked on depth.

```capsule
topic: velocity-and-clocks-fable-pass
date: 2026-07-15

decisions:
  - X1: ẇ is Rate(κ)-typed on the common-edge restriction; birth/death separate axes. Every
    downstream object inherits the declared clock.
  - X2: exact one-step differences are MEASUREMENT-class (R-ladder-exempt, the bp-038 precedent
    generalized); the ladder gates fits only. Unlocks two-snapshot velocity instruments now.
  - X3: dedup is type-directed — Inv: either clock; Rate: raw declared clock, never silent dedup.
    (Answers clocks-capsule-1 open question 1.)
  - V1: velocity-Hodge splits into P_harm(Δw) + (ΔP_harm)(w); NEW two-snapshot instrument — the
    harmonic-subspace rotation (principal angles), the metric complement of ‖[d,τ]‖ (TRA R4 made
    measurable). Falsifier-as-stated near-tautological → replaced by the alive/stale hole
    discriminator.
  - V2: covariance eigenmodes are POD, NOT Koopman (transport is order-upper-triangular ⇒
    non-normal ⇒ they differ exactly when supersession is active); POD legitimized as DMD's
    spatial half, one rung early as infrastructure. Compositional-closure caveat pinned.
  - V3: track eigenSPACE projections, not eigenvectors (degeneracy ⇒ determinism repair);
    thread-that-pulses = harmonic projection with an L-S peak. R2-gated, now precisely specified.
  - V4: duality is HALF a theorem (dominant low-frequency ⇒ long-range correlation); converse
    refuted (delocalized ≠ low-frequency). Cheap test stands.
  - V5: the conflation split — transverse stability = R3 Koopman real-parts; the Hodge reading
    is V1, deleted as a separate object.
  - V6: innovation process (Kalman frame); by TRA R6 the residual is supported on injection
    events (conditional on estimator consistency); PROVENANCE-DECOMPOSABLE by construction
    (r_owner + r_dreamer) — the demon-vs-source question becomes measurable. β-split = rank-1 of
    the same nested hierarchy.
  - T1: proper time = N_s-increment EXACTLY (per-store total orders make longest-chain = count);
    cross-store durations = longest chains between cuts, Inv-typed. The TRA §2 anchor answer.
  - T2: locally-clocked superconnection DEFINED (clock field n: V→ℕ; admissible iff the target
    is a consistent cut — the SLICE rule as admissibility); REDUCTION to [d,τ] at constant n
    proven (the brainstorm's consistency check: YES); uniform n is gauge. Full gauge theory a
    SKETCH, data-gated (version chains ≤1 today).
  - T3: Φ = L⁺J auto-centers (global rate is gauge — theorem-let); source typed Rate(κ) ⇒ the
    geometry is clock-relative, declare κ; v1 source = node-aggregated |ẇ|; first instrument =
    activity-for-density substitution in the diffusion-maps α-normalization; ẅ/radiation REFUTED
    for now (no wave equation ⇒ no formal home); f(Φ) stays measured.
  - T4: heat death = Banach on TRA R6 (cooling rate γ^t); belief view has ONE injection channel
    (promotions) — the dreamer modulates it, exact two-mover form = a one-way-coupled two-layer
    skew-product; FDT first formula: corpus temperature σ² = q/(1−γ²) (discrete Lyapunov),
    measurable at R1.
  - T5: unification candidate 𝔸_Φ = d_Φ + τ (conformally weighted coboundary) recovering ‖[d,τ]‖
    at constant Φ — SKETCH, twice data-gated.

parked:
  - decision: every V-object's DATA gate (R1/R2/R3 as in PARKING-LOT)
    default: unchanged — this pass cleared only the (ext) Fable formalization half
    re_entry: per-rung gates unchanged; EXCEPT V1's two instruments + V6's attribution design,
      which are measurement-class (X2) and may graduate ahead of R1
  - decision: T2 full gauge theory; T3 empirical program (sign, f(Φ)); T5 candidate
    default: banked as definitions/sketches
    re_entry: per-note version depth (T2/T5); the J field at R1 (T3); the post-reset TRA revision
      states T1/T4 (+ the owner's §2.5 erratum) with this pass as warrant

open_questions:
  - V4's empirical form: WHICH modes carry long-range correlation on the real corpus?
  - T3's sign (attract/repel) and coupling f(Φ) — empirical, unchanged.
  - T4: does the Lyapunov temperature match a healthy-corpus operating point the owner can feel?
  - V6/T4: the dreamer-alone run — demon or source? (Now fully specified as an experiment.)

next_steps:
  - /triage batches: the TRA revision (post-reset) now carries T1 + T4 + the owner's §2.5
    erratum, warranted by this pass — one revision, three payloads.
  - Measurement-class candidates for a future graduation (owner picks timing): the
    harmonic-subspace rotation (V1) and the alive/stale hole discriminator (V1) at the
    two-snapshot grain; V6's provenance-attribution design rides DD-1's charter.
  - VERIFY the flagged externals before any note/book cites them: Schmid 2010; Rowley et al.
    2009; Kalman 1960; Aitchison 1986; Coifman–Lafon 2006; BLMS 1987 (+ the CQ-scope pass's
    Lamport/Chandy–Lamport/Mattern/Fidge batch — one sonnet+web sweep covers both passes).

references:
  - docs/brainstorms/edge-dynamics-vector-field.md   # input, read in full — the six novel_objects
  - docs/brainstorms/temporal-clocks-and-strata.md   # input, read in full — all three capsules
  - docs/design-notes/edge-dynamics.md               # §2.2 Hodge/L₁; §2.5 the ladder + inversion (X2 sharpens)
  - docs/design-notes/temporal-retrieval-algebra.md  # R4 (V1's rotation), R5/R6 (V6, T4), σ_*/π_active
  - docs/brainstorms/cq-scope-fable-pass.md          # Rate/Inv typing (X1/X3), SLICE rule (T2 admissibility)
  - core/complex/hodge.py                            # the built projectors V1/V3 consume
  - core/temporal_view.py                            # the bp-038 restrict/two-snapshot precedent (X1/X2)
  - external [FROM MEMORY — verify]: Schmid 2010 (DMD); Rowley et al. 2009 (Koopman); Kalman
    1960 (innovations); Aitchison 1986 (compositional data); Coifman & Lafon 2006 (α-normalization);
    Bombelli–Lee–Meyer–Sorkin 1987 (causal sets).
```
