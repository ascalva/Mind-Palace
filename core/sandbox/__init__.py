"""Zone A — sandboxed code execution: same power, no reach (BUILD-SPEC §11, Invariant 4).

Executed code runs in an ephemeral, network-off, vault-less, non-root, resource-limited
container (rootless Podman) and returns DATA, never actions. The isolation profile is built
into the podman argv in `policy.py` so it is verifiable by construction. A warm pool avoids
cold start; the broker is the thin facade agents call.
"""

from core.sandbox.broker import ExecutionBroker, build_broker
from core.sandbox.policy import RUNTIMES, SandboxPolicy, build_run_argv, build_warm_argv
from core.sandbox.pool import SandboxBusyError, WarmPool
from core.sandbox.runner import PodmanRunner, SandboxRunner, WasmRunner, build_runner
from core.sandbox.spec import ExecResult, ExecSpec, Limits, Network

__all__ = [
    "RUNTIMES",
    "ExecResult",
    "ExecSpec",
    "ExecutionBroker",
    "Limits",
    "Network",
    "PodmanRunner",
    "SandboxBusyError",
    "SandboxPolicy",
    "SandboxRunner",
    "WarmPool",
    "WasmRunner",
    "build_broker",
    "build_run_argv",
    "build_runner",
    "build_warm_argv",
]
