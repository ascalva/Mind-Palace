# Distillation — the Schur (Hadamard) product theorem

**Load-bearing result (what our corpus relies on).** Schur (1911) proves that if `A` and `B`
are both positive-semidefinite (PSD) matrices, then their **entrywise (Hadamard) product**
`A ⊙ B` is also positive-semidefinite. Equivalently: the PSD cone is closed under the
Hadamard product, not just under addition and nonnegative scaling. This is the classical
Schur product theorem.

**Where we use it.** In `dn-core-query-protocol` §2.2, this grounds the claim that **hybrid
retrieval is an operation in the PSD-kernel cone**: given the structural kernel `K_struct`
(mode 1b, e.g. the graph heat kernel) and the semantic kernel `K_sem` (mode 2, the embedding
Gram matrix), both PSD, the Hadamard product `K_struct ⊙ K_sem` — "cited **and**
semantically near" — is *itself* a valid PSD kernel, i.e. hybrid retrieval stays inside the
same cone rather than requiring an ad-hoc combination rule. `[ESTABLISHED: Schur product.]`
per §2.2's unification bullet.

**Verification.** Confirmed against the primary source 2026-07-13 (Schur, *J. reine angew.
Math.* 140, 1–28, 1911; doi 10.1515/crll.1911.140.1). Verdict CONFIRMED — the paper does
establish the Hadamard-product-preserves-PSD result, as cited.
