---
name: book
description: Author the LaTeX design manual in docs/book/ — chapter map, voice, TikZ/notation conventions, citation scheme, snippet provenance, and sync semantics. Use under a scribe-contract plan.
---

# book — the design manual (scribe contract)

The book (`docs/book/`, LaTeX) is a **derived projection** of the ratified record
and the codebase — design notes remain authoritative for design, the repo for
implementation (§3). It is minted and maintained only under a `contract: scribe`
plan (via `/scribe` → `/build`), whose write scope is `docs/book/**`. The scribe
cannot edit a design note; `scope-guard` already guarantees it. This skill is the
depth; the book's scaffold and first edition are the first scribe plans through
the finished machinery (§12).

## Accuracy outranks everything

A beautiful sentence about a false mechanism is a **defect**, not prose. When
writing exposes a gap or contradiction in the design record — and it will;
explanation is an audit pass — **file a finding and route it** (`spec-defect` or
`discovery`). Do not "fix" design in exposition.

## Grounding & citation — assert nothing uncited

Every claim is checkable against a cited source:
- design → an **artifact id** (design-note / finding id);
- implementation → **code by path plus git ref** (`path@ref`).

Code snippets are included wherever they genuinely aid understanding; each is a
**copy** annotated `source: path@ref`, so drift is detectable rather than silent.
The sync acceptance re-verifies every snippet and citation against HEAD.

## Chapter map

Philosophy → architecture (the zones and their boundaries) → the mathematics (the
coboundary framing and its derived instruments get their canonical write-up here)
→ the intuition connecting them → a future-work chapter that reproduces **parked**
decisions verbatim with their re-entry conditions. Superseded material may be
retained as marked *design-evolution* remarks, warrant-linked — provenance as
pedagogy. Draft notes never enter the book.

## Conventions

- **Figures** are TikZ/pgfplots — text, diffable, versioned like everything else.
  No binary image assets.
- **Notation** is defined once in `notation.tex` and used everywhere; never
  redefine a symbol locally. Extend the registry, don't fork it.
- **Voice/register:** precise, unhurried, explanatory; the reader is the owner —
  a security-focused engineer — not a novice and not a marketing audience.

## Sync semantics

A scribe run ends by updating `docs/book/SYNC.md` (git ref + artifact ids
incorporated); the commit is the edition. Fixed acceptance on every sync plan:
whole-book review; every snippet and code citation re-verified against HEAD; clean
compile (latexmk or tectonic — record the default on the first run); zero
undefined references; sync marker updated. PDF publishing cadence is parked (§14):
source-only commits for now, PDF built locally.
