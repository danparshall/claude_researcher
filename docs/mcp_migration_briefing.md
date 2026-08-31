# Briefing — migrate claude_researcher off PAT-in-Project-Instructions to MCP

Written by a Claude Code session (Opus 4.7, CLI, laptop) for a Fable session on claude.ai web. You (Fable) will design and build. This is a cold handoff — everything you need is in this doc or linked from it. Do not assume shared context.

## The task

The `claude_researcher` public workflow (github.com/danparshall/claude_researcher) currently authenticates claude.ai web sessions to GitHub by embedding a rotating fine-grained PAT in the Project Instructions field. See `template/_PROJECT_INSTRUCTIONS.md.template` in that repo for the current design. The PAT is scoped to two repos (read `<user>/claude_research_config`, read/write `<user>/<project_repo>`) and rotated manually.

The user (Dan) wants this replaced with an MCP-based flow so he never has to copy-paste a credential again. That's your job: design the replacement, build whatever custom pieces are needed, and produce a migration plan for the template.

## Why this is worth investigating now, not before

The template's line 17 says the PAT design exists "until Anthropic supports GitHub integration for web-only users." Per web research done just before this handoff (August 2026), that support now exists:

- claude.ai Pro/Max (not just Team/Enterprise) can attach custom remote MCP connectors via Settings → Connectors. Attaches at account level; activates per-conversation via the `+` menu.
- GitHub publishes an official remote MCP server at `https://api.githubcopilot.com/mcp/` — publicly hosted, OAuth-based, no self-hosting needed.

If that first-party GitHub MCP server covers the workflow's needs, the ideal outcome is: **delete the credentials block entirely; replace with a one-line "activate the GitHub connector" instruction.** No custom server, no rotation, no paste. Verify this path first before designing anything custom.

## Unknowns to resolve before you commit to a design

The Claude Code session that gathered the research above is not on claude.ai web and could not test any of this. You should verify, ideally by trying it against a throwaway Project:

1. **Copilot subscription?** The URL `api.githubcopilot.com` lives on GitHub's Copilot infra. Check GitHub's docs for whether using this MCP server requires a paid Copilot license, or whether it's free-tier accessible.
2. **Tool surface.** List the tools the GitHub MCP server exposes. Does it cover what `template/RESEARCHER.md` needs a session to do — clone the user's project repo, read/write files, commit, push? Or is it more issues/PRs/code-search-oriented (which would leave the core research-repo workflow uncovered)?
3. **Scope narrowness.** The current PAT is scoped to two specific repos. OAuth scopes on GitHub apps are typically per-installation. Verify whether the connector's OAuth can install against just the two target repos rather than the user's whole account. If not, this is a blast-radius regression vs. today — flag it, don't silently accept it.
4. **Project-vs-account attachment.** Research says connectors attach account-wide and activate per-conversation. Verify that a Project can be configured to auto-enable the GitHub connector for every conversation inside it (so the user doesn't have to remember to toggle it each time).

## Design branches, depending on what you find

- **A. GitHub's official server covers everything.** Rewrite `_PROJECT_INSTRUCTIONS.md.template` to replace the credentials block with connector-activation instructions. Update `RESEARCHER.md` to expect MCP-tool-shaped access rather than shell git commands. Ship.
- **B. It covers most but not all.** Hybrid: official server for what it covers, PAT stays for the gap (or a custom MCP server wraps just the gap). Document the split clearly.
- **C. Tool surface too narrow / auth too coarse.** Custom MCP server that exposes exactly the ops `RESEARCHER.md` needs, backed by a server-side PAT (so the rotation lives on Dan's server, not in Project Instructions). This is more infra but preserves current scoping.

Rank in that order — A is the cleanest outcome by a wide margin.

## Files to read in the claude_researcher repo

- `template/_PROJECT_INSTRUCTIONS.md.template` — current PAT-carrying design; the file you'll ultimately rewrite
- `template/RESEARCHER.md` — canonical runtime spec; tells you what git operations a session actually does, which determines what the MCP tool surface must cover
- `template/BOOTSTRAP.md` — the entry point that gets fetched first; may or may not reference credentials
- `README.md` and `STATUS.md` — for context on the workflow's shape and recent history

## Sources (verify these — don't just cite them)

- Custom connectors intro: https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp
- GitHub MCP server repo: https://github.com/github/github-mcp-server
- Claude plan/connector matrix: https://claude.com/pricing
- Compliance API (read-only, confirms no first-party write path to Project Instructions exists): https://platform.claude.com/docs/en/manage-claude/compliance-api-access

## Related artifact on disk (not committed)

The Claude Code session started building a paste-helper as a fallback before pivoting to this MCP handoff: `tools/fill_project_instructions.py` in the local checkout. It's untracked. If your investigation lands on design A (clean MCP win), delete it. If it lands on B or C with a scenario where paste is still needed, keep it. Dan hasn't decided.

## Recommended output from you

1. A short verification report answering the four unknowns above.
2. A design doc — which branch (A/B/C), rationale, and the concrete change set for the template repo.
3. Only then, if custom pieces are needed, code.

Don't skip step 1. The whole point of this handoff is that a bad design commitment here means Dan does another round of the migration in six months.
