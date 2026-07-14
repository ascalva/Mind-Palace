---
type: design-note
id: dn-magnetic-laplacian
status: draft # draft → ratified → superseded.  draft→ratified is an OWNER-ONLY hand edit.
implementation: design-only # nothing built; states the fable-finalized results, defers the operator, licenses nothing new
created: 2026-07-14
updated: 2026-07-14
links:
  - docs/brainstorms/magnetic-laplacian-fable-pass.md # the fable warrant this note states (whole; proofs live there)
  - docs/brainstorms/magnetic-laplacian.md # the framing brainstorm that chartered the pass
  - docs/design-notes/temporal-retrieval-algebra.md # ratified; A5, Result 1–5, §2.1(ii), §3 item 2 (Thread-C), TA-a/TA-c/TA-d
  - docs/design-notes/edge-dynamics.md # ratified; PD-b, PD-c (Ollivier), §5 vocabulary question, the inversion
  - docs/design-notes/recursive-strata-amendment.md # the A6 data-integrity invariants (F2, and the covering-only rider)
warrant: docs/brainstorms/magnetic-laplacian-fable-pass.md
supersedes: null
superseded_by: null
---

# The magnetic (Hermitian) Laplacian — direction as a U(1) gauge field, formalized then deferred

> Composed by the orchestrator (**Opus 4.8/xhigh**, 2026-07-14) from the **verified Fable pass**
> (`claude-fable-5`, tier owner-confirmed) captured in
> `docs/brainstorms/magnetic-laplacian-fable-pass.md`. This note **states** the fable-finalized results
> (Q1–Q7) and makes the design decisions they inform; the derivations and proofs live in the capsule
> (cited, not repeated) — the same "opus-drafted, fable-checked, owner-ratified" seam
> `dn-temporal-retrieval-algebra` used.
>
> It formalizes the magnetic Laplacian `L^{(q)}` — the directed-diffusion upgrade named in ratified
> `dn-temporal-retrieval-algebra` §2.1(ii) / TA-a — as the formalization of graph **"direction."** The
> owner reversed decision-#4's DEFER to license *this math pass* (framing brainstorm
> `docs/brainstorms/magnetic-laplacian.md`); the math is now done. **The decision this note records is
> that the operator BUILD stays deferred behind three named gates while the settled formalization — and
> the combinatorial census that earned its place — are finalized here** (owner direction, 2026-07-14).
>
> `dn-edge-dynamics` and `dn-temporal-retrieval-algebra` are **ratified/immutable** — cited, never
> edited. Every nontrivial result carries its fable grade (`[ESTABLISHED]`/`[DERIVED]`/`[INFERENCE]`/
> `[ANALOGY]`); trust-weight accordingly. Ratification is a hand edit by the owner — no command performs
> it, and it is where the two OPEN owner decisions (§ Owner rulings) are ruled.

## 1. Purpose and scope

`dn-temporal-retrieval-algebra` §2.1(ii) named the **magnetic/Hermitian Laplacian `L^{(q)}`** as the
directed-diffusion upgrade to the symmetric v1 (`q=0` recovers v1; `q>0` keeps direction in complex
phase, stays Hermitian-PSD) and parked it with PD-b / TA-a. This note formalizes it and rules what it
earns:

1. **The operator, its gauge structure, and its house grounding** (§2.1) — `L^{(q)}` exists, is
   Hermitian-PSD, is DAG-native, recovers the built degree-0 operator at `q=0`, and its `q=1/2` fiber
   **is** the signed Laplacian the codebase already trusts.
2. **Magnetic Hodge — conditional** (§2.2, Q1) — a degree-1 operator always; genuine Hodge theory only
   on flat 2-cells, which the citation flag complex **parity-obstructs** and the covering DAG makes
   vacuous. Flux is a literal curvature 2-form.
3. **The diamond conjecture — REFUTED** (§2.3, Q2) — magnetic flux is the *abelianization* of the
   `[d,τ]` diamond holonomy; **TA-c is not closed and provably not by any abelian/spectral object.**
