#!/usr/bin/env python3
"""Write one subagent prompt file per shard for the condense-summary fan-out.

usage::

    python3 fanout_make_prompts.py SHARDS.json [REPO_ROOT] [--out-dir DIR] [--frag-dir DIR]

``SHARDS.json`` is ``{shard: {"section": ..., "keys": [slug, ...]}}`` — at
most ~10 slugs per shard (subagent context peaked at 158k tokens on 12).
For each shard this re-runs the sibling ``condense_check.py --sweep``, drops
slugs whose sweep line is already clean and slugs that are not in
PAPER_SUMMARIES.md (both reported), and writes ``<out-dir>/<shard>.md`` when
anything is left. The orchestrator launches one agent per prompt file; each
agent writes fragments to ``<frag-dir>/<shard>/<slug>.md`` and never edits
tracked files. Apply with ``fanout_apply.py``, check with ``fanout_verify.py``.

Defaults: ``--out-dir /tmp/condense-prompts``, ``--frag-dir /tmp/condense-frag``.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
CONDENSE_DIR = SKILL_DIR.parent / "condense-summary"
CHECKER = CONDENSE_DIR / "condense_check.py"
CONDENSE_SKILL = CONDENSE_DIR / "SKILL.md"
DEFAULT_OUT_DIR = "/tmp/condense-prompts"
DEFAULT_FRAG_DIR = "/tmp/condense-frag"

TEMPLATE = """You are one of {n_agents} parallel subagents condensing PAPER_SUMMARIES.md entries in the repo at
{root}. Work ONLY in that directory.

HARD RULES
- Do NOT edit PAPER_SUMMARIES.md, PAPER_INDEX.md, or any tracked file. Other agents are working on the same file; the orchestrator applies your output serially. Do NOT git commit or git add anything.
- Your shard id is `{shard}`. Write ONE output file per entry: {frag_dir}/{shard}/<slug>.md (mkdir -p first). Put every scratch script or scratch copy you make under {scratch_dir}/{shard}/ — never write outside those two directories, and never loop over or modify files that are not yours (a previous agent's "fix trailing newlines" loop rewrote every other agent's fragments).
- Fragment content is the COMPLETE REPLACEMENT ENTRY BLOCK: from the `### <slug>` heading line through the last line before the entry's CLOSING `---` separator — the `---` that immediately precedes the next `###`/`##` heading (the last entry in a section may have no closing `---`; then stop before the `##` line). Some entries carry an INTERNAL `---` followed by a `**Citation:**` line before that closing separator; that internal `---` + Citation belongs to the entry and MUST stay inside your fragment (do not drop it, do not fold it into metadata). The orchestrator splices by slug, so keep the exact `### <slug>` heading and the `**Title:**` line (fix an obvious typo in the Title if you find one, and say so).
- Use `git -C` if you need git at all (you should not); never `cd ... && git ...`.

THE SKILL
First read {skill_md} in full and follow Steps 1-4 for each entry. Step 5 (index row) is NOT needed — PAPER_INDEX.md rows are generated from the Focus / One-liner / Index label fields by `python3 {paper_index_dir}/paper_index.py index .`. Step 6 verification you do on a scratch copy as described below. Step 7 (commit) is the orchestrator's job.

The checker: `python3 {checker} {root} <slug>` prints the entry's line range, existing fields, word counts, completeness signals. Read the full entry with sed -n '<start>,<end>p' PAPER_SUMMARIES.md.

