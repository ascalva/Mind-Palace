---
type: design-note
id: dn-inner-outer-core
status: draft            # draft → ratified → superseded.  draft→ratified is an OWNER-ONLY hand edit.
created: 2026-07-20
updated: 2026-07-20
links:
  - docs/brainstorms/inner-outer-core.md           # THE WARRANT — the 2026-07-18/19 owner brainstorm + the 2026-07-20 layout directive
  - docs/brainstorms/hypothetical-subspace.md      # the first concrete outer-ring consumer (grounded in §2.8; NOT designed here)
  - docs/findings/finding-0103.md                  # the outer ratchet (19 → 0) this note refines, never launders
  - tests/unit/test_core_self_containment.py       # the existing outer scanner — UNCHANGED by this note
  - ops/import_lint.py                             # NETWORK_MODULES, the audited ban set the v1 predicate reuses (DRY)
  - docs/design-notes/agent-taxonomy.md            # "core-resident" refines to outer-core-resident; the computation agrees (§2.8)
  - docs/design-notes/capability-scope-algebra.md  # the algebra the inner ring is the code-side home of
  - docs/build-plans/bp-065/plan.md                # precedent: math→core, clean break, no alias wrappers
  - docs/build-plans/bp-067/plan.md                # precedent: the config split that put core.config inside the perimeter
supersedes: null
superseded_by: null
warrant: null
---

# Inner core / outer core — the two-ring refinement of core self-containment

> Composed at **fable** (`claude-fable-5`, 2026-07-20, session-39 dispatched design pass). Filed as
> `draft`; ratification is an owner-only hand edit. **Design only; the single build this note
> licenses is §3's M0 plan.** Every membership claim below is **computed, not asserted**: the
> fixed point was run over `core/**` at `dcf76b7` (135 modules) with an AST scanner extended from
> `tests/unit/test_core_self_containment.py` (relative-import resolution + third-party
> classification + closure iteration). Re-run at build time; the numbers here are evidence, not
> the enforced artifact.

## 1. Purpose and scope

`core/` is heterogeneous: a pure mathematical/algebraic kernel, a boundary/invariant layer, and
administrative machinery. The owner decided (brainstorm capsules 2026-07-19 and 2026-07-20) to
split it into two rings, and fixed four pillars this note designs **within, not around**:

1. Membership is **mechanical**: inner core = the maximal import-closed subset of `core/**` over
   {stdlib, pinned pure-math third-party (numpy/scipy), the inner ring itself} — computed, never
   curated.
2. **Two nested ratchets + a direction law**: a new inner-ring test born green; the existing outer
   ratchet **unchanged**, still counting 19 → 0 over ALL of `core/`; outer imports inner, never
   the reverse. Explicit no-laundering clause.
3. Rings run through **modules, not packages**.
4. The eventual repo structure **physically reflects** the separation (owner directive,
   2026-07-20) — target layout and migration path are first-class here (§2.7).

This note decides: the v1 membership predicate and its one sharpening (§2.1); the closure
semantics (§2.3); the enforcement artifacts, test by test (§2.4); what "inner" does and does not
mean (§2.5); the disposition of finding-0103's four strata-overlapping parked inversions under
the ring lens (§2.6); the target directory layout and the migration sequence with the
no-laundering clause intact at every step (§2.7); and the grounding of the ring boundary against
its first consumer (§2.8).

**Out of scope:** the hypothetical-subspace design itself (it graduates separately after this
note reaches draft — its brainstorm's parked decision); any change to the outer ratchet test; any
relaxation of any finding-0103 obligation; the sibling packages (`eval`, `ops`, `scheduler`, …)
— they are machinery *outside* core and are untouched by ring vocabulary (§2.8, the three-zone
picture).

## 2. Principles / decision

### 2.1 The membership predicate, v1 — import-grain, with one computed-forced sharpening

The decided formula, applied literally (base = stdlib ∪ {numpy, scipy}), produces an
indefensible artifact: **`core/models/ollama_client.py` (urllib — the loopback HTTP client) and
`core/sealing.py` (socket) land INSIDE the inner ring**, because `urllib` and `socket` are
stdlib. An "inner core" containing the repo's only two network-capable core files (the audited
`NETWORK_ALLOWLIST` of `ops/import_lint.py`) would poison the term on day one. The literal
predicate computes to 59 strict members including `models/*`, `agent.py`, `sealing.py`, and
`ingest/embed.py`.

**Decision (v1):** the admissible base is

> **(stdlib ∖ `ops.import_lint.NETWORK_MODULES`) ∪ {numpy, scipy}**,

