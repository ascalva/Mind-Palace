---
type: finding
id: finding-0161
status: resolved         # open → routed → resolved | promoted
created: 2026-07-22
updated: 2026-07-22
links:
  - docs/design-notes/code-ingest-pipeline.md          # §2.7 the default-OFF / owner-visible posture
  - docs/findings/finding-0159.md                      # the ON switch is part of finishing (bp-098)
  - docs/findings/finding-0146.md                      # code is a first-class semantic source
  - config/defaults.toml                               # where the shipped default lives
  - config/local.toml                                  # where this instance opts in today
ftype: direction         # a design-default philosophy call — owner's
origin_plan: orchestrator
route: orchestrator      # → owner-questions.md (oq-0034); owner input required
resolution: DEFAULT ON — owner ruled 2026-07-22 that code-ingest ships enabled=true in defaults.toml (the Ouroboros ingests its own code natively). His own reframe settled it: gating-off is a "not-yet", not permanent conservatism. Made the change + tests; §2.7 ratified-note amendment owed (owner-hand). See Resolution.
---

# Should code-ingest be ON by default (defaults.toml), not opt-in per-instance (local.toml)?

## What

Today `[code_ingest].enabled` ships **false** in `config/defaults.toml`; this Mac opts in via
`config/local.toml` (`enabled = true`, 2026-07-22), the same shape as `[secrets]`/`[backup]`. The
owner questions that placement (2026-07-22): **maybe code-ingest should default ON for mind-palace
itself**, because:

- **It is NOT a security issue, and "off" was only ever a "not-yet."** `secrets`/`backup` gate real
  security/credential surfaces, so off-by-default is a firewall. Code-ingest's gate is not that —
  and (owner clarification 2026-07-22) gating a feature off in this project means *a safeguard UNTIL
  WE ARE READY to turn it on; once on it STAYS on.* "Off" is a transitional state (not-yet), not a
  standing conservative posture. So the question is not "flip a permanent default" — it's "we are
  now ready; the terminal state is ON; where should that permanent ON live?" (See
  [[wiring-is-part-of-finishing]]: "dormant-by-design" is banned; the only legit off is
  wired-but-flag-off, i.e. temporary.)
- **The Ouroboros is about self-consumption.** The founding frame ([[ouroboros-naming]]) is a
  system that mines/consumes itself — the palace as a self-map ("mining my own brain",
  [[owner-background-self-mapping]]). Code is a first-class semantic source (finding-0146). A
  system whose whole point is to eat its own tail arguably SHOULD ingest its own code by default,
  not as a per-machine opt-in. "On" would be the philosophically native posture.

## Why it matters

