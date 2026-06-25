# Mind-Palace — Personal AI System

A sealed, offline-first personal AI: it indexes your private notes and reflects patterns back, with a gated agent layer, a dynamic agent factory, a pluggable text interface, and a one-way research airlock. Single-user, self-hosted, built to expand over time. Designed to be built by **Claude Code (Opus 4.8), one verified phase at a time**.

## Files (this is the repo root)
- `CLAUDE.md` — operating rules the builder loads every session. **Start here.**
- `CONSTITUTION.md` — the fixed-point directives every agent inherits.
- `CONVENTIONS.md` — engineering & security practice.
- `docs/BUILD-SPEC.md` — the full master spec (20 sections, 11 phases).
- `docs/PROGRESS.md` — append-only build log the builder maintains across sessions.
- `scripts/keep-awake.sh` — prevent sleep during long builds.

The builder creates the rest of the tree (`core/`, `edge/`, `cloud/`, `agents/`, `scheduler/`, `ops/`, `eval/`, …) in Phase 0.

## Prerequisites
- **Claude Code** with **Opus 4.8** — the builder.
- Runtime toolchain, installed as phases need it (Phase 0 sets up the base): Python 3.x, Ollama, Podman or Colima, Terraform + AWS credentials, restic. You don't need all of it on day one.

## Keep the Mac awake (clamshell on Thunderbolt)
Clamshell on AC power with an external display/input attached stays awake by default. **Screen lock, screensaver, and display sleep do not stop compute — only *system sleep* does.** So you only need to prevent system idle sleep.

Run your build session under `caffeinate`, so the Mac stays awake for exactly as long as the build runs:
```
caffeinate -ims claude
```
`-i` no idle sleep · `-m` no disk sleep · `-s` no system sleep on AC. The display still sleeps normally. (`caffeinate -i` alone usually suffices.)

For an unattended / long-running setup, hard-disable sleep on AC and revert when done:
```
sudo pmset -c disablesleep 1     # disable sleep on charger
sudo pmset -c disablesleep 0     # re-enable later
```
Or use the script: `./scripts/keep-awake.sh` (awake until Ctrl-C) or `./scripts/keep-awake.sh -- <command>` (awake only while the command runs).

**Power caveat:** under sustained local-LLM load an M2 Max can draw more than some Thunderbolt docks supply, so the battery can slowly drain even while "plugged in." Use a high-wattage charger/dock (Apple 96W+ or a dock with strong power delivery) for long runs.

## Start the build
1. `cd` into the repo and launch Claude Code (under `caffeinate` as above).
2. Paste this as your **first message**:

> Read these four files in full: `CLAUDE.md`, `docs/BUILD-SPEC.md`, `CONSTITUTION.md`, `CONVENTIONS.md`. Confirm in 3–4 sentences that you treat the Hard Invariants (BUILD-SPEC §3) and the Constitution as inviolable. Then list the §20 decisions you need from me to begin Phase 0, with your recommended default for each, and stop — do not write code yet. We build one phase at a time: when I approve, build only Phase 0, verify it against the Phase 0 gate, append a terse entry to `docs/PROGRESS.md`, update the Current-phase line in `CLAUDE.md`, then stop and report. Do not begin Phase 1 until I say so. Reference files rather than pasting them back.

3. Answer its §20 questions, approve, and let it build Phase 0. **Start a fresh session for each subsequent phase** so the builder stays within its own context budget.

## Why phase-by-phase
The spec is split so the builder loads a lean `CLAUDE.md` every session and pulls the full spec only when needed; each phase is a self-contained, verifiable unit; and the most dangerous capability (self-modification) is built last, after its safety scaffolding exists.
