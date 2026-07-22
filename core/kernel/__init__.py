"""The inner core — the kernel subtree (dn-inner-outer-core §2.7, wave K1 / bp-090).

`core/kernel/**` physically *is* the inner ring: the founding language of the system — the
mathematics, the algebra, the sacred-boundary vocabulary — **not** the austere plumbing (the owner's
v2 ruling, §2.1). Membership is mechanical, never curated: the inner ring is the maximal
import-closed subset of `core/**` over the admissible base
`(stdlib ∖ NETWORK_MODULES ∖ PLUMBING_STDLIB) ∪ {numpy, scipy}` under strict closure semantics.
The declaration lives in `core.kernel.rings.INNER`; `tests/unit/test_inner_ring.py` forces it to
equal the recomputed fixed point (§2.4-B1).

This package is **inner by construction**: stdlib-only, side-effect-free at import, wires no read
path. The outer ring is `core/**` minus `core/kernel/**` — machinery beside the vocabulary it is
written in. The core-wide egress perimeter (`ops.import_lint`, the outer ratchet) still binds ALL of
`core/**`, this subtree included — the kernel is a *meaning* boundary, not the egress boundary.
"""
