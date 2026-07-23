---
type: finding
id: finding-0167
status: routed
created: 2026-07-23
updated: 2026-07-23
links:
  - core/ingest/code_corpus.py                         # _embed_and_land — embeds ALL chunks of a changed version
  - core/ingest/index.py                               # index_amendment — the reuse-unchanged discipline to port
  - core/stores/vectorstore.py                         # supersede_source — O(versions×chunks) re-land per flip
  - docs/design-notes/temporal-code-corpus.md          # the store model this optimizes within (D1/D2 unchanged)
ftype: discovery         # efficiency gap, owner-raised ("as efficient as possible"); mechanical fix
origin_plan: orchestrator
route: orchestrator      # small mechanical plan, or rides the next code-lane build wave
resolution: null
---

# Code-lane embedding is file-grain, not chunk-grain — port `index_amendment`'s reuse-unchanged discipline

## What (owner question 2026-07-23: "if only one line changed, only that vector should re-embed")

Grounded: the temporal code corpus is efficient at FILE grain (unchanged blob = zero embeds; the
supersession flip = zero embeds; backfill skips present versions) but NOT at CHUNK grain — on a
changed blob, `_embed_and_land` embeds **every** chunk of the new version
(`embed_documents([c.text for c in chunks])`, no reuse), even though ~most chunks carry a
`content_hash` identical to the prior version's rows sitting in the store with vectors. The NOTE
lane already has the exact discipline (`index_amendment`, `core/ingest/index.py:61-82`: prior rows
→ `vec_by_hash` → embed only new hashes); the code lane never received the port — a DRY gap
([[owner-dry-strictness]]).

Per-layer edit-stability of a one-line change (what reuse recovers):
- **L0a** (per-symbol): edit-STABLE — chunk text is header (`# path:qualname(sig)`) + the symbol's
  own lines; line coords are row COLUMNS, not embedded text; only the touched symbol re-hashes.
  ~all other symbols reusable. (Verified in `_l0a_chunks` — no line numbers in text.)
- **L0b** (windows): structurally UNSTABLE past the edit point (windows shift) — those re-embeds
  are legitimate; reuse-by-hash automatically recovers whatever happens to align.
- **L1** (prose view): CHECK AT FIX TIME whether comment items embed their line number in the
  chunk text (`{path}:{qualname or line}` headers) — if so, line drift spuriously re-hashes
  downstream prose chunks; coords are already columns and should not also live in embedded text.

Bonus from keep-and-link (D2): the reuse lookup can span ALL retained versions' rows — a REVERTED
line re-finds its old vector for free. History makes reuse better, not worse.

Secondary: `supersede_source` re-lands every version's rows of the path per flip (the id-collision
workaround) — zero embeds but O(version_depth × chunks) I/O per change; fine at ~6 versions/file
today, deserves a bound (e.g., flip only rows where current=true — needs digest-scoped targeting,
not id-scoped) when depth grows.

## Why it matters

Housekeeping-cadence embeds scale with edit velocity; at parallel-builder pace the waste is ~10×
per changed file (absolute cost small on the local embedder, but the owner's standing bar is "as
efficient as possible", and the fix is a port, not an invention). Also keeps the embedder budget
predictable as history and velocity grow.

## Re-entry / next step

A small mechanical plan (or a rider on the next code-lane wave): (1) port `vec_by_hash` reuse into
`_embed_and_land` (lookup across the path's retained rows, all versions); (2) settle the L1
line-number-in-text question and, if present, move coords out of embedded text (a re-projection,
vectors are derived); (3) optional: bound `supersede_source`'s re-land. Acceptance: a one-line
body edit to a multi-symbol file embeds only the touched symbol's L0a chunk + shifted L0b windows
+ (post-fix) the touched L1 items; a revert embeds ZERO new chunks.

## Routing

`discovery`/efficiency → orchestrator. Weight per [[owner-dry-strictness]] (reuse-before-
reimplement is high-priority, not a nit). Coordinate with the integrator graduation wave (same
files likely in scope).
