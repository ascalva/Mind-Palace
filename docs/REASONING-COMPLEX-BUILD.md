# Building the Reasoning Complex
### Representation, tools, and the Dreamer loop v2 — the buildable companion to `REASONING-COMPLEX-MATHEMATICS.md`

**2026-06-30 · implementation spec**

> *Notation: every load-bearing symbol (ρ, π_MR, 𝒜, D(t), 𝔎, K_σ, ℋ, δ\*δ, …) is defined once in [`NOTATION.md`](NOTATION.md) — symbol ↔ code ↔ object ↔ family (companion IV §A). This document builds family 5.*

This document turns the mathematical framework (companion III v0.2) into something a builder can
start from: the data model, the computation modules, the restructured Dreamer loop, the integration
points, and a phased build order. It respects every existing invariant and convention — sealed core,
no network in `core/`, thin custom code over heavy frameworks, object-capability scope, dream R&D
flag OFF, trough-only scheduling, everything behind the `DreamerAdapter` seam.

**What we are building and why.** The Dreamer's reasoning is thin: it clusters the authored mirror
by cosine and summarizes. This spec builds the **reasoning complex** — a multilayer, typed, temporal
knowledge structure — and the deterministic instruments that reason over it (Laplacians, curvature,
persistence, balance, block models, message passing). The Dreamer then arrives at synthesis already
knowing where the bridges, tensions, holes, and robust themes are, and how they are changing. The
model call stays the last, earned step. **This is the strengthening of the system's weak spot, and
it is the precondition for hands worth having** — a hand acts on the Dreamer's model, so the model
must be deep before the hand is worth building.

**The governing engineering rule (from companion III v0.2):** the complex is **derived and
regenerable** from the raw store. We persist only what cannot be recomputed cheaply (typed/signed
edges, structural snapshots, interpreted outputs); everything else recomputes from vectors on the
trough. "Raw is sacred; derived is regenerable" holds unchanged.

---

## 1. The data model

### 1.1 What is stored vs. what is recomputed

| Object | Storage | Rationale |
|---|---|---|
| atoms (vectors, digest, $\rho$, $t$) | **LanceDB** (existing `VectorStore`) | unchanged |
| similarity edges $E_\sigma$ (cos ≥ σ) | **recomputed** from vectors | regenerable; never persisted (a config change, not a loss) |
| **typed/signed edges** $(t,w,s,\tau)$ | **SQLite** `edges` table (new) | the fiber components are *authored structure* (support/contradict), not derivable from cosine |
| flag complex $K_\sigma$ (simplices) | **recomputed** on the trough | regenerable from $E_\sigma$; persisting all simplices is wasteful |
| derivation hyperedges (B-arcs) | **SQLite** `DerivedStore` junction (existing) | already present as `derived_from`; generalize to the junction schema |
| structural snapshots (time series) | **DuckDB** `structural_snapshots` (new) | time-series is DuckDB's job; feeds drift/F4 |
| interpreted findings (dreams) | **SQLite** `DerivedStore` (existing) | interpreted-only, attested, unchanged |

This keeps the persisted surface minimal and every stored row either *authored structure* or an
*attested interpreted output* — nothing recomputable is frozen.

### 1.2 Schemas (SQLite / DuckDB)

```sql
-- NEW: the typed/signed edge fiber (§1.2 of the framework). Authored + interpreted edges.
CREATE TABLE edges (
    edge_id     TEXT PRIMARY KEY,      -- content-id(u,v,rel_type)
    u           TEXT NOT NULL,         -- source atom digest
    v           TEXT NOT NULL,         -- target atom digest
    w           REAL NOT NULL,         -- strength >= 0
    sign        INTEGER NOT NULL,      -- +1 support / -1 contradict  (polarity)
    rel_type    TEXT NOT NULL,         -- derives | supports | contradicts | contextualizes | similar
    created_at  TEXT NOT NULL,         -- ISO ts (temporal index)
    provenance  TEXT NOT NULL          -- authored_* | interpreted  (edges are layered too)
);
CREATE INDEX idx_edges_u ON edges(u);
CREATE INDEX idx_edges_v ON edges(v);
CREATE INDEX idx_edges_type ON edges(rel_type);

-- GENERALIZE (existing derived_from -> junction, framework §2.4 of III 0.1):
CREATE TABLE hyperedges (
    edge_id     TEXT PRIMARY KEY,
    rel_type    TEXT NOT NULL,         -- derives (acyclic) | ...
    provenance  TEXT NOT NULL,         -- interpreted (structural: no other value writable)
    created_at  TEXT NOT NULL
);
CREATE TABLE hyperedge_nodes (
    edge_id     TEXT NOT NULL,
    node_id     TEXT NOT NULL,
    role        TEXT NOT NULL,         -- tail | head   (today every head-set has size 1)
    PRIMARY KEY (edge_id, node_id, role)
);
```

