# Distillation — the p-resistance family and its phase transition (PARTIAL — corrected)

**Load-bearing result (what our corpus relies on).** Alamgir & von Luxburg (2011) define the
**p-resistance**, a family of graph distances generalizing the standard (electrical)
resistance distance by an exponent parameter `p` on edge conductances/flows in an
optimization-based (p-norm flow) formulation. They characterize a **phase transition** in the
family's behavior as `p` varies: at `p = 2` the p-resistance **coincides with the standard
resistance distance**; as `p` is taken to its other extreme, the family's behavior
**transitions away from resistance-like behavior toward a distance governed by graph cuts /
connectivity** (the shortest-path regime sits at the opposite, low-`p` end of the spectrum).
The paper's central point is precisely this phase transition — the family does **not** stay
"resistance-like" across its whole range.

**The correction this card records (dn-core-query-protocol §1.3 item 6, item (b)).** The
original attribution in the corpus described the p-resistance span as shortest-path (p=1) →
resistance (p=2) → **resistance** at the high-`p` end. On verification this is **wrong at the
high-`p` end**: the paper's own phase-transition result is that the high-`p` limit is
**cut/connectivity**, not resistance. The correct span is:

- **p = 1** — shortest-path,
- **p = 2** — (standard electrical) resistance,
- **p → ∞** — **cut / connectivity** (NOT resistance).

Only the low-`p` and middle (`p=2`) points reduce to shortest-path and resistance
respectively; the high-`p` end is a qualitatively different regime governed by graph cuts and
connectivity, which is exactly the paper's phase-transition finding. Any distillation or
citation asserting "resistance" at the high-`p` end mischaracterizes the source.

**Where we use it.** In `dn-core-query-protocol` §2.2, this reference grounds the description
of the p-resistance family as one of the concrete parametrized families instantiating the
mode 1a/1b deformation picture — but with its own internal endpoint at cut/connectivity, not
a second resistance regime. `[ESTABLISHED: p-resistances]` per §1.3 item 6 / §2.2's
unification bullet, **with the correction above applied**.

**Verification.** Confirmed (PARTIAL) against the primary source 2026-07-13 (Alamgir & von
Luxburg, *NIPS* 24, 2011). Verdict PARTIAL — the family and the p=1/p=2 endpoints are
confirmed as cited, but the original high-`p` attribution ("resistance") is incorrect; the
paper's own phase-transition result places **cut/connectivity**, not resistance, at that end.
This correction is owed to the successor note / book chapter per §1.3 item 6(b); it has not
yet been applied inline to `dn-core-query-protocol` §2.2 itself.
