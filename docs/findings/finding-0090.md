---
type: finding
id: finding-0090
status: routed        # /triage 2026-07-17: routed to orchestrator; batched to oq-0028 (non-blocking erratum)
created: 2026-07-16
updated: 2026-07-17
links:
  - docs/design-notes/temporal-geometry-and-drives.md   # the ratified §2.1 claim this corrects (A8 — never hand-edited)
  - docs/design-notes/global-event-clock.md             # the store audit that surfaced it (§2.2)
  - eval/harness/store.py                               # the chain-less exemplar (no seq/ts column)
  - core/stores/versions.py                             # per-DOC chains, not one per-stratum chain
ftype: math
origin_plan: the 2026-07-16 Fable design pass (dn-global-event-clock, §2.2 store audit)
route: orchestrator
---

# dn-temporal-geometry §2.1 "each stratum's store is totally ordered ⇒ proper time is exact" is overtaken by the store audit — exactness holds PER CHAIN, not per stratum

## What
Ratified `dn-temporal-geometry` §2.1 asserts: *"Proper time = per-stratum event count, exactly.
Because each stratum's store is totally ordered, longest-chain length equals event count — the
causal-set construction is an identity in this system, not an approximation."* The
`dn-global-event-clock` §2.2 disk audit (2026-07-16) shows the premise is not universally true:

1. **DuckDB-backed stores record no append order at all.** The eval-results table has no
   seq/rowid/timestamp column (`eval/harness/store.py:30-44`); telemetry's tables are
   wall-labeled only. Their events carry no chain — they order only via reads-from references.
   (The A-4 routing pin — ledgers→SQLite, analytics→DuckDB — turns out to be exactly the
   chained/chain-less boundary: SQLite stores carry rowid chains; DuckDB stores do not.)
2. **Chained stores are often per-KEY chains, not one per-stratum chain.** `version_seq` is
   monotonic per `doc_id` (`versions.py:71-81`) — the corpus stratum's version events form a
   union of per-doc chains, a partial order.
3. **A stratum can span stores** (e.g. mirror = raw + catalog + vectors + versions), so even
   all-chained stores give N_s as a union of chains, not a total order.

## Why it matters
"Longest-chain length = event count" is an identity only within ONE chain. Per stratum, the
maximal chain UNDERCOUNTS the event count wherever the restriction N_s is genuinely partial —
so "proper time = per-stratum event count, exactly" silently conflates an ordinal aggregate
(event count) with a causal-set proper time (chain length). Any future instrument that divides
by "proper time" inherits the ambiguity — the exact confound class Rule CLOCK exists to catch.

## The corrected statement (carried by dn-global-event-clock §2.3/GC-N6)
Proper time between two events is the maximal-chain length in `(Ev, ≼)` restricted to the
relevant stratum — exact per chain (per-doc version chains; per-run claim sequences), an
identity with event count only where the restriction is total. Per-stratum event COUNTS remain
lawful as ordinal indices (`N_s` window sizes); calling them proper time requires the chain
qualification. Chain-less (DuckDB) events participate via reference edges only.

## Route
The note is ratified → A8-immutable; per the oq-0025/oq-0026 discipline this finding is the
**standing erratum of record** — the note is never hand-edited. Owner may annotate by hand if a
book chapter or successor note is about to cite §2.1's exactness claim. Fold into the next
/triage; `dn-global-event-clock` (draft) already carries the corrected statement.
