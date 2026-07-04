# Ingest Identity, Deduplication, and Amendment

**Status:** DRAFT — pending codebase reconciliation and owner ratification
**Origin:** Design dialogue, July 2026
**Boundary:** Inbound channel — ingestion (structural layer). Governed by the
sacred-boundary principle (`the-sacred-boundary.md`): the ingestion point is
sacred, and sanctity here is achieved by dissolving the mutate-the-core
privilege, not by granting it.
**Reconciles with:** `recursive-strata.md` (supersession edges), the provenance-
migration `--apply` work, the dual-scale / group-by-digest reframing.

---

## 1. The separation that dissolves the append-only/dedup tension

The apparent conflict between append-only provenance and deduplication is an
artifact of conflating two objects at different layers:

- the **log of ingest events** — where the append-only invariant belongs;
- the **derived index that instruments read** — where it does **not** belong.

Once separated, the "extremely privileged permission to modify the authored
layer" is unnecessary. That permission was the dangerous capability; the right
structure removes it.

## 2. Authored layer = append-only log of events

The authored layer is an append-only log of *events*, not a mutable store of
*current beliefs*.

**Re-ingesting an unchanged note** is a second event with the same content-hash.
It is never deleted — "ingested twice" is historical truth and provenance must
record it faithfully. But document **identity** is a canonical object keyed by
content-hash; the second event references the existing identity rather than
minting a new one. One document, two occurrences.

This answers "did I re-ingest?": yes — recognized by hash, logged as an
occurrence, no new identity.

## 3. Derived index = content-addressed projection

The embedding index is a **derived projection** of the log — the same discipline
as MirrorView, one level down. It holds **one point per canonical chunk, keyed by
chunk-content-hash**, not one point per ingest event.

Exact re-ingestion therefore **coalesces on the way in**: it resolves to the
existing point and adds nothing. The false-density pathology — duplicated points
inflating a region and manufacturing false importance — cannot arise, because the
index is content-addressed rather than occurrence-addressed. The problem is
dissolved at the key, not repaired after the fact by deletion.

## 4. Modified note = versioned amendment

The modified-note case is a **versioned amendment**:

- stable document identity (source path or a stable doc-id, **not**
  content-hash);
- new content as a new **version**;
- the log records **supersession**: version *v2*, hash *H₂*, supersedes *v1*.

Provenance is **enhanced**, not destroyed: a full version history plus a
supersession edge is strictly more provenance than before.

An amendment is a **chunk-level diff**, not a wholesale re-embed:

- unchanged chunks (same chunk-hash across versions) keep their existing points
  and fingerprints — no re-embed;
- changed and new chunks get new points;
- removed chunks are marked superseded.

The stable parts of a frequently-edited note therefore never accumulate
duplicates.

## 5. No mutate-the-immutable operation exists

Corrections are **appends** (a supersession edge) **plus re-materialization** of
the derived view. The privilege required is the ordinary append privilege plus
view-rebuild — **not** a special capability to reach into and alter the authored
layer. The scary permission was never needed; this is the capability-dissolution
test passing for the ingestion boundary.

## 6. Two views over one log

- The reasoning complex reads the **active projection**: current versions,
  deduplicated by chunk-identity, so diffusion, SBM, and curvature see clean
  density and never the double-ingested log.
- Provenance queries read the **full historical log**.
- The Dreamer's MirrorView is content-deduplicated and version-current by
  construction; the auditor sees complete history.

The math is protected without lying about history.

## 7. The dedup boundary rule (it inverts — get this right)

Coalesce by **content identity** (same bytes = one fact = one point). **Do not**
coalesce by **semantic proximity.**

Two distinct authored artifacts that happen to agree are **corroboration** —
independent provenance asserting the same claim is evidentiary weight the system
*should* feel. Collapsing them by embedding-distance would erase it. The "false
sense of importance" worry is correct for *occurrences of a single artifact* and
wrong for *agreement between distinct artifacts*.

> **Rule: dedup exactly at authored-artifact identity, never by proximity.**
> Two occurrences of one note inflate density spuriously → coalesce.
> Two notes that agree inflate it correctly → keep both.

## 8. Open question (requires reading the code)

- **Q1.** Does the librarian key the derived embedding index by
  **chunk-content-hash** or by **ingest occurrence**? Cite the schema and the
  write path (`path:line`). State plainly whether the §3 content-addressed-
  projection model is already satisfied, partially satisfied, or absent. This is
  the single place the current code either already gives this model or quietly
  does not, and it touches stored data, so it must be resolved before any corpus
  work and coordinated with provenance migration `--apply`.

## 9. Reconciliation

Consistent with the append-only-log / derived-index separation and the
versioned-amendment direction already in the project's learnings, and with the
supersession edges in `recursive-strata.md`. The builder should locate the
existing passages this extends and propose a cross-reference (or a partially-
superseded banner if any existing text conflicts), per repository discipline.
