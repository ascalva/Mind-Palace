---
type: design-note
id: dn-core-integrity
status: draft
created: 2026-07-05
updated: 2026-07-05
links:
  - docs/research/security-planes.md
  - docs/design-notes/agent-workflow.md
  - docs/design-notes/sacred-boundary/ (write-channel properties)
  - verdict-authorization (Ed25519 signing, YubiKey dual enrollment)
supersedes: null
warrant: null
---

# Core Integrity: Sealed Attestation of the Executable Base

## 1. Purpose and scope

This note specifies an integrity layer that binds the sealed core to a blessed set of bytes. When sealed, the core refuses to run if any file in its verified set differs from what was signed; when open, it runs freely and reports drift without refusing. The transition between those postures — sealing — is a hardware-gated owner ceremony that reuses the verdict-authorization key, so the whole system has one root of trust.

The design resolves a standing tension explicitly. Integrity enforcement must not strangle development: features are added, code is refactored, hashes churn continuously during a working session. The open/sealed duality is the resolution. Development happens in the open posture (or against a deliberately unsealed core); operation happens sealed. Re-sealing is the checkpoint that admits a new code state into operational trust — the same shape as ratifying a note or approving a plan split, and the third member of the blessing-gate family (see agent-workflow §10).

This is a **hardening, not a bright line**. §11 states the threat boundary honestly: it makes core tampering *loud and refused-when-sealed* instead of silent, rooted in key custody; it is not TPM-grade secure-boot attestation. The bright line remains the network seal and the zone architecture. This layer makes the core's executable bytes self-verifying beneath that seal.

Out of scope: hardware attestation of the boot chain (TPM/measured boot — parked, §14); integrity of the store contents (the store is the knowledge layer, governed by provenance and supersession, explicitly *not* by this manifest — §2, §9); integrity of steering documents that instruct agents but do not execute (parked, §14).

## 2. Principles

The integrity layer is the attestation counterpart to doctrine already in the corpus. It sits *beneath* the three security planes: types enforce properties of code as written, provenance labels the data plane, capabilities the boundary — and integrity attestation guarantees that the code those planes reason about is the code that was blessed (see security-planes cross-ref, §15).

1. **Attestation is not assertion.** Code integrity is a fact about bytes, established by a hash compared against a signature. It is not a claim about the world warranted by provenance. Filing code as core *knowledge* would route an attestation guarantee through the assertion layer and reintroduce circularity. The manifest is config — a precondition for the process — never a store artifact. This is the same category discipline that rejected FIDO2-for-signing and `derived_from`-pointing-at-C.
2. **The check roots outside what it checks.** A verifier that reads its own validity out of the store it protects can be disabled by tampering with that store. The root of trust is acyclic by construction: a signature over a manifest, verified by a minimal preflight the owner has personally audited, with the private key on hardware. The regress is cut at a small, explicit, audited base — not dissolved (§3).
3. **Verify needs the public key; sign needs the token.** The operational path (running the core) contains only a verification capability and a pinned public key. No signing capability exists in that path. Sealing — the only operation that produces a valid manifest — requires the private key on the YubiKey, so it cannot be performed by any agent or by malware lacking the physical token. Asymmetric, for the same reason Ed25519-over-payload was right for verdicts and TOTP was wrong.
4. **Agents produce; the owner blesses.** An agent may edit any code in scope, in open mode, freely. It can never *seal*, because sealing is hardware-gated. So an agent can never bless its own changes into operational trust — exactly parallel to drafting-but-not-ratifying and writing-a-plan-but-not-flipping-it-ready. The blessing-gate family gains a third member, and this one is the strongest: enforced by key custody, not merely by policy.
5. **The enforcement layer is in the set it enforces.** The hooks and the verifier are themselves verified (§8, §9). A sealed core will refuse to run with modified guardrails, so an agent cannot quietly disable its own constraints and continue operating. The system protecting itself is not a slogan here; it is the verified set including the protectors.

## 3. Trust tiers

