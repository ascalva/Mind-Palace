"""Embedding adapter (BUILD-SPEC §8 derived layer).

Wraps the local embedding model. Documents are embedded plain; queries are wrapped in the
model's instruction format (Qwen3-Embedding is instruction-aware on the query side, which
materially improves retrieval). Embeddings are a regenerable derived representation —
re-embed from the raw store if the model changes (§8).
"""

from __future__ import annotations

from dataclasses import dataclass

from config.loader import EmbeddingConfig
from core.models.ollama_client import OllamaClient


@dataclass
class Embedder:
    client: OllamaClient
    config: EmbeddingConfig

    @property
    def dim(self) -> int:
        return self.config.dim

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        return self.client.embed(self.config.model, texts)

    def embed_query(self, text: str) -> list[float]:
        # Qwen3-Embedding query format: "Instruct: <task>\nQuery: <text>".
        wrapped = f"Instruct: {self.config.query_instruction}\nQuery: {text}"
        return self.client.embed(self.config.model, [wrapped])[0]


def build_embedder(config: object | None = None) -> Embedder:
    from config.loader import get_config

    cfg = config or get_config()
    return Embedder(client=OllamaClient(cfg.ollama), config=cfg.embedding)
