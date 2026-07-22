"""bp-067 falsifiers — the config loader moved into `core.config` (finding-0103, the core-is-sacred
cleanup). These pin the three guarantees of the move: config VALUES are unchanged, `core.config` is
network-free (the security win of landing inside `import_lint`'s perimeter), and the trust boundary
held — core's `get_secret` is env-only while the outside facade stays token-capable.
"""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

from ops.import_lint import NETWORK_MODULES, scan_file

_REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").exists())
_CORE_CONFIG = _REPO_ROOT / "core" / "kernel" / "config"   # K1 (bp-090): config moved


def test_config_values_resolve_under_repo_root() -> None:
    """The move must not drift any config value. REPO_ROOT re-anchors to the real repo root (not
    `core/`), and the tomls (which stay in `config/`) still drive the same resolved paths."""
    from core.kernel.config import REPO_ROOT, get_config, load_config
    from core.kernel.config.loader import _DEFAULTS

    assert REPO_ROOT == _REPO_ROOT                               # re-anchored correctly (not core/)
    cfg = get_config()
    assert cfg.paths.data_dir == _REPO_ROOT / "data"            # defaults.toml data_dir="data"
    assert cfg.paths.derived_store == _REPO_ROOT / "data" / "derived.sqlite"
    assert cfg.paths.derived_store.parent == cfg.paths.data_dir
    # against the COMMITTED defaults (bypassing an owner's local.toml overlay, which may enable it):
    assert load_config(_DEFAULTS).secrets.enabled is False      # shipped-safe default preserved


def test_core_config_is_network_free() -> None:
    """The security win: `core/config/**` now falls under `import_lint`'s core ban, so config
    loading is STRUCTURALLY network-free — no file imports a networking primitive or a bad zone."""
    for py in _CORE_CONFIG.rglob("*.py"):
        violations = scan_file(py, repo_root=_REPO_ROOT)
        assert violations == [], f"{py} imports a banned module: {violations}"


def test_core_config_imports_no_first_party_sibling() -> None:
    """core.config is self-contained: nothing under it imports a first-party sibling of core
    (config/eval/ops/agents/edge/scheduler) — the whole point of moving the loader IN."""
    forbidden = {"config", "eval", "ops", "agents", "edge", "scheduler"}
    for py in _CORE_CONFIG.rglob("*.py"):
        tree = ast.parse(py.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                roots = [node.module]
            elif isinstance(node, ast.Import):
                roots = [a.name for a in node.names]
            else:
                continue
            for r in roots:
                assert r.split(".", 1)[0] not in forbidden, f"{py}:{node.lineno} {r}"


def test_core_get_secret_is_env_only() -> None:
    """The trust boundary held: core's `get_secret` is the ENV path only — no `token` parameter, and
    the module imports neither `secrets_backend` nor `hvac`, so the Vault path cannot leak in."""
    from core.kernel.config import get_secret

    params = inspect.signature(get_secret).parameters
    assert "token" not in params                                # env-only signature
    assert list(params) == ["name"]

    # No IMPORT of the network Vault wiring anywhere in the moved module (a docstring may NAME
    # build_secrets_backend in prose — an import is the leak, not a mention). AST, not substring.
    tree = ast.parse((_CORE_CONFIG / "loader.py").read_text(encoding="utf-8"))
    imported_roots = {
        (n.module.split(".", 1)[0] if isinstance(n, ast.ImportFrom) and n.module else
         (n.names[0].name.split(".", 1)[0] if isinstance(n, ast.Import) else ""))
        for n in ast.walk(tree) if isinstance(n, ast.Import | ast.ImportFrom)
    }
    imported_full = {
        n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module
    } | {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
    assert "config" not in imported_roots                       # no secrets_backend / config reach
    assert not any("secrets_backend" in m or "hvac" in m for m in imported_full)
    assert not (NETWORK_MODULES & imported_roots)               # no networking primitive imported


def test_outside_facade_stays_token_capable() -> None:
    """The outside `config.loader` facade preserves the FULL public surface for the ~147 non-core
    importers, including the token-capable `get_secret` (the machinery/Vault form) and the privates
    a couple of callers name."""
    import config.loader as facade

    params = inspect.signature(facade.get_secret).parameters
    assert "token" in params                                    # token-capable out here
    # the pure public API is re-exported (one source of truth — defined in core.config.loader)
    for name in ("get_config", "load_config", "Config", "REPO_ROOT", "LEVERS_OVERLAY"):
        assert hasattr(facade, name), f"facade missing {name}"
