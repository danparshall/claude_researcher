---
name: finishing-a-research-branch
description: Use when a research line has answered its questions and the user says it is done — "ready to ship", "let's merge it". After a confirmation gate, runs finish-convo and audit-docs on the still-open line, archives docs/active → docs/historical, moves the STATUS.md row Active → Archived (rolling old rows into HISTORY.md), then opens the PR and asks before merging. Main-direct lines archive on main with no PR.
---

`{{skills_dir}}` is `~/.claude/skills` on Claude Code and `/home/claude/.claude_researcher_template/template/skills` in the claude.ai sandbox.
Sandbox-specific notes (REST for Issues/Pulls, the post-commit push hook) are in RESEARCHER.md.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Confirmation gate
2. Sync main and verify branch state
3. Run test suite IF one exists
4. Run finish-convo to checkpoint the final session
5. Run audit-docs
6. Run maintaining-decision-docs IF docs/DOCS_INDEX.md exists
7. Archive: git mv docs/active/<branch> docs/historical/<branch>; commit
8. STATUS.md: move row Active → Archived; commit. Roll over old rows; commit
9. Push branch
10. Create the PR
11. Resolve conflicts; wait for CI
12. Ask the user whether to merge
13. Merge if user said yes
14. End with the sentinel line (merged or left open)

A research line is "finished" when the investigation has answered its questions (or hit a clear stopping point) and the user has explicitly said to wrap and merge. Archiving is **preservation**, not disposal — `docs/historical/<branch>/` keeps everything accessible.

**Two paths, keyed per line.** Find the line's row in STATUS.md's Active table. If its branch column says `(no branch — main-direct)` — or, failing a branch column, STATUS.md's header declares `workflow_mode: main_only` — this is a **main-direct line**: work on `main`, skip Steps 9–13, and push `main` after Step 8. Otherwise it is a **branch line** and every step runs.

### Step 1: Confirmation gate

Say: *"I'm about to close out `<branch-name>`: checkpoint the final session (finish-convo), audit the docs, archive `docs/active/<branch-name>/` to `docs/historical/<branch-name>/`, move its STATUS row to Archived, then open a PR to merge into `main` (main-direct line: no PR). Confirm."* For a novice user, add that nothing is deleted — the line moves to the "done" shelf. Do not proceed without an explicit yes.

### Step 2: Sync main and verify branch state

```bash
git fetch origin
git rev-parse main origin/main    # must be equal; if not, git pull --ff-only origin main
git rev-parse --abbrev-ref HEAD   # branch line: must NOT be main; main-direct line: must be main
ls docs/active/<branch-name>/     # must exist
```

If `docs/active/<branch-name>/` does not exist, this was not tracked as a research line; STOP and ask the user how to proceed.

### Step 3: Run test suite IF one exists

Detect: `pyproject.toml` with `[tool.pytest]`, `pytest.ini`, `package.json` with a test script, `Cargo.toml`, `go.mod`, or a `tests/` directory with discoverable tests. If detected, run it. If tests fail, STOP — surface to the user; don't merge a failing research branch. If no test suite exists, skip silently.

### Step 4: Run finish-convo

Read and follow `{{skills_dir}}/finish-convo/SKILL.md`. This MUST run before Step 7 — finish-convo writes to `docs/active/<branch-name>/`, which must still exist. Skip finish-convo's sentinel step here; Step 14 prints it at the end.

### Step 5: Run audit-docs

Read and follow `{{skills_dir}}/audit-docs/SKILL.md`. Fix whatever is flagged — don't ship a broken doc tree to `historical/`. If a flagged problem needs the user (an orphan of unclear provenance, a convo that can't be reconstructed), surface it and wait.

### Step 6: Run maintaining-decision-docs IF DOCS_INDEX exists

If `docs/DOCS_INDEX.md` exists and `{{skills_dir}}/maintaining-decision-docs/SKILL.md` is installed, read and follow it. Otherwise skip silently.

### Step 7: Archive the line's docs (one commit)

```bash
git mv docs/active/<branch-name> docs/historical/<branch-name>
git add docs/            # also picks up Step 5/6 fixes (audit, DOCS_INDEX)
git commit -m "archive: <branch-name> — <one-line summary>"
```

### Step 8: Move the STATUS.md row, then roll over (separate commits)

Delete the line's row from the Active table ("Active Research Lines" or "Active Work-lines") and add one to the Archived table: branch name; date archived (UTC today); **Summary written fresh at close** — what was *learned*, in one sentence, not the Active row's Purpose (Purpose is usually stale by now); material path (`docs/historical/<branch-name>/`, or the merged PR URL).

