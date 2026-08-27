---
name: finishing-a-research-branch
description: Merge a completed research line into main and archive its docs. Use when the user says the line is "done", "ready to ship", "let's merge it", or equivalent. Runs finish-convo + audit-docs on the still-open line before anything merges. Handles both `branches` mode (checkpoint + audit + open PR + merge + archive) and `main_only` mode (checkpoint + audit + archive). This is the full research-line close ceremony; for a mid-session or end-of-session checkpoint that keeps the branch open, use `finish-convo` instead.
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

**If `claude.ai sandbox`:** the project repo is at `/home/claude/<REPO>/` per `RESEARCHER.md` §2.0b. Run the `git` commands directly from that working tree. The PR open/merge steps use the Pulls REST API because there's no plain-git equivalent — use the `curl` recipes below with the PAT from Project Instructions. If the §2.0b clone failed (degraded REST fallback), translate the directory move into per-file Contents API PUTs and surface degraded mode.

**If `Claude Code`:** follow the skill body as-is; substitute `gh pr create` / `gh pr merge` for the `curl` calls if `gh` is available.

**If `unknown`:** stop and surface to the user.

<required>
1. Confirmation gate
1.5. Run finish-convo, then audit-docs, on the still-open line (both modes) — nothing merges or archives before these pass
2. `branches` mode: open PR (Pulls API)
3. `branches` mode: merge PR (Pulls API); on 405/422 stop and hand off to user
4. On `main`: `git mv docs/active/<branch> docs/historical/<branch>` + commit + push (single atomic commit)
5. On `main`: move STATUS.md row Active → Archived + commit + push (separate commit)
6. Optional: delete merged branch
</required>

# Finishing a Research Branch

Announce at start: "I'm using the finishing-a-research-branch skill to close out `<branch-name>`."

Two paths, keyed off STATUS.md's `workflow_mode`:

- `workflow_mode: branches` (default) — steps 1 through 6, PR ceremony included.
- `workflow_mode: main_only` — skip steps 2, 3, and 6; the directory move + STATUS update happen directly on `main`. Step 1's gate still applies.

## Step 1: Confirmation gate

**CONFIRMATION GATE.** *"I'm about to close out `<branch-name>`: checkpoint the final session (finish-convo), audit the docs, then open a PR to merge into `main`. After merge, I'll move `docs/active/<branch-name>/` to `docs/historical/<branch-name>/` and update STATUS.md's archived-lines table. Confirm."*

> **(novice:** explain that this is "finalizing your research line into the permanent record. After this, the work is part of `main` — the canonical version of the repo — and the active directory moves to `historical` so future sessions know it's complete. The work isn't deleted; just relocated to the 'done' shelf.") **(fluent:** just do it.)

Do not proceed past this step without the user's explicit "yes" (or equivalent).

## Step 1.5: Checkpoint and audit the line before anything merges (both modes)

The merge is the one-way door; whatever isn't on the branch when it swings shut needs a second PR to fix. Two sub-steps, in order, while the line is still open:

**1.5a — finish-convo.** Read and follow `template/skills/finish-convo/SKILL.md`. This captures the final session — convo doc + RESEARCH_LOG entry — into `docs/active/<branch-name>/`, committed on the branch. The PR then carries the line's complete record, including its own close-out session.

**1.5b — audit-docs.** Read and follow `template/skills/audit-docs/SKILL.md`. Fix whatever it flags and commit the fixes on the branch — don't ship a broken doc tree to `historical/`. If a flagged problem needs the user (orphaned file of unclear provenance, missing convo that can't be reconstructed), surface it and wait; the ceremony pauses here, not after merge.

Skipping either sub-step and merging anyway defeats the ceremony — see Common mistakes. In `main_only` mode both sub-steps still run; they just commit to `main` directly before the Step 4 archive move.

## Step 2: Open the PR (branches mode only)

No native-git equivalent — `git push` publishes commits but does not open a pull request.

```bash
curl -sX POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/$USERNAME/$REPO/pulls" \
  -d "{\"title\":\"<branch-name>: <one-line summary>\",\"head\":\"<branch-name>\",\"base\":\"main\",\"body\":\"<short summary of what was learned>\"}"
```

The response includes `number` (PR number) and `html_url` (link the user can visit). Capture both.

## Step 3: Merge the PR (branches mode only)

Also no native-git equivalent — a local `git merge` + `git push` would bypass GitHub's PR machinery and lose the PR record.

This PUT is the **only** merge affordance in the whole workflow. If Step 1.5 (finish-convo + audit-docs) has not run this session, stop and go back — do not merge a line whose final session is uncaptured.

```bash
curl -sX PUT -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/$USERNAME/$REPO/pulls/<number>/merge" \
  -d "{\"merge_method\":\"merge\"}"
```

Outcomes:

- **200 success** → continue to Step 4.
- **405 Method Not Allowed** or **422 Unprocessable Entity** → the merge is blocked. Most common cause: branch protection requires review before merge. This is the **collaborator-mode case** (see RESEARCHER.md "Known v1 limitations"). **Stop here.** Surface the PR URL to the user; tell them the owner needs to review and merge in the GitHub web UI. Steps 4–5 wait for a future session — typically the owner will do them after merging.
- Other 4xx/5xx → surface the response body to the user; don't retry blindly.

