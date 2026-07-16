# Journal — bp-048 `review-repl`: the review REPL + theory probes (E6, Track L L2)

> The fresh-agent contract: a new session with only `plan.md` + this journal + the write-scope files
> must continue without re-asking. Checkpoint at every semantic boundary. Status flips are the
> orchestrator's, by hand.

## 2026-07-16 — GRADUATED (proposed), awaiting owner `proposed→ready` blessing

- Graduated by the orchestrator (opus, self-driven) from ratified `dn-evaluation-harness` §3 **E6**
  (Track L L2, carried). Independent of every other harness plan and of the σ-lever fork parking
  E3a-1 — it reads the BUILT `RunLedger` + the BUILT verdict store and produces verdicts that later
  feed E7's `precision@review`.
- **Grounding done in-session** (`path:line` in the plan §3/§6). Key facts:
  - `scripts/review.py` does NOT exist on disk (verified) → greenfield; the REPL is built for the
    first time over already-built stores.
  - **A/B is native, not new machinery:** `RunLedger.claims()` rows carry `run_id`; `runs()` maps
    `run_id → pipeline` — interleaving claims labeled by pipeline IS the phase7-vs-dream_v2 split
    (`runledger.py:171-186`). precision splits fall out of a verdict × pipeline join.
  - **The signing path is REUSED verbatim from `scripts/verdict.py`:** `get_secret(cfg.attestation.
    owner_key_secret)` → `sign_verdict(VerdictPayload(subject_id=claim_id, ...), Ed25519Signer.
    from_seed(seed,"owner"))` → `build_verdict_receiver(cfg)(signed)` (verify + append monotonic-seq +
    apply disposition). The REPL adds NO new persistence path; the store is append-only.
  - `subject_id = claim_id` (content-addressed, excludes surface+confidence) so a re-emitted claim
    inherits its prior verdict (the note's carryover property) — pinned as the Item-17 falsifier.
  - **Probes are the LESS-grounded half (honest N/A-adjacent):** the BUILT surface has no probe store;
    the probe schema lives in the superseded **Track L §3 protocol annex** (in the plan's §2 context
    manifest). The plan does NOT invent a schema — Item 18 grounds it against the annex at build and
    STOPS+files a finding if the annex implies a store/trigger the write_scope can't honor. Probe
    *execution* (the R-gated demon run, catalog row 12) is explicitly out of scope.
- **Scope discipline:** greenfield → §3 is real grounding (not blanket N/A), §4 is cross-reference-only,
  §8 is N/A. `RunLedger`, `scripts/verdict.py`, `core/verdict/**` are read-only dependencies, NOT in
  write_scope. Retrofit-pre-widen does not bite (no existing surface moved).
- **Next:** owner blesses `proposed→ready`; delegate as a supervised builder in parallel with bp-047
  (disjoint write_scope). Pre-flight budget gate first (est opus/220k).

## 2026-07-16 — BUILD START (delegated builder, opus, worktree)

Active-plan pointer set to bp-048. Context manifest read in order (annex + all read-only deps).

### Grounding decisions (settled during context read — NO §10 STOP)
- **§3 Q4 probe schema — GROUNDED, not invented.** Track L §3 annex
  (`docs/design-notes/live-adoption-and-longitudinal-harness.md:140-142`) pins the probe record as
  `probe(probe_id, hypothesis, expectation_kind, target_hints)`; the `plausible → probe candidate`
  trigger is pinned in the annex verdict table (`:117`) AND `core/verdict/taxonomy.py:19`. Mapping
  the annex fields onto a `plausible`-verdicted claim (plan Q4 "claim_id + probe question +
  provenance key"):
    - `probe_id` = sha256(claim_id ‖ hypothesis) — idempotency-by-(claim_id, question) made
      structural (PRIMARY KEY);
    - `claim_id` = verdict subject linkage (plan Q2);
    - `hypothesis` = probe question = claim `surface_text` (annex field);
    - `expectation_kind` = claim `kind`; `target_hints` = claim `support_json` (annex fields);
    - `pipeline` = provenance (plan Q4).
  Store honored in write_scope: small append-only SQLite table beside the verdict store (plan §11
  parked default). Probe *execution* (catalog row 12, R-gated) stays OUT. → No STOP: annex grounds
  the shape and write_scope honors it.
- **RunLedger real schema** (`runledger.py:90-98`): `dream_claims` = `claim_id, run_id, kind,
  confidence, support_json, surface_text, novel` — NO `polarity`/`pipeline` column (plan §6 pin
  lists `polarity` loosely). pipeline is sourced from `runs()` `run_id → pipeline`. `claims(
  novel_only=True)` exists and is used (design note: "queue novel-first").
- **Fail-closed on missing owner key** mirrors `scripts/verdict.py:43-47` (stderr + return 1).

### The seam (model-free + testable)
`run_review(items, deps, blind=...)` with `deps: ReviewDeps` injecting `signer / submit / next_seq
/ record_probe / read_key / write / now`. Production `main()` wires the REAL owner path
(`get_secret` → `Ed25519Signer.from_seed`, `build_verdict_receiver(cfg)`, `open_verdict_store` for
seq, `open_probe_store`). Tests inject an in-memory `VerdictStore` + generated test signer +
scripted keystrokes — the builder NEVER touches the real signed store. Keystroke map:
`n`=novel_useful `k`=true_known `p`=plausible `w`=wrong `x`=noise; `s`=skip `q`=quit; unknown key
re-prompts the SAME claim with NO store write.

### Progress
- [x] Item 17 — `scripts/review.py` (model-free REPL: interleaved A/B, keystroke signed verdicts
      via the built receiver seam, `subject_id=claim_id`, session summary split by pipeline).
- [x] Item 18 — `eval/harness/probes.py` (annex-grounded `ProbeCandidate` + append-only idempotent
      `ProbeStore`; wired into `review.py`'s `plausible` branch via `deps.record_probe`).
- [x] green gate (5 legs) — all green; argless mypy == 69 baseline.

### Tests (write scope)
- `tests/integration/test_review_repl.py` — 7 cases: signed+monotonic+claim_id-keyed verdicts;
  re-emission shares subject_id; out-of-taxonomy key rejected with NO write; skip/quit; input
  exhaustion; keymap == taxonomy; model-free source scan.
- `tests/unit/test_probes.py` — 11 cases: annex-field mapping; idempotency by (claim_id, question);
  open_probes reader; no mutation API; store-path placement; plausible→exactly-one-probe;
  non-plausible→none (parametrized); re-emitted plausible → one probe.

### Green-gate output (all five legs run SEPARATELY)
- `ruff check .` → All checks passed!
- `mypy core agents eval ops scheduler scripts` → Success: no issues found in 197 source files
- `mypy` (argless) → Found 69 errors in 20 files (checked 403 source files)  [== baseline; exit 1]
- `python -m ops.type_gate` → Tier-2 membership OK; bare-ignore scan OK
- `pytest -q -m 'not live'` → 1235 passed, 10 skipped, 9 deselected

### Notes for a fresh agent
- The seam is `run_review(items, deps)`; production wiring in `main()`/`_build_production_deps`
  is the ONLY place the real owner key + real stores are touched — untested by design (owner's act).
- Interleave orders pipelines ALPHABETICALLY (`dream_v2` before `phase7`), novel-first/conf-desc
  within each group — the queue `[C, A, B]` in the integration test is deliberate, not incidental.
- No §10 STOP triggered; no finding filed. Probe schema grounded at annex `:140-142` (see above).
