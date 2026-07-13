# core-query-protocol

Owner direction (2026-07-13, chat): every agent — orchestrator, ambassador, sensors, and a
proposed new reference agent — is a **scoped client of the core**, and what's missing is the
shared, typed **query language they are all clients of**. Two threads emerged: (A) the
protocol + the client-scope model + a new deterministic single-stratum agent archetype;
(B) a math observation — removing the time dimension collapses the edge vector field's
gradient part to a scalar, which is the Hodge gradient/harmonic split seen from the time
axis (a feed for `edge-dynamics` Lane B). Captured together, threads kept separate.

## 2026-07-13T05:01:27Z (captured)

```capsule
topic: core-query-protocol
date: 2026-07-13

decisions:
  - The reference substrate already exists and is live: data/reference_edges.sqlite,
    ~61,380 edges, indexed on corpus_ref/code_path/commit_sha, ref_type ∈
    {note-citation, path-mention, symbol-mention, design-ref}, with source_line. A
    "where/how-many references to doc X" query runs TODAY (code↔corpus).
  - It is CODE-ANCHORED: only corpus_to_code / code_to_corpus edges. There is NO
    corpus_to_corpus (doc→doc) edge — a plan's design_ref citing a note, a finding's
    links/[[name]] — which is exactly the finding-0059 pain (a note's stale count cited
    by two plans, with no visible citation graph). Closing it is a bounded extractor
    addition over docs/**.
  - The librarian is a DIFFERENT tool than a reference lookup: semantic RAG over the
    authored mirror (MIRROR_READABLE firewall, budgeter, selfcheck) — reasoning, not a
    deterministic graph query. "Test the librarian" is a separate axis; the real synthesis
    is (i) the reference graph as a retrieval signal for the librarian, and (ii) a distinct
    deterministic reference surface for the agent-bookkeeping need.

thread_A_the_protocol_and_the_archetype:
  - Reframing (owner, corrects an earlier false View-vs-agent split): agents are NOT of
    different kinds; they are all CLIENTS OF THE CORE that must speak a precise interaction
    protocol. The orchestrator itself is "an agent that knows how to properly interact with
    the core." What differs is CAPABILITY SCOPE: which strata a client may read, and whether
    it may only-read / read+propose / write.
  - The new archetype: a DETERMINISTIC SINGLE-STRATUM QUERY SERVER — the read-side dual of a
    sensor. Not a sensor (writes nothing), not the ambassador (no model, no cross-plane).
    Because it touches ONE stratum only (lateral edges, never cross-stratum), it drops the
    ambassador's ENTIRE governance stack: no cross-stratum budget, no firewall question, no
    model, no hallucination surface. Every answer is a verifiable query result, attestable
    exactly like a sensor's projection. "No model" is correct, not a compromise — reference
    lookup is deterministic.
  - The missing artifact (point 3): a STANDARD TYPED QUERY ALGEBRA over the core's strata.
    The existing MirrorView / ObservedView / OpsView / EffectView are already PARTIAL,
    capability-scoped sentences in that language, not yet unified. The single-stratum
    reference agent is its simplest well-typed sentence: read(one stratum, fibers, no time).
    The ambassador is a long sentence: read(mirror+curated+ops), reason, propose. Same
    grammar, different scope.
  - Edge taxonomy grounding (recursive-strata-amendment): FIBERS = warrant/citation edges
    (budgeted lateral OR cross-stratum by where they land; the cross-stratum ones are "the
    tower's building material"). SUPERSESSION lines are a SEPARATE class — "dispositional
    edges" — which the grounding-ratio walk MUST NOT traverse. The time dimension lives on
    the dispositional class, held apart from citation geometry on purpose.

thread_B_time_collapse_math_LaneB_feed:
  - Owner intuition: the edge model is a vector field (strength + direction); the direction
    comes from direction in TIME (the supersession/dispositional edges carry time); remove
    the time dimension (d → d-1) and the vector field collapses to a scalar.
  - Grounding (edge-dynamics.md): the edge model IS a 1-form (1-cochain). The Helmholtz/
    Hodge decomposition splits it uniquely+orthogonally into GRADIENT (= d₀φ, induced by a
    NODE POTENTIAL φ, a scalar field on states), CURL (triangle circulation), and HARMONIC
    (= ker L₁, dim = β₁ — the THREADS).
  - The precise mapping: the GRADIENT part IS a vector field whose whole content is a scalar
    φ on states; its direction is ∇φ, and if φ is a time-coordinate (or authorship-distance)
    the direction IS time-direction. Strip the time-potential and the gradient part
    COLLAPSES to φ — the owner's "d-1 → scalar," correct FOR THE GRADIENT PART.
  - The sharpening (the payoff): it is correct ONLY for the gradient part. The HARMONIC part
    has, by definition, NO scalar potential — it cannot be written as ∇φ — so it does not
    collapse; it is precisely what SURVIVES the collapse, and it is the β₁ threads the THREAD
    lens keeps. So Helmholtz already names time-derived (gradient/potential) vs
    time-invariant (harmonic loops). The owner's morning vector-field intuition and the
    existing hole/thread instrument are the same object from two sides.
  - Why it matters for the roadmap: Lane A samples STATIC snapshots (the d-1 slices) and
    measures β₁ / harmonic-persistence per slice — exactly the part that survives the
    collapse. The genuine TIME flow (how slices connect, direction on dispositional edges)
    is the parked Lane B / continuum. This framing sits right on that seam.

parked:
  - decision: graduate this brainstorm to a design note (brainstorm → design)
    default: stays a brainstorm; no design note yet
    re_entry: THE OWNER OPENS A FABLE-TIER DESIGN SESSION. The brainstorm→design pass is
      fable work (open architecture, unpinned interfaces, a cross-plane boundary ruling, and
      a math framing that feeds Lane B) — NOT to be drafted at opus/sonnet. This is the
      owner-requested fable-guard on the brainstorm→design process (2026-07-13).
  - decision: one design note or two
    default: undecided — likely TWO (an architecture note: the core-query protocol +
      client-scope model, with the reference archetype as its simplest case; and a math
      note / Lane B feed: the time→gradient collapse framing)
    re_entry: the fable design session decides the split at graduation
  - decision: shared live substrate vs. a build-time reference index
    default: undecided — "it's already live, make it useful for us" wants the workflow to
      query the daemon's stratum directly (max dogfooding, crosses the sacred boundary); the
      safe alternative is a separate build-time index (no crossing, duplicates the sensor)
    re_entry: the design pass rules on the-sacred-boundary question below
  - decision: does the sacred boundary permit build-time query of the live reference stratum
    default: PLAUSIBLY clean — the reference graph is corpus-STRUCTURAL (who-cites-what), not
      observed exhaust (not the mirror, not private interaction data) — but this needs an
      EXPLICIT ruling, expressed as a capability SCOPE, not a special case
    re_entry: the fable design session, referencing docs/design-notes/the-sacred-boundary.md

open_questions:
  - What are the query primitives of the core-query algebra, and how is capability-scope
    expressed (which strata × {read | read+propose | write})?
  - Is the reference agent a ReferenceView (library object a caller constructs) or a
    request-addressable service across the process boundary? "Takes requests, responds back"
    leans service; the single-stratum discipline holds either way.
  - Should the doc→doc extractor land first (retires finding-0059/0061's class immediately),
    independent of the larger protocol design?
  - Does the time-collapse framing change how Lane B models the flow (gradient = the
    time-potential channel to model; harmonic = the invariant to hold fixed)?

next_steps:
  - HOLD for a fable design session (the fable-guard above). Until then this brainstorm +
    finding-0062 carry the thread; no design-note edit, no build.
  - The doc→doc extractor MAY be split out as a small independent plan if the owner wants the
    finding-0059/0061 class retired before the full protocol is designed.

references:
  - docs/findings/finding-0062.md  # the direction finding this brainstorm expands
  - docs/findings/finding-0059.md  # the doc→doc-blindness instance
  - docs/findings/finding-0061.md  # the stale-baseline class the reference graph would guard
  - core/stores/reference_edges.py # the live substrate (61k edges) + its minimal query API
  - core/librarian/librarian.py    # the semantic-RAG tool (a different axis)
  - agents/ambassador/agent.py     # the heavy read-side client (the long sentence)
  - core/mirror.py, core/sensing.py, core/ops_view.py, ops/effects.py # the existing partial Views
  - docs/design-notes/recursive-strata-amendment.md # fibers vs dispositional edges; edge_budget types
  - docs/design-notes/edge-dynamics.md # the 1-form lift, Helmholtz split, THREAD lens, Lane A/B seam
  - docs/design-notes/the-sacred-boundary.md # the plane-crossing ruling this needs
```

