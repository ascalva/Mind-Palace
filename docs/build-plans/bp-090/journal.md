# bp-090 journal — K1: the born ring moves to core/kernel/**

## 2026-07-21 — minted (graduation, session-41)

Graduated from ratified `dn-inner-outer-core` §2.7-M2/§3 on the owner's direct instruction
(finding-0148 — the M2 follow-through the wave-complete framing dropped). Entry gates
evaluated at graduation: ratified `fbea48d` ✓; born-set stability across bp-083+bp-089 ✓;
no open plans ✓; K1 import-closure verified by AST scan at `438cef2` (zero core-imports
outside the set) ✓. Importer surface at graduation: 291 files (tests 155 / core 89 /
scripts 19 / ops 9 / eval 8 / scheduler 8 / agents 2 / config 1); string-ref files: 4.
Status: `proposed` — awaiting the owner's `proposed → ready` hand-bless. No work performed.

## 2026-07-22 — Item 1: recompute + pin the manifest at build HEAD (read-only) — DONE

Build HEAD `22bdaee`. Ran the fixed-point computation (the test's own `_fixed_point`) + K1
closure + import-shape census at HEAD.

**Fixed point (F6 clear):** `computed == INNER`, both 37. The map is NOT stale — the born
inner-ring test is green (`4 passed`). Baseline outer-ratchet count = **19** (the move-neutrality
invariant §2.4-D2 pins this unchanged across every commit).

**K1 membership:** `INNER` (37) − the S1 seven (`integrator_math`, `recursion_ops`, `temporal`,
`temporal.{boundary,complex,operators,superconnection}`) = **30 K1 members**; `core` (root init)
does not move ⇒ **29 movable**. K1 **import-closure verified at HEAD: 0 members import outside K1**
(the wave is import-closed against kernel-so-far = ∅ — §2.7 wave rule satisfied; no K1 module
reaches an S1 or outer module).

**The 29 movable members → new kernel paths (subpaths preserved):**
- 11 top-level: `agent_scope, complex_types, constitution, matching, mirror, provenance, recursion,
  rings, scope, selfcheck, velocity_view` → `core/kernel/<name>.py`.
- `complex` cluster (6): `__init__, balance, curvature, hodge, laplacian, support` → `core/kernel/complex/`.
- `config` cluster (2): `__init__, loader` → `core/kernel/config/`.
- `ingest` cluster (6): `__init__, amend, chunk, logseq, pipeline, verify` → `core/kernel/ingest/`.
- `stores` cluster (3): `__init__, rawstore, sourceset` → `core/kernel/stores/`.
- `typedshims` (1): `__init__` → `core/kernel/typedshims/`.

**Split packages (residue inits needed):** `complex` (residue holds `blocks, build, cut, spectral,
temporal, topology`), `ingest` (residue holds `curated, dialogue, embed, founding, index, mint_ids,
purge, run, sync, watch`), `stores` (residue holds the 19 sqlite/duckdb/lancedb stores + staging +
claim_ops + …), `typedshims` (residue holds `lancedb, psutil, sknetwork`). **Q7 refinement:
`config` is NOT a split — it has only `__init__` + `loader`, both K1-inner, so the WHOLE
`core/config/` relocates and its directory disappears; no residue.** 4 residue inits, not 5.

**New pure package modules the map must claim (per §2.4-B1 new-module rule):** `core.kernel` (new
kernel pkg init) + the 4 residue inits (`core.complex`, `core.ingest`, `core.stores`,
`core.typedshims` — docstring-only ⇒ compute inner). Exact post-move map is recomputed in Item 2,
not asserted.

**Importer surface at HEAD (Q5 recompute):** the census of `from <moved-module> import …`
(the ONLY shape used — 454 statements across **216 files**; **zero** bare `import core.X` and
**zero** mixed `from core.pkg import a,b`). Repoint is therefore a clean per-module rewrite
`from core.X import` → `from core.kernel.X import` for the moved set.

**Split-package repoint hazard (the one non-uniform case), resolved:** the moved package roots
`core.stores` / `core.typedshims` / `core.complex` / `core.ingest` must NOT be blanket-rewritten —
`from core.stores import staging` (`tests/unit/test_staging_store.py:20`) and
`from core.typedshims import psutil` (`ops/lifecycle/launcher.py:245,732`) name **residue**
submodules that stay. Rewrite set = MOVED − {`core.complex`,`core.ingest`,`core.stores`,
`core.typedshims`} (the bare roots), keeping `core.config` (full move) and all full-submodule
paths (`core.stores.rawstore`, `core.complex.hodge`, `core.ingest.pipeline`, `core.config.loader`,
…). No mixed `from core.pkg import <moved>,<residue>` exists (would need line-splitting) — verified 0.

**String-ref sweep targets (Item 3, F8 class), pinned at HEAD:** `core/rings.py` (the map — handled
in Item 2's map rewrite); `tests/integrity/test_eval_isolation.py` (`_INGEST_PREFIX="core.ingest"`,
`_MIRROR_WORLD={"core.mirror","core.provenance"}`, seed `core/ingest/pipeline.py`);
`tests/integrity/test_shadow_isolation.py:62` (`"core.mirror"` assertion). `test_inner_ring.py`'s
known-impurity strings are all OUTER modules that stay put (move-neutral). `_DERIVED_MODULE =
"core.stores.derived"` in shadow-isolation is residue (stays).

## 2026-07-22 — Item 2: the kernel skeleton + the moves, green (reversible) — DONE

Executed as **one atomic move commit** (§7 permits fewer larger commits iff each is green; the
uniform mechanical transform makes the single-slice map recompute far less error-prone than
partial-state juggling across 7 commits).

**Correction to Item 1's clustering:** `core.matching` is a **package** (`core/matching/__init__.py`,
import-free, no submodules), not a top-level `.py`. Like `config`, it moved WHOLE (no residue). So
the 29 movable = 10 single-file leaf modules + `matching` (pkg) + `complex`(6) + `config`(2) +
`ingest`(6) + `stores`(3) + `typedshims`(1).

