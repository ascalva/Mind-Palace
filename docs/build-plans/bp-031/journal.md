# bp-031 journal

## 2026-07-14 — authored `proposed` (orchestrator, opus/xhigh graduation)

Graduated from `dn-temporal-retrieval-algebra` (ratified `6108dd8`) — the **FIRST** plan of that note's
graduation, per the A6 ruling (note §2.4 / Owner rulings 2026-07-14: rename-stable identity is a HARD
PREREQUISITE, gating the diachronic reader / Result-1 H1 / β\*-over-lineage). Companion plan bp-032
(`core/temporal/` module) `depends_on: bp-031`.

**Grounded pass (citations in §3):**
- The fork point is `sync.py`: identity keyed on `source_path` throughout (`:84,89,99,112`); a rename =
  `handle_deleted(old)` tombstone + `sync_path(new)` fresh seq-1 chain → version continuity lost
  (`supersession-lifecycle.md:287-289`).
- **De-risking discovery #1:** `versions.py` **already** keys on a generic `doc_id` column (`:54,59`);
  today `sync.py:112` just passes `source_path` *as* the doc_id → **the version schema is UNCHANGED**;
  only the value sync resolves changes.
- **De-risking discovery #2:** `logseq.py`'s `_PROP` regex (`:19,64`) already parses `id::` into
  `ParsedNote.properties` → reading an **existing** page id is zero-new-code, zero-vault-mutation.
- Blast radius: `source_path`/catalog/versions referenced across ~20 test files (grep) → contained by
  **behavior-preservation** (backfill `doc_id := source_path`; default resolution to `source_path`).

**One decision is deliberately UNRESOLVED (A4 discipline):** the identity *mechanism* — the note left it
open ("front-matter uuid **or equivalent**", `supersession-lifecycle.md:290`). Routed to the owner as
**oq-0019** (recommended default: existing-`id::` + exact-content rename detection on rescan; **no**
mint-into-vault). The plan is split at that seam: **Item 1 is mechanism-agnostic and buildable on
blessing**; Items 2–3 park on the ruling and proceed after (never-block).

**write_scope lists all three test paths** (finding-0075 discipline — the THIRD recurrence of 0071/0072):
`test_rename_identity.py` (NEW) + `test_version_history.py` + `test_vault_sync.py` (the store/sync homes
that may need a visible-surface touch). The finding-0075 nuance is honored: any OTHER existing test
reddening is a **stop-and-raise** (§10), not a self-widen — Item 1 must be additive.

Estimate opus/300k (live-store migration + a behavior-preservation falsifier needing judgment). Awaiting
the owner-only `proposed → ready` blessing **and** the oq-0019 mechanism ruling. No code written.

## 2026-07-14 — blessed `proposed → ready` (owner, by hand); orchestrator commits the flip

Owner hand-blessed bp-031 (and bp-032/033) `proposed → ready`. Orchestrator commits the flip (rule 0060).
**oq-0019 is still OPEN** → on `/build`: **Item 1** (the additive, behavior-preserving `doc_id :=
source_path` foundation) proceeds; **Items 2–3** (mechanism + rename carry-forward) **PARK on default (A)**
(existing-`id::` + exact-content rename detection, NO mint-into-vault) with re-entry = the owner ruling
oq-0019. To let bp-031 complete FULLY in one build session, rule oq-0019 first (default A stands otherwise).
No code written yet.

## 2026-07-14 — `/build` START: ready → in-progress (orchestrator-driven, opus/high)

Fresh build session. `/build bp-031` set active-plan + flipped `ready → in-progress`. **oq-0019 is now
RULED B** (mint `id::`; answer drafted in owner-questions.md, owner confirm-flip → `answered` pending —
non-blocking). Per the oq-0019 answer, **bp-031's scope is UNCHANGED under B**: Item 1 = additive `doc_id`;
Item 2 = resolve from existing `id::` + exact-content rename detection (the superset-compatible base for B);
the mint itself is the separate **bp-034** (owner-run). So all three items build here as §7 specifies.

**Context manifest read in full** (sync.py, catalog.py, versions.py, logseq.py, the two in-scope tests).
Confirmed the de-risking facts on disk:
- `versions.py` schema is `(doc_id, version_seq)` — UNCHANGED; today `sync.py:112` passes `source_path`
  *as* doc_id. Item 1 routes `version_store.record` through a resolved `doc_id` (== source_path in Item 1).
- `catalog.py` `vault_files` PK = `source_path`, no `doc_id` column — the store that gains it.
- `logseq.py` `_PROP` already parses `id::` into `parsed.properties` (Item 2 reads it, zero new parsing).
- `test_version_history.py:74-75` keys the version chain on `active_entries()[0].source_path` → since
  `doc_id_for(p) == p` in Item 1, that chain stays `[1,2]`. Behavior-preservation holds.

