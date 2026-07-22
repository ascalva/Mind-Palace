# bp-092 journal

## 2026-07-21 — minted (graduation, session-41)

Graduated from ratified dn-code-ingest-pipeline (0c2deae; fable-audited, finding-0147)
per §3. Status: proposed — awaiting the owner's proposed→ready hand-bless. No work
performed. Grounding computed at graduation is recorded in the plan's §3.

## 2026-07-22 — build session (delegated builder, worktree agent-aef072ee)

**Step 0 — bind + sync.** `active-plan` = bp-092 (verified). `git merge --no-edit main` →
"Already up to date" (worktree base already on current main; `core/kernel/**` tree present,
recent `seal(bp-091)` visible). Stayed inside the worktree dir throughout — never the shared
checkout.

**Grounding (whole-file reads).** Plan, journal, ratified note (dn-code-ingest-pipeline),
findings 0146/0147. Machinery at REAL post-K1/K3 locations: `core/kernel/provenance.py` (the
StrEnum, six classes; mirror `OBSERVED` hardcoded mint pattern is `code_observations.py:146-150`),
`core/kernel/ingest/{chunk,pipeline,amend,verify}.py`, `core/ingest/{index,embed}.py` (stayed
outer), `core/stores/vectorstore.py` (outer; 8-col schema, no `layer`), `ops/code_snapshot.py`
(the ledger: symbols carry `lineno` only, no `end_lineno`; `imports` stores only the dotted ROOT;
`#` comments enter no store), `scheduler/{vault_sync,chat_sync,router}.py` + `ops/lifecycle/
launcher.py:311-346` (the KIND registry + housekeeping/catchup enqueue), `config/defaults.toml`.

**BLOCKER found — write_scope drift from K1/K3 (filed finding-0156).** bp-092 was graduated
2026-07-21; K1 (bp-090) + K3 (bp-091) sealed 2026-07-22 01:12–01:35, AFTER graduation, and
relocated `core/provenance.py` → `core/kernel/provenance.py`. Adding `Provenance.CODE` (the
lane's whole structural mint, note §2.3 / plan §6) therefore needs a kernel file that is OUTSIDE
this plan's write_scope. Verified empirically: `bash .claude/hooks/scope-guard.sh --standalone
core/kernel/provenance.py` → rc=2 (DENY). No route-around permissible. Escalated to the
orchestrator for a one-line write_scope widen (`core/provenance.py` → `core/kernel/provenance.py`);
filed finding-0156 (spec-fidelity → orchestrator). Everything else in bp-092 is reachable within
the existing scope. Comment count at HEAD = 3360/254 main-package files (vs audited 3318/247 at
625a058 — real commits since; Item 1 test will self-consistently recount, NOT hardcode 3318).

**Proceeding:** Item 1 (ledger extensions, `ops/code_snapshot.py`) is enum-independent and fully
in-scope — building it now. Items 2–4 park on the widen (re-entry: write_scope carries
`core/kernel/provenance.py`).

### Item 1 — ledger capture extensions — DONE

`ops/code_snapshot.py`, all ADDITIVE (no existing row mutated):
- **`symbols.end_lineno`** (L0a slice boundary): captured in `_walk_defs` from `ast` `end_lineno`;
  additive `ALTER` migration in `open_snapshot_db` (default 0 → backfilled to a real span).
- **`comments` sidecar** (closes finding-0146 defect 2): a stdlib `tokenize` pass (`_comments`),
  each `#` comment attributed to the INNERMOST symbol whose `lineno..end_lineno` span contains it
  (`_innermost_qualname`, smallest span wins), '' = file grain. Tokenize errors → no comments for
  that file, never a snapshot failure. New `comments` table (auto-created by the DDL executescript).
- **`import_records`** (full dotted module + names; CI-3's precondition): `_import_records` — one
  row per imported name, FULL dotted `module`, `name`/`asname`/`level`. The legacy root-only
  `imports` table is UNCHANGED (existing consumers untouched). New `import_records` table.
- **§4 header correction**: the "Deliberately NOT here… stays on the ops side until ratified"
  paragraph rewritten to cite ratification (dn-code-ingest-pipeline, 2026-07-21; warrant 0146) and
  name the CI-1 captures — banner-on-correction, not silent.
- **Backfill**: `backfill_code_corpus(db, repo)` mirrors `backfill_docstrings` exactly — re-parses
  each unique blob once (cached), fills end_lineno + comments + import_records for pre-CI-1 rows,
  mark-guarded by `_code_corpus_backfilled` (idempotent, self-healing on sync).

**Tests** (`tests/unit/test_code_corpus_ledger.py`, 9 passing): span capture; comment innermost-
symbol attribution; full import records (dotted preserved, legacy `imports` set unchanged); the
L0a span+shell PARTITION check (F-CI2 precursor — every line in exactly one bucket); snapshot
roundtrip; **the additivity falsifier** (`_pre_existing_checksum` over files/symbols/imports pre-
existing columns identical before/after a backfill on a regressed-to-pre-CI-1 ledger); and the
acceptance measurement — comment capture reproduces an INDEPENDENT tokenize recount over the pinned
main-package set (self-consistent, floor >3000; HEAD measures 3360/254 vs audited 3318/247 @625a058).
`ruff` + targeted `mypy` clean. **Touches stored data:** the real ledger is absent in this worktree
(`data/` empty); all captures are additive + backfill is mark-guarded, so a live ledger heals on
next sync with zero row mutation (proven by the additivity test on a copy-shaped in-test ledger).
