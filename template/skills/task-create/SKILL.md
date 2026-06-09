---
name: Task-Create
description: Convert "I should remember to do X" into a tracked GitHub issue — auto-detects repo/branch/convo, drafts title+summary for user approval, asks "when?" (optional ISO date prefix for reminder-style items), creates the issue with a `task` label, back-links the issue from the convo doc, and auto-commits the back-link. Use when the user says "add a task," "add task," "capture this," "capture a task," "open a task," "track this for later," "remind me later," "add a reminder," "track this with a date," or similar.
nori_researcher_source: nori-researcher/skills/task-create/SKILL.md@8b619b5 (2026-06-04)
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

Both environments set positive markers; the probe checks for either side affirmatively rather than inferring from absence. If neither fires, something is misconfigured (env vars stripped, custom shell, etc.) and silently picking a branch is worse than surfacing the question.

**If `claude.ai sandbox`:** the user's project repo is already cloned at `/home/claude/<REPO>/` per `RESEARCHER.md` §2.0b — run the `git add` / `git commit` / `git push` commands in this skill directly from that working tree. Translate local skill paths like `/Users/<user>/.claude/skills/...` to the template clone at `/home/claude/.claude_researcher_template/template/skills/...`. Only if the §2.0b clone failed (degraded REST fallback, surfaced to the user) do you translate `git add` / `git commit` / `git push` into the Contents API recipes from your Project Instructions. The `gh` verbs in this skill (`gh issue create` / `gh issue list` / `gh issue edit` / `gh issue close` / `gh search issues` / `gh label list` / `gh label create` / `gh repo view` / `gh api user`) still translate to the GitHub REST endpoints from your Project Instructions (`POST /repos/{owner}/{repo}/issues`, `PATCH /repos/{owner}/{repo}/issues/{number}`, `GET /repos/{owner}/{repo}/issues`, `GET /search/issues`, `GET /user`) — Issues and Pulls remain REST surfaces per `RESEARCHER.md` §2.0b. (gh-CLI adoption is tracked separately in upstream issue #27.)

**If `Claude Code`:** follow the skill body as-is.

**If `unknown`:** stop and surface to the user. Don't guess which environment you're in — the cost of a wrong guess (operating against the wrong working tree, or using the wrong write path for the environment) is higher than the cost of one round-trip clarification.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Detect context (repo, branch, convo doc, GH user)
2. Draft title + summary; present for approval
3. Ask "when?" — optional `[YYYY-MM-DD]` prefix; re-present + re-approve if a date was added
4. Ensure `task` label exists in target repo
5. Create the issue
6. Append back-link to convo doc (with cross-repo prompt if routed elsewhere)
</required>

# Creating a Task

Announce at start: "I'm using the Task-Create skill to open a tracked issue for this."

The goal is to externalize a TODO out of the user's head and into a single discoverable surface (GH issues with the `task` label). Companion skills:
- `task-remind` runs at session-start and surfaces fired reminders (items whose `[YYYY-MM-DD]` title prefix is `<= today`).
- `task-triage` is the cross-repo on-demand inventory and priority discussion.

## Step 1: Detect context

Run these in parallel:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner    # current repo (owner/name) or fails if no remote
git branch --show-current                              # current branch
gh api user --jq .login                                # current GH user (for fallback)
```

Find the most recent convo doc on the current branch (research repos only):

```bash
BRANCH=$(git branch --show-current)
ls -t "docs/active/$BRANCH/convos/"*.md 2>/dev/null | head -1
```

**Determining the target repo:**

| Situation                                                            | Target repo                                                                                 |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| In a git repo with a GH remote                                       | That repo                                                                                   |
| Not in a git repo, OR no GH remote                                   | Read `home_repo` from `personal_info.md`; fall back to `<gh-user>/claude_research_config` if unset |
| User says "my personal list" / "personal task" / "real-world task"   | Same: `home_repo` or fallback                                                               |
| User overrides with a specific repo                                  | What they said                                                                              |

**Reading `home_repo`:** look in `personal_info.md` (typically `~/code/claude_research_config/personal_info.md` or wherever the user's config repo is cloned) for the `Home repo:` field under `## Operating preferences` — formatted as `- **Home repo:** <owner>/<repo>`, matching sibling fields like `Git fluency` and `Mode`. If the file is missing or the field is absent, derive `<gh-user>` from `gh api user --jq .login` and use `<gh-user>/claude_research_config` as the default. A missing `personal_info.md` is not a hard failure — just fall through to the default.