i.e. the inner ring's import closure may touch the stdlib *minus the audited network-capable
set*, the two pinned pure-math libraries, and the ring itself. This stays entirely inside the
mechanical spirit of pillar 1: it is still import-grain, still AST-computable, still zero
judgment calls — the subtraction reuses the **already-audited** ban set that `ops/import_lint.py`
maintains (DRY: no new taste surface, one source of truth for "network-capable"). Consequence:
**inner ⊆ network-incapable is a theorem with an empty allowlist** — the two allowlisted files
are structurally outer, and the inner ring inherits the import-firewall guarantee for free.

Scanner semantics (both rings, identical): absolute imports + resolved relative imports;
`TYPE_CHECKING` imports and lazy in-function imports **count** (the outer scanner already counts
them — e.g. `core/factory/factory.py`'s TYPE_CHECKING reach is among the 19; `ast.walk` sees
function bodies, so `core/complex/temporal.py`'s lazy `import duckdb` at `:153` counts).
Limitation stated honestly: string-based `importlib.import_module` calls are invisible to both
scanners — falsifier F7 below.

**Is import-closure sufficient, or must v1 forbid I/O / clock / env reads?** Decision: **v1 is
import-grain only** — no call-level purity analysis. Rationale: (a) every enforcement surface
this repo trusts is import-structural (the outer ratchet, the import firewall, the P1 boundary
tooth) — call-grain analysis (`datetime.now` vs the `datetime` type, `open`, `os.environ`) is a
different, brittler machine with a large false-positive surface, and nothing yet consumes the
stronger guarantee; (b) the honest cost is named in §2.5: inner does **not** mean effect-free in
v1. The effect-free refinement is parked with a computed preview and a re-entry condition
(Parked, P1). **Falsifier for the sufficiency claim (F1):** a consumer builds on "inner ⇒
effect-free" and a store write / env read / clock read under an inner label breaks a real
guarantee — that fires P1's re-entry, and the v2 predicate activates.

### 2.2 The computed membership — evidence, with every surprise flagged

At `dcf76b7`, under the v1 predicate: **51 strict members** (runtime-true semantics, §2.3) of
135 core modules; 68 under lax (per-module) semantics. Full list in Appendix A. Against the
brainstorm's expected seed:

| Expected | Computed | Verdict |
|---|---|---|
| `core/scope.py` | IN | as expected — the algebra is inner |
| `core/agent_scope.py` | IN | as expected |
| `core/complex/*` | **SPLIT 5/11 files** | **surprise** — `balance, curvature, hodge, laplacian, support` (+ the already-thin `__init__`) are in; `spectral` (sknetwork via `core/typedshims/sknetwork.py`), `topology` (ripser), `temporal` (duckdb, lazy+TYPE_CHECKING), `blocks`/`cut` (closure via spectral), `build` (closure via `core.dreaming`) are out. The spectral half of the reasoning complex is **not** inner under v1. |
| `core/graph/composed.py` | lax-IN, strict-OUT | **surprise** — pure by its own imports (numpy only); excluded solely because `core/graph/__init__.py:19,30` re-exports `conductance`/`sigma_star`, whose closure reaches `eval`. Packaging-blocked, not import-blocked (§2.3). |
| recursion (`recursion.py`, `recursion_ops.py`) | IN | as expected |
| split: `sigma_star` math vs `acquire_mirror_cut` | **REVISED** | the module-level cut vertex is `core/temporal/spine.py` (one eval import, `spine.py:98` → `eval.harness.store.EvalResultsStore`), imported at `sigma_star.py:58`. If the spine inversion lands (§2.6) and the attestation packaging is thinned, **spine itself becomes inner-eligible and sigma_star may come in whole** — the bp-065-style within-module split is *not forced*. The fixed point found a cheaper remedy than the brainstorm predicted. |
| split: `dreaming/cluster` vs pipeline | **REVISED** | `cluster.py` is already clean (numpy-only). The blocker is packaging: `core/dreaming/__init__.py:13-25` pulls the full pipeline (`dreamer` → `core.attestation` → cryptography). No within-module split needed — a packaging remedy (§2.3/§2.7). |

**The three large surprises, stated plainly:**

1. **The sqlite store layer is inner.** 15 of 19 `core/stores/*` modules (+ the thin package
   `__init__`) compute inner: `sqlite3` is stdlib, and `chatlog`, `derived`, `edges`,
   `rawstore`, `runledger`, `sourceset`, `catalog`, `causal_edges`, `chat_events`,
   `agent_observations`, `authored_supersession`, `code_observations`, `observation_history`,
   `reference_edges`, `versions` import nothing beyond stdlib + `core.config` +
   `core.provenance`. Only `vectorstore` (pyarrow), `telemetry` (duckdb), `curated_store`
   (closure via vectorstore), and `verdicts` (closure via `core.verdict.payload` → attestation)
   are outer. The seed intuition "stores are administrative ⇒ outer"
   is **not what the decided predicate computes**. §2.5 resolves this honestly rather than
   curating it away.
2. **The literal predicate admits the network.** §2.1's sharpening exists because the
   computation demanded it — `ollama_client`, `sealing`, `models/*`, `agent`, `ingest/embed`
   are inner under the un-sharpened formula and outer under v1.
3. **Packaging is load-bearing — "directory moves are cosmetic" is falsified.** 17 modules are
   lax-inner but strict-outer purely because an ancestor `__init__.py` drags in an impure
   sibling (list in Appendix A.2; among them `graph.composed`, `dreaming.cluster`,
   `dreaming.graph`, `attestation.record`, `attestation.store`, `factory.{registry,roles,tools}`,
   `verdict.{dispositions,taxonomy}`, `models.registry`, `sandbox.{policy,spec}`). The
   2026-07-19 capsule called repackaging "optional cosmetics"; under runtime-true semantics the
   physical layout *changes membership*. The owner's 2026-07-20 directive (structure reflects
   the split) is therefore not aesthetic — it is the remedy for a computed defect.

