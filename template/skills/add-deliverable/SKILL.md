---
name: add-deliverable
description: Use when the user is ready to create an outward-facing deliverable — a paper, memo, bill response, briefing, essay, or any artifact that will leave the repo for an external audience. Creates `deliverables/<target>/` with a seeded `LINEAGE.md` capturing which research lines fed the deliverable and where its citable numbers came from. Tiered rigor — the LINEAGE starts light (source path + branch SHA) and can be upgraded to include runnable regeneration commands for numbers that will be defended in Q&A.
---

## Runtime detection

Before following the rest of this skill, determine your environment:

```bash
if [ "$IS_SANDBOX" = "yes" ] || [ -d "/mnt/skills/public" ]; then
  echo "claude.ai sandbox"
elif [ "$CLAUDECODE" = "1" ]; then
  echo "Claude Code"
else
  echo "unknown — surface to user before proceeding"
fi
```

**If `claude.ai sandbox`:** the user's project repo is already cloned at `/home/claude/<REPO>/` per `RESEARCHER.md` §2.0b — run the file writes and `git` commands directly from that working tree. If the §2.0b clone failed (degraded REST fallback), translate the file writes into Contents API PUTs and surface degraded mode.

**If `Claude Code`:** follow the skill body as-is.

**If `unknown`:** stop and surface to the user.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Confirmation gate (target name + purpose + input research lines)
2. Check for existing deliverables/<target>/ (surface if collision)
3. Resolve merge-commit SHAs for each named input research line
4. Create deliverables/<target>/ + seed LINEAGE.md
5. Optional: create deliverables/<target>/src/ for build scripts
6. Commit + push
7. Report
</required>

# Add Deliverable

Creates a new deliverable directory with the provenance scaffolding that makes citable numbers traceable back to the research lines that produced them.

Announce at start: "I'm using the Add Deliverable skill to create `deliverables/<target>/`."

## Why this skill exists

Research repos produce outputs that leave the repo — papers, policy memos, bill responses, briefing decks, essays, testimony. Those outputs typically draw on **multiple** research lines, and they outlive the branches that produced them. When someone later asks "Section 2 says the value is X — can you confirm?", the deliverable needs a paper trail that survives branch renames, merges, and the passage of time.

`deliverables/<target>/LINEAGE.md` is that paper trail. It pins **merge-commit SHAs** (not branch HEAD) so references survive the branch getting deleted, records which claim goes with which source, and — for numbers that will be defended externally — carries a runnable command that regenerates the number from scratch.

The lineage discipline is what makes `deliverables/<target>/` at repo top-level safe. Without it, a deliverable dir is just a bag of files whose provenance decays fast; branches get merged into `main` and then their `docs/active/<branch>/` moves to `docs/historical/<branch>/`, but a deliverable that just says "we found X" with no pointer becomes unverifiable within a few months.

## The Process

### Step 1: Confirmation gate

Ask the user for three pieces of information:

> *"I'm about to create `deliverables/<target>/` with a seeded `LINEAGE.md`. Three things I need:*
> *1. **Target name** (short, kebab-case) — what the deliverable is going to, or what it is. Examples: `paper-canary-jan2027`, `bill-sb1047-response`, `memo-obernolte-trahan`, `essay-shallow-intent-rebuttal`. What should the target name be?*
> *2. **Purpose** — one sentence about what this deliverable does and for whom. Goes at the top of LINEAGE.md.*
> *3. **Input research lines** — which branches (active or already merged) fed material or numbers into this deliverable? Comma-separated list of branch names, or `none yet` if you're just cutting the target and sources will land later. Doesn't have to be exhaustive at creation time — you can (and will) add rows later as more branches feed in."*

**Target name validation.** Lowercase, alphanumeric plus hyphens, ≤50 characters. Common prefixes clarify what the deliverable is:

- `paper-<slug>` for academic-style papers
- `memo-<recipient>` for direct memos
- `bill-<number>-<action>` for legislative responses
- `essay-<slug>` for public essays
- `deck-<venue>` for slides
- `testimony-<venue>-<date>` for spoken testimony

Suggest a name derived from what the user described; user can override.

