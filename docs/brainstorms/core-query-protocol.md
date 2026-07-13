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
