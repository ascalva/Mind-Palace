# The track board — the portfolio view

> **The tracking hierarchy (owner, 2026-07-21):** item (a build-plan item) ⊂ build plan (a
> session) ⊂ **track** (all design + all builds + wiring for one cohesive body of work — e.g.
> "the inner/outer core track") ⊂ **this board** (the portfolio view of ALL concurrent tracks,
> so none is lost — the "another category of tracking" a team needs when many run at once).
>
> **A track is CLOSED only when DESKCHECKED and owner-approved** — demonstrated working (or its
> true state shown), walked through (what/how/surprises), and the owner has the final say.
> "Sealed" is not "closed." The orchestrator OWNS this board and keeps every track visible until
> the owner closes it. Maintained by `/triage` and every seal. `docs/DESKCHECK-QUEUE.md` is the
> filtered action-list of tracks in `deskcheck-pending`.
>
> **Phases:** `designing` → `building` → `built` → `wired` → `deskcheck-pending` → `CLOSED`
> (owner-approved). A track can also be `dormant-by-design` (accepted, e.g. effectors).

## Active tracks

| track | phase | design | builds | wired / delivered? | open follow-through |
|---|---|---|---|---|---|
| **Code-ingest** (warrant f-0146) | building | dn-code-ingest-pipeline **ratified** | bp-092/093/094/095 **ready**, not built | — | integrator densification (f-0151) is part of its DoD; deskcheck on completion |
| **Inner/outer core** | building | dn-inner-outer-core **ratified** | M0 bp-083 + S1 bp-089 **built+LIVE**; M2 K1 bp-090 + K3 bp-091 **ready**, not built | enforcement (ratchet) LIVE; physical `core/kernel/` split NOT done | K1→K3→M3 flip; **deskcheck the M0/S1 enforcement half now** (it's real and demonstrable) |
| **Sync/diac dreamers** | **built, NOT delivered** | dn-synchronic-diachronic-dreamer **ratified** | bp-079/080/081/082 **sealed** | **NO** — `[dream_rnd] enabled=false`, no live dispatch entry (f-0141); diachronic (SD-a) parked | **deskcheck → decide: wire live or accept dormant.** This is the track that fell through (Q5) |
| **Reference bookkeeper** (f-0145/0154) | designing | Fable pass PENDING (after builds) | — | minting LIVE; bookkeeper (deferred resolution, external-research citations, current-view) UNBUILT | full design pass; a librarian-sibling async agent |
| **Agentic loop** | built (wiring unverified) | dn-agentic-loop **ratified** | AL-1 bp-086 · AL-2 bp-087 · AL-3 bp-088 **sealed** | origin(e) view built; **deskcheck to confirm delivery** (not verified this session) | deskcheck AL-1/2/3; f-0142 note-amendment candidate |
| **Fiber geometry** | built (readings owed) | dn-fiber-geometry **ratified** | G-A survey bp-085 **sealed** | survey ran; **deskcheck the readings** | G-A's deferred S-rows (M2/M4/M5/M8 — re-run with embed headroom, per PROGRESS) |
| **Track G / effectors** | **dormant-by-design** | dn-hands (draft) | G1–G7 built (`e0bf1ad`) | intentionally NONE (f-0011) | deskcheck = confirm dormancy is still intended (don't assume) |

## Pending-design tracks (Fable pass, AFTER the current builds — owner re-tiers)

| track | warrant | note |
|---|---|---|
| Integrator densification | f-0151 | dense version-grain dialogue→code authorship; part of code-ingest DoD |
| Deskcheck / track workflow | f-0153 | formalize this board + the gate + `/deskcheck` ceremony + seal-time enforcement |
| Reference bookkeeper | f-0154 | the async F-consistency agent |

## How a track closes (the discipline)

1. All its builds seal → phase `built`.
2. Wire/deliver it (or record why it's `dormant-by-design`) → phase `wired`.
3. Orchestrator says **"ready to deskcheck"** and presents the bundle (`/verify` + the
   phone-build-report: what / how / surprises / it-working-or-its-state / what's NOT done).
4. Owner deskchecks → **CLOSED** (approved) or **needs-work** (spawns a follow-up plan/finding,
   track stays open).
5. The orchestrator NEVER self-declares a track closed. It keeps every open track on this board
   until the owner closes it — that is the follow-through obligation Q5 lacked.
