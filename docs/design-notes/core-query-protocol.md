---
type: design-note
id: dn-core-query-protocol
status: draft # draft → ratified → superseded.  draft→ratified is an OWNER-ONLY hand edit.
implementation: design-only # nothing built; the reference substrate (reference_edges, 61k edges) exists but is code-anchored + agent-unreachable
created: 2026-07-13
updated: 2026-07-13
links:
  - docs/brainstorms/core-query-protocol.md # the graduate-ready arc (warrant): four threads + two opus sketches + the fable rigorous pass
  - docs/design-notes/edge-dynamics.md # the 1-form lift, Hodge/Helmholtz split, L₁ Fourier basis, THREAD lens, Lane A/B seam
  - docs/design-notes/recursive-strata-amendment.md # γ^d damping, typed edge_budget, fibers vs dispositional edges
  - docs/design-notes/supersession-lifecycle.md # what a dispositional (supersession) edge IS; §4.5 depth re-anchoring; §7 rename identity
  - docs/design-notes/the-sacred-boundary.md # the plane-crossing ruling §2.4 makes concrete
  - docs/design-notes/capability-evaluation-harness.md # the eval-harness home for the self-grading loop
  - docs/design-notes/observed-data-and-the-assistant-tier.md # the mirror firewall the scope model inherits
  - docs/findings/finding-0059.md # doc→doc blindness (the prerequisite this note surfaces)
  - docs/findings/finding-0061.md # the stale-baseline class the reference graph would guard
  - docs/findings/finding-0062.md # the direction finding this note graduates
supersedes: null
superseded_by: null
warrant: docs/brainstorms/core-query-protocol.md
---

# The core-query protocol — retrieval as a scoped algebra over the strata

