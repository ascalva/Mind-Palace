"""The agent taxonomy's role constructors + conformance (bp-070 D2, dn-agent-taxonomy §2.1).

Each role is a *region* of the ratified `(Σ, E, T, A)` lattice; a constructor must land an agent
INSIDE its region and REFUSE an out-of-region request, and `assert_conforms` must reject a handle
that exceeds the declared scope. These tests are that guard — the D2 analog of the Views'
declared-vs-actual `SCOPE` check (`test_view_scopes.py`). Composition is the EXISTING `Scope.meet`
(no new lattice ops), so the delegation law is reused verbatim, not re-proved here.
"""

from __future__ import annotations

import pytest

from core.agent_scope import (
    ConformanceError,
    Handle,
    assert_conforms,
    dreamer_scope,
    integrator_scope,
    query_scope,
    sensor_scope,
)
from core.scope import (
    Clock,
    Privilege,
    Stratum,
    StratumScope,
    Tier,
    WorldReach,
)


# ── each constructor lands inside its §2.1 region ─────────────────────────────────────────────
def test_sensor_scope_is_own_stratum_no_edges():
    """Sensor: its OWN stratum (downset), NO edges, the sensor-dual write bit W_Σ=1, W_world=NONE,
    clocked on its stratum's event clock N_s."""
    s = sensor_scope(Stratum.DIALOGUE)
    assert s.sigma.strata == StratumScope.of(Stratum.DIALOGUE).strata      # downset (+ refinements)
    assert Stratum.DIALOGUE_TRANSCRIPT in s.sigma.strata
    assert s.edges.fibers == frozenset()                        # produces nodes, not edges
    assert s.authority.privilege is Privilege.READ
    assert s.authority.store_write == 1                                    # the sensor dual
    assert s.authority.world is WorldReach.NONE
    assert s.time.clock is Clock.N_S
    assert s.tier is Tier.STATIC_GUARD


def test_query_scope_is_read_only_store_write_zero():
    """Query agent: reads a grantable subset, writes NOTHING structural (W_Σ=0), no world reach."""
    s = query_scope([Stratum.DIALOGUE, Stratum.OBSERVED])
    assert s.sigma.strata == StratumScope.of(Stratum.DIALOGUE, Stratum.OBSERVED).strata
    assert s.authority.privilege is Privilege.READ
    assert s.authority.store_write == 0                                    # the defining bit
    assert s.authority.world is WorldReach.NONE
    assert "C" in s.edges.fibers                                # may READ every edge class


def test_integrator_scope_spans_two_base_strata_and_writes_c_or_f():
    """Integrator: ≥ 2 BASE strata, edge-store writes over fibers ⊆ {C, F}, W_Σ=1, W_world=NONE."""
    s = integrator_scope(
        [(Stratum.DIALOGUE_TRANSCRIPT, "L1-action-log"), (Stratum.OBSERVED, "commit-ledger")],
        ["C", "F"],
    )
    assert {Stratum.DIALOGUE_TRANSCRIPT, Stratum.OBSERVED} <= s.sigma.strata
    assert s.edges.fibers == frozenset({"C", "F"})
    assert s.authority.store_write == 1
    assert s.authority.world is WorldReach.NONE


def test_dreamer_scope_is_apex_all_fibers():
    """Dreamer: up to ⊤_Σ per grant, ALL edge fibers, interpreted-only projection-write (W_Σ=1)."""
    s = dreamer_scope([Stratum.DIALOGUE, Stratum.OBSERVED, Stratum.MIRROR])
    assert s.edges.fibers == frozenset({"F", "D", "C"})                    # all edge types
    assert s.authority.store_write == 1
    assert s.authority.world is WorldReach.NONE