4. **Where the field lives** (§2.4–§2.5, Q3–Q4) — the **gradedness defect** on the supersession DAG; two
   charges never one (forced by ratified A5); retro-citations as a measurable census.
5. **Flux ≠ Ricci** (§2.6, Q5) — gauge vs metric curvature; the five-row curvature ledger.
6. **What each role earns, and the deferral** (§2.7, Q6/Q7) — the **combinatorial census earns a v1 that
   needs no operator**; the operator earns its *math, not its build*, and re-parks behind three gates;
   the F1–F5 falsifier inventory is ready-made.

**Out of scope, explicitly:** this note **builds nothing and licenses no new build.** The census rides the
**already-licensed** Thread-C sweep (`dn-temporal-retrieval-algebra` §3 item 2 — "no new license"); the
operator is deferred; the retrieval-protocol architecture stays in `dn-core-query-protocol`; the true
"directed Ricci" is the parked PD-c (`dn-edge-dynamics`). This note is the **formalization + the deferral
ruling + the prophylactic vocabulary**, not an instrument.

## 2. Principles / decision

### 2.1 The operator `L^{(q)}`, its gauge facts, and its house grounding

`[capsule §1]` For a directed graph with symmetrized weights `w_{uv}` and charge `q ∈ [0, 1/2]`, set the
phase 1-cochain `θ^{(q)}(u,v) = 2πq·(a(u,v) − a(v,u))` (a one-way edge `u→v` gets `+2πq`, a reciprocal
pair `0`), the Hermitian adjacency `H^{(q)}_{uv} = w_{uv} e^{iθ^{(q)}(u,v)}`, and

    L^{(q)} = D − H^{(q)},     x*L^{(q)}x = Σ_{u~v} w_{uv} |x_u − e^{iθ(u,v)} x_v|²   (Hermitian, PSD).

- **`q=0` is v1, exactly.** `θ ≡ 0 ⇒ L^{(0)} = D − A`, the built degree-0 operator
  (`core/complex/laplacian.py:26–30`) on the symmetrized graph; both normalizations (`L`, `L_sym`)
  magnetize identically (`D` unchanged, `A → H`). **DAG-native** — no strong connectivity, no stationary
  distribution (the ground on which Chung's directed Laplacian was rejected, §2.1(ii)). `[ESTABLISHED:
  Lieb–Loss; Shubin; Sunada; Fanuel 2017]`
- **The gauge-invariant content is the flux.** `U(v←u) = e^{iθ(u,v)}` is a U(1) connection; a gauge
  transform `x_u ↦ e^{iψ_u}x_u` shifts `θ ↦ θ + d₀ψ` and leaves the spectrum unchanged. **Flux-trivial
  (every cycle `Φ(C) ≡ 0 mod 2π) ⟺ gauge-equivalent to the undirected operator ⟺ identical spectrum.**
  So the magnetic spectrum carries information *exactly on the flux*; everything else is v1. `[ESTABLISHED:
  Wilson 1974]`
- **The elementary invariant.** `[DERIVED]` For a skeleton cycle `C`, the **circulation** `w(C) =
  #(with-arrow) − #(against)`; then `Φ_q(C) = 2πq·w(C)`, and `w: H₁(skeleton) → ℤ` is a homomorphism (the
  **degree/imbalance class**), `Φ_q = χ_q∘w` with `χ_q(n) = e^{2πiqn}`. This one line does most of the
  work below.
