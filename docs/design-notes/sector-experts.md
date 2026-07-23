---
type: design-note
id: dn-sector-experts
track: workflow
status: draft            # draft → ratified → superseded.  draft→ratified is an OWNER-ONLY hand edit.
created: 2026-07-23
updated: 2026-07-23
links:
  - docs/brainstorms/sector-expert-community.md        # the warrant capture (owner vision, near-verbatim)
  - docs/brainstorms/reconciliation-audit.md           # the adversarial-gate + expert-panel rulings this generalizes
  - docs/design-notes/agent-taxonomy.md                # the corpus-side agent species this mirrors (workshop-pointed)
  - docs/design-notes/agent-workflow.md                # the constitution this amends (the chain gains a review stage)
  - docs/findings/finding-0151.md                      # witness discipline precedent (answers carry evidence)
supersedes: null         # amends dn-agent-workflow (the review stage + the sector map) at ratification — owner banners
warrant: docs/brainstorms/sector-expert-community.md
adversarial_review: OWED               # the gate reviews the design of its own generalization — harness + security + core panel minimum
---

# Design note — the sector-expert community (learn · audit · defend)

> The maintainer community becomes part of the organism. Experts hold sectors; the owner holds
> the constitution and the gates. Every interaction — review, answer, dispute, re-learning — is
> planned, tracked, attested, and INGESTED: the workshop merges into the palace, and the
> development process becomes something the system itself can understand.

## 0. Provenance & mode

Fable design pass, in-session (owner-directed, 2026-07-23). Warrant: the owner's vision capture
(sector-expert-community.md) plus the two rulings it generalizes — the adversarial-review gate
(every artifact reaches the owner WITH an independent refutation attempt) and the domain-expert
panel (adversaries are specialists, not generalists). This note turns a gate-time panel into a
STANDING institution with a lifecycle: **learn, audit, defend**.

## 1. Objective

1. **Touch-triggered review.** Any orchestrator/builder change touching a sector triggers that
   sector's expert — on TOUCH, not only at bless/ratify. Gate-time panel review becomes the
   special case of a general mechanism.
2. **Experts as oracles.** Load-bearing questions route to the sector expert; answers are
   ARTIFACTS carrying evidence and a falsifier — definitive by grounding, never by role.
3. **Experts as institutions.** Each expert is a durable, versioned knowledge artifact (brief +
   lens + checklist) that LEARNS its sector, compounds its misses into checklist lines, and is
   itself gated like any design artifact.
4. **The community as corpus.** Expert interactions are exhaust: transcripts ingest (the chat
   sensor already eats them), reviews are typed artifacts, attestations land in the existing
   store, and the composed causal graph covers the community's own work — trackable, attestable,
   understandable.

### 1.2 Out of scope (non-goals — read deliberately at ratification)

- **No authority transfer.** Blessings/ratifications stay owner-only by hand; experts hold NO
  write power beyond reviews, findings, and answers (the model advises; code acts; gates
  unchanged). The community scales the owner's ATTENTION, never his authority.
- **No resident daemons.** Experts are spawned from artifacts on demand (review, question,
  re-learn) — sessions disposable, artifacts durable. A standing process per sector is rejected
  on context-economy grounds.
- **No separate corpora.** An expert's memory is a LENS over the one corpus + its brief — never a
  private store (mini-palaces rejected; DRY at architecture level).
- **No expert-to-expert autonomous negotiation loops** in v1 — interactions route through the
  orchestrator (planned), and boundary disputes route UP to the owner, never resolved by the
  disputants.
- **Not the palace's own runtime agents** (dreamer/curator/integrator — dn-agent-taxonomy):
  same species, different pointing; nothing in core/ changes here. This is workshop-side.

## 2. Decisions

### D1 — The sector map: one owner-ratified routing artifact