Pleasing confirmations: `core/config/loader.py` is inner (bp-067's split vindicated — config
loading sits inside the ring it was moved for); `core/mirror.py` (MirrorView) is inner — the
firewall *vocabulary* is pure even though the machinery that wields it is not; `core/provenance.py`,
`core/constitution.py`, `core/integrator.py`, `core/chat_events.py`, the temporal mathematics
(`boundary`, `complex`, `operators`, `superconnection`) and the View vocabulary (`dreams_view`,
`velocity_view`) are all inner. The dreamer, librarian, and curator all compute **outer** —
the machinery/agents intuition holds exactly where dn-agent-taxonomy predicted (§2.8).

### 2.3 Closure semantics: strict (runtime-true), and what the strict/lax gap measures

Two defensible dependency semantics exist. **Lax**: a module depends only on the modules it
names. **Strict**: importing `core.a.b` executes `core/a/__init__.py` (and `core/__init__.py`),
so a module also depends on every ancestor package of everything it imports.

**Decision: the inner ring is defined and enforced under STRICT semantics.** The ring's promise
— "importing an inner module pulls in only inner + admissible base" — must be true *at runtime*,
or it is not a guarantee, merely a reading. Lax membership is a diagnostic, not a ring.

Consequences, stated as invariants:

- **`core/__init__.py` must stay import-free** (today: a docstring, zero imports). This needs no
  new test: under strict semantics `core` is an ancestor of every module, so a single impure
  import there collapses the computed fixed point to near-empty and the equality test (§2.4)
  goes catastrophically red. Structural, not conventional.
- **The strict/lax gap (17 modules at `dcf76b7`) is the packaging debt**, and it is exactly what
  the physical migration (§2.7) pays off: in the end-state, inner modules live under a subtree
  whose `__init__`s are inner by construction, and strict ≡ lax over that subtree. The gap is a
  *measurable* progress gauge for the migration. **Falsifier (F2):** thinning the responsible
  ancestor `__init__` (or moving the module in M2) fails to promote a listed gap module — then
  the contamination was not packaging-only and the gap analysis was wrong.

### 2.4 Enforcement — the artifacts, test by test (structural-enforcement rule)

Two new files, one small plan (§3 M0). Nothing else changes.

**A. The ring map — `core/rings.py` (new, inner by construction).** A stdlib-only module
declaring `INNER: frozenset[str]` (module names, not paths — survives M2 renames as a mechanical
edit in the move commit) and `MATH_3P: frozenset[str] = {"numpy", "scipy"}`. The map is a
*declaration forced to match a computation* — it exists so that every membership change is a
reviewable diff in exactly one file, named in a plan's `write_scope` (scope-guard therefore makes
every promotion/demotion plan-visible with zero new machinery).

**B. The inner-ring test — `tests/unit/test_inner_ring.py` (new, BORN GREEN).**
Recomputes the strict-v1 fixed point over `core/**` at test time and asserts:

