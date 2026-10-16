#!/usr/bin/env python3
"""paper-index — one entry point for the paper-collection index tool.

PAPER_SUMMARIES.md is the source of truth (one ``### <slug>`` entry per
paper, carrying the metadata bullets). Everything else is generated from it:
PAPER_INDEX.md's marker-scoped blocks, PAPER_RELATED.md, and the header count
line of PAPER_SUMMARIES.md itself when it carries the markers.

Usage::

    python3 paper_index.py index [<root>]                rewrite the generated files
    python3 paper_index.py check [--no-strict] [<root>]  exit 1 if anything is stale or inconsistent
    python3 paper_index.py counts [<root>]               print counts and problems
    python3 paper_index.py --print-hook                  the .githooks/pre-commit a repo should carry

``check`` runs the index check (strict unless ``--no-strict``: every entry
needs Focus + One-liner and a derivable Paper label) and then the count
reconciliation; its exit code is the first non-zero of the two. Stdlib only,
Python 3.9+ (a stock macOS ``python3`` works; ``tomllib`` is used when the
interpreter has it). Per-repo settings live in ``paper_index.toml`` — see
``count_papers.py``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:  # installed copies are symlinks; find the siblings
    sys.path.insert(0, str(HERE))

import count_papers  # noqa: E402
import gen_index  # noqa: E402

HOOK = """\
#!/bin/sh
# Check-only: refuses a commit whose staged PAPER_SUMMARIES.md is out of step
# with the generated index. Never rewrites anything. Fix: run
#   python3 $PAPER_INDEX_DIR/paper_index.py index .
# and re-stage. Locator: $PAPER_INDEX_DIR, the web template clone, then ~/.claude/skills.
case "$(git diff --cached --name-only)" in
  *PAPER_SUMMARIES.md*|*PAPER_INDEX.md*|*PAPER_RELATED.md*|*.pdf*|*paper_index.toml*) ;;
  *) exit 0 ;;
esac
DIR="${PAPER_INDEX_DIR:-}"
[ -z "$DIR" ] && [ -d /home/claude/.claude_researcher_template/template/skills/paper-index ] && DIR=/home/claude/.claude_researcher_template/template/skills/paper-index
[ -z "$DIR" ] && [ -d "$HOME/.claude/skills/paper-index" ] && DIR="$HOME/.claude/skills/paper-index"
if [ -z "$DIR" ]; then echo "pre-commit: paper-index tool not found; skipping check" >&2; exit 0; fi
python3 "$DIR/paper_index.py" check . || { echo "pre-commit: generated index is stale — run 'python3 $DIR/paper_index.py index .' and re-stage" >&2; exit 1; }
# The check above reads the working tree. Refuse if the generated files are
# fresh on disk but not in the index — the commit would still carry the stale copy.
git diff --quiet -- PAPER_SUMMARIES.md PAPER_INDEX.md PAPER_RELATED.md || { echo "pre-commit: PAPER_SUMMARIES/INDEX/RELATED have unstaged changes — stage them (the commit would carry the stale copy)" >&2; exit 1; }
"""


def cmd_index(root: str) -> int:
    return gen_index.main([root])


def cmd_check(root: str, strict: bool) -> int:
    rc_index = gen_index.main(["--check", *(["--strict"] if strict else []), root])
    rc_counts = count_papers.main(["--check", root])
    return rc_index or rc_counts


def cmd_counts(root: str) -> int:
    return count_papers.main([root])


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="paper_index.py", description=__doc__.splitlines()[0]
    )
    ap.add_argument("--print-hook", action="store_true", help="emit the pre-commit hook text")
    sub = ap.add_subparsers(dest="command")

    p = sub.add_parser("index", help="rewrite the generated files")
    p.add_argument("root", nargs="?", default=".")
    p = sub.add_parser("check", help="exit 1 if stale or inconsistent")
    p.add_argument("--no-strict", action="store_true", help="missing Focus/One-liner only warns")
    p.add_argument("root", nargs="?", default=".")
    p = sub.add_parser("counts", help="print counts and problems")
    p.add_argument("root", nargs="?", default=".")

    args = ap.parse_args(argv)
    if args.print_hook:
        sys.stdout.write(HOOK)
        return 0
    if args.command == "index":
        return cmd_index(args.root)
    if args.command == "check":
        return cmd_check(args.root, strict=not args.no_strict)
    if args.command == "counts":
        return cmd_counts(args.root)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
