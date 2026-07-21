# Edge-dynamics vector field — the velocity 1-cochain, the diachronic dreamer, and the query modes

Brainstorm family: `edge-dynamics-and-continuum.md` + `core-query-protocol.md`. This capsule holds the
owner↔orchestrator session that ran while `bp-035` (ReferenceView) was building — the second dreamer,
the velocity-field questions, the corrected covariance reading, the magnetic-unpark check, and the live
census. Grades tag every claim: **✓note** (in a ratified note, named), **~mine** (orchestrator synthesis,
NOT yet in a note — fable-grade), **?open**.

## 2026-07-15T04:52:47Z — the velocity field + the diachronic dreamer (opus/xhigh)

```capsule
decisions:
  - ReferenceView (bp-035, COMPLETE) is Mode 1 (structural, fibers F, no-time) of the three-mode
    query algebra (dn-core-query-protocol §2.2); specifically the 1a hard-connectivity corner.
    Mode 2 (semantic) exists (semantic_search); Mode 3 (temporal) is core/temporal, unwired. ✓note.
  - The "second dreamer" = the DIACHRONIC INTERPRETER (dn-core-query-protocol §2.7, Ruling B): reads
    the graph's MOTION (direction/velocity), not one snapshot's state. A DISTINCT interpreter, not a
    mode of the synchronic dreamer (Lane A/B firewall). Unblocks the registered-but-deferred
    change_point seam (interpreters.py:64,269). Two tiers — corpus-structural over X_cite ships first;
    the observed-plane weaving tier = the Track D charter. Consumes the velocity field below. ✓note.
  - The velocity 1-cochain ẇ_e = d/dt (edge strength) IS the phase-space momentum p that edge-dynamics
    §5 left as an OPEN OWNER CALL ("adopt the phase-space axis: q from snapshots, measured p from the
    chains"). This session ADOPTS that framing as the diachronic tier's substrate. ✓note (the call) +
    ~mine (adopting it).
  - The magnetic Laplacian OPERATOR stays PARKED (ML-a). None of the vector questions trips its three
    gates: they want the TEMPORAL evolution operator (Koopman/DMD, edge-dynamics rung R3), not the
    magnetic (spatial-directed) one. Conflating them is the exact category error dn-magnetic-laplacian
    §2.3/§2.7c exists to prevent (flux = the abelian SHADOW of the σ-transport; it forgets all content).
    ✓note.
  - Ran the arrow-aware combinatorial census on the LIVE store (2026-07-15, read-only; scratchpad
    census.py). Result: distinct doc→doc graph = 234 pairs / 113 nodes (the 76k row-count is per-commit
    re-minting). Directed cycles: 9 SCCs, 28/113 = 24.8% of nodes — but INFLATED by trivial sibling
    2-cycles + union-across-commits (only 2 SCCs > size 2). Retro-citations: 18/213 = 8.5% of dated
    pairs (target younger than source's original authorship → added by revision). Verdict: answers the
    owner's Q1 (retro-citations real + named), does NOT open magnetic gate (iii) — cycles inflated,
    retro modest. The cheap census ran first and taught the refinement, exactly as the note predicted.

novel_objects:   # ~mine — the fable-grade candidates this session generated; NOT in any ratified note
  - Velocity Hodge decomposition: apply gradient⊕curl⊕harmonic (edge-dynamics §2.2) to the VELOCITY ẇ,
    not the static edge vector. A harmonic component of ẇ = the corpus's CHANGE circulating around an
    unstated gap — knowledge sloshing around a question without converging. Falsifier candidate: does a
    nonzero harmonic-velocity coincide with an open `hole`-lens gap?
  - The velocity-covariance object (the owner's CORRECTED Q1 — cosine WITHIN the field, not across
    object types): C_ij = cos(ẇ_ei, ẇ_ej) over time-sample space is a PSD Gram/correlation matrix; its
    eigendecomposition = the empirical coherent modes = an operator-free, data-driven Koopman-lite
    catalog (ties to Q5's "distant edges moving together"). Anti-correlated edges (cos≈−1) = the
    fingerprint of SUBSTITUTION / paradigm shift (a rising framing tracking a falling one). And
    cos(ẇ_e, ẇ_graph) with ẇ_graph = mean velocity is a MARKET-BETA decomposition
    ẇ_e = β_e·ẇ_graph + ε_e: β_e = participation in the common corpus tempo, the residual ε_e = the
    edge-specific innovation. Needs aligned per-edge series (R1 gate — resample via splines).
  - Joint space×time spectrum: L₁-eigenmodes (graph Fourier, ✓note edge-dynamics §2.2) × Lomb-Scargle
    (temporal, ✓note R2, irregular sampling) → "which spatial circulation patterns oscillate at which
    temporal frequencies." harmonic-in-space + periodic-in-time = a THREAD THAT PULSES. R3/Koopman
    computes this as coupled spatiotemporal eigenmodes.
  - Distant-correlation ⟺ low-graph-frequency DUALITY: distant edges correlated in TIME ⟺ a global
    (low-L₁-frequency) spatial mode (a global mode is inherently non-local). Links Q4 and Q5 into one
    statement; a cheap test. ?open.
  - Normal-to-velocity = transverse STABILITY: the direction ⊥ the trajectory ẇ carries the
    attractor-vs-saddle information (is knowledge converging to a settled structure, or poised to
    bifurcate) = the real parts of R3/Koopman eigenvalues. (Also: normal-in-cochain-space = the
    curl+harmonic part by Hodge orthogonality — the change NOT explained by any node-potential.)
  - Prediction-residual-as-creative-signal (the session's deepest object): the AUTONOMOUS evolution
    operator (Koopman/R3, or R4 gradient-flow ẇ≈−∇V) predicts the DISSIPATION — where knowledge relaxes
    if the owner stopped thinking — because ✓note (dn-temporal-retrieval-algebra §2.5, Sz.-Nagy) the
    transport is a strict γ-contraction EXCEPT at owner promotions ("the owner is the only energy
    source"). So predict(G_{t+1}) − reality = the INNOVATION term = the measure of live creative
    direction. "Predict the next graph" is really "measure the resting-state so the owner's perturbation
    stands out." This is the same ε_e residual as the market-beta object, one level up.

parked:
  - Every novel_object above → fable-grade formalization, PARKED. Re-entry: the WEEKLY Fable cap resets
    Jul 17 8pm ET (currently 100% used) → a scoped fable pass to grade/formalize (velocity-Hodge
    well-definedness; the covariance-eigenmode = Koopman identification; the joint-spectrum object; the
    duality theorem; the residual-as-innovation framing). Do the cheap framing/grounding now; spend fable
    only on the reasoning depth (delegate skill's up-to-fable discipline).
  - The census as a PERMANENT diagnostic lens → candidate plan, deferred. Re-entry: a cleaner per-commit
    census (filter trivial sibling 2-cycles; anchor to one snapshot not the union) shows directed cycles
    are common, OR the diachronic dreamer's corpus-structural tier is built (it would consume the census
    as a claim source). Default: the one-off measurement (this session) suffices for now.
  - The magnetic operator (ML-a) → stays parked behind its three gates. This session's census did NOT
    open gate (iii). Re-entry unchanged (dn-magnetic-laplacian ML-a).

open_questions:
  - Sample depth: the distinct doc→doc graph is only 234 pairs / 113 nodes (young corpus). Is the
    velocity-field program PREMATURE until the corpus deepens enough for honest per-edge series (the R1
    gate, edge-dynamics §2.5 inversion — continuous fits gated on sample count)? Likely yes for now.
  - Does the diachronic dreamer's FIRST tier (corpus-structural over X_cite) need the velocity field at
    all, or can it ship on the exact-combinatorial census (retro-citations, cycles, diamond imbalance)
    while the velocity/spectral objects wait for depth? (Sequencing call at that graduation.)

next_steps:
  - Reference/query arc downstream graduations (dn-core-query-protocol): the diachronic interpreter
    (corpus-structural tier first), the build-time repo-derived twin (§2.4, owner ruled YES), the §2.1
    capability-scope type system (the fable-grade piece), wiring core/temporal into a query answer.
  - Post-Jul-17: a scoped fable pass on the novel_objects (grade + formalize the strongest — likely the
    velocity-covariance/Koopman-lite object and the prediction-residual framing).

references:
  - docs/design-notes/core-query-protocol.md  # §2.2 three modes; §2.7 diachronic interpreter (Ruling B)
  - docs/design-notes/edge-dynamics.md         # §2.2 Hodge/L₁ Fourier; §2.5 R1–R4 ladder; §5 phase-space open call
  - docs/design-notes/temporal-retrieval-algebra.md  # §2.5 Sz.-Nagy contraction / "owner is the only energy source"
  - docs/design-notes/magnetic-laplacian.md    # §2.3 refutation; §2.4–2.5 gradedness defect / retro-citations; ML-a gates
  - docs/build-plans/bp-035/plan.md            # ReferenceView (Mode 1) — COMPLETE
  - docs/findings/finding-0080.md              # the note-staleness reconciliation (oracle 0.996)
  - scratchpad census.py (2026-07-15)          # the one-off arrow-aware census: 234 pairs, 8.5% retro, 24.8% in-cycle (inflated)
```