1. `test_inner_ring_is_the_computed_fixed_point` — **computed == declared**, both directions.
   A new impure import in an inner module removes it from the computed set → red until the map
   change is made explicitly (a demotion, §below). A module that *becomes* pure (an inversion
   lands) enters the computed set → red until the map adds it — **promotions are forced to be
   explicit artifacts**, the excavation made visible. New modules are classified automatically:
   pure ⇒ the map must claim them; impure ⇒ outer by default, no action.
2. `test_outer_never_imported_by_inner` — the direction law, asserted explicitly per member with
   its own error message. Mathematically this is a corollary of (1) — an import-closed set
   cannot reach its complement — but the law gets its own named tooth so a scanner regression
   cannot silently retire it. **Falsifier (F3):** an inner→outer import with (1) green means the
   scanner lies; assertion (3) exists to catch that.
3. `test_scanner_sees_known_impurities` — the honesty guard, mirroring the outer test's pattern:
   asserts the computed exclusions include known-outer modules for their known reasons
   (`sealing` via socket, `stores.vectorstore` via pyarrow, `temporal.spine` via eval,
   `complex.spectral` via sknetwork) and that the computed set is non-trivially large. A scanner
   that stops parsing cannot fake a green ring.

The test imports `NETWORK_MODULES` from `ops.import_lint` (tests are machinery; the arrow is
allowed) and `INNER`/`MATH_3P` from `core.rings`. The fixed-point computation itself lives in
the test module. **A deliberate, named DRY exception:** the outer scanner in
`test_core_self_containment.py` is *not* refactored into a shared helper — pillar 2 pins that
file unchanged, and two independent scanners cross-check each other (a bug in one cannot blind
both; the same redundant-sensor argument as its own `test_scanner_sees_the_known_violation_set`).
The audited constant is reused; the 20-line scanner is intentionally not.

**C. The outer ratchet — UNCHANGED.** `tests/unit/test_core_self_containment.py` keeps counting
19 → 0 over **all** of `core/` (its domain is `core.rglob("*.py")` — every file under `core/`
stays bound no matter which ring claims it or which directory M2 moves it to, so long as it
remains under `core/`).

**D. The no-laundering clause, mechanized.** Four bindings:

1. *Domain preservation:* no module leaves `core/**` under this program, ever. A sanctioned
   relocation of a violating module out of core (a legitimate finding-0103 remedy shape) is NOT
   this program: it requires its own owner-blessed plan whose acceptance names the ratchet count
   delta explicitly. The default reading of any count drop is inversion, never relocation.
2. *Move-neutrality:* every M2 migration commit asserts outer-count-before == outer-count-after.
   This is doubly held: structurally (only inner members ever move, and inner members carry zero
   sibling imports **by definition** — violations live exclusively in outer modules, which do
   not move) and by the plan's acceptance re-running the ratchet on both sides of the move.
3. *Ring assignment cannot redefine a violation:* membership is computed from imports; a
   violating module is outer *because* it violates — there is no assignment step a violation
   could hide in.
4. *Map monotonicity:* the inner map may shrink only via an explicit plan line-item (a named
   demotion with rationale). Enforced by process — the map's single-file diff plus scope-guard's
   requirement that a plan name `core/rings.py` — the same tier of enforcement as the outer
   ratchet's "count only decreases." **Falsifier (F4):** a demotion ships without a plan
   line-item naming it.

### 2.5 What "inner" means — and does not mean

The computed ring forces precision the brainstorm did not have. **Inner core (v1) = the
self-contained, network-incapable substrate**: the region of core whose runtime import closure
is stdlib-minus-network + pure math + itself. Its heart is what the owner named — the scope
algebra, the spectral-family mathematics that survives the 3p test, the graph math, provenance,
the View vocabulary, the Constitution frame — but its full extent, mechanically, also contains
the **sqlite store layer and the config loader**. That is not a bug in the computation; it is
the predicate telling the truth: those modules are dependency-austere, audit-small, and
structurally incapable of egress. In CONSTITUTION §II.1 terms, the inner ring is precisely the
region where private data and network capability *provably* cannot meet — and the vault-side
store code belongs to the private-data side of that line.

What v1 inner does **not** mean: effect-free. An inner module may read env (`config.loader`),
touch disk (`stores/*`), or read the clock. Nobody may build on "inner ⇒ pure function" —
that is v2's possible promise, parked (P1) with its preview computed: subtracting `sqlite3`
from the base yields a 29-module strict ring (scope, agent_scope, the complex math five,
`config.loader`, `mirror`, `provenance`, `constitution`, `matching`, `recursion`, ingest's
text machinery, `rawstore`, `sourceset`, `selfcheck`, `velocity_view`) — recognizably "the
math and the sacred boundaries." If the owner wants *that* ring, the lever is a predicate
amendment to this note (ratified, one line, recompute) — **never** a per-module exception;
curation stays impossible by construction.

