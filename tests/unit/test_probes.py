"""Unit tests — the theory-probe candidate recorder (E6 Item 18).

The probe schema is grounded in the Track L §3 protocol annex
(`docs/design-notes/live-adoption-and-longitudinal-harness.md:140-142`):
`probe(probe_id, hypothesis, expectation_kind, target_hints)`, mapped onto a `plausible`-verdicted
claim. These tests pin the Item-18 acceptance: a `plausible` verdict emits exactly one candidate
keyed to the claim_id, a non-`plausible` verdict emits none, and the recorder is append-only +
idempotent by (claim_id, question). No probe *execution* is built (catalog row 12, R-gated).
"""

from __future__ import annotations

import pytest

from core.attestation import Ed25519Signer, generate_seed
from core.stores.runledger import RunLedger, claim_id
from core.stores.verdicts import VerdictStore
from core.verdict.taxonomy import VERDICT_TAXONOMY
from eval.harness.probes import ProbeCandidate, ProbeStore, open_probe_store, probe_id_for
from scripts.review import ReviewDeps, ReviewItem, run_review


def _claim_row(*, kind="tension", support=("s1", "s2"), polarity="-",
               surface="a tension between X and Y", confidence=0.9, novel=True):
    """A run-ledger-shaped claim dict (the columns `RunLedger.claims()` returns)."""
    return {
        "claim_id": claim_id(kind, support, polarity),
        "run_id": "run-abc",
        "kind": kind,
        "confidence": confidence,
        "support_json": '["s1","s2"]',
        "surface_text": surface,
        "novel": 1 if novel else 0,
    }


def _keyed_reader(keys):
    it = iter(keys)

    def read_key(_prompt):
        return next(it)   # StopIteration ends the session (treated as quit)

    return read_key


def _sink(tmp_path):
    """An in-memory-ish verdict sink (real store on tmp disk) + a generated test signer — the
    builder NEVER touches the real signed store."""
    store = VerdictStore(tmp_path / "verdicts.sqlite", allowed_verdicts=VERDICT_TAXONOMY)
    signer = Ed25519Signer.from_seed(generate_seed(), "owner")
    pub = signer.public_b64()

    def submit(signed):
        return store.append(signed, public_b64=pub)

    def next_seq():
        latest = store.latest_seq()
        return (latest + 1) if latest is not None else 1

    return store, signer, submit, next_seq


# --- the store in isolation --------------------------------------------------------------------

def test_from_claim_grounds_the_annex_fields(tmp_path):
    claim = _claim_row(surface="my notes on X and Y are connected")
    cand = ProbeCandidate.from_claim(claim, pipeline="dream_v2")
    assert cand.claim_id == claim["claim_id"]
    assert cand.hypothesis == "my notes on X and Y are connected"   # annex: hypothesis = surface
    assert cand.expectation_kind == claim["kind"]                   # annex: expectation_kind
    assert cand.target_hints == claim["support_json"]              # annex: target_hints
    assert cand.pipeline == "dream_v2"                              # plan Q4: provenance key
    assert cand.probe_id == probe_id_for(claim["claim_id"], cand.hypothesis)


def test_record_is_idempotent_by_claim_and_question(tmp_path):
    store = ProbeStore(tmp_path / "probes.sqlite")
    claim = _claim_row()
    cand = ProbeCandidate.from_claim(claim, pipeline="phase7")
    first = store.record(cand)
    second = store.record(ProbeCandidate.from_claim(claim, pipeline="phase7"))
    assert store.count() == 1                       # append-only + idempotent by probe_id
    assert first.probe_id == second.probe_id
    assert first.recorded_at == second.recorded_at  # the original row stands (no overwrite)


def test_open_probes_enumerates_recorded_candidates(tmp_path):
    store = ProbeStore(tmp_path / "probes.sqlite")
    store.record(ProbeCandidate.from_claim(_claim_row(surface="claim one"), pipeline="phase7"))
    store.record(ProbeCandidate.from_claim(_claim_row(surface="claim two"), pipeline="dream_v2"))
    probes = store.open_probes()
    assert len(probes) == 2
    assert {p.pipeline for p in probes} == {"phase7", "dream_v2"}


