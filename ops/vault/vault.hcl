# Mind-palace production Vault — single-node, loopback-only (vault-runtime-auth.md §1; runbook
# "Security & trust infrastructure" §2b). The build agent authored this config — it holds NO
# secrets. The owner runs `vault operator init`/`unseal` and places keys (owner-operated).
#
# The storage path is RELATIVE to the server's working directory, which the LaunchAgent pins to the
# repo root (`data/` is gitignored, alongside the other local stores). If you run the server by
# hand, run it from the repo root: `vault server -config ops/vault/vault.hcl`.
storage "raft" {
  path    = "data/vault/raft"
  node_id = "mac"
}

# Loopback only = inside the sealed-core egress guard (Invariant 1), the same allowlist as Ollama.
# When a server node joins the Tailscale mesh, ADD a second listener on the 100.x.x.x interface —
# do NOT remove this one (vault-runtime-auth.md §1).
listener "tcp" {
  address     = "127.0.0.1:8200"
  tls_disable = true
}

api_addr      = "http://127.0.0.1:8200"
cluster_addr  = "http://127.0.0.1:8201"

# macOS launchd sandbox doesn't grant the mlock capability; disabling it avoids a startup failure.
# The at-rest protection here is FileVault (full-disk encryption) under the Raft directory — keep
# FileVault on. This is the documented single-user-Mac posture, not a server-grade one.
disable_mlock = true
ui            = true