## 2026-07-21T05:35Z — the THREE vector fields (one per fiber), session-39

Owner, near-verbatim: *"did we ever finish the edge-dynamics/velocity track? studying the vector
field produced by the edges — which now we can talk about differently since we have three vector
fields (three edge types)."*

**Track status, honest (the first half of the question).** The CORE is ratified + built, NOT
exhausted — it was deliberately parked with a customer-gated fringe:
- Ratified: `dn-edge-dynamics` (the 1-form lift, Hodge gradient⊕curl⊕harmonic, the R1–R4 ladder),
  `dn-velocity-instruments`, `dn-magnetic-laplacian`. Built: Lane A/B (bp-021/022). The one-off
  arrow-census ran (above).
- Parked-with-re-entry (NOT abandoned): PD-a (sheaf/general-transport, `laplacian.py` deferral),
  PD-b (weighted L₁), PD-c (Ollivier–Ricci), PD-e (gradient-flow potential), PD-f; the R3 Koopman/
  DMD rung gated on **corpus depth** (the R1 sample-count gate — flagged possibly premature at
  234 pairs/113 nodes; corpus has since grown, worth re-checking); and every `novel_object` above
  (velocity-Hodge, velocity-covariance/Koopman-lite, prediction-residual-as-creative-signal) still
  fable-grade unformalized.
