---
name: add-paper
description: Use when adding a paper (or a blog post or thread worth keeping) to the research collection — obtain the source, extract text, write its PAPER_SUMMARIES.md entry in the metadata contract, gate it with condense_check, then regenerate and check the index with paper-index.
---

`{{skills_dir}}` is `~/.claude/skills` on Claude Code and `/home/claude/.claude_researcher_template/template/skills` in the claude.ai sandbox.
Sandbox-specific notes (REST for Issues/Pulls, the post-commit push hook) are in RESEARCHER.md.

<required>
*CRITICAL* Add the following steps to your task tracker: TaskCreate (claude), update_plan (codex), etc.

1. Check the repo's state (markers, hook)
2. Obtain the source
3. Extract text
4. Write the PAPER_SUMMARIES.md entry from the Step 4 template (check slug uniqueness first)
5. Gate the entry: `condense_check.py --strict` must exit 0
6. Generate and check the index (repos with markers only)
7. Stage all new files
8. Report repo-state notices (once per session)
</required>

# Adding a Paper

PAPER_SUMMARIES.md is the source of truth. PAPER_INDEX.md and PAPER_RELATED.md are generated from it by the `paper-index` tool — you write the entry, the tool writes the rows.

## Step 1: Check the repo's state

Check for `<!-- BEGIN GENERATED:` markers in PAPER_INDEX.md (`grep -c`), for `git config core.hooksPath`, and for a tracked `.githooks/pre-commit`.

- **No PAPER_SUMMARIES.md:** run `init-paper-collection` first, then continue.
- **Markers present:** the full flow. If `.githooks/pre-commit` exists but `core.hooksPath` is empty (normal in a fresh clone), run `git config core.hooksPath .githooks` and say so in one line. If there is no `.githooks/pre-commit`, note it for Step 8.
- **PAPER_SUMMARIES.md but no markers** (a collection that predates the contract): **do not stop, and do not copy the house style.** Write the entry from the Step 4 template exactly as for a set-up repo, even when every neighbouring entry looks different; gate it (Step 5); skip Step 6; note it for Step 8. Do not install the hook here — `check` fails without markers, so the hook would refuse every commit that touches PAPER_SUMMARIES.md.

## Step 2: Obtain the source

URL: `curl -L -o papers/<filename>.pdf <url>`. Local path: copy to `papers/`. Named only: search, and confirm the URL before downloading.

**Filename.** If the user's personal info (`researcher_config.md`, or the user section of CLAUDE.md on Claude Code) sets **`Paper naming format`** under Operating preferences, use it. Otherwise the default: `AuthorLast_Year__short_description.pdf` — double underscore, snake_case description (`Acemoglu_2024__simple_macroeconomics_AI.pdf`). If the user has no format set, ask once and offer to save their answer there.

**Not a PDF** (blog post, X thread): print it to PDF where you can and treat it as a paper. Otherwise save the text as `papers/text/<filename>.md` and use a `- **Text extraction:**` bullet in place of `File:` in Step 4; the tool classifies the entry as text-only.

## Step 3: Extract text

```bash
pdftotext papers/<filename>.pdf papers/text/<filename>.txt
```

Without pdftotext: `python3 -m pymupdf convert -output papers/text/<filename>.txt papers/<filename>.pdf`. If neither works, read the PDF directly and write the text yourself. Check the first ~20 lines aren't garbled.

<system-reminder>Always extract, even when the current task doesn't need the text — `check` fails on a PDF with no extraction, and future sessions can't search the paper without it.</system-reminder>

## Step 4: Write the entry

### Slug rules

1. **Format:** kebab-case, lowercase, `[a-z0-9-]+` (`sleeper-agents`, `emergent-misalignment`). The slug is the entry's `### ` heading and the key everything generated hangs off.
2. **Uniqueness (mandatory):** `grep -n '^### <slug>$' PAPER_SUMMARIES.md` must print nothing.
3. **Source of the name:** the paper's common name; if none, `<authorlast>-<yearsuffix>-<topic>` (`hubinger-24-sleepers`). Not the filename.
4. **Stable after commit.** Other entries' `Related` bullets point at it; see Common Mistakes before renaming. To remove a paper, delete the entry and run Step 6; the rows go with it.

### The entry

Copy this template — not a neighbouring entry. Neighbours may predate the contract, and the tools read their labels as missing. Labels are exact: bold, colon inside the bold (`**Summary:**`), metadata as `- **Name:**` bullets. Read the paper from `papers/text/`. Put the entry in the `## ` section where it belongs (create one if needed), closed by a `---` line:

```markdown
### <slug>

**Title:** <Paper title> (<Authors>, <Year> — <Org>)

- **Authors:** Names (Affiliations)
- **Date:** Month Year
- **File:** `<filename>.pdf`
- **Source:** <URL or DOI>
- **Focus:** <2–5 words, in the vocabulary the repo's Focus column already uses>
- **One-liner:** <thesis, target ≤50 words (hard limit 60), with the number that carries it, if the paper has one>
- **Related:** `slug-a`, `slug-b`
- **Summarized:** <model name>, YYYY-MM-DD

**Summary:** 2–4 sentences (at least 50 words) on the core contribution and approach.

**Key findings:**
- Finding with its number and context — what was measured, on what, against what baseline
- Range estimate where the paper gives one

**Relevance:** 1–2 sentences on why this paper matters for this collection.

---
```

