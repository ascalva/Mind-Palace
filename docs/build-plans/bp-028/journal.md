# bp-028 journal

## 2026-07-13 — minted at graduation (orchestrator)

Born `proposed` from `/graduate dn-external-grounding` (ratified 2026-07-13). The live
driver: wire the dormant airlock into a running `research_criteria → emit → collect →
rank → surface` chain, foreground (Ambassador TASK-intent) + background (scheduler
trough), surfacing **transiently**. §3 grounded against a 2026-07-13 read-only recon
(citations inline: the chain is dormant — zero production callers of `research_criteria`/
`rank_literature`; `"research"` job kind mapped at `scheduler/router.py:31` but never
enqueued; the Ambassador TASK path currently routes to `librarian.answer`). §4 reconciles
the BUILD-SPEC §16 medical-only framing via a cross-ref banner (Item 26), no body rewrite.
Items 23→24→25 gated; Item 26 independent. `parallelizable_with: [bp-027]`. bp-029 depends
on this. Model estimate opus/300k (invariant-adjacent — do not cheap-delegate). Awaiting
the owner-only `proposed → ready` blessing. No work started.

## 2026-07-13 — build session opened (orchestrator, self-driven opus/high)

`status: ready → in-progress`; `active-plan` pointer set. §2 context manifest read whole,
in order: `airlock.py`, `criteria.py`, `rank.py`, `librarian.research_criteria` +
`_deterministic_proposer`, `scheduler/{router,cron,queue,interface,supervisor}.py`,
`agents/ambassador/{agent,policy,intent}.py`, and the existing research tests
(`test_research_{airlock,rank}.py`) + `test_ambassador_conversation.py` for fixtures.

**Design decisions (grounded; before code):**

1. **`collect_one(criteria.id)` not `collect()`** in the driver. Item 23's prose says
   `collect(consume=True)`, but a single-request driver that drains `collect()` would
   wrongly rank OTHER pending criteria's results against THIS criteria. `collect_one` is
   the keyed primitive (§6 pins both as available; using the precise one is within spec, not
   a signature change). Documented deviation.
2. **De-identify at the foreground enqueue boundary** (Item 25). Its acceptance test says
   "a `research` job is enqueued with a **de-identified** query" → the payload must carry
   `criteria.to_request()` (topic + scrubbed terms + coarse filters), never raw conversation
   text. The `delegate` closure calls `librarian.research_criteria(query)` (deterministic
   proposer — no model needed) and stores `to_request()`; the gate ledger records only
   `criteria.topic`. The driver's `run_research(criteria, …)` takes the already-built
   criteria; `airlock.emit` re-asserts clean (defense in depth) at the true outbound edge.
   Item 23's own `research_driver(query, …)` de-identifies internally for its end-to-end test.
3. **Async reality:** emit writes the request; a real fetcher responds later. A single
   invocation that emits-then-collects returns `[]` when nothing is back yet (the graceful
   degrade — §3 risk + §10 stop-condition). Round-trip tests inject a **fake airlock** whose
   `collect_one` returns canned papers (matching the codebase's injectable-fakes pattern);
   `build_conversation_runtime` gains an injectable `airlock=` param.
4. **Research-shape check** (`is_research_request`, `agents/ambassador/policy.py`): conservative
   external-literature cues ("research on", "papers", "literature", "studies", "meta-analysis",
   …); default → the existing `ambassador_task` (mirror) path on doubt (§11 parked decision).

**Scope finding (to file):** the PRODUCTION daemon handler map + delegate are assembled in
`ops/lifecycle/launcher.py:188,193` — OUTSIDE this plan's `write_scope`. Registering
`RESEARCH_KIND` + passing a librarian to `build_task_delegation` there is the one-line
production activation; it is a `spec-fidelity` finding to park (§10), NOT a silent
out-of-scope edit. All four items' acceptance tests are satisfiable in-scope (driver test,
supervisor/queue drain, delegate-routing + Ambassador tests, ConversationRuntime e2e).
Starting Item 23.

## 2026-07-13 — BLOCKED on write_scope defect + high-effort re-review (orchestrator)

