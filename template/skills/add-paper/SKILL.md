---
name: add-paper
description: Use when adding a paper (or a blog post or thread worth keeping) to the research collection — obtain the source, extract text, write its PAPER_SUMMARIES.md entry in the metadata contract, then regenerate and check the index with paper-index.
---

`{{skills_dir}}` is `~/.claude/skills` on Claude Code and `/home/claude/.claude_researcher_template/template/skills` in the claude.ai sandbox.
Sandbox-specific notes (REST for Issues/Pulls, the post-commit push hook) are in RESEARCHER.md.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Obtain the source
2. Extract text
3. Write the PAPER_SUMMARIES.md entry (check slug uniqueness first)
4. Generate and check the index
5. Stage all new files
</required>

# Adding a Paper

PAPER_SUMMARIES.md is the source of truth. PAPER_INDEX.md and PAPER_RELATED.md are generated from it by the `paper-index` tool — you write the entry, the tool writes the rows. A repo with no generated-block markers in PAPER_INDEX.md is not set up yet: run `init-paper-collection` first (new collection) or stop and tell the user (legacy format — that is a migration).

## Step 1: Obtain the source

- URL: `curl -L -o papers/<filename>.pdf <url>`
- Local path: copy to `papers/`
- Named only: search, confirm the URL before downloading

**Filename.** If the user's personal info (`personal_info.md`, or the user section of CLAUDE.md on Claude Code) sets **`Paper naming format`** under Operating preferences, use it. Otherwise the default: `AuthorLast_Year__short_description.pdf` — double underscore, snake_case description (`Acemoglu_2024__simple_macroeconomics_AI.pdf`). If the user has no format set, ask once and offer to save their answer there.

**Not a PDF** (blog post, X thread): print it to PDF where you can and treat it as a paper. Otherwise save the text as `papers/text/<filename>.md` and use a `- **Text extraction:**` bullet in place of `File:` in Step 3; the tool classifies the entry as text-only.

## Step 2: Extract text

```bash
pdftotext papers/<filename>.pdf papers/text/<filename>.txt
# or, without pdftotext:
python3 -m pymupdf convert -output papers/text/<filename>.txt papers/<filename>.pdf
```

If neither works, read the PDF directly and write the text yourself. Check the first ~20 lines aren't garbled.

<system-reminder>Always extract, even when the current task doesn't need the text — `check` fails on a PDF with no extraction, and future sessions can't search the paper without it.</system-reminder>

## Step 3: Write the entry

### Slug rules

The slug is the entry's `### ` heading and the key everything generated hangs off.

1. **Format:** kebab-case, lowercase, `[a-z0-9-]+` (`sleeper-agents`, `emergent-misalignment`).
2. **Uniqueness (mandatory):** `grep -n '^### <slug>$' PAPER_SUMMARIES.md` must print nothing.
3. **Source of the name:** the paper's common name; if none, `<authorlast>-<yearsuffix>-<topic>` (`hubinger-24-sleepers`). Not the filename.
4. **Stable after commit.** Other entries' `Related` bullets point at it; see Common Mistakes before renaming.
5. **On removal:** delete the entry, run Step 4. The rows go with it.

### The entry

Read the paper from `papers/text/`. Put the entry in the `## ` section where it belongs (create one if needed), closed by a `---` line like its neighbours:

```markdown
### <slug>

**Title:** <Paper title> (<Authors>, <Year> — <Org>)

- **Authors:** Names (Affiliations)
- **Date:** Month Year
- **File:** `<filename>.pdf`
- **Source:** <URL or DOI>
- **Focus:** <2–5 words, in the vocabulary the repo's Focus column already uses>
- **One-liner:** <≤50-word thesis with the one number that carries it>
- **Related:** `slug-a`, `slug-b`
- **Summarized:** <model name>, YYYY-MM-DD

**Summary:** 2–3 sentences on the core contribution and approach.

**Key findings:**
- Finding with its number and context — what was measured, on what, against what baseline
- Range estimate where the paper gives one

**Relevance:** 1–2 sentences on why this paper matters for this collection.

---
```

- The Title parenthetical is what the tool turns into the index's Paper cell. If it can't take the `(<Authors>, <Year> — <Org>)` shape, add `- **Index label:** Surname (Org) (Year)` after the One-liner — only then.
- `Related` names only slugs that exist in this file; omit the bullet if there are none.
- Write the One-liner last, from the entry, per the `condense-summary` skill. Empirical papers need at least one number in Key findings.
- `Summarized:` is the model that wrote the summary (a subagent's own model when it writes) and the date. Re-summarizing replaces it.
- Institutional reports (no abstract, no research question, synthesis rather than new estimates): if your profile has `paper-processing-institutional`, follow its fuller (a)–(d) body and extraction rules; the header above still applies.

## Step 4: Generate and check

```bash
python3 {{skills_dir}}/paper-index/paper_index.py index .
python3 {{skills_dir}}/paper-index/paper_index.py check .
```

Never hand-edit between `GENERATED` markers. Fix what `check` reports in the entry, then run `index` again.

## Step 5: Stage

```bash
git add papers/<filename>.pdf papers/text/<filename>.txt PAPER_SUMMARIES.md PAPER_INDEX.md PAPER_RELATED.md
```

Do NOT commit — the user may be adding several papers or want to review first. The repo's pre-commit hook re-runs the check.

# Adding Several Papers

For 1–3 papers, take each through Steps 1–3 in turn, then run Step 4 once. For 4 or more, use fragments: parallel agents must never write PAPER_SUMMARIES.md, because concurrent writes clobber each other.

1. **One subagent per paper.** It obtains the source, extracts text, reads it, and writes the complete entry to `<slug>.summary.md` in a gitignored scratch dir (e.g. `data/summaries-frag/`). Give each agent this skill's Step 3 and one existing entry as a style reference; have it check its slug against PAPER_SUMMARIES.md.
2. **The orchestrator inserts serially.** One pass, Edit tool, each fragment into its section, rejecting duplicate slugs. (`paper-index`'s `fanout_apply.py` replaces existing entries only — it is for condense waves, not new papers.)
3. **Index once.** Run Step 4.
4. **Verify hunks before staging.** Confirm every hunk in the shared files is yours — other sessions may edit them too — and stage by name (a filtered `git apply --cached` patch if needed).
5. **Fragments are scratch.** Leave them for re-runs; never stage them.

# Common Mistakes

**Writing from the abstract only.** Abstracts omit the numbers, edge cases and limitations; read the results and check tables and figures.

**Numbers without context.** "The model achieved 0.73" means nothing without the metric, dataset and baseline.

**Hand-editing a generated block.** The next `index` overwrites it and `check` fails until then. Edit the entry; run `index`.

**Renaming a slug after commit.** `grep -rn "<old-slug>" .`, update every `Related` bullet that names it in the same commit, then run Step 4.
