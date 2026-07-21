"""D-0 Item 1 — the DreamCharter type + the instrument ceiling (bp-079, dn-synchronic-diachronic
-dreamer §2.2 SD-2).

The charter is the typed dream-dispatch record with STRUCTURAL refusal at construction. These are
the guard-tier tests §2.2 licenses:

  * an instrument grant outside INSTRUMENT_MAX is **refused** at construction (never clamped — the
    D-0 falsifier: a code path that silently narrows an over-ceiling set instead of refusing);
  * the scope grant equals the `core.scope` meet on fixtures (the charter is a *client* of the
    algebra, not a re-implementation);
  * gauge defaults ANCHORED; RETRO/ARCHIVAL construct-but-refuse, naming the SD-b park;
  * invariants: output authority stays `(READ, W_Σ=1, NONE)`; 𝔇 (FOUNDATION) is subtracted from
    every grant.
"""

from __future__ import annotations

import pytest

from core.agent_scope import dreamer_scope
from core.dreaming.charter import (
    INSTRUMENT_MAX,
    Budget,
    DreamCharter,
    Gauge,
    Instrument,
    InstrumentCeilingError,
)
from core.scope import (
    Authority,
    Privilege,
    Scope,
    Stratum,
    StratumScope,
    WorldReach,
)


def _budget() -> Budget:
    return Budget(node_ceiling=1000, edge_ceiling=5000, eigensolve_dim_cap=64, walk_budget=10_000)


def _owner_grant(*strata: Stratum) -> Scope:
    """A broad owner grant over `strata` — a dreamer_scope is the natural owner grant shape (it
    carries the role's `(READ, W_Σ=1, NONE)` authority the meet must preserve)."""
    return dreamer_scope(strata)


# ── the scope grant IS the meet (client of the algebra, not a re-implementation) ───────────────
def test_grant_is_the_meet_of_owner_and_dreamer_scope():
    owner = _owner_grant(Stratum.MIRROR, Stratum.OBSERVED, Stratum.INTERPRETED)
    charter = DreamCharter.mint(
        owner_grant=owner,
        strata=[Stratum.MIRROR, Stratum.INTERPRETED],
        instruments={Instrument.CENSUS},
        budget=_budget(),
    )
    expected = owner.meet(dreamer_scope([Stratum.MIRROR, Stratum.INTERPRETED]))
    assert charter.grant == expected
    # the meet narrowed Σ to the intersection (OBSERVED dropped)
    assert charter.grant.sigma.strata == StratumScope.of(Stratum.MIRROR, Stratum.INTERPRETED).strata
    assert Stratum.OBSERVED not in charter.grant.sigma.strata


def test_meet_is_monotone_delegation():
    """`meet(owner, template) ⊑ owner` — the ratified delegation law, reused, not re-proved."""
    owner = _owner_grant(Stratum.MIRROR, Stratum.OBSERVED)
    charter = DreamCharter.mint(
        owner_grant=owner,
        strata=[Stratum.MIRROR],
        instruments=set(),
        budget=_budget(),
    )
    assert charter.grant <= owner


# ── the instrument ceiling: REFUSE, never clamp (the D-0 falsifier) ────────────────────────────
def test_instrument_within_ceiling_is_accepted():
    charter = DreamCharter.mint(
        owner_grant=_owner_grant(Stratum.MIRROR),
        strata=[Stratum.MIRROR],
        instruments={Instrument.SIGMA_STAR_MST, Instrument.CENSUS},
        budget=_budget(),
    )
    assert charter.instruments == frozenset({Instrument.SIGMA_STAR_MST, Instrument.CENSUS})


def test_full_registry_is_the_ceiling():
    """INSTRUMENT_MAX is exactly the registry — granting all of it is admissible."""
    charter = DreamCharter.mint(
        owner_grant=_owner_grant(Stratum.MIRROR),
        strata=[Stratum.MIRROR],
        instruments=INSTRUMENT_MAX,
        budget=_budget(),
    )
    assert charter.instruments == INSTRUMENT_MAX
    assert INSTRUMENT_MAX == frozenset(Instrument)


class _FakeInstrument(str):
    """A red-team handle masquerading as an instrument — outside INSTRUMENT_MAX by construction."""


def test_instrument_outside_ceiling_refuses_at_construction():
    """The falsifier: an over-ceiling instrument must RAISE, not be silently clamped away."""
    rogue = frozenset({Instrument.CENSUS, _FakeInstrument("world_effector")})
    with pytest.raises(InstrumentCeilingError):
        DreamCharter.mint(
            owner_grant=_owner_grant(Stratum.MIRROR),
            strata=[Stratum.MIRROR],
            instruments=rogue,  # type: ignore[arg-type]
            budget=_budget(),
        )


