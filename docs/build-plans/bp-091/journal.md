# bp-091 journal — K3: the S1 seven join the kernel

## 2026-07-21 — minted (graduation, session-41)

Graduated alongside bp-090 from ratified `dn-inner-outer-core` §2.7 (K3 after K1). HARD
GATE recorded: the §2.7 stability window for the seven closes only at bp-090's seal
(bp-089 minted them; bp-090 is the second sealed plan leaving them unchanged) — do not
start before. K3 closure verified against kernel∪K3 at `438cef2` (zero violations). The
integrator_math-not-integrator delta vs the note's §2.6b preview is grounded in
rings.py:44-49 (bp-089's honest landing). Status: `proposed` — awaiting the owner's
hand-bless, sequenced strictly behind bp-090. No work performed.

## 2026-07-22 — Item 1: recompute the manifest at build HEAD (read-only) — DONE

Worktree base and shared checkout both at `74c2334` (seal bp-090), which already carries K1 —
`core/kernel/**` present before I started (K1's `refactor(core): K1 …` in the log). The §2.7
stability window is CLOSED: bp-090 is sealed (the 2nd sealed plan leaving the seven unchanged).

**Fixed point (F6 clear) at HEAD, pre-move:** the born inner-ring test is green (`4 passed`),
`computed == INNER` both 42 — the map is NOT stale. Baseline **outer-ratchet count = 19**
(`test_core_imports_nothing_outside_core`; move-neutrality §2.4-D2 pins this unchanged).

**The exact seven at their `core.*` names, present:** `core.integrator_math`,
`core.recursion_ops`, `core.temporal` (init) + `core.temporal.{boundary,complex,operators,
superconnection}`.

**Consumer census at HEAD (Q4/Q5):** 15 importer files across core + tests (an order of magnitude
below K1) — `core/integrator.py`, `core/stores/{claim_ops,derived}.py`, `core/temporal/acquire.py`
(the S1 seam, STAYS outer — imports `boundary`/`complex`, outer→inner, allowed), `core/temporal_view.py`,
and 7 tests. **New arrival vs graduation:** `core/temporal/atlas.py` (merged onto main after mint)
imports only `core.kernel.scope` + `core.temporal.spine` (both outer/kernel) — it is OUTER, stays in
the residue, needs no repoint. No bare `import core.X`; the one `from core.temporal import spine`
(`test_spine_invariants.py`) names the residue submodule and needs no repoint. **String/path refs:**
none of the seven use `__file__`/`REPO_ROOT` (verified) — so NO path re-anchoring (unlike K1's
loader.py/constitution.py). One isolation-test module-name string scan (`test_temporal_isolation.py`)
needs the two-prefix treatment (below).

## 2026-07-22 — Item 2: the moves + repoint + map, green (reversible) — DONE

Executed as **one atomic commit `f3909be`** (§7 permits fewer larger commits iff each is green; the
move + repoint + map + isolation-guard are indivisible for green — the isolation test and the moved
math break unless swept together, the K1 "never a red intermediate" shape).

**Moves (7 `git mv`, subpaths preserved):** the 4 temporal math submodules + the re-exporting
`__init__` → `core/kernel/temporal/`; `integrator_math` + `recursion_ops` (single-file leaves) →
`core/kernel/`. New **docstring-only residue** `core/temporal/__init__.py` (import-free marker;
acquire.py/spine.py/atlas.py stay behind, OUTER by design — the S1 seam invariant §2.6b).

**Repoint (15 files):** `core.{integrator_math,recursion_ops,temporal.boundary,temporal.complex,
temporal.operators,temporal.superconnection}` → `core.kernel.*` (imports + the acquire/derived
docstring path-mentions, updated for accuracy). Then `ruff --fix` re-sorted 9 import blocks (the
mechanical alpha-order consequence of the prefix rename; no logic touched). Zero stale old-name refs
by grep.

**Map (`core/kernel/rings.py`):** INNER recomputed to the post-move strict-v2 fixed point = **43**
(42 − 6 old S1 names + 7 kernel names; `core.temporal` STAYS as the new residue marker — its old
pure init was inner, its new residue init is inner too). Set via the test's own `_fixed_point()`
then edited to match (F6 discipline, never hand-toward-green). **`test_inner_ring` → 4 passed:
computed == declared == 43, both directions.**

**Isolation guard (`test_temporal_isolation.py`):** `test_core_complex_never_imports_core_temporal`
now forbids BOTH `core.temporal` AND `core.kernel.temporal` prefixes (factored into
`_TEMPORAL_PREFIXES`) — the K1 eval-isolation unweakening lesson, so the relocation cannot silently
weaken the "core/complex never sees the citation math" invariant. → 3 passed.

**Move-neutrality (F7 clear):** outer-ratchet count = **19**, identical to the Item-1 baseline.

**A note on process (codebase concern, no finding — routing rule):** my Bash calls initially ran in
the shared checkout on `main` (cwd `/Users/ascalva/mind-palace`) while the Edit tool wrote the
worktree — I caught the split, `git stash`-ed the accidental work off the shared checkout (fully
recoverable in its `stash@{0}`, pre-existing stashes untouched), and redid ALL work cleanly inside
the worktree with `cd <worktree>`. Shared checkout is pristine `main`; no commit ever landed there.

## 2026-07-22 — Item 3: end-state verification + the full 5-leg gate — DONE

**End-state (Item 3 acceptance):** `core/kernel/temporal/` = 5 `.py` (init + 4 math submodules);
`core/kernel/{integrator_math,recursion_ops}.py` present; residue `core/temporal/` = `__init__` +
acquire + spine + atlas. Map == kernel tree; `INNER == 43`; outer ratchet **19**. Zero stale
old-name imports.

**The full 5-leg attestable-green gate (each leg separately, FORCE_COLOR unset):**
1. `ruff check .` → **All checks passed!**
2. `mypy core agents eval ops scheduler scripts` → **Success: no issues found in 250 source files**.
3. argless `mypy` → **Found 69 errors in 20 files (checked 520 source files)** — tests-baseline **== 69**.
4. `python -m ops.type_gate` → **Tier-2 membership: OK · Bare-ignore scan: OK**.
5. `pytest -q -m 'not live and not podman and not needs_vault and not needs_restic' --deselect
   …::test_core_imports_nothing_outside_core --cov` → **1853 passed, 11 skipped, 21 deselected** (46.49s).

All three §7 items complete. Zero behavior change; the S1 seven are physically at `core/kernel/**`;
the residue `core/temporal/` holds only the OUTER seam. Plan left `status: ready` for the
orchestrator to flip at seal. Commit `f3909be` on branch `worktree-agent-ace13634c52856e49`.

**Ready to deskcheck.** (Suggested: show `core/kernel/temporal/` holds the citation-complex math and
`core/temporal/` holds only acquire/spine/atlas; `INNER == 43` computed==declared; outer ratchet still
19; `from core.kernel.temporal.complex import dim_ker_L1` resolves; the two-prefix isolation guard is
green.)

## Follow-through

- **Built?** Yes — the seven S1-promoted modules (`integrator_math`, `recursion_ops`, and the
  `temporal` citation-complex math: init + `boundary`/`complex`/`operators`/`superconnection`) are
  physically relocated to `core/kernel/**` (7 `git mv`, subpaths preserved), repo-wide repoint (15
  files), the map recomputed to the 43-member post-move fixed point, a new docstring-only
  `core/temporal/` residue init, and the isolation guard unweakened to forbid both temporal prefixes.
  One atomic green commit `f3909be`.
- **Wired/delivered (or why dormant)?** Delivered and live: the whole runtime now imports
  `core.kernel.{integrator_math,recursion_ops,temporal.*}`; the inner-ring ratchet
  (`core.kernel.rings.INNER` + `test_inner_ring.py`) recomputes the fixed point over the NEW tree and
  is green at 43. Not dormant — every consumer repointed in the same commit (clean break, no shims §6).
- **Does a consumer use it?** Yes — `core/integrator.py`, `core/stores/{claim_ops,derived}.py`,
  `core/temporal/{acquire,view}` and 7 tests import the relocated modules; the full suite (1853 tests)
  exercises them and passes. The inner-ring ratchet consumes the map and forces it to equal the tree.
- **Track state (what remains on `dn-inner-outer-core`)?** M2 wave **K3 COMPLETE** — with K1 (bp-090)
  this finishes the two-wave physical relocation of the born + S1 rings into `core/kernel/**`.
  Remaining on the note: **K2** (the 13 packaging-debt promotions, each as its remedy lands — un-minted
  by design) and **M3** (the flip: when the OUTER ratchet reaches 0 and map == kernel-tree). The outer
  ratchet (19 → 0) runs on its own parallel track, untouched here. **The ring program is NOT done when
  this plan seals** (completion-claims honesty).
- **Opened a new track/finding?** No new finding. No `__file__`/path re-anchors were needed (none of
  the seven compute a `REPO_ROOT` — the K1 hazard did not recur). The shared-vs-worktree cwd split
  (recorded in Item 2) was a process slip I self-corrected; no code/spec defect.
