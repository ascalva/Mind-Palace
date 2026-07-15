# Journal — bp-037 `CQ-wire`: `TemporalView` (β₁ citation threads)

> The fresh-agent contract: a new session with only `plan.md` + this journal + the write-scope files
> must continue without re-asking. Checkpoint at every semantic boundary (criterion closed, commit,
> finding filed). Status flips are the orchestrator's, by hand.

## 2026-07-15 — GRADUATED (proposed), awaiting owner `proposed→ready` blessing

- Graduated by the orchestrator (opus) from ratified `dn-core-query-protocol` §3 C5 + bp-035 §12 item 3.
  Grounded pass done in-session: read the built `core/temporal/{complex,operators,superconnection,
  boundary}.py`, the sibling `core/reference_view.py`, the store API, and `test_temporal_complex.py`.
- **Key grounding finding (§3 Q2):** `build_citation_complex` is NOT commit-anchored (`complex.py:66`
  calls `all(direction="corpus_to_corpus")` with no commit filter) → today's `X_cite` is the all-history
  union. Item 1 fixes this additively (`commit` kwarg, default None = unchanged).
- **Scope decision (§0/§12):** the built surface bifurcates single-snapshot (`complex.py`, β₁ — THIS
  plan) vs two-snapshot (`operators`/`superconnection`/`boundary`, `‖[d,τ]‖` — `CQ-wire-2`, a follow-on
  gated on this so its upstream `TemporalView` interface is built, not inferred). The note's open "what
  answer, to whom?" → **a `TemporalView`** (read-surface sibling to `ReferenceView`; NOT a dreamer lens —
  that's the gated `DD-1`).
- **Not started** — no code written; this is a `proposed` plan. Owner blesses `proposed→ready` by hand,
  then `/build bp-037` (opus, self-driven; no fable, no delegation — week at 89%, budget-tight).

## 2026-07-15 — BUILD started (self-driven, orchestrator-as-builder); Item 1 GREEN

- Owner blessed `proposed→ready`; flipped `ready→in-progress`, active-plan pointer set.
- **Item 1 CLOSED** — `build_citation_complex(ref_store, *, commit=None)` additive kwarg
  (`core/temporal/complex.py`): `commit=None` = all-history union (unchanged); `commit=<sha>` filters
  `corpus_to_corpus` edges by `commit_sha`. Pure-Python filter over already-read rows — no new import,
  no store-API change, isolation untouched. 2 new tests in `test_temporal_complex.py`
  (`test_commit_anchor_filters_to_one_snapshot`, `test_commit_none_is_the_all_history_union_unchanged`):
  a 4-cycle at c1 + dup a→b + lone e→f at c2 → anchor sees only its slice, union dedups. **12 passed**
  (10 pre-existing unchanged + 2 new). Falsifier held: c2 edges don't leak into the c1 snapshot.
- Next: Item 2 (`TemporalView` + `open_temporal_view`), Item 3 (live β₁ vs ripser).

## 2026-07-15 — Items 2 + 3 GREEN; all 3 items closed; running the full gate

- **Item 2 CLOSED** — `core/temporal_view.py`: `TemporalView` (frozen dataclass holding the eagerly-
  assembled `CitationComplex` + anchor `commit`; NO store handle retained) + `open_temporal_view`
  factory (reuses `core.reference_view._resolve_default_commit` so both Views anchor "now" identically).
  Reads: `citation_threads()` (β₁), `boundary_composition_is_zero()` (∂₁∂₂=0), `n_nodes`/`n_edges`.
  `tests/unit/test_temporal_view.py` — 5 tests: 4-cycle→β₁=1, filled-triangle→0, anchor scopes to one
  commit (falsifier: c2 doesn't leak into c1), empty-anchor honest, scope-leak guard (no
  store/`add_batch`/`_conn`/`all` reachable; `vars(view)=={_complex,commit}`). **5 passed.**
- **Item 3 CLOSED** — `tests/integration/test_temporal_view_live.py`: β₁ on the LIVE store @ HEAD,
  computed two independent ways (Hodge `dim_ker_L1` via the view vs ripser H₁ @ t=0) — **assert equal**;
  skip-with-reason if no corpus→corpus edges at the anchor (environmental, mirrors bp-035). **1 passed.**
  **LIVE RESULT** (HEAD `a18fe187`): **β₁ = 24** (both methods agree), n_nodes=110, n_edges=217,
  ∂₁∂₂=0 True. The corpus carries 24 independent citation threads — the algebra's first live number.
- Next: full 5-leg gate (ruff / mypy typed==0 / argless mypy re-baseline / type_gate / pytest), then
  flip in-progress→complete + seal.

## 2026-07-15 — GATE: legs 1–4 GREEN; leg 5 (full pytest) running

- **Leg 1 ruff:** pass (reflowed several docstring/comment lines to ≤100 after an initial E501 batch —
  cosmetic only, no logic touched).
- **Leg 2 mypy typed** (`core agents eval ops scheduler scripts`): **0 issues, 186 files** (185→186,
  the new `core/temporal_view.py`).
- **Leg 3 argless mypy:** **69** (checked 378 files) — UNCHANGED from baseline; the 2 new test files
  introduced zero new type errors (the new-tests tooth holds at 69, no re-baseline needed).
- **Leg 4 `ops.type_gate`:** OK (tier-2 membership + bare-ignore scan both pass).
- **Leg 5 pytest -q:** backgrounded (~10–13 min); expect baseline 1123 + 8 new (5 view + 2 complex +
  1 live) = 1131 passed / 9 skipped. Tolerate ONLY the 2 live-e2e flakes on a loaded box.
- Then: flip in-progress→complete + seal (cost.actual — owner /usage relay for the $ deltas).

## 2026-07-15 — COMPLETE. All 5 legs green; sealed. β₁ = 24 live.

- **Leg 5 pytest:** **1131 passed / 7 skipped / 2 failed** (9:40). The 2 failures = the known-flaky
  live-model dream e2e (`test_dream_v2_live`, `test_dreaming_live`, `TimeoutError` on a loaded box) —
  the ONLY tolerated ones (resume brief); unrelated to citation-complex code. All 8 new tests pass.
- **All 3 items closed + verified.** The temporal algebra has its first live consumer: `TemporalView`
  answers β₁ = **24** independent citation threads over the corpus reference graph @ HEAD (Hodge ==
  ripser, cross-verified), n_nodes=110, n_edges=217, ∂₁∂₂=0.
- **Flipped in-progress→complete**; cost.actual filled (self-driven opus, ~0.55× est; $ deltas pending
  the next owner /usage relay). PROGRESS.md checkpointed; active-plan cleared.
- **CQ-wire-2 grounding banked** (probed live during the gate): the store holds **435 distinct commits**
  carrying corpus→corpus edges (~320/commit) — so the two-snapshot `‖[d,τ]‖` comparison is NOT
  data-starved; consecutive commits give real citation-graph deltas. Feeds the CQ-wire-2 §3 pass.

### Re-entry (for the builder — HISTORICAL; plan is COMPLETE)
- Start at **Item 1** (`core/temporal/complex.py` commit kwarg) — lowest blast radius, unblocks Items 2/3.
- Mirror `ReferenceView` EXACTLY for the View shape + anchor resolution (`reference_view.py:47,60,111,129`).
- The green gate: ruff; `mypy core agents eval ops scheduler scripts`==0; argless `mypy`==69 (the
  new-tests tooth — assert it, will rise with the two new test files); `ops.type_gate`; `pytest -q`
  (baseline 1123 passed / 9 skipped — the 2 live e2e may flake on a loaded box; tolerate only those).
