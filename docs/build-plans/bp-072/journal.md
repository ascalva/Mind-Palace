# Journal — bp-072 (owner cockpit)

Contract: builder. Write scope: `scripts/cockpit.sh`, `scripts/docket.py`,
`scripts/readmap.py`, `scripts/palace.py`, `docs/supplemental/cockpit.md`, plus
`tests/unit/test_{docket,readmap,bless}.py`. Plan: `docs/build-plans/bp-072/plan.md`.

---

## Item 0 — ground the leans (2026-07-19, session-34; DONE)

Confirmed every §6 lean against the live tree before writing code:

- **Q8 — daemon log path (was unpinned).** `ops/lifecycle/com.mind-palace.palace.plist`
  StandardOut/StandardError → `data/logs/palace.out.log` and `data/logs/palace.err.log`
  (both exist live; `launcher.py:515` also names `data/logs/palace.err.log` in a hint).
  **Decision:** the ops window tails `data/logs/palace.out.log` (primary) — it exists
  whether or not the daemon is up, so the cockpit never depends on Ouroboros running (§9).

- **Q2 — front-matter helpers exist & work live.** `.claude/hooks/_lib.py` provides
  `parse_front_matter(text)`, `read_front_matter(path_abs)` (ABS path; `{}` on error),
  `status_of(path_rel)` (keys off `_lib.ROOT`), and `_normalize_status(v)` (cuts a
  trailing ` #` comment). **docket.py REUSES these** via a `sys.path` insertion of
  `.claude/hooks`, importing `read_front_matter` + `_normalize_status`, computing abs
  paths from its OWN repo root (not relying on `_lib.ROOT`). Never re-derives parsing.

- **Status values carry trailing comments.** Live design notes read e.g.
  `status: ratified               # draft → ratified …` — so docket MUST normalize:
  `_normalize_status` is the exact reused cut. Confirmed real `draft` notes exist
  (`alignment-subsystem`, `attestation-layer`, `authorship-distance-axis`, …).

- **Q3 — oq grammar.** `docs/inbox/owner-questions.md`: `## oq-NNNN — <title>`,
  `- status: open|answered|swept`, `- blocking: true|false`. No per-entry date field
  (id-order aging stands; parked §11).

- **Q4 — read map is prose.** `bp-073/journal.md:188` is `**Read map (concept-bearing
  lines…)**` prose — NO ```read-map fence anywhere. `readmap.py bp-073` must exit 1.

- **Q6 — tmux.** 3.7b at `/opt/homebrew/bin/tmux`; `focus-events` is a server option
  settable at runtime.

- **Q7 — docket home.** `.claude/state/.gitignore` = `*` except `!.gitignore` → any
  `.claude/state/docket.md` is already ignored. No `.gitignore` edit.

**Falsifier (a §6 lean contradicted by the tree, surviving unamended into 1–4):** none —
the only unpinned lean (Q8) is now pinned; all others held.

Next: Items 1/2/3 (mutually parallel, sequential in one session) → Item 4.

---

## Item 1 — docket.py + tests (2026-07-19, session-34; DONE)

`scripts/docket.py` — the derived view. `scan_docket(root)` recomputes from the tree
every call, no persisted state. Three sources → three actions; ready plans + answered/
swept oqs EXCLUDED. Sort classes: blocking-oq → proposed-plan → draft-note →
non-blocking-oq, oldest-first within class (plans/notes by `created:`, oqs by id).
CLI: bare → render; `--count` → one int; `--write` → `.claude/state/docket.md`.
DRY honored: imports `_lib._normalize_status` + `parse_front_matter` (sys.path insert of
`.claude/hooks`); computes abs paths off its OWN `ROOT` (`__file__`-derived), not
`_lib.ROOT`; never imports `core` (a static-AST test enforces both).

`tests/unit/test_docket.py` — 7 tests GREEN: exact owner-awaiting set (inclusions +
all four exclusion kinds); sort order `oq-0002(blocking), bp-101, bp-100, alpha,
oq-0001`; blocking action flag; `--count` prints exactly `5`; `--write` emits the
landing buffer; empty tree → "Inbox zero"; static-AST DRY/no-core falsifier.

Live smoke: `uv run scripts/docket.py` exits 0, 52 rows, lists known-open oq-0003 &
oq-0024. `--count` → 52. (No proposed plans right now — bp-072 is in-progress — so the
live board opens with draft notes; the sort classes are still proven on the fixture.)

**Falsifiers ruled out:** no persisted state (view is a pure function of the tree);
no agent-actionable row (exclusions tested); no re-derived parser / no `core` import
(AST-enforced).

---

## Item 2 — readmap.py + tests (2026-07-19, session-34; DONE)

`scripts/readmap.py` — finds the LAST ```read-map fence in a plan's `journal.md` and
prints its lines VERBATIM (authoring format IS output format → nothing transforms). No
block → exit 1 with the legacy-prose message; it NEVER parses prose. A listed path that
no longer exists → stderr warning, line still emitted. `_BLOCK` regex is DOTALL/multiline,
`findall`→`[-1]` for the current block.

