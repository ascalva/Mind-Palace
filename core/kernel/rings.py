"""The inner-ring map — a declaration forced to equal a computation (dn-inner-outer-core §2.4-A).

The inner core is the *founding language* of the system: the mathematics, the algebra, the
sacred-boundary vocabulary — **not** the austere plumbing (the owner's v2 ruling, §2.1). Membership
is **mechanical, never curated**: the inner ring is the maximal import-closed subset of ``core/**``
over the admissible base

    (stdlib ∖ ops.import_lint.NETWORK_MODULES ∖ PLUMBING_STDLIB) ∪ MATH_3P

under STRICT closure semantics (ancestor ``__init__``s counted — §2.3). This module only *declares*
that fixed point; ``tests/unit/test_inner_ring.py`` recomputes it at test time and forces
``INNER`` to equal the computation, both directions (§2.4-B1). ``INNER`` therefore changes only via
a reviewable one-file diff named in a plan's ``write_scope`` — every promotion/demotion is
plan-visible with zero new machinery (the map-monotonicity law, §2.4-D4).

This module is **inner by construction**: stdlib-only, side-effect-free at import, wires no read
path. It names modules (``"core.kernel.scope"``), never paths — so a further directory move is a
mechanical rename here, not a re-computation. This file itself now lives at ``core/kernel/rings.py``
(K1, bp-090) and is named ``core.kernel.rings``.

The ``INNER`` set below was recomputed at build HEAD after the K1 physical move (bp-090); it is the
strict-v2 fixed point over the post-move ``core/**`` tree. If
``test_inner_ring_is_the_computed_fixed_point`` ever lands red, the map — never the test — is stale:
recompute at HEAD and edit ``INNER`` to match, never hand-edit toward green (falsifier F6). See
``tests/unit/test_core_self_containment.py`` — the OUTER ratchet (19 → 0 over all of ``core/``), a
deliberately independent second scanner this file's test mirrors but does not import (the
redundant-sensor DRY exception, §2.4-B).
"""

from __future__ import annotations

# The pinned pure-math third-party libraries admitted into the base (§2.1). numpy/scipy are
# side-effect-free numerics; nothing else third-party is admissible.
MATH_3P: frozenset[str] = frozenset({"numpy", "scipy"})

# The v2 owner-ruled subtraction (§2.1, 2026-07-20T22:08Z): sqlite3 is stdlib, but the sqlite store
# layer is plumbing, not the founding language — subtracted so the ring means *meaning*, not
# import-austerity. This is the predicate's one home-in-core parameter; the network subtraction
# keeps its single home in ``ops.import_lint.NETWORK_MODULES`` (the test's computation sources it
# there). Membership stays computed — the lever is the predicate, not any module's assignment.
PLUMBING_STDLIB: frozenset[str] = frozenset({"sqlite3"})

# The inner ring — the strict-v2 fixed point over the post-K1 ``core/**`` tree (42 members).
# **K1 (bp-090): the born inner ring physically moved to ``core/kernel/**``.** The 30 born members
# (37 pre-move − the S1 seven) were relocated ``core.X → core.kernel.X`` (subpaths preserved),
# except ``core`` (the root package) which stays. The move MINTED five new pure package modules the
# fixed point now claims (§2.4-B1, "pure ⇒ the map must claim them"): ``core.kernel`` (the new
# kernel package init) and the four split-package residue inits — ``core.complex`` / ``core.ingest``
# / ``core.stores`` / ``core.typedshims`` — each a docstring-only marker whose outer submodules stay
# behind. ``config`` and ``matching`` moved WHOLE (no outer submodule ⇒ no residue). The S1 seven
# (bp-089) STAY at their pre-move names — they are K3, a later wave (bp-091). Module names, not
# paths (survives further renames).
INNER: frozenset[str] = frozenset({
    "core",                       # the root package init (import-free; does not move — §2.3)
    # ── the kernel subtree: the 29 relocated born members + the kernel package init ──
    "core.kernel",                # K1 (bp-090): the new inner-core package
    "core.kernel.agent_scope",
    "core.kernel.complex",
    "core.kernel.complex.balance",
    "core.kernel.complex.curvature",
    "core.kernel.complex.hodge",
    "core.kernel.complex.laplacian",
    "core.kernel.complex.support",
    "core.kernel.complex_types",
    "core.kernel.config",
    "core.kernel.config.loader",
    "core.kernel.constitution",
    "core.kernel.ingest",
    "core.kernel.ingest.amend",
    "core.kernel.ingest.chunk",
    "core.kernel.ingest.logseq",
    "core.kernel.ingest.pipeline",
    "core.kernel.ingest.verify",
    "core.kernel.matching",
    "core.kernel.mirror",
    "core.kernel.provenance",
    "core.kernel.recursion",
    "core.kernel.rings",          # this map module, now at core/kernel/rings.py
    "core.kernel.scope",
    "core.kernel.selfcheck",
    "core.kernel.stores",
    "core.kernel.stores.rawstore",
    "core.kernel.stores.sourceset",
    "core.kernel.typedshims",
    "core.kernel.velocity_view",
    # ── split-package outer residues (K1, bp-090): pure package markers, outer submodules behind ──
    "core.complex",               # residue: spectral/topology/temporal/blocks/build/cut stay
    "core.ingest",                # residue: embed/watch/curated/dialogue/founding/… stay
    "core.stores",                # residue: the sqlite/duckdb/lancedb store layer stays
    "core.typedshims",            # residue: lancedb/psutil/sknetwork shims stay
    # ── the S1 seven (bp-089), UNMOVED — K3, a later wave (bp-091) ──
    "core.integrator_math",       # S1: the pure integrator gauge math (report + coverage)
    "core.recursion_ops",         # S1: the pure dialogue-operation vocabulary
    "core.temporal",              # S1: the temporal package (seams shed to acquire.py)
    "core.temporal.boundary",     # S1: the supersession coboundary δ_D (pure)
    "core.temporal.complex",      # S1: the citation complex X_cite (pure)
    "core.temporal.operators",    # S1: the σ chain maps / active projection (pure)
    "core.temporal.superconnection",  # S1: the temporal curvature (pure)
})
