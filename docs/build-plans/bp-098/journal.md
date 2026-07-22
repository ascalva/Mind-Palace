# Journal — bp-098 (CI-wiring / Plan B: the code-ingest ENABLE path)

> Alive while the plan is proposed/in-progress; sealed on completion.

## 2026-07-22 — MINTED (graduation, session-42)

- **State:** `proposed`. Graduated from the ratified `dn-code-ingest-pipeline`'s deferred
  "owner-visible enable step" (§2.7), **warrant finding-0159** (the owner ruling: the ON switch
  is part of finishing — a capability with no way to turn it on is missing functionality, not
  "dormant by design"). This is "Plan B" from the session's chat.
- **Why it exists:** CI-1..4 (bp-092..094) shipped the code embed lane but with an INERT flag
  (`[code_ingest].enabled` read by nothing — no `CodeIngestConfig`), no daemon enqueue of the
  `code_sync` KIND, and no CLI. Flipping the flag did nothing; the only way to run the seed was a
  raw `build_code_corpus_sync().seed()` call. This plan builds the switch.
- **Grounding done at graduation** (so a builder inherits it): the engine (`code_corpus.py`) +
  KIND/handler/enqueue (`scheduler/code_sync.py`) are DONE (bp-092) — this plan only CALLS them.
  Pinned in §6: the `SelfModConfig` schema template (`loader.py:257`), the `build_components`
  handler dict + `_housekeeping` sibling (`enqueue_chat_sync`), and `Launcher.ingest_chat()` /
  `palace.py:245` as the CLI-triggered-enqueue precedent for `code-seed`. Two "code does not
  settle" items flagged (the loader assembly call shape; whether `ingest_chat` reaches a live
  queue) — builder reads + mirrors, never infers.
