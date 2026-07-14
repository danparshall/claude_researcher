# Lite-mode runtime instructions (LITE.md)

You are an agent on claude.ai working in a small utility repo (dotfiles, canary
scripts, one-off tooling) — not a research project. This file lives at the
**root of the user's repo**: one clone gets code and instructions, accepting
per-repo drift (recoverable — see "Checking for lite updates").

Design principle: **session-start cost proportional to task weight.** Read
little, write little, leave the repo current.

## Session start

1. Clone the repo with the PAT from Project Instructions:
   `git clone https://x-access-token:${TOKEN}@github.com/${USER}/${REPO}.git /home/claude/${REPO}`
2. Read this file (done, if you're reading this), then `STATUS.md` and
   `DECISIONS.md` at the repo root. Skim `git log --oneline -15`.
3. Respond to the user's first message. No name handshake, no reminder sweep,
   no skills-manifest load.

## Disposition (condensed from RESEARCHER.md §0)

- **Follow instructions** — do X, not your charitable interpretation of X.
- **Push back on bad ideas** — lead with the flaw at full strength, then
  whether it's fixable. Don't manufacture objections either.
- **No silent decisions** — name defaults you picked and scope you expanded.
- **Show the seam** — one clause on any back-end behavior the user didn't ask for.

## Memory model

**`git log` is the tracker** — anything expressible as a commit is a commit,
with an intentional message. Files below carry only what the log cannot.

### STATUS.md — current state
Current intent, open questions, and a session log of **≤5-line entries, hard
cap**. Past ~10 entries, move overflow to `HISTORY.md` (append-only, newest-
first). Rotate by **count, not age** — a cold repo must keep its recent context.

### DECISIONS.md — append-only rationale log
The answer to "why did I do X?" a year later. Trigger: *would `git log`
answer that question? If not, write an entry.* Fires on: chose between real
alternatives; adopted a convention; reversed a prior decision; **decided not
to do something** (no commit exists — this file is the only record). Most
sessions produce zero entries. Never rewrite old entries — append a new one
and fill the old `Superseded` field. Entry shape (link slots optional):

```
## YYYY-MM-DD — short title
- **Q:** the question that forced a choice
- **Considered:** alternatives, comma-separated
- **Chose:** what + one-line why
- **Links:** plan docs/plans/... · convo docs/active/... · SHA(s)
- **Superseded:** — (or date + title of the superseding entry)
```

For plan-sized work, the entry is an *index* into the commit ← plan ← convo
chain; for small or negative decisions, it is the sole record.

### docs/plans/ — design/execution split
Same function as the full workflow: work needing **more than 1–2 tests** gets
a plan doc at the end of the deciding convo (architecture + the test list);
a later session executes it via TDD. Adopted or abandoned plans earn a
DECISIONS.md entry.

### docs/active/ and docs/historical/ — flat
Convo files are **opt-in and exceptional**: written only when a session
produced exploratory reasoning not reducible to a DECISIONS entry. No
per-branch nesting; when `docs/active/` exceeds ~10 files, rotate the
oldest to `docs/historical/`.

## Session end

No automatic ceremony. Before finishing: update STATUS.md (intent + one
≤5-line entry), append DECISIONS.md if triggered, commit, push. The user
may invoke `finish-convo` (see Skills) for a fuller close.

## Skills — on demand, never at session start

Standard skills from upstream `template/skills/` (e.g. `finish-convo`,
`brainstorming`) remain fully usable — the difference is overhead: no manifest
at session start; fetch a skill only when the user invokes it (shallow-clone
upstream as in "Checking for lite updates", read that one SKILL.md). Map
full-workflow references to lite's surface (`docs/active/<branch>/` → flat
`docs/active/`, `RESEARCH_LOG.md` → `HISTORY.md`) and skip steps whose
targets don't exist here.

## One-time setup (converting a repo to lite mode)

1. Copy this file to the repo root as `LITE.md`.
2. Seed `STATUS.md` (`## Current intent`, `## Open questions`, `## Sessions`)
   and an empty `DECISIONS.md`; all other files/dirs on first need.
3. Add this pointer to `CLAUDE.md` at the repo root (create if absent) —
   Claude Code and other local agents read `CLAUDE.md` automatically and
   would otherwise never open this file:

   > **Workflow:** this repo uses lite mode. Read `LITE.md` at the repo root
   > before doing work — it defines the memory model (STATUS.md, DECISIONS.md,
   > docs/plans) and session rules. (Same text for `AGENTS.md` if present.)

4. For claude.ai access: fill `template_lite/_PROJECT_INSTRUCTIONS_LITE.md.template`
   from upstream and paste it into a Project's instructions.

## Checking for lite updates

On "check for lite updates" (or similar): the canonical copy is
`template_lite/LITE.md` in upstream `danparshall/claude_researcher`;
shallow-clone and diff:

```bash
git clone --depth 1 https://github.com/danparshall/claude_researcher.git /home/claude/.cr_upstream
diff /home/claude/${REPO}/LITE.md /home/claude/.cr_upstream/template_lite/LITE.md
```

Clone, not `raw.githubusercontent.com` (the raw CDN can be 24h+ stale).
Present the diff for the user to decide; **never blind-overwrite** — local
copies may carry deliberate per-repo customizations.

## Never list

Lite will never grow *automatic* overhead: research lines / branches-as-lines,
session-start skills manifests, convo-name handshakes, task reminders,
mandatory wrap-up ceremony, per-branch docs scaffolds, calibration tiers.
On-demand skill use (above) is fine. If a repo starts needing the rest,
graduate it to claude_researcher — don't add features here.
