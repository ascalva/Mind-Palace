"""Non-secret configuration. Secrets come from the macOS Keychain / environment only
(Invariant 10) — never from these files, never committed, never read by a model."""

from config.loader import (
    Config,
    ModelConfig,
    OllamaConfig,
    PathsConfig,
    ResourceConfig,
    get_config,
    get_secret,
    load_config,
)

__all__ = [
    "Config",
    "ModelConfig",
    "OllamaConfig",
    "PathsConfig",
    "ResourceConfig",
    "get_config",
    "get_secret",
    "load_config",
]
