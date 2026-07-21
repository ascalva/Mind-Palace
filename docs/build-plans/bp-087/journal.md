# Journal — bp-087 (AL-2)

**Status:** in-progress → item 15 done, session complete (builder, worktree `agent-ada43367f46e83c01`).
**Design ref:** `docs/design-notes/agentic-loop.md`.

## Graduation — 2026-07-21 (session-40)

Minted `proposed` by `/graduate` over the three ratified notes (`fbea48d`). Decomposition and
grounding done in a single orchestrator context (subagent-assisted decomposition parked, §14);
seams/instruments re-verified on disk at HEAD `d08da37`. No implementation performed —
graduation implements nothing (A4). The plan's §3 carries the grounding citations; §6 pins the
interfaces verbatim so a fresh builder infers no design.

Next: owner blesses `proposed → ready` by hand, then `/build bp-087` in a fresh (delegated)
session.

## Build — 2026-07-21 (session builder, worktree behind main at start)

Worktree was pinned at `d08da37` (pre-graduation) — `bp-087/plan.md` did not exist on disk yet.
Confirmed working tree clean, then fast-forwarded the worktree branch onto main's `82a76d5`
(`bless: bp-083..088 proposed→ready`), which is exactly the graduate+bless pair this plan depends
on. No other divergence; ff-only, no conflicts.

Set `.claude/state/active-plan` → `docs/build-plans/bp-087/plan.md`.

**Item 15 (only item) — done.** Traced the §6-pinned interfaces plus their real upstream callers
(not assumed): `coverage_gauge` needs `ChatEventStore`/`CausalEdgeStore` opened directly on the
live `data/*.sqlite` paths (no `Config`/`get_config` needed — constructed the stores by absolute
path); `long_lived_holes` is not standalone-runnable on raw data — traced its actual caller
(`core/dreaming/interpreters.py: build_structural_context`) to find the real input pipeline:
`VectorStore` → `MirrorView.project` (π_MR, authored-only) → `note_centroids` → `cosine_distance_matrix`.
`doc_coverage` is a query embedded in `CodeSensor.sync` (`ops/code_sensor.py:329-332`) — replicated
the SELECT directly against `data/code_snapshots.sqlite` via a `mode=ro` connection URI rather than
running the full (ingesting) sync. `eval.drift.measure_drift` needs a live `Retriever` — i.e. an
active embedding pass through Ollama — which is daemon-adjacent infra I judged out of scope for an
ambient read-only builder session (memory-ceiling non-negotiable #8); recorded as
"deferred: needs live daemon" per plan §10's second stop condition, verbatim match.

Readings (full detail + populations in `docs/findings/finding-0143.md`):
- M-3 C-coverage = 0.8996 (4,084 witnessed / 4,540 integrable, 456 unwitnessed) — matches M-2's
  4,084 C-edges exactly (cross-check).
- M-6a holes: 19 note centroids (28 mirror-readable chunk rows; 19 matches the vault's actual file
  count — a full read, not truncated), 0 long-lived holes at `hole_min_persistence=0.15`.
- M-6b doc_coverage: 0.3391 (1,008,484 / 2,973,708 symbols documented), 883 commits in the ledger.
- M-6c drift-vs-anchor: deferred (needs live daemon/retriever).

Filed `docs/findings/finding-0143.md` (id pinned by the plan; not auto-picked), `ftype: discovery`,
`route: orchestrator` (direction). Notes PD-3's precondition as satisfied for M-6a/b, still pending
M-6c, and asks the orchestrator to checkpoint the readings into `dn-agentic-loop` §2.8's table
(design-note edit, out of this builder's write_scope) and update the plan's §11 parked-decision row.

No `core/**`/`eval/**` edit; no store write beyond the stores' own idempotent `CREATE TABLE IF NOT
EXISTS` DDL on open (the pinned `ChatEventStore`/`CausalEdgeStore`/`VectorStore` constructors run
this on every open, existing schema unaffected — not a data mutation). `docs/PROGRESS.md` untouched.

Ran the acceptance gate (see report) — no new reds vs the plan's stated baseline.

**Session complete.** Not merged to main, plan status left `in-progress` (orchestrator flips on
completion per CLAUDE.md roles) — the only follow-on step is the orchestrator's checkpoint into
§2.8 + PROGRESS, and eventually a daemon-attached session for M-6c.
