---
type: finding
id: finding-0068
status: routed
created: 2026-07-13
updated: 2026-07-13
links:
  - docs/findings/finding-0065.md
  - docs/design-notes/core-query-protocol.md
  - docs/design-notes/observed-data-and-the-assistant-tier.md
  - core/stores/reference_edges.py
ftype: direction
origin_plan: orchestrator
route: orchestrator
resolution: null
---

# The reference graph's "corpus" is agent-dialogue, not the owner's verbatim notes — the kind vocabulary needs a mirror/dialogue split

## What

Surfaced by the owner (2026-07-13) reviewing finding-0065's ruling. The ruling (and the store's
current schema) treats `corpus` as one kind, spanning `docs/design-notes|findings|brainstorms`.
But those are **not the owner's authored notes** — they are **agent-synthesized artifacts of
owner↔agent dialogue**: brainstorms are dialogue capsules, design notes are rulings distilled
from discussion, findings are work-surfaced issues. None is the owner's verbatim writing.

The owner's actual authored corpus is the **vault** (`~/.mind-palace/vault/janus_notes` — what
the daemon watches, what the Librarian reads as the mirror, `MIRROR_READABLE`). The vault is
**not in the reference graph today**: the store reserves `corpus_kind='digest'` "for vault-note
targets when one becomes resolvable" (`core/stores/reference_edges.py`) — anticipated,
unpopulated. So the reference graph's `corpus` kind is really the **design-conversation
(dialogue) layer**, and the *true* corpus (the mirror) is a distinct, not-yet-present kind.

## Why it matters

The taxonomy is likely **four kinds, not two** (grounded in the existing provenance model —
`Provenance.AUTHORED_SOLO` vs the "authored-dialogue" category the 2026-07-11 owner ruling
names):

| kind | layer | provenance |
| --- | --- | --- |
| `code` | sensed code stream | observed exhaust |
| `mirror` (true corpus) | the owner's vault notes — verbatim | authored-**solo** |
| `dialogue` | the design conversation (notes/findings/brainstorms) | authored-**dialogue** |
| `workflow` | build-plans/journals/PROGRESS | process |

Collapsing `mirror` and `dialogue` (as finding-0065's ruling did) blurs a real provenance seam —
the same class the mirror firewall (`observed-data-and-the-assistant-tier.md`) exists to keep
sharp. It also matters for the §2.5 math: the citation complex the owner cares about (the
*reasoning* corpus) is arguably `dialogue↔dialogue` (+ eventually `mirror`), NOT the raw
"corpus" the ruling scoped it to.

## The owner's framing: the kinds are a derivation gradient (2026-07-13)

The four kinds are NOT a flat list — they sit in the stratum model as a **derivation-depth
climb, and the artifact chain IS that stratification**:

```
  workflow   (build-plans, journals)      depth 2  — derived from dialogue: plans GRADUATE from notes
     ↑ graduate            ↓ findings
  dialogue   (notes/findings/brainstorms) depth 1  — curated owner↔agent discussions, on top of authored
     ↑ brainstorm
  authored / mirror (the owner's vault)   depth 0  — K₀; MY thoughts, my intuition, verbatim

  observed   (code)  — the ORTHOGONAL axis: not derived from the owner's mind, SENSED from the
                        codebase, firewalled (the mirror boundary); referenced by all layers.
```

Owner's words: "authored are MY thoughts, my intuition; dialogue are curated discussions we've
had, sits on top; then observed, which is the code." The completion: **workflow sits ABOVE
dialogue** (plans graduate from notes; journals narrate builds), so brainstorm → note → plan →
journal, with findings looping back, is a climb up derivation-depth.

**Two consequences + one caution for the fable-vet:**
- The reference-graph kinds `{code, mirror, dialogue, workflow}` are this picture read as node
  kinds — which is why they feel natural, not arbitrary.
- It predicts *weighting*: recursive-strata's `γ^d` damps by depth — authored (0) weighs most, a
  build-plan citation (2) least. The stack is a priority order for reasoning, not just a label.
- CAUTION (the fable-0065 pass flagged it): "stratum" already means the *Dreamer's* auto-derived
  layers Sₙ (`recursive-strata.md` §2). This authored/dialogue/workflow climb is *structurally*
  the same shape (derived-on-top, depth-damped) but is an **authorship/provenance-depth axis**,
  not literally a Dreamer stratum. The fable-vet decides: one mechanism or two parallel ones.

## Re-entry condition

**The fable-vet of `dn-core-query-protocol` settles the full node-kind vocabulary WITH the owner
(it is genuinely their call — it defines what their notes ARE).** Candidate: `{code, mirror,
dialogue, workflow}`, with `dialogue` = the current `corpus` renamed, `mirror` reserved for the
vault (digest-addressed, populated when the vault enters the graph). This SUPERSEDES the naive
`{code, corpus, workflow}` in finding-0065's ruling — so the finding-0065 follow-up plan should
**wait** for this vocabulary, then implement the whole taxonomy in ONE additive migration
(avoiding a workflow-now + corpus→dialogue-rename-later double migration).

## Routing

`direction` → orchestrator, deferred to the fable-vet (owner's explicit "finish bp-026 first").
Non-blocking; the v2 store is live + correct under its current single `corpus` kind. This
refines, not reverses, finding-0065 (workflow stays distinct; the `corpus` side subdivides).
