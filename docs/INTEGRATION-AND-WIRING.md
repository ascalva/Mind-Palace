# Integration & Wiring Guide
### How the mathematical reframing lands in the repo, the stores, and the build order

**2026-07-01**

This ties the four new documents into the running system: where each doc lives, how the new code wires
into the existing stores and seams, the order across the Dreamer (Track H) and the hands (Track G), and
the guardrails. Nothing here flips a flag; every step except the new-code families is behavior-preserving.

---

## 1. The document set (where each goes)

| Doc | Companion | Role | Repo location |
|---|---|---|---|
| `WHITEPAPER.md` | I | philosophy / the DNA | `docs/` *(exists, unchanged)* |
| `WHITEPAPER-FORMAL-PROPERTIES.md` | II | verification plan (invariants, tiers) | `docs/` *(exists; regroup by family — §5)* |
| `REASONING-COMPLEX-MATHEMATICS.md` | III | the reasoning complex (the engine, math) | `docs/` *(new)* |
| `REASONING-COMPLEX-BUILD.md` | III | the buildable spec for the complex | `docs/` *(new)* |
| `MATHEMATICAL-REFRAMING.md` | IV | unified account + reframing direction | `docs/` *(new)* |
| `hands-and-the-effector-layer.md` | — (Track G note) | the effector layer, reframed | `docs/design-notes/` *(new/updated)* |
| `NOTATION.md` | — (shared) | the symbol ↔ code ↔ object glossary | `docs/` *(new — build first)* |

`WHITEPAPER-DREAMER-MATHEMATICS.md` (the 0.1 audit/errata) is **superseded** by companion III v0.2;
keep it in `docs/archive/` for the errata history, marked superseded.

---

## 2. The two dual boundaries (the wiring, conceptually)

Everything wires around the two boundary operators of family 1 — read-flow in, action-flow out — with
the reasoning complex between them:

```
   WORLD ──raw bytes──►  INGEST (H, ρ)  ──►  RAW STORE (immutable) ──f──► DERIVED (regenerable)
                                                                              │
                                          ┌───────────────────────────────────┘
                                          ▼
                        REASONING COMPLEX 𝔎  (family 5: Laplacians, curvature, persistence, SBM)
                          built ONLY from MirrorView  ← firewall (observed ↛ mirror), structural
                                          │
                                          ▼
                        DREAMER model (bridges / tensions / themes, over time)
                                          │  read via MirrorView (authored-only)
                                          ▼
                        AMBASSADOR / EFFECTOR  → composes a PROPOSAL (never a sent artifact)
                                          │  ProposedEffect
                                          ▼
                        GATE G_effect (family 3) + blast-radius weight (family 4)
                                          │  ── owner approves ──►  code acts
                                          ▼
                        WORLD  ── observations return ──►  observed-tier (family 1, ↛ mirror)
```

`MirrorView` and `EffectView` are the two typed boundaries; the complex and the gate are what sit
between them. **The whole integration is: strengthen the middle (Track H), then open the right boundary
(Track G), under the two flow constraints that already exist.**

---

## 3. Code wiring — the reasoning complex (Track H)

New namespace `core/complex/` (Zone A, reaches no network — import-firewall must stay green). It wires
to the existing seams as follows:

| New module | Wires into | How |
|---|---|---|
| `core/complex/build.py` | `core/mirror.MirrorView`, `VectorStore`, `edges` table, `DerivedStore` | assembles `ReasoningComplex` from an authored-only view — firewall structural at construction |
| `core/complex/{laplacian,spectral,curvature,balance,topology,cut,blocks,support}.py` | `ReasoningComplex` | pure deterministic functions; no model call |
| `core/complex/temporal.py` | DuckDB `structural_snapshots` (new) → `eval/drift.py` | writes structural-invariant time series; A2 axes feed the drift `Profile` |
| `core/dreaming/dreamer.py` (loop v2) | the above via the `DreamerAdapter` seam; `DerivedStore`; `StoreAttestor` | one earned model call (narration); interpreted-only writes; attested chains |
| `core/dreaming/interpreters.py` | `core/complex/*` | each interpreter is a thin `Claim`-emitter over a complex function (R0 pattern, real instruments) |

**Three small type moves** (behavior-preserving, each a reviewed diff; companions III–IV):
- `derived_from` column → the **hyperedge junction** (`hyperedges` + `hyperedge_nodes`).
- the **confidence clamp** $c=\min\{1,\gamma^{d}g(1+\lambda(|\mathrm{Agr}|-1))\}$ as the *single*
  definition of $c$ in `core/recursion.py` + the adjudicator.
- the **signed-edge polarity enum** (`sign ∈ {+1,−1}` as a type, in the new `edges` table).

**Store deltas:** one new SQLite `edges` table (typed/signed fiber), the `DerivedStore` junction
generalization (additive migration), one new DuckDB `structural_snapshots` table. Everything else
recomputes from vectors on the trough — the complex is derived and regenerable.

**Scheduler:** all of it is trough-only (`HEAVY_TIERS`, foreground gate); the complex rebuilds on the
`dream`/`curate` cron jobs; snapshots on the same cadence.

