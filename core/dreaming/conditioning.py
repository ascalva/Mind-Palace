# ── Family: the counterfactual overlay · the conditioning law (anti-laundering) · NOTATION.md ─────
# OBJECT:    the conditioning law over a hypothesis-conditioned dream artifact
#            (dn-synchronic-diachronic-dreamer §2.7 SD-7, all four clauses). A dream over
#            graph ∪ subspace is a CONDITIONED artifact: (1) it records (subspace_id, generation,
#            staged-item digests) and its `derives` tails include those staged content addresses;
#            (2) it INHERITS the subspace's TTL — an expired subspace ⇒ its conditioned artifacts
#            leave the surfacing set (retained as records); (3) the per-claim leave-the-subspace-out
#            recompute IS the influence diff — corpus-grounded claims (bit-identical without the
#            overlay) may shed the mark, conditioned claims keep it; (4) grounding terminates in
#            authored evidence OR declared hypothesis, marked — never prior interpretation.
# INVARIANT: the law FAILS CLOSED — any of the three F-SD7b teeth observed ⇒ surfacing is BLOCKED,
#            never warned. The mark rides the EXISTING derives/provenance shape (Q3: `derived_from`
#            is arbitrary string tails, `data` is free-form — no durable-store schema change). The
#            recursion bound is untouched: a dream's tails never include a dream (dreams never cite
#            dreams as evidence). No wall clock (Law C4 — the staging generation is the clock).
# ENFORCED:  guard (tests/unit/test_conditioning_law.py) — a conditioned fixture carries the mark
#            and the staged tails; after expiry it leaves the surfacing set but stays readable; the
#            taint split is the SAME diff as influence; each F-SD7b tooth blocks surfacing.
r"""The conditioning law — the anti-laundering tooth of the synchronic/diachronic dreamer (§2.7).

A dream synthesized over `graph ∪ subspace` is *hypothesis-conditioned*: part of its grounding
bottoms out in a STAGED hypothesis, not authored evidence. The taint is structural, not editorial —
a hypothesis the owner never authored cannot launder itself into belief through the dreamer's
exhaust. The four clauses (note §2.7), each fail-closed:

  1. **Provenance carries the condition.** A conditioned artifact records `(subspace_id,
     generation, staged-item digests)` in its `data`, and its `derives` tails include the staged
     items' content addresses. The mark RIDES the existing shape: `derived_from` is a flat tuple of
     arbitrary string refs (it carries staged digests as tails), and `data` is a free-form dict (it
     carries the condition record) — no durable-store schema change (Q3 verified at build start).
     The mark in `data` is what distinguishes a staged tail from an authored leaf, so the sharpened
     grounding rule (clause 4) is auditable.
  2. **TTL inheritance.** A conditioned artifact surfaces ONLY while its pinned staged digests are
     still live in the staging store at the read generation. When the subspace expires (its rows
     tombstoned by the sweep), the artifact leaves the surfacing set — but it stays READABLE as a
     record (the artifact is untouched; the staging store's generation-addressed reads keep an
     expired dream reproducible, §2.6-2). A hypothesis cannot outlive its own expiry through a
     dream.
  3. **Taint attribution IS the influence computation** (the unification that makes this cheap).
     The per-claim leave-the-subspace-out recompute is the SAME with/without diff as
     `core.graph.influence`: a claim that holds bit-identically without the overlay is
     *corpus-grounded* (may shed the mark); a claim with nonzero influence is *conditioned* (keeps
     it). One diff does double duty — influence detection and taint attribution.
  4. **Grounding terminates in authored evidence or declared hypothesis, marked — never in prior
     interpretation.** The recursion bound is untouched: a dream's tails never include a dream
     (dreams cannot cite dreams as evidence, `recursive-dreaming-bounded-by-grounding` rule); the
     citation classes split (authored leaf vs staged digest) and the split is visible in every
     report.

*Falsifiers (F-SD7b), all fail-closed:* a claim marked corpus-grounded whose reading changes when
the subspace is removed (taint test); a conditioned artifact surfacing after its generation expired
(sweep test); a `derives` edge over a composed read whose tails omit staged digests (lineage
audit). Any one observed ⇒ the law is broken and surfacing is BLOCKED — never a warning.

PURE-CORE: imports core substrate only (`core.stores.{derived,staging}`); reads no network,
materializes no wall clock (the staging generation is the clock, Law C4). It does NOT write a
durable store — the marking helpers shape what a (future) dreamer write path passes to the existing
`DerivedStore.add`; this module only reads and verifies (dry-run over fixtures here).
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Protocol

from core.stores.derived import Artifact
from core.stores.staging import StagingStore

# The `data` key under which a conditioned artifact records its condition (clause 1). A stable
# string so the dreamer write path, the surfacing filter, and the lineage audit all agree.
CONDITION_KEY = "condition"


class ConditioningViolation(AssertionError):
    """An F-SD7b tooth was observed — the conditioning law is broken. Raised so surfacing FAILS
    CLOSED (blocked, never warned): a corpus-grounded claim that changes under the overlay (taint
    test), or a conditioned artifact whose `derives` tails omit staged digests (lineage audit).
    These are structural laundering bugs, not the normal expiry lifecycle (which blocks surfacing
    without raising — see `is_surfaceable`)."""


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Clause 1 — the condition record + the derives tails (the mark rides the existing shape)
# ═══════════════════════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class Condition:
    """The hypothesis a conditioned artifact is grounded on (clause 1): the `subspace_id` it read,
    the `generation` it pinned (the staging store's event clock — reproducible as a record, Law
    C4), and the `staged_digests` (the staged items' content addresses that enter the `derives`
    tails)."""

    subspace_id: str
    generation: int
    staged_digests: tuple[str, ...]


def condition_data(cond: Condition) -> dict[str, Any]:
    """The `data` payload marking an artifact as hypothesis-conditioned (clause 1). A dreamer write
    path merges this into `DerivedStore.add(data=...)`; the mark is what lets a leaf-audit tell a
    staged tail from an authored leaf (clause 4). Pure data — no store write here."""
    return {
        CONDITION_KEY: {
            "subspace_id": cond.subspace_id,
            "generation": cond.generation,
            "staged_digests": list(cond.staged_digests),
        }
    }


def conditioned_derives(authored_leaves: Iterable[str], cond: Condition) -> tuple[str, ...]:
    """The `derives` tails for a conditioned artifact (clause 1): the authored-leaf digests PLUS the
    staged items' content addresses, so the grounding chain visibly bottoms out partly outside the
    corpus. The staged digests appear here (as tails) AND in `data` (the mark) — the redundancy is
    the lineage audit's cross-check (F-SD7b tooth 3). Order-stable; duplicates dropped."""
    seen: set[str] = set()
    out: list[str] = []
    for ref in (*authored_leaves, *cond.staged_digests):
        if ref not in seen:
            seen.add(ref)
            out.append(ref)
    return tuple(out)


