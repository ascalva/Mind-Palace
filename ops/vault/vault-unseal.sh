#!/bin/sh
# Start the mind-palace Vault server and auto-unseal it from Keychain (runbook §2b). The
# LaunchAgent (com.mind-palace.vault.plist) invokes this and keeps it alive; the final `wait`
# holds this script open for the server's lifetime so launchd supervises the pair as one unit
# (KeepAlive restarts the whole thing if the server dies).
#
# The unseal key is read from Keychain at RUNTIME — it is never written to this file or any log.
# Owner-operated prerequisites (one time): `vault operator init -key-shares=1 -key-threshold=1`
# done, and Unseal Key 1 placed at Keychain service `vault-unseal-key`, account `mind-palace`:
#     security add-generic-password -U -a mind-palace -s vault-unseal-key -w
set -eu

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO"
export VAULT_ADDR="http://127.0.0.1:8200"

# Raft does not create its own storage dir — ensure it exists (no-op once initialised).
mkdir -p data/vault/raft

vault server -config ops/vault/vault.hcl &
server_pid=$!

# Wait for the API to answer. `vault status` exits 0 (unsealed) or 2 (sealed but up); any other
# code means the listener isn't ready yet.
while true; do
  vault status >/dev/null 2>&1 && break       # already unsealed
  [ $? -eq 2 ] && break                         # up but sealed -> unseal below
  sleep 1
done

key="$(security find-generic-password -a mind-palace -s vault-unseal-key -w)"
vault operator unseal "$key" >/dev/null 2>&1 || true   # no-op if already unsealed
unset key

wait "$server_pid"
