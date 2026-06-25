# cloud/ — Zone C (AWS)

Terraform-managed airlock + backups. Sees only de-identified topic criteria and public literature; never plaintext private data (BUILD-SPEC §16). Built in Phases 8–9.

- `terraform/` — least-privilege IAM, S3 `requests/`+`results/`, fetcher infra.
- `fetcher/` — Lambda/Fargate public-literature aggregation.
