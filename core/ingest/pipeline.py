"""Ingest pipeline: vault -> raw store (dedup) -> chunks (BUILD-SPEC §8, §9).

The deterministic write path. Embedding + LanceDB indexing consume `IngestRecord` (next
increment). Everything produced here is provenance AUTHORED (the mirror's ground truth).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from core.ingest.chunk import Chunk, chunk_text
from core.ingest.logseq import ParsedNote, iter_vault, parse_note
from core.provenance import Provenance
from core.stores.rawstore import RawStore


@dataclass(frozen=True)
class IngestRecord:
    digest: str               # content hash of the raw note (identity in the raw store)
    source_path: str
    title: str
    provenance: Provenance
    tags: frozenset[str]
    links: frozenset[str]
    chunks: tuple[Chunk, ...]
    is_new: bool              # False => raw content already present (deduped)


def ingest_note(note: ParsedNote, raw: RawStore, *,
                max_chars: int = 1200, overlap_chars: int = 150) -> IngestRecord:
    # Store the verbatim ORIGINAL bytes (raw is sacred, §8); chunk the decoded text view.
    digest, is_new = raw.add(note.raw_bytes)
    chunks = tuple(chunk_text(note.text, max_chars=max_chars, overlap_chars=overlap_chars))
    return IngestRecord(
        digest=digest,
        source_path=note.source_path,
        title=note.title,
        provenance=Provenance.AUTHORED,
        tags=note.tags,
        links=note.links,
        chunks=chunks,
        is_new=is_new,
    )


def ingest_vault(vault: Path, raw: RawStore, *, pattern: str = "**/*.md",
                 max_chars: int = 1200, overlap_chars: int = 150) -> list[IngestRecord]:
    return [
        ingest_note(parse_note(path, vault), raw, max_chars=max_chars, overlap_chars=overlap_chars)
        for path in iter_vault(vault, pattern=pattern)
    ]