The three-zone picture, to prevent a vocabulary slide: **inner ring ⊂ core; outer ring = core ∖
inner; the siblings (`eval`, `ops`, `agents`, `scheduler`, `edge`, `config`) are not core at
all.** "Outer core" never becomes a euphemism for machinery outside core; finding-0103's arrow
(everything → core, never the reverse) is untouched.

### 2.6 The four parked strata-overlapping inversions, under the ring lens

finding-0103's 16 machinery reaches include four that PROGRESS (session-27 game plan, Track 3)
parked as strata-overlapping — they touch the View/strata seam and fold into Track 2
("coordinate, don't invert blind"): `core/sensing.py → ops.effects` (ObservedView),
`core/ops_view.py → {eval.drift, ops.ledger}`, `core/reference_view.py → ops.lifecycle.runs`,
`core/temporal/spine.py → eval.harness.store`. Does the split change their disposition?
**Sequencing: no — all four stay folded into Track 2. Shape and priority: yes, three ways:**

1. **Spine is revealed as the keystone, and its priority rises.** The computation shows
   `spine.py:98` (one line) transitively excludes the entire expected graph-math membership:
   `graph/conductance`, `graph/sigma_star`, `temporal/atlas` directly, plus `core/graph/
   __init__` and therefore `graph/composed` under strict semantics. No other single violation
   blocks four-plus expected inner members. The spine inversion (harness-side store injected or
   the readings read moved to eval — the machinery calls core, core returns data) is the
   highest-leverage single edit in the entire 19→0 program *for the inner ring's growth*.
   Honestly computed caveat: post-inversion, spine is **lax**-inner only until its
   `core.attestation.store` import stops strict-contaminating it (`core/attestation/__init__.py`
   pulls `crypto` → cryptography); full promotion needs the inversion **plus** the attestation
   packaging remedy (thin `__init__` or the M2 move of `attestation/{record,store}`). The ring
   map and test make this chain visible instead of vibes: each landing turns a named set of
   modules green.
2. **Each inversion acquires a computed target-state.** `sensing`, `ops_view`,
   `reference_view` are leaf violations — no other core module imports them except
   `temporal_view → reference_view` — so their inversions promote {self} (+`temporal_view` for
   reference_view). When Track 2 rebuilds these Views over the strata-access machinery, the
   ring test states the acceptance mechanically: **born inner-eligible** (pure over injected
   handles) or consciously outer, but decided by computation at the plan's seal, not assumed.
3. **The laundering guard binds them explicitly.** The tempting remedy — relocate
   `sensing.py`/`ops_view.py` into `ops/` so the ratchet stops seeing them — is exactly clause
   §2.4-D1: out-of-core relocation is its own owner-blessed decision with the count delta named,
   never a side effect of a Track-2 build.

Non-strata inversions get the same treatment for free: the map delta of every future
finding-0103 plan is part of its diff (e.g. the shadow.py inversion promotes nothing by itself —
`shadow` stays outer via its dreaming ancestors — which the plan will know *before* building,
the ground-before-building rule applied to ring expectations).

### 2.7 The physical end-state and the migration path (owner directive, first-class)

**Target layout — decision: one-sided `core/kernel/`.** The inner ring physically lives at
`core/kernel/**`, preserving relative subpaths (`core/scope.py → core/kernel/scope.py`;
`core/stores/chatlog.py → core/kernel/stores/chatlog.py`; `core/complex/laplacian.py →
core/kernel/complex/laplacian.py`). The outer ring **stays where it is** — outer is the
complement, `core/**` minus `core/kernel/**`. Rationale: (a) one migration direction, half the
churn — no mass `core/machinery/` move that would touch every outer file for zero enforcement
gain; (b) the separation is fully visible (the kernel subtree *is* the inner ring); (c) the
end-state test becomes self-describing — computed == everything-under-kernel; (d) "kernel" over
"inner" as the directory name because it is a noun that reads in import paths
(`core.kernel.scope`) and matches the owner's founding language; "inner/outer" remain the ring
names in prose. Packages the ring runs through (stores, complex, temporal, ingest, and
post-inversion graph/dreaming) will have two physical homes (`core/kernel/stores/` and
`core/stores/`) — that is the honest physicalization of pillar 3, not an accident to hide.
Rejected: permanent re-export facades to preserve old paths (`core/scope.py` shimming
`core.kernel.scope`) — the owner's no-alias-wrappers rule and bp-065's clean-break precedent;
every move repoints all importers repo-wide in the same commit.

