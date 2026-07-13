---
type: reference-material
id: moore-aronszajn-1950
citation: "Aronszajn, N. (1950). Theory of Reproducing Kernels. Transactions of the American Mathematical Society, 68(3), 337–404."
identifiers:
  doi: 10.2307/1990404
  arxiv: null
  isbn: null
  url: https://www.ams.org/journals/tran/1950-068-03/S0002-9947-1950-0051437-7/
verification:
  state: verified
  date: 2026-07-13
  verdict: CONFIRMED
  by: web-check 2026-07-13 (dn-core-query-protocol §1.3 item 6 literature pass)
source_ingestion:
  state: not_fetched          # VERIFIED + DISTILLED, not yet EMBEDDED — full paper not fetched into data/ yet
  venue: null                 # Trans. AMS 68(3); available via ams.org / JSTOR (doi 10.2307/1990404)
  store_ref: null
  retrieved: null
authority: high
load_bearing_for:
  - "docs/design-notes/core-query-protocol.md#2.2: every PSD kernel is some embedding's Gram (an inner product in a Hilbert space) — the 'Moore–Aronszajn inversion' that makes mode 2 the generic point of the PSD-kernel cone."
cited_by:
  - docs/design-notes/core-query-protocol.md
  - docs/brainstorms/core-query-protocol.md
  - docs/brainstorms/external-grounding.md
docs:
  - distillation.md
provenance: owner-curated
---

# Moore–Aronszajn (1950) — Theory of Reproducing Kernels

The first resident of the curated layer, and a dogfood: this reference was ingested *because* the
2026-07-13 literature pass found `dn-core-query-protocol` §2.2 had misattributed the general
"PSD kernel = inner product" fact to **Mercer**. It is **Moore–Aronszajn**. The note was corrected
inline; this card is the durable, verified record of the correct attribution. See `distillation.md`
for the load-bearing statement and the Mercer-vs-Moore–Aronszajn distinction.
