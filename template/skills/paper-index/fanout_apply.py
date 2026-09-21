#!/usr/bin/env python3
"""Serially splice replacement entry blocks into PAPER_SUMMARIES.md.

usage::

    python3 fanout_apply.py REPO_ROOT [--frag DIR] [--apply] [--only slug1,slug2]

Fragments are ``<slug>.md`` files in the fragment directory or any immediate
subdirectory (one per shard); subdirectories named ``applied-*`` are skipped.

Entry block = ``### <slug>`` line through the line before the closing ``---``
that precedes the next ``###``/``##`` heading (entries may contain an
internal ``---`` before a Citation line, so the boundary is the next heading,
not the first ``---``). Fragments may or may not include the closing ``---``;
it is stripped either way and the file's own closing separator is kept. If
the original block ends with an internal ``---`` + ``**Citation:**`` tail and
the fragment has no Citation line, the tail is carried over.

Validates each fragment before writing:
  - first line is ``### <slug>`` and matches the filename
  - slug exists exactly once in PAPER_SUMMARIES.md
  - fragment keeps a ``**Title:**`` line and contains Focus + One-liner bullets
  - fragment contains no ``## `` / other ``### `` heading; one-liner <= 60 words
Dry-run by default; ``--apply`` writes. Exit 1 when any fragment was rejected
(valid ones are still applied under ``--apply``).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

DEFAULT_FRAG_DIR = "/tmp/condense-frag"
HEAD = re.compile(r"^### (\S+)\s*$")


def is_heading(line: str) -> bool:
    return line.startswith("### ") or line.startswith("## ")


def strip_close(seq: list[str]) -> int:
    """Index after the last content line: drops trailing blanks and one
    trailing ``---`` (plus blanks)."""
    e = len(seq)
    while e > 0 and seq[e - 1].strip() == "":
        e -= 1
    if e > 0 and seq[e - 1].strip() == "---":
        e -= 1
        while e > 0 and seq[e - 1].strip() == "":
            e -= 1
    return e


def has_citation(seq: list[str]) -> bool:
    return any(line.startswith("**Citation:**") for line in seq)


def find_blocks(lines: list[str]) -> dict[str, list[tuple[int, int]]]:
    blocks: dict[str, list[tuple[int, int]]] = {}
    for i, slug in [(i, m.group(1)) for i, l in enumerate(lines) if (m := HEAD.match(l))]:
        h = i + 1
        while h < len(lines) and not is_heading(lines[h]):
            h += 1
        blocks.setdefault(slug, []).append((i, i + strip_close(lines[i:h])))
    return blocks


def list_fragments(frag_dir: Path) -> list[Path]:
    return sorted(
        p
        for p in list(frag_dir.glob("*.md")) + list(frag_dir.glob("*/*.md"))
        if not p.name.startswith("_") and not p.parent.name.startswith("applied-")
    )


def validate(slug: str, body: list[str], blocks) -> list[str]:
    probs: list[str] = []
    m = HEAD.match(body[0]) if body else None
    if not m or m.group(1) != slug:
        probs.append(f"first line is not '### {slug}'")
    if slug not in blocks:
        probs.append("slug not found in PAPER_SUMMARIES.md")
    elif len(blocks[slug]) != 1:
        probs.append(f"slug appears {len(blocks[slug])} times")
    if not any(l.startswith("**Title:**") for l in body):
        probs.append("no **Title:** line")
    if not any(l.startswith("- **Focus:**") for l in body):
        probs.append("no Focus bullet")
    ol = [l for l in body if l.startswith("- **One-liner:**")]
    if not ol:
        probs.append("no One-liner bullet")
    nw = len(ol[0].split("**One-liner:**", 1)[1].split()) if ol else 0
    if nw > 60:
        probs.append(f"one-liner {nw} words (>60 hard fail)")
    for k, l in enumerate(body[1:], 2):
        if is_heading(l):
            probs.append(f"line {k} is a heading: {l[:40]!r}")
            break
    return probs


def one_liner_words(body: list[str]) -> int:
    ol = [l for l in body if l.startswith("- **One-liner:**")]
    return len(ol[0].split("**One-liner:**", 1)[1].split()) if ol else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("root")
    ap.add_argument("--frag", default=DEFAULT_FRAG_DIR)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", default="")
    a = ap.parse_args(argv)

    root = Path(a.root)
    summ = root / "PAPER_SUMMARIES.md"
    lines = summ.read_text(encoding="utf-8").split("\n")
    only = set(filter(None, a.only.split(",")))
    blocks = find_blocks(lines)

    ok, bad = [], []
    for p in list_fragments(Path(a.frag)):
        slug = p.stem
        if only and slug not in only:
            continue
        raw = p.read_text(encoding="utf-8").split("\n")
        body = raw[: strip_close(raw)]
        probs = validate(slug, body, blocks)
        if probs:
            bad.append((slug, probs))
            continue
        s, e = blocks[slug][0]
        old = lines[s:e]
        if has_citation(old) and not has_citation(body):
            k = max(i for i, l in enumerate(old) if l.startswith("**Citation:**"))
            j = k
            while j > 0 and old[j - 1].strip() != "---":
                j -= 1
            tail = old[j - 1 :] if j > 0 else old[k:]
            while tail and tail[0].strip() == "":
                tail = tail[1:]
            body = body + [""] + tail
            print(f"note   {slug}: carried over {len(tail)}-line Citation tail")
        ok.append((slug, s, e, body, one_liner_words(body), p))

    dup = {slug for slug, n in Counter(t[0] for t in ok).items() if n > 1}
    if dup:
        bad.extend((slug, ["delivered by more than one fragment file"]) for slug in sorted(dup))
        ok = [t for t in ok if t[0] not in dup]
    for slug, probs in bad:
        print(f"REJECT {slug}: " + "; ".join(probs))
    for slug, s, e, body, nw, p in ok:
        print(
            f"OK     {slug}: lines {s + 1}-{e} ({e - s} -> {len(body)} lines), "
            f"one-liner {nw} words  [{p.parent.name}]"
        )

    if a.apply and ok:
        for slug, s, e, body, _, _ in sorted(ok, key=lambda t: -t[1]):
            lines[s:e] = body
        summ.write_text("\n".join(lines), encoding="utf-8")
        print(f"applied {len(ok)} fragments")
    elif not a.apply:
        print(f"dry run: {len(ok)} would apply, {len(bad)} rejected")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
