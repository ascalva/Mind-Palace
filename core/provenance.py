"""Provenance classes for the data architecture (BUILD-SPEC §8; design-notes/
observed-data-and-the-assistant-tier.md).

Every stored datum carries a provenance class so a query or agent can always distinguish
"the owner wrote this" from "the system inferred this" — and, in a later phase, from
"a third-party system observed this". The mirror (introspection / dreaming) reads
AUTHORED only; that firewall keeps algorithmic exhaust out of the owner's reflection and
out of the behavioral baselines (§15).
"""

from __future__ import annotations

from enum import StrEnum


class Provenance(StrEnum):
    AUTHORED = "authored"        # owner wrote it. Ground truth, immutable, feeds the mirror.
    INTERPRETED = "interpreted"  # system inference over other data. Derived, regenerable, marked.
    # RESERVED — not ingested yet. Third-party behavioral exhaust (Data Portability export,
    # web/social history, sensor streams). Low-trust, ASSISTANT-TIER ONLY, quarantined from
    # the mirror and from behavioral baselines (§15). Lands Phases 3+; defined now so stores
    # and queries are provenance-aware from the start (cf. the dormant sensor schema).
    OBSERVED = "observed"


# What the introspective mirror / dreaming agent is permitted to read (the firewall).
MIRROR_READABLE: frozenset[Provenance] = frozenset({Provenance.AUTHORED})
