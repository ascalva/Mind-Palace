# Documentation index

Canonical map of every doc in the repo: what it is, whether it's current, and how it
cross-references. For the reading protocol (what to actually read for a given task), start at
[`ORIENTATION.md`](ORIENTATION.md) instead — this file is the index, not the entry point.

## Authority order

When docs conflict, higher wins:

**`CONSTITUTION.md` > `BUILD-SPEC.md` > `CONVENTIONS.md` > `design-notes/` > `research/`**

`PROGRESS.md` is state-of-the-world (a build log), never a spec — it records what happened, not
what should happen. `schema.md` and `runbook.md` are code-adjacent operational references, not
design authorities.

## Status legend

| Status | Meaning |
|---|---|
| current | live and accurate |
| realized | the parked design was built; note kept as rationale, not a build target |
| parked | not built; re-entry conditions stated in the note itself |
| draft | research-in-progress, not ratified |
| point-in-time | an audit/snapshot honestly dated, not meant to stay current |
| mostly-consumed | a builder prompt whose steps are mostly done; remaining steps still live |
| historical | superseded or complete; kept in `archive/` for the record |

---

## Root

| Doc | Category | Status |
|---|---|---|
| [`CLAUDE.md`](../CLAUDE.md) | authoritative-spec | current — operating rules, loaded every session |
| [`CONSTITUTION.md`](../CONSTITUTION.md) | authoritative-spec | current — **read-only fixed point, never edited** |
| [`CONVENTIONS.md`](../CONVENTIONS.md) | authoritative-spec | current — engineering & security practice |
| [`README.md`](../README.md) | index | current — public-facing overview |

## Core spec, state, and reference

| Doc | Category | Status |
|---|---|---|
| [`ORIENTATION.md`](ORIENTATION.md) | index / builder-facing | current — top-of-session card; the map and reading protocol |
| [`BUILD-SPEC.md`](BUILD-SPEC.md) | authoritative-spec | current — the full master specification |
| [`PROGRESS.md`](PROGRESS.md) | live-state | current — append-only build log, resume source. Phases 0–10 rotated to `archive/PROGRESS-phases-0-10.md`; this file now starts at the Forward layer |
| [`schema.md`](schema.md) | authoritative-spec | current — live data schema |
| [`runbook.md`](runbook.md) | authoritative-spec | current — operational procedures |
| [`ROADMAP-V1.md`](ROADMAP-V1.md) | live-state / builder-facing | current — forward-layer track sequencing and dependencies |
| [`MIND-PALACE-V1.md`](MIND-PALACE-V1.md) | authoritative-spec | current — v1.0 technical map (issued at the 10-phase completion) |

## The whitepaper / mathematics companion series

A deliberate numbered set — companions I–IV plus a shared glossary. Keep-separate: each is a
distinct layer (prose, formal models, invariant catalog, unified reframing), not redundant
copies. `NOTATION.md` is load-bearing — cited by ~15 code file headers as the symbol↔code join.

| Doc | Companion | Category | Status |
|---|---|---|---|
| [`WHITEPAPER.md`](WHITEPAPER.md) | I — prose | authoritative-spec | current, living document |
| [`WHITEPAPER-TECHNICAL.md`](WHITEPAPER-TECHNICAL.md) | formal models & figures | authoritative-spec | current |
| [`WHITEPAPER-FORMAL-PROPERTIES.md`](WHITEPAPER-FORMAL-PROPERTIES.md) | II — invariant catalog | authoritative-spec | current |
| [`REASONING-COMPLEX-MATHEMATICS.md`](REASONING-COMPLEX-MATHEMATICS.md) | III v0.2 — Dreamer math | authoritative-spec | current — supersedes `archive/WHITEPAPER-DREAMER-MATHEMATICS.md` (0.1) |
| [`REASONING-COMPLEX-BUILD.md`](REASONING-COMPLEX-BUILD.md) | III build spec | builder-facing | current — Track H (H1–H9) mostly built against this |
| [`MATHEMATICAL-REFRAMING.md`](MATHEMATICAL-REFRAMING.md) | IV — the five families | authoritative-spec | current — unified account, most of it since integrated |
| [`NOTATION.md`](NOTATION.md) | glossary | authoritative-spec | current — **load-bearing**, referenced from code headers |
| [`supplemental/math-spine-field-guide.md`](supplemental/math-spine-field-guide.md) | reference | draft-research | current — per-construct falsifiability guide, ties to Track L |

## Builder prompts & wiring