- **The track is reactivating from the DEMAND side:** `clock-curvature.md` became the customer
  PD-c (Ollivier metric curvature) was parked awaiting; and THIS seed is the customer for **PD-a**
  (the sheaf / vector-bundle Laplacian) — see below. Both parks named "a customer appears" as
  their re-entry; the recent brainstorms are supplying them.

### Orchestrator chew — three fields, and what's genuinely new (the second half)

- **Each fiber is its own 1-cochain / vector field.** `w_F` (similarity strengths), `w_D`
  (derivation/supersession), `w_C` (causal witness) — three fields on the same node set, each with
  its own velocity `ẇ_F, ẇ_D, ẇ_C` and its own Hodge decomposition (gradient⊕curl⊕harmonic). The
  §2.2 machinery applies THREE times. That alone triples the instrument surface for free.
- **⚑ The new physics is the COUPLING, and it is literally PD-a.** Three fibers over each edge =
  a rank-3 **fiber bundle**; a joint vector field is a **section** of it; the Hodge theory over a
  bundle-valued / **sheaf Laplacian** is EXACTLY the "general-transport members (`laplacian.py`
  deferral)" that PD-a parked. So "three vector fields" is not a metaphor that reuses the fiber
  word by accident — it is the fiber-bundle whose Laplacian PD-a was waiting for a reason to build.
  This is the design consumer PD-a's re-entry names.
