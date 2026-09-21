---
name: paper-index
description: Use when a paper-collection repo's PAPER_INDEX.md or PAPER_RELATED.md needs regenerating or checking against PAPER_SUMMARIES.md, or when adding the pre-commit hook to such a repo. Bundles the stdlib-only paper_index.py tool (index, check, counts).
---

`{{skills_dir}}` is `~/.claude/skills` on Claude Code and `/home/claude/.claude_researcher_template/template/skills` in the claude.ai sandbox.
Sandbox-specific notes (REST for Issues/Pulls, the post-commit push hook) are in RESEARCHER.md.

<required>
CRITICAL: Add the following steps to your task list:

1. After editing any PAPER_SUMMARIES.md entry, run `index` — never hand-edit a generated block
2. Before committing, run `check`; fix what it reports in the entry, then `index` again
3. Stage PAPER_SUMMARIES.md, PAPER_INDEX.md and PAPER_RELATED.md together
</required>

Announce at start: "I'm using the paper-index skill to regenerate/check the index."

PAPER_SUMMARIES.md is the source of truth: one `### <slug>` entry per paper carrying the metadata bullets below. Everything else is derived from it by the tool — PAPER_INDEX.md's marker-scoped blocks (counts, Quick Reference table, section list), PAPER_RELATED.md (the reverse index of `Related`), and PAPER_SUMMARIES.md's own header count line. Edit entries, not rows.

## Commands

```
python3 {{skills_dir}}/paper-index/paper_index.py index .              # rewrite the generated files
python3 {{skills_dir}}/paper-index/paper_index.py check .              # exit 1 if stale or inconsistent (strict)
python3 {{skills_dir}}/paper-index/paper_index.py check --no-strict .  # missing Focus/One-liner only warns
python3 {{skills_dir}}/paper-index/paper_index.py counts .             # counts + problems, no exit code
```

The python form is the only form — there is no Makefile (dropped 2026-09-17; `make` is absent on the web sandbox anyway). Stdlib only, Python 3.9+ — whatever `python3` is on PATH.

`check` runs two checks and exits with the first non-zero: the generated files must equal a fresh render (strict: every entry has Focus + One-liner and a derivable Paper label, no `Related` slug dangles, no One-liner over 60 words), then the counts must reconcile (every File/Text ref resolves, no unreferenced PDF under `papers/`, every top-level `papers/*.pdf` has a `papers/text/` extraction, the header claims match).

## Tool locator

The hook finds the tool in this order: `$PAPER_INDEX_DIR`, then `/home/claude/.claude_researcher_template/template/skills/paper-index` (web clone), then `$HOME/.claude/skills/paper-index` (Claude Code). The hook skips with a message when none exists — a collaborator without the skill can still commit.

## The metadata contract

An entry is `### <slug>` (kebab-case, stable once merged), then `**Title:** <title> (<authors>, <year> — <org>)`, then the bullets:

```
- **Authors:** ...
- **Date:** ...
- **File:** `<name>.pdf`            # or **Files:** + indented sub-bullets; or **Text extraction:** `papers/text/<name>.md` for web captures
- **Source:** ...
- **Focus:** 2-5 words
- **One-liner:** ≤50-word thesis with the number that carries it (warn >50, fail >60)
- **Related:** `slug-a`, `slug-b`   # only slugs that exist in this repo
- **Index label:** Surname (Org) (Year)   # ONLY when the Title parenthetical does not parse
- **Summarized:** YYYY-MM-DD
```

Rules the tool enforces (from `gen_index.py`):
- Row order is section order, then entry order, as in PAPER_SUMMARIES.md.
- Key Contribution = One-liner. Paper = Index label, else derived from the Title parenthetical `(<authors> — <org>, <year>)` or `(<authors>, <year> — <org>)` → `<authors> (<org>) (<year>)`, `(<authors>, <year>)` → `<authors> (<year>)`, where `<year>` is a plain 4-digit year (optionally `2024a` or `2024/2025`) and `<org>` is copied verbatim; anything else does not parse and is reported. File = first file (+N for multi-part), the text path for text-only entries, `—` for reference-only.
- Entries missing Focus or One-liner are reported and omitted (warning; error under strict). A `Related` slug naming no entry is always an error. A `###` above the first `##` is an error.
- An entry is local (a File ref resolves to a PDF), text-only (only a text ref resolves), reference-only (the block says `reference-only`), else unclassified — which fails.

The body is free-form; keep a `Key findings:` paragraph with a number (empirical papers) and a `Relevance:` paragraph — the `condense-summary` skill's checker reads those.

## Per-repo config — `paper_index.toml` (optional)

```toml
[paths]
extra_pdf_dirs = ["blogs", "gladstone"]     # refs also resolve under these roots
exempt_dirs = ["papers/org_docs"]           # PDFs catalogued elsewhere; skipped by the unreferenced sweep
pending_index = "papers/pending_index.txt"  # PDFs awaiting summaries; stale lines fail
```

## Setting up a repo

1. Markers. PAPER_INDEX.md needs three pairs, PAPER_SUMMARIES.md one; each `<!-- BEGIN GENERATED: <name> -->` … `<!-- END GENERATED: <name> -->` on its own lines, exactly once. Names: `counts`, `quick-reference`, `section-list` (INDEX); `summaries-header` (SUMMARIES). The tool never invents markers — a file without them is left alone.
2. Hook: `mkdir -p .githooks && python3 {{skills_dir}}/paper-index/paper_index.py --print-hook > .githooks/pre-commit && chmod +x .githooks/pre-commit && git config core.hooksPath .githooks`. The hook is tracked; `core.hooksPath` is per-clone, so every fresh clone (web sessions included) runs the `git config` line once. It is check-only: it refuses a commit whose staged PAPER_SUMMARIES.md disagrees with the generated files, and a commit whose regenerated files are fresh on disk but unstaged.
3. `index`, then `check`; commit the three files together.

`init-research-repo` does 1–2 for a new repo.

## Condense fan-out (many entries at once)

```
python3 {{skills_dir}}/paper-index/fanout_make_prompts.py shards.json . --out-dir /tmp/condense-prompts --frag-dir /tmp/condense-frag
python3 {{skills_dir}}/paper-index/fanout_apply.py . --frag /tmp/condense-frag            # dry run; add --apply to write
python3 {{skills_dir}}/paper-index/fanout_verify.py . /tmp/condense-frag
```

`shards.json` is `{shard: {"section": ..., "keys": [slugs]}}`, ≤10 slugs per shard. Launch one subagent per prompt file, all in one message; agents write fragments and never touch tracked files. After each wave: apply, verify, `index`, `check`, commit with the slugs in the subject.
