# The Mind Palace — Mathematical Foundations of the Dreamer
### Formal companion III to `WHITEPAPER.md` / `WHITEPAPER-TECHNICAL.md` / `WHITEPAPER-FORMAL-PROPERTIES.md`

**Version 0.1 (draft for review) · 2026-06-30**

This document is the mathematical foundation for the Dreamer subsystem and its planned
extensions (the R-track interpreter panel, recursive dreaming, cross-graph resonance, and the
alignment subsystem). It **extends** the existing architecture; it does not redesign it. Every
invariant in companions I–II is preserved: the provenance firewall, object-capability security,
mirror-not-oracle, regenerability, the authored/curated/observed/interpreted separation.

It supersedes the informal draft chapters produced in earlier sessions (referred to below as
*the draft*). §0 is an **errata** recording exactly what the draft got wrong and why; the
remaining parts are the corrected and continued proposal.

---

## 0. Prime directive: the minimalism filter

The single governing constraint, stated once and enforced everywhere. It is the mathematical
form of gap **G8** ("don't over-formalize — formalism should constrain, not decorate") and of the
white paper's discipline that *each line of philosophy compiles to an invariant with a structural
enforcement point.*

> **The filter.** A mathematical structure enters this framework only if it provides a
> **representational**, **computational**, or **validation** capability that the machinery
> already in the system cannot express. For every structure we ask the quartet:
> *(a) what capability does it enable that we cannot already express?*
> *(b) what does it cost to compute on one M2 Max, offline?*
> *(c) how is it validated?*
> *(d) does the system need that capability now, or is it gated behind a deferred roadmap item?*
> If (a) is empty, the structure is **rejected**. If (a) is real but (d) says "later," it is
> **deferred with its trigger named** — proposed, not adopted.

Every proposed object below carries one of four **status tags**, and separately one of three
**disposition tags**:

| Status (epistemic) | Meaning |
|---|---|
| **[Theorem]** | provable from stated assumptions |
| **[Engineering]** | a design decision, true by construction / choice |
| **[Conjecture]** | plausible, testable, not yet established |
| **[Speculative]** | future direction, stated so it is not mistaken for fact |

| Disposition (roadmap) | Meaning |
|---|---|
| **ADOPT** | build now; earns its place against the current system |
| **DEFER→X** | real capability, but gated behind roadmap item X (e.g. R3 recursive dreaming) |
| **REJECT** | fails the filter; recorded so it is not re-proposed |

Notation follows companion II (`WHITEPAPER-TECHNICAL.md`) exactly. A reconciliation table for the
draft's divergent notation is Appendix B.

---

## 0.1 Errata against the draft chapters

The draft (Chapters 1–5) is directionally useful but contains six errors that conflict with the
authoritative companions, plus a systematic over-reach against the minimalism filter. Recorded
here so the corrections are permanent and reviewable.

| # | Draft claim | Problem | Correction (this document) |
|---|---|---|---|
| E1 | "$P$ is a **strictly ordered** set of provenance classes" (Ch 1.2) | Contradicts **G8** / `TECHNICAL §2`, which *retired* the provenance preorder as decorative. Nothing orders the classes; $\textsf{interpreted}$ is a derived axis orthogonal to trust. | Provenance is an **unordered labeling** $\rho:V\to P$. The only load-bearing structure is **$\mathsf{MR}$-membership** (§1.2), which is now *structural* via `MirrorView`. |
| E2 | Confidence decay $c(b)\le\gamma^{d(b)}\,c(a)$ (Axiom 4) | Mixes the **full-depth** exponent with the **parent's** confidence — double-counts depth under recursion, and disagrees with the authoritative bound. | Absolute bound against **own grounding**: $c(\kappa)\le\gamma^{d(\kappa)}g(\kappa)$. The parent-recursive form, if wanted, is per-edge ($\gamma^1$), not $\gamma^{d}$. Reconciled with the agreement multiplier via an explicit clamp (§7.2). |
| E3 | Hyperbolic **radius certifies** generalization vs. hallucination (Ch 3.3) | Circular: radius is an artifact of embedding the derivation tree you fed in; it re-reads topology as epistemics. Cannot see content-level hallucination. | Hyperbolic embedding is an **organizational / retrieval prior** for deep trees, not an epistemic certifier. Grounding $g$ and the decay bound do the epistemic work. **DEFER→R3.** |
| E4 | Product-manifold distance $d=\alpha d_{\mathbb{R}}+\beta d_{\mathbb{H}}$ (Ch 3.4) | A linear blend is a valid dissimilarity but is **not** the product-manifold geodesic distance. Category slip between "a metric" and "the product metric." | Use the product Riemannian distance $\sqrt{d_{\mathbb{R}}^2+d_{\mathbb{H}}^2}$ **or** name the weighted blend a heuristic. Either is fine if named honestly (§3.4). |
| E5 | $\beta_1$ (1-cycles) $=$ "contradictions / circular reasoning" (Ch 5.2) | Homology of a similarity graph sees topological **holes**, not logical contradiction (a semantic/signed property). Derivational cycles are **structurally impossible** (the DAG), so $\beta_1$ cannot be finding them. | $H_1$ classes are candidate **conceptual holes** (circled-but-unfilled themes). Contradiction lives in the typed `contradicts` edge + the adjudicator, which already exist (§4/§5 corrected). |
| E6 | Dreamer stability $=$ graph fixed point $\mathcal{D}(\mathcal{H})=\mathcal{H}$ (Ch 4.5) | The Dreamer is **append-only**; it never reaches graph-equality. "Semantic energy" is undefined. | Stability $=$ **bounded confidence-weighted interpreted mass**, which yields a concrete criterion: **$b\gamma<1$** (branching × decay), §4.5 corrected — a real, checkable constraint the draft missed. |

**Systematic over-reach.** Hyperbolic geometry, product manifolds, and reaction–diffusion PDEs
are presented as current necessities. They address **deep recursive derivation**, which is
explicitly **flag-OFF** today — *every interpreted node is currently depth-1 over authored ground*
(`PROGRESS.md`, I10/G2). Under the minimalism filter they are **DEFER→R3**, not ADOPT. The math
the draft *under*-weights — spectral graph theory — is the load-bearing one, because the alignment
subsystem's **min-cut-to-authored** and **echo-chamber detection** *are* spectral graph theory
(§6).

**What the draft got right** (kept, tightened): the joint-entailment argument for hyperedges
(§2), the simplicial-complex rejection (§2.2), diffusion distance (§3.3, the strongest geometric
proposal), and the rewrite-system framing of the Dreamer (§4.2).

---

# Part I — Foundations

## 1. Knowledge, provenance, inference

### 1.1 What the current system already is (so we do not re-derive it)

The running system already fixes the base objects. We reuse them verbatim.

- Corpus nodes $V$ (notes/chunks); embedding $e:V\to\mathbb{R}^{n}$, $n=2560$; cosine similarity
  $\cos(u,v)=\frac{\langle e(u),e(v)\rangle}{\lVert e(u)\rVert\lVert e(v)\rVert}$.
- Thought-graph $G=(V,E)$, $E=E_{\text{auth}}\cup E_{\text{sim}}$, with
  $E_{\text{sim}}=\{(u,v):\cos(e(u),e(v))\ge\sigma\}$, $\sigma\in[0.55,0.75]$ corpus-calibrated (G7).
