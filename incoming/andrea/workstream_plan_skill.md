---
name: workstream-plan
description: "The workstream plan file — <stem>_PLAN.md living with the work — for a workstream: multi-artifact work with its own sequence, cross-artifact dependencies, and open decisions. Plain mode (the default): steps run in ordinary full-context sessions; the plan holds the step table and the sketch, and lookup surfaces (STATUS.md, the workdesk queue) carry a pointer plus a one-line position, never a copy. Scoped mode (the upgrade, decided by the in-skill gate): steps run in separate sessions with controlled reading scopes — blind-session prompts cut from the plan, disjoint write territories, the report inbox; companion asset skills/BLIND_SESSION.md. Does NOT cover: the multi-session carryover, which exists only because resource limits (context, execution risk, fatigue) split one bounded task (that is multisession_task_skill.md; a carryover can nest under one step of a plan — see Composition); or actions waiting on the user (the workdesk queue, workdesk/INDEX.md)."
triggers: >-
  "make a plan for this workstream," "this needs blind sessions," "cut the prompts"; "we are
  here" / "where are we on plan X" on re-entry; a STATUS entry outgrowing its slot
---

# Workstream Plan

This skill governs the **workstream plan file** — `<stem>_PLAN.md`, living beside
the work it steers. A **workstream** — multi-artifact work with its own sequence,
cross-artifact dependencies, and open decisions; the unit of `STATUS.md`'s
Current state — carries its plan in a plan file, not in anyone's memory and not
in `STATUS.md` itself.

One skill, two modes:

- **Plain mode — the default.** Steps run in ordinary full-context sessions. The
  plan holds what the workstream produces, the step table, and the sketch; the
  "we are here" ritual carries re-entry.
- **Scoped mode — the upgrade.** The same plan additionally controls what each
  step's session reads: steps execute in separate sessions with **controlled
  reading scopes** — blind sessions with prompts cut from the plan, disjoint
  write territories, a report inbox. Chosen only when the upgrade gate (below)
  says a step needs isolation or parallel execution.

The mode is a property of the plan, not of the trigger: the skill is entered the
same way for both, and the gate decides. A plain plan upgrades in place if a
step later turns out to need isolation.

*Documented predecessors: this skill merges the plain workstream plan-file
convention (owned by `project_tracker_skill.md`
v2.1.0–v2.2.0) and `scoped_plan_skill.md` (v1.x, retired at this merge —
its machinery is Scoped mode below, intact). `project_tracker_skill.md` keeps
only the STATUS-surface mechanics: the entry shape and the close-out position
refresh.*

## When to use this skill

Read this skill when:

- The user says "make a plan for this workstream," or the `CLAUDE.md` "Plan"
  routing trigger's triage lands on *workstream* (its other branch, the
  carryover, is `multisession_task_skill.md`).
- A `STATUS.md` Current-state entry has visibly outgrown its slot — the
  `project_tracker_skill.md` close-out offers the plan file; on the user's yes,
  this skill runs.
- A brainstorm or an exploration-branch finalize resolves into a workstream —
  those skills' hand-offs offer the plan file.
