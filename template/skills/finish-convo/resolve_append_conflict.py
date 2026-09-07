#!/usr/bin/env python3
"""Resolve append-on-top merge conflicts by keeping both sides (HEAD first, then incoming).

## What this script does

For a file with one or more git merge-conflict regions of the shape:

    <<<<<<< HEAD
    <lines from this branch>
    =======
    <lines from incoming branch>
    >>>>>>> origin/whatever

…rewrites each region to drop the markers and concatenate the two blocks (HEAD
side first, then incoming side). No content from either side is dropped.

## When this is safe

This resolution is **only correct** when both sides legitimately added their
own content in the same region and the union of both blocks is the right
final state. The canonical cases, by workflow mode:

- **`branches` mode:** STATUS.md's lifecycle tables — two concurrent
  ceremonies both appending a row to `## Active Research Lines` (two
  `start-research-line` invocations) or `## Archived Research Lines` (two
  merge ceremonies). Both rows must survive; row order in these tables does
  not encode precedence.
- **`main_only` mode:** STATUS.md's `## Recent Sessions` section — session A
  adds a one-liner on top, session B adds a one-liner on top, the merge
  wants both present.
- **Either mode:** RESEARCH_LOG.md's newest-first session entries when the
  same branch is worked from two sessions.

Each contributor's block stays internally chronological; the newest-first
invariant holds within each block, though absolute chronology across
contributors may not interleave perfectly. That's the expected shape for a
multi-committer running ledger.

## When this is NOT safe

This script does NOT understand the semantics of the conflicting content.
**Do not run on conflicts where:**
- Both sides modify the same logical line (the resulting "keep both" would
  produce duplicated or contradictory state).
- The file has structured constraints (JSON/YAML/TOML, source code, etc.)
  where concatenating two diverging blocks produces a parse error or
  semantic incoherence.
- The conflict is in a structured table where row order matters (e.g., a
  config file whose order encodes precedence). Markdown ledger tables whose
  rows are independent (the STATUS.md lifecycle tables above) are fine; the
  unsafe case is order-as-semantics.
- One side *deleted* lines the other side kept or edited (e.g., a merge
  ceremony's Active-row removal tangled with a neighboring edit) — keeping
  both would resurrect the deleted content.

Limit usage to multi-committer running ledgers like STATUS.md, RESEARCH_LOG
sections, or other append-on-top text files. Surface any other shape to the
user.

## Usage

    python3 resolve_append_conflict.py <path/to/file>

Sanity-checks that no conflict markers remain after writing. Exits non-zero
if any are detected (e.g., the file had a malformed conflict region).

## When invoking from a skill

A skill that wants to use this script should:
1. Confirm the conflict is the append-on-top shape (e.g., by inspecting the
   conflicted file and verifying both sides' content is in a list-on-top
   region with no overlap on shared lines).
2. Run this script.
3. After resolution, `git add` the file to mark it resolved, run any
   relevant tests, and commit the merge.

The skill should NOT run this script reflexively on any conflict — only when
the append-on-top shape is confirmed. The user's CLAUDE.md may explicitly
forbid auto-resolving conflicts on shared files in general; STATUS.md is an
explicit carve-out.
"""

from __future__ import annotations

import sys
from pathlib import Path


def resolve_append_conflicts(text: str) -> tuple[str, int, int, int]:
    """Resolve all <<<<<<<…=======…>>>>>>> blocks by keeping both sides.

    Returns (new_text, n_conflicts_resolved, head_lines_kept, incoming_lines_kept).
    Raises ValueError if a conflict region is malformed (e.g., orphan marker).
    """
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    i = 0
    n_conflicts = 0
    head_lines_kept = 0
    incoming_lines_kept = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("<<<<<<< "):
            # Find the matching ======= and >>>>>>>.
            head_start = i + 1
            sep_idx = None
            end_idx = None
            j = head_start
            while j < len(lines):
                if lines[j].startswith("======="):
                    sep_idx = j
                elif lines[j].startswith(">>>>>>> "):
                    end_idx = j
                    break
                j += 1
            if sep_idx is None or end_idx is None:
                raise ValueError(
                    f"Malformed conflict region starting at line {i + 1}: "
                    f"missing ======= or >>>>>>> marker."
                )
            head_block = lines[head_start:sep_idx]
            incoming_block = lines[sep_idx + 1 : end_idx]
            out.extend(head_block)
            out.extend(incoming_block)
            n_conflicts += 1
            head_lines_kept += len(head_block)
            incoming_lines_kept += len(incoming_block)
            i = end_idx + 1
        else:
            out.append(line)
            i += 1
    return "".join(out), n_conflicts, head_lines_kept, incoming_lines_kept


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} <path/to/file>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 1
    original = path.read_text()
    if "<<<<<<< " not in original:
        print(f"No conflict markers found in {path}; nothing to do.")
        return 0
    try:
        resolved, n_conflicts, head_kept, incoming_kept = resolve_append_conflicts(original)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    # Sanity-check no markers remain (a well-formed input shouldn't leave any).
    if "<<<<<<< " in resolved or ">>>>>>> " in resolved:
        print(
            "ERROR: conflict markers remain after resolution — file may have "
            "malformed regions. Not writing.",
            file=sys.stderr,
        )
        return 1
    path.write_text(resolved)
    print(
        f"Resolved {n_conflicts} conflict region(s) in {path}: "
        f"kept {head_kept} HEAD line(s) + {incoming_kept} incoming line(s)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
