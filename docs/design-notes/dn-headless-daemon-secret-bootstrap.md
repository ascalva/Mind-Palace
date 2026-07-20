---
type: design-note
id: dn-headless-daemon-secret-bootstrap
status: draft            # draft → ratified → superseded.  draft→ratified is an OWNER-ONLY hand edit.
created: 2026-07-20
updated: 2026-07-20
links:
  - docs/findings/finding-0123.md                    # the problem statement + 4 candidate options
  - docs/findings/finding-0120.md                     # role accounts have no login keychain (proved)
  - docs/findings/finding-0122.md                     # the workflow-plane analogue (env-injection pattern)
  - docs/design-notes/plane-principals.md              # ratified — §3.2 amended by this note (see §3 below)
  - docs/design-notes/vault-runtime-auth.md            # the AppRole/scoped-token model this note leans on
  - docs/design-notes/secrets-management-evolution.md  # superseded, but §3 unseal-problem framing still true
  - docs/runbooks/plane-migration.md                   # §7–§11, re-graduated in §4 below
  - ops/vault/vault-unseal.sh
  - ops/vault/com.mind-palace.vault.plist
  - ops/lifecycle/com.mind-palace.palace-daemon.plist
supersedes: null          # this note AMENDS a clause of dn-plane-principals §3.2, not the whole note —
                           # see §3 "Relationship to dn-plane-principals" below for the exact scope
superseded_by: null
warrant: finding-0123
---

# Headless daemon secret bootstrap — how `ouroboros` gets its boot-time secrets

> Filed by a FABLE design agent as `draft` (chat-side protocol, §8). Ratification is a
> hand edit by the owner — no command performs it, and `gate-guard` denies any agent
> attempt. `/graduate` refuses this note until `status: ratified`.

## 1. Purpose and scope

`finding-0123`: `dn-plane-principals` §3.2 says "`vault-unseal.sh` and the unseal
keychain item migrate [to `ouroboros`]" without grounding that against the reality
`finding-0120` then proved — **a role account has no login keychain**, and a
LaunchDaemon starts at boot, headless, with no wrapper seam to inject an env var (the
mechanism that solved the *workflow*-plane credential problem, `finding-0120`/§5 of
the runbook, does not exist for a system LaunchDaemon: there is no `sudo -u`-launching
parent process to hold a decrypted secret in its own environment).
[GROUNDED docs/findings/finding-0123.md:30-44, docs/runbooks/plane-migration.md:183-222]

This note decides the mechanism by which `ouroboros` — as a headless, at-boot,
role-account `LaunchDaemon` — bootstraps its secrets, and specifically the Vault
unseal key that `ops/vault/vault-unseal.sh:31` reads today. It evaluates finding-0123's
four options against security, non-negotiable compliance, complexity/reversibility, and
macOS empirical feasibility, and recommends one. It re-grounds runbook §7–§11 against
that recommendation.

**Out of scope:** `ci_witness.py`'s `github-api` token and `backup.sh`'s AWS/backup
keys are addressed only to the extent needed to confirm they are *not* blocked by this
decision (§2.4) — their own launch context is unchanged by this note.

## 2. The four options, evaluated

### 2.0 A naming disambiguation the finding elides

Two different things are called "the vault" in this codebase and the finding blurs
them together:

- **The corpus** — `~/.mind-palace/vault`, `0700 ouroboros` per `dn-plane-principals`
  §3.1. This needs **no secret** to access; it's a filesystem permission. Once `chown`
  (§8 of the runbook) lands, `ouroboros` reads it by uid alone.
- **HashiCorp Vault** — the secrets/credential backend
  (`ops/vault/vault-unseal.sh`, `dn-vault-runtime-auth`), a separate rootless-Podman
  process on `127.0.0.1:8200`, started and unsealed today by `com.mind-palace.vault.plist`
  — a **separate** GUI LaunchAgent from `com.mind-palace.palace.plist` (the reasoning
  daemon). [GROUNDED ops/vault/com.mind-palace.vault.plist:1-9,
  ops/lifecycle/com.mind-palace.palace-daemon.plist:1-31 — two distinct `Label`s, two
  distinct plists]

finding-0123's blocked secret is the **unseal key for HashiCorp Vault**, not corpus
access. This distinction matters directly for option 3 below: the corpus's isolation
(`0700 ouroboros`) is untouched no matter which option is chosen here — this decision
only concerns the credential-serving plumbing, never the corpus.

### 2.1 Option 1 — System keychain (`/Library/Keychains/System.keychain`) with an ACL

