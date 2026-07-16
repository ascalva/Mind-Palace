# Journal — bp-046 `sweep-levers` (E3a-1a: the σ-fork resolution)

Alive at graduation (2026-07-16). Status `proposed` — awaits owner `proposed → ready` blessing.

## Fresh-agent orientation
This plan is the fork-resolution half of E3a-1, warranted by finding-0087 (owner resolved the σ-lever
fork 2026-07-16: register the `[dream_rnd]` knobs as levers). Read `plan.md` in full, then the §2 context
manifest IN ORDER. The one item (12) does two coupled things that MUST land together:
1. register `dream_rnd_sigma` in `ops/levers._LEVERS` (the knob the shadow runner actually reads for the
   dream_v2 mirror graph — `shadow.py:139-146` reads `dream_rnd.sigma`, NOT `dreaming.similarity_threshold`);
2. widen `core/dreaming/shadow.py:_config_fingerprint` to hash the live value of every REGISTERED lever
   (derive the set from `ops.levers.LEVERS`, key `"<section>.<key>"`) so a σ-sweep gives distinct cell keys.

The whole point: today a σ-sweep would (a) not move dream_v2 (it reads an unregistered knob) and (b)
collide every eval-store cell on one `config_fingerprint` (`store.py:100-104` `put` skips present keys).
Item 12 kills both. The named falsifier is the collision test — two Configs differing only in
`dream_rnd.sigma` must yield DIFFERENT fingerprints.

## Retrofit awareness
`tests/unit/test_levers.py` (registry contents) and `tests/unit/test_shadow_runner.py:88-91` (the
`config_fingerprint` assertions) are in `write_scope` because this plan widens the surfaces they pin. The
`len(fingerprints) == 1` assertion still HOLDS (both pipelines share one cfg → one fingerprint per run);
only its comment rationale updates.

## Open at graduation
- Bound `[0.55, 0.75]` for `dream_rnd_sigma` is the reviewable choice (matches the dreaming σ + bp-040) —
  owner blesses at proposed→ready.
- Registering ONLY σ (not the broader `[dream_rnd]` knobs) is deliberate (§11) — minimal reviewable diff.

## Checkpoints
_(none yet — build has not started)_