**Purpose** is one sentence. If the user gives you a paragraph, condense it and read it back. If the user says "just make it, I'll fill it in later," write `Purpose: TBD` and note the placeholder in the report so they know to update it before shipping.

**CONFIRMATION GATE.** Do not proceed past this step without the user's explicit "yes" (or equivalent).

### Step 2: Check for collision

```bash
ls -d deliverables/<target>/ 2>/dev/null
```

If `deliverables/<target>/` already exists, surface to the user and stop. Two options:

- Different target — pick a new name.
- Same target, want to add to it — this skill is for creating; use plain file edits on the existing `LINEAGE.md` instead.

Never silently merge into an existing target dir. Deliverables carry provenance obligations and quietly appending to someone else's lineage record is the wrong shape.

### Step 3: Resolve merge-commit SHAs for input research lines

For each named input branch, resolve which SHA to pin in LINEAGE.md:

**If the branch is already merged into main:** find the merge commit and pin its SHA.

```bash
git fetch --all --quiet
git log main --oneline --merges --grep="<branch-name>" | head -20
```

Grep the recent merge commits for the branch name (GitHub PR merges include the branch name in the merge subject by default: `Merge pull request #NN from <user>/<branch-name>`). If you find the merge, take its SHA. If you can't find it, ask the user for the PR number and cross-reference:

```bash
gh pr view <PR-number> --json mergeCommit,mergedAt --jq '{sha: .mergeCommit.oid, at: .mergedAt}'
```

**If the branch is still active (not merged):** pin the current HEAD SHA of the branch, and mark the row `active` so a future audit knows to re-pin at merge time.

```bash
git rev-parse origin/<branch-name>
```

**If the user said "none yet":** skip Step 3 and leave the Input research lines section with a `(none yet — add rows as branches feed in)` placeholder.

Record the resolved `{branch, status, sha, date}` tuples for use in Step 4.

### Step 4: Create the deliverable dir + seed LINEAGE.md

```bash
mkdir -p deliverables/<target>
```

Seed `deliverables/<target>/LINEAGE.md`:

```markdown
# Lineage — <target>

**Created:** YYYY-MM-DD
**Purpose:** <the one-sentence purpose from Step 1 — or `TBD` if the user deferred>
**Status:** draft

## Input research lines

Which research lines contributed material or numbers to this deliverable. Merge-commit SHAs are pinned (not branch HEAD) so the reference survives the branch being deleted or renamed. For lines still active at deliverable creation, the current HEAD is pinned with `status: active` — re-pin to the merge SHA at merge time.

- `<branch-1>` — merged YYYY-MM-DD as PR #NN (merge commit `<sha>`) — <what it contributed, one clause>
- `<branch-2>` — active, HEAD `<sha>` as of YYYY-MM-DD — <what it contributes>
- `<branch-3>` — merged YYYY-MM-DD as PR #NN (merge commit `<sha>`) — <what it contributed>

## Claims and their sources

Every citable number or specific claim that appears in the deliverable, with where it came from.

**Start with the light format below** (claim + where-it-appears + source path pinned to a branch SHA). It's the working default — it tells a future reader where to look, without forcing you to write a regeneration command for every value.

**Upgrade to the fuller format** (add a Method column with a runnable regeneration command) **for numbers that will be cited externally or defended in Q&A** — the paper's headline number, the value the policymaker will ask about, the figure that opens the executive summary. Not everything needs the upgrade; match rigor to stakes.

### Light format (default)

| Claim / value | Where it appears | Source |
|---|---|---|
| (add rows as you write) | | |

Example row:
| $X TAM by 2030 | §2, ¶3 | `data/processed/econ-run-3/summary.csv` (branch `econ-impact-scenarios`, merge SHA `a1b2c3d`) |

### Fuller format (for citable / defensible numbers)

Add a Method column with a runnable command that regenerates the number from scratch:

| Claim / value | Where it appears | Source | Method |
|---|---|---|---|
| (add rows as numbers get promoted from Light) | | | |

Example row:
| $X TAM by 2030 | §2, ¶3 | `data/processed/econ-run-3/summary.csv` (branch `econ-impact-scenarios`, merge SHA `a1b2c3d`) | `git checkout a1b2c3d && uv run scripts/run_scenarios.py --config config/scenarios/v3.yaml` |

## Reproducibility notes

<Any conventions specific to this deliverable — e.g., "figures are regenerated from `deliverables/<target>/src/make_figures.py`; PDF built via `make pdf` in `deliverables/<target>/src/`; raw survey data is under NDA and lives in a separate encrypted store — the source paths above resolve to public aggregates only.">

## Change log

Deliberate reproducibility choices, deliverable-level revisions, or shifts in what LINEAGE covers. Not for every file save — for decisions a future reader would want to see.

- YYYY-MM-DD — Created. Initial input research lines: `<branch-1>`, `<branch-2>`.
```

