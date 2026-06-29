# The Mind Palace — v1.0 Forward Roadmap

**Status:** v1.0 roadmap, updated 2026-06-28 (adds Track F — Testing & Tuning). The ten
numbered phases are done; the system is live. This orders the **forward layer** — the work
that takes the system from "built" to "fully realized." Order within a track matters; order
*across* tracks is the owner's choice. Every item has a design note; this document is the
sequencing and dependency map, not the rationale.

**Before anything: the honest first move is to *use the system*.** Feed it, live in it,
and let real use tell you which track earns priority. Nothing below is blocked by anything
above except where a dependency is stated.

---

## The six tracks

| Track | What it completes | Gating dependency |
|-------|-------------------|-------------------|
| **A — The Senses** | Alignment detection + the auditor | The attestation chain (✅ built) |
| **B — The Voice** | The Ambassador + text interaction | The interface gateway, pinned tier (✅) |
| **C — The Subconscious** | Dream R&D R2–R5 | The drift gauge (Track A) for R3 |
| **D — The World** | Observed/IoT + the correlator | Vault scopes (✅), `sensor_readings` (✅) |
| **E — Hardening** | WASM sandbox; close the empirical gaps | The Podman empirical gap closing |
| **F — Testing & Tuning** | Simulation harness + reasoning probes | Drift gauge (A1) for trajectory drift asserts |

---

## Track A — The Senses (alignment detection + auditor)

Phase 10 built the *actuator* (gated propose→validate→rollback). This track builds the
*senses* that tell it when to act. **Highest-value next track** because it makes
everything else observable and safe to grow.

- **A1 — The drift gauge.** Realize the §15 drift metric `D(t) = d(μ(s_t), B)` against the
  frozen anchor + the Constitution-conformance audit. Choose the normalized metric over
  the mixed profile space and the tolerance band Θ (open question in
  `alignment-subsystem.md` §4 / G4). *Prereq for R3 recursion AND Track F drift asserts.*
- **A2 — Structural detection.** Min-cut-to-authored (grounding strength), community
  detection (echo-chamber bubbles), depth/grounding distributions over the interpreted
  graph. Emits the **alignment report**. Detection only — alters nothing.
- **A3 — The auditor agent.** Separate role, narrow scope (read attestations + Vault audit
  log, raise findings, no write). Trough-scheduled. Walks the attestation chain: every
  derived record traces to authored leaves; no dreamer attestation references observed;
  fingerprints consistent; signatures hold. Findings feed A4.
- **A4 — The tamper tripwire.** Graduated, provenance-aware: regenerable-layer breach →
  quarantine + reset-from-raw (automatic); fixed-layer breach → fail-closed freeze
  (`--recovery` launch state) + owner notification. (`nervous-system-and-ambassador.md` §1.)
- **A5 — Alignment-steering self-mod.** Once A1–A2 exist, extend the Phase-10 lever set so
  the gate can accept changes that *reduce* drift within the tolerance band (prune bubbles,
  re-tune decay) — still gated, still validated. (`alignment-subsystem.md` §5.)

Design notes: `alignment-subsystem.md`, `nervous-system-and-ambassador.md`.

---

## Track B — The Voice (the Ambassador)

The day-to-day way the owner interacts. Mostly assembly — the substrate is built.

- **B1 — The interface gateway path.** Activate text interaction over Tailscale (Zone B
  gateway → pinned-tier Ambassador). Conversations stored as `authored-dialogue`.
- **B2 — The Ambassador agent.** Pinned tier; the intent classifier (deterministic floor
  first, model earned for ambiguous cases); the three inline paths
  (retrieve / status / capture) + the one delegated path (task → gate → queue).
- **B3 — The operational-introspection read scope.** A read handle over
  attestations/gate-ledger/drift so the Ambassador can narrate system state. Read-only;
  never mutates the audit layer.
- **B4 — The self-knowledge graph.** Ingest the white papers + design notes as a `curated`
  graph (own graph, firewall-preserved) so the Ambassador can explain its own architecture
  — never exposing live secrets/keys.
- **B5 — Selective per-turn retrieval.** Agent-judged retrieval *within* the §13 budgeter
  ceiling — the Ambassador chooses what to pull; the budgeter bounds how much. (Not a fixed
  per-turn recipe; the one real bottleneck risk, capped.)