- **Scope discipline:** the seed stays owner-visible (§2.7) — housekeeping enqueues INCREMENTAL
  sync when `enabled`; the deliberate SEED is `palace code-seed`. This plan does NOT flip
  `enabled` on or run the seed (owner's runtime/deskcheck act).
- **Next action (on owner bless → ready):** `/build bp-098`; Items 1→2→3 (schema → daemon
  enqueue → CLI). After it, "turn on code ingest" is a real command through the proper discipline.
- **Blocking:** none. Awaiting the proposed→ready blessing (owner-only, by hand).

## 2026-07-22 — BUILT (session-43, orchestrator in-session under builder contract)

**Delegation note:** run IN-SESSION (not a separate worktree agent) — weekly budget 89% used
(resets Jul 24), and the full grounding was already loaded here, so a fresh builder re-loading
~150k of context did not fit the pre-flight budget gate. The banked delegation lessons still
applied (foreground pytest to completion; true scope; config-retrofit surface Q6).

**The two "code does not settle" items — SETTLED before writing (read + mirrored, never inferred):**
- **Q3 (loader assembly shape):** `sm = raw.get("selfmod", {})` (`loader.py:363`) + the
  `selfmod=SelfModConfig(enabled=bool(sm.get("enabled", False)), …)` construction (`:500`). Mirrored
  exactly for `code_ingest`.
- **Q5 (does the CLI reach a LIVE daemon queue?):** `ingest_chat()` does NOT enqueue — it runs
  `build_chat_sensor(cfg).sync()` DIRECTLY in-process (a standalone one-shot). But the `JobQueue` is
  on-disk SQLite (`scheduler/queue.py:122`, `path: Path`), so it is **durable + cross-process**: a
  fresh CLI process can INSERT a `code_sync` row that the running daemon's supervisor drains. That
  is *cleaner* than mirroring ingest_chat's direct-sync (which would be a raw store write from the
  CLI, violating Item 3's single-writer invariant). So Item 3 was NOT the §10 stop-and-raise —
  `code_seed()` enqueues via the shared queue, mirroring the `:739` `JobQueue(cfg.paths.data_dir /
  "queue.sqlite")` precedent. Item 3 shipped (not parked).

**What landed (all three items, linear 1→2→3):**
- **Item 1 — `CodeIngestConfig`** (`core/kernel/config/loader.py`): frozen dataclass
  `{enabled=False, max_chars=1200, overlap_chars=150}` beside `SelfModConfig`; a `Config.code_ingest`
  field (default_factory); `ci = raw.get("code_ingest", {})` + the assembly beside `selfmod=…`.
  `config/defaults.toml` inert-comment corrected (the block is now schema'd; still `enabled=false`).
  ✔ default reads `False/1200/150`; a local.toml `[code_ingest] enabled=true` overlay → `True`.
- **Item 2 — daemon enqueue** (`ops/lifecycle/launcher.py`): `CODE_SYNC_KIND:
  code_sync_handler(build_code_corpus_sync(cfg))` registered UNCONDITIONALLY in the `handlers` dict
  (consistent with vault_sync's eager store-open — verified `build_vault_sync`/`build_components`
  already open the vector store at startup; code_sync adds only a git rev-parse). `_housekeeping`
  gains `if cfg.code_ingest.enabled: enqueue_code_sync(queue, router)` — INCREMENTAL only, gated.
  ✔ enabled=True → housekeeping enqueues exactly one `code_sync`; enabled=False → none; handler
  registered either way.
- **Item 3 — `palace code-seed`** (`scripts/palace.py` dispatch+USAGE, `Launcher.code_seed()`):
  inserts ONE `code_sync` job onto the shared supervisor queue (single-writer: a job insert, never a
  store write), returns 0, and messages clearly whether a daemon is live to drain it (`run.active`)
  or the durable queue holds it until `palace start`. ✔ unit test asserts one queued `code_sync`;
  USAGE renders `code-seed`. **Did NOT fire a real seed** — the running daemon is on the old commit
  (no `code_sync` handler), and running the seed is the owner's deskcheck act (§9 non-goal, §10).

**Tests:** `tests/unit/test_code_ingest_wiring.py` (new, 5 tests — all three items). `build_components`
proven to run offline (embedders build lazily; temp stores) so the wiring is exercised for real,
not mocked. `test_config_split.py` (K1's, carried for Q6): unchanged + green — no config-shape
assertion reddened.

**Gate:** ruff ✔ · import-firewall ✔ · mypy (source 3 files, 0 errors; test file 0 — one
`# type: ignore[attr-defined]` on `.supervisor.handlers`, the SupervisorLike protocol hides the
concrete attribute; tests baseline unchanged) ✔ · ops.type_gate ✔ · full green-gate pytest:
**1907 passed, 3 failed, 8 skipped, 21 deselected** (168s). No engine/KIND change (bp-092's,
untouched); `enabled` stays `false`; no φ_code change.

**The 3 failures are PRE-EXISTING and NOT bp-098 → filed finding-0160.** They are in
`tests/unit/test_provenance_tags.py` (mypy-error-line assertions over `provenance_fixture.py`);
under the installed **mypy 2.2.0** the emitted diagnostics drifted (the mirror-bypass case now
collects 0 errors where 2 are expected — possibly a real weakening of the type-level MIRROR guard,
flagged for the fix session). PROVEN pre-existing: stashed all bp-098 changes, ran the three on
clean HEAD → fail identically; none of `test_provenance_tags.py`'s imports touch bp-098's files.
bp-098's own 5 tests + everything else it bears on are green.

## 2026-07-22 — SEALED (session-43), status in-progress→complete

- **Acceptance:** all three items' acceptance tests pass (Item 1 default-OFF + local override;
  Item 2 handler-registered + housekeeping-gate; Item 3 one-queued-code_sync + USAGE). Falsifiers
  checked: gate does NOT enqueue when `enabled=False`; housekeeping does NOT auto-seed (incremental
  only); `code_seed()` enqueues (never a raw CLI store write).
- **§10 stop-and-raise NOT hit:** the `ingest_chat`-vs-live-queue ambiguity resolved in favor of the
  durable-queue enqueue (Item 3 shipped, not parked). No config test forced a semantic Config-shape
  change. No pressure to flip `enabled`/run the seed was accepted.
- **Cost:** ~110k opus, ~0.55× estimate (well-pinned; grounding pre-loaded at graduation). Run
  in-session (not delegated) on the pre-flight budget gate — weekly 89% used.
- **This is the ENABLE PATH, NOT a deskcheck.** Turning it on — flip `[code_ingest].enabled=true`
  and/or run `palace code-seed`, then prove it actually ingests HEAD `.py` — remains **owner-owed**
  ([[deskcheck-discipline]], [[wiring-is-part-of-finishing]]). Note that the SEED run also owes a
  φ_code re-projection consideration at next deploy (carried on the code-ingest track, not here).
- **Follow-through owed by the code-ingest track (not this plan):** the deliberate seed run that
  proves ingest (f-warrant: finding-0159) + integrator densification (f-0151) + the bp-094
  reference-edge patterns gate (`ENABLED_L2B_PATTERNS`, needs F-CI6 samples). bp-098 delivered the
  SWITCH; flipping + proving it is the next, owner-visible act.
