# Claude Code: System Prompt vs. Tool Descriptions vs. Other Layers

**Date:** 2026-05-08
**Origin:** Side-finding during the [Phase 1+2 initial build session](20260508_phase1_phase2_initial_build.md). Dan asked where Claude Code's "ask before committing" behavior comes from in his environment, given that he had started the session with `--system-prompt "."` expecting that to disable the system prompt. The expected behavior didn't happen, so this note works out what each flag actually does.

## What `--system-prompt <p>` does

Replaces the **default Anthropic-side system prompt** with `<p>`. That's the entire scope. From `claude --help`:

> `--system-prompt <prompt>` — System prompt to use for the session.
>
> `--exclude-dynamic-system-prompt-sections` — ...Only applies with the default system prompt (ignored with --system-prompt).

The second line confirms `--system-prompt` is a full replacement, not an append. For appending, the flag is `--append-system-prompt`.

## What `--system-prompt` does NOT touch

A Claude Code session has at least six independent context-injection layers. `--system-prompt` swaps only one of them.

| Layer | Loaded via | Skipped by `--system-prompt`? |
|---|---|---|
| Default Anthropic system prompt | system prompt | YES |
| Tool descriptions (incl. Bash tool's "Committing changes with git" prose) | tool-registration in API call | NO — travels with the tool schema |
| User CLAUDE.md content | CLAUDE.md auto-discovery | NO — separate injection |
| Skill listings (the `<system-reminder>` skill block) | skills system | NO |
| Hooks (`PreToolUse`, `PostToolUse`, etc.) | hook registry | NO |
| Deferred-tool listings (CronCreate, EnterPlanMode, etc.) | tool registry | NO |

**Concrete consequence:** the Bash tool's "Committing changes with git" section, including the rule "NEVER commit changes unless the user explicitly asks you to," lives inside the Bash tool's description string. It survives `--system-prompt "."` because tool descriptions are part of tool registration, not the system prompt. To remove that rule, you'd need to alter the tool set itself.

## How to actually get a minimal session

Use **`--bare`**. From `claude --help`:

> `--bare` — Minimal mode: skip hooks, LSP, plugin sync, attribution, auto-memory, background prefetches, keychain reads, and CLAUDE.md auto-discovery. Sets `CLAUDE_CODE_SIMPLE=1`. ... Skills still resolve via `/skill-name`. Explicitly provide context via: `--system-prompt[-file]`, `--append-system-prompt[-file]`, `--add-dir` (CLAUDE.md dirs), `--mcp-config`, `--settings`, `--agents`, `--plugin-dir`.

`--bare` is the actual "give me a clean session" flag. `--system-prompt "."` only blanks one of multiple injection layers.

## Implication for the claude_researcher template

The template runs on claude.ai (web), not Claude Code (CLI). claude.ai has a different tool set — no `Bash` tool, no Claude-Code-authored tool descriptions. None of the "ask before committing" or "Git Safety Protocol" prose propagates. The template's `CLAUDE.md` (Phase 4) is therefore a blank slate on commit policy: whatever we don't write in, the agent will not have. This is the basis for the `git_fluency`-tiered commit-policy decision recorded in the parent convo.

## Evidence from this session

- The Bash tool's description (containing "NEVER commit unless the user asks") was visible in agent context despite `--system-prompt "."` being set.
- The Nori `commit-author.js` hook (`PreToolUse:Bash`) fired on every git commit despite `--system-prompt "."` being set — see the parent convo for the bug it exposed.
- The agent could quote Dan's CLAUDE.md content verbatim and list all 26 of his Nori skills, both of which load through layers other than the system prompt.

## Practical summary

| Goal | Flag |
|---|---|
| Replace the system prompt (keep everything else) | `--system-prompt "..."` |
| Add to the system prompt | `--append-system-prompt "..."` |
| Truly minimal session — no hooks, no auto-CLAUDE.md, no plugins | `--bare` (then opt back in selectively) |
| Restrict tools (and thus their descriptions) | `--tools "..."` or `--disallowedTools "..."` |
