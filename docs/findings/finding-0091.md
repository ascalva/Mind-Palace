---
type: finding
id: finding-0091
status: routed        # /triage 2026-07-17: routed to orchestrator; batched to oq-0028 (non-blocking erratum)
created: 2026-07-16
updated: 2026-07-17
links:
  - docs/design-notes/velocity-instruments.md   # the ratified §2.2 (a) RotationReport the build had to make constructive (A8 — never hand-edited)
  - core/temporal_view.py                        # RotationReport / _principal_angles — where the choice was resolved
  - docs/build-plans/bp-052/journal.md           # the builder's recorded rationale
ftype: math
origin_plan: bp-052 (velocity-pair)
route: orchestrator
---

# dn-velocity-instruments §2.2(a) pins principal angles between two harmonic subspaces that live in DIFFERENT edge spaces after restriction — the note left the cross-space construction implicit; bp-052 resolved it by union-embedding

## What
Ratified `dn-velocity-instruments` §2.2(a) defines `RotationReport` as the principal angles
between `ker L₁(X_cite,n | common)` and `ker L₁(X_cite,n+1 | common)` at two commit anchors.
The two harmonic bases are computed on the complexes *restricted to the common node set at each
anchor* — but the restricted complexes at anchor *n* and anchor *n+1* do **not** in general share
the same edge set (the citation edges differ between the two commits even over identical nodes).
The note pins the angles as `θ_i` from the SVD of `Qₐᵀ Q_b` (§8) but does not say **which shared
ambient space** the two orthonormal bases `Qₐ`, `Q_b` are expressed in for that product to be
meaningful. As written it is a well-posed *quantity* with an under-specified *construction*.

## How bp-052 resolved it (in-scope, spec-fidelity)
The builder zero-embedded both harmonic bases into the **union edge space over the common nodes**
(the restricted complexes share a node ordering, so integer edge pairs are directly comparable;
zero-padding preserves orthonormality, so the SVD of `Qₐᵀ Q_b` still yields the cosines). This is
the standard construction for principal angles between subspaces of two different-but-embeddable
spaces, and it satisfies every pinned falsifier: identical snapshots ⇒ all angles ≈ 0; β₁ = 0 at
either anchor ⇒ empty report with `principal_angles == ()`; and the angles agree with an
independent `scipy.linalg.subspace_angles` path (`tests/unit/test_rotation_report.py`, 6 tests, green).

## Why it routes to design (not a builder-closable codebase item)
The builder made a defensible, falsifier-passing modeling choice, but it is a choice the *ratified
note left implicit* — so the note and the code now agree only by the builder's judgment, not by
the note's letter. Ratified notes are A8-immutable; the correct closure is an owner act: either
(a) errata `dn-velocity-instruments` §2.2(a)/§8 to name the union-edge-space embedding as the
definition, or (b) ratify the construction as-implemented by cross-reference. Until then the
instrument's meaning rests on `core/temporal_view.py`, not on the note.

## Recommendation
Batch with finding-0090 (a sibling ratified-note erratum from the same 2026-07-16 design pass) for
the next owner-facing design pass. No code change is implied — the implementation stands; this is a
note-vs-code reconciliation. Low urgency, non-blocking (bp-052 shipped green).

## Non-goals
Not re-opening any parked VI-a/VI-b/VI-c decision. Not a correctness defect — the geometry is the
standard one and the tests prove it. Purely a design-record fidelity gap.
