---
description: Use when the user wants to start a new research line ("start a new line", "cut a branch for X", "let's begin Y"). Bundles branch creation + docs/active/<line>/ scaffold + RESEARCH_LOG.md seed + STATUS.md Active Research Lines table update as one atomic ceremony, so every future session-start read of STATUS.md sees the line at a glance.
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

**If `claude.ai sandbox`:** the user's project repo is already cloned at `/home/claude/<REPO>/` per `RESEARCHER.md` §2.0b — run the git commands in this skill directly from that working tree. Only if the §2.0b clone failed (degraded REST fallback, surfaced to the user) do you translate `git checkout` / `git commit` / `git push` into the Refs API / Contents API recipes from your Project Instructions.

<required>
1. Confirmation gate (branch name + one-sentence purpose)
2. Ensure on main + up-to-date
3. Update STATUS.md's Active Research Lines table + commit + push (still on main)
4. Cut the branch: `git checkout -b <branch> && git push -u origin <branch>` (skip in `main_only` mode)
5. Scaffold `docs/active/<branch>/{convos,plans,results}` + seed RESEARCH_LOG.md
6. Commit + push
7. Report
</required>

# Starting a Research Line

Announce at start: "I'm using the Start Research Line skill to create the new line."

The goal is a single ceremony that guarantees four artifacts appear together whenever a new research line is created:

1. The git branch (in `branches` mode)
2. The `docs/active/<line>/` directory tree
3. The seeded `RESEARCH_LOG.md`
4. **A row in STATUS.md's Active Research Lines table** — the load-bearing one

STATUS.md is the canonical inventory that every session reads at start (per `RESEARCHER.md` §2c). If a line exists on disk but isn't in the table, future sessions won't reliably notice it — `ls docs/active/` is not part of the session-start sequence. This skill's job is to make sure the table entry lands atomically with the rest of the ceremony.

## Step 1: Confirmation gate

Ask the user:

> *"I'm about to create a new research line called `<branch-name>`. This will:*
> *- Add a row to STATUS.md's Active Research Lines table on `main` (so every future session sees it at a glance).*
> *- Cut a new branch `<branch-name>` and push it (in `branches` mode).*
> *- Scaffold `docs/active/<branch-name>/{convos,plans,results}` with a seeded `RESEARCH_LOG.md`.*
>
> *Also — a one-sentence description of what this line is investigating. It goes into both STATUS.md's Purpose column and the RESEARCH_LOG.md header. Confirm to proceed?"*

**Branch name validation.** Lowercase, alphanumeric plus hyphens, ≤39 characters. Suggest a name derived from the topic (suggest-with-Enter pattern); user can override.

