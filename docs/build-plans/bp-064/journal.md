# Journal — bp-064 (chat clock wiring: CS-4)

## 2026-07-17 — graduated (proposed), not yet started
Minted by /graduate from RATIFIED `dn-chat-sensor` CS-4 (second of the §3 tranche). Status `proposed` —
awaits the owner's `proposed → ready` blessing (owner-only, by hand). **`depends_on: bp-063`** — the
`chatlog` store must be built first (this plan enrolls it).

**Grounding carried in the plan (so a fresh builder needn't re-derive):**
- This plan EXTENDS the pinned spine surface (`spine.py:100-105` "EXTEND, never reshape"): additive only —
  a `chatlog: ChatlogStore | None` field on `SpineSources`, a `_Builder.chatlog` method (per-session g1
  chains copied from the `versions` per-doc exemplar `:394-406`; chain-key = session_id, pos = turn_index),
  a `Spine.derive` call, `_STRATUM["chatlog"]="observed"`, and — the one behavioral change —
  `_STRATUM_CERTIFICATES["observed"]=frozenset({TROUGH})` (§3 Q2: session-close trough-style; local-file
  sensor ⇒ NO HANDOFF, unlike ops/interpreted; grounded against the `eval→TROUGH` case `:259`).
- Cut legality: open sessions are excluded at INGEST (bp-063 stores only closed sessions), so a cut's
  frontier is closed-only; TROUGH attests no in-flight sensor append. Utterances consume nothing ⇒
  `crossing_edges == []` (§3 Q5).
- Atlas (§3 Q4): the chat clock is store-scoped (read-clock frontier borrow, Law C3 `:740-741`) — expected
  to resolve through existing atlas machinery with NO change; a gap is a `codebase` finding, not a patch.
- Write_scope carries `test_cuts.py` + `test_cut_soundness.py` (the retrofit rule — CS-4 extends the
  surface they pin; a new positive `observed→TROUGH` case, never an edited assertion meaning).

**Next action when built:** item 1 (`observed→TROUGH` certificate rule + test_cuts case) → item 2 (enroll
the store's per-session chains + resolve()/derive wiring + the CS-4 falsifiers). 2-item serial. Estimate
opus/150k. Completing this opens ONE of CS-6's three gates (sensor+clock built); the lag instrument stays
gated on the correlator's scoped grant (owner act) + uuid-identity for claim grain.

---

## session-27 (2026-07-17) — BUILT, in-session OPUS builder contract

**Setup.** active-plan → bp-064; status `ready → in-progress`. Grounded fully against the pinned spine
surface (spine.py:100-270, 300-357, 394-636, 675-880) + chatlog.py + atlas.py + the two test files.

**⚠️ Ratchet awareness (bp-066 just landed).** `test_core_self_containment` is red-at-106 by design.
This build touches `core/temporal/spine.py`, which already holds 3 forbidden imports (eval:97,
config:100,343). Discipline: the chatlog enrollment reuses spine's EXISTING imports and pulls
`ChatlogStore` from `core.stores.chatlog` (INTRA-core, not a sibling) — **verified: the ratchet stays
at 106, no new forbidden import.**

### Item 1 — `observed → TROUGH` certificate ✅
- `_STRATUM_CERTIFICATES["observed"] = frozenset({Certificate.TROUGH})` with a grounding comment
  (§3 Q2: session-close trough-style, local-file sensor ⇒ NO HANDOFF; cf. the eval→TROUGH case).
- `tests/unit/test_cuts.py` gains `test_observed_cut_composes_trough` (additive beside the existing
  per-stratum cases; no assertion's meaning changed). **Acceptance: `test_cuts.py` green.**

### Item 2 — enroll the chatlog store (per-session g1 chains) ✅
- `from core.stores.chatlog import ChatlogStore` (intra-core); `_STRATUM["chatlog"]="observed"`;
  `SpineSources.chatlog` field; `resolve()` branch `chatlog_p = data_dir/"chatlog.sqlite"` guarded by
  `.exists()` (no side effect — matches `open_chatlog_store`'s path, DRY); `_Builder.chatlog` (per-
  session g1 chains, chain_key=session_id pos=turn_index, produces=()/consumes=() — reuses the
  store's own ordered `all_rows()`, mirrors the `versions` exemplar); the `Spine.derive` call.
- `tests/unit/test_chat_clock.py` (7 falsifiers): per-session chains at the latest turn; contiguous
  positions; **order by turn index NOT ts_bookmark** (seeded ts descending vs turn ascending — the
  Law C4 falsifier); observed cut composes {TROUGH} + `crossing_edges==[]`; refuses without a
  quiescent trough; **atlas-reachable** (§3 Q4 — `frontier_at("chatlog")` + `SpineAtlas.has(N_S)` +
  chat events in the pullback; resolved through existing machinery, NO atlas change, as predicted);
  enrollment reshapes no other store's frontier.
- `tests/integrity/test_cut_soundness.py` gains a seeded chat-chain-no-crossing case.
  **Acceptance: `test_chat_clock.py tests/integrity/test_cut_soundness.py` green (real-store legs
  pass on main).**

**Verification.** All 3 test files + spine.py: ruff `All checks passed`, mypy `Success (4 files)`.
bp-064 tests: **32 passed**. Existing spine/cut regression: 36 passed (no reshape). Ratchet: 106
(unchanged). Falsifiers all checked (no wall-time ordering; contiguous positions; no crossing; no
reshape of other stores).

### Non-goals honored
No new `Stratum` enum member; no correlator (CS-5); no atlas.py/scope.py change (§3 Q4 held — no
finding needed); no reshape of any pinned method (additive only); no wall-clock ordering.

### Acceptance — ALL MET (full-suite gate)
- Full suite: **1 failed, 1547 passed, 8 skipped** — the sole failure is the intentional
  `test_core_imports_nothing_outside_core` (bp-066's red-at-106). +9 vs bp-066's 1538 = the new
  bp-064 tests. Two-part green check ✓.
- Argless mypy: **69** (baseline held; 453 source files checked). ruff clean on all touched files.

**Deliverable committed `c3fef76`** (`feat(core): wire the chat clock — chatlog as observed-stratum
g1 chains (CS-4)`).

### SEAL — bp-064 COMPLETE (session-27, 2026-07-17)
Status → complete. cost.actual recorded (~85k opus, ratio ~0.57 — tightly pinned plan; dollar/
session/week deltas OWED, fold into the pending relay). Journal sealed to the fresh-agent bar.
**Downstream:** CS-6's formalization-lag instrument now has TWO of its three gates open (connectivity
tranche via bp-059 ✓; sensor+clock via bp-063+bp-064 ✓); it stays gated on the correlator's scoped
grant (CS-5, owner act) + uuid claim-identity. bp-061/062 re-mints (now core/graph) still pending.
