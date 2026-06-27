#!/bin/sh
# Phase B — configure Vault's AWS dynamic secrets engine (runbook §3; vault-runtime-auth.md §4).
# This is the end state where the bridge/airlock get short-lived (TTL=1h) AWS creds minted per
# interaction instead of a static profile. It depends on AWS infra that the build agent did NOT
# apply, so it is separated from the kv standup.
#
# PREREQUISITES (owner-operated, in order):
#   1. The airlock Terraform is applied (cloud/terraform/airlock) so the bridge-role / airlock-role
#      IAM roles exist — get their ARNs from `terraform output`.
#   2. A Vault-dedicated IAM principal exists whose access key Vault uses to mint creds, with an
#      IAM policy allowing sts:AssumeRole on those two role ARNs; AND each role's trust policy
#      permits that principal to assume it. (IAM wiring — do it in Terraform, not here.)
#   3. You've set the engine root creds (SECRET — run by hand, NOT in this script):
#        vault write aws/config/root access_key=<…> secret_key=<…> region=us-east-1
#
# Then run with BRIDGE_ROLE_ARN and AIRLOCK_ROLE_ARN in the env. Idempotent.
set -eu
: "${VAULT_ADDR:?export VAULT_ADDR=http://127.0.0.1:8200}"
: "${VAULT_TOKEN:?export VAULT_TOKEN}"
: "${BRIDGE_ROLE_ARN:?export BRIDGE_ROLE_ARN=\$(cd cloud/terraform/airlock && terraform output -raw bridge_role_arn)}"
: "${AIRLOCK_ROLE_ARN:?export AIRLOCK_ROLE_ARN=\$(cd cloud/terraform/airlock && terraform output -raw airlock_role_arn)}"

if ! vault secrets list -format=json | grep -q '"aws/"'; then
  vault secrets enable -path=aws aws
fi

# Dynamic creds via STS AssumeRole, TTL=1h — they expire automatically (vault-runtime-auth.md §4).
# These role NAMES are exactly what the policies grant: aws/creds/bridge-role, aws/creds/airlock-role.
vault write aws/roles/bridge-role \
  credential_type=assumed_role \
  role_arns="$BRIDGE_ROLE_ARN" \
  default_sts_ttl=1h max_sts_ttl=1h

vault write aws/roles/airlock-role \
  credential_type=assumed_role \
  role_arns="$AIRLOCK_ROLE_ARN" \
  default_sts_ttl=1h max_sts_ttl=1h

echo "OK: aws engine + bridge-role + airlock-role configured."
echo "Verify (mints a temp cred that expires in 1h): vault read aws/creds/bridge-role"
