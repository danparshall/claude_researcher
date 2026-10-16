---
name: multisession-task
description: >
  Governs the multi-session carryover — a per-task carryover doc that exists only
  because resource limits (context, execution risk, fatigue) force one current
  task to be carried across several sessions. Use when a task will not finish in
  one session and a resume prompt won't reliably carry it across the gap. The
  carryover doc lives in workspace/multisession_active_tasks/ as
  MULTISESSION_CARRYOVER_<task_stem>.md. Distinct from the workdesk queue
  (actions waiting on the user, not the task in hand).
triggers: >-
  "make a carryover"; a task that will not finish in one session and a resume prompt cannot
  carry
---

# Multi-session task skill

This skill governs the **multi-session carryover** — the working doc that carries
one task across the several sessions it takes to finish.

## What this governs — a constraint artifact

The carryover doc exists **only because** resource limits — context window, execution
risk, fatigue — force the work to be split across sessions. It is scaffolding for
*the task in hand*, not a record of work to do someday.

This is what makes it **categorically distinct from the workdesk queue**
(`workdesk/INDEX.md`). A queue row holds an action *waiting on the user* ("read
this," "decide this"); the carryover doc holds the live state of the task
currently being worked. The
test that keeps them apart: imagine infinite context, no execution risk, no
fatigue. The queue rows survive — they always waited on the user, never on
resources — but
the carryover **vanishes**, because the whole task would be done in one pass. The carryover
is the thing the constraints call into being; a queue row is gated on
the user's action, never on the constraints.

Consequence: a queue item that gets picked up and turns out to be
multi-session **does not grow into** a carryover. The row is cleared; a carryover is
**born at the stop**, when the task crosses the multi-session threshold. Clean
hand-off, two distinct constructs.

## When it fires — the two-question gate

A task crossing into multi-session territory triggers a two-question gate. It
fires at one of two moments: **recognized big up front** (create the carryover doc at
the start), or **started small, then hit the wall** (stop and create it now).
Same gate, two entry points. The session close is the gate's standing trigger:
`project_tracker_skill.md`'s **close check** asks of every unfinished task which
resume grade it needs — the STATUS entry's own Next line, a carryover, or a plan
file — and this gate decides between the first two; the entry's Resume field
points at the carryover.

The two questions split by *who can see the answer*:

- **Q1 — Is one more session enough?** The part **Claude** can read (the work
  remaining and the horizon).
- **Q2 — Can a prompt carry everything needed *and* still be intact when the user
  returns?** The **carrier-survival** part, which only **the user** can fully see. A
  prompt is fragile two ways: too small to *hold* the state (complexity), **or**
  fine in size but **stale by the time they return** (the gap — e.g. resuming
  after a night's sleep, where live context is gone even though the work itself
  is small).

**Both yes → leave a prompt, not a doc.** Reuse what's already there: the
workstream entry's Next line (or, if the next concrete step waits on the user, a
workdesk queue row) — *no new artifact, no skill machinery*. (If the user will simply re-prompt
from memory, even that is unnecessary.) **Either no → build the carryover doc. Ties go
to the doc** — a doc you didn't need is cheap; losing the thread across sessions
is not.

## Not for workstreams

