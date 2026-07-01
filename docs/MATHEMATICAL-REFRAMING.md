# The Mind Palace as Mathematical Structure
### Unified account & reframing direction for code and documentation — companion IV

**2026-06-30 · direction document**

> *Notation: every load-bearing symbol (ρ, π_MR, 𝒜, D(t), 𝔎, …) is defined once in [`NOTATION.md`](NOTATION.md) — symbol ↔ code ↔ object ↔ family. This document (§A) defines the five families that glossary is keyed to.*

The Dreamer is where the *heavy, novel* mathematics lives (companions III). But the system as a whole
is **already composed of mathematical objects and operations** — the firewall is a projection, scope
is a set algebra, the loader and gate are automata, drift is a metric, the raw store is a hash, the
attestation chain is a DAG. This document does two things:

- **Part A — the unified account:** the whole system as a small number of mathematical object
  *families*, with one shared notation, subsuming and extending the companion II invariant catalog.
- **Part B — the direction:** how to reframe the code and documentation to reflect it — *disciplined*,
  non-breaking, and explicit about where **not** to reframe.

---

## 0. The discipline (read this first — it is the point)

The system works and is tested. Companion II already compiled philosophy into invariants. So this is
**unification and propagation, not a rewrite**, and it is governed by one rule, the same minimalism
filter (G8) that already shaped the system:

> **Reframe a piece of code or design mathematically only if doing so (a) makes an illegal state
> *unrepresentable*, or (b) clarifies a *trust boundary* for a reader. Otherwise the mathematics
> belongs in a docstring or a design note, not in a new type or a renamed symbol. Notation must never
> outrun enforcement.**

Three failure modes this rule exists to prevent:

1. **Decoration.** Renaming `Cluster` to `Simplex` or `handles` to `SemilatticeElement` buys nothing
   if the behavior is unchanged — it just raises the reading cost. **Do not.**
2. **Ceremony.** Introducing a mathematical type that does *not* delete an illegal state is cost
   without safety. A `Metric` protocol around `drift()` when `drift()` already works is ceremony.
3. **Notation outrunning enforcement** — the exact G8 failure: asserting a rich structure (a preorder,
   a sheaf, a manifold) that nothing in the code actually uses or checks. If the structure is not
   load-bearing, drop it.

**The positive form of the rule** (why this is worth doing): the system's strongest code *already*
follows it. `MirrorView` is the projection $\pi_{\mathsf{MR}}$ made a type so a non-authored view is
*unrepresentable*. `DerivedStore` has no provenance parameter, so a forged authored inference is
*unconstructable*. `ProposedChange` has no path/diff field, so a code-change proposal *cannot be built*.
Each is a mathematical object turned into a type that makes the wrong state unbuildable. **Reframing =
naming that pattern and applying it deliberately** — to the gaps, and to the Dreamer's new structures.

---

# Part A — The unified account

## A.0 The organizing claim

The Mind Palace is **five families of mathematical objects, plus the composition laws that hold when
they are put together**. One notation (Appendix / `docs/NOTATION.md`) names them all.

| Family | The object | The system pieces it *is* |
|---|---|---|
| **1. Labelings & information-flow** | typed labels in a bounded lattice + monotone/erasure maps | the provenance firewall · the capability ceiling · the airlock de-identification |
| **2. Regenerable derivation** | content-addressed base + pure-function derived + acyclic provenance-of-inference | the raw store · embeddings/chunks · the derivation DAG · attestation chains |
| **3. Guarded transition systems** | small finite automata with a checked guard before each side effect | the two-slot loader · the self-mod gate · the queue lifecycle |
| **4. Metric geometry** | distances on a profile/graph, measured against frozen anchors | the drift gauge · the boiling-frog inequality · diffusion distance · min-cut-to-authored |
| **5. The reasoning complex** | a multilayer, typed, temporal complex + a generalized Laplacian family | the Dreamer, interpreters, adjudicator (companions III) |

Families 1–4 are the **substrate** — the connective tissue of the whole system. Family 5 is the
**engine** — where the heavy math concentrates. The point of this account is that they are **one
mathematical system**, not a mathematical Dreamer bolted to a non-mathematical host.

