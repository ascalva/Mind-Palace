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
