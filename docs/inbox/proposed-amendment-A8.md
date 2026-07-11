# Proposed amendment A8 — status-aware design-note guard (paste-ready)

Warrant: **finding-0025** (+ the live evidence: bp-005's owner temp-lift `d6e518f→f5d435d`,
and the 2026-07-11 inbox-delivery workaround for `code-observation-projection`). The
orchestrator cannot edit `docs/design-notes/**` (that is the point); the three edits below
are the OWNER's paste into `docs/design-notes/agent-workflow.md`, then commit. bp-010
(proposed, delivered alongside) lands the mechanical consequence in `_lib.py` after your
`proposed → ready` blessing.

---

## Edit 1 — front-matter: add the warrant + the amendment id

In `links:` add:

```yaml
  - docs/findings/finding-0025.md (warrant, amendment A8)
```

In the `amendments:` list add:

```yaml
    A8 (finding-0025),
```

## Edit 2 — §16 Amendment log: append this entry

```markdown
- **A8** — warrant: finding-0025 (surfaced by the bp-005 denylist collision; live evidence:
  the owner temp-lift `d6e518f→f5d435d`, and orchestrator note-drafting forced through
  docs/inbox/ delivery, 2026-07-11). The foundation denylist guarded design notes by
  LOCATION (`docs/design-notes/**`), collapsing two distinct properties: agents must be
  able to author *draft* notes (the brainstorm → note → graduate flow is the
  orchestrator's purpose), and the *ratified* record must be tamper-proof to agents. A8
  redraws the guard on STATUS, the axis the rest of the system already runs on: a
  **draft** note (or a new note created at `status: draft`) is agent-writable under the
  normal write-scope rules; a **ratified or superseded** note is agent-immutable — content
  and status, Edit/Write and Bash alike. Enforcement is two-layer and laundering-proof:
  pre-hoc, `scope-guard` denies any write to a note whose ON-DISK status is
  ratified/superseded (the write has not happened yet, so on-disk is the committed
  truth); post-hoc, the Stop-gate audits every design-note change against the note's
  **HEAD** status (a Bash write has already mutated the working tree, so a
  ratified→draft laundering flip is caught by comparing against the committed status,
  the same HEAD-keyed mechanism §6(c) uses for blessing detection). `CONSTITUTION.md`,
  `eval/golden/**`, and `eval/golden.py` remain on the unconditional denylist;
  `gate-guard`'s transition denials (`→ratified`, `→ready`) are unchanged and compose
  with the new content rule. Net: the blessed record stays sacred; the working material
  becomes workable — task capability still never exceeds what §5 grants.
```

## Edit 3 — §5 hook-contract row (line ~135), scope-guard description

Replace the final sentence of the `scope-guard` row:

> A global foundation-file denylist applies beneath any plan, in every session,
> orchestrator included.

with:

> A global foundation-file denylist (`CONSTITUTION.md`, `eval/golden/**`,
> `eval/golden.py`) applies beneath any plan, in every session, orchestrator included.
> Design notes are guarded by STATUS, not location (A8): draft notes are agent-writable
> working material; ratified/superseded notes are agent-immutable, enforced pre-hoc on
> on-disk status and post-hoc against HEAD status (laundering-proof).

---

## After pasting

1. Commit (your authorship — it is a re-ratification):
   `git add docs/design-notes/agent-workflow.md && git commit -m "docs(design): ratify amendment A8 — status-aware design-note guard (warrant finding-0025)"`
2. Bless `docs/build-plans/bp-010/plan.md` → `status: ready` (your hand).
3. Optionally answer oq-0011 with: "RATIFIED as A8, <date>; bp-010 licensed" — or leave
   it and the orchestrator sweeps it against your commit at the next /triage.

The orchestrator then executes bp-010 (the `_lib.py` guard + six-case harness + CLAUDE.md
digest line), after which finding-0025 flips `→ promoted` and this file is deleted.
