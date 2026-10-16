# MCP path for Project Instructions — pain complaint to Fable handoff

**Date:** 2026-08-31
**Branch:** github-mcp-migration
**Machine:** Dans-MacBook-Pro

## Summary

Dan opened with a UX-and-security complaint: rotating the fine-grained GitHub PAT embedded in the `claude_researcher` Project Instructions requires copy-pasting a token through the claude.ai web UI every time, and "bad UX leads to bad security." He asked whether there was any way to update Project Instructions programmatically. Two research passes followed — first for a programmatic write path, then for MCP-on-web as a structural alternative — and the session ended with a cold handoff briefing written for a Fable session to design and build the migration.

The first research pass (Claude Code + `claude-code-guide` subagent, web search) confirmed no supported public API exists for programmatic writes to Project Instructions on claude.ai. The only documented Projects surface is the Compliance API, which is read-only. Community reverse-engineered clients exist but require a session cookie, violate ToS, and break whenever Anthropic changes the backend — not appropriate for a security-flavored workflow. The honest answer to Dan's original question was "no."

The second research pass (same subagent, different scope) surfaced that the whole PAT-in-instructions design premise may no longer hold. Anthropic now supports custom remote MCP connectors on claude.ai Pro/Max (not just Team/Enterprise), attached at account level and activated per-conversation. GitHub publishes an official remote MCP server at `https://api.githubcopilot.com/mcp/`, publicly hosted, OAuth-based, no self-hosting required. If that server's tool surface covers what `RESEARCHER.md` sessions actually do (clone, read/write files, commit, push) and the OAuth scoping can be made as narrow as the current fine-grained PAT, the credentials block in `_PROJECT_INSTRUCTIONS.md.template` can be deleted entirely and replaced with a one-line "activate the GitHub connector" note. Dan opted to have a Fable session verify these unknowns and design the migration, rather than doing it in this Claude Code session.

## Topics Explored

- Whether Anthropic exposes any documented API for managing claude.ai Projects (create, read, update Project Instructions)
- Community/unofficial reverse-engineered clients for claude.ai (auth model, brittleness, ToS status)
- Whether MCP connectors are attachable to claude.ai web on Pro/Max, or gated to Team/Enterprise
- Whether GitHub ships a first-party remote MCP server, and if so, its auth model and hosting
- Attachment granularity (account vs. Project vs. conversation)
- The paste-helper fallback: script that fills the template with USERNAME/REPO/PAT and pipes to clipboard, so even without the MCP path the copy-paste friction drops

## Provisional Findings

- **Compliance API is read-only** — list projects, list attachments/collaborators, delete; no create/update. Source: platform.claude.com/docs/en/manage-claude/compliance-api-access.
- **Managed Agents have full CRUD via API** — but they are a separate product (Anthropic-hosted agents), not claude.ai Projects.
- **Custom MCP connectors are available across all claude.ai plans** — Free (limited to one custom connector), Pro/Max/Team/Enterprise. Attach at account level via Settings → Connectors, activate per-conversation via the `+` menu. For Team/Enterprise, org owners can configure at org level.
- **GitHub's remote MCP server exists at `https://api.githubcopilot.com/mcp/`** — OAuth (browser flow) is the recommended auth for claude.ai; PAT-via-env is for self-hosted. Publicly hosted; no localhost variant possible for claude.ai web.
- **Unofficial reverse-engineered clients (e.g., `claude-ai-re-client`)** require a session cookie, break on Anthropic backend changes, and violate ToS. Ruled out for Dan's use case.

Findings above are what the subagent's web research surfaced; none has been verified by a claude.ai web session yet. The four highest-leverage unknowns (called out in the briefing) are: (1) whether the GitHub MCP server requires a paid Copilot subscription — the URL lives on `githubcopilot.com` infra — (2) whether its tool surface covers RESEARCHER.md's actual git ops, (3) whether OAuth scoping can be as narrow as the current two-repo fine-grained PAT, and (4) whether a Project can auto-enable the connector for every conversation inside it.

## Decisions Made

- **Do not pursue programmatic writes to Project Instructions.** No supported path exists; the unofficial path is not appropriate here.
- **Do not build the paste-helper further in this session.** Dan pivoted from "automate the paste" to "have Fable design an MCP-based replacement so this is the last rotation ever." Paste-helper is kept on this branch as a fallback pending Fable's design outcome.
- **Hand off to Fable via a cold briefing doc rather than driving the design from a Claude Code session.** Rationale: Claude Code can't test claude.ai web behavior; Fable can. Verification-before-design is the whole point.
- **Rank three design branches for Fable, in preference order:** A (official GitHub MCP server covers everything — delete credentials block), B (hybrid: official for most, custom or PAT for gaps), C (custom MCP server wrapping just the ops RESEARCHER.md needs, backed by server-side PAT so rotation lives on Dan's infra).
- **New branch `github-mcp-migration` opened on `main` to hold the briefing + paste-helper.** Fable will branch/worktree/PR from here as needed.

## Results

- **Briefing doc for Fable:** [`docs/mcp_migration_briefing.md`](../mcp_migration_briefing.md) — cold handoff, self-contained, names the four unknowns and the three design branches.
- **Paste-helper (fallback):** [`tools/fill_project_instructions.py`](../../tools/fill_project_instructions.py) — stdlib-only Python; auto-detects username via `gh api user` / `git config github.user` and repo via `git rev-parse --show-toplevel`; prompts for PAT with `getpass` (hidden input); substitutes and pipes to clipboard (pbcopy / xclip / wl-copy); the PAT never touches disk. Substitution policy: `<USERNAME>` and `<REPO>` global, `<TOKEN>` only in the `TOKEN="<TOKEN>"` line (keeps description prose readable, avoids doubling the secret surface). Delete if Fable's design lands on A; keep for B/C.

## Open Questions

- **Copilot subscription requirement for `api.githubcopilot.com/mcp/`?** URL is on GitHub Copilot infra — flagged for Fable to verify against GitHub's docs directly.
- **Does the GitHub MCP tool surface cover clone + read + write + commit + push?** Fable to list tools against a throwaway Project and compare with what `RESEARCHER.md` currently expects sessions to do.
- **Can OAuth scope be as narrow as the current PAT (two specific repos)?** Fine-grained PATs scope to individual repos; GitHub App OAuth typically scopes per-installation but repo-level is possible on some flows. Fable to verify — this determines whether design A is a blast-radius regression vs. today.
- **Can a claude.ai Project auto-enable a connector for every conversation inside it?** Research says connectors attach account-wide and activate per-conversation. If Project-level auto-enable exists, the UX is silent; if not, the user has to remember to toggle on entry.
- **Fate of `tools/fill_project_instructions.py`?** Depends on Fable's design outcome — deferred until then.

## Handoff line

> Read `docs/mcp_migration_briefing.md` on the `github-mcp-migration` branch; verify the four unknowns before committing to a design; A/B/C ranked in the briefing.
