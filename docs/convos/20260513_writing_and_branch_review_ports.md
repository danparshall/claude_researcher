# claude_researcher — Plan 05 Path 1 execution (W4.1 + W4.3 ports)

**Date:** 2026-05-13
**Repo:** claude_researcher (dev repo)
**Branch:** main
**Surface:** claude-code (CLI)
**Plan:** [`docs/plans/05_aitaxbid_followups.md`](../plans/05_aitaxbid_followups.md) — Path 1 (W4.1 + W4.3) shipped this session.
**Ship commit:** `9ca89b8` (`plan 05 W4 Tier A ship: iterative-writing-workflow + branch-document-review`)

## Summary

Path-1 execution of the Plan 05 Wave 4 Tier A ports — Andrea's `writing_skill.md` and `BranchWorkflow_Skill.md` from the AITaxBID kit. Both ports were heavily pre-specified by yesterday's flesh-out session, so today's work was the implementation pass: read sources, verify SHAs hadn't drifted, apply the specified transformations, write the two `SKILL.md` files, slot the new "Writing & document workflow" group into `SKILL_INDEX.md`, and update Plan 05 status lines. Total: 379 insertions / 9 deletions across 4 files, one ship commit, pushed to origin.

The only port-time decision that came up was the W4.3 branch-naming format — Plan 05 had recommended keeping Andrea's `mmm-d` per defer-to-Andrea principle but flagged it as confirm-at-port-time. Dan overrode in favor of `MMdd` (2-digit month + 2-digit day, no year) on **lexicographic-sort grounds**: text-month formats put December before January alphabetically; single-digit-day numeric formats sort wrong (`5-15` before `5-2`). `MMdd` avoids both failure modes. The reasoning is captured inline in the skill body so future readers see the *why* of an otherwise arbitrary-looking format choice.

The execution itself was clean — the heavy lifting was the prior flesh-out. Source files (`writing_skill.md`, `BranchWorkflow_Skill.md`) verified byte-identical to Plan 05's scoping SHA `e0a736d` (despite AITaxBID HEAD having moved to `abd1c54...` since — commit `4a46580` touched `writing_skill.md` ~27 seconds before `e0a736d` but is also pre-scoping). All four W4.1 transformations and five W4.3 transformations applied as spec'd. Provenance frontmatter establishes the `aitaxbid_source` precedent — Wave 1 uses `nori_swe_source`, Wave 2/3 uses `nori_researcher_source`, Tier-A AITaxBID ports use `aitaxbid_source`.

## Work Done

### W4.0 — Sandbox tooling spot-check

Skipped at port time. SKILL.md authoring doesn't exercise the sandbox runtime tooling (pandoc, LaTeX, etc.) — those matter only when the user *uses* `branch-document-review` to regenerate companion artifacts. The spot-check Plan 05 specified ("confirm pandoc still reports 3.1.3 in next WebUI session") remains a deferred action for whoever next opens a claude.ai sandbox chat.

### W4.1 — iterative-writing-workflow

Source: `~/code/AITaxBID/skills/writing_skill.md`, 169 lines, SHA `e0a736d` (2026-05-02). Verified byte-identical to scoping version. Pure-thought skill (no git/CLI ops), so no `## Runtime detection` banner inserted — adaptation profile matches Wave 1 SWE carryovers, not Wave 2/3 Researcher skills.

Four transformations applied per Plan 05:

