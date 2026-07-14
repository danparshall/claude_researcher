---
description: Check that STATUS.md's Active and Archived Research Lines tables match the actual git branch state, and that STATUS itself hasn't ballooned past its dashboard role. Use when the user says "audit STATUS," "check repo hygiene," "make sure STATUS is current," or when STATUS looks stale after several sessions of active work. Companion to `audit-docs` (docs/ directory consistency) and `audit-papers` (papers/ completeness).
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

**If `claude.ai sandbox`:** the user's project repo is already cloned at `/home/claude/<REPO>/` per `RESEARCHER.md` §2.0b — run the git commands in this skill directly from that working tree. **This skill requires clone-first mode.** If the §2.0b clone failed and you're in degraded REST fallback, the branch-merge queries this skill depends on don't have clean REST equivalents; stop and tell the user you can't audit STATUS without the local clone. Don't attempt a partial audit — the whole point of the skill is comparing git state against STATUS state, and half-visibility into git state produces misleading findings.

<required>
1. Preflight: confirm clone-first mode; `git fetch --prune origin` — the `--prune` is load-bearing: without it, branches deleted on origin persist as stale local refs and generate phantom Bucket A findings (found live on econ-impact, 2026-07-14: 8 phantom flags from a deletion sweep three days prior)
2. Inventory branches: classify each remote branch as merged / unmerged; check for docs directories
3. Parse STATUS.md's Active and Archived tables
4. Compute findings: table-vs-git mismatches (buckets A–D) plus bloat heuristics
5. Present findings one at a time; get approval; apply approved fixes; commit + push
6. Report
</required>

# Audit STATUS

Announce at start: "I'm using the Audit STATUS skill — I'll check that STATUS.md matches the actual branch state and hasn't drifted."

The goal is to keep STATUS.md a fast-glance dashboard. The Active Research Lines table reflects what's in flight (one row per unmerged branch), the Archived table reflects what's shipped (one row per merged/historical line), and the rest of STATUS stays lean (project parameters, current focus, recent sessions) so a session-start read fits in reasonable context. Per-line detail lives in `docs/active/<branch>/RESEARCH_LOG.md`, not in STATUS. Drift on any of these dimensions makes STATUS less useful as an at-a-glance inventory — this skill catches the drift.

## Step 1: Preflight

Confirm the project-repo clone is present:

```bash
ls /home/claude/${REPO}/.git > /dev/null 2>&1 && echo "clone present" || echo "no clone"
```

If the clone isn't present, tell the user: *"I can't audit STATUS without the project-repo clone — the branch-merge queries don't work over the REST fallback. Try again after the §2.0b clone succeeds (may require restarting the session)."* Stop.

Fetch, with prune:

```bash
cd /home/claude/${REPO}
git fetch --all --prune
```

`--prune` removes local refs to branches that were deleted upstream — important for accuracy.

## Step 2: Inventory branches

Classify each remote branch:

```bash
# Merged into main:
git branch -r --merged origin/main | grep -v 'origin/main$' | grep -v 'origin/HEAD'

# Unmerged (still in flight):
git branch -r --no-merged origin/main | grep -v 'origin/HEAD'
```

For each **unmerged** branch, check whether `docs/active/<branch>/` exists *on that branch*:

```bash
git ls-tree -d origin/<branch> docs/active/<branch>/ > /dev/null 2>&1 && echo "docs present" || echo "no docs dir"
```

For each **merged** branch, check whether `docs/historical/<branch>/` exists on `origin/main`:

```bash
git ls-tree -d origin/main docs/historical/<branch>/ > /dev/null 2>&1 && echo "archived" || echo "not archived"
```

Build a working table in memory or a scratch file (`/tmp/branch_inventory.tsv`):

| Branch | Merge status | docs present? |

## Step 3: Parse STATUS.md tables

Read STATUS.md from `origin/main`:

```bash
git show origin/main:STATUS.md
```

Extract two tables:

- **`## Active Research Lines`** — find the heading; capture rows until the next `##`. Row format: `| Topic | Started | Purpose |`. Skip the header row and separator; skip the `| (none yet) | | |` placeholder.
- **`## Archived Research Lines`** — same shape. Row format: `| Topic | Summary | Archived | Material |`.

For each table, collect the Topic column into a set. If either heading is missing, note it — that's itself a finding (STATUS predates the current schema).

## Step 4: Compute findings

Cross-reference the branch inventory against the table contents. Findings fall into four buckets:

### Bucket A — Unmerged branch missing from Active table

