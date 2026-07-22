"""Eval-isolation firewall (dn-evaluation-harness §2.10, bp-042 Item 4) — non-skippable.

Two structural facts, proven from the import graph without running the system:

* **No path from the eval-results store to ingest.** An eval run must never be able to seed the
  corpus — so `eval.harness.store` (and the registry) must reach no ingest entry point through ANY
  transitive first-party import. After K1 (bp-090) ingest spans two physical trees — the moved
  text-projection machinery at `core.kernel.ingest` and the outer residue at `core.ingest` — so the
  guard forbids BOTH prefixes (the same logical package, unweakened).
* **The eval store is ∉ `MIRROR_READABLE`.** It is its own Σ, outside the complex — so it must not
  even touch the mirror/provenance world (`core.kernel.mirror`, `core.kernel.provenance` post-K1).
  A reading carrying no `Provenance` cannot be mirror-readable; that structural distance from the
  world is the proof.

Same spirit as `test_import_firewall.py` (I2): a static AST scan is stronger than a runtime guard —
it proves no path *exists* rather than catching a leak at run time.
"""

from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# First-party top-level packages — the boundary of the transitive scan (stdlib / third-party are
# leaves: they cannot reach first-party ingest).
_FIRST_PARTY = {"eval", "core", "ops", "config", "scheduler", "agents"}

# The forbidden targets. Post-K1 (bp-090) ingest lives in two trees: the moved inner machinery
# (`core.kernel.ingest`) and the outer residue (`core.ingest`) — forbid both so the property is
# renamed, not weakened.
_INGEST_PREFIXES = ("core.kernel.ingest", "core.ingest")
_MIRROR_WORLD = {"core.kernel.mirror", "core.kernel.provenance"}


def _reaches_ingest(mod: str) -> bool:
    """True iff a module name is (or lives under) either ingest tree."""
    return any(mod == pre or mod.startswith(pre + ".") for pre in _INGEST_PREFIXES)

# The seeds: the eval-store surface this plan introduced.
_SEEDS = ["eval/harness/store.py", "eval/harness/registry.py", "eval/harness/__init__.py"]


def _module_of(rel_path: str) -> str:
    """`eval/harness/store.py` -> `eval.harness.store`; `core/ingest/__init__.py` -> `core.ingest`.
    """
    p = rel_path[:-3] if rel_path.endswith(".py") else rel_path
    if p.endswith("/__init__"):
        p = p[: -len("/__init__")]
    return p.replace("/", ".")


def _resolve(modname: str) -> Path | None:
    """Map a first-party dotted module to its file under the repo, else None (not first-party)."""
    if modname.split(".")[0] not in _FIRST_PARTY:
        return None
    base = REPO_ROOT / Path(modname.replace(".", "/"))
    for cand in (base.with_suffix(".py"), base / "__init__.py"):
        if cand.exists():
            return cand
    return None


def _imports_of(path: Path) -> set[str]:
    """Every module name imported anywhere in the file (nested/lazy imports included — ast.walk)."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.add(node.module)
    return names


def _reachable_first_party(seeds: list[str]) -> set[str]:
    """BFS the first-party import graph from the seeds; return every reachable first-party mod."""
    frontier = [_module_of(s) for s in seeds]
    seen: set[str] = set(frontier)
    while frontier:
        mod = frontier.pop()
        path = _resolve(mod)
        if path is None:
            continue
        for imp in _imports_of(path):
            if imp.split(".")[0] in _FIRST_PARTY and imp not in seen:
                seen.add(imp)
                frontier.append(imp)
    return seen


def test_eval_store_reaches_no_ingest_entry_point() -> None:
    """No transitive first-party import path from the eval store to `core.ingest` — an eval run
    cannot seed the corpus (§2.10 eval isolation)."""
    reachable = _reachable_first_party(_SEEDS)
    ingest = {m for m in reachable if _reaches_ingest(m)}
    assert ingest == set(), f"eval store reaches ingest via import graph: {sorted(ingest)}"


def test_eval_store_does_not_touch_the_mirror_world() -> None:
    """The eval store never imports `core.mirror` / `core.provenance` — it is its own Σ, so an eval
    reading carries no Provenance and is structurally ∉ MIRROR_READABLE (§2.10 mirror firewall)."""
    reachable = _reachable_first_party(_SEEDS)
    touched = reachable & _MIRROR_WORLD
    assert touched == set(), f"eval store touches the mirror world: {sorted(touched)}"


def test_scanner_would_catch_an_ingest_path() -> None:
    """Negative control: the BFS actually detects an ingest import when one exists (a green result
    above means isolation, not a broken scanner)."""
    reachable = _reachable_first_party(["core/kernel/ingest/pipeline.py"])
    assert any(_reaches_ingest(m) for m in reachable)
