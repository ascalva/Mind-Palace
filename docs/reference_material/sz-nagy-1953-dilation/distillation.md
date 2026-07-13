# Distillation — unitary dilation of Hilbert-space contractions

**Load-bearing result (what our corpus relies on).** Sz.-Nagy (1953) proves that every
**contraction** `T` (an operator with operator norm ≤ 1) on a Hilbert space `H` can be
**dilated**: there exists a larger Hilbert space `K ⊇ H` and a **unitary** operator `U` on
`K` such that `T^n = P_H U^n |_H` for all `n ≥ 0` (`P_H` the orthogonal projection onto `H`).
Informally, every contraction is the "shadow" (compression) of a unitary — a
norm-non-increasing, information-losing operator can always be understood as the restriction
of a norm-preserving, information-preserving one acting on a bigger space.

**Where we use it.** In `dn-core-query-protocol` §2.5, this grounds the claim that **the
transport is not unitary; the ledger is its dilation**: because revision destroys, creates,
and merges content, the active-view supersession transport is a genuine contraction (it can
only lose structure, never gain it), while the **append-only ledger** — where nothing is
ever destroyed — is exactly the larger space carrying the **isometric (unitary) dilation** of
that contraction, per the Sz.-Nagy construction. This is the precise sense in which "revision
destroys structure in the active view; the ledger is the space in which nothing was ever
destroyed." `[DERIVED, contingent on supersession-lifecycle §4.5 — Parked.]`

**Verification.** Confirmed against the primary source 2026-07-13 (Sz.-Nagy, *Acta Sci.
Math.* 15, 87–92, 1953). Verdict CONFIRMED — the paper does establish the unitary-dilation
theorem for Hilbert-space contractions, as cited.
