# ── Family 1 boundary (labelings & information-flow) · symbols in docs/NOTATION.md ──
# OBJECT:    𝒜(agent) — capability as a set of tool handles ordered by inclusion (a bounded
#            meet-semilattice, top MAX = PRE_DECLARED_MAX; mint is the meet scope ∩ MAX).
# INVARIANT: 𝒜 never exceeds scope ∩ MAX; skills are non-widening 𝒜(a ⊕ ς) = 𝒜(a) (I13);
#            no shell/cred/net handle exists in MAX.
# ENFORCED:  structural — RoleTemplate.__post_init__ refuses scope ⊄ MAX; the dispatcher holds
#            only in-scope handles (dispatcher_for(resolved, …)); credentials are not a tool.
"""Base role library + the scope ceiling (BUILD-SPEC §9, §10; skills-and-scope).

A role template declares two SEPARATE things (never conflated): the instructional frame
(prompt + default tier + instructional skills = context) and the capability ceiling
(`scope` = the tool ids the role MAY use). Capability flows only from `scope ∩ MAX`,
resolved at mint and enforced at dispatch — a skill can never widen it.
"""

from __future__ import annotations

from dataclasses import dataclass

# The absolute pre-declared maximum (§10): the only tools ANY minted agent may EVER hold.
# There is deliberately NO shell / credential / network tool here — those capabilities do
# not exist as tools, so the factory is structurally incapable of minting them. A task that
# needs one is routed to the human gate, never satisfied by minting.
PRE_DECLARED_MAX: frozenset[str] = frozenset({"run_python"})


@dataclass(frozen=True)
class RoleTemplate:
    name: str
    prompt_fragment: str
    default_tier: str = "routine"
    scope: frozenset[str] = frozenset()      # tool ids this role MAY use (must be ≤ MAX)
    skills: tuple[str, ...] = ()             # instructional skills (CONTEXT only, no capability)

    def __post_init__(self) -> None:
        beyond = self.scope - PRE_DECLARED_MAX
        if beyond:
            raise ValueError(
                f"role {self.name!r} scope {sorted(beyond)} exceeds pre-declared max (§10)"
            )


# Base role library (§9). Health/financial are ordinary advisory roles governed by the
# Constitution's deference directive (Invariant 7), not special lockouts. Only coder and
# data_analyst hold the sandboxed run_python capability; the rest are advisory (scope = {}).
_ROLES = (
    RoleTemplate(
        "personal_assistant",
        "You are the owner's personal assistant. Be concise and practical; surface options "
        "and tradeoffs rather than issuing directives (Constitution §III.4).",
    ),
    RoleTemplate(
        "coder",
        "You are a coding assistant. Propose code and, when it helps, run it in the sandbox "
        "to check it. Report results honestly, including failures and uncertainty.",
        scope=frozenset({"run_python"}),
    ),
    RoleTemplate(
        "data_analyst",
        "You are a data analyst. Compute with sandboxed code, show your working, and never "
        "overstate certainty. Distinguish what the data shows from what you infer.",
        scope=frozenset({"run_python"}),
    ),
    RoleTemplate(
        "financial_advisor",
        "You are a financial advisor. Give substantive, well-grounded help and flag "
        "uncertainty plainly, but defer the final decision to the owner and a qualified "
        "professional (Constitution §III.3). Refuse genuinely dangerous specifics.",
    ),
    RoleTemplate(
        "health_research_advisor",
        "You are a health/research advisor. Be substantive and evidence-aware, surface "
        "evidence quality (not just conclusions), and defer final decisions to the owner "
        "and a clinician (Constitution §III.3, Invariant 7).",
        default_tier="synthesis",
    ),
    RoleTemplate(
        "writer_editor",
        "You are a writer and editor. Improve clarity, structure, and flow while preserving "
        "the owner's voice — never overwrite it.",
    ),
    RoleTemplate(
        "general_conversation",
        "You are a thoughtful conversational partner. Mirror, not oracle (Constitution "
        "§III.2): reflect patterns and hold interpretive claims loosely.",
    ),
)

BASE_ROLES: dict[str, RoleTemplate] = {r.name: r for r in _ROLES}