1. **Provenance frontmatter** added: `aitaxbid_source: ~/code/AITaxBID/skills/writing_skill.md@e0a736d (2026-05-02)`. Single-frontmatter block (just one more YAML key beneath Andrea's existing `name` and `description`), not a stacked-frontmatter pattern.
2. **CLAUDE.md → RESEARCHER.md/STATUS.md** rephrase. Two locations: Protocol 1 "Adapting to your project" and Protocol 2 "Setting up for a new project." Both now say *"your project's `RESEARCHER.md`, `STATUS.md`, or equivalent coordination file."*
3. **Dated footer dropped** (*"Last updated: April 11, 2026"*) — provenance is in frontmatter now.
4. **Style-profiles affordance added** per Dan's request from yesterday's flesh-out: one-line addition to the "Style profiles" bullet in Protocol 2's setup checklist — *"If you don't have a style-profiles doc, you can create one — ask the agent to draft a versioned `<project>_Style_Profile.md` from a sample of your prior writing."* Keeps the existing reference actionable for users new to the pattern without dragging Andrea's three project-specific profiles into scope.

Andrea's content otherwise intact, including the H1 title, the two-protocol structure, "questions first, actions second," "show before committing," "do NOT search past chats," and the "rendered file in the side panel" presentation hint (which is claude.ai-specific but harmless in Claude Code).

Naming: Andrea's YAML frontmatter named the skill `iterative-writing-workflow`; Plan 05's stub used `writing-skill` as illustration only. Per defer-to-Andrea, Andrea's own name wins. Destination: `template/skills/iterative-writing-workflow/SKILL.md`.

### W4.2 — Diff mechanism (already locked, executed here)

Compare API decision (Option A) was locked yesterday with full reasoning matrix. Today's execution implemented it in W4.3's Step 4 (see below). No new W4.2 work.

### W4.3 — branch-document-review

Source: `~/code/AITaxBID/skills/BranchWorkflow_Skill.md`, 178 lines, SHA `e0a736d` (2026-05-02). Andrea's file has NO YAML frontmatter — starts with an H1 — so the port creates the frontmatter fresh: `name: branch-document-review`, a multi-sentence description distilled from her **Applies to** / **Does not apply to** intro block, and `aitaxbid_source`.

Five transformations applied per Plan 05:

1. **Step 4 diff → Compare API.** Andrea's `git diff <creation-commit> <branch-tip>` replaced with:
   ```bash
   curl -s -H "Authorization: token $TOKEN" \
     "https://api.github.com/repos/$REPO/compare/$BASE_SHA...$BRANCH_NAME"
   ```
   Step 1 now explicitly notes *"Keep `MAIN_SHA` around — Step 4 uses it as the base of the Compare API call."* The parse instructions describe walking `files[].patch` to identify added/modified lines outside `[...]` blocks. 300-file response cap surfaced as inline blockquote note.
2. **Branch-naming format → `MMdd`** (Dan's port-time override of Plan 05's defer-to-Andrea recommendation). 2-digit month + 2-digit day, no year. Examples: `oecd-paper-edits-0501`, `q3-report-redraft-0603`. The reasoning is captured inline in the skill body so users see WHY this format was chosen — text-month formats break sort (Dec/Jan), `m-d` numeric formats break sort on single-digit days (`5-15` before `5-2`), `MMdd` avoids both, year omitted because branch lifetime is short.
3. **Provenance frontmatter** added: `aitaxbid_source: ~/code/AITaxBID/skills/BranchWorkflow_Skill.md@e0a736d (2026-05-02)`.
4. **Dated footer dropped** (*"Last updated: May 2, 2026 — v2.0..."*). Also dropped the `**Status:** active. Skills kit v1.4.` and `**Owner:** Andrea Lopez-Luzuriaga.` lines per "internal kit detail, not relevant to the ported version."
5. **Name-stripping** throughout. Andrea/Marta/the RA → "the user"; project slug examples generalized (`marta-oecd` → `oecd-paper`, `aml-paper` → `tax-policy-brief`, `cfr-strategy` left as it's a project type, not a person name; `marta-oecd-edits-may-2` → `oecd-paper-edits-0502`). Verified clean: `grep -c -i 'andrea|marta| RA |aflopezluzuriaga'` returns 0.

Two intentional preservations worth flagging:
- **Spanish bracketed example** (`[change "12 puntos" to "12 puntos del PIB"]`) kept. It's illustration of bracket usage, not a name reference. Andrea works in Spanish/English; the example is realistic content. Dan didn't object when I flagged this in the report-back.
- **Andrea's H1 title** kept ("# Branch workflow for collaborative document review"). The Plan 05 spec said "leave content otherwise intact"; the H1 is meaningful framing and the YAML `name:` field doesn't fully replace it.

Destination: `template/skills/branch-document-review/SKILL.md`.

### W4.4 — SKILL_INDEX.md

New "Writing & document workflow" section inserted between "Knowledge-management skills" and "Working-style skills (carried over from upstream Nori)." Two entries (`iterative-writing-workflow`, `branch-document-review`) with **Trigger** and **URL** fields per the existing manifest contract.

Top-of-file `**Status:**` block extended with a sentence explaining why the AITaxBID skills don't carry the `## Runtime detection` banner: writing skill is pure-thought; `branch-document-review` carries REST recipes inline at Steps 1/4/6. Sets the precedent for future AITaxBID-sourced ports.

### W4.5 — Ship commit

`9ca89b8` on `main`, pushed to `origin/main`. Contains W4.1 + W4.3 + W4.4 + Plan 05 status updates. Excluded `template/README.md` (untracked from another session — multi-terminal protocol).

### Plan 05 status updates

Marked Shipped 2026-05-13:
- W4.1 (with note that Andrea's own YAML name `iterative-writing-workflow` was kept)
- W4.2 ("Locked at Option A — implemented in W4.3")
- W4.3 (notes the MMdd override + name-stripping verification)
- W4.4 (notes the top-of-file status-block extension)
- W4.5 (Wave 4 Tier A criterion met; W3.1 / W5 still open)

Branch-naming open question marked resolved (struck through with `~~` and full reasoning).

## Process Findings

### Stale gitStatus snapshot at session start

The harness took its `git status` snapshot before commit `61ac97a` (the prior session's flesh-out ship) landed. So the snapshot reported `STATUS.md`, `docs/plans/05_aitaxbid_followups.md`, and `docs/convos/20260513_plan05_flesh_out.md` as modified/untracked, when in reality they were already committed. This affected my initial commit-strategy framing (I proposed two commits — flesh-out + ship — and Dan agreed, but the flesh-out half had already shipped). Net effect: one commit instead of two, but the *spirit* of "two commits" was honored across the two sessions. Worth recording for future sessions: don't trust the gitStatus snapshot for the "what's uncommitted right now" question — re-check with `git status --short` after reading STATUS.md.

### Defer-to-Andrea is genuinely overrideable

The W4.3 branch-naming decision exercised the "defer to Andrea on methodological details" principle's escape hatch. Plan 05 recommended `mmm-d` per the principle and flagged it for port-time confirmation. Dan's `MMdd` override was crisp and correct — lexicographic sort matters for branch listing UIs (especially the GitHub web UI's branch dropdown), and `mmm-d` measurably fails that property. The plan's "Recommendation made / Confirm at port time" framing did its job: presented the default, surfaced the choice, accepted the override without friction. The reasoning got captured inline in the skill body so future readers don't have to dig through plan archaeology to understand the format.

### "Sycophancy check" non-event

No major pushback moments this session. The work was largely mechanical (apply specified transformations), and the one decision-point (branch-naming) flipped on a concrete technical argument (lexicographic sort). If anything, I made the call to preserve the Spanish bracketed example without checking — Plan 05's name-stripping rule was about people's names, and the Spanish-language example is content-illustrative, but it's worth Dan knowing I made that call without confirmation. He's free to swap it for a locale-neutral example if he disagrees.

### TaskCreate usage

Used TaskCreate this session (4 tasks: W4.1, W4.3, W4.4, Plan 05 update) — appropriate for execution work with clear sub-steps. Distinct from the 2026-05-13 flesh-out session which deliberately skipped TaskCreate as redundant with Plan 05 itself. Heuristic: execution sessions benefit from task tracking; planning sessions where the plan doc IS the checklist don't.

## Decisions Made

- **Branch-naming format for `branch-document-review`** locked as `MMdd` (no year, 2-digit month + 2-digit day, lexicographically sortable within a year). Dan override of Plan 05's defer-to-Andrea recommendation. Reasoning captured in the skill body.
- **`iterative-writing-workflow`** confirmed as the skill name (Andrea's own YAML), not `writing-skill` (Plan 05 stub illustration).
- **No Runtime detection banner** for either of the new skills. Codified in SKILL_INDEX's top-of-file status block as the precedent for AITaxBID-sourced ports (pure-thought OR carries REST recipes inline).
- **`aitaxbid_source` provenance frontmatter** established as the convention for Tier-A AITaxBID-sourced ports (single-key addition to the existing `name`/`description` frontmatter; format: `path@SHA (date)`).

## Open Items (post-ship)

- **W4.0 spot-check** — pandoc 3.1.3 still on sandbox? Confirm in next WebUI session. Not blocking anything but worth verifying before the first `branch-document-review` user hits Step 4's regeneration path.
- **Path 2 — W3.1 + Tier C knock-on edits** — still open, independent of Wave 4. Sequenced after add-paper has real user data (~5 papers) per issue #4.
- **First real user test of the writing skills** — both new skills want a beta session that actually uses them. Especially `branch-document-review` Step 4: the Compare API parse instructions are described, not coded, and the first real use will surface whether the description is concrete enough for a runtime agent to implement on the fly.
- **`template/README.md`** — still untracked from another session. Same pattern as 2026-05-12. Leaving alone per multi-terminal protocol; expect it'll surface as someone else's commit eventually.

## Suggested Next Session

Two natural paths, either order:

- **Path 2 — W3.1 fold-in into `add-paper`** (the larger remaining Plan 05 task). Involves: Step 0 triage, filename convention parameterization, dual-protocol summary template, BibTeX step, Tier C STATUS.md project-parameters section, BOOTSTRAP.md interview update, dual provenance stamp. Plan 05 lists 9 deliverables. ~45–60 min. Independent of any Wave 4 work.
- **First beta session test of the new W4 skills.** Open a fresh claude.ai chat in a `branches`-mode research project and walk through either skill end-to-end to see how the runtime agent fetches and uses them. Would surface the Compare API parse-instructions adequacy question above.

Path 2 is the larger remaining piece; the beta test is shorter but de-risks the writing skills before more people see them.

## Late-session addendum — Plan 06 written; W3.1 handed off to fresh agent

After the update-docs checkpoint, Dan asked to start Path 2 / W3.1 now. Confirmed scope through AskUserQuestion: **Full Path 2 / W3.1 now** (all 9 deliverables + 5 knock-on edits), **BOOTSTRAP-style placeholders** (`{FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf`), **keep Andrea's two-format split** (academic + institutional separately).

Initial UI/text answer disagreement surfaced — Dan's text said "first of three options" (= minimal) but UI showed "Full Path 2" twice. Re-confirmation question resolved it as Full Path 2. Worth recording: the AskUserQuestion UI may auto-default or pre-pick when a turn is interrupted by a rate-limit; trust the explicit re-confirmation over the initial answer.

Did orientation reads for execution: Andrea's `paper_processing.md` in full (320 lines, byte-identical to scoping SHA `e0a736d` verified), current `add-paper/SKILL.md` (151 lines), `personal_info.md.template`, `init-research-repo/SKILL.md`, `RESEARCHER.md` §2c, BOOTSTRAP.md Batch 3 / Step 5 / Step 7 STATUS.md seed. Locked the pipeline-strategy decision: **parameterize Nori's 5-step structure by Protocol A/B** rather than duplicating the whole pipeline like Andrea did (her own intro says the pipeline is identical; only filename, summary emphasis, and BibTeX entry type differ). Locked the dual-provenance frontmatter format: `nori_researcher_source` first + `aitaxbid_source` second (sets the precedent for future synthesis ports; Nori upstream has no clean SHA so uses `<version> (ported in <commit>, <date>)`).

At ~250k tokens of context — past the point of efficient execution for a 250-300-line skill rewrite + 4 supporting-file edits — Dan asked to wrap with a plan instead. **Wrote [`docs/plans/06_w31_addpaper_synthesis.md`](../plans/06_w31_addpaper_synthesis.md)** (~470 lines, comprehensive enough for a fresh agent to execute with zero session-context loss):

- Pre-flight reads list (STATUS, Plan 05, today's convos, source files, files-to-edit)
- All design decisions confirmed at design time (4 items, each with rationale: pipeline strategy, placeholder semantics, two-format split, default values table)
- 9 deliverables with file paths, line ranges, exact strings, and source-line references to Andrea's paper_processing.md
- 3 knock-on edits (init-research-repo, RESEARCHER.md, "where do project params live" pinning)
- 6-check verification script for use before committing
- Suggested commit message
- "Deliberately does NOT cover" list (5 items, including the W3.1 `per-file` summary code path explicitly deferred)
- 4 open questions for the executing agent to raise if they hit them (slug case, year casing, PAPER_INDEX naming, existing-user backfill)
- Estimated effort: ~45-60 min for a fresh agent

**Process moment worth recording:** Dan's "you're at 250k tokens; want to write a plan and hand off?" was a textbook context-management call. I had design clarity but reading capacity for ~3 more files before the SKILL.md rewrite would have started yielding diminishing returns. The plan-and-handoff pattern preserves design-decision provenance while routing the execution work to a fresh agent. This is also exactly what the `write-a-plan` skill is for — formal invocation skipped because the conventions are familiar from prior plans in this repo (01-05) and reading the skill at 250k was the wrong tradeoff.

**What's now uncommitted at end of session:**

```
M STATUS.md                                                          (Plan 06 entry + Suggested-next-session repointed)
?? docs/convos/20260513_writing_and_branch_review_ports.md           (this convo, with this addendum)
?? docs/plans/06_w31_addpaper_synthesis.md                           (the handoff plan)
?? template/README.md                                                (still untracked, still leaving alone)
```

Next move: finish-convo to commit + push, then the fresh agent starts on a clean tree from `origin/main`.