**Item 1 design (least-migration, additive):** add a nullable `doc_id TEXT` column to `vault_files` +
`CREATE INDEX IF NOT EXISTS vault_files_doc_id`; an idempotent `_migrate()` (`ALTER TABLE … ADD COLUMN`
if absent + backfill `doc_id := source_path WHERE doc_id IS NULL`); `record()` populates a new row's
`doc_id := source_path` and PRESERVES it on conflict (a diverged id is not reset by a routine re-ingest —
sets up Item 2); a `doc_id_for(source_path) -> str` resolver (falls back to source_path for an unknown
path). `CatalogEntry` is deliberately UNCHANGED (adding a field would risk reddening equality assertions —
Item 1 needs only `doc_id_for`). sync routes `version_store.record(catalog.doc_id_for(source_path), …)`.
versions.py:55 comment corrected (§4). Building now.

## 2026-07-14 — Item 1 COMPLETE (the additive `doc_id` foundation) — behavior-preserving, dry-run verified

**Code (all in write_scope):**
- `core/stores/catalog.py`: `_DDL` gains a nullable `doc_id TEXT` column (fresh stores); an idempotent
  `_migrate()` runs in `__post_init__` — `ALTER TABLE … ADD COLUMN doc_id` when absent, then (always,
  IF NOT EXISTS) creates the `vault_files_doc_id` index and backfills `doc_id := source_path WHERE doc_id
  IS NULL`. `record()` populates a new row's `doc_id := source_path` and PRESERVES it on conflict (a
  diverged id is not reset by re-ingest — the Item 2 seam). New `doc_id_for(source_path) -> str` resolver
  (falls back to the path for an unknown row). **`CatalogEntry` deliberately UNCHANGED** — adding a field
  risked reddening equality assertions; Item 1 needs only `doc_id_for`.
- `core/ingest/sync.py`: `version_store.record(...)` now keys on `self.catalog.doc_id_for(source_path)`
  (resolved AFTER `catalog.record`, so the row exists) — == source_path in Item 1, byte-identical. Two
  now-inaccurate "keyed on (source_path, …)" comments corrected to doc_id.
- `core/stores/versions.py`: the DDL comment on `doc_id` corrected (§4 — no longer literally source_path).

**Gotcha fixed:** the `vault_files_doc_id` index cannot live in `_DDL` — on a legacy store `CREATE TABLE
IF NOT EXISTS` is a no-op so the column isn't there yet and the index DDL errors (`no such column: doc_id`).
Moved it into `_migrate()`, after the column is guaranteed. Caught by the legacy-catalog migration test.

**Acceptance — MET:**
- Behavior-preservation falsifier did NOT fire: FULL suite **1026 passed, 8 skipped** (nothing outside the
  two named test files reddened).
- Focused tests added to `test_vault_sync.py`: `test_doc_id_defaults_to_source_path` (fresh store: doc_id
  == path; chain [1,2] under the resolved id), `test_doc_id_for_unknown_path_resolves_to_itself`,
  `test_migration_backfills_doc_id_on_legacy_catalog` (raw-sqlite legacy schema → reopen → backfill for
  active AND tombstoned rows, digest/active untouched, idempotent second open). 17/17 in the two files.
- **Live-store dry-run** (the plan's Item-1 requirement): copied the LIVE `data/vault_catalog.sqlite`
  (legacy schema, 5 active rows) to scratch, ran the real `VaultCatalog` migration against the COPY →
  5→5 rows, every `doc_id == source_path`, 0 NULLs, index created, idempotent on reopen. Never touched the
  real file. The live migration is de-risked; it runs automatically when the daemon next opens the catalog
  on the new code (deploy-coupled, finding-0066 — optional owner `mind-palace deploy` align after landing).

**Next: Item 2** — resolve `doc_id` from an existing `id::` (`parsed.properties.get("id")`) + exact-content
rename carry-forward on rescan (the superset-compatible base for oq-0019 ruling B). The hard part is rescan
rename detection WITHOUT appending a phantom version (a pure rename is not a new version) and rebinding the
new source_path's projection. Item 3 = the falsifiable rename-stability proof (`test_rename_identity.py`).

## 2026-07-14 — Items 2 & 3 COMPLETE (resolution + rename carry-forward + the A6 proof)

**Design realization (corrected an early assumption):** a pure rename is EXPECTED to append a version —
Item 3's acceptance asserts the chain becomes `v1,v2,v3` under ONE doc_id (the re-appearance at the new
path is v3). The A6 property is not "no new version" but "no FORK": the new path must continue the SAME
doc_id chain, never open an orphan seq-1 chain. That simplified the carry-forward.

**Item 2 code:**
- `core/stores/catalog.py`: `record()` gains an optional `doc_id: str | None = None`. Omitted → a new row
  defaults `doc_id := source_path`, a re-record PRESERVES the stored id (Item 1 behavior, byte-identical).
  Given → binds/overwrites it — but sync passes one ONLY at first bind (see below), so a historied note's
  identity is never silently switched (that re-key is owner-run bp-034).
