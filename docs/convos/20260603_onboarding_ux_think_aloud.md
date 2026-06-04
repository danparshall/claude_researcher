# 20260603 — Onboarding UX findings from think-aloud session

**Date:** 2026-06-03
**Branch:** onboarding-ux-cleanup
**Surface:** Claude Code (CLI)

## Summary

Dan ran an in-person think-aloud session with a new user attempting the
`claude_researcher` bootstrap flow end-to-end. This convo captures the raw
feedback dump, organizes it by target file, and records the decisions that
were locked in during the triage conversation that followed. **No file edits
yet** — this is the parking lot before scoping. A plan and execution come
next.

The session is high-signal: the documentation authors cannot un-see their own
assumptions, and the recently-merged `egress-docs-ui-agnostic` PR (#8) — which
was *specifically* a UI clarity pass — still failed at exactly the point a new
user would stub their toe. That alone is worth treating as evidence that
"clarify the egress step" needs a different intervention than further wordsmithing
of the same prose.

## Topics Explored

The dump touched essentially every public-facing surface: README, HUMANS.md,
`template/BOOTSTRAP.md`, and (by implication) `RESEARCHER.md` for the
project-repo-isolation rule. Plus a substantive net-new piece of infrastructure
(a public website) that's been mentioned before but not until now sized as a
tracked task.

### Account/access claims (README front matter)

- **Setup time:** 15 min → 10 min. (BOOTSTRAP Step 0 currently says "~5 min if
  network is already set up, ~15 min if first-time" — needs update too.)
- **Account tiers:** README currently says "Claude.ai Pro or Team account" —
  confirmed correct. GitHub free tier is fine for everything. Phrasing should
  be explicit: "Claude.ai Pro (or Team) + a GitHub account (free tier is
  fine)."
- **New privacy one-liner up top:** *"goal is to get everything set up so only
  you can access it; we never see or use your data"*

### Framing

- Up-front explainer for the bootstrap prompt: *"This tells Claude how to set
  up a workflow so that you can get back to thinking"*
- Drop "Nori" from intro entirely (currently README line 3 + HUMANS line 27).
  The brand reference is jargon at the moment of first contact; it can survive
  deeper in HUMANS.md as historical context.
- Prompt block needs a **header/label** ("The prompt:" or similar) so it
  reads as a thing to copy, not as continuous prose.
- Clarify: *the prompt doesn't need to be read, but you can.*

### Terminology cleanup

The think-alouder tripped on a recurring pattern of developer jargon that has
no analog in the academic user's vocabulary.

**Drop from user-facing copy:**
- "orchestration"
- "fork" (it's a brand-new repo creation, not a fork — the BOOTSTRAP doesn't
  actually fork anything; the term is leakage from the GitHub mental model)
- "repo" (in narrative; "GitHub project" or just "project" works)
- "shell commands"
- "my VM" (BOOTSTRAP Step 1 leans hard on this — "the user needs to understand
  that bash runs in a virtual machine Anthropic spins up" — the user just
  needs to know "Claude needs internet access for this")
- "egress" (in narrative — but it's the literal claude.ai Settings UI label,
  so the *configuration step* still has to use the term, even as the narrative
  routes around it)

**Handle carefully:**
- **"token"** — in the audience's vocabulary, "tokens" means *things Anthropic
  charges you for*. The GitHub PAT is something else entirely. Frame the PAT
  as "the password Claude uses to talk to GitHub on your behalf" or similar;
  avoid leading with the word "token" until it's been disambiguated.

**Drop entirely from the bootstrap interview:**
- **Paper-naming conventions** (BOOTSTRAP Step 4 Batch 3). Currently a major
  sub-section with two formats (academic + institutional), camelCase rules,
  SurnameF disambiguation, etc. — load-bearing if the user is doing literature
  work, irrelevant for everyone else, and a *lot* of cognitive load to absorb
  during setup. Removing it from the interview doesn't mean removing it from
  the system — `add-paper` can ask at use-time if it isn't set, or default to
  something sensible.

### README vs Claude-facing split

- README should be **very short, humans-only**.
- "Most content moves out of README into BOOTSTRAP." Bootstrap prompt block
  stays in README (the user needs a copy-pasteable thing to start with), but
  the "What's in this repo" / "About" / "Developer info" prose largely moves
  out. The README becomes: *what this is, the privacy one-liner, the prompt,
  pointer to HUMANS.md for everything else.*

### Project = repo + NDA/IP isolation rule

- User-facing: explain the **claude.ai "Project"** concept — one Project per
  research project, with its own repo. Distinguish from "GitHub project"
  (deprecated nuance) and from the generic word.
- **Claude-facing rule lands in `RESEARCHER.md`:** project ≡ repo, do not let
  data or code cross between them. Motivated by NDA/IP concerns —
  cross-contamination between, say, a confidential consulting project and a
  public-policy research project is a real risk. The instruction should be
  explicit enough that even when the user asks "remind me what we worked on
  for ClientX," the agent doesn't auto-bridge into a different repo's context.

### BOOTSTRAP §1 — Egress

The fresh user hit friction here despite PR #8's specifically-targeted UI-
agnostic rewrite. Dan's read: the *prose* clarification isn't enough; the step
needs **screenshots** and a stronger default.

- Need screenshot(s) of the claude.ai network egress UI variants.
- "Flip switch to enable egress, then set from dropdown." — i.e., name the
  two-step shape of the interaction explicitly, not just "find and turn on."
- Domain allow-list: copy each, click `+` (the UI mechanics matter).
- **Push allow-all as the default:** *"easiest to just allow all... it's not
  the user's computer!"* The current Step 1b text mentions "pick the broadest
  option for now," but mealy-mouths it; lead with allow-all, and frame the
  allow-list as "if you have a corporate-style preference for tighter scoping,
  here's the minimum set."
- **New affordance:** after the bootstrap completes, set up a task reminder
  (either in Claude itself via memory, or in `basic_config`) to revisit egress
  settings after a week. This honors the privacy posture without blocking the
  user's first session on perfect configuration. *Open question:* where the
  reminder lives — Claude memory is more discoverable per-chat but less
  persistent; `basic_config` is durable but the user has to actually look at
  it. Could plausibly do both.

### BOOTSTRAP §2b — PAT

Currently the PAT section spends ~30 lines explaining each GitHub permission
in detail (Administration, Contents, Metadata, etc.). The think-alouder
glazed. Dan's rewrite intent:

> "Explain to user that they don't need to understand any of this. They are
> just setting up their GitHub account so that Claude can talk to GitHub on
> their behalf. (But happy to explain in detail if you want.)"

I.e., the section becomes:
- **What this is, in one sentence:** the credentials Claude uses to make a
  repo for you and read/write files there.
- **Action:** follow these steps (linked or in-band, but compact).
- **Affordance:** "Want the details on what each permission means? Ask me." —
  this is *Claude's* line, not just a doc line. The agent should offer to
  expand on demand but not front-load it.

Plus the smaller copy-edits from the dump:
- Explain "repo-scoped" the first time it appears
- "Configure" → "use these values" (more imperative, less abstract)
- Screenshots: the GH Settings configure page, the "Add permissions" button,
  the read → read-write flip
- "Click `Add permissions`" — name the button explicitly
- "Then enable categories, change from read to RW"

Plus a meta-instruction *to Claude* (probably lands in RESEARCHER.md, not
BOOTSTRAP.md): **calibrate git-explanation depth to the user's git fluency.**
The current `<GIT_FLUENCY>` field exists for this; the agent isn't
consistently using it as a dial. The PAT-section affordance ("happy to
explain") is the canonical example — fluent users want it skipped, novices
want it expanded.

### Screenshots — cross-cutting

No screenshots anywhere in the repo currently. Need at minimum:
- claude.ai Settings → network egress (with the toggle + the dropdown if
  visible)
- GitHub Settings → fine-grained PAT create form
- GitHub Settings → PAT "Add permissions" button
- GitHub Settings → a permission toggled from read-only to read-write

**Open question:** where these live. Options: (a) `template/reference/
screenshots/` directory referenced inline in BOOTSTRAP.md, (b) a new
`docs/reference/screenshots/` location, (c) inline at the file level. The
BOOTSTRAP.md currently has no images at all; the repo has no `screenshots/`
anywhere.

### HUMANS.md additions

A new paragraph reassuring the user that the workflow is durable:

> "You don't want to care about prompts and config files; now you don't have
> to. But it's all yours, and you CAN update whenever you decide you're
> ready. Also every change is recorded and saved, so it's almost impossible
> to screw anything up permanently."

This sits naturally either in the existing "What this is" / "Where this comes
from" framing block, or as a new "Don't worry about the machinery" section.

## Decisions Made

These were locked in during the triage conversation following the dump:

- **`repin-tooling` PR'd and merged first** — kept separate from the UX work
  so its narrow scope stays clean. PR #10, merged with a real merge commit
  (the SHA-pin reachability constraint required it).
- **Claude.ai = Pro/Team. GitHub = free tier is fine.** README phrasing should
  be explicit about both.
- **Most content moves from README into BOOTSTRAP.** README becomes a thin
  human-facing entry point; the bootstrap prompt block stays, the
  developer-facing detail leaves.
- **Project-repo isolation rule lands in `RESEARCHER.md`** (universal Claude
  rule), not in `personal_info.md` or Project Instructions.
- **Allow-all is the egress default.** Pair with a "revisit after a week"
  reminder set during bootstrap. Mechanism for the reminder is open (Claude
  memory vs `basic_config`); could plausibly do both.
- **PAT section becomes "you don't need to understand this, ask me if you
  do."** Affordance-based, not didactic.
- **Drop paper-naming from the bootstrap interview entirely.** Move to
  use-time prompting in `add-paper` or set a sensible default; do not block
  setup on it.
- **All UX work lands on `onboarding-ux-cleanup` branch**, not on
  `repin-tooling`.
- **Public website is real, separate scope.** A GH issue is being filed
  alongside this convo (see "Captured Tasks" below) to track the work — the
  hoi-polloi audience reads a website, not GitHub.

## Resolutions (2026-06-03 follow-up)

The six open questions above were closed in a follow-up triage with Dan.

- **Screenshot location → `template/reference/screenshots/`**, referenced from
  BOOTSTRAP.md by path. Ships with the bootstrap material the agent fetches.
- **Reminder mechanism (egress revisit) — durable file in `basic_config`.**
  Recommendation: a `basic_config/reminders.md` (or `STATUS.md`-style
  parking-lot section) carrying revisit-by dates per item; `RESEARCHER.md`
  tells the agent at session start to check the file and surface anything
  past its revisit date. **Not claude.ai memory.** The web-UI memory surface,
  as far as I know, is static text the agent loads — it has no scheduled-task
  / time-based recall primitive, so building on it would either drift silently
  or require the agent to re-derive "is it time yet?" from chat date, which
  is fragile. The durable-file approach matches the same logic that put
  `personal_info.md` in `basic_config` (user-readable, user-editable,
  version-controlled, cross-Project). *Pending Dan's confirmation that the
  claude.ai-memory option is genuinely off the table — if he wants to verify
  the web UI's reminder affordances before locking, that's the right move.*
- **Paper-naming relocation → option (a), filed as a separate task issue.**
  First time `add-paper` runs in a repo with no `paper_naming.*` set in
  `personal_info.md`, the skill asks how the user wants to name papers,
  explains the default if they don't care, and persists the answer. Drop the
  question from the bootstrap interview entirely.
- **PAT-section affordance — bootstrap-only, not RESEARCHER.md.** The
  "happy to explain in detail if you want" line lives in BOOTSTRAP.md
  Step 2b. Setup is the only context where it fires; subsequent sessions
  don't touch PATs.
- **Git-fluency elicitation — replace tier-dial question with concept-check.**
  Instead of "Git fluency — pick one: novice / occasional / fluent," ask:
  *"the program used to track all changes in the project is called 'git' —
  are you familiar with it?"* This drops the loaded word "fluency" (which
  pre-supposes a scale the user may not know), introduces the concept first,
  and probes laterally. The tier classification probably still happens
  internally so downstream skills can read it, but the elicitation is
  natural-language rather than menu-driven.
- **Sequencing locked.** Prose pass + RESEARCHER.md rules first (text-only,
  cheap, reviewable); screenshots second; website third (separate scope,
  tracked at issue #11).

### Across-the-board addition to the interview

Each batch of interview questions ends with:

> "It's okay if you don't want to answer right now, and remember you can
> always ask me for explanations."

Lowers the cost of "I don't know" responses, signals the calibration
affordance up front, and reinforces the "ask me to explain" framing that
the PAT section uses too.

## Results

No analysis artifacts — this is the parking lot. The next session against
this branch should produce an implementation plan (`docs/plans/08_<slug>.md`
or similar) that turns these decisions into ordered tasks.

## Captured Tasks

- [#11: Create public website — non-dev companion to the GitHub repo](https://github.com/danparshall/claude_researcher/issues/11) — captured 2026-06-03
- [#12: add-paper: ask naming convention on first save (drop from bootstrap)](https://github.com/danparshall/claude_researcher/issues/12) — captured 2026-06-03