The trusted computing base is layered. Higher tiers are verified by lower ones; the lowest is verified by the owner and the hardware.

| Tier | Contents | Verified by |
|---|---|---|
| **Root** (irreducible) | The verifier preflight + the pinned public key + the manifest-signing tool | The owner, out-of-band: a recorded hash of the verifier and the pubkey fingerprint, checked independently; the private key lives on the YubiKey |
| **T1 — sealed core** | `core/**` — reasoner, store management, the Dreamer, effector scaffolding | The verifier, against the signed manifest, at every startup |
| **T2 — workflow enforcement** | `.claude/hooks/**`, `.claude/settings.json` (decision: in-set by default, §9) | The verifier, same pass |
| **Excluded — knowledge & artifacts** | The store (SQLite/LanceDB/DuckDB), `docs/**`, session state, caches, journals, findings | Not this mechanism — provenance, ratification gates, and gitignore govern these |

**The irreducible root.** Trust bottoms out somewhere; the honest move is to make that somewhere small and name it. The root is the verifier plus its pinned public key: if an attacker rewrites the verifier, they can swap in their own key and sign with their own private key. Nothing downstream detects that. The mitigation is not another layer of software — it is that the root is minimal enough to audit by eye, and the owner pins its identity out-of-band (verifier hash + pubkey fingerprint recorded on the token metadata or in the password manager, checked when it matters). The manifest-signing tool is Root-tier for the same reason — a compromised generator could sign a manifest that omits tampered files — but it runs *only* at the sealing ceremony, under the owner, with the token, so its exposure window is the ceremony, not continuous operation.

## 4. The integrity manifest

A signed table of `path → content-hash` over the verified set, plus provenance metadata.

**Contents.** Per file: repo-relative path and SHA-256 of its exact bytes. Header: manifest schema version, the inclusion and exclusion globs that defined the set, the git ref at sealing time (provenance only — see below), an ISO-8601 seal timestamp, the signing key fingerprint, and a `posture` field (`sealed | open`).

**Canonical form and signing.** The manifest is written in already-canonical form: keys sorted, UTF-8, LF line endings, no trailing whitespace, terminal newline. The Ed25519 signature is a detached signature over the file's *exact bytes* — `manifest.json` alongside `manifest.json.sig`. The verifier does not re-serialize before checking; it verifies the raw bytes, then parses. This eliminates canonicalization-mismatch bugs — the same byte-exactness discipline that `edit_file` demands and that smart quotes violate.

**Content hashes, not git.** The check hashes the actual working-tree files that will execute, not `git` state. Working tree versus HEAD, index contents, and `.git/**` are all irrelevant to "are the bytes I am about to run the blessed bytes." The git ref in the header is provenance — *what state was blessed* — never the object of the check. (Dimension is a property of the realization, not the graph; the executable bytes are the realization, git is a proxy.)

**Hash choice.** SHA-256 — conservative, ubiquitous, no dependency beyond stdlib `hashlib`. If hashing the tree ever measurably delays startup, BLAKE3 is the faster drop-in (parked, §14). At current core size the pass is sub-second.

## 5. The verifier

**Placement: preflight, upstream of the core.** The verifier is not imported by the core; it runs *before* it. The entry point is a thin wrapper: invoking the core starts the verifier, which hashes the verified set, verifies the signature with the pinned public key, compares hashes to the manifest, and only on a clean result hands off (exec/import) to the core. On mismatch in sealed posture, it refuses the handoff and exits nonzero.

**Verify-only, dependency-minimal.** The preflight contains a single vetted Ed25519 *verify* path (no signing) and stdlib hashing. It is deliberately small enough to read in one sitting, because it is Root-tier (§3) and its auditability *is* the security property. No part of the operational path can sign.

**Refuse behavior is loud and diagnostic.** On a sealed-mode mismatch the verifier prints exactly what diverged — each offending path with expected versus actual hash — before exiting. This doubles as a "what changed" report and matches the fail-loud posture of the workflow hooks (agent-workflow §6): the alarm names the intruder, it does not merely trip.

