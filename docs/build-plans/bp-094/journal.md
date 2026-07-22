# bp-094 journal

## 2026-07-21 — minted (graduation, session-41)

Graduated from ratified dn-code-ingest-pipeline (0c2deae; fable-audited, finding-0147)
per §3. Status: proposed — awaiting the owner's proposed→ready hand-bless. No work
performed. Grounding computed at graduation is recorded in the plan's §3.

## 2026-07-22 — Item 1 built (delegated builder, worktree)

Synced to main (`git merge main`, clean; bp-092's `core/ingest/code_corpus.py` +
`import_records` table present; `seal(bp-092)` in log). Bound `active-plan=bp-094`. Stayed in
worktree throughout.

**Item 1 (pattern extraction + existence check + code_to_code resolver) — DONE, patterns
shipped DISABLED (`ENABLED_L2B_PATTERNS = frozenset()`).** Files: `ops/code_sensor.py`,
`core/stores/reference_edges.py`, `tests/unit/test_code_sensor_l2b.py` (new),
`tests/unit/test_reference_edges.py`, `tests/integration/test_reference_edge_isolation.py`,
`tests/unit/test_code_sensor.py`, `tests/unit/test_interpreter_versions.py`.

What landed:
- **REF_TYPES += `dn-slug`,`finding-id`,`inherits`,`calls`** (additive vocabulary; the store's
  DOMAIN, precision gate lives in the extractor). `code_to_code` KINDS comment updated.
- **Existence check (§2.4-3), ALWAYS ON:** `extract_references(...,known_corpus=...)` drops a
  `note-citation` whose `docs/…md` target is absent from the tree at the commit (the `x.md`
  false-positive fix). `known_corpus=None` ⇒ pre-CI-3 behavior byte-identical (keeps the
  out-of-scope `test_reference_extraction.py` green). path-mention is NOT existence-checked (a
  code/path target stored as written). `_project` computes the tree's `.md` corpus set once
  (`_known_corpus_docs`) and threads it to the observation pass + both corpus scanners (a DRY
  win — the pre-CI-3 code re-`ls-tree`d per helper).
- **Shorthand resolvers (§2.4-1/-2), gated OFF:** `dn-<slug>`→`docs/design-notes/<slug>.md`
  (strip the `dn-` id-prefix), `finding-NNNN`→`docs/findings/finding-NNNN.md`, both
  tree-existence-checked (unresolved dropped, never guessed); paired-`§` binds only when the
  docstring cites exactly ONE resolvable note (ambiguous/unpaired dropped, PD-F). Edge-lane
  only (NOT in references_out).
- **code_to_code inherits/calls (§2.1 L0a), gated OFF:** static resolution — a bare base/callee
  name resolves module-internally (top-level def/class of the same file) OR via bp-092's
  `import_records` (consumed from the ledger) to a defining `.py` present in the tree
  (existence-checked). Attribute chains / dynamic dispatch / unresolved / self-edges dropped
  (PD-I). `_module_to_path` handles absolute + relative (`level`) imports.
- **8 new unit tests** (`test_code_sensor_l2b.py`): existence-check drop (pure + full
  projection), shorthand resolve/drop/disabled, paired-§ unambiguous-only, code_to_code static
  resolution + all four drop classes, `_module_to_path`. Isolation ratchet extended with a
  planted `code_to_code` edge (still bit-identical — F-CI5 holds).

**φ_code INTERPRETER_VERSION — BUMP 1.0.0 → 1.1.0 (attestation ESCALATED to orchestrator).**
Case: WORLDVIEW BUMP, not a re-pin. Why: the existence check changes `references_out` — the
code→corpus half of the versioned code-OBSERVATION content that `emit_batch` hashes and
`mark_projected` stamps — by dropping absent corpus targets. Same commit, different versioned
output ⇒ the doctrine's re-projection case (plan Q5), distinct from finding-0064/bp-026/bp-092
(which touched ONLY the unversioned reference-edge lane / the ops ledger and left observations
byte-identical → re-pin). The NEW reference-edge patterns are unversioned (edge-lane only, gated
off) and do NOT themselves justify the bump. Recomputed sha256 over
(`ops/code_sensor.py`,`ops/code_snapshot.py`) =
`a218c71daacc55fda5ed9aa8b0f324ab9357ebb6367f27931cc5fbfcd60709ee`, pinned at 1.1.0 in
`test_interpreter_versions.py`. **Re-projection/backfill under 1.1.0 is OWED** (owner-nod;
deliberately NOT run — no projection touched real data this session).

**Item 2 (M-C6 precision samples + enable) — PARKED, owner/deskcheck-gated.** It is the
"irreversible mint begins" step: it requires HAND-CHECKED stratified precision samples over the
real corpus at HEAD (human judgment — a builder cannot self-certify precision, F-CI6) and it
writes to the accumulating `data/reference_edges.sqlite` (owner-nod, no-backfill discipline). The
machinery is complete and flag-ready; enabling a pattern is one entry in `ENABLED_L2B_PATTERNS`
after its sample clears.

**Finding filed:** `finding-0158` (spec-fidelity) — the store has no section-anchor field for
paired-`§`; v1 overloads `target_detail` (pattern gated off, no data at risk); design confirms
the shape or adds a column at the enable gate.

Full attestable-green gate (each leg separately; pytest foreground; FORCE_COLOR unset):
- `ruff check .` → All checks passed
- `mypy core agents eval ops scheduler scripts` → Success, no issues (252 files)
- `mypy` (argless) → **Found 69 errors** (baseline; unchanged)
- `python -m ops.type_gate` → OK (tier-2 + bare-ignore scans pass)
- `pytest -q -m 'not live and not podman and not needs_vault and not needs_restic' --deselect …
  --cov` → **1888 passed, 11 skipped, 21 deselected in 61s**

## Follow-through

- **Built?** Yes — Item 1 complete: existence check (active), shorthand resolvers + code_to_code
  inherits/calls (implemented, unit-tested, shipped DISABLED behind `ENABLED_L2B_PATTERNS`).
  INTERPRETER_VERSION bumped 1.0.0→1.1.0, ratchet re-pinned. Item 2 parked (owner/deskcheck).
- **Wired/dormant?** The existence-check correction is WIRED into the live projection path (it
  changes references_out whenever a projection runs). The new reference-edge patterns are DORMANT
  (flag-gated off; mint nothing until Item 2 enables per M-C6). No projection/backfill run this
  session → no real store touched.
- **Consumer?** F-fiber substrate for CI-4 (the S↔F code↔design lens, bp-095) — needs the resolved
  reference edges. `references_out` consumers see the existence-checked (cleaner) code→corpus set.
- **Track state?** code-ingest track: CI-1 (bp-092) sealed; CI-3 Item 1 done, Item 2 parked. NOT
  self-declared done — see deskcheck below.
- **New track/finding?** finding-0158 (spec-fidelity, routed). Owed: (a) orchestrator verifies the
  φ_code bump attestation + re-pin; (b) backfill_observations() re-projection under 1.1.0 at the
  owner's nod; (c) Item 2 M-C6 hand-checked samples + enable (owner-visible).

ready to deskcheck
