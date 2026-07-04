"""The ratified verdict taxonomy — the categories the signed verdict store accepts.

Ratified as the live-adoption §3 (L2) review set (build plan R3, resolving the verdict-authority §1
"adopt/reject/supersede/promote" paraphrase against the concrete L2 candidate). Kept to five — the
review-fatigue bound live-adoption names: "keep it ≤5 or review fatigue kills the loop."

These are LABELING verdicts (how good is this claim?). The promotion / supersession the
sacred-boundary channel effects is the DOWNSTREAM action a label triggers (`novel_useful` ⇒ promote,
…) — the apply-half (build plan Item 4b-apply), parked on the promotion mechanism (recursive-strata
I1). A strata-promotion verdict ("promote insight weight", recursive-strata §8) folds in when that
layer unparks; it is intentionally NOT added now, to keep this the clean L2 set.
"""

from __future__ import annotations

VERDICT_TAXONOMY: frozenset[str] = frozenset({
    "novel_useful",   # true, and I didn't already know it — the number that matters
    "true_known",     # correct but already in my head — calibration, not failure
    "plausible",      # can't verify yet; interesting — a probe candidate
    "wrong",          # the claim is false — precision (also a grounding defect if unsupported)
    "noise",          # not even a claim worth judging — a clusterer/threshold signal
})