## 2026-07-13T05:12:18Z (captured — self-grading eval loop + pseudo-RAG crystallization)

```capsule
topic: core-query-protocol
date: 2026-07-13

thread_C_self_grading_eval_loop:
  - Idea (owner): the reference agent is self-testable from day one — ask for a reference,
    get a result, immediately CHECK if it was correct, keep a performance record. Because
    reference lookup is DETERMINISTIC, the judge has FREE, CORRECT ground truth — STRONGER
    than LLM-as-judge (a differential test against an oracle, not a subjective call). Every
    query becomes a labeled example → the eval set bootstraps itself, no hand-labeling.
  - Discipline (the one sharpening): the oracle MUST be an INDEPENDENT repo-grep at HEAD, NOT
    the store — else it is circular (testing the store against itself). Grep-vs-store tests
    whether the stored graph matches REALITY.
  - The sleeper win: the loop does not only grade the query agent — it continuously measures
    SENSOR FIDELITY (store vs repo), turning finding-0059/0061's staleness anxiety into a
    monitored number. A stale/missing edge = a measurable recall miss.
  - The spectrum: deterministic reference lookup → grep oracle (free, exact). Semantic
    retrieval → a genuine LLM-judge (subjective, needs the selfcheck discipline). "Starting
    off" = the deterministic end = the perfect bootstrap.
  - Golden-set FIREWALL: the auto-accumulated query→oracle pairs are a CANDIDATE eval set,
    never the frozen sacred golden set (CONSTITUTION §9 — human-only, deliberate, logged).
  - Dogfood: the performance record could itself become an OBSERVATION STREAM (a φ_ref, like
    φ_self for cost) — Ouroboros measuring its own reference accuracy over time.
  - Connects to docs/design-notes/capability-evaluation-harness.md.
  - LIVE DEMO (2026-07-13, run by hand over the existing 61k-edge store — the METHOD needs no
    agent to exist): target self-sensing.md. CODE-side recall ~5/7 — the store MISSED
    core/stores/observation_history.py + ops/lifecycle/launcher.py (a real store-vs-repo
    fidelity miss, caught by the loop). DOC→DOC recall 0/16 (the code-anchored blindness,
    finding-0059, now a number). The loop worked and caught real gaps on the FIRST query.

thread_A_refinement_pseudo_RAG:
  - Crystallization (owner): the core can now perform in PSEUDO-RAG mode — a query to a
    well-connected SET of nodes, NO TIME component. Retrieval by graph CONNECTIVITY (fibers /
    citations), not by embedding SIMILARITY (the librarian's semantic RAG), and not by
    TEMPORAL traversal (dispositional/supersession edges). It is the "R" without the "AG":
    deterministic structural retrieval that CAN augment generation (feed the librarian) but
    stands alone for the bookkeeping use — the shared retrieval primitive.
  - A THREE-MODE retrieval taxonomy over the core — three sentences in the same query algebra
    (Thread A), differing by edge class + whether time is included:
      1. STRUCTURAL pseudo-RAG — fiber connectivity, one stratum, NO time. Deterministic, no
         model. (the reference agent; the d-1 state slice)
      2. SEMANTIC RAG — embedding similarity over the mirror. Model-mediated. (the librarian)
      3. TEMPORAL / provenance — traverse dispositional edges ACROSS time. The d-dimension.
         (supersession / history queries)
  - "No time" is exactly Thread B's d-1 state slice: retrieving over the static connectivity
    (the gradient/state layer), not the temporal flow. Adding time promotes mode 1 → mode 3.

parked:
  - decision: the eval-loop + pseudo-RAG threads graduate to design ONLY in an owner-opened
    fable session (the fable-guard is unchanged from the first capsule)
    default: HOLD; this brainstorm + finding-0062 carry the threads
    re_entry: the owner opens the fable design session over this brainstorm

references:
  - docs/design-notes/capability-evaluation-harness.md # the eval-harness home for thread C
  - docs/design-notes/the-sacred-boundary.md
```

