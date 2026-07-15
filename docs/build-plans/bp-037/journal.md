# Journal — bp-037 `CQ-wire`: `TemporalView` (β₁ citation threads)

> The fresh-agent contract: a new session with only `plan.md` + this journal + the write-scope files
> must continue without re-asking. Checkpoint at every semantic boundary (criterion closed, commit,
> finding filed). Status flips are the orchestrator's, by hand.

## 2026-07-15 — GRADUATED (proposed), awaiting owner `proposed→ready` blessing

- Graduated by the orchestrator (opus) from ratified `dn-core-query-protocol` §3 C5 + bp-035 §12 item 3.
  Grounded pass done in-session: read the built `core/temporal/{complex,operators,superconnection,
  boundary}.py`, the sibling `core/reference_view.py`, the store API, and `test_temporal_complex.py`.
- **Key grounding finding (§3 Q2):** `build_citation_complex` is NOT commit-anchored (`complex.py:66`
  calls `all(direction="corpus_to_corpus")` with no commit filter) → today's `X_cite` is the all-history
  union. Item 1 fixes this additively (`commit` kwarg, default None = unchanged).
- **Scope decision (§0/§12):** the built surface bifurcates single-snapshot (`complex.py`, β₁ — THIS
  plan) vs two-snapshot (`operators`/`superconnection`/`boundary`, `‖[d,τ]‖` — `CQ-wire-2`, a follow-on
  gated on this so its upstream `TemporalView` interface is built, not inferred). The note's open "what
  answer, to whom?" → **a `TemporalView`** (read-surface sibling to `ReferenceView`; NOT a dreamer lens —
  that's the gated `DD-1`).
- **Not started** — no code written; this is a `proposed` plan. Owner blesses `proposed→ready` by hand,
  then `/build bp-037` (opus, self-driven; no fable, no delegation — week at 89%, budget-tight).

### Re-entry (for the builder, once blessed)
- Start at **Item 1** (`core/temporal/complex.py` commit kwarg) — lowest blast radius, unblocks Items 2/3.
- Mirror `ReferenceView` EXACTLY for the View shape + anchor resolution (`reference_view.py:47,60,111,129`).
- The green gate: ruff; `mypy core agents eval ops scheduler scripts`==0; argless `mypy`==69 (the
  new-tests tooth — assert it, will rise with the two new test files); `ops.type_gate`; `pytest -q`
  (baseline 1123 passed / 9 skipped — the 2 live e2e may flake on a loaded box; tolerate only those).
