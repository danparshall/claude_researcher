# 20261004_registry_upload_1.0.28

**Date:** 2026-10-04
**Branch:** main (flat-docs repo; all changes landed in dotfiles)
**Surface:** claude-code
**Machine:** Dans-MacBook-Air
**Session:** Dan (air, claude_researcher, 20261004T1750, opus-5.5) · `~/.claude/projects/-Users-dan-code-claude-researcher/32294787-0d14-4a4f-a1a6-7bfdb917865d.jsonl` · —

## Summary

This session picked up the handoff from `20261004_kelsey_style_and_registry_drift`: upload the `researcher` skillset so fresh installs stop missing the 7 custom skills that 1.0.27 fetched as separate packages (those packages 404). The agent ran `dotfiles/nori-researcher/PUBLISHING.md` §7 end to end without Dan. It ran `install.sh`, checked the style was `default`, and checked there were 19 bundled and 17 linked skill manifests. It then did a dry run and the real upload. The registry now serves **researcher@1.0.28**, with all 19 customs bundled inside the package and only amol's 17 fetched separately. The `nori.json` version write-back was committed in dotfiles as `529c98c`.

The terminal can't answer the interactive conflict prompts, so the upload used `--resolve link`. The sks source (`uploadPolicy.js`) shows that action `link` is the one labelled "Use Existing". Dan got a "you're under review" email. Even so, the 1.0.28 package downloaded anonymously within minutes, from the address the installer uses (`/api/skillsets/researcher/tarball/researcher-1.0.28.tgz`), with all 19 SKILL.md files. The registry's version history confirms 1.0.27 (Sep 3) was the previous latest.

Follow-ups, all in dotfiles. PUBLISHING.md §7 was rewritten so any agent can run it on request with no prompts. §5 and §6 record the 1.0.28 fix and what the review email does and doesn't mean. NORI_NOTES' skill table was updated to 1.0.28 (`f067808`). dotfiles #96 was closed. Kelsey's original closing line was transcribed from the screenshot into `communication-styles/kelsey.original.txt` (`972eed9`). It's a .txt so the style-swap script can never put it into AGENTS.md. The screenshot was then deleted from this repo. Dan also got a paste-ready paragraph for amol describing the 404 behaviour.

## Topics Explored

- Running the upload without prompts: `--resolve link` is the same as picking "Use Existing"
- Whether the registry's review gates downloads of a new version
- The registry's version history (1.0.0–1.0.28, uploader, bundled/linked counts)
- How the style-swap script composes styles into AGENTS.md (it copies the whole file, comments included)

## Provisional Findings

- Review does not appear to block downloads of a new version of an already-approved skillset. 1.0.28 was public within minutes of upload. We can't tell whether that's owner-specific. `vouchStatus` is per skillset, not per version.
- The upload summary listed 4 of amol's skills as "Uploaded" (creating-skills, creating-slides, finishing-a-development-branch, using-skills). using-skills was confirmed still at 1.0.9 / `org_created`, so no new version was published. The other three weren't checked.
- The JSON's `dist.tarball` path (`/profiles/...`) returns an HTML page on the bare host. The working path is `/api/skillsets/<name>/tarball/<file>`.
- Dan's standalone packages (e.g. `finish-convo`) still 404, but nothing points at them now.

## Decisions Made

- Upload checklist is agent-runnable by default. Dan's only step is to ask ("upload the researcher skillset").
- Kelsey's original closing line is kept out of `kelsey.md` (it would reach AGENTS.md if the style is switched on). It lives in `kelsey.original.txt`.
- Deleted `Kelseys__chat__advice.png` from this repo after transcription.

## Results

- None saved to this repo. Commits are in dotfiles: `529c98c`, `f067808`, `972eed9`.

## Open Questions

- Whether amol wants the orphaned standalone packages cleaned up, and why packages Dan owns are invisible even to him. Dan has a paste-ready message.
- No clean-machine install test yet. The anonymous package download is strong evidence but not the same thing.
- Whether to switch on the `kelsey` style (carried over).
