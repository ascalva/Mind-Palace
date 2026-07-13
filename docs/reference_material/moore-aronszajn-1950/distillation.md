# Distillation — the reproducing-kernel / feature-map correspondence

**Load-bearing result (what our corpus relies on).** Every symmetric positive-semidefinite (PSD)
kernel `K` corresponds to a *unique* reproducing-kernel Hilbert space (RKHS) in which `K(x, y)` is
the inner product `⟨φ(x), φ(y)⟩` of a feature map `φ`. Equivalently: **a PSD kernel is always a Gram
(inner-product) matrix of some embedding into a Hilbert space.** This is the Moore–Aronszajn
theorem (Aronszajn 1950, crediting E. H. Moore's earlier "positive Hermitian matrices").

**Where we use it.** In `dn-core-query-protocol` §2.2, this is the "inversion" that makes **mode 2
(semantic) the generic point of the PSD-kernel cone**: since *every* PSD kernel is some embedding's
Gram, an arbitrary similarity kernel `K_sem` need not be graph-spectral — mode 1b (the structural
diffusion kernel `𝔉(L) = {f(L)}`) is the *thin* spectral locus inside the cone, mode 2 is the
generic interior. A learned embedding is on the cone always, on the structural curve only if it is
(a rotation of) a spectral embedding.

**The distinction that was corrected (Mercer ≠ Moore–Aronszajn).**

- **Moore–Aronszajn (1950)** — general. Any PSD kernel on *any* set yields an RKHS / an inner-product
  feature map. This is the fact the note needs. *(Also the elementary "kernel trick" folklore.)*
- **Mercer (1909)** — narrower. A *continuous* PSD kernel on a *compact* domain admits a uniformly
  convergent eigenfunction expansion `K(x,y) = Σ λ_i ψ_i(x) ψ_i(y)` with an explicit orthonormal
  basis. Mercer gives the spectral *expansion* under topology/compactness hypotheses; it is **not**
  the general "PSD ⇒ inner product" statement, which needs none of those hypotheses.

Using "Mercer" for the general fact (as the opus draft did) is a real misattribution — Mercer's
theorem is a stronger, more specialized claim. The correct general reference is Moore–Aronszajn.

**Verification.** Confirmed against primary sources 2026-07-13 (Aronszajn, *Trans. AMS* 68(3),
1950). Verdict CONFIRMED; the correction (Mercer → Moore–Aronszajn) was applied to
`dn-core-query-protocol` §2.2 and logged in its §1.3 item 6.