**Blocker surfaced → finding-0071.** `write_scope` lists NO test paths, so `scope-guard`
denies every `tests/**` write — the §7 acceptance tests for Items 23–25 cannot be authored.
Every sibling code-build plan (bp-021/022/024/025/026) enumerates its test files; this is a
graduation oversight. Widening an owner-blessed **invariant-adjacent** plan's capability is
owner-gated ("never route around"), so this parks pending the owner's hand-edit of
`write_scope` (owner chose: hand-edit, 2026-07-13). finding-0071 also carries the launcher.py
production-registration gap.

**Delivered in-scope (verified):**
- **Item 23** — `scheduler/research.py` (driver: `run_research`, `research_driver`,
  `criteria_from_request`, `render_ranked`). **Untested** (test denied) but: `ruff check`
  clean, `mypy scheduler` = *Success, no issues* (Tier-2 hard-floor 0-error requirement met),
  imports clean. Logic re-reviewed: `collect_one(id)` keyed (no cross-criteria mis-rank),
  graceful `[]` on empty, outbound built only via `research_criteria`, zero store writes.
- **Item 26** — BUILD-SPEC §16 banner. Diff = **7 insertions, 0 deletions** (body untouched);
  cites `dn-external-grounding §2.4`/`§2.5` — both **verified to exist** (note L170/L197);
  link target `docs/design-notes/external-grounding.md` verified; renders as a blockquote.

**Effort correction (context for next agent).** This session ran at **low** effort for the
first pass (wrong tier — the resume brief mandated high for this invariant-adjacent build);
owner switched to **high** mid-session and requested a re-review. The re-review found no
correctness defects in the delivered code, but surfaced the gate shape + one deeper design
point below.

**Gate legs identified (`.github/workflows/ci.yml`), for seal time:** (1) ratchet =
`uv run ruff check .` + import-firewall + `pytest -q -m 'not live and not podman and not
needs_vault and not needs_restic'`; (2) type-gate = `mypy core agents eval ops scheduler
scripts` (**0 errors, hard floor**) + argless `mypy` pinned at **69** (tests baseline);
(3) vault-axis `pytest -m needs_vault`; (4) semgrep report-only (non-blocking); (5) release.
**`ruff format` is NOT a gate leg** — it would reformat existing passing files
(`policy.py`/`cron.py`/`interface.py`); house style is the compact hand-format, so do NOT run
`ruff format` on new files (`research.py` already matches house style + passes `ruff check`).

**Deeper design point (high-effort pass).** `emit` and `collect` are temporally separated by
the cloud round-trip: a single `run_research` invocation emits, then `collect_one` finds
nothing back yet in a LIVE deployment → returns `[]`. The one-shot driver is the correct SEAM
for this plan (the plan's §3 risk + §9 non-goals scope the live async round-trip out — it
degrades gracefully). The full live round-trip (a separate collect pass keyed to persisted
criteria ids, so a result that arrives later is ranked against ITS criteria) is **future**,
not built here — do not assume live results surface same-run. Synchronous/fake-airlock tests
exercise the chain fully; that is what the §7 acceptance tests do.

**Re-entry (unchanged from finding-0071):** owner adds test paths to `write_scope` → author
§7 tests for Items 23–25, write Items 24/25 code (`scheduler/cron.py` handler+`enqueue_research`;
`scheduler/interface.py` research-routing delegate + `RESEARCH_KIND` in `pending_results` +
injectable `airlock` in `ConversationRuntime`; `agents/ambassador/policy.py` `is_research_request`),
run the 5-leg gate, seal. Items 24/25 design validated against the code: `router.plan("research")`
→ synthesis tier + `PRIORITY_BACKGROUND`; `HEAVY_TIERS` (⊇ synthesis) defers it under foreground.

## 2026-07-13 — UNBLOCKED, build resumed at high effort (orchestrator)

Owner hand-added FOUR paths to `write_scope`: the three §7 test files **plus**
`ops/lifecycle/launcher.py` (the production activation). The owner's raw edit glued the inline
`# Item NN` comments to the unquoted paths — the repo's front-matter parser only strips comments
from *quoted* scalars (oq-0013), so scope-guard saw `'tests/…driver.py      # Item 23'` (would
never match). Reconciled the FORMATTING to the owner's explicit intent: **quoted** the four new
paths (comments now stripped) + fixed the wrapped `Ambassador)` line. Verified via
`_lib.plan_write_scope` → the seven entries parse clean. This is a formatting reconciliation of
the owner's stated authorization, not a scope widening.

