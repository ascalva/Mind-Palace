"""Dynamic agent factory (BUILD-SPEC §10).

Mints a personalized agent on demand as nested frames, outermost-first (Invariant 6):
    Constitution → base role template → task
then resolves the tool scope and binds a dispatcher holding ONLY the in-scope handles.

The scope ceiling is the whole safety story: a minted agent can never exceed its template's
scope, never be granted scope beyond `PRE_DECLARED_MAX`, and always inherits the
Constitution. A request for capability beyond that is **routed to the human gate**, never
satisfied by minting a privileged agent (§10). Capability is checked twice, by two
subsystems, at two times: at mint (scope resolution) and at dispatch (object-capability).
The advisory path (`respond`) and the action path (`invoke`) are kept separate — model
advises, code acts (Invariant 3).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.constitution import Message, frame_context
from core.factory.registry import AgentRegistry
from core.factory.roles import BASE_ROLES, PRE_DECLARED_MAX, RoleTemplate
from core.factory.tools import (
    ToolDispatcher,
    ToolNotInScopeError,
    ToolRegistry,
    ToolResult,
    dispatcher_for,
)
from core.models import ModelServer
from core.selfcheck import SelfCheck, SubjectiveJudge, self_evaluate
from ops.gate import GateRequest, HumanGate


@dataclass
class MintedAgent:
    name: str
    role: RoleTemplate
    scope: frozenset[str]            # resolved = role.scope ∩ PRE_DECLARED_MAX
    dispatcher: ToolDispatcher
    gate: HumanGate
    server: ModelServer | None = None
    ephemeral: bool = True

    def build_context(self, task: str, *, history: list[Message] | None = None) -> list[Message]:
        """Constitution outermost (Invariant 6); the role nests inside; task last."""
        return frame_context(self.role.prompt_fragment, task, history=history)

    def respond(self, task: str, *, history: list[Message] | None = None,
                judge: SubjectiveJudge | None = None,
                think: bool | None = None) -> tuple[str, SelfCheck]:
        """Advisory path: generate + run the Constitution pre-return check (§4)."""
        if self.server is None:
            raise RuntimeError(f"agent {self.name!r} has no model server bound")
        out = self.server.chat(self.role.default_tier,
                               self.build_context(task, history=history), think=think)
        return out, self_evaluate(out, judge=judge)   # advisory => no retrieval sources

    def invoke(self, tool_id: str, args: dict) -> ToolResult:
        """Action path: dispatch a tool the agent is scoped for. An out-of-scope id is
        unreachable in the dispatcher → route to the human gate and refuse (§10)."""
        try:
            return self.dispatcher.invoke(tool_id, args)
        except ToolNotInScopeError:
            self.gate.submit(
                "out_of_scope_tool",
                f"agent {self.name!r} requested {tool_id!r} outside its scope "
                f"{sorted(self.scope)}",
                agent=self.name,
            )
            raise


@dataclass
class AgentFactory:
    server: ModelServer | None = None
    tools: ToolRegistry = field(default_factory=ToolRegistry)
    gate: HumanGate = field(default_factory=HumanGate)
    roles: dict[str, RoleTemplate] = field(default_factory=lambda: dict(BASE_ROLES))
    agent_registry: AgentRegistry | None = None

    def mint(self, role_name: str, *, requested_tools: frozenset[str] = frozenset(),
             name: str | None = None, persist: bool = False) -> MintedAgent | GateRequest:
        """Mint an agent for `role_name`. If `requested_tools` reaches beyond the role's
        resolved scope ceiling, route to the human gate instead of minting (§10)."""
        if role_name not in self.roles:
            raise KeyError(f"unknown role {role_name!r}")
        role = self.roles[role_name]
        resolved = role.scope & PRE_DECLARED_MAX          # never beyond the pre-declared max
        beyond = frozenset(requested_tools) - resolved
        if beyond:
            return self.gate.submit(
                "privileged_mint",
                f"mint {role_name!r} requested capability beyond scope: {sorted(beyond)}",
            )
        agent = MintedAgent(
            name=name or role_name,
            role=role,
            scope=resolved,
            dispatcher=dispatcher_for(resolved, self.tools),
            gate=self.gate,
            server=self.server,
            ephemeral=not persist,
        )
        if persist and self.agent_registry is not None:
            self.agent_registry.promote(agent.name, role.name, resolved, role.default_tier)
        return agent


def build_factory(config=None, *, broker=None) -> AgentFactory:
    """Wire a factory against the real model server + default tool registry (run_python is
    available only if a sandbox `broker` is supplied)."""
    from core.factory.tools import build_default_registry
    from core.models import build_model_server

    server = build_model_server(config) if config is not False else None
    return AgentFactory(server=server, tools=build_default_registry(broker))
