# Owner questions

The one file the owner answers. Orchestrator-maintained (`/triage` batches
routed `design | math | direction` findings here; never dripped). Each entry
carries a `default_if_unanswered` with a **park condition**, so an unanswered
question degrades to a parked item with a re-entry — never a stalled builder (§10).

To answer: edit the entry's `answer:` line and flip `status: open → answered`.
`/triage` then sweeps the answer back to its origin artifact and marks it `swept`.

Entry shape: `status`, `origin`, `blocking` (bool), `question`, `default_if_unanswered`
(with park), `answer`.

---

## oq-0001 — Should CLAUDE.md re-home any of the pre-BP-000 domain digest?
- status: open
- origin: docs/findings/finding-0001.md
- blocking: false
- question: BP-000 replaced the pre-BP-000 CLAUDE.md (mind-palace operating rules)
  with the persona-neutral workflow constitution, keeping only a pointer to the
  domain layer (`CONSTITUTION.md` / `BUILD-SPEC.md` / `CONVENTIONS.md`). Dropped
  from the auto-loaded surface: the 12-item non-negotiables digest, the repo map,
  the "current phase" marker, and the live-verification directive. All remain in
  `BUILD-SPEC.md` / `CONVENTIONS.md` / git history. Do you want any of that digest
  re-homed into the constitution (which costs tokens every turn), or is the
  pointer sufficient?
- default_if_unanswered: pointer-only stands (workflow constitution stays lean per
  §5). Parks as finding-0001; re-entry — owner answers here, or a `direction`
  finding reports a session missing dropped context.
- answer:

---
