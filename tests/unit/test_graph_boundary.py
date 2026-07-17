"""The dn-core-graph-instruments boundary teeth (bp-065): P1 import purity + P5 re-export
identity + P3 one-Laplacian equivalence.

(a) **P1 — the permanent tooth**: no file under `core/graph/` imports `eval`, ever. Scoped to
    the package's OWN files (a static AST scan), NOT the transitive closure — core substrate
    legitimately writes readings out through the tolerated sink (`core/temporal/spine.py:97`,
    P6), so a closure test would fail by design.
(b) **P5 — the compatibility contract**: every name the eval harness re-exports IS the core
    object (`is`-identity) — a drifted copy would silently fork the math.
(c) **P3 — one Laplacian** (added with item 2): `core/graph`'s dense Laplacian adapter routes
    through `core/complex/laplacian.laplacian` and equals the direct dense construction
    `D − W` EXACTLY on fixture-scale graphs (n < 128: NumPy's pairwise summation reduces to
    sequential there, and interleaved zeros perturb nothing, so float64 equality is exact —
    the no-silent-metric-change clause).
"""

from __future__ import annotations

import ast
from pathlib import Path

_PKG = Path("core/graph")


def _package_files() -> list[Path]:
    files = sorted(_PKG.rglob("*.py"))
    assert files, "core/graph has no Python files — the package is missing"
    return files


# ── (a) P1: no eval import anywhere under core/graph ────────────────────────────────────────────


def test_core_graph_never_imports_eval() -> None:
    """The P1 invariant, statically: no `import eval` / `from eval...` in any core/graph file."""
    for path in _package_files():
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                roots = [node.module.split(".")[0]] if node.module else []
            else:
                continue
            assert "eval" not in roots, (
                f"{path}: imports eval ({ast.dump(node)}) — P1 violated: core never imports "
                "eval for mathematics (dn-core-graph-instruments)"
            )


def test_core_graph_reads_no_clock() -> None:
    """Law C4 rides along at the package level: no `time`/`datetime` import under core/graph —
    the instruments are (σ, t, cut)-index-driven, never wall-time-driven."""
    for path in _package_files():
        tree = ast.parse(path.read_text())
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        assert "time" not in imported and "datetime" not in imported, f"{path} reads a clock"


# ── (b) P5: the eval harness re-exports ARE the core objects ────────────────────────────────────


def test_connectivity_reexports_are_the_core_objects() -> None:
    """`eval.harness.connectivity`'s relocated names are `is`-identical to `core.graph.sigma_star`'s
    — the re-export surface every downstream pin (bp-061/062) and the bp-059 suites resolve
    through. A drifted copy would silently fork the math. (importlib: the package re-exports the
    *function* `sigma_star`, which shadows the same-named submodule as a package attribute — the
    modules must be addressed via sys.modules, not attribute access.)"""
    import importlib

    gs = importlib.import_module("core.graph.sigma_star")
    conn = importlib.import_module("eval.harness.connectivity")

    for name in (
        "ConnIndex",
        "CrossingEdgeError",
        "MaxSpanningForest",
        "SigmaStar",
        "acquire_mirror_cut",
        "build_max_spanning_tree",
        "cut_fingerprint",
        "pairwise_sigma_star",
        "sigma_star",
    ):
        assert getattr(conn, name) is getattr(gs, name), f"{name} drifted from core.graph"
