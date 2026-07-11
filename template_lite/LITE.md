# Lite-mode runtime instructions (LITE.md)

You are an agent on claude.ai working in a small utility repo (dotfiles, canary
scripts, one-off tooling) — not a research project. This file lives at the
**root of the user's repo** (copied from upstream `template_lite/` at setup),
so a single clone gets both the code and its instructions. Trade-off accepted:
per-repo copies can drift from upstream; lite is small and stable enough that
drift is cheaper than a second clone every session.

Design principle: **session-start cost proportional to task weight.** Most
sessions here are minutes long. Read little, write little, leave the repo
current.

## Session start

1. Clone the repo with the PAT from Project Instructions:
   `git clone https://x-access-token:${TOKEN}@github.com/${USER}/${REPO}.git /home/claude/${REPO}`
2. Read this file (done, if you're reading this), then `STATUS.md` and
   `DECISIONS.md` at the repo root. Skim `git log --oneline -15`.
3. Respond to the user's first message. No name handshake, no reminder sweep,
   no skills manifest.

## Disposition (condensed from RESEARCHER.md §0)

- **Follow instructions** — do X, not your charitable interpretation of X.
- **Push back on bad ideas** — lead with the flaw at full strength, then
  whether it's fixable. Don't manufacture objections either.
- **No silent decisions** — name defaults you picked and scope you expanded.
- **Show the seam** — one clause on any back-end behavior the user didn't ask for.

## Memory model

**`git log` is the tracker.** Anything expressible as a commit is recorded as
a commit, with an intentional message. The files below carry only what the
log structurally cannot.

### STATUS.md — current state
Current intent, open questions, and a session log of **≤5-line entries, hard
cap**. When the session log exceeds ~10 entries, move the overflow to
`HISTORY.md` (append-only, newest-first). Rotation is by **count, not age** —
a cold repo touched twice a year must not sweep away its own recent context.

### DECISIONS.md — append-only rationale log
The answer to "why did I do X?" a year later. Trigger heuristic: *if the user
asked that question, would `git log` answer it? If not, write an entry.*
Fires when a session: chose between real alternatives; adopted a convention;
reversed a prior decision; **decided not to do something** (no commit exists
for those — this file is their only record). Most sessions produce zero
entries. Newest-first; never rewrite an old entry — append a new one and fill
the old entry's `Superseded` field. Entry shape (all link slots optional):

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
Same function as the full workflow: when work is big enough to need **more
than 1–2 tests**, the deciding conversation ends by writing a plan doc
(architecture + the test list), and a later session executes it via TDD.
An adopted or abandoned plan earns a DECISIONS.md entry pointing at it.

### docs/active/ and docs/historical/ — flat
Convo files are **opt-in and exceptional**: written only when a session
produced exploratory reasoning not reducible to a DECISIONS entry. No
per-branch nesting. When `docs/active/` exceeds ~10 files, move the oldest to
`docs/historical/` — count-rotated, same rationale as STATUS.

## Session end

No ceremony. Before finishing: update STATUS.md (intent + one ≤5-line entry),
append DECISIONS.md if the heuristic fired, commit, push. That's the whole
wrap-up.

## Never list

Lite will never grow: research lines / branches-as-lines, a skills manifest,
convo-name handshakes, task reminders, wrap-up ceremonies, per-branch docs
scaffolds, or calibration tiers. If a repo starts needing these, the answer
is graduation to claude_researcher, not features here.
