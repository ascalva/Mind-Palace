# Journal — bp-039 `CQ-scope`: the capability-scope typing layer (`core/scope.py` + `req()` on the five Views)

> The fresh-agent contract: a new session with only `plan.md` + this journal + the write-scope files
> must continue without re-asking. Checkpoint at every semantic boundary (criterion closed, commit,
> finding filed). Status flips are the orchestrator's, by hand.

## 2026-07-15 — GRADUATED (proposed), awaiting owner `proposed→ready` blessing

- Graduated by the orchestrator (opus, self-driven) from **ratified** `dn-capability-scope` §3
  Consequence 1 (owner ratified all three fable notes by hand this session; blessing flip committed
  first at `3f5591d`). The note licenses exactly ONE plan — the scope typing layer — and this is it.
- **Grounding done in-session** (one Explore subagent, to keep main context small — the >150k-context
  cost driver). Confirmed with `path:line` citations:
  - **No existing `Scope`/read-scope type** (§3 Q1) — the note's "Views carry no explicit scope type"
    holds. Five factories: `MirrorView.project` (`core/mirror.py:72`), `ReferenceView.over`
    (`core/reference_view.py:60`), `TemporalView.over` (`core/temporal_view.py:109`), `OpsView.over`
    (`core/ops_view.py:77`), `EffectView.admit` (`ops/effects.py:194`) — all frozen dataclasses w/
    classmethod factories → `SCOPE` attaches as a class constant, no factory/read touch.
  - **`core/` is flat** → new file is `core/scope.py` (not `core/query/scope.py`).
  - **The `W_world` reconciliation (§3 Q3 / §4):** the note's `NONE < SENSING < …` is NOT
    `ReversibilityClass` (`ops/effects.py:47-56`, which is `SENSING(0) < REVERSIBLE < IRREVERSIBLE`,
    no NONE). `NONE` is `ApprovalStrength.NONE`, a different enum. **Decision:** `core/scope.py`
    defines a NEW pure `WorldReach: NONE<SENSING<REVERSIBLE<IRREVERSIBLE`; the `ReversibilityClass →
    WorldReach` bridge is authored **ops-side** (`world_reach()` in `ops/effects.py`), preserving
    ops→core so `core/scope.py` imports nothing from ops. `ReversibilityClass` stays unchanged.
  - **SLICE anchor shared** (§3 Q4): `_resolve_default_commit` (`core/reference_view.py:111`), both
    Views route through it — the commit SHA IS the consistent cut; the type states it, changes nothing.
  - **`CoherenceReport` is `Inv`** (§3 Q5): `core/temporal_view.py:56-70` — count + two anchors, no
    division. Item 4's audit target.
  - Flagged: two MORE View-shaped types NOT in the note's five — `ObservedView` (`core/sensing.py:190`)
    + `DreamsView` (`core/dreams_view.py:44`) — scoped OUT (§9, §11).
- **Key scoping decisions (the graduation judgment):**
  1. **`req()` is a DECLARATION, not enforcement wiring** — a `SCOPE` class constant per View from the
     §2.4 table, guarded by a declared-vs-actual test. No live caller passes a granted scope, so reads
     stay **bit-identical** (the whole-plan falsifier). Wiring `minted = meet(parent, template)` into
     `factory.grant` is behavior change → **parked** (§11).
  2. **ONE plan, four blast-radius-ordered items:** Item 1 new `core/scope.py` (lowest radius) → Item 2
     property/law tests → Item 3 the five View retrofits + ops bridge (touches existing code) → Item 4
     Inv/Rate markers (independently approvable — the deferrable one; owner may drop it to the R1
     velocity build at `proposed→ready`). Items are tightly coupled (all read the same-session
     `core/scope.py`) — splitting into separate PLANS would force interface-inference, so they are
     items, not plans. Confidence it fits one Opus session: high (bp-037 precedent, same character).
- **Cost estimate:** opus 240k (bigger than bp-037's 180k — more distinct pieces — but same
  deterministic pure-typing, test-pinned, no-live-model character; self-driven lands ~0.5–0.8×). No
  fable (design banked/ratified), no xhigh.
- **Not started** — no code written; `proposed`. Owner blesses `proposed→ready` by hand, then
  `/build bp-039`. Budget note: week at 92% (relayed this session) — the BUILD is a separate session;
  right-size at build time (self-driven if week still tight, else consider delegation w/ pre-flight
  budget gate).
