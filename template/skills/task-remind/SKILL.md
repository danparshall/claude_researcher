---
name: Task-Remind
description: Session-start check for fired reminders. Queries the current repo + `home_repo` for open issues with a `[YYYY-MM-DD]` title prefix, filters to those whose date is `<= today`, and presents them in two labeled sections. Reads metadata only (no body fetches). Offers close / snooze / skip / strip-prefix (last one only if the user signals uncertainty about when to revisit). Use at session-start, or when the user says "check reminders," "what's pending," "session-start reminders," "any reminders?", "/task-remind," or similar.
nori_researcher_source: nori-researcher/skills/task-remind/SKILL.md@8b619b5 (2026-06-04)
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

**If `claude.ai sandbox`:** translate every `gh issue list` / `gh issue edit` / `gh issue close` / `gh repo view` / `gh api user` and every `git add` / `git commit` / `git push` in this skill into the GitHub REST API recipes from your Project Instructions (the `write_update` / `write_new` recipes for files; the `GET /repos/{owner}/{repo}/issues`, `PATCH /repos/{owner}/{repo}/issues/{number}`, and `GET /user` endpoints for issues). Translate local paths like `/Users/<user>/.claude/skills/...` into `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/...` URLs (fetched via WebFetch).

**If `Claude Code`:** follow the skill body as-is.

**If `unknown`:** stop and surface to the user. Don't guess which environment you're in — the cost of a wrong guess (running `git push` in a sandbox with no git, or writing REST calls against a local working tree) is higher than the cost of one round-trip clarification.

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

Announce at start: "I'm using the Task-Remind skill to check for any pending reminders before we get going."

This is a **once-per-session** pre-flight check, not a heartbeat. It surfaces date-prefixed reminders that have fired (prefix date `<= today`) from the current repo plus the user's personal `home_repo`. Fired items get an interactive close / snooze / skip menu. For the full cross-repo open-task inventory, see the companion skill `task-triage`.

Companion skills:
- `task-create` writes the issues this skill reads. The `[YYYY-MM-DD]` title prefix is what makes a task a "reminder" — without the prefix, the issue is a plain task and never fires here.
- `task-triage` is the on-demand cross-repo view (includes non-dated tasks too).

## Step 1: Detect GH user and `home_repo`

Run in parallel:

```bash
gh api user --jq .login                                # current GH user
gh repo view --json nameWithOwner -q .nameWithOwner    # current repo (or fails if no remote)
```

