# STATUS — [Repo Name]

*Last updated: YYYY-MM-DD — reviewed*

<!--
  STATUS.md is the repo's resume file: read at session start on the user's "yes", rewritten at
  every close (skills/project_tracker_skill.md owns the protocol, the three header flags
  included; skills/finish_session_skill.md Step 3 invokes it). It holds what is open and
  nothing finished: a closed record rotates to STATUS_ARCHIVE.md, verbatim, at the close that
  closes it. The header line is date and flag only, rewritten in place, never a `Prior:` stack;
  a propagation's record is the repo's skills/CHANGELOG.md entry and the Last curated line.
  Sections are the slots: the kit owns the form (headings, order, these comments, the fixed
  lines) and Part C's conformance pass rebuilds it in template order at every propagation,
  keeping every entry in its section; a section this repo adds is asked about at the pass.
  A collaborator's session rewrites its own workstream's entry only, on its branch.
-->

Closed records rotate to `STATUS_ARCHIVE.md` (born at the first rotation). Cite entries by
section and name, never by line number. Where the project stands at the big-picture level is
`RECORD.md` (born at its first row).

## Current state

<!--
  One entry per workstream, named by its folder — a research line, a NONE repo's skeleton
  folder — plus `general` (the shared spine, where the archetype has one), `funding/`
  (research) and `repo` (infrastructure), in the root FOLDER_MAP.md's order. A workstream
  with no unit in the list takes the name of the folder its work sits in (a root product
  takes the product's stem) — the list names the usual units, never all
  of them. Fields, fixed: where it stands as of a date · Next · Waits on ·
  Resume (the carryover, plan file or unseen-close transcript, only when one exists; the
  `repo` entry's names the conformance items file while one stands in the carryover home).
  Rewritten in place at every close that touched the workstream, never appended: a session's
  narrative is not state. An entry that outgrows a few lines gets a plan file and keeps a
  one-line position (skills/workstream_plan_skill.md). Deferred Claude actions go in the
  Next field; actions waiting on the user are queue rows in workdesk/INDEX.md, pointed at,
  never copied. A closed workstream's entry becomes its close line and rotates.
  Protocol: skills/project_tracker_skill.md, "Current state".
-->

- **[workstream folder]** (as of YYYY-MM-DD) — [where it stands]. Next: [the next move, or
  "none until <event>"]. Waits on: [the user | a named person | data | nothing]. Resume: [the
  carryover, plan file or transcript, when one exists; otherwise omit the field].
- **general** (as of YYYY-MM-DD) — [the spine: intake, library, notes]. Next: [...].
- **repo** (as of YYYY-MM-DD) — [infrastructure and kit state beyond the block below].
  Next: [...].

### Pending re-integrations

<!--
  Chapter files whose section files changed after assembly (hierarchical naming); `(none)`
  otherwise. skills/project_tracker_skill.md, "The Pending re-integrations subsection".
-->

(none)

### Pending placement fixes

<!--
  Deferred folder moves and staged files awaiting a home, written by CLAUDE.md's placement
  check and the intake funnel, never by hand; `(none)` otherwise.
  skills/project_tracker_skill.md, "The Pending placement fixes subsection".
-->

(none)

### Index audit

<!--
  Stamped by the index audit's closing commit, read by the close-out cadence check;
  `(never)` until the first run. skills/project_tracker_skill.md, "Index-audit cadence read".
-->

Index audit last run: (never)

## Open questions

<!--
  Decisions to resolve, one named entry each, dated. A question closes at the close that
  answers it and rotates with its answer. An action waiting on the user is a queue row
  (workdesk/INDEX.md), not a question. A question about a kit file also logs its
  [SKILL-FEEDBACK] entry in skills/CHANGELOG.md in the same commit and points at it; once a
  propagation has cleared the entry, the pointer names the kit record instead.
-->

- **[Question name]** (YYYY-MM-DD) — [the question, with the context needed to decide it].

## Known issues

<!--
  What broke and the workaround, while the issue is live; a fixed issue rotates. An issue in
  a kit file also logs its [SKILL-FEEDBACK] entry in skills/CHANGELOG.md in the same commit
  and points at it ("logged as [SKILL-FEEDBACK] <date>"); the issue stays here for the workaround,
  and a pointer at an entry a propagation has cleared is rewritten to the kit record at the pass.
-->

- **[Issue name]** (YYYY-MM-DD) — [what broke, how it was diagnosed, the workaround].

## Cluster activations (current)

<!--
  Kit-owned: written by skills/skills_curation_skill.md Step 7 at every propagation (Parts A,
  B and C of skills/PROJECT_SETUP.md), never by hand; the archetype and the module set are
  in CLAUDE.md's frontmatter. The Last curated line is rewritten in place, never stacked.
  Initial-template state is "unknown"; the first curation sets the values. A cluster
  active with a member declined reads "active, less <file> (<reason>, <date>)": this
  block is the one home of that choice, read by the audit's Check 10 and by the pass.
-->

- Source material: unknown
- Writing and deliverables: unknown
- Voice and style: unknown
- Final-production formats:
  - Academic paper LaTeX: unknown
  - Academic slides: unknown
  - Deck reconciliation: unknown
  - <any format-pair you have added>: unknown

Last curated: not yet curated

---
<!-- Kit file marker below: the template's own version line, not part of the repo file. -->
*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
