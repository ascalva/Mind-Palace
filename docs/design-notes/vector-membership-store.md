---
type: design-note
id: dn-vector-membership-store
track: code-ingest
status: draft            # draft → ratified → superseded.  draft→ratified is an OWNER-ONLY hand edit.
created: 2026-07-23
updated: 2026-07-23
links:
  - docs/findings/finding-0168.md                      # the warrant — four owner rulings, verbatim
  - docs/findings/finding-0167.md                      # the interim reuse port this subsumes
  - docs/findings/finding-0164.md                      # corpus-wide keep-and-link (notes-lane adoption path)
  - docs/design-notes/temporal-code-corpus.md          # partially superseded (D1/D2 row model — see §6)
  - docs/design-notes/integrator-densification.md      # consumer: slot-lineage edges join the composed graph
  - core/stores/sourceset.py                           # the axiom this completes (overlapping sets)
supersedes: dn-temporal-code-corpus D1/D2 row model (digest-stamped duplicated rows)   # PARTIAL — keep-and-link semantics, backfill, commit_diffs, current-view default ALL STAND
warrant: docs/findings/finding-0168.md
adversarial_review: OWED               # the new gate (2026-07-23 ruling): expert panel (core+systems+math) BEFORE ratification
---

# Design note — the vector membership store

> A point is a point — geometry, assertion-free. Meaning lives in **membership** (who contains
> it), history in **lineage** (which occupancy chains pass through it). The vector plane is a
> growing, append-only dictionary of idea-atoms; the corpus is the usage record over it. Git's
> content-addressed model, one level down: `digest` = blob sha at file grain, `content_hash` =
> chunk sha at idea grain.

## 0. Provenance & mode

Fable design pass, in-session (owner-directed, 2026-07-23). Warrant **finding-0168** — four owner
rulings, one thread: (1) vectors are the versioned entities, stored once; (2) succession is a
property of the `(path, slot)` occupancy chain, never of the vector; (3) the plane is
append-only, no machinery deletes; (4) membership cardinality n(v) and its distribution are
first-class observables. Grounded against the live bp-099 store model (whose duplication this
removes) and the shipped `commit_diffs`/chains machinery (which stands unchanged).

## 1. Objective

Replace the per-version duplicated row model with:

1. **One vector row per distinct idea-atom** `(layer, content_hash)` — deduplicated across
   versions, reverts, and files. Append-only: a vector, once landed, is permanent.
2. **A membership relation** carrying all occupancy: which `(path, blob_sha)` versions contain
   which atoms, at which slot/lines, and whether that occupancy is current.
3. **Slot-lineage supersession** `(path, slot): hash_i → hash_{i+1}` — derived, never stored as a
   second truth — giving the integrator's composed graph its finest D-fiber.
4. **The frequency plane**: n(v) counts and the corpus histogram as standing gauges.

Embedding reuse (finding-0167) falls out: landing a version embeds only atoms absent from the
plane. A revert or copy-paste costs zero geometry — metadata only.

### 1.2 Out of scope (non-goals — read deliberately at ratification)

- **No change to keep-and-link semantics, the backfill, `commit_diffs`, current-view default
  retrieval, or the flag-less posture** — dn-temporal-code-corpus stands except its row model.