- **The cross-fiber MISMATCH field is the payload — and it rhymes with clock-curvature.** The
  interesting objects are where the fields DISAGREE: a strong `C` (causal) with weak `F`
  (similarity) = **causation without resemblance** (the non-obvious dependency — the valuable
  one); strong `F`, no `C` = mere resemblance (a similarity that never did any work). The F↔C
  mismatch field is kin to clock-curvature's effective-vs-embedding metric mismatch — same
  "two measures of the same pair diverge, and the divergence is the signal" shape.
- **The D-field is the clock (already established).** clock-curvature's dying-cluster capsule
  ruled "the D-fiber IS the thermometer" — D-arrow density per unit time = the churn/temperature
  field. So `ẇ_D` (the velocity of the derivation field) is the change-of-the-change — an
  acceleration of revision, the dynamics of the temperature itself. The three fields are not
  symmetric: F carries transit, C carries proven dependency, **D carries time**.
- **Discrete ⟺ continuum, unified with the fiber grammar.** The just-captured
  `fiber-chain-grammar.md` is the DISCRETE view of the same three-fiber structure (a chain spells
  a word over {F,D,C}; the grammar constrains valid transitions); THIS is the CONTINUUM view
  (three coupled fields, differential/Hodge). Edge-dynamics is built on exactly that discrete⟺
  continuum discipline — so the grammar and the vector fields are the two faces the note already
  anticipates.
- **Magnetic caution, honored.** Three DIRECTED fibers hint at a non-abelian gauge structure
  (where the abelian flux the diamond conjecture REFUTED, ML §2.3, might finally have content) —
  but that is ML-d territory (flux-aware/Weitzenböck), parked behind BOTH "a curvature customer"
  AND "the obstruction addressed." This seed is a candidate customer, not a gate-opener; the
  magnetic OPERATOR stays parked (ML-a). Do not conflate the bundle Laplacian (PD-a, real customer
  here) with the magnetic operator (ML-a, not opened).

```capsule
topic: edge-dynamics-vector-field
date: 2026-07-21

decisions:
  - Track status recorded (owner asked): core ratified+built (edge-dynamics/velocity/magnetic,
    Lane A/B); NOT exhausted — PD-a..f + the vector-field novel_objects + R3 Koopman (depth-gated)
    remain parked with re-entry. Reactivating from the demand side (clock-curvature→PD-c;
    three-vector-fields→PD-a).
  - The seed (owner): three fibers ⇒ three vector fields (w_F, w_D, w_C), each Hodge-decomposable;
    the new content is the cross-fiber coupling = a rank-3 fiber-bundle / sheaf-Laplacian object
    = the concrete consumer PD-a was parked awaiting. Seed only; no design decisions taken.

parked:
  - decision: the sheaf / vector-bundle Laplacian over the three fibers (PD-a's build)
    default: PD-a stays parked (flag complex only; general-transport deferred)
    re_entry: THIS is a candidate customer — a design pass grounds whether the coupling needs the
      bundle Laplacian or three independent scalar Hodge runs suffice (measure first)
  - decision: the magnetic/non-abelian reading of three directed fibers
    default: stays ML-d parked (needs curvature customer AND the Q1 obstruction addressed); the
      operator ML-a not opened
    re_entry: unchanged — this seed is a candidate customer only, does not open the gate

open_questions:
  - Does the coupling need a genuine bundle/sheaf Laplacian, or do three independent per-fiber
    Hodge decompositions + a scalar cross-fiber correlation (F↔C mismatch, D as clock) capture the
    payload without the heavier operator? (The DRY/measure-first call for the design pass.)
  - Is the corpus finally deep enough for the velocity/spectral tier (the R1 sample-count gate that
    made this "possibly premature" in July)? Re-run the depth check on the grown corpus first.
  - The F↔C mismatch field (causation without similarity): is it computable now from ReferenceView
    (F) + the C-fiber proven edges, and does it coincide with anything the dreamer already narrates?

next_steps:
  - A design pass (fable) candidate that treats the three-fiber bundle as PD-a's customer — AFTER
    the dreamer builds land (bp-080's census gives the C/D-fiber structure; bp-082's influence
    gives the differential machinery). Ground on the fiber composition semantics shared with
    fiber-chain-grammar (the discrete face).
  - MEASURE FIRST: re-run the corpus-depth check (R1 gate); compute the F↔C mismatch field on the
    current store before formalizing the coupling.

references:
  - docs/brainstorms/fiber-chain-grammar.md            # the DISCRETE face of the same three-fiber structure (captured same session)
  - docs/brainstorms/clock-curvature.md                # PD-c's customer; the mismatch-field shape; D-fiber = thermometer
  - docs/design-notes/edge-dynamics.md                 # §2.2 Hodge; PD-a (sheaf/transport) = the park this seeds; the discrete⟺continuum discipline
  - docs/design-notes/magnetic-laplacian.md            # ML-a/ML-d — the non-abelian caution; not opened
  - docs/design-notes/velocity-instruments.md          # the velocity substrate (ẇ per fiber)
  - docs/build-plans/bp-080/plan.md · bp-082/plan.md   # census (C/D structure) + influence (differential) — downstream enablers
```

