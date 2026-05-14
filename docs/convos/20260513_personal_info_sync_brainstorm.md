# 20260513-14 — Personal info sync architecture brainstorm

**Date:** 2026-05-13 → 2026-05-14
**Branch:** `discourse-register` (claude_researcher) — though most implementation lands in dotfiles
**Surface:** Claude Code (CLI)

## Summary

Started as a request to update RESEARCHER.md with a new §0.5 "Discourse register" section containing four curated dialectic-style exchanges (real, from Dan's sessions). Expanded into a multi-surface architecture brainstorm covering: (1) how Dan's personal config propagates across CLI and web UIs, (2) how the public researcher profile actually renders for both platforms via two separate artifacts that have been drifting independently, and (3) where personalization content (including the new discourse register) should actually live.

End result: §0.5 work in the public template is dropped. The discourse register exchanges move to `dotfiles/claude/personal_info.md`, which becomes canonical for personal content with automated sync to `<USERNAME>/basic_config/personal_info.md` for web parity. The existing `discourse-register` branch in claude_researcher shrinks to just §0 tightening (orthogonal cleanup). Plan B (in dotfiles) is the main implementation work; persona/discipline core alignment between the two public researcher renderings is parked as a separate later concern.

## Topics Explored

- Initial §0.5 insertion on `discourse-register` branch in `claude_researcher` — TOC entry + full discourse-register block (HTML-comment wrapped for easy excision) between §0 and §1 of `template/RESEARCHER.md`. Not committed.
- §0 history: traced via `git log` to commits `0c99e5b` (initial four-trait paragraph form, May 11 17:33) and `633c1dd` (single Push-Back paragraph edit dropping universal-baseline phrases that were already in personal_info.md, May 11 18:08). No prior leaner version — the current full-paragraph form is original.
- Three-chunks framing of `~/.claude/CLAUDE.md` (user's mental model: static-personal + Nori-managed + permissions-managed). Verified actual structure has four blocks: the seed top from `dotfiles/claude/CLAUDE.md.template` is also there, but is only copied once at initial install and never regenerated (orphan).
- `personal_info.md` divergence: `<USERNAME>/basic_config/personal_info.md` is 39 lines, schema fields ("Git fluency: fluent", "Mode: claude.ai-only", "Paper naming format:"), v1 format. `dotfiles/claude/personal_info.md` is 73 lines, prose-heavy, no schema fields, contains "Note from Dan" + machine setup + dogfooding nudge + multi-terminal block. Not in sync. Neither is a strict parent of the other; they serve overlapping purposes for different platforms and have evolved independently.
- Wrinkle (user-surfaced): Dan maintains and uploads the public "researcher" Nori skillset via `sks upload researcher`. Source is `dotfiles/nori-researcher/` (symlinked into `~/.nori/profiles/researcher/`). So there are TWO public researcher profile renderings: web (`claude_researcher/template/RESEARCHER.md`) + CLI (Nori registry, sourced from `dotfiles/nori-researcher/CLAUDE.md`).
- Verified `sks` semantics by reading the npm package source at `/opt/homebrew/lib/node_modules/nori-skillsets/build/src/`:
  - `cli/features/shared/instructionsLoader.js`: `sks switch` reads profile's CLAUDE.md, strips any pre-existing NORI-AI markers, applies template path substitution, appends auto-generated skills list, then **surgically replaces just the `BEGIN NORI-AI MANAGED BLOCK`/`END` region** in `~/.claude/CLAUDE.md`. Content outside the block is never touched. Earlier worry about static-personal content being clobbered: disproven.
  - `cli/commands/registry-upload/registryUpload.js` + `utils/uploadFileFilter.js`: `sks upload` tarballs the entire `~/.nori/profiles/<name>/` directory recursively (resolving symlinks), filtering only system junk (`.DS_Store`, `.nori-version`, vim swap, AppleDouble, backup files). **No content filtering, no Dan-personal pattern detection.** Boundary is discipline-enforced only.
- Confirmed `dotfiles/nori-researcher/GUIDE.md` and `README.md` (regular files uploaded as part of the tarball, not symlinked from dotfiles) contain no Dan-personal references — boundary has held.
- Repo visibility verified: `dotfiles` PRIVATE, `basic_config` PRIVATE, `claude_researcher` PUBLIC.
- Iterated through several positions on where the discourse-register content should live:
  1. *Initial agent proposal:* slot contract in public RESEARCHER.md + content in personal_info.md (both surfaces).
  2. *Privacy refinement (agent):* voice content in dotfiles only, not basic_config — the verbatim exchanges are sensitive enough that even private-but-network-fetched-every-session is too exposed.
  3. *User pushback on (2):* parity across UIs is the explicit goal; the privacy distinction was overcautious — content reaches Anthropic-side context either way; both repos private at rest; for non-CLI academic adopters the asymmetry would be especially harmful since they have no CLI side at all.
  4. *User pushback on the slot-contract idea:* `claude_researcher` shouldn't own the distribution mechanism for Dan's personal content. Personalization patterns don't need a public-template API surface; content can be self-describing in personal_info.md.
  5. *Final landing:* discourse register in `dotfiles/claude/personal_info.md` (canonical), automated sync to `basic_config/personal_info.md` for web parity, strips only genuinely-CLI-only operational content (multi-terminal block, machine inventory, dogfooding nudge, Nori-block-editing pointer) — content that's *about* CLI setup, not about Dan.
- Project Instructions text role clarified by user: stays minimal-bootstrap-only. Doesn't carry personal content. No sync target needed. Academics doing first-session onboarding can paste the bootstrap once; agent then guides them to populate `<username>/basic_config/personal_info.md` going forward.
- UX corollary (user-surfaced): agent CAN edit `basic_config` via the user's PAT; agent CANNOT edit Project Instructions UI. So personalization content in basic_config is iterable in-session ("Claude, update my push-back stance"); content in Project Instructions is paste-stuck. Architecturally reinforces "all personalization in personal_info.md, Project Instructions stays thin."
- Sync direction policy for Dan specifically: dotfiles canonical, one-way overwrite to basic_config. Dan's discipline: never edit basic_config from web sessions (if you'd want to, do it in dotfiles next CLI session instead). Cheap safety net (~10 lines Python): SHA-divergence check in sync script aborts with a clear message if basic_config was modified out-of-band, converts a silent failure mode into a loud one.
- Audience consideration: most `claude_researcher` adopters are non-CLI academics. For them, `basic_config` IS canonical (no dotfiles, no sync). The Dan-specific dotfiles plumbing is more complex than the academic path; academics get the simple path for free.
- Persona/discipline core alignment between RESEARCHER.md (web) and `dotfiles/nori-researcher/CLAUDE.md` (CLI Nori upload source) — drift between two public artifacts. Deferred. With parity as explicit goal, becomes more important not less; parked until Plan B is drafted.
- `CLAUDE.md.template` orphan: only copied at initial install, never regenerated; still says "AI Safety and Advocacy" (Dan now explicitly prefers "AI Policy"), has model prices "verified March 6, 2026". `install.sh` comment "regenerated by sks switch" is misleading — sks switch only touches the Nori block, not the whole file.

## Provisional Findings

- **Architecture is now coherent.** Dotfiles owns ALL personalization and its distribution. `claude_researcher` (and the Nori-published researcher profile) own only the workflow/persona/discipline that all adopters share. Personal content never leaks into public artifacts.
- **Slot-contract idea was premature abstraction.** Discourse register is the first instance of a structured personalization pattern; one instance doesn't motivate a public API. Self-describing content in personal_info.md is sufficient. If a second instance later emerges and the duplication becomes painful, revisit then.
- **"CLI-only sensitive voice" was an overcautious distinction.** Removed in favor of one CLI-only-operational filter that strips only machine-setup and dogfooding content that doesn't apply to web sessions.
- **`sks switch` is non-destructive to non-Nori content.** Static-personal at top, personal-info block, permissions block — all safe. The install.sh comment is misleading but the actual behavior is correct.
- **`sks upload` boundary is discipline-only.** No code-level guard against Dan-personal content leaking into the published Nori profile via `dotfiles/nori-researcher/`. Worth documenting with a README so the discipline is explicit, but pre-push hook would be overkill for the current rate of edits.
- **Onboarding for non-CLI academics is genuinely simple.** Create `<username>/basic_config` repo, drop in a PAT, paste the bootstrap into the claude.ai Project, talk to the agent: agent reads personal_info.md (initially empty or schema-only), proposes additions based on the conversation, writes them back via the PAT. No copy-paste, no scripts, no dotfiles. The complex path is Dan's because Dan wants CLI parity.

## Decisions Made

- **§0.5 / DISCOURSE_REGISTER does NOT go in the public template (`claude_researcher/template/RESEARCHER.md`).** The existing in-tree edits on the `discourse-register` branch (TOC entry + full block) will be reverted. Branch scope shrinks to just §0 tightening.
- **DISCOURSE_REGISTER content lives in `dotfiles/claude/personal_info.md`** with no special privacy classification; propagates to both CLI managed block and `basic_config/personal_info.md`.
- **Personal info sync architecture:** dotfiles canonical, two outputs:
  - (existing) `update_claude_personal_info.py` → `~/.claude/CLAUDE.md` PERSONAL-INFO managed block, ALL content.
  - (new) `sync_to_basic_config.py` → `basic_config/personal_info.md` via `gh api`, strips only sections marked `<!-- CLI-ONLY -->`.
- **One-way sync with SHA-divergence guard:** dotfiles overwrites basic_config; pre-push check fetches current basic_config SHA, compares to last-pushed SHA stored in dotfiles (e.g., `dotfiles/claude/.sync_state`), aborts on mismatch with a clear message. No automatic merge.
- **Project Instructions stays bootstrap-only.** No sync target, no paste-source file generation.
- **Persona/discipline core alignment** between `template/RESEARCHER.md` and `dotfiles/nori-researcher/CLAUDE.md` is **deferred**. Real concern, especially given parity goal, but not blocking Plan B. Park for a separate brainstorm + plan.
- **`CLAUDE.md.template` orphan resolution: Option A.** Delete the template, fold its static content (model prices table from March 2026) into a new "## Reference data" section in `personal_info.md`. Update `install.sh` to create an empty `~/.claude/CLAUDE.md` on first install; managed blocks (PERSONAL-INFO via `update_claude_personal_info.py`, NORI-AI via `sks switch`, PERMISSIONS via `update_claude_permissions.py`) populate it from there.
- **Schema fields (Git fluency, Mode, Paper naming format) live in dotfiles canonical** as a new "## Operating preferences" section in `personal_info.md`. Not CLI-ONLY-marked — propagates to both surfaces. Harmlessly redundant on CLI (not parsed); parsed on web.
- **`dotfiles/claude/.sync_state` is committed** to dotfiles, not gitignored. Cross-machine sync requires it to travel with the canonical content.
- **`dotfiles/nori-researcher/` gets a `README.md`** documenting the multi-tenant boundary discipline. No pre-push hook (lightweight only).
- **Fix the misleading `install.sh` comment** in Plan B (one-line tweak: clarify that sks switch only regenerates the Nori block, not the whole file).
- **Convo named `20260513_personal_info_sync_brainstorm`**, not the earlier-proposed `20260513_discourse_register_§0.5_insert` — name reflects where the convo landed, not the starting prompt. ASCII slug matches existing convo file convention.

## Results

No code changes landed this convo. Artifacts produced:
- This convo summary at `docs/convos/20260513_personal_info_sync_brainstorm.md`.
- Plan B at `dotfiles/docs/plans/01_personal_info_sync.md` (separate branch in dotfiles repo).

State of the `discourse-register` branch in claude_researcher at convo end: still has the §0.5 insert + TOC entry uncommitted in `template/RESEARCHER.md`. These will be reverted before §0 tightening proceeds — handled in follow-up session, not this one.

## Open Questions

- **Plan B implementation timing.** Plan written; actual implementation is Dan's call. Estimated bite-sized-task count makes it a 1-2 session job in dotfiles.
- **Persona/discipline core alignment.** Parked, but real. Will need its own brainstorm + plan when picked up. With parity as the explicit goal, this is now a higher-value item than it looked initially.
- **§0 tightening shape.** Three options offered earlier: (a) demote four trait subheadings to inline bold leads, (b) drop the second corollary paragraph under Push Back, (c) tighten the framing paragraph. Dan hasn't picked. To be resolved when §0 tightening proceeds.
- **Branch rename.** `discourse-register` no longer reflects scope (DR moved out of this branch). Suggested `tighten-section-0`. Not acted on.
