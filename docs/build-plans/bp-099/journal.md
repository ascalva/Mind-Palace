# Journal — bp-099 (the temporal code corpus)

> Alive while the plan is proposed/in-progress; sealed on completion.

## 2026-07-22 — MINTED (Fable design pass → immediate graduation, session-43)

- **State:** `proposed`. Owner-directed one-motion design+graduation ("create the design and
  immediately create the build plan — the design is already there; I will bless, and we build
  immediately"). Design: `dn-temporal-code-corpus` (draft, ratifies at the same blessing sitting).
  **Warrant finding-0163** — owner ruling: PD-B reversed. *"You can't add causal edges if the
  history of the code isn't represented."* The product is a graph that evolves over time;
  HEAD-only embedding + delete-on-change made the integrator's causal chain
  (conversation → commit → code-change-as-supersession-edge) structurally impossible.
- **Grounding done at graduation** (live reads, session-43): the backfill scale is **1,542
  distinct (path, blob_sha) versions / 977 commits** (~6× the HEAD seed that ran clean today);
  the current sync **deletes** superseded rows (`code_corpus.py:238-239` — the load-bearing
  defect); `_migrate_layer_if_needed` is the additive-migration precedent for the `current`
  column; `poset_from_chains` (`core/temporal/boundary.py:99-112`) is store-free and consumed
  as-is; `commit_diffs` capture discharges finding-0111's "cheap, uncaptured" gap **without
  touching** `code_snapshot.py`/`code_sensor.py` (φ_code pin protected by keeping them out of
  write_scope). Three code-does-not-settle items flagged in §3 (Q3 shim update shape, Q5 ledger
  commit ordering, Q6 batching) — builder reads + mirrors, never infers.
- **Scope discipline:** flag-less by design (§3 of the note — finding-0159/0161 lineage: a
  store-model correction ships ON; an off-switch would re-create the defect). The C-side
  densification stays finding-0151's separate Fable pass; this plan builds the D-side substrate
  it composes against.
- **Next action (on owner bless → ready):** `/build bp-099`; Items 1→2→3 (retention schema →
  history backfill → lineage edges). Deploy promptly after seal — the live daemon's old sync
  discards superseded rows until then (recoverable via backfill; still, don't bleed).
- **Blocking:** none. Awaiting `dn-temporal-code-corpus` draft→ratified + bp-099 proposed→ready
  (both owner-only, by hand; `palace bless bp-099` for the plan).
