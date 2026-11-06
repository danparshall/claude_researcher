# 20261106_plan18_session_start_refusals

**Date:** 2026-11-06
**Branch:** session-start-refusals, pi-v2.2 (both merged to main); record on convo-20261106-plan18
**Surface:** claude-code
**Machine:** air
**Session:** Dan (air, dotfiles, 20261106T1002, opus-5.5) · /Users/dan/.claude/projects/-Users-dan-code-dotfiles/f33e0843-ccd4-44d1-9f21-0142870bf1c6.jsonl · —

## Summary

Dan came in frustrated that claude.ai web sessions no longer start cleanly. The auto-mode permission check blocks repo attaches at startup, and agents mention the refusal in passing inside a long first reply, so it's easy to miss. He asked for a stop-and-print rule, with a paste-able override, in all his Project Instructions.

The session found that Plan 18 (#107, written 2026-11-03) already specified most of this but had never been built: only the plan doc was on main. The older, softer rule from `61cb62d` ("suggest a go-ahead") was live, plus a line telling agents not to ask for the config read at all. Plan 18 was built on `session-start-refusals`, then amended twice at Dan's request. First, a session-start refusal now **stops** the first reply with a capitalized "⚠️ SESSION START BLOCKED" heading, instead of being answered alongside it. Second, the go-ahead sentence sits alone in its own fenced code block so claude.ai shows a copy button. Merged as `9dab76a`.

Because RESEARCHER.md can't help when the template clone itself is blocked, the rule was also put into the Project Instructions text: v2.2 (full and LITE templates) has an "If anything is blocked at startup" section. A third version number now marks a user's own variant (`2.2.1` = 2.2 plus their edits; compare the first two numbers; the user's added text wins where it differs). Merged as `6d11b48`. Dan's personal Verification copy is v2.2.1, with his own heading and override wording (profanity kept out of the public repo), and was handed over for manual pasting.

## Topics Explored

- Where Project Instructions live: only the public template is in files; each Project's text sits in the claude.ai UI, so Dan pastes it himself.
- Whether "ALLOW THE REPO CONNECTIONS" would work: evidence says a go-ahead that names the action and repo clears refused attaches, while a bare "go ahead" doesn't, so the override now names every blocked repo.
- Plan 18's real state: plan doc only (`c494fa8`), issue #107 open, no branch.
- Stop vs. answer-alongside: the plan said don't block; Dan overrode it, since a refusal buried in a wall of text gets missed.
- The PI version format is `N.M` only (`tools/test_pi_version.py`); a three-part `2.2.1` needed a rule.

## Provisional Findings

- The LITE PI template still said "don't retry" for the config read and attached repos in parallel. Both were fixed in v2.2.
- `resolve-runtime-issue` also carried the old "don't ask" wording and was updated (it isn't exported from dotfiles, so editing it in place is safe).
- None of this is web-tested yet. The attach-order change (config repo first, on its own) is an experiment with one data point behind it.

## Decisions Made

- Plan 18 built and amended (stop + capitals + copy box): `92debfb`, `111b546`, `3ccd3af`; merged `9dab76a`.
- PI v2.2 with the blocked-at-startup section; third version number marks a user variant: `1d8483a`; merged `6d11b48`.
- The public text uses a clean heading; Dan's profane wording lives only in his own Project copies.
- The Plan 18 evidence table and the 5-session watch log stay in `docs/plans/18_session_start_refusals.md`, not RESEARCH_LOG.md (which is one-line entries).
- #107 stays open until the 5-session acceptance run.

## Results

- `docs/plans/18_session_start_refusals.md`: Implementation status, the amendment, and the watch-log table.

## Open Questions

- Does the copy-box format actually render a copy button in every claude.ai surface Dan uses?
- Does attaching the config repo first, on its own, reduce refusals? Revisit after 5 sessions.
- Plan 18 change 5: is there a claude.ai permission setting other than auto? Not checked.
- The "user's variant wins where it differs" rule is broader than the blocked-at-startup case; narrow it if it causes trouble.
- Dan's other Projects are still on 2.1; each needs a rendered 2.2.1 copy with its own `REPO`.
- The remote branches `session-start-refusals` and `pi-v2.2` were not deleted (no answer yet).