`docs/sectors/MAP.md` (owner-ratified; agent-immutable once ratified): sector → {write_scope
globs, design-note surface, the expert's brief path, review tier}. Routing is MECHANICAL: a
change's touched paths select its experts (core/** → core; scheduler/** → systems; edge/,
secrets, effectors, hooks → security ALWAYS; a non-N/A §8 → math MANDATORY; docs/design-notes/**
→ workflow + the note's surface experts). Overlaps select BOTH (a union, never a coin-flip).
Initial roster: **core · harness/workflow · security · math/logic · systems/scheduler** — grown
only by the D6 institution-minting path.

### D2 — The expert is its artifacts: contract + brief + lens

- **Contract**: `.claude/agents/auditor-<sector>.md` — the spawn template (persona-neutral,
  CONSTITUTION-framed, read-only tools + findings/review write).
- **Brief**: `docs/sectors/<sector>/brief.md` — the grown sector model: invariants, interfaces,
  design philosophy digest, open findings/PDs, and the **misses ledger** (every detection-lag
  failure in the sector becomes a permanent checklist line — the compounding property).
- **Lens**: a retrieval recipe over the ONE corpus (sector-scoped globs + note/finding filters +,
  when the membership store lands, sector-scoped semantic search). The expert's "context
  management system" = brief + lens + the checklist; the process instantiating it is ephemeral.

### D3 — AUDIT: touch-triggered review, tiered by stakes

Two tiers, selected by the sector map: **conformance pass** (cheap: checklist + invariants +
pins-verified, for small in-sector mechanical touches) and **full adversarial review** (the gate
tier: merit/logic/correctness/measured-premises, briefed to REFUTE) for invariant-adjacent
surfaces, all design notes, all seals. Security and math sit on the low threshold (when in
doubt, in). Output: a typed review artifact (severity-ranked findings, named coverage — WHICH
expert examined WHAT, so an unexamined surface is visible). The blessing-gate input remains
{artifact + reviews}, per the standing ruling.

### D4 — DEFEND: the oracle discipline + the challenge protocol

An expert ANSWER to a load-bearing question is an artifact: `{answer, evidence refs (paths/
greps/measurements), confidence, what-would-falsify}`. Graded like composed edges — grounding
earns "definitive"; an ungrounded answer is a defect. **Challenge protocol**: any agent (or the
owner) may challenge an answer or a sector invariant; the expert must defend WITH EVIDENCE; a
successful challenge is a finding against the sector brief, which UPDATES it (the community
error-corrects itself). Defend also means guarding: reviews defend the sector's invariants
against erosion — the guardian posture is the same discipline pointed at changes.

### D5 — LEARN: bootstrap + drift-triggered re-learning

Bootstrap = a sector sweep (code + docs + state + philosophy → the brief's first edition,
reviewed like any artifact). Maintenance = re-learn ON CHANGE VELOCITY, not on a clock: each
sector carries a small drift gauge (files changed / findings filed / notes ratified since the
brief's `grounded_at` commit); crossing the threshold queues a re-learn pass that DIFFS the brief
against reality and files what it finds. A stale brief is a visible state, never a silent one
(`grounded_at` is printed in every review the expert signs).

### D6 — Institution minting is organizational self-modification — gated

A new expert / a sector-boundary change = a brief + MAP entry through the full chain (draft →
adversarial review → owner ratifies). §14's shape applied to the org: propose → approve →
validate (the new expert's first reviews are themselves reviewed) → reversible (a sector can be
merged back; briefs are versioned). No agent mints an institution by side effect.

### D7 — The community is corpus: tracked, attested, understood

Nothing new to build for capture — the existing machinery eats it: expert sessions are
transcripts (chat sensor → L1 events); reviews/answers/briefs are typed files in git (the code
lane embeds them; `commit_diffs` chains their evolution); attestations ride the existing store;
the composed causal graph (dn-integrator-densification) covers community work exactly as it
covers code — *which review changed which design* becomes a traversable path. The procedure is
the point: **ingested → tracked → attested → understood.**

### D8 — The owner's read surface: verdicts and dissents, not transcripts

The bottleneck moves from reading artifacts to reading reviews — so reviews COMPRESS: one merged
report per gated artifact (severity-ranked, named-coverage, DISSENTS PRESERVED — a lone dissent
is a feature, never averaged away), sized for the exhaust lane (phone-readable). The owner reads
verdicts + dissents; transcripts remain for descent when something smells.

## 3. Wiring & enablement (required §)

**Interim (EFFECTIVE ALREADY, owner ruling 2026-07-22/23):** no artifact reaches the owner
un-reviewed; the orchestrator convenes the panel manually per the sector map's logic. **Structural
(this note's build):** (1) the MAP + initial five briefs + contracts (bootstrap sweeps, reviewed);
(2) hook-side: the write_scope→sector trigger (scope-guard already sees every write — it gains
the routing lookup; a Stop-gate check demands the review artifact for gate-bound transitions);
(3) the review/answer artifact templates in docs/templates/; (4) the per-sector drift gauges.
Flag-less: discipline is not a feature toggle. Enable act = ratifying MAP.md + the five briefs —
owner-by-hand, the D6 path's first execution.

## 4. Math carried explicitly

Mostly N/A (an organizational design). Two formal pins: routing is a MONOTONE map (more touched
surface ⇒ superset of experts — never fewer eyes on a bigger change; carried as a property test
on the MAP resolver); coverage accounting is the integrator's named-not-dropped law applied to
review (Σ examined + Σ declared-out-of-scope = the artifact's surface — a gap is a visible
verdict, not an omission).

## 5. Risks

- **R1 brief staleness** → D5 drift gauges + `grounded_at` visibility; the reconciliation sweep
  audits the auditors (the outer loop).
- **R2 circularity** (an expert's review changes the sector that defines it) → briefs re-learn
  from reality, not from their own reviews; the sweep is the independent check.
- **R3 review-fatigue / rubber-stamping** → tiered depth (D3) keeps cheap things cheap;
  the misses ledger makes a rubber-stamped miss PERMANENTLY visible in-sector.
- **R4 boundary gaps** (a surface no sector owns) → the MAP resolver's default is
  harness/workflow + a finding demanding a MAP amendment — unowned is loud, not silent.
- **R5 cost creep** → conformance tier is checklist-cheap; full panels reserve for gates +
  invariant-adjacent touches; budget-gated like all delegation.

## 6. Parked decisions

| PD | Decision | Default recorded | Re-entry condition |
|---|---|---|---|
| PD-1 | expert-to-expert direct dialogue | routed via orchestrator in v1 | a recurring dispute class the routing demonstrably serves badly |
| PD-2 | oracle answers as a queryable store | answers are findings-adjacent files | answer reuse becomes frequent enough to want retrieval |
| PD-3 | automated challenge generation (adversary spawns challenges on a cadence) | manual/owner-triggered challenges only | the T3b logic-test harness lands and can drive it |
| PD-4 | sector-scoped semantic lenses | glob/path lenses until then | the membership store (dn-vector-membership-store) ratifies + rebuilds |

## 7. Acceptance shape (for graduation)

(a) MAP.md ratified + resolver with the monotonicity property test. (b) Five briefs bootstrapped,
each itself panel-reviewed (the gate reviews its own institution — D6's validate step). (c) A
touched-surface simulation: a synthetic diff spanning core+scheduler selects exactly {core,
systems (+security if hook-adjacent)} — routing is mechanical and tested. (d) One full gated
artifact traverses the chain end-to-end: touch → reviews (named coverage, a dissent preserved) →
merged report → owner reads verdicts only. (e) An oracle answer round-trip: question → grounded
answer artifact → a successful challenge → the brief visibly updates. (f) The community exhaust
check: the review session's transcript lands in L1 and its artifacts in the code lane —
ingested/tracked/attested demonstrated, not asserted.
