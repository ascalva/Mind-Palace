"""Zone A — theme clustering / synthesis (cron, mirror-not-oracle). BUILD-SPEC §9.

The dreaming agent clusters the AUTHORED corpus into themes (deterministic, model-free) and
reflects each back to the owner as a lens on their own notes — never external truth. Output
is INTERPRETED + regenerable, self-checked before it is kept, and only runs in troughs.

The Phase-7 `Dreamer` is the LIVE path. The interpreter panel (R0) + adjudicator (R1) are a
**flag-OFF R&D track** (`design-notes/dream-phase-rnd-charter.md`) — exported here for tests
but never wired into `scheduler/cron.py`; their entry points refuse to run unless the
`[dream_rnd] enabled` flag is set (`core.dreaming.rnd`).
"""

from core.dreaming.adjudicator import DreamLogEntry, adjudicate, run_dream_rnd
from core.dreaming.cluster import (
    Cluster,
    NoteVector,
    cluster_notes,
    near_duplicate_pairs,
    note_centroids,
    note_snippets,
)
from core.dreaming.dreamer import Dreamer, Synthesizer, Theme, build_dreamer
from core.dreaming.graph import MirrorGraph
from core.dreaming.interpreters import Claim, run_panel
from core.dreaming.rnd import DreamRnDDisabledError, require_rnd_enabled

__all__ = [
    "Claim",
    "Cluster",
    "DreamLogEntry",
    "DreamRnDDisabledError",
    "Dreamer",
    "MirrorGraph",
    "NoteVector",
    "Synthesizer",
    "Theme",
    "adjudicate",
    "build_dreamer",
    "cluster_notes",
    "near_duplicate_pairs",
    "note_centroids",
    "note_snippets",
    "require_rnd_enabled",
    "run_dream_rnd",
    "run_panel",
]
