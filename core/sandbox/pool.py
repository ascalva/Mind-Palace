"""Warm pool of ready sandboxes (BUILD-SPEC §11, §5).

Cold-starting a container per execution is slow, so we keep a small pool warm and reuse it.
Pool size **is** the concurrency cap — we never hold more sandboxes than the RAM ceiling
allows (Invariant 8). A container that overran its timeout is *discarded*, never reused (it
may be wedged); a healthy one is reset (its scratch tmpfs cleared) and returned to the pool.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.sandbox.policy import SandboxPolicy, image_for
from core.sandbox.runner import SandboxRunner
from core.sandbox.spec import Limits


class SandboxBusyError(RuntimeError):
    """All warm sandboxes are in use — the concurrency cap (Invariant 8) was reached."""


@dataclass
class WarmPool:
    runner: SandboxRunner
    policy: SandboxPolicy
    limits: Limits
    size: int = 1
    language: str = "python"            # the pool is warmed for one image
    _free: list[str] = field(default_factory=list)
    _in_use: set[str] = field(default_factory=set)

    @property
    def _image(self) -> str:
        return image_for(self.language, self.policy)

    def _warm_one(self) -> str:
        return self.runner.start(self.policy, self.limits, self._image)

    def prewarm(self) -> None:
        while len(self._free) + len(self._in_use) < self.size:
            self._free.append(self._warm_one())

    def acquire(self) -> str:
        if self._free:
            cid = self._free.pop()
        elif len(self._in_use) < self.size:
            cid = self._warm_one()       # lazily warm up to the cap
        else:
            raise SandboxBusyError(f"all {self.size} sandbox(es) in use")
        self._in_use.add(cid)
        return cid

    def release(self, container: str, *, healthy: bool = True) -> None:
        self._in_use.discard(container)
        if healthy:
            self.runner.reset(container)   # clear scratch; keep it warm
            self._free.append(container)
        else:
            self.runner.destroy(container)  # wedged/timed-out -> discard, don't reuse

    def shutdown(self) -> None:
        for cid in [*self._free, *self._in_use]:
            self.runner.destroy(cid)
        self._free.clear()
        self._in_use.clear()

    def stats(self) -> dict[str, int]:
        return {"free": len(self._free), "in_use": len(self._in_use), "size": self.size}
