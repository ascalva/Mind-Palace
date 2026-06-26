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
