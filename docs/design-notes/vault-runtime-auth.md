---
type: design-note
id: dn-vault-runtime-auth
status: draft
created: 2026-06-27
updated: 2026-07-07
links:
  - docs/design-notes/secrets-management-evolution.md
supersedes: dn-secrets-management-evolution
superseded_by: null
warrant: finding-0022
---

# Design note — Vault as runtime authorization layer

_Family tag → family 1 (capability / information-flow): per-interaction runtime authorization — ephemeral scoped Vault tokens (object-capability), the credential analogue of 𝒜. See [`../NOTATION.md`](../NOTATION.md)._

**Status:** design only. Supersedes `secrets-management-evolution.md` (which framed
Vault as a multi-machine secrets store — correct but incomplete). This note frames
Vault as a **per-interaction runtime authorization layer**: every agent interaction
that touches a privileged resource gets an ephemeral scoped token minted by the
supervisor, uses it, and the token expires. Buildable now on the Mac; extends
naturally to the server. Honor at Phase 5 (agent factory + dispatcher).

---

## 0. The gap this closes

The current object-capability model scopes _store handles_ at the code level — the
dreamer gets a `MirrorView`, not a raw vector store handle. But there is no
equivalent enforcement at the _credential_ level. Any code that imports `config` can
call `get_secret()` and retrieve any credential. Vault agent tokens close this:

| Layer             | Enforcement       | Mechanism                                        |
| ----------------- | ----------------- | ------------------------------------------------ |
| Store access      | Structural (code) | Scoped handles — `MirrorView`, `TelemetryWriter` |
| Credential access | Runtime (Vault)   | Scoped ephemeral tokens minted per interaction   |

Together: neither code nor runtime can exceed declared scope. The model never holds a
real credential — only an ephemeral token code minted for it, scoped to what this
interaction needs, expiring in minutes. **"Code acts, model advises" now extends to
credentials.**

The audit trail is the second half: every privileged access creates a Vault log
entry (agent role, resource path, timestamp). This is the runtime analog of the
import lint — the lint proves at static time that `core` can't import `edge`; the
Vault log proves at runtime that the dreamer never touched the financial key.

---

## 1. Running locally (now, on the Mac)

Vault in a rootless Podman container on `127.0.0.1:8200`. Loopback = inside the
egress guard (Invariant 1 permits loopback, same as Ollama). The sealed core can
call it without any egress violation. No multi-machine setup required; this is
viable immediately.

**Storage:** Raft integrated backend — a single directory on the Mac, persisted
outside the container (Podman volume mount). No external database.

**Unseal on Mac:** store the unseal key in macOS Keychain. A small launchd agent
runs on login, reads the key from Keychain, calls `vault operator unseal`. The
container start + unseal is automatic after first init. One secret in Keychain
bootstraps everything above it — the irreducible bottom turtle, same as always.

**Extension to server:** expose Vault on the Tailscale interface additionally
(`100.x.x.x:8200`) when the server joins the mesh. The Mac remains the Vault host
(always-on is better on the server long-term — see §6); client config changes, Vault
data doesn't.

---

## 2. Per-interaction token lifecycle

```
1. Supervisor receives a job from the queue (e.g. "run dreamer pass")
2. Supervisor calls vault_client.mint_token(role="dreamer", ttl="10m")
   → Vault validates supervisor's token has minting authority for "dreamer"
   → returns ephemeral token T scoped to the "dreamer" policy
3. Supervisor passes T to the agent as part of its context (NOT the real credential)
4. Agent calls get_secret("oura-daily-stats", token=T)
   → get_secret() presents T to Vault
   → Vault checks: does "dreamer" policy permit reading kv/oura-daily-stats? YES
   → returns the value
5. Agent calls get_secret("financial-api-key", token=T)
   → Vault checks: does "dreamer" policy permit reading kv/financial? NO
   → raises PermissionDenied — agent learns nothing, log records the attempt
6. Interaction ends (or TTL=10m elapses) → token T is invalid
7. Vault audit log: {role: "dreamer", path: "kv/oura-daily-stats", op: "read",
                     time: "...", allowed: true}
                    {role: "dreamer", path: "kv/financial-api-key", op: "read",
                     time: "...", allowed: false}
```

The agent never sees the real credential unless its policy permits it. Even a
misbehaving or confused agent cannot exceed its minted scope. The log records both
successes and denials — denials are as informative as successes for alignment audits.

---

## 3. Policy taxonomy (per agent role)

Policies are narrow by default — grant the minimum, document why each grant exists.

