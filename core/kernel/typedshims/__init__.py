"""Boundary wrappers for untyped third-party surfaces (type-system-as-core-audit.md §2.5).

One module per dependency without `py.typed` (V2, 2026-07-11: `lancedb`,
`sknetwork`, `psutil`). Core imports the shim, never the raw package, so the
`Any` an untyped import launders is quarantined to exactly one file per
dependency instead of smeared through the checked region. Every raw import here
carries a per-line warranted ignore — the pyproject `ignore_missing_imports`
override no longer covers these packages.

Discipline: a shim exposes the minimal typed surface core actually calls, with
no explicit `Any` anywhere (falsifier: `disallow_any_explicit` spot-check).
Widen a Protocol only together with the new call that needs it.
"""