| Doc | Category | Status |
|---|---|---|
| [`BUILDER-PROMPT-FORWARD.md`](BUILDER-PROMPT-FORWARD.md) | builder-facing | current — **the canonical forward-layer prompt**, `CLAUDE.md` points here |
| [`BUILDER-PROMPTS-INTEGRATION.md`](BUILDER-PROMPTS-INTEGRATION.md) | builder-facing | mostly-consumed — R0–G3 executed; G4–G6 prompts still live |
| [`INTEGRATION-AND-WIRING.md`](INTEGRATION-AND-WIRING.md) | builder-facing | mostly-consumed — companion to the above; same live G4–G6 tail |
| [`WIRING-AUDIT.md`](WIRING-AUDIT.md) | historical / audit | point-in-time (2026-06-29) — a dated WIRED/DANGLING/FLAG-OFF snapshot; some DANGLING items closed since. Don't treat as current state, don't archive — an audit is inherently dated |

## Design notes (`design-notes/`)

Every note below was audited against the codebase on 2026-07-03 (read-only). Status is verified
against what is **actually built**, not against the note's own header — where a note's self-declared
status has gone stale, that is flagged. "Realized" = built (the note stays as rationale, not a live
target); "partial" = foundations built, remainder tracked; "parked/future" = not built, with the
re-entry condition stated in the note.

### Realized (built; note retained as rationale)

| Note | Track | Verified status & evidence |
|---|---|---|
| [`attestation-layer`](design-notes/attestation-layer.md) | security | Built — `core/attestation/{record,store,crypto,verify,attestor}.py`, Ed25519 + append-only store, `scripts/verify_attestation.py`. **Caveat:** `[attestation] enabled=false` here → live records are unsigned, dev keys only (`audits/prompt-integrity-audit.md` G5). |
| [`vault-runtime-auth`](design-notes/vault-runtime-auth.md) | security | Built — per-interaction scoped tokens (`config/secrets_backend.py` + factory mint); production Vault (kv + AWS engine) stood up. `[secrets] enabled=false`, `grant_roles` empty by default. |
| [`secrets-management-evolution`](design-notes/secrets-management-evolution.md) | security | Realized, then **superseded by `vault-runtime-auth`** (Vault as per-interaction auth, not just a multi-machine store). Kept for the Keychain-era rationale. |
| [`vault-sync-and-capture`](design-notes/vault-sync-and-capture.md) | ingest | Built + live — `core/ingest/{sync,watch,catalog,purge}.py`; Syncthing-over-Tailscale operational (runbook). |
| [`test-organization`](design-notes/test-organization.md) | testing | Built — `tests/` reorganized to the exact target tree (unit·integration·e2e·property·metamorphic·adversarial·integrity·emergent·longitudinal·quality + fixtures·keys). |
| [`dreamer-quality-suite-evaluation`](design-notes/dreamer-quality-suite-evaluation.md) | F (F9) | Built — `tests/quality/` bound to the real Dreamer/DerivedStore. Decoy-proxy + `g`-support-count caveats remain open in the note. |
| [`ambassador-as-reasoning-agent`](design-notes/ambassador-as-reasoning-agent.md) | B | Built — `agents/ambassador/` end-to-end. The **authoritative** Ambassador note; overrides the two older ones. |
| [`dreaming-v2-interpreter-panel`](design-notes/dreaming-v2-interpreter-panel.md) | dream R&D (R0/R1) | Built behind the flag — `core/dreaming/{graph,interpreters,adjudicator}.py`; `[dream_rnd] enabled=false`, live path still the Phase-7 Dreamer. Seed of the Track-H reasoning complex. |

### Partially realized (foundations built; remainder tracked)