```sql
-- NEW (DuckDB): structural snapshots for temporal tracking (framework §5.4).
CREATE TABLE structural_snapshots (
    snapshot_id     BIGINT,
    taken_at        TIMESTAMP,
    n_nodes         INTEGER,
    n_components     INTEGER,          -- beta_0
    fiedler          DOUBLE,           -- lambda_2 (algebraic connectivity)
    frustration      DOUBLE,           -- lambda_min(signed L), dissonance proxy
    mean_forman      DOUBLE,           -- mean Forman-Ricci curvature
    frac_neg_curv    DOUBLE,           -- fraction of bridge (negative-curvature) edges
    n_blocks_sbm     INTEGER,          -- SBM model-selected theme count
    min_conductance  DOUBLE,           -- worst interpreted-community conductance (alignment)
    persistence_h1   INTEGER           -- count of long-lived H_1 holes
);
```

### 1.3 In-memory representation

The complex is assembled per trough pass into a small in-memory object (regenerated, never a
long-lived global):

```python
@dataclass(frozen=True)
class ReasoningComplex:
    nodes:   list[str]                       # atom digests, MirrorView-filtered
    idx:     dict[str, int]                  # digest -> matrix index
    A:       scipy.sparse.csr_matrix         # weighted adjacency (similarity backbone)
    A_signed: scipy.sparse.csr_matrix        # signed adjacency (+w / -w)
    hyper:   list[tuple[frozenset[str], str]]# (tail set, head) B-arcs
    layers:  np.ndarray                      # provenance code per node
    created: np.ndarray                      # timestamps per node
    # complex (flag) and Laplacians are computed lazily by the modules below
```

Built **only** from a `MirrorView` (authored-only, structural firewall) for introspective passes, or
a `CuratedView` for R5 resonance — never from a raw `VectorStore` handle.

---

## 2. The computation layer

**Principle:** *every module is a pure function of a `ReasoningComplex`, deterministic, offline, and
model-free.* The model is never called here. New module namespace: `core/complex/`.

### 2.1 Module layout

```
core/complex/
  build.py        ReasoningComplex assembly from a MirrorView (nodes, A, A_signed, hyper)
  laplacian.py    L, L_sym, signed L̄, hypergraph L_H  (scipy.sparse builders)
  spectral.py     Fiedler, spectral & diffusion clustering, diffusion map   (eigsh)
  curvature.py    Forman-Ricci (numpy, floor); Ollivier-Ricci (optional, gated)
  balance.py      signed spectrum; frustration proxy; frustrated-triangle enumeration
  topology.py     flag complex + persistent homology (ripser); beta_0 / H_1 with lifetimes
  cut.py          min-cut-to-authored + conductance (alignment detector, A2)
  blocks.py       degree-corrected SBM: posterior memberships + ICL model selection
  support.py      noisy-OR message passing on the derivation DAG (multi-path grounding)
  flow.py         Ricci-flow community surgery (optional cross-check)
  temporal.py     structural-invariant snapshot writer (DuckDB)
```

### 2.2 Libraries (offline, pip-installable, local)

| Need | Library | Notes |
|---|---|---|
| sparse linear algebra, eigensolves, `expm_multiply` | **scipy** | small add over numpy (already transitive via lancedb) |
| spectral embedding / Louvain cross-check | **scikit-network** (`sknetwork`) | pure-python-friendly, pip; avoids `graph-tool` compilation |
| persistent homology | **ripser** (`ripser.py`) | light C++ backend; lighter than gudhi for $H_0/H_1$ |
| min-cut / max-flow | **networkx** or `scipy.sparse.csgraph` | networkx max-flow is fine at $10^3$ nodes |
| Ollivier–Ricci (optional) | **GraphRicciCurvature** (uses POT) | gated behind a flag — OT cost; Forman is the default floor |
| SBM | **custom** (~200 lines, VEM) or `sknetwork` | keep it thin per conventions; degree-corrected |

All are within the network allowlist for install; **none is imported by any networked path** —
`core/complex/` lives in Zone A, reaches no network (import-firewall must stay green).

