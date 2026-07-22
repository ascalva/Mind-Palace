# Deskchecks owed — the persistent inbox

> **The deskcheck analog of `docs/inbox/owner-questions.md`.** These are demonstrations the
> orchestrator OWES the owner to *close* a track. Like OQ and findings, this list is **surfaced
> every session (in the resume brief) and at every `/triage`, and kept raised until the owner
> acts** — a track is not closed until its deskcheck is approved. The full phase/track picture is
> the board (`docs/TRACKS.md`); this is the "what I owe you to close, right now" filter.
>
> Verdict: `PENDING` (owed, unsurfaced-resolved) · `DONE` (owner-approved → move the track to the
> board's Closed section) · `NEEDS-WORK` (owner found a gap → send-back + follow-up plan/finding).

## Owed now — from earlier "sealed" waves (independent of the new builds)

| # | track / item | what I'll demo (working, or true state) + the surprise to flag | verdict |
|---|---|---|---|
| 1 | **Sync/diac dreamers** (bp-079/080/081/082) | the sealed dispatch machinery + **that it is NOT wired** (`[dream_rnd] enabled=false`, no live entry, f-0141); the decision I need from you: **wire it live, or accept dormant-by-design** like effectors | PENDING |
| 2 | **Inner/outer M0+S1** (bp-083/089) | the live two-ring ratchet (INNER=37) green, the map, the enforcement working end-to-end — the one here that's genuinely demonstrable-working | PENDING |
| 3 | **Agentic loop AL-1/2/3** (bp-086/087/088) | the profile constructors + the zone lattice test + the `exhaust ⊂ dialogue` refinement + `origin(e)`; confirm each is delivered, not just sealed (wiring unverified) | PENDING |
| 4 | **Fiber geometry G-A** (bp-085) | the survey readings (M1–M8) with their honest nulls; the owed S-rows (M2/M4/M5/M8, re-run with embed headroom) | PENDING |
| 5 | **Track G effectors** (G1–G7) | confirm-only: the dormancy (tier NONE, f-0011) is still the intended state | PENDING |

## Owed on completion — the current build tracks

Every plan in the board's `build` phase (bp-090/091/092/093/094/095) enters this inbox at seal:
`build → audit → deskcheck`. The orchestrator adds the row and says "ready to deskcheck" when a
track reaches phase 6. None is closed by sealing.

## The surfacing obligation (why this file exists)

Q5 (the dreamers) fell through because "sealed" was treated as terminal and nothing kept the
owed deskcheck in front of the owner. This inbox is surfaced **every session + every triage**
and stays until the owner closes each — the same persistence as owner-questions and findings.