**Empirical probe run (safe, throwaway, cleaned up):** as the unprivileged
`ouroboros-work` role account (this design session's own uid — the workflow plane,
already migrated), I attempted to add a throwaway item
(`-a mp-probe-0123 -s mp-probe-0123-svc`, junk value, never a real secret) to
`/Library/Keychains/System.keychain`:

```
$ security add-generic-password -a mp-probe-0123 -s mp-probe-0123-svc -w 'throwaway-value-not-real' \
    /Library/Keychains/System.keychain
security: SecKeychainItemCreateFromContent (/Library/Keychains/System.keychain): Write permissions error.
```
rc=195. **Result: write requires root.** No item was created (confirmed by a
follow-up `find-generic-password`, rc=44 "item could not be found" — nothing to clean
up). This is expected and fine: provisioning is a one-time owner (`sudo`) step, same
shape as every other bootstrap secret in the runbook.

**A sharper finding, from `security add-generic-password -help` (run on this
machine, no sudo needed):**

```
    -A  Allow any application to access this item without warning (insecure, not recommended!)
    -T  Specify an application which may access this item (multiple -T options are allowed)
```
[GROUNDED — literal output of `security add-generic-password -help` on this host,
macOS 26.5.2]

**There is no flag to scope a keychain item's ACL to an OS account/uid — only to a
trusted *application* (by path/code-signature).** This is standard Keychain Services
behavior (`SecTrustedApplication`), not something I'm inferring from the help text
alone, but the help text is the closest thing to a citable, on-machine confirmation. The
practical consequence: whatever binary/script is named as the trusted app for an item
(e.g. `/usr/bin/security`, or the `vault-unseal.sh` interpreter `/bin/sh`) is **the
same binary path for every local OS user on the machine** — trusting it does not
restrict *which uid* invokes it. A compromised process running as `ascalva` that
execs the same trusted path would be trusted exactly as `ouroboros` would be.

**Net: Option 1's headline security property — "an ACL grants `ouroboros`, so only
`ouroboros` can read it" — does not hold as macOS Keychain ACLs are actually scoped.**
It is not a regression versus doing nothing (the *file itself*,
`/Library/Keychains/System.keychain`, is `root:wheel 644` — world-readable at the
container level but item *values* still require securityd + app-trust, confirmed by
the write-permission and not-found results above), but the specific isolation
finding-0123 cites Option 1 for ("even an ascalva-login process can't read [it]") is
**not delivered by the ACL mechanism** — only by *which binary* is trusted, which is
uid-agnostic. A plain Unix-permission file (Option 2) with `0600 ouroboros` gives
**strictly stronger uid-based isolation** than a System-keychain item does, because
POSIX file modes have a uid axis and Keychain ACLs do not.

*Owner-to-validate (not run — requires root I don't have in this session):* whether a
non-root `ouroboros` LaunchDaemon can actually **read** an item at boot, before any
GUI login, with no prompt. Standard macOS behavior (System.keychain auto-unlocks at
boot without a login-window unlock, used today for e.g. VPN/Wi-Fi system profiles) —
[INFERENCE, not reboot-tested this session] — is very likely fine mechanically; the
ACL-isolation question above is answered, but "does it read at boot with zero GUI
session present" is not empirically confirmed here.

### 2.2 Option 2 — an `ouroboros`-only `0600` file

Simplest, and per §2.1 not meaningfully weaker on the uid-isolation axis than a
System-keychain item — arguably stronger. But it fails non-negotiable #10 on its
letter: **"Secrets outside code — Keychain/env only."** That line is explicit and does
not carve out an exception for "a scoped, revocable secret is different from the
master key." A bare file is a bare file. This option is **rejected on non-negotiable
grounds**, not on a security-quality basis — the security argument (§2.1) actually
favors it, but CLAUDE.md's non-negotiables are "never violate," not "weigh against
convenience." A file is out unless a future amendment to #10 itself explicitly
carves out narrow-secret bootstrap files — that's a Constitution-adjacent change, well
outside this note's authority.

### 2.3 Option 3 — hybrid: Vault + its unseal LaunchAgent stay `ascalva`-operated

The palace daemon moves to `ouroboros` (as planned); `com.mind-palace.vault.plist`
(the *separate* Vault-server LaunchAgent, §2.0) stays exactly as it is today — GUI
LaunchAgent, `ascalva` session, `vault-unseal.sh` reading `vault-unseal-key` from
`ascalva`'s login keychain, unchanged. **This is the only option that touches zero
bits of the real unseal key's storage or handling** — directly honoring #9 (the vault
is sacred, never auto-modified) by simply never putting it anywhere new.

