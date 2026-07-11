---
type: design-note
id: dn-ci-platform-and-runner-strategy
status: draft            # draft → ratified → superseded.  draft→ratified is an OWNER-ONLY hand edit.
created: 2026-07-11
updated: 2026-07-11
links:
  - docs/findings/finding-0034.md          # warrant-in-fact: runner-minutes bottleneck → this note
  - docs/findings/finding-0032.md          # folded: needs:[] gate topology (subsumed on GitHub)
  - docs/design-notes/attestation-layer.md # the witness this note re-points
  - .gitlab-ci.yml                         # the gate being replaced
  - .github/workflows/ci.yml               # the stale workflow being rebuilt
  - ops/ci_witness.py                      # the deploy-attestation machinery
  - .releaserc.json                        # release commit-back — the divergence constraint
supersedes: null
superseded_by: null
warrant: null            # promotion (finding → design), not a supersession
---

# CI platform and runner strategy — the gate moves to GitHub Actions; MicroVM runners park on triggers

> Filed by the orchestrator as `draft` (promoted from finding-0034 + finding-0032 on the
> owner's 2026-07-11 direction). Ratification is a hand edit by the owner. `/graduate`
> refuses this note until `status: ratified`.

## 1. Purpose and scope

GitLab's shared-runner budget is exhausted (0 of 400 min, 2026-07-11): every
`.gitlab-ci.yml` pipeline is dead until the monthly reset, so the project has **no working
CI gate and no attestable deploy path** (`mind-palace deploy` requires a witness-attested
green pipeline — `ops/ci_witness.py:79-99`). finding-0034's re-entry trigger fired; the
owner directed a design note, not a supervision hack.

**This note decides:** (1) which platform hosts the CI gate; (2) where deploy attestation
points; (3) where semantic-release runs — jointly with the repo-host question it turns out
to force; (4) the disposition of `.gitlab-ci.yml`; (5) whether/when self-hosted AWS Lambda
MicroVM runners enter; (6) the disposition of finding-0032's `needs:[]` remedy.

**Out of scope:** the *content* of the gates (ruff / import-firewall / mypy split / pytest
tiers / vault-axis are settled design — bp-008, finding-0029; they port verbatim, they are
not redesigned here); the WASM sandbox and effector designs themselves; the repo's public
posture (already public, owner-confirmed 2026-07-11).

## 2. Gate 0 — nothing sensitive is in the public tree (cleared, one residual)

The repo is publicly mirrored (`github.com/ascalva/Mind-Palace`, push-mirror main-only,
SSH). Before any GitHub-ward move, the tree had to be checked. Evidence, 2026-07-11:

- **Tracked-file scan (669 files):** no data stores, no credential-shaped files. The only
  "corpus" in-tree is the frozen **synthetic** golden set (`eval/golden/corpus/*.md` —
  deliberately committed fixed points), synthetic test fixtures
  (`tests/fixtures/corpus.py`), and two design-vs-code reconciliation audits
  (`docs/audits/corpus-state-audit-2026-07*.md` — cite code lines, contain no personal
  corpus content).
- **Structural exclusions hold** (`.gitignore`): `data/`, `*.duckdb`, `*.lance/`, `.env`,
  `*.secret`, `config/local.toml`, `config/levers.toml`, `*.tfstate` — the raw corpus and
  per-machine state never enter git. Secrets are Keychain/env-only by Invariant 10.
- **Full-history pattern scan: 0 hits** for AWS access keys, PEM private-key blocks,
  GitLab PATs (`glpat-`), GitHub tokens (`ghp_`/`gho_`), Slack tokens, `sk-` API keys —
  across all commits (`git log --all -p` grep, 2026-07-11).
- **PII:** the only phone numbers in HEAD are `555`-prefixed test fixtures
  (`tests/adversarial/test_pii_scrubber.py:17`); the owner's pre-registered number
  (Invariant 12) is correctly absent. No personal email in tracked content (git author
  metadata is public by nature of a public repo — accepted).
- GitLab's `secret_detection` job has run green on every push all month (it is partly
  *what burned the minutes*).

**Residual, carried into Plan A:** the history scan above is pattern-based, not
entropy-based. The first plan runs a real scanner (gitleaks) once over **full history**
as an acceptance criterion, then keeps it as a CI job. Named remediation if it ever hits:
rotate the credential, purge history (`git filter-repo`), force-remirror — decided now so
it is not improvised under alarm.

**Verdict: cleared.** Framework public, corpus local — the privacy ethos (Invariant 11)
is intact.

## 3. Principles

- **P1 — The gate must not depend on a metered budget.** The failure mode just observed:
  quota exhaustion silently removes the only release path. A gate that can be *used up*
  is not a gate. (GitHub Actions on a public repo is unlimited-free; the entire
  minute-conservation apparatus — `rules:changes`, batched pushes — was a workaround for
  P1 being violated, and is not ported.)