`tests/unit/test_readmap.py` — 6 tests GREEN: two-block journal → LAST block only,
verbatim; no-block → exit 1 + "no structured read-map block"/"legacy prose seal";
missing path → warned once but kept, present path silent; missing journal → exit 1;
`extract_block` None without a fence; **live bp-073 → exit 1** (its seal is prose — Q4).

Live: `uv run scripts/readmap.py bp-073` → exit 1, honest message. ✓

**Falsifiers ruled out:** no transform between authored lines and output (verbatim,
tested); no prose-guessing (exit 1 on legacy, tested live on bp-073).

**Note:** the read-map format SPEC (Item 2's `cockpit.md` doc deliverable) is authored
together with the full `docs/supplemental/cockpit.md` in Item 4 — it is one file, written
once, not stubbed then rewritten.

---

## Item 3 — palace bless + tests (2026-07-19, session-34; DONE)

`scripts/palace.py` gains a `bless(plan_id)` fn + a dispatch arm at the TOP of `main()`,
BEFORE `seal()` and the launcher import (bless never touches the daemon). Guard order (LAW):
(1) `os.environ.get("CLAUDECODE")` → refuse BEFORE path resolution; (2) resolve, missing →
exit 2; (3) status must be EXACTLY `proposed` (leading `\S+` capture excludes a trailing
comment, so the compare is on the bare token; no force path); (4) line-targeted rewrite of
ONLY the `status:` value (proposed→ready) and the `updated:` date — `rest` (trailing comment)
preserved verbatim, NO YAML round-trip; (5) print. USAGE + module docstring updated in the
same edit (cross-reference-on-extension).

`tests/unit/test_bless.py` — 8 tests GREEN (tmp_path fixtures ONLY): flip lands + updated→
today; design_ref comment survives byte-identical; a trailing comment ON the status line
survives (`status: ready   # was minted 07-01`); ready/complete/missing → exit 2, file
untouched; **agent-session refusal fires BEFORE resolution** (fake id → agent message, not
"no such plan"); agent session flips nothing even with a real proposed plan present.

**LIVE demo (this build session, CLAUDECODE=1):** `uv run scripts/palace.py bless
bp-nonexistent` → the agent-session refusal, exit 2. `git status docs/build-plans/` shows
ONLY bp-072's own files (the session-start `/build` status flip + this journal) — bless
modified NOTHING. The blessing gate held.

**Falsifiers ruled out:** no real plan modified by bless (git-verified live); no force/
override flag exists (only proposed flips); launcher NOT imported on the bless path (dispatch
precedes the import). The two owner-only gates + Stop-gate audit are unchanged in behavior —
bless mints no capability; it is a keystroke wrapper over the hand edit, refused to agents.

---

## Item 4 — cockpit.sh + cockpit.md (2026-07-19, session-34; DONE)

`scripts/cockpit.sh` — idempotent tmux launcher. `run()` echoes-or-executes so `--dry-run`
prints every tmux command and runs none. `build()`: session `palace`, `desk` window
(pane .0 = `docket.py --write` then `nvim .claude/state/docket.md`; pane .1 = `claude`;
focus left on .0), `ops` window (`palace status` + `tail -F data/logs/palace.out.log` — Q8,
never needs the daemon up), `status-interval 60` + `status-right` awaiting-count hook,
`set -s focus-events on` (the ONLY server option). `join()` is `$TMUX`-aware: switch-client
inside, attach outside. `main()`: `has-session` → join (no rebuild) else build→join. ROOT
derived from `${BASH_SOURCE[0]}` so panes root at the repo from any cwd.

`bash -n scripts/cockpit.sh` clean; `--dry-run` prints the full §6 layout + both join
variants legibly (comment line names attach-outside / switch-inside), executes nothing.

`docs/supplemental/cockpit.md` — carries: the guide-not-gate rule VERBATIM from
`owner-cockpit.md:59-62`; nvim snippets (`autoread`+`checktime`, `<leader>pb`→`palace bless`,
`:PalaceRead`→readmap→`:cfile`/`]q`, render-markdown + diffview suggestions); the permanent
`set -g focus-events on` tmux line; session-switching tips (`prefix+s` choose-tree, `prefix+L`
last-session toggle); and the **read-map block format spec** (Item 2's doc deliverable —
`path:line: why`, last-block-wins, verbatim, legacy-prose-exits-1, checkpoint-skill cross-ref
noted as an orchestrator seal-time act). Cleaned a stray U+200B from the format example.

**Falsifiers ruled out:** writes no path outside the repo (only `.claude/state/docket.md`,
in-repo; no dotfile — those are proposals adopted by hand); does not require the daemon (log
tail + status both run daemon-down); sets no tmux server option but `focus-events`; a second
run joins, never mints a second session (`has-session` branch).

---

## All items DONE — ready for the Stop gate / seal handoff

Items 0–4 complete; per-item acceptance met with live smokes. Remaining to SEAL (orchestrator
acts, outside builder scope): run the full suite for the ratchet, clear `active-plan`, flip
plan status→complete + `cost.actual`, PROGRESS checkpoint, add the checkpoint-skill read-map
cross-ref (plan §4), author the FIRST structured ```read-map block for this seal, commit, push,
verify CI green. Budget probe at seal for `week_delta`.

---

### SEAL (2026-07-19, session-34) — bp-072 COMPLETE. Orchestrator, autonomous (clean papercut).

All five deliverables landed; +21 new tests GREEN. The CI green gate reproduced locally —
`pytest -m 'not live and not podman and not needs_vault and not needs_restic' --deselect
test_core_self_containment::test_core_imports_nothing_outside_core` → **1648 passed, 4 skipped,
21 deselected**. The finding-0103 ratchet is unchanged at **19** (core untouched — every bp-072
file is a leaf script/doc/test; verified the count is non-increasing).

**Mid-build finding filed:** `finding-0114` (`direction`, routed to orchestrator) — the owner
observed `scripts/` has drifted into three drawers (durable entrypoints · spent migrations ·
eval-flavored harnesses); captured for a future tidy plan, NOT acted on (moving harnesses
touches `eval/`, outside scope). bp-072 unaffected — its 4 files are all durable entrypoints.

**cost.actual (measured by /usage delta, %-only — output-token count not directly observable):**
session 59%→63% (+4%); week all-models 22%→22% (Δ<1%, the gate figure); Fable untouched (opus
build, correct model discipline). A well-pinned papercut — the low session_delta confirms the
pinning held (no re-derivation, no design questions raised beyond the one owner-routed finding).

**This is the FIRST seal authored in the structured read-map block format** (the format this very
build specified in `docs/supplemental/cockpit.md`). `uv run scripts/readmap.py bp-072` will emit
it verbatim once committed:

```read-map
scripts/palace.py:59: bless() guard order — CLAUDECODE refusal BEFORE path resolution (the gate, proven by fake-id probe)
scripts/palace.py:101: the line-targeted status flip — preserves front-matter comments, never a YAML round-trip
scripts/docket.py:144: scan_docket — the derived owner-awaiting view, recomputed every run (a pure function of the tree ⇒ cannot drift)
scripts/docket.py:34: the DRY seam — imports _lib's front-matter parser, never re-derives one (AST-enforced)
scripts/readmap.py:37: last ```read-map block wins, emitted verbatim — the authoring format IS the output format
scripts/cockpit.sh:58: join() — $TMUX-aware switch-vs-attach, idempotent, never nests
tests/unit/test_bless.py:111: the falsifier worth reading — the guard fires BEFORE resolution (fake id, zero flip risk)
tests/unit/test_docket.py:120: the DRY / no-core falsifier, enforced by static AST inspection
docs/supplemental/cockpit.md:16: the guide-not-gate rule, verbatim from owner-cockpit.md — the trust surface named honestly
docs/supplemental/cockpit.md:88: the read-map block format spec (this very format)
```

Fresh-agent sufficient. bp-072 sealed.

**CI reconciliation (post-push).** The first push (05db00b) went red on `ratchet` + `type-gate`:
I had run pytest locally but NOT `ruff check` / `mypy` — the miss. Fixed with no behavior change:
ruff E501 line-length on 6 lines + E402 on palace.py (pycodestyle permits only `sys.path` calls —
not a `_ROOT=` assignment — before an import, so `_ROOT` now defines AFTER the `core.sealing`
import); mypy Tier-2 floor (typed `sort_key: tuple[int,str]`, `_status(fm: dict[str,object])`,
narrowed the `bm`/`m` match guards, `# type: ignore[import-not-found]` on the three dynamic
sys.path imports — specific codes, so the bare-ignore scan passes) and the `tests/` baseline held
at exactly 69. Local re-run of the full CI matrix GREEN: `ruff check .` clean · `mypy scripts` 0 ·
`mypy` 69 · `ops.type_gate` OK · import-firewall OK · pytest 1648p/4s/21deselected. Read-map anchors
above re-pinned to the shifted line numbers. Lesson: run ruff+mypy, not just pytest, before a seal.