**Migration sequence — four stages, enforcement stated at each:**

- **M0 — enforce the rings in place (the ONE plan this note licenses; no file moves).**
  `core/rings.py` + `tests/unit/test_inner_ring.py`, exactly §2.4. Born green: the map is the
  fixed point recomputed at the build's HEAD (not this note's list — **falsifier F5:** if the
  M0 test lands red, the map was computed at a stale tree; recompute, never hand-edit toward
  green). Write scope: those two files, nothing else. Blast radius: purely additive.
  Sequencing: rides behind the lead build — this program does **not** preempt the diamond
  (brainstorm pin: bp-069 remains the lead).
- **M1 — membership grows as the cleanup lands (riders, no standalone plans).** Every
  finding-0103 inversion / Track-2 plan carries its ring-map delta because the equality test
  forces it; `core/rings.py` joins those plans' write_scopes. The outer ratchet falls 19 → 0 on
  its own track; the inner map only grows (§2.4-D4). Enforcement: both tests, plus scope-guard
  making every promotion plan-visible.
- **M2 — physical migration, per-wave plans, entry-gated.** Begins only after ratification of
  this note AND per-wave stability: a wave may move when its membership has been stable across
  ≥ 2 sealed plans and no open inversion names any module in the wave's closure. Waves must be
  import-closed against kernel-so-far (a wave's members' closures lie within kernel ∪ wave —
  no dangling inner-outside-kernel imports mid-migration). Suggested order (exact manifests are
  computed at graduation, not pinned here — split at graduation, never mid-build): **K1** the
  algebra and math vocabulary (scope, agent_scope, complex_types, provenance, constitution,
  mirror, matching, the complex math five, recursion, recursion_ops, selfcheck…); **K2** the
  store layer + config.loader + ingest text machinery + the View vocabulary; **K3+** the
  post-inversion promotions (graph math, dreaming/cluster, spine…) as they stabilize. Each move
  commit: `git mv` + repo-wide repoint + map rename + **outer count unchanged** (§2.4-D2) +
  inner test green + the full local CI gate. The outer ratchet reaching 0 is **not** a
  precondition for M2 — move-neutrality is structural (only violation-free modules move) — it
  is only a precondition for M3. This decouples the owner's end-state from the slowest
  inversion (the security-sensitive factory/Vault leg) while keeping every step laundering-proof.
- **M3 — the flip.** When map == kernel-tree and the outer ratchet is 0: the test's declared
  side switches from `core/rings.py` to the tree itself (the map becomes derived or retires),
  and the program is complete. End-state statement: `core/kernel/**` is the inner core,
  self-verifying under strict semantics (strict ≡ lax over the kernel subtree — the packaging
  debt of §2.3 is provably zero); `core/**` minus kernel is the outer core; the outer ratchet
  stands green as the permanent perimeter.

### 2.8 Grounding the boundary — the first consumer, and the taxonomy

**The hypothetical subspace** (its brainstorm; NOT designed here) decomposes cleanly on the
computed boundary, which is the grounding pillar 4 asked for:

- *Machinery (outer ring, or not core at all):* the TTL sweep and dispatch (scheduler-side —
  a sibling, outside ring vocabulary entirely); the dispatched dreaming agent
  (`core/dreaming/dreamer.py` — computed outer, closure via attestation); the staging store —
  role-wise machinery, though if sqlite-backed it may *compute* inner, which is fine: **rings
  classify import closures, not roles** (roles stay dn-agent-taxonomy's vocabulary; the two
  labelings are orthogonal and both true).
- *Mathematics (inner ring, some of it pending):* the graph ∪ subspace assembly is
  `core/graph/composed.py` — inner-target, today packaging-blocked (§2.2), promoted by the
  spine inversion + graph `__init__` remedy or the K3 move; σ*/conductance likewise. **One
  honest flag for the subspace design pass:** the influence metric's *spectral* half
  (`core/complex/spectral.py`) is outer under v1 (sknetwork) and will not enter the inner ring
  without a dependency decision that is out of this note's scope — the subspace note should
  treat instrument purity per-instrument, not assume "the instruments are inner."
- *Isolation:* a View-firewall variant for hypothetical reads is inner-eligible vocabulary —
  `core/mirror.py` (computed inner) is the precedent shape.