- Branch exists on origin, not merged into main, no matching row in Active table.
- **Pending-deletion carve-out (check first):** if the branch is annotated as classified-for-deletion — in STATUS's `## Known issues`, or in a worksheet that Known issues references — do NOT flag it as a finding. List all such branches once, in a compact "Pending deletion (suppressed)" block at the end of the report, so they stay visible without generating repeat findings every audit. If a suppressed branch is still undeleted after ~30 days, ask once whether the sweep is still planned.
- **Proposed fix (unannotated branches):** add a row. Ask user for one-sentence Purpose. Suggest Started date from the branch's first-commit date: `git log --reverse --format=%as origin/<branch> | head -1`.

### Bucket B — Active table row with no matching branch

- Row's Topic doesn't match any origin branch.
- **Ask user what happened.** Possibilities:
  - Branch was renamed → update Topic in row to match the new name.
  - Branch was deleted without merge → remove row; note reason in commit message.
  - Branch was merged but row wasn't moved → handle as Bucket C.
  - Genuine orphan (row created by mistake) → remove row.

### Bucket C — Merged branch missing from Archived table

- Branch is merged into `origin/main`; no row in Archived table. **Bundle rows count:** a consolidated row (e.g. "v4-prompt-design (bundle)") covers every branch it names in its Topic, Summary, or Material — check those fields before flagging.
- **Proposed fix sequence** (offer as two steps, approve each):
  1. Move the branch's row from Active (if present) to Archived. Ask for Summary + Archived date + Material path (typically `docs/historical/<branch>/`).
  2. Offer to delete the stale remote branch: `git push origin --delete <branch>`. The user may want to keep it around; honor that.

### Bucket D — Archived row whose Material reference doesn't resolve

- The check is **"does the row's Material reference resolve?"** — NOT "does `docs/historical/<topic>/` exist." Valid Material under the one-row-per-line convention: a per-topic historical dir, a *shared/consolidated* historical dir, a code or `results/` path, a specific file or glob (`docs/20260303_*`), a commit/merge reference, or a merged-PR link with a content map. Resolve dirs/files/globs with `ls` on main; commit refs with `git cat-file -e <sha>`; PR links count as resolving if the PR exists and is merged. (Requiring a per-topic dir produced 27 false positives on a fully-conformant repo — econ-impact, 2026-07-11.)
- **Surface only genuine non-resolution.** A dangling Material suggests a partial archive (row added but the move never happened, or the target was later deleted/renamed). Ask the user how to reconcile:
  - Fix the Material reference → point it at where the record actually lives.
  - Delete the row → treat as never-archived.
  - Restore the target from git history → check `git log --all -- <path>` for the last-known state.
  - Leave the discrepancy → note in commit message that it's intentional.

Don't auto-fix Bucket D. The information asymmetry is the point.

### Schema & bloat heuristics (mode-aware; soft unless marked firm)

Check the repo's mode first: `workflow_mode` in STATUS.md (absent = `branches`) — but **before that, check for lite mode** (a `LITE.md` at repo root, or STATUS.md opening with `## Current intent`). Lite repos have their own memory model and this skill's tables/buckets don't apply as-is: offer the lite checks instead — session-log entries ≤5 lines each, ≤~10 entries with overflow rolled to `HISTORY.md` (newest-first, rotate by count not age), and `docs/active/` ≤~10 files with the oldest rotated to `docs/historical/`. Run Buckets A–D on a lite repo only if it actually maintains Active/Archived tables.

For full-workflow repos, present each finding as a question, not a prescription:

**`branches` mode (orchestrator schema):**
- **`## Recent Sessions` EXISTS** → schema finding, not bloat: *"This STATUS still carries a Recent Sessions section — under the orchestrator model sessions log to RESEARCH_LOG only. Migrate (entries → a sessions-archive file in docs/historical/)?"* The entry-count heuristic does not apply in this mode; the section's presence is the finding.
- **Section order** → the how-to-read header, `## Current focus`, and `## Active Research Lines` should precede everything else (partial-read convention, RESEARCHER.md §2c). If not: *"Reorder so session-start can read only the top of the file?"*
- **STATUS.md > ~200 lines** → soft flag (a healthy orchestrator STATUS runs ~100–150 even with 15+ active lines). **> ~300 lines → firm finding**: something diary-shaped is accumulating; identify which section.
- **Oversize Purpose (>1 sentence) or Summary (>2 sentences)** → soft flag: *"Row X's Purpose/Summary has drifted past the cap — trim, or move the detail to the line's RESEARCH_LOG?"*

