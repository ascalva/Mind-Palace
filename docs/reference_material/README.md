# `docs/reference_material/` — the curated literature layer (filesystem form)

**Status: v0, PROVISIONAL.** This directory gives the *curated (objective) strata* a filesystem
home so a vetted external reference has an easy path into the corpus. The design is captured in
`docs/brainstorms/external-grounding.md` (the 2026-07-13 arc). The manifest schema below is v0 — the
`dn-core-query-protocol` **fable-vet (gated Jul 17)** owns the reference *kind* vocabulary, the edge
verification-state, and the authority field, and may revise it. Nothing here is yet **kind-tagged**
in the reference graph; until the vet + its additive migration, these files ingest as ordinary
corpus (semantically searchable, not yet distinguished as a `reference` kind).

## What this is (and is NOT)

Each **reference** is a subdirectory holding **one or many docs** — our vetted *distillation* of the
load-bearing result, fair-use excerpts, figures — plus a **`manifest.md`** encoding the metadata.
A reference is a bundle (a paper + its appendix + our extraction; a textbook + notes on the
chapters we actually use), which is why it is a directory, not a single file.

**Two planes — "not git-tracked" ≠ "not ingested" (they are separate decisions).**

- **In git (here):** the manifest + our **distillation** + fair-use excerpts. Lightweight, portable,
  shareable — what we *know* we use (the load-bearing claim). Committing raw paywalled PDFs is
  legally fraught and bloats the repo, so they are **not git-tracked**.
- **In the local embedding store (`data/`, gitignored):** the **full source text**, fetched from the
  searchable venue (arXiv / Scholar / Nature / …) and embedded into the reference corpus. This is
  **ingested** — it is the pattern-finding substrate: embedding the *whole* source lets the system
  surface connections we did not manually distill. It is **not git-tracked** (bloat + copyright), but
  it *is* part of the live corpus. The `manifest.md` is the **join**: it records the identifier (how
  to fetch), points at the git distillation, and references the locally-ingested full text.
- **Objective only.** These are ground truth *about the world*, never *about the owner* — never mirror
  /private/interaction content (a different stratum, behind the firewall).
- **Invariants.** The full text enters the *local* corpus exactly as vault content does — never git,
  never egress; the sealed core reasons over it offline (Inv 11). Fetching a source is a network act →
  an `edge/` operation (Inv 2) or an owner action at curation time; the sealed core never fetches.
  Local private ingestion for the owner's own pattern-finding is a different act from redistribution
  — which is *why* the distillation is portable (it is ours) and the source stays local (it is not).

## Layout

```
docs/reference_material/
  README.md                         # this file
  <ref-slug>/                       # one subdir per reference (e.g. moore-aronszajn-1950)
    manifest.md                     # the typed metadata node (front-matter below)
    distillation.md                 # our extraction of the load-bearing result
    <other docs…>                   # excerpts, figures, notes — one or many
```

## `manifest.md` front-matter schema (v0)

```yaml
type: reference-material
id: <ref-slug>                      # kebab, e.g. moore-aronszajn-1950
citation: "<full citation string>"
identifiers:                        # any that apply; null others
  doi: <doi or null>
  arxiv: <id or null>
  isbn: <isbn or null>
  url: <stable url or null>
verification:                       # about the CLAIM — is the source real + does it say what we cite?
  state: verified                   # asserted | verified
  date: <YYYY-MM-DD>
  verdict: CONFIRMED                # CONFIRMED | PARTIAL | REFUTED | UNCERTAIN
  by: <how — e.g. web-check 2026-07-13>
source_ingestion:                   # about the FULL TEXT — is it fetched + embedded in the LOCAL store?
  state: not_fetched                # not_fetched | fetched | embedded
  venue: <arxiv | scholar | nature | … | null>
  store_ref: <local store id / content hash, or null>   # never git; the join to data/
  retrieved: <YYYY-MM-DD or null>
authority: high                     # domain-vetted rank; maps to w(d,a,c)'s `a` (fable-vet finalizes)
load_bearing_for:                   # which corpus claim(s) this grounds
  - "<path#section>: <the claim>"
cited_by:                           # back-links into our corpus (φ_doc extracts these as edges)
  - <path>
docs:                               # the material files in this subdir
  - distillation.md
provenance: owner-curated           # owner-curated | agent-proposed
```

**Three separable states of a reference** (do not conflate them):

- **VERIFIED** (`verification.state`) — the source is confirmed to exist and to say what we cite it
  for (e.g. the 2026-07-13 web pass). About the *claim*. Precursor: `asserted` = a citation exists in
  our corpus with no subdir yet (a candidate).
- **DISTILLED** — this git subdir exists with our `distillation.md`. About *our summary*; portable.
- **EMBEDDED** (`source_ingestion.state`) — the full source text is fetched and embedded into the
  local reference corpus (`data/`, gitignored). About the *full text*; the pattern-finding substrate.
  Never git-tracked; `store_ref` is the join to `data/`.

A reference can be VERIFIED + DISTILLED without being EMBEDDED (as the seed set is initially), or all
three. Full-text acquisition (fetch → chunk → embed) is a curation-time pipeline with a network
(`edge/`) boundary and a licence gate — a substantive build, distinct from writing the manifest.