**Open-mode behavior.** In open posture the verifier still runs and still computes drift, but hands off regardless, emitting the drift as an advisory line. Development is never blocked; you always know what has moved since the last seal.

## 6. Two postures: open and sealed

The `posture` field in the signed manifest drives a two-state lifecycle. This is the mechanism that lets one system be both a live development workspace and a hardened operational core.

| Posture | Verifier on drift | Intended use |
|---|---|---|
| **open** | Reports, hands off | Active development, refactors, feature additions — hashes churn freely |
| **sealed** | Refuses handoff, exits loud | Operational runs: the Dreamer over the authoritative store, anything trusted against real data |

```
        seal (ceremony, §7)
  open ─────────────────────▶ sealed
   ▲                            │
   │      unseal (ceremony)     │
   └────────────────────────────┘
        re-seal = unseal → edit → seal at new state
```

The working rhythm is **develop → test → seal → operate**. To change sealed code you unseal (a ceremony), make changes in the open window, then re-seal, which regenerates and re-signs the manifest at the new state. Both edges of the transition are hardware-gated owner ceremonies (§7); the edits between them are ordinary work an agent may perform. The seal is what converts "code an agent wrote" into "code blessed for operation," and only the owner holds that conversion.

Note the graceful-degradation property: because the *edits* happen in open mode, builder sessions never run against a sealed core, so integrity enforcement and the build loop never collide. You do not fight the seal to develop; you step out of it and step back.

## 7. The seal ceremony — the third blessing transition

Sealing (and unsealing) is owner-manual, hardware-rooted, and inaccessible to agents. It is the third member of the blessing-gate family (agent-workflow §10: ratify a design note; approve a plan split; **seal the core**), and mechanically the strongest of the three.

**Procedure.** With the YubiKey present: the signing tool enumerates the verified set by the inclusion/exclusion globs, hashes each file, assembles the canonical manifest with `posture: sealed`, and produces a detached Ed25519 signature via the token (OpenPGP or PIV applet, touch-to-sign). Unsealing is the same tool flipping `posture: open` and re-signing — an unsealed state is still a *signed* state, so the manifest is always authentic; posture says whether drift refuses or merely reports.

**Why it needs no hook to be safe from agents.** The other two blessing transitions are hand-edits an agent is *forbidden* to make, enforced by `gate-guard` denying the write (agent-workflow §6). This one an agent *cannot* make even if every hook failed open, because producing a valid manifest requires the private key on the physical token, which the agent does not have. Its root is custody, not policy — so it degrades gracefully through a total failure of the workflow-enforcement layer. This is the property that makes it worth building: it holds when other things break.

**Dual enrollment applies.** The signing key is the verdict-authorization key (§15) — two enrolled YubiKeys, primary and backup, from day one, because firmware is not field-upgradable. Sealing inherits that ceremony wholesale; there is one hardware root for verdicts and code alike.

## 8. Self-protection

The verified set includes the enforcement layer, so the protectors are protected.

- The **hooks and `settings.json`** are in-set (T2, §9). A sealed core refuses to run with modified guardrails; an agent cannot edit a hook to disable a constraint and then operate. This mechanizes the intuition behind read-only-ing the constitution and hook scripts — a startup refusal instead of a mutable filesystem bit.
- The **verifier** is in the Root tier and cannot meaningfully verify itself (§2, §3); its integrity is anchored by minimality plus the owner's out-of-band pin. This limit is stated, not hidden — the verifier is the one thing the mechanism cannot bootstrap-check, which is precisely why it is kept small enough to check by hand.

The composition: the store is governed by provenance, the workflow by hooks, the code by the manifest, and the manifest's protectors by the manifest itself down to an irreducible audited root. Self-consistency all the way down until it terminates, explicitly, at the owner and the token.

## 9. Verified set: inclusion and exclusion

The set is defined by globs recorded in the manifest header, so the definition is itself signed.

