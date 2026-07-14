# bp-034 journal

## 2026-07-14 — authored `proposed` (orchestrator, opus/xhigh; the oq-0019 B follow-on)

Authored as the follow-on to **oq-0019's (B) ruling** (owner sided with mint-into-vault as the durable,
rename-stable identity). `depends_on: bp-031`. The owner asked for **extreme rigor** — grounded hard
against the ingest + store code.

**The decisive grounding (why the plan is precise, not hand-wavy):**
- **The re-key surface is TINY and exact.** Only `versions.doc_id` (+ the catalog `doc_id` column) needs
  an explicit re-key (`source_path → minted id`). The **vector store self-heals** (keyed by
  `(source_path, chunk_hash)`, `index.py:32,88`; `index_amendment` re-projects under the stable
  source_path, `:80`); the **raw store + `authored_supersession` are digest-keyed** (old digests persist,
  raw is sacred) — neither needs re-keying. Grounded, not assumed.
- **The owner's "won't ingest see it as an update?" is half-right.** The in-place mint IS detected as an
  amendment (`sync.py:89-113`), BUT the amendment `record()`s under the RESOLVED (new) doc_id, and
  `versions` is append-only with no self-heal → `current(new_id)` is None → **seq 1 → fork**
  (`versions.py:88-94`). So the **explicit version re-key is mandatory**; the digest change alone does
  not carry lineage. This is the load-bearing fact oq-0019 named.
- **An invariant tension surfaced (owner-gated):** `versions` is structurally append-only ("no
  update/delete"). The re-key is a **relabel** (preserves `(seq, digest, at)`), not a history rewrite —
  precedented by `catalog.relabel_provenance:124`. But it's invariant-adjacent → **§4/§10/§11 surface it
  as an owner ruling at blessing** (default: admit an `OwnerDeclaration`-gated `migrate_rekey_doc_id`;
  the capability model borrowed from `authored_supersession.py`).

**Shape: BUILD THE TOOL, don't run the migration** — mirrors `purge.py`/`scripts/purge_raw.py` (owner-
gated, `confirm=True` fail-closed, offline). The owner runs it once, corpus-wide, **daemon DOWN**
(deploy-coupled, finding-0066). Byte-preserving `id::` insertion (Item 15); idempotent-skip notes with
existing `id::`/YAML `id:` (this is why repo design-notes/findings — already `id:`-stamped — are
untouched, addressing the owner's "design notes and docs" concern). The build writes **no vault file**.

**Highest-blast plan to date** (first corpus write + first append-only relabel) → opus/high, maximal
scrutiny; a vault backup + store backup + dry-run + confirm all gate the real run; reversible.

write_scope names both test paths (finding-0075): `test_mint_ids.py` (end-to-end) + `test_version_rekey.py`
(the primitive). Items 13–16 continue the family. Estimate opus/450k. Awaiting the owner-only `proposed →
ready` blessing **and** the Q3 append-only-re-key ruling (§11). No code written.
