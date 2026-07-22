"""Outer-ring residue of the reasoning complex (dn-inner-outer-core §2.7, K1 / bp-090).

The pure family-5 mathematics (`balance, curvature, hodge, laplacian, support` + the package's inner
init text) moved to `core/kernel/complex/`. What remains here is the outer half — the modules whose
closure leaves the admissible base: `spectral` (sknetwork), `topology` (ripser), `temporal`
(duckdb), and the `blocks`/`build`/`cut` assembly that reaches them. This init is stdlib-import-free
so it stays inner by construction (a pure package marker); the residue submodules beside it are the
outer machinery.
"""
