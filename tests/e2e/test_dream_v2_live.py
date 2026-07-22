"""Live gate: the loop-v2 Dreamer pass end to end with real local models (H8/H9; BUILD §3.1).

The full strong-Dreamer pass over the golden fixture corpus: real embedder → the reasoning
complex + interpreter panel → noisy-OR support → adjudication → REAL synthesis-tier narration →
interpreted store → structural snapshot. Gated on the synthesis-tier model being pulled, exactly
like the v1 gate (`test_dreaming_live`); the dream-R&D flag is enabled for the run (the loop v2
is that engine's assembly). Run: pytest -m live.
"""

import dataclasses

import pytest

from config.loader import get_config
from core.complex.temporal import SnapshotStore
from core.dreaming import Dreamer
from core.ingest.embed import build_embedder
from core.ingest.index import index_records
from core.kernel.ingest.pipeline import ingest_vault
from core.kernel.stores.rawstore import RawStore
from core.models import build_model_server
from core.models.ollama_client import OllamaClient
from core.stores.derived import DREAM, DerivedStore
from core.stores.vectorstore import VectorStore
from eval.golden import CORPUS_DIR

pytestmark = pytest.mark.live


def _models_present() -> bool:
    try:
        cfg = get_config()
        have = set(OllamaClient(cfg.ollama).list_models())
        return {cfg.embedding.model, cfg.model_for_tier("synthesis").name} <= have
    except Exception:
        return False


@pytest.mark.skipif(not _models_present(), reason="synthesis-tier model not pulled")
def test_dream_v2_synthesizes_grounded_themes_live(tmp_path):
    cfg = get_config()
    rnd_on = dataclasses.replace(cfg, dream_rnd=dataclasses.replace(cfg.dream_rnd, enabled=True))
    raw = RawStore(tmp_path / "raw")
    store = VectorStore(tmp_path / "v.lance", dim=cfg.embedding.dim)
    index_records(ingest_vault(CORPUS_DIR, raw), build_embedder(cfg), store)

    server = build_model_server(cfg)
    snapshots = SnapshotStore(tmp_path / "structural.duckdb")
    dreamer = Dreamer(
        store=store,
        synthesize=lambda messages: server.chat("synthesis", messages),
        derived=DerivedStore(tmp_path / "derived.sqlite"),
        snapshots=snapshots,
        max_clusters=3,            # cap the live generations — this is a gate, not a benchmark
    )

    themes = dreamer.dream_v2(config=rnd_on)

    assert themes                                            # candidates were narrated
    assert all(t.summary.strip() for t in themes)
    # The grounding mechanism fired end to end (PASS/FAIL depends on the live generation's
    # citation discipline, asserted deterministically in test_dream_v2 — not here).
    assert any(f.directive == "grounded-citations" for f in themes[0].check.findings)
    stored = dreamer.derived.all(kind=DREAM)
    assert len(stored) == len(themes)                        # persisted as INTERPRETED dreams
    assert all(a.data.get("loop") == "v2" for a in stored)
    assert snapshots.count() == 1                            # the pass measured itself (§5.4)
    assert snapshots.latest_structural() is not None
    snapshots.close()
