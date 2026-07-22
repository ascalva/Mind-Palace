---
type: design-note
id: dn-integrator-densification
track: code-ingest
status: draft            # draft → ratified → superseded.  draft→ratified is an OWNER-ONLY hand edit.
created: 2026-07-22
updated: 2026-07-22
links:
  - docs/findings/finding-0151.md                      # the warrant — "a proper integrator design pass"
  - docs/findings/finding-0163.md                      # history embedded — the D-side substrate (bp-099)
  - docs/findings/finding-0164.md                      # the corpus-wide keep-and-link ruling (D8)
  - docs/findings/finding-0111.md                      # the no-fan-out boundary this design honors
  - docs/findings/finding-0141.md                      # C-fiber thinness — the defect being closed
  - docs/design-notes/temporal-code-corpus.md          # bp-099: commit_diffs + version nodes (consumed here)
  - docs/design-notes/agent-taxonomy.md                # §2.5 the integrator/witness law
  - core/integrator.py                                 # E_proven — UNTOUCHED; its docstring defers the composition here
  - core/stores/causal_edges.py                        # the proven-edge store — UNTOUCHED
supersedes: null         # extends; nothing superseded. Discharges core/integrator.py's deferred "Δ's ComposedGraph job" and restores bp-093's pulled PD-J consumer (code_origin).
warrant: docs/findings/finding-0151.md
---

# Design note — integrator densification: the composed causal graph (C ∘ D)

> The causal chain the system exists to represent: **conversation → commit → code change**, where
> the code change IS a supersession edge `blob(v) → blob(v+1)` (dn-temporal-code-corpus D5). The
> proven integrator (bp-071) witnesses the first hop sparsely (78 commit-anchored of 4,160 edges);
> bp-099 builds the second hop's substrate (`commit_diffs`, version nodes). This note designs the
> composition — dense, version-grain, honestly graded.

## 0. Provenance & mode