The default encodes what mind-palace *is*. If the Ouroboros self-consumption thesis is load-bearing,
burying code-ingest behind a per-instance opt-in understates it. Conversely, a wrong default is
heavy and silent (finding-0150's lesson): flipping it in `defaults.toml` changes behavior for
*every* consumer of the default, not just this Mac.

> **NOTE (owner, 2026-07-22, folded into the resolution):** the framework-vs-instance framing below
> was thin. `config/defaults.toml` is ALREADY Ouroboros-instance config throughout — `[planes]`
> names the `/var/ouroboros*` principals, the model lineup is this box's M2 Max, the paths / AWS
> region are this deployment's. There is no neutral "framework default" being protected; `local.toml`
> only carries the security-gated opt-ins. So code-ingest defaulting to the Ouroboros-native posture
> (ON) is simply *consistent with the file*, not a special framework decision. Kept below for the
> record of how the question was first posed.

## The crux to deliberate — FRAMEWORK default vs INSTANCE posture

`defaults.toml` is the **framework**'s shipped default; `local.toml` is **this instance**'s posture.
[[ouroboros-naming]] already draws exactly this line: *mind-palace = the framework; the LIVE
system (daemon + evolving corpus) = Ouroboros.* The self-consumption philosophy is an **instance**
property (Ouroboros, this deployment) — which `local.toml` already expresses. Flipping
`defaults.toml` asserts it for **every clone and CI run**, which is a different (stronger) claim.

Technical considerations for the deliberation (recorded neutrally, both directions):
- **Default-ON auto-seeds on first housekeeping.** The `enabled` gate drives the INCREMENTAL sync;
  on a cold store "incremental" embeds everything (= the full seed). So `defaults.toml` ON means a
  fresh clone / CI would fire a heavy first embed unbidden at its first housekeeping tick — the
  exact heavy-op-from-a-flag the §2.7 owner-visible-seed rule was written to avoid. (The deliberate
  `palace code-seed` stays separate either way; the question is only the housekeeping gate.)
- **CI / fresh clones usually can't and shouldn't.** No Ollama in CI, no daemon; a default that
  assumes a live embedder + running daemon is wrong for the framework's non-instance consumers.
- **Middle paths exist** (for the owner to weigh, not decide here): (a) keep `defaults.toml` OFF but
  make the LIVE-instance default ON explicit/documented (status quo, just named); (b) default ON but
  keep the first SEED deliberate and gate the housekeeping auto-embed on "daemon + embedder present"
  (default-on-when-runnable); (c) a distinct "this is the Ouroboros instance" marker that flips a
  set of instance-native defaults together, code-ingest among them.

## Re-entry condition

Owner deliberates (oq-0034). The reframe (owner clarification): the off-in-`defaults.toml` was a
"not-yet", not a permanent default — this instance is now turning it ON to STAY on (via `local.toml`,
already live). So the OPEN part is narrow: **should the FRAMEWORK default (`defaults.toml`, every
clone/CI) ALSO become permanently ON**, given the Ouroboros-self-consumption thesis — or is the
instance-level permanent-on (local.toml) the right home, with `defaults.toml` staying OFF only
because CI/fresh-clones lack a daemon+embedder (not conservatism)? Nothing is blocked; the deploy +
seed proceed under the current local.toml opt-in. A default-ON ruling ⇒ a `defaults.toml` edit
warrant-linked here, with the cold-store auto-embed handled (likely middle-path (b),
default-on-when-runnable).

## Routing

`direction` (design-default philosophy) → **orchestrator → owner-questions.md (oq-0034)**. Owner's
call; not a build or a security fix. A default-ON ruling promotes to a dn-code-ingest-pipeline §2.7
amendment (the owner-visible-seed rule would need the cold-store auto-embed caveat).

## Resolution (owner ruling 2026-07-22)

**DEFAULT ON.** Two owner observations closed it:
1. **"Gated off" is a *not-yet*, not conservatism** — off until we're ready; once on it stays on. So
   the off-in-`defaults.toml` was always transitional; code-ingest ingesting the Ouroboros's own
   code is the native posture (finding-0146).
2. **`defaults.toml` is already the Ouroboros instance's config, not a neutral framework default** —
   `[planes]` names the `/var/ouroboros*` principals, the model lineup is this box's, paths + region
   are this deployment's. So the framework-vs-instance hesitation was illusory: ON-by-default is
   *consistent with everything else in the file*, and `local.toml` remains only the security-gated
   opt-in surface. The [[ouroboros-naming]] framework/instance line is a NAMING distinction, not a
   defaults.toml-vs-local.toml one.

Change made (this session):
- `config/defaults.toml` `[code_ingest].enabled` **false → true** (comment rewritten to state the
  ON-by-default rationale + the opt-out path).
- `config/local.toml` — the now-redundant `[code_ingest] enabled=true` opt-in **removed** (single
  source of truth = the shipped default; a stub comment notes the opt-OUT path).
- `tests/unit/test_code_ingest_wiring.py` — `test_code_ingest_default_on` asserts the SHIPPED default
  (read from `defaults.toml` directly, so a machine's local.toml can't mask it) is `True`; the
  override test flipped to assert an instance can opt **OUT** (`enabled=false`). Green.

**Why default-ON is safe (not the §2.7 heavy-op-from-a-flag hazard):** the daemon refuses to start
without a live Ollama (preflight), so a fresh clone / CI never auto-embeds without an embedder; CI
and test runs don't start the housekeeping loop at all. When the Ouroboros daemon *does* run, its
first housekeeping embeds the cold store (= the seed) — which is exactly the intended behavior now.

**Owed (owner-hand, NOT done here):** `dn-code-ingest-pipeline` §2.7 is RATIFIED (agent-immutable).
Its "the seed is one deliberate, owner-visible run, never auto-run from the flag" wording now
coexists with default-ON (a fresh daemon auto-seeds on first housekeeping; `palace code-seed` remains
the *immediate* deliberate trigger). That §2.7 amendment is an owner-hand edit to the ratified note —
flagged here, left for the owner. Not blocking.
