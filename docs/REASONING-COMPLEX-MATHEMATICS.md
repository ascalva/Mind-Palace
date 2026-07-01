# The Reasoning Complex — Mathematical Framework for the Dreamer
### Formal companion III (v0.2) · supersedes the `WHITEPAPER-DREAMER-MATHEMATICS.md` 0.1 draft

**2026-06-30 · living document**

> *Notation: every load-bearing symbol (ρ, π_MR, 𝒜, D(t), 𝔎, K_σ, ℋ, δ\*δ, …) is defined once in [`NOTATION.md`](NOTATION.md) — symbol ↔ code ↔ object ↔ family (companion IV §A). This document is family 5.*

This document establishes the mathematical substrate for the Dreamer subsystem — the system's
reasoning engine. It extends the existing architecture (companions I–II); every invariant holds:
the provenance firewall, object-capability, mirror-not-oracle, regenerability, the
authored/curated/observed/interpreted separation.

**Why this exists (the honest framing).** The Dreamer today clusters the authored mirror and
synthesizes a grounded summary per theme. That is a competent retrieval loop; it is not yet a
reasoning engine. It does not discover non-obvious structure, surface the tensions the author is
carrying, track how understanding evolves, or build a model that deepens as the corpus grows.
**The dreaming mechanism is the weak spot of the system as a whole** — and it is the precondition
for everything downstream. Hands act on the Dreamer's model; a shallow model yields shallow action.
The purpose of this framework is to give the Dreamer the structural vocabulary that reasoning
requires. It cannot make a dream *insightful* — that is validated by the author and ultimately
proven when the hands act well — but it makes the Dreamer *equipped*: reasoning over curvature,
balance, homology, and evolution rather than over cosine clusters.

Notation follows companion II. Status tags: **[Theorem]** (provable), **[Engineering]** (design
choice, true by construction), **[Conjecture]** (plausible, testable), **[Speculative]** (future).
Disposition tags: **ADOPT** / **DEFER→X** / **REJECT**. The minimalism filter (companion III 0.1
§0) still governs — but the object below is now understood correctly, which changes several
verdicts from the 0.1 draft. §0.2 records those reversals.

---

## 0.1 The unifying thesis

The 0.1 draft treated the mathematics as a scattered menu and adopted conservatively. Held to a
sharper lens, the promising structures are not a menu — they are **one object seen from several
sides**. The unifying object is:

> **A generalized Laplacian on a multilayer, typed, temporal knowledge complex.**

Watch how much collapses onto that single operator:

