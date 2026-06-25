"""Sealed-core runtime entrypoint.

Any Zone-A process starts here. It installs the egress guard FIRST (Invariant 1), so
"the core has no egress" holds before any work runs, then wires the Zone-A services
(models, telemetry, vitals) and exposes an agent factory seam. Sealing is done here —
explicitly, at startup — rather than as an import side effect, so importing core
modules for tests/tools is free of surprises.
"""

from __future__ import annotations

from dataclasses import dataclass

from config.loader import Config, get_config
from core.agent import Agent
from core.constitution import constitution_fingerprint
from core.models import ModelServer, build_model_server
from core.sealing import assert_sealed, seal
from core.stores.telemetry import TelemetryStore, open_store
from core.vitals import VitalsCollector


@dataclass
class Core:
    config: Config
    models: ModelServer
    telemetry: TelemetryStore
    vitals: VitalsCollector
    constitution_fingerprint: str

    def make_agent(self, name: str, role_prompt: str, tier: str = "routine") -> Agent:
        """Mint a trivial agent bound to the model server. Every agent inherits the
        Constitution via `core.constitution.frame_context` (Invariant 6)."""
        return Agent(name=name, role_prompt=role_prompt, tier=tier, server=self.models)


def bootstrap(config: Config | None = None) -> Core:
    seal()           # structural egress guard BEFORE anything else (Invariant 1)
    assert_sealed()
    config = config or get_config()
    store = open_store(config)
    return Core(
        config=config,
        models=build_model_server(config),
        telemetry=store,
        vitals=VitalsCollector(store.writer()),
        constitution_fingerprint=constitution_fingerprint(),
    )
