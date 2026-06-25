"""Zone A — model serving (BUILD-SPEC §5, §7).

Two lifecycles kept separate: the *model* lifecycle (pull/update + the two-slot loader)
lives here; the *agent* lifecycle (the factory + registry) arrives in Phase 5. Nothing
is baked into Ollama — personas and params are injected at request time.
"""

from core.models.loader import TwoSlotLoader
from core.models.ollama_client import Message, OllamaClient, OllamaError
from core.models.registry import MemoryCeilingError, Registry, get_registry
from core.models.server import ModelServer, build_model_server

__all__ = [
    "Message",
    "MemoryCeilingError",
    "ModelServer",
    "OllamaClient",
    "OllamaError",
    "Registry",
    "TwoSlotLoader",
    "build_model_server",
    "get_registry",
]