def test_no_mutation_api(tmp_path):
    store = ProbeStore(tmp_path / "probes.sqlite")
    # Append-only: no update/delete surface exists (probes are standing candidates).
    assert not hasattr(store, "update")
    assert not hasattr(store, "delete")


def test_open_probe_store_paths_beside_derived(tmp_path):
    class _Paths:
        derived_store = tmp_path / "derived" / "store.db"

    class _Cfg:
        paths = _Paths()

    store = open_probe_store(_Cfg())
    assert store.path == tmp_path / "derived" / "probes.sqlite"


# --- the probe spillover wired into the REPL (Item 18 composes into Item 17) -------------------

def test_plausible_verdict_emits_exactly_one_probe(tmp_path):
    probe_store = ProbeStore(tmp_path / "probes.sqlite")
    _store, signer, submit, next_seq = _sink(tmp_path)
    claim = _claim_row()
    item = ReviewItem(claim=claim, pipeline="dream_v2")

    def record_probe(it):
        probe_store.record(ProbeCandidate.from_claim(it.claim, pipeline=it.pipeline))

    deps = ReviewDeps(signer=signer, submit=submit, next_seq=next_seq,
                      record_probe=record_probe, read_key=_keyed_reader(["p"]),
                      write=lambda _m: None, now=lambda: "2026-07-16T00:00:00")
    run_review([item], deps)

    probes = probe_store.open_probes()
    assert len(probes) == 1
    assert probes[0].claim_id == claim["claim_id"]      # keyed to the claim_id (plan Q2)


@pytest.mark.parametrize("key", ["n", "k", "w", "x"])
def test_non_plausible_verdict_emits_no_probe(tmp_path, key):
    probe_store = ProbeStore(tmp_path / "probes.sqlite")
    _store, signer, submit, next_seq = _sink(tmp_path)
    item = ReviewItem(claim=_claim_row(), pipeline="phase7")

    def record_probe(it):
        probe_store.record(ProbeCandidate.from_claim(it.claim, pipeline=it.pipeline))

    deps = ReviewDeps(signer=signer, submit=submit, next_seq=next_seq,
                      record_probe=record_probe, read_key=_keyed_reader([key]),
                      write=lambda _m: None, now=lambda: "2026-07-16T00:00:00")
    run_review([item], deps)
    assert probe_store.count() == 0                     # no probe for a non-plausible verdict


def test_reemitted_plausible_claim_maps_to_one_probe(tmp_path):
    """Two runs re-emit the same claim (shared claim_id); verdicting both `plausible` records ONE
    probe — idempotency by (claim_id, question) across re-emission (plan Q2)."""
    ledger = RunLedger(":memory:")
    p7 = ledger.start_run(pipeline="phase7", config_fingerprint="f1", corpus_digest="c1",
                          node_count=1, edge_count=0, duration_s=0.1, spectral_stats={})
    d2 = ledger.start_run(pipeline="dream_v2", config_fingerprint="f2", corpus_digest="c1",
                          node_count=1, edge_count=0, duration_s=0.1, spectral_stats={})
    ledger.add_claim(p7, kind="tension", confidence=0.9, support=("s1", "s2"),
                     surface_text="a tension", polarity="-")
    ledger.add_claim(d2, kind="tension", confidence=0.5, support=("s1", "s2"),
                     surface_text="a tension", polarity="-")   # re-emit → same claim_id, novel=0
    rows = ledger.claims()
    assert rows[0]["claim_id"] == rows[1]["claim_id"]

    probe_store = ProbeStore(tmp_path / "probes.sqlite")
    _store, signer, submit, next_seq = _sink(tmp_path)
    items = [ReviewItem(claim=rows[0], pipeline="phase7"),
             ReviewItem(claim=rows[1], pipeline="dream_v2")]

    def record_probe(it):
        probe_store.record(ProbeCandidate.from_claim(it.claim, pipeline=it.pipeline))

    deps = ReviewDeps(signer=signer, submit=submit, next_seq=next_seq,
                      record_probe=record_probe, read_key=_keyed_reader(["p", "p"]),
                      write=lambda _m: None, now=lambda: "2026-07-16T00:00:00")
    run_review(items, deps)
    assert probe_store.count() == 1                     # one probe despite two plausible verdicts
    ledger.close()
