"""Apply the `quality` marker to every test under tests/quality/ (test-organization.md §3).

The output-quality suite (signal-vs-noise / apophenia) is pure-CI: no scheduler loop, no
models, no network — it drives the live clustering/grounding/confidence machinery through the
DreamerAdapter with a deterministic embedder + synthesizer. Marked so `-m quality` selects it
and `-m "not quality"` excludes it, like every other category.
"""

from __future__ import annotations

import pytest


def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker(pytest.mark.quality)