| Instrument | Is really… |
|---|---|
| spectral clustering, diffusion, heat flow | the **ordinary** graph Laplacian $L$ |
| contradiction / dissonance at scale | the **signed** Laplacian $\bar L$ |
| inconsistency along a reasoning chain | the **sheaf / connection** Laplacian $L_{\mathcal F}$ (holonomy) |
| joint entailment | the **hypergraph** Laplacian $L_{\mathcal H}$ |
| structural holes / bridges | negative **Ollivier–Ricci curvature** (dual to $L$'s diffusion) |
| conceptual holes / robust domains | **persistent homology** ($\beta_0=\dim\ker L$ across scales) |
| how many themes, with confidence | **stochastic block model** posterior over the same graph |

The framework the project has been reaching for is real. Its unifying object is a **shared
operator**, not a shared embedding. That distinction is the whole game: a shared operator is a
*container* onto which typed, signed, higher-order, and temporal structure bolt **without loss**; a
shared embedding is a *lossy projection* that forces one distance on things that do not share one.
This is why the 0.1 draft was right to reject the "everything embeds in one product manifold"
ambition and right to keep the tools — but wrong about *why* they cohere. They cohere because they
are all $\delta^{\!*}\delta$ for an appropriate coboundary $\delta$ (§2.1). And crucially, unlike
the manifold version, this object is **computable, offline, deterministically** on the real corpus.

## 0.2 Reversals from the 0.1 draft

Four dispositions change because the object is now understood correctly. Recorded so the evolution
is auditable.

| Item | 0.1 verdict | v0.2 verdict | Reason for the change |
|---|---|---|---|
| Simplicial complexes | REJECT | **ADOPT (similarity-simplices)** | I rejected *derivation*-simplices (correctly — reasoning isn't downward-closed). But *similarity*-simplices (the flag complex of the cosine graph) **are** downward-closed by construction, and are the substrate the adopted persistence already runs over. I was computing persistence without naming its object. (§4.1) |
| Curvature / geodesics | not offered | **ADOPT (Forman now, Ollivier optional)** | Ollivier–Ricci is negative on bridges — the R0 `bridge` interpreter with a principled continuous measure — and *is* intrinsic hyperbolicity, doing the job I deferred to R3 without any embedding. (§3) |
| Signed / fiber-bundle edge | typed edge + deferred judge (weak) | **ADOPT (signed Laplacian)** | The right instrument for contradiction is the *signed* graph the support/contradict component already implies: Harary balance, the frustration index, and $\lambda_{\min}(\bar L)=0\iff$ balanced. Rigorous, computable, the tractable instance of the fiber-bundle view. (§2.3) |
| Bayesian graph inference | REJECT | **ADOPT (over structure, not truth)** | "Trivial on a DAG" is a reason to do it *properly*, not to avoid it: exact message-passing combines multi-path support; the SBM gives clustering *with uncertainty and model selection*. The line held: Bayesian over **structure** yes, over an interpretation's **truth** no. (§6) |

The tensor and full-fiber-bundle deferrals stand, with their blockers named honestly (§8).

---

# Part 1 — The knowledge complex (the object)

**Principle:** *the Dreamer reasons over a multilayer, typed, temporal complex built from the
corpus; it never computes on ingest, and ingest never computes on it.* The complex is derived,
regenerable, and interpreted-only where it is written to.

## 1.1 Layers: provenance strata as a multilayer network

The corpus is not one graph; it is a **multilayer network** whose layers are the provenance
classes. Let $\mathfrak{L}=\{\textsf{auth-solo},\textsf{auth-dlg},\textsf{curated},\textsf{observed},\textsf{interpreted}\}$.
Each node lives in exactly one layer ($\rho(v)$). Edges are **intra-layer** or **inter-layer**, and
the firewall is precisely a **constraint on which inter-layer edges may exist**:

$$\text{permitted inter-layer edges}\ =\ \big\{(u,v):\rho(u)\in\mathsf{MR}\ \Rightarrow\ \text{introspective reads only cross within }\mathsf{MR}\big\},\quad \mathsf{MR}=\{\textsf{auth-solo},\textsf{auth-dlg}\}.$$

Concretely: the introspective Dreamer operates on the **sub-complex induced by $\mathsf{MR}$**
(the `MirrorView`, structural). Cross-layer resonance (curated↔authored, R5) is a controlled
inter-layer map that **records** correspondence without **merging** layers (§5.2, §7 of companion
III 0.1). The observed layer connects only to the assistant tier, never to $\mathsf{MR}$. **[Engineering].**

```
        LAYERS (provenance strata)                 the firewall = which inter-layer edges may exist
   ┌───────────────────────────────┐
   │ interpreted   ● ● ● ● ●        │  ← Dreamer writes here ONLY (append-only, ρ≡interpreted)
   ├───────────────────────────────┤     derives-edges DOWN to authored leaves (acyclic)
   │ observed      ○ ○ ○            │  ← assistant tier only; NO edge into MR
   ├───────────────────────────────┤
   │ curated       ◇ ◇ ◇            │  ← resonance map to authored (records, never merges)
   ├───────────────────────────────┤
   │ auth-dialogue ▲ ▲ ▲   ┐        │
   │ auth-solo     ■ ■ ■ ■  ├ = MR  │  ← the introspective sub-complex (MirrorView)
   └───────────────────────────────┘  ┘
```

## 1.2 The typed edge as a fiber (the connection view)

This is the structure the project's intuition named a "fiber bundle over a graph," and it is
correct. An edge is not a scalar weight; it carries a **tuple of components** — a fiber over the
edge:

$$\varepsilon(u,v)\ =\ \big(\ \underbrace{t}_{\text{time}},\ \underbrace{w\in\mathbb{R}_{\ge0}}_{\text{strength}},\ \underbrace{s\in\{+1,-1\}}_{\text{polarity: support / contradict}},\ \underbrace{\tau\in\mathcal{T}}_{\text{relation type}}\ \big).$$

The polarity component $s$ is what makes the graph a **signed graph**; the strength $w$ is the
metric weight; $\tau\in\{\textsf{derives},\textsf{supports},\textsf{contradicts},\textsf{contextualizes},\textsf{similar}\}$
types it; $t$ timestamps it. The full "fiber-bundle" reading assigns to each edge a **transport map**
(a restriction map, §2.4) that says how meaning on one endpoint maps to the other; the signed case
is the one-dimensional, $\pm1$-transport instance — the tractable one we build now. The general case
is a research problem with a named blocker (§8). **[Engineering]** (the components), **[Speculative]**
(rich transport).

## 1.3 Higher-order structure: two complexes for two relations

There are **two distinct** higher-order structures, and conflating them was an error the project's
list correctly separates:

- **The similarity complex** $K_\sigma$ — the **flag (clique) complex** of the cosine graph: a set
  of $k$ notes that are *pairwise* similar (all $\binom{k}{2}$ edges present at threshold $\sigma$)
  fills in as a $(k{-}1)$-simplex. This complex is **downward-closed by construction** (every face
  of a present simplex is present), which is exactly why the simplicial-complex rejection of the
  0.1 draft was aimed at the wrong object. $K_\sigma$ is the substrate for persistence (§4). A
  *filled* triangle is three notes in mutual coherence (a genuine 2-D theme); an *empty* triangle
  (three pairwise edges, no fill) is a **conceptual hole**. **[Engineering].**

- **The derivation hypergraph** $\mathcal{H}$ — directed **B-arcs**, tail set $T(e)=\operatorname{supp}(\kappa)$
  → single head $\kappa$ (the existing `derived_from`, §2 of companion III 0.1). This carries
  **joint entailment** and is **not** downward-closed (a synthesis from three premises does not
  imply a coherent synthesis from any two). It is acyclic on $\textsf{derives}$ (A3). **[Engineering].**

> **The two must not be confused.** $K_\sigma$ is undirected, downward-closed, and about
> *coherence*; $\mathcal{H}$ is directed, non-closed, and about *entailment*. Different math applies
> to each. This is the single most important structural distinction in the framework.

## 1.4 Temporal indexing

Every node and edge carries a creation time $t$; the corpus is a **filtration in wall-clock time**
$G(\tau_0)\subseteq G(\tau_1)\subseteq\cdots$ (authored is append-only; interpreted grows). This is
distinct from the *diffusion-scale* time $t$ in $e^{-tL}$ (§5.1) — one is the dynamics, the other is
a multiscale analysis knob on a snapshot. Keeping them distinct is essential (§5.1). **[Engineering].**

## 1.5 Formal definition

**Definition 1.1 (The reasoning complex).**
$$\mathfrak{K}\ =\ \big(\,V,\ \varepsilon,\ K_\sigma,\ \mathcal{H},\ \rho,\ t\,\big)$$
where $V$ are atoms; $\varepsilon$ assigns each edge its fiber $(t,w,s,\tau)$; $K_\sigma$ is the
similarity flag complex; $\mathcal{H}$ the derivation B-hypergraph; $\rho:V\to\mathfrak{L}$ the layer
(provenance) map; $t$ the temporal index. The introspective Dreamer sees $\mathfrak{K}|_{\mathsf{MR}}$
(the induced sub-complex on mirror-readable layers). $\mathfrak{K}$ is derived from and regenerable
from the raw store; the Dreamer writes only $\textsf{interpreted}$ nodes/edges into it. **[Engineering].**

---

# Part 2 — The generalized Laplacian family (the operator)

**Principle:** *one operator, several structures.* Every reasoning primitive below is a quadratic
form $x^{\!\top}\!Lx = \|\delta x\|^2$ for a coboundary $\delta$ matched to the structure. This is
the mathematical heart of the framework.

## 2.1 The coboundary construction that unifies them

Fix an orientation of edges. A **0-cochain** $x$ assigns a value (scalar or vector) to each vertex;
the **coboundary** $\delta$ maps it to a 1-cochain on edges. The Laplacian is $L=\delta^{\!*}\delta$
(PSD by construction), and its **Dirichlet energy** $x^{\!\top}Lx=\|\delta x\|^2$ measures how much
$x$ *disagrees across edges*. The four Laplacians differ only in **what $\delta$ does on an edge**:

| Laplacian | stalk (per node) | $(\delta x)_{e=(u,v)}$ | energy $x^{\!\top}Lx$ | reads |
|---|---|---|---|---|
| ordinary $L$ | $\mathbb{R}$ | $x_u-x_v$ | $\sum_e w_e(x_u-x_v)^2$ | smoothness / clusters |
| signed $\bar L$ | $\mathbb{R}$ | $x_u-s_e x_v$ | $\sum_e w_e(x_u-s_e x_v)^2$ | balance / frustration |
| sheaf $L_{\mathcal F}$ | $\mathbb{R}^{d_v}$ | $F_{u\lhd e}x_u-F_{v\lhd e}x_v$ | $\sum_e\|F_{u\lhd e}x_u-F_{v\lhd e}x_v\|^2$ | consistency / holonomy |
| hypergraph $L_{\mathcal H}$ | $\mathbb{R}$ | clique/star of edge $e$ | (Zhou normalized form) | joint entailment |

$L$ is the trivial-transport sheaf ($F=\mathrm{id}$); $\bar L$ is the $\pm1$-transport sheaf; both
are special cases of $L_{\mathcal F}$. **[Theorem]** (Hansen–Ghrist spectral sheaf theory). This
single fact is why the framework is coherent rather than a pile of tools.

## 2.2 The ordinary Laplacian: diffusion, clusters, Fourier

$L=D-A$, $L_{\mathrm{sym}}=I-D^{-1/2}AD^{-1/2}$. Standard facts, all used by the Dreamer:
$\dim\ker L=$ #components; the **Fiedler value** $\lambda_2$ is algebraic connectivity; eigenvectors
are the **graph Fourier basis**; a signal's smoothness is $s^{\!\top}Ls$; the **heat kernel**
$e^{-tL}$ diffuses/smooths; **spectral clustering** partitions by the bottom eigenvectors. **[Theorem].**

*Dreamer use.* Spectral/diffusion clustering replaces the ad-hoc cosine single-linkage as the
deterministic clustering floor (this dissolves the chaining that forced $\sigma=0.50$ in F9);
$s^{\!\top}Ls$ scores whether a proposed theme label sits *smoothly* over its cluster or is
scattered. **ADOPT.**

## 2.3 The signed Laplacian: contradiction at scale (ADOPT)

**Intuition.** The author holds tensions — "I love this work" beside "I have to leave." Cosine puts
these *close* (shared topic); the graph must carry the *disagreement*, and it does, in the polarity
component $s$. A signed graph is **balanced** when its nodes can be 2-colored so every $+$ edge is
within a color and every $-$ edge crosses — i.e., the tensions resolve into two coherent camps. When
they *can't*, there is **frustration**: irreducible dissonance.

**Rigorous.** Signed adjacency $A$ (entries $\pm w$), absolute degree $\bar D_{ii}=\sum_j|A_{ij}|$,
**signed Laplacian** $\bar L=\bar D-A$. Then
$$x^{\!\top}\bar L x\ =\ \sum_{+\text{edges}}w_e(x_u-x_v)^2\ +\ \sum_{-\text{edges}}w_e(x_u+x_v)^2\ \ge\ 0,$$
and $\bar L$ is **singular iff the signed graph is balanced**: $\lambda_{\min}(\bar L)=0\iff$ balanced.
**[Theorem]** (Hou; Kunegis). The **frustration index** $\mathrm{fr}(G)=$ minimum number (or weight)
of edges whose deletion makes $G$ balanced quantifies total dissonance; it is **NP-hard** exactly,
but (i) $\lambda_{\min}(\bar L)$ is a cheap spectral lower-bound proxy, and (ii) **local frustration**
— counting unbalanced triangles (a triangle is frustrated iff it has an odd number of $-$ edges) — is
$O(\#\triangle)$ and directly localizes *which* tensions don't resolve. **[Theorem].**

**Dreamer use.** The signed Laplacian's smallest eigenvector partitions the author's thinking into
the two nearest-coherent camps; the residual $\lambda_{\min}$ is a global dissonance score; frustrated
triangles are **the specific unresolved tensions to surface** ("these three commitments can't all
hold — you keep circling this"). This is contradiction-detection done rigorously, replacing the 0.1
draft's deferred judge seam. **ADOPT.** *(The signed graph is also the simplest cellular sheaf, §2.4 —
so this is the buildable instance of the fiber-bundle view.)*

```
   balanced (frustration 0):            frustrated triangle (odd # of − edges):
        +                                        +
     A ─── B                                  A ─── B
     │      │        two clean camps           │      ╲ −         no 2-coloring works:
   − │      │ −      {A,B} vs {C,D}          + │       ╲          irreducible tension
     │      │                                  │        ╲
     D ─── C                                   C ────────┘
        +                                          −
```

## 2.4 The sheaf / connection Laplacian: inconsistency along a chain (the fiber bundle)

**Intuition.** A concept can mean subtly different things in different notes. Transport the meaning
along a chain of edges and back around a loop; if you don't return to where you started, the loop has
accumulated **inconsistency** — the discrete analogue of curvature/holonomy in a fiber bundle. This
is the project's fiber-bundle-over-a-graph, in full.

**Rigorous.** A **cellular sheaf** $\mathcal{F}$ on $G$: a stalk $\mathcal{F}(v)$ per vertex, edge
stalk $\mathcal{F}(e)$, **restriction maps** $F_{v\lhd e}:\mathcal{F}(v)\to\mathcal{F}(e)$. Coboundary
$(\delta x)_e=F_{u\lhd e}x_u-F_{v\lhd e}x_v$; **sheaf Laplacian** $L_{\mathcal F}=\delta^{\!*}\delta$.
Global sections (globally consistent assignments) $=\ker L_{\mathcal F}$; the Dirichlet energy
$x^{\!\top}L_{\mathcal F}x$ measures failure to glue. Around a cycle, the composite of restriction maps
is the **holonomy**; nontrivial holonomy = inconsistency. **[Theorem]** (Hansen–Ghrist).

**The honest blocker (why this is DEFER, not ADOPT beyond the signed case).** The power is real, but
it requires *defining the restriction maps* $F_{v\lhd e}$ — the transport of meaning across an edge.
If they are taken as cosine projections, $L_{\mathcal F}$ **collapses to the weighted graph Laplacian**
and you have bought vocabulary, not computation. The $\pm1$ (signed) case works because $\pm1$ is a
*meaningful* transport (agree/oppose). Anything richer must be *defined* and *justified* for this
corpus, which is unsolved. **DEFER→(research):** adopt the signed shadow now; treat rich transport as
an open problem with this exact blocker. **[Speculative]** beyond signed.

## 2.5 The hypergraph Laplacian: joint entailment

For $\mathcal{H}$ with incidence $\mathbf{B}$, edge weights $W$, degrees $D_v,D_e$:
$L_{\mathcal H}=I-D_v^{-1/2}\mathbf{B}W D_e^{-1}\mathbf{B}^{\!\top}D_v^{-1/2}$ (Zhou normalized,
clique-expansion). **Exact** on the undirected similarity backbone (those edges are already pairwise);
an **approximation** on the directed derivation structure (it discards tail→head direction), so we
use it **only** on the similarity backbone and handle derivation combinatorially (min-cut, §3.5 /
companion III 0.1 §6.4). **[Engineering] tradeoff.** **ADOPT (backbone only).**

## 2.6 The unification, in one picture

```
                         δ*δ  (coboundary → Laplacian)
                          │
   ┌──────────────┬───────┴────────┬──────────────────┐
   │              │                │                  │
 F = id        F = ±1        F = general           clique/star
   │              │                │                  │
   ▼              ▼                ▼                  ▼
 ordinary L    signed L̄       sheaf L_F         hypergraph L_H
 clusters/     balance/       holonomy/          joint
 diffusion     frustration    consistency        entailment
 (ADOPT)       (ADOPT)        (DEFER: maps)      (ADOPT: backbone)
```

Every reasoning primitive the Dreamer needs on *pairwise* structure is one choice of transport in
this family. **This is the framework's spine.** **[Theorem]** (the family), **[Engineering]** (the dispositions).


---

# Part 3 — Geometry & curvature

**Principle:** *curvature is the intrinsic, embedding-free way to find where the interesting
structure is.* It is the geometric dual of the Laplacian's diffusion behavior, and it answers the
question the Dreamer most wants answered: *where are the bridges — the surprising links across
otherwise-separate concerns?*

## 3.1 Ollivier–Ricci curvature: bridges are negatively curved (ADOPT, optional)

**Intuition.** Put a little probability mass on the neighbors of $x$ and of $y$. If the two
neighbor-clouds are easy to transport into each other (they overlap), the edge $xy$ sits *inside a
community* — positively curved. If moving one cloud to the other is expensive (they point into
different regions), $xy$ is a **bridge** spanning a structural hole — negatively curved. Bridges are
where cross-domain insight lives.

**Rigorous.** For edge $(x,y)$ with graph distance $d$ and lazy-random-walk measures $m_x,m_y$,
$$\kappa(x,y)\ =\ 1-\frac{W_1(m_x,m_y)}{d(x,y)},$$
where $W_1$ is the Wasserstein-1 (earth-mover) distance, solved by a small optimal-transport LP per
edge. $\kappa>0$: community interior; $\kappa\approx0$: flat; $\kappa<0$: bridge / tree-like /
structural hole. **[Theorem]** (Ollivier; Lin–Lu–Yau graph form). Cost: an LP per edge,
$O(\deg^3)$-ish — tractable on the sparse, $\sim10^3$-node corpus, but the heaviest instrument here.

*Dreamer use.* Rank edges by curvature; the **most negative** are the candidate cross-domain
connections a synthesis pass should look at first — a principled, continuous version of the R0
`bridge` interpreter (which uses the local clustering coefficient as a cheap proxy). **ADOPT as an
optional/enrichment interpreter** (gate the OT cost).

## 3.2 Forman–Ricci curvature: the cheap deterministic floor (ADOPT now)

Ollivier is principled but costs an LP per edge. **Forman–Ricci** is a purely *combinatorial*
curvature — computable from local degrees and triangle counts, no optimal transport:
$$\mathrm{Ric}_F(u,v)\ =\ 4-\deg(u)-\deg(v)+3\,|\triangle(u,v)|\quad(\text{augmented, unweighted form; variants exist}),$$
where $|\triangle(u,v)|$ is the number of triangles through the edge. It is **negative on bridges**
(low triangle support, high endpoint degree) and positive inside triangle-dense communities — the same
qualitative signal as Ollivier, at $O(\#\triangle)$ total. **[Theorem]** (Forman; Sreejith et al.).
**ADOPT now** as the deterministic-floor curvature; reserve Ollivier for enrichment where the OT cost
is affordable.

```
   community interior (κ > 0):            bridge / structural hole (κ < 0):
     ●───●                                   ●───●        ●───●
     │╲ ╱│   many triangles,                  ╲   │        │  ╱
     │ ╳ │   clouds overlap,                    ╲  │        │ ╱
     │╱ ╲│   easy transport                      ╲ │        │╱
     ●───●                                        ●──────────●
                                                    ↑ the surprising cross-domain link
                                                      the Dreamer wants to surface first
```

## 3.3 Ricci flow: how edges evolve (ADOPT for community surgery)

**Intuition.** Let the graph *relax* under its own curvature: stretch the negatively-curved bridges,
shrink the positively-curved community edges, iterate; then cut the stretched bridges. Communities
fall out as the connected components that remain. This directly answers *"how do the edges evolve?"* —
with a real dynamic, not a metaphor.

**Rigorous.** Discrete graph **Ricci flow**: $w_e^{(k+1)}\leftarrow(1-\kappa_e^{(k)})\,w_e^{(k)}$
(renormalized), iterated to convergence; edges whose weight has grown past a surgery threshold (the
bridges) are removed. Communities = remaining components. **[Theorem]/[Engineering]** (Ni–Lin–Gao–Luo,
"Community detection with Ricci flow"). This is a **community-detection dynamic** and a cross-check
against spectral/SBM clustering — where three methods agree, the theme is robust; where they diverge,
it is fragile (a signal in itself).

## 3.4 Negative curvature *is* hyperbolicity (retires the R3 embedding deferral)

The 0.1 draft deferred hyperbolic geometry to R3 (deep recursion) and worried about embeddings.
Curvature gives the same signal **intrinsically**: a negatively-curved graph *is* tree-like /
hyperbolic (Gromov $\delta$-hyperbolicity, CAT(0) comparison). So we get the "hierarchy is
exponential, bridges are hyperbolic" content **without committing to a Poincaré embedding and without
waiting on R3** — by measuring curvature on the graph we already have. **The embedding is now optional
visualization, not a prerequisite.** This is a genuine simplification the curvature view buys. **[Theorem].**

## 3.5 Diffusion distance & min-cut (carried from companion III 0.1, unchanged)

Diffusion distance $D_t(x,y)^2=\sum_z(p_t(x,z)-p_t(y,z))^2/\phi(z)=\sum_{\ell\ge1}\lambda_\ell^{2t}(\psi_\ell(x)-\psi_\ell(y))^2$
(Coifman–Lafon), and the **min-cut-to-authored / conductance** alignment detector
($\Phi(S)=w(\partial S)/\min(\mathrm{vol}\,S,\mathrm{vol}\,\bar S)$, Cheeger $\tfrac12\lambda_2\le\Phi\le\sqrt{2\lambda_2}$)
remain **ADOPT** exactly as in companion III 0.1 §3.2/§6.4. The alignment detector is the same
$\delta^{\!*}\delta$ operator restricted to the authored/interpreted cut — the spectral family again.

---

# Part 4 — Topology

**Principle:** *homology sees holes the spectrum cannot — but only when computed over the right
complex, and only interpreted as holes, never as contradictions.*

## 4.1 The flag complex (naming the substrate the 0.1 draft omitted)

Persistence needs a **simplicial complex**, and the right one is the **flag (clique) complex**
$K_\sigma$ of the similarity graph (§1.3): every $k$-clique of pairwise-$\sigma$-similar notes is a
$(k{-}1)$-simplex. Downward-closed by construction. This is what the 0.1 draft's persistence ran over
without naming; naming it fixes the earlier simplicial-complex confusion. **[Engineering].**

The **filled vs. empty** distinction carries a real signal: a *filled* triangle is three notes in
mutual coherence — a 2-D theme; an *empty* triangle (three edges, no fill) is a **conceptual hole**.
$H_0$ counts domains; $H_1$ counts holes. **[Theorem]** (standard).

```
   filled 2-simplex (a real theme):        empty triangle (a conceptual hole):
        A                                        A
       ╱█╲   all three mutually                 ╱ ╲     pairwise related,
      ╱███╲  coherent → one theme              ╱   ╲    no central note ties them →
     B─────C                                  B─────C   "you orbit this without stating it"
```

## 4.2 Persistent homology under a filtration (ADOPT, corrected interpretation)

Filter $K_\sigma$ by a threshold — either the **similarity scale** (Vietoris–Rips: sweep $\sigma$)
or the **confidence/grounding** level (companion III 0.1 §5.1). Track how $\beta_0,\beta_1$ are born
and die; the **lifetime** (persistence) separates robust structure from noise. The **bottleneck
stability theorem** guarantees persistence diagrams change no more than the input perturbation —
so this is a *stable* diagnostic. **[Theorem]** (Cohen-Steiner–Edelsbrunner–Harer).

- $\beta_0$ persistence → **robust intellectual domains** and the scale at which they merge.
- $H_1$ persistence → **conceptual holes** (long-lived empty cycles): themes circled but unfilled.

**What $H_1$ is NOT (the correction stands):** a 1-cycle is a topological hole, **not** a logical
contradiction (a signed/semantic property) and **not** circular reasoning (structurally impossible on
the acyclic $\textsf{derives}$-DAG). **Contradiction lives in the signed Laplacian (§2.3), not in
$H_1$.** Route dissonance through balance/frustration; route gaps through homology. **ADOPT** $H_1$
persistence as a **utility-axis** gap-surfacing prompt.

## 4.3 What topology sees that the spectrum does not

The spectrum is a *global average* (connectivity, cut quality); homology is a *precise count of
holes at every scale*. Two graphs can share a spectrum yet differ in $\beta_1$. For the Dreamer, this
is the difference between "there's a loosely-connected region" (spectral) and "there is exactly one
conceptual hole here, born at similarity 0.6, still open at 0.4" (persistent). The latter is a
*specific* prompt; the former is a vague one. That specificity is the value. **[Engineering].**

---

# Part 5 — Dynamics & evolution

**Principle:** *distinguish the two times.* The project's list rightly grouped "graph evolution, heat
equation, edges evolving, diffusion" — but these live on **two different clocks**, and conflating them
is precisely the reaction–diffusion error. Disentangling them is where the framework gains honesty.

## 5.1 The two time scales

- **Diffusion time $t$** in $e^{-tL}$: a **scale/resolution knob** for analyzing a *fixed snapshot*.
  Small $t$ = local neighborhoods; large $t$ = global structure. This is *multiscale analysis*, not
  the passage of time. The heat equation $\partial_t u=-Lu$ describes diffusion *at this scale*, on a
  *frozen* graph. **[Theorem].**
- **Wall-clock time $\tau$**: the graph itself changing as notes arrive and dreams accrue —
  $G(\tau_0)\subseteq G(\tau_1)\subseteq\cdots$. This is the **actual dynamics**. **[Engineering].**

**The reaction–diffusion PDE stays REJECTED** for the dynamics: the graph evolves by **discrete
events** (a note arrives; a dreaming pass mints interpreted nodes), not by a smooth flow. A continuous
PDE is the wrong discretization of $\tau$. But the *heat kernel at diffusion-scale $t$* is a perfectly
good **analysis** tool on each snapshot (label propagation, §2.2). Keep the smoother; reject the PDE
dynamics. This is the corrected version of the 0.1 draft's §4.3.

## 5.2 The Dreamer as graph rewriting (double-pushout) — with confluence for the panel

**Intuition.** A dreaming pass *rewrites* the complex: match a pattern (a cluster, a bridge, a
frustrated triangle), replace it with the pattern-plus-a-new-interpreted-node. Formalizing this as
**double-pushout (DPO) graph rewriting** — a rule is a span $L\leftarrow K\rightarrow R$ (pattern,
interface, replacement) — buys a concrete, valuable question the moment there is a **panel** of
interpreters: **do their rewrites commute?**

**Rigorous.** A DPO rewrite applies rule $L\leftarrow K\rightarrow R$ at a match $L\hookrightarrow G$
via two pushouts. When two rules' matches **overlap**, they form a **critical pair**; the rewriting
system is **locally confluent** if every critical pair can be joined (the order of application does not
change the result). **[Theorem]** (Ehrig et al., algebraic graph transformation). For the interpreter
panel this is exactly the well-posedness question: *if the community interpreter and the curvature
interpreter both fire on the same region, is the adjudicated result order-independent?* Critical-pair
analysis answers it. **ADOPT** as the formal model of the panel; **[Conjecture]** that the panel can be
made confluent by construction (the adjudicator orders by grounding, which is match-independent — a
plausible confluence argument to verify).

## 5.3 Edge-evolution laws (what actually changes on $\tau$)

Being precise about which edge components evolve and how:

| Component | Evolution law | Clock |
|---|---|---|
| strength $w$ (similarity) | static given embeddings; changes only on re-embed | discrete (re-embed event) |
| polarity $s$ | set at edge creation; never silently flips | discrete |
| confidence $c$ of a claim | $c=\min\{1,\gamma^{d}g(1+\lambda(|\mathrm{Agr}|-1))\}$ — decays with derivational depth $d$, **not** wall-clock | derivational |
| recency weight (optional) | an explicit $e^{-\lambda(\tau_{\text{now}}-t)}$ down-weighting of stale edges | wall-clock |
| Ricci-flow weight | an **analysis iteration**, not a stored evolution | analysis-time |

Most "evolution" is **discrete events + derivational decay**; the only genuinely continuous-in-$\tau$
law is an optional recency weighting. Stating this prevents the category error of treating confidence
decay or Ricci flow as wall-clock dynamics. **[Engineering].**

## 5.4 Tracking structure over time (feeds drift & the longitudinal harness)

The valuable *temporal* program is not a PDE but a **time series of structural invariants**: compute
$\lambda_2$, the curvature distribution, community structure, frustration $\lambda_{\min}(\bar L)$, and
the persistence diagram at each snapshot $G(\tau_k)$; watch how they move. This is exactly the input
the **drift gauge (A1)** and **longitudinal harness (F4)** want: a rising frustration, a bubble whose
conductance is falling, a domain fragmenting — each is a *measurable trajectory*, appended as an
additive `Axis` (A2). **ADOPT** as the temporal layer; it is the honest realization of "study the
evolution over time." **[Engineering].**


---

# Part 6 — Probabilistic inference (over structure, not truth)

**Principle:** *"trivial on a DAG" is a reason to do it properly, not to skip it — but Bayesian
inference belongs on the graph's **structure**, never on an interpretation's **truth**.* The prior
over "is this dream true?" does not honestly exist; the prior over "how is this graph organized?" does.

## 6.1 Message passing on the derivation DAG (exact multi-path support)

The current adjudicator combines interpreter agreement with an ad-hoc multiplier
$c_0=g(1+\lambda(|\mathrm{Agr}|-1))$. The principled upgrade: treat the **derivation DAG** as a
graphical model and combine support by **message passing**. When a claim $\kappa$ is supported through
several independent paths, the natural combination is a **noisy-OR**:
$$\Pr[\kappa\text{ supported}]\ =\ 1-\prod_{\text{paths }p}\big(1-s_p\big),$$
with $s_p$ the support strength along path $p$. On a **polytree** (singly-connected DAG) this is
**exact and linear**; the derivation structure is currently depth-1 (a polytree), so it is exact today,
and the bounded depth keeps it tractable as recursion deepens. **[Theorem]** (Pearl, BP on polytrees).
This replaces the multiplier with a defensible combination of multi-path evidence — and preserves the
"adjudication not voting" discipline, because noisy-OR of *grounding-weighted* paths still ranks on
evidence, not headcount.

## 6.2 The stochastic block model: clustering *with* uncertainty and model selection

**Intuition.** The spectral/diffusion clusterer gives a point partition and makes *you* pick the
number of themes $k$. A generative model does better: it says *how likely* each note belongs to each
theme, and *how many themes* the data actually support.

**Rigorous.** The **stochastic block model** posits latent block memberships $z_i$ and edge
probabilities $\theta_{z_i z_j}$:
$$\Pr[A\mid z,\theta]\ =\ \prod_{i<j}\theta_{z_i z_j}^{A_{ij}}(1-\theta_{z_i z_j})^{1-A_{ij}}.$$
Fit by variational EM or MCMC → a **posterior over block assignments** (theme membership *with
confidence*) and **model selection** for the number of blocks via the integrated complete likelihood
(ICL) / minimum description length. The **degree-corrected** SBM (Karrer–Newman) handles hubs so a
prolific topic does not swallow the graph. **[Theorem]/[Engineering].**

**Dreamer use.** "How many distinct concerns is the author actually holding, and how sure are we each
note belongs to each?" — answered with a posterior, not a guess. The SBM's block count is a
cross-check against spectral and Ricci-flow community counts; agreement = a robust theme, disagreement
= a fragile one. **ADOPT** (light implementation; the corpus scale makes MCMC/VEM cheap). *This is the
single biggest upgrade to the "how many themes" question, which the deterministic clusterer answers
only by fiat.*

## 6.3 The line held: structure yes, truth no

We **REJECT**: a Bayesian posterior over an interpretation's *truth* (no honest prior; re-entangles
belief with a manufactured number), loopy BP over the full graph (needless — the DAG is near-polytree),
and Fisher-information uncertainty per thought (duplicates $g$; $O(n^2)$/atom). Uncertainty stays the
triple $(g,d,|\mathrm{Agr}|)$ surfaced as such. **Calibration is empirical** (F9), never derived.
**[Engineering].** The distinction is the whole discipline: probabilistic machinery organizes the
*graph*; it never certifies a *thought*.

---

# Part 7 — The instruments in concert: what a strong Dreamer pass looks like

**Principle:** *the value is not any single instrument but the pass that uses them together.* Here is
the concrete difference between the weak Dreamer (cluster → summarize) and the strong one. Every
structural step is deterministic, offline, model-free; the model is earned exactly once, for narration.

```
   WEAK Dreamer (today):        cluster (cosine)  →  summarize each cluster (LLM)  →  grounding check  →  store
                                └─ one signal ─┘     └───── the only reasoning ─────┘

   STRONG Dreamer (this framework):

   1. BUILD      construct 𝔎|_MR : similarity flag complex K_σ + derivation hypergraph ℋ, typed/signed edges
   2. LOCATE     Forman–Ricci curvature → rank BRIDGES (negative κ)         ← where is the surprising link?
   3. THEME      SBM posterior + spectral/Ricci-flow → themes WITH counts    ← how many concerns, how sure?
                 (three methods cross-checked; disagreement = fragile theme)
   4. TENSION    signed Laplacian λ_min + frustrated triangles → DISSONANCE  ← which commitments can't co-hold?
   5. GAPS       persistent H₁ over K_σ → conceptual HOLES (long-lived)      ← what is circled but unstated?
   6. SUPPORT    noisy-OR message passing on ℋ → multi-path grounding        ← how well-supported, combining paths?
   7. ADJUDICATE rank candidates by c = min{1, γ^d · g · (1+λ(|Agr|−1))}     ← evidence-ordered, not voted
   8. SYNTHESIZE the ONE earned model call: narrate the top candidates,      ← mirror-not-oracle, cites authored
                 grounded in authored notes, over a MirrorView
   9. STORE      interpreted-only into DerivedStore (derives-edges to leaves, acyclic, attested)
  10. MEASURE    append structural drift axes (frustration↑, conductance↓, domain-split) to the A2 profile
```

The weak Dreamer has **one** thing to say per cluster (a summary). The strong Dreamer arrives at
synthesis already knowing *where the bridges are, how many concerns there are and how confident it is,
which tensions don't resolve, which themes are only orbited, and how well each candidate is supported
across paths* — and it has **measured how all of that is changing over time**. That is the difference
between summarizing and reasoning. The model is still the last, earned step; everything upstream is
rigorous, deterministic structure. **[Engineering].**

> **This section is the answer to "the dreaming mechanism still feels like a weak spot."** The weak
> spot is that the Dreamer reasons over one signal (cosine clusters). The framework gives it seven,
> unified by one operator family, all computable offline — and a temporal layer to watch itself. It
> does not make dreams insightful by theorem; it makes the Dreamer *equipped* to be, and gives the
> hands a deep model to eventually act on instead of a shallow one.

---

# Part 8 — Deferrals, with named blockers

Honesty about what is *not* adopted and *exactly why* — so nothing is re-proposed without clearing
its blocker.

| Item | Disposition | The specific blocker |
|---|---|---|
| Rich fiber-bundle transport (sheaf beyond ±1) | **DEFER→research** | The restriction maps $F_{v\lhd e}$ must be *defined and justified* for this corpus; cosine projection collapses $L_{\mathcal F}$ to the weighted graph Laplacian (§2.4). Signed (±1) is the meaningful tractable instance; adopt that now. |
| Tensor factorization (RESCAL/CP/Tucker over relation×node×node) | **DEFER→evidence** | A fitted, low-rank, non-convex model with a *chosen rank* — closer to the LLM's stochastic character than to the deterministic floor. Justified **only** if the typed+temporal edges become rich enough that per-relation-slice analysis *provably* misses cross-slice structure. Cannot be known until those edges exist and are populated. Build the typed temporal complex first; let the data decide the rank. |
| Hyperbolic/product **embedding** | **DEFER→R3 (now optional)** | Curvature (§3.4) supplies the hyperbolic *signal* intrinsically; the embedding is now optional visualization, not a prerequisite. Trigger unchanged: median derivation depth > 2. |
| Reaction–diffusion PDE dynamics | **REJECT** | Wrong discretization of wall-clock time — the graph evolves by discrete events (§5.1). The heat kernel survives as snapshot analysis. |
| Higher category theory / full 2-categorical rewriting tower | **REJECT** (keep DPO + confluence) | DPO rewriting + critical-pair analysis (§5.2) is the useful, buildable layer; the tower above it decorates. |
| Bayesian posterior over interpretation *truth* | **REJECT** | No honest prior; manufactures calibrated-looking numbers the evidence can't support (§6.3). |

---

## Appendix — The operator zoo & disposition ledger (v0.2)

| Structure | § | Operator / object | Status | Disposition |
|---|---|---|---|---|
| Multilayer complex (layers = provenance) | 1.1 | multiplex network + firewall constraint | [Engineering] | **ADOPT** |
| Typed/signed edge fiber $(t,w,s,\tau)$ | 1.2 | edge attribute vector | [Engineering] | **ADOPT** |
| Similarity flag complex $K_\sigma$ | 1.3,4.1 | clique complex (downward-closed) | [Engineering] | **ADOPT** |
| Derivation hypergraph $\mathcal{H}$ (B-arcs) | 1.3 | directed, non-closed, acyclic | [Engineering] | **ADOPT** |
| Ordinary Laplacian | 2.2 | $L=\delta^{\!*}\delta$, $F=\mathrm{id}$ | [Theorem] | **ADOPT** |
| Signed Laplacian (contradiction) | 2.3 | $\bar L$, $F=\pm1$; frustration | [Theorem] | **ADOPT** |
| Sheaf/connection Laplacian | 2.4 | $L_{\mathcal F}$, general $F$; holonomy | [Speculative] | **DEFER (maps)** |
| Hypergraph Laplacian | 2.5 | $L_{\mathcal H}$ (clique-exp.) | [Engineering] | **ADOPT (backbone)** |
| Ollivier–Ricci curvature | 3.1 | $1-W_1/d$ | [Theorem] | **ADOPT (optional)** |
| Forman–Ricci curvature | 3.2 | combinatorial | [Theorem] | **ADOPT (floor)** |
| Ricci flow (community surgery) | 3.3 | weight evolution + cut | [Theorem] | **ADOPT** |
| Curvature = intrinsic hyperbolicity | 3.4 | Gromov $\delta$ | [Theorem] | **ADOPT (retires R3 embed)** |
| Diffusion distance / map | 3.5 | Coifman–Lafon | [Theorem] | **ADOPT** |
| Min-cut-to-authored / conductance | 3.5 | Cheeger; max-flow | [Theorem] | **ADOPT (A2)** |
| Persistent homology on $K_\sigma$ | 4.2 | $\beta_0$ domains, $H_1$ holes | [Theorem] | **ADOPT (utility axis)** |
| DPO rewriting + confluence | 5.2 | critical pairs | [Theorem] | **ADOPT (panel model)** |
| Temporal structural trajectories | 5.4 | invariant time series | [Engineering] | **ADOPT (drift/F4)** |
| Noisy-OR message passing on DAG | 6.1 | polytree BP | [Theorem] | **ADOPT** |
| Stochastic block model | 6.2 | SBM posterior + ICL | [Theorem] | **ADOPT** |
| Rich fiber transport / tensors / hyp-embed / RD-PDE / 2-cat / truth-posterior | 8 | — | — | **DEFER / REJECT** (blockers named) |

*This framework is authoritative for the Dreamer's mathematics. It changes no running behavior:
every ADOPT ships behind the `DreamerAdapter` seam and the trough-only gate, dream R&D flag OFF. The
buildable realization is the companion document `REASONING-COMPLEX-BUILD.md`.*