**Moves (29 `git mv`, subpaths preserved):** 10 leaves → `core/kernel/<name>.py`; `matching`,
`config` whole → `core/kernel/{matching,config}/`; `complex`/`ingest`/`stores`/`typedshims` inner
members → `core/kernel/<pkg>/`. New: `core/kernel/__init__.py` + 4 residue inits
(`core/{complex,ingest,stores,typedshims}/__init__.py`, docstring-only markers). `config`/`matching`
directories are now GONE (full move).

**Repoint:** the AST-driven script rewrote **455** `from core.X import` → `from core.kernel.X import`
across **215** files, keying on the exact moved module and EXCLUDING the four bare split-package roots
(so `from core.stores import staging` / `from core.typedshims import psutil` stayed). Mixed-import
hazard scan: **0** (no `from core.pkg import <moved>,<residue>` line needed splitting). Then
`ruff check --fix` re-sorted imports (79 isort fixes — the mechanical consequence of the prefix
rename changing alpha-order; no logic touched).

**Map rewrite (`core/kernel/rings.py`):** `INNER` recomputed to the post-move fixed point = **42**
(37 − 29 old names + 29 kernel names + 5 new pure package modules: `core.kernel` + the 4 residues;
`config`/`matching` mint no residue). Docstring/comment updated to record K1.

**Acceptance (Item 2) — all green:**
- `test_inner_ring.py` → **4 passed** (computed == declared == 42; direction law + honesty guard hold).
- Outer ratchet count = **19**, IDENTICAL to Item-1 baseline (move-neutrality §2.4-D2 / F7 clear).
- `scripts/check_imports.py` (import firewall) → OK.
- `ruff check .` → All checks passed.
- pytest collection over the CI marker set → **1838/1858 collected (20 deselected), 0 import errors**
  (proves every one of the 215 repointed files resolves).
- Item-2 acceptance grep (`(from|import) core.<moved>` minus `core.kernel.`) → **empty** (zero
  stale old-name imports).

## 2026-07-22 — Item 3: the reference sweep — string module-names + file-path re-anchors (F8) — DONE

