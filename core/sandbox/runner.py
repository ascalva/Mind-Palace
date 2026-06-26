"""Sandbox runners — the thing that actually executes isolated code (BUILD-SPEC §11).

`PodmanRunner` is the default substrate (rootless Podman). `WasmRunner` is the seam for the
pure-compute wasmtime+Pyodide path (the §11 upgrade option); it is declared but not built in
Phase 4. The runner shells out to `podman` — that is deterministic *code* acting, never a
model holding a shell (Invariant 3); the executed code itself is powerless (Invariant 4),
which is enforced structurally by the argv in `policy.py`.

The wall-clock timeout is enforced here via the subprocess timeout; a container that overran
is force-removed (and, if pooled, discarded rather than reused).
"""

from __future__ import annotations

import shutil
import subprocess
import time
from dataclasses import dataclass
from typing import Protocol
from uuid import uuid4

from core.sandbox.policy import (
    SandboxPolicy,
    build_run_argv,
    build_warm_argv,
    runtime_for,
)
from core.sandbox.spec import MAX_OUTPUT_BYTES, ExecResult, ExecSpec, Limits


def _truncate(text: str) -> tuple[str, bool]:
    raw = text or ""
    if len(raw.encode("utf-8")) <= MAX_OUTPUT_BYTES:
        return raw, False
    return raw.encode("utf-8")[:MAX_OUTPUT_BYTES].decode("utf-8", "replace"), True


class SandboxRunner(Protocol):
    def available(self) -> bool: ...
    def run_once(self, spec: ExecSpec, policy: SandboxPolicy) -> ExecResult: ...
    def start(self, policy: SandboxPolicy, limits: Limits, image: str) -> str: ...
    def exec_in(self, container: str, spec: ExecSpec) -> ExecResult: ...
    def reset(self, container: str) -> None: ...
    def destroy(self, container: str) -> None: ...


@dataclass
class PodmanRunner:
    binary: str = "podman"

    def available(self) -> bool:
        """Usable, not merely installed: the binary must exist AND the (rootless) Podman
        service must answer. On macOS `podman` can be on PATH while the machine is stopped."""
        if shutil.which(self.binary) is None:
            return False
        try:
            return subprocess.run([self.binary, "info"], capture_output=True,
                                  text=True, timeout=10).returncode == 0
        except (OSError, subprocess.SubprocessError):
            return False

    def _exec(self, argv: list[str], *, input_text: str, timeout_s: int,
              on_timeout=None) -> ExecResult:
        t0 = time.monotonic()
        try:
            proc = subprocess.run(argv, input=input_text, capture_output=True,
                                  text=True, timeout=timeout_s)
        except subprocess.TimeoutExpired as e:
            if on_timeout is not None:
                on_timeout()
            out, _ = _truncate(e.stdout or "" if isinstance(e.stdout, str) else "")
            return ExecResult(stdout=out, stderr="wall-clock timeout", exit_code=-1,
                              timed_out=True, duration_s=time.monotonic() - t0)
        out, tr = _truncate(proc.stdout)
        err, _ = _truncate(proc.stderr)
        return ExecResult(stdout=out, stderr=err, exit_code=proc.returncode,
                          timed_out=False, duration_s=time.monotonic() - t0, truncated=tr)

    def run_once(self, spec: ExecSpec, policy: SandboxPolicy) -> ExecResult:
        name = f"mp-sbx-{uuid4().hex[:12]}"
        argv = build_run_argv(spec, policy, name=name)
        return self._exec(argv, input_text=spec.code, timeout_s=spec.timeout_s,
                          on_timeout=lambda: self.destroy(name))

    def start(self, policy: SandboxPolicy, limits: Limits, image: str) -> str:
        name = f"mp-sbx-{uuid4().hex[:12]}"
        argv = build_warm_argv(policy, name=name, image=image, limits=limits)
        subprocess.run(argv, capture_output=True, text=True, timeout=60, check=True)
        return name

    def exec_in(self, container: str, spec: ExecSpec) -> ExecResult:
        _, cmd = runtime_for(spec.language)
        argv = [self.binary, "exec", "-i"]
        for k, v in spec.env.items():
            argv += ["--env", f"{k}={v}"]
        argv += [container, *cmd]
        return self._exec(argv, input_text=spec.code, timeout_s=spec.timeout_s)

    def reset(self, container: str) -> None:
        subprocess.run([self.binary, "exec", container, "sh", "-c",
                        "rm -rf /tmp/* 2>/dev/null || true"],
                       capture_output=True, text=True, timeout=30)

    def destroy(self, container: str) -> None:
        subprocess.run([self.binary, "rm", "-f", container],
                       capture_output=True, text=True, timeout=30)


@dataclass
class WasmRunner:
    """Seam for the pure-compute path (wasmtime + Pyodide, §11) — strongest isolation, no
    syscalls. Declared now so the broker can target it later; not implemented in Phase 4."""

    def available(self) -> bool:
        return False

    def _unbuilt(self) -> ExecResult:
        raise NotImplementedError(
            "WASM (wasmtime+Pyodide) pure-compute sandbox is a planned §11 upgrade path; "
            "Phase 4 ships the Podman substrate"
        )

    def run_once(self, spec: ExecSpec, policy: SandboxPolicy) -> ExecResult:
        return self._unbuilt()

    def start(self, policy: SandboxPolicy, limits: Limits, image: str) -> str:
        raise NotImplementedError("WASM runner not built in Phase 4")

    def exec_in(self, container: str, spec: ExecSpec) -> ExecResult:
        return self._unbuilt()

    def reset(self, container: str) -> None: ...

    def destroy(self, container: str) -> None: ...


def build_runner(runtime: str, *, binary: str = "podman") -> SandboxRunner:
    if runtime == "podman":
        return PodmanRunner(binary=binary)
    if runtime == "wasm":
        return WasmRunner()
    raise ValueError(f"unknown sandbox runtime {runtime!r}")