Fable design pass (owner-directed, 2026-07-22 session-43), **warrant finding-0151** (owner ruling
2026-07-21: PD-J pulled, shipping thin rejected; a proper design pass required; it completes the
code-ingest program). Grounded live this session: `core/integrator.py` (the witness law + the
explicit deferral "Composing action→commit with commit→file is Δ's `ComposedGraph` job, not this
agent's"), `core/stores/causal_edges.py` (edge schema; `pair_cut_sha` only on commit edges),
`core/stores/chat_events.py` (L1 = structural `(session_id, ord, kind, ref)` rows), and
dn-temporal-code-corpus / bp-099 (in build this sitting: `commit_diffs`, `current`-flagged version
nodes, `supersession_chains`).

## 1. Objective

Answer **"which conversation wrote this code version?"** densely and honestly:

1. A **composed-edge layer** `E_composed`: `(session, event) → (commit, path, old_blob → new_blob)`
   — turn-grain where evidence permits, session-grain otherwise, every edge carrying an explicit
   **evidence grade**. The existing `E_proven` (bp-071) is **untouched** — its witness law (one
   edge = the deterministic image of one L1 record; no time-join, no inference) stays inviolate.
2. A **prospective blob-tag sensor**: at write time, record the post-write blob sha — making
   future authorship *exact* (grade TAGGED) instead of inferred.
3. The **`code_origin` reader restored** (bp-093's pulled PD-J consumer): blob → authoring
   sessions, grade-sorted — the deskcheck query.
4. **Coverage gauges**: the fraction of supersession edges with a witnessed author, by grade —
   the densification metric (baseline: 78/4,160 edges commit-anchored; supersession coverage ~0).

### 1.2 Out of scope (non-goals — read deliberately at ratification)

- **Any change to `core/integrator.py` / `causal_edges.py` semantics.** E_proven is correct as
  built; density was never its job. The composer is a NEW role beside it. `[ESTABLISHED — its
  docstring defers exactly this composition]`
- **Any model/LLM involvement.** The composer is deterministic and model-free, like every
  integrator-family agent (dn-agent-taxonomy §2.5).
- **Notes/chat/curated lane temporalization** — D8 states the general law; each lane's
  instantiation is its own design (finding-0164 routes there). Code-lane only here.
- **Retrospective content corroboration** (matching a turn's inserted strings against historical
  blob diffs to upgrade old WINDOWED edges) — PD-1, parked with re-entry. `[INFERENCE — high cost,
  modest yield over the tag+window pair; nothing blocks on it]`
- **Guessing at unwitnessed changes.** An owner hand-edit or untracked-session commit stays
  UNWITNESSED forever — honesty outranks coverage. No fabricated authorship, ever.
- **Cross-repo; non-code artifacts as composition endpoints** (docs/plans keep their existing
  file/doc edges).

## 2. Decisions

### D0 — Two layers, one law: E_proven stays pure; E_composed is born graded

The bp-071 invariant ("NO time-join, NO inference") is a feature, not a limitation — it makes
E_proven re-derivable ground truth. Densification therefore lands as a **separate store and a
separate agent**: the **composer** (the "Δ / ComposedGraph" role the integrator's docstring
reserves). The composer MAY time-join — but every edge it mints **declares its evidence grade**,
and the grade vocabulary makes PROVEN structurally unmintable by it (D1). No consumer can mistake
an inferred edge for a witnessed one; the firewall is the schema, not a convention. `[DERIVED]`

### D1 — The evidence-grade lattice

Every composed edge carries exactly one grade; the set is ordered (strongest first):

| grade | meaning | evidence |
|---|---|---|
| `ANCHORED` | the turn itself named the commit | an E_proven commit edge (pair_cut_sha) whose commit's diff contains this (path, old→new) — composition of two witnessed facts, zero inference |
| `TAGGED` | the write's post-state blob equals the committed blob | a write-tag row `(session, turn, path, blob_sha)` with `blob_sha == new_blob` (D3) — exact, content-grain |
| `WINDOWED_UNIQUE` | exactly one session wrote the path in the commit window | temporal join (D2), single candidate |
| `WINDOWED_CONTESTED` | ≥2 sessions wrote the path in the window | temporal join; ALL candidates minted, each marked contested (no arbitration — honesty over tidiness) |
| `UNWITNESSED` | no observed write in the window | not an edge — a GAP row in the gauge (owner hand edit / untracked session). Never fabricated. |

`ANCHORED` and `TAGGED` are compositions of witnessed facts (deterministic record images on both
hops) — they are as strong as E_proven without being stored as E_proven. `WINDOWED_*` is honest
inference and says so. Consumers filter by minimum grade. `[DERIVED]`

### D2 — The temporal window join (the dense fallback)

For each path `p`, bp-099's `commit_diffs` yields the commit chain `k₀ < k₁ < … < kₙ` touching
`p` (first-parent order). Define the authorship window
**`W(p, kᵢ) = ( t(kᵢ₋₁), t(kᵢ) ]`** (commit timestamps; `t(k₋₁) = −∞`). An L1 write event
`w = (session s, ord o, path p, time τ)` is a **candidate author** of the supersession edge
`(kᵢ, p, old→new)` iff `τ ∈ W(p, kᵢ)`. The author set
`A(p, kᵢ) = { (s,o) : candidate }` determines the grade: `|A|=1 → WINDOWED_UNIQUE`,
`|A|>1 → WINDOWED_CONTESTED` (all minted), `|A|=0 → UNWITNESSED` (gauge gap).

- **Timestamp source:** commit side — the ledger's commit time (local commits, one machine; skew
  is seconds against windows of minutes-to-days — acceptable, recorded as risk R1). Event side —
  the transcript timestamp. **Code does not settle** whether the L1 `chat_events` schema carries
  `ts` today (column list not fully read); if absent, the L1 projector gains it — the store is a
  `reset_targets()` wipe+re-projection target, so this is a re-projection, not a migration.
  Builder settles at §2-manifest time.
- **Determinism:** the join is a pure function of `(L1, commit_diffs, ledger)` — re-runnable,
  idempotent (edge identity is content-derived from `(session, ord, commit, path, new_blob,
  grade)`), monotone under append (new events/commits only add edges; no re-grading of ANCHORED/
  TAGGED by later data; a WINDOWED edge may gain contested siblings — grades never silently
  upgrade). `[DERIVED]`

### D3 — Prospective blob-tagging: the write-tag sensor (finding-0151's "blob-tagged writes")

From now forward, authorship should be **exact**, not inferred. At write time, a PostToolUse hook
on the file-writing tools (Edit/Write/NotebookEdit) computes `git hash-object <file>` on the
written file (repo-tracked `.py` first; cheap, local, no network) and APPENDS one structural row —
`{session_id, turn, path, blob_sha, ts}` — to **`data/write_tags/<session_id>.jsonl`**
(O_APPEND, one shard per session: multi-process-safe under parallel builders by construction; the
transcript-sweep pattern the chat sensor already uses). The composer sweeps shards incrementally.
When a commit lands `new_blob = B` for `p` and a tag row has `blob_sha = B, path = p, ts ≤ t(k)`:
grade **TAGGED**, turn-grain, content-exact.

- **Plane discipline:** structural facts only (sha/path/ids — never content), OBSERVED-side
  sensor exhaust; the composer is its sole reader; the daemon never writes it. Rows are tiny;
  growth is per-edit, prunable by session with its transcript (PD-4).
- **Coverage honesty:** Bash-mediated writes (sed, scripts) and owner edits are not hooked — they
  remain WINDOWED/UNWITNESSED. Recorded, not hidden (the gauge splits by grade). Hook is
  fail-open: a hash failure loses a tag, never blocks a write. `[DERIVED]`

### D4 — The composed-edge store (new; INTERPRETED-plane; re-derivable)

New sibling store `core/stores/composed_edges.py` (`data/composed_edges.sqlite`, the
`chat_events`/`causal_edges` store convention): one row =
`(edge_id, commit_sha, path, old_blob, new_blob, session_id, event_order NULLABLE, grade,
evidence TEXT, ts)` — `evidence` is a structural pointer (the proven edge_id / tag shard+line /
window bounds), NEVER content. Derived + re-derivable from retained inputs ⇒ joins
`reset_targets()` and rebuilds by re-composition. Provenance: INTERPRETED (minted only by the
composer; no provenance parameter — non-launderable), ∉ MIRROR_READABLE. `[DERIVED — the sibling
store conventions, verbatim]`

### D5 — The composer agent (the Δ role, claimed)

Model-free, deterministic, born-scoped exactly like the integrator
(`core/kernel/agent_scope.py` pattern): **reads** L1 (`ChatEventStore`), E_proven
(`CausalEdgeStore`), `commit_diffs` + ledger (bp-099 / snapshots db), write-tag shards; **writes**
composed edges only. Registered as its own scheduler KIND (`compose`) at BACKGROUND on the pinned
tier, riding the integrate cadence, **sliced with a per-pass cap** (`compose_max_per_pass`, the
`integrate_max_per_pass` precedent) — the finding-0165 lesson applied at birth: no hours-long
queue-starving pass; catch-up over full history proceeds in slices across ticks. Scope conformance
asserted at build (`assert_conforms`). `[DERIVED]`

### D6 — `code_origin` restored (the PD-J consumer, un-pulled)

The reader bp-093 pulled ships against the composed layer: `code_origin(blob_sha) → [(session,
turn?, commit, grade, ts), …]` grade-sorted; and per path, the full authored timeline
`version chain × authors`. This is the **deskcheck query**: for a blob authored in a live session
after the hook ships, it must return that session at grade TAGGED (or ANCHORED via the session's
own commit event). Home: eval/ or the ops read surface — settled at graduation (it is a reader,
not core machinery).

### D7 — Gauges (the honesty instrument)

Per-grade counts over all supersession edges: `coverage(g) = |edges ≥ g| / |commit_diffs rows|`,
plus the UNWITNESSED gap count. Baselines recorded at first composition (expected: ANCHORED ≈ the
78-edge lineage; TAGGED = 0 until the hook ships; WINDOWED fills most of history). The gauge is
the plan's acceptance instrument and the standing drift metric thereafter. Extends the existing
pure-gauge convention (`core/kernel/integrator_math.py`). `[DERIVED]`

### D8 — The general law (finding-0164, stated once)

The pattern instantiated here is corpus-wide: **version nodes (keep-and-link) + supersession
edges (a ledger-derived chain) + witnessed authorship (graded composition)**. The notes lane has
the same three ingredients waiting (immutable rawstore = the version nodes' source; the vault
catalog's `(source_path, digest)` lineage = the ledger; the same composer pattern over note
edits). Each lane instantiates in its own note per finding-0164 — this section is the template
they conform to, not their design.

## 3. Wiring & enablement (required §)

**How it wires:** the composer registers as `compose` in `build_components` handlers +
housekeeping enqueue (the `integrate` sibling, sliced per D5); the write-tag hook installs in
`.claude/settings.json` PostToolUse (repo-scoped, fail-open); `code_origin` ships as a reader with
a CLI/eval surface. **What it takes to flip on: nothing** — flag-less per the standing rulings
(finding-0159/0161: a capability worth building ships wired-ON; gating-off is a not-yet, and
there is no not-yet here). First housekeeping after deploy begins sliced catch-up composition over
existing history; the hook tags from its first installed session onward.

## 4. Math carried explicitly

Per path, `commit_diffs` rows form a chain (first-parent total order); windows `W(p, kᵢ)`
partition `(−∞, t(kₙ)]` — every write event falls in **exactly one** window per path (no double
attribution; the partition property is the correctness core and gets a property test). The grade
set is totally ordered (D1 table order); `coverage(g)` is antitone in `g` (asserted). Composition
is associative fact-joining, not path search: `E_composed ⊆ L1 × commit_diffs`, each element
tagged with its witness route; `E_proven` embeds injectively into the ANCHORED stratum
(`edge ↦ (edge, diff-row)` for each diff row of its commit — note: this is the ONE place a commit
fans out to its diff set, and it is legitimate here precisely because `commit_diffs` now EXISTS as
witnessed data (bp-099) rather than an inferred tree-walk; finding-0111's boundary — "the ledger
holds the tree, not the diff" — is discharged by capturing the diff, not by inferring it).
Idempotency: `compose(compose(X)) = compose(X)` under content-derived edge ids. Monotonicity:
append-only inputs ⇒ append-only edges (grades immutable once minted; contested-set growth adds
rows, never mutates).

## 5. Risks

- **R1 clock skew** (transcript vs commit clocks): same machine, seconds vs minute-scale windows;
  a boundary write can mis-window — mitigated by TAGGED (exact) going forward; recorded, accepted.
- **R2 contested inflation** in parallel-builder eras (multiple sessions, one path, one window):
  by design — contested edges are the honest answer; the gauge tracks the contested fraction.
- **R3 hook gaps** (Bash writes, owner edits): permanent WINDOWED/UNWITNESSED strata — the gauge
  makes the gap visible instead of papering it.
- **R4 L1 `ts` presence** unsettled (D2) — builder settles; worst case one re-projection.
- **R5 queue pressure**: sliced by birth (D5); finding-0165's direction-1 applied.

## 6. Parked decisions

| PD | Decision | Default recorded | Re-entry condition |
|---|---|---|---|
| PD-1 | retrospective content corroboration of historical WINDOWED edges | not built | a consumer needs historical turn-grain exactness the window join can't give |
| PD-2 | contested-edge arbitration/weighting | none — all candidates minted equal | a consumer needs a single-author answer and accepts a stated heuristic |
| PD-3 | hooking Bash-mediated writes | not hooked | tag coverage gauge shows Bash writes dominate the WINDOWED stratum |
| PD-4 | write-tag shard retention | keep (tiny) | disk pressure; prune-with-transcript policy then |

## 7. Acceptance shape (for graduation)

(a) The window-partition property test (every event exactly one window per path). (b) Composer
determinism + idempotency on a fixture (two runs, identical edge sets). (c) The E_proven
embedding: every pair_cut edge whose commit has diff rows yields ANCHORED edges, count =
Σ diff-rows. (d) The hook round-trip: an Edit in a test harness produces a tag row whose sha
equals the committed blob → TAGGED edge. (e) `code_origin` end-to-end on a real blob from this
repo's history. (f) Gauge baseline recorded and ≥ the 78-edge ANCHORED floor. Graduation splits
session-sized plans (likely: composer+store+window-join; hook+tags+TAGGED; code_origin+gauges) —
decided at /graduate against bp-099's landed surface.

## 8. Sequencing

**Hard dependency: bp-099 sealed + deployed** (commit_diffs + version nodes are this design's
inputs). Then ratify → graduate → build. The write-tag hook (D3) has no dependency and could ship
early, accumulating tags while the rest builds — graduation may order it first for exactly that
reason (every day without tags is a day of history capped at WINDOWED).
