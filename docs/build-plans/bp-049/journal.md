# Journal — bp-049 `sweep-engine` (E3a-1b: the grid optimizer)

Alive at graduation (2026-07-16). Status `proposed` — awaits owner `proposed → ready` blessing.
**Depends on bp-046** (the registered `dream_rnd_sigma` lever + the widened `_config_fingerprint`);
**supersedes bp-040** (re-derives its σ sweep as `config/sweeps/dreamer-sigma-ab.toml`, §2.9).

## Fresh-agent orientation
Read `plan.md` in full, then the §2 context manifest IN ORDER. This is the deterministic, model-free
optimizer: sweep a registered lever's grid → drive the BUILT `ShadowRunner` per cell (resumable by the
eval store's keying — free, don't reimplement it) → build the curve from `EvalResultsStore.query` →
admissibility filter (guardrails lexicographically prior) → selection (§8: plateau center, least-motion
tie-break) → emit `ProposedChange` into the §14 ledger via `SelfModLoop.propose` (PROPOSED only; the owner
blesses the apply). Two items: 13 (spec + grid driver, writes cells) → 14 (optimizer + emit, the effect).

## The three grounding nuances the plan bakes in (read §3)
1. **Objective must be a metric the runner WRITES per cell** — `golden_recall` / `drift_D` /
   `structural_axes.*`. `f9_composite` is registered but NOT written per-cell (§3 Q3) → first instance
   can't use it; wiring F9 per-cell is a separate concern (§11 parked, §10 stop-and-raise if empty).
2. **Resumability is the store's guarantee, not the engine's** — bp-046 makes `config_fingerprint` move
   with σ; `put` returns False on a present cell. Reuse ONE eval store + ONE run ledger across cells.
3. **The proposal is a `ProposedChange`, not a new `TuningProposal` type** — no ledger schema change;
   `rationale` carries the curve summary + evidence `EvalKey`s; honors `[selfmod] enabled` (emit only when
   on; else record + log).

## §8 math — the selection instrument
A pure function `select(admissible_curve, current) -> value | None`. Falsifier: it must NOT return a
knife-edge max when a wider near-optimal plateau exists (peak-chasing — the exact failure §2.6 forbids).
Unit-tested as a pure function on synthetic curves before the integration test.

## Supersession
bp-040 flipped `proposed → superseded` (`superseded_by: bp-049`) at this graduation — an orchestrator act
(not a blessing). bp-040 stays inspectable; this plan re-derives its intent.

## Checkpoints
_(none yet — build has not started)_
