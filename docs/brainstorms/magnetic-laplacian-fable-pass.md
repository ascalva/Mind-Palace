# The magnetic Laplacian — the fable finalization pass (Q1–Q7)

> **Fable session capsule** (`claude-fable-5`, tier owner-verified in-session; 2026-07-14).
> Durable *working material* (a brainstorm), **not** a design note — nothing here flips a
> status, edits a ratified note, or blesses a transition. This is the fable warrant
> `docs/brainstorms/magnetic-laplacian.md` charters: rule the seven §3 questions on the
> magnetic (Hermitian) Laplacian `L^{(q)}` as the formalization of graph "direction."
>
> **Scope discipline.** Design reasoning only. `dn-edge-dynamics` and
> `dn-temporal-retrieval-algebra` are ratified/immutable and are cited, never edited.
> Owner-reserved calls are surfaced as explicit **OWNER DECISION** items. Every nontrivial
> claim is labeled `[ESTABLISHED: cite]` / `[DERIVED: from X]` / `[INFERENCE]` / `[ANALOGY]`.
> Established prior results (`dn-temporal-retrieval-algebra` §2.3 Results 1–5, A5, A7;
> the lane-B capsule A1–A8) are consumed, not re-derived.

---

## 0. Executive map (what this pass concludes)

- **Q1.** `L^{(q)}` always exists at degree 0 (Hermitian, PSD, `q=0` = v1 exactly). It lifts
  to a genuine **magnetic Hodge theory at degree 1 iff the connection is flat on every
  filled 2-cell** — and a **parity obstruction** kills that on the citation flag complex for
  *every* nontrivial charge (all-one-way triangles have odd circulation). On the covering
  (Hasse) supersession DAG the skeleton is triangle-free, so the magnetic Helmholtz
  decomposition exists there **vacuously** (gradient ⊕ harmonic, curl ≡ 0). The flux **is** a
  genuine curvature 2-form in the literal lattice-gauge sense (`F = dθ`), and `d²= (1−e^{iF})·`
  — the obstruction and the curvature are the same object.
- **Q2 — REFUTED, three independent ways.** The magnetic flux is **not** the `[d,τ]` diamond
  holonomy; it is exactly its **abelianization** (the image under the time-degree character
  `χ_q`), and the TA-c defect lives in the **kernel** of that character. **TA-c is NOT closed**
  — and provably cannot be closed by any abelian/spectral object.
- **Q3.** On the Hasse DAG all flux is supported on fork/merge cycles (trivially — a DAG
  skeleton has no other cycles), but with a refinement: **flux = 2πq × arm-length imbalance;
  balanced diamonds carry zero flux.** The magnetic content beyond the depth gradient is
  precisely the **gradedness defect** (revision-count asymmetry between branches) — real,
  exact, and modest.
- **Q4.** **Two charges, two operators, never one connection over a mixed edge set** (forced
  by ratified A5). Influence is anti-aligned with citation arrows and structurally aligned
  with time at mint; the deviations (**retro-citations**) are a measurable census, not an axiom.
- **Q5 — FALSE as a theorem, and the wrong analogy.** Flux is *gauge* curvature; Ricci
  (Forman/Ollivier) is *metric* curvature — independent axes (the Einstein–Maxwell slot).
  Forman is provably **flux-blind** (it reads only the support). The curvature ledger grows
  to five rows with exact relations.