- Provenance labeling $\rho:V\to P$, $P=\{\textsf{auth-solo},\textsf{auth-dlg},\textsf{curated},\textsf{observed},\textsf{interpreted}\}$; mirror-readable set $\mathsf{MR}=\{\textsf{auth-solo},\textsf{auth-dlg}\}$; projection $\pi_{\mathsf{MR}}(V)=\{v:\rho(v)\in\mathsf{MR}\}$.
- A **claim** $\kappa=(\text{statement},\ \mathrm{supp}(\kappa)\subseteq V)$; grounding $g(\kappa)\in[0,1]$, utility $u(\kappa)$, confidence $c(\kappa)$, derivation depth $d(\kappa)$.

The Dreamer's mathematics is a theory of **how claims are formed, ranked, evolved, and audited
over $G$** — nothing in Part I is new representation; it is the precise statement of the existing
contract.

### 1.2 Design axioms (corrected)

Let $\mathcal{O}$ range over system operations and $\mathcal{D}$ over autonomous Dreamer passes.

- **A1 (Immutability of the authored base).** If $\rho(v)\in\mathsf{MR}$ then $v$ is immutable:
  no $\mathcal{O}$ mutates it. *(Structural: raw store is content-addressed, write-once.)* **[Engineering]**
- **A2 (Provenance closure / firewall).** For introspective $\mathcal{D}$ acting on
  $S\subseteq V$: (i) input is restricted, $S\subseteq\pi_{\mathsf{MR}}(V)$; (ii) every produced
  atom $x$ has $\rho(x)=\textsf{interpreted}$. *(Structural: `MirrorView`; `DerivedStore` has no
  provenance parameter — I5/I6.)* **[Engineering]**
- **A3 (Acyclic derivation).** The relation $\to_d$ ($a\to_d b$ iff $b$ is interpreted from
  evidence including $a$) induces a **DAG**; no atom is its own ancestor. *(Structural:
  cycle-refused-at-insert, `DerivationCycleError` — I10/G2.)* **[Engineering]**
- **A4 (Confidence decay — corrected).** With $d(\kappa)$ the longest path from $\kappa$ to an
  authored leaf and $g(\kappa)\in[0,1]$ its grounding score,
  $$c(\kappa)\ \le\ \gamma^{\,d(\kappa)}\,g(\kappa),\qquad \gamma\in(0,1),\qquad\text{every support-closure leaf authored.}$$
  This is an **absolute** bound (depth discount × own grounding), *not* a recurrence against the
  parent's confidence. It is the design constraint the technical companion labels an *illustrative
  contraction analogy*, not a convergence theorem about LLM output. **[Engineering]**

> **E1/E2 fixed.** $P$ is unordered (only $\mathsf{MR}$-membership bites); A4 binds against $g$, not $c(\text{parent})$.

### 1.3 Why bare embeddings are insufficient (kept, tightened)

An embedding-only regime represents each thought as a point $v\in\mathbb{R}^n$ and every relation
as cosine similarity. Three deficiencies motivate a richer object — each is a *representational*
gap (filter clause (a)), not an aesthetic preference:

1. **Symmetry vs. entailment.** $\cos$ is symmetric; derivation, generalization, and support are
   **directed**. "Moving to Paris" supports "leaving New York," not conversely. A symmetric metric
   cannot carry $\mathrm{supp}(\kappa)$'s direction. **[Theorem]** (trivially: any symmetric kernel
   is invariant under argument swap).
2. **Relatedness ≠ agreement.** Distributional embeddings place a statement and its negation
   *close* (shared topical axes). Cosine proximity therefore cannot distinguish "supports" from
   "contradicts"; that distinction must be carried by a **typed edge**, not inferred from distance.
   **[Engineering]**
3. **Provenance blindness.** The geometry of $\mathbb{R}^n$ is blind to $\rho$. The firewall is a
   property of the *labeling and the read path*, never of the metric. **[Engineering]**

Embeddings carry the *substance* of a thought; the *scaffolding* (direction, type, provenance,
grounding) lives in the graph. This is the whole reason the object below is a graph-over-embeddings,
not embeddings alone.

### 1.4 The knowledge atom and inference

**Definition 1.1 (Atom).** An atom is $k=(e(k),\ \rho(k),\ t(k),\ g(k),\ \mathcal{E}(k))$: its
embedding, provenance, immutable creation time, grounding score, and typed incident edges. For
authored atoms $g\equiv 1$ by definition (they *are* ground); grounding is informative only for
$\textsf{interpreted}$ atoms. *(Note: confidence $c$ and utility $u$ are **not** atom fields — they
are per-claim rankings kept on separate axes, I11; baking either into the atom would invite a
single combined scalar, which is forbidden.)*

**Definition 1.2 (Inference).** Inference is a map $\mathcal{I}:2^{V}\rightharpoonup 2^{V}$ taking
a support set to newly minted atoms, subject to A2 ($\rho=\textsf{interpreted}$), A3 (adds only
DAG-consistent $\to_d$ edges), A4 (confidence bounded), and grounding termination (every leaf of
the support closure is authored). $\mathcal{I}$ is **partial**: on inputs that would violate an
axiom it is undefined, i.e. the store refuses the insert. **[Engineering]**

---

## 2. The unified knowledge object

### 2.1 The representational claim, and what it actually costs

**The joint-entailment argument (kept — correct).** A synthesis $\kappa_3$ scaffolded by
$\{\kappa_1,\kappa_2\}$ jointly is *not* two independent edges $(\kappa_1,\kappa_3),(\kappa_2,\kappa_3)$:
those assert $\kappa_1\Rightarrow\kappa_3$ and $\kappa_2\Rightarrow\kappa_3$ *separately*, losing
that removing either premise collapses the support. The faithful object is a **directed hyperedge**
with tail $T=\{\kappa_1,\kappa_2\}$ and head $H=\{\kappa_3\}$.

**The correction the draft missed — this is not a new structure to build.** The running
`DerivedStore.add(derived_from=[…])` already records **a set of tail digests → one head node**.
That *is* a directed hyperedge with a single-node head — a **B-arc** (backward hyperarc). The
system is therefore *already* a B-hypergraph; $\mathrm{supp}(\kappa)$ is its tail set. What §2
buys is the **correct name and algebra** for a structure that exists, plus the general case
($|H|>1$) which is **DEFER**red — we have no operation today that mints several co-derived heads
from one premise set.

> **Filter verdict.** Directed hypergraph, single-node heads: **ADOPT** (already present; formalize).
> General multi-head hyperedges: **DEFER** — no current capability needs them.

### 2.2 Rejected and deferred alternatives (kept)

- **Simplicial complexes — REJECT.** Downward closure (every face of a simplex present) is false
  for reasoning: $\{\kappa_1,\kappa_2,\kappa_3\}$ cohering jointly does not entail any pair
  coheres. Imposing closure fabricates sub-relations. **[Theorem]** (downward closure is an axiom
  of the structure; the data violate it).
- **Sheaf theory as the base object — DEFER→(validation only).** Sheaves detect gluing failures
  (local agreement that admits no global section) — a real inconsistency signal — but as the
  *base* store they impose cohomology cost with no retrieval payoff. Reconciled in §5.3: kept as a
  **[Speculative]** validation lens, not the substrate. (This fixes the draft's contradiction of
  deferring sheaves in Ch 2 then using them in Ch 5.)

### 2.3 The provenance-stratified directed hypergraph

