# clauderesearcher.com Site Build

**Date:** 2026-08-16 → 2026-08-17 (session spanned midnight UTC)
**Branch:** convo-clauderesearcher-site-build (docs only — site work lives in `danparshall/claude-researcher-site`)
**Machine:** Dans-MacBook-Air
**Surface:** CLI

## Summary

Built and shipped the public website for `claude_researcher` (issue #11) — a super-simple entry point for researchers who aren't yet github-pilled. The site lives in `danparshall/claude-researcher-site` (local clone `~/code/websites/claude-researcher/`), deployed on GitHub Pages at <https://danparshall.github.io/claude-researcher-site/>, awaiting DNS for `clauderesearcher.com`.

Design center per Dan's spec: above the fold, a one-line value prop plus two copy-paste blocks — "have Claude explain it" and "have Claude set it up." Below the fold, full transparency: what it is, a session vignette, how it works (with the two setup screenshots), privacy, who's behind it. Key architectural decision: **the human pastes once; the agent hops.** Both paste blocks are self-contained prompts; the setup block sends the agent to the upstream README on `main` to find and follow the pinned Quick-start prompt. This keeps the site drift-free — `tools/repin.py` never needs to know the site exists.

Mid-session surprise: the site repo's remote `main` already held a forgotten v0 — seven commits from 2026-06-08, 10:41 (web-UI/noreply signature), nine minutes after the placeholder commit. The local clone had never pulled it. v0's index duplicated the bootstrap prompt verbatim and had already rotted twice (unpinned BOOTSTRAP fetch predating the SHA-pin decision; stale PAT permission list missing Issues + Pull requests) — a live specimen of the drift failure mode today's indirection design avoids. Reconciled by merging today's overhaul over v0 (today's files won all conflicts; nothing force-pushed), salvaging v0's `resources.html` restyled into the new design; `background.html` (a HUMANS.md mirror, drift-prone) and `fast.css` rest in history.

## Topics Explored

- Fold structure and copy for a non-developer academic audience
- Bootstrap-prompt drift: how a static site stays in sync with the pinned-SHA Quick-start prompt
- raw.githubusercontent.com vs github.com in agent-facing prompts (raw = clean file for fetch; github.com kept for all human-facing links)
- Reconciling two independently-built site versions (June 8 web v0 vs today's overhaul)

## Provisional Findings

- The June-8 v0's rotted verbatim prompt copy is empirical support for the indirection design: any duplicated prompt surface outside `repin.py`'s reach goes stale silently.
- Commits with the `danparshall@users.noreply.github.com` author + rapid-fire timestamps indicate web-UI/Contents-API provenance — useful signature for identifying forgotten web-session work.

## Decisions Made

- Site = single page + `resources.html`; modernized-simple style (`style.css`, Charter/Georgia; replaced template's `fast.css`); only JS is copy-to-clipboard.
- Paste blocks self-contained; setup block routes agent → README@main → pinned Quick-start prompt (Dan: agent may hop, human must not).
- Privacy flip-side reworded per Dan: "all of the guidelines about how this framework functions are open-source, so you can tell exactly what instructions Claude is getting."
- Added cross-linked-record paragraph (STATUS.md → RESEARCH_LOG.md → convo summaries: easy to reconstruct *why*, easy to find original conversations).
- Footer describes HUMANS.md as "User guide & tips" (was "The longer story").
- Screenshot captions kept permission-list-free so they don't rot; screenshots copied from `template/reference/screenshots/` (see its CAPTURED.md).
- No "Opus 4.7 only" note on the page (lives in README the agent reads; rots on a static page).
- Anthropic non-affiliation disclaimer in footer ("Claude" appears in the domain).
- CNAME **deliberately deferred**: with the CNAME file present, the first Pages build would bind `clauderesearcher.com` and redirect the github.io preview to a then-dead domain. Re-add at DNS time.
- Pages enabled via API, now serving from the site repo's `main` (initially from `overhaul` for pre-merge preview).
- v0 reconciliation: merge (not force-push); today's design wins; keep+restyle `resources.html`; drop `background.html` + `fast.css`.
- Reminders #42 and #36 skipped this session (fire again next session).

## Results

- Live site: <https://danparshall.github.io/claude-researcher-site/> (all site artifacts committed in `danparshall/claude-researcher-site@main`)

## Open Questions

- Whether the Agentics-blog and claude-exit entries on `resources.html` fit the non-github-pilled audience — Dan to skim the live page.
- Whether the site should eventually get an OG preview image for link-sharing.

## Captured Tasks

- [#50: [2026-08-18] Set clauderesearcher.com DNS at Namecheap + re-add site CNAME](https://github.com/danparshall/claude_researcher/issues/50) — captured 2026-08-17. Contains the full DNS checklist (A records, www CNAME, CNAME file restore, Pages domain bind, close #11).
