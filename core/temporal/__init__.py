"""`core/temporal/` — the citation complex `X_cite` and its topological falsifier, living OUTSIDE
`core/complex/` so the isolation invariant (`core/complex/**` never imports `reference_edges`) is
never weakened (dn-temporal-retrieval-algebra §2.4 A4; bp-032). Read-only sensing: no store write
handle, no model, no network, and no path into the balance math (`build_complex`/`A_signed`).
"""

from __future__ import annotations

from core.temporal.boundary import (
    SupersessionCycleError,
    SupersessionPoset,
    coboundary_0,
    coboundary_1,
    delta_D_squared,
    delta_D_squared_is_zero,
    poset_from_chains,
    poset_from_pairs,
    supersession_poset,
)
from core.temporal.complex import (
    CitationComplex,
    build_citation_complex,
    citation_distance_matrix,
    dim_ker_L1,
    flag_boundary_composition_is_zero,
)

__all__ = [
    "CitationComplex",
    "SupersessionCycleError",
    "SupersessionPoset",
    "build_citation_complex",
    "citation_distance_matrix",
    "coboundary_0",
    "coboundary_1",
    "delta_D_squared",
    "delta_D_squared_is_zero",
    "dim_ker_L1",
    "flag_boundary_composition_is_zero",
    "poset_from_chains",
    "poset_from_pairs",
    "supersession_poset",
]