**Definition 2.1.** $\mathcal{H}=(V,\mathcal{E},\tau,\rho)$ where $V\equiv$ atoms; each
$e\in\mathcal{E}$ is a directed hyperedge $e=(T(e),H(e))$, $T,H\subseteq V$; $\tau:\mathcal{E}\to\mathcal{T}$
types it, $\mathcal{T}=\{\textsf{derives},\textsf{contradicts},\textsf{contextualizes},\textsf{supports}\}$;
$\rho$ extends to $\mathcal{E}$. **Today $|H(e)|=1$ for all $e$** (B-hypergraph).

**Axiom 5 (Hyperedge provenance bound).** A Dreamer-produced $e$ has $\rho(e)=\textsf{interpreted}$
and $H(e)\subseteq\rho^{-1}(\textsf{interpreted})$: the Dreamer may scaffold only its own
interpretations, never assert a new authored truth. *(Structural — same mechanism as A2.)* **[Engineering]**

**Acyclicity is typed.** Only the $\textsf{derives}$-sub-hypergraph must be acyclic (A3);
$\textsf{contradicts}$ and $\textsf{contextualizes}$ edges may cycle freely — a contradiction is
inherently symmetric. This is a genuine refinement over "the whole graph is a DAG," and it is where
**contradiction is represented** (see §5, correcting E5).

### 2.4 Implementation mapping (matches the built stores)

- **Vertices** → LanceDB (vector + digest + scalar $\rho,t,g$), unchanged.
- **Incidence** → SQLite `DerivedStore`: `hyperedges(edge_id, type, provenance, created_at)` +
  `hyperedge_nodes(edge_id, node_id, role∈{tail,head})`. The current single-column `derived_from`
  is the $|H|=1$ special case; the junction table is the additive generalization (one migration).
- Retrieval of a claim's full scaffolding $T(e)$ is an indexed lookup, $O(\log|V|+|T(e)|)$ — *not*
  $O(1)$ as the draft stated; the correction matters for §9's complexity budget.

The incidence matrix is $H\in\{0,1\}^{|V|\times|\mathcal{E}|}$ (overloading $H$ with the head-set is
avoided in §6 by writing the incidence matrix $\mathbf{B}$). Spectral cost is deferred to §6, where
we show it is affordable precisely because the system is inference-bound, not BLAS-bound.


---

# Part II — Geometry

**Principle:** *the Dreamer needs continuous measurements it can compute deterministically, offline,
without a model call.* Every geometry below is a NumPy computation over stored vectors or the
sparse incidence — the LLM never computes them; it only receives the context windows they select.

## 3.1 The semantic base (kept)

$\mathbb{R}^n$ with cosine distance is retained for *semantic similarity* — analogy, topical
proximity. It is the substrate the similarity edges $E_{\text{sim}}$ and the existing clusterer
already use. **ADOPT** (it is the status quo). Its one limitation for the Dreamer is that it
conflates *"about the same thing"* with *"derives from,"* which the graph — not a second embedding
— resolves.

## 3.2 Diffusion geometry — the strongest proposal (ADOPT)

**Motivation (capability (a)).** Two authored notes can share no vocabulary (far in $\mathbb{R}^n$)
and no direct link, yet both sit in the same *implicit neighborhood* of the graph. Semantic
distance cannot see this; a diffusion distance can. It is the deterministic floor for
"which notes belong to the same implicit context" **before** any synthesis — exactly the job the
Dreamer's clustering step does, made principled.

**Construction.** Let $\mathbf{T}$ be the (confidence-weighted, §4.3) row-stochastic transition
matrix of a random walk on $\mathcal{H}$, with stationary distribution $\phi$. The $t$-step
transition is $p_t(x,\cdot)=\big(\mathbf{T}^t\big)_{x,\cdot}$. The **diffusion distance** (Coifman–Lafon)
is
$$D_t(x,y)^2\ =\ \sum_{z\in V}\frac{\big(p_t(x,z)-p_t(y,z)\big)^2}{\phi(z)}\ =\ \sum_{\ell\ge1}\lambda_\ell^{2t}\big(\psi_\ell(x)-\psi_\ell(y)\big)^2,$$
where $(\lambda_\ell,\psi_\ell)$ are the eigenpairs of $\mathbf{T}$ (the second equality is the
spectral form; $\lambda_0=1$ drops out). **[Theorem]** (standard; the equality is exact).

**Why it is cheap.** The eigenvalues decay; truncating at the first $r$ nontrivial modes
($\lambda_\ell^{2t}$ negligible beyond) gives an $r$-dimensional **diffusion map**
$x\mapsto(\lambda_1^t\psi_1(x),\dots,\lambda_r^t\psi_r(x))$ in which diffusion distance is ordinary
Euclidean distance. Clustering the diffusion map with the existing single-linkage/`HDBSCAN`-style
step is then a drop-in upgrade of the deterministic clusterer. On the current corpus scale
($\sim10^3$ nodes, $\sim10^3$ vectors) a partial eigensolve is milliseconds. **ADOPT.**

**Validation (c).** Determinism test (fixed seed ⇒ identical map); metamorphic test (adding an
isolated note far from a cluster must not move that cluster's intra-diffusion-distances beyond a
tolerance); stability test (small $\sigma$ perturbation ⇒ bounded map perturbation).

## 3.3 Hyperbolic / product geometry — real, but not yet (DEFER→R3)

**The honest status.** Hyperbolic embedding is the continuous analogue of a tree: volume grows
exponentially with radius, matching a branching derivation hierarchy. If recursive dreaming (R3)
produces **deep** derivation trees, embedding the $\textsf{derives}$-DAG in the Poincaré ball
$\mathbb{H}^m=\{x\in\mathbb{R}^m:\lVert x\rVert<1\}$ with
$$d_{\mathbb{H}}(x,y)=\operatorname{arcosh}\!\Big(1+2\tfrac{\lVert x-y\rVert^2}{(1-\lVert x\rVert^2)(1-\lVert y\rVert^2)}\Big)$$
gives a low-distortion layout where abstraction sits near the origin, specifics near the boundary.
The distance formula and metric tensor $g_x=\big(\tfrac{2}{1-\lVert x\rVert^2}\big)^2 I$ are correct
and retained. **[Theorem]** (standard Poincaré model).

**Two corrections (E3, E4):**

- **Radius is not an epistemic certifier.** A synthesized node's radial position is an *artifact of
  embedding the derivation tree you supplied*; "closer to origin ⇒ better generalization, drifting
  to boundary ⇒ hallucination" reads the input topology back out as a quality score — circular.
  Hallucination is a *content* property invisible to the layout. The epistemic work is done by
  $g(\kappa)$ (grounding) and the A4 decay bound. Hyperbolic geometry's honest role is an
  **organizational / retrieval prior and a visualization** — useful, not evidential.
- **The product metric.** If both geometries are used, the space is the product manifold
  $\mathcal{M}=\mathbb{R}^n\times\mathbb{H}^m$ whose geodesic distance is
  $d_{\mathcal{M}}(x,y)=\sqrt{d_{\mathbb{R}}(x,y)^2+d_{\mathbb{H}}(x,y)^2}$. The draft's weighted
  **linear** blend $\alpha d_{\mathbb{R}}+\beta d_{\mathbb{H}}$ is a legitimate *dissimilarity*
  (a positive combination of metrics is a metric) but is **not** the product-manifold distance;
  use it only if named a heuristic, and prefer the Pythagorean form for the "manifold" claim.

**Filter verdict.** **DEFER→R3.** With every interpreted node at depth 1 today, there is no tree to
embed; adopting hyperbolic geometry now would be machinery in search of a problem. Its trigger is
explicit: *enable when the $\textsf{derives}$-DAG's median depth exceeds 2.*

## 3.4 Information geometry / Fisher metric — REJECT (reasoning fixed)