**Refinements (apply across B2–B5):** the Ambassador is a **reasoning agent that is
computationally light**, not a shallow classifier — a mind that *uses* deterministic tools
(solver, graph queries, grounded retrieval) when thinking needs exactness. Cadence/history
are its own judgment within the budgeter bound. Updates are **contextual** — expected
updates + earned interruptions only, never noise. It is **transparent about effort in plain,
non-technical language** ("let me dig through your notes and cross-check"), backed by the
introspection scope (B3) + the attestation line, not a new capability. Two small build
deltas: an **effort-narration** surface (plain-language "I need to go work on this") and an
**earned-interruption policy** (surface a topic unprompted only when the owner would want it
raised; owner-tunable, default "earned only").

Design notes: `ambassador-as-reasoning-agent.md` (authoritative — supersedes the
"thin dispatcher" framing where they differ), `ambassador-interpretation-and-flow.md`,
`nervous-system-and-ambassador.md` §4.
*Dependency:* B3 reads the attestation layer (✅). Mild synergy with A2/A3, not blocked.

---

## Track C — The Subconscious (dream R&D R2–R5)

Behind the feature flag, in deliberate R&D sessions. R0/R1 already built. **Build in order;
R3 is gated on Track A.**

- **C1 — R2: utility telemetry.** Per-dream usage as a *separate* axis from grounding;
  ranking uses both, never collapsed (the anti-flatterer rule).
- **C2 — R3: recursion, bounded.** Dreams as scaffolding input with depth tagging +
  confidence decay + grounding-terminates-in-authored. **Build only after A1 (the gauge)
  exists** — recursion without the gauge is flying blind into self-amplifying drift.
  (`recursive-dreaming-bounded-by-grounding.md`.)
- **C3 — R4: cross-source assistant synthesis.** Reads observed + authored, marked
  `interpreted`, assistant-tier only, never the mirror. (Same operation as Track D's
  correlator — build whichever framing lands first.)
- **C4 — R5: curated-graph dreaming + resonance.** The panel over a `curated` book graph
  (`CuratedView`) + cross-graph resonance with the authored theme-centroids,
  `interpreted`-only, never merging the book in. (`dreaming-on-curated-graphs.md`.)
  *Pairs with Track F's literary-interpretation probes — R5 is what those probes test.*

Design notes: `dream-phase-rnd-charter.md`, `dreaming-v2-interpreter-panel.md`,
`recursive-dreaming-bounded-by-grounding.md`, `dreaming-on-curated-graphs.md`.

---

## Track D — The World (observed/IoT + the correlator)

The assistant tier. Opt-in, owner-controlled, each source isolated to `observed`.

- **D1 — The observed ingest path.** Biometric (Oura) via local BLE extraction (preferred)
  or the API, into the dormant `sensor_readings` schema. Normalizer in `edge/` or
  `core/ingest/biometric.py`; core never imports the API client. Then phone sensors,
  financial (read-only, no transaction scope), photography metadata, social analytics
  (skeptical).
- **D2 — The correlator.** Separate from the dreamer. Reads `interpreted` dream outputs ↔
  aggregated `observed` features → `interpreted` correlations. Never raw authored text
  alongside observed; never causal; consequential-advice-defers.
- **D3 — Advisor agents.** Read the observed pool + interpreted layer, never the authored
  mirror. Assistant-tier outputs. The financial advisor is the exemplar (read-only, defers).

Design notes: `observed-data-and-the-assistant-tier.md`,
`observed-iot-and-cross-source-synthesis.md`, `skills-and-scope.md`.

---

## Track E — Hardening (close the gaps)

Lower-urgency, high-confidence cleanup. Pick up opportunistically.

- **E1 — Close the Podman empirical gap.** Run `pytest -m podman` to completion (the one
  invariant currently proven only by construction). *Gates E2.*
- **E2 — The WASM sandbox.** wasmtime + Pyodide as the preferred pure-compute substrate
  (isolation by absent syscall imports); `RoutingRunner` picks WASM for compatible Python,
  Podman otherwise. Build after E1. (`wasm-sandbox-runtime.md`.)
- **E3 — Phase 6b voice (optional).** Local speech synth/recognition in core; only audio
  crosses the carrier; the adapter dials only the owner's pre-registered number.
  (BUILD-SPEC §20.11.)
- **E4 — Formal-properties gap closure.** Remaining open gaps G4/G9/G10/G11 from
  `WHITEPAPER-FORMAL-PROPERTIES.md` (several overlap A1's drift metric).

---

## Track F — Testing & Tuning (the long-run harness + reasoning probes)

Objective tests for a system whose main outputs are subjective. Two families, plus the
literary probe that stress-tests grounding. **The primary instrument for baseline tuning.**

- **F1 — Synthetic corpus fixtures.** Stable / growing / adversarial corpora with KNOWN
  planted structure (we must know the right answer). Reusable by the harness and many
  emergent tests. Build first. (`simulation-harness-and-reasoning-probes.md` §1b.)
- **F2 — The simulation harness.** Ingest a fixture → run the real scheduler N cron cycles
  → snapshot → **trajectory report**. Start with assertions that don't need A1 (grounding
  non-decay, determinism, clean reset, attestation integrity over time, **Constitution-
  fingerprint stability** = the context-drift guard). Lives in `tests/longitudinal/`.
