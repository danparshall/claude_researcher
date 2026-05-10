---
name: Finish-Convo
description: End a research session — runs update-docs to checkpoint all progress, then commits and pushes. Use update-docs for mid-session checkpoints without ending the session.
---

## Runtime detection

Before following the rest of this skill, determine your environment:

```bash
if [ "$IS_SANDBOX" = "yes" ] || [ -d "/mnt/skills/public" ]; then
  echo "claude.ai sandbox"
else
  echo "Claude Code"
fi
```

**If `claude.ai sandbox`:** translate every `git add` / `git commit` / `git push` in this skill into the REST `write_update` / `write_new` recipes from your Custom Instructions. Translate local paths like `/Users/<user>/.claude/skills/...` into `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/...` URLs (fetched via WebFetch).

**If `Claude Code`:** follow the skill body as-is.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Run the update-docs skill first.

Read and follow `/Users/dan/.claude/skills/update-docs/SKILL.md`. This creates/updates the convo summary, saves results with provenance links, and updates RESEARCH_LOG.md and STATUS.md.

2. If the session produced something ready to implement:

- Ask the user: "This session produced [X] — should I create a plan doc for implementation?"
- If yes: read and follow the `write-a-plan` skill, saving to `docs/active/<branch-name>/plans/`
- The plan MUST reference the originating convo file

3. Stage and commit all changed files:

```bash
git add docs/active/<branch-name>/ STATUS.md
git commit -m "convo: <convo-name> — <one-line summary>"
```

- Add specific files, NOT `git add .` or `git add -A`
- If other files were changed during the session (code, data, etc.), include those too

4. Push to remote for backup:

```bash
git push -u origin <branch-name>
```

Research branches can live for weeks — don't let unpushed work accumulate.

5. Do NOT:
- Create a PR (research branches stay open until user explicitly asks to merge)
- Merge into main (NEVER without explicit request)
- Run the finish-branch pipeline
- Rewrite STATUS.md with authoritative conclusions
</required>