- **The NOTES lane** — adoption is intended (finding-0164's law; one membership machinery) but
  designed when the notes lane temporalizes; this note builds the code lane. PD-2.
- **No stored edge table for slot lineage** — edges stay derived from membership + `commit_diffs`
  (single source of truth; the dn-code-ingest §436-447 doctrine, kept).
- **No ANN/index tuning, no embedder change, no pruning** — append-only makes pruning a
  non-feature; purge (below) is the only removal and it is an owner act, not policy.
- **No retroactive re-chunking** — atoms are whatever the (unchanged) chunkers emit.

## 2. Decisions

### D1 — The split: geometry / reference / history

Three stores, one truth each:

- **`vectors` (LanceDB)** — one row per `(layer, content_hash)`:
  `id = "{layer}:{content_hash}"`, `layer`, `text`, `vector`, `current_any` (denormalized: does
  ANY current membership contain this atom — the cheap default-search prefilter), `tombstoned`
  (purge only). **Sheds `source_path`/`digest`/`qualname`/`line_*`/`chunk_index`** — those are
  occupancy properties, not atom properties (the same text in two files has different
  coordinates; stamping them on the row was the duplication).
- **`memberships` (SQLite, beside the vault catalog)** — one row per occupancy:
  `(content_id, path, blob_sha, slot, line_start, line_end, chunk_index, current, tombstoned)`.
  `slot` = qualname for L0a/L1 (stable across versions), `''` for L0b (windows are slotless —
  membership-only, honestly chainless). A version's projection = the fiber
  `M(path, blob_sha) = {content_id, …}`.
- **History** — derived: occupancy chains per `(path, slot)` from memberships ordered by the
  blob chain (`commit_diffs`, already captured); supersession edge where consecutive occupants'
  hashes differ. Materializable as a view; never a second store.

Provenance is unchanged (CODE minted structurally; MIRROR firewall untouched — code atoms remain
∉ MIRROR_READABLE regardless of representation).

### D2 — Landing a version (the write path)

`land(path, blob_sha, chunks)`: (1) compute `content_hash` per chunk; (2) **insert only the atoms
absent from the plane** (the embed step — everything else is reuse by construction); (3) write
the membership fiber for `(path, blob_sha)` with `current = (blob == HEAD blob)`; (4) flip the
prior version's memberships `current=false` (supersession is a MEMBERSHIP flip — no vector row is
touched, ever); (5) maintain `current_any` on atoms whose current-membership count crossed 0↔1.
Write amplification: an edit = ≤1 vector insert + one membership fiber + flips. Idempotent:
re-landing an existing `(path, blob)` fiber is a no-op (fiber equality).

### D3 — Retrieval (the read path)

ANN search over `vectors` (prefilter `current_any AND NOT tombstoned` by default;
`include_superseded=True` lifts it) → top-k atoms → **join memberships** to resolve occupancies
`(path, blob, slot, lines, current)`. One atom may resolve to several occupancies — that is the
FEATURE: a hit natively answers "this idea lives in versions v3–v7 of X and also in Y" (the
atom's reach). Default consumers see current occupancies only — flat retrieval behavior
preserved. `sourceset`'s group-by-digest becomes the membership fiber lookup — the axiom
completed: source object = a SET of atoms; sets overlap; shared elements stored once.

### D4 — Fork/join semantics (ruled; the formal pin)

**Supersession edges live on slot-lineages, never on vectors.** A vector shared by two files =
one atom, two memberships. An edit in one file mints an edge on ITS `(path, slot)` chain and
swaps ITS membership; the other file's chain passes through the original untouched. Forks,
parallel same-edits (same endpoints, distinct chains), and convergence (a later copy-paste
re-shares the atom) are all **graph facts** — two lineages intersecting at a node — never stored
claims. Edge identity: `(path, slot, old_hash → new_hash, at blob transition)`.

### D5 — Append-only + the purge exception (ruled)

No machinery delete exists in the API surface (the store exposes no vector delete; supersession
flips memberships). The ONE removal is **purge** (finding-0164, owner-gated, privacy outranks
lineage): delete the vector row, set `tombstoned` on its memberships — a recorded hole, never
silent. Near-moot for CODE (public in git); load-bearing when notes adopt this model.

### D6 — The frequency plane (ruled)

`n(v)` = COUNT over memberships (current-cut or lifetime — both defined, both cheap). Standing
gauge: the **n(v) histogram** per lane and over time — Zipf-shape conformance is a falsifiable
corpus property (deviation localizes something real: boilerplate consolidation, vocabulary flux);
drift across cuts = the common language consolidating/diversifying. Consumers: IDF-style
retrieval weighting (or its deliberate inverse — idiolect mining), code-idiom detection,
hub-degree for the dreamer, fork-in-high-n as a signal event. Home: an ops/eval gauge beside the
drift-gauge family; joins the T4 limits work.

### D7 — Migration: one rebuild, cheaper than what it replaces

Vectors are derived and regenerable (§8 doctrine; `reset` exists). The migration is ONE
deliberate rebuild: reset the code rows → re-derive all ledger versions → embed **distinct atoms
only** (strictly fewer embeds than the duplicated backfill: the atom set ≤ Σ per-version chunks)
→ write membership fibers. Owner-visible (`palace code-rebuild`, the code-seed shape), with the
incompleteness-probe pattern for auto-catch-up thereafter. Note rows (prose) migrate vacuously
(their `current=true` semantics unchanged) or stay on the old path until PD-2 — builder settles
which is mechanically smaller.

### D8 — Crash consistency (the one real systems risk)

Order of writes: vector inserts FIRST (append-only, unreferenced-is-harmless), membership fiber
SECOND (transactional in SQLite), `current_any` maintenance LAST (re-derivable from memberships —
a repair pass exists). An orphan atom (inserted, fiber write crashed) is dormant geometry — the
idempotent re-land repairs; nothing dangles by reference. Membership SQLite is the reference
truth; `current_any` is a cache with a rebuild path.

## 3. Wiring & enablement (required §)

Flag-less (the standing rulings): this is the store's semantics, not a feature. Ships as the code
lane's store vNext; `sync()`/`backfill()` land through D2 unchanged in their triggers (the bp-098
wiring — housekeeping gate, `code-seed`, `code-backfill`, the catch-up probe — all stand). The
enable act is the D7 rebuild: `palace code-rebuild`, owner-visible, once; the probe auto-repairs
thereafter. The n(v) histogram gauge registers beside the existing gauges (read-only, cheap).

