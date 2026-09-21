---
name: task-remind
description: Use when starting a session, or when the user says "check reminders," "what's pending," "session-start reminders," "any reminders?", "/task-remind," or similar. Session-start check for fired reminders — queries the current repo + `home_repo` for open issues with a `[YYYY-MM-DD]` title prefix, filters to those whose date is `<= today`, and presents them in two labeled sections. Reads metadata only (no body fetches). Offers close / snooze / skip / strip-prefix (last one only if the user signals uncertainty about when to revisit).
---

`{{skills_dir}}` is `~/.claude/skills` on Claude Code and `/home/claude/.claude_researcher_template/template/skills` in the claude.ai sandbox.
Sandbox-specific notes (REST for Issues/Pulls, the post-commit push hook) are in RESEARCHER.md.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Detect GH user and `home_repo`
2. Query current repo + `home_repo` (metadata only)
3. Filter to fired items (prefix date `<= today`)
4. Present two labeled sections (skip empty ones; bail early if both empty)
5. For each fired item, offer close / snooze / skip (and strip-prefix only on uncertainty signal)
6. Cross-repo escape valve pointer to `task-triage`
</required>

# Checking Reminders

Announce at start: "I'm using the `task-remind` skill to check for any pending reminders before we get going."

A **once-per-session** pre-flight check, not a heartbeat. It surfaces date-prefixed reminders that have fired (prefix date `<= today`) from the current repo plus the user's `home_repo`. Companion skills: `task-create` writes these issues (the `[YYYY-MM-DD]` prefix is what makes a task a reminder); `task-triage` is the on-demand cross-repo view, including non-dated tasks.

## Step 1: Detect GH user and `home_repo`

```bash
gh api user --jq .login                                # current GH user
gh repo view --json nameWithOwner -q .nameWithOwner    # current repo, or fails if no remote
```

Resolve `home_repo` as in `{{skills_dir}}/task-create/SKILL.md` Step 1. If the current repo and `home_repo` are the same, query once and present one section instead of two — don't double-fetch.

## Step 2: Query both repos (metadata only)

One `gh issue list` per repo. **Do not fetch issue bodies** — the title prefix is the entire filter signal.

```bash
gh issue list \
  --repo <repo> \
  --state open \
  --label task \
  --json number,title,url,updatedAt \
  --limit 200
```

If a call fails (404, no access, network), report that repo's failure and continue with the one that worked — don't block the session.

## Step 3: Filter to fired items

Parse each title against `^\[(\d{4}-\d{2}-\d{2})\] (.*)$`. No match → a plain task, which `task-remind` ignores (that's `task-triage`'s job). On a match, the captured date is the fire-date.

Compute today with `date -u +%Y-%m-%d`. A reminder has **fired** if its prefix date is `<=` today (ISO dates sort correctly as strings — plain string compare, no date library). Pending reminders (prefix `>` today) are silently skipped here.

## Step 4: Present fired reminders

```
== In <current-repo> ==
  #<N>  <title without prefix>     (fired YYYY-MM-DD, <K days ago>)

== In <home-repo> ==
  #<N>  <title without prefix>     (fired YYYY-MM-DD, <K days ago>)
```

- Strip the `[YYYY-MM-DD] ` prefix from the displayed title (redundant with the parenthetical).
- "K days ago": "Today" if K=0, "yesterday" if K=1, else "N days ago".
- Omit an empty section's header entirely.
- If **both** sections are empty, output one line and stop: *"No reminders pending. Continuing with session-start."* No empty headers, no commentary, no "want me to triage?".

## Step 5: Per-fired-item action menu

Interactive, one item at a time, smallest menu by default — *"close, snooze, or skip?"*:

- **Close** — done. `gh issue close <N> --repo <owner>/<repo> --comment "Done"`.
- **Snooze N days** — ask the user for `N`, don't default one (*"How long? (e.g., '3 days', 'next Monday')"*). Mutate the prefix to today + N: `gh issue edit <N> --repo <owner>/<repo> --title "[<new-date>] <rest>"`. Use the same BSD/GNU `date` fallback as `task-create` Step 3.
- **Skip** — no action; fires again next session.

**Strip-prefix is conditional.** Offer it only if the user signals uncertainty about when to revisit (*"ugh, I don't know," "not sure when," "someday," "open-ended"*) — offering it unprompted suggests giving up on the reminder, which most users don't want. When it fires: `gh issue edit <N> --repo <owner>/<repo> --title "<rest without prefix>"`. The item then drops out of `task-remind`'s view and lives on `task-triage`'s open-task list.

When you mutate an issue (snooze or strip), briefly say what changed — e.g., *"Snoozed to 2026-06-11"* — so the user knows what happened on the back-end.

## Step 6: Cross-repo escape valve

After processing all fired items (or after the empty-both-sections bail, if the user wants to dig deeper anyway), close with one line, and don't auto-run it:

> *"Want a full view of every open task across all your repos? Run `task-triage`."*