- A workstream has steps that could run in parallel in separate sessions, or
  steps where independent verification requires that the executing session not
  see other parts of the repo ("this needs several sessions but not because of
  context," "I need to control what the new session reads," "this needs blind
  sessions," "cut the prompts").
- The user opens a session with "we are here on plan X," "where are we on X," or
  points at an existing `<stem>_PLAN.md` — that is a re-entry (the "we are
  here" ritual; in scoped mode, a **coordinating session** re-entry).
- A prompt identifies the current session as a **blind session** — then this
  skill is NOT read; the blind session reads only `skills/BLIND_SESSION.md` and
  what its prompt licenses. (This bullet exists so a coordinating session
  recognizes the boundary; a blind session never opens this file.)

**Do not use this skill for:**

- **The resource-driven case.** One bounded task that context, execution risk,
  or fatigue force across sessions gets a carryover, not a plan — see
  `multisession_task_skill.md`. The test: with infinite context the carryover
  vanishes; a workstream plan survives, because its structure is in the work
  itself.
- **Deferred actions waiting on the user.** Those are rows in the workdesk queue
  (`workdesk/INDEX.md`), pointing at artifacts — not plan steps.

**The triage is entrance-independent.** The carryover-vs-plan triage runs the
same whoever raises it — the user saying "plan," or Claude suggesting a carryover
when a session needs to split (a context check, a looming close): check what is
actually being carried before picking the artifact. If what's splitting is one
bounded task, carryover; if it's a workstream, the plan file already carries
re-entry and no new artifact is needed; if it's one bounded step *inside* a
planned workstream, the two nest — see Composition.

## The plan file (both modes)

- **Placement.** `<stem>_PLAN.md` next to the work it steers, on `main`. Never
  a central plans folder; discoverability comes from the lookup surfaces below.
  The plan stays on `main` even when steps' work runs on branches — the plan is
  the coordination surface, and re-entry and the STATUS pointer must find it
  without knowing branch state. Where each step's work runs is the step's own
  business: the repo's workflow mode and the step's own skills (a review
  branch, an exploration branch, a blind step's prompt-named branch) decide.
- **Register.** Plain didactic prose (the plain-register rule in `CLAUDE.md`'s
  Working Conventions): full sentences, one idea per beat — the plan is read
  cold at re-entry, days later.
- **Single authoritative copy.** The plan file is the only full copy of the
  step structure and state. Renders in chat are ephemeral; **lookup surfaces
  carry a pointer plus a one-line position, never a copy** (see below).

Skeleton:

```markdown
# <Workstream name> — Plan

**Status:** active, opened YYYY-MM-DD
**Home:** <folder>
**Mode:** plain | scoped
**Governed by:** skills/workstream_plan_skill.md

## What this workstream produces
<one or two paragraphs>

## Step table

| Step | Produces | Depends on | State |
|---|---|---|---|
| S1 <name> | ... | — | not started |

<scoped mode adds columns: Parallel group, Mode (blind/open), Write territory>

## Sketch
<see "The sketch" — numbered list minimum; mermaid when the structure earns it>

## Open decisions
<what is still unsettled; in scoped mode, what only a coordinating session can settle>
```

Scoped mode adds two sections: **Prompts** (each blind step's verbatim prompt)
and **Report log** (step / report file / swept on / outcome).

**States:** not started / in flight / done / blocked — plus **report in**
(scoped mode only: a blind session has reported, awaiting sweep).

## The sketch

Every plan file carries a **sketch section** — the step structure with current
state marks, at a glance. The section is required; **the form scales with the
structure**:

- **Minimum form** — a numbered step list with per-step state:

  ```
  1. [done]       Corpus assembled
  2. [in flight]  Drafting section A
  3. [not started] Peer review
  ```

- **Mermaid** — required when the structure earns it: parallel steps,
  non-linear dependencies, or any blind step (scoped mode always qualifies).
  Conventions: one node per step, labeled `S<N>: short name`; blind steps
  marked `[blind]`, open steps unmarked, coordinating checkpoints as distinct
  nodes; arrows for dependencies; parallel steps side by side with no arrow
  between them; chained steps drawn in a single lane. Plain-text fallback if
  the interface does not draw it.

The sketch's job is **position at a glance for re-entry** — it is what "we are
here" renders and what the user reacts to. It is updated at every session close
on the plan (and at every coordinating-session close in scoped mode).

**Sketch before plan.** In both modes, the proposed step table and sketch are
presented for the user's reaction *before* the plan file is written — a wrong
dependency or an unnecessary step is cheapest to catch on the sketch. This is
an enumeration point: present the sketch and stop. In scoped mode this is a
hard gate (no approved sketch, no prompts).

## Lookup surfaces — pointer plus position, never a copy

Any surface that points at a plan carries three things: a short description, a
pointer to the plan file, and a **one-line position** — `step 3/6 — drafting`
— refreshed at session close, never a copy of the step table or sketch.

- **`STATUS.md` Current state**: the workstream's entry is description +
  pointer + position. The entry shape and the close-out refresh are
  `project_tracker_skill.md` mechanics; this skill owns what the line says.
- **The workdesk queue** (`workdesk/INDEX.md`): when a plan artifact starts
  waiting on the user (a step's output ready for review, a plan decision only they
  can take), the row points at the artifact or the plan's Open decisions —
  per the queue's own pointer-not-artifact rule.

The position line is derived from the step table (`<current step>/<total> —
<short phase label>`); if the two ever disagree, the plan file wins — the
position line is a cache, and stale cache is repaired at the next close.

## Plain mode — the default lifecycle

**Construct.** Decompose the workstream with the user into steps — for each:
what it produces, what it depends on, current state. Render the sketch and
present it (sketch before plan; stop for the user's reaction). Then write the
plan file with **Mode: plain**, and trim the `STATUS.md` Current-state entry to
description + pointer + position.

**Maintain.** Steps run in ordinary full-context sessions; no prompts, no
territories, no report inbox. As work happens, the step table and sketch update
— at the latest at the session close that touched the workstream.

**Re-enter.** The "we are here" ritual (below), every time.

**Retire.** When the last step is done: write the workstream's **close line**
in its `STATUS.md` entry — closed on what date, what was produced and where it
lives, what was learned — and delete the plan file; it is scaffolding, and the
deliverables and the close line stay (the entry rotates to `STATUS_ARCHIVE.md`
at that close, per `project_tracker_skill.md`; the pre-v6.5 Archived-workstreams
row is retired). Before deleting, run the **last-call review**: anything in the
plan that supports a still-live claim (a number a deliverable cites, a decision
rationale a reader will need) is distilled into the close line or the
deliverable's own documentation, and **the plan's big rulings and its outcome go
into `RECORD.md`** as rows of the part's section, with their Why
(`project_tracker_skill.md`, "The record"): the close line says what came out, the
record says what was decided on the way and still holds. Git history preserves without surfacing — a record backing a
live claim must stay findable in the tree.

## "We are here" — the universal re-entry ritual

The user runs two or three workstreams in different repos at a time; the plan
file, not anyone's memory, carries the state. **Every re-entry to an active
plan opens the same way, before any new work:**

1. Read the plan file.
2. *(Scoped mode only)* Sweep `workspace/step_reports/` for reports not yet in
   the Report log, and update step states from them.
3. Check the step table against repo reality (commits, files produced since
   the plan was last updated) and refresh states.
4. Re-render the sketch with current state marks.
5. Present the sketch with a short "we are here" summary — **and stop.** The user
   reacts to the sketch; their reaction decides what happens next (work the next
   step, revise the plan, cut prompts, re-run a step).

At the close of any session that moved the workstream: write the updated sketch
and step table back into the plan, refresh the position line on the lookup
surfaces (the `STATUS.md` refresh rides the `project_tracker_skill.md`
close-out), and — scoped mode — log swept reports.

## The upgrade gate (plain → scoped)

Scoped mode is bought only when the work's structure demands it. Upgrade when a
step needs **isolation** (independent verification that must not see the
material it verifies, fresh-eyes review) or **parallel execution** in separate
concurrent sessions. Resource limits are never the reason (that is the
carryover). **Ties go to plain**: scoping costs context and courier effort, so
a step is blind only when contamination would actually damage its output.

**Upgrade in place.** The existing plan text is the "What this workstream
produces" material. Add: **Mode: scoped** in the header, the step table's
Parallel group / Mode / Write territory columns, the mermaid sketch (scoped
always qualifies), and the Prompts and Report log sections. Prompts are cut
only for the steps that need scoping — open steps keep running as ordinary
sessions. Then run Scoped mode's setup check (Part F).

A scoped plan does not downgrade — once any step has run blind, the plan keeps
the scoped sections as its record.

## Scoped mode

Scoped mode is run by **coordinating sessions** — full-context sessions
(CLAUDE.md, STATUS, the plan) where the user and Claude construct or revise the
plan, cut prompts, and sweep reports. Only coordinating sessions update the
plan. Steps marked blind execute in **blind sessions**.

### Core concepts

- **Blind session.** A session opened with a scoped prompt, executing one step
  without full repo context. It reads `skills/BLIND_SESSION.md` plus exactly
  what its prompt licenses, writes a step report, commits, and stops. It never
  opens CLAUDE.md, STATUS.md, or the plan.
- **The courier.** The user carries prompts from the plan file into fresh
  sessions. The plan stores every prompt verbatim, so the courier route works
  days later and from any interface; the executing session never opens the plan.
- **Read scope / exclusions.** What a step's session may open, and — stated
  first — what it must not. Exclusions come first because a file once read
  cannot be unread.
- **Write territory.** The paths a step may create or modify. Territories of
  steps in the same parallel group must not overlap, so concurrent sessions
  cannot collide.
- **Report inbox.** `workspace/step_reports/` — where every blind session
  leaves its step report. Reports are disposable scaffolding: swept by the next
  coordinating session, deleted when the plan retires.

### Part A — Constructing the scoped plan (coordinating session)

**A1 — Gate check.** Confirm scoped mode is warranted (the upgrade gate above).
If the driver is resource limits, route to the carryover. If no step needs
isolation or parallel execution, stay plain.

**A2 — Decompose.** As in plain mode, plus per step: whether it can run in
parallel with others (assign a parallel group); mode — **blind** or **open**
(open steps run as ordinary sessions or inside a coordinating session — they
still get a territory, but no scoped prompt); for blind steps, the read scope
(exclusions first) and the write territory.

**A3 — Sketch approval gate.** Sketch before plan, as in every mode — and here
it is a **hard gate**: do not proceed to A4 without the user's approval. Mermaid
per the sketch conventions above.

**A4 — Write the master plan.** The skeleton above with **Mode: scoped** and
the Prompts / Report log sections.

**A5 — Cut the prompts.** Write each blind step's prompt into the plan.
The rules below govern **writing any blind-session prompt**, not only prompts
cut into a plan: a coordinating session commissioning a standalone blind step
(see "Blind steps without a plan" below) applies them from here, minus the
plan references. Prompt-cutting rules:

1. **Identity and exclusions first.** The prompt opens: "You are a blind
   session (defined in `skills/BLIND_SESSION.md` — read it first). Do not open
   CLAUDE.md, STATUS.md, `<plan file>`, or anything not listed below."
   Step-specific exclusions (the files being verified, other steps'
   territories) are named explicitly right there.
2. **Self-contained.** The prompt carries everything the step needs: the task,
   the licensed reading list, the write territory, the branch to work on,
   output naming. It must survive being pasted into a fresh session on any
   interface with no other context.
3. **Fixed close.** Every prompt ends: write the step report to
   `workspace/step_reports/REPORT_<plan_stem>_S<N>_<YYYYMMDD>.md`, commit,
   push, stop. No STATUS update, no plan update, no further exploration.
4. **Chaining only when scope-independent.** "When done, continue with the
   S<N+1> prompt below" is allowed only when the next step's read scope and
   task do not depend on the current step's outcome. If they might, the chain
   breaks and the prompt ends with "stop; the next step is cut at the
   coordinating session."
5. **Territory stated even for solo steps.** It costs one line and protects
   the plan when a step later gains a parallel sibling.
6. **Counting steps state the unit and record their calls.** Where the step's
   output is a count or a classification, the prompt states the unit of count
   and instructs the session that any judgment call it meets which the prompt
   did not foresee is **recorded as a named call with the alternative count
   stated**, never absorbed into the number. A blind session cannot ask, so
   recording the call is the only move it has; see the key rule "A count
   carries its boundary calls" for why the rule binds beyond blind steps.

**A6 — Wire and close.** Check `skills/BLIND_SESSION.md` and
`workspace/step_reports/` exist (create per Part F if not). Trim the
`STATUS.md` entry to description + pointer + position. Commit plan and wiring;
session closes per `finish_session_skill.md`.

### Part B — What a blind session does

(For the coordinating session's awareness; the blind session itself learns this
from its prompt and `skills/BLIND_SESSION.md`, never from this file.)

Read `skills/BLIND_SESSION.md`; read exactly what the prompt licenses; do the
step inside the write territory; write the step report (what was done, what was
produced, verification outcomes, anything that blocked, any contamination —
see below); commit; push; stop.

**Contamination rule.** If a blind session cannot proceed without opening a
file outside its scope, it does not open the file. It stops and reports the
blocker. If it realizes it has already seen out-of-scope material (a stray
read, an over-broad search), it declares that in the report — a contaminated
verification is reported as contaminated, and the coordinating session decides
whether the step re-runs.

### Blind steps without a plan

A blind session may be commissioned with **no plan behind it** — a one-off
independent read, re-derivation, or recheck, where the value is the same
isolation the scoped mode prizes, applied to a single verification question
rather than to a step in a sequence. This is the natural shape of an
independent-verification step, not an edge case: the need for one is usually
discovered after the work it checks is already done.

The path:

- **The prompt is cut by A5's rules, minus the plan references.** It opens by
  saying there is no plan ("There is no plan file for this step; do not go
  looking for one") and follows rules 1–6 above: identity and exclusions
  first, self-contained, fixed close, territory stated, counting calls
  recorded.
- **The prompt is filed in `workspace/step_prompts/`** as
  `PROMPT_<stem>_<YYYYMMDD>.md` — the sibling of `step_reports/`, created on
  first use with its standing `README.md`, a catalog document whose catalog is
  the register of standalone blind steps (one row each: date, stem, question,
  report); with no plan file to log the step, **the register is the trace**.
  The body is `standing_documents_template.md`'s (`workspace/step_prompts/`;
  the inbox's label is there too).
- **The report drops the `S<N>`**:
  `workspace/step_reports/REPORT_<stem>_<YYYYMMDD>.md`, sharing the prompt's
  stem; assets next to the report.
- **The report sweep covers standalone reports.** The coordinating session's
  sweep of `workspace/step_reports/` (Part D) reads them like any step
  report, and retirement (Part E) deletes them under the same last-call
  review.

### Part C — Parallel execution

Steps in the same parallel group may run as concurrent blind sessions. The plan
guarantees their write territories are disjoint; their prompts name only their
own territory. On `main`-only repos disjoint territories are what prevents
collisions; on branch-mode repos each prompt names its own branch and the
coordinating session merges. If two parallel steps turn out to need the same
file, that is a plan error: stop, report, re-plan at the coordinating session.

### Part D — Coordinating-session re-entry

The "we are here" ritual, with the scoped additions: sweep
`workspace/step_reports/` (ritual step 2 — standalone reports included; see
"Blind steps without a plan"), update states from reports, and use
the full state vocabulary in the sketch (done / in flight / report in, awaiting
sweep / blocked / not started).

### Part E — Completion and retirement

As in plain mode's Retire — plus: delete the swept step reports (they are
scaffolding; anything worth keeping was distilled). The deletion pass doubles
as the **last-call review**: before deleting, check each verification-type
report and distill any outcome that supports a still-live claim (a number in a
deliverable, a result the white paper cites) into the STATUS row or the
deliverable's own documentation.

### Part F — Setting up a repo for scoped mode

1. `skills/BLIND_SESSION.md` ships with this skill; confirm it is present (or
   recreate it: the blind-session definition; the minimal conventions —
   working language, git hygiene, no force-push, naming conventions, branch
   discipline; the report format and inbox path; the contamination rule; the
   closing sequence). It contains **only** generic survival material — nothing
   project-specific, no findings, nothing whose exposure could contaminate a
   step.
2. Create `workspace/step_reports/` with its standing `README.md`, a label
   marking it as the disposable blind-session inbox
   (`structure_conventions.md`: a `workspace/` subfolder carries a standing
   document, never a map).
3. The stop line for a blind session is the template's, in `CLAUDE.md`'s form
   comment at the top, regenerated at every propagation — nothing to add by
   hand; a repo not yet on the v6.5 template gets it at its next propagation.

## Composition with other skills

- **`multisession_task_skill.md` — the carryover nests under a step, never
  over the plan.** If one bounded step's work won't fit a session, the
  carryover gate fires on it independently, exactly as on any bounded work —
  the plan neither blocks nor auto-opens it. Division of state: the plan holds
  workstream-level state (the step stays *in flight*, its row noting
  "carryover active"); the carryover holds task-internal state (the resume
  head, micro-decisions). The boundary is the carryover's own "Not for
  workstreams" rule applied one level down: the moment a carryover starts
  accreting cross-step dependencies or open workstream decisions, that content
  belongs in the plan. Re-entry reads the plan first (position in the
  workstream), then the carryover (position in the task). At task completion
  the carryover folds into the `STATUS.md` close-out and is deleted; the
  plan's step flips to done in the same close.
- **`project_tracker_skill.md`** — owns the `STATUS.md` surface: the
  Current-state entry shape (description + pointer + position), the close-out
  position refresh, and the outgrowth catch that offers a plan file when an
  entry visibly outgrows its slot. This skill owns the plan file itself.
- **`brainstorming_skill.md` / `exploration_branch_skill.md`** — their
  close-side hand-offs offer a plan file when what resolved is a workstream;
  the offer routes here.
- **`finish_session_skill.md`** — the plan's close-side writes (sketch and
  step table back into the plan, position refresh on the lookup surfaces) ride
  the standard session close via the `project_tracker_skill.md` close-out it
  invokes at Step 3.
- **`skills/BLIND_SESSION.md`** — scoped mode's companion asset; ships with
  this skill.

## Key rules

- **Every plan carries a sketch; every re-entry opens with "we are here."**
  Sketch first, work second, always — both modes.
- **Sketch before plan.** The proposed sketch is presented and the user reacts
  before the plan file is written; in scoped mode this is a hard gate (no
  approved sketch, no prompts).
- **Lookup surfaces carry pointer + one-line position, never a copy.** The
  plan file is the single authoritative copy of the step structure.
- **Ties go to plain, and inside scoped mode, to open.** Scoping is bought
  only when contamination or parallel isolation matters; and once bought, ties
  on scope go to *narrower* — a file can be licensed later by a revised
  prompt, but not unseen.
- **Exclusions before anything else.** A read-scope instruction that arrives
  after the session has started reading is worthless.
- **Blind sessions never open CLAUDE.md, STATUS.md, or the plan.** The plan
  describes the other steps — exactly the contamination being avoided.
- **Only coordinating sessions update the plan.** Blind sessions leave
  reports; the coordinator sweeps them.
- **Prompts live in the plan, verbatim.** A prompt that exists only in
  yesterday's chat is lost by Thursday. (A standalone blind step, which has
  no plan, files its prompt in `workspace/step_prompts/` instead — see
  "Blind steps without a plan.")
- **A count carries its boundary calls.** Any step whose output is a count or
  a classification states the unit of count and records every judgment call
  that moves the number as a named call with its alternative count — never
  absorbed into the number. This binds whether or not anything will ever be
  checked against it: a count with its boundary calls visible is a different
  and better artifact than a count without them.

## Edge cases

- **Outcome-dependent next step (scoped).** S4's reading list depends on what
  S3 finds → never chain S3→S4; S3's prompt ends at the report, and S4 is cut
  at the next coordinating session with S3's report in hand.
- **A blind step that finishes trivially.** The report can be three lines.
  Write it anyway — the Report log is how the coordinator trusts the step
  table.
- **Mid-flight plan revision.** Reality diverges from the plan (a step splits,
  a dependency appears): revise, re-render the sketch for approval, and — in
  scoped mode — re-cut only the affected prompts at a coordinating session,
  noting the revision in the plan header. Prompts already executed are not
  rewritten.
- **A step that outgrows the workstream.** If a "step" turns out to be a
  workstream of its own (its own artifacts, sequence, open decisions), give it
  its own plan file and let the parent plan's step point at it — plans nest by
  pointer, never by copying state upward.
- **Blind sessions cannot be physically walled — either environment.** On
  claude.ai web the connector may fetch whole files; at Cowork the session
  could read any file on disk. The barrier is the same in both:
  `skills/BLIND_SESSION.md` contains nothing to leak, the prompt's exclusion
  list does the rest, and the discipline instruction binds — listed files
  only.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
