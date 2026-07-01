# Builder Prompts — Integrating the Mathematical Reframing
### Self-contained prompts for the Opus-class builder agent (one per session)

**2026-07-01**

Each prompt is a single session's work, in the `BUILDER-PROMPT-FORWARD.md` style: **context → read →
task → constraints → definition of done.** Hand them to the builder one at a time; resume from
`docs/PROGRESS.md`. All preserve the non-negotiables (sealed core, no network in `core/`,
object-capability, flags OFF, trough-only, behavior-preserving except the new-code families). The
recommended order is R0 → R1 → H1–H3 → H4–H7 → H8–H9 → G1–G3 → G4 → G5–G6.

---

## Prompt R0 — Documentation wiring (zero risk, do first)

> **Context.** The mathematical reframing (companions III–IV) is written. Before any code, wire the
> documentation so the whole codebase speaks one vocabulary. This is pure documentation — no runtime
> behavior changes.
>
> **Read.** `docs/MATHEMATICAL-REFRAMING.md` (companion IV, esp. §A the five families, §B.2 the glossary,
> §B.4 the docstring convention), `docs/WHITEPAPER-FORMAL-PROPERTIES.md` (companion II).
>
> **Task.**
> 1. Create `docs/NOTATION.md`: the shared glossary — a table of *symbol ↔ code name ↔ object ↔ family*
>    for every load-bearing symbol (ρ, π_MR, 𝒜, MAX, H, Σ, c, g, d, γ, λ, D(t), B, Θ, 𝔎, K_σ, ℋ, δ*δ).
>    Reference it from the top of each whitepaper.
> 2. Add the three-line `OBJECT / INVARIANT / ENFORCED` docstring header (companion IV §B.4) to each
>    family-1–4 boundary: `core/mirror.py`, `core/provenance.py`, `core/stores/derived.py`,
>    `ops/gate.py`, `scheduler/queue.py`, `eval/drift.py`, `core/research/criteria.py`, the factory scope.
> 3. Regroup the companion II invariant catalog under the five family headings (A.1–A.5).
> 4. Add a one-line family tag to each design note (e.g. *alignment-subsystem → family 4*).
>
> **Constraints.** Documentation only — no code logic changes. Where a docstring's INVARIANT is not
> structurally ENFORCED, say so honestly (the G9–G11 pattern); do not overclaim.
>
> **Done when.** `NOTATION.md` exists and is referenced; every named boundary has the header; companion
> II reads by family; design notes are tagged. The ~480-test suite is unchanged and green.

---

## Prompt R1 — The three small type moves (behavior-preserving)

> **Context.** Three reframings that each *delete an illegal state* (the `MirrorView`/`ProposedChange`
> move). Behavior-preserving; each is a reviewed diff with tests.
>
> **Read.** `docs/REASONING-COMPLEX-MATHEMATICS.md` §2 (hypergraph), §7.2 (the clamp);
> `docs/REASONING-COMPLEX-BUILD.md` §1.2 (schemas); `docs/MATHEMATICAL-REFRAMING.md` §B.1.
>
> **Task.**
> 1. **Hyperedge junction.** Migrate the `DerivedStore` `derived_from` column to the junction schema
>    (`hyperedges` + `hyperedge_nodes(role∈{tail,head})`); today every head-set has size 1. Additive
>    migration; keep acyclicity-at-insert.
> 2. **Confidence clamp.** Make $c=\min\{1,\gamma^{d}g(1+\lambda(|\mathrm{Agr}|-1))\}$ the *single*
>    definition of confidence in `core/recursion.py` and the adjudicator; delete any path that can
>    produce $c>1$ or $c$ rising with depth. (Closes the companion III §7.2 whitepaper tension.)
> 3. **Signed-edge enum.** Introduce `ReversibilityClass`-style enums where free ints/strings encode a
>    closed set — here the edge `sign ∈ {+1,−1}` (used by the new `edges` table, Prompt H1).
>
> **Constraints.** No behavior change (the clamp equals the old value on all currently-produced inputs,
> since today $d=1$ and agreement is bounded). Property tests must still pass; add the monotone-in-depth
> and $c\in[0,1]$ properties.
>
> **Done when.** The junction, clamp, and enum are in; property tests (monotone-in-$d$, $c\le1$) green;
> full suite green; import-firewall green.

---

## Prompt H1–H3 — The reasoning-complex core (the engine's foundation)