Populate the Input research lines section with the tuples from Step 3. Leave the Claims tables with the example row visible-but-commented (`<!-- example: ... -->`) so the researcher has a pattern to copy without polluting the initial file with fake data.

### Step 5: Optional — create `deliverables/<target>/src/` for build scripts

Some deliverables have build machinery — LaTeX templates, `make pdf` recipes, figure-generation scripts, DOCX conversion. If the user says yes when asked, create:

```bash
mkdir -p deliverables/<target>/src
touch deliverables/<target>/src/.gitkeep
```

Otherwise skip. Most memos and short essays don't need this; papers and multi-format outputs usually do.

### Step 6: Commit + push

```bash
git add deliverables/<target>/
git commit -m "Add deliverable <target>: <purpose sentence>"
git push
```

Commit even if the deliverable dir is empty except for LINEAGE.md — creating the paper trail is the point. If the user is on a research branch (not main), the commit lands on that branch; if on main, it lands on main directly.

**Which branch should the deliverable dir live on?** Two viable answers:

- **On main** — most deliverables draw on multiple research lines and outlive any single branch, so `main` is the natural home. Cut a short deliverable branch off `main` if the deliverable itself needs review before landing.
- **On a research branch** — if the deliverable is tightly scoped to a single line and it makes sense to develop it alongside the research, keep it on the branch. It'll land on main when the branch merges.

Ask if the user hasn't already made this call. Default is `main` unless they say otherwise.

### Step 7: Report

Tell the user briefly:

```
Deliverable created:
  Path:     deliverables/<target>/
  LINEAGE:  seeded with <N> input research line(s)
  Purpose:  <the purpose sentence, or "TBD — remember to fill this in">
  [src/:    created for build scripts]

Next steps:
  - As you write the deliverable, add a row to LINEAGE.md's Claims table for each citable value
  - For numbers that will be defended externally, upgrade the row to the fuller format with a Method column
  - When an active input branch merges, re-pin its LINEAGE.md row from HEAD SHA to merge-commit SHA
  - When the deliverable ships, update the Status: line in LINEAGE.md (draft → shipped) and log the ship date in the Change log
```

## LINEAGE.md maintenance — the audit affordance

The whole point of LINEAGE.md is that a future reader can verify a claim. When a claim gets challenged:

1. Read LINEAGE.md's Claims table.
2. Find the row for the challenged value.
3. Follow the Source column to the file (a `data/processed/<branch>/*.csv`, a `docs/active/<branch>/results/*.md`, etc.).
4. If the branch is merged, the merge-commit SHA lets you `git show <sha>:<path>` to see the exact file version at merge time. If the branch is still active, the row will say so and you'll want to re-fetch the current version.
5. If the row has a Method column, run it — that's the definitive check.

If step 4 fails (the source file has been moved, deleted, or refactored beyond recognition), that's a lineage break and is worth fixing in the same session as the challenge — either update the row to point at where the source *actually* lives now, or restore the old file's content via `git show <sha>:<path> > <path>` if you need to make the exact original accessible again.

## Notes

