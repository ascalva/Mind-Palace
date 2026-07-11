"""ModelServer — the facade agents use to talk to local models.

Combines the registry, the two-slot loader, and the Ollama client so callers say
"chat at the synthesis tier" and the right model is made resident first (model
advises, code acts). Persona/params are passed through at request time.
"""

from __future__ import annotations

from dataclasses import dataclass

from config.loader import Config, get_config
from core.constitution import Message
from core.models.loader import ModelConfig, TwoSlotLoader
from core.models.ollama_client import OllamaClient
from core.models.registry import Registry


@dataclass
class ModelServer:
    config: Config
    client: OllamaClient
    loader: TwoSlotLoader

    def version(self) -> str:
        return self.client.version()

    def ensure_pinned(self, *, warm: bool = True) -> ModelConfig:
        return self.loader.ensure_pinned(warm=warm)

    def chat(self, tier: str, messages: list[Message], *,
             think: bool | None = None, temperature: float | None = None) -> str:
        model = self.loader.ensure_tier(tier)
        return self.client.chat(
            model.name,
            messages,
            num_ctx=model.num_ctx,
            think=think,
            temperature=temperature,
            keep_alive=self.config.ollama.default_keep_alive,
        )


def build_model_server(config: Config | None = None) -> ModelServer:
    config = config or get_config()
    client = OllamaClient(config.ollama)
    registry = Registry(config)
    loader = TwoSlotLoader(config=config, client=client, registry=registry)
    return ModelServer(config=config, client=client, loader=loader)