**Purpose.** One sentence, amendable at milestones (if the line's direction shifts materially, update the row's Purpose in the same commit as the milestone — but the fresh Summary at merge time is where the final story gets told, so don't over-groom). If the user hasn't provided one, ask before proceeding — it lands in two files and is the future-you-and-them signal of what this line was for.

> **(novice:** explain first that "branches are like separate parallel workspaces in your repo. We can experiment in this branch without touching anything in `main`. When the work is done, we'll merge it into `main` as the permanent record.") **(fluent:** just proceed.)

**CONFIRMATION GATE.** Do not proceed past this step without the user's explicit "yes" (or equivalent).

## Step 2: Ensure on main and up-to-date

```bash
cd /home/claude/${REPO}
git checkout main
git pull --ff-only origin main
```

If the pull is rejected (divergent branches), **stop and surface to the user** — someone pushed to `main` externally and the state needs reconciliation before proceeding. Don't auto-rebase or auto-merge.

## Step 3: Update STATUS.md (still on main)

Read `STATUS.md`. Locate the `## Active Research Lines` section.

**If the section exists:** append a row to its table:

```markdown
| <branch-name> | <YYYY-MM-DD> | <one-sentence purpose> |
```

**If the section is missing** (older repo, or a `STATUS.md` predating this convention): insert the section just before `## Recent Sessions` (or wherever fits between Project parameters and Recent Sessions):

```markdown
## Active Research Lines

Lines currently in flight; see `docs/active/<topic>/` for material.

| Topic | Started | Purpose |
|-------|---------|---------|
| <branch-name> | <YYYY-MM-DD> | <one-sentence purpose> |
```

Commit and push (still on `main`):

```bash
git add STATUS.md
git commit -m "STATUS: start active line <branch-name>"
git push origin main
```

**Push race.** If the push is rejected (non-fast-forward), another STATUS-writing ceremony landed on `main` since Step 2's pull. Recover per the `resolve-runtime-issue` skill's entry for rejected pushes: `git pull --rebase origin main`; if the only conflict is both sides appending rows to a lifecycle table, resolve with `python3 /home/claude/.claude_researcher_template/template/scripts/resolve_append_conflict.py STATUS.md` (keeps both rows), then `git add STATUS.md`, `git rebase --continue`, re-push. Any other conflict shape: surface to the user.

**Verification affordance.** GET `https://api.github.com/repos/$USERNAME/$REPO/contents/STATUS.md`, decode `content` from base64, confirm the new row is present. Skip if you're confident the write landed.

**Rationale for pre-branch ordering.** STATUS.md lives on `main` and reflects all active lines. Updating it *before* cutting the new branch means (a) `main`'s STATUS is always current, and (b) if the branch cut fails for any reason, the STATUS update rolls back naturally (nothing to clean up — just leave the row or revert).

## Step 4: Cut the branch

Check `workflow_mode` from STATUS.md. Defaults to `branches` if absent.

**In `branches` mode:**

```bash
git checkout -b <branch-name>
git push -u origin <branch-name>
```

**In `main_only` mode:** skip this step. The `docs/active/<branch>/` directory in Step 5 gets created on `main` directly, and Step 6's commit goes to `main`.

**Fallback if the §2.0b clone failed** (degraded REST): use the Refs API recipe from your Project Instructions:

```bash
MAIN_SHA=$(curl -s -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/$USERNAME/$REPO/git/ref/heads/main" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['object']['sha'])")

curl -sX POST -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/$USERNAME/$REPO/git/refs" \
  -d "{\"ref\":\"refs/heads/<branch-name>\",\"sha\":\"$MAIN_SHA\"}"
```

Surface degraded mode to the user.

## Step 5: Scaffold `docs/active/<branch-name>/`

```bash
mkdir -p docs/active/<branch-name>/convos
mkdir -p docs/active/<branch-name>/plans
mkdir -p docs/active/<branch-name>/results
```

Seed `docs/active/<branch-name>/RESEARCH_LOG.md`:

```markdown
# Research Log: <branch-name>

Created: <YYYY-MM-DD>
Purpose: <the one-sentence purpose from Step 1>

---

(Sessions logged here, newest first)
```

## Step 6: Commit + push

```bash
git add docs/active/<branch-name>/
git commit -m "Scaffold <branch-name>: RESEARCH_LOG + directory structure"
```

**In `branches` mode:**

```bash
git push origin <branch-name>
```

**In `main_only` mode:**

```bash
git push origin main
```

## Step 7: Report

Tell the user briefly:

```
New research line created:
  Branch:  <branch-name>          (branches mode; omit line for main_only)
  Docs:    docs/active/<branch-name>/
             RESEARCH_LOG.md     (seeded with purpose)
             convos/
             plans/
             results/
  STATUS:  Active Research Lines table row added on main

Next: what's the first thing you want to look at?
```

# Common mistakes

**Skipping the STATUS.md update**
- Problem: The whole reason this skill exists. If the row isn't in the table, future sessions won't reliably discover the line — `ls docs/active/` is not in the session-start read sequence.
- Fix: Step 3 is not optional. If the table section is missing, create it. Then add the row.

**Updating STATUS.md on the branch instead of main**
- Problem: `main`'s STATUS won't reflect the new line until the branch is merged (which may be weeks away). Sessions reading `main`'s STATUS see stale state.
- Fix: Step 3 explicitly runs on `main` before Step 4 cuts the branch. Follow the ordering.

**Forgetting to ask for the purpose sentence**
- Problem: STATUS's Purpose column gets `<to be filled in>` or gets skipped; RESEARCH_LOG's header carries no context. Future-you-and-them look at the line six months later and can't remember what it was for.
- Fix: Ask in Step 1's confirmation gate. If the user says "just cut the branch and I'll fill it in later" — fine, but write a one-line placeholder like `Purpose: TBD — see first convo` in both places so the future reader knows to look further.

**Running the skill in a repo that isn't set up for research**
- Problem: If `docs/active/` and `docs/historical/` don't exist yet, `mkdir -p docs/active/<branch>/...` succeeds but the parent structure was never intended — you may be setting up a repo the user thought was pre-configured.
- Fix: Check for `docs/active/` and `docs/historical/` before Step 5. If missing, surface to the user — they may want to run `init-research-repo` first, or you may be in the wrong repo entirely.
