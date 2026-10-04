---
name: finish-convo
description: Use when ending a research session — runs update-docs to checkpoint the session, then commits, pushes, confirms the push, and prints the close-out sentinel. Use update-docs instead for mid-session checkpoints without ending the session.
---

`{{skills_dir}}` is `~/.claude/skills` on Claude Code and `/home/claude/.claude_researcher_template/template/skills` in the claude.ai sandbox.
Sandbox-specific notes (REST for Issues/Pulls, the post-commit push hook) are in RESEARCHER.md.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Run the update-docs skill first.

Read and follow `{{skills_dir}}/update-docs/SKILL.md`. It writes the convo summary, saves results with provenance links, and writes the session's one-line RESEARCH_LOG entry. It does not write STATUS.md, except a LITE repo's `## Sessions` entry.

2. If the session produced something ready to implement:

- Ask the user: "This session produced [X] — should I create a plan doc for implementation?"
- If yes: read and follow the `write-a-plan` skill, saving to `docs/active/<line>/plans/`
- The plan MUST reference the originating convo file
- If a plan was created, give the user a one-sentence handoff to pass to the next agent — naming the plan/convo file and where to start.

2.5. If `paper_index.toml` exists at the repo root, run `python3 {{skills_dir}}/paper-index/paper_index.py check .` before committing. Do not commit a red check.

3. Stage and commit all session artefacts:

Run `git status` and account for everything the session produced or touched. At minimum:

- `docs/active/<line>/` — convo summary, RESEARCH_LOG line, plans, results (a session with no line: `RESEARCH_LOG.md`, `docs/convos/`, `docs/results/`)
- **Reports and artefacts produced during the session** — analysis outputs, figures, tables, data summaries, generated notebooks, extracted text, or any other output the work produced. Session outputs sometimes land outside the line directory — scripts at the repo root, generated files under `data/`, papers under `papers/`, etc. Stage those too. If it was produced or updated this session and belongs in the repo's history, it gets committed.
- Any code, data, or config files the session modified
- **Not `STATUS.md`** — sessions don't write it. The one exception is a LITE repo (`LITE.md` at the root), whose `## Sessions` entry update-docs just wrote.

Stage each path explicitly by name — never `git add .` or `git add -A`:

```bash
git add docs/active/<line>/ <other-files>
git commit -m "convo: <convo-name> — <one-line summary>"
```

If `git status` shows leftover untracked or modified files after the commit, resolve them explicitly (add-and-recommit, or explain to the user why they should stay out) before moving on. Do not push a partial checkpoint that silently leaves session artefacts behind.

4. Push to remote for backup:

```bash
git push -u origin <branch-name>
```

Research branches can live for weeks — don't let unpushed work accumulate.

If the push is rejected (non-fast-forward — another session pushed this branch first): `git pull --rebase`. If the only conflicts are append-on-top regions (RESEARCH_LOG.md's newest-first lines), resolve with `python3 {{skills_dir}}/finish-convo/resolve_append_conflict.py <file>` (keeps both sides), `git add <file>`, `git rebase --continue`, and push again. Any other conflict shape: surface it to the user.

5. Do NOT:
- Create a PR (research branches stay open until user explicitly asks to merge)
- Merge into main (NEVER without explicit request)
- Run the finish-branch pipeline
- Write STATUS.md (only opening and closing a line write it; LITE's `## Sessions` entry is the exception)

6. Confirm the push landed, then end your final message with the sentinel line.

Confirm first: `git fetch origin` and check that `git rev-parse HEAD` equals `git rev-parse origin/<branch-name>`. **If the push failed or the SHAs differ, print no sentinel** — report the failure instead. A sentinel means the close-out is on the remote, nothing less.

The sentinel is the last line of your final message, exactly this shape:

```
FINISH-CONVO-COMPLETE <convo-name> <short-sha> at $FINISH_TIME by $AGENT_CODENAME
```

The all-caps token is deliberate: it exists so a later check can search past chats for it and get exact hits, without colliding with ordinary discussion of this skill. Don't paraphrase it, and don't write the token anywhere else in conversation (refer to it as "the sentinel").

- `<convo-name>` — the convo file's name without `.md` (e.g. `20260314_d_axis_stability_analysis`). If the session wrote no convo file, use `-`.
- `<short-sha>` — `git rev-parse --short HEAD`, the commit you just confirmed on the remote. A later check verifies it with `git cat-file -e <sha>`.
- **Called from `finishing-a-research-branch`:** skip this step. That skill prints the sentinel itself at its end, so the chat doesn't look closed while the archive and PR steps are still running.
- `$FINISH_TIME` — a fresh `date -u +"%Y-%m-%d %H:%M UTC"`, run at this step. Do not reuse the session-start time; sessions can span days.
- `$AGENT_CODENAME` — this session's agent codename, the same string used as `user.name` on the session's commits (e.g. `<Name> (web, my-repo, 20260818T1710, fable-5.1)`), with the model slot reflecting the model you are running as now. If the session has no codename, use the model name and say so.
- **Model change mid-session (rare — flag it):** compare the model you are running as now against the one the session started with (the session-start identity line, and the model slot on this session's earlier commits). If they differ, append ` — model changed mid-session: <start-model> → <current-model>` to the sentinel line, and list any of this session's commits that carry the old model slot.
</required>
