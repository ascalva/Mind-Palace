# bp-020 journal

## 2026-07-12 — minted at graduation (orchestrator, Fable/xhigh)

Plan created `proposed` by /graduate over the ratified `dn-self-sensing` (B-c:
backfill). Grounding verified in-session: bp-013's partially-recoverable seal usage
(`docs/build-plans/bp-013/journal.md:263-265` — opus, 54,048 tokens for the Item-8
session; Items 6-7 never captured, the recorded ledger gap), V3's expected inventory
(→ ≥5 pairs post-annotation), the dry-run-then-orchestrator-live split (finding-0031
class: builders never touch the main checkout's live stores). No code written; no data
touched. Awaiting the owner's `proposed → ready` hand edit; depends on bp-019.

## 2026-07-12 — /build enactment (builder session, worktree agent-acf8163bd0be42450)

Plan flipped `ready → in-progress`. Worktree pointer written to
`.claude/state/active-plan` (own worktree, `$PWD`-explicit per finding-0051).
Read the full §2 manifest: dn-self-sensing.md whole, bp-019/plan.md §6(d,e,f),
bp-013/journal.md:263-265, build-plan.md template §cost, `ops/self_sensor.py` +
`scripts/sense_self.py` as landed by bp-019.

**Reconciliation note (honest delta from plan §4's premise).** Plan §4 states
bp-013's `actual: null` → correction. At this builder's HEAD, `actual` was **NOT
null** — bp-013 was already seal-filled at commit `ef9319e` ("docs(triage): seal
bp-013") with `actual: { model: opus, tokens_item8: 54k, tool_calls_item8: 44,
note: "items 6-7 uncaptured" }`. That fill used non-conforming field names
(`tokens_item8`/`tool_calls_item8` instead of the schema's `tokens`/`tool_calls`,
and `54k` not the exact `54048`), so it silently under-parsed: running the current
`ops/self_sensor.py` `parse_plan_cost_block` against pre-edit HEAD yielded
`actual: {model: 'opus', raw: …}` — **no `tokens` key at all**, which would NOT
have joined as a complete pair the way Q1/V3 expects. So Item 9 is not "filling a
null" — it is **correcting a mis-shaped fill to match the parser's schema** so the
join is actually recoverable. The recorded facts (opus, 54048, items-6-7
uncaptured) are unchanged; only the encoding moves to match §6(a)'s pinned shape.
Not a stop-and-raise (no invented number; the correction is licensed by Item 9's
own §6(a) target-state spec, and Q3's "late ledger discipline, not history
rewriting" reasoning covers a field-name fix identically to a null fill).

**Item 9 — DONE.** Edited `docs/build-plans/bp-013/plan.md` cost block:
```
-  actual: { model: opus, tokens_item8: 54k, tool_calls_item8: 44, note: "items 6-7 uncaptured" }
+  actual: { model: opus, tokens: 54048, tool_calls: null, duration_min: null } # PARTIAL — Item 8 + finding-renumber session only; the Items 6-7 session was never captured (journal :263-265, the recorded ledger gap). Late seal-fill, 2026-07-12.
```
`git diff` confirms exactly one changed line (the honesty comment rides the same
line). `estimate:` line untouched (copied verbatim — never edited). Verified via
`uv run python3 -c "..."` calling `ops.self_sensor.parse_plan_cost_block` against
the edited file text: `actual == {model: 'opus', tokens: 54048, raw: '{ model:
opus, tokens: 54048, tool_calls: null, duration_min: null }'}` — acceptance test
PASSES. `tool_calls`/`duration_min` correctly absent from the payload (both
`null`, not digit strings) — no invented numbers, falsifier respected.

Committed locally (worktree branch only, `6d6bc24`, "docs(bp-013): late seal-fill
of cost.actual (bp-020 Item 9)") — no Co-Authored-By trailer (docs/frontmatter
change, per plan instruction). NOT pushed.

## 2026-07-12 — Item 10 (the dry-run inventory)

Ran §6(b)'s harness: `SelfSensor` with `store=AgentObservationStore(Path(":memory:"))`,
`handoff=AgentSensingHandoff(handoff=<tmp dir>)`, `attestor=None`, `history=None`,
`repo=<this worktree>`, `branch=<worktree branch, includes Item 9's commit>`. Two
independent runs (fresh tmp dirs + fresh `:memory:` stores each) for the determinism
check, per Item 10's acceptance test.

**First branch subtlety, resolved.** `branch="main"` (the plan's literal §6(b) pin)
resolves, inside this worktree, to the SHARED `main` ref (`36906fb`) — which does
NOT include Item 9's commit (that commit lives only on
`worktree-agent-acf8163bd0be42450`, not yet merged). Running against `main` verbatim
therefore shows bp-013's PRE-Item-9 `actual` shape — expected and correct given the
plan's own ordering (Item 9 → Item 10 → Item 11; Item 11 is the orchestrator's
post-merge live run, by which point Item 9 will be on `main` too). To demonstrate the
full post-Item-9 pipeline end-to-end THIS session, the dry-run was additionally run
against `branch="worktree-agent-acf8163bd0be42450"` (this worktree's own branch,
which does include `6d6bc24`) — both runs are reported below; neither touches
`data/`. Not a stop-and-raise: this is branch-resolution behaving exactly as `git`
and the plan's own text define it, not a sensor defect.

**Second subtlety, resolved (a test-harness bug, not a sensor bug).** An edited fact
(bp-013's `actual`, changed at `6d6bc24`) correctly lands as a SECOND, NEW row at the
new `commit_sha` (identity key includes `commit_sha` — the design's explicit "an
edited fact is a new observation at its landing commit" semantics, self-sensing.md
§2.3/bp-019 §3 risk note). `store.all_rows()` returns BOTH the old row (at seal
commit `ef9319e`) and the new row (at `6d6bc24`) — correctly. My first pass at
building a "latest fact per plan" table naively aggregated by iterating `all_rows()`
in its default order (`commit_sha` lexical ascending) and let whichever row's SHA
sorted last win — which is NOT commit recency. Fixed by aggregating in TOPOLOGICAL
commit order (`rev-list --first-parent --reverse`, the same order `sync()` itself
walks) before folding per-identity — the correct notion of "latest." Recording this
so a future consumer (the parked report generator) does not repeat the mistake: "latest
observation for an identity key" means latest by commit ancestry, never by `commit_sha`
string sort.

**Finding filed: finding-0059** (`spec-fidelity`, resolved by this builder). V3's
"11 pre-rule plans, zero cost block, zero rows" baseline (dn-self-sensing.md §3.2;
carried into both bp-019 §3 Q4 and bp-020 §3 Q1 / Item 10's acceptance-test wording)
is STALE at this HEAD: only 8 of bp-000..010 truly have no `cost:` block
(bp-000,001,002,003,004,005,008,010); bp-006/007/009 were retroactively backfilled
with `actual`-only cost blocks by `ea3d8e8` — the SAME commit that introduced the
`cost:` convention (commit message: "Backfilled: bp-007/009 actuals ..., bp-006
honestly unmeasured, bp-011..013 estimated"). The dry-run correctly projects these 3
as `actual`-only rows (no join, since `estimate: null`), zero warnings, deterministic
— the SENSOR is right; the plan's carried-forward COUNT is wrong. Re-verified Item
10's actual falsifier (a complete cost block yielding no join) against the TRUE
zero-block set of 8 — holds exactly (0 rows, 0 errors). See finding-0059 for full
detail and routing.

**Inventory table (topologically-latest fact per plan, this HEAD / worktree branch,
`6d6bc24`):**

| plan | estimate | actual | class |
| --- | --- | --- | --- |
| bp-006 | — | fable, tokens unmeasured | actual-only |
| bp-007 | — | sonnet, 657000 | actual-only |
| bp-009 | — | fable, 153000 | actual-only |
| bp-011 | sonnet, 350000 | sonnet, 163000 | **PAIR** |
| bp-012 | fable, 300000 | fable, 157000 | **PAIR** |
| bp-013 | fable, 250000 | opus, 54048 | **PAIR** (post-Item-9) |
| bp-014 | fable, 350000 | opus, 101000 | **PAIR** |
| bp-015 | opus, 250000 | opus (raw only, unparsed tokens field name) | **PAIR** |
| bp-016 | fable, 300000 | fable (tokens: "unknown" — unparseable, no tokens key) | **PAIR** |
| bp-017 | sonnet, 100000 | sonnet, 97449 | **PAIR** |
| bp-018 | fable, 250000 | fable, 194279 | **PAIR** |
| bp-019 | sonnet, 350000 | sonnet, 236576 | **PAIR** |
| bp-020 | sonnet, 100000 | — (this plan, in-progress) | estimate-only |
| bp-021 | sonnet, 300000 | sonnet, 173956 | **PAIR** |
| bp-022 | sonnet, 250000 | sonnet, 210223 | **PAIR** |
| bp-000..005,008,010 | — | — | zero rows (8 plans, true pre-rule) |

Total rows: 27. Complete pairs: 11 (bp-011,012,013,014,015,016,017,018,019,021,022).
Estimate-only: 1 (bp-020). Actual-only: 3 (bp-006,007,009). "Complete pair" here
means both `estimate` and `actual` KEYS present (a join exists) — bp-015/bp-016's
actual VALUES are themselves under-specified (`raw`-only / no numeric `tokens`),
which is a corpus fact about those plans' OWN seal fills, not a parser defect;
out of scope for this plan (Item 9 licenses ONLY the bp-013 fix).

**The four Item-10 assertions, measured:**

1. **≥5 complete estimate/actual pairs (post-Item-9, bp-013 included):** MEASURED
   **11** (bp-013 included). PASS.
2. **bp-000..010 contribute zero rows and zero errors:** measured against the TRUE
   zero-cost-block subset of bp-000..010 (8 plans: 000,001,002,003,004,005,008,010)
   — **0 rows, 0 errors**. PASS on the corrected baseline (finding-0059: 3 of the
   11 originally-claimed IDs — bp-006/007/009 — are NOT zero-block at this HEAD;
   they correctly yield 3 actual-only rows, still zero PAIRS/zero errors).
3. **Zero parse warnings:** MEASURED **0** (`report.warnings == []`) on both runs
   and both branch variants (`main` and the worktree branch). PASS.
4. **Determinism (re-run → identical counts):** MEASURED — two independent runs
   (fresh `:memory:` store + fresh tmp handoff dir each) against the same branch
   yielded IDENTICAL `projected` (60), `observation_rows` (27), row count (27), and
   zero warnings both times. PASS.

No write outside tmp paths (`:memory:` store, `tempfile.TemporaryDirectory()`
handoff); no attestor constructed (`attestor=None`); `data/agent_observations.sqlite`
never opened or touched by this item's runs — verified by construction (the store
object passed was never `open_agent_observation_store()`).

Item 10 — **DONE**. All four assertions measured and passing on the corrected
baseline; one finding filed (0059, resolved) documenting the stale-count discovery.

## 2026-07-12 — Item 11 prep (command + verification queries, NOT run)

Per plan §6(c)/§11 parked-decision table ("who runs the live write: orchestrator at
seal, main checkout") and the CRITICAL REALITY briefing (φ_self is already live on
main; the store already holds rows from the post-commit hook running on every main
commit since bp-019 merged) — this builder does NOT run the live write. Preparing
the exact command + read-only verification queries for the orchestrator to execute
from the MAIN checkout, post-merge of this plan's Item 9 commit.

**The exact command (§6(c), verbatim):**
```
uv run scripts/sense_self.py
```
Run from the main checkout's repo root, on `main`, after this plan's commit(s) are
merged (so bp-013's corrected `actual` block is part of `main`'s history and
projects at its own commit). Idempotent: safe to run even though the hook has
already been running incrementally — `sync()` reconciles the full
`rev-list --first-parent` history against `is_projected`, so this is "the first
FULL run" only in the sense that it is the first time it is invoked as a deliberate
backfill act; mechanically it is identical to every hook-triggered call.

**Verification queries (sqlite3 CLI, read-only, against
`data/agent_observations.sqlite` from the main checkout):**

```sql
-- Q_total: total row count
SELECT count(*) FROM agent_observations;

-- Q_per_key: rows per (stream, key)
SELECT stream, key, count(*) FROM agent_observations GROUP BY stream, key ORDER BY 1,2;

-- Q_join: estimate/actual join per subject_id — expected >=5 complete pairs incl. bp-013
-- (measured 11 in this session's dry-run at this HEAD; more may land as history moves,
-- per plan §3 Q1's own >=  not == framing)
SELECT
  e.subject_id,
  e.payload AS estimate_payload,
  a.payload AS actual_payload
FROM
  (SELECT subject_id, payload FROM agent_observations WHERE stream='cost' AND key='estimate') e
  JOIN
  (SELECT subject_id, payload FROM agent_observations WHERE stream='cost' AND key='actual') a
  ON e.subject_id = a.subject_id
ORDER BY e.subject_id;

-- Q_bp013: bp-013 specifically resolves to the Item-9-corrected shape (tokens=54048)
SELECT subject_id, key, payload FROM agent_observations
WHERE subject_id='bp-013' ORDER BY commit_sha;

-- Q_projections: sanity — projected-commit count matches the dry-run's `projected` figure
SELECT count(*) FROM projections;

-- Q_idempotence (run scripts/sense_self.py a SECOND time after the above, then re-run
-- Q_total — the count must be byte-identical; Item 11's acceptance test)
```

Expected values at this builder's HEAD (post-merge, on `main`, once Item 9's commit
lands there): `Q_total` = 27 (this session's dry-run measurement, `worktree` branch
— will differ slightly if more commits land on `main` before the orchestrator runs
this, per the plan's own ">= not ==" framing); `Q_join` >= 5 pairs including
`bp-013` (measured 11 this session); `Q_bp013` shows the corrected
`{model: opus, tokens: 54048, ...}` payload at `commit_sha=6d6bc24...` (or whatever
sha this plan's commit lands at on `main` after merge — the dry-run's `6d6bc24` is
the WORKTREE-local sha; a merge or rebase onto `main` may mint a different sha for
the same content, which is expected and fine — φ_self records whichever sha
actually lands the fact on `main`).

**NOT run this session** — no live write, no `data/` touch, no attestation emitted
by this builder. This satisfies plan §3's risk note (builders never touch the main
checkout's live stores, finding-0031 class) and §11's parked "who runs the live
write" decision (orchestrator at seal, main checkout).