**In-set (recommended default):**
- `core/**` — the sealed core in full (T1).
- The verifier and manifest-signing tool — the trust root, anchored out-of-band as well (§3).
- `.claude/hooks/**`, `.claude/settings.json` — workflow enforcement (T2). *Decision, §14:* default in-set, so guardrails cannot be silently altered and operated against; revisit if hook churn during development makes frequent re-sealing burdensome.

**Out of set (must be excluded, or sealed mode is unusable):**
- The store — SQLite, LanceDB, DuckDB files and their WALs. Mutable knowledge with its own provenance; hashing it would make every ingestion a manifest violation.
- `docs/**` — design notes (own ratification gate), brainstorms, findings, journals, the book. These change constantly and do not execute.
- `.claude/state/**` — gitignored session state.
- Caches, logs, `__pycache__`, virtualenvs, build products.

The discipline is exact: the verified set is *the code whose precise bytes must be what I blessed for an operational run to be trustworthy* — nothing that legitimately churns, or sealed mode collapses into noise.

## 10. Integration with the workflow

This layer and the agent-workflow machinery share surfaces without redefining each other.

- **Session brief.** The `session-brief` SessionStart hook (agent-workflow §6) reports seal status as world-state: `core SEALED at <ref>` or `core OPEN — <n> files drifted since last seal`. Landing in a bare session tells you which posture you are in and what has moved.
- **Blessing-gate family.** Sealing takes its place beside the two existing gates (§7). No command performs it; the workflow's `gate-guard` need not even cover it, since custody already does — but for defense in depth, an attempted write to the manifest or its signature by an agent session is denied by the scope guard regardless (the manifest path is outside any build plan's write scope, and belongs on the foundation denylist).
- **Bootstrap ordering.** Integrity tooling is built *by* the workflow (§12), then the workflow's own enforcement files enter the verified set. The workflow scaffolds integrity; integrity then seals the workflow. Neither is circular because the sealing step is a distinct, later, owner-run ceremony.

## 11. Threat model and honest boundary

**What this buys.** Against accidental modification, casual tampering, and an agent or process operating with the owner's filesystem permissions but *without the token*: a sealed core refuses to run on any divergence and names what changed. An agent cannot rewrite core code and then bless it into operation; malware on the box cannot silently substitute code and have a sealed core accept it, because it cannot produce a valid manifest without the physical key. Core tampering becomes loud and refused, not silent.