Read `home_repo` from `personal_info.md` (typically `~/code/claude_research_config/personal_info.md` or wherever the user's config repo is cloned). Look for a line shaped `home_repo: <owner>/<repo>`. If the file is missing or the key is absent, default to `<gh-user>/claude_research_config` derived from the GH user.

If the current repo and `home_repo` are the same (the user is *in* their config repo), query once and present one section instead of two. Don't double-fetch the same repo.

## Step 2: Query both repos (metadata only)

Two `gh issue list` calls, one per repo, with `--state open --label task` and a metadata-only field set. **Do not fetch issue bodies** — the title prefix is the entire filter signal.

```bash
gh issue list \
  --repo <current-repo> \
  --state open \
  --label task \
  --json number,title,url,updatedAt \
  --limit 200

gh issue list \
  --repo <home-repo> \
  --state open \
  --label task \
  --json number,title,url,updatedAt \
  --limit 200
```

If either call fails (404, no access, network), report the failure for that repo and continue with the one that worked. Don't block the session on a single repo being unavailable.

## Step 3: Filter to fired items

For each returned issue, parse the title against the regex:

```
^\[(\d{4}-\d{2}-\d{2})\] (.*)$
```

If it matches, the date capture group is the fire-date. Otherwise the issue is a plain (non-reminder) task and **`task-remind` ignores it** — that's `task-triage`'s job.

Compute today's date:

```bash
date -u +%Y-%m-%d
```

A reminder has **fired** if its prefix date is lexicographically `<=` today (ISO-8601 dates sort correctly as strings, so a plain string compare is fine — no date library needed). Pending reminders (prefix `>` today) are silently skipped at this step; the user doesn't need to see them at session-start.

## Step 4: Present fired reminders

Format:

```
== In <current-repo> ==
  #<N>  <title without prefix>     (fired YYYY-MM-DD, <K days ago>)
  ...

== In <home-repo> ==
  #<N>  <title without prefix>     (fired YYYY-MM-DD, <K days ago>)
  ...
```

- Strip the `[YYYY-MM-DD] ` prefix from the displayed title (it's redundant with the parenthetical).
- Compute "K days ago" from today's date and the prefix date. "Today" if K=0; "yesterday" if K=1; "N days ago" otherwise.
- If a section is empty, **omit the section header entirely** — don't print "== In <repo> == (nothing)".
- If **both** sections are empty after filtering, output a single line and stop:

  > *"No reminders pending. Continuing with session-start."*

  Don't print empty headers, don't add commentary, don't ask "want me to triage?" — that's noise when there's nothing to surface.

## Step 5: Per-fired-item action menu

For each fired item, offer the following actions (interactive, one at a time, smallest menu by default):

- **Close** — the reminder is done. Run `gh issue close <N> --comment "Done"` against the appropriate repo (use `--repo <owner>/<repo>`).
- **Snooze N days** — the user picks `N`. Mutate the title's date prefix to today + N. Use `gh issue edit <N> --repo <owner>/<repo> --title "[<new-date>] <rest>"`. **Don't default to a specific N** — ask the user. Common phrasing: *"How long? (e.g., '3 days', 'next Monday')."* Use the same BSD/GNU `date` fallback as `task-create`'s Step 2.5.
- **Skip** — no action this session. The reminder stays in the current state and fires again next session.

**Strip-prefix is conditional.** Only offer it if the user signals uncertainty about when to revisit — phrases like *"ugh, I don't know,"* *"not sure when,"* *"someday,"* *"open-ended."* When the signal fires, offer:

- **Strip prefix** — convert the reminder back into an open-ended task. `gh issue edit <N> --repo <owner>/<repo> --title "<rest without prefix>"`. The item then moves out of `task-remind`'s view (no prefix → no fire date) and lives on `task-triage`'s open-task list until the user comes back to it.

Don't menu-dump every option upfront. The default presentation is *"close, snooze, or skip?"*. Strip-prefix shows up only when the user's reaction earns it.

When mutating an issue (snooze or strip), briefly say what the mutation was — e.g., *"Snoozed to 2026-06-11"* or *"Stripped prefix — this is now an open-ended task in `task-triage`."* That's the LIGHT-explanation discipline (see `RESEARCHER.md` §0); the user might want to know what just changed on the back-end.

## Step 6: Cross-repo escape valve

After processing all fired items (or after the bail-early empty-both-sections case if the user wants to dig deeper anyway), close with a single line:

> *"Want a full view of every open task across all your repos? Run `task-triage`."*

Don't auto-run `task-triage` — it's the user's call. The escape valve is just a pointer.

# Common Mistakes

**Fetching issue bodies**
- Problem: Wastes I/O and context. The `[YYYY-MM-DD]` title prefix is the entire filter signal at session-start; the body is irrelevant until the user wants to dig into a specific item.
- Fix: Always use `--json number,title,url,updatedAt` — no `body`, no `labels`. The `task` label is already implied by `--label task`.

**Auto-snoozing on the user's behalf**
- Problem: The agent picks "+7 days" because it seems reasonable, but the user actually wanted "+3 days" or "tomorrow." The user has context the agent doesn't.
- Fix: Always ask. The user picks the new date. This matches the "don't infer — ask" rule in `RESEARCHER.md` §5.

**Running on every turn instead of only session-start**
- Problem: `task-remind` is a one-shot pre-flight check. Re-running it every turn floods the session with the same list and breaks the "background subagent" framing.
- Fix: Once per session. If the user wants to re-check mid-session (e.g., after creating a new reminder), they can invoke it explicitly.

**Showing non-fired (future-dated) reminders**
- Problem: The user sees a long list at session-start, most of which is "fires in 5 days" / "fires in 3 weeks" — noise they didn't ask for.
- Fix: Filter strictly to `prefix <= today`. Future reminders silently skip. They'll surface on the day they fire.

**Showing non-dated tasks**
- Problem: `task-remind` and `task-triage` overlap if `task-remind` shows tasks without a `[YYYY-MM-DD]` prefix. The session-start surface becomes a full task inventory, defeating the point of the date encoding.
- Fix: Only items with the prefix regex are reminders. Non-prefixed open tasks belong to `task-triage`, not here.

**Menu-dumping all four actions upfront**
- Problem: "Close, snooze, skip, or strip prefix?" presents four options when most reminders only need three (close/snooze/skip). The fourth signals "you can give up on this whole reminder," which isn't what most users want — but offering it suggests it.
- Fix: Default menu is three options. Strip-prefix only surfaces if the user's reaction signals uncertainty (e.g., "ugh, I don't know when").

**Hardcoding the home repo name**
- Problem: The skill breaks for users who set `home_repo` to a non-default value.
- Fix: Always read `home_repo` from `personal_info.md` first; fall back to `<gh-user>/claude_research_config` only if unset.