- **Q6.** (a) retrieval upgrade — earns its **math**, not its build (defer to the
  retrieval-eval-set gate); (b) diagnostic lens — **earns a combinatorial v1** (directed-cycle
  / unbalanced-diamond / retro-citation census) that does *not* need the operator; the
  spectral version is the parked upgrade; (c) unifying structure — earns **vocabulary only**,
  and its chief value is prophylactic (this pass's refutations).
- **Q7 — DEFER the operator build; graduate the formalization as a new draft note; extract
  the census into the already-licensed Thread-C sweep.** A complete falsifier inventory
  exists (F1–F5 below, ready-made for any future graduating plan) — the buildable-now test
  passes on *falsifiability* but fails on *customer*: unlike the undirected lift (where only
  `L₁` could produce the harmonic threads), nothing the operator computes today is
  unreachable by elementary exact combinatorics.
- **Bonus grounding:** the house already built one fiber of this family — the signed
  Laplacian `L̄` is the `q = 1/2`, ℤ/2-holonomy magnetic Laplacian, and its
  "singular iff balanced" theorem (`laplacian.py:48–53`) is the flux-triviality kernel
  theorem restricted to ℤ/2. The magnetic family is the U(1) completion of machinery the
  codebase already trusts.

---

## 1. Setup — the operator, the connection, the gauge facts (shared ground)

**Definition.** `[ESTABLISHED: Lieb–Loss 1993; Shubin; Sunada; Fanuel et al. 2017 "magnetic
eigenmaps"]` Given a directed graph with symmetrized weights `w_{uv}` and charge
`q ∈ [0, 1/2]`, set the phase 1-cochain `θ^{(q)}(u,v) = 2πq·(a(u,v) − a(v,u))` (`a` the
directed indicator; a one-way edge u→v gets `+2πq`, a reciprocal pair gets `0`), the
Hermitian adjacency `H^{(q)}_{uv} = w_{uv} e^{iθ^{(q)}(u,v)}`, and

    L^{(q)} = D − H^{(q)},      x*L^{(q)}x = Σ_{u~v} w_{uv} |x_u − e^{iθ(u,v)} x_v|².

Hermitian ⇒ real spectrum; the quadratic form ⇒ PSD; `q=0` ⇒ `θ ≡ 0` ⇒ `L^{(0)} = D − A`,
**exactly** the built degree-0 operator (`core/complex/laplacian.py:26–30`) on the
symmetrized graph — the graceful-generalization requirement is met at the operator level,
and both normalizations (`L`, `L_sym`) magnetize identically (`D` unchanged, `A → H`).
DAG-native: no strong connectivity, no stationary distribution needed (the ground on which
Chung's directed Laplacian was already rejected — `dn-temporal-retrieval-algebra` §2.1(ii)).

**Gauge structure.** `[ESTABLISHED: lattice gauge theory, Wilson 1974]` `U(v←u) = e^{iθ(u,v)}`
is a U(1) connection. A gauge transformation `x_u ↦ e^{iψ_u}x_u` conjugates `L^{(q)}` by a
diagonal unitary and shifts `θ ↦ θ + d₀ψ`. The gauge-invariant content is the **flux**
(holonomy) through each cycle, `Φ(C) = Σ_{(u,v)∈C} θ(u,v) mod 2π`; the spectrum depends only
on the fluxes. **Flux-trivial (all cycles ≡ 0 mod 2π) ⟺ gauge-equivalent to the undirected
operator ⟺ identical spectrum.** So the magnetic spectrum carries information *exactly* on
the flux; everything else is the undirected v1.

**The elementary invariant.** `[DERIVED]` For a cycle `C` of the undirected skeleton with a
traversal, define the **circulation** `w(C) = #(edges traversed with their arrow) −
#(against)`. Then `Φ_q(C) = 2πq·w(C)`. `w: H₁(skeleton) → ℤ` is a homomorphism — the
**degree/imbalance class** — and `Φ_q = χ_q ∘ w` where `χ_q(n) = e^{2πiqn}` is a character
of ℤ. This one line does most of the work below.

**The signed-Laplacian fiber (house grounding).** `[DERIVED identification; ESTABLISHED for
the signed case: Hou/Kunegis, cited at laplacian.py:51]` At `q = 1/2` the phases lie in
`{±1}`: `L^{(1/2)}` with sign data *is* the signed Laplacian `L̄ = D̄ − A_signed`
(`core/complex/laplacian.py:48–56`), whose "λ_min = 0 iff balanced" theorem is the
flux-triviality kernel theorem for structure group ℤ/2 ⊂ U(1); `balance.py`'s frustration
proxy is the ℤ/2 shadow of the U(1) **frustration index** that controls `λ_min(L^{(q)})`
(magnetic Cheeger inequalities `[ESTABLISHED: Bandeira–Singer–Spielman 2013;
Lange–Liu–Peyerimhoff 2015]`). Semantics differ — polarity there, direction here (*same
family, different meaning of the phase*; the same-word-different-tensors discipline) — but
the theorems transfer verbatim. Two degeneracy notes: (i) at exactly `q = 1/2` the phase
forgets orientation (`e^{iπ} = e^{−iπ}`) — the polarity slot, a bad charge for reading
direction; (ii) `L^{(−q)} = conj(L^{(q)})`, so spectra are even in `q` and `q ∈ [0, 1/2]`
is the whole family.

---

## Q1 — Magnetic Hodge: the lift, the decomposition, the curvature 2-form

**(a) The degree-1 lift exists as an operator, always; as Hodge theory, conditionally.**

The twisted coboundary `(d₀^θ x)(u,v) = x_v − e^{iθ(u,v)} x_u` gives
`L₀^{(q)} = (d₀^θ)^* d₀^θ` (the definition above). For degree 1 one needs
`d₁^θ : C¹ → C²` transporting edge values into a common frame per triangle. Direct
computation (values-at-top-vertex convention, triangle `(i,j,k)`):

    (d₁^θ d₀^θ x)(ijk) = e^{iθ(i,k)} (1 − e^{iF(ijk)}) x_i,
    F(ijk) = θ(i,j) + θ(j,k) + θ(k,i)   (the flux through the triangle).

`[DERIVED — full computation]` So **`d² = multiplication by (1 − e^{iF})`: the twisted pair
is a cochain complex iff the connection is flat (`F ≡ 0 mod 2π`) on every filled 2-cell.**
This is the discrete instance of the general fact that a connection with curvature has
`d_∇² = F_∇` `[ESTABLISHED: standard; the cellular-sheaf degree-1 Laplacian of Hansen–Ghrist
2019 requires the flat/sheaf case]` — and it is formally the same *pattern* as Quillen's
`𝔸² = curvature` in the ratified Result 3 (`dn-temporal-retrieval-algebra` §2.3). A rhyme,
not an identification (see Q2).

**(b) The parity obstruction on the citation flag complex.** `[DERIVED]` On a 3-clique whose
three edges are all one-way, the circulation is a sum of three ±1's — **odd, never zero**:
`w ∈ {±1, ±3}` (cyclic triangle ±3, transitive triangle ±1). Hence `F = 2πq·w ≠ 0 mod 2π`
for **every** `q ∈ (0,1)`; no uniform charge makes an all-directed flag complex 2-cell-flat
(`q = 1/3` kills only the cyclic `w = ±3` triangles — the known motif charge `[ESTABLISHED:
Fanuel et al.]` — never the transitive ones). Only triangles containing a reciprocal
citation pair (`θ = 0` on that edge, so `w` can be 0) can be flat. **Consequence: the
magnetic Helmholtz decomposition over the flag complex — the 2-cells `hodge.py` is pinned to
by Rips consistency (`core/complex/hodge.py:5–12`) — fails for every nontrivial charge,
not marginally but on every generic filled triangle.** The degree-1 magnetic object on
`X_cite` therefore lives in the *curved* (twisted-complex) world, not in a chain complex.
One can still define the Hermitian PSD operator `L₁^θ = d₀^θ(d₀^θ)^* + (d₁^θ)^*d₁^θ`, but
its kernel is not homological, the three-way orthogonal split fails
(`im d₀^θ ⊄ ker d₁^θ`), and no `dim ker = β₁`-style falsifier exists there.

**(c) On the covering (Hasse) supersession DAG the decomposition exists — vacuously.**
`[DERIVED]` Three notes mutually adjacent in a covering DAG would force either a shortcut
(non-covering) or a directed cycle (acyclicity) — so **the Hasse skeleton is triangle-free**,
the flag complex has no 2-cells, flatness is vacuous, and the complexified Helmholtz
decomposition holds in the two-term form `C¹ = im d₀^θ ⊕ ker L₁^θ` (curl ≡ 0 identically).
Two riders: (i) this is a property of the *covering* edge set — the transitive closure H2
takes for the bicomplex math (`dn-temporal-retrieval-algebra` §2.3 Result 1) would fill the
complex with flux-carrying transitive triangles, so **the magnetic operator must be pinned to
the Hasse DAG; the closure belongs to the reachability semiring (Mode 1a), not to the
connection** — the two-dictionaries discipline one more time; (ii) triangle-freeness is
guaranteed only if authors declare covering supersessions — a declared shortcut
(`supersedes: [P, P′]` where P′ already supersedes P) mints a transitive triangle. That is a
cheap checkable **data-integrity invariant** to add beside F2 in the A6 list (see OWNER
DECISION 3).

**(d) Is the flux a genuine curvature 2-form? YES — literally.** `[ESTABLISHED: lattice
gauge theory]` `F = d₁θ ∈ C²(X; ℝ/2πℤ)` on filled complexes: gauge-invariant (gauge shifts
`θ` by `d₀ψ`, and `d₁d₀ = 0` on the *real* cochain level), Bianchi identity trivial
(`d₂F = 0` since `d² = 0` on real cochains), and discrete Stokes: the holonomy around `∂S`
is `e^{iF(S)}`. On the triangle-free Hasse DAG (no 2-cells) the honest phrasing is
**curvature as periods**: the flux is the homomorphism `Φ_q = χ_q∘w : H₁(skeleton) → U(1)`.
Both readings are exact; neither is a metaphor.

**Q1 verdict:** lift YES (operator), Hodge CONDITIONAL (flat 2-cells: DAG yes-vacuously,
`X_cite` no — parity-obstructed), curvature-2-form YES (literal). `q=0` recovers
`hodge.py`'s `L₁` exactly where the complex exists (real operator ⇒ complexified kernel
dimension unchanged ⇒ the `dim ker L₁ = β₁` falsifier is preserved at `q=0`).

---

## Q2 — The diamond identification: REFUTED (and the autopsy is the payoff)

**The conjecture.** Magnetic flux around a supersession fork/merge diamond = the `[d,τ]`
diamond holonomy that Result 3 could only sketch (TA-c); if yes, `L^{(q)}` closes TA-c.

**The two objects, made comparable.** `[DERIVED]` Both live over the note-level diamond
`P → {A, B} → Q`. The TA-c object is the holonomy of an **operator-valued (non-abelian)
connection**: transport of cochain data along supersession arms
(`σ_{A→Q}∘σ_{P→A}` vs `σ_{B→Q}∘σ_{P→B}`), whose disagreement is the coherence defect the
twisted-complex `τ_k` must fill. The magnetic object is the holonomy of a **U(1) (abelian)
connection** whose per-edge datum is only the fixed phase `e^{2πiq}` per time-step.
Every supersession step shifts the time-degree by +1, so the magnetic transport factors as
`χ_q ∘ deg` — **the magnetic connection is the abelian character of the time-degree grading
of the σ-transport; it remembers the bookkeeping of τ and none of its content.**

**Refutation, three independent legs:**

1. **Support mismatch (kills the `[d,τ]` layer).** `[DERIVED from Result 2,
   temporal-retrieval-algebra.md:142–145]` `[d,τ]` is supported **exactly on severed
   citations** — mixed squares `(u, v, σu, σv)` whose top edge `(σu,σv)` is *missing* from
   `X_{n+1}`. An open square is not a cycle; **flux is defined only on closed cycles.** Where
   `[d,τ]` lives, the magnetic holonomy does not exist; where the square closes (citation
   carried forward, F1), the mixed two-charge flux cancels to 0 (`+2πq_c +2πq_t −2πq_c
   −2πq_t`). The supports are disjoint *in kind*.
2. **Balanced diamonds: flux ≡ 0, defect generic ≠ 0 (kills one direction).** `[DERIVED]`
   The equal-arm diamond (`P→A→Q`, `P→B→Q`) has circulation `w = +1+1−1−1 = 0`, so
   `Φ_q = 0` **for every charge q** — yet the two arm-composites are two different maps and
   nothing forces them to agree; their difference is exactly the TA-c defect, generically
   nonzero. The magnetic flux is blind to precisely the diamonds TA-c is about.
3. **Coherent shortcuts: defect = 0, flux ≠ 0 (kills the converse).** `[DERIVED]` A
   transitive triangle `P→P′→P″` + direct `P→P″` with **F2 holding**
   (`σ_{P→P″} = σ_{P′→P″}∘σ_{P→P′}`, the ratified coherence invariant) has trivial operator
   holonomy by definition of F2 — but circulation `w = +1+1−1 = 1`, flux `2πq ≠ 0`.

**The structure theorem behind the failure.** `[DERIVED]` `w: H₁ → ℤ` (the degree class) is
the universal abelian invariant of supersession loops; `Φ_q = χ_q∘w` ranges over exactly the
U(1) characters of it as `q` varies. So the whole magnetic family `{Φ_q}` jointly captures
**precisely the abelianization** of the transport holonomy — and the TA-c defect on a
balanced diamond lies in the **kernel** of the degree character. Therefore **no choice of
charge, and no abelian/spectral gadget that reads only path-length bookkeeping, can close
TA-c.** The diamond superconnection needs the operator-valued twisted-complex machinery
(Bondal–Kapranov / Block, per Result 3's sketch) or nothing. TA-c's original park-with-gate
(measured diamond frequency) stands unmodified.

**Steelman, named and rejected.** `[INFERENCE]` A content-dependent phase (e.g.
`θ(e) = arg det σ_e`) could make flux see *some* content — but σ is generically
non-invertible (severances have kernels; merges are non-injective), so `det = 0` and the
phase is undefined exactly where it matters; and any such phase abandons the fixed-charge,
model-free, `q=0`-recovers-v1 contract. Even where defined it captures a 1-dimensional
shadow, never the matrix-valued defect.

**Q2 verdict: REFUTED (two-sided plus support-mismatch). TA-c is NOT closed. The consolation
is real: "flux = the abelian character of the diamond holonomy" explains why the two felt
like one object (both are time-direction holonomies around the same diamond) and proves
exactly what the abelianization forgets — all content.** The exciting conjecture dies; the
category error it would have seeded ("close TA-c with a spectrum") dies with it.

---

## Q3 — E_disp: where the magnetic field lives on the acyclic DAG

**Reconciliation with ratified A5 first** (`temporal-retrieval-algebra.md:194–203`). A5's
object is the depth potential: acyclicity ⇒ a monotone `ℓ` exists ⇒ the *direction field* is
gradient-representable (`E_disp` is pure `d₀(depth)` — curl-free, harmonic-free). The
magnetic phase is a **different 1-cochain**: the *unit-speed* direction field `θ = 2πq·𝟙`.
The two coincide (`𝟙 = d₀ℓ`) **iff a unit-increment potential exists — iff the DAG is
graded.** `[DERIVED]` So there is no contradiction: A5 speaks of representability of the
sign pattern; the flux measures the cyclic residue of the *unit* field.

**Theorem (support and value of the flux on the Hasse DAG).** `[DERIVED]`
(i) Every cycle of a DAG's undirected skeleton contains both a local source and a local sink
— i.e., *is* a fork/merge cycle — so "flux lives only on fork/merge structure" holds
**trivially on support**. (ii) The content is quantitative: for a diamond with arm lengths
`ℓ₁, ℓ₂`, `Φ_q = 2πq(ℓ₁ − ℓ₂)`. **Balanced diamonds (equal arms) carry zero flux** — a
refinement of the brainstorm's guess: not all diamonds, only length-unbalanced ones.
(iii) Corollary: on a **graded** supersession DAG (every diamond balanced — in particular on
any forest/linear-chain corpus, which has no diamonds at all) the connection is flux-trivial,
hence `L^{(q)}` is **gauge-equivalent to the undirected Laplacian: identical spectrum, zero
added information, for every q.**

**So what IS the magnetic content beyond the depth gradient?** Exactly the **gradedness
defect**: the failure of "number of supersession steps" to be a consistent clock across
branches — one branch took three revisions, the sibling took one, to reach the same merge.
Semantic reading: **revision-effort asymmetry** at forks. It is a genuine, exact, deterministic
invariant that the depth gradient does not carry (`[DERIVED]` — the depth potential ignores
per-edge unit speed). It is also *modest*: an integer per independent diamond, computable by
subtraction. Answering the question as posed: **yes — this is precisely the content
"direction" has beyond the depth gradient, and it is exactly the magnetic Laplacian's
non-trivial temporal role. Whether that content is worth an operator is Q6/Q7's business,
and the answer there is: count it combinatorially first.**

---

## Q4 — One field or two

**Two. Forced, not chosen.** `[DERIVED from ratified A5, temporal-retrieval-algebra.md:194–203]`
Citation-influence direction lives on `X_cite` edges; supersession-time direction lives on
`E_disp`. A single connection over the union edge set is the same **type error** A5 already
ruled against for `L₁` (incompatible metrics; supersession leaking into balance-adjacent
math). Two phase cochains `θ^{(q_c)}_cite`, `θ^{(q_t)}_time`, two operators, two homes —
`X_cite`'s in the future `core/temporal/` module (TA-d), the DAG's beside it; both **outside**
`core/complex/` (the isolation grep, `reference_edges.py:5–9`; A4). A coupled
`U(1)×U(1)`-connection on a product complex is nameable vocabulary `[ANALOGY]` and rejected
as a build — nothing needs it, and Q2's analysis already used the mixed square as a *pencil
computation* without wiring it.

**Do they correlate?** Structurally yes, by mint-time causality, and the deviation is the
interesting measurable. `[DERIVED]` A note can only cite what exists when the citation is
authored, so citation arrows (citing → cited) point **backward in time**; influence
(cited → citing) flows **forward** — alignment by construction, not by observation. The
exceptions are **retro-citations**: a citation edge whose target is *younger* than the
source's original authorship — mintable only through revision (F1 carry-forward plus edit),
and each one is a witness of **revision-mediated influence backflow**. This is directly
measurable today: `reference_edges.sqlite` keys every edge by `commit_sha` ("the time
coordinate," `reference_edges.py:121–122`), and endpoint creation times come from git
history — a deterministic census, no model. **Ruling: keep `q_cite`/`q_time` independent;
the correlation is an output (an INTERPRETED-class statistic under §2.7), never a wiring
assumption.**

---

## Q5 — Flux ⟷ Ricci: false as a theorem, and the wrong analogy

**The category distinction.** `[ESTABLISHED: differential geometry]` Ricci curvature
(Forman, Ollivier) is curvature of the **metric/measure** structure — an edge scalar
contracted from how geometry focuses or spreads. Magnetic flux is curvature of a **U(1)
gauge connection** — a 2-cell/cycle quantity independent of the metric. On a manifold the
pair `(g, A)` carries two independent curvatures `Ric(g)` and `F = dA`; no identity links
them — they meet only dynamically (Einstein–Maxwell, where `F`'s stress-energy *sources*
Ricci). "Magnetic flux ≈ directed Ricci" is therefore **false as a theorem and a category
error as an analogy**.

**Separation witnesses, both directions.** `[DERIVED]`
- **Forman is provably flux-blind:** the built formula reads only the *support* —
  `curvature.py:30` binarizes (`B = (A != 0)`) before `Ric_F(u,v) = 4 − deg u − deg v +
  3|△(u,v)|` (`curvature.py:9–15, 25–43`). Phases never enter: `Ric_F(L^{(q)}) ≡
  Ric_F(L^{(0)})` for every q, while the flux ranges freely. 
- **Conversely:** a directed path graph (no cycles: flux vacuously zero everywhere) with
  asymmetric walk rates has nontrivial *directed Ollivier* curvature — the non-reversible
  Markov-kernel form `[ESTABLISHED: Ollivier 2009 is defined for arbitrary Markov chains]` —
  so directed Ricci varies where flux cannot.

**What the owner's instinct correctly points at:** the legitimate "directed Ricci" is the
**Ollivier curvature of the directed walk** — which is exactly the already-parked PD-c
object (`dn-edge-dynamics` §2.4, §4), now with a sharper description. It is a *different,
also-real* object; the flux is not it and does not approximate it.

**The salvage (where they honestly meet).** `[INFERENCE, flagged]` Forman's own derivation
is a discrete Bochner–Weitzenböck decomposition of `L₁` `[ESTABLISHED: Forman 2003]`; a
*magnetic* Forman could in principle be extracted the same way from `L₁^θ`, in which
flux-dependent terms and degree terms would appear as **separate summands of one operator
identity** — the Einstein–Maxwell slot, cohabitation, never identification. On the flag
`X_cite` this is complicated by the Q1 curvature obstruction (the decomposition is
non-standard when `d² ≠ 0`); recorded as vocabulary only, no customer.

**The curvature ledger (consolidated — extends the ratified "same word, different tensors"
note, Result 3):**

| curvature | type | base | measures | relations |
|---|---|---|---|---|
| magnetic flux `F = dθ` / `Φ_q` | abelian U(1) 2-form / periods | cycles of one snapshot's directed structure | directed circulation (`X_cite`); gradedness defect (DAG) | `= χ_q∘deg` — the abelian character of the transport holonomy (Q2) |
| superconnection `[d,τ]` | operator-valued, degree 1 | the linear time chain | severed citations (Result 2, exact support) | lives on *open* squares — outside flux's domain (Q2 leg 1) |
| diamond holonomy / `τ_k` defect | non-abelian groupoid holonomy | note-level fork/merge diamonds | fork/merge content incoherence (TA-c) | in `ker(χ_q∘deg)` on balanced diamonds (Q2 leg 2) |
| Forman–Ricci (built) | edge scalar, metric | one snapshot's weighted support | bridges/communities (`curvature.py`) | flux-blind (support-only) — independent axis |
| Ollivier–Ricci, incl. directed-walk form (deferred PD-c) | edge scalar, metric/measure | a Markov kernel | transport contraction; the true "directed Ricci" | independent of flux (separation witnesses above) |

---

## Q6 — The three roles: what each genuinely earns

**(a) Retrieval upgrade (directed Mode-1b diffusion; PD-b/TA-a's "second customer").**
**Earns its math; does not yet earn its build.** `[DERIVED ruling]` The math is now
finalized: `e^{−tL^{(q)}}` / resolvent kernels are Hermitian PSD, DAG-native, `q=0`-graceful.
But two honest facts bind: (i) Hermiticity forces `|K_{su}| = |K_{us}|` — **the magnitudes
are symmetric; direction lives only in the phase** `arg K_{su}`, so a directed *ranking*
needs a phase→score dictionary that does not yet exist (the literature uses phases for
embeddings/communities, not asymmetric affinities `[ESTABLISHED: Fanuel et al.; MagNet 2021
(q=1/4 convention)]`) — one more real design decision, recorded for the gate; (ii) hard
directed reachability ("downstream of s") is **already served exactly** by Mode 1a's
transitive closures (ratified §2.1(ii)); what 1b-directed adds is *soft* directional
nearness — a tuning-class object with **no falsifier until a retrieval eval set exists**,
the very logic that parked TA-b's z-dial. **Ruling: re-park with TA-a, re-entry sharpened to
the retrieval-eval-set gate (= TA-b's gate), with the phase→score dictionary named as the
gate's entry work.** Rejected alternative: build it now as infrastructure-ahead-of-need —
violates the discipline (elegant, no falsifiable customer).

**(b) Diagnostic lens (the THREAD lens's directed cousin).** **Earns a combinatorial v1 —
which does not need the operator.** `[DERIVED ruling]` The claim classes the direction
structure genuinely supports, all mirror-safe (corpus-structural tier — `X_cite` and the
supersession chains are embedder-independent; prior pass ruling B.4):
- **directed influence cycles** on `X_cite` ("these notes feed each other" — feedback, a
  different animal from the undirected `hole`'s "you orbit this") — computable exactly by
  SCC/cycle enumeration (Tarjan, O(V+E));
- **unbalanced diamonds** on the supersession DAG (Q3's revision-effort asymmetry) —
  computable by arm-length subtraction over a cycle basis;
- **retro-citations** (Q4) — computable from `commit_sha` + git history.
None of these needs a spectrum; all are exact, deterministic, gauge-free. The magnetic
*spectral* version (rank directed structures by eigenvector localization; soft/persistent
cycles) is the upgrade, parked with a **new admissibility pin surfaced by this pass:
eigenvector phases are gauge-DEPENDENT** — only fluxes, magnitudes, and along-edge phase
*differences* are gauge-invariant, so a spectral lens must narrate gauge-invariant
quantities only, or it manufactures apophenia from an arbitrary gauge choice. `[DERIVED —
the A7 discriminator's gauge-theoretic instance; combinatorial invariants are immune by
construction.]` The census's honest-seam: emits nothing when no directed cycle / no
unbalanced diamond / no retro-citation exists. Whether census claims enter dream narration
is owner taste (the standing `dn-edge-dynamics` §5 vocabulary question — OWNER DECISION 2).

**(c) Unifying structure.** **Earns vocabulary only — and the vocabulary's value is mostly
prophylactic.** `[DERIVED ruling]` The three unification hopes resolve: magnetic Hodge —
obstructed on the flag complex (Q1); flux = diamond holonomy — refuted, abelian shadow only
(Q2); flux = directed Ricci — false, wrong category (Q5). What survives is exact and worth
keeping: flux as literal gauge curvature; the five-row curvature ledger with proved
relations; the signed-Laplacian-as-q=1/2 grounding. This is design-tier vocabulary in
precisely the brainstorm §4 sense — it prevents future category errors (e.g., an attempt to
"close TA-c with a spectrum" now dies at the note instead of in a build).

---

## Q7 — The falsifier inventory, and graduate-or-defer

**The magnetic falsifiers exist and are exact** — ready-made §7 material for any future
graduating plan; none requires new theory:

- **F1 (endpoint):** `spec L^{(0)} == spec L` (and `== hodge.py`'s `L₁` at degree 1 where
  the complex exists) to machine precision — the graceful-generalization check as a test.
- **F2 (gauge):** the spectrum is invariant under random gauge transforms `θ ↦ θ + d₀ψ`;
  any drift is an implementation bug by definition.
- **F3 (degree-0 kernel drop):** per connected component, `dim ker L₀^{(q)} = 1` iff every
  cycle's flux ≡ 0 mod 2π, else 0 — so `dim ker L₀^{(q)} = #components −
  #flux-nontrivial-components`, cross-checked by independent spanning-tree/cycle-basis flux
  enumeration. `[DERIVED — flat-section argument; generalizes the built signed theorem,
  laplacian.py:48–53]`
- **F4 (degree-1 kernel on the Hasse DAG):** with the triangle-free skeleton,
  `dim ker L₁^{(q)} = Σ_c (β₁(c) − 1 + triv(c))` where `triv(c) = 1` iff component `c` is
  flux-trivial — the twisted Euler-characteristic count `[DERIVED: rank-1 local system,
  dim H⁰ − dim H¹ = 1 − β₁ per component]`, cross-checked against ripser β₁
  (`topology.py:61–67`) plus the F3 census. **This is the magnetic analog of the built
  `dim ker L₁ == ripser` falsifier** — it exists, it is exact, it is integer-valued.
- **F5 (determinism):** census and spectra byte-identical run-to-run on fixed commits
  (house invariant).

**The ruling: DEFER the operator build; GRADUATE the formalization; EXTRACT the census.**
`[DERIVED ruling — the discipline applied, not a budget judgment]`

The undirected lift graduated because its deliverable — harmonic threads — was falsifiable
**and only `L₁` could produce it** (no elementary algorithm yields the harmonic subspace).
The magnetic operator today fails the second clause: every falsifiable deliverable it has
(directed cycles, diamond imbalances, retro-citations, flux censuses) is computable by
elementary exact combinatorics without the operator, and every deliverable that *needs* the
operator (directed-diffusion retrieval scores, spectral rankings, magnetic eigenmaps) has no
customer with a falsifier (no retrieval eval set; no lens that demands ranking over exact
enumeration). Buildable-now: **falsifiability yes, customer no — so it waits**, exactly as
the discipline demands of elegant machinery.

Concretely, three routed pieces:
1. **The new draft design note** (the brainstorm §6 home; orchestrator-composed from this
   capsule, owner-ratified — the same opus-drafts/fable-warrants seam as
   `dn-temporal-retrieval-algebra`): states Q1's conditional Hodge + parity obstruction,
   Q2's refutation + character theorem (TA-c stands), Q3's structure theorem, Q4's
   two-charge ruling, Q5's ledger, the F1–F5 inventory, and the re-park below. This capsule
   is its warrant; I do not create the note (not my write scope, and notes are the
   orchestrator's seam).
2. **The arrow-aware combinatorial census folds into the already-licensed Thread-C sweep**
   (`dn-temporal-retrieval-algebra` §3 item 2 already lists "diamond frequency" verbatim —
   temporal-retrieval-algebra.md:268–272): add arm-length imbalance per diamond,
   retro-citation count, and `X_cite` SCC/directed-cycle count. No new license needed; the
   sweep was the TA-c re-entry gate's instrument anyway, and it is exactly the data that
   would justify any magnetic re-entry.
3. **The operator re-parks with three named re-entry gates** (any one suffices):
   (i) a retrieval eval set exists (role a; = TA-b's gate) *and* the phase→score dictionary
   is designed; (ii) the combinatorial lens proves insufficient — ranking/softness over
   exact enumeration is demonstrably needed (role b; mirrors PD-b's own re-entry form);
   (iii) the Thread-C census shows unbalanced diamonds / directed cycles are *common* on the
   real corpus (data warrants the finer instrument; shared with TA-c's gate). Pinned build
   constraints, recorded now so no future builder re-derives them: Hasse-DAG-only (never the
   transitive closure), two charges never one (Q4), home outside `core/complex/` (A4/TA-d;
   `reference_edges.py:5–9` isolation grep), `q` generic (recommend 1/4; `q = 1/2` is the
   polarity-degenerate slot; `q = 1/3` only as the cyclic-triangle motif charge), dense
   Hermitian eigh under a `hodge.py:41`-style size guard, gauge-invariant outputs only,
   F1–F5 as acceptance.

---

## OWNER DECISION items (surfaced, not resolved)

1. **Adopt or override the Q7 defer-the-operator ruling.** The owner reversed decision-#4's
   DEFER to license *this math pass* — the math is now done and warranted. My ruling keeps
   the *operator build* parked behind the three named gates while the census rides Thread-C.
   If the owner weighs the vocabulary/instrument value differently (e.g., wants the flux
   census computed *via* the operator as a cross-check from day one), the graduating note
   can flip that — it is a taste call on top of an argued default. (Rec: defer, as ruled.)
2. **Dream-narration vocabulary for the arrow-aware census** (directed influence cycles,
   revision-effort asymmetry, retro-citations): does this claim family enter the dreamer's
   narration, and with what language? Extends the standing `dn-edge-dynamics` §5 open
   question; costs nothing until a lens plan exists.
3. **Covering-only supersession declarations as a checked invariant** (Q1c rider): rule that
   `supersedes` frontmatter declares covering relations only (no transitive shortcuts), and
   add the cheap check beside F2 in the A6 list. Constrains authoring practice slightly;
   keeps the Hasse skeleton triangle-free (which the diamond census also prefers). (Rec:
   adopt; near-zero cost.)

## Open questions / what a follow-up needs

- **Empirical (runnable now, bp-026):** the extended Thread-C census — diamond frequency
  *with arm-length imbalance*, retro-citation count, `X_cite` SCC/cycle count. This is
  simultaneously the TA-c gate's instrument and magnetic re-entry gate (iii).
- **The phase→score dictionary** for directed diffusion retrieval — the open design item at
  re-entry gate (i); nothing to decide until an eval set exists.
- **Magnetic Weitzenböck / flux-aware Forman** (Q5 salvage) — vocabulary only; a small math
  pass *if* a curvature customer ever appears; blocked conceptually by the Q1 obstruction on
  curved complexes.
- **TA-c itself** is untouched and un-closable by spectral means (Q2); its gate (measured
  diamond frequency) is now better instrumented but unchanged.
- **Rename-stable identity (A6)** still gates everything diachronic, including the
  retro-citation census's lineage joins across renames — the owner's standing prerequisite
  ruling applies here too.
