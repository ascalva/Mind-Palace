"""Zone A — the sealed core (BUILD-SPEC §6).

Holds the private vault, the vector/telemetry stores, the private-reasoning models,
and the introspection/agent logic. **No outbound network.** Communicates outward only
by writing sanitized job specs into a handoff directory and reading results back.

Structural enforcement: the core runtime (`core.runtime.bootstrap`) installs a
fail-closed egress guard at startup (`core.sealing`) that permits only loopback
sockets — the local Ollama model-server channel — and raises on any attempt to reach
an external host. Nothing in this package may import a module whose purpose is to
reach the network; an accidental network-capable import in `core/` is a build-breaking
defect (CONVENTIONS). Network-facing code lives in `edge/` (Zone B).

Importing this package has no side effects — sealing is an explicit runtime step, not
an import-time surprise.
"""
