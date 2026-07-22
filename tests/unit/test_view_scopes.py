"""The five Views' declared `SCOPE` matches the algebra AND their disposition (bp-039 Item 3).

`req()` is a DECLARATION, not enforcement: each View carries a `SCOPE` ClassVar from the
dn-capability-scope §2.4 table. These tests are the declared-vs-actual guard — the constant equals
the table row AND matches what the View really is (its tier, its read-only authority, its fibers).
The bit-identical-reads proof (the whole-plan falsifier) is the EXISTING View suites passing
unmodified; here we additionally confirm `SCOPE` is a ClassVar (not a dataclass field), so it
changed neither construction nor any read.
"""

from __future__ import annotations

import dataclasses

from core.kernel.mirror import MirrorView
from core.kernel.scope import (
    DEPLOYED_WORLD_CEILING,
    Clock,
    Privilege,
    Stratum,
    Tier,
    WindowKind,
    WorldReach,
)
from core.ops_view import OpsView
from core.reference_view import ReferenceView
from core.temporal_view import TemporalView
from ops.effects import EffectView, ReversibilityClass, world_reach


# ── the table rows (dn-capability-scope §2.4, [VERIFIED] in the fable pass S7) ─────────────────
def test_mirror_view_scope_matches_table():
    s = MirrorView.SCOPE
    assert s.sigma.strata == frozenset({Stratum.MIRROR_AUTHORED})
    assert s.edges.fibers == frozenset()
    assert s.time.clock is Clock.PROJECTION_EVENT
    assert s.time.window.kind is WindowKind.POINT
    assert s.authority.privilege is Privilege.READ
    assert s.authority.store_write == 0
    assert s.authority.world is WorldReach.NONE
    assert s.tier is Tier.STRUCTURAL


def test_reference_view_scope_matches_table():
    s = ReferenceView.SCOPE
    assert s.sigma.strata == frozenset({Stratum.REFERENCE_REPO})
    assert s.edges.fibers == frozenset({"F"})
    assert s.time.clock is Clock.COMMIT
    assert s.authority.privilege is Privilege.READ
    assert s.authority.store_write == 0
    assert s.authority.world is WorldReach.NONE
    assert s.tier is Tier.STATIC_GUARD


def test_temporal_view_scope_matches_table():
    s = TemporalView.SCOPE
    assert s.sigma.strata == frozenset({Stratum.REFERENCE_REPO})
    assert s.edges.fibers == frozenset({"F", "D"})     # the ONLY View carrying D (supersession)
    assert s.time.clock is Clock.COMMIT
    assert s.authority.world is WorldReach.NONE
    assert s.tier is Tier.STATIC_GUARD


def test_ops_view_scope_matches_table():
    s = OpsView.SCOPE
    assert s.sigma.strata == frozenset({Stratum.OPS})
    assert s.edges.fibers == frozenset()
    assert s.time.clock is Clock.LAST_WRITE
    assert s.authority.world is WorldReach.NONE
    assert s.tier is Tier.STATIC_GUARD


def test_effect_view_scope_matches_table():
    s = EffectView.SCOPE
    assert s.sigma.strata == frozenset({Stratum.WORLD})
    assert s.edges.fibers == frozenset()
    assert s.time.clock is Clock.NOW
    assert s.authority.privilege is Privilege.READ
    assert s.authority.store_write == 0
    # ε = world_reach(default ceiling SENSING); a view's reach is world_reach(ceiling).
    assert s.authority.world == world_reach(ReversibilityClass.SENSING)
    assert s.tier is Tier.STRUCTURAL


# ── declared-vs-actual disposition (the constant matches what the View really IS) ─────────────
def test_only_temporal_view_carries_the_supersession_fiber_D():
    assert "D" in TemporalView.SCOPE.edges.fibers
    for V in (MirrorView, ReferenceView, OpsView, EffectView):
        assert "D" not in V.SCOPE.edges.fibers


def test_all_five_views_are_read_only_and_store_write_zero():
    """Every View is a reader: P = READ (never READ_PROPOSE), W_Σ = 0 (no projection-write — that is
    the sensor's dual, not a View's)."""
    for V in (MirrorView, ReferenceView, TemporalView, OpsView, EffectView):
        assert V.SCOPE.authority.privilege is Privilege.READ
        assert V.SCOPE.authority.store_write == 0


def test_structural_views_are_mirror_and_effect_only():
    """MirrorView/EffectView are STRUCTURAL (illegal state unconstructable); the other three are
    STATIC_GUARD (typed reads + a no-mutator integrity test) — honestly the weaker tier."""
    assert MirrorView.SCOPE.tier is Tier.STRUCTURAL
    assert EffectView.SCOPE.tier is Tier.STRUCTURAL
    for V in (ReferenceView, TemporalView, OpsView):
        assert V.SCOPE.tier is Tier.STATIC_GUARD


def test_read_only_views_have_no_world_reach():
    """The four non-effector Views hold W_world = NONE (no EffectView → no world reach)."""
    for V in (MirrorView, ReferenceView, TemporalView, OpsView):
        assert V.SCOPE.authority.world is WorldReach.NONE


def test_deployed_world_ceiling_is_none():
    """Track G's standing fact (finding-0011): no EffectView is wired at any tier, so the deployed
    lattice top's world reach is NONE — not SENSING."""
    assert DEPLOYED_WORLD_CEILING is WorldReach.NONE


# ── SCOPE is a DECLARATION: a ClassVar, not a dataclass field (no behavior change) ────────────
def test_scope_is_a_classvar_not_a_dataclass_field():
    """`SCOPE` must not have become a construction field — that would change every View's signature.
    It is absent from `dataclasses.fields`, and construction is unchanged (MirrorView() still works
    with its `_rows` default)."""
    for V in (MirrorView, ReferenceView, TemporalView, OpsView, EffectView):
        field_names = {f.name for f in dataclasses.fields(V)}
        assert "SCOPE" not in field_names
    # the additive retrofit did not perturb the empty-construction defaults
    assert len(MirrorView()) == 0
    assert len(EffectView.admit([])) == 0
