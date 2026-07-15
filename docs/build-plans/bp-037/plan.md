---
type: build-plan
id: bp-037
alias: CQ-wire
status: proposed
design_ref:
  - docs/design-notes/core-query-protocol.md
  - docs/design-notes/temporal-retrieval-algebra.md
contract: builder
write_scope:
  - core/temporal_view.py
  - tests/unit/test_temporal_view.py
  - core/temporal/complex.py
  - tests/unit/test_temporal_complex.py
  - tests/integration/test_temporal_view_live.py
session_budget: 1
cost:
  estimate:
    model: opus
    tokens: 180k
    rationale: >-
      Read-only / additive engineering over a settled, test-pinned surface (`core/temporal/complex.py`
      is built + graded). Mirrors bp-035 (250k est / 145k actual, delegated) but SMALLER: one View,
      β₁ only, no `connected_set` BFS, no repo-grep oracle to write (the ripser β₁ cross-check already
      exists — Item 3 re-runs it on live data). Self-driven this session lands ~0.5–0.8× (budget-tight,
      week 89%). No fable (the math is banked theorem-grade in `dn-temporal-retrieval-algebra`).
  actual: null
depends_on: []
parallelizable_with: []
created: 2026-07-15
updated: 2026-07-15
links:
  - docs/design-notes/core-query-protocol.md
  - docs/design-notes/temporal-retrieval-algebra.md
  - docs/build-plans/bp-035/plan.md
  - core/reference_view.py
  - core/temporal/complex.py
  - core/stores/reference_edges.py
re_entry: null
supersedes: null
superseded_by: null
warrant: null
---

# Build Plan — `CQ-wire` (bp-037): `TemporalView` — the algebra's first live consumer (β₁ citation threads)

> **Every section below is required.** Inapplicable sections are marked `N/A — <reason>`.

## 0. Mode & provenance