A **workstream** — multi-artifact work with its own sequence, cross-artifact
dependencies, and open decisions; the unit of `STATUS.md`'s Current state — does
not get a carryover, however many sessions it spans. Its plan lives in a
**workstream plan file** with the work (`<stem>_PLAN.md`; the convention is owned
by `workstream_plan_skill.md`), with `STATUS.md` holding a short description, a
pointer, and a one-line position. The gate above applies to *tasks*: one bounded
piece of work that resource limits force across sessions. (One bounded step
*inside* a planned workstream can still earn a carryover of its own — the gate
fires on the step's task and the carryover stays scoped to it, workstream state
staying in the plan; see `workstream_plan_skill.md`'s Composition.) If the doc you are about to write needs
the full apparatus — resume-head layers accreting session over session,
cross-cutting state from other lines, dependencies on other artifacts — that is
the workstream signal: route to a plan file, not here.

## Who decides

When the user opens with "make a carryover," the burden flips to **Claude to argue
*down* to a prompt** where it has standing — citing what it can see (Q1, and the
complexity half of Q2). The user then either **accepts** (drop to a prompt) **or
states the carrier reason** ("I won't be back for a week," "this is fragile in my
head"). A **stated carrier reason makes the doc — no re-litigation.**

This is genuine pushback, not a rubber stamp: Claude pushes on the axis it can
read, and the final say sits with the user on the axis Claude is blind to (the gap).
The direction stays conservative — Claude argues toward the lighter artifact, and
the tie still goes to the doc.

## The carryover doc

**Home:** `workspace/multisession_active_tasks/`. The folder is created up front
and reads as state — **empty means "no active multi-session task."** The carryover doc
itself is **born on use**, when the gate calls for it. Two other files share the home, each
named in a `STATUS.md` entry's Resume field and neither a carryover, so this skill's gate does
not govern them: the unseen-close transcript (`project_tracker_skill.md`, the unseen path) and,
while one stands, the repo's `CONFORMANCE_ITEMS.md` (the ruled conformance items for
this repo; `structure_conventions.md`, the carryover home).

**Filename:** `MULTISESSION_CARRYOVER_<task_stem>.md` — the `MULTISESSION_CARRYOVER_`
prefix says what it is at a glance (an `ALL_CAPS` content-file marker on a lowercase
stem, `naming_conventions.md`'s closed list), the `<task_stem>` says which task. More than one carryover doc can
exist if more than one long task is genuinely in flight; the stem keeps them from
colliding.

**Format — a scaled-down mimic of a workstream plan.** Two parts decaying at different
rates inside one file:

- **Resume-head (volatile, top).** Rewritten every session close: where we are
  and where to pick up next. This is the handoff, living inside the doc rather
  than as a separate tier.
- **Stable body.** Three parts:
  - **Objective** — one line, never moves, so mid-stream adjustment never loses
    the thread.
  - **Sequence** — the ordered steps, each marked lightly (done / current /
    pending). No marker legend; that is plan-scale apparatus and too heavy here.
  - **Decisions & open questions** — the part most at risk across the gap, and the
    plan's defining discipline scaled down to one task. Two sub-parts:
    **settled decisions recorded as conclusions** (the answer, not the debate, so
    they are not re-litigated a session later) and **open questions** still to
    resolve (held here, not in the volatile resume-head, so a rewrite never drops
    them).

**Scales down hard.** A 2–4 session task is just the one-line objective plus a few
sequence bullets — no resume-head ceremony, and no decisions record until there is
a decision or open question worth keeping. If a task needs the full apparatus, it
is a *workstream*, not a task, and belongs in a plan file (`workstream_plan_skill.md`), not this folder.

## Per-session close update

Each session close updates the one doc:

- **Light** if the session went to plan — tick the step done, confirm the
  sequence, refresh the resume-head.
- **Heavier** if it deviated — revise the objective or sequence, record a step
  that split into more sessions, or note an interruption that had to be handled
  first.

The original objective stays at the top throughout, so mid-stream adjustment
never loses the thread.

## Completion — one fold, one delete

At task completion the doc **distills into `STATUS.md`** (the durable record of
what the task accomplished lands in the session close-out; a big-picture decision
or outcome the task settled goes to `RECORD.md` in the same close,
`project_tracker_skill.md`, "The record") **and is then deleted.** The folder returns to empty, which reads correctly as "no active
multi-session task."

**The delete is gated on the distill being *committed*, not merely attempted.**
This is the carryover doc's *own* guard — patterned on, but **not inherited from**,
the workdesk queue's confirm-gated clearing. Do not hang the delete off
`project_tracker`'s opt-in session-start surfacing; deletion is a completion act
run here, after the distill commit lands.

## Threads and hand-offs

This skill is **not invoked by an upstream skill handing over a carryover** — and that
follows directly from the constraint-artifact thesis above. A carryover doc is born
*at the stop*, when the gate fires; no other skill produces it and passes it on.
The gate fires on a multi-session task **whatever its origin** — a brainstormed
approach, the restructure an overturning exploration sets off, or a long job
recognized as multi-session up front. In every one of those cases the origin
produces *real work*, which carries its own plan **inside the work** and its
position in `STATUS.md`; the separate carryover doc appears only if and when resource
limits force the split, per the gate.

- **`finish_session_skill.md`.** No new machinery — `finish_session` routes the
  per-session close (Step 3) to the project-tracker close-out; the carryover doc's
  per-session update rides the active task (this skill's own close-update),
  not a new `finish_session` step.
- **`project_tracker_skill.md`.** No new machinery — an in-flight task is
  surfaced from `STATUS.md` at session start, and a completed task's distill
  lands in the `STATUS.md` close-out. The carryover doc is not a new tracked
  subsection.

---
*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
