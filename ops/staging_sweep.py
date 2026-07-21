"""The HYPOTHETICAL staging expiry sweep (bp-081 Item 10; dn-synchronic-diachronic-dreamer §2.6).

The sweep is machinery-side (ops): housekeeping that advances the staging store's `N_hyp` clock and
TOMBSTONES expired rows, so an expired hypothesis leaves every readable view (SD-d default —
tombstone, not hard delete). It is READ/TOMBSTONE-ONLY on the staging store: it moves NO row
anywhere, least of all durable-ward (the no-promotion spine invariant is the store's, and this sweep
holds no durable handle either).

**Wall → generation resolution (D8, note §2.6-2).** A staged row may carry a wall-denominated TTL
(`ttl_wall` — owner convenience, "expire after this instant"). Wall NEVER orders anything (Law C4):
`resolve_wall_to_generation` maps a wall time to a GENERATION INTERVAL over the store's own bookmark
chart, and is AMBIGUITY-WIDENING — clock skew / non-monotone bookmarks widen the interval and the
report SAYS SO, never silently picking a generation. Wall enters ONLY this resolver; the sweep's
expiry decision and every read are generation-ordered.

**Q3 — scheduling (STOP-AND-RAISE, plan §10).** Registering this as a trough-tier job requires
editing `scheduler/cron.py` internals (a `SWEEP_KIND`, a handler, an enqueue helper,
`cron_handlers`, and `router._PINNED_KINDS`) — all OUTSIDE this plan's write_scope. Per the plan's
stop-and-raise, this module lands as a CALLABLE (`run_sweep`) and the trough wiring is PARKED with a
finding (finding-0130). A future plan owning the scheduler surface wires `run_sweep` as a pinned
trough job exactly like `chat_events`/`integrate` (model-free housekeeping, background priority).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.stores.staging import GenerationEvent, StagedRow, StagingStore


@dataclass(frozen=True)
class GenerationInterval:
    """A wall time resolved onto the `N_hyp` bookmark chart (D8). `lo`/`hi` bracket the generation
    the wall time falls between; `ambiguous` is True when the bookmarks are non-monotone across the
    bracket (skew) or the bracket spans more than one generation gap — the interval was WIDENED and
    the caller must not treat it as a point. `future` is True when the wall time is beyond every
    recorded bookmark (a deadline not yet reached by the clock)."""

    lo: int
    hi: int
    ambiguous: bool
    future: bool = False


def resolve_wall_to_generation(events: list[GenerationEvent], wall: str) -> GenerationInterval:
    """Map a wall time to a generation INTERVAL over the bookmark chart (D8). INTERVAL-VALUED and
    AMBIGUITY-WIDENING: the tightest bracketing pair of generations, widened across any bookmark
    inversion (skew), with `ambiguous` set when it is not a clean point/adjacent bracket. Wall
    appears ONLY here — never as an ordering key on rows (Law C4).

    Bookmarks are fixed-width ISO strings, so `<=`/`>` on the string is the wall order. Pure over
    `events`, so it is testable with hand-built (skewed) chains."""
    ev = sorted(events, key=lambda e: e.generation)
    if not ev:
        return GenerationInterval(0, 0, ambiguous=False)
    before = [e.generation for e in ev if e.at <= wall]   # bookmarks at/behind the wall time
    after = [e.generation for e in ev if e.at > wall]      # bookmarks ahead of it
    if not before:                                         # wall precedes even genesis
        return GenerationInterval(ev[0].generation, ev[0].generation, ambiguous=False)
    if not after:                                          # wall is beyond every bookmark — future
        last = ev[-1].generation
        return GenerationInterval(last, last, ambiguous=False, future=True)
    b, a = max(before), min(after)
    lo, hi = min(b, a), max(b, a)
    inverted = b > a                    # a "before" bookmark sits at a HIGHER generation than an
    #                                     "after" one — non-monotone bookmarks ⇒ widen + flag
    ambiguous = inverted or (hi - lo) > 1
    return GenerationInterval(lo, hi, ambiguous=ambiguous)


@dataclass(frozen=True)
class ExpiredRow:
    """One expired staged row and the generation interval its wall TTL resolved to (the honest,
    possibly-widened report — never a silently-picked point)."""

    row_id: int
    subspace_id: str
    ttl_wall: str
    resolved: GenerationInterval


@dataclass(frozen=True)
class SweepReport:
    """The outcome of one sweep pass. `dry_run` reports what WOULD expire without ticking; a live
    pass carries `swept_generation` (the sweep tick) and the tombstoned row ids. `expired` is the
    per-row resolution detail (interval-valued, ambiguity-flagged)."""

    dry_run: bool
    current_generation: int
    expired: tuple[ExpiredRow, ...]
    swept_generation: int | None = None
    tombstoned_row_ids: tuple[int, ...] = field(default_factory=tuple)


def _expired_rows(store: StagingStore, now_wall: str) -> tuple[list[StagedRow], list[ExpiredRow]]:
    """The live rows whose wall TTL has passed `now_wall`. Expiry is a per-row THRESHOLD
    (`now_wall >= ttl_wall`) — a predicate on each row's OWN deadline, never a comparison that
    orders rows against each other (Law C4). Rows are iterated in the store's generation order."""
    events = store.generations()
    live = store.read_at()                                 # generation-ordered; no wall sort
    expiring: list[StagedRow] = []
    detail: list[ExpiredRow] = []
    for r in live:
        if r.ttl_wall is not None and now_wall >= r.ttl_wall:
            expiring.append(r)
            detail.append(ExpiredRow(row_id=r.row_id, subspace_id=r.subspace_id,
                                     ttl_wall=r.ttl_wall,
                                     resolved=resolve_wall_to_generation(events, r.ttl_wall)))
    return expiring, detail


def run_sweep(store: StagingStore, *, now_wall: str, dry_run: bool = True) -> SweepReport:
    """Sweep the staging store: find rows whose wall TTL has passed `now_wall`, and — unless
    `dry_run` — TOMBSTONE them at a fresh `N_hyp` tick (SD-d default), so they leave every
    `read_at(g')` for g' ≥ the tick while their records survive. Dry-run first is the template rule
    for a store-touching pass; a live pass is idempotent (already-tombstoned rows are not re-listed,
    since it reads only the LIVE view).

    Read/tombstone-only: the sweep never writes a durable store (it holds no durable handle) and
    never promotes — it only advances the generation and marks tombstones."""
    current = store.current_generation()
    expiring, detail = _expired_rows(store, now_wall)
    if dry_run:
        return SweepReport(dry_run=True, current_generation=current, expired=tuple(detail))
    row_ids = [r.row_id for r in expiring]
    swept_gen = store.tombstone(row_ids)                   # one sweep tick, even if row_ids empty
    return SweepReport(dry_run=False, current_generation=current, expired=tuple(detail),
                       swept_generation=swept_gen, tombstoned_row_ids=tuple(row_ids))