## A.1 Labelings & information-flow — *the key unification*

The single most clarifying observation: **three subsystems you treat as separate are one object.**

- **Provenance** is a labeling $\rho:V\to P$ into an *unordered* set (G8 retired the order); the only
  load-bearing structure is membership in $\mathsf{MR}=\{\textsf{auth-solo},\textsf{auth-dlg}\}$. The
  **firewall** is the projection $\pi_{\mathsf{MR}}$, made structural by `MirrorView`.
- **Capability** is authority $\mathcal{A}(\text{agent})$ = a *set* of handles, ordered by inclusion
  — a bounded meet-semilattice with top $\textsf{MAX}$. Minting is a **meet**:
  $\mathcal{A}(\mathrm{mint})=\mathrm{scope}\cap\textsf{MAX}$. Skills are **non-widening**:
  $\mathcal{A}(a\oplus\varsigma)=\mathcal{A}(a)$.
- **De-identification** (the airlock) is an **erasure map** $\pi_{\text{public}}$ that projects a
  request onto a label with *no field that can carry note content* (`ResearchCriteria`) — the
  information-flow analogue of the firewall.

All three are the **same pattern**: *typed labels that constrain flow, enforced by making the wrong
flow unrepresentable.* The firewall constrains **read** flow (observed ↛ mirror); the ceiling
constrains **capability** flow (skill ↛ new handle); the airlock constrains **egress** flow (content
↛ network). Recognizing them as one family means one vocabulary, one enforcement discipline
(structural > static > runtime), and one place to reason about non-interference (A.6).

| Instance | Label / map | "Wrong flow" made unrepresentable by | Invariant | Tier |
|---|---|---|---|---|
| firewall | $\rho$, $\pi_{\mathsf{MR}}$ | `MirrorView` (non-MR view untypable) | I6 | structural |
| unforgeable inference | $\rho\equiv\textsf{interpreted}$ | `DerivedStore` (no provenance param) | I5 | structural |
| capability ceiling | $\mathcal{A}$ = handle set | dispatch table = held handles only | I13 | structural |
| airlock de-id | $\pi_{\text{public}}$ | `ResearchCriteria` (no content field) | (Phase 8) | structural |
| self-mod surface | knob registry | `ProposedChange` (no path/diff field) | (Phase 10) | structural |

**[Engineering].** This family is the system's security spine, and it is already almost entirely
structural. The reframing here is *documentation* — name the family, state the shared pattern — not
new code.

## A.2 Regenerable derivation

**Object.** A content-addressed base $H:\mathcal{B}^*\to\Sigma$ (SHA-256, injective by
collision-resistance), write-once; a derived layer that is a **family of pure functions of the raw**
($\text{chunk}$, $e=\text{embed}$), so recomputation is never loss; and an **acyclic
provenance-of-inference** — the derivation DAG (B-hypergraph, companions III) with attestation chains
as signed paths to authored leaves.

**Operations.** $\text{store}(b)=(H(b),b)$; $\text{derive}=f\circ\text{raw}$ (regenerable);
$\text{add}(\text{derived\_from})$ with cycle-refused-at-insert; $\text{attest}$ = a signed step whose
chain terminates in authored leaves.

**Invariants.** raw immutable (A1); derived = $f(\text{raw})$ (regenerability); derivation acyclic
(I10/A3); every support-closure leaf authored; attestation chains complete to authored leaves.

**Code.** `core/stores/rawstore.py` (hash), vector/derived stores (functor), `core/stores/derived.py`
(`derived_from` + acyclicity), `core/recursion.py` (depth + decay), `core/attestation/` (signed DAG).

**Reframing note.** Mostly framed already. The two additions from companions III: the `derived_from`
column becomes the hyperedge **junction** (naming what it is), and the confidence **clamp** becomes
the single definition of $c$. The attestation chain is *a typed path in the derivation DAG* — worth
saying in a docstring so the two are understood as one structure, not two.

## A.3 Guarded transition systems

**Object.** Small finite automata $M=(S,\to)$ where each transition is **guarded**: a predicate is
checked *before* the side effect, and rejection is identity. Small enough to enumerate exhaustively.

