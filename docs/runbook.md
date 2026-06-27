# Runbook

Operational notes for running and verifying the mind-palace. Grows per phase.

## Prerequisites (Phase 0)
- Python 3.11+ (built/verified on 3.14). Local venv at `.venv`.
- Ollama running on loopback (`127.0.0.1:11434`).
- Models: `qwen3.5:2b` (pinned, pulled). `qwen3.5:9b` / `qwen3.6:27b` are pulled as
  Phases 1–2 need them; `qwen3.6:35b-a3b` (stretch) already present.

## Setup
```
python3 -m venv .venv
./.venv/bin/pip install duckdb psutil pytest ruff
```

## Verify Phase 0
```
./.venv/bin/ruff check .
./.venv/bin/pytest -q              # full suite (skips live if Ollama down)
./.venv/bin/pytest -q -m "not live"   # logic-only, no Ollama needed
```
Gate: model responds; vitals flow into DuckDB; sealed core blocks external egress;
a trivial agent inherits the Constitution.

## Sealing — egress enforcement (Invariant 1)
The sealed core (`core/`) must have zero network egress. Enforcement is layered:

1. **In-process guard (`core.sealing`, active now).** `core.runtime.bootstrap()` calls
   `seal()` at startup, installing a fail-closed guard that permits only loopback
   connects (the local Ollama channel) and raises `SealedCoreEgressError` on anything
   else. Verifiable in tests. Fails closed, but a native extension opening its own
   socket could bypass a Python-level hook — hence layer 2.
2. **OS-level isolation (deployment hardening, TODO before any networked phase).**
   Run the core process under a `pf` anchor that denies outbound for its uid, or in a
   container/netns with `--network=none` plus a loopback path to Ollama. This is the
   structural guarantee the in-process guard approximates on bare macOS.

Edge (`edge/`, Zone B) is the only zone allowed to reach the network; the guard is
**not** installed there. Core↔edge communicate by filesystem handoff, never imports.

## Sandbox runtime — Podman machine (Phase 4) — ⚠️ KNOWN ISSUE, REVISIT

The Phase 4 sandbox (`core/sandbox/`) runs code in rootless Podman. On macOS Podman needs
a Linux VM ("podman machine"). The **logic gate is fully met by construction** — the
isolation profile is asserted on the argv (`tests/test_sandbox_policy.py`) and the
pool/broker behavior with a fake runner (`tests/test_sandbox_*.py`), all passing. What is
**not yet done is the empirical run** (`pytest -m podman`), because no podman machine would
stay up on this host (2026-06-25).

**Config written:** `~/.config/containers/containers.conf` sets `[machine] provider = applehv`,
`cpus = 2`, `memory = 2048`, `disk_size = 20`. Sizing is deliberately small so the VM does
not eat the model RAM ceiling (Invariant 8); the sandbox uses 256 MB containers, concurrency 1.

**What was tried and what failed:**
- **libkrun / krunkit 1.2.2 + podman 6.0** — guest Fedora CoreOS boots into **emergency
  mode** (a virtio-fs mount failure in the guest → SSH never starts → `connection refused`).
  Unusable here. (krunkit is installed from the `libkrun/krun` tap, tap trusted.)
- **applehv** — the **first** machine booted cleanly and a smoke test passed
  (`podman run --network=none python:3.12-slim …` → ok). After tearing it down to try
  libkrun and back, the **re-created** applehv machine fails with `vfkit exited unexpectedly
  (exit 1)` / ssh handshake reset — i.e. wedged machine/socket state from the churn, not a
  code problem.

**Current state:** no machine defined (cleaned up), no zombie `vfkit`/`krunkit`/`gvproxy`
procs, provider config left at `applehv`. Decent/idle.

**To come back (do this when revisiting):**
1. Fresh start: `podman machine init --now` (uses applehv from config). If `vfkit exited
   unexpectedly` recurs, try `podman machine reset` first, or reboot to clear stale state.
2. Pre-pull the image so the 10 s wall-clock timeout isn't spent pulling:
   `podman pull python:3.12-slim`.
3. Empirically verify isolation: `./.venv/bin/pytest -m podman`
   (network-off, vault-unreachable, non-root, timeout-enforced).