The daemon (now `ouroboros`) reaches Vault over loopback (`127.0.0.1:8200` — inside
Invariant 1's egress allowlist per `dn-vault-runtime-auth` §1, and inside the pf
anchor's `lo0` carve-out, runbook §10a) using a **scoped AppRole credential**, not the
unseal key. This is not a new idea invented for this note — it is exactly the
architecture `dn-vault-runtime-auth` already specifies (§2 "per-interaction token
lifecycle," §3 "policy taxonomy per agent role"): the palace daemon becomes one more
Vault client, minted a narrow policy (its own KV/dynamic-secret paths — `github-api`,
backup keys, whatever it needs at runtime), never the master unseal capability.

**This does not eliminate the boot-secret problem — it shrinks it.** The daemon still
needs *one* credential at boot (an AppRole `role_id`/`secret_id` pair, or an
equivalent long-lived-but-narrow token) to authenticate to Vault the first time. But
the blast radius is now bounded to whatever that one role's policy permits — revocable
independent of the unseal key, independent of the corpus, independent of every other
Vault-held secret. **For that one remaining secret, §2.1's finding applies just as
much as it does to the unseal key** — the only non-negotiable-#10-compliant mechanism
for a headless LaunchDaemon's own bootstrap secret is still System.keychain (env-in-plist
is not viable — see §2.4). So the concrete recommendation composes Option 3's
architecture with Option 1's mechanism, applied to a much smaller secret. See §3.

**Cost named honestly:** Vault (the process) keeps running inside `ascalva`'s ambient
GUI session rather than moving fully into the core plane. Does this cost anything
against non-negotiable #2 ("network and private data never share a component")? No —
Vault holds *credentials*, not the corpus (§2.0); its presence under `ascalva` does not
expand what `ascalva` can reach (the corpus stays `0700 ouroboros` regardless of where
Vault runs), and `ascalva` is already the most-privileged human account on the box
(`dn-plane-principals` §2: "does not protect against root; sudo is the honest,
deliberate, logged escape hatch"). The isolation this migration is chartered to
deliver — "core has no network," "even an ascalva-login process can't read the
corpus" — is fully intact: `ouroboros` (core) still makes zero off-host network calls
under the pf anchor (Vault-over-loopback is inside the carve-out, same as the model
server), and the corpus is untouched by this decision. What is *not* achieved: Vault
itself does not move into the core-plane's process-isolation boundary. That is a
named, bounded, honest residual, not a silent one.

### 2.4 Option 4 — a boot-time privileged unseal helper

A root-privileged one-shot that reads the secret and drops privilege before handing it
to `ouroboros`. Evaluated and **not recommended**:

- It does not solve the underlying problem — it still needs to *read the secret from
  somewhere* (System.keychain, most likely, since root has no login keychain either),
  so it inherits §2.1's finding (no uid-based ACL isolation) while adding a new
  privileged component on top.
- **Complexity/reversibility is the worst of the four.** A custom privileged helper is
  new code that must be hand-audited for the handoff mechanism itself (how does a
  root process hand a secret to a non-root process without writing it to disk or a
  world-readable pipe? A `SO_PEERCRED`-checked Unix socket is the standard answer, but
  that is meaningfully more surface than any other option — a new attack primitive to
  build and prove correct, not reuse.
- No existing pattern in this codebase does this; every other bootstrap (finding-0120,
  finding-0122, the cockpit wrapper) uses off-the-shelf `security`/`sudo -u`
  primitives. A bespoke privileged helper is the one option that adds a genuinely new
  category of risk for a problem §2.3 already solves with existing primitives at a
  fraction of the complexity.
- (Ruled out on env-in-plist, for completeness, which both this option and Option 3's
  residual secret might otherwise reach for: `com.mind-palace.palace-daemon.plist`'s
  `EnvironmentVariables` dict is a **static, root:wheel 644 file**
  [GROUNDED ops/lifecycle/com.mind-palace.palace-daemon.plist:55-59] — a secret placed
  there is world-readable on disk and visible via `launchctl print`, violating "never
  logged" even though it is technically not "in the repo." Not a candidate for any
  option.)

## 3. Recommendation

**Option 3 (hybrid), with Option 1's mechanism (System.keychain) applied to the one
shrunk secret it leaves.** Concretely:

1. **Vault + `com.mind-palace.vault.plist` stay exactly as they are** — GUI
   LaunchAgent, `ascalva` session, `vault-unseal.sh` unchanged, the real
   `vault-unseal-key` **never moves, is never touched, is never re-keyed** by this
   migration. This is the strongest possible honoring of #9: the sacred secret's
   storage is simply not part of this change.
2. **The palace daemon moves to `ouroboros`** exactly as `dn-plane-principals` §3.2
   already specifies (`UserName ouroboros` in the LaunchDaemon plist — already
   authored, `ops/lifecycle/com.mind-palace.palace-daemon.plist:40-41`).
3. **The daemon becomes a Vault client**, minted a narrow AppRole policy per
   `dn-vault-runtime-auth` §3 (extend the policy taxonomy with a `palace-daemon` row:
   whatever KV paths / dynamic secrets it needs at runtime — likely `github-api`,
   backup-adjacent reads, nothing more).
4. **The one remaining boot secret** (the daemon's AppRole `role_id`/`secret_id`, or a
   long-lived narrow Vault token if AppRole is deferred) is provisioned by the owner,
   once, as a `System.keychain` item ACL'd/trusted to the daemon's invoking path —
   with the **explicit, documented understanding (per §2.1) that this ACL provides no
   stronger uid isolation than a Unix file mode would**. It is chosen anyway, over a
   file, **solely because non-negotiable #10 names Keychain/env as the only compliant
   seam** — not because the ACL adds real protection beyond what "well, root and
   `ouroboros` can both read System.keychain items with the right trust, and so can
   anyone else who can exec the trusted binary" already implies. This is intellectually
   honest rather than reaching for a keychain-flavored placebo without saying so.

**Security rationale, stated against the isolation the finding cares about:**

- **"Core has no network" (non-negotiable #1) — fully intact.** `ouroboros`'s only
  network call is loopback to Vault (127.0.0.1:8200), which is inside the same `lo0`
  carve-out the pf anchor already assumes for the model server
  (runbook §10a). No off-host egress is added.
- **"Even an ascalva-login process can't read the corpus" — fully intact and
  untouched.** This decision never touches `~/.mind-palace/vault` (§2.0); `0700
  ouroboros` lands exactly as `dn-plane-principals` §3.1 specifies, independent of
  where Vault runs.
- **The vault is sacred (#9) — maximally honored.** The real unseal key's storage,
  access pattern, and keychain identity are **unchanged by this migration** — the
  smallest possible diff to the most sensitive secret in the system.
- **#10 (Keychain/env only) — honored for both secrets**: the unseal key stays in
  `ascalva`'s login keychain (as today); the daemon's shrunk AppRole secret goes into
  System.keychain, not a file. The *quality* of the isolation that buys is named
  honestly (§2.1) rather than oversold.
- **What is NOT achieved, named plainly:** Vault (the process) does not move fully
  into the core-plane's process-isolation boundary — it continues running inside
  `ascalva`'s ambient session. This is a bounded, understood residual (§2.3), not a
  silent one, and it costs nothing against the specific properties (#1, #2, the
  corpus) this migration is chartered to deliver.

## 4. §7–§11 re-graduation sketch

- **§7 ("migrate Syncthing + the unseal keychain item to `ouroboros`")** — the
  **unseal-key half of this step is dropped**. Syncthing still migrates as written
  (it serves the corpus, unrelated to this decision). In its place: provision the
  daemon's AppRole/token bootstrap secret into System.keychain (owner, once, `sudo`),
  and extend `dn-vault-runtime-auth` §3's policy table with the `palace-daemon` role.
  `com.mind-palace.vault.plist` is explicitly **not** touched by this step — call that
  out in the runbook so a future reader doesn't "fix" it by moving Vault too.
- **§8 (chown/chmod every lane)** — unchanged; independent of this decision (§2.0).
- **§9 (install the daemon plist, bootstrap system)** — unchanged mechanically; add a
  precondition line: "the daemon's Vault AppRole secret is present in System.keychain
  and readable by the invoking path" (mirrors the existing precondition comment at
  `ops/lifecycle/com.mind-palace.palace-daemon.plist:24-28`).
- **§10 (pf anchor)** — unchanged; the loopback carve-out already covers Vault traffic
  the same way it covers the model server (both are `127.0.0.1` — worth an explicit
  verify line addition: confirm `ouroboros`'s loopback socket to `:8200` alongside the
  existing `:11434` check in §10a).
- **§11 (verifier green)** — `scripts/verify_planes.py` gets one new lane: "daemon
  authenticates to Vault via AppRole, unseal key never touched by `ouroboros`" (a
  read-only assert, same shape as the existing manual-SKIP lanes).
- **`dn-plane-principals` §3.2 amendment (owner-only, on ratification):** the clause
  "`vault-unseal.sh` and the unseal keychain item migrate" is **superseded by this
  note** — the corrected statement is "`vault-unseal.sh` stays under `ascalva`
  unchanged; the daemon (`ouroboros`) becomes a Vault *client* via a separate, narrow,
  System-keychain-provisioned AppRole secret." This is a targeted amendment to one
  clause of §3.2, not a full supersession of `dn-plane-principals` — the rest of that
  note (four principals, the ownership matrix, the cockpit sudo launch, §3.3, §3.4)
  is untouched and this note does not re-litigate it. The owner performs the actual
  text edit to `dn-plane-principals` §3.2 by hand on ratification, same as every other
  ratified-note edit (A8).

## Parked decisions

- **Moving Vault fully into the core-plane boundary** (own `ouroboros` LaunchDaemon,
  own keychain-equivalent bootstrap). Default: parked, per §2.3/§3 — the loopback
  trust boundary already satisfies #1/#2 without it, and moving it adds exactly the
  same boot-secret problem this note works to shrink, for no isolation gain the
  finding actually asked for. Re-entry: if Vault itself becomes a target the owner
  wants inside the core-plane uid boundary for reasons beyond this migration (e.g. a
  future threat-model tightening), or if `ascalva`'s GUI-session dependency for Vault
  becomes an operational pain point (Vault down whenever `ascalva` is logged out).
- **AppRole vs a simpler long-lived scoped token** for the daemon's Vault
  authentication. Default: AppRole (response-wrapped, rotatable `secret_id`) as
  `dn-vault-runtime-auth` §3/§7 already sketches, over a static token, for the same
  reason the rest of that note prefers ephemeral scope — but a single long-lived
  narrow token is an acceptable fallback if AppRole's response-wrapping proves fiddly
  to script for a boot-time reader. Re-entry: whichever build plan implements this
  discovers a concrete blocker with AppRole's boot flow.
- **The empirical read-side confirmation of System.keychain's boot-time,
  pre-GUI-login readability by a role-account LaunchDaemon** (§2.1). Default:
  proceed on the [INFERENCE] that it works (standard macOS behavior for system
  services); re-entry / owner-validation step: after §9 installs the daemon plist,
  the very first boot is the real test — `verify_planes.py`'s new lane (§4) either
  passes or surfaces this immediately, and rollback is a `launchctl bootout` away
  (no different in kind from any other step's rollback risk).
- **`ci_witness.py` (`github-api`) and `backup.sh` (AWS/backup keys)** — confirmed
  **not blocked** by this decision: `ci_witness.py` runs explicitly UNSEALED at the
  ops tier [GROUNDED ops/ci_witness.py:13-16 — "this runs UNSEALED at the ops tier...
  the sealed core never does"], invoked standalone or as a `palace deploy` subprocess,
  never as the `ouroboros` LaunchDaemon itself; `backup.sh`'s LaunchAgent
  (`ops/backup/com.mind-palace.backup.plist`) has **no `UserName` override**
  [GROUNDED ops/backup/com.mind-palace.backup.plist:13-27], so it stays under whichever
  session bootstraps it (today `ascalva`, GUI, login keychain intact) unless a future
  plan explicitly moves it. Flagged as a small residual for the runbook: confirm
  by hand which principal should own the backup LaunchAgent post-migration (it reads
  `$REPO/data` — `ouroboros:palace 0755` per §8 — which stays traversable by `ascalva`
  as today regardless), but this is **not** a finding-0123 blocker and is out of this
  note's scope to decide.

## Cross-references

- Warrant: `docs/findings/finding-0123.md`
- Amends (on ratification, owner hand-edit): `docs/design-notes/plane-principals.md`
  §3.2, the "`vault-unseal.sh` and the unseal keychain item migrate" clause
- Leans on: `docs/design-notes/vault-runtime-auth.md` §2 (token lifecycle), §3 (policy
  taxonomy — extend with a `palace-daemon` row)
- Empirical grounding this session: `security add-generic-password -help` (this host,
  macOS 26.5.2); a throwaway-item write-permission probe against
  `/Library/Keychains/System.keychain` as `ouroboros-work` (uid 551, unprivileged) —
  rc=195 "Write permissions error," no item created, nothing to clean up
- Code: `ops/vault/vault-unseal.sh:31` (unchanged by this note), `ops/vault/com.mind-palace.vault.plist`
  (unchanged), `ops/lifecycle/com.mind-palace.palace-daemon.plist:24-28,40-41,55-59`,
  `ops/ci_witness.py:13-16`, `ops/backup/com.mind-palace.backup.plist:13-27`
- Sibling findings: `finding-0120` (role accounts have no login keychain — proved),
  `finding-0122` (the workflow-plane env-injection analogue, structurally different —
  wrapper-launched vs launchd-launched-at-boot, per finding-0123's own root-cause
  paragraph)
