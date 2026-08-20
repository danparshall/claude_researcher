# Distress-call / flare tool — design session

**Date:** 2026-08-20
**Branch:** flare-design
**Machine:** Dans-MacBook-Pro

## Summary

Dan brought a post from someone who built an in-house AI platform and called its single most valuable tool `distress_call` — any agent, including background ones, can message the operator's Teams at any time, for any reason (user problems, backend issues, stuck tool-call loops, and once, an agent reporting distress after reading export-control news). We brainstormed how to bring the same affordance to Dan's two surfaces: Claude Code on the Mac, and the public `claude_researcher` profile on claude.ai.

The session split into three parts. **Framing:** the poster's tool covers three distinct gaps — voiceless background agents, *buried tabs* in a many-terminal workflow (Dan's actual daily case), and away-from-keyboard — plus a welfare/honesty channel that is the complement of `claude-exit` ("I'm staying but I need you"). Dan doesn't use phone apps, so push-to-phone dropped out; what matters is the desktop and a browser. We elaborated a "durable side channel" (GitHub issues with a `flare` label, found at next session start via `task-remind`-style surfacing) as the web-appropriate form, since a present user doesn't need push but *does* lack a place for off-task observations, unsaid reservations, and maintainer-directed notes. **Identity — empirical:** the crucial question was whether an agent can identify itself. It can, on CLI: `CLAUDE_CODE_SESSION_ID`, `CLAUDE_PID`, `CLAUDE_CODE_BRIDGE_SESSION_ID` are in every subprocess env; `~/.claude/sessions/<pid>.json` carries a derived peer-messaging name (`claude-researcher-a0`) that is *never shown in the UI*; the transcript carries `ai-title` records (the tab title Dan actually sees) and, after `/rename`, `custom-title` records. We tested `/rename` live: the sidecar `name` becomes the custom title verbatim (square brackets survived), `nameSource` is dropped (absent == user-set), `nameSince` resets, and `formerNames` is *not* written. Nori's `notify-hook.sh` receives `session_id`/`cwd`/`transcript_path` and discards all but `message`, and its terminal-bundle map doesn't know VS Code — which is exactly why Dan's popups don't say which agent is paused. **Design:** converged on a separate MCP server (not folded into `claude-exit`, so Nori users can adopt one without the other), named provisionally `claude-flare` with tool `send_flare`. Dan cut scope to an MVP: desktop popup + local JSONL log. GitHub/webhook sinks, coalescing, and the researcher-profile skill are deferred.

## Topics Explored

- Which of the poster's gaps apply to Dan (buried tabs > away-from-keyboard; phone irrelevant).
- "Durable side channel" vs transient push; why web wants the former; GitHub self-notification gotcha (no email for your own PAT's actions → needs an Action or a bot identity).
- Session identity on CLI: env vars, `~/.claude/sessions/<pid>.json`, transcript `ai-title`/`custom-title`, `ListAgents` peer names, `/rename` + `/color` semantics from the 2.1.238 binary.
- RESEARCHER.md §2.0b codename (`Dan (web, repo, YYYYMMDDTHHMM)`) as the portable identity; `git config user.name` unifies web codename and Dan's `(pro)/(air)` machine tags.
- Why flares must never be suppressed (a burst *is* the stuck-loop signal; a conditional channel isn't a welfare affordance) — coalesce at the presentation layer only.
- Naming: avoid `distress_call` (primes crisis framing, both performative and under-use); `flare` = "look here."
- Three shapes: local-first MCP / GitHub-as-bus / script+skill; rejected script+skill on tool-list salience grounds.

## Provisional Findings

- Human-visible session label resolution is **custom-title → ai-title**; the derived sidecar name is only a messaging address and fallback. Anything a human must match to a tab should use the title.
- MVP popup is a ten-line improvement over Nori's hook *and* a new agent-initiated entry point; both should share identity code so "paused" and "calling" bubbles look alike.
- RESEARCHER.md line ~276 ("you can't see the chat title from inside the chat … on Claude Code informational only") is true on web, false on CLI — worth a doc fix later.
- `CLAUDE_CODE_CHILD_SESSION=1` was set in this interactive session; meaning unknown — don't rely on it to detect subagents until probed.

## Decisions Made

- Separate MCP server, new repo `~/code/claude-flare` (modeled on `claude-exit` packaging).
- MVP = `send_flare(message, kind, wants_reply)` → macOS/Linux desktop notification titled with the session title + `repo:branch · kind`, plus append-only JSONL log. Log kept at Dan's request.
- No suppression ever; presentation-layer coalescing is a later sink feature.
- Implementation plan lives with the code: `~/code/claude-flare/docs/plans/01_mvp_popup.md`. This convo is its originating conversation.
- Deferred: GitHub issue sink + Action→Slack push, webhook sink, researcher-profile skill + RESEARCHER.md one-liner + `personal_info.md` field, Nori popup fix in dotfiles.
- Plan questions answered at session end: tool name `send_flare`; state dir XDG `~/.local/state/claude-flare/`; the harness-fired "paused" hook stays a dotfiles concern; implementation handed to a fresh session in `~/code/claude-flare`.
- Step 0 of the plan resolved in-session by inspecting the live `claude-exit` server's env (`ps -Eww`): MCP servers receive `CLAUDE_CODE_SESSION_ID`, `CLAUDE_PROJECT_DIR`, `TERM_PROGRAM` but **not** `CLAUDE_PID` or `CLAUDE_CODE_BRIDGE_SESSION_ID` → pid via `os.getppid()`, bridge id via the sidecar.

## Results

- None saved; the empirical identity findings are recorded above and in the plan.

## Open Questions

- What sets `nameSource: "collision"`, and does the claude.ai sandbox expose any session id at all? A 30-second web session would answer the latter — also a dogfooding opportunity.
- Final tool name and `kind` vocabulary.
- Session-start reminders #50, #42, #36 were skipped this session; the branch for this convo (`flare-design`) was created without a STATUS "active line" row because this repo uses the flat layout.