- `core/ingest/sync.py`:
  - `sync_path(path, *, rename_by_digest=None)`: resolves the stable doc_id **at first bind only**
    (`prev is None`) — prefer an existing `id::` (`parsed.properties.get("id")`, non-mutating, already
    parsed by `logseq._PROP`), else a renamed predecessor's carried doc_id via exact-content match.
    An already-bound note keeps its identity (guard on `prev is None`) → **no live fork** even before
    bp-034. `catalog.record(..., doc_id=resolved)`; version keys on `catalog.doc_id_for(source_path)`.
  - `rescan()`: builds `rename_by_digest = {digest: (gone_path, doc_id)}` from the PRE-sync catalog for
    every vanished (`active_paths() - present`) path; a new path whose content digest matches adopts that
    doc_id. A digest held by >1 vanished path is AMBIGUOUS (dedup) → dropped (fresh identity, no false
    carry). `id::` wins over content-match (decided in sync_path).

**Item 3 — `tests/integration/test_rename_identity.py` (NEW, 4 proofs):**
1. `test_pure_rename_keeps_one_continuous_version_chain` — A(v1,v2) → rename → ONE chain `[1,2,3]` under
   one doc_id; `history(str(b)) == []` (no fork); `count()==3`; vault byte-unchanged (no mint).
2. `test_existing_id_property_is_the_stable_identity_across_rename` — `id:: note-xyz` is the doc_id, survives
   rename, chain `[1,2]` under `note-xyz`; file still starts `id:: note-xyz` (read, not written).
3. `test_rename_with_edit_falls_back_to_new_lineage` — the §11 parked ambiguity: rename+edit → distinct
   lineage (defaults to path), no false carry — the no-regression floor.
4. `test_ambiguous_shared_content_rename_does_not_misattribute` — two vanished twins + a new match → dropped
   → defaults to path, never a coin-flip carry.

**FULL attestable-green gate (5 legs, run SEPARATELY — finding-0038):**
- LEG 1 `ruff check .` → **All checks passed** (reflowed several >100-char comments to the 100 ceiling).
- LEG 2 `mypy core agents eval ops scheduler scripts` → **0** (hard floor held).
- LEG 3 argless `mypy` → **69** (== tests-baseline). My new test file's `FakeEmbedder→VaultSync` arg-type
  (the same duck-type baselined in test_version_history.py:67) carried a coded `# type: ignore[arg-type]`
  so the count stayed at 69 rather than growing to 70 — the baseline is a hard `==`, not a `≤`.
- LEG 4 `python -m ops.type_gate` → OK (tier-2 membership + bare-ignore scan).
- LEG 5 `pytest -q` → **1033 passed, 8 skipped** (+7 new: 3 doc_id in test_vault_sync, 4 in
  test_rename_identity). Behavior-preservation held across the whole suite.

## 2026-07-14 — SEAL: bp-031 COMPLETE (in-progress → complete)

**All 3 items landed; the A6 hard prerequisite is met.** A file rename no longer forks version-history
lineage — proven by `test_rename_identity.py`. This unblocks **bp-032** (the `core/temporal/` module,
whose δ_D/version chains need rename-stable `doc_id`), then bp-033.

**Diff vs write_scope — CLEAN.** Changed exactly: `core/stores/catalog.py`, `core/ingest/sync.py`,
`core/stores/versions.py`, `tests/integration/test_vault_sync.py`, `tests/integration/test_rename_identity.py`
(new) — all in `write_scope` — plus this journal and the plan's own status/cost. `test_version_history.py`
(in scope) needed no touch. No out-of-scope write; the behavior-preservation falsifier never fired.

**Verification (the /verify obligation):** the rename-identity integration tests drive the real flow
end-to-end (real raw/vector/catalog/version stores, real sync, observed version chains), and the migration
was dry-run TWICE against a COPY of the LIVE `data/vault_catalog.sqlite` (5 rows → 5, all doc_id ==
source_path, idempotent) — never the real file.

**Cost (owner /usage relayed at seal):** est opus/300k; actual **91k non-cache** (9.4k in + 81.7k out;
+11.2M cache-read, 149k cache-write), **$9.19**, ratio **0.30** — UNDER, self-driven band (cf. bp-029 0.27×).
session +21pp (14%→35%), week +2pp (78%→80%, cache-dominated). Model opus, high effort, **single-lane
(0 subagents)** — a live-store migration the owner chose to scrutinize directly.

**⚠ DEPLOY-COUPLED (finding-0066).** The catalog gains a `doc_id` column; the migration runs
automatically when the daemon next opens the catalog on this code. The **live daemon (run 16, PID 75337)
lags HEAD** — an align is an **owner-only `mind-palace deploy`** (optional; the dry-run de-risked it).

**⚠ oq-0019 SEQUENCING.** Ruling B (mint `id::`) is IMPLEMENTED here only as *resolution* (read an existing
`id::` at first bind + exact-content carry-forward) — the superset-compatible base. The **mint + append-only
re-key is bp-034** (owner-run, `depends_on: bp-031`, daemon down). Item 2 deliberately does NOT switch an
already-historied note's identity (guard: `prev is None`), so there is **no live-fork window** before bp-034.

**Next: bp-032** (strict dependency order). opus/high.
