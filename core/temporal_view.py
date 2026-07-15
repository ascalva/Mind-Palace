# ── Family 1 boundary (labelings & information-flow) · symbols in docs/NOTATION.md ──
# OBJECT:    The §2.7 corpus-structural read surface — a deterministic, commit-anchored read
#            window over the citation complex X_cite (`core/temporal/complex.py`). The read-side
#            sibling of `ReferenceView` (bp-035): where ReferenceView answers "who cites this?"
#            over the raw reference edges, TemporalView answers "how many independent citation
#            threads (β₁) does the corpus carry, as of one commit?" over the flag complex.
# INVARIANT: read-only + in-core. The view holds an ALREADY-ASSEMBLED `CitationComplex` (built
#            eagerly at `.over()`), never a live store handle — so no mutator and no connection is
#            reachable through it (Inv 4 flavor: reports data, takes no action). An in-core reader
#            is not a plane crossing (dn-core-query-protocol §2.4 item 5). No model, no network,
#            and — by construction of `core/temporal` — no path into the balance math (§2.4 A4).
# ENFORCED:  static (the frozen dataclass exposes read methods + a bound `CitationComplex`, no
#            store) + guard (test_temporal_view.py asserts no store/`add_batch`/`_conn` reachable).
"""`TemporalView` — the deterministic "how many citation threads?" read window (bp-037 / CQ-wire).

`core/temporal/complex.py` (`build_citation_complex`, `dim_ker_L1`) is built and graded, but its
only importers were tests (finding-0059/0061's staleness class, one level up: the *algebra* was
built and agent-unreachable). This module is the first live consumer — a typed read window in the
mould of `ReferenceView` (`core/reference_view.py`): assemble the anchored `X_cite`, expose β₁ and a
structural self-check, and only those.

**Commit-anchored (the §3 Q2 decision).** Citation edges are per-commit (`commit_sha` is part of
edge identity), so β₁ over the all-history union can count threads across citations that never
co-existed. `TemporalView.over(store, *, commit=…)` builds `X_cite` from ONLY that anchor's edges,
and `open_temporal_view` resolves the default anchor **identically to `ReferenceView`** (the active
run's `commit_sha`, else git HEAD) — so the two Views agree on what "now" means.

**Single-snapshot (bp-037 scope).** This wires the single-snapshot half of `core/temporal` (β₁
threads, `∂₁∂₂=0`). The two-snapshot `‖[d,τ]‖` citation-coherence (`σ_*`, severed citations) is
`CQ-wire-2`, a follow-on that extends this surface.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from core.temporal.complex import (
    CitationComplex,
    build_citation_complex,
    dim_ker_L1,
    flag_boundary_composition_is_zero,
)

if TYPE_CHECKING:  # annotations only — the factory imports the config/store lazily at runtime
    from config.loader import Config
    from core.stores.reference_edges import ReferenceEdgeStore


@dataclass(frozen=True)
class TemporalView:
    """A deterministic, commit-anchored read window over the citation complex `X_cite`.

    Construct with `TemporalView.over(store, commit=…)`; the view holds the assembled
    `CitationComplex` (built once, eagerly) and the anchor commit — the store's mutators are
    unreachable because no store handle is retained (§2.1 scope: the type names reads, never a
    mutator). Read-only + in-core (Inv 4/Inv 2)."""

    _complex: CitationComplex   # the anchored X_cite, built eagerly at .over(), frozen here
    commit: str                 # the anchor commit these reads are scoped to (as ReferenceView)

    @classmethod
    def over(cls, store: ReferenceEdgeStore, *, commit: str) -> TemporalView:
        """Assemble the commit-anchored `X_cite` from the store's citation edges and freeze it into
        a view. The store is READ here (eagerly, once) and NOT retained — the view exposes the reads
        below and only those; the store's `add_batch`/`_conn` are unreachable through it."""
        return cls(_complex=build_citation_complex(store, commit=commit), commit=commit)

    # --- reads -----------------------------------------------------------------------------------
    def citation_threads(self) -> int:
        """β₁ = `dim ker L₁` — the number of independent citation "threads" (1-cycles in the flag
        complex not bounding a filled 2-simplex) at the anchor. Combinatorial v1 (unweighted
        `A_cite`). Deterministic; cross-checked vs an independent ripser β₁ in the live test."""
        return dim_ker_L1(self._complex)

    def boundary_composition_is_zero(self) -> bool:
        """`∂₁∂₂ = 0` on the citation backbone — the chain-complex identity; a self-check that the
        assembled incidence is sign-consistent (a backbone sign error would break it)."""
        return flag_boundary_composition_is_zero(self._complex)

    @property
    def n_nodes(self) -> int:
        """The number of 0-cells: distinct notes that are a citation endpoint at the anchor."""
        return self._complex.n_nodes

    @property
    def n_edges(self) -> int:
        """The number of 1-cells: distinct undirected citation pairs at the anchor commit."""
        return self._complex.n_edges


def open_temporal_view(config: Config | None = None, *,
                       commit: str | None = None) -> TemporalView:
    """Factory: open the live reference store read-only and build a `TemporalView` anchored at
    `commit` — defaulting (§3 Q1/Q2) to the active run's `commit_sha` (`RunLedger.last()`), else git
    HEAD. The default is resolved via `core.reference_view._resolve_default_commit` so this View and
    `ReferenceView` anchor identically (both answer "now" the same way); reference_view.py is the
    authoritative resolver, out of this plan's scope to make public."""
    from config.loader import get_config
    from core.reference_view import _resolve_default_commit
    from core.stores.reference_edges import open_reference_edge_store

    cfg = config or get_config()
    anchor = commit if commit is not None else _resolve_default_commit(cfg)
    store = open_reference_edge_store(cfg)
    return TemporalView.over(store, commit=anchor)
