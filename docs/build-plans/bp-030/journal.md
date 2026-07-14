# bp-030 journal

## 2026-07-13 — authored `proposed` (orchestrator)

Authored directly from `docs/brainstorms/lifecycle-cli-overhaul.md` + finding-0066 (concrete
ops/infra — no ratified design note needed). Scope: the operational-control + cleanup + status
unit of the lifecycle overhaul — Item 1 `down`/`up`/`restart` (KeepAlive-aware `bootout`/`bootstrap`,
so maintenance-down ≠ operational-stop, finding-0066), Item 2 remove the dead edge monitor
(dormant, `enabled=false`, never worked; owner redoes it later), Item 3 enrich `status`.

§3 grounded against this session's read-only recon (citations inline): the KeepAlive/bootout
semantics (`com.mind-palace.palace.plist` header); the monitor is dormant + its ONLY child-model
caller (`launcher.py:238-243`); **`snapshot.build_status` already assembles the rich status dict** →
Item 3 reuses it (the "repurpose the snapshot" insight); `children.py`/`snapshot.py` are KEPT (dormant
+ reused, not deleted — avoid churn for the future dashboard redo).

**write_scope lists its 3 test paths** (finding-0072/0071 discipline applied at authoring):
`test_lifecycle.py` (extend) + `test_lifecycle_control.py` (Item 1) + `test_status_report.py` (Item 3).

The **diagnostic** subcommand is a SEPARATE plan (bp-031), fully scoped in the brainstorm (fixed-point
integrity · store/firewall health · ingestion freshness+completeness · runtime/drift · `--deep`).
bp-031 reuses this plan's enriched `status`/`build_status` seam → sequence bp-030 first.

Model estimate opus/300k (invariant-adjacent `launcher.py` + a Zone-B deletion; falsifiers need
judgment). Awaiting the owner-only `proposed → ready` blessing. No work started.

## 2026-07-14 — blessed + recon complete; PARKED (owner pivoted the session)