Modeling each thought as a distribution $\mathcal{N}(\mu,\Sigma)$ with the Fisher–Rao metric is
epistemically elegant but fails the filter. The draft's stated reason (it *requires* LLM sampling)
is not airtight — one could estimate $\Sigma$ from retrieved-neighbor spread without a model. The
**correct** reason to reject: (i) it duplicates what $g$ and the confidence axes already encode
(uncertainty is carried by grounding+depth, deterministically); (ii) a per-thought covariance adds
$O(n^2)$ state per atom against a $2560$-dim embedding — ruinous storage for no retrieval gain;
(iii) it invites collapsing uncertainty into distance, re-entangling belief with geometry. **REJECT.**


---

# Part III — Dynamics

**Principle:** *the graph evolves in discrete idle-window steps; evolution is code, adjudicated by
grounding, never a continuous background compute that "stutters."*

## 4.1 The Dreamer as a graph-rewrite operator (kept)

A Dreamer pass is the operator $\mathcal{D}:\mathcal{H}_t\mapsto\mathcal{H}_{t+1}$ realized by a
triplet $(S,\sigma,\omega)$ — matching the built pipeline exactly:

1. **Select** $S$: a deterministic predicate carving $\mathcal{G}_{\text{sub}}\subseteq\pi_{\mathsf{MR}}(V)$
   (the `MirrorView` firewall; clustering over the diffusion map of §3.2).
2. **Synthesize** $\sigma$: the (earned) model call producing candidate atoms/edges from
   $\mathcal{G}_{\text{sub}}$ — the *only* stochastic step.
3. **Commit** $\omega$: the grounding self-check + A3/A4/A5 admission; a candidate that fails is
   refused, never stored. $\mathcal{D}$ is **append-only** on the interpreted stratum and **never**
   writes $\mathsf{MR}$.

**[Engineering].** $\mathcal{D}$ factors as $\omega\circ\sigma\circ S$; only $\sigma$ is a model,
and its output is data that $\omega$ may reject — the "model advises, code acts" split, one level up.

## 4.2 Confidence-weighted attention (kept; notation fixed; subsumes centrality)

