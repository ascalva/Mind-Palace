---
type: finding
id: finding-0164
status: routed           # open → routed → resolved | promoted
created: 2026-07-22
updated: 2026-07-22
links:
  - docs/design-notes/temporal-code-corpus.md          # the code-lane correction this generalizes (PD-3 → ruled)
  - docs/findings/finding-0163.md                      # the principle: no causal edges without represented history
  - docs/findings/finding-0151.md                      # the integrator pass that consumes the edges
  - core/ingest/index.py                               # index_amendment — notes delete+replace
  - core/ingest/sync.py                                # vault tombstone drops derived rows
  - core/ingest/dialogue.py                            # chat delete-by-digest idiom
  - core/ingest/curated.py                             # curated delete-by-digest idiom
  - core/ingest/founding.py                            # same idiom
ftype: direction         # owner ruling — corpus-wide ingest semantics
origin_plan: orchestrator
route: orchestrator      # audit + per-lane design lands in the temporal/integrator design pass
resolution: null
---

# Owner ruling: EVERY ingest path must keep-and-link (supersession edges), never delete-and-replace

## What

Owner ruling (2026-07-22, extending finding-0163 beyond the code lane): **all ingest paths must
create supersession edges — keep and link superseded versions — not delete and replace them.** The
temporal-graph model ("a graph that evolves over time; causal edges need represented history") is
corpus-wide, not code-specific. This elevates dn-temporal-code-corpus PD-3 ("note-corpus
temporalization — parked") from an open question to a ruled direction: the remaining question is
per-lane design, not whether.

## The audit surface (grounded sweep, 2026-07-22 — delete+replace is the pervasive idiom)

| Lane | Site | Today | Temporal gap |
|---|---|---|---|
| Notes (vault) | `index.py:87` `index_amendment` → `delete_source(path)`; `sync.py:143` tombstone → `delete_source` | old projection DESTROYED on every note edit; tombstone drops derived rows | raw store IS immutable+content-addressed (§8) — history recoverable, like the code ledger; the semantic store retains nothing and no version chain is exposed |
| Chat (dialogue) | `dialogue.py:62` `delete(digest=…)` | re-index idiom | AUDIT: if a grown session re-ingests under a NEW digest, do prior-version rows orphan/delete? distinguish same-digest idempotency (harmless) from version destruction |
| Curated | `curated.py:61` `delete(digest=…)` | same idiom | same distinction owed |
| Founding | `founding.py:109` `delete(digest=…)` | same idiom (curated idiom, by comment) | same |
| Code | `code_corpus.py:256,272` | delete+replace | **being fixed NOW — bp-099** (the template the other lanes follow) |
| Purge | `core/ingest/purge.py` | deliberate irreversible removal | **EXEMPT BY DESIGN** — owner-gated privacy destruction (tombstone-first, raw removed). Keep-and-link is the default; purge is the one legitimate delete and must remain one |

## Why it matters

Same argument as finding-0163, corpus-wide: causal edges (conversation → artifact-change) cannot
exist for a lane whose history is destroyed at ingest. Notes are the sharpest case — the owner's
own thought evolution ("how did this idea change?") is exactly the self-map's purpose, the raw
history already exists (immutable raw store), and the semantic layer throws the linkage away on
every edit. The audit must also preserve two disciplines while correcting this: (a) same-digest
re-index idempotency is NOT version destruction — don't "fix" what isn't broken; (b) purge stays —
temporal retention must never make owner-gated deletion impossible (privacy outranks lineage).

## Re-entry condition / next step

Lands in the temporal/integrator design pass (finding-0151's Fable pass, which finding-0163
founded): per-lane audit → per-lane keep-and-link design (the bp-099 `current`-flag + chains
pattern is the template; notes likely key on the vault catalog's `(source_path, digest)` lineage
the way code keys on the ledger) → graduate. Until then: bp-099 fixes code; the other lanes keep
today's semantics — every note edit still discards its superseded projection (recoverable from
raw, so nothing is permanently lost; the correction should not dawdle for that reason alone).

## Routing

`direction`, owner-ruled → **orchestrator → the temporal/integrator design pass** (one pass owns
the corpus-wide model: code done by bp-099, notes/chat/curated designed there; supersedes
dn-temporal-code-corpus PD-3's code-only default when ratified).
