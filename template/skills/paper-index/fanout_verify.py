#!/usr/bin/env python3
"""Run the sibling condense_check.py on each slug in a fragment directory.

usage::

    python3 fanout_verify.py REPO_ROOT FRAG_DIR

One line per fragment (``<frag-dir>/*.md`` and ``<frag-dir>/*/*.md``): the
One-liner verdict and the Completeness line as the checker reports them for
the entry now in PAPER_SUMMARIES.md; entries the checker still flags carry a
``<-- CHECK`` marker. Exit 1 iff any is flagged.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
CHECKER = SKILL_DIR.parent / "condense-summary" / "condense_check.py"
VERDICTS = ("OK", "WARN", "FAIL", "MISSING")


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2:
        print(__doc__.split("\n\n")[1].strip(), file=sys.stderr)
        return 2
    root, frag_dir = argv
    frags = sorted(list(Path(frag_dir).glob("*.md")) + list(Path(frag_dir).glob("*/*.md")))
    bad = 0
    for p in frags:
        out = subprocess.run(
            [sys.executable, str(CHECKER), root, p.stem],
            capture_output=True, text=True,
        ).stdout
        one_liner = next(
            (
                l.strip()
                for l in out.splitlines()
                if "One-liner" in l and any(v in l for v in VERDICTS)
            ),
            "?",
        )
        completeness = next(
            (l.strip() for l in out.splitlines() if l.strip().startswith("Completeness")),
            "?",
        )
        flag = "" if ("OK" in one_liner and completeness.endswith("ok")) else "  <-- CHECK"
        if flag:
            bad += 1
        print(f"{p.stem:45s} {one_liner[:40]:40s} {completeness[:70]}{flag}")
    print("flagged:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
