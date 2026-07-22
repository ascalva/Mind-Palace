"""The reasoning-complex graph enums (Prompt R1, move 3): closed value-sets as types.

EdgeSign is ±1 (the value usable directly in signed arithmetic); HyperedgeRole is {tail, head}.
The point of the move is that any other value is unconstructable, not merely unexpected.
"""

from core.kernel.complex_types import EdgeSign, HyperedgeRole


def test_edge_sign_values_are_plus_minus_one():
    assert int(EdgeSign.SUPPORT) == 1
    assert int(EdgeSign.CONTRADICT) == -1
    # The value IS the ±1 — usable in arithmetic without a lookup table.
    assert EdgeSign.CONTRADICT * 0.7 == -0.7
    assert {int(s) for s in EdgeSign} == {1, -1}          # closed set, no zero


def test_hyperedge_role_values():
    assert HyperedgeRole.TAIL.value == "tail"
    assert HyperedgeRole.HEAD.value == "head"
    assert {r.value for r in HyperedgeRole} == {"tail", "head"}


def test_enums_reject_out_of_set_values():
    import pytest
    with pytest.raises(ValueError):
        EdgeSign(0)                                       # a non-edge is an absent row, not sign 0
    with pytest.raises(ValueError):
        EdgeSign(3)
    with pytest.raises(ValueError):
        HyperedgeRole("middle")