4. **Fallback if Podman stays broken:** Docker works on this host but its daemon is
   **rootful** (weaker than rootless Podman). To use it, add a `DockerRunner` alongside
   `PodmanRunner` (same `build_run_argv` flags — `docker run` accepts the same isolation
   flags except `--pids-limit` syntax is identical; drop `--security-opt no-new-privileges`
   only if unsupported) and set `[sandbox] runtime` accordingly. Treat rootful as a
   temporary measure; the isolation profile (no mounts, no net, caps dropped) still holds
   per-container. Revisit `--userns` for rootless-equivalent uid mapping.

## Vault watcher & sync (capture path, design-notes/vault-sync-and-capture.md)

How the owner feeds notes in and keeps embeddings current. **Two separable pieces:** the
**watcher** (code, core-side, local-filesystem only) and the **sync transport** (a separate
process — never the core). **Status: both operationally configured and live-verified
(2026-06-27)** on the owner's Mac (M2 Max) + iPhone — see `docs/PROGRESS.md` for the full
session log, including a concurrency bug found and fixed during verification.

### Watcher (code — runs locally, no network)
Re-ingests changed notes through the Phase-1 pipeline, idempotently (content-addressing):
unchanged = no-op, changed = re-embed, deleted = **tombstone** (derived dropped, raw kept).
```
./.venv/bin/python scripts/watch.py     # seals the core, then watches [vault].path
```
Real-time via `watchdog` (FSEvents) if installed (`./.venv/bin/pip install watchdog`); without
it the watcher **falls back to polling** every `[vault].watch_poll_interval_s`. Either way the
trigger just enqueues a background `vault_sync` job and the supervisor runs the idempotent
rescan — missed/duplicate events are harmless. It is core-side and reaches no network (the
import-lint proves it); only the local filesystem and local stores are touched.

`scheduler/queue.py`'s `JobQueue` connection is `check_same_thread=False` + `RLock`-guarded
specifically because the watcher's debounce timer and poll loop call `on_change` (→ `enqueue`)
from a thread they spawn, not the thread that constructed the queue. Without this, real-time
and polled triggers crash silently (swallowed by `threading`'s default excepthook) while
`launchctl`/`ps` still report the service healthy — caught + fixed 2026-06-27, see PROGRESS.md.

### Running the watcher as a launchd service (so it survives logout/reboot)
```
~/Library/LaunchAgents/com.mind-palace.watch.plist
```
`ProgramArguments` = the repo's `.venv` python + `scripts/watch.py`; `RunAtLoad`+`KeepAlive`
(10s `ThrottleInterval`); `PYTHONUNBUFFERED=1` (otherwise stdout buffers and the log looks
empty); logs to `data/logs/watch.{out,err}.log`.
```
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.mind-palace.watch.plist  # start
launchctl bootout   gui/$(id -u)/com.mind-palace.watch                              # stop
launchctl print     gui/$(id -u)/com.mind-palace.watch | grep state                 # status
tail -f data/logs/watch.out.log                                                     # live log
cat data/logs/watch.err.log                                                         # errors
```
To pick up a code change, `bootout` then `bootstrap` again (no separate "restart" verb).

### Sync transport (operational — a SEPARATE process, NOT the core)
Keeps the vault directory current across the owner's devices. The core only watches a local
folder; it never runs or talks to the sync daemon.
- **Configured: Syncthing over Tailscale** — peer-to-peer, device-to-device, encrypted, **no
  vendor in the path**. Mac: `brew install syncthing && brew services start syncthing` (GUI at
  `localhost:8384`, loopback-only). iPhone: **Synctrain** (free/OSS; Möbius Sync is the
  documented fallback if it ever stops working). The vault folder (id `mind-palace-vault`) is
  shared `sendreceive` between the two devices; a `.stignore` in the vault root excludes
  `.DS_Store`/`.stversions`/temp files from syncing.
- **Tailscale** is the private mesh: it gives the phone an encrypted path to the laptop, used
  for (a) Syncthing peer sync and (b) reaching the future interface gateway (Zone B) to
  chat-capture/query — matching the established "private default" interface posture.
- **Confinement — both ends, not just one.** Public/global discovery, relays, NAT-PMP/UPnP, and
  STUN are all disabled on **both** the Mac (Syncthing GUI → Settings → Connections) and the
  phone (Synctrain → Advanced Settings); each device's peer address is pinned to the other's
  **Tailscale IP** (`tcp://100.x.x.x:22000`) instead of left `dynamic`. This matters off-LAN: a
  one-sided pin still lets the *other* device fall back to a public discovery/relay server.
  **Verify in the Syncthing GUI:** click the phone device in the sidebar — the address shown
  must read the phone's Tailscale IP (`100.x.x.x`), never a relay name or a different subnet.
  Confirmed live over the phone's cellular connection (no LAN involved):
  `/rest/system/connections` reported `type: tcp-server` direct, not `relay-client`.
- **Vendor-transit tradeoff (flagged):** iCloud / Obsidian Sync are convenient but **transit a
  vendor** — the same class of tradeoff as the interface-transits-third-party invariant
  (Invariant 11). They move the owner's *own authored notes* through a third party (encrypted
  in transit, but the vendor is in the path). Syncthing-over-Tailscale avoids that entirely;
  the owner chooses, and the private option is recommended (and is what's configured).

### iOS capture (no third-party notes app)
Apple Notes' Share→Save-to-Files always names the export `text.txt` (auto-numbering on
collision) and can't produce a real `.md`. Use an iOS **Shortcut** instead: `Ask for Input`
(Text) → `Format Date` (input **Current Date** — not "Date Created") → `Save File` (saves the
*input text*; destination `Ask Each Time` — pick Synctrain → Mind Palace Vault; `Subpath`
`note-[Formatted Date].md`) → **`Rename`** (required — Shortcuts' `Save File` silently forces
the input's native `.txt` extension regardless of what's typed in `Subpath`; `Rename` to the
same `note-[Formatted Date].md` string fixes it). One tap from the home screen or share sheet.
After saving, Synctrain needs a manual **rescan** of the folder (pull-to-refresh) to push a
phone-authored file — iOS suspends its background watcher (see "Known Synctrain quirk" below).

