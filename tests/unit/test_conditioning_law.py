"""The conditioning law (bp-082 Item 13; dn-synchronic-diachronic-dreamer §2.7 SD-7).

The anti-laundering tooth: a dream synthesized over `graph ∪ subspace` is hypothesis-conditioned,
and the four clauses fail CLOSED. Exercised over in-memory DerivedStore / StagingStore fixtures
(dry-run; NO durable-store schema change — the mark rides the existing derives/data shape, Q3):

  * clause 1 — the artifact carries (subspace_id, generation, staged digests) and its derives tails
    include the staged content addresses;
  * clause 2 — TTL inheritance: after the subspace expires the artifact leaves the surfacing set but
    stays readable as a record, and the pinned generation stays reproducible;
  * clause 3 — the per-claim taint split IS the same with/without diff as `core.graph.influence`;
  * clause 4 — grounding terminates in authored evidence or declared (marked) hypothesis, never a
    dream (the recursion bound is untouched);
  * F-SD7b — each of the three teeth blocks surfacing (fail closed): the taint test and the lineage
    audit RAISE, the sweep test blocks quietly.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from core.dreaming.conditioning import (
    Condition,
    ConditioningViolation,
    TaintSplit,
    assert_grounding_terminates,
    condition_data,
    conditioned_derives,
    is_surfaceable,
    read_condition,
    taint_split,
    verify_surfacing,
)
from core.graph.influence import sigma_star_influence
from core.kernel.provenance import Provenance
from core.kernel.scope import (
    Authority,
    Clock,
    EdgeScope,
    Scope,
    Stratum,
    StratumScope,
    Tier,
    TimeScope,
    Window,
)
from core.stores.derived import DREAM, Artifact, DerivedStore
from core.stores.staging import StagedItem, StagingStore

_AUTHORED_LEAVES = ("leafA", "leafB")
_STAGED = ("s1", "s2")


def _staging() -> tuple[StagingStore, int]:
    """An in-memory staging store with subspace-A holding two staged items (digests s1, s2).
    Returns the store and the generation the batch was admitted at."""
    store = StagingStore(Path(":memory:"))
    items = [
        StagedItem(Stratum.MIRROR_AUTHORED, Provenance.AUTHORED_SOLO, d) for d in _STAGED
    ]
    batch = store.stage("subspace-A", items)
    return store, batch.generation


def _conditioned_artifact(store_gen: int, *, tails: tuple[str, ...] | None = None) -> Artifact:
    """A conditioned DREAM artifact in an in-memory derived store — the mark in `data`, the staged
    digests in the derives tails (clause 1). `tails` overrides the derives set for the lineage-audit
    falsifier."""
    derived = DerivedStore(Path(":memory:"))
    cond = Condition("subspace-A", store_gen, _STAGED)
    derives = tails if tails is not None else conditioned_derives(_AUTHORED_LEAVES, cond)
    return derived.add(
        kind=DREAM,
        summary="a reflection conditioned on a staged hypothesis",
        subjects=("theme-1",),
        data=condition_data(cond),
        derived_from=derives,
    )


def _hyp_grant() -> Scope:
    return Scope(
        StratumScope.of(Stratum.MIRROR_AUTHORED, Stratum.HYPOTHETICAL),
        EdgeScope.bottom(),
        TimeScope(Clock.COMMIT, Window.point("deadbeef")),
        Authority.read_only(),
        tier=Tier.STATIC_GUARD,
    )


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Clause 1 — provenance carries the condition (the mark rides the existing shape)
# ═══════════════════════════════════════════════════════════════════════════════════════════════


def test_conditioned_artifact_carries_mark_and_staged_tails():
    """A conditioned artifact records (subspace_id, generation, staged digests) in its data AND its
    derives tails include the staged content addresses — no schema change, the mark rides the
    existing `data`/`derived_from` shape."""
    _, gen = _staging()
    art = _conditioned_artifact(gen)
    cond = read_condition(art)
    assert cond == Condition("subspace-A", gen, _STAGED)              # the mark round-trips
    assert set(_STAGED) <= set(art.derived_from)                     # staged digests are tails
    assert set(_AUTHORED_LEAVES) <= set(art.derived_from)            # authored leaves too
    assert read_condition(_unconditioned()) is None                 # an ordinary dream has no mark


def _unconditioned() -> Artifact:
    derived = DerivedStore(Path(":memory:"))
    return derived.add(kind=DREAM, summary="ordinary", subjects=("t",), derived_from=("leafA",))


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Clause 2 — TTL inheritance: expiry leaves the surfacing set, the record survives
# ═══════════════════════════════════════════════════════════════════════════════════════════════


def test_expired_subspace_leaves_surfacing_set_but_stays_readable():
    """While the subspace is live the artifact surfaces; after the sweep tombstones it, the artifact
    leaves the LIVE surfacing set — yet stays a readable record, and its PINNED generation is still
    reproducible (§2.6-2)."""
    store, gen = _staging()
    cond = Condition("subspace-A", gen, _STAGED)
    assert is_surfaceable(cond, store)                               # live now

    row_ids = [r.row_id for r in store.subspace_at("subspace-A", gen)]
    store.tombstone(row_ids)                                        # the expiry sweep

    assert not is_surfaceable(cond, store)  # gone from the live surfacing set
    assert is_surfaceable(cond, store, at=gen)                      # still reproducible at the pin
    assert len(store.all_rows()) == 2  # the records survive (append-only)


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Clause 3 — the taint split IS the influence diff
# ═══════════════════════════════════════════════════════════════════════════════════════════════


def test_taint_split_is_the_same_diff_as_influence():
    """The per-claim taint split consumes the SAME `core.graph.influence` output: pairs the staged
    overlay MOVED are conditioned (keep the mark); pairs it left bit-identical are corpus-grounded
    (may shed it). One diff, double duty."""
    nodes = ("a", "b", "c", "d")
    sim = [("a", "b", 0.9), ("c", "d", 0.9)]
    staged = [("b", "c", 1.0)]                                      # the staged bridge
    infl = sigma_star_influence(nodes, sim, [], staged, grant=_hyp_grant(), grid=(0.5, 0.7, 0.9))
    split = taint_split(infl)

    assert all(i.changed for i in split.conditioned)
    assert all(not i.changed for i in split.corpus_grounded)
    assert len(split.conditioned) + len(split.corpus_grounded) == len(infl)   # a partition
    # The conditioned set IS the changed set of the same influence diff (read off the typed list).
    conditioned_pairs = {(i.a, i.b) for i in infl if i.changed}
    assert ("a", "d") in conditioned_pairs                          # bridged ⇒ conditioned
    assert ("a", "b") not in conditioned_pairs                      # intra-component ⇒ grounded


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Clause 4 + F-SD7b — the three teeth, fail closed
# ═══════════════════════════════════════════════════════════════════════════════════════════════


def test_tooth3_lineage_audit_missing_staged_digest_raises():
    """F-SD7b tooth 3: a conditioned artifact whose derives tails OMIT a staged digest fails the
    lineage audit — the grounding chain must visibly bottom out on the declared hypothesis. Fail
    closed (raises)."""
    _, gen = _staging()
    art = _conditioned_artifact(gen, tails=(*_AUTHORED_LEAVES, "s1"))   # s2 dropped from the tails
    cond = Condition("subspace-A", gen, _STAGED)
    with pytest.raises(ConditioningViolation):
        assert_grounding_terminates(art, cond, dream_ids=())


def test_tooth4_recursion_bound_a_dream_tail_raises():
    """Clause 4: a dream's derives tails may never include another dream (dreams never cite dreams
    as
    evidence). A tail that is a dream id fails closed (raises)."""
    _, gen = _staging()
    art = _conditioned_artifact(gen)
    cond = Condition("subspace-A", gen, _STAGED)
    with pytest.raises(ConditioningViolation):
        assert_grounding_terminates(art, cond, dream_ids={"leafA"})    # a tail flagged as a dream


def test_tooth1_taint_test_corpus_grounded_claim_that_changes_raises():
    """F-SD7b tooth 1: a claim marked corpus-grounded whose reading actually CHANGES under the
    overlay is an inconsistent taint mark — a laundering bug. `verify_surfacing` fails closed
    (raises)."""
    store, gen = _staging()
    art = _conditioned_artifact(gen)
    cond = Condition("subspace-A", gen, _STAGED)
    bad_split = TaintSplit(conditioned=(), corpus_grounded=(SimpleNamespace(changed=True),))
    with pytest.raises(ConditioningViolation):
        verify_surfacing(art, cond, bad_split, store)


def test_tooth2_sweep_test_expired_artifact_does_not_surface():
    """F-SD7b tooth 2: a conditioned artifact does NOT surface past its subspace's expiry.
    `verify_surfacing` blocks it (returns False) once the sweep tombstones the rows — quietly, since
    expiry is the normal lifecycle, not a bug."""
    store, gen = _staging()
    art = _conditioned_artifact(gen)
    cond = Condition("subspace-A", gen, _STAGED)
    clean = TaintSplit(conditioned=(), corpus_grounded=())

    assert verify_surfacing(art, cond, clean, store) is True        # live ⇒ surfaces
    store.tombstone([r.row_id for r in store.subspace_at("subspace-A", gen)])
    assert verify_surfacing(art, cond, clean, store) is False       # expired ⇒ blocked (no raise)


def test_happy_path_surfaces_when_live_consistent_and_complete():
    """All teeth pass and the subspace is live ⇒ the conditioned dream may surface. The single
    sanctioned True."""
    store, gen = _staging()
    art = _conditioned_artifact(gen)
    cond = Condition("subspace-A", gen, _STAGED)
    clean = TaintSplit(conditioned=(SimpleNamespace(changed=True),), corpus_grounded=())
    assert verify_surfacing(art, cond, clean, store, dream_ids=()) is True
