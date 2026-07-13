---
type: reference-material
id: alamgir-vonluxburg-2011-p-resistances
citation: "Alamgir, M., & von Luxburg, U. (2011). Phase transition in the family of p-resistances. Advances in Neural Information Processing Systems (NIPS) 24."
identifiers:
  doi: null
  arxiv: null
  isbn: null
  url: https://papers.nips.cc/paper_files/paper/2011/hash/9dc0e63f7cae4060c66a1c59103da6d8-Abstract.html
verification:
  state: verified
  date: 2026-07-13
  verdict: PARTIAL
  by: "web-check 2026-07-13 (dn-core-query-protocol §1.3 item 6 literature pass)"
source_ingestion:
  state: not_fetched
  venue: null                 # NIPS 2011 proceedings; available via papers.nips.cc / NeurIPS proceedings archive
  store_ref: null
  retrieved: null
authority: high
load_bearing_for:
  - "docs/design-notes/core-query-protocol.md#2.2: the p-resistance family spans shortest-path (p=1) → resistance (p=2) → cut/connectivity (p→∞) — NOT resistance at the high-p end, correcting the original attribution."
cited_by:
  - docs/design-notes/core-query-protocol.md
docs:
  - distillation.md
provenance: agent-proposed
---

# Alamgir & von Luxburg (2011) — Phase Transition in the Family of p-Resistances

The citation the 2026-07-13 web pass flagged **PARTIAL**: the p-resistance family's
high-`p` endpoint is **cut/connectivity**, not "resistance" — see `distillation.md` for the
recorded correction.
