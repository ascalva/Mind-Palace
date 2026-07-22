"""Outer-ring residue of the store layer (dn-inner-outer-core §2.7, K1 / bp-090).

The two file-backed content stores (`rawstore` — the content-addressed immutable archive — and
`sourceset`, + the package's inner init text) moved to `core/kernel/stores/`. What remains here is
the outer half: the sqlite/duckdb/lancedb/pyarrow-backed stores — the austere persistence plumbing
the owner's v2 ruling (§2.1) placed in the outer ring beside the machinery that operates it
(`chatlog, derived, edges, runledger, catalog, causal_edges, chat_events, agent_observations,
authored_supersession, code_observations, observation_history, reference_edges, versions,
curated_store, telemetry, vectorstore, verdicts, staging, claim_ops`). This init is
stdlib-import-free so it stays inner by construction (a pure package marker); the residue submodules
beside it are the outer machinery.
"""
