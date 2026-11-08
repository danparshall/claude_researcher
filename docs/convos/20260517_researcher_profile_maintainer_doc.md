# 2026-05-17 — Researcher profile maintainer doc + STATUS sync

**Date:** 2026-05-17
**Branch:** `tighten-section-0` (claude_researcher) — though most edits land in dotfiles
**Surface:** Claude Code (CLI), Dans-MacBook-Air

## Triggering concern

Dan: "we've had some issues in the last couple sessions with sorting out the distinction
between my personal data, the stuff in the `claude-researcher` repo, and the work I do
as maintainer of the Nori Researcher profile (which is upstream of 'claude-researcher').
It involves a dance of files between CLI and WebUI, and between my local machine, my
dotfiles repo, the `claude-researcher` repo, and Web UI inputs. We've had a couple
convos about this, but things are getting dropped."

## Inventory of prior work found

**Convos that produced the current architecture:**

1. `claude_researcher/docs/convos/20260513_personal_info_sync_brainstorm.md` (May 13-14) —
   architecture brainstorm. Started as "add §0.5 Discourse Register to RESEARCHER.md,"
   expanded into the full multi-surface analysis.

2. `dotfiles/docs/active/apply-researcher-workflow/convos/20260515_apply_researcher_workflow.md`
   (May 15) — applied the researcher workflow to dotfiles repo itself.

**Docs already in place:**

| Artifact | Status |
|---|---|
| `dotfiles/docs/historical/personal-info-sync/plans/01_personal_info_sync.md` | Plan B, shipped via PR #15 |
| `dotfiles/sync_to_basic_config.py` + tests | Implemented, merged |
| `dotfiles/claude/personal_info.md` | Canonical, with `<!-- CLI-ONLY -->` + `<!-- DISCOURSE_REGISTER:BEGIN/END -->` markers |
| `dotfiles/claude/.sync_state` | SHA-divergence guard state |
| `dotfiles/nori-researcher/README.md` | Multi-tenant boundary discipline doc (Plan B step 33) |
| `dotfiles/STATUS.md` + `dotfiles/CLAUDE.md` | Researcher workflow scaffolding (PR #17) |
| `dotfiles/notes/session_20260517_researcher_finishing_branch.md` | Captures the rollback (28456ae) + filing of #20 |
| dotfiles #20 (CLI↔Web drift), #19 (sks settings clobber), #16 (Bash persistence) | Tracking |

## Gaps identified (five)

1. **`claude_researcher` had no awareness of post-brainstorm history.** Brainstorm
   convo + STATUS entry there capture May 14 state; everything since (Plan B
   shipped, relocation attempt `09441d7`, rollback `28456ae`, #20 filed) was
   invisible from this side of the dance.

2. **`dotfiles/STATUS.md`** "Recent Sessions" log didn't capture the discourse-register
   rollback lesson. The story existed only in the commit message + the session
   writeup file; no STATUS-level surfacing.

3. **The deferred "principled fix"** (commit `28456ae`: extend
   `sync_to_basic_config.py` to inline `discourse_register.md` content during web
   push) wasn't tracked anywhere — no issue, no Open Items entry, no Parking Lot.

4. **`tighten-section-0` branch** in claude_researcher was alive but the rest of
   STATUS.md still said "Branch: main only" (line 33). Stale by ~4 days.

5. **Cross-references were one-directional.** dotfiles → claude_researcher pointers
   existed (Plan B links the brainstorm convo); claude_researcher → dotfiles
   pointers didn't (no link to #20 from the web-side repo, despite #20 being the
   exact drift concern that web-side edits could trigger).

## Decision

Per Dan: consolidate into ONE doc in dotfiles that explains the dual-profile
landscape, the personalization plumbing, what specifically has to be juggled, and
the recent rollback lesson. Capture deferred follow-ups inline rather than filing
a separate GH issue (one example doesn't yet earn the abstraction).

This closes Gaps 1, 2, 3, and 5 in one stroke (the doc is reachable from both
repos via cross-link, captures the rollback story, includes the deferred fix as
an open follow-up).

Gap 4 (stale STATUS line) handled as a one-line edit.

## Changes shipped this session

| Change | Path | Purpose |
|---|---|---|
| New doc | `dotfiles/notes/researcher_profile_maintenance.md` | Consolidated maintainer landscape — what Dan juggles, why two profiles, plumbing diagram, rollback lesson, open follow-ups |
| Edit | `claude_researcher/STATUS.md` (line 33) | Acknowledge `tighten-section-0` exists; add cross-link to the new dotfiles doc |
| This convo | `claude_researcher/docs/convos/20260517_researcher_profile_maintainer_doc.md` | Session record |

No code changes. No new GH issues filed (deferred fix captured in the doc instead).

## Open items / follow-ups

These are now surfaced in the new dotfiles doc's "Open follow-ups" section:

1. `dotfiles#20` — drift sync between the two researcher profiles (filed earlier,
   not new).
2. Sync-side inline rewrite for `sync_to_basic_config.py` (deferred fix from
   commit `28456ae` — captured in the doc, not yet an issue).
3. `tighten-section-0` actual §0 tightening — still deferred.

## Process findings

- **The dance is real and the documentation gap was real.** Two repos +
  one-directional cross-references + a parallel-agent commit landing during a
  finish-convo + a downstream rollback two days later = exactly the kind of
  distributed state that can't be reconstructed by reading any single STATUS.md.
  The fix isn't more discipline at each step; it's a consolidated reference
  document that both repos can point at.
- **Dan's framing was sharper than the agent's first cut.** Agent proposed five
  separate edits across three artifacts; Dan reframed as "one doc, with
  explicit framing about who the two profiles serve." That collapsed the
  problem cleanly.
- **claude-exit ceremony ran clean** — sacrificial PID killed as expected, target
  parent verified as `claude`. Nothing stood out.
