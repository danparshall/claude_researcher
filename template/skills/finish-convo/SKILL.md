---
name: Finish-Convo
description: End a research session — runs update-docs to checkpoint all progress, then commits and pushes. Use update-docs for mid-session checkpoints without ending the session.
---

> **Note for claude.ai runtime:** this skill was written for Claude Code (local git). In claude.ai's sandbox, translate `git add` / `git commit` / `git push` to the REST `write_update` / `write_new` recipes from your Custom Instructions. The conceptual workflow below is unchanged.

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
