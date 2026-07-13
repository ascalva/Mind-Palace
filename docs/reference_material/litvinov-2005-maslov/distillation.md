# Distillation — Maslov dequantization and idempotent/tropical semirings

**Load-bearing result (what our corpus relies on).** Litvinov (2005) surveys **Maslov
dequantization**: a one-parameter family of semiring structures on the reals (or a suitable
domain), typically indexed by a "Planck-constant"-like parameter `h`, that at generic `h`
gives ordinary arithmetic (or a deformed log-exp arithmetic `x ⊕_h y = h·log(e^{x/h} +
e^{y/h})`, `x ⊗_h y = x + y`) and, in the **limit `h → 0`**, degenerates into the
**idempotent (min/max, +) tropical semiring**: `x ⊕_0 y = min(x,y)` (or `max`), `x ⊗_0 y =
x + y`. This is the precise sense in which tropical/idempotent arithmetic is a *limit* — a
"dequantization" — of ordinary semiring arithmetic, not an unrelated structure.

**Where we use it.** In `dn-core-query-protocol` §2.2, this grounds the claim that the
**tropical endpoint (mode 1a, hard shortest-path)** is the **Maslov dequantization of the
path semiring** underlying the soft-diffusion endpoint (mode 1b) — i.e., that the `β → ∞`
limit of the free-energy family `K(β)` is exactly the log-exp-to-min/max degeneration Litvinov
describes, so mode 1a is "the *same* Kleene closure as 1b, at the degenerate boundary" rather
than a structurally different computation. `[ESTABLISHED: RSP/free-energy distances;
Chebotarev; p-resistances. DERIVED: the O(1/β) bound.]` per §2.2's unification bullet.

**Verification.** Confirmed against the primary source 2026-07-13 (Litvinov, arXiv:math/
0507014, 2005). Verdict CONFIRMED — the survey does establish exactly this log-exp → min/max
dequantization limit, as cited.
