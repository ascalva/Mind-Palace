---
type: build-plan
id: bp-028
status: proposed
design_ref:
  - docs/design-notes/external-grounding.md
contract: builder
write_scope:
  - scheduler/**
  - agents/ambassador/**
  - docs/BUILD-SPEC.md
session_budget: 1
cost:
  estimate:
    model: opus
    tokens: 300k
  actual: null
depends_on: []
parallelizable_with: [bp-027]
created: 2026-07-13
updated: 2026-07-13
links:
  - docs/design-notes/external-grounding.md
  - docs/design-notes/edge-core-handoff-protocol.md
  - docs/design-notes/hands-and-the-effector-layer.md
re_entry: null
supersedes: null
superseded_by: null
warrant: null
---

# Build Plan — the live driver (wire the dormant research airlock to run)

> **Every section below is required.** Inapplicable sections are marked `N/A — <reason>`.

## 0. Mode & provenance

Graduated from `dn-external-grounding` (ratified 2026-07-13) §2.4 (the reframe: the
airlock is built but dormant) + §2.5 (the live driver — the common missing piece) +
§3.3 + §3.5 (the §16 reframe). Investigation + planning produced this plan (§3 is
grounded against the code via a 2026-07-13 recon); implementation proceeds item-by-item
on owner approval. `proposed → ready` is owner-only, by hand. No agent flips readiness.

**Design-adjacent, invariant-touching.** This wires an outbound/network-adjacent
subsystem (the airlock, `edge/`-side) and must preserve Inv 2 (only the fetcher touches
the network), Inv 7 (health advice defers), and the never-pollute-the-mirror rule. It is
NOT a cheap-delegate plan — run it as a scrutinized session (delegate skill: falsifier
needs judgment → full-strength).

## 1. Objective

Add the single missing orchestration seam so a query flows
`research_criteria → airlock.emit → collect → rank_literature → surface` — driven both
in the foreground (Ambassador TASK-intent) and in the background (a scheduler trough
job) — surfacing ranked results **transiently** (never persisting to the mirror).

## 2. Context manifest

Read whole, in order, before any work:

1. `docs/design-notes/external-grounding.md` §2.4–§2.5 — the reframe + the live-driver decision (the "what" and "why").
2. `docs/BUILD-SPEC.md` §16 (the airlock spec: dumb-outside/smart-inside, evidence-honesty, Inv 7) + §13 (the scheduler trough).
3. `core/research/criteria.py` — `ResearchCriteria`, `deidentify()`, `assert_clean()`, `to_request()`.
4. `core/research/airlock.py` — `ResearchAirlock.{emit, collect, collect_one}`, `ResearchResult`, `build_airlock()`.
5. `core/research/rank.py` — `rank_literature()`, `RankedPaper`, the transient contract (§7 lines 7–10).
6. `core/librarian/librarian.py` — `research_criteria()` (lines 187–204) + `retrieve/answer` (the existing TASK path).
7. `scheduler/router.py` (`_SYNTHESIS_KINDS`, line 31 `"research"`), `scheduler/cron.py` (the `dream_handler`/`curate_handler` trough pattern), `scheduler/queue.py` (`PRIORITY_BACKGROUND`), `scheduler/interface.py` (the delegate closure, `build_task_delegation`).
8. `agents/ambassador/agent.py` (`_delegate` 204–210, TASK-intent 161–175) + `agents/ambassador/policy.py` (`narrate_effort` 44–53).

## 3. Investigation & grounding

- **Q1 — Does the emit→collect→rank chain exist end-to-end today?** No. `research_criteria()` (`core/librarian/librarian.py:187`) and `rank_literature()` (`core/research/rank.py:102`) are defined and exported (`core/research/__init__.py:31`) but have **zero production callers** — invoked only in unit tests. Job kind `"research"` is mapped to the synthesis tier (`scheduler/router.py:31`) but **never enqueued**. The chain is dormant. The code settles this.
- **Q2 — What is the airlock's exact contract?** `emit(criteria: ResearchCriteria) -> str` writes `criteria.to_request()` to `handoff/requests/<id>.json` and returns `criteria.id` (`core/research/airlock.py:70-80`). `collect(*, consume=True) -> list[ResearchResult]` reads/deletes `handoff/results/<id>.json` (`:95-106`); `collect_one(id, *, consume=True)` for a single id (`:82-93`). `ResearchResult` = `{criteria_id, papers: tuple[Paper,...], sources_queried, ts}` (`:42-57`). Wired via `build_airlock(config)` (`:109-114`) against `cfg.airlock.handoff_dir`. The diode is one-way filesystem; **core never touches the network** — the fetcher (Zone C) reads `requests/`, writes `results/`.
- **Q3 — What does the outbound seam produce, and is it PII-safe?** `research_criteria(query, *, proposer=None, from_year=None, publication_types=(), max_results=50) -> ResearchCriteria` (`core/librarian/librarian.py:187`): the proposer extracts `(topic, terms)`, `deidentify()` scrubs (`core/research/criteria.py:181`), `assert_clean()` re-scrubs at the emit boundary (`:93`). The type has no free-text content field — PII-safety is structural + runtime. The code settles this.
- **Q4 — Does ranking mutate anything?** No. `rank_literature(result_papers, criteria, embedder, store, *, k_notes=5) -> list[RankedPaper]` is a pure read over the embedder + mirror vectorstore (cosine to the owner-notes centroid); papers are ranked in-memory and **discarded** — `core/research/rank.py:7-10` states it is never written to the mirror. This is the transient contract this plan MUST preserve. The code settles this.
- **Q5 — How is a background job registered + gated to idle windows?** `scheduler/router.py:26-40` maps kinds→tiers; `"research"` is already a synthesis kind (`:31`). `scheduler/cron.py` shows the trough-handler pattern (`dream_handler`, `curate_handler`) + `enqueue_*` helpers (`:51-58`). Background priority (`PRIORITY_BACKGROUND`, `scheduler/queue.py`) + the supervisor's foreground gate (`HEAVY_TIERS`) run it only when the conversation is idle (§13). The code settles the registration seam.
- **Q6 — What does the Ambassador do on a TASK intent today?** `_delegate(text, conversation) -> str` (`agents/ambassador/agent.py:204-210`) calls the injected `self.delegate` closure (`:111`), wired by `scheduler/interface.py` (`build_task_delegation`), which currently routes to `librarian.answer()` (a **general grounded retrieval**, `scheduler/interface.py:56`) — NOT a research-criteria emission. `narrate_effort()` (`agents/ambassador/policy.py:44-53`) is production code (the "I'll dig into this" reply), not a stub. So the foreground seam exists but points at the wrong target; this plan adds the research path.

**Additional risks or questions surfaced during reading:**
- The fetcher (Zone C) is an AWS Lambda (`cloud/fetcher/handler.py:58`). In a **local/Tailscale** deployment the `results/` side may have no live producer — the driver must degrade gracefully when `collect()` returns empty (no results yet / no fetcher running), not hang or error. Pinned as a stop-condition + falsifier.
- "Surface" is deliberately transient in this plan (return the ranked list in the job result / foreground reply). Persisting keepers is **bp-029**, not here — do not add any embed/store write.

## 4. Reconciliation

- `docs/BUILD-SPEC.md` §16 — currently frames the airlock as **medical research** ("search and find medical research papers"). `dn-external-grounding §2.4/§3.5` (ratified) generalizes it to literature grounding (arXiv/OpenAlex for design-grounding + Europe PMC for medical), one machinery. → **[cross-ref: extension]** Add a banner at the head of §16: *"Generalized by `dn-external-grounding §2.4` — this machinery is corpus-agnostic literature grounding; the medical case is one use (keeping Inv 7), design-grounding (arXiv/OpenAlex) is another. See §2.5 for the live driver."* **Do NOT rewrite §16's body** (it is still accurate for the medical case); add the banner + a pointer only. Carried by Item 26.
- No committed code is corrected — this plan only ADDS the missing driver + wiring; every existing signature (`emit`/`collect`/`rank_literature`/`research_criteria`) is used as-is, unchanged.

## 5. Write scope

Front-matter: `scheduler/**`, `agents/ambassador/**`, `docs/BUILD-SPEC.md`. In prose: the
new research driver/handler + its router/queue registration live under `scheduler/`; the
foreground TASK-intent → research path is a wiring change under `agents/ambassador/`; the
§16 banner is the ONLY `docs/BUILD-SPEC.md` edit. **Deliberately OUT of scope:**
`core/research/**` and `core/librarian/**` (their signatures are used unchanged — if one
needs changing, that is a spec-defect finding, not a silent edit); `cloud/fetcher/**` (the
fetcher is complete; full-text is bp-029); `core/stores/**` + `data/**` (no persistence —
that is bp-029); `docs/reference_material/**` (bp-027/bp-029); every design note, finding,
and the foundation denylist.

## 6. Interfaces pinned inline

Copied verbatim from the current code (2026-07-13) — the builder honors these, never infers:

```python
# core/librarian/librarian.py:187 — the outbound seam
def research_criteria(self, query: str, *, proposer: TermProposer | None = None,
                      from_year: int | None = None,
                      publication_types: tuple[str, ...] = (),
                      max_results: int = 50) -> ResearchCriteria: ...

# core/research/airlock.py — the one-way diode
class ResearchAirlock:
    def emit(self, criteria: ResearchCriteria) -> str: ...            # writes requests/<id>.json, returns id
    def collect(self, *, consume: bool = True) -> list[ResearchResult]: ...
    def collect_one(self, criteria_id: str, *, consume: bool = True) -> "ResearchResult | None": ...
def build_airlock(config: "Config | None" = None) -> ResearchAirlock: ...

# core/research/airlock.py:42 — the result
@dataclass(frozen=True)
class ResearchResult:
    criteria_id: str
    papers: tuple[Paper, ...]
    sources_queried: tuple[str, ...]
    ts: str

# core/research/rank.py:102 — TRANSIENT ranking (never persists)
def rank_literature(result_papers: list[Paper], criteria: ResearchCriteria,
                    embedder: Embedder, store: VectorStore, *,
                    k_notes: int = 5) -> list[RankedPaper]: ...
# RankedPaper (rank.py:49): paper, relevance: float, evidence_tier: str, score: float, flags: tuple[str,...]

# scheduler/cron.py — the trough-handler pattern to mirror (dream_handler / curate_handler)
#   a Handler is a closure (job: Job) -> str, registered against a job kind; enqueued at BACKGROUND priority.
# scheduler/router.py:31 — "research" is ALREADY a _SYNTHESIS_KINDS member (synthesis tier, background).

# agents/ambassador/agent.py:204 — the foreground TASK seam (self.delegate injected by scheduler/interface.py)
def _delegate(self, text: str, conversation: str) -> str: ...
```

## 7. Items

### Item 23 — The research driver (pure orchestration: emit → collect → rank → surface)

- **Objective:** a driver function/handler that takes a query, calls `librarian.research_criteria(query)`, `airlock.emit(criteria)`, `airlock.collect(consume=True)`, `rank_literature(...)` per result, and returns the ranked list (transiently — as the return value, no store write).
- **Files:** `scheduler/research.py` (new; the driver) or an added handler in `scheduler/cron.py` — builder's call, matching the existing trough-handler shape.
- **Acceptance test:** a unit test drives the chain against a **fake airlock** (a `collect()` returning a canned `ResearchResult` with 2–3 `Paper`s) + a real `rank_literature` over a tiny embedder/store fixture; asserts a sorted `list[RankedPaper]` is returned and that `emit()` was called with a de-identified `ResearchCriteria` (`to_request()` carries no free-text content). Exits 0.
- **Falsifier:** the driver writes any paper/result into the mirror vectorstore or any store (violates the transient contract, `rank.py:7-10`); OR it constructs the outbound request from raw `query` text bypassing `research_criteria`/`deidentify` (PII leak); OR it raises instead of returning `[]` when `collect()` is empty.
- **Invariant(s) it must not violate:** Inv 2 (never touches the network directly — only via the airlock's `requests/` file); never-pollute-the-mirror (transient only); Inv 3 (the model advises via the proposer; `deidentify` code enforces).
- **Touches stored data?** No — reads the mirror store for ranking (read-only), writes nothing.
- **Parallelizable?** No (internal — Items 24/25 depend on it).  **Depends on:** none.

### Item 24 — Register the background (trough) research job

- **Objective:** register the Item-23 driver as the handler for the `"research"` job kind and add the enqueue seam so it runs in idle windows.
- **Files:** `scheduler/cron.py` (register handler + `enqueue_research` helper), `scheduler/router.py` (confirm/verify `"research"` routing — no change expected, `:31`).
- **Acceptance test:** a test enqueues a `"research"` job and asserts (a) the router assigns it the synthesis tier + `PRIORITY_BACKGROUND`; (b) the supervisor's foreground gate defers it while a conversation is active; (c) draining the queue invokes the Item-23 driver. Exits 0.
- **Falsifier:** the research job runs at foreground priority / blocks an active conversation (violates §13 trough discipline); OR routing lands it on a non-synthesis tier.
- **Invariant(s) it must not violate:** §13 (background jobs never block foreground); memory ceiling (≤2 resident models — the synthesis tier already respects it).
- **Touches stored data?** No.
- **Parallelizable?** No.  **Depends on:** Item 23.

### Item 25 — Wire the foreground Ambassador TASK-intent → research

- **Objective:** on a research-shaped TASK intent, route the Ambassador's `_delegate` to enqueue an Item-24 research job (instead of only `librarian.answer`), and reply via `narrate_effort`.
- **Files:** `agents/ambassador/agent.py` (the TASK path, ~161–175/204–210), `scheduler/interface.py` (extend `build_task_delegation` to offer the research enqueue), `agents/ambassador/policy.py` (only if the intent-shape check needs a helper).
- **Acceptance test:** a test sends a research-shaped TASK message; asserts a `"research"` job is enqueued with a de-identified query and the reply is the `narrate_effort` narration; a non-research TASK still routes to the existing `librarian.answer` path (no regression).
- **Falsifier:** every TASK message now enqueues research (over-capture — the existing general-retrieval path is broken); OR the raw conversation text reaches the enqueue payload without going through `research_criteria`/`deidentify` (PII leak into the outbound path).
- **Invariant(s) it must not violate:** Inv 11 (the interface may transit a third party, the corpus never does — the enqueued payload is de-identified criteria, not corpus); Inv 3.
- **Touches stored data?** No.
- **Parallelizable?** No.  **Depends on:** Item 24.

### Item 26 — Reframe BUILD-SPEC §16 (medical-only → general grounding) via a banner

- **Objective:** add a cross-reference banner at the head of §16 pointing to `dn-external-grounding §2.4` (the generalization); leave §16's body intact.
- **Files:** `docs/BUILD-SPEC.md` (§16 head only).
- **Acceptance test:** §16 opens with the banner naming `dn-external-grounding §2.4`; a diff shows ONLY the banner added (no body line changed); the file still parses (renders).
- **Falsifier:** any §16 body sentence changed, or any other BUILD-SPEC section touched.
- **Invariant(s) it must not violate:** the artifact chain (this implements a ratified decision; it does not make a new one) — no design decision is introduced in the banner beyond the ratified note's.
- **Touches stored data?** No.
- **Parallelizable?** Yes (docs-only, independent of 23–25).  **Depends on:** none.

## 8. Math carried explicitly

**N/A — no mathematical object implemented.** `rank_literature`'s cosine/centroid math
already exists and is used unchanged; this plan adds orchestration, not math.

## 9. Non-goals

- **No persistence / embedding.** Surfacing is transient (the return value). Full-text fetch, the curated store, chunk+embed, and manifest minting are **bp-029**.
- **No fetcher changes.** `cloud/fetcher/**` is complete; abstract-level metadata is what crosses the airlock in this plan.
- **No signature changes** to `core/research/**` or `core/librarian/**` — used as-is.
- **No new query surface** (that is the parked index-query slice, finding-0070 / fable-vet).

## 10. Stop-and-raise conditions

- `collect()` returns empty because no fetcher is running in this deployment → the driver returns `[]` gracefully; if the WIRING itself can't be tested without a live fetcher, file a `codebase` finding describing the test seam and park that item (do not fake a network call).
- A signature in `core/research`/`core/librarian` turns out to need changing to wire the driver → **file a `spec-defect` finding** (it means the design under-specified the seam); park, continue other items.
- Any urge to persist results, touch the fetcher, or edit a design note → STOP (out of scope, §9).
- Any `proposed→ready` / `draft→ratified` flip it would have to perform → it must not.

## 11. Parked decisions

| Decision | Default recorded | Rejected alternatives (why) | Re-entry condition |
|---|---|---|---|
| Foreground vs background as the primary driver | BOTH (Item 25 foreground TASK + Item 24 background trough); foreground for owner-initiated grounding, background for the demand-driven worklist | foreground-only (rejected: the ratified-note worklist needs the idle-window job); background-only (rejected: owner asks interactively) | — (both built) |
| Transient vs persisted surfacing | transient (this plan) | persist now (rejected: the copyright/licence gate is a substantive separate build — bp-029) | bp-029 reaches `ready` |
| Research-intent detection shape | a conservative shape-check in Item 25 (explicit "research/find papers on…" cues), default to the existing `librarian.answer` path on doubt | model-classified intent (rejected here: over-capture risk; keep the general path as default) | if precision is poor in use, revisit with a classifier |

## 12. Dependency & ordering summary

Blast-radius order: **Item 23** (pure orchestration, no writes) → **Item 24** (background
registration) → **Item 25** (foreground wiring) — 23 gates 24 gates 25. **Item 26** (docs
banner) is independent and parallelizable within the plan. `depends_on: []` at the plan
level; `parallelizable_with: [bp-027]` (disjoint scope: `scheduler`/`agents`/`BUILD-SPEC`
vs `docs/reference_material`). **bp-029 depends on this plan** (it flips this plan's
transient surfacing to persisted). Model: opus (invariant-adjacent; falsifiers need
judgment — do not cheap-delegate).
