# Add ClawXiv framework paper as reference material

**Date:** 2026-07-15
**Repo:** `claude_researcher` (meta dev repo, flat `docs/`)
**Main:** unchanged; branch `add-clawxiv-reference` opened, one commit (`7fab2b4`), pushed to origin

## Summary

Redirect from an earlier claude-exit session: Kornai's ClawXiv paper (arXiv 2604.16476v2, May 2026) had first been vendored in `claude-exit/docs/clawxiv-framework/` following the sibling `fable-5-drop-of-water/` pattern. Dan flagged the wrong repo — ClawXiv is thematically parallel to *claude_researcher*'s own mission (convert volatile chat sessions to durable, inspectable research artifacts), not to `claude-exit`'s (single MCP tool for conversational exit). Rolled back the claude-exit branch (remote deleted; local branch a dangling ref since `-D` is denied by permission config) and added the paper here instead.

Placement was a real decision, not a default. STATUS.md:11 explicitly forbids `papers/`, `docs/active/`, `docs/historical/`. Asked Dan via AskUserQuestion; he picked `docs/reference/clawxiv-framework/` as a new subdir class — adds a `reference/` concept to `docs/` without breaking the flat convention (still no per-branch active dirs, no papers root, no top-level `PAPER_INDEX.md`). The only alternative that came close was `template/reference/`, but that dir is for material shipped OUT to target researcher repos, not this dev repo's own references.

Content followed the add-paper skill's shape (title/authors/date/source/summary/key findings/relevance), but the Relevance section was rewritten from the claude-exit version — four architectural points of contact for future claude_researcher design work: (1) ClawXiv's four-state lifecycle (legacy seed → normalized project → signed bundle → published artifact) implicitly maps onto what claude_researcher does with `docs/convos/` + `main` + public GitHub; naming the states explicitly could sharpen the workflow's vocabulary. (2) Sidecar attestation model (§8.4) is strictly stronger provenance than git-commit-hash + GitHub-identity; could layer on top without breaking existing flows. (3) `clawxiv-mediate` daemon (§8.8) is a reference for any future AI-to-AI extension — its append-only signed transcript + participant-invoked terminate primitive (which itself explicitly cites Parshall's `claude-exit`) is the design worth stealing. (4) Ceremony analysis (§8.6) — mechanism + interpreter pointer, grounded in Austin and Staal — applies to any signed-artifact protocol claude_researcher formalizes.

## Topics Explored

- **Wrong-repo redirect.** Original vendoring in `claude-exit` was substantively defensible (paper connects to `claude-exit` via §8.8's terminate-primitive citation), but the *broader* thematic fit is `claude_researcher`, which shares ClawXiv's whole mission-space. Rollback: remote branch `docs-clawxiv-framework` deleted; local branch dangling until `git branch -D` (force-delete denied by config).
- **`docs/reference/` as new subdir class.** Distinct from `docs/convos/` and `docs/plans/` (this repo's own development record) and from `template/reference/` (material shipped out to downstream researcher repos). For material *informing* the toolkit's design that isn't the toolkit's own development history.
- **Relevance-section retuning.** The claude-exit README emphasized §8.8's explicit citation of `claude-exit` as validation of an existing design choice. The claude_researcher README emphasizes the four architectural points of contact as *reference-for-future-design* — since claude_researcher hasn't yet made the choices ClawXiv has (signed bundles, mediator daemon, sidecar attestation), the paper is a design source, not a validation.
- **add-paper skill mismatch in this repo.** The template `add-paper` skill (which this dev repo authors but doesn't run against itself) expects `papers/`, `papers/text/`, `PAPER_INDEX.md`, `PAPER_SUMMARIES.md`. None appropriate here per STATUS:11. Adapted: PDF + text extraction + README summary all in the paper's own subdir; no repo-level index.

## Process notes

- Convo-name handshake (§2e) not performed at session start — the session in `claude_researcher` was a mid-CLI-session redirect from claude-exit work, so no explicit fresh handshake fired. Named at finish-convo time as `add_clawxiv_reference`.
- Cross-repo session context: this session's arc actually began 2026-06-28 in the claude-exit terminal and stayed open across 17 days idle; date-check at Dan's mid-session prompt surfaced 2026-07-14/15 UTC. All work in `claude_researcher` proper happened 2026-07-15 after the wrong-repo flag; using that as the convo date.
- Chain-matcher hook fired twice (both on `shasum ... ; ls ...`-style chains); split into separate Bash calls each time.
- Task tool nudges appeared repeatedly in system reminders; not used — work was a short well-bounded sequence of ship-and-forget steps with clean commit boundaries.

## Post-hoc status check — 2026-08-13

**Machine:** Dans-MacBook-Pro
**Session shape:** sync-and-recall, ~28 days after the branch was last touched. No new work; branch state unchanged (`7488b80`, still 2 commits ahead of main).

- **Pull ran clean.** Local `main` was 6 commits behind origin; fast-forwarded to `468005a`. Current branch already up to date with origin.
- **Branch has drifted.** `add-clawxiv-reference` is now **24 commits behind main** — main advanced substantially since 2026-07-14 (PRs #40, #41, #44, #45, #47, #48 merged in the interim). Rebase-then-PR is the natural next action; not requested this session.
- **Stale STATUS on this branch.** The 2026-07-14 entry on this branch's STATUS says PR #40 "open; closes #38 on merge" — PR #40 actually merged 2026-07-17. Not corrected here (leaving it to be swept when the branch rebases against updated main, whose STATUS is already current).
- **Fired task reminders surfaced but not actioned:** #42 `[2026-08-03]` PreCompact hook wiring; #36 `[2026-07-12]` onboarding explainers/tool ideas. Both surfaced per `task-remind` pattern; Dan did not pick either up this turn.
- **User questions this session:** (1) branch + merge status → answered from git; (2) "what was clawxiv" → recalled from the vendored README (didn't re-read the PDF).