- **House grounding — the signed Laplacian is the `q=1/2` fiber.** `[DERIVED identification; ESTABLISHED
  signed case: Hou/Kunegis, `laplacian.py:51`]` At `q=1/2` the phases lie in `{±1}`: `L^{(1/2)}` with sign
  data **is** the signed Laplacian `L̄ = D̄ − A_signed` (`core/complex/laplacian.py:48–56`), whose
  "λ_min = 0 iff balanced" theorem is the flux-triviality kernel theorem for structure group ℤ/2 ⊂ U(1);
  `balance.py`'s frustration proxy is the ℤ/2 shadow of the U(1) frustration index (magnetic Cheeger,
  `[ESTABLISHED: Bandeira–Singer–Spielman 2013; Lange–Liu–Peyerimhoff 2015]`). **The magnetic family is
  the U(1) completion of machinery the codebase already trusts** — *polarity there, direction here* (same
  family, different meaning of the phase). Degeneracies: at `q=1/2` the phase forgets orientation
  (`e^{iπ}=e^{−iπ}` — the polarity slot, a bad charge for direction); `L^{(−q)} = conj(L^{(q)})`, so
  spectra are even in `q` and `q ∈ [0,1/2]` is the whole family.

### 2.2 Magnetic Hodge — a lift always, Hodge theory conditionally (Q1)

`[capsule Q1]` The twisted coboundary `(d₀^θ x)(u,v) = x_v − e^{iθ(u,v)} x_u` gives `L₀^{(q)} =
(d₀^θ)^*d₀^θ`. Lifting to degree 1 needs `d₁^θ`, and direct computation gives (values-at-top-vertex,
triangle `(i,j,k)`):

    (d₁^θ d₀^θ x)(ijk) = e^{iθ(i,k)} (1 − e^{iF(ijk)}) x_i,   F(ijk) = θ(i,j)+θ(j,k)+θ(k,i)  (the flux).

So **`d² = ` multiplication by `(1 − e^{iF})`: the twisted pair is a cochain complex iff the connection is
flat (`F ≡ 0 mod 2π`) on every filled 2-cell** — the discrete instance of `d_∇² = F_∇`. `[DERIVED — full
computation; ESTABLISHED: Hansen–Ghrist 2019 need the flat/sheaf case]` This is formally the same *pattern*
as Quillen's `𝔸² = curvature` (Result 3) — **a rhyme, not an identification** (§2.3).