> **Context.** Build the foundation of the reasoning complex: the object, the principled clusterer, and
> rigorous contradiction. This is the highest-value, lowest-risk part of strengthening the Dreamer.
> Behind the `DreamerAdapter` seam, dream R&D flag OFF, trough-only.
>
> **Read.** `docs/REASONING-COMPLEX-MATHEMATICS.md` §1–2, §6 (Laplacians, spectral, signed);
> `docs/REASONING-COMPLEX-BUILD.md` §1–3 (data model, computation layer, loop v2); the F9 quality suite.
>
> **Task.**
> - **H1.** The `edges` SQLite table (typed/signed fiber $(t,w,s,\tau)$) + `core/complex/build.py`
>   `build_complex(view: MirrorView) -> ReasoningComplex` — constructs nodes, weighted adjacency `A`,
>   signed adjacency `A_signed`, and the derivation hyperedges. Constructor takes a `MirrorView` so a
>   non-authored complex is unrepresentable (firewall structural).
> - **H2.** `core/complex/laplacian.py` (L, L_sym, signed L̄) + `core/complex/spectral.py` (Fiedler,
>   diffusion map via `scipy.sparse.linalg.eigsh`, spectral/diffusion clustering). Replace the
>   chaining-prone lexical single-linkage clusterer behind the adapter.
> - **H3.** `core/complex/balance.py` — signed spectrum ($\lambda_{\min}(\bar L)$), frustration proxy,
>   and frustrated-triangle enumeration (the specific unresolved tensions).
>
> **Constraints.** `core/complex/` is Zone A, imports no network (import-firewall green). Deterministic
> (fixed seeds). No model call in these modules. Libraries: `scipy`, `scikit-network`; no `graph-tool`.
> All behind the `DreamerAdapter`; the live path calls only the adopted subset.
>
> **Done when.** `build_complex` produces a complex from a `MirrorView`; the diffusion clusterer runs
> and passes F9 non-regression through `MindPalaceDreamerAdapter` (planted-signal recall ≥ lexical
> baseline; noise max-confidence ≤ ceiling); balance module enumerates a planted frustrated triangle;
> new property tests (determinism, spectral stability, frustration correctness) green; full suite green.

---

## Prompt H4–H7 — The structural interpreters

> **Context.** Give the Dreamer real things to reason over: bridges, holes, alignment, and themes with
> confidence. Each is a thin `Claim`-emitter over a `core/complex/` function (R0 panel pattern).
>
> **Read.** `docs/REASONING-COMPLEX-MATHEMATICS.md` §3 (curvature), §4 (topology), §3.5/§6.4 (min-cut),
> §6.2 (SBM); `docs/REASONING-COMPLEX-BUILD.md` §3.2 (the panel).
>
> **Task.**
> - **H4.** `core/complex/curvature.py` — Forman–Ricci (deterministic floor); the `bridge` interpreter
>   ranks the most-negative-curvature edges (surprising cross-domain links). (Ollivier optional, gated.)
> - **H5.** `core/complex/topology.py` — the flag complex + persistent $H_1$ (via `ripser`); the `hole`
>   interpreter surfaces long-lived conceptual holes. **Interpret $H_1$ as holes, never contradictions.**
> - **H6.** `core/complex/cut.py` — min-cut-to-authored + conductance; append the structural axes
>   (frustration, min-conductance) to `eval/drift.py` as additive `Axis` entries (the A2 extension).
> - **H7.** `core/complex/blocks.py` — a degree-corrected SBM (light VEM or `sknetwork`) giving theme
>   membership *with posterior* and a model-selected theme count; the `theme` interpreter. Cross-check
>   against spectral and (optional) Ricci-flow community counts.
>
> **Constraints.** Deterministic; model-free; behind the adapter. Contradiction stays in the signed
> Laplacian (H3) + typed `contradicts` edge — not in $H_1$.
>
> **Done when.** Each interpreter emits grounded `Claim`s; property tests (curvature sign on a planted
> bridge, persistence stability, alignment monotonicity, SBM block recovery) green; the A2 axes appear
> in the drift profile; full suite green.

---

## Prompt H8–H9 — Support propagation & temporal self-watching

> **Context.** Combine multi-path support principledly, and let the system watch its own structure
> evolve — the temporal layer that feeds drift and the longitudinal harness.
>
> **Read.** `docs/REASONING-COMPLEX-MATHEMATICS.md` §6.1 (noisy-OR), §5.4 (temporal); §7 (the pass).
>
> **Task.**
> - **H8.** `core/complex/support.py` — noisy-OR message passing on the derivation DAG (exact on the
>   current polytree) to combine multi-path grounding; feed the adjudicator.
> - **H9.** `core/complex/temporal.py` — write `structural_snapshots` (DuckDB) each trough pass
>   (β₀, Fiedler, frustration, mean curvature, frac-negative-curvature, SBM count, min-conductance,
>   H₁-count); expose drift trajectories to `eval/drift.py`.
> - Restructure `core/dreaming/dreamer.py` into the **loop v2** (build → locate → theme → tension →
>   gaps → support → adjudicate → one earned synthesis → interpreted store → snapshot).
>
> **Constraints.** Deterministic; the single model call is the synthesis step (mirror-not-oracle, over a
> `MirrorView`, grounded). Trough-only.
>
> **Done when.** The loop v2 runs end to end; snapshots persist and drift trajectories compute; the
> synthesis remains the only model call; full suite green; F9 still green.

