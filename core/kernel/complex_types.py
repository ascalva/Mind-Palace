# ── Family 5 shared types (the reasoning complex) · symbols in docs/NOTATION.md ──
# OBJECT:    the closed value-sets of the typed graph — edge polarity s ∈ {+1,−1} and the
#            B-arc node role ∈ {tail, head} (companion III §1.2–§1.3, §2.3).
# INVARIANT: these sets are CLOSED — an edge sign is +1 or −1 (never 0/3), a role is tail or head.
# ENFORCED:  structural — enums make any other value unconstructable (the ProposedChange move,
#            MATHEMATICAL-REFRAMING §B.1); no free int/str encodes the set at a call site.
"""Typed enums for the reasoning-complex graph (family 5; companion III §1.2–§1.3).

Small *closed* sets that would otherwise be free ints/strings — made enums so an illegal value
is unrepresentable rather than merely unexpected (the `MirrorView`/`ProposedChange` move,
`MATHEMATICAL-REFRAMING.md` §B.1: make it a type when that deletes an illegal state). These are
the shared vocabulary the derivation-hypergraph junction (`core/stores/derived.py`) uses today and
the signed `edges` table (Prompt H1) will use next; kept in a leaf module with no core imports so
both Zone-A consumers depend on it without a cycle. Nothing here touches the network.
"""

from __future__ import annotations

from enum import IntEnum, StrEnum


class EdgeSign(IntEnum):
    """Polarity of a typed edge (companion III §1.2, §2.3): +1 support / −1 contradict.

    An `IntEnum` so the *value itself* is the ±1 the signed-Laplacian arithmetic and the
    `edges.sign` column consume — `EdgeSign.CONTRADICT * w` is just `-w`. The enum deletes the
    illegal `sign = 3` (or `0`) state: polarity is a closed two-element set. A non-edge is the
    *absence* of a row, never a zero sign, so 0 is deliberately not a member.
    """

    SUPPORT = 1
    CONTRADICT = -1


class HyperedgeRole(StrEnum):
    """A node's role in a derivation B-arc (companion III §1.3, §2.5): the tail set
    T(e) = supp(κ) jointly entails the single head κ.

    `role ∈ {tail, head}` — the closed set the `hyperedge_nodes.role` column stores. A `StrEnum`
    so the stored value is the readable word while any other string is unconstructable. Today
    every head-set has size 1 (one head per `derives` hyperedge).
    """

    TAIL = "tail"
    HEAD = "head"
