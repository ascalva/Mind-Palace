# BP-007 — Build journal

Alive while the plan is `in-progress`; sealed by `/triage` on completion.
Fresh-agent test (§9): a session given only `plan.md` + this journal + the
write-scope files must continue without re-asking anything already answered.

---

## Entry — 2026-07-11 — start: plan flipped `ready → in-progress`; Item 5 measurement + floor decision

**Status.** Plan flipped to `in-progress` (legal builder transition). Building in worktree
`.claude/worktrees/agent-a7311e30e485c40ab` on branch `worktree-agent-a7311e30e485c40ab`
(own worktree per delegation contract; never merging to main).

**Item 5 — re-measure (post-bp-006).** `uv run --extra dev mypy` (current config, unchanged):
**296 errors in 83 files** (322 source files checked). By Tier-2 package (grep on path
prefix, matches plan's rough expectations closely):

| package   | plan's rough estimate | measured 2026-07-11 |
|-----------|------------------------|----------------------|
| tests     | ~221                   | 221                  |
| ops       | ~42                    | 43                   |
| agents    | ~16                    | 16                   |
| scheduler | ~10                    | 10                   |
| scripts   | ~6                     | 0                    |
| eval      | (unlisted)             | 0                    |

**Unplanned discovery: `edge`/`config` leak into the run.** `edge` (9 errors) and `config`
(4 errors) are NOT in `[tool.mypy].files` and are Tier-3 by the note's own V1a measurement
(zero core imports, confirmed again by grep here) — but mypy follows imports transitively
from files that ARE in the list (`ops`, `agents`, `scheduler`, `scripts` all `import config`;
`scheduler/interface.py` and `scripts/monitor.py` `import edge`), so their errors surface in
the run anyway. This is a **codebase/spec-fidelity** finding, self-resolved (not routed): the
fix is a `pyproject.toml` per-module override — `[[tool.mypy.overrides]] module = ["edge.*",
"config.*"]` / `follow_imports = "silent"` — which keeps them out of error-reporting (Tier-3,
recorded default, per §2.5) while core/Tier-2 modules that reference their types still get
checked normally. Verified: 296 → 283 with the override added, 322 source files still checked
(nothing silently excluded from analysis, only from **error reporting** on Tier-3 paths).
`config/**` was never in write_scope to begin with (edge/cloud are the plan's named
out-of-scope; config weren't discussed — the override is the only lever available, since
editing those files is out of scope regardless). Recorded here, not filed as a separate
finding — self-resolved per the routing rule (mechanical, no design judgment involved).

**Floor decision — `disallow_any_generics`: ADOPTED.** Measured the delta by adding
`disallow_any_generics = true` to the global `[tool.mypy]` block (test config, not yet
committed): 296 → 364, **delta = +68**, all 68 are `type-arg` (bare generic containers:
`dict`, `list`, `CompletedProcess`, `Sequence`, `set`, `Counter` missing type params). Split
by writability: **54 in write_scope** (ops 31, tests 22, eval 1) vs **14 out of scope**
(edge 13, config 1 — fully absorbed by the `follow_imports=silent` override above, confirmed
by combined test run: 364 → 337 with both changes applied).

**Falsifier check (plan Item 5, verbatim): "the stricter floor adds only T3 friction (zero
T1/T2 in the delta) — record and stay at the base floor."** NOT tripped: all 54 in-scope
delta errors are T2 (representability — real shape info the type system currently can't see:
untyped dicts crossing signatures, `subprocess.CompletedProcess` left ungenerified, an
untyped `Counter`/`Sequence`/`set`). Zero T1 in the delta (no behavior-changing defect
detected merely by adding the flag). This is genuine T2 signal, mechanically cheap to close
(same `dict[str, Any]` / concrete-type-param convention bp-006 already established) — **floor
raised to `check_untyped_defs` + `disallow_any_generics`**, recorded in `pyproject.toml` with
today's date and this reasoning inline.

**Decision, made explicit for Items 6–7:** fix the 54 in-scope `type-arg` sites as part of the
same sweep (they are now baseline errors under the adopted floor, not a separate pass) —
`dict[str, Any]` for open payloads per bp-006's convention, concrete element/value types
(e.g. `CompletedProcess[str]`, `dict[str, int]`) where the call site makes the shape obvious
without guessing.

**Acceptance evidence (Item 5):** journal table above; `pyproject.toml` floor comment to be
updated in the same commit as the override (next action).

**Next action:** commit the `pyproject.toml` floor + edge/config override change first (small,
isolated, config-only), re-measure the true post-floor baseline for Items 6–7, then start
Item 6 (ops/scheduler/agents/scripts/eval) package by package, smallest first.

---

## Markers