def test_over_ceiling_is_not_clamped_to_the_intersection():
    """Directly assert the anti-shape is absent: an over-ceiling set never yields a charter whose
    instruments are the clamped intersection `grant ∩ MAX` — it raises instead."""
    rogue = frozenset({_FakeInstrument("shell")})
    with pytest.raises(InstrumentCeilingError):
        DreamCharter.mint(
            owner_grant=_owner_grant(Stratum.MIRROR),
            strata=[Stratum.MIRROR],
            instruments=rogue,  # type: ignore[arg-type]
            budget=_budget(),
        )


# ── the gauge: ANCHORED live, RETRO/ARCHIVAL construct-but-refuse (SD-b) ───────────────────────
def test_gauge_defaults_anchored():
    charter = DreamCharter.mint(
        owner_grant=_owner_grant(Stratum.MIRROR),
        strata=[Stratum.MIRROR],
        instruments=set(),
        budget=_budget(),
    )
    assert charter.gauge is Gauge.ANCHORED


@pytest.mark.parametrize("gauge", [Gauge.RETRO, Gauge.ARCHIVAL])
def test_parked_gauge_refuses_naming_sd_b(gauge: Gauge):
    with pytest.raises(NotImplementedError, match="SD-b"):
        DreamCharter.mint(
            owner_grant=_owner_grant(Stratum.MIRROR),
            strata=[Stratum.MIRROR],
            instruments=set(),
            budget=_budget(),
            gauge=gauge,
        )


# ── invariants: output authority (READ, W_Σ=1, NONE); 𝔇 subtracted ────────────────────────────
def test_output_authority_is_read_wsigma1_none():
    charter = DreamCharter.mint(
        owner_grant=_owner_grant(Stratum.MIRROR, Stratum.INTERPRETED),
        strata=[Stratum.MIRROR, Stratum.INTERPRETED],
        instruments=set(),
        budget=_budget(),
    )
    a = charter.grant.authority
    assert a.privilege is Privilege.READ
    assert a.store_write == 1                      # interpreted-only projection write
    assert a.world is WorldReach.NONE              # zero world reach


def test_grant_narrowing_output_authority_is_refused():
    """A malformed owner grant that would narrow the dreamer's interpreted-write bit (W_Σ=0) cannot
    yield a charter — the output-authority invariant is enforced at construction."""
    # A read-only owner grant (W_Σ=0) meets the dreamer role down to W_Σ=0 — not the role's output.
    read_only_owner = Scope(
        sigma=StratumScope.of(Stratum.MIRROR),
        edges=dreamer_scope([Stratum.MIRROR]).edges,
        time=dreamer_scope([Stratum.MIRROR]).time,
        authority=Authority(Privilege.READ, 0, WorldReach.NONE),
        tier=dreamer_scope([Stratum.MIRROR]).tier,
    )
    with pytest.raises(ValueError, match="output authority"):
        DreamCharter.mint(
            owner_grant=read_only_owner,
            strata=[Stratum.MIRROR],
            instruments=set(),
            budget=_budget(),
        )


def test_foundation_naming_grant_is_inadmissible():
    """𝔇 (FOUNDATION) is subtracted from every grant — a charter over a grant that names it refuses.
    Constructed directly (dreamer_scope/StratumScope.of would not surface FOUNDATION via the meet),
    exercising the denylist-ideal check in __post_init__."""
    tainted = Scope(
        sigma=StratumScope(frozenset({Stratum.MIRROR, Stratum.FOUNDATION})),
        edges=dreamer_scope([Stratum.MIRROR]).edges,
        time=dreamer_scope([Stratum.MIRROR]).time,
        authority=Authority(Privilege.READ, 1, WorldReach.NONE),
        tier=dreamer_scope([Stratum.MIRROR]).tier,
    )
    with pytest.raises(ValueError, match="denylist"):
        DreamCharter(
            grant=tainted,
            instruments=frozenset(),
            budget=_budget(),
        )


# ── the budget guards its own inputs ───────────────────────────────────────────────────────────
def test_budget_refuses_negative_ceiling():
    with pytest.raises(ValueError, match="non-negative"):
        Budget(node_ceiling=-1, edge_ceiling=10, eigensolve_dim_cap=8, walk_budget=10)
