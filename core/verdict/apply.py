"""Receive + verify a transported owner verdict, then persist it — the inbound verdict channel's
verify seam (design-notes/verdict-authority.md §4; build plan Item 4b).

SEPARATE from the Ambassador, which is read+propose only (build plan R7): the Ambassador — or any
transport — carries a `SignedVerdict` HERE; this verifies it against the owner PUBLIC key and
appends it to the append-only store. A compromised transport can drop/reorder (refused or made
visible by the store's monotonic seq + `gaps()`) but can never FORGE one (only the public key is
held). Zone A, no network.

The APPLY half — effecting the promotion / supersession on the reasoning graph — is deliberately
deferred: it depends on the promotion mechanism (recursive-strata I1), which is parked. This seam
closes the AUTHENTICATION + DURABILITY boundary; promotion lands with that mechanism (4b-apply).
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from config.loader import Config
from core.stores.verdicts import VerdictRecord, VerdictStore
from core.verdict.dispositions import DispositionStore, VerdictEffect
from core.verdict.payload import SignedVerdict


class OwnerKeyMissing(RuntimeError):
    """No owner public key is placed, so a verdict cannot be verified — fail closed (an
    unverifiable verdict is never stored). Place `[attestation] owner_pub` before receiving."""


def load_owner_pub_b64(config: Config | None = None) -> str:
    """The owner's base64 Ed25519 public key from the committed `[attestation] owner_pub` file —
    the same non-secret key material the attestation verifier already loads
    (`core/attestation/verify.load_public_keys`). Raises `OwnerKeyMissing` if absent, so a verdict
    is never accepted without a key to check it against."""
    from config.loader import get_config

    cfg = config or get_config()
    path = Path(cfg.attestation.owner_pub)
    if not path.exists():
        raise OwnerKeyMissing(
            f"owner public key not found at {path} — place it "
            "(scripts/gen_attestation_keys.py) before receiving verdicts"
        )
    return path.read_text().strip()


def receive_verdict(signed: SignedVerdict, store: VerdictStore, *,
                    owner_pub_b64: str) -> VerdictRecord:
    """Verify a transported verdict against the owner key and append it. Fail-closed throughout:
    `store.append` re-verifies the signature, enforces the ratified taxonomy, and enforces the
    monotonic sequence — so a forged, mis-categorized, or replayed verdict never persists."""
    return store.append(signed, public_b64=owner_pub_b64)


def effect_of(verdict: str) -> VerdictEffect:
    """Map a verdict category to its active-projection effect (pure). `wrong`/`noise` RETRACT the
    claim (drop it from the active view, keep it in history); `novel_useful` ENDORSES it;
    `true_known`/`plausible` are RECORDED. WEIGHT promotion (recursive-strata I1) is parked and
    intentionally not expressed here."""
    return {
        "wrong": VerdictEffect.RETRACT,
        "noise": VerdictEffect.RETRACT,
        "novel_useful": VerdictEffect.ENDORSE,
    }.get(verdict, VerdictEffect.RECORD)


def apply_verdict(record: VerdictRecord, dispositions: DispositionStore) -> VerdictEffect:
    """Apply a stored verdict to the active projection: compute its effect and record the
    disposition against its subject (append-only, latest-wins by seq). Implements the supersession /
    endorsement half of 'apply' (ingest-identity §6); the WEIGHT-promotion half (recursive-strata
    I1) is parked. Returns the effect applied."""
    effect = effect_of(record.verdict)
    dispositions.record(record.subject_id, effect, record.seq)
    return effect


def build_verdict_receiver(
    config: Config | None = None,
) -> Callable[[SignedVerdict], VerdictRecord]:
    """Wire (store, owner key) from config into a `receive(signed)` closure — the transport seam a
    scheduler/interface layer calls with a `SignedVerdict` it carried inbound. The store is opened
    beside the other core stores with the ratified `VERDICT_TAXONOMY`; the owner public key is the
    committed `[attestation] owner_pub`. Reuses existing key material — no parallel key path."""
    from core.stores.verdicts import open_verdict_store
    from core.verdict.dispositions import open_disposition_store
    from core.verdict.taxonomy import VERDICT_TAXONOMY

    store = open_verdict_store(config, allowed_verdicts=VERDICT_TAXONOMY)
    dispositions = open_disposition_store(config)
    owner_pub_b64 = load_owner_pub_b64(config)

    def receive(signed: SignedVerdict) -> VerdictRecord:
        rec = receive_verdict(signed, store, owner_pub_b64=owner_pub_b64)
        apply_verdict(rec, dispositions)   # verify + store + APPLY (weight promotion I1 parked)
        return rec

    return receive
