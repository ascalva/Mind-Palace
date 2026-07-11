"""Typed facade over `psutil` (type-system-as-core-audit.md §2.5 boundary wrapper).

psutil ships no `py.typed` (V2, 2026-07-11). This module is the ONE place core
touches the raw package; the vitals path reads system measurements through these
typed functions only. Local measurement only — no network (Invariant 2).
"""

from __future__ import annotations

from dataclasses import dataclass

import psutil  # type: ignore[import-untyped]  # warrant: no py.typed upstream (V2); Any quarantined to this shim


@dataclass(frozen=True)
class VirtualMemory:
    """The fields of `psutil.virtual_memory()` the vitals emitter reads."""

    total: int  # bytes
    available: int  # bytes
    percent: float  # 0..100


def virtual_memory() -> VirtualMemory:
    vm = psutil.virtual_memory()
    return VirtualMemory(
        total=int(vm.total), available=int(vm.available), percent=float(vm.percent)
    )


def process_rss(pid: int) -> int:
    """Resident-set size of `pid`, in bytes."""
    return int(psutil.Process(pid).memory_info().rss)


def cpu_percent() -> float:
    """System-wide CPU percent since the previous call (non-blocking: interval=None)."""
    return float(psutil.cpu_percent(interval=None))


def loadavg_1m() -> float | None:
    """1-minute load average, or None on a platform without `getloadavg`."""
    if not hasattr(psutil, "getloadavg"):
        return None
    return float(psutil.getloadavg()[0])
