# Plan 14 implementation (proxy-only)

**Date:** 2026-10-10 to 2026-10-12
**Branch:** proxy-only
**Surface:** Claude Code
**Machine:** pro (exporter run on the Air)
**Session:** Dan (pro, claude_researcher, 20261010T1803, opus-5.5) · /Users/dan/.claude/projects/-Users-dan-code-dotfiles/dd25383b-cd41-4aa4-8098-a6317d95e5fc.jsonl

## Summary

Implemented [plan 14](../plans/14_proxy_only.md): the web template no longer supports a pasted token. Only claude.ai's GitHub proxy is supported, with repos attached per session. Phases 1–4 (RESEARCHER.md, Project Instructions and lite, BOOTSTRAP and README, web-only skills) landed on the branch. Phase 5 was split: a web agent fixed the dotfiles-sourced `finishing-a-research-branch` and the maintenance notes (dotfiles `cba4208`, `87ebe95`); the exporter ran on the Air (`024d02f` on main, merged into the branch). PR #75.

Phase 6 ran seven web sessions plus two probes; the run-by-run record is [20261011_plan14_web_runs.md](20261011_plan14_web_runs.md). The auto-mode permission check refused startup steps in four of the seven, under shifting labels. The template was revised after each batch:

- **Profile essentials in Project Instructions.** Display name, commit email, git fluency and home repo are copied into the Project Instructions, so a refused profile read no longer blocks a session. The read is optional; the profile wins where they differ.
- **Shallow clone,** as the add-repository reply asks (a full clone was refused once). Fetch before pushing a new branch (413 otherwise).
- **One named go-ahead.** A bare "go ahead" cleared nothing; a go-ahead naming the action and repo cleared attaches and pushes. The agent suggests one pasteable line covering every refused step plus the coming push, retries once, and never retries in another form.
- **Tools by full name.** `register_repo_root` and `list_repos` are deferred and a keyword search misses them; load with `select:`. `register_repo_root` is present in some sessions only; the fallback is reading the repo's `CLAUDE.md`.
- **Codename and version (#78, folded in).** The first reply states the session codename; Project Instructions carry `PI_VERSION=2`, and an older or missing version gets a one-time notice.
- **Stop hook.** The sandbox's stop hook suggests changing the author to `Claude <noreply@anthropic.com>` for a Verified badge; the template says to decline. Dan's rule: the author name doesn't matter as long as every commit and every chat carries the codename.

## Open after this branch

- Project-repo attach is refused in about 3 of 7 sessions, while the config-repo attach in the same turn never was. No fix in Projects: a probe found no "Repository Scope" list in Project chats, so every repo is attached during the session. The named go-ahead clears it.
- Profile file rename to `researcher_config.md` with a fallback: #79 (3/3 allowed vs 1/4 for `personal_info.md`; small sample, confounded).
- Pinning and other PAT/web_fetch-era cruft: #77.
- Claude Code on the web as the target surface: #80, #81 (see below).
- Run D (lite) and run E (BOOTSTRAP read-through) deferred to after merge.

## Close-out and merge prep (2026-10-11)

Repository Scope probe in a Project chat found no such section (lead closed). Rename ticketed as #79; Dan's rule on authorship recorded on #77 (any author name, as long as every commit and chat carries the codename). Grep gate clean apart from history, 14 tests passing, `tools/repin.py` run (BOOTSTRAP → `a315b0b`, README → `3b7d518`), #72's checklist updated, PR #75 description rewritten and marked ready. Not merged.

## Claude Code on the web (2026-10-11/12)

Dan asked what the workflow should target now that claude.ai/code exists, rather than defaulting to Project chats. Three probes in `danparshall/proxy-scratch` (seeded with a `CLAUDE.md` marker and a repo skill `probe-hello`):

- **A first session, from Dan, on `claude_researcher`.** Its notes are on branch `claude/claude-researcher-github-workflow-4zbkxm` (`docs/convos/20261011_ccw_surface_probe.md`, `20261011_pr75_two_surfaces.md`, not merged here). Findings:
  - The repo is pre-attached and cloned at `/home/user/<repo>`; the system prompt has the Repository Scope list.
  - A random `claude/…` branch is assigned.
  - Non-GitHub hosts are blocked under the Default environment.
  - The GraphQL refusal advertises "CCR" REST routes for review threads, auto-merge and draft toggles.
- **Probe 1** (`claude/pensive-mayer-3uh6j7`):
  - The repo `CLAUDE.md` and the repo skill load.
  - Pushing to an existing non-assigned branch works with the user's permission.
  - PR tools exist; there is a deep-research skill; WebSearch works.
  - Paper hosts get 403 and the PDF upload never arrived.
- **Network fix.** Dan created a `Research` environment with Network access = Full. The chat setting "Capabilities → Domain allowlist" doesn't apply to claude.ai/code.
- **Probe 2** (`claude/affectionate-cerf-nfc7l9`): "grab arXiv 1706.03762 and add it" worked first try by `curl`.
- **Probe 3** (`claude/jolly-brown-vxl40v`): `add-paper`, uploaded as a claude.ai account skill, appeared as `anthropic-skills:add-paper` and was chosen unprompted. Its companion skills were missing, the paper-naming preference didn't reach it, and the sandbox stop hook overrode the skill's "leave committing to the user".

Dan's objections, both accepted:
- Account skills need a manual re-upload per change, so they can't be how updates ship. The candidate is the environment's Setup script cloning the template into `~/.claude/skills/`; untested.
- Random assigned branch names conflict with RESEARCHER.md §3 Branch resolution.

Ticketed for later: #80 (move to claude.ai/code? findings) and #81 (skill updates via setup script; §3 branch model).

## Process notes

- The exporter has no `__main__` and runs only on the Air (flag file); plan 14's note was corrected.
- The D runs all wrote the same file at once, so D2's push was rejected non-fast-forward: a test-design flaw, not a template one. D2 stopped correctly.