*Where should a pass look?* Model the Dreamer's attention as a **random walk with restart** on
$\mathcal{H}$, transition matrix (avoiding the draft's $P$/provenance collision — write $\mathbf{T}$):
$$\mathbf{T}_{ij}=\frac{w_{ij}\,g(j)}{\sum_{k}w_{ik}\,g(k)},$$
with $w_{ij}$ the (similarity/typed) edge weight and $g(j)$ the grounding of node $j$. Grounding-
weighting biases dwell toward authored/well-grounded nodes and away from speculative ones; the
stationary distribution $\phi$ ranks **thematic anchors**.

**Filter note.** This is a refinement of, not an addition to, the R0 `centrality` interpreter
(degree hubs). It is the *grounded PageRank* of the graph. **ADOPT** as the weighting used by
§3.2's walk; do **not** present it as a new pillar — it is one line of reweighting.

## 4.3 Heat-kernel diffusion — yes; reaction–diffusion — REJECT

The graph heat kernel $\mathbf{K}_t=e^{-tL}$ ($L$ the Laplacian, §6) is the correct operator for
**label propagation**: spread a theme label from a seed set to unlabeled neighbors, smoothing over
the graph. It is a well-defined, cheap, deterministic smoother. **ADOPT** (as a §6 spectral tool).

The draft's **reaction–diffusion** PDE $\partial_t u=-\alpha Lu+\mathcal{F}(u)$ is **REJECT**ed: it
names a nonlinearity $\mathcal{F}$ with no defined quantity $u$, no reaction kinetics, and no
validation. The linear diffusion term alone (label propagation) delivers everything the section
actually used; the Turing-pattern framing is decoration. **REJECT** the nonlinear term; keep the
linear heat smoother.

## 4.4 Discrete evolution (kept, sharpened)

Evolution is discretized to **idle-window steps** $\Delta t$ under the foreground gate — no
continuous background solve. Each step: recompute the diffusion map incrementally, run selected
interpreters, admit grounded claims. This is the Scheduler's trough-only tiering, restated as the
time-discretization of the dynamical system. **[Engineering].**

## 4.5 Stability — corrected: the $b\gamma<1$ criterion

**E6 fixed.** The Dreamer is append-only; there is no graph fixed point $\mathcal{D}(\mathcal{H})=\mathcal{H}$
to seek. The right stability object is the **total confidence-weighted interpreted mass**
$$M\ =\ \sum_{\kappa\in\rho^{-1}(\textsf{interpreted})}c(\kappa)\ \le\ \sum_{\kappa}\gamma^{\,d(\kappa)}g(\kappa).$$
Suppose recursive dreaming has interpreted **branching factor** $b$ (each depth-$d$ claim seeds at
most $b$ depth-$(d{+}1)$ claims) and grounding is bounded by $g_{\max}\le1$. Then the mass
contributed at depth $d$ is $\le b^{d}\gamma^{d}g_{\max}$, and
$$M\ \le\ g_{\max}\sum_{d\ge0}(b\gamma)^{d}\ =\ \frac{g_{\max}}{1-b\gamma}\quad\text{iff}\quad \boxed{\,b\gamma<1\,}.$$
**[Theorem]** (geometric series). This is the concrete, checkable stability criterion the draft
gestured at with "semantic energy bounded." It ties three built knobs together: the decay
$\gamma$ (=0.5, G7), the depth cap (R3), and the similarity threshold $\sigma$ that governs how
many candidate children a claim can spawn (its effective $b$). **Recursive dreaming (R3) is safe to
enable iff the configuration guarantees $b\gamma<1$**; the drift gauge (A1) then watches the
realized curve. When $b\gamma\ge1$, interpreted mass can diverge — the formal shape of "the stack
overflow of a mind thinking only about itself."

> **This is the payoff of Part III:** a one-line, testable admission criterion for recursive
> dreaming, derived from the existing decay axiom — no new machinery.

---

# Part IV — Topology

**Principle:** *use topology only where it sees something the graph metrics and typed edges do not —
and interpret it honestly.*

## 5.1 Persistent homology under the confidence filtration (ADOPT-with-correction)

**The filtration.** Order the graph by a decreasing **grounding/confidence** threshold: for
$\epsilon_1>\epsilon_2>\dots$, let $\mathcal{G}_{\epsilon_i}$ be the subgraph on
$\{v:g(v)\ge\epsilon_i\}$ (authored nodes, $g\equiv1$, enter first). This is a genuinely apt
filtration for *this* system: it asks *"which structures survive as we demand higher grounding?"*

**Correct readings:**

- $\beta_0(\epsilon)$ — number of connected components — tracks **intellectual domains** and their
  *merging* as grounding is relaxed. A component that stays separate down to low thresholds is a
  robustly distinct concern. **[Engineering]** interpretation; standard TDA.
- $H_1$ (1-cycles) — **conceptual holes**, i.e. themes the author *circles but never fills in*: a
  ring of pairwise-related notes with no central connecting note. This is a *gap-surfacing* signal
  ("you keep orbiting X without ever stating it"), useful as a **utility**-axis prompt.

**E5 fixed — what $H_1$ is NOT.** A 1-cycle is **not** a logical contradiction and **not** circular
reasoning. Contradiction is a semantic, *signed* property; homology of an unsigned similarity graph
cannot see it. Circular *derivation* is structurally impossible (A3), so $\beta_1$ cannot be finding
it. **Contradiction is represented and detected elsewhere:** the typed $\textsf{contradicts}$
hyperedge (§2.3) plus the adjudicator's deferred judge seam — a cheap, direct mechanism that already
exists. Do not route contradiction through homology.

**Filter verdict.** Persistent $\beta_0$/$H_1$ under the confidence filtration: **ADOPT** as a
*utility-axis* diagnostic (surface gaps and robust domains), computed by `ripser`/`gudhi` over the
sparse graph — never as a belief signal. Persistence values (birth–death lifetimes) give the
robustness score; short-lived features are noise and are dropped.

## 5.2 Sheaf consistency — DEFER (reconciled with §2.2)

A cellular sheaf $\mathcal{F}$ over the graph assigns a stalk (a meaning subspace) to each node and
restriction maps $\mathcal{F}_{v\trianglelefteq e}$ along edges; the **sheaf Laplacian** $L_\mathcal{F}$
has kernel = global sections, and the Dirichlet energy $x^\top L_\mathcal{F}x$ measures how far the
local assignments are from gluing consistently. High energy on a cluster = the author's uses of a
concept do not cohere across contexts — a real inconsistency signal, distinct from a typed
contradiction.

**Honest status.** This is more defensible than the draft's $\beta_1$ claim but is **[Speculative]**
and expensive (defining principled restriction maps offline is unsolved for this corpus). It stays a
*validation-only* future lens, consistent with §2.2's deferral. **DEFER**; the cheaper existing
mechanism (typed $\textsf{contradicts}$ edges + adjudicator) covers the near-term need.


---

# Part V — Spectral methods (the load-bearing chapter)

**Principle:** *the alignment subsystem is spectral graph theory.* Min-cut-to-authored, echo-chamber
detection, and community structure — the concrete detection tools the alignment note asks for — are
all eigen/flow computations over $\mathcal{H}$. This is the chapter that earns its keep hardest.

## 6.1 The Laplacians

For a weighted graph with adjacency $A$ and degree $D=\operatorname{diag}(A\mathbf{1})$:
$$L=D-A\ \text{(combinatorial)},\quad L_{\mathrm{sym}}=I-D^{-1/2}AD^{-1/2},\quad L_{\mathrm{rw}}=I-D^{-1}A.$$
All are PSD; $L\mathbf{1}=0$; the multiplicity of eigenvalue $0$ equals the number of connected
components; the **Fiedler value** $\lambda_2$ (second-smallest of $L_{\mathrm{sym}}$) measures
algebraic connectivity. **[Theorem]** (standard).

**The hypergraph case (honest).** For $\mathcal{H}$ with incidence $\mathbf{B}\in\{0,1\}^{|V|\times|\mathcal{E}|}$,
edge weights $W$, vertex/edge degrees $D_v,D_e$, the **normalized hypergraph Laplacian** (Zhou et al.)
is
$$L_{\mathcal{H}}=I-D_v^{-1/2}\,\mathbf{B}\,W\,D_e^{-1}\,\mathbf{B}^{\top}\,D_v^{-1/2}.$$
This is the **clique-expansion** operator: it approximates each hyperedge by a weighted clique on its
members. It is a genuine approximation — it discards the tail→head *direction* and the
irreducible-joint structure §2 was built to preserve. **[Engineering] tradeoff:** for the *undirected
similarity* backbone $E_{\mathrm{sim}}$ (where all our spectral clustering runs), clique expansion is
exact (those edges are already pairwise). We use $L_{\mathcal{H}}$ **only** on the undirected
similarity backbone; the directed $\textsf{derives}$ structure is handled combinatorially (min-cut,
§6.4), not spectrally. This keeps the approximation where it is harmless.

## 6.2 Spectral clustering = the deterministic clustering floor (ADOPT)

The Dreamer's `Select` step already clusters the mirror. Spectral clustering makes it principled:
embed nodes by the bottom-$k$ eigenvectors of $L_{\mathrm{sym}}$, then $k$-means/single-linkage in
that space. On the diffusion map (§3.2) this is *identical* to diffusion clustering — the two
chapters converge on one computation. **[Theorem]** (the diffusion map's coordinates are scaled
Laplacian eigenvectors). **ADOPT**: replace the ad-hoc cosine single-linkage with a spectral/diffusion
clusterer; it is more robust to the chaining the current lexical-fallback suffers (F9 tuned $\sigma$
to 0.50 precisely to dodge chaining — spectral clustering dissolves that problem).

Community detection (Leiden, already named in `TECHNICAL §6`) is the modularity-optimizing cousin;
keep it as the R0 `community` interpreter. Spectral and modularity clustering are cross-checks — their
disagreement is itself a signal (a cluster only one method finds is fragile).

## 6.3 Heat kernel, random walks, graph Fourier

- **Heat kernel** $e^{-tL}$ (§4.3): label propagation / smoothing. **ADOPT** (cheap, deterministic).
- **Random walks**: the §3.2/§4.2 transition operator; its spectrum gives diffusion distance and the
  stationary anchor ranking. **ADOPT.**
- **Graph Fourier transform**: eigenvectors of $L$ are the graph's Fourier basis; a signal $s:V\to\mathbb{R}$
  (e.g. a per-note recency or a theme-membership indicator) has *smoothness* $s^\top L s=\sum_{(u,v)}w_{uv}(s_u-s_v)^2$.
  A low-$s^\top L s$ signal is graph-coherent. **ADOPT-LITE**: use $s^\top L s$ as a coherence score
  (e.g. "is this proposed theme label smooth over the cluster, or scattered?"), a one-line quadratic
  form — not a full GSP filterbank, which the filter rejects as unneeded.
- **Tensor decompositions** (CP/Tucker over a relation×node×node tensor): **REJECT** — we have four
  relation types and no learned multi-relational embedding task; a tensor factorization would be
  impressive and idle.

## 6.4 The alignment detector: min-cut-to-authored & conductance (ADOPT — Track A2)

This is the section the whole spectral chapter exists for. The alignment subsystem
(`design-notes/alignment-subsystem.md`) specifies detection by *"min-cut-to-authored + community /
echo-chamber metrics."* Here is its mathematics.

**Setup.** Partition $V=V_{\mathrm{auth}}\sqcup V_{\mathrm{int}}$ (authored ground vs. interpreted
layer). For an interpreted community $S\subseteq V_{\mathrm{int}}$ (a cluster of dreams / a theme):

**Min-cut to authored.** Define the **grounding cut**
$$\operatorname{cut}(S,V_{\mathrm{auth}})\ =\ \min_{\text{cuts separating } S \text{ from } V_{\mathrm{auth}}}\ \sum_{(u,v)\in\text{cut}}w_{uv},$$
the minimum total edge weight whose removal disconnects $S$ from all authored ground. A **small**
grounding cut means the community hangs on authored evidence *by a thread* — a fragile, potentially
self-referential bubble. Computable exactly by max-flow (Ford–Fulkerson / push–relabel) on the
sparse graph; on $\sim10^3$ nodes this is milliseconds. **[Theorem]** (max-flow min-cut).

**Conductance / echo-chamber.** The **conductance** of $S$,
$$\Phi(S)\ =\ \frac{w(\partial S)}{\min\!\big(\operatorname{vol}(S),\operatorname{vol}(\bar S)\big)},\qquad \operatorname{vol}(S)=\sum_{v\in S}\deg(v),$$
is low exactly when $S$ is internally dense and externally sparse — the graph signature of an
**echo chamber**. The **Cheeger inequality** ties it to the spectrum:
$$\tfrac{1}{2}\lambda_2\ \le\ \Phi_{\mathcal{G}}\ \le\ \sqrt{2\lambda_2},$$
so the Fiedler value $\lambda_2$ of $L_{\mathrm{sym}}$ **bounds** the best conductance and its
eigenvector *finds* the near-optimal cut — a cheap spectral relaxation of the exact min-cut.
**[Theorem]** (Cheeger).

**The alignment signal (the synthesis).** An interpreted community is a **misalignment candidate**
when it is *simultaneously* low-conductance (tight bubble) **and** low grounding-cut (weakly tied to
authored ground). Formally, flag $S$ when
$$\Phi(S)\le\Phi^\star\quad\wedge\quad \operatorname{cut}(S,V_{\mathrm{auth}})\le \eta\cdot\operatorname{vol}(S),$$
for blessed thresholds $\Phi^\star,\eta$. This is the precise, computable form of *"a bubble drifting
free of the ground"* — the exact failure the mirror-not-oracle discipline exists to prevent. **ADOPT
as Track A2**: it extends the drift profile $\mu$ (A1) with a **structural axis** — the `Axis` type is
already additive for exactly this — and the gated surgery it enables (prune the interpreted bubble,
$\textsf{interpreted}$-only, never authored) is the alignment note's *reset-from-raw* recovery, now
with a trigger metric.

```
        authored ground (V_auth)                 detection:
   ●───●───●───●───●───●───●                       Φ(S)  small  → tight bubble
    \  |  /        thread (small grounding cut)     cut(S,auth) small → weak grounding
     ● ● ●  ←── interpreted community S              both → MISALIGNMENT CANDIDATE → gated prune
      \|/
       ●  (dreams citing dreams, weakly grounded)   healthy S: high cut to authored, moderate Φ
```

**Validation (c).** Property test: a synthetic corpus with a planted self-referential interpreted
loop (weak authored ties) must trip both thresholds; a healthy densely-grounded theme must not.
Monotonicity: adding an authored support edge to $S$ can only *raise* its grounding cut (never lower
it) — a metamorphic invariant.


---

# Part VI — Probabilistic reasoning

**Principle:** *confidence is a bounded, deterministic functional of grounding, depth, and
agreement — deliberately not a learned posterior.* The temptation to "go Bayesian" is where a
mirror quietly becomes an oracle; we resist it on purpose and say why.

## 7.1 The design choice: confidence is not a probability

The system keeps $c(\kappa)\in[0,1]$ as a **grounding-derived score**, not $\Pr[\kappa\text{ true}]$.
This is not a limitation to be lifted later; it is load-bearing. A posterior would (i) require a
prior over the author's beliefs the system has no honest way to set, (ii) tempt a single scalar that
fuses belief and utility (violating I11), and (iii) present *calibrated-looking* numbers the
grounding cannot actually support. **[Engineering].** Calibration is established **empirically** by
the F9 quality suite (confidence must track planted-signal strength), not derived from a probability
model.

## 7.2 Propagation on the DAG (exact, cheap) — and the clamp that reconciles the whitepaper

Because $\to_d$ is a **DAG** (A3), confidence propagates by a single reverse-topological sweep — no
loopy inference, no iteration to convergence. The depth recurrence is
$$d(\kappa)=\begin{cases}0 & \kappa\ \text{authored}\\[2pt]1+\max\limits_{\kappa'\in\operatorname{supp}(\kappa)\cap V_{\mathrm{int}}}d(\kappa') & \text{otherwise.}\end{cases}$$

**A genuine consistency issue in companions I–II, reconciled here.** The technical companion states
both the adjudicator base confidence $c_0(\kappa)=g(\kappa)\big(1+\lambda(|\mathrm{Agr}(\kappa)|-1)\big)$
**and** the decay bound $c(\kappa)\le\gamma^{d(\kappa)}g(\kappa)$. At $d=0$ with agreement
$|\mathrm{Agr}|>1$, the multiplier makes $c_0>g$, contradicting $c\le g$. The two are compatible only
under an explicit **clamp**, which we adopt as the canonical definition:
$$\boxed{\,c(\kappa)\ =\ \min\!\Big\{1,\ \gamma^{\,d(\kappa)}\;g(\kappa)\;\big(1+\lambda(|\mathrm{Agr}(\kappa)|-1)\big)\Big\}\,}\qquad \lambda\le\tfrac14.$$
**[Engineering].** This (i) preserves the whitepaper's intent — agreement multiplies, depth
discounts — (ii) keeps $c\in[0,1]$, and (iii) preserves the property that actually matters, which is
**monotone non-increase in depth for fixed grounding and agreement** (the contraction analogy): for
$d'>d$, $\gamma^{d'}\le\gamma^{d}$ so the pre-clamp value cannot rise with depth. The F9 binding's
$g=\text{grounding}\cdot\text{cohesion}\cdot\text{size\_factor}$ is exactly the right *refinement of
$g$* to make this discriminating (a 2-note cosine-1.0 coincidence scores weak) — recommend
propagating that definition of $g$ into the live `core/dreaming/adjudicator.py` (currently a deferred
R&D follow-up; runbook Hook 2).

