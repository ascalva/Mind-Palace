"""Apply the `e2e` marker to every test collected under this directory.

Directory-level marking (test-organization.md §3): a test's *location* declares its
execution profile, so `-m e2e` selects this whole category without per-file decoration.
The path filter is load-bearing — pytest calls every conftest's
`pytest_collection_modifyitems` with the *global* item list, so we must only mark items
that actually live beneath this directory.
"""

from __future__ import annotations

import fcntl
import hashlib
import tempfile
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        try:
            item.path.relative_to(_HERE)
        except ValueError:
            continue  # not under this category dir — another conftest owns it
        item.add_marker(pytest.mark.e2e)


@pytest.fixture(autouse=True)
def _serialize_live_axis(request: pytest.FixtureRequest):  # type: ignore[no-untyped-def]
    """Cross-process mutual exclusion for `live`-marked tests (bp-023, finding-0046 +
    finding-0048): two separate pytest processes (a builder suite overlapping the
    orchestrator's gate, or two builder suites) hitting the single local Ollama endpoint
    concurrently produce a resource-contention race (async-unload race / empty-content
    mid-swap), not something an in-process lock can fix. An OS-level advisory file lock
    (`fcntl.flock`), keyed to the endpoint and acquired for the duration of each
    `live`-marked test, serializes the endpoint across processes.

    Autouse but a no-op for every non-`live` item — the fast tier pays nothing (Item 12
    invariant). `flock` is released by the kernel on process exit (even a kill -9), so a
    crashed builder cannot wedge the lock; there is no lock file cleanup to do.
    """
    if request.node.get_closest_marker("live") is None:
        yield
        return

    # Ground the endpoint from config.loader (the same import every live test already
    # uses to reach core.models.ollama_client's OllamaConfig) rather than hardcoding a
    # guessed URL (§6(a), plan bp-023). Import is local to the fixture so the collection
    # of `not live` runs never touches config loading for this fixture's sake.
    from config.loader import get_config

    endpoint = get_config().ollama.base_url
    key = hashlib.sha256(endpoint.encode()).hexdigest()[:16]
    lockfile = Path(tempfile.gettempdir()) / f"mp-live-ollama-{key}.lock"
    with open(lockfile, "w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)  # blocks until the other process releases
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)