| Note | Track | Verified status & what remains |
|---|---|---|
| [`holistic-testing`](design-notes/holistic-testing.md) | F | Most categories have populated homes (adversarial·metamorphic·property·integrity·emergent). **Longitudinal is thin** (1 file); the longitudinal + attestation-as-oracle-at-scale layers land with Track L / F4. |
| [`skills-and-scope`](design-notes/skills-and-scope.md) | factory | Scope ceiling + object-capability tools **built & enforced** (`core/factory/`, `PRE_DECLARED_MAX`). **Instructional-skill loading is dormant** — `RoleTemplate.skills` is declared but has no consumer (audit G4). Executable-skill catalog = Track G G4. Referenced from `core/factory/__init__.py`. |
| [`observed-data-and-the-assistant-tier`](design-notes/observed-data-and-the-assistant-tier.md) | D | **Firewall realized** — `OBSERVED` provenance exists (`core/provenance.py`), excluded from `MIRROR_READABLE`; Track G sensing already emits observed-tier. **Future:** the assistant tier, observed-ingestion pipeline, advisor agents. |
| [`nervous-system-and-ambassador`](design-notes/nervous-system-and-ambassador.md) | A/B | Ambassador front door (§4) **built** (Track B); recovery mode exists (`ops/lifecycle/`). **Unbuilt:** the async auditor (§2 = "A3") and the tamper tripwire/freeze (§1) — confirmed absent (audit G9.7). Ambassador framing superseded by `ambassador-as-reasoning-agent`. |
| [`alignment-subsystem`](design-notes/alignment-subsystem.md) | A | **Detection foundations built** — drift gauge A1 (`eval/drift.py`), `DerivedStore.reset()`, Curator prune-flagging. **Future:** structural detection (A2), the auditor (A3), gated surgery, alignment-steering self-mod. |
| [`wasm-sandbox-runtime`](design-notes/wasm-sandbox-runtime.md) | sandbox | ⚠️ **Note header is stale.** It says "design only, not implemented," but `WasmRunner` + `RoutingRunner` are **built** with a real wasmtime path (`core/sandbox/runner.py`; `build_runner` `wasm`/`routing` branches). **Dormant:** `available()=False` until a WASI `python.wasm` asset is placed → fails closed to Podman. Header wants a refresh to "runner built, asset-pending." |

### Parked / future (not built; re-entry condition in the note)

| Note | Track | Verified status & re-entry |
|---|---|---|
| [`hands-and-the-effector-layer`](design-notes/hands-and-the-effector-layer.md) | G | **Track G complete (structurally), flag-off** — G1–G7 built: types + gate (`ops/effects.py`, `ops/effect_gate.py`), catalog (`ops/effect_catalog.py`), sensing (`core/sensing.py`), reversible writes (`core/effect_proposal.py`, `edge/effectors/writes.py`, `ops/effect_ledger.py`), irreversible/JIT-credential (`ops/effect_exec.py`), blast-radius drift (`eval/effector_drift.py`). `[effectors] enabled=false`, wired ceiling ε=SENSING; acting classes cataloged but unreachable until ε is raised (§4). Value gated on Track H. |
| [`skill-mining-pipeline`](design-notes/skill-mining-pipeline.md) | G (G4) | Built — the §8 audit as a repeatable process (read untrusted → re-implement native → classify → mint scope → sandbox → attest → catalog+test), each step tied to its code artifact. The reviewed process for adding a hand. |
| [`observed-iot-and-cross-source-synthesis`](design-notes/observed-iot-and-cross-source-synthesis.md) | D | Future — the **correlator is absent** (no correlator module, no `core/ingest/biometric.py`). The `sensor_readings` slot exists (Phase 0, dormant). The Track-D capstone. |
| [`live-adoption-and-longitudinal-harness`](design-notes/live-adoption-and-longitudinal-harness.md) | L | Future — **every L-series artifact is absent** (`shadow.py`, `runledger.py`, `verdicts.py`, `complex/manifest.py`, `scripts/{review,tune}.py`, `eval/longitudinal.py`, `config/tuning.toml`). Prereqs `migrate_provenance_split.py --apply` + `ingest_self_knowledge.py` exist (owner-run). Gates Track G's value. |
| [`stability-adjudication`](design-notes/stability-adjudication.md) | dream R&D | Parked (flag-off). Interpreter-panel prereqs **landed** (`core/complex/{support,curvature,blocks,topology}.py`); its validation instrument — the Track-L L2 verdict store — is **absent**, so it stays parked. Cross-linked with `security-planes` §6. |
| [`recursive-strata`](design-notes/recursive-strata.md) | L successor | Parked; re-entry = Track L L4. ⚠️ **Its one authorized immediate action is undone:** §8 says reserve `DERIVED_STRATUM` (+ integer `depth`) in the provenance taxonomy *before* the migration relabels rows — `core/provenance.py` has no such label yet. Cross-linked with `security-planes` + `stability-adjudication`. Owner-edited this session. |
| [`recursive-dreaming-bounded-by-grounding`](design-notes/recursive-dreaming-bounded-by-grounding.md) | dream R&D (R3) | Future — recursion not built; gated on the drift gauge (now exists) + panel solidity. Largely **superseded as the formal treatment by `recursive-strata`**; retains the four safety rules the successor inherits. |
| [`dreaming-on-curated-graphs`](design-notes/dreaming-on-curated-graphs.md) | dream R&D (R5) | Future — `CuratedView` (its precondition) is **absent**. Build after R0/R1, in a deliberate R&D session. |
| [`dream-phase-rnd-charter`](design-notes/dream-phase-rnd-charter.md) | dream R&D | The charter for the R&D track: R0/R1 built (flag-off), R2–R5 future. `[dream_rnd] enabled=false`, not wired into cron. Referenced from `config/`. |
| [`roadmap-and-future-directions`](design-notes/roadmap-and-future-directions.md) | cross-cutting | Umbrella roadmap (2026-06-25). Several threads **landed** (provenance spectrum split, Phase-3 concurrency, Phase-9 backups, attestation/signatures); much remains future (assistant tier, multimodal, dashboards/Phase 11, multi-node). Superseded as *sequencing* by `ROADMAP-V1.md`; kept for the rationale ROADMAP-V1 omits. |

