# Distillation — randomized shortest-paths as a family interpolating shortest-path and diffusion

**Load-bearing result (what our corpus relies on).** Saerens, Achbany, Fouss & Yen (2009)
define the **randomized shortest-path (RSP)** framework: a probability distribution over
paths between two nodes that minimizes expected path cost subject to a relative-entropy
(Kullback-Leibler) constraint against the natural random-walk distribution, controlled by
an inverse-temperature parameter. As that parameter is varied, the induced distribution over
paths — and the associated distance — sweeps continuously between two limiting regimes: the
**deterministic shortest path** at one extreme and the **random-walk / diffusion-based**
behavior at the other. The paper frames this as one **family**, not two unrelated
constructions, with the shortest-path and the diffusion/commute-time-like distances as its
two limiting members.

**Where we use it.** In `dn-core-query-protocol` §2.2, this is the primary citation grounding
the claim that a single free-energy / randomized-shortest-path family `K(β)` (parameterized
by an inverse temperature `β` on edge costs) has **mode 1a (β→∞, hard/tropical
shortest-path) and mode 1b (β→0, soft diffusion) as its two endpoints** — i.e., that the
"structural" retrieval mode's bifurcation into hard-reachability and soft-diffusion sub-modes
is not two separate objects but one deformation family. This is the `[ESTABLISHED: RSP/
free-energy distances]` tag in §2.2's unification bullet.

**Verification.** Confirmed against the primary source 2026-07-13 (Saerens, Achbany, Fouss &
Yen, *Neural Computation* 21(8), 2363–2404, 2009; doi 10.1162/neco.2009.11-07-643). Verdict
CONFIRMED — the paper does define exactly this two-endpoint interpolating family via the RSP
framework, as cited.
