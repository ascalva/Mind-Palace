# Distillation — forest metrics generalizing shortest-path and resistance distances

**Load-bearing result (what our corpus relies on).** Chebotarev (2011) constructs a
one-parameter family of graph distances built from **weighted spanning-forest counts**
(rooted forests of the graph, generalizing the spanning-tree counts underlying the
matrix-forest theorem of Chebotarev & Shamis, 1997). As the family's parameter varies, the
resulting distance interpolates between the **shortest-path distance** at one extreme and
the **resistance distance** at the other, with both being members of a single
"graph-geodetic" family characterized combinatorially via forests. The paper is explicit
that this generalizes and unifies the two previously-separate distance notions.

**Where we use it.** In `dn-core-query-protocol` §2.2, this grounds the **resistance/
forest-metric locus of mode 1b** — the claim that mode 1b's soft-diffusion/resistance
distance sits inside a combinatorially well-characterized (forest-counting) family, which is
part of the evidentiary basis (together with Saerens 2009 / Kivimäki 2013) for treating
1a and 1b as the two ends of one deformation rather than unrelated constructions.
`[ESTABLISHED: Chebotarev]` per §2.2's unification bullet.

**Verification.** Confirmed against the primary source 2026-07-13 (Chebotarev, *Discrete
Applied Mathematics* 159(5), 295–302, 2011; arXiv:0810.2717; doi 10.1016/j.dam.2010.11.017).
Verdict CONFIRMED — the paper does construct exactly this forest-metric family spanning
shortest-path and resistance distance, as cited.
