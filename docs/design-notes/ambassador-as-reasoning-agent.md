# Design note — The Ambassador as a reasoning agent: thinking, cadence, and transparent effort

*Family tag → family 1 (labelings & flow): a pinned-scope agent (𝒜) that reads only the mirror (π_MR) and proposes tasks through the gate (family 3); a light consumer of the reasoning complex (family 5). See [`../NOTATION.md`](../NOTATION.md).*

**Status:** design only. Refines and *corrects* `ambassador-interpretation-and-flow.md`
and `nervous-system-and-ambassador.md` §4 with the owner's intent. Resolves the open
questions those notes flagged (proactive vs. reactive, the intent-classifier floor, history
handling) and fixes a framing error ("thin dispatcher" read as "shallow"). Honor as part of
Track B (the Voice). The corrections here take precedence where they differ from the earlier
notes.

---

## 0. The correction: light ≠ shallow

The earlier note leaned on "thin dispatcher" to resolve the bottleneck worry. That was
right about *computation* and misleading about *cognition*. Two different axes:

- **Computationally light** — holds no heavy work inline; delegates expensive jobs to the
  async scheduler. (True; keep this — it is why it does not bottleneck.)
- **Cognitively real** — genuinely *reasons* about the request: can it answer from what is
  already derived, or must it go *do* something; and *which* exact tool fits. (Also true;
  the earlier note undersold it.)

**The Ambassador is a reasoning agent that is computationally light, not a classifier that
is cognitively shallow.** It is an agent, not a router.

---

## 1. The shape: a mind that *uses* deterministic tools

The Ambassador is **not** deterministic — it is an LLM agent. What is deterministic is the
machinery it *reaches for*: the sandbox solver, graph/knowledge queries, grounded
retrieval, the constraint tools. The model is the **mind**; the deterministic machinery is
what the mind **uses**.

This is **"model advises, code acts" one level up**: the Ambassador advises *the owner* and
*orchestrates* exact tools, rather than being exact itself. It thinks; when thinking is not
enough, it delegates to something that is precise instead of improvising from the model
alone.

```
Owner asks  →  Ambassador *reasons*:
                 • can I answer from already-derived/grounded material?  → retrieve + render
                 • do I need an exact result?  → delegate to a deterministic tool (solver,
                                                  graph query, grounded search) and wait
                 • is this a real task?  → compose a scoped task → gate → queue
               It chooses the tool; the tool is exact; the Ambassador narrates the result.
```

---

## 2. Cadence & history are the agent's own judgment (within bounds)

The Ambassador decides — it does not run a fixed per-turn recipe:
- **when** to retrieve, and **how much** history to pull,
- **when** a conversational thread is worth carrying vs. letting go,
- **when** a query needs background work.

**The one guardrail:** self-determined retrieval still answers to the §13 budgeter's
ceiling. It can *choose what* to pull; it cannot choose to pull *everything*. Judgment
operates **within** a context bound, not without one. (This is what keeps "agentic
retrieval" from becoming the context-assembly bottleneck.)

**History handling (resolves the open question):** the Ambassador judges how much prior
thread to rehydrate per turn, drawing on the `authored-dialogue` ingest rather than
re-storing the thread inline — recent turns are cheap working context; older relevant
context is *retrieved* like any other shelf when the agent judges it relevant. No
double-storage: the conversation lives once, in the `authored-dialogue` corpus.

---

## 3. Updates are contextual — the proactive/reactive question, resolved

The Ambassador speaks in three cases, and stays quiet otherwise:

1. **When the owner is expecting an update.** The owner asked it to look into something →
   it reports back on completion. (Expected → deliver.)
2. **When it has genuine reason to surface a topic.** A real alignment/tamper alarm; a
   high-confidence finding; something it *judges the owner would want raised*. The bar is
   "would the owner want this raised," and meeting that bar is itself an agent judgment.
3. **When it needs to set expectations about effort** (see §4).

**It does not volunteer noise.** Not a silent oracle the owner must interrogate; not a nag
that interrupts. It answers when asked, *and* speaks when it has something that earns the
interruption — and the earning bar is a judgment, not a fixed trigger. (Owner-tunable
sensitivity remains available, but the default is "earned interruptions only.")

---

## 4. Transparent about effort, without being technical

When a query needs real work, the Ambassador **tells the owner plainly**: that it needs to
go think / study / work, *roughly* what it will do, and that there will be a wait. The owner
does not mind waiting — the owner minds being *surprised* by the wait or *buried in jargon*
about it.

- **Right register:** "Let me dig through your notes on this and cross-check a few things —
  give me a bit." / "That's a bigger question; I want to study the connections before I
  answer. I'll come back to you."
- **Wrong register:** "Spawning a synthesis-tier job against the interpreted layer with a
  grounding pass over the mirror." (Internals; verbose; technical.)

The transparency is about **setting the owner's expectation**, not narrating internals. Plain
language, low verbosity, honest about the wait and the rough plan — nothing more.

**Why this needs no new capability:** the attestation layer already draws the line between
"what it is doing" (knowable — every action is attested) and "the secrets/internals" (never
exposed — the self-knowledge-graph firewall). So "tell me what you're doing, in plain
words" is just the **conversational surface of the operational-introspection scope** the
Ambassador already has (B3): it reads its own activity and renders it in human terms, the
same way it reads a dream and renders it. Narrate the *shape* of the work; never the
credentials or the plumbing.

---

## 5. What this changes in Track B (build deltas)

The five Track-B items stand; these refine them:

- **B2 (the agent):** the intent step is a **reasoning step**, not a bucket-classifier. The
  "deterministic floor first, model earned" pattern still applies to *cheap obvious cases*
  (a clear retrieval, a clear status query), but ambiguous or compound requests get genuine
  model reasoning about how to proceed and which tools to use. Floor for the obvious; mind
  for the rest.
- **B5 (retrieval):** retrieval is **agent-judged within the budgeter ceiling**, not a fixed
  per-turn pull. The budgeter enforces the bound; the agent chooses within it.
- **New — effort narration:** a small, plain-language "I need to go work on this" surface,
  emitted when the agent delegates a slow task. Backed by B3's introspection scope; capped
  at plain, non-technical, low-verbosity phrasing. (One render template, not a feature.)
- **New — earned-interruption policy:** the agent may surface a topic unprompted *only* when
  it judges the owner would want it raised (alarms, high-confidence findings). Owner-tunable
  sensitivity; default "earned only."

---

## 6. The one-line summary
**The Ambassador is a reasoning agent that is computationally light: it thinks, it uses
deterministic tools when thinking needs exactness, it judges its own cadence and history
within the budgeter's bound, it surfaces things only when expected or genuinely warranted,
and it is honest in plain language about when it needs to go work — narrating the shape of
its effort, never the internals. A mind that uses exact tools; not an exact thing, and not a
shallow one.**

---

## 7. Resolved vs. still-open
**Resolved here:** proactive vs. reactive (earned interruptions + expected updates);
the intent step (reasoning, not bucketing); history (agent-judged rehydration from the
`authored-dialogue` corpus, no double-store); effort transparency (plain-language narration
via the introspection scope).

**Still open (settle when building / using):**
- Result delivery mechanics for delegated tasks: push on completion vs. await next turn
  (lean: push for explicitly-requested work, await for ambient findings).
- The exact owner control for interruption sensitivity (a single dial? per-category?).
- How long an "I'm working on it" task runs before the Ambassador volunteers a progress
  note vs. staying quiet until done.
