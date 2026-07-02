"""Unit tests for the typed/signed EdgeStore (H1; companion III §1.2).

Proves: an edge round-trips with its polarity (EdgeSign); ids are content-derived so re-asserting
is idempotent; the sign is a closed ±1 set (out-of-set values rejected at the boundary); negative
strength is refused (polarity lives in `sign`, not `w`).
"""

import pytest

from core.complex_types import EdgeSign
from core.stores.edges import CONTRADICTS, SUPPORTS, EdgeStore


def _store(tmp_path):
    return EdgeStore(tmp_path / "edges.sqlite")


def test_add_and_read_back(tmp_path):
    s = _store(tmp_path)
    e = s.add("a", "b", sign=EdgeSign.CONTRADICT, rel_type=CONTRADICTS, w=0.8)
    assert e.sign is EdgeSign.CONTRADICT
    got = s.all()[0]
    assert (got.u, got.v, got.rel_type, got.w) == ("a", "b", CONTRADICTS, 0.8)
    assert got.sign is EdgeSign.CONTRADICT           # polarity survives the round-trip as the enum


def test_ids_are_content_derived_so_reassertion_is_idempotent(tmp_path):
    s = _store(tmp_path)
    s.add("a", "b", sign=EdgeSign.SUPPORT, rel_type=SUPPORTS)
    s.add("a", "b", sign=EdgeSign.SUPPORT, rel_type=SUPPORTS, w=2.0)   # same (u,v,rel) → replace
    assert s.count() == 1
    assert s.all()[0].w == 2.0


def test_reset_is_regenerable(tmp_path):
    s = _store(tmp_path)
    s.add("a", "b", sign=EdgeSign.SUPPORT, rel_type=SUPPORTS)
    s.reset()
    assert s.count() == 0


def test_negative_strength_is_refused(tmp_path):
    s = _store(tmp_path)
    with pytest.raises(ValueError):
        s.add("a", "b", sign=EdgeSign.CONTRADICT, rel_type=CONTRADICTS, w=-1.0)


def test_sign_is_a_closed_set(tmp_path):
    s = _store(tmp_path)
    with pytest.raises(ValueError):
        s.add("a", "b", sign=3, rel_type=CONTRADICTS)    # not ±1 → EdgeSign rejects it
