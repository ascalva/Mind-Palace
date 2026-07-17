# Journal — bp-065 (core-graph-rehome)

In-session orchestrator self-build, fable/xhigh (owner-directed, session-26). Minted on
ratification of dn-core-graph-instruments; blessed ready by owner hand (recorded `7f75fa9`).

## 2026-07-17 — item 1 COMPLETE: core/graph/sigma_star.py + thin connectivity + boundary teeth

- **Manifest formatting repair (pre-item):** scope-guard parses write_scope entries LITERALLY —
  my inline YAML comments made 5 paths unmatchable (Write denied, correctly). Moved the comments
  to a block above the list; the blessed capability is byte-identical. Not a scope change.
- **The split:** `core/graph/sigma_star.py` takes the MATH verbatim (CrossingEdgeError, ConnIndex,
  SigmaStar, MaxSpanningForest, build_max_spanning_tree, _tree_path_bottleneck, _grid_snap,
  _SNAP_EPS, sigma_star, pairwise_sigma_star, cut_fingerprint, acquire_mirror_cut,
  _MIRROR_STRATUM). `eval/harness/connectivity.py` keeps the INSTRUMENT (ConnEvidence, ConnResult,
  _aggregate, _corpus_ref, _spec_hash, run_connectivity, METRIC_*, _INSTRUMENT/_TYPE_TAG) +
  re-exports every moved name under `__all__` (P5). Code moved byte-identical; only docstrings
  updated for placement. `run_connectivity` keeps a deferred `MirrorGraph` import (build-time only).
- **Import surfaces verified pre-move** (grep, journal-worthy): the ONLY importers of connectivity
  anywhere are its two bp-059 test files + the harvest tests; every cross-file import is a public
  name (no private leaks). Re-export set = exactly the moved publics.
- **One surprise + fix:** `core.graph.sigma_star` is ambiguous as an ATTRIBUTE — the package
  __init__ re-exports the *function* sigma_star, which shadows the same-named submodule (PEP-328
  getattr binding). `from core.graph.sigma_star import X` is unaffected (sys.modules path); the
  boundary test addresses the modules via importlib. Documented in the test.
- **Acceptance RUN:** `uv run pytest tests/unit/test_connectivity.py
  tests/quality/test_connectivity_sigma_star.py tests/unit/test_graph_boundary.py -q` →
  **19 passed** (bp-059 suites UNCHANGED — zero edits, out of write_scope by design). ruff clean;
  `mypy core agents eval ops scheduler scripts` → 214 files clean. Boundary teeth green:
  P1 no-eval-import (static AST, package-own files — NOT the closure; spine's P6 sink is tolerated),
  Law-C4 no-clock, P5 is-identity on all 9 re-exports.
- **NEXT:** item 2 — conductance harvest (core/graph/conductance.py from scratchpad bp060-harvest/,
  `_laplacian` → core.complex adapter `_dense_laplacian`), eval wrapper, tests + the ONE retarget
  (`_CONDUCTANCE_SRC`), L-equivalence tooth, __init__ extension.