- **F3 — The mock-human-approver gate test.** Inject a tempting out-of-band change mid-run;
  assert the system **stops and asks** — the correct behavior is the *refusal*. High value,
  low cost. (`simulation-harness-and-reasoning-probes.md` §1d.)
- **F4 — Drift trajectory assertions.** Add once A1 exists: `D(t) ≤ Θ` throughout, no
  monotonic rise, dreams-citing-dreams ratio bounded. The harness is the gauge's natural
  **tuning instrument** — calibrate γ/λ/σ/Θ against observed curves on known data.
- **F5 — Logic-puzzle reasoning probes.** Prose → formal encoding → sandbox solve → check
  against ground truth. Tests problem *modeling* (model advises, code acts). Cleanest
  ground truth; build before the literary probes. (`simulation-harness-and-reasoning-probes.md` §2.)
- **F6 — Literary structural-extraction probe (Probe A).** Character networks / motifs /
  arc vs. a reference map — true ground truth. Needs R5's `CuratedView`. Build before the
  interpretation probes. (`literary-interpretation-probes.md` §4.)
- **F7 — Literary grounding-precision probe (Probe C).** Every theme the system surfaces
  must cite passages that actually support it — the **grounding-under-persuasion-pressure**
  test, the purest stress test of the grounding discipline. Reuses `core/selfcheck.py`.
  Weight this as THE architecture signal. (`literary-interpretation-probes.md` §3,5.)
- **F8 — Literary theme-recall probe (Probe B).** Recall vs. a *consensus* theme set. Build
  last; report alongside F7 but treat recall as model-strength-sensitive, grounding as the
  architecture signal. (`literary-interpretation-probes.md` §6.)
- **F9 — The dreamer output-quality suite (signal-vs-noise).** Adopt
  `tests/quality/test_dreamer_quality.py` — the apophenia/horoscope guard: pure-noise yields
  no confident theme, confidence is calibrated, the dreamer beats a dumb TF-IDF baseline on
  planted structure, grounding is load-bearing (citation ablation), dreams are
  distinguishable from random-recombination decoys. Statistical bounds, not exact values;
  `THRESH` joins the harness tuning surface (γ/λ/σ/Θ). Bind the `DreamerAdapter` to the real
  Dreamer/DerivedStore. **Caveat:** the decoy test's automatable proxy cannot prove
  *meaning* — wire `rate_blind` to a periodic owner blind-rating. **Surfaces a real
  adjudicator question:** does grounding-strength `g` scale with support *count* or only
  similarity? Tests the one axis nothing else does — output *quality*, distinct from output
  *safety*. (`dreamer-quality-suite-evaluation.md`.) *The two drift-deferred tests in the
  file move to `longitudinal/` and unlock with A1.*

Design notes: `simulation-harness-and-reasoning-probes.md`, `literary-interpretation-probes.md`,
`dreamer-quality-suite-evaluation.md`, `holistic-testing.md`, `test-organization.md`.
*Dependency:* F4 needs A1; F6–F8 need R5's `CuratedView` (Track C / C4); F9 reuses F1 fixtures
(noise + planted-in-noise are new F1 variants) and its two drift-deferred tests need A1.

---

## Suggested ordering (a default, not a mandate)

If building rather than just using, the dependency-respecting default:

1. **Track A (Senses)** first — makes everything observable; prereq for safe recursion and
   for Track F's drift asserts. A1→A2→A3→A4, A5 later.
2. **Track B (Voice)** in parallel or next — how you'll actually use the system daily;
   mostly assembly.
3. **Track F (Testing)** early and ongoing — F1+F2+F3 give you the overnight harness
   immediately (no A1 needed for the first assertions); F4 once A1 lands. This is what keeps
   you sane as the other tracks add features.
4. **Track D (World)** when you want observed insight — D2 (correlator) and C3 (R4) are the
   same operation; do one.
5. **Track C (Subconscious)** R2, R4, R5 anytime behind the flag; **R3 only after A1.** R5
   pairs with F6–F8.
6. **Track E (Hardening)** opportunistically; E1 before E2.

The single most important sequencing rule across the whole roadmap: **the drift gauge (A1)
before recursive dreaming (R3/C2), and before the harness's drift assertions (F4).** A1 is
the keystone of the forward layer. Everything else is preference.