- **The parity obstruction on `X_cite`.** `[DERIVED]` On an all-one-way 3-clique the circulation is a sum
  of three ±1's — **odd, never zero** (`w ∈ {±1, ±3}`), so `F = 2πq·w ≠ 0 mod 2π` for **every** `q ∈
  (0,1)` (`q=1/3` kills only cyclic `w=±3` triangles — the motif charge — never transitive ones). Only a
  triangle with a reciprocal citation pair can be flat. **Consequence: the magnetic Helmholtz
  decomposition over the flag complex `hodge.py` is pinned to (Rips consistency,
  `core/complex/hodge.py:5–12`) fails for every nontrivial charge — on every generic filled triangle.**
  The Hermitian PSD operator `L₁^θ` still exists, but its kernel is not homological, the three-way split
  fails, and **no `dim ker = β₁` falsifier exists there.**
- **On the covering (Hasse) DAG the decomposition exists — vacuously.** `[DERIVED]` Three mutually
  adjacent covering-DAG notes force a shortcut or a directed cycle, so **the Hasse skeleton is
  triangle-free**; flatness is vacuous, curl ≡ 0, and `C¹ = im d₀^θ ⊕ ker L₁^θ` holds in two-term form.
  **Riders:** (i) the magnetic operator must be pinned to the **Hasse DAG**, never the transitive closure
  (which fills the complex with flux-carrying transitive triangles — the closure belongs to the
  reachability semiring, Mode 1a, not to the connection); (ii) triangle-freeness holds only if authors
  declare *covering* supersessions — a declared shortcut mints a transitive triangle → a cheap checkable
  data-integrity invariant (Owner decision 3).
- **Flux is a genuine curvature 2-form — literally.** `[ESTABLISHED: lattice gauge theory]` `F = d₁θ` is
  gauge-invariant, obeys the Bianchi identity, and gives discrete Stokes (holonomy around `∂S` is
  `e^{iF(S)}`). On the triangle-free DAG the honest phrasing is **curvature as periods**: `Φ_q = χ_q∘w :
  H₁(skeleton) → U(1)`. Both readings are exact; neither is a metaphor.

**Q1 verdict:** lift YES (operator); Hodge CONDITIONAL (flat 2-cells — DAG yes-vacuously, `X_cite` no,
parity-obstructed); curvature-2-form YES (literal). `q=0` recovers `hodge.py`'s `L₁` exactly where the
complex exists (the `dim ker L₁ == β₁` falsifier is preserved at `q=0`).

### 2.3 The diamond conjecture — REFUTED; flux is the abelianization of the holonomy (Q2)

`[capsule Q2]` **The conjecture:** magnetic flux around a supersession fork/merge diamond = the `[d,τ]`
diamond holonomy Result 3 could only sketch (TA-c); if yes, `L^{(q)}` closes TA-c. **REFUTED, three
independent ways** — the magnetic connection is an **abelian** U(1) connection carrying only `e^{2πiq}`
per time-step; the TA-c object is an **operator-valued (non-abelian)** transport holonomy. The magnetic
connection factors as `χ_q ∘ deg` — **it is the abelian character of the time-degree grading of the
σ-transport; it remembers the bookkeeping of τ and none of its content.**

1. **Support mismatch** `[DERIVED from Result 2, temporal-retrieval-algebra.md:142–145]` — `[d,τ]` is
   supported **exactly on severed citations** (open mixed squares whose top edge is *missing*). An open
   square is not a cycle; **flux is defined only on closed cycles.** Where `[d,τ]` lives, the magnetic
   holonomy does not exist; where the square closes (F1), the mixed two-charge flux cancels to 0. Disjoint
   *in kind*.
2. **Balanced diamonds: flux ≡ 0, defect generic ≠ 0** `[DERIVED]` — the equal-arm diamond has `w =
   +1+1−1−1 = 0`, so `Φ_q = 0` for **every** charge, yet the two arm-composites are different maps whose
   difference is exactly the (generically nonzero) TA-c defect. Flux is blind to precisely the diamonds
   TA-c is about.
3. **Coherent shortcuts: defect = 0, flux ≠ 0** `[DERIVED]` — a transitive triangle with **F2 holding**
   has trivial operator holonomy but circulation `w = 1`, flux `2πq ≠ 0`.

**Structure theorem.** `[DERIVED]` `w: H₁ → ℤ` is the universal abelian invariant of supersession loops;
`{Φ_q}` jointly captures **precisely the abelianization** of the transport holonomy, and the TA-c defect
on a balanced diamond lies in the **kernel** of the degree character. Therefore **no charge, and no
abelian/spectral gadget reading only path-length bookkeeping, can close TA-c.** The steelman (a
content-dependent phase `θ = arg det σ_e`) fails: σ is generically non-invertible (`det = 0` exactly at
severances/merges), and any such phase abandons the fixed-charge, `q=0`-recovers-v1 contract.

**Q2 verdict: REFUTED (two-sided + support mismatch). TA-c is NOT closed; its park-with-gate (measured
diamond frequency) stands unmodified.** The consolation is real — *"flux = the abelian character of the
diamond holonomy"* explains why the two felt like one object and proves exactly what the abelianization
forgets (all content). The category error it would have seeded — *"close TA-c with a spectrum"* — dies at
this note instead of in a build.

### 2.4 Where the field lives on the acyclic DAG — the gradedness defect (Q3)

`[capsule Q3]` **Reconciliation with ratified A5 first** (`temporal-retrieval-algebra.md:194–203`): A5's
object is the depth potential (acyclicity ⇒ a monotone `ℓ` ⇒ `E_disp` is pure `d₀(depth)`, curl-free); the
magnetic phase is a **different** 1-cochain — the *unit-speed* field `θ = 2πq·𝟙`. They coincide (`𝟙 =
d₀ℓ`) **iff the DAG is graded.** No contradiction: A5 is about representability of the sign pattern; the
flux measures the cyclic residue of the *unit* field. `[DERIVED]`

**Theorem (support + value on the Hasse DAG).** `[DERIVED]` (i) Every skeleton cycle of a DAG contains a
local source and sink — *is* a fork/merge cycle — so "flux lives only on fork/merge structure" holds
trivially on support. (ii) For a diamond with arm lengths `ℓ₁, ℓ₂`, `Φ_q = 2πq(ℓ₁ − ℓ₂)` — **balanced
diamonds carry zero flux** (a refinement: not all diamonds, only length-unbalanced ones). (iii) On a
**graded** DAG (every diamond balanced — in particular any forest/linear-chain corpus) the connection is
flux-trivial: `L^{(q)}` is gauge-equivalent to the undirected Laplacian, **zero added information, for
every q.**

**The magnetic content beyond the depth gradient is exactly the gradedness defect** — the failure of
"number of supersession steps" to be a consistent clock across branches (one branch took three revisions,
its sibling one, to reach the same merge). Semantically, **revision-effort asymmetry at forks**: a genuine,
exact, deterministic integer-per-diamond invariant the depth gradient does not carry — and *modest*
(computable by subtraction). Whether it is worth an operator is Q6/Q7: **count it combinatorially first.**

### 2.5 Two charges, not one; retro-citations (Q4)

`[capsule Q4; DERIVED from ratified A5]` **Two fields, forced not chosen.** Citation-influence direction
lives on `X_cite` edges; supersession-time direction lives on `E_disp`. A single connection over the union
is the same **type error** A5 ruled against for `L₁`. So: two phase cochains `θ^{(q_c)}_cite`,
`θ^{(q_t)}_time`, two operators, two homes — `X_cite`'s in the future `core/temporal/` (TA-d), the DAG's
beside it; **both outside `core/complex/`** (the isolation grep, `reference_edges.py:5–9`; A4). A coupled
`U(1)×U(1)` connection is nameable vocabulary `[ANALOGY]` and rejected as a build.

**Correlation is an output, not a wiring assumption.** `[DERIVED]` Citation arrows point **backward in
time** (a note cites only what already exists); influence flows **forward** — aligned by construction. The
exceptions are **retro-citations**: a citation whose target is *younger* than the source's original
authorship — mintable only through revision (F1 carry-forward + edit), each a witness of
**revision-mediated influence backflow**. Directly measurable today: `reference_edges.sqlite` keys every
edge by `commit_sha` (`reference_edges.py:121–122`) and endpoint times come from git — a deterministic
census, no model. **Ruling: keep `q_cite`/`q_time` independent; the correlation is an INTERPRETED-class
statistic (§2.7), never an axiom.**

### 2.6 Flux ≠ Ricci — the five-row curvature ledger (Q5)

`[capsule Q5]` **False as a theorem, a category error as an analogy.** `[ESTABLISHED: differential
geometry]` Ricci (Forman/Ollivier) is curvature of the **metric/measure** structure; magnetic flux is
curvature of a **U(1) gauge connection** — independent axes (the Einstein–Maxwell slot, where `F`'s
stress-energy only *sources* Ricci). Separation witnesses both ways: `[DERIVED]` **Forman is provably
flux-blind** — `curvature.py:30` binarizes support (`B = (A != 0)`) before `Ric_F`, so `Ric_F(L^{(q)}) ≡
Ric_F(L^{(0)})` while flux ranges freely; **conversely** a directed path graph (flux vacuously 0) with
asymmetric walk rates has nontrivial **directed Ollivier** curvature. The owner's instinct correctly
points at the legitimate "directed Ricci" = the **Ollivier curvature of the directed walk** — the
already-parked **PD-c** (`dn-edge-dynamics` §2.4/§4), a *different, also-real* object the flux is not and
does not approximate.

The salvage (a magnetic Forman via Bochner–Weitzenböck) is **vocabulary only, no customer** — and
conceptually blocked on the flag complex by the Q1 curvature obstruction. **The curvature ledger (extends
Result 3's "same word, different tensors"):**

| curvature | type | base | measures | relation |
|---|---|---|---|---|
| magnetic flux `F = dθ` / `Φ_q` | abelian U(1) 2-form / periods | cycles of one snapshot's directed structure | directed circulation (`X_cite`); gradedness defect (DAG) | `= χ_q∘deg` — abelian character of the transport holonomy (§2.3) |
| superconnection `[d,τ]` | operator-valued, degree 1 | the linear time chain | severed citations (Result 2, exact) | lives on *open* squares — outside flux's domain |
| diamond holonomy / `τ_k` defect | non-abelian groupoid holonomy | note-level fork/merge diamonds | fork/merge incoherence (TA-c) | in `ker(χ_q∘deg)` on balanced diamonds |
| Forman–Ricci (built) | edge scalar, metric | one snapshot's weighted support | bridges/communities (`curvature.py`) | flux-blind (support-only) — independent axis |
| Ollivier–Ricci, incl. directed-walk (deferred PD-c) | edge scalar, metric/measure | a Markov kernel | transport contraction; the true "directed Ricci" | independent of flux (witnesses above) |

### 2.7 What each role earns — the census earns v1; the operator defers (Q6/Q7)

`[capsule Q6/Q7; DERIVED rulings]`

- **(a) Retrieval upgrade (directed Mode-1b diffusion; PD-b/TA-a's "second customer") — earns its math,
  not its build.** Hermiticity forces symmetric magnitudes (`|K_{su}| = |K_{us}|`); direction lives only
  in `arg K_{su}`, so a directed *ranking* needs a **phase→score dictionary that does not yet exist**; and
  hard reachability is already served exactly by Mode 1a's transitive closures. Soft directional nearness
  is tuning-class with **no falsifier until a retrieval eval set exists** (the logic that parked TA-b's
  z-dial). **Re-park with TA-a; re-entry sharpened to the retrieval-eval-set gate (= TA-b's), with the
  phase→score dictionary named as the gate's entry work.**
- **(b) Diagnostic lens — earns a combinatorial v1 that does NOT need the operator.** Exact, deterministic,
  gauge-free, mirror-safe (corpus-structural, embedder-independent): **directed influence cycles** on
  `X_cite` (SCC/cycle enumeration, Tarjan O(V+E)); **unbalanced diamonds** on the supersession DAG
  (arm-length subtraction); **retro-citations** (`commit_sha` + git). None needs a spectrum. The magnetic
  *spectral* version is the parked upgrade, with a **new admissibility pin this pass surfaced:
  eigenvector phases are gauge-DEPENDENT** — only fluxes, magnitudes, and along-edge phase *differences*
  are gauge-invariant, so a spectral lens must narrate gauge-invariant quantities only or it manufactures
  apophenia from an arbitrary gauge choice (`[DERIVED]` — the A7 discriminator's gauge-theoretic instance;
  combinatorial invariants are immune by construction). The census's honest-seam: emits **nothing** when
  no directed cycle / no unbalanced diamond / no retro-citation exists.
- **(c) Unifying structure — earns vocabulary only, mostly prophylactic.** Magnetic Hodge obstructed
  (Q1); flux = diamond holonomy refuted (Q2); flux = directed Ricci false (Q5). What survives is exact and
  worth keeping: flux as literal gauge curvature; the five-row ledger with proved relations; the signed-`L̄`
  = `q=1/2` grounding. **Its value is preventing future category errors.**

**The falsifier inventory (F1–F5) — ready-made for any future graduating plan, none needing new theory:**
`[capsule Q7]`
- **F1 (endpoint):** `spec L^{(0)} == spec L` (and `== hodge.py`'s `L₁` at degree 1 where the complex
  exists) to machine precision.
- **F2 (gauge):** the spectrum is invariant under random gauge transforms `θ ↦ θ + d₀ψ`; any drift is an
  implementation bug by definition.
- **F3 (degree-0 kernel):** `dim ker L₀^{(q)} = #components − #flux-nontrivial-components`, cross-checked
  by independent spanning-tree/cycle-basis flux enumeration `[DERIVED — flat-section; generalizes the
  built signed theorem, laplacian.py:48–53]`.
