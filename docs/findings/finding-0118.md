---
type: finding
id: finding-0118
status: resolved
created: 2026-07-20
updated: 2026-07-20
links:
  - scripts/exhaust_report.py                       # the writer that failed at the CLI
  - scripts/verify_attestation.py                   # the sibling with the correct idiom (line 18)
  - docs/build-plans/bp-075/plan.md                 # the sealed plan that shipped it
re_entry: null
ftype: spec-fidelity
origin_plan: bp-075
route: orchestrator
resolution: >
  Hotfixed in place (orchestrator, 2026-07-20): added
  `sys.path.insert(0, str(Path(__file__).resolve().parent.parent))` before the
  `from config.loader import get_config` import (+ `# noqa: E402`), matching
  scripts/verify_attestation.py:18 — the idiom bp-075 §6 named as the precedent.
  Verified end-to-end: `uv run scripts/exhaust_report.py …` now places a report
  and the overwrite guard fires. Ruff green.
---

# bp-075's `exhaust_report.py` was not runnable as a CLI — missing `sys.path` bootstrap; the CLI path was never exercised

## What
Surfaced at FIRST REAL USE (the owner: "materialize the exhaust now — this is the design"):
`uv run scripts/exhaust_report.py <html> --plan … --slug …` failed with
`ModuleNotFoundError: No module named 'config'`. Running a script BY PATH puts the script's own
directory (`scripts/`) on `sys.path[0]`, not the repo root — so `from config.loader import
get_config` (line 30) could not resolve. The sibling `scripts/verify_attestation.py:18` does
`sys.path.insert(0, str(Path(__file__).resolve().parent.parent))` before importing `config` —
the exact idiom bp-075 §6 cited as the precedent — and `exhaust_report.py` simply omitted it.

## Root cause — the acceptance tested the FUNCTION, not the CLI invocation
bp-075 Item 3's acceptance drove `place_report()`/`main()` **via import** (`tests/unit/
test_exhaust_report.py` does `sys.path.insert(0, REPO/"scripts")` then `import exhaust_report`),
and pytest itself runs from the repo root — so `config` was always importable in the test
context, masking the bug. The actual documented invocation (`uv run scripts/exhaust_report.py`)
was never run — not by the builder, and not by the orchestrator's gate re-run (which ran the
suite, not the CLI). This is precisely the gap the **verify** skill targets: exercise the change
end-to-end through its real entry point, not only its tests.

## Why it matters
- The writer is the whole point of the exhaust lane (bp-075) — it was shipped un-runnable and
  sealed `complete`, undetected through two green gates, because no one invoked the CLI.
- **Lesson (recorded):** a CLI/script deliverable's acceptance must include running the ACTUAL
  command form (`uv run scripts/<name>.py …`), not just importing its functions in a test. The
  green gate (ruff+mypy+pytest) does not cover "is the entry point runnable." Pin an end-to-end
  CLI invocation in the acceptance of any script plan.

## Resolution
Hotfixed as above (orchestrator, owner actively blocked). The lane materialized on the fixed
run: `~/.mind-palace/exhaust/reports/2026-07-20-bp-074-session-handoff-gate.html`. No behavior
change beyond making the import resolve; the test suite is unaffected (it never depended on the
missing line).