## 2026-07-13T05:26:27Z (captured — Thread B deepened: a formalization sketch, "what algebra is allowed")

> Opus first-sketch, marked PROVISIONAL. The rigorous development (fixing the inner
> products, PROVING the bicomplex commutation, the norm bounds) is the FABLE design note's
> job — the fable-guard stands. Cross-refs docs/design-notes/edge-dynamics.md +
> docs/brainstorms/edge-dynamics-and-continuum.md (the existing 1-form/Hodge home).

```capsule
topic: core-query-protocol (Thread B formalization)
date: 2026-07-13

objects_the_cochain_complex:
  - Nodes V, typed edges E = F (fibers/citations) ⊔ D (dispositional/supersession).
  - Cochains C^k with coboundary d: C^k → C^{k+1}, and the FUNDAMENTAL IDENTITY d∘d = 0
    (established): C⁰ (node scalars) —d₀→ C¹ (edge flows) —d₁→ C² (triangles), d₁d₀ = 0
    ("curl of a gradient is zero"). Inner products ⟨·,·⟩_k give adjoints δ = d*, and the
    Hodge Laplacian L_k = d δ + δ d.

hodge_decomposition_established:
  - C¹ = im d₀ ⊕ ker L₁ ⊕ im δ₂  =  GRADIENT ⊕ HARMONIC ⊕ CURL (orthogonal, unique).
  - Three orthogonal idempotents (a RESOLUTION OF THE IDENTITY):
      P_grad + P_harm + P_curl = I,   P_i² = P_i,   P_i P_j = 0 (i≠j).
  - ker L₁ ≅ H¹, dim ker L₁ = β₁ (the THREAD/hole count; edge-dynamics.md). The THREAD lens
    IS P_harm; the "d-1 collapse to a scalar" IS P_grad landing back on a C⁰ potential φ.

three_modes_are_three_DIFFERENT_algebras:  # this is the "what algebra is allowed" crux
  - Mode 1 STRUCTURAL pseudo-RAG: the fiber adjacency A_F (built on F ONLY, never D).
    Retrieval = neighborhoods/reachability = polynomials/closure in the PATH ALGEBRA of F:
    Boolean reachability ⋁_k A_F^k in the (∨,∧) semiring; weighted in tropical (min,+).
    No time. Deterministic, no model.
  - Mode 2 SEMANTIC RAG: a KERNEL/Gram operator K(s,·)=⟨emb(s),emb(·)⟩ over node embeddings —
    a metric algebra, not a path algebra. Model-mediated.
  - Mode 3 TEMPORAL: a TRANSFER operator T_n: K(t_n) → K(t_{n+1}) walking D across snapshots.
  - Claim to test: the three modes are three inequivalent algebraic structures over the SAME
    complex; the query protocol = "declare edge-class scope {F,D} + time-scope → the mode
    (hence the admissible algebra) falls out."

time_as_a_second_differential_the_bicomplex_question:  # the central OPEN problem
  - Two coboundaries: spatial d (citation geometry) and temporal δ_D (supersession).
  - IS (C^{p,q}, d, δ_D) a legitimate BICOMPLEX? i.e. does d δ_D = ± δ_D d, and does δ_D² = 0?
    If yes → a total complex with D_tot = d ± δ_D and a well-defined total cohomology; the
    "d-1 collapse" = the fixed-time row (δ_D = 0). If NO (supersession fails to commute or
    δ_D² ≠ 0) → space-time operations are NOT freely composable and the allowed algebra is
    constrained to the modes that avoid the obstruction. THIS is the load-bearing question.

invariants_become_algebraic_constraints_on_what_is_allowed:
  - ORIENTATION-INVARIANCE (edge-dynamics.md: every quantity orientation-invariant): edge
    quantities are defined up to a per-edge sign flip (a (Z/2)^E gauge group); the ALLOWED
    algebra is the ORIENTATION-INVARIANT (gauge-invariant) subalgebra — L₁, β₁, ⟨ω,ω⟩ live
    here; a bare signed edge value does not.
  - D-EXCLUSION (grounding walk must not traverse supersession): mode-1's operator is
    generated by A_F alone; A_D is a SEPARATE generator the structural algebra excludes.
    Mixing them is a different (mode-3) algebra by construction, not by choice.
  - γ^d CONTRACTION (Invariant 10, c ≤ γ^d·g): a cross-stratum operator is contractive by γ
    per depth ⇒ spectral radius < 1 ⇒ the strata tower's total operator is BOUNDED/convergent.
    "Allowed" cross-stratum compositions are exactly the ones that stay under the γ^d ceiling.

open_questions:
  - Which inner products ⟨·,·⟩_k? (unweighted vs strength-weighted — edge-dynamics parks the
    weighted variant; it changes δ, hence L₁, hence the harmonic representatives.)
  - Does δ_D² = 0 and d δ_D = ± δ_D d actually hold on this corpus? (the bicomplex test)
  - Is mode-2's kernel algebra reconcilable with mode-1's path algebra under one framework
    (e.g. both as operators on C⁰), or are they genuinely separate?
  - Persistence: strata depth d + budget γ^d·g gives a FILTERED complex ⇒ a persistence
    module (graded k[t]-module). Is the strength-filtration persistence edge-dynamics already
    reports the same filtration, or a second axis?

parked:
  - decision: the formalization graduates to a design note ONLY in an owner-opened fable
    session (fable-guard unchanged); the RIGOROUS math is fable work, this is a sketch to seed it.
    default: HOLD; brainstorm carries the sketch
    re_entry: the owner opens the fable design session

references:
  - docs/design-notes/edge-dynamics.md            # the 1-form lift, Hodge split, L₁ Fourier basis
  - docs/brainstorms/edge-dynamics-and-continuum.md # the existing edge-math brainstorm home
  - docs/design-notes/recursive-strata-amendment.md # γ^d, edge_budget, fibers vs dispositional
```

