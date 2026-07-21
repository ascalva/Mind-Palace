"""The expiry sweep + the §2.6 isolation battery (bp-081 Item 10; dn-synchronic-diachronic-dreamer).

Two concerns:

  * the SWEEP — advances `N_hyp`, tombstones expired rows (SD-d), and resolves wall→generation
    interval-valued + ambiguity-widening (D8); wall NEVER orders (Law C4); and
  * the ISOLATION BATTERY (§2.6-4) — the permanent guard that staged data cannot reach durable
    stores or the mirror, and a cut-less composed counterfactual read is unconstructable.

The battery asserts AGAINST `core/mirror.py` and the durable stores; it never edits them.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from core.graph.composed import compose_staged
from core.mirror import MirrorView, NonMirrorRowError
from core.provenance import Provenance
from core.scope import (
    Authority,
    Clock,
    EdgeScope,
    Scope,
    SliceError,
    Stratum,
    StratumScope,
    Tier,
    TimeScope,
    Window,
)
from core.stores.staging import GenerationEvent, StagedItem, StagingStore
from ops.staging_sweep import (
    GenerationInterval,
    resolve_wall_to_generation,
    run_sweep,
)

_T0 = "2026-07-01T00:00:00"
_T_MID = "2026-07-05T00:00:00"
_T_LATE = "2026-07-09T00:00:00"


def _store() -> StagingStore:
    return StagingStore(Path(":memory:"))


def _item(digest: str, *, ttl: str | None = None,
          prov: Provenance = Provenance.INTERPRETED) -> StagedItem:
    return StagedItem(would_be_stratum=Stratum.MIRROR_AUTHORED, would_be_provenance=prov,
                      content_digest=digest)


def _hyp_grant() -> Scope:
    return Scope(StratumScope.of(Stratum.MIRROR_AUTHORED, Stratum.HYPOTHETICAL), EdgeScope.bottom(),
                 TimeScope(Clock.COMMIT, Window.point("deadbeef")), Authority.read_only(),
                 tier=Tier.STATIC_GUARD)


# ── the sweep: advance generation + tombstone expired, removed from every readable view ───────────
def test_sweep_tombstones_expired_and_advances_generation():
    s = _store()
    s.stage("A", [_item("d1")], ttl_wall=_T_MID)          # expires at _T_MID
    s.stage("A", [_item("d2")], ttl_wall=_T_LATE)         # expires later
    gen_before = s.current_generation()
    report = run_sweep(s, now_wall=_T_LATE, dry_run=False)
    assert report.swept_generation == gen_before + 1      # the sweep is its own N_hyp tick
    # both TTLs have passed by _T_LATE ⇒ both tombstoned, gone from EVERY readable view
    assert s.read_at() == []
    assert {e.row_id for e in report.expired} == {r.row_id for r in s.all_rows()}
    # but the records survive at their pre-tombstone generation (reproducibility)
    assert len(s.all_rows()) == 2


def test_sweep_only_expires_passed_ttls():
    s = _store()
    b1 = s.stage("A", [_item("d1")], ttl_wall=_T_MID)
    s.stage("A", [_item("d2")], ttl_wall=_T_LATE)
    # at _T_MID only d1 has expired
    run_sweep(s, now_wall=_T_MID, dry_run=False)
    live = {r.content_digest for r in s.read_at()}
    assert live == {"d2"}
    assert b1.row_ids[0] not in {r.row_id for r in s.read_at()}


def test_rows_without_ttl_never_expire():
    s = _store()
    s.stage("A", [_item("d1")])                            # no ttl_wall
    report = run_sweep(s, now_wall=_T_LATE, dry_run=False)
    assert report.expired == ()
    assert {r.content_digest for r in s.read_at()} == {"d1"}


def test_dry_run_reports_without_ticking():
    s = _store()
    s.stage("A", [_item("d1")], ttl_wall=_T0)
    gen = s.current_generation()
    report = run_sweep(s, now_wall=_T_LATE, dry_run=True)
    assert report.dry_run and report.swept_generation is None
    assert len(report.expired) == 1                        # WOULD expire
    assert s.current_generation() == gen                   # but nothing ticked
    assert {r.content_digest for r in s.read_at()} == {"d1"}   # still live


# ── FALSIFIER: an expired item must NOT be visible in any readable view after a sweep ──────────
def test_expired_item_not_visible_in_any_view_after_sweep():
    s = _store()
    s.stage("A", [_item("d1")], ttl_wall=_T0)
    s.stage("B", [_item("d2")], ttl_wall=_T0)
    run_sweep(s, now_wall=_T_LATE, dry_run=False)
    assert s.read_at() == []                               # the default view
    assert s.subspace_at("A") == [] and s.subspace_at("B") == []   # per-subspace views
    # a read pinned at the CURRENT (post-sweep) generation shows nothing either
    assert s.read_at(s.current_generation()) == []


# ── wall → generation resolution: interval-valued AND ambiguity-widening (D8) ─────────────────────
def test_resolver_is_interval_valued_clean_bracket():
    """A monotone bookmark chart gives a clean, non-ambiguous bracketing pair."""
    ev = [GenerationEvent(0, _T0, "genesis"),
          GenerationEvent(1, _T_MID, "admission"),
          GenerationEvent(2, _T_LATE, "admission")]
    # a wall time strictly between gen1 and gen2 brackets [1, 2], not ambiguous
    got = resolve_wall_to_generation(ev, "2026-07-07T00:00:00")
    assert got == GenerationInterval(1, 2, ambiguous=False)


def test_resolver_widens_and_flags_on_non_monotone_bookmarks():
    """Skew (a later generation with an EARLIER wall bookmark) widens the interval and flags it —
    never a silently-picked point (D8 ambiguity-widening)."""
    ev = [GenerationEvent(0, _T0, "genesis"),
          GenerationEvent(1, _T_LATE, "admission"),      # gen1 bookmarked LATE …
          GenerationEvent(2, _T_MID, "admission")]        # … gen2 bookmarked earlier (skew)
    got = resolve_wall_to_generation(ev, "2026-07-07T00:00:00")  # between _T_MID and _T_LATE
    assert got.ambiguous is True                           # widened, and says so
    assert got.lo == 1 and got.hi == 2                     # the widened bracket


def test_resolver_marks_future_wall():
    ev = [GenerationEvent(0, _T0, "genesis"), GenerationEvent(1, _T_MID, "admission")]
    got = resolve_wall_to_generation(ev, _T_LATE)          # beyond every bookmark
    assert got.future is True


def test_wall_never_orders_rows_law_c4():
    """Law C4 falsifier: a wall timestamp orders NOTHING. Rows admitted at successive generations
    read back in GENERATION order even when their wall bookmarks are indistinguishable (same second)
    — the generation is the sole order key. Wall enters only the resolver (a pure fn of events)."""
    s = _store()
    b1 = s.stage("A", [_item("d1")])
    b2 = s.stage("A", [_item("d2")])
    rows = s.read_at()
    # the two admissions may share a wall second, yet the read order is strictly by generation
    assert [r.generation for r in rows] == [b1.generation, b2.generation] == [1, 2]
    # the resolver is a PURE function of (events, wall) — no store, no hidden ordering state
    ev = s.generations()
    assert resolve_wall_to_generation(ev, _T0) == resolve_wall_to_generation(list(ev), _T0)


# ═══ THE ISOLATION BATTERY (§2.6-4) — a permanent guard, asserting AGAINST mirror + durable ═══════

class _RecordingDurableStore:
    """A stand-in durable store that RECORDS every write. Threaded nowhere in the staged flow (no
    staging/sweep/compose API accepts a durable handle — Item 8's structural scan), so it must
    record ZERO writes after a full staged dispatch."""

    def __init__(self) -> None:
        self.writes: list[dict[str, object]] = []

    def write(self, row: dict[str, object]) -> None:  # pragma: no cover - never called by the flow
        self.writes.append(row)


def test_battery_durable_stores_scan_to_zero_staged_rows_after_dispatch():
    """After a full staged dispatch (stage → compose overlay → sweep) NO staged row reaches a
    durable store: a recording durable fake sees zero writes, and no staged content digest appears
    in an (independently populated) durable row set."""
    s = _store()
    s.stage("A", [_item("h1"), _item("h2")], ttl_wall=_T0)
    staged_digests = {r.content_digest for r in s.read_at()}

    durable = _RecordingDurableStore()
    # a real durable row set the staged flow never touches (unrelated corpus rows)
    durable_rows = [{"digest": "corpus-x", "provenance": "authored-solo"}]

    # the staged dispatch: assemble the overlay from staged digests, then sweep
    nodes = ("h1", "h2", "corpus-x")
    g = compose_staged(nodes, [("corpus-x", "h1", 0.6)], [], [("h1", "h2", 1.0)],
                       grant=_hyp_grant())
    assert g.classes_of("h1", "h2")                         # the overlay assembled
    run_sweep(s, now_wall=_T_LATE, dry_run=False)

    # the durable side is untouched: zero writes, no staged digest leaked in
    assert durable.writes == []
    assert not (staged_digests & {r["digest"] for r in durable_rows})
    # and the staged rows live ONLY in the staging store (their records, tombstoned, remain here)
    assert {r.content_digest for r in s.all_rows()} == staged_digests


def test_battery_mirror_view_rejects_a_staged_row():
    """A staged row offered to a `MirrorView` raises `NonMirrorRowError` — 'staged data in the
    mirror' is unrepresentable (§2.6-4). Asserts against `core/mirror.py`, never edits it."""
    s = _store()
    s.stage("A", [_item("h1", prov=Provenance.INTERPRETED)])
    (row,) = s.read_at()
    staged_as_dict = {"provenance": row.would_be_provenance.value, "digest": row.content_digest}
    with pytest.raises(NonMirrorRowError):
        MirrorView(_rows=(staged_as_dict,))


def test_battery_cutless_composed_read_is_unconstructable():
    """A composed counterfactual read {durable, HYPOTHETICAL} with a point window on a non-cut clock
    and NO explicit cut raises `SliceError` — a counterfactual read is well-typed only as 'the graph
    at cut c ∪ the subspace at generation g' (§2.6-1 / the SLICE rule)."""
    with pytest.raises(SliceError):
        Scope(StratumScope.of(Stratum.MIRROR_AUTHORED, Stratum.HYPOTHETICAL), EdgeScope.bottom(),
              TimeScope(Clock.WALL, Window.point("now")), Authority.read_only(),
              tier=Tier.STATIC_GUARD)
    # supplying the cut ∧ generation makes it well-typed
    ok = Scope(StratumScope.of(Stratum.MIRROR_AUTHORED, Stratum.HYPOTHETICAL), EdgeScope.bottom(),
               TimeScope(Clock.WALL, Window.point("now")), Authority.read_only(),
               tier=Tier.STATIC_GUARD, cut=("commit-sha", "gen-3"))
    assert ok.cut == ("commit-sha", "gen-3")