**Superseded framing, kept (not obsolete):** [`ambassador-interpretation-and-flow`](design-notes/ambassador-interpretation-and-flow.md) — Track B is built; its §1–4 interpretation/no-bottleneck analysis is valid, but the "thin dispatcher" framing is corrected by `ambassador-as-reasoning-agent` (the note self-flags this). Retained for the analysis.

**Audit summary:** of 24 design notes — 9 realized, 6 partially realized, 9 parked/future. None is obsolete. Two carry a stale self-status the index corrects above (`wasm-sandbox-runtime` header; `recursive-strata`'s undone `DERIVED_STRATUM` reservation); three carry explicit supersession relationships (`secrets-management-evolution`, `recursive-dreaming-bounded-by-grounding`, `ambassador-interpretation-and-flow`).

## Research (`research/`) & audits (`audits/`)

| Doc | Category | Verified status |
|---|---|---|
| [`research/security-planes.md`](research/security-planes.md) | draft-research | Draft, parked items with re-entry conditions. Three-plane composition (types · provenance · capabilities). **Foundation-file-set enumeration is blocking ratification on a repo verification pass** (§2); the Rust-via-PyO3 privileged-path split is parked with the default recorded; AEAD store-encryption parked; TLA+/Alloy + Hypothesis on the three invariants unscheduled. Candidate for promotion to `design-notes/`. Cross-linked with `recursive-strata`, `stability-adjudication`, `prompt-integrity-audit`. |
| [`research/un-represent-ability.md`](research/un-represent-ability.md) | reference/research | External literature survey on "make illegal states unrepresentable" (Rust · Haskell · seL4 · F* · effect systems) — the raw material that seeded `security-planes`. Background reference, not a spec; no re-entry condition. |
| [`audits/prompt-integrity-audit.md`](audits/prompt-integrity-audit.md) | audit (current) | Read-only audit (2026-07-02); **findings re-checked against code this session and still hold.** Threat A (injection-via-content): well-defended, structural, tested. Threat B (prompt/Constitution tampering): weak — only `CONSTITUTION.md` is fingerprinted, the blessed-anchor check is dormant in the live loop, the full-assembled-prompt fingerprint is OPEN, attestation signing is OFF, the A3 auditor/tripwire is unbuilt. Maps directly to future Threat-B hardening. Cross-linked with `security-planes` §2. |

## Planned but not yet written

Referenced from `ROADMAP-V1.md`, `MIND-PALACE-V1.md`, and `BUILDER-PROMPT-FORWARD.md` as forward
pointers for Track F (F1–F8); intentional, not dangling:
- `simulation-harness-and-reasoning-probes.md`
- `literary-interpretation-probes.md`

## Archive (`archive/`)

Superseded or historically-complete; moved here, never deleted.

| Doc | Superseded by / reason |
|---|---|
| [`HANDOFF.md`](archive/HANDOFF.md) | the security & attestation track it scoped is complete (`PROGRESS.md`, 2026-06-27) |
| [`PROGRESS-phases-0-10.md`](archive/PROGRESS-phases-0-10.md) | rotated out of the live `PROGRESS.md` (2026-07-03 docs cleanup) — the numbered-phase build log, verbatim |
| [`CLAUDE-current-phase-2026-07-03.md`](archive/CLAUDE-current-phase-2026-07-03.md) | verbatim snapshot of `CLAUDE.md`'s "Current phase" marker before it was trimmed to a 3-line pointer (2026-07-03 docs cleanup) |
| [`WHITEPAPER-DREAMER-MATHEMATICS.md`](archive/WHITEPAPER-DREAMER-MATHEMATICS.md) | superseded by `REASONING-COMPLEX-MATHEMATICS.md` (companion III v0.2) |
| [`math_proposals/gem_chats.md`](archive/math_proposals/gem_chats.md), [`math_proposals/gpt_chats.md`](archive/math_proposals/gpt_chats.md) | raw source-chat logs behind the mathematics companions |
