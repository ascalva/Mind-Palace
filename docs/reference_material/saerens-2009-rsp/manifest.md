---
type: reference-material
id: saerens-2009-rsp
citation: "Saerens, M., Achbany, Y., Fouss, F., & Yen, L. (2009). Randomized Shortest-Path Problems: Two Related Models. Neural Computation, 21(8), 2363–2404."
identifiers:
  doi: 10.1162/neco.2009.11-07-643
  arxiv: null
  isbn: null
  url: https://direct.mit.edu/neco/article/21/8/2363/7442/Randomized-Shortest-Path-Problems-Two-Related
verification:
  state: verified
  date: 2026-07-13
  verdict: CONFIRMED
  by: "web-check 2026-07-13 (dn-core-query-protocol §1.3 item 6 literature pass)"
source_ingestion:
  state: not_fetched
  venue: null                 # Neural Computation 21(8); available via MIT Press Direct (doi 10.1162/neco.2009.11-07-643)
  store_ref: null
  retrieved: null
authority: high
load_bearing_for:
  - "docs/design-notes/core-query-protocol.md#2.2: the randomized shortest-path (RSP) / free-energy distance family K(β) that interpolates between mode 1a (hard shortest-path) and mode 1b (soft diffusion/resistance) as endpoints of a single β-deformation."
cited_by:
  - docs/design-notes/core-query-protocol.md
docs:
  - distillation.md
provenance: agent-proposed
---

# Saerens, Achbany, Fouss, Yen (2009) — Randomized Shortest-Path Problems

One of the two references (with Kivimäki–Shimbo–Saerens 2013) that ground the
`K(β)` free-energy family unifying modes 1a and 1b in `dn-core-query-protocol` §2.2. See
`distillation.md` for the load-bearing statement.
