"""System-vitals emitter (BUILD-SPEC §8, §9 reactive tier).

"The system is itself a sensor source." At launch this is system vitals only — memory
headroom, CPU, load, process RSS — written into the DuckDB telemetry store. Queue depth,
model-load time, error rates, and cron durations join as those subsystems come online
(Phases 3+). Body/health sensors are a deferred, dormant adapter (§20.6).

This is deterministic measurement, not a model (the reactive tier escalates to a model
only when a threshold is crossed — that logic arrives with the scheduler in Phase 3).
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import psutil

from core.stores.telemetry import TelemetryWriter

_GB = 1024 ** 3


@dataclass(frozen=True)
class Reading:
    metric: str
    value: float
    unit: str
    labels: dict | None = None


def collect_system_vitals() -> list[Reading]:
    vm = psutil.virtual_memory()
    proc = psutil.Process(os.getpid())
    readings = [
        Reading("mem.total_gb", vm.total / _GB, "GB"),
        Reading("mem.available_gb", vm.available / _GB, "GB"),  # headroom vs model budget
        Reading("mem.used_pct", vm.percent, "%"),
        Reading("cpu.percent", psutil.cpu_percent(interval=None), "%"),
        Reading("proc.rss_gb", proc.memory_info().rss / _GB, "GB"),
    ]
    if hasattr(psutil, "getloadavg"):
        readings.append(Reading("load.1m", psutil.getloadavg()[0], "procs"))
    return readings


@dataclass
class VitalsCollector:
    writer: TelemetryWriter
    source: str = "vitals"

    def collect_once(self) -> list[Reading]:
        """Sample current system vitals and write them to telemetry. Returns the
        readings written (so callers can verify the path end to end)."""
        readings = collect_system_vitals()
        self.writer.record_vitals(readings, source=self.source)
        return readings