- **P2 — Every main sha yields a terminal, attestable verdict.** The witness never
  guesses (`ops/ci_witness.py:59-66`); GitLab guaranteed a pipeline per push
  (`workflow.rules: when: always`, `.gitlab-ci.yml:1-5`). On GitHub this means the `ci`
  workflow triggers unconditionally on `push: branches: [main]` — **no `paths:` filters
  that could leave a sha runless.** Unlimited minutes make the skip-optimization
  pointless anyway.
- **P3 — Attestation is re-pointed, never weakened.** "Green" stays an attested fact
  chained to the commit's ingest (`ci_witness / pipeline_green`), whichever host produces
  it. The witness's verdict semantics (`green | red | pending | absent`) are preserved.
- **P4 — Isolation follows the workload.** Hosted runners are sufficient for
  deterministic gates over public code (lint, types, model-free tests). Firecracker
  MicroVM isolation is Invariant 4 ("executed code is powerless") realized at the infra
  layer — it becomes *load-bearing* only when CI itself executes untrusted or
  AI-generated code. Build it then, not now.
- **P5 — No diverging release shape.** `.releaserc.json:46-55` commits release artifacts
  back to main (`@semantic-release/git`: CHANGELOG.md, package.json, terraform
  versions.tf). A release host that is not the origin host therefore **forks main** and
  breaks the push-mirror (non-fast-forward). Consequence: *"move semantic-release to
  GitHub" and "GitLab stays origin" cannot both hold.* The release-home decision is
  jointly the repo-host decision — this is the one structural fact the findings had not
  yet surfaced.

## 4. Decision — the owner's fork resolved as a sequence

The owner framed three shapes: **(a)** GitHub as destination, **(b)** GitHub as bootstrap
toward AWS MicroVM runners, **(c)** both/split. Grounding shows these are not rivals but
stages: choosing GitHub for the gate is also what keeps the MicroVM lane cheapest to open
later (the MicroVM runner tooling is GitHub-Actions-first — finding-0034 §3). **(a) now;
(b) parked on explicit triggers; arriving at (c) exactly when a workload demands it.**

### D1 — GitHub Actions becomes the authoritative CI gate

Effective when Plan A lands. GitLab pipelines cease to be the gate (they are dead today
regardless). Observed 2026-07-11: Actions already fire on every mirrored main push —
three runs on recent seals, all **red at the `Install` step** (`pip install -e '.[dev]'`,
pre-uv) in `integrity-gate` and `lint-and-test`, while the dependency-free
`import-firewall` job passes (run 29169533661 on `ef9319ea`). So the stale workflow is
not false-green today, it is **red-at-install** — nothing can mistake it for a working
gate, and a re-pointed witness would hard-block deploys until parity lands. Parity is
therefore the first plan, before any attestation move.

### D2 — Rebuild `.github/workflows/ci.yml` to real parity (Plan A)

Port the gate content verbatim from `.gitlab-ci.yml` (the source of truth for commands;
pin them inline at graduation):

- **Toolchain:** uv (`uv sync --frozen --extra dev`), Python 3.12 floor (scikit-network
  wheel constraint, `.gitlab-ci.yml:35-38`), `ubuntu-latest`.
- **ratchet:** `ruff check .` + `uv run python scripts/check_imports.py` (Invariant 2
  static proof, finding-0014) + `pytest -m 'not live and not podman and not needs_vault
  and not needs_restic'`.
- **type-gate:** mypy hard-zero over `core agents eval ops scheduler scripts` + the
  tests/ baseline pinned at exactly 69 (finding-0029; a different count in either
  direction blocks) + `ops.type_gate` Tier-2/bare-ignore scans (`.gitlab-ci.yml:111-127`).
- **vault-axis:** `pytest -m needs_vault` against a `hashicorp/vault` **service
  container** (GitHub Actions `services:` supports this directly — parity with
  `.gitlab-ci.yml:133-162`).