**What it does not buy.** This is not secure boot or TPM-measured attestation. Specifically:
- An attacker who holds the signing token (or compromises the owner's environment *during* a sealing ceremony) can re-sign arbitrary code. Key custody is the whole ballgame; hardware-rooting it (signing capability never on disk, touch-to-sign) is what keeps that bar high.
- An attacker who rewrites the verifier and its pinned key defeats the check, undetected by the mechanism itself. Only the out-of-band pin of the Root tier catches this, and only if the owner checks it. Minimality is the defense; there is no software backstop beneath the root.
- Runtime compromise after a clean handoff is out of scope — this attests bytes at startup, not behavior during execution.

**Framing.** Defense in depth, not a bright line. The bright line is the network seal and the zone architecture; those bound the feasible set. This layer makes the executable core self-verifying beneath them and makes tampering expensive and conspicuous. Sold as more than that, it would be theater; sold as this, it is a genuine and worthwhile hardening consistent with the rest of the system.

## 12. Bootstrap

Graduates as a build plan after ratification. Deliverables:

- The verifier preflight (verify-only, stdlib hashing + one vetted Ed25519 verify path), small and auditable by design.
- The manifest-signing tool (Root-tier; enumerates the set, hashes, assembles canonical manifest, token-signs; supports `seal` and `unseal`).
- The entry-point wrapper that routes core invocation through the preflight.
- Inclusion/exclusion glob configuration; initial manifest generated in **open** posture (development continues unimpeded until the owner first seals).
- Session-brief integration for seal status (§10).

Acceptance criteria:

1. Open posture: a modified `core/**` file is reported at startup; the core still runs.
2. Sealed posture: the same modification causes the preflight to refuse handoff and exit nonzero, naming the file with expected vs actual hash.
3. Sealed posture, clean tree: the core starts normally; startup overhead is sub-second.
4. The seal and unseal ceremonies produce a valid detached signature via the token, and manifest bytes verify against the pinned public key.
5. An agent session cannot produce a valid manifest (no signing capability in the operational path; manifest path denied by the scope guard).
6. A modified hook file, with the core sealed, causes refusal — the enforcement layer is inside the verified set (§8).
7. The out-of-band root pin (recorded verifier hash + pubkey fingerprint) is documented, and an altered verifier is shown to be catchable *only* by that pin — the irreducible limit is demonstrated, not glossed.

The initial manifest ships **open**, so ratifying this note and building the tooling changes nothing about the development experience until the owner chooses to seal for the first operational run.

## 13. Failure modes and mitigations

| Failure | Mitigation |
|---|---|
| Verifier tampered (swap key, sign with own key) | Irreducible root; minimal auditable verifier; out-of-band pin of hash + pubkey fingerprint (§3, §11) — no software backstop, stated honestly |
| Signing token compromised | Hardware root: signing capability never on disk, touch-to-sign; dual-enrollment custody discipline (§7); this is the whole security assumption, named as such |
| Sealed mode blocks development | Open/sealed duality — develop in open, seal for operation; builders never run against a sealed core (§6) |
| Churning files in verified set make sealing unusable | Exact inclusion discipline; store, docs, state, caches excluded by signed globs (§9) |
| Canonicalization mismatch corrupts verification | Sign raw canonical bytes; verifier checks bytes before parsing, never re-serializes (§4) |
| Manifest generator compromised at seal time | Root-tier tool, exposure window limited to the ceremony under owner + token (§3) |
| Startup hashing latency grows | Sub-second at current size; BLAKE3 drop-in parked (§14) |
| Agent edits manifest directly | No signing capability in path → invalid signature → refused when sealed; manifest path on foundation denylist and outside any write scope (§10) |
| Root pin never actually checked by owner | Documented ceremony; the limit is inherent — the mechanism cannot force the human check, only make it cheap (§11) |

## 14. Parked decisions

| Decision | Default recorded | Re-entry condition |
|---|---|---|
| Hardware/measured-boot attestation (TPM) | Software preflight + hardware-signed manifest only | A threat model emerges where the host OS itself is untrusted at boot |
| Steering docs (`CLAUDE.md`, skills) in the verified set | Excluded — they instruct, do not execute | A steering-doc modification is shown to materially alter agent behavior in an operational run |
| BLAKE3 instead of SHA-256 for tree hashing | SHA-256 (stdlib, conservative) | Startup hashing measurably delays core launch |
| `.claude/hooks/**` + `settings.json` in verified set | In-set (self-protection default, §9) | Hook churn during development forces re-sealing often enough to be burdensome |
| Continuous / runtime integrity re-checking | Startup-only attestation | A threat requiring detection of mid-run substitution is identified |

## 15. Cross-references

- `docs/research/security-planes.md` — the three planes (types/provenance/capabilities over code/data/boundary). Integrity attestation sits *beneath* them: it guarantees the artifact the planes reason about is the blessed artifact. The foundation-file denylist originates there; the manifest path joins it (§10).
- `docs/design-notes/agent-workflow.md` — the blessing-gate family (§7, §10) and the fail-loud hook posture (§5) this note extends; `session-brief` carries seal status (§10); the workflow builds the integrity tooling and its enforcement files then enter the verified set (§12).
- Verdict authorization (Ed25519 over canonical payloads; YubiKey 5, OpenPGP/PIV, dual enrollment) — the manifest reuses this key and ceremony wholesale, giving verdicts and code one hardware root of trust (§7).
- Sacred Boundary design set — the four write-channel properties; the manifest is attributable (signed), append-only in spirit (each seal a new signed state, prior states inspectable in history), and un-purchasable (custody-gated, not policy-gated).
- `docs/PROGRESS.md` — receives a checkpoint entry when this note is filed, and when the integrity build plan completes.
