---
name: write-a-plan
description: Use when a research conversation has produced something ready to implement — creates implementation plans that reference their originating conversation, carry epistemic context, and assume the implementing agent has zero codebase context
---

`{{skills_dir}}` is `~/.claude/skills` on Claude Code and `/home/claude/.claude_researcher_template/template/skills` in the claude.ai sandbox.
Sandbox-specific notes (REST for Issues/Pulls, the post-commit push hook) are in RESEARCHER.md.

<required>
*CRITICAL* Add the following steps to your task tracker: TaskCreate (claude), update_plan (codex), etc.

- Read the 'Guidelines'.
- **Check for a convo file.** Look in `docs/active/<branch>/convos/` for this session's convo file.
  - If it exists: use it as the originating conversation.
  - If it doesn't exist: "We don't have a conversation summary for this session yet. Let me create one before the plan, so the plan can reference its reasoning." Run `{{skills_dir}}/update-docs/SKILL.md` first, then continue.
- Create a plan that a senior engineer can follow, with full provenance.
<system-reminder>Any absolute paths in your plan MUST take into account any worktrees that may have been created</system-reminder>
- Think about backwards compatibility. Add any notes to the plan.
- Think about edge cases. Add them to the plan.
- Think about questions or areas that require clarity. Add them to the plan.
<system-reminder> Questions are an opportunity to validate assumptions. Be aggressive. Ask questions even of things that you already feel confidence about. Aim for at least 3. </system-reminder>
- Emphasize how you will test your plan.
- Present plan to user.
</required>

# Guidelines

## Overview

Create implementation plans for engineers who have zero context for the codebase. Document which files to touch, what to test, what docs to check. Give them bite-sized tasks. DRY. YAGNI.

Assume the implementing engineer is talented but knows almost nothing about the toolset or problem domain.

Do not add code, but include enough detail that the necessary code is obvious.

Do not write a file to disk unless explicitly asked.

## Key Difference from Generic Plans

**Plans come from research conversations.** They are proposals based on current understanding, not settled specifications. The implementing engineer needs to know:
- What conversation/research produced this plan
- What the current confidence level is
- What might change if we learn more

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

**Goal:** [One sentence describing what this builds]

**Originating conversation:** [link to docs/active/branch/convos/YYYYMMDD_name.md]

**Context:** [2-3 sentences about WHY we're doing this — what research finding or hypothesis motivated it]

**Confidence:** [How settled is this direction? E.g., "High — consistent finding across 3 pilot runs" or "Exploratory — testing whether this approach works at all"]

**Architecture:** [2-3 sentences about approach]

**Branch:** [Which branch to implement on]

**Tech Stack:** [Key technologies/libraries]

---
```

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**

- "Write the failing test for `behavior`" - step
- "Write the failing test for `other behavior`"
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Test Section

Every plan that involves code MUST have a test section. This should be written first, and should document how you plan to test the *behavior*.

```markdown

**Testing Plan**

I will add an integration test that ensures foo behaves like blah. The
integration test will mock A/B/C. The test will then call function/cli/etc.

I will add a unit test that ensures baz behaves like qux...
```

You should end EVERY testing plan section by writing:

```markdown
NOTE: I will write *all* tests before I add any implementation behavior.
```

<system-reminder>Your tests should NOT contain tests for datastructures or
types. Your tests should NOT simply test mocks. Always test actual behavior.</system-reminder>

<required>
For each test, follow this checklist:
- Ensure that the test does not just test mocks. If it does, remove the test and try again.
- Ensure the test does not test implementation detail. If it does, rewrite the test so that it tests boundary behavior.
- Ensure the test does not test data structure format or types. If it does, remove the test and try again.
- Ensure the test does not test for removed behavior. For example, if some behavior has been deprecated, do not write a test that simply confirms the behavior no longer works.
- Evaluate if the test treats the interior of the test boundary as a blackbox. You should not know anything about interior variables, function calls, or control flow.
</required>

**Exception:** Pure analysis or exploration tasks (e.g., "run this classification on 50 occupations and see what happens") do not need TDD. They need a clear description of what to run, what outputs to check, and what constitutes a surprising result.

## Plan Document Footer

**Every plan MUST end with this footer:**

```markdown
**Testing Details** [Brief description of what tests are being added and how they specifically test BEHAVIOR and NOT just implementation]

**Implementation Details** [maximum 10 bullets about key details]

**What could change:** [Things that might shift if ongoing research produces different findings — helps the implementing agent know what's provisional]

**Questions** [any questions or concerns that may be relevant that need answers]

---
```
