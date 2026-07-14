# bp-033 journal

## 2026-07-14 — authored `proposed` (orchestrator, opus/xhigh graduation)

Graduated from `dn-temporal-retrieval-algebra` §3 Consequence 1 — the **temporal-transport half** of the
`core/temporal/` module: `π_active`, `σ_*`/`σ^*`, and the superconnection curvature `‖[d,τ]‖`. Split from
bp-032 (the topological half) because the objective carried an "and" and each half has an independent
runnable falsifier. **`depends_on: bp-032`** — consumes its `X_cite` assembler + boundary maps +
two-snapshot accessor (honored, not redesigned; an API change is a stop-and-raise → re-graduate bp-032).

**Grounded pass (citations in §3):** the operator definitions + laws come from the note §2.2–§2.3 (A2:
`π_active` = the ambient default projection, idempotent contraction, NOT a chain map; `σ_*` = the opt-in
chain map, degree 0, chain-map iff F1; `σ^*` = the pullback, always a contraction, the Sz.-Nagy dilation
pin). `‖[d,τ]‖` = the **exact** severed-citation-carry-forward count (Result 2, tight — "not a proxy"),
so the check is the operator value vs the discrete count (inversion Rule 2). σ is induced by the
supersession correspondence (`versions.supersessions`, `reference_edges.for_commit`).

**Scoped to the LINEAR CHAIN only** — fork/merge diamonds (σ not single-valued) are TA-c (SKETCH,
data-gated on measured diamond frequency); a diamond is a stop-and-raise, never a silently-averaged σ.
Combinatorial v1 (inherits bp-032's unweighted `A_cite`); asserts only the topological chain-map law, not
metric/kernel coherence (Result 4 / PD-b / TA-a, deferred).

**write_scope** = `core/temporal/**` + one NEW test path (`test_temporal_operators.py`) — clean
(finding-0075). Item numbering continues the family (9–12). Estimate opus/400k. Awaiting the owner-only
`proposed → ready` blessing; **do not build before bp-032 (and bp-031) land.** No code written.

## 2026-07-14 — blessed `proposed → ready` (owner, by hand); orchestrator commits the flip

Owner hand-blessed bp-033 (with bp-031/032) `proposed → ready`. Orchestrator commits the flip (rule 0060).
**`depends_on: bp-032` binds — DO NOT `/build` bp-033 before bp-032 lands** (it consumes bp-032's module
API). Build order is strict: bp-031 → bp-032 → bp-033. No code written yet.

## 2026-07-14 — `/build` START + Items 9–12 COMPLETE (bp-032 landed; opus/high, orchestrator-driven)

bp-032 sealed (`07686fb`) → dependency satisfied. Same session (built bp-031 + bp-032 already), so
bp-032's `CitationComplex` shape + hodge boundary reuse are in hand; re-read the bp-033 plan §6/§8 (the
operator laws) and confirmed the `[d,τ]` closed form by DERIVATION: with `τ = σ^*`, `[d,τ]φ = d(σ^*φ) −
σ^*(dφ)` telescopes to `(φ(σv) − φ(σu))·𝟙[{σu,σv} ∉ X_{n+1}]` — EXACTLY the note's Result 2. So the
operators are the note's, verified, not inferred.

**API-change check (§10):** bp-033 ADDS `operators.py` + `superconnection.py` to `core/temporal/` (its own
write_scope) consuming bp-032's EXISTING public functions (`build_citation_complex`, `CitationComplex`,
hodge's `boundary_1`) — no bp-032 signature redesigned. The "two-snapshot accessor / active-subspace basis"
bp-033 §6 anticipated become small NEW helpers here (`sigma_node_map`, `active_projection`), derived from
bp-032's `CitationComplex` — additive, so NO stop-and-raise (the §10 trigger is *changing* bp-032's contract).

**Item 9 — π_active** (`operators.py`): `active_projection(cx, superseded)` = the diagonal 0/1 projection
onto not-yet-superseded nodes. Idempotent, contraction, annihilates superseded; a test proves it is NOT a
chain map (`Π_edge δ⁰ ≠ δ⁰ Π_node` when an edge joins an active + superseded node).

