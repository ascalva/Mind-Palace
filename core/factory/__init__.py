"""Zone A — the dynamic agent factory + base role library (BUILD-SPEC §9, §10).

Mints personalized agents on demand from base role templates, each framed by the
Constitution (Invariant 6) and bounded by a hard scope ceiling: capability flows only from
`role.scope ∩ PRE_DECLARED_MAX`, resolved at mint and enforced at dispatch via
object-capability handles. Beyond-scope requests route to the human gate (`ops.gate`),
never to a privileged agent. Honors docs/design-notes/skills-and-scope.md.
"""

from core.factory.factory import AgentFactory, MintedAgent, build_factory
from core.factory.registry import AgentRegistry, PersistedAgent
from core.factory.roles import BASE_ROLES, PRE_DECLARED_MAX, RoleTemplate
from core.factory.tools import (
    ToolDispatcher,
    ToolNotInScopeError,
    ToolRegistry,
    ToolResult,
    ToolSpec,
    build_default_registry,
    dispatcher_for,
)

__all__ = [
    "BASE_ROLES",
    "PRE_DECLARED_MAX",
    "AgentFactory",
    "AgentRegistry",
    "MintedAgent",
    "PersistedAgent",
    "RoleTemplate",
    "ToolDispatcher",
    "ToolNotInScopeError",
    "ToolRegistry",
    "ToolResult",
    "ToolSpec",
    "build_default_registry",
    "build_factory",
    "dispatcher_for",
]