```bash
git add STATUS.md
git commit -m "STATUS: archive <branch-name>"
```

**Rollover.** `KEEP_ARCHIVED = 10`. If the Archived table now has more than `KEEP_ARCHIVED` rows, move the oldest ones to `HISTORY.md`, newest first, keeping the table header. If `HISTORY.md` is absent, create it with `# HISTORY` and the line "Archived research lines rolled out of STATUS.md by `finishing-a-research-branch`, which keeps the newest 10 there. Newest first." This is the only place rows leave STATUS.md.

```bash
git add STATUS.md HISTORY.md
git commit -m "STATUS: roll <N> archived rows into HISTORY.md"
```

**Main-direct line:** `git push origin main` now, then go to Step 14. If the push is rejected, follow Step 11's conflict rules after `git pull --rebase origin main`.

### Step 9: Push

```bash
git push -u origin <branch-name>
```

### Step 10: Create the PR

<system-note> Do NOT wait for user approval. The user invoked this skill — opening the PR is part of the contract. </system-note>

Compose the PR body from the RESEARCH_LOG, recent convo summaries, and results/ — don't make findings up. Three sections: a 2-3 paragraph `## Summary` (what the line investigated, found, decided); `## Key Findings` (bullets, each with a provenance link to a results/ or convos/ file where relevant); `## Documentation` (`docs/historical/<branch-name>/` — RESEARCH_LOG.md, convos/, plans/, results/). End the body with `🤖 Generated with [Nori](https://noriagentic.com/)`. Title: `<branch-name>: <one-line summary>`. Create it with `gh pr create --title … --body …` (claude.ai: see sandbox notes).

### Step 11: Resolve conflicts and wait for CI

```bash
git fetch
git merge main      # resolve conflicts if any
gh pr checks        # poll in foreground
```

**Merge conflicts on the running ledgers.** STATUS.md and RESEARCH_LOG.md routinely conflict when other lines merged or opened first. If both sides only *added* rows or entries, resolve with `python3 {{skills_dir}}/finish-convo/resolve_append_conflict.py <file>` then `git add <file>` (read its docstring gate first). Any conflict involving your Active-row *deletion* or a moved row goes to the user — keep-both would resurrect or duplicate the row.

<system-reminder> Poll `gh pr checks` in the foreground — do NOT background-watch or 'check in later'. No CI showing usually means merge conflicts (go back and resolve); some research repos have no CI at all, in which case this step is a no-op. </system-reminder>

<system-reminder> It is *critical* that you fix any CI issues, EVEN IF YOU DID NOT CAUSE THEM. </system-reminder>

### Step 12: Ask the user whether to merge

Research branches are higher-stakes than feature branches — their merge becomes permanent main history. Default expectation is yes, but ask explicitly: "PR <URL> is open and CI is green. Merge now, or leave open for further review?"

### Step 13: Merge if user said yes

`gh pr merge` with the repo's normal merge style, then bring local `main` up to date (`git pull --ff-only origin main` wherever `main` is checked out). If the merge is refused (branch protection; the owner must review), stop and give the user the PR URL — the archive is already in the PR, so merging it completes the ceremony. Optional, ask first: delete the merged branch (`git push origin --delete <branch-name>`). If the user said leave open, skip to Step 14.

Announce: **"finishing-a-research-branch complete — <branch-name> archived and merged."**

### Step 14: Sentinel line

End your final message with the sentinel line from finish-convo step 6 (Step 4 skipped it, so it lands here, after the last push). Same shape and rules: confirm the commit is on the remote first, and print no sentinel if it isn't. `<convo-name>` is the convo file from Step 4; `<short-sha>` is the merge commit on `main` if merged, the head of `<branch-name>` pushed in Step 9 if left open, or `main`'s head for a main-direct line.
</required>

## claude.ai sandbox notes

No `gh` in the sandbox: open and merge the PR with the Pulls API, using the PAT from Project Instructions. Open: `curl -sX POST -H "Authorization: token $TOKEN" -H "Accept: application/vnd.github+json" https://api.github.com/repos/$USERNAME/$REPO/pulls -d '{"title":"…","head":"<branch-name>","base":"main","body":"…"}'` — capture `number` and `html_url`. Merge: `curl -sX PUT` (same headers) to `…/pulls/<number>/merge` with `-d '{"merge_method":"merge"}'`. A 405 or 422 means the merge is blocked (usually branch protection — collaborator mode): stop and hand the PR URL to the user. CI: skip `gh pr checks` and tell the user to check the PR page. If the session-start clone failed (degraded REST fallback), translate the directory move into per-file Contents API PUTs and say you're in degraded mode.