**Item 10 — σ_*/σ^*** (`operators.py`): `sigma_node_map` resolves σ by note id (raises `DiamondError` on a
merge — non-injective, §10/TA-c; `ValueError` on a non-total σ). `pushforward_0/1` = σ_* on 0-/1-chains
(a severed edge → zero column); `is_chain_map` checks `∂_{n+1}σ_*¹ == σ_*⁰∂_n` (TRUE iff F1); `pullback_0`
= σ^* (contraction). Edge indexing matches hodge's `edge_index` (both sort `(u,v)`, `u<v`) so `boundary_1`
columns align with `cx.edges`.

**Item 11 — ‖[d,τ]‖** (`superconnection.py`): `severed_citations` / `curvature` (the `[d,τ]` matrix
`C⁰(X_{n+1})→C¹(X_n)`) / `curvature_norm` (= the severed count) / `is_flat`. The Item-11 acceptance: on a
known-severed fixture `curvature_norm == the direct Σ𝟙[severed] == 1` and the matrix is supported on exactly
that edge's row; on an all-carry-forward fixture `[d,τ] = 0` (flat, the bicomplex case).

**Item 12 — T_active** (`operators.py`): `t_active = Π_active ∘ σ_*⁰` — a contraction (`‖T_active‖ ≤ 1`).

**Fixtures (hand-verified):** X_n = 4-cycle `a-b-c-d-a` (all 4 nodes); F1 = same cycle; SEVERED = drop
`d-a` → path (nodes persist, `{d,a}` severed); diamond = `σ(a)=σ(b)=x`. σ = identity on rename-stable ids.

**Gate (5 legs, separate):** ruff ✓; mypy strict floor **0** (182 files); argless mypy **69**; type_gate ✓;
the 9 new tests green. **Full `pytest -q` running** (leg 5). Next: seal on green + diff vs write_scope + flip.

## 2026-07-14 — SEAL: bp-033 COMPLETE (in-progress → complete) — the temporal chain is CLOSED

**All 4 items landed; the temporal-transport half is built.** `π_active`, `σ_*`/`σ^*`, `‖[d,τ]‖`, and
`T_active` — the mode-3 operators over `X_cite`, each carrying the note's operator laws as runnable checks.
**With bp-032, dn-temporal-retrieval-algebra §3 Consequence 1 is fully realized** (the topological +
transport halves). bp-031→032→033 all sealed this session.

**Diff vs write_scope — CLEAN.** Added `core/temporal/operators.py` + `core/temporal/superconnection.py`
+ export-only edits to `core/temporal/__init__.py` + `tests/unit/test_temporal_operators.py` — all in
`write_scope`. **bp-032's `complex.py`/`boundary.py` were NOT edited** (public API honored, §5/§10). No
out-of-scope write.

**5-leg gate:** ruff ✓ · mypy strict floor **0** (182 files) · argless mypy **69** · type_gate ✓ ·
`pytest -q` = **1055 passed, 8 skipped** — a CLEAN full run (the bp-032-era e2e scheduler flake did not
recur).

**Verification (the /verify obligation):** the operator laws ARE the end-to-end drive — the chain-map law
`σ_* ∂ = ∂ σ_*` verified TRUE under F1 and FALSE on a severed-citation fixture (the honest negative);
`‖[d,τ]‖ == the discrete severed count` (Result 2, "not a proxy") on a known-severed fixture, and `[d,τ]=0`
(flat) when all citations carry forward; `π_active` idempotent+contraction and demonstrably NOT a chain map;
`σ^*`/`T_active` contractions; a merge diamond raises `DiamondError` (§10/TA-c).

**Cost:** est opus/400k; actual ≈60k (ratio ≈0.15, operators over a landed module, laws pre-derived).
dollars/deltas **pending the owner's next /usage relay** (bp-032's seal read $19.02 session-total, 39%/80%).
Single-lane, 0 subagents.

**⭐ DOWNSTREAM UNBLOCKED (does NOT auto-graduate — design-tier, gated):** with the `core/temporal/` module
concrete, the empirical **Thread-C sweep + arrow-aware census** (note §3 Consequence 2) and the **`K(β)`
retrieval curve** (Consequence 3, TA-b) can each graduate. Both are separate design/graduate steps, not
this session's work.
