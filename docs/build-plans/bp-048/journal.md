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