**`main_only` mode:**
- **`## Recent Sessions` > ~20 entries** → *"Recent Sessions has N entries. Roll the oldest into a per-year archive file?"*
- **Any entry > 2 lines** → *"Entry from YYYY-MM-DD runs long — trim to ≤2 lines + link, detail into the convo/log?"*
- **STATUS.md > ~200 lines** → soft flag, same question as above.

**Both modes:**
- **`## Current focus` > ~30 lines** → *"Current focus is N lines — beyond dashboard length. Move the detail into the relevant `docs/active/<branch>/RESEARCH_LOG.md` and leave a pointer here?"*
- **Derived recency:** include a last-activity-per-line table in the report by default — `git for-each-ref --sort=-committerdate --format='%(refname:short) %(committerdate:short)' refs/remotes/origin` joined against the Active table. This replaces what Recent Sessions used to signal, at zero storage cost.

A project with 60 active-but-slow research lines has a legitimately long Active table. The soft thresholds are calibration hints, not rules; only the >300-line branches-mode check is firm.

## Step 5: Present findings, one at a time

Order: A → B → C → D → bloat.

For each finding:

1. Present the finding with the proposed fix (or the question, for D and bloat).
2. Wait for user response. Accept: approve / edit / skip.
3. If approved, apply the fix:

```bash
git checkout main
git pull --ff-only origin main
# edit STATUS.md (using view/edit tools; for programmatic edits, prefer stable anchors like the table headers over line numbers)
git add STATUS.md
git commit -m "STATUS audit: <one-line description of what changed>"
git push origin main
```

If the fix involves deleting a branch (Bucket C's optional second step) or moving directories (Bucket D reconciliation), do those as separate commits with descriptive messages so the audit trail stays legible in git log.

**Do not batch findings into a single approval.** The audit's value comes from surfacing disagreements between the trackers and the git state — those disagreements often carry information (a renamed branch, a deferred archive, a branch the user is deliberately keeping unmerged) that the user should think through case by case.

**Verification affordance.** After each STATUS.md edit, if the user wants confirmation the write landed on origin: `curl -s https://api.github.com/repos/$USERNAME/$REPO/contents/STATUS.md | jq -r .content | base64 -d | grep '<the-new-row>'`.

## Step 6: Report

At the end:

```
Audit complete:
  Findings surfaced: <N>
  Fixes applied:     <M>
  Skipped:           <N - M>

Post-audit STATUS state:
  - <K> active-branch rows in Active Research Lines table
  - <L> archived rows in Archived Research Lines table
  - STATUS length: <X> lines
  - Recent Sessions: <Y> entries
  - Current Focus: <Z> lines
```

If any findings were skipped, mention that they'll surface again on the next audit — no state is kept between runs.

# Common mistakes

**Auto-fixing without approval**
- Problem: The audit's core value is surfacing disagreements that carry information. A renamed branch might mean the research pivoted; an unarchived merge might mean the user isn't ready to archive yet; an orphaned Active row might be a placeholder for imminent work. Auto-fixing loses those signals.
- Fix: One finding at a time, explicit approval, no batching.

**Running in degraded REST mode**
- Problem: The REST fallback for merge-checking is expensive and error-prone (walk commits or one Compare API call per branch). The audit produces misleading findings under partial visibility.
- Fix: Preflight in Step 1. If the clone isn't present, stop cleanly and tell the user.

**Treating bloat heuristics as hard limits**
- Problem: The 200-line / 20-session / 30-line thresholds are hints for a "typical" research repo. Real repos vary. A bloat "flag" turning into a "must trim" mandate creates busywork.
- Fix: Present bloat findings as questions, not prescriptions. If the user says "yes, that's the length it should be for this project," that's a valid answer.

**Editing STATUS.md on the wrong branch**
- Problem: If you're on a feature branch when the audit runs, `git add STATUS.md` stages the feature-branch version, not main's. The push then creates diverging STATUS files.
- Fix: Step 5's edit sequence explicitly `git checkout main` first. If the user says "actually I want the audit to run against the feature-branch STATUS," that's a different task — surface and confirm before proceeding.

**Missing the "no Active Research Lines section" case**
- Problem: STATUS.md files predating the `start-research-line` convention may not have an `## Active Research Lines` section at all. The parser then reports zero active rows and everything looks like a Bucket A finding.
- Fix: In Step 3, check for the section's existence. If missing, treat it as a distinct finding: *"STATUS.md doesn't have an Active Research Lines section. Add one (with rows populated from the branch inventory), then continue the audit?"* If the user approves, add the section per the shape in `start-research-line` Step 3, then re-enter Step 4.