# ── the falsifier: a constructor CANNOT express an out-of-region scope ─────────────────────────
def test_integrator_rejects_single_base_stratum():
    """An integrator is inherently multi-strata: naming layers of ONE base stratum (which would be a
    sensor's region) is refused — the 'a constructor expresses an out-of-region scope' falsifier."""
    with pytest.raises(ValueError):
        integrator_scope(
            # both refine the SAME base stratum (dialogue) — a sensor's region, not an integrator's
            [(Stratum.DIALOGUE_TRANSCRIPT, "L0"), (Stratum.DIALOGUE_ARTIFACT, "docs")],
            ["C"],
        )


def test_integrator_rejects_write_fiber_outside_c_f():
    """D (supersession) is the D-machinery's, never an integrator's — a D write grant is refused."""
    with pytest.raises(ValueError):
        integrator_scope(
            [(Stratum.DIALOGUE_TRANSCRIPT, "L1"), (Stratum.OBSERVED, "commit")],
            ["C", "D"],
        )


# ── delegation is monotone — the EXISTING Scope.meet, reused (never widens the parent) ─────────
def test_delegation_meet_never_widens_the_parent():
    """meet(parent, template) ⊑ parent AND ⊑ template for role templates — the ratified delegation
    law reused verbatim (no new lattice op). A wide template cannot launder authority up to a narrow
    parent."""
    narrow = query_scope([Stratum.DIALOGUE])                              # ledger clock (N)
    wide = query_scope([Stratum.DIALOGUE, Stratum.OBSERVED, Stratum.OPS])
    minted = narrow.meet(wide)
    assert minted <= narrow and minted <= wide
    assert minted == narrow                                    # meet with a superset = parent

    # same law over the integrator region (COMMIT clock)
    p = integrator_scope(
        [(Stratum.DIALOGUE_TRANSCRIPT, "L1"), (Stratum.OBSERVED, "commit")], ["C"]
    )
    t = integrator_scope(
        [(Stratum.DIALOGUE_TRANSCRIPT, "L1"), (Stratum.OBSERVED, "commit"),
         (Stratum.REFERENCE_REPO, "docs")],
        ["C", "F"],
    )
    assert p.meet(t) <= p and p.meet(t) <= t


# ── conformance: an agent's actual handles ⊑ its declared scope ────────────────────────────────
def test_assert_conforms_accepts_a_matching_inventory():
    """A sensor over dialogue holding a handle on its refinement `dialogue_transcript` (inside the
    downset) that projection-writes (its W_Σ=1) conforms — no raise."""
    declared = sensor_scope(Stratum.DIALOGUE)
    handles = (
        Handle(name="rawstore", stratum=Stratum.DIALOGUE_TRANSCRIPT, writes_stratum=True),
        Handle(name="chatlog", stratum=Stratum.DIALOGUE_TRANSCRIPT, writes_stratum=True),
    )
    assert_conforms(declared, handles)          # does not raise


def test_assert_conforms_rejects_a_handle_outside_the_declared_sigma():
    """The smuggled-extra-handle falsifier: a sensor over dialogue holding a handle on `observed`
    (outside its declared Σ) is caught."""
    declared = sensor_scope(Stratum.DIALOGUE)
    handles = (Handle(name="smuggled", stratum=Stratum.OBSERVED),)
    with pytest.raises(ConformanceError):
        assert_conforms(declared, handles)


def test_assert_conforms_rejects_projection_write_beyond_authority():
    """A query agent (W_Σ=0) may not hold a projection-writing handle — conformance catches it."""
    declared = query_scope([Stratum.DIALOGUE])
    handles = (Handle(name="writer", stratum=Stratum.DIALOGUE, writes_stratum=True),)
    with pytest.raises(ConformanceError):
        assert_conforms(declared, handles)


def test_assert_conforms_rejects_edge_write_outside_declared_e():
    """A sensor writes no edges (E=⊥); a handle claiming to write fiber C exceeds the declared E."""
    declared = sensor_scope(Stratum.DIALOGUE)
    handles = (Handle(name="edge-writer", stratum=Stratum.DIALOGUE, writes_fiber="C"),)
    with pytest.raises(ConformanceError):
        assert_conforms(declared, handles)