The import repoint (Item 2) is blind to two reference classes; this item swept both.

**(a) String module-name references (the pinned F8 targets):**
- `tests/integrity/test_eval_isolation.py` — `_INGEST_PREFIX="core.ingest"` → `_INGEST_PREFIXES=
  ("core.kernel.ingest","core.ingest")` (ingest now spans two trees — forbid BOTH, unweakened, via a
  new `_reaches_ingest` helper); `_MIRROR_WORLD` → `{"core.kernel.mirror","core.kernel.provenance"}`;
  negative-control seed `core/ingest/pipeline.py` → `core/kernel/ingest/pipeline.py`.
- `tests/integrity/test_shadow_isolation.py:62` — `"core.mirror"` assertion → `"core.kernel.mirror"`
  (shadow's own import was repointed in Item 2; `_DERIVED_MODULE="core.stores.derived"` is residue,
  untouched).
- `core/kernel/rings.py` map strings — handled in Item 2's map rewrite.
- NOTE: my Item-2 repoint (whole-file `str.replace` of `from core.X import`) already fixed the
  `from core.provenance import`/`from core.mirror import` **inside string fixtures** in
  `tests/unit/test_provenance_tags.py` — the mypy-fixture snippets now import `core.kernel.provenance`
  correctly. (Those 3 tests briefly showed red under my shell's `FORCE_COLOR=3`, which makes mypy
  emit ANSI codes that break the test's `": error:"` parser — an ENVIRONMENT artifact, NOT the move;
  CI sets no FORCE_COLOR. Re-running the gate with FORCE_COLOR unset → green.)

**(b) File-path references the repoint cannot see (the sharper F8 class — paths built from string
parts or `__file__` depth):** the move changed both moved-module `__file__` depth AND constructed
paths that name old locations. Found and re-anchored:
- `core/kernel/config/loader.py` — `REPO_ROOT = Path(__file__)...parent×3` → `×4` (moved one dir
  deeper; without this REPO_ROOT resolved to `core/`, so `config/defaults.toml` 404'd).
- `core/kernel/constitution.py` — `REPO_ROOT = Path(__file__)...parent.parent` → `.parent×3` (else
  `CONSTITUTION.md` resolved to `core/CONSTITUTION.md` 404 — this was the dominant failure cluster,
  ~90 tests loading config/constitution). **These two are the ONLY `__file__`-relative REPO_ROOT
  computers among the 29 moved modules** (verified by a corrected recursive scan — my first
  `git grep 'core/kernel/**/*.py'` pathspec silently skipped files directly under `core/kernel/`).
- `tests/unit/test_config_split.py:16` — `_REPO_ROOT/"core"/"config"` → `…/"core"/"kernel"/"config"`.
- `tests/integrity/test_shadow_isolation.py:84` — `REPO_ROOT/"core"/"mirror.py"` → `…/kernel/mirror.py`.
- `tests/unit/test_reference_edges.py:214` — `complex_dir` now scans BOTH `core/kernel/complex` and
  `core/complex` (the family spans two trees post-split; unweakened).

**Deliberately LEFT (documented per §11 / non-goal "no doc rewrites"):** docstring prose path-mentions
(`core/graph/{conductance,influence}.py`, `test_support.py`, `test_inner_ring.py` examples) and
`ReferenceEdge` fixture DATA strings (`source_ref="core/recursion.py"` etc. in `test_reference_edges`,
`test_reference_edge_isolation`) — commit-anchored identifiers/data, not filesystem lookups.

**These `__file__`/constructed-path re-anchors are a necessary consequence of relocation (behavior
PRESERVED, identical to before), the same class as an import repoint — not a behavior change.** The
plan §6 "no source edits beyond imports and the map" describes the typical case; re-anchoring a
`__file__`-relative path is the path analogue of repointing an import. Filed no finding: this is the
codebase concern the builder resolves and annotates (routing rule), not a spec-defect.

**Acceptance (Item 3) — all green:** straggler grep for quoted `'core.<moved>'` strings and
`patch()`/`import_module()` dynamic targets → **empty**; the isolation/config/reference tests →
**39 passed**; ruff → clean.
