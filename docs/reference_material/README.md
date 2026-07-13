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

- **Distillations and metadata live here — NOT raw copyrighted sources.** Committing paywalled PDFs
  is legally fraught and bloats the repo. The raw source stays external (linked by identifier); the
  local artifact is *our* extraction + the citation. Open-access material may be included where its
  licence permits.
- **Objective only.** These are ground truth *about the world*, never *about the owner* — a
  reference card must never contain mirror/private/interaction content (that is a different stratum,
  behind the firewall). Acquisition (reading the source) is an outside-core human act; the committed
  card is offline, and the sealed core reasons over it without egress (Invariant 11 holds).

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
verification:
  state: verified                   # asserted | verified | ingested
  date: <YYYY-MM-DD>
  verdict: CONFIRMED                # CONFIRMED | PARTIAL | REFUTED | UNCERTAIN
  by: <how — e.g. web-check 2026-07-13>
authority: high                     # domain-vetted rank; maps to w(d,a,c)'s `a` (fable-vet finalizes)
load_bearing_for:                   # which corpus claim(s) this grounds
  - "<path#section>: <the claim>"
cited_by:                           # back-links into our corpus (φ_doc extracts these as edges)
  - <path>
docs:                               # the material files in this subdir
  - distillation.md
provenance: owner-curated           # owner-curated | agent-proposed
```

**Verification states.** `asserted` — a citation exists in our corpus with no subdir yet (a
candidate). `verified` — the source is confirmed to exist and say what we claim (e.g. the
2026-07-13 web pass). `ingested` — this subdir exists with the distillation embedded; the reference
is a first-class corpus node. Creating the subdir *is* ingestion.
