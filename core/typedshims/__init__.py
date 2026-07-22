"""Outer-ring residue of the typed-shim boundary (dn-inner-outer-core §2.7, K1 / bp-090).

The package's inner init text moved to `core/kernel/typedshims/`. The shims themselves stay here in
the outer ring: each wraps an untyped third-party surface (`lancedb, sknetwork, psutil`) that is
inadmissible to the inner base, so the shim modules compute outer. Core imports the shim, never the
raw package. This init is stdlib-import-free so it stays inner by construction (a pure package
marker); the residue shim submodules beside it are the outer machinery.
"""
