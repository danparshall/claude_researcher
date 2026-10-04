---
name: task-create
description: Use when the user says "add a task," "add task," "capture this," "capture a task," "open a task," "track this for later," "remind me later," "add a reminder," "track this with a date," or similar. Converts "I should remember to do X" into a tracked GitHub issue — auto-detects repo/branch/convo, drafts title+summary and creates the issue without an approval round-trip, asks "when?" only if no date is stated or implied (optional ISO date prefix for reminder-style items) with a `task` label, back-links the issue from the convo doc, and auto-commits the back-link.
---

`{{skills_dir}}` is `~/.claude/skills` on Claude Code and `/home/claude/.claude_researcher_template/template/skills` in the claude.ai sandbox.
Sandbox-specific notes (REST for Issues/Pulls, the post-commit push hook) are in RESEARCHER.md.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Detect context (repo, branch, convo doc, GH user)
2. Draft title + summary
3. Determine the date — use one from context if stated or implied; otherwise ask "when?" (optional `[YYYY-MM-DD]` prefix)
4. Ensure `task` label exists in target repo
5. Create the issue
6. Append back-link to convo doc (with cross-repo prompt if routed elsewhere)
</required>

# Creating a Task

Announce at start: "I'm using the `task-create` skill to open a tracked issue for this."

Externalize a TODO onto a single discoverable surface — GH issues with the `task` label. Companions: `task-remind` surfaces fired reminders at session-start; `task-triage` is the cross-repo priority view.

## Step 1: Detect context

Run in parallel:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner    # current repo, or fails if no remote
git branch --show-current                              # current branch
gh api user --jq .login                                # current GH user (for fallback)
```

Find the most recent convo doc on the current branch (research repos only):

```bash
ls -t "docs/active/$(git branch --show-current)/convos/"*.md 2>/dev/null | head -1
```

Determine the target repo:

| Situation | Target repo |
| --- | --- |
| In a git repo with a GH remote | That repo |
| Not in a git repo, OR no GH remote | `home_repo`; fall back to `<gh-user>/claude_research_config` |
| User says "my personal list" / "personal task" / "real-world task" | Same: `home_repo` or fallback |
| User overrides with a specific repo | What they said |

Read `home_repo` from the `- **Home repo:** <owner>/<repo>` field under `## Operating preferences` in `personal_info.md` (usually `~/code/claude_research_config/personal_info.md`); if the file or field is missing, default to `<gh-user>/claude_research_config`. When you fall through to the default, tell the user in one clause where it landed. If the user names a repo that doesn't exist or that they can't access, surface the error from `gh issue create` and offer to retry with a different target.

## Step 2: Draft title and summary

- **Title:** one line, imperative for actions ("Rerun d-axis sweep with corrected BCs"). Under ~70 chars.
- **Summary:** 1–2 sentences — enough for future triage to judge priority without opening the convo. Note what makes it important if that's non-obvious.

**Real-world task exception:** when the task isn't tied to a convo doc, the issue body is the only place operational details live. Append the concrete details the user gave (dates, contacts, flight numbers, addresses, amounts) below the summary, as a list — keep the summary itself short.

Do NOT pause for approval — draft and proceed. The Report is the review surface; issues are cheap to retitle or re-body afterward with `gh issue edit`. The only question this skill may ask is "when?" (Step 3), and only when the date is genuinely unknown.

<good-example>
Rerun d-axis sweep with corrected BCs
Prior sweep used the wrong boundary conditions; results feed the March writeup.
</good-example>
<bad-example>
Rerun the d-axis sweep
We talked about how last week's sweep might have used the wrong BCs, and I was going to rerun it, but first check the config, and there's the March writeup thing where... [sprawls — too long to triage without opening the convo]
</bad-example>

## Step 3: Determine the date

If the request states or implies a date ("remind me Monday," "in a month," "before the Sept 1 deadline"), convert to ISO and skip the question. Otherwise ask:

> *"Should this fire on a specific date, or is it open-ended? Saying a date turns this into a reminder you'll see at session-start; saying 'no date' keeps it on the regular triage list. You can always re-date later by editing the issue title."*

Accept an ISO date (use as-is), a relative date (convert to ISO — BSD/macOS form first, GNU/Linux fallback), or "no date" / "open-ended" / "skip" / silence (no prefix — a plain task, not a reminder).

```bash
date -u -v+7d +%Y-%m-%d        # BSD/macOS — '+7 days from now'
date -u -d '+7 days' +%Y-%m-%d # GNU/Linux equivalent
```

For "next Monday"-style phrases GNU `date -d 'next monday'` works directly; on BSD/macOS compute the offset manually (today Thursday → Monday is +4 days → `date -u -v+4d +%Y-%m-%d`). If both forms fail, surface it and ask for an ISO date directly — don't silently skip the prefix.

If a date is given, prepend `[YYYY-MM-DD] ` to the title and proceed to Step 4. When you inferred it from context rather than a direct answer, say so in the Report so the user can re-date.

<system-reminder>The `[YYYY-MM-DD]` prefix is the entire mechanism `task-remind` reads at session-start. Without it a reminder-shaped task files as a plain task and never fires.</system-reminder>

## Step 4: Ensure the `task` label exists

Idempotent — run every time; the grep guard makes create a no-op when the label already exists.

```bash
gh label list --repo <owner/repo> --json name -q '.[].name' | grep -qx task || \
  gh label create task --repo <owner/repo> --description "Tracked todo (task-create skill)"
```

## Step 5: Create the issue

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

## Step 6: Back-link from the convo doc

If a convo doc was detected in Step 1, append (or extend) a `## Captured Tasks` section at the end of it — a bullet if the header already exists, rather than duplicating it. Otherwise skip this whole step (no back-link, no commit).

```markdown
## Captured Tasks

- [#<N>: <title>](<issue url>) — captured YYYY-MM-DD
```

If the target repo differs from the current repo (the personal-list path), the convo and the issue live in different repos. Back-link anyway, and note in the Report that the link is one-way — the convo points at the issue, but the issue's `Convo:` path is in another repo. Don't block on a question. If the target repo *is* the current repo, proceed silently.

Commit the convo doc:

```bash
git add docs/active/<branch>/convos/<file>.md
git commit -m "$(cat <<'EOF'
convo: link captured issue #<N>
EOF
)"
```

<system-reminder>Use the heredoc form — a single-line `git commit -m "..."` trips a bug in the Nori commit-author hook that writes literal `\n` into the body. `git add <file>` will also stage any other uncommitted edits in that file; commit those separately first if they shouldn't ride along. Do not push — that's the user's call (covered by `finish-convo` at session end).</system-reminder>

## Report

```
Captured:        <issue url>
Title:           <final title, including any [YYYY-MM-DD] prefix>
Summary:         <summary>
Repo:            <owner/repo>
Back-linked in:  <convo doc path or 'no convo doc — issue stands alone'>
Committed:       <commit sha or 'no — issue stands alone'>
```