---

## Prompt G1–G3 — Hands: the type, the gate, read-only sensing (β = 0, safe, parallelizable)

> **Context.** Open the outward boundary at its safest end. Sensing hands are just new sensors; they add
> no action risk. Can run in parallel with Track H.
>
> **Read.** `docs/design-notes/hands-and-the-effector-layer.md` (Track G), esp. §3 (the type), §4 (blast
> radius as a filtration), §6 (the gate), §8 (the audit); `docs/MATHEMATICAL-REFRAMING.md` §A.1.
>
> **Task.**
> - **G1.** The `Effect` / `EffectView` types + `ReversibilityClass` enum. `Effect.__post_init__` raises
>   if a non-SENSING class has no `approval_ref` — an illegal effect is unconstructable (the dual of
>   `MirrorView`). Effects carry no confidence of their own (worth is $u$-like, never read off $c$).
> - **G2.** Generalize the Phase-10 gate: `ProposedChange` → `ProposedEffect`; the guard $G_{\text{effect}}$
>   carries a blast-radius-weighted approval $w(\beta)$ and a scoped-capability check. Same guarded-
>   transition machine, FSM-verified.
> - **G3.** Read-only **sensing** effectors (class 1) in a new `effectors/` surface in the **edge/assistant
>   tier** (never Zone A): sandboxed fetch → de-identified → `observed`-tier view (via the correlator).
>
> **Constraints.** No agent holds a live credential; sensing observations are `observed`-tier and never
> touch the authored mirror; effectors live in edge, not core; skills re-implemented natively, never
> live-installed. Flag OFF by default.
>
> **Done when.** `Effect` deletes the no-approval illegal state (test); the gate generalization is FSM-
> verified; a sensing effector returns `observed`-tier data that provably cannot reach the mirror
> (firewall test); full suite green; import-firewall green (core reaches no network; effectors are edge).

---

## Prompt G4 → G6 — Hands: catalog, then the acting classes (gated; value needs Track H)

> **Context.** Make adding a hand a repeatable reviewed process, then graduate outward — but only after
> sensing (G3) is solid and Track H has produced a model deep enough to tailor actions worth proposing.
>
> **Read.** `docs/design-notes/hands-and-the-effector-layer.md` §5 (what holds), §7 (the Dreamer's model
> tailors the proposal), §8 (the audit), §10 (build order).
>
> **Task.**
> - **G4.** The **effector catalog** + the SKILL-mining pipeline doc: the §8 audit checklist as a
>   repeatable process (read source as untrusted → re-implement natively → classify reversibility → mint
>   scope not credential → sandbox profile → attest → catalog + test).
> - **G5.** **Reversible writes** (class 2): draft an email, add a calendar hold, stage a file. Approval-
>   light. If tailoring in the owner's voice, read a `MirrorView`; the output is a proposal, never a sent
>   artifact.
> - **G6.** **Irreversible / external** (class 3): send, pay, post, actuate. Full gate; JIT short-TTL
>   scoped Vault credential minted *at the moment of action*; attested action record.
> - **G7.** A blast-radius drift `Axis` — effector reach watched against a frozen anchor.
>
> **Constraints.** You do not get a class until the one below is solid (the blast-radius filtration).
> Every irreversible effect is human-gated and attested; the credential is minted per-action, never
> held. Flag OFF; owner-activated.
>
> **Done when.** The catalog + pipeline doc exist; class-2 effectors propose (never send) with a
> `MirrorView` tailoring read; class-3 effectors are fully gated with JIT scoped credentials and attested
> records; the blast-radius axis reports; property tests (gate-weight monotone in $\beta$, unconstructable-
> without-approval, observations observed-tier) green; full suite green.

---

*Hand these to the builder one at a time, resuming from `docs/PROGRESS.md`. R0 and R1 are zero/low-risk
and come first; H1–H3 is the engine's critical path; G1–G3 (sensing) is safe and parallelizable; the
acting hands (G5–G6) come after the engine is deep. Keep every flag OFF until a deliberate session.*
