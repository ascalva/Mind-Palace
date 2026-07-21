# Brainstorm — the fiber-chain grammar: a language of admissible chains, and how to build it

> Captured by the orchestrator from owner chat (2026-07-21 ~05:28Z, session-39, while the
> bp-080/bp-081 builders run). A continuation of the chain-composition / fiber-signature thread
> (`clock-curvature.md`, 2026-07-20T02:45Z capsule — composed chain / fiber chain / fiber
> signature; "restriction is a LANGUAGE not a subset"). Owner's seed, near-verbatim: *"given the
> fiber alphabet and a well-defined language of correct words, can you rule out certain paths? if
> the word is not a member of the language set, then it is rejected — prune the chains until all
> chains from a given node are valid members of the language set. how do you construct such a
> language?"*

## 2026-07-21T05:28Z (session-39)

### The seed, in two halves

1. **Use** — a language `L ⊆ Σ_fib*` over the fiber alphabet (`Σ_fib = {F, D, C, …}` —
   similarity, derivation/supersession, causal witness) is a membership test on chains: a chain
   is admissible iff its **fiber signature** ∈ L. Non-members are rejected; prune from a node
   until every surviving chain spells a valid word.
2. **Construct** — the hard question: where does L come from?

### Orchestrator chew — the pruning mechanism (offered, not decided)

- **This is exactly a regular-path query if L is regular.** The efficient pruning is NOT
  "enumerate all chains, then filter" (exponential) — it is the **product-automaton walk**: run
  the graph traversal and an automaton for L in lockstep; at each node the automaton's current
  state says which fiber-edges may extend the prefix. `[FROM MEMORY — external-grounding: regular
  path queries / automaton-graph product; Mendelzon–Wood]`
- **The load-bearing object is the *viable-prefix* test, not membership.** You prune the instant a
  prefix enters a **dead state** — a state from which no accepting state is reachable — because
  that prefix can never complete to a valid word. Membership answers "is this finished chain
  valid"; viability answers "can this partial chain still become valid," and that is what lets you
  cut a branch at the frontier. Ties directly to the **laziness laws** (dreamer note §2.4, and the
  just-built bp-079 materialization boundary): never materialize the chain set; the automaton
  state is the compact certificate that prunes lazily.
- **Order matters — which is why a LANGUAGE, not a set, is forced.** The `[d, τ]` diamond proved
  walking-derivation and shifting-time do not commute (`dn-magnetic-laplacian` §2.3; TA-c refuted).
  A word is ordered; a set is not. So the language formulation is the *correct* generalization of
  "which edges may you walk" — the commutative subset (today's `E ⊆ {F, D}`,
  `capability-scope-algebra.md:65`) is the order-blind shadow of it.
- **Two layers that must not be confused: membership (hard) vs ranking (soft).** The language is a
  BOOLEAN admissibility filter (prune the nonsensical). Among the survivors, *which chain is best*
  is the conductance/curvature question (`clock-curvature.md` — hop-vs-distance, the phase model).
  They compose cleanly: **prune to L, then rank the survivors by conductance.** The owner's
  question is the membership layer; the earlier metric discussion was the ranking layer.
