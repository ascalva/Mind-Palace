# Journal — bp-067 (config-split: move the loader into core.config)

## 2026-07-18 — minted (proposed), awaiting owner bless
Owner-directed (2026-07-18), the config leg of finding-0103's cleanup program under the core-is-sacred
principle (bp-066). Owner chose **option 1** — the loader move (red 106 → ~18) — after asking for "the
most secure approach that keeps the spirit of the form"; the secrets/Vault inversion is DELIBERATELY
deferred to its own adversarially-verified plan (bp-068+) rather than smuggled into a wide mechanical
sweep. Status `proposed` — awaits the owner's `proposed → ready` blessing (owner-only, by hand).

**Grounding carried in the plan (so a fresh builder needn't re-derive):**
- `config/loader.py` is stdlib-only + side-effect-free (`lru_cache`'d pure TOML reads → frozen
  dataclasses). Clean move into `core/config/`. Its tomls (`defaults/local/levers.toml`) move with it;
  `tuning.toml`/`sweeps/` stay outside (not loader-read).
- TWO entanglements, both pinned in §6: `REPO_ROOT = __file__.parent.parent` re-anchors to `.parent
  .parent.parent` (module now two levels deeper); `get_secret`'s token branch lazily reaches
  `config.secrets_backend` (network Vault) — so core's `get_secret` is the ENV path ONLY, the
  token-capable form stays in the outside facade.
- The entire core secrets/Vault/network entanglement is LOCALIZED to `core/factory/factory.py` (the one
  core file using the Vault `get_secret` token path + the 2 `secrets_backend` imports). It stays RED
  after this plan — the deferred inversion. The attestor (env-path get_secret) repoints cleanly.
- The outside `config/` becomes a re-export FACADE over `core.config` → the 104 non-core importers are
  untouched; only the ~47 core files repoint. Facade re-exports (defines nothing but the token
  get_secret wrapper) ⇒ one source of truth, DRY-clean.
- Security WIN: once inside `core/`, config loading falls under `import_lint`'s network ban — config
  loading becomes structurally network-proven (it wasn't, as an outside module).

**Next action when blessed:** item 1 (relocate + re-anchor + get_secret split) → item 2 (repoint core +
facade) → item 3 (verify red drops 106→~18 with the remaining set = factory secrets + the 16 reaches,
and core/config/** is network-free). Estimate opus/130k. ⚠️ The suite stays RED-by-design (the ratchet)
— acceptance = the ONLY failure is `test_core_self_containment` AND its count dropped to ~18.
