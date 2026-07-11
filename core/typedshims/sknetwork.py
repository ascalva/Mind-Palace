"""Typed facade over `sknetwork` (type-system-as-core-audit.md §2.5 boundary wrapper).

scikit-network ships no `py.typed` (V2, 2026-07-11). This module is the ONE
place core touches the raw package — today that is the Louvain cross-check the
reasoning complex runs as a diagnostic beside its spectral partition. Offline
compute only — no network (Invariant 2).

The raw import stays lazy (inside the function): sknetwork is heavy and the
Louvain cross-check is off the live path, matching the call site's prior
behavior in `core/complex/spectral.py`.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp
from numpy.typing import NDArray


def louvain_labels(
    adjacency: sp.csr_matrix[np.float64], *, resolution: float = 1.0, random_state: int = 0
) -> NDArray[np.int64]:
    """Modularity (Louvain) community labels for a (sparse) adjacency — one label per node.
    Deterministic under the fixed `random_state`."""
    import sknetwork.clustering as _skc  # type: ignore[import-untyped]  # warrant: no py.typed (V2)

    labels = _skc.Louvain(resolution=resolution, random_state=random_state).fit_predict(adjacency)
    return np.asarray(labels, dtype=np.int64)
