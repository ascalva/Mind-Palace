# CONVENTIONS

Engineering and security practice for this repo. Binding unless the full `docs/BUILD-SPEC.md` says otherwise. The goal is **efficient, secure, open-source code, with thin custom logic where we want ownership** — a flexible system we expand as needs grow.

## Language & style
- **Python** for orchestration, agents, stores access, and the supervisor — the owner's strongest language and the native home of the ML/embedding ecosystem.
- Performance-critical deterministic stream math (EWMA, z-scores, changepoint) uses **Polars/NumPy**; it may later move to Rust if it becomes a bottleneck. Don't prematurely optimize.
- The job queue is **SQLite-backed Python** by default; **River (Go)** is the sanctioned alternative if more robustness is wanted (decision point).
- Type-hint everything. Keep modules small and single-purpose. Prefer pure functions for anything testable.

## Frameworks — what NOT to use
Do **not** pull in LangGraph, CrewAI, AutoGen, or similar agent frameworks. They are ceremony that obscures ownership and fights the resource model. **Hand-roll the ReAct/tool loop and the supervisor.** Build thin wrappers over solid primitives (Ollama HTTP, LanceDB, DuckDB, SQLite, Podman) rather than adopting large abstractions.

## Data stores & access
- **LanceDB** — thought-graph vectors (in-process, no daemon).
- **DuckDB** — telemetry/time-series (system vitals now; body-sensor adapter contract built but dormant).
- **SQLite** — job queue, scheduler state, the propose/approve/validate gate ledger, rollback metadata, persisted-agent registry.
- **Scoped access is enforced in code, not by convention.** Each agent gets a store handle limited to exactly the reads/writes its role needs. The introspection agents have no write access to telemetry; the watchdog has no write access to the vault. Build a small access layer that makes the wrong access impossible, not just discouraged.
- Ship migrations and a `schema.md`. Keep each store independently replaceable.

## Model serving & the resource ceiling
- Serve models over **HTTP via Ollama** (or `llama-server`); keep the interface abstract so a future Linux/GPU node can join as another worker.
- Honor the **two-slot model** (BUILD-SPEC §5): one pinned tiny model, one swappable worker. Never attempt to hold more, or exceed ~20–24 GB usable. The scheduler must refuse breaching work. The ~32B stretch model evicts the pinned model — account for that.
- Group same-tier jobs to minimize model-load swaps; that latency is the real cost.
- **Context budgets are deterministic.** Count tokens with the model's tokenizer and assemble each context (Constitution → role/task → retrieval → history → tool output) to fit the active model's window with reply headroom; on overflow, trim retrieval top-k, compact history, then escalate model tier — never silently drop. Track usage to telemetry.
- **Size the context window per role at load time** (`num_ctx` / KV-cache), not at the model's max — small for the router and the conversational role, large for synthesis — from tracked per-role usage. Smaller windows save RAM (KV cache scales with context length) and latency.
- **Inject persona and parameters at request time via the Ollama API — never bake `SYSTEM`/`PARAMETER` into Modelfiles.** Keep two lifecycles separate: agent lifecycle (the factory + SQLite registry, runtime config) and model lifecycle (pull/update + the two-slot loader). The router decides routing/tier/window; code assembles prompts and drives Ollama. Changing `num_ctx` reloads the model, so vary it per role at load, not per call.

## Code execution (sandbox)
Any code an agent runs is **powerless** (Invariant 4):
- Default substrate: **ephemeral rootless Podman** — `--network=none`, no vault mount, read-only base + scratch tmpfs, dropped capabilities, seccomp profile, non-root user, CPU/memory/pids limits, wall-clock timeout.
- Keep a **warm pool** of sandboxes to avoid cold start; cap concurrency to the memory ceiling. Wrap it in a thin execution-broker.
- For pure computation, prefer **wasmtime + Pyodide** (no syscalls). For hardening, the upgrade path is **gVisor/Firecracker**.
- Executed code returns **data**, never actions on the system. Any network grant is per-execution, narrowly scoped, and logged.

## Secrets
- **macOS Keychain** (the owner already uses Keychain-backed auth) or environment variables. Never commit secrets, never let a model read them, never log them. Config files hold non-secret config only.

## Cloud (AWS)
- **Terraform for everything.** No click-ops. Least-privilege IAM — the research fetcher gets web egress + the two S3 prefixes and nothing else.
- Backups via **restic → S3** (client-side encrypted + deduplicated) with SSE-KMS on the bucket. macOS is APFS — restic over data directories; don't assume btrfs.

## Trust boundaries in code
- `core/` (Zone A) must contain **no import path that can reach the network.** Treat an accidental network-capable import in core as a build-breaking defect.
- Only `edge/` (bridge, interface gateway) touches the network, containerized, vault unmounted, no inbound listeners beyond what the job needs.
- **Comment the *why*** at every boundary — the airlock's outbound-only/de-identified asymmetry, the propose/execute split, the agent-factory scope ceiling — so a later edit can't quietly erode the property.
- **Voice/telephony adapter** lives in `edge/`; TTS/STT run in `core/` and the adapter pipes raw audio only. The dial target comes from **fixed config, never from model output** — the adapter must be structurally incapable of dialing any number but the owner's registered one. Authenticate the human (passphrase/callback) before relaying privately-derived content.

## Testing & validation
- Write tests alongside code. For retrieval, use **deterministic metrics** (recall@k, set overlap, cosine distance) against the **frozen golden set**. For behavior, check conformance to `CONSTITUTION.md`. Use a model-judge only for subjective cases, always **A/B against a baseline snapshot**, never scored cold.
- The agent that made a change never grades it. Keep **two baselines**: a rolling one for acute regressions, the frozen anchors (golden set + Constitution) for slow drift.

## Working rhythm
- Build **phase by phase** (BUILD-SPEC §18); verify against the gate; **checkpoint with the human** before advancing.
- **Ask, don't guess** on BUILD-SPEC §20 decisions; otherwise choose a sensible default and state it inline.
- Keep changes small and reversible. When unsure whether something belongs in `core/` or `edge/`, it belongs in `edge/` if it can ever touch the network.
