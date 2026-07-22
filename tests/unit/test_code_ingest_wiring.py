"""The code embed lane wired to RUN (bp-098) — the enable path CI-1..4 (bp-092..094) deferred.

CI-1..4 shipped the code embed lane but with an INERT flag (`[code_ingest].enabled` read by
nothing), no daemon enqueue of the `code_sync` KIND, and no CLI — flipping the flag did nothing
(finding-0159: the ON switch is part of finishing). These tests pin the three seams that make it
runnable through the proper discipline, all deterministic (no Ollama, no network; temp stores;
embedders build lazily so `build_components` runs fully offline):

  1. `CodeIngestConfig` — the loader now schemas `[code_ingest]`: OFF by default (a fresh clone
     does not ingest its own code), and a hand-authored local.toml override flips `enabled` on.
  2. `build_components` REGISTERS `code_sync` unconditionally (like vault_sync it eagerly opens the
     store) and `_housekeeping` enqueues the INCREMENTAL sync ONLY when `code_ingest.enabled` — the
     gate (note §2.7: a flag flip never fires the heavy seed).
  3. `Launcher.code_seed()` (the `palace code-seed` verb) inserts ONE deliberate `code_sync` job
     onto the shared supervisor queue — single-writer preserved (a job insert, never a store write
     from the CLI), independent of the incremental gate.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

from core.kernel.config import get_config, load_config
from ops.lifecycle.launcher import Launcher, build_components
from ops.lifecycle.runs import RunLedger
from scheduler.code_sync import CODE_SYNC_KIND
from scheduler.queue import JobQueue

# --- Item 1: CodeIngestConfig loader schema -------------------------------------------------


def test_code_ingest_defaults_off() -> None:
    """A fresh clone (defaults only) has the code lane OFF — the fail-safe default (finding-0159:
    ship the switch, gated off). `max_chars`/`overlap_chars` mirror the note chunker (§2.2)."""
    ci = get_config().code_ingest
    assert ci.enabled is False
    assert ci.max_chars == 1200
    assert ci.overlap_chars == 150


def test_code_ingest_local_override_enables(tmp_path, monkeypatch) -> None:
    """A hand-authored local.toml `[code_ingest] enabled=true` flips it on — the owner's deliberate
    enable act, honoring the overlay precedence (defaults ← levers ← local, loader.py)."""
    local = tmp_path / "local.toml"
    local.write_text("[code_ingest]\nenabled = true\n", encoding="utf-8")
    monkeypatch.setattr("core.kernel.config.loader._LOCAL", local)
    assert load_config().code_ingest.enabled is True


# --- temp-config fixture (mirrors tests/integration/test_lifecycle.py::_cfg) -----------------


def _cfg(root: Path, *, enabled: bool):
    """A fully temp-pathed Config (every store under `root`) so build_components runs in isolation,
    with `code_ingest.enabled` set. Mirrors the test_lifecycle `_cfg` path set exactly."""
    root.mkdir(parents=True, exist_ok=True)
    base = load_config()
    paths = dataclasses.replace(
        base.paths, data_dir=root, raw_store=root / "raw", vector_store=root / "v.lance",
        vault_catalog=root / "cat.sqlite", derived_store=root / "d.sqlite",
        attestation_store=root / "att.sqlite", telemetry_db=root / "t.duckdb")
    vault = dataclasses.replace(base.vault, path=root / "vault")
    code_ingest = dataclasses.replace(base.code_ingest, enabled=enabled)
    return dataclasses.replace(base, paths=paths, vault=vault, code_ingest=code_ingest)


def _housekeeping_kinds(comps) -> list[str]:
    """Run one housekeeping pass and return the KINDs it enqueued onto the (fresh) queue."""
    comps.enqueue_housekeeping()
    return [j.kind for j in comps.queue.list()]


# --- Item 2: daemon registration + gated housekeeping enqueue --------------------------------


def test_code_sync_handler_registered_regardless(tmp_path) -> None:
    """The handler registers unconditionally (like vault_sync it eagerly opens the vector store) so
    the supervisor can drain a deliberate code_seed job even before the incremental gate is on."""
    comps = build_components(_cfg(tmp_path, enabled=False))
    try:
        # .handlers is on the concrete Supervisor; the narrow SupervisorLike Components contract
        # hides it, so the runtime attribute access is annotated for the type-checker.
        assert CODE_SYNC_KIND in comps.supervisor.handlers  # type: ignore[attr-defined]
    finally:
        comps.queue.close()


def test_housekeeping_enqueues_code_sync_only_when_enabled(tmp_path) -> None:
    """The GATE: enabled=True → housekeeping enqueues exactly one incremental code_sync; enabled=
    False → none (the seed stays deliberate, note §2.7 — a flag flip never fires the heavy op)."""
    off = build_components(_cfg(tmp_path / "off", enabled=False))
    try:
        assert _housekeeping_kinds(off).count(CODE_SYNC_KIND) == 0
    finally:
        off.queue.close()
    on = build_components(_cfg(tmp_path / "on", enabled=True))
    try:
        assert _housekeeping_kinds(on).count(CODE_SYNC_KIND) == 1
    finally:
        on.queue.close()


# --- Item 3: palace code-seed -> a queued code_sync job --------------------------------------


def test_code_seed_enqueues_one_code_sync(tmp_path) -> None:
    """`palace code-seed` inserts ONE code_sync job onto the shared supervisor queue (single-writer:
    a job insert, never a store write from the CLI) and returns 0. Works with enabled=False — the
    seed is the deliberate owner-visible path, independent of the incremental housekeeping gate."""
    cfg = _cfg(tmp_path, enabled=False)
    launcher = Launcher(cfg=cfg, runs=RunLedger(tmp_path / "runs.sqlite"),
                        repo_root=Path(".").resolve())
    assert launcher.code_seed() == 0
    q = JobQueue(cfg.paths.data_dir / "queue.sqlite")
    try:
        assert [j.kind for j in q.list()].count(CODE_SYNC_KIND) == 1
    finally:
        q.close()
