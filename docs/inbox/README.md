# The inbox — documents pending the owner's signature

Owner ruling (2026-07-11): this directory is the **signing desk**. Everything here awaits
exactly one thing — the owner's approval, rejection, or answer. Nothing here is in force.

The contract:

- **The orchestrator delivers here** what it cannot enact: proposed design notes (the
  agent cannot write `docs/design-notes/**`), proposed amendments (paste-ready), and
  batched questions (`owner-questions.md`, the standing file).
- **The owner signs by hand** — a status flip, a paste-and-commit, an answer line. The
  signature IS the act; no agent performs it, ever (§10; the two blessing gates).
- **After signature** the orchestrator sweeps: proposals move to their real home and the
  inbox copy is deleted; answered questions fold back to their origin artifacts; findings
  flip `promoted`. The inbox trends toward empty — a non-empty inbox is the to-sign list,
  nothing else.

Currently this holds: `owner-questions.md` (standing), plus any
`proposed-*` files in flight.