Graduated from ratified `dn-core-query-protocol` §3 Consequence 5 + bp-035 §12 item 3 (named verbatim:
*"Wiring `core/temporal` into a query answer — X_cite β₁ threads … the algebra's first production
consumer beyond tests"*). The math successor `dn-temporal-retrieval-algebra` §3 is the theorem-grade
home of `X_cite`; this plan does not re-derive it — it **wires the built, test-pinned `core/temporal/
complex.py` into a live read surface** so something other than a unit test computes β₁.

**The design question the note left open — *what answer, to whom?* — is settled here as: a
`TemporalView`**, the read-surface sibling to `ReferenceView` (bp-035). Grounded rationale (§3 Q1):
- **NOT a dreamer lens.** `dn-core-query-protocol` §2.7 makes the diachronic interpreter a *distinct*,
  provenance-gated unit (lands INTERPRETED, needs the A7 discriminator + the lens contract) — that is
  the later `DD-1`, not this. (roadmap: `docs/PARKING-LOT.md`.)
- **A typed read View, per the §2.1 frame** ("a View is a declared scope; a query is a sentence within
  it"). `ReferenceView` is the proven sibling pattern (frozen dataclass + `.over` + `open_*` factory,
  read-only + in-core). `TemporalView` is the same shape over the *temporal* half of the store.

**Read-only, in-core, no model** — the same posture bp-035 established. An in-core reader of the live
reference stratum is not a plane crossing (`dn-core-query-protocol` §2.4 item 5). Model tier **opus** —
deterministic engineering over a settled surface; **no fable, no xhigh**.

**Scope boundary (the decomposition decision — see §12).** The built `core/temporal/` surface
bifurcates by data shape: **single-snapshot** (`complex.py` → β₁, `∂₁∂₂=0`; needs ONE `X_cite`) vs
**two-snapshot** (`operators.py` + `superconnection.py` + `boundary.py` → `σ_*`, `‖[d,τ]‖`
citation-coherence, poset `δ_D²=0`; needs TWO commit-anchored snapshots + a σ node-map). **This plan
builds ONLY the single-snapshot half.** The `‖[d,τ]‖` coherence is `CQ-wire-2`, a follow-on graduation
gated on this one (§12) — because its σ-resolution/data-availability design is genuinely open, and
authoring it now would force it to read this plan's unbuilt `TemporalView` interface.

## 1. Objective

Make β₁ of the corpus citation graph a live, agent-reachable number. `core/temporal/complex.py`
(`build_citation_complex`, `dim_ker_L1`) is built and graded (`tests/unit/test_temporal_complex.py`,
Item 7: `dim ker L₁ == ripser β₁`), but its **only importers are tests** (grep-verified: zero non-test
callers of `core.temporal`). Build `TemporalView` — a deterministic, commit-anchored read window over
`X_cite` — exposing **`citation_threads()` (β₁ = the count of independent citation "threads")**, a
structural self-check (`∂₁∂₂ = 0`), and corpus size at the anchor commit; and prove β₁ on the **live
graph** against the independent ripser oracle. This is the first thing outside a test to ask the
temporal algebra a question.

## 2. Context manifest

Read whole, in order:

1. `core/temporal/complex.py` — the surface being wired. `build_citation_complex(ref_store)` (`:59`,
   calls `ref_store.all(direction="corpus_to_corpus")` — **no commit filter**, the §3 Q2 gap);
   `CitationComplex` (`:37`: `nodes`, `node_index`, `edges`, `A_cite`; `.n_nodes`/`.n_edges`);
   `dim_ker_L1(cx) -> int` (`:95`, β₁ via `hodge.harmonic_basis`); `citation_distance_matrix(cx)`
   (`:105`, the ripser input); `flag_boundary_composition_is_zero(cx) -> bool` (`:119`).
2. `core/reference_view.py` — the sibling pattern to mirror EXACTLY: the frozen `ReferenceView` (`:47`),
   `.over(store, *, commit)` (`:60`, bind read closures), `_resolve_default_commit(cfg)` (`:111`, active
   run `commit_sha` → git HEAD), `open_reference_view(config, *, commit=None)` (`:129`). `TemporalView`
   copies this skeleton; the anchor resolution MUST match so the two Views agree on "now" (§3 Q1).
3. `core/stores/reference_edges.py` — the substrate. `all(*, direction, ref_type, source_ref,
   target_ref)` (`:282`, **no `commit_sha` kwarg**); `for_commit(commit_sha)` (`:312`, per-commit slice);
   `open_reference_edge_store(config)` (`:336`); `ReferenceEdge.commit_sha` (`:163`), `.source_ref`/
   `.target_ref` (`:165`/`:168`). Edges are per-commit (§3 Q2).
4. `tests/unit/test_temporal_complex.py` — the existing grading. `_cite_store(tmp_path, edges)` fixture
   (in-memory `ReferenceEdgeStore` of `corpus_to_corpus` edges); `_ripser_b1(cx)` (`:43`, independent β₁
   = ripser H₁ at `t=0` on `citation_distance_matrix`); the Item-7 tree/4-cycle/filled-triangle
   fixtures (`:79`–`:102`). Item 3 reuses `_ripser_b1` on the live complex.
5. `docs/design-notes/core-query-protocol.md` §2.1 (Views are partial scope instances — do NOT build
   the general scope type system here, §9), §2.7 (the diachronic interpreter is a SEPARATE gated unit).
6. `docs/design-notes/temporal-retrieval-algebra.md` §3 (X_cite is theorem-grade; the combinatorial v1
   `A_cite` is binary — the `(β,z)` weighted curve is TA-a/parked, §9); §2.4 (the isolation invariant
   this plan must not weaken).
7. `tests/integration/test_temporal_isolation.py` — the isolation guard `core/temporal` must keep:
   `core/complex/**` never imports `core.temporal` (`:109`); the balance math never sees `X_cite`.
   Extending `complex.py` (Item 1) must not touch that direction.

## 3. Investigation & grounding

- **Q1 — What answer, to whom? (the note's open question) → a `TemporalView`.** Settled above (§0),
  grounded in `dn-core-query-protocol` §2.1 (typed Views) + §2.7 (the dreamer lens is a distinct gated
  unit) + `core/reference_view.py` (the proven sibling). The anchor commit is resolved **identically to
  `ReferenceView`** — active run `commit_sha` (`RunLedger.last()`) → git HEAD — so both Views answer
  "now" the same way. `[grounds: reference_view.py:111 _resolve_default_commit.]`

- **Q2 — Is `build_citation_complex` commit-anchored? NO — the gap this plan settles.** `complex.py:66`
  calls `ref_store.all(direction="corpus_to_corpus")` with **no commit filter**, so today's `X_cite` is
  the graph over the *all-history union* of edges. `reference_edges` accumulates one row per (edge,
  commit) — `commit_sha` is part of identity (`reference_edges.py:163`) — so a union-over-history β₁ can
  count spurious threads from citations that never co-existed at any single commit. A **commit-anchored**
  β₁ ("the citation threads *as of* commit X") is the honest number, and it is a prerequisite for
  `CQ-wire-2`'s two-snapshot comparison. **The code does NOT settle this; the fix is Item 1:** extend
  `build_citation_complex(ref_store, *, commit: str | None = None)` — when `commit` is given, filter the
  `corpus_to_corpus` edges to that `commit_sha`; **`commit=None` preserves today's all-history behavior
  bit-for-bit** (every existing `test_temporal_complex.py` call passes `build_citation_complex(store)`
  and MUST stay green). Announced as a cross-reference-on-extension (§4), not a silent change.

- **Q3 — Why extend `complex.py` rather than pre-filter in the View?** Two options were weighed. (a) A
  commit-filtered *adapter* wrapping the store so `.all(direction=…)` returns only the commit's edges —
  keeps `complex.py` untouched, but duck-types around the `ref_store: ReferenceEdgeStore` type hint
  (mypy friction; a fake store surface). (b) An additive `commit` kwarg on `build_citation_complex` —
  typed, backward-compatible (default None), one obvious call site. **Pinned: (b)** — it is the honest
  API, keeps the View a pure consumer, and the isolation guard is unaffected (the edit adds a Python
  filter over already-read rows; it imports nothing new, never touches `A_signed`/`build_complex`,
  `test_temporal_isolation.py:109` still holds). `[grounds: complex.py:59-92 is a pure store→object fn.]`

- **Q4 — What does `TemporalView` expose?** The single-snapshot reads of `complex.py`: `citation_threads()`
  → `dim_ker_L1` (β₁); `boundary_composition_is_zero()` → `flag_boundary_composition_is_zero` (the
  `∂₁∂₂=0` structural self-check — the cheap correctness attestation on the live backbone); `n_nodes`/
  `n_edges` (corpus size at the anchor, for context). The assembled `CitationComplex` is built once at
  `.over()` and held (frozen); the reads are pure functions of it. **No `σ_*`/`‖[d,τ]‖`/poset** — those
  are two-snapshot, `CQ-wire-2` (§9, §12).

- **Q5 — Does the live graph have data to make β₁ meaningful?** Yes for the single snapshot. The
  2026-07-15 census (resume brief) measured the distinct doc→doc graph at **234 pairs / 113 nodes**,
  cycle participation **24.8%** — so β₁ > 0 is expected (real independent citation loops). Item 3
  computes it on the live store and cross-checks against ripser. *(Whether TWO distinct commit snapshots
  carry enough data for a `‖[d,τ]‖` comparison is a separate, still-open question — deferred to
  `CQ-wire-2`'s own grounded pass, NOT settled here.)*

## 4. Reconciliation

- **`build_citation_complex` is EXTENDED, not corrected (cross-reference-on-extension).** The `commit`
  kwarg is additive with a behavior-preserving default; the existing docstring gains a sentence noting
  the anchor and pointing to `dn-core-query-protocol` §3 Q2 / this plan. No existing behavior changes —
  the falsifier for Item 1 is precisely "an existing `build_citation_complex(store)` call returns a
  different complex." This is an extension of a bp-032 built module, announced as one, carried by Item 1.
- **`dn-core-query-protocol` frontmatter is STALE** (`implementation: design-only`, "nothing built") —
  already flagged by bp-035; this plan adds a second consumer to the same standing note-erratum the
  orchestrator batches to `owner-questions.md` (the ratified note is immutable, A8). **This plan edits
  the note nowhere.** No code is corrected/replaced beyond the additive Item-1 extension.

## 5. Write scope

- `core/temporal_view.py` — the NEW `TemporalView` library object + `open_temporal_view` factory.
- `tests/unit/test_temporal_view.py` — the view's reads over in-memory fixtures (β₁, boundary check,
  commit-anchoring).
- `core/temporal/complex.py` — the additive `commit` kwarg on `build_citation_complex` (Item 1 only;
  extension, §4).
- `tests/unit/test_temporal_complex.py` — one added test for the commit filter (existing tests unchanged).
- `tests/integration/test_temporal_view_live.py` — the live-graph β₁ vs ripser cross-check (Item 3).

**Deliberately OUT of scope:** `core/temporal/{operators,superconnection,boundary}.py` (the two-snapshot
algebra — `CQ-wire-2`), `core/complex/**` (the isolation firewall — never imported here), the general
capability-scope type system (§2.1 — a later graduation, §9), `core/stores/**` (the store is reused;
`all()` gains no kwarg — the filter is in `build_citation_complex` over already-read rows), every design
note, and the denylist.

## 6. Interfaces pinned inline

```python
# core/temporal_view.py — the NEW surface (mirror ReferenceView.over's bind-then-freeze pattern).

from __future__ import annotations
from dataclasses import dataclass
from core.temporal.complex import CitationComplex, build_citation_complex

@dataclass(frozen=True)
class TemporalView:
    """A deterministic, commit-anchored read window over the citation complex X_cite
    (dn-core-query-protocol §2.7 corpus-structural tier; the read-side sibling of ReferenceView).
    Read-only + in-core: it holds an assembled CitationComplex and exposes reads only — no store
    handle, no mutator, no model, no path into the balance math (core/temporal isolation)."""

    _complex: CitationComplex          # built once at .over(), from the anchor-commit citation edges
    commit: str                        # the anchor these reads are scoped to (matches ReferenceView)

    @classmethod
    def over(cls, store: "ReferenceEdgeStore", *, commit: str) -> "TemporalView":
        # build_citation_complex(store, commit=commit) — the commit-anchored X_cite (Item 1)
        ...

    def citation_threads(self) -> int:            # β₁ = dim_ker_L1 — independent citation "threads"
        ...
    def boundary_composition_is_zero(self) -> bool:  # ∂₁∂₂ = 0 structural self-check
        ...
    @property
    def n_nodes(self) -> int: ...                 # corpus size at the anchor (# cited/citing notes)
    @property
    def n_edges(self) -> int: ...                 # # citation 1-cells at the anchor

def open_temporal_view(config=None, *, commit: str | None = None) -> "TemporalView":
    """Factory: open the live reference store read-only, resolve the anchor IDENTICALLY to
    ReferenceView (active run commit_sha via RunLedger.last(), else git HEAD), build the
    commit-anchored X_cite, and return a frozen TemporalView. Resolution MUST match ReferenceView's
    so the two Views agree on 'now' — reuse core.reference_view._resolve_default_commit or replicate."""
    ...

# core/temporal/complex.py — EXTENDED (Item 1); additive, backward-compatible:
def build_citation_complex(ref_store, *, commit: str | None = None) -> CitationComplex:
    """... commit=None ⇒ today's all-history behavior (unchanged); commit=<sha> ⇒ filter the
    corpus_to_corpus edges to that commit_sha before assembly (dn-core-query-protocol §3 Q2)."""
    citations = ref_store.all(direction="corpus_to_corpus")
    if commit is not None:
        citations = [e for e in citations if e.commit_sha == commit]
    ...  # rest unchanged

# REUSED unchanged:
#   core.temporal.complex.dim_ker_L1(cx) -> int
#   core.temporal.complex.flag_boundary_composition_is_zero(cx) -> bool
#   core.temporal.complex.citation_distance_matrix(cx) -> np.ndarray   # ripser input (Item 3)
#   core.stores.reference_edges.open_reference_edge_store(config) -> ReferenceEdgeStore
```

## 7. Items

### Item 1 — commit-anchor `build_citation_complex` (the enabling extension)
- **Objective:** additive `commit: str | None = None` kwarg — filter `corpus_to_corpus` edges to
  `commit_sha` when given; `None` preserves today's all-history assembly bit-for-bit.
- **Files:** `core/temporal/complex.py`, `tests/unit/test_temporal_complex.py`.
- **Acceptance test:** over an in-memory store seeded with the SAME citation at two commits `C1`/`C2`,
  `build_citation_complex(store, commit=C1)` assembles `X_cite` from only the `C1` edges (its `n_edges`
  and `nodes` reflect C1 alone); `build_citation_complex(store)` (no kwarg) returns the union-over-both
  complex — byte-identical to the pre-change assembly (every existing `test_temporal_complex.py` test
  stays green unmodified).
- **Falsifier:** any existing `build_citation_complex(store)` call returns a different complex (default
  behavior changed); OR `commit=C1` leaks a `C2` edge into `X_cite`.
- **Invariant(s):** isolation intact (`test_temporal_isolation.py:109` — no new import, no `core/complex`
  reach; the filter is pure-Python over already-read rows). Determinism preserved (sorted order unchanged).
- **Touches stored data?** No (reads; adds no column, no store kwarg).  **Parallelizable?** No (Item 2 uses it).

### Item 2 — `TemporalView` + `open_temporal_view` (the live read surface)
- **Objective:** the commit-anchored read window: `.over(store, commit=…)` builds the anchored `X_cite`
  and freezes it; `citation_threads()`/`boundary_composition_is_zero()`/`n_nodes`/`n_edges` are pure
  reads; `open_temporal_view` resolves the anchor exactly as `ReferenceView` does.
- **Files:** `core/temporal_view.py`, `tests/unit/test_temporal_view.py`.
- **Acceptance test:** over an in-memory store seeded with a KNOWN 4-cycle at commit `C1` (a→b→c→d→a, no
  chord), `TemporalView.over(store, commit=C1).citation_threads() == 1` (the known β₁) and
  `.boundary_composition_is_zero() is True`; a filled-triangle fixture gives `citation_threads() == 0`;
  `.n_nodes`/`.n_edges` match the C1 slice; the view exposes **no store handle / no mutator** (a
  `hasattr`/attribute assertion — no `add_batch`, no `_conn`, no `store` reachable through it).
- **Falsifier:** the view counts threads over the all-history union despite a `commit` anchor (Item-1
  regression surfacing at the View); OR a write/store surface is reachable through the frozen view.
- **Invariant(s):** read-only (Inv 4 flavor — reports data, takes no action); in-core (Inv 2); the view
  holds a `CitationComplex`, never a live store handle.
- **Touches stored data?** No.  **Depends on:** Item 1.

### Item 3 — β₁ on the live graph, cross-checked against ripser (the "oracle" leg)
- **Objective:** open the live reference store, build the commit-anchored `X_cite` at the resolved
  anchor, and assert `TemporalView.citation_threads() == _ripser_b1(complex)` (the independent β₁) on
  REAL data — the Item-7 falsifier run against the live graph, not a fixture. PRINT β₁, `n_nodes`,
  `n_edges` (the monitored corpus-topology datum).
- **Files:** `tests/integration/test_temporal_view_live.py`.
- **Acceptance test:** the harness opens the live store read-only, resolves the anchor (skip-with-reason
  if the store is empty / no `corpus_to_corpus` edges at the anchor — deploy-lag, exactly as bp-035's
  oracle skips at an un-deployed HEAD), computes β₁ two independent ways (`dim_ker_L1` via the View vs
  `_ripser_b1` via `citation_distance_matrix`), and **asserts they agree exactly**. It prints the β₁ and
  corpus size.
- **Falsifier:** the two β₁ computations disagree on the live graph (a real assembly bug the fixtures
  missed); OR the test asserts a fixed β₁ VALUE (brittle — the corpus grows; only the two-methods-agree
  invariant and a skip-if-empty guard are legitimate).
- **Invariant(s):** the cross-check is the SAME independent oracle the unit tests use (ripser ≠ the Hodge
  null-space path), never circular; read-only over the live store.
- **Touches stored data?** No (reads the live store).  **Depends on:** Items 1, 2.

## 8. Math carried explicitly

`X_cite` is the flag complex of the doc→doc citation graph; **β₁ = `dim ker L₁`** is the number of
independent 1-cycles not bounding a filled 2-simplex — the "citation threads." It is **combinatorial v1**
(`A_cite` binary — the `(β,z)` weighted retrieval curve is TA-a/parked, `dn-temporal-retrieval-algebra`
§2.1, out of scope here). Two independent computations pin it: the Hodge null-space (`harmonic_basis`,
dense SVD) and ripser H₁ at the flag-complex scale `t=0` (`citation_distance_matrix` = 0 on an edge, 1
off) — their agreement is the Item-7/Item-3 correctness proof. **No NEW math object is introduced** — this
plan wires an existing, theorem-graded one (`dn-temporal-retrieval-algebra` §3) into a read surface. The
commit filter (Item 1) is set restriction on edges, not a spectral change. `∂₁∂₂ = 0` is the standard
chain-complex identity (a sign-error tripwire on the backbone), reused from `hodge` unchanged.

## 9. Non-goals

- **No two-snapshot coherence** — `σ_*`/`σ^*`/`π_active` (`operators.py`), `‖[d,τ]‖`/`severed_citations`/
  `is_flat` (`superconnection.py`), and the supersession poset `δ_D²=0` (`boundary.py`) are `CQ-wire-2`
  (§12). They need TWO commit-anchored snapshots + a σ node-map with genuinely-open resolution (deleted-
  note totality vs `DiamondError`, and whether the live store even holds two data-rich distinct commits).
- **No dreamer lens / diachronic interpreter** (`dn-core-query-protocol` §2.7) — that lands INTERPRETED
  via `core/provenance.py`, needs the A7 discriminator + lens contract; it is `DD-1`, a later unit that
  will *consume* this View.
- **No general capability-scope type system** (§2.1 bounded lattice) — `TemporalView` ships as another
  *partial* scope instance (like `ReferenceView`/`OpsView`), before the general algebra (`CQ-scope`).
- **No weighted `(β,z)` retrieval curve, no magnetic Laplacian, no metric-coherence tier** — all parked
  behind gates in `dn-temporal-retrieval-algebra` (TA-a/TA-c/Result 4).
- **No new store API, no edit to `code_sensor.py`** — the substrate is reused; the commit filter lives in
  `build_citation_complex` over already-read rows.
- **No status-CLI / `palace status` surfacing** — a thin consumer of the View is a future item; the View
  is the seam, not the presentation.

## 10. Stop-and-raise conditions

- The commit filter can't be added additively without changing existing `build_citation_complex(store)`
  behavior (some caller relies on a shape the filter perturbs) → **file a `codebase` finding**, do not
  ship a default-behavior change; the filter must be strictly opt-in.
- The live β₁ and ripser β₁ disagree on the real graph → this is Item 3 doing its job: **file a
  `codebase` finding** (an assembly bug the fixtures missed), record both numbers, do NOT paper over it
  by relaxing to an inequality.
- Building `TemporalView` reveals it cannot be read-only without holding a live store handle (e.g. the
  complex is too large to assemble eagerly at `.over()`) → narrow / **file a finding**; never widen to a
  mutable store handle. (The census — 113 nodes / 234 edges — says eager assembly is trivially fine.)
- The isolation guard would be weakened by the Item-1 edit (any new `core/complex` reach) → **stop**;
  the filter must be pure-Python over already-read rows.
- Any blessing flip → must not.

## 11. Parked decisions

| Decision | Default recorded | Rejected alternatives | Re-entry |
|---|---|---|---|
| The "current" commit anchor | active run's `commit_sha` (`RunLedger.last()`), else git HEAD — **identical to `ReferenceView`** | union-across-history (rejected: spurious threads from never-co-existing citations); `max(created_at)` (rejected: write-time, not running code) | if the daemon's projection commit and HEAD diverge in practice (shared with bp-035) |
| Commit filter home | additive kwarg on `build_citation_complex` (§3 Q3 option b) | store-side `all(commit_sha=…)` kwarg (deferred: widens the store API); a filtered store adapter (rejected: duck-types around the type hint) | if a store-level per-commit citation query is wanted elsewhere |
| Eager vs lazy complex assembly | eager at `.over()` (freeze the `CitationComplex`; the corpus is tiny — 113 nodes) | lazy/memoized rebuild per read (deferred: needless while the graph is small) | if `X_cite` grows past `hodge`'s `_MAX_DENSE_EDGES` dense-SVD guard |
| Whether to expose the harmonic *threads* themselves (not just the count) | count only (`citation_threads() -> int`) for v1 | return the harmonic basis / representative cycles (deferred: a richer read for a consumer that needs the actual loops) | when a consumer (DD-1) needs the threads, not the Betti number |

## 12. Dependency & ordering summary

Blast-radius order: **Item 1** (additive commit filter, lowest radius) → **Item 2** (the View, builds on
it) → **Item 3** (live cross-check, reads the View). All in `core/temporal_view.py` + `core/temporal/
complex.py` + three test files → **one session, not parallel.** Model **opus** (deterministic, read-only/
additive, settled + test-pinned surface — no fable, no xhigh). `depends_on: []`.

**The follow-on this plan gates (NOT authored yet — graduate AFTER bp-037 builds, so its upstream
`TemporalView` interface is *built, not inferred*):**
- **`CQ-wire-2` — two-snapshot `‖[d,τ]‖` citation-coherence.** Extends `TemporalView` with
  `citation_coherence(other_commit)` → `‖[d,τ]‖` (severed-citation count), `severed_citations`, `is_flat`
  — wiring `operators.py` + `superconnection.py`, and (likely) the poset `δ_D²=0` health from
  `boundary.py`. `depends_on: [bp-037]`. Its open design (settle in ITS grounded pass, not here): how σ
  is resolved across two commits (identity on surviving doc-ids? version-chain-derived?), the deleted-
  note totality policy vs `DiamondError`, and whether the live store holds two data-rich distinct commits
  to compare. Recorded in `docs/PARKING-LOT.md`.
- **`DD-1` — the diachronic dreamer** (§2.7 corpus-structural tier) consumes this View + `CQ-wire-2`,
  gated additionally on A7 + the lens contract. A later unit.