- **F4 (degree-1 kernel on the Hasse DAG):** `dim ker L₁^{(q)} = Σ_c (β₁(c) − 1 + triv(c))`, cross-checked
  against ripser β₁ (`topology.py:61–67`) + the F3 census — **the magnetic analog of the built
  `dim ker L₁ == ripser` falsifier**, exact and integer-valued.
- **F5 (determinism):** census and spectra byte-identical run-to-run on fixed commits.

## 3. Consequences — what this note decides (on ratification)

**This note licenses no new build.** Its consequences are a *deferral*, a *fold*, and a *vocabulary*:

1. **The operator build is DEFERRED behind three named re-entry gates (any one suffices).** `[capsule Q7]`
   (i) a retrieval eval set exists (role a; = TA-b's gate) **and** the phase→score dictionary is designed;
   (ii) the combinatorial lens proves insufficient — ranking/softness over exact enumeration is
   demonstrably needed (role b; mirrors PD-b's re-entry); (iii) the Thread-C census shows unbalanced
   diamonds / directed cycles are *common* on the real corpus (data warrants the finer instrument; shared
   with TA-c's gate). **Pinned build constraints, recorded now so no future builder re-derives them:**
   Hasse-DAG-only (never the transitive closure), two charges never one (§2.5), home outside
   `core/complex/` (A4/TA-d), `q` generic (recommend **1/4**; `q=1/2` is the polarity-degenerate slot,
   `q=1/3` only the cyclic-triangle motif charge), dense Hermitian `eigh` under a `hodge.py:41`-style size
   guard, **gauge-invariant outputs only**, F1–F5 as acceptance.
2. **The arrow-aware combinatorial census folds into the ALREADY-LICENSED Thread-C sweep** — **no new
   license.** `dn-temporal-retrieval-algebra` §3 item 2 already lists "diamond frequency" verbatim
   (`temporal-retrieval-algebra.md:268–272`); the census adds **arm-length imbalance per diamond**,
   **retro-citation count**, and **`X_cite` SCC/directed-cycle count**. Each result is INTERPRETED-class
   per the inversion (§2.7 / edge-dynamics §2.5). The sweep is the TA-c re-entry gate's instrument anyway,
   and exactly the data that would justify any magnetic re-entry.
3. **The five-row curvature ledger + the F1–F5 inventory are design-tier vocabulary** — prophylactic
   (they kill the "close TA-c with a spectrum" / "flux ≈ directed Ricci" category errors at the note) and
   ready-made §7 material for the day a gate opens.

`dn-edge-dynamics` and `dn-temporal-retrieval-algebra` are cited as ratified/immutable; **no edit to
either** — this note is the magnetic formalization's home, cross-linked from the TA-a park.

## Parked decisions

| id | decision | default recorded | rejected alternatives (why) | re-entry condition |
| --- | --- | --- | --- | --- |
| ML-a | the magnetic **operator** build (`L^{(q)}`) | **DEFER** — census rides Thread-C; math finalized here | build now as infrastructure-ahead-of-need (rejected: elegant, no falsifiable customer — every deliverable it has is exact combinatorics, every deliverable that needs it has no customer) | any of the three §3 item-1 gates (retrieval-eval-set + phase→score; census-insufficiency; census shows common diamonds/cycles) |
| ML-b | the **spectral** census (eigenvector localization; soft/persistent cycles) | combinatorial v1 first (SCC/cycle, arm-imbalance, retro-citation) | spectral now (rejected: gauge-dependent eigenvector phases risk apophenia; combinatorial invariants are gauge-immune) | the combinatorial lens proves insufficient (ML-a gate ii) |
| ML-c | the **phase→score dictionary** for directed-diffusion retrieval | undesigned (no eval set to falsify it) | pick a convention now (rejected: MagNet/Fanuel use phases for embeddings/communities, not asymmetric affinities — unfalsifiable until an eval set) | a retrieval eval set exists (ML-a gate i / TA-b) |
| ML-d | **magnetic Weitzenböck / flux-aware Forman** (Q5 salvage) | vocabulary only | a math pass now (rejected: no curvature customer; blocked by the Q1 obstruction on curved complexes) | a curvature customer appears AND the obstruction is addressed |

## Owner rulings (2026-07-14) + open decisions

- **✓ Adopt the Q7 defer-the-operator ruling (owner decision 1 — RULED, 2026-07-14).** The owner directed:
  *the operator is deferred; the census/formalization is finalized in design.* This note records exactly
  that — the operator build re-parks behind the three gates (ML-a) while the settled math, the census
  design, and the F1–F5 inventory land here. The owner reversed decision-#4's DEFER only to license the
  *math pass* (now done), not to build the operator.

**Open (owner rules at draft → ratified):**

- **Owner decision 2 — dream-narration vocabulary for the arrow-aware census** (directed influence cycles,
  revision-effort asymmetry, retro-citations): does this claim family enter the dreamer's narration, and
  with what language? Extends the standing `dn-edge-dynamics` §5 open question; costs nothing until a lens
  plan exists. *(No recommendation — owner taste.)*
- **Owner decision 3 — covering-only supersession declarations as a checked invariant** (the Q1c rider):
  rule that `supersedes` front-matter declares **covering** relations only (no transitive shortcuts), and
  add the cheap check beside F2 in the A6 list (`recursive-strata-amendment`). Constrains authoring
  practice slightly; keeps the Hasse skeleton triangle-free (which the diamond census also prefers).
  **(Rec: adopt; near-zero cost.)**

## Cross-references

- `docs/brainstorms/magnetic-laplacian-fable-pass.md` — the **warrant**: the full fable derivations
  (Q1–Q7), grades, rejected alternatives, and the steelman-and-reject this note summarizes.
- `docs/brainstorms/magnetic-laplacian.md` — the framing brainstorm that chartered the pass (the seven §3
  questions).
- `docs/design-notes/temporal-retrieval-algebra.md` — ratified; A5 (`E_geom ⊔ E_disp`, do-not-mix), Result
  1–3 (the bicomplex, `[d,τ]`, the superconnection), Result 5, §2.1(ii) (the magnetic Laplacian named),
  §3 item 2 (the Thread-C sweep this census folds into), TA-a (the PD-b re-entry), TA-c (the diamond gate,
  unclosed), TA-d (`core/temporal/` home).
- `docs/design-notes/edge-dynamics.md` — ratified; PD-b (weighted inner products), **PD-c** (the Ollivier
  directed-walk curvature — the true "directed Ricci"), §5 (the dream-narration vocabulary question), the
  inversion / INTERPRETED-class discipline.
- `docs/design-notes/recursive-strata-amendment.md` — the A6 data-integrity invariants (F2; the
  covering-only `supersedes` rider — owner decision 3).
- code: `core/complex/laplacian.py:26–30` (`L^{(0)}` = the built degree-0 operator), `:48–56` (the signed
  `L̄` = the `q=1/2` fiber; the balanced-iff-singular theorem), `core/complex/hodge.py:5–12,41` (the flag
  complex + the dense size guard), `core/complex/curvature.py:9–43` (Forman, provably flux-blind),
  `core/complex/topology.py:61–67` (ripser β₁ — the F4 oracle), `core/stores/reference_edges.py:5–9`
  (the isolation grep), `:121–122` (`commit_sha` — the retro-citation time coordinate).
