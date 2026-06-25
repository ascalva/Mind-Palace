"""Zone A — scoped store access layers (BUILD-SPEC §8, CONVENTIONS).

Polyglot persistence, each store independently replaceable, with access scoped IN CODE
(not by convention): a handle exposes exactly the reads/writes a role needs and nothing
more. Present now: the DuckDB telemetry store. LanceDB (thought-graph vectors) lands in
Phase 1; SQLite (queue/state/gate) in Phase 3.
"""