When falling through to a default, briefly say so to the user (one clause, not a paragraph) — e.g., *"Routing this to `<gh-user>/claude_research_config` since you didn't set a `home_repo`."* That way they know where it landed without you stopping to confirm. (See `RESEARCHER.md` §0 — LIGHT explanation of back-end behavior.)

If the user names a repo that doesn't exist or that they don't have access to, surface the error from `gh issue create` and offer to retry with a different target.

## Step 2: Draft title and summary

From the immediate conversation context (the last few exchanges before the user invoked this skill), draft:

- **Title:** one line, imperative mood for actions ("Rerun d-axis sweep with corrected BCs"). Under ~70 chars.
- **Summary:** 1–2 sentences. Just enough that future-Claude can decide priority during triage *without* opening the linked convo. Mention what makes this important if it's non-obvious.

**Real-world task exception:** when the task isn't tied to a convo doc (real-world / personal / cross-repo without research context), the issue body is the *only* place operational details live — there's no convo to fall back on. In that case, after the summary, append the concrete details the user provided (dates, contact info, flight numbers, addresses, dollar amounts, etc.). Keep the summary itself short for triage; the details go below it. Format the details as a list or sub-section, not prose.

Present the draft for approval:

```
Proposed task:
  Title:   <drafted title>
  Summary: <drafted summary>
  Repo:    <owner/repo>
  Branch:  <branch or 'none'>
  Convo:   <relative path or 'none'>

Approve, or edit?
```

The user accepts (any affirmative response, including just hitting enter) or edits any field. Do NOT proceed past Step 2.5 until they've confirmed.

## Step 2.5: Ask "when?"

After the user approves the draft in Step 2, ask:

> *"Should this fire on a specific date, or is it open-ended? Saying a date turns this into a reminder you'll see at session-start; saying 'no date' keeps it on the regular triage list. You can always re-date later by editing the issue title."*

Accept any of:
- **An ISO date** (`2026-06-11`) — use as-is.
- **A relative date** (`next Monday`, `in a week`, `tomorrow`, `3 days`) — convert to ISO.
- **"No date" / "open-ended" / "skip" / silence** — no prefix; this is a plain task, not a reminder.

**Converting relative dates to ISO.** Try the BSD/macOS form first; fall back to GNU/Linux if it fails:

```bash
date -u -v+7d +%Y-%m-%d        # BSD/macOS — '+7 days from now'
date -u -d '+7 days' +%Y-%m-%d # GNU/Linux equivalent
```

For "next Monday" / "tomorrow"-style phrases, GNU `date -d 'next monday'` works directly; on BSD/macOS you may need to compute the offset days manually (e.g., today is Thursday → Monday is +4 days → `date -u -v+4d +%Y-%m-%d`).

If both shell forms fail (some sandboxes are minimal), surface the issue to the user and ask for an ISO date directly. Do not silently skip the prefix.

If a date is given, prepend `[YYYY-MM-DD] ` to the title from Step 2. Re-present the draft with the prefix visible so the user sees the encoded form before approval:

```
Proposed task:
  Title:   [2026-06-11] Re-check egress allow-list
  Summary: ...
```

The `[YYYY-MM-DD]` prefix is what `task-remind` reads at session-start. Without it, the issue is just a regular task and never fires as a reminder.

**If a date was added, re-present the draft so the user sees the prefix before approving.** The first approval (in Step 2) was for the title/summary; the user should explicitly confirm the prefix. If no date was given, no re-approval is needed and you can proceed directly to Step 3.

## Step 3: Ensure the `task` label exists

```bash
gh label list --repo <owner/repo> --json name -q '.[].name' | grep -qx task || \
  gh label create task --repo <owner/repo> --description "Tracked todo (task-create skill)"
```

Idempotent — run it every time. The grep guard makes the create a no-op when the label already exists.

## Step 4: Create the issue

