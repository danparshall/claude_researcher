# Site as front door, site review, BOOTSTRAP model line + repin

**Date:** 2026-09-21
**Branch:** `main` (main-direct for docs links and README; `bootstrap-model-line` for the BOOTSTRAP edit, merged as PR #63)
**Machine:** Dans-MacBook-Pro
**Model:** Fable 5.1
**Session codename:** `Dan (pro, claude_researcher, 20260921T1536)`
**Transcript:** `/Users/dan/.claude/projects/-Users-dan-code-claude-researcher/69361666-2e84-42c0-8a1d-c86cefc1b017.jsonl`

## Summary

The session opened on ticket #61 (informational CI workflow) and a question about priorities. Ticket #61 turned out not to be buildable as written: one of its two tests, `tests/test_skill_surface_note.py`, lives in dotfiles and has never been in this repo. That is still undecided; no work was done on #61.

Most of the session went to the public website. Ticket #50 named `clauderesearcher.com`; that was a typo for `clauderesearch.ai`, which is Dan's, bound to GitHub Pages on `danparshall/site-claude-researcher` (repo was renamed from `claude-researcher-site`), built, HTTPS enforced. The `.com` belongs to someone else (registered through Cloudflare 2026-01-23, a "Claude for research" guide site). README and HUMANS now link the `.ai` site as the non-developer front door, both repos' homepage fields point at it, and #50 is closed.

Dan then asked for a review of the site. The main finding was that the privacy section overclaimed ("We literally could not read your work if we wanted to") given that every session pulls instructions from a repo Dan controls and acts with the user's token. The section was rewritten and shipped to the site, along with a model-requirement line. The "Opus 4.7 only" wording was corrected everywhere to "Opus 4.7 and Claude 5 models; 4.8 stops" (README, site, BOOTSTRAP). The BOOTSTRAP edit needed a repin, which surfaced that the README's pin had been stale since roughly July.

## Topics Explored

- Ticket #61 feasibility; location of the two tests it names.
- Fired reminders in this repo and dotfiles (not processed one by one; Dan did not pick any up).
- DNS, whois, and Pages binding for both domains; old `github.io/claude-researcher-site/` preview address now returns 404 (repo rename), new one redirects to the `.ai` domain.
- Site review using the reviewing-drafts skill (piece 1,053 words, review 520 / cap 526), plus a link check of both pages.
- What Apache 2.0 requires of forks in the way of credit.
- Why the bootstrap links are pinned to commits, and whether RESEARCHER.md needs the same.

## Provisional Findings

- The token setup in BOOTSTRAP tells users to choose "All repositories" with Administration read and write. The site calls this a "scoped token". Dan's call: keep the site's token description as is.
- Apache 2.0 obliges redistributors to carry the license, keep existing notices, mark changed files, and reproduce a NOTICE file if present. This repo has no NOTICE and the LICENSE copyright line is still the blank placeholder, so a fork can comply without visible credit. Not legal advice.
- The README's BOOTSTRAP pin (`f1cfcad`) predated three commits that changed pinned files (`0cf2375`, `c85d31b`, `184a1da`). New users were getting an old BOOTSTRAP and a `personal_info.md` template without the display-name and commit-email fields the runtime rules expect. A pin trades a bounded automatic delay for an unbounded one that depends on someone remembering to repin.
- Pins are only needed where a web fetch is the only option (before network access is on) and the content changes. That is the README's BOOTSTRAP link. RESEARCHER.md is read from a clone at session start and should stay unpinned; a pin in the Project Instructions would freeze users on their setup-day version.
- The three template links inside BOOTSTRAP are fetched after Step 1 confirms network access, so they could plausibly come from a clone instead. Not verified step by step.

## Decisions Made

- `clauderesearch.ai` is the non-developer front door. README + HUMANS link it (`deea85b`); homepage field set on both repos; #50 closed.
- Model support wording: Opus 4.7 and Claude 5 models; 4.8 stops. README `55c2812`; site `976a30b`; BOOTSTRAP via PR #63 (merge commit `454b788`, commits `3852c4f`, `a0b0972`, `1e23aad`). Pinned commit confirmed reachable from main.
- Site privacy section rewritten ("Where does my data live, and who can see it?"), public-instructions bullet reworded, requirements line added. Shipped in `site-claude-researcher` `976a30b`. Token bullet deliberately unchanged.
- Forks are not supported. Dan's words: anyone who wants to fork and hardcode something different can.
- Ticket #62 filed for better crediting (root NOTICE, copyright line, check Nori's NOTICE).

## Results

None saved as files. The site review was delivered in chat only.

## Open Questions

- Ticket #61: copy the surface-note test here, run only the manifest test here, or put that CI in dotfiles. Agent leaned manifest-only, without having read the surface-note test.
- A test that fails when a pinned file on main differs from its pinned commit would stop the pin drifting silently again. Natural fit for #61's CI. Offered, not ticketed.
- Dropping the three in-BOOTSTRAP pins in favour of a clone after Step 1. Needs a step-by-step check and a fresh setup test.
- The July "review before you run" web fetch of RESEARCHER.md can show a day-old copy while the clone is current. Does the Project Instructions template say the clone is authoritative?
- The merge rolled forward plan 12 and codename changes for new users; none of that has had a fresh setup test.
- Left from the site review: Nori Researcher link on the Resources page is a 404 (use noriskillsets.dev/skillsets/researcher); "about 10 minutes" appears three times with no measurement behind it; em-dashes throughout; no canonical / og:url / og:image tags.
- #11 (public website) still open; closing it is Dan's call on whether the content is finished.
- The lookalike `.com`: use the full `.ai` address in anything sent to funders.
- dotfiles #77 (grant applications, fired 2026-09-01) remains the highest-priority fired item across both lists.
- Worktree `.worktrees/bootstrap-model-line` and its branch remain; removal is Dan's to do.

## Captured Tasks

- [#62: Strengthen attribution: root NOTICE file, fill LICENSE copyright line, check Nori upstream NOTICE](https://github.com/danparshall/claude_researcher/issues/62) — captured 2026-09-21
