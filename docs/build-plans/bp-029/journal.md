# bp-029 journal

## 2026-07-13 — minted at graduation (orchestrator)

Born `proposed` from `/graduate dn-external-grounding` (ratified 2026-07-13). The EMBED
tail: flip transient→persisted — fetch open-access full text (Europe PMC / arXiv), chunk
+ embed into a **separate** curated vectorstore (`data/`, gitignored), mint/update the
`reference_material/` manifest to `source_ingestion.state: embedded`. §3 grounded against
the 2026-07-13 recon (citations inline: fetcher is abstract-only today,
`cloud/fetcher/sources.py:72/125/156`; chunk/embed reused unchanged; the curated store is
a second `VectorStore` instance at a new gitignored path; the network boundary is Inv 2 —
full-text fetch MUST stay in `cloud/fetcher/**`). The copyright/licence gate is the real
decision (§2.6): parked default-DENY (open-access only), with an `owner-questions.md`
degrade path for the allow-list. Items 27∥28 → 29 → 30. `depends_on: [bp-028]`; shares
`docs/reference_material/**` with bp-027 → sequenced after it (`parallelizable_with: []`).
Model estimate opus/450k (network + new store + licence judgment). The heaviest, most
invariant-touching of the three. Awaiting the owner-only `proposed → ready` blessing. No
work started.
