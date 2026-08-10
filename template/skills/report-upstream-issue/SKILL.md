---
name: report-upstream-issue
description: Generate a pre-filled GitHub issue URL for reporting a bug in `claude_researcher` itself (this file, the skills, the bootstrap, the template scripts). Use when the user reports that `claude_researcher`'s behavior is wrong — not when they report a problem with their own research. Produces a URL the user clicks to file; does NOT file directly (v1 has no `UPSTREAM_TOKEN`).
---

## When to use

Fire when the user says something like "this skill has a bug", "the bootstrap didn't work", "RESEARCHER.md said X but Y happened", "there's a typo in the finish-convo skill". If the user is reporting a problem with their own research (data, papers, convos, plans) — that's not this skill; that's a normal session task.

## URL shape

```
https://github.com/danparshall/claude_researcher/issues/new?title=<urlencoded-title>&body=<urlencoded-body>
```

## Body — MUST include

- The user's `Git fluency` tier from `personal_info.md` (e.g., `git_fluency: novice`).
- The SHA of the RESEARCHER.md you're operating against, so triage knows which version. Get it via `cd /home/claude/.claude_researcher_template && git rev-parse HEAD`, or by GETting `https://api.github.com/repos/danparshall/claude_researcher/contents/template/RESEARCHER.md` and reading the `sha` field.
- A short repro of what the user did and what went wrong.
- A section reference where relevant (e.g., "RESEARCHER.md §3 branch resolution", "finishing-a-research-branch skill Step 3", "finish-convo skill step 3").

## Body — MUST NOT include

Scoped to *public-upstream issue bodies* — the `danparshall/claude_researcher` issue tracker is world-readable. This list does not apply to in-session PAT handling against the user's own repos (that's a separate, calibrated workflow in RESEARCHER.md §2).

- The user's PAT (`TOKEN`).
- The contents of `personal_info.md` beyond the `git_fluency` tier.
- The contents of any user research repo (papers, convos, plans, results).
- The user's GitHub username if they'd prefer not to be identified — **ask if unclear.**
- Any URL or path that includes the user's username plus a private-repo hint.

## Report

Present the URL to the user; they click through to file. Don't try to file the issue yourself — v1 doesn't include an `UPSTREAM_TOKEN` for cross-repo issue creation, and even if it did, the user should own the wording of their own bug report.

Example handoff:

> "Here's a pre-filled issue URL. Click to file — you can edit the title/body before submitting. I've included the SHA of the RESEARCHER.md I'm running, your git-fluency tier, and the repro you described. I didn't include your username; add it if you want triage to be able to follow up with you."
