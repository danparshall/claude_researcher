# LITE.md multi-machine note + personal_info.md wiring

**Date:** 2026-08-27
**Branch:** lite-multi-machine-note
**Machine:** Dans-MacBook-Pro
<!-- session spanned 2026-08-21 through 2026-08-27 based on date-changed reminders; started on Pro. -->

## Summary

Session started as a small doc addition — Dan noticed that `LITE.md` didn't warn readers about the multi-machine workflow (repo edited from other machines / by parallel Claude sessions) the way `RESEARCHER.md` does at §188 (mid-session refresh) and §372 (push early and often). Verified the gap by grep; RESEARCHER covered it, LITE was silent. Drafted a compact "Multi-machine / concurrent agents" block for LITE. First wording iteration overshot (fetch+SHA-compare pattern lifted from Dan's NORI block); Dan rolled back to the simpler `git pull --ff-only` form.

Mid-drafting, Dan asked whether web readers of LITE.md have access to `personal_info.md` — the pointer I'd drafted (`See personal_info.md "Multi-terminal sessions"`) would dangle for them if not. Checked: full RESEARCHER's project-instructions template fetches `personal_info.md` from `claude_research_config` at session start, but LITE's project-instructions template (`_PROJECT_INSTRUCTIONS_LITE.md.template`) does not — so web lite readers had no access. Dan chose to fix that gap directly rather than scope the pointer: wire `personal_info.md` fetching into lite mode too, mirroring RESEARCHER §2b's curl recipe.

Landed as 4 commits on `lite-multi-machine-note` and [PR #52](https://github.com/danparshall/claude_researcher/pull/52), open at session close. Dan said "merge it please" after the first two commits, then pivoted to add the personal_info wiring; when he came back to close the session, he did not restate the merge request, so the PR was left open for review.

Session also included a lookup Dan asked mid-flight — "where's the guidance about simple prose and not making up jargon?" — searched personal_info.md, RESEARCHER.md, LITE.md, nori-researcher/AGENTS.md, BOOTSTRAP.md, all skills, and both repos' `docs/`. Not found. Flagged as either misremembered or a "meant to add it, hasn't landed" — see Open Questions.

## Topics Explored

- Whether `LITE.md` covers the multi-machine / concurrent-agents drift risk that `RESEARCHER.md` does (§188, §372) — it didn't.
- Whether web readers of LITE.md have `personal_info.md` in scope — they didn't (lite's project-instructions template doesn't fetch it, unlike full RESEARCHER's).
- Whether extending personal_info.md fetching to lite mode violates lite's "Never list" (which bans automatic session-start overhead like a skills manifest). Argued: personal_info.md is a different category — it's *who the user is*, not workflow machinery — and full RESEARCHER treats it as essential enough to fail-loud on a 404. Dan concurred and extended that judgment to lite.
- PAT-scope cost of wiring the fetch: existing lite users would need to re-scope their PATs to include `<USERNAME>/claude_research_config` read. Accepted as a one-time cost.
- Whether guidance on "simple prose, don't make up jargon" exists anywhere in the workflow docs — Dan asked; grepped extensively, none found.

## Provisional Findings

- LITE.md lacked any mention of multi-machine drift or concurrent-agent-push risk; RESEARCHER.md's §188 (`git pull --ff-only` if user pushed from elsewhere) and §372 ("Push early and often") had no lite analog.
- Lite's `_PROJECT_INSTRUCTIONS_LITE.md.template` is scoped tighter than full RESEARCHER's — token grants read/write on the single project repo only, no `claude_research_config` access. Wiring personal_info.md fetch into lite requires widening the token scope.
- The `personal_info.md` "Multi-terminal sessions" pointer added in commit 2 has a fragility not addressed: that section name is specific to Dan's own personal_info.md, not a universal schema field. Other lite adopters (if any) wouldn't have a section by that exact name.
- No text matching "communication style", "simple prose", "avoid jargon", "no neologism", "plain english", or similar variants exists in `personal_info.md`, `RESEARCHER.md`, `LITE.md`, `BOOTSTRAP.md`, `nori-researcher/AGENTS.md`, `~/.claude/CLAUDE.md`, or any skill file. The `personal_info.md` "Note from Dan" contains a terminology-avoidance rule (prefer "AI Policy" over "AI Safety"), but that's scoped to one specific term with factional connotations, not a general prose-style principle.

## Decisions Made

- **Add a `## Multi-machine / concurrent agents` block to LITE.md** between "Session end" and "Skills". Simple form: `git pull --ff-only` before work, commit → push same beat, surface (don't auto-rebase) on divergent branches. Kept Dan's preferred wording verbatim. (Commit `cba951a`.)
- **Append a `personal_info.md` "Multi-terminal sessions" pointer to that block** — initially with a `(CLI users only — lite's web project instructions don't fetch it)` parenthetical scoping. (Commit `80e8656`.)
- **Wire `personal_info.md` fetch into lite mode session start**, mirroring RESEARCHER §2b. Adds new step 2 to LITE.md's Session start with fail-loud-on-404 handling. (Commit `2646f4f`.)
- **Widen the PAT scope note in `_PROJECT_INSTRUCTIONS_LITE.md.template` and add a `## Fetching personal_info.md` section** with the same curl+python3 recipe as RESEARCHER §2b. (Commit `035cfef`.)
- **Do not merge PR #52 in this session.** Dan's earlier "merge it please" applied to the first two commits; the personal_info wiring materially expanded scope (PAT-scope change, new automatic session-start fetch, tension with the "Never list") and warrants review before merge. Left for Dan.

## Results

No stand-alone `results/` files — output was the branch itself. Deliverables:
- Branch: `lite-multi-machine-note` (worktree at `.worktrees/lite-multi-machine-note/`).
- Commits: `cba951a`, `80e8656`, `2646f4f`, `035cfef`.
- PR: [#52](https://github.com/danparshall/claude_researcher/pull/52) — open at session close.

## Open Questions

- **Stale parenthetical in the multi-machine block.** After commit 3, the `(CLI users only — lite's web project instructions don't fetch it)` scoping is inaccurate — web lite users will now fetch `personal_info.md` too. Flagged in the PR test plan but not fixed. Three options considered: (a) drop the parenthetical only; (b) drop the pointer entirely; (c) genericize to "any multi-machine notes you've added". Not resolved before session close.
- **Fragility of the "Multi-terminal sessions" pointer.** That section name is Dan-specific; other lite users' `personal_info.md` files won't have it. Unresolved whether to leave, drop, or genericize.
- **Is there existing "communication style / simple prose / don't invent jargon" guidance somewhere I didn't search?** Dan asked and searched paths came up empty. Possibilities: misremembered; exists in an unindexed location; or meant-to-add but never landed. If it's the last, `personal_info.md` "Note from Dan" is the natural home — alongside the AI-Policy-vs-Safety terminology rule, which is a nearby-in-concept but narrower rule.
- **Should the `_PROJECT_INSTRUCTIONS_LITE.md.template` change include a note that existing users need to re-scope their PATs?** Currently the change assumes readers of the template are setting up fresh; existing users would silently get a 404 on first fetch after the change lands. A one-line callout in the changelog / migration note would help.