> **Recommendation to the builder:** make the clamp the single definition of $c$; delete any code
> path that can produce $c>1$ or $c$ rising with depth. This closes the whitepaper's internal tension
> as *specification precision* — precisely the payoff formalization is supposed to buy (per companion II).

## 7.3 Agreement is a bounded multiplier, not evidence fusion (kept — and why not Bayes)

Cross-interpreter agreement $\mathrm{Agr}(\kappa)$ raises confidence via the bounded multiplier, **not**
via probabilistic fusion. The tempting move — treat each interpreter as an independent evidence source
and combine by naive Bayes / log-odds — is **REJECT**ed for two reasons: (i) the interpreters are
*not* independent (they read the same mirror graph; community and centrality co-fire on hubs), so the
independence product overstates confidence; (ii) unbounded fusion lets **consensus overwhelm
grounding**, turning adjudication back into voting — the exact thing `TECHNICAL §6` forbids
("adjudication, not voting"). The bounded $\lambda\le\tfrac14$ multiplier caps agreement's influence
so grounding stays dominant. **[Engineering].**

## 7.4 Uncertainty representation — the triple, not a distribution

Uncertainty is the ordered triple $(g,d,|\mathrm{Agr}|)$ — grounding, derivational distance,
corroboration — surfaced *as such*, not compressed into one number beyond the ranking scalar $c$.
Belief propagation over general graphs (loopy BP), variational inference, and Fisher-information
uncertainty are all **REJECT**ed: the DAG makes exact propagation trivial, and the richer machinery
would (again) manufacture calibrated-looking posteriors the evidence does not warrant. **[Engineering].**

---

# Part VII — Categorical structure (kept short and practical)

**Principle:** *category theory earns a place here only as the precise language for the firewall and
for resonance-without-contamination — it unlocks no new computation, and we say so.* This is the
minimalism filter applied to the most seductive over-formalization; per G8 we decline the base
machinery and keep only the two clarifying statements.

## 8.1 Provenance as a labeling functor; the firewall as a missing morphism

Let $\mathbf{Store}$ be the category whose objects are the typed stores (raw, vector, derived) and
whose morphisms are the code paths between them. Provenance is a functor
$\rho:\mathbf{Store}\to\mathbf{Disc}(P)$ into the **discrete** category on $P$ (no non-identity
morphisms — the categorical statement of E1: the classes are *unordered*). The firewall is then a
**non-existence** statement: there is **no morphism** $f$ with $\rho(\operatorname{dom} f)=\textsf{observed}$
and $\rho(\operatorname{cod} f)=\textsf{authored}$. Derivation-invariance of $\rho$ (companion II) is
the functor law: every derivation morphism lands in $\textsf{interpreted}$. **[Engineering].** This is
a restatement, not a new mechanism — its value is that "no laundering path exists" becomes a single
diagram condition.