- The Title parenthetical is what the tool turns into the index's Paper cell. If it can't take the `(<Authors>, <Year> — <Org>)` shape, add `- **Index label:** Surname (Org) (Year)` after the One-liner — only then.
- `Related` names only slugs that exist in this file; omit the bullet if there are none.
- Write the One-liner last, from the entry, per the `condense-summary` skill. Empirical papers need at least one number in Key findings. A source with no results of its own (position paper, essay, FAQ) uses `**Key claims:**` instead, which needs no number — don't invent one.
- `Summarized:` is the model that wrote the summary (a subagent's own model when it writes) and the date. Re-summarizing replaces it.
- Institutional reports (no abstract, no research question, synthesis rather than new estimates): if your profile has `paper-processing-institutional`, follow its fuller (a)–(d) body and extraction rules — but under the template's labels. Put the (a)–(d) content inside `**Summary:**`, `**Key findings:**` and `**Relevance:**`; never use `**(a) …**` as a label.

## Step 5: Gate the entry

```bash
python3 {{skills_dir}}/condense-summary/condense_check.py . <slug> --strict
```

It must exit 0. It exits 1 on a missing Title, Focus or One-liner; no File, Text extraction or reference-only marker; a metadata bullet without the bold; a Summary under 50 words; no Key findings / Key claims paragraph, or any `Key …:` paragraph other than Key claims / arguments / limitations with no number; no Relevance; a One-liner over 60 words; or a `Related` slug that names no entry. The key must be the exact slug. Each is a defect in the entry: fix it and re-run. It is not a warning to report and move past. The gate reads entries directly, so it works in repos without markers too.

## Step 6: Generate and check (repos with markers)

```bash
python3 {{skills_dir}}/paper-index/paper_index.py index .
python3 {{skills_dir}}/paper-index/paper_index.py check .
```

Never hand-edit between `GENERATED` markers: the next `index` overwrites it. Fix what `check` reports in the entry, then run `index` again. Skip this step in a repo without markers (Step 1).

## Step 7: Stage

```bash
git add papers/<filename>.pdf papers/text/<filename>.txt PAPER_SUMMARIES.md PAPER_INDEX.md PAPER_RELATED.md
```

In a repo without markers, PAPER_INDEX.md and PAPER_RELATED.md were not regenerated; stage only what changed. Do NOT commit — the user may be adding several papers or want to review first. The repo's pre-commit hook re-runs the check.

## Step 8: Report repo-state notices

If Step 1 found a problem, end your turn with one line, once per session, without blocking:

- No markers: *"This collection isn't set up for the paper-index tool (no GENERATED markers), so the index wasn't regenerated; I wrote the new entry in the contract format. Migrating is a separate job — see paper-index, 'Setting up a repo'."*
- Markers but no `.githooks/pre-commit`: *"No paper-index pre-commit hook here; nothing will catch a malformed entry at commit. Install: paper-index, 'Setting up a repo', step 2."*

# Adding Several Papers

For 1–3 papers, take each through Steps 2–5 in turn, then run Step 6 once. For 4 or more, use fragments: parallel agents must never write PAPER_SUMMARIES.md, because concurrent writes clobber each other.

1. **One subagent per paper.** It obtains the source, extracts text, reads it, and writes the complete entry to `<slug>.summary.md` in a gitignored scratch dir (e.g. `data/summaries-frag/`; fragments are scratch — keep them for re-runs, never stage them). Give each agent the Step 4 slug rules and template **verbatim**. Do not give it an existing entry as a style reference: in a collection that predates the contract, it will copy the old format. Have it check its slug against PAPER_SUMMARIES.md.
2. **Each subagent gates its own fragment** before handing back: `python3 {{skills_dir}}/condense-summary/condense_check.py <repo_root> <slug> --file <fragment> --strict` must exit 0. `--file` resolves `Related` against the fragment plus PAPER_SUMMARIES.md.
3. **The orchestrator re-runs the same command on every fragment** before inserting any. A non-zero exit goes back to that agent; don't fix it by hand, and don't take the agent's word that it passed.
4. **The orchestrator inserts serially,** then indexes once (Step 6, repos with markers). One pass, Edit tool, each fragment into its section, rejecting duplicate slugs. (`paper-index`'s `fanout_apply.py` replaces existing entries only — it is for condense waves, not new papers.)
5. **Verify hunks before staging.** Confirm every hunk in the shared files is yours — other sessions may edit them too — and stage by name (a filtered `git apply --cached` patch if needed).

# Common Mistakes

**Copying a neighbour's format.** The template is the spec; neighbours are not. In verification (Oct 2026), ~118 entries were written in batched runs in the house style around them, and every one read as empty to the tools. Fixing them meant a full backfill and migration.

**Labels the tools read as missing.** Each of these looks fine to a reader and fails the gate:
- Period labels: `**Summary.**`, `**Key findings.**`, `**Relevance.**` — use `**Summary:**`.
- Plain metadata bullets: `- Focus: …`, `- One-liner: …`, `- Related: …` — use `- **Focus:** …`.
- Institutional-report labels: `**(a) What it argues.**`, `**(b) …**`, `**(d) …**` — fold the content under the template's labels.
- Qualifiers in the wrong place: an em-dash or digit in a `Key …` label (`**Key findings — 2024 wave:**`), or the colon outside the bold (`**Key findings** (2023 numbers):`). Write `**Key findings (2023 numbers):**`, or put the qualifier in the text.

**Writing from the abstract only.** Abstracts omit the numbers, edge cases and limitations; read the results and check tables and figures. A number needs its context: "the model achieved 0.73" means nothing without the metric, dataset and baseline.

**Renaming a slug after commit.** `grep -rn "<old-slug>" .`, update every `Related` bullet that names it in the same commit, then run Step 6.