## 2026-07-13T05:29:30Z (captured — pushing Thread B: the bicomplex cracks, modes 1&2 unify, they meet)

> Still opus first-sketch, PROVISIONAL; fable-guard on graduation stands. But two real steps.

```capsule
topic: core-query-protocol (Thread B, pushed)
date: 2026-07-13

bicomplex_test_result_it_reduces_to_functoriality:
  - δ_D² = 0 is FREE. Supersession is time-directional ⇒ acyclic ⇒ a strict PARTIAL ORDER;
    its NERVE (order complex) is a bona fide simplicial complex, so its coboundary squares to
    zero by construction. (Forks/merges = a DAG poset, still fine; only a cycle would break
    it, and time forbids cycles.) So half the bicomplex condition holds automatically.
  - The REAL condition d·δ_D = ±δ_D·d ⟺ δ_D is a CHAIN MAP on the citation complex ⟺
    SUPERSESSION IS FUNCTORIAL OVER CITATIONS: "when a note is revised, do its citations carry
    forward coherently to the successor?" Reformulation: "is it a bicomplex?" = "is
    supersession a morphism of the citation geometry, not just a relation on vertices?"
  - The OBSTRUCTION [d, δ_D] = d δ_D − δ_D d is a 2-form-valued quantity measuring
    supersession's failure to preserve citations — CURVATURE-LIKE (the commutator of two
    differentials/connections is the standard curvature object; hedged, but it ties to the
    curvature instruments edge-dynamics.md already carries as diagnostic). Flat ⟺ bicomplex.
  - It is MEASURABLE, and the test NEEDS the doc→doc edges: for each supersession edge P→P',
    compare P's out-citations to P''s out-citations under the note-correspondence → a
    citation-coherence score; the mean is supersession's "flatness." Cannot even be computed
    until corpus→corpus (citation) edges exist — so finding-0059's reference-graph gap ALSO
    blocks the math test. Closure: the reference extractor is a prerequisite for Thread B.

unifying_modes_1_and_2_the_kernel_cone:
  - Mode 1 bifurcates: (1a) HARD reachability = Boolean/tropical PATH algebra over A_F (not a
    kernel); (1b) SOFT diffusion = the graph HEAT KERNEL e^{-t L₀^F} or Green's function
    (L₀^F)^+ — a PSD kernel on nodes.
  - Mode 2 = the embedding GRAM matrix K_sem — also a PSD kernel on nodes.
  - So (1b) and (2) are TWO POINTS IN THE SAME CONE: the cone of PSD kernels on V, an algebra
    closed under + , convex mixing, and Hadamard ⊙ (Schur product theorem). Retrieval =
    "choose a kernel K, query K(s,·)." Hybrid = K_struct ⊕ K_sem (union) or K_struct ⊙ K_sem
    (= "cited AND semantically near"). This is exactly how graph-RAG hybrids already work.
  - So modes 1(soft) & 2 UNIFY in the kernel cone; mode-1(hard) stays the discrete semiring
    twin. Mode 3 does NOT fit the static-kernel picture — it is the TEMPORAL TRANSPORT that
    acts BETWEEN kernels at different times.

the_synthesis_2_plus_1:
  - Static layer: two retrieval kernels in one cone (structural-diffusion + semantic), mixed
    by ⊕ / ⊙. Temporal layer: one transport operator (mode 3) moving kernels across snapshots.
  - The bicomplex/functoriality question IS "does the temporal transport move the STRUCTURAL
    kernel coherently?" — i.e. curvature couples the two layers. One picture: a kernel cone
    (space) + a connection (time) whose curvature = supersession's non-functoriality.

open_questions_sharpened:
  - Measure supersession flatness on the real corpus (needs doc→doc edges) — is [d,δ_D] ≈ 0?
  - Does mode-1(hard) reachability have a soft limit that IS the diffusion kernel (semiring →
    kernel as a deformation / zeta-function link)? If so modes 1a,1b,2 are one family.
  - Is the temporal transport UNITARY / measure-preserving, or lossy (revision destroys
    structure)? Determines whether mode 3 is reversible.

parked:
  - decision: rigorous version (proving δ_D chain-map conditions, choosing inner products,
    the curvature formalism) graduates ONLY in an owner-opened fable session (guard unchanged).
    default: HOLD; brainstorm carries the pushed sketch
    re_entry: owner opens the fable design session
```