**Instances.** The **two-slot loader** (guard $\sum_R m\le C\wedge|R|\le2$ before any model load,
I8); the **self-mod gate** ($s'=\Delta\!\cdot\!s$ iff $G_{\text{now}}(\Delta,s)$ else $s$, I12); the
**queue lifecycle** (PROPOSED→APPROVED→EXECUTED→VALIDATED/ROLLED_BACK, precondition-checked).

**Invariants.** ceiling never exceeded; $\Delta$ never self-applies; illegal transitions refused;
the FSMs are **FSM-verified** (state spaces enumerated in tests).

**Code.** `core/loader` (TwoSlotLoader), `ops/gate.py` + `ops/ledger.py` + `ops/apply.py`,
`scheduler/queue.py`.

**Reframing note.** Already framed and FSM-tested. Reframing = **docstring** only: name the states,
the guard, and the "rejection is identity" property at the top of each machine. **Do not** introduce
a generic automaton framework — that is ceremony; the tiny hand-written FSMs are correct.

## A.4 Metric geometry

**Object.** Distances measured against **frozen anchors**. The drift gauge is a one-sided
deterioration (pseudo)metric $D(t)=d(\mu(s_t),B)$ on a profile space (capability rates ⊕ Constitution
conformance), $B$ frozen; the **boiling-frog inequality** ($\forall t\,\delta_t\le\theta\not\Rightarrow
D(T)\le\theta$, since $D(T)\le\sum\delta_t$ diverges) is the *real theorem* that forces a frozen anchor.
The Dreamer adds **diffusion distance** and **min-cut-to-authored/conductance** (companions III) — the
same "distance against ground" idea, on the graph.

**Invariants.** healthy improvement = 0 drift (one-sided); Constitution breach hard-trips ($D=\infty$);
$\Theta$ is a frozen fixed point excluded from the lever set.

**Code.** `eval/drift.py` (Profile, Axis, deterioration, drift), `core/complex/` (diffusion, cut).

**Reframing note.** Already framed (A1/G4). The unification worth stating: **drift-against-frozen-anchor
and min-cut-against-authored are the same move** — measuring fidelity of a regenerable layer to a fixed
ground. That is *the alignment subsystem*, mathematically: alignment = a small distance from the
regenerable layer to the fixed seed. The A2 structural axes (frustration, conductance) are additional
coordinates of the same metric.

## A.5 The reasoning complex (the engine — companions III)

**Object.** A multilayer, typed, temporal knowledge complex $\mathfrak{K}$ (layers = provenance
strata; typed/signed edges; similarity flag complex $K_\sigma$ + derivation hypergraph $\mathcal{H}$;
temporal index) with a **generalized Laplacian family** ($\delta^{\!*}\delta$: ordinary/signed/sheaf/
hypergraph) as its central operator, plus curvature, persistence, and the SBM.

**This is the one family that is genuinely new code** — `core/complex/` and the Dreamer loop v2. It is
fully specified in `REASONING-COMPLEX-MATHEMATICS.md` and `REASONING-COMPLEX-BUILD.md`. Its connection
to the substrate: layer 1 of $\mathfrak{K}$ **is** the provenance labeling (family 1); its base **is**
the regenerable derivation (family 2); its temporal trajectories **feed** the metric geometry (family
4). The engine is built *out of* the substrate families — which is the whole thesis of this document.

## A.6 Composition & non-interference (what survives assembly)

The families do not interfere destructively when composed — and this is provable, per companion II:

- **Zone non-interference** (family 1 + import graph): $\mathsf{Core}\not\to^*\mathsf{Net}$ ⇒ no egress
  path *regardless of edge behavior* — composition cannot create one (I2, static).
- **Authority monotonicity** (family 1): no sequence of skill/role additions raises $\mathcal{A}$ above
  $\mathrm{scope}\cap\textsf{MAX}$ (I13) — the semilattice bound is closed under composition.
- **Provenance preservation** (families 1+2): $\rho$ is invariant under all derivation; the only
  mutator is human promotion — no pipeline stage launders observed into authored.

**Reframing note.** This is the payoff of naming the families: non-interference is a statement *about
the families*, and it already holds. State it once, structurally, rather than re-deriving per subsystem.

## A.7 Concordance (the map)

| Object | Family | Operation(s) | Invariant | Code | Tier |
|---|---|---|---|---|---|
| provenance $\rho$ / firewall $\pi_{\mathsf{MR}}$ | 1 | project, label | I6 | `core/mirror.py`, `core/provenance.py` | structural |
| unforgeable inference | 1,2 | add (codomain pinned) | I5 | `core/stores/derived.py` | structural |
| capability $\mathcal{A}$ | 1 | mint = meet; ⊕ non-widening | I13 | factory / dispatch | structural |
| de-id $\pi_{\text{public}}$ | 1 | erase | (Ph8) | `core/research/criteria.py` | structural |
| self-mod surface | 1 | resolve (no path field) | (Ph10) | `ops/levers.py` | structural |
| raw hash $H$ | 2 | store (write-once) | A1 | `core/stores/rawstore.py` | structural |
| derived $=f(\text{raw})$ | 2 | chunk, embed | regen | ingest / vector store | structural |
| derivation DAG + decay | 2 | add(derived_from), depth, $c$ clamp | I10 | `core/stores/derived.py`, `core/recursion.py` | structural + property |
| attestation chain | 2 | attest (signed path) | chain-to-leaves | `core/attestation/` | runtime + test |
| two-slot loader | 3 | load (guarded) | I8 | loader | FSM-verified |
| self-mod gate | 3 | $\Delta\!\cdot\!s$ iff $G_{\text{now}}$ | I12 | `ops/gate.py` | FSM-verified |
| queue lifecycle | 3 | transition (precond) | liveness/G6 | `scheduler/queue.py` | FSM + test |
| drift $D(t)$ / boiling-frog | 4 | deterioration vs frozen $B$ | G4 | `eval/drift.py` | property |
| grounding predicate | 2,4 | $\mathrm{Cit}(A)\subseteq\mathrm{Ret}$ | I9 | `core/selfcheck.py` | property |
| reasoning complex $\mathfrak{K}$ + $\delta^{\!*}\delta$ | 5 | build, cluster, curvature, balance, persist, SBM | (new) | `core/complex/`, `core/dreaming/` | property (new) |
| zone / authority / provenance non-interference | 6 | composition | I2/I13 | import-lint, factory | static/structural |

---

# Part B — The reframing direction

## B.1 The decision rule: make it a type, or make it a docstring

The one practical rule, applied to every candidate reframing:

```
Does turning this math into a TYPE delete an illegal state (make a wrong value unconstructable)?
   ├─ YES  → make it a type.   (the MirrorView / DerivedStore / ProposedChange move)
   └─ NO   → does naming the math clarify a TRUST BOUNDARY for a reader?
              ├─ YES → put it in a docstring / boundary comment (state object + invariant + tier).
              └─ NO  → leave it alone. Renaming for aesthetics is decoration; do not.
```

**Worked examples, grounded in the codebase:**

| Candidate | Decision | Why |
|---|---|---|
| the signed edge polarity $s\in\{+1,-1\}$ | **type** (an enum, not a free `int`) | a `sign` that can be $3$ is an illegal state; an enum deletes it |
| the reasoning complex built only from `MirrorView` | **type** (constructor takes `MirrorView`) | building from a raw store is the firewall violation; the signature deletes it |
| diffusion distance / heat kernel | **docstring** | it is a computation; naming the operator clarifies, a `Metric` protocol is ceremony |
| the two-slot loader as an FSM | **docstring** | already FSM-tested; name the states + guard; a generic automaton lib is ceremony |
| the boiling-frog inequality | **boundary comment** at `eval/drift.py` | explains *why* the anchor is frozen — a trust boundary; no type needed |
| provenance "order" | **delete** | the order is not load-bearing (G8) — do not reintroduce it as anything |

The rule's discipline is that **most reframing is docstrings, a little is types, and some candidates
are left alone.** If a session produces mostly renames, it went wrong.

## B.2 One shared notation (`docs/NOTATION.md`)

Create a single glossary that every whitepaper and every boundary docstring references: **symbol ↔
code name ↔ the object it denotes ↔ the family**. This gives "the whole codebase speaks one
mathematical language" *without renaming anything* — the code keeps its readable names; the glossary
is the join.

```
| symbol            | code                          | object (family)                     |
| ρ, π_MR           | Provenance, MirrorView        | provenance labeling / projection (1)|
| 𝒜, MAX            | handles, PRE_DECLARED_MAX     | capability semilattice (1)          |
| H, Σ              | rawstore.digest               | content-address hash (2)            |
| c, g, d, γ, λ     | recursion.*, adjudicator.*    | confidence/grounding/depth/decay (2)|
| D(t), B, Θ        | drift.*, baseline.json        | drift metric / frozen anchor (4)    |
| 𝔎, K_σ, ℋ, δ*δ   | complex.*                     | reasoning complex + Laplacian (5)   |
```

This is the highest-leverage single artifact of the whole reframing: it is small, breaks nothing, and
makes the mathematical account and the code mutually navigable.

## B.3 Per-layer refactor map

Module-cluster by module-cluster: the object, whether it is already framed, and the *disciplined*
action (type / docstring / leave).

| Cluster | Object (family) | Already framed? | Action |
|---|---|---|---|
| `core/stores/*` | hash + regenerable derived + hypergraph (2) | strongly | **docstring**: name $H$, "derived = $f$(raw)", the junction; one **type** move = `derived_from`→hyperedge junction (companions III) |
| `core/mirror.py`, `provenance.py` | labeling + projection (1) | exemplary | **docstring** only: state it is an *unordered* labeling; membership is the structure |
| `core/recursion.py`, `selfcheck.py` | decay + subset predicate (2) | yes | **type/impl**: adopt the $c$-clamp as the single definition; **docstring** the predicate |
| `core/attestation/*` | signed DAG / path (2) | yes | **docstring**: "an attestation chain is a signed path in the derivation DAG" |
| `ops/gate,levers,ledger,apply` | guarded transition system (3) | FSM-tested | **docstring**: states + $G_{\text{now}}$ + "rejection is identity"; **leave** the FSM code |
| `scheduler/queue.py` | priority order + monotone aging (3) | yes | **docstring**: the aging monotonicity + liveness; **leave** code |
| `eval/drift.py` | metric + frozen anchor (4) | yes | **boundary comment**: boiling-frog; the A2 axes as new coordinates |
| `core/research/criteria.py` | information-flow erasure (1) | structurally | **docstring**: name it $\pi_{\text{public}}$, connect to the firewall family |
| factory / scope | capability semilattice (1) | structurally | **docstring**: mint = meet, ⊕ non-widening |
| `core/complex/*`, `core/dreaming/*` | the reasoning complex (5) | **new** | **build** per companions III; this is the real new code |

The table's shape is the message: **one genuinely new code family (5), a couple of small type moves
(the junction, the clamp, the signed-edge enum), and the rest is naming/docstrings.**

## B.4 Docstring convention at trust boundaries

At every trust boundary and every family instance, a three-line header:

```python
# OBJECT:     <the math> — e.g. "π_MR : projection onto mirror-readable layers (family 1)"
# INVARIANT:  <what must hold> — e.g. "in(Ω) ⊆ π_MR(V); observed unreachable to introspection (I6)"
# ENFORCED:   <tier + where> — e.g. "structural: non-MR view is untypable (MirrorView.__post_init__)"
```

This is the companion II assurance hierarchy (structural > static > runtime > property > assumption)
made local: every boundary states its object, its invariant, and *how strongly* it is enforced. A
reader learns the math and the guarantee at the point of use, and a reviewer can see immediately when
notation is outrunning enforcement (INVARIANT stated, ENFORCED weak → a gap to record honestly, as
G9–G11 already do).

## B.5 Documentation restructure

Reorganize the whitepapers around the objects, sharing one notation:

- **Companion I** (`WHITEPAPER.md`) — philosophy & the DNA. *(unchanged; the poetry)*
- **Companion II** (`WHITEPAPER-FORMAL-PROPERTIES.md`) — the verification plan (invariants, tiers,
  discharge). *Reframe lightly:* group the invariant catalog by the **five families** (A.1–A.5), so
  the catalog reads as "the objects and their guarantees," not a flat list.
- **Companion III** (`REASONING-COMPLEX-{MATHEMATICS,BUILD}.md`) — the reasoning complex (the engine).
- **Companion IV** (this document) — the unified structural account + reframing direction.
- **`docs/NOTATION.md`** (new) — the shared glossary (B.2), referenced by all four and by boundary
  docstrings.

Design notes stay as-is but gain a one-line **family tag** at the top (e.g. *alignment-subsystem →
family 4 (metric geometry): fidelity of the regenerable layer to the frozen seed*), so each note is
locatable in the account. **Do not** rewrite the design notes; tag them.

## B.6 Phased, non-breaking plan + guardrails

Order, each step independently shippable and behavior-preserving (except family 5, which is new code
behind the flag):

1. **`docs/NOTATION.md`** (B.2) — the glossary. *(pure documentation; highest leverage, zero risk)*
2. **Companion IV + tag design notes** (this doc, B.5) — the account. *(documentation)*
3. **Boundary docstrings** (B.4) across families 1–4 — object/invariant/tier headers. *(documentation;
   surfaces any notation-outruns-enforcement gaps honestly)*
4. **The small type moves** — `derived_from`→hyperedge junction, the $c$-clamp as the single
   definition, the signed-edge enum. *(each a reviewed, tested, behavior-preserving diff)*
5. **Regroup companion II by family** — the verification plan as objects. *(documentation)*
6. **Family 5** — build `core/complex/` and the Dreamer loop v2 per companions III (Track H),
   flag-OFF, behind the adapter. *(the real new code)*

**Guardrails, restated (the discipline is the deliverable):**

- Reframe to a **type** only when it deletes an illegal state; otherwise a **docstring**; otherwise
  **leave it**. No aesthetic renames.
- **Notation never outruns enforcement.** If a boundary docstring states an INVARIANT the code does not
  ENFORCE, record it as an honest gap (the G9–G11 pattern), do not pretend the type exists.
- **Behavior-preserving.** Every step except family 5 changes names/docs/small structural types, never
  runtime behavior. The 480-test suite is the ratchet: green before and after each step.
- **The flag stays OFF.** The Dreamer's new math ships behind the adapter and the dream R&D flag until
  a deliberate session flips it.

---

## Appendix — family × subsystem matrix, and the reframe ledger

**Which family each subsystem instantiates** (a subsystem may span families):

| Subsystem | 1 label/flow | 2 derivation | 3 automata | 4 metric | 5 complex |
|---|:---:|:---:|:---:|:---:|:---:|
| ingest / raw store | | ● | | | |
| provenance / firewall | ● | | | | |
| librarian (grounding) | | ● | | ● | |
| curator | ● | ● | | | ● |
| dreamer / interpreters | ● | ● | | ● | ● |
| two-slot loader | | | ● | | |
| scheduler / queue | | | ● | | |
| agent factory / scope | ● | | | | |
| self-mod gate | ● | | ● | ● | |
| drift gauge / alignment | | | | ● | ● |
| airlock / research | ● | | | | |
| attestation | | ● | | | |

**Reframe ledger (the disposition of each candidate):**

| Candidate | Disposition |
|---|---|
| `docs/NOTATION.md` glossary | **do (1st)** — highest leverage, zero risk |
| boundary docstrings (object/invariant/tier) | **do** — documentation, surfaces gaps |
| `derived_from` → hyperedge junction | **do (type)** — companions III |
| $c$-clamp as single definition of confidence | **do (type/impl)** — closes the whitepaper's own tension |
| signed-edge polarity enum | **do (type)** — deletes the illegal `sign` |
| regroup companion II by family | **do** — documentation |
| generic automaton / metric / lattice frameworks | **do not** — ceremony; the hand-written versions are correct |
| aesthetic renames (Cluster→Simplex, etc.) | **do not** — decoration |
| reintroduce a provenance order / rich sheaf / manifold | **do not** — notation outrunning enforcement (G8) |

*Companion IV. The reframing is unification and propagation, not a rewrite: one new code family, a few
type moves that delete illegal states, and a shared vocabulary that makes the account and the code
mutually navigable — under the discipline that mathematics enters the code only where it constrains,
never where it decorates.*