**The taxonomy tie:** dn-agent-taxonomy's "core-resident" refines to **outer-core-resident**,
and the computation *agrees* rather than stipulates: the dreamer, librarian, and curator all
compute outer; the algebra they are clients of (`scope`, `agent_scope`) computes inner. The
inner core is not an agent — it is the vocabulary agents are written in; nobody grants you
arithmetic. The data-side symmetry stands: 𝔇 ungrantable at the center with grantable strata
around it; the code side now has the same geometry, with `CONSTITUTION.md` to data what the
inner ring is to machinery.

## 3. Consequences

- **Licenses exactly one build plan now (M0):** `core/rings.py` + `tests/unit/
  test_inner_ring.py` — one session, additive-only, born green, no store or behavior change.
  Acceptance and falsifiers are §2.4/§2.7-M0 verbatim; the plan recomputes the membership at
  its HEAD and treats Appendix A as expectation, not authority.
- **Amends the working shape of future finding-0103 plans (M1 riders):** each inversion plan
  adds `core/rings.py` to write_scope and states its expected promotion set in §3-grounding
  (ground-before-building applied to ring deltas). No plan re-blessing needed for already-sealed
  work; this binds plans minted after ratification.
- **Licenses the M2 wave plans and the M3 flip** upon ratification + the §2.7 entry gates; each
  wave graduates as its own small plan with computed manifests.
- **Feeds the book:** the two-ring geometry + the "excavation, not stain-removal" reframe of the
  finding-0103 program is a chapter-arc candidate once M1 shows motion (scribe debt, not now).
- **Does not** change the outer ratchet, the deploy-gate policy (finding-0105 decision-A
  deselection is unaffected — the inner test is green and never deselected), `MIRROR_READABLE`,
  the denylist 𝔇, or any sibling package.

## Parked decisions

| # | Decision | Default recorded | Re-entry condition |
|---|---|---|---|
| P1 | v2 effect-free predicate (base further ∖ {sqlite3, …}) | NO for v1; computed preview recorded: 29 strict members | falsifier F1 fires (a consumer needed inner ⇒ effect-free), or the hypothetical-subspace design wants "provably effect-free" as an isolation grant |
| P2 | two-sided layout (`core/machinery/` for outer) | one-sided `core/kernel/` only | recurring misplacement/confusion in review during M2 (the two-home packages prove costly in practice) |
| P3 | extract the fixed-point computation from the test into `ops/` | computation lives in `tests/unit/test_inner_ring.py` | a second consumer materializes (statusline gauge, M2 tooling) |
| P4 | per-module `# ring:` header annotations | none — `core/rings.py` is the single declaration | reviewers repeatedly lack ring context at the file level |
| P5 | type-only (`TYPE_CHECKING`) import exemption for the inner ring | counted, same as the outer scanner | a genuine type-only inner need arises AND the laundering risk is argued down in a design pass |
| P6 | "librarian" = curator vs retrieval-serving agent (carried from the brainstorm) | vocabulary only; computed outer either way | its own design pass |
| P7 | `sknetwork`/`ripser` dependency decisions for the spectral/topology math | outer under v1; no shim work | the subspace or instrument program needs spectral math inside the ring |

## Falsifiers (the load-bearing set, collected)

- **F1** (§2.1) — v1 sufficiency: an effect under an inner label breaks a consumer's inferred
  guarantee ⇒ activate P1.
- **F2** (§2.3) — packaging-debt claim: thinning the named ancestor `__init__` fails to promote
  a gap-listed module ⇒ the contamination was not packaging-only.
- **F3** (§2.4) — scanner honesty: an inner→outer import observed with the equality test green
  ⇒ the scanner lies; the known-impurities guard must be extended.
- **F4** (§2.4) — map monotonicity: a demotion ships without an explicit plan line-item.
- **F5** (§2.7) — born-green: M0's test lands red ⇒ stale membership computation; recompute at
  HEAD, never hand-edit the map toward green.
- **F6** (§2.4-D2) — move-neutrality: any M2 commit where the outer ratchet count changes.
- **F7** (§2.1) — scanner blind spot: a string-based dynamic import (`importlib.import_module`)
  smuggles an inadmissible dependency into an inner module. Both scanners share this limit; if
  observed, the scanner grows a `Call`-node check for `importlib` in inner members.

## Appendix A — the computed membership at `dcf76b7` (v1 predicate)

### A.1 Inner ring, strict semantics — 51 of 135

