# Distillation — the two-limit free-energy distance

**Load-bearing result (what our corpus relies on).** Kivimäki, Shimbo & Saerens (2013)
develop the **free-energy distance**, a refinement of the randomized-shortest-path (RSP)
dissimilarity of Saerens et al. (2009), and analyze its behavior as the inverse-temperature
parameter is swept across its full range. They show the free-energy distance has two clean
limiting cases: as the parameter tends to one extreme it **recovers the shortest-path
distance**, and as it tends to the other extreme it **recovers a resistance-distance /
commute-time-like (diffusion) distance**. The paper compares this family against a range of
other graph node distances, situating shortest-path and resistance/diffusion distance as
the two endpoints of the same one-parameter family.

**Where we use it.** In `dn-core-query-protocol` §2.2, this is the second of the two citations
(alongside Saerens et al. 2009) grounding the claim that mode 1a (hard shortest-path,
`β→∞`) and mode 1b (soft diffusion/resistance, `β→0`) are the **two endpoints of a single
free-energy family `K(β)`**, not independent constructions — the `[ESTABLISHED: RSP/
free-energy distances]` tag in §2.2's unification bullet.

**Verification.** Confirmed against the primary source 2026-07-13 (Kivimäki, Shimbo &
Saerens, *Physica A* 393, 600–616, 2013; doi 10.1016/j.physa.2013.09.016). Verdict
CONFIRMED — the paper does establish exactly this two-limit behavior of the free-energy
distance, as cited.
