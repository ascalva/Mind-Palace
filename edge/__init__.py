"""Zone B — the networked edge (BUILD-SPEC §6).

The ONLY processes that touch the network: the research bridge and the interface
gateway. Each runs containerized with the private vault unmounted and no inbound
listeners beyond what its job requires. Edge code must never import the private vault
or the sealed core's internals — the boundary between core and edge is a filesystem
handoff, not shared memory or imports. The egress guard (`core.sealing`) is
deliberately NOT installed here: edge is allowed to reach the network. Built out in
Phases 6 (interface) and 8 (bridge).
"""