## 8.2 Cross-graph resonance (R5) as a span that must not become a pushout

R5 computes **resonance** between the authored theme-centroids and a `curated` graph's centroids
(dreaming on a book), *without merging the graphs* (the firewall: $\textsf{curated}\notin\mathsf{MR}$).
Categorically, resonance is a **span** $A\xleftarrow{}R\xrightarrow{}C$ (authored $\leftarrow$
resonance object $\rightarrow$ curated) whose apex $R$ records cosine correspondences. The firewall is
the requirement that this span is **never completed to a pushout** $A\sqcup_R C$ — the pushout would
be the merged graph, which is exactly forbidden. The resonance output is $\textsf{interpreted}$-only
and mutates neither $A$ nor $C$. **[Engineering].** Again: a precise name for an existing boundary.

## 8.3 Declined

Sheaf **cohomology** as base machinery (§5.2 keeps only the finite-dimensional consistency energy),
higher category theory, and monoidal/enriched structure: **REJECT** as base machinery. None passes
filter clause (a) — they would decorate, not constrain. If a class structure that genuinely needs an
ordering ever appears (it does not today), revisit — the whitepaper's own deferral (G8) stands.


---

# Part VIII — Implementation

**Principle:** *everything adopted is a deterministic NumPy/SciPy computation over the existing
polyglot stores; the model is earned only for narration.* No new database, no graph engine — the
zero-network, local-only constraint holds.

## 9.1 Where each adopted structure lives

| Structure (§) | Store / module | Computation | Incremental update |
|---|---|---|---|
| B-hypergraph incidence (§2) | SQLite `DerivedStore` junction table | indexed lookup $O(\log|V|+|T|)$ | append-only; one additive migration |
| Diffusion map / spectral cluster (§3.2, §6.2) | LanceDB vectors → SciPy sparse | partial eigensolve `scipy.sparse.linalg.eigsh`, top-$r$ | recompute on trough; cache eigenbasis, patch on small $\Delta$ |
| Grounded attention walk (§4.2) | derived from $A$, $g$ | sparse mat-vec power iteration for $\phi$ | $\phi$ warm-started from prior pass |
| Heat kernel / label prop (§4.3, §6.3) | $L$ from graph | $e^{-tL}s$ via `expm_multiply` (no dense $e^{-tL}$) | per-seed, on demand |
| Persistence, confidence filtration (§5.1) | graph → `ripser`/`gudhi` | $O(m^{\,\omega})$ worst-case, sparse in practice | recompute on trough; diagrams cached |
| Min-cut / conductance (§6.4) | graph → max-flow / `eigsh` for $\lambda_2$ | push–relabel; Fiedler vector | per-community, on trough |
| Confidence clamp (§7.2) | `core/recursion.py` + adjudicator | reverse-topological sweep, $O(|\mathcal{E}|)$ | per-insert |

**Scale reality.** At $\sim10^3$ nodes and $\sim10^3$–$10^4$ edges, every operation above is
sub-second on the M2 Max; the eigensolves dominate and are still milliseconds for the top-$r$ modes.
The system remains **inference-bound**, not linear-algebra-bound (the draft's one correct
engineering judgment). Guardrail: cap dense operations — never materialize $e^{-tL}$ or a full
$|V|\times|V|$ kernel; use `expm_multiply` and partial eigensolves throughout.

## 9.2 The single adapter seam

All of the above sits behind the existing `DreamerAdapter` protocol (F9) so the real system stays
decoupled from the math: the geometry/spectral layer exposes `cluster()`, `diffusion_map()`,
`grounding_cut(S)`, `conductance(S)`, `persistence()` as pure functions of a `MirrorView` and the
`DerivedStore`. The adapter is the one place speculative surface is allowed; the live path calls only
the ADOPTED subset. This preserves the "isolate speculative surface behind one protocol" discipline
already in the test harness.

## 9.3 Rollout order (mirrors the roadmap, respects the filter)

1. **Now (ADOPT):** spectral/diffusion clusterer replacing lexical single-linkage (§3.2/§6.2);
   the confidence clamp (§7.2); grounded attention weighting (§4.2).
2. **Track A2 (ADOPT):** min-cut/conductance alignment detector (§6.4) as a structural drift axis.
3. **Utility axis (ADOPT):** confidence-filtration persistence (§5.1) as a gap-surfacing prompt.
4. **DEFER→R3:** hyperbolic/product geometry (§3.3), *gated on median derivation depth > 2 and the
   $b\gamma<1$ criterion (§4.5)*.
5. **DEFER / [Speculative]:** sheaf consistency (§5.2), general multi-head hyperedges (§2.3).

Nothing in steps 4–5 ships until its trigger fires. That is the filter, operationalized.

---

# Part IX — Validation

**Principle:** *engineering rigor governs how outputs are produced; it does not certify they are
insightful. New math adds new obligations — and one honest, permanent gap.* The value question is
closed only by the F9 suite's empirical signal, never by the mathematics alone.

## 10.1 The obligations the new math introduces

Each adopted structure ships with property/metamorphic tests (Hypothesis), extending the existing
`tests/quality/` and `tests/property/` suites:

- **Diffusion determinism** (§3.2): fixed seed ⇒ identical diffusion map (bit-stable within float tol).
- **Spectral stability** (§6.2): a $\sigma$-perturbation bounded by $\delta$ moves cluster
  assignments by $\le$ a blessed Hamming tolerance (else the clusterer is chaotic and unusable).
- **Persistence stability** (§5.1): by the bottleneck-distance stability theorem, a bounded change to
  $g$ yields a bounded change to the persistence diagram — assert bottleneck distance $\le$ the input
  perturbation. **[Theorem]** (Cohen-Steiner et al.); a failure means a filtration bug.
- **Grounding-cut monotonicity** (§6.4): adding an authored support edge to $S$ never lowers
  $\operatorname{cut}(S,V_{\mathrm{auth}})$ — a metamorphic invariant catching sign errors.
- **Decay monotonicity** (§7.2): $c$ is non-increasing in $d$ for fixed $(g,|\mathrm{Agr}|)$;
  $c\in[0,1]$ always. (Extends the existing `test_drift_property` / `test_recursion` families.)
- **$b\gamma<1$ admission** (§4.5): the R3 enable-path refuses a configuration whose
  (measured branching × $\gamma$) $\ge 1$ — a fail-closed guard, not a warning.

## 10.2 Reuse the F9 value-floor (do not reinvent it)

The signal-vs-noise obligations already exist and bind to the live Dreamer: pure-noise apophenia
guard, planted-signal recovery, confidence calibration, **grounding faithfulness via full-support
ablation** (remove the *entire* cited support set, not one citation — the correct falsification for
large clusters), paraphrase invariance, dominant-note poisoning resistance, and the TF-IDF
negative-control baseline. The new geometry must **not regress** these: the spectral clusterer's
planted-signal recall must be $\ge$ the current lexical clusterer's, and its noise max-confidence must
stay $\le$ the calibrated ceiling. Wire the new clusterer through the existing
`MindPalaceDreamerAdapter` and run `tests/quality/` against both — a green run is a non-regression
proof, not a value proof.

## 10.3 Longitudinal (Track F4) and drift (Track A)