## 2026-07-21T05:45Z — the DYNAMICS of the three fields (do they interact / share a surface?), session-39

Owner, near-verbatim: *"it would be interesting to study the dynamics of the three fields — do
they interact, are they even aware of each other? how does this field interact with change
clusters, how does it relate to conductivity, do they map different surfaces or the same surface?"*

### Orchestrator chew (five questions, one structure)

- **Do they interact / are they aware of each other? — YES, through TWO channels, and asymmetric.**
  (1) *Nodal (instantaneous) coupling:* the three fibers map different edge-structures but share
  the **0-skeleton — the node set**. A node is the switchboard where F, D, C states meet; the
  fields are "aware" of each other only AT shared nodes (a 0-dimensional interaction), not
  edge-wise. In Hodge terms their **gradient parts** draw on a common node potential (embedding /
  role), so they are correlated by construction wherever they share it. (2) *Generative
  (dynamical) coupling — the real awareness:* F **seeds** C/D formation (similar things get
  linked/revised), and a D-event (revision) **reshapes** the embeddings ⇒ changes F. So the fields
  drive each other's evolution — a reaction system: F → where C/D form; D-revision → F moves. (3)
  *The asymmetry:* **D is the clock** (established: D-arrow density = the temperature field,
  clock-curvature). D doesn't merely interact — it *parameterizes*: `ẇ_F` and `ẇ_C` are velocities
  measured in D-time. F and C are aware of D as their shared clock; D is aware of them only as the
  things it times.
- **Interaction with change clusters.** A change cluster IS a peak of the D-field (high clock
  rate). There the coupling is most visible: `ẇ_F` is large and often **incoherent** (high
  harmonic-velocity = the "sloshing" novel_object — churn circulating around an unsettled
  question), while **C lags** (causal structure crystallizes slower than similarity churns). The
  clock-curvature phase behavior is the three-field joint signature: **hot** = intense D + high
  incoherent `ẇ_F` + sparse C (scatter, route around); **cold/annealed** = quiet D + stable F +
  dense C (the crystal, route through). The change cluster is the single best place to *measure*
  the coupling because that is where the fields most visibly drive each other.
- **Relation to conductivity — via the Hodge split, cleanly.** Conductivity today reads F only.
  The three-field view: **three conductivities** (F = semantic reachability, C = causal
  reachability, D = lineage reachability), and the payload is the **composite** conductance over
  *grammar-valid composed chains* (the `fiber-chain-grammar` tie: which fibers a chain may use ×
  how each field conducts locally). The bridge is Hodge: a field's **gradient** part is its
  conductive throughput (flows high→low potential); its **harmonic** part is trapped circulation
  that conducts nowhere — the **conductivity DEFICIT**. So decomposing each field partitions it
  into conductive vs anti-conductive, and "the harmonic component coincides with an open `hole`"
  (the parked velocity-Hodge falsifier) is exactly "circulation that doesn't conduct."
