# ── Family 1 boundary (capability algebra) · the dispatch record · docs/NOTATION.md ──────────────
# OBJECT:    the DreamCharter — a dream dispatch as a typed record (scope grant, instrument grant ⊆
#            INSTRUMENT_MAX, budget, gauge), the worked example of dn-agent-taxonomy's "role = scope
#            signature" at full depth (dn-sd-dreamer §2.2, N1). The scope grant is
#            `meet(owner_grant, dreamer_scope(strata))` — the ratified delegation law, reused, never
#            re-implemented; the instrument grant reuses the factory's `scope ∩ MAX` ceiling shape.
# INVARIANT: output authority stays the dreamer role's `(READ, W_Σ=1, NONE)` (interpreted writes,
#            zero world reach); 𝔇 (FOUNDATION) is subtracted from every grant (`⊤_Σ = R ∖ 𝔇`); an
#            instrument set is REFUSED at construction if it exceeds INSTRUMENT_MAX (refuse, never
#            clamp — the factory's named anti-shape); RETRO/ARCHIVAL gauges are construct-but-refuse
#            (their dispatch paths are parked, SD-b). No store import in this module.
# ENFORCED:  static (pure-core typing; mypy-checked) + guard (tests/unit/test_dream_charter.py: an
#            over-ceiling instrument raises; grant equals the meet on fixtures; gauge
#            defaults ANCHORED; RETRO/ARCHIVAL refuse with SD-b named; a FOUNDATION-naming grant is
#            inadmissible).
"""The dream-dispatch record (dn-synchronic-diachronic-dreamer §2.2 SD-2, N1).

A dream dispatch is a typed `DreamCharter` binding four things:

  1. the **scope grant** — `meet(owner_grant, dreamer_scope(strata))`: the owner declares strata
     (per-scope-grant, dn-cross-strata-dreamer), the role constructor supplies the region, and
     the meet is the ratified delegation law (`Scope.meet`, non-negotiable #6). This module
     never re-implements the algebra — it is a *client* of it (§2.3, the algebra-as-tools ruling);
  2. the **instrument grant** — the dreamer's senses are named tool handles over evaluators (σ*/MST,
     conductance-profile, census, persistence), granted as a set `⊆ INSTRUMENT_MAX`, resolved at
     construction with the factory's existing ceiling pattern (`core/factory/roles.py:24-40`:
     capability = `scope ∩ MAX`, **refuse** at construction, never widen — and, per the falsifier,
     never silently *clamp*). Instruments are NOT a scope coordinate — they are a capability over
     *code*, result-side machinery over already-granted reads (§2.1 visibility test);
  3. the **budget** — the L3 cost-model parameters (node/edge ceilings, eigensolve dimension cap,
     walk budget) the refusal gate reads (`core.dreaming.evaluate`);
  4. the **gauge** — ANCHORED by default; RETRO/ARCHIVAL are declared descriptors (the enum keeps
     them, so a reading can pin its gauge fingerprint) but their dispatch paths are parked (SD-b),
     so constructing a charter with one refuses, naming the park.

PURE-CORE: imports only `core.scope` and `core.agent_scope` (both pure-core themselves). It reads no
store, materializes no clock, wires no read-path gate — the enforcement is the algebra's own
(admissibility) plus the guard-tier tests. The materialization boundary lives next door in
`core.dreaming.evaluate`; this module is only the record and its construction-time refusals.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum

from core.agent_scope import dreamer_scope
from core.scope import (
    DENYLIST_IDEAL,
    Authority,
    Privilege,
    Scope,
    Stratum,
    WorldReach,
    admissible,
)

# ═══════════════════════════════════════════════════════════════════════════════════════════════
# The instruments — named tool handles over evaluators, and the ceiling INSTRUMENT_MAX
# ═══════════════════════════════════════════════════════════════════════════════════════════════


class Instrument(StrEnum):
    """A named tool handle over an evaluator — the dreamer's *senses* (§2.2-2, §2.3). Each is a
    capability over code (a name-to-callable binding at mint), NOT a scope coordinate. The initial
    registry (the note's §2.2 exemplars); the code does not yet settle a member's machinery beyond
    the handle, so a member demanding more than a name-to-callable binding is a finding (plan §10,
    Q3). Their math is built elsewhere (`core/graph/`, spine-side census, FB-1) and consumed by
    later plans (bp-080/082) — this registry only *names* what a grant may hold."""

    SIGMA_STAR_MST = "sigma_star_mst"            # σ*/MST — max-spanning-tree keystone (core/graph)
    CONDUCTANCE_PROFILE = "conductance_profile"  # conductance / heat-kernel readings (core/graph)
    CENSUS = "census"                            # arrow-aware combinatorial census (spine-side)
    PERSISTENCE = "persistence"                  # σ-persistence, strength-gated surfacing (FB-1)


# INSTRUMENT_MAX — the absolute ceiling on the instrument grant (§2.2-2, the factory's
# PRE_DECLARED_MAX analog). A grant is refused at construction if it names anything outside it.
# Deliberately the full registry today; a narrower deployed ceiling is a later plan's owner call.
INSTRUMENT_MAX: frozenset[Instrument] = frozenset(Instrument)


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# The gauge — a declared descriptor, ANCHORED live; RETRO/ARCHIVAL parked (SD-b)
# ═══════════════════════════════════════════════════════════════════════════════════════════════


class Gauge(StrEnum):
    """The gauge of a (past) read (`graph-at-a-past-cut` D4) — a result-side declared descriptor,
    NOT a scope coordinate (§2.1). ANCHORED (today's vectors, membership-at-c) is the only live one;
    RETRO (content-at-c re-embedded) and ARCHIVAL name then-geometry whose dispatch paths are parked
    (SD-b, waits on `graph-at-a-past-cut`'s graduation). The enum keeps all three so a reading can
    pin its gauge fingerprint (the declared-descriptor discipline); constructing a charter with a
    parked gauge refuses (see `DreamCharter.__post_init__`)."""

    ANCHORED = "anchored"
    RETRO = "retro"
    ARCHIVAL = "archival"


_PARKED_GAUGES: frozenset[Gauge] = frozenset({Gauge.RETRO, Gauge.ARCHIVAL})


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# The budget — the L3 cost-model parameters the refusal gate reads (§2.4 L3)
# ═══════════════════════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class Budget:
    """The dispatch's cost ceilings (§2.2-3 / §2.4 L3) — the parameters the estimate-then-force
    refusal gate (`core.dreaming.evaluate`) compares an estimate against. Metadata-scale integers
    (node/edge counts, eigensolve dimension, walk steps); a force whose *estimate* exceeds any of
    these is refused before a single row is read (L3, rule-#8 kin — the memory-ceiling scheduler
    refusal extended to views)."""

    node_ceiling: int
    edge_ceiling: int
    eigensolve_dim_cap: int
    walk_budget: int

    def __post_init__(self) -> None:
        negatives = {
            name: v
            for name, v in (
                ("node_ceiling", self.node_ceiling),
                ("edge_ceiling", self.edge_ceiling),
                ("eigensolve_dim_cap", self.eigensolve_dim_cap),
                ("walk_budget", self.walk_budget),
            )
            if v < 0
        }
        if negatives:
            raise ValueError(f"Budget ceilings must be non-negative — got {negatives}")


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# The dispatch record itself
# ═══════════════════════════════════════════════════════════════════════════════════════════════


class InstrumentCeilingError(ValueError):
    """An instrument grant names a handle outside INSTRUMENT_MAX. Refused at construction — the
    factory's `scope ∩ MAX` ceiling shape (`core/factory/roles.py:35-40`), and per the D-0 falsifier
    the refusal is a REFUSE, never a silent clamp (`grant ∩ MAX` would narrow, hiding the owner's
    over-grant)."""


# The dreamer role's output authority (§2.2-1): interpreted-only projection-write into the scoped
# strata (W_Σ=1), advisory read privilege, zero world reach. Every charter's grant must preserve it.
_DREAMER_OUTPUT_AUTHORITY: Authority = Authority(Privilege.READ, 1, WorldReach.NONE)


@dataclass(frozen=True)
class DreamCharter:
    """A dream dispatch as a typed record (§2.2 SD-2). Construct via `mint` — it composes the scope
    grant from `owner_grant` and `dreamer_scope(strata)` (the ratified meet) and applies every
    construction-time refusal. The stored `grant` is the composed `Scope`; `instruments` is the
    resolved instrument grant (⊆ INSTRUMENT_MAX); `budget` the cost ceilings; `gauge` the declared
    descriptor (ANCHORED live).

    Refusals (all at construction, guard/structural tier):
      * an instrument outside INSTRUMENT_MAX → `InstrumentCeilingError` (refuse, never clamp);
      * a grant naming FOUNDATION (𝔇) → `ValueError` (the denylist ideal, `⊤_Σ = R ∖ 𝔇`);
      * a grant that does not preserve the dreamer's `(READ, W_Σ=1, NONE)` output authority →
        `ValueError` (a malformed owner grant cannot narrow the role's interpreted-write bit);
      * a parked gauge (RETRO/ARCHIVAL) → `NotImplementedError`, naming SD-b.
    """

    grant: Scope
    instruments: frozenset[Instrument]
    budget: Budget
    gauge: Gauge = Gauge.ANCHORED

    def __post_init__(self) -> None:
        beyond = self.instruments - INSTRUMENT_MAX
        if beyond:
            raise InstrumentCeilingError(
                f"instrument grant {sorted(str(i) for i in beyond)} exceeds INSTRUMENT_MAX "
                f"{sorted(i.value for i in INSTRUMENT_MAX)} — refused at construction, not clamped "
                f"(dn-synchronic-diachronic-dreamer §2.2; the factory ceiling pattern)"
            )
        # 𝔇 stays subtracted from every grant — a grant naming FOUNDATION is inadmissible.
        if not admissible(self.grant, [DENYLIST_IDEAL]):
            raise ValueError(
                f"grant names a denylist stratum (𝔇 = FOUNDATION) — inadmissible; ⊤_Σ = R ∖ 𝔇 "
                f"(got Σ={sorted(s.value for s in self.grant.sigma.strata)})"
            )
        # Output authority is the dreamer role's — interpreted-only writes, zero world reach.
        if self.grant.authority != _DREAMER_OUTPUT_AUTHORITY:
            raise ValueError(
                f"grant authority {self.grant.authority} does not preserve the dreamer's output "
                f"authority {_DREAMER_OUTPUT_AUTHORITY} — a malformed owner grant cannot narrow "
                f"the interpreted-write bit (§2.2-1)"
            )
        if self.gauge in _PARKED_GAUGES:
            raise NotImplementedError(
                f"gauge {self.gauge.value!r} is parked (SD-b — RETRO/ARCHIVAL dispatch paths wait "
                f"on the `graph-at-a-past-cut` family's graduation); only ANCHORED is live"
            )

    @classmethod
    def mint(
        cls,
        owner_grant: Scope,
        strata: Iterable[Stratum],
        instruments: Iterable[Instrument],
        budget: Budget,
        gauge: Gauge = Gauge.ANCHORED,
    ) -> DreamCharter:
        """Compose the record. The scope grant is `meet(owner_grant, dreamer_scope(strata))`
        via the ratified delegation law (`Scope.meet`; `meet(parent, template) ⊑ parent`,
        non-negotiable #6), never re-implemented here. All construction-time refusals fire in
        `__post_init__`."""
        grant = owner_grant.meet(dreamer_scope(strata))
        return cls(
            grant=grant,
            instruments=frozenset(instruments),
            budget=budget,
            gauge=gauge,
        )
