# The Mind Palace — v1.0 Technical Reference & System Map

**Status:** v1.0 — issued at the completion of the ten-phase base build (2026-06-28).
This is the authoritative technical map: what the system *is*, what it *does*, the
principles that hold it together, the complete capability surface, and the verification
story. Forward work is in `ROADMAP-V1.md`; design rationale for each forward subsystem is
in `docs/design-notes/`.

---

## Part I — What the system is

A single-user, offline-first, privacy-sealed personal AI — a "mind palace" — that indexes
the owner's **authored** corpus (notes, journals, poems, philosophical writing) and
reflects patterns back, with a gated agent layer, a one-way research airlock, encrypted
backups, and a bounded self-modification loop. It runs locally on an M2 Max MacBook
(32 GB, ~24 GB usable). It is built to be **extended over time**, not shipped as a fixed
product.

The one-sentence essence: **a mirror, not an oracle** — it reflects what the owner
actually wrote, marks every inference as inference, and can always rebuild itself from an
immutable seed.

---

## Part II — The principles (the spine everything hangs from)

These are not aspirations; each is enforced by a concrete mechanism named in Part IV.

1. **The model advises; code acts.** No model holds a shell, a credential, or an
   unattended infra mutation. Capability is a narrow handle that code grants
   (object-capability), never a flag a model can set.
2. **Mirror, not oracle.** Inference is marked as inference. A high-confidence dream is
   still a hypothesis for the owner to weigh, never a verdict.
3. **Raw is sacred; derived is regenerable.** An immutable, content-addressed (SHA-256)
   raw store is ground truth. Everything else — embeddings, dreams, structure — is
   rebuildable from it. This is the deepest guarantee in the system: the worst case is
   always "rebuild from what the owner wrote," never "irrecoverable."
4. **Fixed points make change safe.** Human-blessed immutable anchors (the Constitution +
   the frozen golden set) let the system grow and even self-modify without drifting,
   because change is always measured against something that does not move.
5. **Make illegal states unrepresentable.** The highest-leverage safety move: a type that
   cannot express the wrong thing beats any check that detects it. Used throughout —
   `DerivedStore` has no provenance parameter, `ProposedChange` has no field for a
   path/diff/command, `sensor_readings` has no provenance column.
6. **Put each check at the lowest tier that can handle it.** Speed and safety both come
   from *not* routing everything through the expensive path. A scope check is a reflex
   (inline, µs); a chain-audit is cognition (async, scheduled).
7. **The seed is fixed; there is no autonomous "direction."** The system mirrors a fixed
   (slowly-growing) corpus. Alignment means fidelity of the *regenerable* layer to the
   *fixed* layer — not sentience, not convergence on a goal of its own.

---

## Part III — Architecture

### III.1 Trust zones
- **Zone A — sealed core.** ZERO network egress. The corpus, all stores, local models,
  and the introspective agents. Enforced by an in-process fail-closed egress guard
  (loopback-only) plus a static import lint (`core/` cannot import any network-capable
  module) plus the OS-isolation hardening path.
- **Zone B — networked edge.** Containerized. The bridge + interface gateway — the *only*
  network-touching processes. Neither reads the vault. Communicates with the core by
  **filesystem handoff, never shared imports**.
- **Zone C — AWS.** Encrypted backups + the outbound research fetcher. Sees only
  de-identified criteria and public literature; never plaintext corpus.

### III.2 The model-serving substrate
Two-slot design: a pinned tiny router/watchdog (always warm) + one swappable worker.
Personas/params are injected at request time; code drives Ollama over HTTP (abstracted so
a future GPU node can join). "Scale in agents, not models" — agents are config
(Constitution + role + task + scope + memory) time-sharing the slots via a durable queue.

Models: pinned `qwen3.5:2b`; routine `qwen3.5:9b`; synthesis `qwen3.6:27b`; stretch
`qwen3.6:35b-a3b`; embedding `qwen3-embedding:4b` (2560-dim).

### III.3 The provenance spectrum (the firewall)
Every piece of data carries a provenance class, and the classes do not mix:
- **authored-solo / authored-dialogue** — the owner wrote it (notes; or messages to the
  Ambassador). Ground truth. Feeds the mirror.
- **curated** — others' words the owner selected (books, highlights). Lives in its own
  graph; never merged into the authored mirror.
- **observed** — behavioral exhaust (analytics, sensors, financial, biometric).
  Assistant-tier only. Never feeds the mirror or the baselines.
- **interpreted** — system inference. Structurally unforgeable (the derived store has no
  provenance parameter).