- **Same surface or different? — DIFFERENT surfaces sharing a 0-skeleton = a SHEAF (PD-a again).**
  The three fibers induce genuinely different 1-skeletons: F is dense, ~undirected, cosine-weighted;
  D is a sparse directed DAG with the gradedness defect (its own geometry, ML §2.4); C is directed,
  witnessed, sparse. They are **three sheets glued along their shared nodes** — which is precisely
  a **sheaf over the node set** (different data per base point, glued by restriction), not one base
  with a clean rank-3 fiber. So: not the same surface, not disjoint — glued along the 0-skeleton,
  and *the coupling lives in the gluing*. The **F↔C mismatch field** literally measures where the
  surfaces DISAGREE: a C-edge whose endpoints are not F-adjacent = causation-without-resemblance =
  the two surfaces diverge on that pair. **This is the crux design decision for the PD-a pass:**
  are the three 1-skeletons similar enough to treat as ONE base with a rank-3 fiber (bundle view,
  lighter), or genuinely different topologies needing the full **sheaf Laplacian** (heavier, but
  what "different surfaces" implies)? Measure-first: compute the F/D/C skeleton overlap on the
  current store before choosing the operator.

```capsule
topic: edge-dynamics-vector-field
date: 2026-07-21

decisions:
  - Working frame the chew proposes (seed-level, for the PD-a pass to test): the three fields
    COUPLE via (a) the shared 0-skeleton (nodal, instantaneous — a node is the switchboard) and
    (b) a generative reaction (F seeds C/D; D-revision reshapes F); D is asymmetric — it is the
    clock the other two velocities are measured in. They map DIFFERENT 1-skeletons sharing the node
    set ⇒ a SHEAF (PD-a), not one clean surface; the coupling lives in the gluing; the F↔C mismatch
    field measures where the surfaces disagree. Conductivity = each field's Hodge GRADIENT
    throughput; the HARMONIC part is the conductivity deficit. Seed only.

open_questions:
  - Is the coupling strong enough to matter, or are the three fields ~independent in practice?
    Measure: cross-fiber correlation of the gradient potentials + the F↔C mismatch density.
  - Bundle (one base, rank-3 fiber — light) vs full sheaf (glued different topologies — heavy):
    which does the actual F/D/C skeleton overlap justify? The operator choice for PD-a's pass.
  - Change-cluster signature: does hot⇒(high incoherent ẇ_F, sparse lagging C, intense D) and
    cold⇒(stable F, dense C, quiet D) actually hold on the corpus's own dead vs live clusters?
    (Runs on the same dead-cluster scan clock-curvature already queued.)
  - Does the harmonic-velocity = open-hole coincidence (the parked velocity-Hodge falsifier) hold
    per-fiber, i.e. is a field's non-conductive part really its trapped circulation?

next_steps:
  - Fold into the PD-a design-pass scope (the three-fiber bundle/sheaf): the operator choice hinges
    on the measured skeleton overlap; the pass grounds on this dynamics framing + fiber-chain-
    grammar (discrete face). Still AFTER bp-080/082 land + measure-first.
  - Measurement battery (built instruments, before any formalization): F/D/C skeleton overlap;
    F↔C mismatch density; per-fiber Hodge gradient/harmonic split; the hot/cold three-field
    signature on dead vs live clusters — joins clock-curvature's measure-first list.

references:
  - docs/brainstorms/fiber-chain-grammar.md            # composite conductance over grammar-valid chains (the discrete face)
  - docs/brainstorms/clock-curvature.md                # change cluster = D-field peak; hot/cold phase; the mismatch-field shape
  - docs/design-notes/edge-dynamics.md                 # §2.2 Hodge (gradient=conductive / harmonic=deficit); PD-a (the sheaf operator this decides)
  - docs/design-notes/magnetic-laplacian.md            # §2.4 the D-DAG gradedness defect (D's distinct geometry)
```