## 2026-07-13T06:06:41Z (captured — FABLE agent deliverable: the rigorous math, tier-verified)

> Produced by a delegated **fable** agent (`claude-fable-5`, verified: 5 tool-uses = the 5
> files read, one uninterrupted pass, stopped on completion not budget). Orchestrator-captured
> (single-writer). Claims carry the agent's labels [ESTABLISHED]/[DERIVED]/[CONJECTURE]/
> [ANALOGY]; literature cited from memory (flag for a 5-min check before a design note cites).
> The fable-guard on graduation stands — this is theorem-grade brainstorm material, not a note.

```capsule
topic: core-query-protocol (Thread B — fable rigorous pass)
date: 2026-07-13

system_grounding_caveat:
  - [DERIVED] TWO candidate "structural graphs" exist: (i) the similarity backbone A =
    cosine_adjacency(emb) that hodge.py consumes — DEFINITIONALLY derived from the semantic
    kernel (thresholded Gram); (ii) the citation fiber graph from reference_edges.sqlite —
    embedding-independent but code-anchored (no doc→doc; finding-0059). Every Q2 claim is
    graph-relative. On (i) the semantic kernel is near-on-family by construction; the
    interesting instance of the fork is (ii) — the one not yet computable on the live corpus.

Q2_the_deformation_VERDICT_derived:
  - The family is naturally TWO-dial, not one: inverse-temp β (soft↔hard on edge COSTS
    c_e = −log w_e) and fugacity z (walk-LENGTH damping). Walk/Green family:
    K(z,β) = (I − z A^{∘β})^{-1} = Σ_walks z^{|γ|} e^{−β ℓ(γ)}; converges iff z·ρ(A^{∘β})<1
    — the SAME contraction as Invariant-10's γ-ceiling (spectral radius <1 ⇒ closure exists).
  - [ESTABLISHED] The interpolating one-parameter families ARE standard: randomized
    shortest paths / free-energy distances (Saerens/Kivimäki/Françoisse), Chebotarev walk &
    logarithmic-forest distances, and p-resistances (Alamgir–von Luxburg). All interpolate
    shortest-path (β→∞) ↔ commute-time/resistance (β→0) = mode 1a ↔ mode 1b EXACTLY.
  - [DERIVED] Prop 1 (tropical limit with RATE): for β ≥ (log 2Δ)/c_min,
    d_c − β^{-1}[log4 + (k*+1)logΔ] ≤ d_β ≤ d_c, k*=⌈d_c/c_min⌉ — O(1/β) convergence,
    explicit combinatorial constant, any finite graph. Framing = Maslov dequantization: the
    S_β semirings are all ISOMORPHIC to (+,×) for finite β, degenerate to tropical (min,+)
    only at β=∞. Mode 1a is the SAME Kleene closure A* as 1b, at the degenerate boundary.
  - [DERIVED] Heat kernel = finite-β path partition function: e^{−tL} = e^{−Λt}Σ (Λt)^k/k! P^k
    (uniformization P = I − L/Λ ≥ 0). Heat kernel, Green's function, resolvent = different
    completely-monotone filters f(L) on one generator; all PSD; all stochastic-compatible.
    Caveat [DERIVED]: β-dequantization of WEIGHTS recovers weighted shortest path; the t→0
    heat clock tropicalizes to the UNWEIGHTED hop metric (weights subleading). Directedness:
    walk/tropical fine for directed A_F; PSD story needs a symmetrization CHOICE (pin it).

Q2_the_mode2_fork_SETTLED_derived:  # the main new result
  - Nested loci: CONE {K⪰0} ⊃ 𝔉(L)={f(L):f≥0 on spec L} ⊃ CURVE {K(β)}.
  - Prop 2–3: K_sem = f(L) IFF the embedding is (up to ambient rotation) the SPECTRAL
    embedding of L with filter √f, i.e. emb(v) ≅ (√f(λ_k)·u_k(v))_k. Diffusion maps = the
    case f=e^{−tλ} [Coifman–Lafon]; Laplacian eigenmaps = low-pass f [Belkin–Niyogi]. On the
    CURVE is strictly stronger: the empirical filter must be the deformation filter at one β.
  - Prop 4 (genericity): learned embeddings have no mechanism forcing [K_sem,L]=0; commutant
    ∩ cone has codim N(N−1)/2 ⇒ off-manifold GENERICALLY. HONEST ANSWER: cone yes, curve no —
    unless the embedding is by construction spectral.
  - THE INVERSION [ESTABLISHED, Mercer]: every PSD kernel is SOME embedding's Gram ⇒ mode 2
    is the GENERIC POINT of the cone, NOT a special subclass. Correct taxonomy: the cone = all
    possible semantic modes; mode 1b = its thin graph-spectral locus 𝔉(L); mode 1a = the
    tropical boundary of the curve inside 𝔉(L). Vacuity trap named: "K_sem = e^{−H} always"
    is empty; the content is LOCALITY of H = −log K_sem (Metzler/Laplacian-like, support ⊆ F).
  - [DERIVED] Canonical projection of an off-curve K_sem: (1) pinch onto the commutant
    K̄ = Σ_λ P_λ K_sem P_λ (Frobenius projection, PSD-preserving); (2) blockwise trace-average
    f̂(λ)=tr(P_λ K_sem P_λ)/m_λ ⇒ f̂(L) is the Frobenius-nearest spectral fn. Yields an
    ALIGNMENT INSTRUMENT: energy fraction ‖f̂(L)‖²/‖K_sem‖² (how graph-explainable) + shape of
    f̂(λ) (heat-like? fit β̂). Deterministic ⇒ a Thread-C measurable. The residual IS the
    instrument, not a failure.
  - [DERIVED/ESTABLISHED, Schoenberg 1938] PHASE TRANSITION: finite β ⇒ honest PSD kernel;
    β=∞ ⇒ a METRIC that generically is NOT of negative type ⇒ e^{−s·d} not PSD ⇒ does NOT
    re-enter the cone. Trees (ℓ₁, negative type) are the exception. [CONJECTURE] on sparse
    citation graphs kernel-representability fails at finite β* < ∞ — settled by sweeping β and
    watching λ_min(e^{−d_β}). Cone ops (+, convex mix, Schur ⊙) preserve PSD [Schur thm];
    K_struct ⊙ K_sem = "cited AND near" stays a kernel; nothing survives at β=∞.

invariants_as_the_allowed_algebra_derived:
  - [DERIVED, form-level] Invariant 10 is already tropical: γ^d = e^{−d·log(1/γ)} is a
    Boltzmann factor in depth (per-stratum cost log(1/γ)); cross-stratum fiber = cost log(1/γ),
    grounding = 0, DISPOSITIONAL = +∞ (D-exclusion IS an infinite-cost assignment — makes
    "grounding walk never traverses supersession" a property of the METRIC). Caveat: d is a
    mint-time stamp (I4), g a support fraction — identification of FORM, licensing a design
    OPTION (a soft grounding ratio g_β with the current bookkeeping as its β→∞ limit), not a
    theorem. Orientation gauge acts trivially on C⁰ ⇒ static family gauge-invariant free; the
    e^{−tL₁} lift is gauge-COVARIANT (invariants = quadratic forms / entry magnitudes).

bicomplex_functoriality_sharpened_derived:
  - [ESTABLISHED w/ hypotheses] δ_D²=0: op-seq strict order ⇒ acyclic ⇒ poset ⇒ nerve (order
    complex) ⇒ coboundary²=0. Hidden assumptions NAMED: (1) transitive closure is a definition
    being made; (2) strictness from op-seq not wall-clock; (3) RENAME-STABLE identity is a data
    PREREQUISITE (supersession-lifecycle §7: doc_id=source_path forks lineage on rename ⇒
    spurious components); (4) with COEFFICIENTS in citation complexes, δ_D²=0 needs the
    COMPOSITION axiom F2 (σ_{P→P″} = σ_{P′→P″}∘σ_{P→P′}) — definitional for version lineage,
    a failable data-integrity invariant for claim-level supersede ops.
  - [DERIVED] Bicomplex ⟺ F1 ∧ F2. F1 = each transport σ is SIMPLICIAL (citations incident to
    a revised note have counterparts at the successor; untouched persist) — "the one killer is
    a SEVERED citation"; merges/additions are fine. F2 = composition coherence. Simplicial maps
    induce chain maps [ESTABLISHED] ⇒ F1 ⟺ d δ_D = ±δ_D d (the ± is Koszul bookkeeping).
  - [DERIVED] LOCALIZED COMMUTATOR: ([d,τ]φ)(u,v) = (φ(σv)−φ(σu))·𝟙[{σu,σv}∉X_{n+1}] —
    supported EXACTLY on severed citations, weighted by the potential drop. So ‖[d,τ]‖ IS the
    citation-carry-forward failure count (not a proxy). Measurable; NEEDS doc→doc edges.
  - CURVATURE [ESTABLISHED frame; DERIVED identification]: the rigorous home is a diagram of
    chain complexes over the time poset (functor T→Ch if strict; homotopy-coherent/twisted
    complex if not; total = Bousfield–Kan homotopy colimit). 𝔸=d+τ on the total module has
    𝔸² = curvature of a QUILLEN SUPERCONNECTION (Block dg-modules; Bondal–Kapranov twisted
    complexes). Flat ⟺ bicomplex. NON-FLATNESS IS THE FIRST OBSTRUCTION, NOT A DEAD END: if
    [d,τ] is exact in the Hom-complex it is REPAIRABLE by a homotopy h (corrected diff d+τ+h);
    the true invariant is the class [[d,τ]] ∈ H¹(Hom(C(X_n),C(X_{n+1}))). Two distinct curvature
    layers: (i) superconnection [d,τ] (exists on a linear time chain); (ii) DIAMOND HOLONOMY on
    fork/merge diamonds (only when D has diamonds). HONEST DEMOTION [ANALOGY]: the edge-dynamics
    Forman–Ricci/bridge curvature is of the STATIC fiber geometry; [d,τ] is of the TEMPORAL
    connection — same word, different tensors; a design note must not merge the sections.
  - [DERIVED] TWO-TIER: even perfect F1∧F2 buys TOPOLOGICAL coherence (chain maps ⇒ homology/
    threads/β₁ transport coherently — the THREAD lens's objects have a well-defined temporal
    life) but NOT METRIC coherence: σ*d=dσ* does NOT give σ*δ=δσ* (adjoints flip variance;
    need σ weight-compatible/isometric). Kernel-flatness ⊋ bicomplex-flatness. This is exactly
    where parked PD-b (weighted vs combinatorial inner products) starts to matter.

transport_true_category_derived:
  - NOT unitary, three measurable reasons: creation (σ never surjective), destruction (partial
    σ kills vectors), merges (‖σ_*‖=√max-fiber>1; repair by conditional-expectation contraction
    or the pullback σ*). σ_* is a PARTIAL ISOMETRY iff supersession is MERGE-FREE ("isometric
    yet irreversible": surviving structure survives undistorted, but revision genuinely
    creates/destroys).
  - γ-TIE [DERIVED, contingent on supersession-lifecycle §4.5]: depth rises monotonically along
    a revision thread ⇒ on confidence-weighted cochains the transport is a STRICT CONTRACTION
    rate ≤ γ; the same γ bounds strata tower AND temporal dynamics. If §4.5 = depth re-anchor on
    promotion ⇒ "transfer operator strictly contractive EXCEPT at owner verdicts; the OWNER is
    the only energy source in the dynamics" (constitution-aligned). If §4.5 the other way ⇒
    unconditionally contractive, deep insight permanently damped. The math makes the tension
    quantitative.
  - LEDGER = DILATION [DERIVED on op-orthonormality convention]: append-only op-seq store with
    distinct-ops-orthonormal ⇒ H_n↪H_{n+1} is an ISOMETRY; active view = subspace; active
    transport = compression of an isometry = contraction; Sz.-Nagy [ESTABLISHED: every
    contraction is the compression of a unitary] ⇒ the lossy dynamics ALWAYS dilates — and here
    the dilation is CONCRETE: the append-only ledger. "Revision destroys structure in the active
    view; the ledger is the isometric dilation in which nothing was ever destroyed." Two mode-3
    operators must NOT be conflated: ledger-compression (kills superseded) vs correspondence σ_*
    (follows D to successors) — different categories; the protocol must type which a query uses.

unifying_picture_four_layers_derived:
  - Per-snapshot: retrieval cone 𝒦_t with cone ops + the structural curve {K_t(β)} (β=∞
    adjoined as a non-kernel metric boundary) + K_sem as a distinguished (generically off-curve)
    point with its projection+alignment. Across snapshots: supersession = a CONNECTION on the
    bundle of cones, acting by congruence K ↦ σ_* K σ_*ᵀ (PSD-preserving). "Curvature =
    non-functoriality" HOLDS but stratifies into FOUR layers: (a) F2 composition incoherence
    (data defect); (b) superconnection [d,τ] (F1/severed citations); (c) diamond holonomy;
    (d) metric defect (σ not weight-compatible — kernels transport only approximately even when
    a–c vanish). Frame does not break; it is four layers not one.

untestable_today_register:  # per the honesty mandate
  - BLOCKED on doc→doc citation edges (finding-0059/0062; reference_edges.sqlite is code-anchored):
    the flatness/coherence ‖[d,τ]‖, the F2 violation count, diamond holonomy, the citation-graph
    alignment of K_sem, the negative-type β* sweep on the CITATION metric. The math DOUBLES the
    warrant for the doc→doc extractor.
  - COMPUTABLE TODAY: the entire §1 β-family on the SIMILARITY backbone (where hodge.py lives);
    the ledger/contraction statements on the version store.

shortlist_for_the_fable_design_session:
  - 1. Pin the normalization triple (cost dictionary c=−log w vs 1−sim; directedness treatment;
    the (β,z) coupling — recommend RSP as the canonical curve). Nothing is theorem-grade before.
  - 2. Adopt F1/F2 as named store invariants with two deterministic violation counters; make the
    doc→doc extractor their explicit prerequisite.
  - 3. Rule on the two mode-3 operators (ledger-compression vs correspondence) in the protocol
    type system — a temporal query must declare which.
  - 4. Decide supersession-lifecycle §4.5 (promotion re-anchoring) with the dynamical dichotomy
    in hand (contractive-except-at-owner-verdicts vs unconditionally contractive).
  - 5. License the alignment instrument (pinch + f̂(λ) + energy fraction) as a Thread-C measurable.
  - 6. Post-extractor empirical sweeps: negative-type β* on the citation metric; ‖[d,τ]‖ mass on
    real supersession events; whether the obstruction class is exact (homotopy-repairable).
  - 7. Weighted inner products (PD-b) now have a second customer: the metric tier of §2.4.

parked:
  - decision: graduation still fable-guarded (unchanged); this pass is the SEED the fable design
    session formalizes — likely TWO notes (architecture: core-query protocol; math: this + Lane B).
    default: HOLD
    re_entry: owner opens the fable design session over this brainstorm
```
