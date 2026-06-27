# supervisor — token-creation authority ONLY (vault-runtime-auth.md §3). Deliberately holds no
# kv/ or aws/ read grant of its own: it mints tokens for other roles' policies, it does not read
# the secrets those tokens unlock. Mirrors the dispatcher-holds-handles-but-isn't-the-agent split.
#
# Minting goes through TOKEN ROLES (auth/token/create/<role>), not a bare policy list: the role's
# allowed_policies does the scoping, so the supervisor never has to hold — and could never read —
# the policies it mints. A bare `policies=[...]` create would fail Vault's subset rule for this
# (non-root) token, which is exactly the property we want. See VaultClient.mint_token and
# ops/vault/setup_policies.sh (which creates one token role per agent policy).
path "auth/token/create/*" {
  capabilities = ["create", "update"]
}
