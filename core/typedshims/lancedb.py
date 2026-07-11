"""Typed facade over `lancedb` (type-system-as-core-audit.md §2.5 boundary wrapper).

lancedb ships no `py.typed` (V2, 2026-07-11), so a raw import launders `Any`
through every downstream call. This module is the ONE place core touches the raw
package: values coming back from lancedb are pinned to the minimal Protocol
surface the vector store actually uses, so the checked region sees honest types.
Compute/storage-only dependency — embedded, no daemon, no network (Invariant 2).

Do not widen these Protocols speculatively: they describe what core calls today,
and each addition should arrive with the call that needs it.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Protocol

import lancedb  # type: ignore[import-untyped]  # warrant: no py.typed upstream (V2); Any quarantined to this shim
import pyarrow as pa

# A row as LanceDB hands it back (Arrow -> Python). `object` values, not `Any`:
# consumers must narrow before doing anything value-shaped with a field.
Row = dict[str, object]


class ArrowTable(Protocol):
    """The slice of `pyarrow.Table` the store consumes from `to_arrow()`."""

    def to_pylist(self) -> list[Row]: ...


class TableNames(Protocol):
    """Result of `list_tables()` — we read only the name list."""

    tables: list[str]


class VectorQuery(Protocol):
    """LanceDB's chained query builder, as used by `VectorStore.search`."""

    def metric(self, name: str) -> VectorQuery: ...

    def where(self, predicate: str, *, prefilter: bool = ...) -> VectorQuery: ...

    def limit(self, k: int) -> VectorQuery: ...

    def to_list(self) -> list[Row]: ...


class VectorTable(Protocol):
    """The slice of a LanceDB table the store calls."""

    def add(self, rows: Sequence[Mapping[str, object]]) -> None: ...

    def count_rows(self) -> int: ...

    def delete(self, predicate: str) -> None: ...

    def to_arrow(self) -> ArrowTable: ...

    def search(self, vector: list[float]) -> VectorQuery: ...


class VectorDB(Protocol):
    """The slice of a LanceDB connection the store calls."""

    def list_tables(self) -> TableNames: ...

    def open_table(self, name: str) -> VectorTable: ...

    def create_table(self, name: str, *, schema: pa.Schema) -> VectorTable: ...

    def drop_table(self, name: str) -> None: ...


def connect(uri: str) -> VectorDB:
    """Open/create an embedded LanceDB at `uri` — the sole typed entry point."""
    db: VectorDB = lancedb.connect(uri)
    return db
