---
type: design-note
id: dn-secrets-management-evolution
status: superseded
created: 2026-06-27
updated: 2026-07-07
links:
  - docs/design-notes/vault-runtime-auth.md
  - docs/audits/archive-recommendation.md
supersedes: null
superseded_by: dn-vault-runtime-auth
warrant: finding-0022
---

# Design note — Secrets management evolution: Keychain → Vault

> **⚠️ SUPERSEDED (2026-07-07).** `vault-runtime-auth.md` is the authoritative Vault
> note and takes precedence wherever the two differ. It reframes Vault from a
> multi-machine secrets store to a **per-interaction runtime authorization layer**
> (its own words: this note was "correct but incomplete"), and the audit confirms the
> successor's design is the one actually built (`cloud/terraform/vault_engine.tf`,
> dynamic secrets engine). Residual value here: the tipping-point analysis (§1), the
> secret taxonomy (§5), and the what-not-to-do list (§6) remain useful reference.

_Family tag → family 1 (capability / information-flow): secrets as object-capability (Keychain → Vault); credentials are never a tool and are held off the model prompt. See [`../NOTATION.md`](../NOTATION.md)._

**Status:** superseded by `vault-runtime-auth.md` — see banner. Keychain remains
correct for a single-machine deployment; the `get_secret()` abstraction below is
still the swap surface.

---

## 0. Current approach (correct for now)

`get_secret()` reads from env or macOS Keychain. Hardware-backed (Secure Enclave),
OS-integrated, zero network dependency. Non-negotiable rule: secrets never in code,
never read by a model, never logged. This is the right approach for one machine.

## 1. The tipping point — when Vault makes sense

**Trigger:** secrets needed on more than one machine. Specifically: the server build
joins the mesh and Zone B bridge code needs AWS credentials, API tokens (Oura,
financial, etc.), and any future integrations. Manually copying credentials to two
machines causes drift and staleness. That's when centralization earns its cost.

**The specific feature that makes it worth it:** Vault's AWS secrets engine issues
**dynamic, short-lived IAM credentials** on demand with a TTL. The bridge asks Vault
for AWS credentials → gets a key pair expiring in 1 hour → uses it → it's gone. The
blast radius of a compromised bridge drops from "long-lived access key compromised"
to "a credential that has already expired." This is a genuine security improvement
over the current static-key approach, and fits the least-privilege IAM posture
already built in Phase 8.

**Second feature that fits:** audit logging. Every `get_secret()` call against Vault
is logged — which component, when, from where. "Comment the why at trust boundaries"
applied to runtime access, not just code.

## 2. Architecture

Run Vault on the **server** (always-on), not the Mac (sleeps, roams). Rootless
Podman container, Raft integrated storage (no external database), exposed ONLY on
the Tailscale interface — never on the public network.

```
Mac (Vault client)  ──[Tailscale 100.x.x.x]──→  Vault (server, rootless Podman)
Server (Vault client, local)  ────────────────→  Vault (server, rootless Podman)
                                                       │
                                             ┌─────────┴─────────┐
                                             │  AWS secrets engine │  ← dynamic creds
                                             │  KV store (tokens)  │  ← Oura, financial
                                             │  Audit log          │  ← who read what
                                             └────────────────────┘
```

Auth method: **AppRole** for each component (bridge, Mac orchestrator, scheduler).
Each role has a policy scoped to exactly the secrets it needs — the bridge reads
`aws/creds/bridge-role` and `kv/oura-token`; it cannot read financial keys. Same
object-capability discipline as the rest of the system.

## 3. The unseal problem (the honest caveat)

Vault is sealed at rest and requires unsealing on every restart before it serves
secrets. Two reasonable options for a personal system:

**Option A — Auto-unseal via AWS KMS (recommended):** Vault calls the existing KMS
key (Phase 8 bootstrap) on startup. No manual step; clean. Tradeoff: Vault needs
AWS credentials to unseal — these live in Keychain on the server host, outside the
container. One remaining secret handled by Keychain; everything above it handled by
Vault. Turtles all the way down to one, which is always the case and is fine.

**Option B — Manual unseal with Keychain:** unseal key in server Keychain; a systemd
unit or launchd script unseals on boot. More manual; works for a system that rarely
restarts.

Either way: the bottom-most secret (unseal key or KMS auth) stays in Keychain on
the host. You cannot escape that anchor; you only reduce everything above it to
Vault's problem.

## 4. The `get_secret()` swap

`config/loader.py` `get_secret()` is already an abstraction. Adding a Vault backend
is one implementation:

```python
def get_secret(name: str) -> str:
    # Current: env → Keychain
    # Future: env → Vault (HVAC client) → Keychain fallback
    if vault_configured():
        return vault_client.read(f"kv/data/{name}")["data"]["value"]
    return _keychain_get(name)
```

Nothing else changes. The bridge, scheduler, and agents call `get_secret()`; they
are unaware of the backend. The swap is entirely behind this function.

## 5. Secret taxonomy (what moves to Vault)

| Secret                      | Current           | With Vault                                 |
| --------------------------- | ----------------- | ------------------------------------------ |
| AWS bridge role credentials | Keychain (static) | Vault AWS engine (dynamic, TTL=1h)         |
| Oura API token              | Keychain (Mac)    | Vault KV (accessible from both machines)   |
| Financial read-only API key | Keychain (future) | Vault KV                                   |
| Vault unseal / KMS auth     | —                 | Keychain (server host) — the bottom turtle |
| AWS SSO (owner-operated)    | Keychain (stays)  | Stays — owner-operated, not code-operated  |

Note: AWS SSO credentials stay in Keychain because they are **owner-operated** (you
run `aws sso login`), not code-operated. Vault manages code-operated credentials
only.

## 6. What NOT to do

- **Do not run Vault on the Mac.** It sleeps; Vault sealed = all secrets inaccessible.
- **Do not expose Vault outside Tailscale.** No public port; Tailscale IP only.
- **Do not use Vault dev mode in production.** Dev mode stores secrets in memory only
  and doesn't persist across restarts. Fine for local testing; wrong for a running
  system.
- **Do not build this before the server is running.** Single machine = Keychain.
  Adding Vault complexity to a single-machine system is pure overhead.

## 7. Build (when the time comes)

1. Rootless Podman container: `hashicorp/vault:latest`, Raft storage, Tailscale-only
   listener (`VAULT_API_ADDR=https://100.x.x.x:8200`), TLS (self-signed or
   Tailscale's built-in TLS).
2. AWS KMS auto-unseal pointing at the existing Phase-8 KMS key.
3. Enable AWS secrets engine; configure the bridge IAM role for dynamic creds.
4. Enable KV v2; store API tokens.
5. AppRole auth for each component with scoped policies.
6. Implement `VaultBackend` in `config/loader.py` behind the existing `get_secret()`
   interface.
7. Update `ops/import_lint.py` — the Vault client (`hvac`) is an `edge/` dependency;
   `core/` may not import it. `get_secret()` in `config/` calls it via a late import
   or the edge layer resolves it. Keep the seal.

Verify: sealed Vault = `get_secret()` raises clearly; unsealed = returns correct
values; audit log shows every access; bridge gets dynamic AWS credentials that expire.