> Composed by the orchestrator (**Opus/xhigh**, 2026-07-13) from the graduate-ready
> `core-query-protocol` brainstorm; filed as `draft`. The brainstorm→design step is
> normally **fable-guarded** (owner rule); the owner relaxed the guard for THIS drafting
> because the tier-justifying work — the rigorous math — was already paid at fable
> (`claude-fable-5`, verified) and is captured in the brainstorm's 2026-07-13 capsules.
> This note therefore *states* the derived/established results and makes the design
> decisions they inform; it does not re-derive them. The remaining fable work is the
> formalization **shortlist** (§ Parked), not the whole note.
>
> **⚠ This draft should be fable-vetted before ratification.** It was composed at opus
> under a relaxed guard; a fable pass should review the design decisions (especially the
> §2.4 boundary ruling and the §2.2 algebra's fidelity to the captured derivations) and
> settle the Parked normalization triple, *before* the owner ratifies. Opus-drafted,
> fable-checked, owner-ratified.
>
> Ratification is a hand edit by the owner — no command performs it, `gate-guard` denies
> any agent attempt, and `/graduate` refuses this note until `status: ratified`.

## 1. Purpose and scope

### 1.1 What this note decides

There is no single, typed way to *ask the core a question*. Every agent — the orchestrator,
the Ambassador, the sensors, and any future reader — reaches into the core through an
ad-hoc, bespoke interface, and the existing typed windows (`MirrorView`, `ObservedView`,
`OpsView`, `EffectView`) are partial, uncoordinated sentences of a language nobody has
written down. This note writes it down. It decides:

1. **The frame (§2.1):** every agent is a **capability-scoped client of the core**, not a
   distinct kind of thing. A client's identity is its *scope* — which strata it may touch,
   under which of `{read | read+propose | write}`. The orchestrator, the Ambassador, and a
   sensor differ only in scope.
2. **The algebra (§2.2):** the core's retrieval modes — **structural**, **semantic**,
   **temporal** — are three sentences in *one* query algebra, distinguished by *edge-class
   scope* `{F, D}` and *time-scope*. The fable pass established that structural and
   semantic retrieval are two regions of a single object (the PSD-kernel cone with a
   deformation curve through it); temporal retrieval is the transport between snapshots.
3. **The archetype (§2.3):** the simplest well-typed client — a **deterministic,
   single-stratum, no-model reference agent** (the read-side dual of a sensor) — as the
   first thing to build and the proof the frame is right.
4. **The boundary ruling (§2.4):** whether, and how, the *build-time* plane may query the
   *live daemon's* reference stratum. Ruling: **as a capability scope, not a special case.**
5. **The self-grading loop (§2.6):** the reference agent is testable from day one against a
   deterministic oracle, which also *continuously measures sensor fidelity*.

### 1.2 What is out of scope

Implementation (this note is `design-only`); the rigorous *proofs* (they live in the
brainstorm's fable capsule — this note cites results, it does not prove them); the full
formalization of the algebra (the normalization triple and friends — Parked, fable work);
and any build (that follows ratification → `/graduate`). This note also does **not** touch
the Ambassador's or Librarian's semantic-RAG machinery — those are heavy clients of the
same protocol, not redefined here.

### 1.3 Provenance, and what fable must finalize (be honest)

The reason these decisions can be made at opus *at all* is the **verified fable pass**
(`claude-fable-5`, uninterrupted; captured in the brainstorm's 2026-07-13 capsule). Without
it, §2.2 would be conjecture and this note could not responsibly decide anything. So the
attribution is load-bearing: **the fable worker is the warrant for the calls made here.** In
that spirit, the honest split of this note — what is settled vs what a fable pass must
finalize before the owner ratifies:

**Fable-grounded (decide on these):** the §2.2 algebra results (the β-deformation with
modes 1a/1b as endpoints; the kernel-cone unification of 1b & 2; the Mercer inversion — mode
2 as the cone's generic point; the Schoenberg phase transition) and the §2.5 temporal results
(the bicomplex ⟺ F1∧F2 reduction; the localized `[d,τ]` obstruction; the superconnection
curvature; the ledger-as-dilation; the γ-contraction). These carry the fable pass's own
`[ESTABLISHED]`/`[DERIVED]` labels; the *decisions* resting on them (§2.2's "three modes are
one algebra"; §2.5's design consequences) are sound.

**Opus-provisional — a fable pass MUST finalize before ratification:**

1. **§2.4 the sacred-boundary ruling** — an opus *design judgment* touching an invariant
   boundary. It is the single highest-stakes call in the note and wants fable + owner scrutiny,
   not opus's say-so.
2. **§2.1 the exact scope grammar** — the specific tuple/primitives are opus synthesis; the
   formal type system (what a scope *is*, how it composes, how it enforces the boundary) is
   fable-grade design.
3. **§2.3/§2.5 surface shapes** — reference agent as `ReferenceView` (library) vs addressable
   service; the naming/typing of the two mode-3 operators. Proposed at opus, not settled.
4. **The Parked normalization triple** (cost dictionary, directedness, `(β,z)` coupling) —
   the fable pass was explicit: *nothing in §2.2 is theorem-grade until these are pinned.*
5. **The Parked `§4.5` dichotomy** (promotion re-anchoring) and **one-note-vs-two**.
6. **Literature verification** — the fable pass flagged its citations (RSP, Chebotarev,
   p-resistances, Schoenberg, Sz.-Nagy, Maslov) as *from memory*; a 5-minute check is owed
   before this note or a book chapter cites them as settled.
7. **The balance-isolation reconciliation.** `core/stores/reference_edges.py` is
   **deliberately balance-isolated** — `core/complex/**` never imports it, `build_complex` has
   no parameter for it, and `tests/integration/test_reference_edge_isolation.py` proves
   bit-identically that no instrument result changes when reference edges are added/removed.
   So the reference store's citation edges are **NOT** the "fibers" `hodge.py` builds its
   complex from (that is the *similarity backbone* `A = cosine_adjacency(emb)`). This is
   exactly the fable pass's "two structural graphs" caveat: the retrieval/algebra §2.2 uses the
   *citation* fiber graph; the built Hodge object uses the *similarity* graph. Using citation
   edges for the §2.5 math (the bicomplex test) means constructing a **separate** citation
   complex — which does not violate the isolation invariant (it never feeds `A_signed`/the
   balance math) but is a distinct, deliberate construction the fable session must specify.

Everything in this list is why the note is `draft`, not why it is wrong — it is a faithful map
of the opus/fable seam so the fable session knows exactly where to spend.

## 2. Principles / decision

### 2.1 Agents are capability-scoped clients of one protocol

**Decision.** Model every core-reader as a client whose type is a **capability scope**

```
scope = ( strata it may touch , edge-classes {F, D} , time-scope , {read | read+propose | write} )
```

The differences we treat as "kinds of agent" are differences of scope:

| Client | Strata | Edges | Time | Authority | Model? |
|---|---|---|---|---|---|
| Reference agent (§2.3) | one | `F` | none | read | **no** |
| Librarian / Ambassador | mirror + curated + ops | — | — | read + propose | yes |
| Sensor (write-side dual) | one | — | stamps | **write** (projects) | no |
| Orchestrator | build-plane artifacts | — | — | read + propose + write (scoped) | yes |

The existing Views are the **partial seed** of this language — each is already a typed,
capability-scoped window onto one plane. This note's frame unifies them: a View is a
*declared scope*; a query is a *sentence within it*. The invariant that makes the frame
safe is that **scope is the access-control primitive** — the sacred boundary (§2.4), the
mirror firewall, and `read+propose≠write` are all expressed as scope, never as ad-hoc
special cases in each client.

### 2.2 The three retrieval modes are one algebra

The core's graph carries **typed edges**: **fibers** `F` (citations/warrants; budgeted
lateral or cross-stratum) and **dispositional** `D` (supersession; time-directional). Over
the cochain complex `C⁰ —d₀→ C¹ —d₁→ C²` (the 1-form lift of `edge-dynamics.md`), retrieval
is a query against these edges, and the mode is fixed by *which edge-class you scope to* and
*whether you keep the time axis*:

- **Mode 1 — structural** (fibers, one stratum, **no time**). Retrieval by *connectivity*.
  It **bifurcates**: (1a) hard reachability in the Boolean/tropical `(min,+)` **path
  semiring**; (1b) soft diffusion — the graph **heat kernel** `e^{-tL_F}` / Green's function
  `(L_F)⁺` — a PSD kernel. Deterministic, no model.
- **Mode 2 — semantic** (the embedding Gram kernel `K_sem`). Retrieval by *similarity*.
  Model-mediated (this is the Librarian's retrieval).
- **Mode 3 — temporal** (traverse `D` across snapshots). The transport *between* the static
  pictures. This is where provenance/history queries live.

**The unification (fable-established; proofs in the brainstorm capsule, cite before a book
uses them):**

- **Modes 1a and 1b are the two ends of one deformation.** A single free-energy /
  randomized-shortest-path family `K(β)` (with an inverse-temperature `β` on edge costs
  `c = −log w`) has **1a = β→∞** (tropical shortest-path/Viterbi) and **1b = β→0**
  (diffusion/resistance) as its endpoints, with `O(1/β)` convergence. The endpoint
  degeneration is **Maslov dequantization** of the path semiring — 1a is the *same* Kleene
  closure as 1b, at the degenerate boundary. `[ESTABLISHED: RSP/free-energy distances;
  Chebotarev; p-resistances. DERIVED: the O(1/β) bound.]`
- **Modes 1b and 2 are two points in the PSD-kernel cone**, whose algebra is `+`, convex
  mixing, and Hadamard `⊙` (Schur). Hybrid retrieval is *an operation in the cone*:
  `K_struct ⊙ K_sem` = "cited **and** semantically near." `[ESTABLISHED: Schur product.]`
- **The correct taxonomy (the fable inversion):** since *every* PSD kernel is some
  embedding's Gram (Mercer), **mode 2 is the generic point of the cone**; **mode 1b is its
  thin graph-spectral locus** `𝔉(L) = {f(L)}`; **mode 1a is the tropical boundary** of a
  curve inside that locus. A learned embedding is **on the cone always, on the structural
  curve generically never** — unless it is (an ambient rotation of) a *spectral* embedding
  (diffusion maps / Laplacian eigenmaps). `[DERIVED, Props 2–4.]`
- **A phase transition at `β=∞`:** finite `β` gives an honest kernel; the `β=∞` limit is a
  *metric* that is generically **not of negative type**, so it does **not** re-enter the
  cone (Schoenberg). Inner-product retrieval degenerates into idempotent, winner-take-all
  metric retrieval exactly at the tropical boundary. `[ESTABLISHED: Schoenberg 1938.]`

**Decision.** The query protocol's surface is *"declare edge-class scope `{F, D}` and
time-scope; the mode — hence the admissible algebra — follows."* The system's invariants are
**algebraic constraints on that algebra, not side rules**: `D`-exclusion (the grounding walk
never traverses supersession) is an *infinite-cost assignment* on `D`; the γ^d strata ceiling
is a *Boltzmann factor in depth* (`γ^d = e^{-d·log(1/γ)}`); orientation gauge-invariance makes
the static family gauge-invariant for free. Retrieval and the safety invariants are one object
read under different scopes.

### 2.3 The reference agent — the archetype, and the first build

**Decision.** Build, first, the **deterministic single-stratum reference agent**: given a
target, return its connected set over fibers `F`, at fixed time, with `ref_type` and
`source_line`. It is the *read-side dual of a sensor* — as deterministic and attestable as a
sensor's projection, but serving queries instead of writing them. Because it touches **one
stratum, lateral edges only, no time**, it needs **none** of the Ambassador's machinery: no
model, no cross-stratum budget, no firewall composition, no hallucination surface. It is the
simplest well-typed sentence of §2.1 — `read(one stratum, F, no time)` — and shipping it is
the proof the whole frame holds.

This is **structural pseudo-RAG**: the "R" of RAG (retrieval by connectivity) without the
"AG," a primitive that can *feed* generation (hand its set to the Librarian for
citation-aware retrieval) but stands alone for the agent-bookkeeping need that motivated this
whole line (findings 0059/0061: agents re-grepping for "who cites this" that they should be
able to *look up*).

### 2.4 The sacred-boundary ruling

The reference stratum (`data/reference_edges.sqlite`, ~61k edges) lives in the sealed core;
"make it useful for *us*" means the **build-time plane** querying the **live daemon's**
stratum — a plane crossing (`the-sacred-boundary.md`).

**Ruling (proposed; owner ratifies).** Expose it **as a capability scope, not a special
case.** The reference graph is **corpus-structural** (who-cites-what — the *shape* of the
authored corpus), not **observed exhaust** (not the mirror's contents, not private
interaction data). A read scoped to *structural edges only* therefore does not cross the
firewall the mirror protects. Concretely, the boundary is drawn *inside* the scope grammar:

- **Permitted scope:** `read( reference stratum , F , structural metadata: ref_type, source_line, path )`.
- **Denied by the same scope grammar:** any read of node *payloads* (the mirror), any
  observed-exhaust stratum, any `D`-traversal that would leak revision *content* rather than
  structure. `read+propose`/`write` never available to a build-time client.

This keeps the boundary a *property of the type system* (§2.1) rather than a rule each caller
must remember — which is the whole point of the protocol.

### 2.5 The temporal layer and the invariants (stated; formalization Parked)

Supersession is a **connection** on the bundle of retrieval cones, acting on kernels by
congruence `K ↦ σ_* K σ_*ᵀ` (PSD-preserving). The fable pass established:

- **The temporal complex is well-founded.** Supersession is acyclic (op-seq is a strict
  order) ⇒ a poset ⇒ its nerve gives `δ_D² = 0`. `[ESTABLISHED, with hypotheses: transitive
  closure is taken; rename-stable identity is a data prerequisite — §7 of supersession-lifecycle.]`
- **"Is space×time a bicomplex?" = "is supersession functorial over citations?"** It holds
  **iff** (F1) each transport is simplicial — *a revised note's citations carry forward; the
  one killer is a severed citation* — **and** (F2) the transports compose. The obstruction
  `[d, τ]` is supported **exactly on severed citations**, weighted by the potential drop — so
  the "citation-coherence" score *is* `‖[d,τ]‖`. Its rigorous home is a **Quillen
  superconnection** whose curvature is `[d,τ]`; **non-flatness is the first obstruction, not a
  dead end** (homotopy-repairable if the class is exact). `[DERIVED.]`
- **Topological ⊊ metric coherence.** Even perfect functoriality transports *homology* (the
  THREAD lens's objects have a well-defined temporal life) but not *kernels* — kernel-flatness
  additionally needs `σ` weight-compatible (isometric). `[DERIVED.]`
- **The transport is not unitary; the ledger is its dilation.** Revision creates, destroys,
  and merges, so the active-view transport is a contraction — and by Sz.-Nagy the append-only
  **ledger is its isometric dilation**: *"revision destroys structure in the active view; the
  ledger is the space in which nothing was ever destroyed."* Under confidence weighting the
  transport is a **strict γ-contraction except at owner promotions** — *the owner is the only
  energy source in the dynamics.* `[DERIVED, contingent on supersession-lifecycle §4.5 —
  Parked.]`

**Design consequence:** the protocol's type system must **name two distinct mode-3 operators**
— *ledger-compression* (kills superseded content) vs *correspondence transport* `σ_*` (follows
`D` to successors) — and a temporal query must declare which.

### 2.6 The self-grading loop (Thread C)

**Decision.** The reference agent ships with a **deterministic self-grading harness**
(`capability-evaluation-harness.md`): query → check against an **independent repo-grep oracle
at HEAD** → score → record. Because reference lookup is deterministic, the judge has *free,
correct* ground truth — a differential test against an oracle, **stronger** than an LLM-judge —
and every query self-labels, so the eval set bootstraps itself.

Three disciplines are load-bearing:

1. **The oracle is repo-grep, not the store** — else it is circular. Grep-vs-store tests
   whether the stored graph matches *reality*, which turns finding-0059/0061's staleness
   anxiety into a **monitored sensor-fidelity number**. *(A hand-run demo over the live 61k-edge
   store already caught it: code-side recall ~5/7 — two stale files; doc→doc recall 0/16.)*
2. **Golden-set firewall.** Auto-accumulated query→oracle pairs are a *candidate* eval set,
   **never** the frozen sacred golden set (Constitution §9 — human-only, deliberate, logged).
3. The record may itself become an **observation stream** (a `φ_ref`, dual to `φ_self`) —
   Ouroboros measuring its own reference accuracy over time.

The fable pass added a fourth measurable: the **alignment instrument** — project `K_sem` onto
the structural spectral manifold and report the energy fraction (how graph-explainable the
embedding is) and its spectral filter shape. Deterministic, gauge-invariant, Thread-C-gradable.

## 3. Consequences — what this note licenses (on ratification)

1. **The doc→doc reference extractor** (a small build plan) — parse `design_ref:`, `links:`,
   `[[name]]`, and `path:line` citations across `docs/**` into `corpus_to_corpus` edges. It is
   **cross-warranted**: finding-0059/0061 (agent bookkeeping) *and* the math test — the fable
   pass showed every empirical claim in §2.5 (flatness, F2 violations, diamond holonomy, the
   citation-side alignment) is **blocked on these edges**. It is the concrete unblocker for both
   halves and the recommended *first* graduation from this note.
2. **The reference query surface** (§2.3) — a `ReferenceView` and/or an addressable reference
   agent; and the **capability-scope type system** (§2.1) it is the first client of.
3. **The boundary scope grammar** (§2.4) — the machinery that expresses `the-sacred-boundary`
   as a scope rather than a special case.
4. **The self-grading harness + the alignment instrument** (§2.6) as Thread-C measurables.
5. **A math successor note (or a section of `edge-dynamics` Lane B)** carrying the formalized
   algebra — the fable session's output (Parked shortlist below). This note deliberately keeps
   the math as *stated results*; the successor makes them theorem-grade.

This note builds nothing itself. Its first plan is the doc→doc extractor; the reference agent
and the protocol type system follow.

## Parked decisions

| Decision | Default recorded | Re-entry condition |
|---|---|---|
| The normalization triple (cost dictionary `c=−log w` vs `1−sim`; directedness treatment; the `(β,z)` coupling) | recommend the RSP coupling as the canonical curve; nothing is theorem-grade before this is pinned | the fable design session (math successor note) |
| One note or two | this unified note now; a math successor note (or Lane B section) splits out for the formalized algebra | the fable session decides at graduation |
| `supersession-lifecycle §4.5` — does promotion re-anchor stratum depth? | undecided; the math makes it a sharp dichotomy — *contractive-except-at-owner-verdicts* (elegant) vs *unconditionally contractive* (deep insight permanently damped) | the fable session, with the dynamical reading in hand |
| Weighted vs combinatorial inner products (PD-b, inherited from `edge-dynamics`) | combinatorial (v1); the metric tier of §2.5 is a second customer | when the metric-coherence tier is built |
| The two mode-3 operators (ledger-compression vs correspondence) | both named; the protocol type system must require a temporal query to declare which | the protocol type-system plan |
| Where kernel-representability is lost along the curve (`β*`) | open; conjectured finite on sparse citation graphs | computable post-extractor (a Thread-C sweep) |

## Cross-references

- `docs/brainstorms/core-query-protocol.md` — the warrant; all four threads, the two opus
  formalization sketches, and the **fable rigorous pass** (2026-07-13 capsules) with the full
  derivations and literature this note summarizes.
- `docs/design-notes/edge-dynamics.md` — the 1-form lift, the Helmholtz/Hodge decomposition
  (`P_grad + P_harm + P_curl = I`), `L₁` as the Fourier basis, the THREAD lens (`P_harm`), the
  Lane A/B seam. The math successor extends its Lane B.
- `docs/design-notes/recursive-strata-amendment.md` — `γ^d` (Invariant 10), the typed
  `edge_budget` (grounding/lateral/cross-stratum), fibers vs dispositional edges.
- `docs/design-notes/supersession-lifecycle.md` — the dispositional edge; §4.5 (the Parked
  dichotomy); §7 (rename identity — the data prerequisite for §2.5's flatness measurements).
- `docs/design-notes/the-sacred-boundary.md` — the plane-crossing the §2.4 scope ruling draws.
- `docs/design-notes/capability-evaluation-harness.md` — the home for §2.6.
- `docs/design-notes/observed-data-and-the-assistant-tier.md` — the mirror firewall §2.1/§2.4
  inherit.
- `docs/findings/finding-0059.md`, `finding-0061.md` — the bookkeeping warrant (doc→doc
  blindness; stale-baseline class); `finding-0062.md` — the direction finding this note graduates.
- `core/stores/reference_edges.py` — the live substrate (61k edges) + its minimal query API;
  the Views `core/mirror.py`, `core/sensing.py`, `core/ops_view.py`, `ops/effects.py`;
  `core/librarian/librarian.py` (the semantic-RAG client); `core/complex/hodge.py` (the built
  degree-1 Hodge object the algebra sits over).