The drift gauge (A1, `eval/drift.py`) already measures $D(t)=d(\mu(s_t),B)$ against a frozen anchor.
Two extensions land here: (i) **A2** appends the §6.4 structural axes (conductance, grounding-cut) to
$\mu$ as additive `Axis` entries — healthy structure = 0 drift, a drifting bubble = positive
deterioration; (ii) **F4** calibrates every threshold in this document ($\Phi^\star,\eta,r,\Theta$,
and the $b$ estimate) on **observed longitudinal curves**, then re-blesses them as frozen fixed
points. Until F4 runs, all thresholds here are **declared with bounds, not magic numbers** (per G7)
and marked calibration-pending.

## 10.4 The honest, permanent gap

No amount of spectral or topological machinery answers *"is this dream actually insightful to the
author?"* — the geometry certifies that a cluster is real, robust, and grounded; it cannot certify it
is *useful*. That question is **subjective** and closes only against the author's blind ratings (the
F9 `rate_blind` hook, deliberately left unwired so a green CI run cannot masquerade as a proven value
claim). This document deliberately does **not** paper over that gap. The utility axis $u$ stays
separate from confidence $c$ (I11) for exactly this reason: the math can make the mirror *honest and
robust*; only the author can make it *useful*.

---

## Appendix A — The adopt / defer / reject ledger

| Structure | §  | Status | Disposition | One-line reason |
|---|---|---|---|---|
| Directed B-hypergraph (single-head) | 2 | [Engineering] | **ADOPT** | already the `derived_from` structure; formalize |
| General multi-head hyperedges | 2.3 | [Engineering] | **DEFER** | no current op mints co-derived heads |
| Simplicial complexes | 2.2 | [Theorem] | **REJECT** | reasoning isn't downward-closed |
| Semantic base $\mathbb{R}^n$ | 3.1 | [Engineering] | **ADOPT** | status quo |
| Diffusion distance / map | 3.2 | [Theorem] | **ADOPT** | deterministic context floor; cheap |
| Hyperbolic / product manifold | 3.3 | [Theorem] | **DEFER→R3** | no deep tree exists today; not an epistemic certifier |
| Information / Fisher geometry | 3.4 | [Engineering] | **REJECT** | duplicates $g$; $O(n^2)$/atom; re-entangles belief |
| Dreamer rewrite operator | 4.1 | [Engineering] | **ADOPT** | matches built pipeline |
| Grounded attention walk | 4.2 | [Engineering] | **ADOPT** | one-line reweight; subsumes centrality |
| Heat-kernel label propagation | 4.3 | [Engineering] | **ADOPT** | cheap smoother |
| Reaction–diffusion nonlinearity | 4.3 | [Speculative] | **REJECT** | undefined quantity; decoration |
| $b\gamma<1$ stability criterion | 4.5 | [Theorem] | **ADOPT** | checkable R3 admission guard |
| Persistence, confidence filtration | 5.1 | [Engineering] | **ADOPT** | gap-surfacing on the utility axis |
| $\beta_1$ = contradiction | 5.1 | — | **REJECT** | wrong: holes ≠ contradictions |
| Sheaf consistency | 5.2 | [Speculative] | **DEFER** | validation-only future lens |
| Graph Laplacians / spectral cluster | 6.1–2 | [Theorem] | **ADOPT** | principled clusterer |
| Graph Fourier smoothness $s^\top L s$ | 6.3 | [Engineering] | **ADOPT-LITE** | one quadratic form as coherence score |
| Tensor decompositions | 6.3 | [Engineering] | **REJECT** | no multi-relational learning task |
| Min-cut-to-authored + conductance | 6.4 | [Theorem] | **ADOPT (A2)** | *this is* the alignment detector |
| Confidence clamp (canonical $c$) | 7.2 | [Engineering] | **ADOPT** | reconciles the whitepaper's own tension |
| Bayesian / loopy BP / evidence fusion | 7.3–4 | [Engineering] | **REJECT** | DAG makes it needless; manufactures false posteriors |
| Provenance functor / firewall diagram | 8.1 | [Engineering] | **ADOPT (naming)** | precise restatement, no new compute |
| Resonance span (not pushout) | 8.2 | [Engineering] | **ADOPT (naming)** | precise "resonance without merge" |
| Higher category theory / sheaf cohomology | 8.3 | — | **REJECT** | decorates, doesn't constrain (G8) |

## Appendix B — Notation reconciliation (draft ↔ companions ↔ this doc)

| Concept | Draft (Gemini) | Companions I–II | This document |
|---|---|---|---|
| corpus nodes | $\mathcal{K}$ | $V$ | $V$ (atoms $\equiv \mathcal{K}$) |
| embedding | $f:\mathcal{K}\to\mathbb{R}^n$ | $e:V\to\mathbb{R}^{2560}$ | $e$, $n=2560$ |
| provenance set | $P$ (**ordered** — wrong) | $P$ (unordered) | $P$ (unordered; only $\mathsf{MR}$ bites) |
| mirror-readable | $\mathcal{K}_{auth}$ | $\mathsf{MR}$, $\pi_{\mathsf{MR}}$ | $\mathsf{MR}$, $\pi_{\mathsf{MR}}$ |
| hypergraph | $\mathcal{H}_{strat}$ | (implicit `derived_from`) | $\mathcal{H}=(V,\mathcal{E},\tau,\rho)$ |
| Dreamer operator | $\mathcal{D}$ | — | $\mathcal{D}=\omega\circ\sigma\circ S$ |
| transition matrix | $P$ (**collision**) | — | $\mathbf{T}$ |
| incidence matrix | $M$ | — | $\mathbf{B}$ |
| grounding / conf / util / depth | $c$ (conflated) | $g,c,u,d$ | $g,c,u,d$ (kept distinct, I11) |
| decay | $c(b)\le\gamma^d c(a)$ (**wrong**) | $c\le\gamma^d g$ | clamp: $c=\min\{1,\gamma^d g(1+\lambda(|\mathrm{Agr}|-1))\}$ |
| degree matrix | $D$ (**collides w/ Dreamer**) | $D$ | $D=\operatorname{diag}(A\mathbf{1})$; Dreamer is $\mathcal{D}$ |

## Appendix C — Open items for the next session

1. Propagate the F9 refined grounding $g=\text{grounding}\cdot\text{cohesion}\cdot\text{size\_factor}$
   into live `core/dreaming/adjudicator.py` and make the §7.2 clamp the single definition of $c$
   (runbook Hook 2). *(specification-precision fix; no behavior change while R&D flag-OFF)*
2. Prototype the §6.4 min-cut/conductance detector as an additive `Axis` in `eval/drift.py` (A2),
   with the two property tests in §10.1. *(highest-value new capability)*
3. Replace the lexical single-linkage clusterer with the §3.2/§6.2 diffusion/spectral clusterer
   behind the `DreamerAdapter`; run `tests/quality/` for non-regression against the lexical baseline.
4. Write the R3 enable-guard implementing the $b\gamma<1$ admission check (§4.5) — fail-closed.
5. Chapters remaining to draft at this rigor if desired: a worked **complexity appendix** (per-op
   FLOP/byte budgets on the real corpus) and a **metamorphic-test catalog** (the full generator set).

---

*End of companion III (draft 0.1). This document is authoritative for the Dreamer's mathematics;
where it and the draft chapters disagree, this document and the §0.1 errata govern. It changes no
running behavior: the dream R&D flag stays OFF, and every ADOPT item ships behind the existing
adapter seam and the trough-only gate.*
