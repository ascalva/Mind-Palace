# Mind Palace

> A knowledge system built around a single question: what does it mean for a system to know _why_ it believes something?

It's deliberately limited in scope — it trades breadth of action for provability — with a formal structure that lets it reason about how its own knowledge holds together. Runs locally, core preserved. Built with the thing it's trying to understand.

## What it is

Mind Palace takes private notes and writing and represents them as a typed, layered graph rather than a pile of documents. On top of that graph sits an operator — one mathematical object in several guises — that turns the relationships between pieces of knowledge into things the system can compute over, test, and revise, instead of leaving them implicit.

The point isn't to produce answers. It's to produce answers that carry their reasons: where a belief came from, what it's allowed to affect, and whether it still holds.

## Design principles

A few ideas do most of the load-bearing work:

- **Make the wrong state unrepresentable, not merely discouraged.** Origin labels, capability limits, and the de-identification airlock are the same pattern — typed labels constraining flow, enforced by making the illegal flow impossible to express rather than by asking components to behave.
- **Read and write are separated by construction.** A read-only view into memory and a write-only view into the world are distinct objects; nothing that reflects can also act, by type.
- **Formalize only what earns it.** A type exists to delete an illegal state. Otherwise a docstring. Otherwise nothing.
- **The core is preserved; everything else is expendable.** The system is designed around what has to survive, not around what happens to be running.

## Architecture at a glance

- **Ambassador** — the reasoning layer you interact with. Computationally light, reaches for deterministic tools when exactness matters, and is plain about how much effort a given answer took.
- **Dreamer** — the offline layer that works over the structure of what's stored. The current frontier (see Status).
- **Store, and its two views** — memory, a read-only reflection of it, and a write-only path to external effect. The asymmetry is deliberate and enforced.
- **Provenance and scope** — every item carries its origin and what it's permitted to affect; flow that would violate either can't be represented.
- **Airlock** — a one-way path for outside research. De-identified on the way out, unable to reach back in.

## Status

The base build (Phases 0–10) is complete and running. Forward work is organized as tracks: senses, voice, the offline reasoning layer, world interaction, hardening, and testing.

The current frontier is the reasoning layer — moving the Dreamer from summarizing structure toward reasoning over it. That's the precondition for everything downstream, so it comes before breadth, not after.

An honest note on scope: the engineering rigor here governs _how_ outputs are produced — their provenance, their limits, whether they still hold. Whether the outputs are actually insightful is a separate question the reasoning layer has to earn against real use, not against provability alone. That gap is named on purpose.

## How it's built

Mind Palace is assembled by Claude Code (Opus 4.8), one verified phase at a time, against a fixed specification and a set of invariants it treats as inviolable. A human directs the architecture; the agent implements; each phase is a self-contained, verifiable unit; and the most dangerous capability — self-modification — is built last, after the scaffolding that constrains it exists.

The recursion is the point. It's a system for reasoning carefully about AI, built with AI, in the open.

Build mechanics — the operating rules, the master spec, and the append-only build log — live in `CLAUDE.md`, `docs/BUILD-SPEC.md`, and `docs/PROGRESS.md`.

## Running it

Local by design. It runs on your own hardware against a local model, with notes in Obsidian and the core backed up, encrypted. Nothing about it depends on a service staying up.

## Repository

- `CLAUDE.md` — operating rules loaded every build session. Start here.
- `CONSTITUTION.md` — the fixed directives every agent inherits.
- `CONVENTIONS.md` — engineering and security practice.
- `docs/BUILD-SPEC.md` — the full master specification.
- `docs/PROGRESS.md` — the build log, maintained across sessions.

## License

AGPL-3.0. You're free to use, study, and build on it; derivatives — including anything run as a hosted service — stay open under the same terms. Lineage preserved.