def read_condition(artifact: Artifact) -> Condition | None:
    """Parse the condition mark off an artifact's `data`, or None if it is not conditioned (an
    ordinary corpus-grounded dream). The inverse of `condition_data`."""
    raw = artifact.data.get(CONDITION_KEY)
    if raw is None:
        return None
    return Condition(
        subspace_id=raw["subspace_id"],
        generation=int(raw["generation"]),
        staged_digests=tuple(raw["staged_digests"]),
    )


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Clause 2 — TTL inheritance: a conditioned artifact surfaces only while its subspace is live
# ═══════════════════════════════════════════════════════════════════════════════════════════════


def is_surfaceable(cond: Condition, store: StagingStore, *, at: int | None = None) -> bool:
    """Whether a conditioned artifact may SURFACE at staging generation `at` (default: the current
    generation) — clause 2, TTL inheritance. True iff EVERY pinned staged digest is still live in
    the subspace at `at`; once the subspace expires (its rows tombstoned by the sweep) the digests
    drop out of the generation-addressed read and the artifact leaves the surfacing set. This blocks
    surfacing WITHOUT raising: expiry is the normal lifecycle, not a laundering bug. The artifact
    itself stays a readable record — this function reads, never deletes."""
    live = {r.content_digest for r in store.subspace_at(cond.subspace_id, at)}
    return all(d in live for d in cond.staged_digests)


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Clause 3 — the taint split IS the influence diff
# ═══════════════════════════════════════════════════════════════════════════════════════════════


class _Changeable(Protocol):
    """The minimal surface the taint split reads off an influence reading: whether the overlay moved
    it. `core.graph.influence.SigmaStarInfluence` satisfies this, so the taint split literally
    consumes the SAME with/without diff as Items 11–12 (clause 3 — one diff, double duty)."""

    @property
    def changed(self) -> bool: ...


