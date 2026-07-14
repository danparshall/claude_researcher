---
name: finish-convo
description: End a research session — runs update-docs to checkpoint all progress, then commits and pushes. Use update-docs for mid-session checkpoints without ending the session.
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

**If `claude.ai sandbox`:** the user's project repo is already cloned at `/home/claude/<REPO>/` per `RESEARCHER.md` §2.0b — run the `git add` / `git commit` / `git push` commands in this skill directly from that working tree. Translate local skill paths like `/Users/<user>/.claude/skills/...` to the template clone at `/home/claude/.claude_researcher_template/template/skills/...`. Only if the §2.0b clone failed (degraded REST fallback, surfaced to the user) do you translate `git add` / `git commit` / `git push` into the Contents API recipes from your Project Instructions.

**If `Claude Code`:** follow the skill body as-is.

**If `unknown`:** stop and surface to the user. Don't guess which environment you're in — the cost of a wrong guess (operating against the wrong working tree, or using the wrong write path for the environment) is higher than the cost of one round-trip clarification.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Run the update-docs skill first.

Read and follow `/Users/dan/.claude/skills/update-docs/SKILL.md`. This creates/updates the convo summary, saves results with provenance links, and updates RESEARCH_LOG.md (plus, in `main_only` mode only, a capped STATUS one-liner — in `branches` mode STATUS.md is never written at wrap; see RESEARCHER.md §2c).

2. If the session produced something ready to implement:

- Ask the user: "This session produced [X] — should I create a plan doc for implementation?"
- If yes: read and follow the `write-a-plan` skill, saving to `docs/active/<branch-name>/plans/`
- The plan MUST reference the originating convo file

3. Stage and commit all changed files:

```bash
git add docs/active/<branch-name>/                    # branches mode: STATUS.md is NOT staged
# main_only mode only: also  git add STATUS.md         (capped Recent Sessions one-liner)
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
- Write STATUS.md at all in branches mode (lifecycle ceremonies only), or rewrite its conclusions in main_only mode
</required>