## Step 4: Move `docs/active/<branch>/` to `docs/historical/<branch>/` on main

Single atomic commit — the `git mv` preserves history so `git log --follow` traces files across the move:

```bash
cd /home/claude/${REPO}
git checkout main
git pull --ff-only origin main            # pull in the just-merged PR
git mv docs/active/<branch-name> docs/historical/<branch-name>
git commit -m "Archive <branch-name>: <one-line summary>"
git push origin main
```

If you want to inspect what's about to move first: `git ls-tree -r HEAD docs/active/<branch-name>/`.

**In `main_only` mode:** you're already on `main` and there's no just-merged PR to pull — the `git pull --ff-only` step is still a good idea (another session may have pushed), but the branch checkout and PR-pull framing don't apply.

## Step 5: Move the STATUS.md row Active → Archived

Separate commit from Step 4 — the directory move and the index update are different concerns; keeping them separate makes history readable.

Edit STATUS.md on `main`:

- **Delete** the `<branch-name>` row from the `## Active Research Lines` table.
- **Add** a row to the `## Archived Research Lines` table with:
  - **Summary** — written *fresh at close* (1 sentence, ≤2 if needed): what was *learned*, not what was attempted. **Do not** copy the Active row's Purpose — Purpose says what the line set out to do and is usually stale by merge time.
  - **Archived** — today, `YYYY-MM-DD`.
  - **Material** — a reference that *resolves*: `docs/historical/<branch-name>/`, a shared/consolidated dir, a results path, or the merged PR URL. One row per research line even when dirs are consolidated.

If the branch carried content edits that were relocated during a STATUS migration or take-main conflict resolution, grep-verify they survived somewhere reachable before committing.

```bash
git add STATUS.md
git commit -m "STATUS: archive <branch-name> (merge ceremony)"
git push origin main
```

This ceremony and `start-research-line` are the **only** writers of STATUS.md in `branches` mode — sessions never touch it (see RESEARCHER.md §2c boundary).

**Push race.** Steps 4 and 5 both push `main`, and STATUS.md is the shared choke point between `start-research-line` and this skill. If a concurrent ceremony lands between your pull and your push, either push comes back rejected (non-fast-forward). Recover per the `resolve-runtime-issue` skill's entry for rejected pushes: `git pull --rebase origin main`; if the only conflicts are both-sides-appended rows in lifecycle tables, resolve with `template/scripts/resolve_append_conflict.py` (keeps both rows — row order in these tables doesn't encode precedence); any conflict involving your Active-row *deletion* goes to the user (keep-both would resurrect the deleted row).

## Step 6: (Optional) delete the merged branch

Default to deleting to keep the branch list tidy; ask if the user has a reason to keep it.

```bash
git push origin --delete <branch-name>
git branch -D <branch-name>          # also clean up the local ref
```

GitHub's merged-PR UI also exposes a "Delete branch" button — either works.

## Report

Tell the user briefly:

```
Research line closed:
  PR:       #<number> merged into main       (branches mode; omit for main_only)
  Docs:     docs/historical/<branch-name>/   (moved from active)
  STATUS:   row moved Active → Archived
  Branch:   deleted                          (or "kept" per user preference; omit for main_only)
```

# Common mistakes

**Merging without running Step 1.5 first**
- Problem: The merge lands, then finish-convo has nowhere to write — `docs/active/<branch>/` is being archived, the branch is closing, and the final session's record either dies with the sandbox or needs a second PR. The line's permanent history is missing its own conclusion.
- Fix: Step 1.5 is not optional and its order is load-bearing: checkpoint + audit happen while the line is still open. The Step 3 merge call is the workflow's only merge affordance — treat "1.5 ran this session" as its precondition.

**Skipping the STATUS row move**
- Problem: `docs/active/<branch>/` becomes `docs/historical/<branch>/` on disk, but STATUS's Active table still lists it. Future sessions read STATUS, think the line is live, and get confused when the docs aren't in `active/`.
- Fix: Step 5 is not optional. It's the closing half of the lifecycle ceremony that `start-research-line` opened.

**Combining Step 4 and Step 5 into one commit**
- Problem: A `git mv` diff and a STATUS index update in the same commit is hard to read six months later. If Step 5 has a mistake and you want to revert just the STATUS update, you can't cleanly.
- Fix: Two commits, as scripted.

**Copying the Active row's Purpose into the Archived row's Summary**
- Problem: Purpose says what the line set out to investigate; Summary says what was learned. They're rarely the same by merge time. A copy-forward gives future sessions a stale story.
- Fix: Write Summary fresh at close, in one sentence.

**Merging without the confirmation gate**
- Problem: Merging is the one-way door of the research workflow. An accidental early merge means the branch is closed before the user is done thinking.
- Fix: Step 1's gate is not optional. `finish-convo` (which does NOT merge) is the right skill when the user just wants to save and stop.
