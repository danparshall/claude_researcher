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

---

## Addendum — 2026-08-27 evening (close-out session)

**Date:** 2026-08-27 (UTC ~20:05–21:00)
**Machine:** Dans-MacBook-Pro
**Session type:** fresh-agent pickup, close-out of PR #52 + side-quest.

### What triggered the pickup

Dan opened the session with "sync with origin, and then let's discuss the apparently-dangling PR 52." Sync fast-forwarded main from `f372225` → `6998784` (PR #53 communication-style-prose swap). PR #52 was `OPEN`/`MERGEABLE`/`CLEAN` in git terms, but "dangling" in workflow terms: STATUS.md's Branch inventory didn't list `lite-multi-machine-note`, "Recent sessions" had no entry for 2026-08-21 or 2026-08-27, and the convo above had left three open questions unresolved.

### Open-question dispositions

- **(a) Stale parenthetical + (b) fragile "Multi-terminal sessions" pointer.** Dan collapsed both into one edit — deleted the entire `See personal_info.md "Multi-terminal sessions" for the fuller pattern (CLI users only ...)` block from `template_lite/LITE.md` lines 84–86 (option (b) from the earlier convo). Kills both the stale-parenthetical and Dan-specific-pointer concerns in a single move. Committed as `992d487`.
- **(c) PAT re-scope migration note.** Discussed at length. Dan's own read: "honestly I don't think anyone else is using LITE." Recommendation surfaced: skip the migration note entirely — defensive documentation warning yourself about a change you just made is theater, and a 6-month cleanup ticket would just be removing debt we created. Dan accepted, skipping (c).
- **(d) "Simple prose / no jargon" guidance search.** Not re-searched this session, but PR #53 (`communication-style-prose`, merged 2026-08-27 morning by another session) swapped the numbered writing-style block for prose — worth checking whether that closes the original gap Dan was looking for, or whether the missing thing is a separate concern. Flagged, not resolved.

### PR #52 close-out mechanics

Sequence, in order:
1. Commit `992d487` on branch (LITE.md drop) + push.
2. STATUS.md update on main (`4743560`): Branch inventory gains `lite-multi-machine-note`; "Recent sessions" gains today's close-out entry.
3. PR body rewritten to reflect the six-commit shape and the design decisions (`personal_info`-fetch vs. Never-list tension, PAT-migration-note skipped).
4. Merge attempt → `DIRTY`/`CONFLICTING`. Cause: step 2's Recent-sessions entry on main collided with the branch's own `a645085` Recent-sessions entry from the original session. Both bullets targeted the same insertion point.
5. Conflict resolution followed the PR #51 pattern: pulled `origin/main` into the branch, resolved STATUS.md by keeping **both** 2026-08-27 entries (close-out first, dev session second — newest-first per the section convention), also updated the Branch inventory line to say "merged" instead of "open for review". Merge commit `d518bb1` on branch, pushed.
6. `gh pr merge 52 --merge` → real merge commit **`6145b7d`** on main.
7. Follow-up STATUS commit on main **`2863e75`** filled in the real merge SHA in the Branch inventory line, matching the pattern from `f372225` (which had done the same for PR #51's `8a79715`).

### Side-quest

Dan asked to move `junk.txt` (untracked in `claude_researcher/`) into `bluedot_coursework/` as "UVC_notes.txt or something." Read the file first — it's substantive UV-C eye-safety notes drafted 2026-08-13: critique of Kaidzu et al. 2021, Ushio-employee majority-authorship COI, threshold-range mis-citation in Sugihara & Tanito 2022, 2025 Scientific Reports anesthesia/eye-closure critique, and a 7–10× spread in corneal-surface-cell turnover across three sources that all get invoked in far-UVC safety arguments (Kaidzu ~24h vs. Sugihara & Tanito ~48h vs. Blueprint 7d). Filed as `docs/active/biorisk/20260827_UVC_eye_safety_kaidzu_critique.md` in `bluedot_coursework` (alongside the other biorisk convo docs — `20260811_gof_dangers_and_uplift.md`, etc. — rather than at the repo root, since the content is a topical research note, not a course brief). Filing date `20260827` per that directory's convention; original 2026-08-13 draft date preserved in the commit message. Committed as `ea89dd2` in `bluedot_coursework`.

### Deliverables from this session

- claude_researcher: commits `992d487` (branch), `4743560` (main STATUS), `d518bb1` (merge into branch), `6145b7d` (PR #52 real merge commit on main), `2863e75` (follow-up STATUS with merge SHA).
- claude_researcher: PR #52 merged, closed.
- claude_researcher: PR body rewritten to six-commit shape.
- bluedot_coursework: commit `ea89dd2` (UVC Kaidzu critique filed in biorisk).

### Still-dangling (deferred, not blocking)

- **Two other undocumented worktrees** in `.worktrees/`: `flare-design` (`f549720`) and `precompact-update-docs` (`9a3d81f`). Neither is in STATUS's Branch inventory. Surfaced to Dan at end of session; deferred.
- **PR #53's writing-style prose swap** may or may not close the "simple prose / no jargon" gap the original convo flagged as open. Not re-checked this session.