Owner blessed `proposed → ready` in-session; orchestrator committed the flip (`81ab7aa`) and flipped
`ready → in-progress`. Read the full §2 context manifest (palace.py, launcher.py, plist, snapshot.py,
children.py, config/loader.py, defaults.toml, edge/monitor/**, test_lifecycle.py + the two monitor
test files). **No code written.**

**Blast-radius analysis (Item 2 — monitor removal):**
- Codebase sweep for `edge.monitor` / `MonitorConfig` / `cfg.monitor` importers → **no NON-monitor
  importer** (§10 stop-and-raise does NOT fire). All hits are monitor-internal or the launcher spawn.
- **`snapshot.build_status` / `write_status`** (Item 3's seam) confirmed self-contained in
  `ops/lifecycle/snapshot.py` — KEEP unchanged, as planned.
- **WRITE_SCOPE GAP → finding-0075 (open, owner-gated):** `tests/unit/test_monitor_server.py`
  imports `edge.monitor` and reds on deletion, but is NOT in write_scope. Item 2 cannot complete
  *green* until the owner hand-adds that path. `tests/integration/test_monitor_snapshot.py` SURVIVES
  (imports `edge.interface`, not `edge.monitor`; tests the retained snapshot seam) — no scope change
  needed, only a cosmetically-stale name.

**Re-entry (fresh-agent sufficient):**
- Items **1** (`down`/`up`/`restart`) and **3** (enrich `status`) are unblocked — resume and build them
  from §7 as pinned; Item 3 reuses the retained `build_status` (construct ops_view/dreams_view/queue
  depth inside `status()`, which today has no Components — see §6 interfaces).
- Item **2** (monitor deletion) is BLOCKED on finding-0075: owner must add
  `tests/unit/test_monitor_server.py` to write_scope, THEN delete `edge/monitor/**` +
  `scripts/monitor.py` + `test_monitor_server.py` together, remove `MonitorConfig`/`[monitor]`, and
  strip the launcher monitor-spawn + monitor-path `write_status` call. Do Item 2's deletion LAST so
  the suite never goes red mid-build.
- Full attestable-green gate (5 legs) before any commit; blast order remains 2 → 1 ∥ 3, but 1 & 3 can
  land first while 2 waits on the scope grant.

Parked to run an owner-directed **Fable design pass on the edge-dynamics design note** (session pivot,
2026-07-14). `active-plan` cleared; `/resume bp-030` re-points and continues.

## 2026-07-14 — Items 1 & 3 BUILT + verified; Item 2 stays PARKED (finding-0075)

Resumed from the journal (fresh-agent test passed — no re-derivation needed). Built the two unblocked
items; Item 2 (monitor deletion) remains blocked on the owner write_scope grant.

**Item 1 — `down` / `up` / `restart` (KeepAlive-aware control).** `ops/lifecycle/launcher.py`:
- Module fn `_run_launchctl(argv)` (captures output) + two injectable Launcher fields: `launchctl`
  (the runner) and `installed_plist` (the LaunchAgent path) — one seam, so tests drive bootout/
  bootstrap with a fake and no real launchd contact.
- `down()` = `launchctl bootout gui/$uid/<label>` (true maintenance-down, outlasts KeepAlive —
  finding-0066); idempotent (already-out → report, rc 0); not-installed → falls back to plain `stop`
  (no KeepAlive to outlast). `up()` = `bootstrap gui/$uid <plist>`; idempotent; not-installed → guided
  message, rc 0. `restart()` = plain down→up (NOT `deploy` — no git/gate/HEAD promotion; falsifier held
  structurally: the path only calls down/up).
- `scripts/palace.py`: dispatch (`down`/`up`/`restart`) + USAGE + docstring.
- Tests `tests/integration/test_lifecycle_control.py` (8): the exact incantations, both idempotency
  reports, both not-installed fallbacks, and a real-bootout-failure → non-zero.
- **Deliberately did NOT run `down`/`up`/`restart` live** — they mutate the real launchd agent (which
  is UP: `status` shows run #20 RUNNING on 4500d42; the resume brief's "daemon is down" was stale, the
  owner already bootstrapped it). Unit-verified only, by design.

**Item 3 — enrich `status`.** `ops/lifecycle/launcher.py`:
- Added the **running-vs-HEAD gap** (compares the live run's `commit_sha` to `git_state(HEAD)` — the
  finding-0066 deploy-lag, made visible) and `_report_snapshot()`, which opens the SAME read-only views
  the edge-monitor snapshot fed (`OpsView`/`DreamsView`/`JobQueue`) and pretty-prints `build_status`:
  queue depth, RAM headroom, drift, constitution, dream + tidy counts, action activity. Read-only —
  `snapshot.py` untouched (reused as pinned).
- Switched `status()`'s preflight to the injectable `self.preflight_fn` (start() already used it;
  default is `run_preflight`, so production behavior is identical) → status is now hermetic/fast to test.
- **Falsifier tension noted:** Item 3's acceptance wishlist names "last-dream + resident-model lines,"
  but `build_status` provides *dream count* and *memory headroom*, not dream text or a model list. The
  falsifier ("must NOT fabricate a field build_status doesn't provide") is the binding constraint → I
  show only what traces to `build_status`/ledger/git. No finding — resolvable within the plan.
- **End-to-end verified on the REAL system:** `uv run scripts/palace.py status` → the HEAD-gap line
  fired (run #20 4500d42 behind HEAD fc34761-dirty), `dreams: 1` (matches the bp-036 body-only result),
  `queue depth: 34`, rc 0, no writes. `drift`/`constitution` render `None` — honest: the daemon's own
  snapshot binds neither on `OpsView.over(...)` either, so status matches it exactly (not a fabrication).
- Tests `tests/integration/test_status_report.py` (5): HEAD-gap warning, running-HEAD-when-current,
  the snapshot lines, read-only (two calls → no new run), no-runs-yet.

**Gate (5-leg attestable-green): GREEN.** ruff clean · `mypy core agents eval ops scheduler scripts` = 0
(185 files) · argless `mypy` = **69** (baseline held) · `ops.type_gate` OK · `pytest` = **1108 passed**,
8 skipped, 2 failed — both failures are `pytest.mark.live` (`test_scheduler_live` + `test_dream_v2_live`),
which the attestable gate DESELECTS (`-m "not live and not podman and not needs_vault and not needs_restic"`
→ 1098 collected, 20 deselected). Neither live test imports launcher/palace/status — they fail on the
loaded, low-RAM box (status reported 2.42 GB available with the daemon live), environmental not a
regression. The 13 new non-live tests + the extended `test_lifecycle.py` are all in the passing set.

**Re-entry — Item 2 (monitor deletion) still PARKED.** Blocked on **finding-0075**: the owner must add
`tests/unit/test_monitor_server.py` to this plan's `write_scope` (correcting a blessed plan's
write_scope is owner-gated — standing rule). Re-entry condition: that grant lands → then delete
`edge/monitor/**` + `scripts/monitor.py` + `test_monitor_server.py` together, remove `MonitorConfig` +
`[monitor]` (`config/loader.py` + `defaults.toml`), and strip the launcher monitor-spawn + the
monitor-path `write_status` call (launcher.py `build_components` :236-253 + the `snapshot=` wiring).
Do Item 2's deletion LAST so the suite never reds mid-build. `build_status`/`children.py`/`test_children.py`
SURVIVE (KEEP). Plan stays `in-progress` until Item 2 lands — this session commits Items 1 & 3 only.

## 2026-07-14 — Item 2 BUILT (owner granted finding-0075) — bp-030 COMPLETE

**Owner granted the finding-0075 write_scope correction in-session** (AskUserQuestion). Added
`tests/unit/test_monitor_server.py` to `write_scope` (plan front-matter, with the grant note);
finding-0075 → **resolved**. Then built Item 2.

**§10 stop-and-raise check:** a full grep (`edge.monitor` / `MonitorConfig` / `cfg.monitor` /
`scripts/monitor`) over core/agents/eval/ops/scheduler/scripts/config/edge/tests found ONLY
monitor-internal references — **no non-monitor importer**, so the deletion is safe (as the prior
blast-radius analysis predicted).

**Removed (Item 2):**
- Files (`git rm`): `edge/monitor/{__init__,page,server}.py` (+ empty dir removed), `scripts/monitor.py`,
  `tests/unit/test_monitor_server.py`.
- `config/loader.py`: the `MonitorConfig` dataclass, the `Config.monitor` field, the `mon =
  raw.get("monitor")` binding, and the `monitor=MonitorConfig(...)` construction in `load_config`.
- `config/defaults.toml`: the `[monitor]` section.
- `ops/lifecycle/launcher.py` `build_components`: the whole edge-monitor block — the `write_snapshot`
  closure (+ its `write_status`/`build_status`/`OpsView`/`DreamsView`/`open_*` local imports and the
  `ops_view`/`dreams_view` it built) and the `if cfg.monitor.enabled:` child spawn; the return no
  longer passes `children=`/`snapshot=`.

**KEPT (as pinned):** `ops/lifecycle/snapshot.py` UNCHANGED (out of write_scope; `build_status`
retained, now feeds `status` via Item 3; `write_status` stays for the future dashboard redo).
`ops/lifecycle/children.py` + `tests/unit/test_children.py` dormant. The `Components.children` /
`.snapshot` fields KEPT (defaults: empty list / no-op) — the dormant seam a future dashboard re-wires;
their comments updated to say so. `tests/integration/test_monitor_snapshot.py` untouched (imports
`edge.interface` + the retained snapshot, never `edge.monitor` — survives; only its NAME is cosmetically
stale, noted in finding-0075 for a later cleanup).

**Falsifier held:** no dangling `edge.monitor`/`cfg.monitor` import (grep = NONE; mypy typed = 0);
`build_status`/`children.py` both still import (asserted in the new test). New test
`test_dead_edge_monitor_is_removed` in `test_lifecycle.py`: no `MonitorConfig`, no `.monitor` on cfg,
`build_status`+`Child` still importable. Verified live: `load_config()` succeeds, `build_components`
imports clean.

**Gate (5-leg) after Item 2: GREEN.** ruff clean · `mypy core agents eval ops scheduler scripts` = 0
(184 files — `scripts/monitor.py` gone) · argless `mypy` = **69** · `ops.type_gate` OK · `pytest` =
**1106 passed, 8 skipped, 0 failed** (10m07s — the 2 live e2e tests that flaked on the loaded box in
the Items-1&3 run both PASS now; no monitor tests remain to red the suite). bp-030 is **COMPLETE** —
all three items landed; status flipped `in-progress → complete` (orchestrator non-blessing flip).