```bash
gh issue create \
  --repo <owner/repo> \
  --title "<title>" \
  --label task \
  --body "<summary>

Convo: <relative-path-or-'none'>
Branch: <branch-or-'none'>"
```

Capture the returned issue URL. Always pass `--repo` explicitly so the call works regardless of cwd.

## Step 5: Back-link from the convo doc

**Cross-repo back-link prompt.** If the target repo (from Step 1) is **not** the current repo (the "personal list" path, where `home_repo` or fallback differs from the cwd's repo), the convo doc lives in a different repo than the issue. Before back-linking, ask the user:

> *"Do you want this task linked back to today's convo doc? That's what I normally do, but the convo lives in this repo and the issue lives in `<target-repo>`, so the link is one-way."*

Default to yes if they're silent; honor a no. (See `RESEARCHER.md` §0 — LIGHT explanation of back-end behavior. The reason this needs explaining is that it's a divergence from the normal same-repo back-link.)

If the target repo *is* the current repo, skip the prompt and proceed silently.

If a convo doc was detected in Step 1 (and the user said yes, or the prompt didn't apply), append (or extend) a `## Captured Tasks` section at the end of the file:

```markdown
## Captured Tasks

- [#<N>: <title>](<issue url>) — captured YYYY-MM-DD
```

If the section already exists, append a new bullet (don't duplicate the header). If no convo doc exists, skip Step 5 entirely (no back-link, no commit).

Then commit the convo doc:

```bash
git add docs/active/<branch>/convos/<file>.md
git commit -m "$(cat <<'EOF'
convo: link captured issue #<N>
EOF
)"
```

Use heredoc form for the commit message — `git commit -m "single line"` triggers a known bug in the Nori commit-author hook that produces literal `\n` in the message body. Heredoc avoids it.

**Caveat:** if the convo doc has *other* uncommitted edits, `git add <file>` will stage them too and they'll ride along in the commit. If you want to keep them separate, save and commit unrelated edits before invoking this skill.

Do **not** push automatically — pushing is the user's call (covered by `finish-convo` at session end).

## Step 6: Done

Report:

```
Captured:        <issue url>
Back-linked in:  <convo doc path or 'no convo doc — issue stands alone'>
Committed:       <commit sha or 'no — issue stands alone'>
```

# Common Mistakes

**Drafting a wall-of-text summary**
- Problem: Triage becomes slow because the issue body is too long to skim.
- Fix: 1–2 sentences. The convo doc is the canonical source; the issue is the pointer.

**Skipping the convo back-link**
- Problem: The convo doc doesn't record what got externalized. Broken bidirectional link, and future sessions can't easily find what tasks came out of past thinking.
- Fix: Always append the `## Captured Tasks` line when a convo exists.

**Skipping user approval**
- Problem: Bad title/summary lives in the issue forever; renaming GH issues is doable but tedious.
- Fix: Always present the draft and wait for approval, even if the user seems impatient.

**Hardcoding a username**
- Problem: The skill breaks for other users who copy this profile.
- Fix: Always derive the GH user via `gh api user --jq .login`. Never hardcode.

**Creating the issue on the wrong repo**
- Problem: A task about repo A gets filed in repo B because the user's cwd is wherever — issues become hard to find later.
- Fix: Always pass `--repo` explicitly based on Step 1's detection. Briefly announce the target when falling back to `home_repo` or the default (`<gh-user>/claude_research_config`) so the user knows where it landed.

**Forgetting to ask "when?"**
- Problem: The `[YYYY-MM-DD]` prefix is the entire mechanism that lets `task-remind` find reminders cheaply at session-start. Skipping the question means a reminder-shaped task gets filed as a regular task and never fires — the user thinks they set a reminder, but the prefix is missing, and session-start never surfaces it.
- Fix: Always ask in Step 2.5, even if context strongly implies a date. The user gets "no date" as a valid answer; don't pre-decide for them.

**Routing a personal task to the current research repo**
- Problem: "Remind me about the dentist next month" filed against the research repo clutters its issue list with non-research items.
- Fix: When the user signals "personal" / "my personal list" / "real-world task" / similar, route to `home_repo` (or the default) per the Step 1 table. The cross-repo back-link prompt in Step 5 handles the convo-doc affordance.