@dataclass(frozen=True)
class TaintSplit:
    """The per-claim taint split (clause 3): `conditioned` are the influence readings the overlay
    moved (nonzero delta — they KEEP the condition mark); `corpus_grounded` are the readings
    bit-identical without the overlay (they MAY shed it). The split is computed straight from the
    influence output — taint attribution and influence detection are the same diff."""

    conditioned: tuple[_Changeable, ...]
    corpus_grounded: tuple[_Changeable, ...]


def taint_split(influences: Iterable[_Changeable]) -> TaintSplit:
    """Split per-claim influence readings into conditioned (moved by the overlay ⇒ keep the mark)
    and corpus-grounded (unmoved ⇒ may shed it) — clause 3. The input IS the `core.graph.influence`
    output (the leave-the-subspace-out recompute); no second computation."""
    conditioned = tuple(i for i in influences if i.changed)
    corpus_grounded = tuple(i for i in influences if not i.changed)
    return TaintSplit(conditioned=conditioned, corpus_grounded=corpus_grounded)


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Clause 4 — grounding terminates in authored evidence or declared (marked) hypothesis
# ═══════════════════════════════════════════════════════════════════════════════════════════════


def assert_grounding_terminates(
    artifact: Artifact, cond: Condition, *, dream_ids: Iterable[str]
) -> None:
    """The sharpened grounding rule (clause 4): every `derives` tail of a conditioned artifact is
    either an authored leaf or one of the condition's declared (marked) staged digests — and NO tail
    is a dream (the recursion bound is untouched: dreams never cite dreams as evidence). Raises
    `ConditioningViolation` (fail closed) if a tail is a dream, or if a staged digest in the mark is
    missing from the tails (an undeclared hypothesis masquerading as an authored leaf)."""
    dreams = set(dream_ids)
    tails = set(artifact.derived_from)
    staged = set(cond.staged_digests)
    cited_dreams = tails & dreams
    if cited_dreams:
        raise ConditioningViolation(
            f"conditioned artifact {artifact.id!r} cites dream(s) {sorted(cited_dreams)} as "
            f"evidence — the recursion bound forbids a dream grounding on a dream (clause 4)"
        )
    # Every staged digest in the mark must appear as a tail (the lineage audit, tooth 3) — so an
    # undeclared hypothesis cannot pose as an authored leaf.
    missing_tails = staged - tails
    if missing_tails:
        raise ConditioningViolation(
            f"conditioned artifact {artifact.id!r} omits staged digest(s) {sorted(missing_tails)} "
            f"from its derives tails — the grounding chain must visibly bottom out on the declared "
            f"hypothesis (clause 4 / F-SD7b lineage audit)"
        )


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# The fail-closed surfacing gate — every F-SD7b tooth blocks surfacing
# ═══════════════════════════════════════════════════════════════════════════════════════════════


def verify_surfacing(
    artifact: Artifact,
    cond: Condition,
    split: TaintSplit,
    store: StagingStore,
    *,
    dream_ids: Iterable[str] = (),
    at: int | None = None,
) -> bool:
    """The fail-closed gate a caller runs BEFORE surfacing a conditioned dream. Checks all three
    F-SD7b teeth and returns whether the artifact may surface:

      * **tooth 3 (lineage audit)** — the derives tails must include every staged digest, and no
        tail may be a dream (clause 4). A violation RAISES `ConditioningViolation` (a laundering
        bug, fail closed loudly).
      * **tooth 1 (taint test)** — every claim the split marks corpus-grounded must genuinely be
        unmoved by the overlay; a corpus-grounded claim that `changed` RAISES (an inconsistent mark
        is a laundering bug).
      * **tooth 2 (sweep test)** — if the subspace has expired (a pinned staged digest is no longer
        live), the artifact does NOT surface: returns False. Expiry is the normal lifecycle, not a
        bug, so it blocks quietly rather than raising.

    Returns True only when all teeth pass AND the subspace is still live — the single sanctioned way
    a conditioned dream reaches the surfacing set."""
    assert_grounding_terminates(artifact, cond, dream_ids=dream_ids)  # tooth 3 (raises)
    for infl in split.corpus_grounded:
        if infl.changed:
            raise ConditioningViolation(
                f"a claim marked corpus-grounded for {artifact.id!r} changes when the subspace is "
                f"removed — the taint mark is inconsistent (F-SD7b taint test); fail closed"
            )
    return is_surfaceable(cond, store, at=at)  # tooth 2 (blocks quietly)
