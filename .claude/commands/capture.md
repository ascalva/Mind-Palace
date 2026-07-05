---
description: Append a brainstorm session capsule (or raw paste) to docs/brainstorms/<topic>.md, timestamped.
argument-hint: <topic>
---
Capture a brainstorm session into `docs/brainstorms/$1.md` (create it if absent).

The owner's pasted content follows. It is normally a `capsule` fenced block
(`decisions`, `parked` with re-entry, `open_questions`, `next_steps`,
`references`; see `docs/templates/capsule.md`). It may instead be a raw
conversation excerpt — **tolerate that**: lossy capture beats no capture (§8).

Steps:
1. Ensure `docs/brainstorms/$1.md` exists (H1 = the topic if creating).
2. Append a `## <UTC timestamp>` section.
3. If the paste is a well-formed capsule, append it verbatim under that heading.
   If it is raw, restructure it into the capsule shape on append — preserve every
   parked item's re-entry condition; never invent one.
4. Do not write any file other than the brainstorm note. The chat agent never
   writes files; this command is the only ingress from chat to repo.

Pasted content:
$ARGUMENTS