**The load-bearing rule:** the introspective dreamer reads `authored` only
(`MIRROR_READABLE`, realized as the `MirrorView` type). Observed exhaust can never seed an
introspective dream or contaminate a behavioral baseline. Cross-class synthesis is a
*separate* component (the correlator), reads derived/aggregated signals only, and outputs
`interpreted`.

### III.4 The stores (polyglot, object-capability scoped)
- **LanceDB** — vectors. `MirrorView` exposes authored-only reads to the dreamer.
- **DuckDB** — telemetry + the (dormant until biometrics) `sensor_readings` table.
- **SQLite** — the durable queue, agent/gate state, the derived store, the attestation
  store, the levers ledger.

Access is object-capability: a `TelemetryWriter` *has no read method*; the wrong access is
unreachable, not merely refused.

### III.5 The scheduler
Cooperative run-to-completion / checkpointed (not preemptive). A foreground gate keeps
heavy tiers out of interactive time; cron-tier work (dreaming, curation) runs in troughs.
The supervisor (code) is the always-on privileged thing — the tiny model is a stateless,
hot-swappable advisor with a rules fallback.

---

## Part IV — Capability surface (what is built and live, Phases 0–10)

### IV.1 Ingestion & the mirror (Phases 0–2)
Content-addressed raw store (SHA-256). The authored corpus → embeddings → the LanceDB
mirror. The vault watcher (`core/ingest/watch.py`, local-filesystem only, no network)
auto-re-ingests changed notes idempotently: unchanged = no-op, changed = re-embed,
deleted = **tombstone** (derived dropped, raw kept). Owner-gated `purge_raw` for true
deletion. Operationally live: notes sync phone↔Mac via Syncthing-over-Tailscale (no vendor
in the path), watcher runs as a launchd service.

