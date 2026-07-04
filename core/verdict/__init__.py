"""The inbound verdict channel — the owner's authorization to promote/supersede an
interpretation (design-notes/verdict-authority.md; the sacred boundary, inbound: verdict).

`payload.py` — the pure signing core (canonical serialization, signing, verification).
`taxonomy.py` — the ratified verdict categories the store accepts (build plan R3).
`apply.py` — the receive+verify seam (SEPARATE from the Ambassador, R7); the promotion-apply
half is deferred (parked on recursive-strata I1). The append-only signed store itself lives in
`core/stores/verdicts.py`. Zone A, no network.

This package `__init__` exports only the PURE surface (payload + taxonomy). `apply.py` depends on
`core.stores.verdicts`, which imports `core.verdict.payload` — importing apply here would close a
package-init cycle. It is a leaf consumers import directly:
`from core.verdict.apply import build_verdict_receiver`.
"""

from core.verdict.payload import SignedVerdict, VerdictPayload, sign_verdict
from core.verdict.taxonomy import VERDICT_TAXONOMY

__all__ = ["SignedVerdict", "VerdictPayload", "sign_verdict", "VERDICT_TAXONOMY"]
