# mypy baseline — B-1 report-only audit (2026-07-11)

First strict run under `type-system-as-core-audit.md` (ratified 2026-07-11, warrant
finding-0026). Config: `[tool.mypy]` in `pyproject.toml` — Tier 1 (`core/`) strict
components; Tier 2 (everything measured to import core) at the interim floor
(`check_untyped_defs`); Tier 3 (`edge/`, `cloud/`) unchecked as recorded default.
**Report-only: no gate is wired** — that is B-2, after both tiers are green.

## V1a — Tier-2 membership (measured, not assumed)

Modules importing `core`, by package: tests 103 · scripts 14 · scheduler 6 · ops 5 ·
agents 2 · eval 1 · **edge 0 · cloud 0** — the inbound zone direction is empirically
clean (bears on finding-0014's asymmetry question: nothing in the networked zones
imports core at all today).

## V2 — stub availability

`duckdb` ships `py.typed`; `numpy`/`scipy` typed; `cryptography` typed.
**No stubs:** `lancedb`, `sknetwork`, `psutil` (+ `watchdog` if ever installed) —
interim `ignore_missing_imports` overrides recorded in config; §2.5 boundary
wrappers (one typed module per dependency) are the build's job.

## V3 — baseline measurement

`mypy 2.2.0` · 312 source files checked · **463 errors in 134 files.**

By tier: **core 193** · tests 223 · ops 27 · agents 9 · scheduler 8 · scripts ~3.

By kind (top): `arg-type` 138 · `attr-defined` 93 · `type-arg` 45 · `union-attr` 38 ·
`import-untyped` 31 · `no-any-return` 29 · `import-not-found` 25 · `operator` 15.

Core hotspots: `stores/vectorstore.py` 15 · `stores/telemetry.py` 8 · `sensing.py` 8 ·
`sandbox/runner.py` 8 · `complex/temporal.py` 8 · `ingest/index.py` 7.

**Falsifier check (§2.2 clause 3 / B-1):** T1+T2 ≠ 0 — 463 errors is strong signal,
not no-signal. The audit claim stands; triage into the §2.3 taxonomy (T1 real defect →
one finding each / T2 imprecise annotation / T3 checker noise) is the next builder pass.

## Not done here (deliberately)

Per-error §2.3 triage and T1 findings (builder-scale — graduate the ratified note);
boundary wrappers; B-2 gate wiring (needs green tiers first); B-3 static-shadow spike
(`Authored`/`Derived` tagging in `core/provenance.py`).
