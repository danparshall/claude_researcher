# Nori registry link + skill taxonomy (namespace vs inline vs linked)

**Date:** 2026-09-04
**Branch:** `main` (main-direct — docs-only)
**Machine:** Dans-MacBook-Air
**Model:** Fable 5.1
**Session codename:** `Dan (air, claude_researcher, 20260904T1416)`

## Summary

Dan asked for two things: (1) make sure this repo links the public registry page for the `researcher` Nori skillset (https://noriskillsets.dev/skillsets/researcher), and (2) get some clarity — documented somewhere — on what "namespace" skills vs "inline" skills vs the other categories actually mean. Context: the dotfiles side had just overhauled `sync-dotfiles` + `install.sh` to stop routing personal-machine sync through `sks switch` (the moderation-queue delay on `--public` uploads was gating Dan's own edits), so the terminology and the mechanics were both in flux.

I read the dotfiles side (`nori-researcher/NORI_NOTES.md`, `notes/nori_update_dance.md`, `notes/nori_block_local_composer.md`, `install.sh`, `nori.json`) and then checked the registry directly — the web page is a JS app so `WebFetch` only got the title; Dan dropped a PDF print of the page, and the JSON API at `/api/skillsets/researcher` gave the machine-readable version. Cross-checking those against the profile dir on disk and the local `nori.json` turned up a taxonomy with **two independent axes** (registry namespace of the *skillset*; travel mode of each *skill*) and five pieces of documentation drift, one of them a real gap (the public-facing README has no source of truth in git).

Both repos took doc edits this session. `claude_researcher`: README "About" + HUMANS.md now link the registry page. `dotfiles`: the NORI_NOTES "skill type" section was rewritten as a namespace-vs-tier explanation with a four-row table; the stale skill lists were fixed; two bigger items were filed as dotfiles tasks (#95, #96) rather than done here — Dan's call was "fixing is less work than a handoff" for the small stuff, and that held for NORI_NOTES but not for bringing the registry README under dotfiles.

## Topics Explored

- What the registry page actually renders: nori.json description, the profile README (long form with "Skills included" tables), a Skills panel tagging 8 skills `INLINE` and 24 as `name@version` links, accordions for subagents / slash commands / nori.json / AGENTS.md, the install box, version 1.0.27, Dan as owner, 56 downloads, `vouchStatus: org_reviewed`.
- **Namespace** — `public/researcher` = the `researcher` skillset in the `public` org. sks 0.31 split `~/.nori/profiles/` into `personal/` and `public/`; bare `researcher` is deprecated but resolves. No `danparshall/` org exists (sks: "Your available organizations: (none)"). The website hasn't caught up: `/skillsets/researcher` and `/api/skillsets/researcher` work, `public/`-prefixed API paths 404.
- **Skill tier** — verified from the 1.0.27 JSON: `skills[]` holds the 8 bundled/inline skills (add-paper, audit-docs, auditing-paper-summaries, clean-worktrees, init-research-repo, maintaining-decision-docs, update-docs, write-a-plan); `dependencies.skills` holds the 24 linked ones (17 amol/Tilework + 7 of Dan's: finish-convo, finishing-a-research-branch, task-create/remind/triage, add-to-reading-list, review-reading-list). Plus two tiers that never publish: local-only (`nori-researcher/skills/` but not in `nori.json` — create-new-repo) and personal (`dotfiles/skills/` — sync-dotfiles, sync-workspaces, new-website).
- Why `sks switch` prints `Skill not found` for exactly those 8: it resolves each `nori.json` dependency as a package, and inline skills aren't packages. Benign.
- What decides inline vs linked at upload time — could not close this from outside. See Open Questions.
- Where each piece of documentation belongs. Decided: this repo's users never touch `sks`, so the taxonomy lives in dotfiles (`NORI_NOTES.md`), and this repo only carries the link.

## Provisional Findings

- **The old "per-skill `type` field decides inline vs linked" story is at best incomplete.** Every `~/.nori/profiles/public/researcher/skills/*/nori.json` says `"type": "skill"` (all re-stamped 2026-08-25 by a registry download), yet the 8 still published INLINE on 2026-09-03. Best guess: sks decides by whether the name resolves as a package for the uploader's account.
- **The registry-facing README and GUIDE have no dotfiles source.** What the page renders under "README" is `~/.nori/profiles/public/researcher/README.md` — a registry-sourced real file from Jul 6, not the maintainer-facing `nori-researcher/README.md`. It's stale (`use-worktree`, `audit-papers`, "Eight subagents" vs 7 in nori.json, bare `download researcher` install commands, no task-*/reading-list/create-new-repo). Every `sks upload` republishes it unchanged. Same failure class as the six-week NORI-block outage: a public file with no writer. → dotfiles #95.
- **Local `nori.json` (1.0.29) and registry latest (1.0.27) disagree.** Registry deps omit the 8 inline skills; local lists all 32 with pins. The Sep 3 upload silently republished at 1.0.27. → dotfiles #96.
- NORI_NOTES skill lists were out of date: task-* called "local-only" (they're linked in the registry now), 10 customs listed (17 dirs exist), `using-git-worktrees` described as Dan's 1.0.7 fork (nori.json pins amol's 2.1.0; the fork is retired, Dan's customization survives as a patch in the composer results dir). Fixed this session.
- `/api/skills/<name>` 404s for *every* Dan-uploaded skill — including the linked ones — but 200s for amol's. So Dan's standalone packages resolve somewhere not visible anonymously (moderation-pending or user-scoped). Recorded, not resolved.
- The registry's `agentsMd` for 1.0.27 still carries the pre-composer "rendered by `sks switch researcher`" preamble; clears on the next accepted upload.

## Decisions Made

- README "About" gains a paragraph naming this repo as the browser-side port of the `researcher` Nori skillset with the registry link + install one-liner; HUMANS.md links inline where it introduces Researcher. Commit `4f910a4` on main (main-direct, matching this repo's habit for docs-only edits).
- dotfiles `NORI_NOTES.md`: "Custom skills / Adopted upstream / Local-only / Upstream / Skill type field" sections replaced by "Namespace vs skill tier — two different axes" (table + consequences + open question), the type-field story struck-through with a superseded note, task-* and using-git-worktrees history moved to Historical paragraphs, a new "registry-facing README and GUIDE have no dotfiles source" section, and two downstream cross-references fixed. `nori-researcher/README.md` gets a pointer + the registry URL. Commit `741454f` on dotfiles main, pushed.
- Filed dotfiles [#95](https://github.com/danparshall/dotfiles/issues/95) (bring profile README/GUIDE under `RESEARCHER_FILES` and refresh) and [#96](https://github.com/danparshall/dotfiles/issues/96) (reconcile nori.json at next upload; ask amol what decides inline vs linked).
- Fired reminders (3 in this repo, 8 in dotfiles) skipped at Dan's direction. #77 (grants, fired 2026-09-01) flagged as the one that matters.
- The PDF print of the registry page (557 KB) was archived in dotfiles as `nori-researcher/registry_page_20260904.pdf` at Dan's request (not symlinked into the profile dir, so it doesn't ship with `sks upload`). Left untracked here — this repo has no results dir.

## Open Questions

- What does `sks upload` key on when it sorts a skill into `skills[]` (inline) vs `dependencies.skills` (linked)? Per-skill `type`? Registry resolvability for the uploader? Something in `skills.json`? → ask amol (dotfiles #96).
- Where do Dan's uploaded standalone skills (finish-convo@1.0.0, task-create@1.0.1, …) actually live, given the anonymous API can't see them? Moderation queue, or a user-scoped namespace?
- Should the registry-facing README replace `nori-researcher/README.md` or sit beside it under another name with `install.sh` renaming at symlink time? (dotfiles #95 asks this.)
- Does a fresh `sks install public/researcher` on a machine with no local files actually receive the 8 inline skills? Still untested since 2026-07-20.

## Correction (same day, from the follow-up dotfiles session)

The "what decides inline vs linked" question above was answered by reading the sks 0.32.0 source (dotfiles `nori-researcher/PUBLISHING.md`, commits `e561141` → `142235f`): **the per-skill `nori.json` `type` field does decide it** — `"inlined-skill"` ships inline, anything else becomes a standalone package. My "at best incomplete" verdict was wrong: I inferred from Air's profile dir, but 1.0.27 was uploaded from Pro, whose untracked per-skill copies had diverged. Fix shipped in dotfiles: per-skill `nori.json` is now tracked and symlinked, all 15 customs are inline, and the registry README/GUIDE have a dotfiles source (#95, #96 both addressed there). Treat `PUBLISHING.md` as authoritative over the Provisional Findings section above.