## 4. Math carried explicitly

Let V = atoms (append-only: V(t) monotone ↑), O = occupancies. Membership M ⊆ V × O; a version is
the fiber M(path, blob); `n(v, t) = |{o ∈ M(v) : current_t(o)}|`, lifetime n(v) = |M(v)| ≥ 1 by
construction (an atom enters via some landing). Per `(path, slot)`: occupants form a total order
(the blob chain, first-parent — bp-099's chains); supersession = covering relations; corpus-wide
the slot-lineage structure is a forest of chains whose nodes are SHARED (viewed on atoms: a DAG —
chains intersecting at common atoms; forks/joins are exactly the intersections). Invariants to
carry as tests: per-slot `|edges| = |occupants| − 1`; Σ fiber sizes = |M|; `current_any(v) ⇔
n(v,t) > 0`; append-only ⇒ no test may ever observe |V| decrease (except across a logged purge).
Histogram: the rank-frequency plot of lifetime n(v); Zipf conformance checked in T2/T4, not
assumed.

## 5. Risks

- **R1 crash consistency** (D8): mitigated by write order + repair pass; property test required.
- **R2 join latency on the read path**: top-k membership joins are k×small SQLite lookups;
  measure in T4 before optimizing; `current_any` prefilter keeps the ANN set lean.
- **R3 `current_any` drift** (cache vs truth): the repair pass + a ratchet comparing flag vs
  membership counts on a sample.
- **R4 L0b slotlessness**: windows carry no chains — accepted and honest; L0a/L1 carry the
  lineage weight (they are the semantic layers; L0b is raw-context capture).
- **R5 migration scope creep**: the rebuild touches only code rows; note rows explicitly parked
  (PD-2) — the builder must not "helpfully" migrate prose.

## 6. Supersession declaration (for the owner's ratification hand)

Partially supersedes **dn-temporal-code-corpus**: D1/D2's ROW MODEL (digest-stamped rows
duplicated per version; `current` on vector rows) → this note's atom+membership split. Everything
else there STANDS: keep-and-link semantics, history embedded, the backfill machinery,
`commit_diffs`, current-view default, flag-less wiring. finding-0167's mechanical port is
subsumed (do not build it separately if this ratifies first).

## 7. Parked decisions

| PD | Decision | Default recorded | Re-entry condition |
|---|---|---|---|
| PD-1 | cross-file dedup scope | RULED IN (owner) — one atom, n memberships, fork semantics | — (closed at capture) |
| PD-2 | notes-lane adoption | code-first; prose rows untouched by the D7 rebuild | notes keep-and-link lands (finding-0164) |
| PD-3 | materialized slot-edge view | derived on read | a consumer needs edge queries at a rate joins can't serve |
| PD-4 | IDF-weighted retrieval | gauge only, no ranking change | a retrieval-quality experiment (T4) shows lift |

## 8. Acceptance shape (for graduation)

(a) Dedup: land two versions sharing k atoms → vector rows = distinct atoms, memberships = both
fibers; a REVERT lands zero vectors. (b) Fork: two files share an atom; edit one → one new atom,
one membership swap, the other file's fiber untouched; both lineages traverse the shared node.
(c) Append-only: no code path can delete a vector (API-level test) except purge, which tombstones
memberships visibly. (d) Retrieval: default search returns only current occupancies; a shared
atom resolves to all its current homes. (e) D8 property test: crash between vector insert and
fiber write → re-land repairs, no dangling reference. (f) The §4 invariants as tests. (g) The
histogram gauge renders per-lane. Graduation: likely two session-plans (store+land+read;
rebuild+gauges+probe) — split at /graduate against the then-current tree.
