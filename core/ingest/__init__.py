"""Outer-ring residue of ingest (dn-inner-outer-core §2.7, K1 / bp-090).

The pure text-projection machinery (`amend, chunk, logseq, pipeline, verify` + the package's inner
init text) moved to `core/kernel/ingest/`. What remains here is the outer half — the modules whose
closure leaves the admissible base: `embed` (the embedding path via the model client), `watch`
(watchdog), and the `curated`/`dialogue`/`founding`/`index`/`mint_ids`/`purge`/`run`/`sync` runners.
This init is stdlib-import-free so it stays inner by construction (a pure package marker); the
residue submodules beside it are the outer machinery.
"""
