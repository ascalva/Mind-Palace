# Builder prompt — the forward roadmap (post-base-build)

The base build (Phases 0–10) is complete and live. This drives the **forward layer** —
six tracks (A–F) that take the system from built to fully realized. Hand to a fresh
builder session per work item; the order across tracks is the owner's choice, the order
*within* a track and the one cross-track dependency are not.

---

## The prompt (paste into a fresh builder session)

> **Fresh builder session — forward roadmap work item.**
>
> Re-ground per CLAUDE.md: read `docs/PROGRESS.md`, `CLAUDE.md`, `CONSTITUTION.md`,
> `CONVENTIONS.md`, `docs/MIND-PALACE-V1.md` (the v1 system map), `docs/ROADMAP-V1.md`
> (the track/dependency map), and the specific design note(s) for the item you are
> building. The ten numbered phases are DONE and live; this is forward-layer work, built
> as **tracks**, not numbered phases.
>
> **The owner will tell you which item (e.g. "A1 — the drift gauge" or "B2 — the
> Ambassador agent").** Build exactly that item. If none is named, propose the
> dependency-respecting default from `ROADMAP-V1.md` §"Suggested ordering" and ask.
>
> **Hold these, every item, without exception:**
> - **The seven principles (MIND-PALACE-V1 Part II)** — especially: model advises / code
>   acts; make illegal states unrepresentable (prefer a type that can't express the wrong
>   thing over a check that detects it); put each check at the lowest tier that can handle
>   it; the firewall (`observed` never feeds the mirror or baselines; the dreamer reads
>   `authored` only via `MirrorView`).
> - **The boundaries that never move (Part VII)** — the Constitution + golden set are
>   human-only; the core never egresses; no agent holds live send/pay credentials; every
>   outward action is gated; consequential advice defers.
> - **The verification discipline** — write tests as you build, in the right
>   `tests/<category>/` home (`test-organization.md`); the `integrity/` suite is a
>   non-skippable gate; new invariants get the right assurance tier (structural > static >
>   guard > property-test). Anything that touches the attestation chain or provenance is
>   `integrity/`.
> - **The build/owner boundary** — you write code, dev-mode/mock tests, policy-as-code,
>   and runbook docs. You do NOT run production Vault ops, apply Terraform, install
>   daemons, authenticate anything, or place production private keys. Those go in the
>   runbook for the owner to run.
> - **Checkpoint discipline** — each item is a checkpoint boundary: build, verify (report
>   test counts before/after), append a terse PROGRESS.md entry (built / verified /
>   owner-deferred / next), then STOP and hand off. Do not chain items in one session if
>   context tightens.
>
> **The one cross-track dependency that is NOT optional:** the **drift gauge (A1)** must
> exist before **recursive dreaming (R3 / C2)** is built. Recursion without the gauge is
> the documented self-amplifying-drift failure mode. If asked to build R3 and A1 is not
> done, STOP and surface it.
>
> **Feature flags stay as they are:** the dream R&D track is flag-OFF; self-mod is
> fail-closed OFF; nothing autonomously proposes. Building an item does not flip its flag
> — wiring into the live path / cron is a separate, deliberate, owner-approved step.
>
> **Per-item specifics:** the design note named in `ROADMAP-V1.md` for the item is the
> spec. Reconcile it against what is actually built before writing code; if the note
> conflicts with the live system, STOP and surface it rather than silently reconciling.
>
> When the item is built, verified, checkpointed — stop. The owner starts the next fresh
> session for the next item.

---

## Track → design-note quick map (for whoever drives the sessions)

| Item | Design note(s) |
|------|----------------|
| A1 drift gauge | `alignment-subsystem.md` §2,4; `WHITEPAPER-FORMAL-PROPERTIES.md` (G4) |
| A2 structural detection | `alignment-subsystem.md` §2 |
| A3 auditor agent | `nervous-system-and-ambassador.md` §2 |
| A4 tamper tripwire | `nervous-system-and-ambassador.md` §1 |
| A5 alignment-steering self-mod | `alignment-subsystem.md` §5 |
| B1–B5 Ambassador | `ambassador-as-reasoning-agent.md` (authoritative); `ambassador-interpretation-and-flow.md`; `nervous-system-and-ambassador.md` §4 |
| C1 R2 utility | `dream-phase-rnd-charter.md` |
| C2 R3 recursion | `recursive-dreaming-bounded-by-grounding.md` (after A1) |
| C3 R4 cross-source | `dream-phase-rnd-charter.md`; `observed-iot-and-cross-source-synthesis.md` |
| C4 R5 curated dreaming | `dreaming-on-curated-graphs.md` |
| D1 observed ingest | `observed-iot-and-cross-source-synthesis.md` §1 |
| D2 correlator | `observed-iot-and-cross-source-synthesis.md` §2 |
| D3 advisor agents | `observed-data-and-the-assistant-tier.md`; `skills-and-scope.md` |
| E1 podman gap | `runbook.md` → "Sandbox runtime" |
| E2 WASM sandbox | `wasm-sandbox-runtime.md` (after E1) |
| E3 voice | BUILD-SPEC §20.11 |
| E4 formal gaps | `WHITEPAPER-FORMAL-PROPERTIES.md` (G4/G9/G10/G11) |
| F1 synthetic corpora | `simulation-harness-and-reasoning-probes.md` §1b |
| F2 simulation harness | `simulation-harness-and-reasoning-probes.md` §1 |
| F3 mock-approver gate test | `simulation-harness-and-reasoning-probes.md` §1d |
| F4 drift trajectory asserts | `simulation-harness-and-reasoning-probes.md` §1c (after A1) |
| F5 logic-puzzle probes | `simulation-harness-and-reasoning-probes.md` §2 |
| F6 literary structural extraction | `literary-interpretation-probes.md` §4 (needs R5 CuratedView) |
| F7 literary grounding precision | `literary-interpretation-probes.md` §3,5 (THE architecture signal) |
| F8 literary theme recall | `literary-interpretation-probes.md` §6 |
| F9 dreamer quality suite (signal-vs-noise) | `dreamer-quality-suite-evaluation.md` (bind DreamerAdapter; THRESH joins harness tuning; wire rate_blind for the value claim) |

---

## PROGRESS.md — add a forward-roadmap pointer block

```markdown
## Forward roadmap (post-base-build, see docs/ROADMAP-V1.md)
Base build (Phases 0–10) COMPLETE + live. Forward layer organized as six tracks:
- A — The Senses: drift gauge → structural detection → auditor → tamper tripwire → alignment-steering self-mod.
- B — The Voice: the Ambassador — a reasoning agent that is computationally light (a mind that uses deterministic tools), read+propose, delegates heavy work, contextual updates (expected + earned interruptions), transparent about effort in plain language + text interaction.
- C — The Subconscious: dream R&D R2 (utility) → R3 (recursion, AFTER A1) → R4 (cross-source) → R5 (curated dreaming).
- D — The World: observed/IoT ingest → correlator → advisor agents (assistant tier; firewall holds).
- E — Hardening: close the podman empirical gap → WASM sandbox; optional voice; close formal gaps G4/G9/G10/G11.
- F — Testing & Tuning: synthetic corpora → simulation harness (trajectory asserts, mock-approver refusal) → logic-puzzle + literary probes (grounded interpretation = the grounding stress test). The baseline-tuning instrument.
Cross-track rule (non-optional): the drift gauge (A1) precedes recursive dreaming (R3/C2). All else is owner preference; the honest first move is to use the system. Full map: docs/MIND-PALACE-V1.md + docs/ROADMAP-V1.md.
```
