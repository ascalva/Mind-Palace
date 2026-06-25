"""Chunk note text for embedding (BUILD-SPEC §8 derived layer).

Block-aware and deterministic: split on blank lines (Logseq blocks), hard-split any block
larger than the budget, then greedily pack blocks up to a character budget with overlap.
Chunks are a *regenerable* derived representation — re-chunk from the raw store if the
strategy or embedding model changes. Token-aware sizing (per the embedding model's
tokenizer) is a later refinement; characters are a stable proxy now.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    index: int
    text: str


def _blocks(text: str, max_chars: int) -> list[str]:
    out: list[str] = []
    for raw in text.split("\n\n"):
        b = raw.strip()
        if not b:
            continue
        if len(b) <= max_chars:
            out.append(b)
        else:  # a single oversized block: hard-split into windows
            out.extend(b[i:i + max_chars] for i in range(0, len(b), max_chars))
    return out


def chunk_text(text: str, *, max_chars: int = 1200, overlap_chars: int = 150) -> list[Chunk]:
    chunks: list[str] = []
    cur = ""
    for b in _blocks(text, max_chars):
        if cur and len(cur) + len(b) + 2 > max_chars:
            chunks.append(cur)
            tail = cur[-overlap_chars:] if overlap_chars else ""
            cur = f"{tail}\n\n{b}" if tail else b
        else:
            cur = f"{cur}\n\n{b}" if cur else b
    if cur:
        chunks.append(cur)
    return [Chunk(i, c) for i, c in enumerate(chunks)]
