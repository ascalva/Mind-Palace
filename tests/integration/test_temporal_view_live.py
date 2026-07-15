"""`TemporalView` β₁ on the LIVE citation graph, cross-checked vs an independent ripser oracle
(bp-037 / CQ-wire, Item 3).

The Item-7 falsifier lifted from fixtures onto the live store: β₁ of `X_cite` at HEAD must agree
when computed two INDEPENDENT ways — the Hodge null space (`dim ker L₁`, via `TemporalView`) and
ripser H₁ at scale `t=0` (`citation_distance_matrix`). A disagreement is a real assembly bug the
unit fixtures missed (plan §10 stop-and-raise → a codebase finding, NOT a relaxed assertion). The
test PRINTS the live β₁ + corpus size (the monitored corpus-topology datum).

**Skip, not fail, when the anchor carries no citation structure.** The projected reference store
lives in the running system's data dir; a fresh git worktree / a code-only commit has no
`corpus_to_corpus` edges at HEAD → environmental skip, exactly as bp-035's oracle skips at an
un-projected HEAD. It does NOT assert a fixed β₁ VALUE (the corpus grows) — only that the two agree.
"""

from __future__ import annotations

import subprocess

import pytest

from config.loader import REPO_ROOT, get_config
from core.complex.topology import persistence
from core.stores.reference_edges import open_reference_edge_store
from core.temporal.complex import build_citation_complex, citation_distance_matrix
from core.temporal_view import open_temporal_view


def _head_sha() -> str:
    return subprocess.run(["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],  # noqa: S607
                          capture_output=True, text=True, check=True).stdout.strip()


def _ripser_b1(cx) -> int:
    """Independent β₁: ripser H₁ alive at `t=0` on `citation_distance_matrix` (0 on an edge, 1
    off) — the SAME oracle the unit test uses, reimplemented here (a different computation than the
    Hodge null space `dim_ker_L1` the view reports)."""
    D = citation_distance_matrix(cx)
    if D.shape[0] < 1:
        return 0
    dgm1 = persistence(D, maxdim=1)["dgms"][1]
    return sum(1 for b, d in dgm1 if b <= 1e-9 < d)


def test_live_beta1_agrees_with_independent_ripser_oracle() -> None:
    head = _head_sha()

    # The view IS the probe: it assembles X_cite at HEAD. No corpus→corpus edges at the anchor (a
    # fresh worktree, a code-only commit, deploy-lag) → environmental skip, not a failure.
    view = open_temporal_view(commit=head)
    if view.n_edges == 0:
        pytest.skip(f"no corpus→corpus citation edges at HEAD {head[:12]} in this checkout "
                    "(environmental — the projected store lives in the running system's data dir)")

    # The INDEPENDENT oracle: rebuild the same anchored complex and count β₁ a DIFFERENT way (ripser
    # H₁), never the Hodge null space the view uses.
    store = open_reference_edge_store(get_config())
    try:
        cx = build_citation_complex(store, commit=head)
    finally:
        store.close()

    b1_hodge = view.citation_threads()
    b1_ripser = _ripser_b1(cx)

    # PRINT the corpus-topology datum (visible with `pytest -s`/`-rP`).
    print("\n=== X_cite β₁ — Hodge null-space vs ripser, live store @ HEAD ===")
    print(f"anchor commit: {head[:12]}   corpus at anchor: n_nodes={view.n_nodes}  "
          f"n_edges={view.n_edges}")
    print(f"β₁ (dim ker L₁, via TemporalView): {b1_hodge}")
    print(f"β₁ (ripser H₁ @ t=0, independent): {b1_ripser}")
    print(f"∂₁∂₂ = 0 self-check: {view.boundary_composition_is_zero()}")

    assert b1_hodge == b1_ripser, (
        f"live β₁ disagreement: TemporalView/dim_ker_L1={b1_hodge} vs ripser={b1_ripser} — an "
        "assembly bug the fixtures missed (plan §10 stop-and-raise → a codebase finding, NOT a "
        "relaxed assertion)")
    assert view.boundary_composition_is_zero() is True   # ∂₁∂₂=0 on the live citation backbone
    assert view.n_nodes >= 1                              # the anchor carried citation structure