### Known Synctrain quirk — reverse sync needs a manual rescan
A file created/edited *on the phone* often doesn't push to the Mac until Synctrain's
**Mind Palace Vault folder is manually rescanned**: open the folder in Synctrain and
pull-to-refresh (or use its Rescan action). Mac→phone sync doesn't need this — only
phone-originated changes are affected, because iOS suspends Synctrain's background
file-watcher. Forward sync (Mac edits → phone) is unaffected.

### True deletion — owner-gated purge (not the watcher's default)
A vault delete only **tombstones** (raw kept) so re-adds dedup and nothing is lost. To destroy
the raw bytes too (genuine privacy deletion), use the deliberate, irreversible purge — refused
unless `--confirm` is passed AND the content is held by no active note (tombstone it first):
```
./.venv/bin/python scripts/purge_raw.py --list                 # show purgeable (tombstoned) digests
./.venv/bin/python scripts/purge_raw.py <digest> --confirm     # destroy raw + derived for it
```

### Verify
- Edit a note → its embeddings update (search reflects the new content; old rows gone).
- Delete a note → it stops surfacing in search; raw blob is retained until a purge.
- Unchanged re-scan → no-op (no new digests, no duplicate rows).
- `./.venv/bin/python -m ops.import_lint` → green (the watcher reaches no network).
Cold-tested in `tests/test_vault_sync.py`, `tests/test_vault_watcher.py`,
`tests/test_purge_raw.py`, `tests/test_vault_sync_wiring.py`.

**Live-verified end-to-end (2026-06-27, real iPhone + Mac, not mocks):** a phone-authored note
(via the Shortcut above, over cellular) synced → watcher caught it automatically → embedded →
returned as the top semantic-search hit. Deleting a tracked note tombstoned automatically
(catalog inactive, vector rows dropped, `RawStore.exists(digest)` still `True`). A no-change
rescan returned `indexed=0` with the vector count unchanged. Full details + the concurrency bug
this surfaced (now fixed) in `docs/PROGRESS.md`'s 2026-06-27 entry.
