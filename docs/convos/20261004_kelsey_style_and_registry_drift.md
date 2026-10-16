# 20261004_kelsey_style_and_registry_drift

**Date:** 2026-10-04
**Branch:** main (flat-docs repo; most of the work landed in dotfiles)
**Machine:** Dans-MacBook-Air
**Agent:** Dan (air, claude_researcher, 20261004T1655, opus-5.5)
**Transcript:** `~/.claude/projects/-Users-dan-code-claude-researcher/0334d89f-d464-45db-bf7e-8db8c753efb2.jsonl`

## Summary

Dan dropped two untracked files into this repo: a PNG of Kelsey Piper's chat advice, and a PDF of the `researcher` skillset's public registry page. He asked whether the Kelsey text was already available as a communication style, and what he needed to know about the published skillset.

The Kelsey text was already in dotfiles as `nori-researcher/communication-styles/kelsey.md`. It is not switched on (`.active` = `default`), and its last line is Dan's deliberate reframe of the PNG's. The registry PDF was byte-identical to `dotfiles/nori-researcher/registry_page_20260904.pdf`, so the copy here was deleted.

The live registry still serves 1.0.27, uploaded Sep 3 from the Pro (84 downloads, `org_reviewed`). It lists 7 of Dan's skills as separate packages to fetch, and those 404 (`/api/skills/finish-convo` → 404; amol's `brainstorming` → 200 as a control). So a fresh install most likely gets no finish-convo, finishing-a-research-branch, task-create/remind/triage, or add-/review-reading-list. The Sep 4 fix (bundle all of Dan's skills inside the skillset) is already on dotfiles `main`: all 19 custom skills are marked `inlined-skill`, and the separate-fetch list names only amol's 17. What's missing is the upload itself. The local registry README had already fixed most of the live page's stale text. The one remaining gap was the four newer skills (condense-summary, paper-index, identify-chinese-person, reviewing-drafts), now added via dotfiles PR #110 (merge `306aff3`).

## Decisions Made

- Deleted the duplicate registry PDF from this repo.
- identify-chinese-person ships as-is. Its real-name collision examples (翁健, 李一鸣, 姚苏) are fine to publish (Dan: nothing sensitive).
- Upload deferred to a fresh session, run by Dan.
- Dan removed the merged `persona-drift-stopgap` and `persona-block-markers` worktrees and branches here, and the dotfiles `researcher-readme-refresh` worktree and branches. Before that, both claude_researcher branches were checked as fully merged and clean, with no open processes.

## Open Questions

- Whether to switch on the `kelsey` style. If Dan switches it on, he must switch back to `default` before any upload, because the style section is in the published `AGENTS.md`.
- Whether the orphaned standalone packages (finish-convo@1.0.0 etc.) need cleanup on the registry. This is still waiting on amol (see `dotfiles/nori-researcher/PUBLISHING.md` §5).
- `Kelseys__chat__advice.png` is still untracked at this repo's root. Dan hasn't said whether to keep it.
