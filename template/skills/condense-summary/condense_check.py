#!/usr/bin/env python3
"""Locate a PAPER_SUMMARIES.md entry and its PAPER_INDEX.md row; count words.

Bundled with the condense-summary skill. Stdlib only; works in any collection
repo that has PAPER_SUMMARIES.md with ``### `` entry headings (slug-anchored
or not) and a PAPER_INDEX.md with markdown tables.

Usage:
    python3 condense_check.py <repo_root> <key>          # report on one entry
    python3 condense_check.py <repo_root> --sweep        # one line per entry
    python3 condense_check.py <repo_root> --sweep --section "Section Name"

<key> is the ``### `` heading text (the slug in slug-anchored repos). If no
heading equals it exactly, a case-insensitive substring match on headings is
tried; multiple hits are an error, so tighten the key.

Exit 0 on a report, 1 when the key resolves to no entry (or to several).
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SECTION_RE = re.compile(r"^## (.+?)\s*$")
ENTRY_RE = re.compile(r"^### (.+?)\s*$")
TITLE_RE = re.compile(r"^\*\*Title:\*\*\s*(.+?)\s*$")
FILE_BULLET_RE = re.compile(r"^- \*\*File:?\*\*:?\s*(?:`([^`]+)`.*|(\S+))\s*$")
FILES_HEADER_RE = re.compile(r"^- \*\*Files:?\*\*:?\s*$")
SUB_BULLET_RE = re.compile(r"^\s+- (?:`([^`]+)`.*|(\S+))\s*$")
TEXT_BULLET_RE = re.compile(
    r"^- \*\*Text(?: extraction)?:?\*\*:?\s*(?:`([^`]+)`.*|(\S+))\s*$"
)
FOCUS_RE = re.compile(r"^- \*\*Focus:\*\*\s*(.+?)\s*$")
ONE_LINER_RE = re.compile(r"^- \*\*One-liner:\*\*\s*(.+?)\s*$")
INDEX_LABEL_RE = re.compile(r"^- \*\*Index label:\*\*\s*(.+?)\s*$")
# The canonical name is ``Related``; the others are the legacy spellings the
# skill renames on contact. Order matters only for the reported field name.
RELATED_NAMES = (
    "Related",
    "Relationship to other repo entries",
    "Cross-references (in this collection)",
    "Cross-references in this collection",
    "Cross-references",
    "Companions in this collection",
)
RELATED_RE = re.compile(
    r"^- \*\*(" + "|".join(re.escape(n) for n in RELATED_NAMES) + r"):?\*\*:?\s*(.*?)\s*$"
)
BACKTICK_SLUG_RE = re.compile(r"`([a-z0-9][a-z0-9-]*)`")
# "Key findings" is the canonical label; the collection also uses Key claims /
# Key results / Key arguments etc. for non-empirical sources. All count.
# A parenthetical qualifier ("Summary (compiled from secondary sources):") is
# still the Summary paragraph.
LABELLED_PARA_RE = re.compile(
    r"^(?:\*\*)?(Summary|Key [A-Za-z ]+?|Relevance)(?: \([^)]*\))?:(?:\*\*)?\s*(.*)$"
)
REFERENCE_ONLY_RE = re.compile(r"reference-only", re.IGNORECASE)
TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$")
SLUG_CELL_RE = re.compile(r"^\s*`([^`]+)`\s*$")

ONE_LINER_WARN = 50
ONE_LINER_FAIL = 60
SUMMARY_FLOOR = 80


@dataclass
class Entry:
    key: str
    line: int
    section: str = ""
    title: str = ""
    files: list[str] = field(default_factory=list)
    focus: str | None = None
    one_liner: str | None = None
    index_label: str | None = None
    related: list[str] = field(default_factory=list)
    related_field_name: str | None = None
    reference_only: bool = False
    summary_words: int = 0
    key_findings_text: str = ""
    has_key_findings: bool = False
    has_relevance: bool = False
    end_line: int = 0


@dataclass
class IndexRow:
    line: int
    text: str
    cells: list[str]
    cell_word_counts: list[int]
    matched_by: str


def word_count(text: str | None) -> int:
    if not text:
        return 0
    cleaned = re.sub(r"[`*_]", " ", text)
    return len(re.findall(r"[^\s—–|]+", cleaned))


def verdict(n: int | None) -> str:
    if n is None:
        return "MISSING"
    if n > ONE_LINER_FAIL:
        return "FAIL"
    if n > ONE_LINER_WARN:
        return "WARN"
    return "OK"


def parse_entries(md_text: str) -> list[Entry]:
    lines = md_text.splitlines()
    entries: list[Entry] = []
    current: Entry | None = None
    section = ""
    in_files_list = False
    para: str | None = None  # which labelled paragraph we are inside
    para_buf: list[str] = []

    def close_para():
        nonlocal para, para_buf
        if current is None or para is None:
            para, para_buf = None, []
            return
        text = " ".join(para_buf).strip()
        if para == "Summary":
            current.summary_words = word_count(text)
        elif para.startswith("Key "):
            current.key_findings_text = text
            current.has_key_findings = True
        elif para == "Relevance":
            current.has_relevance = True
        para, para_buf = None, []

    for i, line in enumerate(lines, start=1):
        if m := ENTRY_RE.match(line):
            close_para()
            if current is not None:
                current.end_line = i - 1
            current = Entry(key=m.group(1), line=i, section=section)
            entries.append(current)
            in_files_list = False
            continue
        if m := SECTION_RE.match(line):
            close_para()
            if current is not None:
                current.end_line = i - 1
            current = None
            section = m.group(1)
            continue
        if current is None:
            continue
        if line.strip() == "---":
            close_para()
            current.end_line = i
            current = None
            continue

        if REFERENCE_ONLY_RE.search(line):
            current.reference_only = True

        if in_files_list:
            if m := SUB_BULLET_RE.match(line):
                current.files.append((m.group(1) or m.group(2)).strip())
                continue
            in_files_list = False

        if m := LABELLED_PARA_RE.match(line):
            close_para()
            para = m.group(1)
            para_buf = [m.group(2)]
            continue
        if para is not None:
            para_buf.append(line)
            continue

        if m := TITLE_RE.match(line):
            current.title = m.group(1)
        elif FILES_HEADER_RE.match(line):
            in_files_list = True
        elif m := FILE_BULLET_RE.match(line):
            current.files.append((m.group(1) or m.group(2)).strip())
        elif m := TEXT_BULLET_RE.match(line):
            current.files.append((m.group(1) or m.group(2)).strip())
        elif m := FOCUS_RE.match(line):
            current.focus = m.group(1)
        elif m := ONE_LINER_RE.match(line):
            current.one_liner = m.group(1)
        elif m := INDEX_LABEL_RE.match(line):
            current.index_label = m.group(1)
        elif m := RELATED_RE.match(line):
            current.related_field_name = m.group(1)
            current.related = BACKTICK_SLUG_RE.findall(m.group(2))
    close_para()
    if current is not None:
        current.end_line = len(lines)
    return entries


def completeness_signals(e: Entry) -> list[str]:
    signals: list[str] = []
    if e.summary_words < SUMMARY_FLOOR:
        signals.append(
            f"Summary is {e.summary_words} words (< {SUMMARY_FLOOR}) — read the paper before condensing"
        )
    if not e.has_key_findings:
        signals.append("No Key findings (or Key claims/results) paragraph")
    elif not re.search(r"\d", e.key_findings_text):
        signals.append("Key findings carry no numerical result")
    if not e.has_relevance:
        signals.append("No Relevance paragraph")
    if e.focus is None:
        signals.append("No Focus field")
    if e.one_liner is None:
        signals.append("No One-liner field")
    if e.related_field_name and e.related_field_name != "Related":
        signals.append(f"Related field uses legacy name '{e.related_field_name}' — rename to Related")
    return signals


def _split_cells(row: str) -> list[str]:
    inner = row.strip()
    if inner.startswith("|"):
        inner = inner[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    return [c.strip() for c in inner.split("|")]


def find_index_rows(index_text: str, key: str, files: list[str]) -> list[IndexRow]:
    rows: list[IndexRow] = []
    basenames = [Path(f).name for f in files]
    for i, line in enumerate(index_text.splitlines(), start=1):
        if not TABLE_ROW_RE.match(line):
            continue
        cells = _split_cells(line)
        if not cells or set(cells[0]) <= {"-", ":", " "}:
            continue
        matched_by = None
        if (m := SLUG_CELL_RE.match(cells[0])) and m.group(1) == key:
            matched_by = "slug"
        elif basenames and any(b in line for b in basenames):
            matched_by = "filename"
        if matched_by:
            rows.append(
                IndexRow(
                    line=i,
                    text=line,
                    cells=cells,
                    cell_word_counts=[word_count(c) for c in cells],
                    matched_by=matched_by,
                )
            )
    return rows


def dangling_related(entries: list[Entry]) -> dict[str, list[str]]:
    keys = {e.key for e in entries}
    return {
        e.key: [s for s in e.related if s not in keys]
        for e in entries
        if any(s not in keys for s in e.related)
    }


def resolve_key(entries: list[Entry], key: str) -> Entry | None:
    exact = [e for e in entries if e.key == key]
    if len(exact) == 1:
        return exact[0]
    loose = [e for e in entries if key.lower() in e.key.lower()]
    return loose[0] if len(loose) == 1 else None


def report_one(root: Path, entries: list[Entry], key: str, out, err) -> int:
    e = resolve_key(entries, key)
    if e is None:
        hits = [x.key for x in entries if key.lower() in x.key.lower()]
        if hits:
            print(f"key {key!r} is ambiguous: {hits}", file=err)
        else:
            print(f"no entry matches {key!r} in PAPER_SUMMARIES.md", file=err)
        return 1
    print(f"### {e.key}  (PAPER_SUMMARIES.md lines {e.line}-{e.end_line}, section: {e.section})", file=out)
    print(f"Title: {e.title or '(none)'}", file=out)
    print(f"Files: {e.files or '(none)'}{'  [reference-only]' if e.reference_only else ''}", file=out)
    print(f"Focus: {e.focus or '(none)'}", file=out)
    n = word_count(e.one_liner) if e.one_liner else None
    print(f"One-liner: {n if n is not None else '-'} words {verdict(n)}", file=out)
    if e.index_label:
        print(f"Index label: {e.index_label}", file=out)
    print(f"Related ({e.related_field_name or 'none'}): {e.related}", file=out)
    dangling = dangling_related([e] + [x for x in entries if x is not e]).get(e.key)
    if dangling:
        print(f"  dangling Related slugs: {dangling}", file=out)
    signals = completeness_signals(e)
    print("Completeness:", "ok" if not signals else "", file=out)
    for s in signals:
        print(f"  - {s}", file=out)

    index_path = root / "PAPER_INDEX.md"
    if not index_path.is_file():
        print("PAPER_INDEX.md: not present in this repo", file=out)
        return 0
    rows = find_index_rows(index_path.read_text(), e.key, e.files)
    if not rows:
        print("Index row: none", file=out)
        return 0
    for r in rows:
        print(f"Index row (line {r.line}, matched by {r.matched_by}):", file=out)
        for cell, n in zip(r.cells, r.cell_word_counts):
            preview = cell if len(cell) <= 90 else cell[:87] + "..."
            print(f"  [{n:>3} words {verdict(n) if n > ONE_LINER_WARN else '  '}] {preview}", file=out)
    return 0


def sweep(root: Path, entries: list[Entry], section: str | None, out) -> int:
    index_text = (root / "PAPER_INDEX.md").read_text() if (root / "PAPER_INDEX.md").is_file() else ""
    dangling = dangling_related(entries)
    print("key\tsection\trow\tfocus\tone-liner\tsignals", file=out)
    for e in entries:
        if section and e.section != section:
            continue
        rows = find_index_rows(index_text, e.key, e.files) if index_text else []
        n = word_count(e.one_liner) if e.one_liner else None
        sig = completeness_signals(e)
        if e.key in dangling:
            sig.append(f"dangling Related: {dangling[e.key]}")
        print(
            f"{e.key}\t{e.section}\trow={'yes' if rows else 'no'}\t"
            f"focus={'yes' if e.focus else 'no'}\tone-liner={n if n is not None else '-'}:{verdict(n)}\t"
            f"{'; '.join(sig) if sig else 'ok'}",
            file=out,
        )
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("root", type=Path, help="repo root containing PAPER_SUMMARIES.md")
    ap.add_argument("key", nargs="?", help="entry heading (slug) to report on")
    ap.add_argument("--sweep", action="store_true", help="one line per entry instead of a single report")
    ap.add_argument("--section", help="with --sweep: restrict to one ## section")
    args = ap.parse_args(argv)

    summaries = args.root / "PAPER_SUMMARIES.md"
    if not summaries.is_file():
        print(f"{summaries} not found", file=sys.stderr)
        return 1
    entries = parse_entries(summaries.read_text())
    if args.sweep:
        return sweep(args.root, entries, args.section, sys.stdout)
    if not args.key:
        ap.error("give a key, or --sweep")
    return report_one(args.root, entries, args.key, sys.stdout, sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