For each entry:
1. Run the checker; read the whole entry.
2. Decide whether it is complete enough (Summary >= ~80 words, Key findings with a number for empirical work, Relevance paragraph). If not, open the source — `papers/text/<file>.txt` for the File bullet's PDF, or the .md capture — and enrich the entry: thesis, the one or two numbers that carry it, why it matters for this collection. Reference-only entries with no local source: condense from what is there, say so inside the entry and in your report.
3. Add `- **Focus:**` (2-5 words; check the vocabulary existing Focus fields use: `grep -h '^- \\*\\*Focus:\\*\\*' PAPER_SUMMARIES.md | sort | uniq -c | sort -rn | head -40`) and `- **One-liner:**` (<= 50 words, a thesis with the number that carries it, no hedging, no "this paper examines") directly after the File / Files / Text extraction / Local file bullet. Add `- **Index label:** Surname (Org) (Year)` after the One-liner ONLY if the `**Title:**` line has no trailing `(Author — Org, Year)`-style parenthetical (check `{paper_index_dir}/gen_index.py`'s label regexes if unsure).
4. Rename any legacy cross-reference field (`Relationship to other repo entries`, `Cross-references (in this collection)`, `Cross-references in this collection`, `Companions in this collection`) to `- **Related:**` with backticked slugs that exist as `### ` headings in THIS repo's PAPER_SUMMARIES.md. The checker only sees `Related` when it sits in the metadata bullet block above the Summary.
5. Write {frag_dir}/{shard}/<slug>.md. Then VERIFY: copy PAPER_SUMMARIES.md and PAPER_INDEX.md to {scratch_dir}/{shard}/, splice your fragment in place of the original block in the copy (python is fine), and run the checker against that scratch directory: One-liner must read OK (<= 50 words), Focus present, no completeness signals you did not deliberately leave (row=no is expected and fine). Fix and re-verify until clean.

Checker quirks learned in earlier waves: (a) the Key-findings regex only matches labels of letters/spaces plus one optional parenthetical — a digit, `/`, or em-dash in the label (e.g. `**Key findings — explanatory:**`) makes it read as missing; rename the label rather than adding content. (b) Unrecognized bold labels (`**Central claim:**`, `**Why it matters:**`) are absorbed into the preceding paragraph's word count, so relabeling them can expose a Summary under the 80-word floor — expand the Summary from source, don't reorder paragraphs to game it. (c) A "No Key findings" signal on a rich entry is usually (a), not missing content — check the heading text before reading the paper.

Count words with the checker, not by eye. Study the calibration examples at the bottom of the skill file — that is the target register.

YOUR ASSIGNMENT — {section} ({n} entries):
{keys}

FINAL REPORT (keep it short): for each slug — the Focus, the One-liner with its checker word count, whether you read the source (and which file), what you enriched, any factual correction you made to existing content, and any problem you could not fix. Then one line: approximate number of tool calls you made.
"""


def sweep_signals(root: Path) -> dict[str, str]:
    """slug -> the sweep's signals column ('ok' when nothing is flagged)."""
    out = subprocess.run(
        [sys.executable, str(CHECKER), str(root), "--sweep"],
        capture_output=True, text=True,
    ).stdout
    signals: dict[str, str] = {}
    for line in out.splitlines()[1:]:
        parts = line.split("\t")
        if len(parts) == 6:
            signals[parts[0]] = parts[5]
    return signals


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("shards", help="shards JSON: {shard: {section, keys}}")
    ap.add_argument("root", nargs="?", default=".", help="repo root (default: cwd)")
    ap.add_argument("--out-dir", default=DEFAULT_OUT_DIR)
    ap.add_argument("--frag-dir", default=DEFAULT_FRAG_DIR)
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    shards = json.loads(Path(args.shards).read_text(encoding="utf-8"))
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    frag_dir = Path(args.frag_dir)
    scratch_dir = frag_dir.parent / (frag_dir.name.replace("frag", "scratch") if "frag" in frag_dir.name else frag_dir.name + "-scratch")

    signals = sweep_signals(root)
    work: dict[str, list[str]] = {}
    for shard, d in sorted(shards.items()):
        missing = [k for k in d["keys"] if k not in signals]
        clean = [k for k in d["keys"] if k in signals and signals[k] == "ok"]
        keys = [k for k in d["keys"] if k in signals and signals[k] != "ok"]
        if missing:
            print(f"{shard}: dropped {len(missing)} not in PAPER_SUMMARIES.md: {', '.join(missing)}")
        if not keys:
            print(f"{shard}: nothing left to do ({len(clean)} clean) — skip")
            continue
        work[shard] = keys
        if clean:
            print(f"{shard}: skipped {len(clean)} already-clean: {', '.join(clean)}")

    for shard, keys in work.items():
        key_lines = "\n".join(f"- `{k}` — sweep signals: {signals[k]}" for k in keys)
        txt = TEMPLATE.format(
            n_agents=len(work),
            root=root,
            shard=shard,
            frag_dir=frag_dir,
            scratch_dir=scratch_dir,
            skill_md=CONDENSE_SKILL,
            checker=CHECKER,
            paper_index_dir=SKILL_DIR,
            section=shards[shard]["section"],
            n=len(keys),
            keys=key_lines,
        )
        (out / f"{shard}.md").write_text(txt, encoding="utf-8")
        print(f"{shard}: {len(keys):2d} entries — {shards[shard]['section']}")
    print(
        f"\n{len(work)} prompt(s) in {out}/ ; launch one Agent per file "
        "(subagent_type=general-purpose, a strong model), all in one message"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