- **security:** semgrep job (replacing GitLab's `Security/SAST` template) + gitleaks job
  (replacing `Secret-Detection`; first run discharges Gate 0's full-history residual).
  Additionally the owner enables GitHub-native **secret scanning + push protection**
  (free on public repos) in repo settings — a console toggle, listed as an owner step.
- **Topology:** jobs independent by default — no stage ordering exists to suppress a
  gate, which is finding-0032's remedy *by construction* (see D6). `concurrency` with
  `cancel-in-progress` replaces `interruptible: true`. Triggers: `push: branches: [main]`
  + `workflow_dispatch`; **no `paths:` filters** (P2). `live`/`podman`/`longitudinal`
  tiers stay local by design (runbook §Verifying), exactly as on GitLab.
- **Not ported, deliberately:** `rules:changes` (a P1-violation workaround; obsolete under
  unlimited minutes) and any `needs:` topology.
- **Same plan:** tombstone `.gitlab-ci.yml` (`workflow.rules → when: never` + a banner
  comment naming this note) so the monthly reset does not resume burning minutes on a
  non-authoritative pipeline. Full deletion awaits the D4 host ruling.

### D3 — Re-point deploy attestation (Plan B)

`ops/ci_witness.py` is hard-pinned to GitLab (`PROJECT`/`API`, `ci_witness.py:28-29`;
GitLab status vocabulary, `:59-66`; manual-job play, `:157-182`; PAT rotation, `:115-154`).
Plan B gives it a GitHub backend with the same contract:

- **Verdict source:** `GET /repos/ascalva/Mind-Palace/actions/runs?head_sha=<sha>` for
  the `ci` workflow. Mapping: `completed`+`success` → green; `completed`+anything else →
  red; `queued`/`in_progress` → pending; no runs → absent. Only `success` is green — the
  witness never guesses.
- **Absent gains a grace window.** Today absent returns immediately
  (`ci_witness.py:88-91`) because GitLab pipelines are created synchronously with the
  push. The push-mirror batches (up to ~5 min), so on GitHub "absent" can mean "mirror
  lag" — the witness retries absent within its existing 600 s poll window before
  concluding. Semantics pinned at graduation.
- **Auth:** unauthenticated reads are rate-limited (60/h/IP — one 600 s poll at 10 s
  intervals consumes it). A fine-grained PAT (`actions:read` + dispatch) lands in
  Keychain as `github-api`, mirroring the `gitlab-api` pattern including `rotate()`.
- **Attestation unchanged:** same `ci_witness / pipeline_green|pipeline_red` emission,
  same chaining to the commit's ingest (P3). `pipeline:<id>` becomes `run:<id>`.

### D4 — Release home = repo-host decision (the ratification ruling this note requests)

P5 forbids the shape "GitLab origin + GitHub-hosted semantic-release with commit-back."
The two coherent shapes, with a recommendation:

- **End-state (recommended): GitHub becomes origin.** `git remote origin` re-points;
  the mirror reverses (GitHub → GitLab) or retires; `@semantic-release/gitlab` →
  `@semantic-release/github`; release runs as a `workflow_dispatch` workflow that the
  witness dispatches after green — exact parity with today's manual-play gate
  (`ci_witness.release()`, `:157-182`). This also unlocks PR/branch CI (the mirror is
  main-only) and consolidates token management on one host. Nothing structural holds the
  project to GitLab: the code-sensor ingests **local** commits, and the only GitLab-side
  dependencies are the `pipeline-fragments` include (dies with the tombstone) and Pages
  (Plan C).
- **Interim (acceptable, default until the owner migrates): GitLab stays origin; releases
  are cut locally** by the owner (`npm run release` with the Keychain GitLab token) —
  semantic-release runs fine outside CI, needs zero runner minutes, and commit-back lands
  on the true origin, so nothing diverges. Releases stay rare, owner-in-loop, and
  decoupled from the (dead) GitLab pipeline.
- **Never: the diverging shape.** Ruled out regardless of the ruling above.

### D5 — GitLab pipeline disposition

Tombstoned in Plan A (D2). Deleted entirely — along with the push-mirror re-pointing —
if/when the owner rules for origin migration in D4. GitLab Pages (the rendered
docstring docs, `.gitlab-ci.yml:164-197`) dies with the tombstone; docs hosting moves to
GitHub Pages (`mkdocs` + `actions/deploy-pages`) as small Plan C. The URL changes
(`*.gitlab.io` → `*.github.io`) — owner-visible, parked below with a default.

### D6 — finding-0032 is closed as subsumed

On GitHub Actions, jobs have no implicit stage ordering — a red release lane cannot
suppress `type-gate`/`ratchet`, which is the entire exposure finding-0032 documented.
The owner-adopted `needs:[]` remedy is delivered **by construction**, not by port. The
standalone GitLab plan is not minted. If the owner's D4 ruling keeps any authoritative
GitLab lane, that lane's plan carries `needs:[]` + the `rules:changes` hygiene
(finding-0034 option 2) as a rider.

### D7 — AWS Lambda MicroVM runners: parked, with wake triggers

The MicroVM lane's value was never minutes (unlimited-free already) — it is **Firecracker
per-job isolation (Invariant 4 at the infra layer) and compute beyond hosted runners.**
No current CI job needs either: every gate runs deterministic tooling over public code;
the tiers that execute models or containers (`live`, `podman`) stay local by design.
Parked with re-entry triggers, any one of which reopens this lane as a new design pass:

1. **CI begins executing untrusted or AI-generated code** — sandbox-tier or
   effector-tier jobs entering CI (Track G wiring; today the max reachable effector tier
   is NONE, finding-0011).
2. **A wanted job exceeds hosted-runner capability** — nested virt/podman tier, live-model
   evaluation in CI, or runtimes beyond hosted limits.
3. **The repo goes private** — the metered cap (2 000 min/mo) returns and P1 pressure
   resumes.

Recorded constraints for when it wakes (from finding-0034, still unverified): GitHub
Actions is the mature integration path (validated by D1 — this note keeps that lane
cheap); ARM64/Graviton-only → arm64 images + service-container behavior to verify;
us-east-1 availability; runner IAM approaches zero — no vault reach, ephemeral
workspaces, per-job VM. The isolation model is the design, not a checkbox.

## 5. Consequences

Graduation (after owner ratification) mints, in order:

- **Plan A — the parity gate** (first; unblocks everything): rebuild
  `.github/workflows/ci.yml` per D2; gitleaks full-history discharge (Gate 0 residual);
  tombstone `.gitlab-ci.yml`. Write scope ≈ `.github/**` + `.gitlab-ci.yml`. Verification
  is crisp (actionlint locally; a mirrored push goes green on GitHub; each gate proven by
  a deliberate red). No stored-data touch.
- **Plan B — witness re-point** per D3: GitHub backend in `ops/ci_witness.py`, Keychain
  `github-api` + rotation, absent-grace semantics, release relocation per the D4 ruling.
  Write scope ≈ `ops/ci_witness.py` + `scripts/ci_witness.py` + `tests/unit/test_ci_witness.py`
  (+ `.releaserc.json`/`package.json` iff D4 rules end-state now).
- **Plan C — docs home**: GitHub Pages via Actions (small; can fold into A if sizing allows).
- **Not minted:** any MicroVM plan (D7 parked); the GitLab `needs:[]` plan (D6 subsumed).

Sequencing vs **bp-014** (ready, enforcement layer): independent write scopes; owner
priority rules. Note-keeping: finding-0034 resolves to this note; finding-0032 resolves
as subsumed (D6). The interim standing rule "pushing is unconstrained" persists until
Plan A lands, then re-tightens to batching by habit (the gate is free but wall-clock and
verdict hygiene still favor unit-boundary pushes).

## Parked decisions

| # | Decision | Default recorded | Re-entry condition |
|---|---|---|---|
| 1 | Repo-host end-state (origin → GitHub) | Interim shape: GitLab origin + local owner-run releases; diverging shape never built | The owner's D4 ruling at ratification; or first mirror/branch-CI friction |
| 2 | MicroVM runner lane | Not built | Any D7 trigger fires |
| 3 | `.gitlab-ci.yml` final deletion | Tombstoned, retained | D4 rules origin migration |
| 4 | Docs/Pages host | GitHub Pages at Plan C | Owner URL preference at ratification |
| 5 | PR/branch CI | None (mirror is main-only; matches today's main-only gate rules) | Origin migration (D4) enables it |
| 6 | GitHub-native secret scanning + push protection | On (owner console toggle at Plan A) | — (free on public repos) |

## Cross-references

- `docs/findings/finding-0034.md` — the warrant-in-fact: runner-minutes bottleneck, owner
  fork (a)/(b)/(c), evening addendum (exhaustion + public mirror confirmed).
- `docs/findings/finding-0032.md` — `needs:[]` topology; disposition D6.
- `ops/ci_witness.py:28-29,59-66,79-99,115-154,157-182` — GitLab pinning, verdict
  semantics, deploy gate, rotation, release play (all re-pointed by Plan B).
- `.releaserc.json:46-63` — commit-back assets + `@semantic-release/gitlab` (the P5
  constraint).
- `.gitlab-ci.yml:1-5,33-71,86-127,133-162,164-197` — `when: always`, ratchet, type-gate,
  vault-axis, pages (the ported gate content).
- `.github/workflows/ci.yml` — stale (pre-uv install, old markers, no type-gate/security/
  release); observed red-at-install on mirrored main (run 29169533661, sha `ef9319ea`,
  2026-07-11).
- `docs/findings/finding-0029.md` — the mypy 0/69 split baseline the type-gate pins.
- `docs/findings/finding-0014.md` — `scripts/check_imports.py` as the Invariant 2 CI proof.
- `docs/findings/finding-0011.md` — effector tiers unwired (grounds D7 trigger 1).
- Gate 0 evidence: tracked-file scan (669 files), full-history pattern scan (0 hits),
  fixture-only PII — orchestrator session 2026-07-11; residual discharged by Plan A's
  gitleaks acceptance item.
