---
name: task-triage
description: Use when the user says "task-triage," "triage," "what should I work on," "/task-triage," "/triage-tasks," or otherwise wants a cross-repo view of pending work — lists all open `task`-labeled issues across the user's GH repos, groups them by repo, and runs a conversational priority discussion. Read-only — does not modify issues. Shows date-prefixed (reminder) items inline with regular tasks; the fired-vs-pending split is `task-remind`'s job at session-start.
---

`{{skills_dir}}` is `~/.claude/skills` on Claude Code and `/home/claude/.claude_researcher_template/template/skills` in the claude.ai sandbox.
Sandbox-specific notes (REST for Issues/Pulls, the post-commit push hook) are in RESEARCHER.md.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Detect the GH user
2. Pull all open task-labeled issues
3. Present grouped inventory
4. Conversational priority discussion
5. Optionally fetch a convo doc on demand
</required>

# Triaging Tasks

Announce at start: "I'm using the `task-triage` skill to pull your open tasks and walk through priority."

The companion skill `task-create` writes these issues; this skill reads them and helps you decide what to work on next. It is **read-only** — it never closes, edits, or re-labels issues. The output is a conversation; the user takes action manually.

Date-prefixed items (titles starting with `[YYYY-MM-DD]`) are reminder-style tasks with a fire-date. **They stay in this inventory alongside non-dated tasks** — the user wants to see them all in one place. The fired-vs-pending split is `task-remind`'s job at session-start; `task-triage` is the broader "what should I work on" view.

## Step 1: Detect the GH user

```bash
gh api user --jq .login
```

This is the `--owner` filter for the search. Always derive it dynamically; don't hardcode a username.

## Step 2: Pull all open task-labeled issues

```bash
gh search issues \
  --owner "$(gh api user --jq .login)" \
  --state open \
  --label task \
  --json repository,number,title,body,url,createdAt,updatedAt,labels
```

One call, all repos in the user's GH space, only issues tagged `task`. The JSON output goes straight into your working memory.

If the result is empty: tell the user "No open tasks. Nothing to triage." and stop.

## Step 3: Present the inventory

Group by repository, sorted with most recently updated first within each group. Format:

```
== <owner>/<repo-A> ==
  #<N>  <title>                              (<age>, updated <ago>)
  #<N>  [2026-06-11] <title-without-prefix>  (<age>, updated <ago>)

== <owner>/<repo-B> ==
  #<N>  <title>                              (<age>, updated <ago>)
```

Compute `<age>` as days since `createdAt`, `<ago>` as days since `updatedAt`. If they're the same day, show just one.

**Render the `[YYYY-MM-DD]` prefix as part of the title** when the issue is date-prefixed — don't strip it (that's what `task-remind` does for its surface), and don't filter date-prefixed items out: they're tasks too, and the user wants the full view here. The prefix carries useful triage signal — "this one's already overdue," "this one fires next week" — without needing a separate column.

Parse each issue body and capture the `Convo:` and `Branch:` references into your working memory — but do **not** auto-fetch the convo docs. They get fetched only when the user wants to discuss a specific issue in depth (Step 5).

After the table, give a one-paragraph quick read: "You have N open tasks across M repos. The oldest is #X (Y days). The newest is #Z (touched Q hours ago). Anything jumping out before I propose an ordering?"

## Step 4: Conversational priority discussion

Ask 1–2 framing questions to get information that isn't in the issue bodies:
- "Anything externally time-sensitive — deadlines, people waiting on you?"
- "Anything you've already mentally written off and want me to flag for closure?"

Then propose an ordering with brief reasoning per item:

```
Proposed order:
  1. <repo>#<N>: <title>
     — <one-line reason: "feeds the X writeup", "blocking your collaborator", etc.>
  2. <repo>#<M>: <title>
     — <reason>
  ...
```

The user pushes back, refines, asks questions. Iterate until they're satisfied.

## Step 5: Deep-dive on demand

If the user says "tell me more about #N" or "why did we open that one?" or similar, *then* fetch the linked convo doc:

```bash
# If on the linked branch in the current repo:
cat docs/active/<branch>/convos/<convo-file>.md

# If on a different branch or in a different repo (most common — tasks are cross-repo):
git -C /path/to/relevant/repo show <branch>:docs/active/<branch>/convos/<convo-file>.md
```

Use the convo to answer the question. Return to the priority discussion.

## Step 6: Done

End with a one-line summary:

```
Recommended next: <repo>#<N>: <title>
```

Do **not** mutate any issues. Do **not** create a "today" or "this week" issue. The user's working agreement with themself is in their head; this skill just informed it.

# Common Mistakes

**Treating the issue body as gospel**
- Problem: The body is a snapshot at capture time — the blocker may have resolved, the priority may have shifted.
- Fix: When the user's recollection differs from the body, trust the user; offer to update the issue later, manually, but don't overwrite their understanding with a stale body.