| Role               | Permitted paths                    | Rationale                                |
| ------------------ | ---------------------------------- | ---------------------------------------- |
| `dreamer`          | `kv/oura-daily-aggregates` (read)  | Biometric aggregates for correlator only |
| `dreamer`          | _(nothing else)_                   | No AWS, no financial, no raw API tokens  |
| `bridge`           | `aws/creds/bridge-role` (dynamic)  | S3 access, TTL=1h, expires automatically |
| `bridge`           | `kv/oura-api-token` (read)         | Polls Oura API on the owner's behalf     |
| `research-airlock` | `aws/creds/airlock-role` (dynamic) | Research S3 bucket only                  |
| `advisor`          | `kv/financial-readonly-key` (read) | Financial data advisor agent             |
| `advisor`          | `kv/oura-api-token` (read)         | Can query current biometric state        |
| `correlator`       | `kv/oura-daily-aggregates` (read)  | Cross-source synthesis                   |
| `correlator`       | _(no financial, no AWS)_           | Correlates observed signals only         |
| `supervisor`       | Token creation for all roles       | Mints; cannot read role secrets directly |
| `gate`             | `kv/gate-ledger-key` (read/write)  | Gate state encryption only               |

The supervisor holds **token creation authority only** — it cannot read the secrets
it mints tokens for. This is the same principle as the dispatcher holding handles
but not being the agent.

---

## 4. Secrets taxonomy (what lives in Vault)

| Secret                   | Engine           | Notes                                     |
| ------------------------ | ---------------- | ----------------------------------------- |
| AWS bridge role          | `aws/` (dynamic) | TTL=1h; replaces static key               |
| AWS airlock role         | `aws/` (dynamic) | TTL=1h                                    |
| Oura API token           | `kv/` (static)   | Personal access token; rotated manually   |
| Financial read-only key  | `kv/` (static)   | No transaction scope — enforced by broker |
| Future API tokens        | `kv/` (static)   | Same pattern                              |
| Vault unseal key         | macOS Keychain   | The bottom turtle; never in Vault         |
| AWS SSO (owner-operated) | macOS Keychain   | Owner-operated; not code-operated         |

AWS SSO stays in Keychain — it's used by `aws sso login`, an owner-operated action,
not by any agent. Vault manages code-operated credentials only.

---

## 5. Integration with existing architecture

**`config/loader.py` `get_secret()`:**

```python
def get_secret(name: str, token: str | None = None) -> str:
    """
    token: a Vault ephemeral token minted for the calling agent's role.
    If None, falls back to env → Keychain (for owner-operated / bootstrap use).
    Core agents always pass a token; bootstrap/scripts use None.
    """
    if token:
        return _vault_get(name, token)   # raises PermissionDenied if out of scope
    return _env_or_keychain_get(name)    # owner-operated path unchanged
```

The agent's token is part of its injected context (like the Constitution frame) —
the agent receives it, passes it to `get_secret()`, and never constructs or stores
it. The supervisor mints; the agent uses; code enforces.

**Import discipline:** `hvac` (the Vault Python client) is permitted in `config/`
and `ops/` (supervisor token minting). It is NOT a `core/` agent import — agents
receive tokens in context, they do not call Vault directly. The import lint enforces
this. The Vault call is in `get_secret()`, one level below the agent.

**Egress guard:** Vault on `127.0.0.1:8200` is loopback — already permitted by
Invariant 1 (same allowlist as Ollama). No guard change needed for local Vault.

**The gate (Phase 3):** Gate decisions can optionally log to Vault's audit path
alongside the existing gate ledger. Two independent audit trails for the most
privileged operation in the system.

---

## 6. Alignment connection

The Vault audit log is a component of the alignment detection layer
(alignment-subsystem.md). A dreamer interaction that attempted to read
`kv/financial-api-key` and was denied is a behavioral signal — an `interpreted`
finding can note "an agent attempted access outside its declared scope at T." This
is the Blade Runner test applied to credentials: the graph of allowed-vs-attempted
access reveals behavioral drift before it reaches the authored layer.

Vault denials are therefore not just security events — they are alignment signals.
The correlator can surface patterns of out-of-scope access attempts as `interpreted`
findings in the alignment report.

---

## 7. Build (when Phase 5 lands)

1. Rootless Podman container: `hashicorp/vault:latest`, config:
   ```hcl
   storage "raft" { path = "/vault/data" }
   listener "tcp" { address = "127.0.0.1:8200" tls_disable = true }
   # add Tailscale listener when server joins
   ```
2. `vault operator init` → store unseal key in macOS Keychain.
3. LaunchAgent plist: on login, read unseal key from Keychain → `vault operator unseal`.
4. Enable `aws` secrets engine; configure `bridge-role` and `airlock-role` IAM.
5. Enable `kv` v2; write initial static secrets.
6. Define AppRole + policies per §3.
7. Implement `_vault_get()` in `config/loader.py` via `hvac`.
8. Add `mint_token(role, ttl)` to the supervisor.
9. Update `ops/import_lint.py`: `hvac` allowed in `config/`, `ops/`; blocked in
   `core/` agent modules.
10. Verify: dreamer token cannot read financial key (PermissionDenied logged); bridge
    token gets dynamic AWS creds that expire; supervisor token cannot read secrets
    directly; audit log shows full access history.
