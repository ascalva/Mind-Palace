# bp-082 journal

## 2026-07-21T02:40Z — minted at graduation (session-39, orchestrator)

Plan minted `proposed` from ratified `dn-synchronic-diachronic-dreamer` (§2.7, H-2 — the
capstone). No build session yet. The conditioning law fails CLOSED (F-SD7b). The likeliest
stop-and-raise is Q3 (the derives/provenance shape). Depends on bp-079 + bp-081. Awaiting
owner blessing.

## 2026-07-21 — Items 11–13 complete (opus builder, worktree branch)

Dispatched by session-39 as an opus builder in an isolated worktree (branch off current main;
bp-079 + bp-081 merged). Read the whole contract + the merged substrate (`composed.py`,
`staging.py`, `sigma_star.py`, `conductance.py`, `census.py`, `derived.py`, `evaluate.py`,
`dreamer.py`, `charter.py`, dn §2.6/§2.7). All three items landed; no scope escape.

### Q3 (§3 Q3 / §10) — the Item-13 stop-and-raise did NOT fire.
Read `core/stores/derived.py` at HEAD before implementing clause 1. The derives/provenance shape
CARRIES the staged tails without a durable-store schema change: `derived_from` is a JSON array of
arbitrary string refs (holds staged content addresses as tails) and `data` is a free-form JSON
dict (holds the `(subspace_id, generation, staged_digests)` mark). So the conditioning mark rides
the EXISTING shape — no schema change, Item 13 lands in FULL (both clauses). Did NOT edit
`dreamer.py`/`derived.py` (out of write_scope, read-only): `conditioning.py` provides the marking
helpers a future dreamer write-path calls + the fail-closed law, exercised over in-memory
DerivedStore/StagingStore fixtures (dry-run). No finding filed.

### Item 11 — integer-family influence (exact diff + CN-3 attribution). GREEN.
`core/graph/influence.py`: `sigma_star_influence` (Δσ* component structure — exact recompute-diff
of every pair's σ* WITHOUT vs WITH the overlay via `compose_staged`, reusing the real
`build_max_spanning_tree`/`pairwise_sigma_star`) + `census_influence` (Δcensus set-diff over the
arrow layer, reusing the real `census`). Leave-one-out attribution (`_attribute_sigma`; census LOO
inline) names only revert-confirmed staged elements — the decorative-attribution falsifier is
structurally impossible. One-sided law structural: `after >= before` (None as floor) asserted;
`NegativeAdditiveInfluenceError` raises on a violation (fails the suite, never a finding). The
whole op is gated by the HYPOTHETICAL grant (a durable-only grant → `StagedGrantRequired`).
Acceptance: staged bridge flips a—d None→0.9, attribution names exactly `("b","c",1.0)`; staged
arc closing a→b→c→a shows in Δcensus with witness `("e1","e2","s1")`; empty overlay ⇒ zero
influence. 13 tests in `test_influence.py`.

### Item 12 — smooth-family influence (Rayleigh + finite-difference check). GREEN.
`rayleigh_influence(w_base, w_overlay, index)` over a synthetic Laplacian (Q4 fixture is the
ground; `[FROM MEMORY]` first-order-perturbation/Weyl citations kept as code comments for the
external-grounding sweep). estimate = `x*ΔL x`; exact = `λ_i(L+ΔL) − λ_i(L)` (the
finite-difference check). `perturbative` claimed ONLY when ‖ΔL‖₂ ≤ 0.5·gap AND
|estimate−exact| ≤ second-order bound (‖ΔL‖²/gap); past either it switches to exact and declares
"recomputed, not perturbative" (F-SD7a). One-sided structural: ΔL PSD ⇒ estimate/exact ≥ 0
(`_assert_one_sided_smooth` raises on negative); a removal-ward Δ is refused up front
(`NonAdditiveOverlayError`, SD-e parked). Acceptance: small Δ perturbative within bound; large Δ
recompute-declared; sweep asserts the flag never disagrees beyond bound.

### Item 13 — the conditioning law (four clauses, fails closed). GREEN.
`core/dreaming/conditioning.py`. Clause 1: `Condition` + `condition_data` (the `data` mark) +
`conditioned_derives` (authored leaves ++ staged digests as tails). Clause 2: `is_surfaceable`
(TTL inheritance — surfaces iff every pinned staged digest is still live at the read generation;
expiry blocks quietly, the record survives + pinned generation stays reproducible). Clause 3:
`taint_split` consumes the SAME `SigmaStarInfluence` output as Item 11 (one diff, double duty).
Clause 4: `assert_grounding_terminates` (no dream tail — recursion bound; staged tails must be
declared). The fail-closed gate `verify_surfacing` checks all three F-SD7b teeth: taint-test (1)
and lineage-audit (3) RAISE `ConditioningViolation`; sweep-test (2) blocks quietly (returns
False). 8 tests in `test_conditioning_law.py`.

### CI gate (all green) + ratchet
ruff `.` clean; check_imports OK; mypy on the 4 files clean; `ops.type_gate` OK; full pytest
`1789 passed, 11 skipped` (deselecting the finding-0103 node + green-gate markers). finding-0103
ratchet UNCHANGED at 19 (both new modules import core.* + stdlib + numpy/scipy only; neither
appears in the violation list). Scope: wrote only the 4 write_scope files + this journal.

Parked (unchanged from the plan): SD-e removal overlays, SD-f spectral influence, influence
narration — all §11 defaults stand; no re-entry triggered. No findings filed. NOT merged (the
orchestrator is single-writer).
