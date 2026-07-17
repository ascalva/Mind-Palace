---
type: finding
id: finding-0101
status: promoted
created: 2026-07-17
updated: 2026-07-17
links:
  - docs/design-notes/connectivity-instruments.md   # RATIFIED — the tranche this bears on (CN-2/3/4)
  - docs/build-plans/bp-060/plan.md                  # conductance — re-derives the primitives
  - docs/build-plans/bp-061/plan.md                  # bridges — overlaps core/complex/curvature
  - eval/harness/conductance.py                      # bp-060's built file (rolls its own Laplacian)
  - core/complex/laplacian.py                        # the core primitive already present
  - core/complex/spectral.py                         # diffusion_map = diffusion distance at scale t
  - core/complex/cut.py                              # conductance Φ(S), grounding_cut
  - core/complex/curvature.py                        # most_negative_edges = candidate cross-domain bridges
  - core/complex/build.py                            # build_complex(view: MirrorView) — same graph source
ftype: discovery
origin_plan: orchestrator
route: orchestrator
resolution: >-
  PROMOTED (2026-07-17, session-26): the owner ruled (A) — reconcile immediately — and
  selected the target architecture (new core/graph/ reusing core/complex; eval thin
  wrappers). Proposed as the amendment note docs/design-notes/core-graph-instruments.md
  (warrant: this finding); bp-065 executes on ratification. bp-060 → superseded at bp-065
  mint; bp-061/062 re-minted after it lands.
---

# The connectivity-instruments tranche re-derives `core/complex/` primitives in the harness

## What
The `dn-connectivity-instruments` tranche (bp-059 σ*, bp-060 conductance, bp-061 bridges,
bp-062 helix) builds Laplacian / diffusion-distance / conductance / bridge machinery in
`eval/harness/`, apparently without reconciling against **`core/complex/`, which already
provides the same family as first-class core primitives**:

- `core/complex/laplacian.py` — `laplacian` (L=D−A), `laplacian_sym`, `signed_laplacian`.
- `core/complex/spectral.py` — `diffusion_map(A, t)` (*"diffusion distance at scale t"*),
  `fiedler` (λ₂ algebraic connectivity — itself a connectivity instrument).
- `core/complex/cut.py` — `conductance(A, S)` (set/Cheeger conductance Φ(S)),
  `min_conductance`, `grounding_cut`.
- `core/complex/curvature.py` — Forman curvature + `most_negative_edges` =
  *"the candidate cross-domain bridges"* — which is **bp-061's** stated job.

bp-060's built `eval/harness/conductance.py` rolls its **own** `_laplacian(w)` and
`_diffusion_distances` (heat kernel `exp(−tL)` via `np.linalg.eigh`) over a dense array,
importing none of `core/complex`. And the graphs are **the same object**:
`core/complex/build.py`'s `build_complex(view: MirrorView, …)` derives its adjacency from
`cosine_adjacency(view)` — the same cosine-similarity-over-notes graph that `MirrorGraph.sim`
represents. So the Laplacian + diffusion + conductance family is implemented **twice**
(sparse `csr_matrix` in `core/complex`; dense `np.ndarray` in `eval/harness`).

What bp-060 adds that is **not** in `core/complex` (so it is a real new instrument, not a pure
duplicate): the σ-grid sweep, certified-cut gating, **pairwise** effective resistance R_eff
(core has *set* conductance Φ(S), not pairwise), the von-Luxburg degeneracy diagnostic, the
churn change-of-measure weighting, and the reconnection scan. The duplication is in the
**base** it is built on (Laplacian, diffusion distance), not the top-level metric.

## Why it matters
The owner's design read (surfaced 2026-07-17): these are **core graph instruments** — the
graph's own vocabulary for describing itself, the peer of `MirrorGraph.local_clustering`,
`degree`, and the `core/complex` spectral family — and placing re-derived copies in the eval
harness both (a) duplicates first-class core math and (b) denies them the "correct treatment"
(a core primitive callable by the dreamer / a query API, not only an eval reading). Left
unreconciled it calcifies a second Laplacian/diffusion implementation and lets bp-061 (bridges,
overlapping `core/complex/curvature`) and bp-062 (helix) compound it across three more plans.
Note the boundary is not a hard layer: `core/` already imports `eval/` (`spine.py`,
`dreaming/shadow.py`, `ops_view.py`), so a core consumer of these instruments is not
structurally blocked either way — the choice is genuinely a design/ontology one.

## Re-entry condition
The connectivity lane (merge of bp-060; spawn of bp-061/062) is **held** pending an owner
design ruling. Re-entry = the owner decides one of:
- **(A) Reconcile first** — revisit `dn-connectivity-instruments` against `core/complex/`:
  whether the instruments build on (or move beside) the core primitives, and whether
  bp-060/061 are re-graduated. The connectivity lane resumes on the re-graduated plans.
- **(B) Land as-is, unify later** — merge bp-060 (built + green on its branch), and schedule
  a dedicated "unify connectivity instruments on `core/complex` primitives" plan; the lane
  resumes immediately.

bp-063/bp-064 (the chat lane) are **unaffected** and proceed regardless.

## Routing
`design` discovery → orchestrator → owner (a design-changing discovery: proposed as a
`dn-connectivity-instruments` amendment/supersession warrant-linked here if the owner picks
(A), at which point this flips to `promoted`). Surfaced by the owner during bp-060 post-build
review; orchestrator-filed. bp-059 already merged (`67b373d`) — its σ* is in the same eval
lane and would come along in any reconciliation.
