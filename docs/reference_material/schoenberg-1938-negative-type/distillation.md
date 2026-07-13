# Distillation — metrics of negative type and the PSD-kernel cone

**Load-bearing result (what our corpus relies on).** Schoenberg (1938) characterizes when a
metric space can be isometrically embedded into a Hilbert space (equivalently, when the
squared distances form a matrix expressible as a PSD Gram-type kernel): a metric is
embeddable exactly when it is of **negative type** (a specific conditionally-negative-
definite condition on the distance-squared matrix). Metrics that fail this condition cannot
arise as a squared Euclidean/Hilbert-space distance — they lie strictly outside what an
inner-product (PSD-kernel) structure can produce.

**Where we use it.** In `dn-core-query-protocol` §2.2, this grounds the claim of a **phase
transition at `β=∞`**: while every finite `β` in the free-energy family `K(β)` gives an
honest PSD kernel, the `β→∞` limit is a genuine *metric* (the tropical shortest-path
distance) that is **generically not of negative type** — by Schoenberg's characterization,
such a metric cannot be re-expressed as (embedded back into) the PSD-kernel cone. This is
what licenses the description of the tropical boundary as a qualitative break — inner-product
retrieval degenerating into idempotent, winner-take-all metric retrieval — rather than a
smooth continuation of the cone's structure. `[ESTABLISHED: Schoenberg 1938.]`

**Verification.** Confirmed against the primary source 2026-07-13 (Schoenberg, *Trans. AMS*
44(3), 522–536, 1938; doi 10.2307/1989894). Verdict CONFIRMED — the paper does establish
the negative-type ⟺ Hilbert-embeddability characterization, as cited.