---

## 4. Code wiring — the hands (Track G)

New surface `effectors/` in the **edge/assistant tier** (never Zone A). Wires to:

| New piece | Wires into | How |
|---|---|---|
| `Effect` / `EffectView` / `ReversibilityClass` | (new types) | illegal states unrepresentable — the `MirrorView`/`ProposedChange` move, dual direction |
| `ProposedEffect` gate | `ops/gate.py` (generalize `ProposedChange`) | same guarded-transition machine, wider domain, blast-radius-weighted approval |
| per-effect capability | the **Vault scoped-token mechanism** (already wired) | mints scope ("send one email to X"), short-TTL, at the moment of action — never a held credential |
| sensing effectors (class 1) | the **correlator** / `observed`-tier ingest | sandboxed fetch → de-identified → observed view; never the authored mirror |
| tailoring read (if any) | `core/mirror.MirrorView` | authored-only; output is a proposal, never a sent artifact |
| blast-radius drift axis | `eval/drift.py` | effector reach becomes a measured trajectory (A2) |

**The connection to Track H:** the effector's tailoring read is the Dreamer's model (via `MirrorView`).
Track G's *acting* classes (G5–G6) deliver value only when Track H has produced a model deep enough to
tailor actions worth proposing.

---

## 5. Documentation wiring

1. **`docs/NOTATION.md` first** — the glossary (companion IV §B.2). Zero risk, highest leverage; every
   whitepaper and boundary docstring references it.
2. **Boundary docstrings** (companion IV §B.4) — the three-line `OBJECT / INVARIANT / ENFORCED` header
   at each family instance. Surfaces any notation-outruns-enforcement gaps honestly (the G9–G11 pattern).
3. **Regroup companion II by the five families** (companion IV §A) — the invariant catalog as "objects
   and their guarantees," not a flat list.
4. **Tag design notes** with their family (e.g. *alignment-subsystem → family 4*; *hands → family 1 dual
   + family 4 metric*). Tag, don't rewrite.

---

## 6. The recommended sequence (across both tracks)

Ordered by (value ÷ risk), respecting one-item-per-checkpoint and flags-OFF:

```
 Phase R0  (docs, zero risk)     NOTATION.md → boundary docstrings → regroup companion II → tag notes
 Phase R1  (small type moves)    derived_from→junction · c-clamp · signed-edge enum   [behavior-preserving]
 Phase H1–H3 (engine core)       edges+build_complex · spectral/diffusion clusterer · signed Laplacian
 Phase H4–H7 (interpreters)      Forman curvature · persistence · min-cut→A2 · SBM
 Phase H8–H9 (support+temporal)  noisy-OR · structural snapshots → drift trajectories
 Phase G1–G3 (hands, β=0)        Effect type · ProposedEffect gate · read-only sensing    [safe, parallelizable]
 Phase G4    (process)           effector catalog + SKILL-mining pipeline
 Phase G5–G6 (hands, acting)     reversible writes → irreversible/external               [gated; value needs H]
 Phase G7    (watch)             blast-radius drift axis
```

**Parallelism:** R0/R1 and H1–H3 are the critical path (they strengthen the weak spot). G1–G3 (sensing,
$\beta=0$) can run in parallel — it is safe and adds sensors. The *acting* hands (G5–G6) come after the
engine is deep, because that is what makes them worth building.

---

## 7. Validation wiring

- **F9 non-regression** — the new clusterer runs through `MindPalaceDreamerAdapter`; `tests/quality/`
  must stay green against the lexical baseline (planted-signal recall ≥ baseline; noise max-confidence ≤
  ceiling; grounding faithfulness under full-support ablation).
- **New property tests** (companion III §10.1 / build §6.1) — determinism, spectral stability,
  persistence stability, frustration correctness, curvature sign, alignment monotonicity, SBM recovery,
  and the $b\gamma<1$ recursion guard.
- **Effector property tests** (hands §8) — unconstructable-without-approval, gate-weight-monotone-in-$\beta$,
  observations-are-observed-tier.
- **Drift A2 axes** — frustration, min-conductance, curvature stats, and effector blast-radius, all
  appended to `eval/drift.py` as additive `Axis` entries against the frozen anchor.
- **The test ratchet** — the ~480-test suite is green before and after every R0/R1 step; new families
  add tests, never regress the base.

---

## 8. Guardrails (the discipline, restated)

- **Type only where it deletes an illegal state; else docstring; else leave it.** No aesthetic renames.
- **Notation never outruns enforcement** — a stated INVARIANT the code doesn't ENFORCE is recorded as an
  honest gap, not pretended into a type.
- **Behavior-preserving** except the new families (H, G); the flag stays OFF until a deliberate session.
- **The firewall and the gate are the two boundaries** — nothing crosses either without its typed
  constraint. Observed never reaches the mirror; no effect reaches the world without the gate.
- **Engine before hands** — Track H is the precondition for Track G's acting classes delivering value.

*Wire the glossary and the docstrings first (zero risk), then the small type moves, then the engine
(H1–H3), then the hands from the reversible end. Everything behind the adapter and the gate, flags OFF.*
