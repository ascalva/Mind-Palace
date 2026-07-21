# Brainstorm — clock curvature: high-change regions distort the graph's space

> Captured by the orchestrator from owner chat (2026-07-21 ~01:00Z, session-39, fable — the
> night's last seed). Owner, near-verbatim: *"high clock rate (high change) regions distort
> space, which has a few consequences: (1) the geodesic distance might be shorter between two
> points in the cluster/hub, but the number of hops is likely to increase when going through that
> region, which lowers conductivity (more hops); (2) the path of highest conductivity is a
> trade-off, an optimization problem — reduce hops (sometimes route around the hub, not through)
> and reduce distance; you then have to take a path close to the hub to minimize distance to the
> next hop, but not too close, or find paths that are around and not in the hub, which could lead
> to longer chains of edges; (3) if you choose to go around the hub, then you help build more
> conducive regions — you expand the cluster, the space of conductivity."*

## 2026-07-21T01:00Z (session-39)

### The seed, unpacked

Three claims, escalating in depth:

1. **Activity curves the metric.** A high-clock-rate region (dense churn: many versions, many
   fine-grained nodes and edges) pulls its points semantically close (short geodesics) while
   fragmenting traversal into many short hops. If conductivity attenuates per hop, dense regions
   are simultaneously *near* and *resistive* — mass curving space.
2. **Best-conductivity routing is a variational problem.** Through-the-hub minimizes distance but
   pays hop attenuation; around-the-hub saves hops but must graze the hub closely enough to keep
   inter-hop distances short — with "too close" and "too far" both losing. This is Fermat's
   principle: the hub is a high-refractive-index medium and the optimal chain bends around it,
   grazing.
3. **Traversal is plastic — routing builds the medium.** Choosing the around-path mints/reinforces
   structure in the periphery, expanding the conductive region. Geometry shapes flow; flow
   reshapes geometry (the Einstein-equation shape, or desire paths). Consequence, if true:
   **hubs are self-limiting** — as a hub densifies, its hop cost rises, traffic routes around,
   and the periphery grows. The graph anneals toward distributed conductivity instead of runaway
   concentration.

### Orchestrator chew (chat-side scrutiny — connections and honest frictions, not decisions)

- **⚑ The built σ\* does NOT price hops — this seed proposes a different functional.** Verified in
  code: `core/graph/sigma_star.py` is maximin/bottleneck semantics (grid-snapped bottleneck cosine
  on the MST path); a widest path through fifty short strong edges scores the same as one edge at
  the same bottleneck. Claim (1) says that path should attenuate. So the seed is either (a) a
  REFINEMENT of the conductivity functional (e.g. multiplicative per-edge attenuation ⇒ max-product
  path = shortest path under −log conductance, which automatically prices hops), or (b) a second,
  complementary reading beside σ\*. Which one is an empirical question first: on the real corpus,
  do bottleneck-optimal and product-optimal chains actually diverge, and where? (The σ-sweep,
  oq-0024, is the grounding run — again.)
- **The conformal-metric formalization is nearly free.** Write the effective cost as a conformal
  rescale ds_eff = n(x)·ds, where the "refractive index" n is the local hop density per unit
  semantic distance. Claim (1)'s modeling premise, made falsifiable: *high-clock-rate regions mint
  fine-grained, short edges* — i.e. n correlates with the local clock rate. Checkable today with
  the velocity instruments + edge-length distributions conditioned on local churn.
- **This is the curvature customer the parks have been waiting for.** `dn-edge-dynamics` parked
  PD-c (Ollivier–Ricci, "the principled form") behind a customer appearing; `dn-magnetic-laplacian`
  parked ML-d likewise ("a curvature customer appears") and drew the flux≠Ricci ledger — this seed
  is METRIC curvature (the Ricci side), not gauge curvature, so it re-enters PD-c/ML-d, not ML-a.
  And **Forman curvature is already built as the instrument** (dn-edge-dynamics PD-c row), so the
  "distortion" of claim (1) may be measurable now: does high local clock rate correlate with
  Forman curvature sign/magnitude? Note the sign question is genuinely open — a dense clique curves
  positive, a star-like hub curves negative — and the two have OPPOSITE routing consequences; the
  corpus should answer, not intuition.
- **Claim (3) is the deepest and currently has NO mechanism.** Nothing today mints edges from
  traversal: chains are read, not written. The honest wiring candidates, in escalating strength:
  (i) dreamer exhaust — a dispatched dreamer narrating an around-the-hub chain files claims whose
  ratified admission mints the peripheral edges (the taxonomy's interpreted-only/owner-gated path —
  slow, sacred-boundary-safe); (ii) traversal telemetry as a sensor stratum (routes-taken as
  observations, no authority); (iii) Hebbian edge reinforcement (automatic) — almost certainly a
  bright-line violation as stated (self-modification ungated) and noted only to be rejected. The
  plasticity loop should enter design as (i)+(ii); (iii) is named to be refused.
- **The dreamer tie-in is direct:** the just-drafted dn-synchronic-diachronic-dreamer makes chains
  the dreamer's medium (laziness law: σ\*/MST as the compact certificate) and its exhaust the only
  structure-minting path. "Routing around the hub expands the space of conductivity" is then a
  DREAM-DRIVEN annealing dynamic: the conditioning law + admission gates already bound it safely.

```capsule
topic: clock-curvature
date: 2026-07-21

decisions:
  - The seed itself (owner): high clock-rate regions distort the graph's metric (near yet
    resistive); highest-conductivity routing is a hop-vs-distance variational trade-off that can
    prefer grazing around hubs; and around-routing EXPANDS the conductive space (plasticity).
    Seed only — no design decisions taken in this capture.

parked:
  - decision: whether hop-pricing REFINES sigma_star's functional or stands beside it
    default: beside it (the built bottleneck sigma_star is ratified machinery; no silent change)
    re_entry: the sigma-sweep (oq-0024) shows bottleneck-optimal vs product-optimal chains
      diverging materially on the real corpus
  - decision: any automatic (Hebbian) edge reinforcement from traversal
    default: REFUSED — structure enters only via dreamer exhaust through the ratified admission
      gates or owner authorship (bright line 5; self-modification is gated)
    re_entry: none foreseen; recorded to be refused deliberately

open_questions:
  - The modeling premise, falsifiable: do high-clock-rate regions actually mint short, fine-grained
    edges (n ∝ local clock rate)? Measure edge-length distribution vs local churn (velocity
    instruments).
  - Curvature sign of high-churn regions on OUR graph: dense-clique-positive or hub-negative
    (Forman curvature is built — run it conditioned on clock rate); the two invert the routing
    story.
  - The functional: multiplicative per-hop attenuation (max-product = min Σ −log conductance) vs
    bottleneck σ*; do the optimal chains diverge on the corpus, and which better predicts the
    chains the owner/dreamer actually endorses?
  - Does the plasticity loop close safely through dreamer exhaust alone (admission-gated), and is
    the self-limiting-hub / annealing consequence observable longitudinally once it does?
  - Continuum limit: is the conformal-rescale picture (ds_eff = n(x)·ds) the right bridge to the
    edge-dynamics vector-field/continuum brainstorms?

next_steps:
  - Ride the edge-dynamics/curvature track: this is the CUSTOMER whose absence parked PD-c
    (Ollivier principled form) and ML-d — their re-entry conditions begin to fire when this
    graduates.
  - MEASURE FIRST (ground-before-building): oq-0024 sigma-sweep + a Forman-vs-clock-rate read +
    the edge-length-vs-churn distribution — all with built instruments — before any design pass
    formalizes the functional.
  - Design pass (fable) after the measurements: likely amends/extends dn-edge-dynamics territory;
    does NOT touch sigma_star machinery without its own plan.

references:
  - docs/design-notes/edge-dynamics.md                        # PD-c park (Ollivier); Forman BUILT; §5 vocabulary
  - docs/design-notes/magnetic-laplacian.md                   # ML-d park ("a curvature customer appears"); flux ≠ Ricci ledger
  - docs/design-notes/connectivity-instruments.md             # sigma machinery; the sweep this grounds on (oq-0024)
  - docs/design-notes/temporal-geometry-and-drives.md         # clock-rate geometry precedent
  - docs/design-notes/velocity-instruments.md                 # local churn measurement
  - docs/design-notes/synchronic-diachronic-dreamer.md        # chains as the dreamer's medium; exhaust = the only minting path
  - docs/brainstorms/edge-dynamics-and-continuum.md           # continuum-limit sibling
  - docs/brainstorms/conductivity-and-reasoning-chains.md     # per-hop attenuation intuition's origin
  - docs/brainstorms/temporal-clocks-and-strata.md            # clock rates per region
  - core/graph/sigma_star.py                                  # VERIFIED: bottleneck semantics, no hop pricing (the divergence)
```
