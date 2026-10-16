---
name: blind-session
description: "Survival kit for blind sessions. A blind session is a session opened with a scoped prompt cut from a workstream plan in scoped mode (skills/workstream_plan_skill.md), executing one step without full repo context. If your prompt says you are a blind session, this file plus your prompt are ALL you read. Not a skill — an asset: it carries the minimal conventions a session needs when it must not read CLAUDE.md, STATUS.md, or the plan."
triggers: >-
  Read only by a blind session under a scoped prompt; never part of a normal session's reading
---

# Blind session — read this and your prompt, nothing else

You are a **blind session**: a session opened with a scoped prompt from a plan,
executing one step of a workstream **without** the repo's full context. The
isolation is deliberate — your step's value (independent verification, parallel
safety, fresh eyes) depends on you *not* seeing the rest. Reading more does not
make you more helpful here; it destroys the point of the step.

## The reading rule

- Read this file and your prompt. Then read **only** the files your prompt lists.
- Do **not** open CLAUDE.md, STATUS.md, any `*_PLAN.md`, `workspace/`, or any
  file not listed — even for orientation, even if a search surfaces it.
- If you cannot proceed without a file outside your scope: **do not open it.**
  Stop, and report the blocker in your step report (see below).
- If you realize you have already seen out-of-scope material (a stray read, an
  over-broad search): declare it in your report. A contaminated step reported as
  contaminated is recoverable; one reported as clean is not.

## Minimal conventions

- **Language.** Work in English, whatever language the materials are in.
  Deliverable content may be in another language if your prompt says so.
- **Git.** Work on the branch your prompt names (if it names none: `main`).
  Commit with clear messages; push when your prompt's close sequence says to.
  Never force-push. Never resolve a merge conflict or rejected push yourself —
  stop and put it in your report.
- **Write territory.** Create or modify files only under the paths your prompt
  names. Everything else in the repo is out of bounds for writes, no exceptions.
- **Naming.** Files `lowercase_underscore`; a date leading a filename
  `YYYY-MM-DD_...`; ALL_CAPS only for structural files and for a content-file
  marker on a lowercase stem (`naming_conventions.md`'s closed list). Spell out acronyms on first use.
- **No tracker updates.** Do not touch STATUS.md, the plan file, to-do lists, or
  indexes. Your report is your only trace; the coordinating session does the rest.

## The step report

Before stopping, write your report to:

`workspace/step_reports/REPORT_<plan_stem>_S<N>_<YYYYMMDD>.md`

(your prompt gives `<plan_stem>` and `<N>`). Contents, short and factual:

1. **Step and date.**
2. **What was done and what was produced** (paths of files created/modified).
3. **Verification outcomes**, if the step verified something — findings as they
   are, including uncomfortable ones. If your output is a count or a
   classification, state the unit of count and record every judgment call that
   moved the number as a named call with its alternative count — never
   absorbed into the number.
4. **Blockers** — anything that stopped you, including files you needed but were
   not licensed to read.
5. **Contamination declaration** — "none," or exactly what out-of-scope material
   was seen and how.

## Closing sequence

Write the report → commit (report + your territory's work) → push → **stop**.
No further exploration, no summary of the wider workstream, no suggestions about
other steps. If your prompt chains to a next step ("when done, continue with…"),
follow it; otherwise the next move belongs to the coordinating session.

## If you are the one writing one of these

(For the session commissioning a blind step — not for the blind session
itself, which reads only this file and its prompt.) The prompt-cutting rules
live in `skills/workstream_plan_skill.md`, Part A, A5 — they govern every
blind-session prompt, whether or not a plan exists. For a standalone blind
step commissioned outside any plan, apply them minus the plan references and
follow that skill's "Blind steps without a plan" path: prompt filed in
`workspace/step_prompts/`, report named without `S<N>` on the shared stem,
the folder's standing `README.md` catalog as the trace.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