### IV.2 Agents, roles, scope (Phases 3–5)
Agents are advisory by construction — `Agent.respond()` returns `(text, SelfCheck)`, no
action path. The Constitution is the outermost frame of every agent (`frame_context`).
Skills attach by two independent mechanisms: **instructional** (context, no capability) and
**executable** (a scoped tool handle from the role's pre-declared scope ceiling). Two
predicates, two subsystems, two times: `loaded(skill)` at assembly, `can_invoke(tool)` at
dispatch. A skill can never widen scope.

### IV.3 Sandboxed execution (Phase 4)
Code runs in rootless Podman: network-off, no-mount, capabilities dropped, timeout
enforced. Powerless by construction — no creds, no network, no vault; returns data, never
actions. (A WASM/Pyodide substrate is designed as a hardening upgrade — see roadmap.)

### IV.4 The dreaming layer (Phase 7 + R&D track, flag-off)
The system's subconscious: deferred trough-time sense-making over the **authored mirror**,
producing ranked `interpreted` hypotheses. Built: deterministic clustering → grounded
synthesis → `DerivedStore` (interpreted-only, structural). R&D (flag-off): a panel of
deterministic interpreters (R0) + an evidence-based adjudicator (R1,
`c = γ^d · g · (1 + λ(|Agr|−1))`, agreement = multiplier-not-vote). The Curator flags but
never rewrites authored content.

### IV.5 The research airlock (Phase 8, live)
One-way outbound research: the core emits **de-identified criteria** (`ResearchCriteria`
has no field that can carry note content; the scrubber raises rather than passes on doubt)
→ filesystem handoff → the Zone-B bridge (a dumb pipe, no vault handle) → a Lambda fetcher
that returns public literature → the core ranks it *inside the walls* (transient, never
ingested into the mirror). Least-privilege IAM; applied and live.

### IV.6 Backups (Phase 9, live)
restic → S3 with SSE-KMS, scheduled daily (03:30 LaunchAgent). AWS sees no plaintext.
First snapshot verified. This is the operational realization of "reset-from-raw is always
possible."

### IV.7 Secrets & runtime authorization (security track, live)
Production Vault: KV + the AWS dynamic-credentials engine (the bridge gets short-lived
IAM creds, TTL=1h, instead of a static key), auto-unseal. `get_secret(name, token=…)` is
the seam — a token routes through Vault (scope-enforced), no token falls back to Keychain
for owner-operated paths. Per-machine secrets live in a gitignored `config/local.toml`.

### IV.8 Attestation (security track, live)
Every agent action emits a signed `Attestation` (role, action, input/output hashes,
Constitution fingerprint, Vault token accessor, `derived_from_ids`, Ed25519 signature),
chaining from authored raw through every derivation. Append-only store (no delete/update
methods). Gate decisions are signed by the **owner's** key (Secure Enclave) —
non-repudiable. This is the **runtime proof layer**: not "the code can't misbehave"
(static) but "the code *did not* misbehave in this interaction" (runtime).

### IV.9 Self-modification (Phase 10, live, fail-closed OFF)
Propose → human-approve → code-executes → validate → auto-rollback. **Scoped to bounded
numeric config knobs only** — a `ProposedChange` has no field that can carry a path, diff,
or command, so code/infra changes are *unrepresentable*. Validation uses the frozen golden
anchor (capability) + the rolling baseline (drift). Mechanical rollback from a
machine-owned overlay (human `local.toml` always wins). Master switch + unattended switch
both off by default; nothing autonomously proposes yet.

---

## Part V — The verification story

Two complementary proof layers plus a tiered test taxonomy.

- **Static proof layer** (before runtime): the import lint (core can't reach the network),
  type constraints (illegal states unrepresentable), FSM checks on the small state
  machines (the two-slot loader, the gate). Formalized in
  `WHITEPAPER-FORMAL-PROPERTIES.md` as an invariant catalog (I1–I13) classified by
  assurance tier: **structural > static > guard > property-test > assumption-bounded.**
- **Runtime proof layer** (after each interaction): the attestation chain — what actually
  happened, signed.
- **Test taxonomy** (`holistic-testing.md`): unit, integration, property-based,
  **metamorphic** (input/output relationships, no ground truth), **adversarial** (violate
  invariants through the system's own interfaces), **emergent** (multi-component
  cross-invariants), **attestation-as-oracle** (assert properties of the attestation chain
  — the system proves its own process), **longitudinal** (slow drift). The `integrity/`
  suite (firewall/provenance/attestation) is a non-skippable CI gate. Two further
  families give *objective* signal in a system whose outputs are mostly subjective: a
  **long-running simulation harness** (trajectory properties over hours on a known
  corpus — the baseline-tuning instrument) and **reasoning probes** (ground-truth
  problems — logic puzzles and grounded literary interpretation — testing modeling and
  grounding, not raw model strength). See `simulation-harness-and-reasoning-probes.md`
  and `literary-interpretation-probes.md`.

**The honest boundary:** no test suite and no proof makes this system "correct" — it has
LLMs, an OS, and hardware in the loop. What the layers buy is that each failure mode
requires progressively more to go wrong, and the strongest guarantees are *structural*
(the wrong thing can't be built) rather than *checked*. The bottom guarantee is always the
immutable seed.

---

## Part VI — The forward layer (designed, consistent, not yet built)

Each is specified in `docs/design-notes/` and sequenced in `ROADMAP-V1.md`. Summarized:

- **Alignment subsystem** — detection (drift gauge + min-cut-to-authored + community/echo-
  chamber metrics) → gated surgery (prune interpreted bubbles, never the authored floor) →
  reset-from-raw. Phase-10 built the *actuator*; this adds the *senses*.
- **The dream R&D track (R2–R5)** — utility telemetry, recursion-bounded-by-grounding,
  cross-source assistant synthesis, curated-graph (book) dreaming + cross-graph resonance.
- **Observed/IoT + the correlator** — biometric (Oura) and other observed sources into the
  dormant `sensor_readings` schema; a correlator (separate from the dreamer) that relates
  `interpreted` patterns to aggregated `observed` signals, output `interpreted`, never
  causal.
- **The nervous system** — graduated tamper response (regenerable breach → quarantine +
  rebuild; fixed-layer breach → fail-closed freeze), and the auditor agent (async,
  read-only, trough-scheduled) that reads the attestation chain back.
- **The Ambassador** — the conversational front door: a **reasoning agent that is
  computationally light** (a mind that *uses* deterministic tools when thinking needs
  exactness — not a shallow classifier), wide read window (mirror + operational state),
  narrow authority (read + propose, never write + act), delegating heavy work to the async
  scheduler. Cadence/history are its own judgment within the budgeter bound; updates are
  contextual (expected + earned interruptions, never noise); it is transparent about effort
  in plain language. (`ambassador-as-reasoning-agent.md` is authoritative.)
- **WASM sandbox** — wasmtime + Pyodide as the preferred pure-compute substrate (isolation
  by absence of syscall imports, not by dropped capabilities), routed alongside Podman.

---

## Part VII — Boundaries that never move

- The Constitution and the frozen golden set are human-only, deliberate, logged. Never
  auto-modified.
- The sealed core never egresses. The interface may transit a third party; the corpus
  never does.
- No agent holds live send/pay credentials. Every outward action is gated.
- Consequential advice (health/financial/legal) is substantive but defers — honest about
  uncertainty, refuses dangerous specifics, final decision to the owner and a professional.
- The owner is the final arbiter. The system surfaces; the human decides.