**Consequence:** `launcher.py` in scope ⇒ finding-0071's item 2 (production registration) is
resolved IN-PLAN, not parked. Resuming at high effort: Item 23 test → Items 24/25 code+tests →
launcher activation → 5-leg gate → seal.

## 2026-07-13 — COMPLETE (orchestrator, self-driven opus/high)

All four items landed + the production activation. Every §9 non-goal honored (no persistence —
`ExplodingStore` test proves zero store writes; no fetcher change; no `core/research` or
`core/librarian` signature change — used as-is; no new query surface). Every §7 falsifier
checked and NOT tripped.

- **Item 23 — the driver** (`scheduler/research.py`): `run_research` (emit → `collect_one` keyed →
  rank, transient `[]` on empty), `research_driver` (de-identify → run), `criteria_from_request`,
  `render_ranked`. Test `test_research_driver.py` (6): ranked return, de-identified emit (PII query
  "MY migraines since March 2019" → no march/2019 in the outbound blob), empty-degrade, keyed
  collect (no cross-criteria bleed), request round-trip, plain render.
- **Item 24 — the trough job** (`scheduler/cron.py`): `research_handler` + `enqueue_research`.
  Test `test_research_cron.py` (3): routes synthesis + `PRIORITY_BACKGROUND`; the foreground gate
  (`HEAVY_TIERS ⊇ synthesis`) keeps it QUEUED while the owner is present then drains it in the
  trough; de-identified payload; graceful degrade with no result.
- **Item 25 — the foreground path** (`scheduler/interface.py` + `agents/ambassador/policy.py`
  `is_research_request`/`RESEARCH_CUES`): research-shaped TASK → de-identified `"research"` job +
  `narrate_effort` reply; non-research TASK → unchanged `ambassador_task` path; `pending_results`
  surfaces the ranked reading list on a later turn; `ConversationRuntime` gained a research
  handler + injectable `airlock`. Robustness (high-effort add, §11 warrant): a query yielding no
  de-identifiable terms FAILS CLOSED (nothing emitted) and falls back to the general path — never
  crashes. Test `test_research_foreground.py` (5): enqueue+de-identify, no-regression, surfacing,
  no-librarian-off, fail-closed fallback.
- **Item 26 — §16 banner**: 7 insertions, 0 deletions; cites the ratified §2.4/§2.5.
- **Production activation** (`ops/lifecycle/launcher.py`): `RESEARCH_KIND` registered in the
  supervisor handler map; `build_task_delegation` now receives the task librarian (the
  `research_criteria` de-identify seam) + a `build_airlock(cfg)`. The daemon now RUNS the airlock.

**Gate (all five legs, run separately):** ruff `All checks passed`; import-firewall (Inv 2) `OK`;
model-free pytest **991 passed, 4 skipped, 20 deselected**; mypy Tier-2 hard floor `0 errors`
(174 files); argless mypy pinned **69** (tests baseline intact — new-test fakes cast, not left as
errors); semgrep `0 findings` (report-only). **Vault-axis** = 3 skipped locally (no vault; the
change doesn't touch it). **Live tier NOT run** (plainly noted per CONVENTIONS): every bp-028 test
is deterministic with injected fakes (airlock/embedder/store) — the live model tier is not newly
exercised by a path I could test live-vs-deterministic; finding-0069/oq-0018 default (c) stands.

**finding-0071 → resolved** (both halves). Cost: est opus/300k; **actual recorded at seal from
/usage** (self-driven, no subagent fan-out — the lean path chosen for the budget). Sealing:
status `in-progress → complete`, `active-plan` cleared, PROGRESS checkpointed.

**Seal state (2026-07-13, mid-close):** code committed `97d98ca` (Co-Authored-By). Plan flipped
`complete`; finding-0071 `resolved`. REMAINING for the seal commit (no Co-Authored-By): pin
`cost.actual` from the owner's `/usage` relay, append the PROGRESS checkpoint, clear `active-plan`,
rewrite the resume-brief, then `docs(build-plans): seal bp-028` + push. A fresh agent resuming here:
everything is built + gated green (991 pass, mypy 0/69); only the bookkeeping commit + push remain.
