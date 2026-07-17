# Journal — bp-059 (σ*/MST, the keystone)

## 2026-07-17 — graduated (proposed), not yet started
Minted by /graduate from RATIFIED `dn-connectivity-instruments` CN-1 + CN-2. Status `proposed` —
awaits the owner's `proposed → ready` blessing (owner-only, by hand).

**Grounding carried in the plan (so a fresh builder needn't re-derive):**
- `MirrorGraph.build(view, *, sigma)` takes **NO cut** (`core/dreaming/graph.py:32-40`); `MirrorView`
  has **no cut-restriction surface** (`core/mirror.py:96-105`). Resolution: v1 pins to the **latest
  cut** via `spine.cut_at(strata=frozenset({"mirror"}))`, recorded in `ConnEvidence`; historical
  cut-restriction is PARKED (§11 — a future `core/` plan).
- σ* falsifiers are structural (ultrametric inequality; MST≡union-find), **not** a recall signal —
  finding-0096 established golden_recall saturates at this scale; do NOT couple σ* to recall.
- Evidence pinning copies the `FibersEvidence` pattern (`eval/harness/fibers.py:112-133`).

**Next action when built:** item 1 (CN-1 scaffolding) → item 2 (MST/σ*) → item 3 (entry point +
quality battery). 3-item serial. Estimate opus/180k.

## 2026-07-17 — build session START (opus/high), context manifest loaded
Flipped `ready → in-progress` (`a5da95f` was the blessing). §2 manifest read in full: design note
(CN-1/CN-2 + the two σ* falsifiers), `MirrorGraph` (`sim` full cosine + `_adj`/`neighbors` at σ;
NO cut arg), `cluster.similarity_matrix` (L2-normed pairwise cosine), `MirrorView` (Invariant-6;
`project(RowSource)`; no cut surface), `spine` (`cut_at(strata=frozenset({"mirror"}))` needs only
`CutSources.commit_sha` → `Certificate.COMMIT`; `crossing_edges` legality tooth; `downset`),
`fibers.FibersEvidence` (the evidence-pin pattern to copy verbatim), `store` (`EvalKey`/`Reading`/
`put` idempotent-by-key).

**Test-fixture paths located (reuse, don't reinvent):**
- Certified mirror cut: `tests/unit/test_cuts.py` — `Spine.derive(SpineSources(versions=vs),
  cut_sources=CutSources(commit_sha="c0"))` then `cut_at(strata=frozenset({"mirror"}))`. A mirror
  cut needs ONLY commit_sha (no trough/handoff). `commit=None` ⇒ `CutCertificateError` (the item-1
  refusal falsifier).
- `MirrorView` over a fake `RowSource`: `tests/unit/test_complex.py::_Rows` — rows are dicts
  `{digest,title,vector,text,provenance=AUTHORED_SOLO.value}`; `MirrorView.project(_Rows(rows))`.

**Registration decision (fibers precedent, explicit):** `put()` does NOT gate on registration
(store.py has no registry import); `registry.py` is OUT of write_scope. So — exactly as FB-1 wrote
`sigma_persistence.*` before bp-054 registered them — this instrument emits `sigma_star.*` readings
now; registering them + the `SigmaStar` type_tag is a separate future act (a bp-054-style companion),
recorded here so it never reads as a violation. `test_registry_res.py` checks registry contents, not
a dynamic emit, so unregistered `sigma_star.*` breaks no existing test.

Now writing `eval/harness/connectivity.py` (whole module — items 1–3 are one cohesive surface),
then unit tests (items 1–2) → quality battery (item 3), gating + journaling at each boundary.

## 2026-07-17 — items 1–3 COMPLETE, 5-leg gate GREEN
Built the whole module `eval/harness/connectivity.py` + `tests/unit/test_connectivity.py` (items 1–2)
+ `tests/quality/test_connectivity_sigma_star.py` (item 3). All three §7 acceptance tests pass.

**What landed (the load-bearing surface bp-060/061/062 import):**
- **Item 1 — CN-1 scaffolding.** `ConnIndex(grid, cut)` (declares σ* uses (grid, cut), no t);
  `ConnEvidence(grid, base_fingerprint, cut_fingerprint)` with `as_ref()` (the FibersEvidence pattern
  copied verbatim, stable sort_keys JSON); `acquire_mirror_cut(spine)` →
  `spine.cut_at(strata=frozenset({"mirror"}))`, lets `CutCertificateError` PROPAGATE (fail-closed),
  asserts the CN-1 legality tooth (`crossing_edges == []` ⇒ else `CrossingEdgeError`); `cut_fingerprint`
  hashes frontier+certificates+evidence (never wall-time — Law C4; module reads no clock).
- **Item 2 — MST + σ*.** `build_max_spanning_tree(graph)` (Kruskal descending, O(E log V), a FOREST
  when the loosest-grid graph is disconnected); `sigma_star(forest, a, b, *, grid)` → grid-snapped
  bottleneck + realizing MST chain, `None/()` when "not connected within grid". Both falsifiers pass:
  ultrametric inequality on real triples + **MST ≡ union-find** on every pair (independent oracle in
  the test).
- **Item 3 — entry + readings.** `run_connectivity(*, view, spine, grid, eval_store, base_fingerprint)`
  builds at `min(grid)`, acquires the cut FIRST (fail-closed before graph work), writes `sigma_star.*`
  aggregates (mean/p50/max over connected + always frac_connected/n_pairs) keyed idempotently with the
  `ConnEvidence` ref. n≤1 → no readings, noted. Grid-relativity is observable (bridged two-cluster
  fixture: cross pair connects at loose grid, "not connected within grid" at tight).

**Design decisions journaled (no design edits — builder posture; none rose to a finding):**
- **corpus_ref** = `conn:` + sha256 of the sorted node digests (the store's corpus-growth confound
  key; the base_fingerprint param carries the config/embedding regime, cut_fingerprint the history).
- **SigmaStar kept minimal** (a, b, sigma_star, chain) exactly per the §6 pin — the pre-snap bottleneck
  stays internal (grid-snapped is the honest answer); the chain-realizability falsifier recomputes it
  test-side. If bp-060 needs the raw bottleneck it files a finding.
- **_SNAP_EPS=1e-12** guards grid-snap against float noise at an exact grid point.

**5-leg gate (each run separately, diff vs merge-base c14d6a4):**
- ruff: clean (hand-wrapped all docstrings to ≤100).
- mypy targeted (the 3 files): **0**.
- argless mypy: **69** — baseline held, my files add 0.
- type_gate (`test_type_gate.py`): **11 passed**.
- pytest not-live (`-m 'not live and not podman and not needs_vault and not needs_restic'`):
  **1454 passed, 4 skipped, 0 failed** (+16 new: 10 unit + 6 quality).

**Next:** orchestrator-side — flip status → complete, seal cost.actual, clear the pointer, commit,
update PROGRESS + resume-brief. Then owner blesses bp-060 (amended per finding-0099) → build.
