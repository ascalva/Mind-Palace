# ── Family 5 (the reasoning complex) · symbols in docs/NOTATION.md ──
# OBJECT:    𝔎 = (V, ε, K_σ, ℋ, ρ, t) — the multilayer typed complex, and the generalized
#            Laplacian family δ*δ over it (companion III §1–§2).
# INVARIANT: the introspective complex is built ONLY from a MirrorView (𝔎|_MR); everything here
#            is deterministic and model-free (companion III §2.2, §7); no module touches the net.
# ENFORCED:  structural — build_complex takes a MirrorView (non-authored complex unrepresentable,
#            I6); Zone A (import-firewall: no edge/cloud/network import). Adopted subset only
#            (L, L_sym, signed L̄, Fiedler, diffusion); deferred instruments are not wired.
"""The reasoning complex (family 5, companions III) — Zone A, deterministic, model-free.

This package is the foundation of the strong Dreamer: the *object* (`build.py` — nodes, the
weighted similarity backbone A, the signed adjacency A_signed, the derivation hyperedges), the
*operator* (`laplacian.py` — L, L_sym, signed L̄), the principled *clusterer* (`spectral.py` —
Fiedler, diffusion map, spectral/diffusion clustering that dissolves the single-linkage chaining),
and rigorous *contradiction* (`balance.py` — λ_min(L̄), frustration, frustrated triangles).

It reaches no network (import-firewall green) and calls no model — the model is earned only for the
final narration step, elsewhere. Everything is deterministic under a fixed seed. The clusterer is
offered behind the `DreamerAdapter` seam; the live path opts in, and only the adopted subset (this
package's modules) is wired — the deferred instruments (sheaf Laplacian, Ollivier–Ricci, SBM,
persistence) are specified in the companions but not built here.
"""
