"""ops/code_snapshot.py — CI-1 ledger extensions (bp-092 Item 1): symbol spans (`end_lineno`),
the inline-comment sidecar, and full import records. Additive migration + backfill discipline.

The three captures the code embed lane (`core/ingest/code_corpus.py`) reads FROM the ledger:
L0a slice boundaries, the `#` comments the AST drops (finding-0146 defect 2), and the full
dotted import records CI-3 resolves cross-module edges from. Every assertion here also guards
the falsifier: the migration/backfill is ADDITIVE — no pre-existing ledger row may change.
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

import pytest

from ops.code_snapshot import (
    Comment,
    ImportRecord,
    Symbol,
    backfill_code_corpus,
    open_snapshot_db,
    parse_source,
    snapshot_commit,
)

_MAIN_PACKAGES = ("core", "ops", "edge", "config", "scripts", "agents", "eval")


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True).stdout


_FIXTURE = (
    "import json\n"                                  # 1
    "from pathlib import Path as P\n"                # 2
    "from . import sibling\n"                        # 3
    "from a.b.c import x, y\n"                        # 4
    "\n"                                             # 5
    "# module-grain comment\n"                       # 6
    "class Thing:\n"                                 # 7
    "    # class-body comment\n"                     # 8
    "    def method(self, x):\n"                      # 9
    "        # innermost comment\n"                   # 10
    "        return x  # trailing comment\n"          # 11
    "\n"                                             # 12
    "async def run():\n"                             # 13
    "    pass\n"                                     # 14
)


# ── parse_source: the three captures ────────────────────────────────────────────────────

def test_parse_source_captures_end_lineno():
    shape = parse_source("m.py", "sha", _FIXTURE)
    spans = {s.qualname: (s.lineno, s.end_lineno) for s in shape.symbols}
    assert spans["Thing"] == (7, 11)
    assert spans["Thing.method"] == (9, 11)
    assert spans["run"] == (13, 14)
    # every symbol's span is well-formed (end_lineno >= lineno >= 1), never the pre-CI-1 zero
    assert all(s.end_lineno >= s.lineno >= 1 for s in shape.symbols)


def test_parse_source_captures_comments_at_innermost_symbol():
    shape = parse_source("m.py", "sha", _FIXTURE)
    by_line = {c.lineno: c for c in shape.comments}
    assert by_line[6].qualname == ""                       # module grain (outside every symbol)
    assert by_line[8].qualname == "Thing"                  # class body, not yet in the method
    assert by_line[10].qualname == "Thing.method"          # innermost wins over the parent class
    assert by_line[11].qualname == "Thing.method"          # trailing comment on a body line
    assert by_line[10].text == "# innermost comment"       # verbatim token, '#' included


def test_parse_source_captures_full_import_records():
    shape = parse_source("m.py", "sha", _FIXTURE)
    recs = {(r.module, r.name, r.asname, r.level) for r in shape.import_records}
    assert ("json", "", "", 0) in recs                     # plain whole-module import
    assert ("pathlib", "Path", "P", 0) in recs             # aliased from-import
    assert ("", "sibling", "", 1) in recs                  # relative `from . import`
    assert ("a.b.c", "x", "", 0) in recs                   # FULL dotted module preserved
    assert ("a.b.c", "y", "", 0) in recs
    # the legacy root-only `imports` set is UNCHANGED (kept for existing consumers)
    assert shape.imports == {"json", "pathlib", "a"}


# ── L0a span cover (the F-CI2 precursor: top-level spans + module shell partition the file) ──

def _covered_by_top_level(symbols: list[Symbol]) -> set[int]:
    top = [s for s in symbols if "." not in s.qualname]
    # top-level symbol spans must be pairwise non-overlapping (each source line in <= 1 symbol)
    covered: set[int] = set()
    for s in top:
        rng = set(range(s.lineno, s.end_lineno + 1))
        assert not (rng & covered), f"overlapping top-level span at {s.qualname}"
        covered |= rng
    return covered


def test_top_level_spans_plus_shell_partition_every_line():
    shape = parse_source("m.py", "sha", _FIXTURE)
    n_lines = _FIXTURE.count("\n")
    covered = _covered_by_top_level(shape.symbols)
    shell = set(range(1, n_lines + 1)) - covered           # the module shell (outermost parent)
    # union is exactly every source line, each in exactly one L0a bucket (symbol slice OR shell)
    assert covered | shell == set(range(1, n_lines + 1))
    assert covered & shell == set()


# ── full snapshot roundtrip + idempotence + backfill (the DB path) ──────────────────────

@pytest.fixture
def repo(tmp_path) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "t@t")
    _git(r, "config", "user.name", "t")
    (r / "mod.py").write_text(_FIXTURE)
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "one")
    return r


def _pre_existing_checksum(db) -> str:
    """A digest over ONLY the pre-CI-1 columns of files/symbols/imports — the additivity guard.
    If any of these change across a migration/backfill, the change was NOT additive (falsifier)."""
    h = hashlib.sha256()
    for row in db.execute("SELECT commit_sha, path, blob_sha, loc, functions, classes, "
                          "parse_error, docstring FROM files ORDER BY commit_sha, path"):
        h.update(repr(row).encode())
    for row in db.execute("SELECT commit_sha, path, kind, qualname, lineno, signature, docstring "
                          "FROM symbols ORDER BY commit_sha, path, qualname, lineno"):
        h.update(repr(row).encode())
    for row in db.execute("SELECT commit_sha, path, module FROM imports "
                          "ORDER BY commit_sha, path, module"):
        h.update(repr(row).encode())
    return h.hexdigest()


def test_snapshot_records_ci1_captures(repo, tmp_path):
    db = open_snapshot_db(tmp_path / "snap.sqlite")
    sha = snapshot_commit(db, repo)
    assert sha is not None
    spans = dict(db.execute("SELECT qualname, end_lineno FROM symbols"))
    assert spans == {"Thing": 11, "Thing.method": 11, "run": 14}
    cqual = dict(db.execute("SELECT lineno, qualname FROM comments"))
    assert cqual == {6: "", 8: "Thing", 10: "Thing.method", 11: "Thing.method"}
    full = {(m, n) for m, n in db.execute("SELECT module, name FROM import_records")}
    assert ("a.b.c", "x") in full and ("a.b.c", "y") in full and ("json", "") in full


def test_snapshot_idempotent_and_backfill_noop_on_fresh_ledger(repo, tmp_path):
    db = open_snapshot_db(tmp_path / "snap.sqlite")
    assert snapshot_commit(db, repo) is not None
    before = _pre_existing_checksum(db)
    ncomments = db.execute("SELECT count(*) FROM comments").fetchone()[0]
    # a fresh snapshot already carries the captures, so backfill visits nothing new and mutates
    # nothing; the pre-existing checksum and the comment count are byte-stable (idempotence).
    assert snapshot_commit(db, repo) is None
    backfill_code_corpus(db, repo)
    assert _pre_existing_checksum(db) == before
    assert db.execute("SELECT count(*) FROM comments").fetchone()[0] == ncomments


def test_backfill_is_additive_on_a_pre_ci1_ledger(repo, tmp_path):
    """A ledger snapshotted, then STRIPPED of the CI-1 data (simulating a pre-CI-1 ledger), must
    backfill without changing any pre-existing row — end_lineno fills in, comments/imports appear,
    and the files/symbols/imports pre-existing columns are byte-identical before and after."""
    db = open_snapshot_db(tmp_path / "snap.sqlite")
    snapshot_commit(db, repo)
    # regress to pre-CI-1: zero the added span column, empty the added tables, clear the marks
    with db:
        db.execute("UPDATE symbols SET end_lineno = 0")
        db.execute("DELETE FROM comments")
        db.execute("DELETE FROM import_records")
        db.execute("DELETE FROM _code_corpus_backfilled")
    before = _pre_existing_checksum(db)
    visited = backfill_code_corpus(db, repo)
    assert visited == 1
    assert _pre_existing_checksum(db) == before               # ← the additivity falsifier
    assert dict(db.execute("SELECT qualname, end_lineno FROM symbols"))["Thing.method"] == 11
    assert db.execute("SELECT count(*) FROM comments").fetchone()[0] == 4
    assert db.execute("SELECT count(*) FROM import_records").fetchone()[0] == 5
    # idempotent: a second backfill is marked-done, a no-op
    assert backfill_code_corpus(db, repo) == 0


# ── the acceptance measurement: comment capture reproduces over the real main-package set ──

def test_comment_capture_reproduces_over_main_package():
    """The ledger's tokenize pass must reproduce an INDEPENDENT comment recount over the pinned
    main-package set (audit set = {core, ops, edge, config, scripts, agents, eval}). Self-
    consistent by construction (not a hardcoded 3,318 — the tree evolves), and a floor guards a
    silent capture regression."""
    import io
    import tokenize

    root = Path(__file__).resolve().parents[2]
    files = sorted(
        p for pkg in _MAIN_PACKAGES for p in (root / pkg).rglob("*.py") if p.is_file()
    )
    captured = 0
    independent = 0
    for p in files:
        src = p.read_text(encoding="utf-8", errors="replace")
        captured += len(parse_source(str(p), "sha", src).comments)
        try:
            independent += sum(
                1 for tok in tokenize.generate_tokens(io.StringIO(src).readline)
                if tok.type == tokenize.COMMENT)
        except (tokenize.TokenError, IndentationError, SyntaxError, ValueError):
            pass
    assert captured == independent
    assert captured > 3000              # sanity floor near the audited ~3,318/3,360 measurement


def test_dataclasses_are_frozen_value_types():
    # the ledger units are immutable value types (hashable, dedup-safe in the walk)
    assert Symbol("function", "f", 1, "()", "", 3).end_lineno == 3
    assert Comment(6, "", "# c").qualname == ""
    assert ImportRecord("a.b", "x", "", 4, 0).module == "a.b"
