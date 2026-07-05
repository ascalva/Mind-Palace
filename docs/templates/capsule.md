<!--
Session capsule (chat-side protocol, §8). Every brainstorm session in Claude chat
ends with one of these in a fenced block. The owner pastes it into
`/capture <topic>`, which appends it (timestamped) to docs/brainstorms/<topic>.md.
Capsule loss is tolerated: `/capture` also accepts a raw pasted transcript and the
orchestrator restructures on append. Lossy capture beats no capture.
-->
```capsule
topic: <topic>
date: <YYYY-MM-DD>

decisions:
  - <a decision reached this session>

parked:
  - decision: <what was deferred>
    default: <what holds until revisited>
    re_entry: <the condition that reopens it>   # required — no park without re-entry

open_questions:
  - <question still unresolved>

next_steps:
  - <concrete next action>

references:
  - <artifact id, or code path@ref, or external source>
```