- **Merge-commit SHA, not branch HEAD.** Branches get deleted after archive (`git push origin --delete <branch>`). Branch names can be reused. Merge-commit SHAs are permanent and unambiguous. Always pin the SHA in LINEAGE rows.
- **Tiered rigor is deliberate.** The light format is the working default because filling in a Method column for every row is maintenance theater — most rows are context, not defensible-under-fire values. Upgrade the ones that matter; leave the rest light.
- **LINEAGE.md is a living document.** Rows get added as you write. Update the Change log for real revisions (added a new input line, restructured what a row covers, moved a claim from light to fuller); don't log every save.
- **Deliverables can draw on active branches.** If your deliverable cites a value from a branch that hasn't merged yet, that's fine — mark the row `active, HEAD <sha> as of <date>`. At the branch's merge, re-pin the row to the merge SHA. A quick grep of LINEAGE.md files at branch-merge time (or as part of `finishing-a-research-branch`) is worth doing to catch stale HEAD pins.
- **`add-deliverable` does not create the deliverable itself** — just the dir and the provenance scaffolding. The deliverable's actual content (markdown, LaTeX, DOCX, PDF, whatever) is authored by the user and Claude together, typically via `iterative-writing-workflow` or `branch-document-review`.
- **A deliverable dir can hold multiple output formats** — e.g., a `paper.md` source, a rendered `paper.pdf`, a companion `slides.pptx`. LINEAGE.md covers all of them: the "Where it appears" column can distinguish (`paper.md §2, ¶3` vs. `slides.pptx slide 4`).
- **The `deliverables/` top-level directory should not be gitignored.** LINEAGE.md and the deliverable source files (markdown, code that builds the deliverable) belong in git. Only large binary outputs — rendered PDFs regenerable from source, exported DOCX/PPTX — might warrant gitignoring on a per-deliverable basis, and even that's usually not worth it for typical policy-brief-sized artifacts.

## Common mistakes

**Pinning branch HEAD instead of the merge-commit SHA**
- Problem: Branch HEAD moves. Branches get renamed. Branches get deleted after archive. A LINEAGE row that says "branch `foo`, SHA `abc123`" is only useful if that SHA is still reachable via a permanent ref (a merge commit on `main`, a tag). A branch-HEAD SHA that gets deleted vanishes from `git log` without a trace, and the row now points nowhere.
- Fix: For merged branches, always pin the merge commit's SHA. For active branches, pin HEAD SHA and mark the row `active` — re-pin at merge time.

**Filling in the Method column for every claim**
- Problem: LINEAGE becomes a huge table where 80% of the rows are values that nobody will ever challenge. Maintenance burden goes up; signal-to-noise goes down; when the row that *does* matter gets challenged, it's harder to find.
- Fix: Default to the light format. Upgrade only citable / defensible values. If you're not sure whether a value warrants the upgrade, ask: "will anyone external ever ask me to defend this specific number?" If no, leave it light.

**Silently appending to an existing deliverables/<target>/**
- Problem: If someone else has been working on `deliverables/paper-canary-jan2027/`, this skill blindly adding files there is the wrong shape — the existing LINEAGE has assumptions and you don't know what they are.
- Fix: Step 2's collision check is not optional. If the target exists, stop. Either pick a new target name or hand the situation to the user.

**Committing large derived outputs (rendered PDFs, exported DOCXs) into the deliverable dir without thought**
- Problem: A 20MB rendered PDF committed and re-committed on every edit bloats the repo history fast. Once in git, it's expensive to remove cleanly.
- Fix: Only commit outputs when it's meaningfully useful (the final "shipped" version, e.g.). Regenerable intermediate builds can be gitignored per-deliverable. For a paper with dozens of build iterations, add `deliverables/paper-foo/build/` to `.gitignore` and only commit the shipped copy.

**Creating a deliverable dir with no LINEAGE.md**
- Problem: A `deliverables/foo/` with just source files but no LINEAGE is the exact bag-of-files shape the LINEAGE requirement is designed to prevent. Six months later, nobody can trace the values.
- Fix: LINEAGE.md is created in Step 4 unconditionally. If you're creating a deliverable dir without this skill, seed LINEAGE.md by hand — don't skip it.

**Treating "Purpose: TBD" as the final state**
- Problem: The purpose sentence goes at the top of LINEAGE.md and in STATUS.md-adjacent surfaces. Leaving it TBD means every future reader has to reconstruct what the deliverable is for.
- Fix: The `TBD` placeholder is fine at creation-in-a-hurry time, but treat it as a follow-up task — fill it in before the deliverable ships.