```
core                                    core.recursion
core.agent_scope                        core.recursion_ops
core.chat_events                        core.scope
core.complex                            core.selfcheck
core.complex.balance                    core.stores
core.complex.curvature                  core.stores.agent_observations
core.complex.hodge                      core.stores.authored_supersession
core.complex.laplacian                  core.stores.catalog
core.complex.support                    core.stores.causal_edges
core.complex_types                      core.stores.chat_events
core.config                             core.stores.chatlog
core.config.loader                      core.stores.code_observations
core.constitution                       core.stores.derived
core.dreams_view                        core.stores.edges
core.ingest                             core.stores.observation_history
core.ingest.amend                       core.stores.rawstore
core.ingest.chunk                       core.stores.reference_edges
core.ingest.logseq                      core.stores.runledger
core.ingest.pipeline                    core.stores.sourceset
core.ingest.verify                      core.stores.versions
core.integrator                         core.temporal
core.matching                           core.temporal.boundary
core.mirror                             core.temporal.complex
core.provenance                         core.temporal.operators
                                        core.temporal.superconnection
                                        core.typedshims
                                        core.velocity_view
```

### A.2 Packaging debt — lax-inner, strict-outer (17): promoted by `__init__` thinning or M2

`attestation.record`, `attestation.store` (via `core/attestation/__init__` → crypto);
`complex.build` (via `core.dreaming`); `dreaming.cluster`, `dreaming.graph`, `dreaming.rnd`
(via `core/dreaming/__init__` → dreamer → attestation); `factory.registry`, `factory.roles`,
`factory.tools` (via `core/factory/__init__` → factory.factory, a sibling violation);
`graph.composed` (via `core/graph/__init__` → sigma_star/conductance → spine → eval);
`models.registry` (via `core/models/__init__` → ollama_client); `research.airlock`,
`research.criteria` (via `core/research/__init__` → rank → ingest.index → vectorstore);
`sandbox.policy`, `sandbox.spec` (via runner → wasmtime);
`verdict.dispositions`, `verdict.taxonomy` (via payload → attestation).

### A.3 Notable exclusions and their computed reasons

| Module(s) | Reason |
|---|---|
| `sealing`, `models.ollama_client` | network stdlib (socket / urllib) — the two `NETWORK_ALLOWLIST` files, outer by the v1 sharpening |
| `models.*`, `agent`, `ingest.embed` | closure via `ollama_client` |
| `attestation.crypto`, `attestation.verify` | cryptography (pinned, not pure-math) |
| `complex.spectral`, `complex.topology`, `complex.temporal` | sknetwork / ripser / duckdb (lazy + TYPE_CHECKING both counted) |
| `stores.vectorstore`, `stores.telemetry`, `stores.curated_store` | pyarrow / duckdb / closure |
| `sandbox.runner`, `ingest.watch`, `typedshims.{lancedb,psutil,sknetwork}` | wasmtime / watchdog / shimmed 3p |
| `shadow`, `effect_proposal`, `factory.factory`, `interface`, `ops_view`, `reference_view`, `sensing`, `spine` | the 19 sibling violations (finding-0103) — the 8 violating files |
| `graph.*`, `temporal.atlas` | closure via `spine` (the keystone, §2.6) |
| `dreaming.*`, `curator`, `librarian`, `verdict.*`, `stores.verdicts`, `runtime`, `vitals`, `research.*`, `temporal_view` | closure via the above |

Counts under the alternatives, for calibration: decided-literal predicate 59 strict / 75 lax
(admits the network client); v1 51 / 68 (this note); v2 preview (∖ sqlite3) 29 / 42 (P1).

## Cross-references

`docs/brainstorms/inner-outer-core.md` (both capsules — the warrant) ·
`docs/brainstorms/hypothetical-subspace.md` (§2.8 grounding) ·
`docs/findings/finding-0103.md` + `tests/unit/test_core_self_containment.py@dcf76b7` (the outer
ratchet, 19 at authoring) · `ops/import_lint.py` (`NETWORK_MODULES`, `NETWORK_ALLOWLIST`) ·
`core/temporal/spine.py:98` (the keystone reach) · `core/graph/sigma_star.py:58` +
`core/graph/__init__.py:19,30` (the packaging block) · `core/dreaming/__init__.py:13-25` ·
`core/attestation/__init__.py:8-21` · `core/complex/temporal.py:26,153` (lazy import counted) ·
`docs/design-notes/agent-taxonomy.md` §2.1 (residence column) ·
`docs/design-notes/capability-scope-algebra.md` (the algebra housed in the ring) ·
`docs/build-plans/bp-065/plan.md` (clean break precedent) · `docs/build-plans/bp-067/plan.md`
(the config split that made `config.loader` inner-eligible) · `docs/PROGRESS.md` session-27
(the Track-2/Track-3 game plan the §2.6 dispositions slot into).