### 2.3 Key module contracts & complexity (corpus scale ≈ $10^3$ nodes, $10^3$–$10^4$ edges)

| Function | Signature (sketch) | Cost | Determinism |
|---|---|---|---|
| `build_complex(view)` | `MirrorView -> ReasoningComplex` | $O(nk)$ kNN edges | fixed (embeddings fixed) |
| `laplacian.signed(A_signed)` | `-> csr` | $O(\text{nnz})$ | exact |
| `spectral.diffusion_map(A, r, t)` | `-> np.ndarray (n×r)` | partial `eigsh`, top-$r$: ms | fixed seed |
| `spectral.cluster(map)` | `-> labels` | $k$-means on $r$ dims | fixed seed |
| `curvature.forman(A)` | `-> edge->float` | $O(\#\triangle)$ | exact |
| `balance.frustration(A_signed)` | `-> (lambda_min, frustrated_triangles)` | eigsh + $O(\#\triangle)$ | exact |
| `topology.persistence(A, maxdim=1)` | `-> diagrams` | sparse Rips $H_0/H_1$: sub-sec | exact |
| `cut.alignment(complex, S)` | `-> (min_cut, conductance)` | max-flow / $\lambda_2$ | exact |
| `blocks.sbm(A, k_range)` | `-> (memberships posterior, k*)` | VEM, few iters: sub-sec | fixed seed |
| `support.noisy_or(hyper, g)` | `-> claim->float` | $O(|\mathcal{E}|)$ topo sweep | exact |

**Scale reality:** the eigensolves dominate and are milliseconds for top-$r$ modes; Ollivier (if
enabled) is the only heavy op. The system stays **inference-bound, not BLAS-bound**. Hard guardrails:
never materialize a dense $e^{-tL}$ (use `expm_multiply`), never a dense $n\times n$ kernel, always
partial eigensolves.

---

## 3. The Dreamer loop v2

**Principle:** *deterministic structure first, one earned model call last.* This restructures
`core/dreaming/dreamer.py`. The interpreter panel (`core/dreaming/interpreters.py`) becomes the set of
**consumers of `core/complex/`** — each a `Claim`-emitter, still model-free (the R0 pattern, now with
real instruments behind it).

### 3.1 The pass (pseudocode)

```python
def dream_pass(view: MirrorView, synth: Synthesizer, attestor) -> list[Dream]:
    K = build_complex(view)                                  # 1. BUILD 𝔎|_MR (firewall structural)

    bridges   = curvature.forman(K.A)                        # 2. LOCATE bridges (negative κ)
    themes    = blocks.sbm(K.A, k_range=(2, 16))             # 3. THEME with counts + posterior
    xcheck    = spectral.cluster(spectral.diffusion_map(K.A))#    cross-check (agree=robust)
    tensions  = balance.frustration(K.A_signed)              # 4. TENSION (frustrated triangles)
    holes     = topology.persistence(K.A, maxdim=1)          # 5. GAPS (long-lived H_1)
    support   = support.noisy_or(K.hyper, grounding_scores)  # 6. SUPPORT (multi-path grounding)

    candidates = assemble_claims(bridges, themes, xcheck,    #    each carries its authored support set
                                 tensions, holes, support)
    ranked = adjudicate(candidates)                          # 7. c = min{1, γ^d·g·(1+λ(|Agr|−1))}

    dreams = []
    for cand in ranked[:MAX]:
        theme = synth(frame_context(role=MIRROR_NOT_ORACLE,  # 8. the ONE earned model call
                                    evidence=cand.support, …))#    narrate, grounded, mirror-not-oracle
        if self_check(theme, cand.support).passed:           # deterministic grounding gate
            d = DerivedStore.add(kind="dream", body=theme,   # 9. interpreted-only, derives→leaves
                                 derived_from=cand.support,  #    acyclic; attested
                                 provenance=INTERPRETED,
                                 attestor=attestor)
            dreams.append(d)

    temporal.write_snapshot(K, themes, tensions, holes)      # 10. structural drift axes (A2/F4)
    return dreams
```

### 3.2 The interpreter panel, restated

Each interpreter is a thin adapter over a `core/complex/` function, emitting `Claim(method,
statement, support=authored_digests, data)` — model-free, deterministic:

| Interpreter | Backed by | Surfaces |
|---|---|---|
| `bridge` | `curvature.forman` (Ollivier optional) | surprising cross-domain links |
| `theme` | `blocks.sbm` + `spectral.cluster` | concerns, with count + membership confidence |
| `tension` | `balance.frustration` | commitments that can't co-hold (frustrated triangles) |
| `hole` | `topology.persistence` | themes circled but unstated (long-lived $H_1$) |
| `anchor` | grounded attention walk / centrality | the author's core intellectual anchors |
| `change_point` | (still deferred — needs per-note temporal axis) | never faked |

The adjudicator ranks by grounding-weighted confidence (companion III v0.2 §7.2 clamp); agreement
across interpreters is a bounded multiplier, not a vote. This is exactly the R0/R1 substrate, now
with the instruments that make each interpreter say something real.

### 3.3 Where the model is (and is not)

The **only** model call is step 8 (narration of already-selected, already-grounded candidates over a
`MirrorView`). Every structural judgment — where the bridges are, how many themes, which tensions,
which holes, how well-supported — is deterministic. This preserves "the model advises, code acts" and
makes the entire reasoning layer **reproducible and auditable**. **[Engineering].**

---

## 4. Integration with the existing architecture

Nothing here breaks an invariant; each new piece plugs into an existing seam.

- **Firewall (`MirrorView`, structural).** `build_complex` accepts only a `MirrorView` for
  introspective passes → the complex is provably authored-only. Observed never enters. Structural, not
  checked-then-refused.
- **Interpreted-only (`DerivedStore`).** All Dreamer output (dreams, structural findings) is written
  through `DerivedStore` (no provenance parameter → interpreted by construction). New **edges** minted
  by the Dreamer carry `provenance=interpreted`; authored edges are ingested, not minted.
- **Adapter seam (`DreamerAdapter`, F9).** The whole `core/complex/` layer sits behind the existing
  adapter: `cluster()`, `diffusion_map()`, `curvature()`, `frustration()`, `persistence()`,
  `alignment()`, `sbm()` become adapter methods. The live path calls the ADOPTED subset; speculative
  surface (Ollivier, SBM richness) is isolated here.
- **Drift gauge (A1 → A2).** `temporal.write_snapshot` appends structural axes (frustration↑,
  min-conductance↓, domain-split, frac-negative-curvature) to the `eval/drift.py` `Profile` as
  additive `Axis` entries — the A2 extension the gauge was built to accept. A drifting interpreted
  bubble becomes a *measurable* deterioration.
- **Quality suite (F9).** The new clusterer must **not regress** the apophenia guard, planted-signal
  recall, calibration, or grounding-faithfulness (full-support ablation). Wire it through
  `MindPalaceDreamerAdapter`, run `tests/quality/` against the lexical baseline → a green run is a
  non-regression proof (not a value proof).
- **Attestation.** Every dream and structural finding emits an attestation chaining to authored leaves
  (existing `StoreAttestor` wiring). Structural findings are attested the same way.
- **Scheduler.** All of this is trough-only (`HEAVY_TIERS`, foreground gate). The complex is rebuilt on
  the `dream`/`curate` cron jobs; snapshots on the same cadence. No foreground stutter.

---

## 5. Build order

**Principle:** *one instrument per checkpoint, ordered by (value ÷ cost) and dependency; each behind
the adapter, flag-OFF, trough-only, with its property tests.* This mirrors the roadmap's
one-item-per-checkpoint discipline. Suggested track identifier: **Track H — the reasoning complex**
(new; sits beside R-track dreaming, consumes A-track drift).

| Step | Item | Value | Cost | Depends on | Disposition |
|---|---|---|---|---|---|
| H1 | `edges` schema + typed/signed edge ingest; `build_complex` | foundation | low | — | **build first** |
| H2 | `laplacian.py` + `spectral.py`: diffusion/spectral clusterer | replaces chaining-prone lexical clusterer | low | H1 | high value, low risk |
| H3 | `balance.py`: signed Laplacian + frustration + frustrated triangles | **contradiction, rigorously** | low | H1 | high value |
| H4 | `curvature.py`: Forman-Ricci `bridge` interpreter | **surprising links** | low | H1 | high value |
| H5 | `topology.py`: flag complex + $H_1$ persistence `hole` interpreter | conceptual gaps | med | H1 | good (verify usefulness) |
| H6 | `cut.py`: min-cut/conductance → A2 drift axes | **alignment detection** | low | H1, A1 | high value (alignment) |
| H7 | `blocks.py`: degree-corrected SBM `theme` interpreter | **themes with confidence + count** | med | H2 | biggest theming upgrade |
| H8 | `support.py`: noisy-OR message passing on the DAG | principled multi-path grounding | low | derivation edges | good |
| H9 | `temporal.py`: structural snapshots → DuckDB, drift trajectories | **self-watching over time** | low | H2–H7, A1 | high value (longitudinal) |
| H10 | `flow.py`: Ricci-flow community surgery (cross-check) | robustness signal | med | H4 | optional enrichment |
| H11 | Ollivier–Ricci (gated), DPO confluence checks | rigor / enrichment | high | H4, panel | optional / research |

**Deferred (blockers named, framework §8):** rich sheaf transport maps, tensor factorization,
hyperbolic embedding (curvature covers the signal), reaction–diffusion dynamics.

Recommended first three checkpoints: **H1 → H2 → H3** (foundation, the clusterer upgrade, and rigorous
contradiction) deliver the most reasoning depth for the least cost and risk, all flag-OFF behind the
adapter.

---

## 6. Validation & the honest gap

### 6.1 Property tests per module (extend `tests/quality/`, `tests/property/`)

- **Determinism:** fixed seed ⇒ identical diffusion map, SBM assignment, persistence diagram.
- **Spectral stability:** a $\sigma$-perturbation $\le\delta$ moves cluster labels $\le$ a blessed
  Hamming tolerance (else the clusterer is chaotic).
- **Persistence stability:** bottleneck distance between diagrams $\le$ input perturbation (the
  stability theorem — a failure means a filtration bug).
- **Frustration correctness:** a synthetically balanced signed graph ⇒ $\lambda_{\min}(\bar L)=0$;
  planting one frustrated triangle ⇒ it is enumerated.
- **Curvature sign:** a planted bridge edge has negative Forman curvature; a triangle-dense edge
  positive.
- **Alignment monotonicity:** adding an authored support edge to a community never lowers its
  grounding cut (metamorphic).
- **SBM recovery:** a graph generated from a known block structure ⇒ model selection recovers the
  block count within tolerance.
- **Non-regression (F9):** planted-signal recall $\ge$ lexical baseline; noise max-confidence $\le$
  calibrated ceiling; grounding faithfulness under **full-support** ablation.

### 6.2 The honest gap (unchanged, and load-bearing)

None of this certifies a dream is **insightful**. The instruments certify a theme is *real, robust,
grounded, and correctly located*; they cannot certify it is *useful to the author*. That is subjective
and closes only against the author's blind ratings (the F9 `rate_blind` hook, deliberately unwired so
a green CI run can't masquerade as a proven value claim) and, ultimately, when the hands act well on
the Dreamer's model. The utility axis $u$ stays separate from confidence $c$ for exactly this reason.

> **The point, restated for the build:** this framework does not make the Dreamer insightful by
> construction. It makes it *equipped* — reasoning over seven unified structural signals and watching
> itself evolve, instead of clustering and summarizing. That is what turns the reasoning core from the
> system's weak spot into the deep model a future hand can act on. The engine has to be strong before
> the hands are worth building; this is how the engine gets strong.

---

## Appendix — quick reference

**Module → store map**

| Module | Reads | Writes |
|---|---|---|
| `build.py` | LanceDB vectors (via MirrorView), `edges`, `DerivedStore` | in-memory `ReasoningComplex` |
| `laplacian/spectral/curvature/balance/topology/cut/blocks/support/flow` | `ReasoningComplex` | in-memory results |
| `temporal.py` | `ReasoningComplex` + results | DuckDB `structural_snapshots` |
| `dreamer.py` (loop v2) | all of the above (via adapter) | `DerivedStore` (dreams + edges), attestations |

**Build order (condensed):** H1 edges+complex → H2 spectral clusterer → H3 signed/frustration →
H4 Forman curvature → H5 persistence → H6 alignment cut → H7 SBM → H8 noisy-OR → H9 temporal →
H10 Ricci flow → H11 Ollivier/DPO. First three (H1–H3) are the high-value, low-risk core.

**Invariants preserved:** firewall (MirrorView structural), interpreted-only (DerivedStore),
model-advises-code-acts (one earned call), trough-only (scheduler gate), no-network-in-core
(import-firewall), attested chains to authored leaves, flag-OFF by default.

*Companion to `REASONING-COMPLEX-MATHEMATICS.md`. Build behind the adapter; keep the dream R&D flag
OFF until a deliberate session flips it.*
