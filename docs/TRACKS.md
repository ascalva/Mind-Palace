# The board — tracks × phases (the JIRA-like swim-lane board)

> The single place that answers, for every active item: **which track** it belongs to and
> **which phase** it is in. Swim lanes = tracks; the phase pipeline is the columns. The
> orchestrator owns this board and updates it every seal + `/triage`; the owner moves cards at
> the gates (ratify, bless, deskcheck-approve). A **track is CLOSED only when its deskcheck is
> owner-approved** — never self-closed.

## The phase pipeline (owner spec 2026-07-21) — and the model each phase requires

| # | phase | model | what happens | artifact |
|---|---|---|---|---|
| 1 | **brainstorm** | any (spur-of-moment) | capture an idea | `docs/brainstorms/` |
| 2 | **design-pass** | **FABLE (required)** | a true discussion → the design document; owner ratifies | `docs/design-notes/` (draft→ratified) |
| 3 | **graduate** | Fable or Opus (by size) | decompose a ratified note → build plan(s) | `docs/build-plans/` (proposed→ready) |
| 4 | **build** | the right model for the job (Opus/Sonnet/Haiku by verification complexity) | execute a build plan | journal + seal |
| 5 | **audit** | Opus or Fable | check it got built correctly to spec | finding / audit note |
| 6 | **deskcheck** | **Opus** | demo it to the owner (working, or its true state); **owner approves or sends it back to any earlier phase** | owner verdict |
| → | **CLOSED** | — | owner-approved; the track is complete | — |

**Cross-cutting item types (not linear phases — routed as before):** **OQ** (owner questions,
`docs/inbox/owner-questions.md`) · **findings** (`docs/findings/`; codebase/spec-fidelity →
builder, design/math/direction → orchestrator). Either can be raised in any phase.

## Active board (swim lanes = tracks)

| track | item | phase | model | next / gate |
|---|---|---|---|---|
| **Code-ingest** | bp-092 CI-1 — embed lane (code+docstrings+comments) | build · ready | opus | START; not concurrent w/ bp-090 |
| **Code-ingest** | bp-094 CI-3 — reference resolvers + inherits/calls | build · ready | opus | after bp-092 Item 1 |
| **Code-ingest** | bp-093 CI-2 — retrieval/geometry proof | build · ready | opus | after bp-092 |
| **Code-ingest** | bp-095 CI-4 — S↔F lens | build · ready | opus | after 092/093/094 + M-C4 informative |
| **Code-ingest** | integrator densification (f-0151) — *part of DoD* | design-pass · queued | **FABLE** | after the build tracks |
| **Inner/outer core** | K1 bp-090 — born-30 → `core/kernel/**` | build · ready | opus | FIRST; not concurrent w/ bp-092 |
| **Inner/outer core** | K3 bp-091 — the S1 seven | build · ready | opus | after K1 seals |
| **Inner/outer core** | M0+S1 ring enforcement (bp-083/089) | **deskcheck** · pending | opus | demo the live ratchet (INNER=37) |
| **Sync/diac dreamers** | bp-079/080/081/082 (D-0/D-1/H-0/H-1/H-2) | **deskcheck** · pending | opus | **wire-or-accept-dormant decision** (the Q5 track; built-not-wired, f-0141) |
| **Reference bookkeeper** | the async F-consistency agent (f-0145/0154) | design-pass · queued | **FABLE** | after builds; minting live, bookkeeper unbuilt |
| **Agentic loop** | AL-1/2/3 (bp-086/087/088) | **deskcheck** · pending | opus | demo delivery (wiring unverified) |
| **Fiber geometry** | G-A survey (bp-085) | **deskcheck** · pending | opus | demo readings; M2/M4/M5/M8 S-rows owed |
| **Track G / effectors** | G1–G7 (`e0bf1ad`) | dormant-by-design | — | deskcheck = confirm dormancy still intended (f-0011) |
| **Workflow / tooling** | deskcheck + this board, formalized (f-0153) | design-pass · queued | **FABLE** | after builds; makes this board enforced |

**Cross-cutting lanes:** OQ — 18 open (`docs/inbox/owner-questions.md`). Findings — 0142–0154
unswept (`/triage`).

## Updating the board (keep it honest, keep it cheap)

- **Advance a card:** change its `phase` cell when it moves (e.g. `build · ready` → `build ·
  in-progress` → `audit` → `deskcheck · pending`).
- **A seal is NOT a phase-6 pass** — a sealed build moves to `audit`, then `deskcheck`; the track
  is not closed until the owner approves the deskcheck. On any seal, the orchestrator adds/moves
  the row and says "ready to deskcheck" when the track reaches phase 6.
- **Send-back:** a failed deskcheck moves the card back to the phase that fixes it (build,
  graduate, or design-pass) with a note; the track stays open.
- **Close:** when the owner approves a deskcheck, move the track to `## Closed` (below) with the
  date — the only terminal state.
- The **model column is the phase's required tier** — a design-pass on Opus, or a deskcheck the
  owner never saw, is a process defect, not progress.

## Closed (owner-approved deskchecks)

_(none yet — the discipline starts here; earlier "sealed" waves owe their deskchecks above)_