- **The same object wears two hats — capability vs epistemics.** As a *capability* (the scope
  algebra's E generalized from set → automaton), L constrains which chains a dreamer/query is
  ALLOWED to walk. As an *epistemic filter*, L encodes which chains are MEANINGFUL — a chain
  whose signature ∉ L is an unsound inference, not just a forbidden one. The owner's phrasing
  ("rule out," "rejected," "valid members") is epistemic; it doubles as authorization. This is
  the same meaning=capability duality the inner/outer-core and dreamer work kept surfacing.
- **The deepest framing: L is a grammar of sound reasoning over the heterogeneous graph.** A
  valid word IS a well-formed inference path. Constructing L = writing down what counts as sound
  cross-fiber reasoning. That is why "how do you construct it" is the real question — it is the
  palace formalizing its own inference discipline.

### The construction question — four routes, escalating in principle

1. **Axiomatic / hand-authored (top-down, by fiat from semantics).** Declare the grammar from what
   makes a chain meaningful. The worked example already exists in ratified text: the grounding law
   (`recursive-dreaming-bounded-by-grounding`, sharpened in the dreamer note §2.7-4) — *grounding
   terminates in authored evidence or declared hypothesis, never in prior interpretation* — is
   literally a regular constraint on chains: `F* · (C | D)` (any run of similarity hops, then
   terminate in exactly one witnessed causal/derivation edge; never end on an interpretation
   edge). Other axioms: a lineage query = `D+` (pure supersession); "no two consecutive C without
   an intervening D." This is the E-coordinate as an authored automaton — a **CS-x extension**,
   and per the capability-scope discipline it needs a concrete consumer (it now has one: the
   dreamer's chain traversal in bp-080's census walks and bp-082's influence chains).
2. **Type-theoretic (the fibers carry their own composition rules).** Some compositions are
   ill-typed by the fibers' own semantics (deriving-from a similarity may be nonsense; a causal
   edge's endpoints constrain the next step). Then L is the set of type-correct words — constructed
   like a typing judgment, or a category where fibers are morphisms and only some compositions are
   defined. The `[d, τ]` non-commutativity is evidence the fibers form a non-commutative structure;
   L falls OUT of that structure rather than being imposed. The most principled route — the grammar
   is discovered, not decreed.
3. **Learned / empirical (bottom-up, from endorsed chains).** Induce L from the chains the
   owner/dreamer actually endorse (the endorsed-chain corpus the dreamer's forecast-scoring and the
   census produce) via grammatical inference `[FROM MEMORY — Angluin L*, RPNI]`: the minimal
   automaton consistent with the positive/negative examples. Falsifiable and self-refining as
   endorsements accumulate — but carries the **apophenia risk** (a learned grammar can manufacture
   structure), so it needs the held-out validation arm from the forecaster capsule
   (`synchronic-diachronic-dreamer.md`, 2026-07-21 forecaster addendum).
4. **Hybrid (the likely answer).** Type-correctness (route 2) as the provable HARD core — "can
   this word exist at all"; the domain grammar (route 1, owner-authored) layered on; soft
   preferences refined empirically (route 3) — "which valid words *conduct best*" (route 3 feeds
   the ranking layer, closing back to clock-curvature). Hard constraints prune; soft preferences
   rank.

### Honest frictions / falsifiers

- **Keep L regular or the lazy pruning breaks.** If a genuine validity rule needs counting
  ("equal F and D," a balanced structure — context-free) the product-automaton frontier-pruning
  fails and you need a pushdown parser (costlier, harder to prune lazily). *Falsifier:* a real
  soundness rule proven non-regular ⇒ the cheap-lazy-pruning claim dies; either approximate it
  with a regular over-language or accept the parser cost.
- **Calibration is two-sided.** Too restrictive ⇒ prunes real inferences (false negatives); too
  permissive ⇒ admits nonsense (false positives). Only measurable against endorsed chains — so
  this is measure-first, like everything on the clock-curvature track.
- **Learned L must not smuggle apophenia** — held-out validation, never fit-and-ship.

```capsule
topic: fiber-chain-grammar
date: 2026-07-21

decisions:
  - The seed itself (owner): a language L over the fiber alphabet as a membership/viability filter
    that prunes chains to admissible fiber signatures; plus the construction question. Seed only —
    no design decisions taken here.
  - Working frame the chew proposes (ratifies by use, like the composed-chain vocabulary):
    MEMBERSHIP (hard, L, prunes) is a distinct layer from RANKING (soft, conductance, orders the
    survivors); they compose — prune to L, then rank. L generalizes the scope algebra's
    E-coordinate from a SET to a LANGUAGE (an automaton), forced by [d,τ] non-commutativity.

parked:
  - decision: the language class (regular vs context-free vs learned/typed)
    default: REGULAR — the product-automaton frontier-prune stays lazy (ties to the materialization
      boundary); richer classes only if a real rule provably needs them
    re_entry: a genuine soundness rule proven non-regular appears
  - decision: whether E in capability-scope-algebra generalizes set → language
    default: it does NOT yet (E ⊆ {F,D}, capability-scope-algebra.md:65 unchanged); this is a CS-x
      extension, and per the algebra's discipline it lands only on a concrete consumer
    re_entry: a dreamer/query traversal (bp-080 census walks, bp-082 influence chains) concretely
      needs language-constrained walking, not set-constrained

open_questions:
  - Which construction route is right — axiomatic grammar, fiber type-theory (compositions
    well-typed by the fibers' own semantics), learned-from-endorsed-chains, or the hybrid? The
    grounding law F*·(C|D) is the first concrete authored production — is the rest discoverable
    from the fiber composition algebra, or must it be authored?
  - Is the viable-prefix (dead-state) prune the right seam to fold into the materialization
    boundary / CN-7 refusal posture (prune-at-frontier = refuse-before-materialize)?
  - Membership vs ranking boundary: exactly which constraints are hard (soundness — belong in L)
    vs soft (preference — belong in conductance)? The grounding law is clearly hard; hop-count is
    clearly soft; where is the line?

next_steps:
  - A design pass (fable) candidate AFTER the dreamer builds land (bp-080/082 give the concrete
    consumer + the endorsed-chain data route 3 needs). Grounds on: the fiber composition semantics
    (route 2), the ratified grounding law as the seed production (route 1), and the scope algebra's
    E-coordinate.
  - MEASURE FIRST (the clock-curvature discipline): which fiber signatures actually appear in
    endorsed chains (bp-080's census enumerates C/D-signature structures) before authoring or
    learning L — calibration needs the data.
  - External-grounding sweep gains: regular path queries (Mendelzon–Wood), automaton learning
    (Angluin L*, RPNI) — [FROM MEMORY] until verified.

references:
  - docs/brainstorms/clock-curvature.md                        # fiber signature born here (02:45Z); the RANKING layer (conductance)
  - docs/design-notes/synchronic-diachronic-dreamer.md         # composed/fiber chains; §2.4 laziness (the lazy prune); §2.7-4 grounding law = the seed production; the forecaster held-out arm
  - docs/design-notes/capability-scope-algebra.md              # E ⊆ {F,D} (:65) — the set this generalizes to a language (CS-x)
  - docs/design-notes/magnetic-laplacian.md                    # [d,τ] non-commutativity — why a LANGUAGE not a set
  - docs/design-notes/recursive-dreaming-bounded-by-grounding.md  # the grounding law F*·(C|D)
  - docs/design-notes/connectivity-instruments.md              # CN-7 refusal posture ~ frontier prune
  - docs/build-plans/bp-080/plan.md · docs/build-plans/bp-082/plan.md  # the census/influence chain-walkers = the concrete consumer
```
