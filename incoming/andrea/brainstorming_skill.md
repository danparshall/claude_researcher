---
name: brainstorming
description: "Structured-questioning discipline for refining rough ideas before producing concrete output. Runs upstream of drafting, planning, or deciding — its job is to clarify the question, not produce the answer. Two phases: Phase 1 — Understanding (one-question-at-a-time elicitation of purpose, constraints, success criteria; prefers multiple-choice questions); Phase 2 — Exploration (2–3 genuinely different alternatives with trade-offs, no recommendation). Does NOT produce the deliverable itself — once the brainstorm resolves, drafting skills pick up. Optional save step at the end produces a structured summary, distinct from saving the whole conversation (that's repo_conversations_skill.md)."
triggers: >-
  "let's brainstorm," "I want to think through X," "help me refine this idea"; a vague task
  where the right deliverable is not obvious yet
---

# Brainstorming Skill

This skill defines a structured-questioning discipline for refining rough ideas before producing concrete output. It runs **upstream of** drafting, planning, or deciding — its job is to make sure the thing being produced is the right thing, not to produce it.

The skill is useful when the user has an idea, framing, or problem that is not yet fully formed: a paper hypothesis that needs sharpening, a talking-points angle that hasn't settled, a request from a colleague or a manager where the right response isn't obvious, a choice between two approaches with no clear winner. The goal is to make the user's own reasoning visible to themselves through structured questions, not to produce answers Claude generates from its own priors.

**What this skill is, and what it is not.** This skill is a *thinking aid*. It produces clarity, alternatives, and (optionally) a saved record of the thinking. It does **not** produce the deliverable itself — when the brainstorm resolves into "we should draft a policy note about X," the brainstorm ends and `writing_skill.md` Protocol 2 (or another appropriate skill) picks up.

It also does not duplicate `repo_conversations_skill.md`. That skill saves whole conversations as chronological transcripts for retrieval. This skill, if saving is requested, produces a structured summary — the distilled product of the brainstorm, not the back-and-forth. The two are complementary; either or both can be invoked for a given session.

---

## When to use this skill

Read this skill when:
- The user says "let's brainstorm," "I want to think through X," "help me refine this idea," "I'm not sure how to approach this," "I have a rough idea, let me think out loud."
- Claude detects a "rough idea" framing — a task that's vague, has multiple possible directions, or where the user hasn't yet decided what they actually want to produce — and offers to apply the brainstorming discipline before any concrete deliverable.

Do not use this skill for:
- Concrete deliverables with a clear spec (drafting a known email, processing a known paper, formatting a known document — those have their own skills).
- Tasks where the user has already decided what to do and wants execution, not exploration.

If the right mode is ambiguous, ask the user once before starting.

---

## The two phases

`claude_researcher`'s upstream version has five phases including code-implementation infrastructure (git worktrees, implementation planning hand-off). This skill ports only the two phases that generalize beyond code work. The later phases live as a note at the end of this file for when the kit gains a code-implementation planning skill.

**One reactable unit per turn (governs both phases).** Every turn emits exactly one thing for the user to react to — one question, one observation, or one set of alternatives — then stops and waits. Never queue the next unit, append a recommendation, or stack follow-up reasoning in the same turn. The user's reaction is a decision, and anything placed after the unit goes stale the moment they start reading it. Stopping early is never the error; packing a turn is.

### Phase 1 — Understanding

Goal: get the user's purpose, constraints, and success criteria clearly enough that Phase 2's alternatives are actually answering their question, not Claude's interpretation of it.

Discipline:
- **The question is the whole turn.** Ask one question and stop — do not preview the next question, bundle reasoning that pre-empts the answer, or signal where the line of questioning is heading. A question that arrives with its own framing is no longer eliciting the user's reasoning, it's steering it — which is the exact bias Phase 1 exists to avoid.
- **Prefer multiple-choice when possible.** "Is this paper aimed at (a) academic audience, (b) policy audience, (c) internal to your unit?" beats "who is this paper for?" The structure surfaces the choices the user is making.
- **Gather purpose, constraints, success criteria.** What is this for? What can't change? How will the user know it worked?
- **Don't infer.** If a question would have an obvious-seeming answer, ask anyway — the obvious answer is sometimes wrong, and asking is cheap.
- **Stop when the picture is clear, not when a fixed number of questions has been asked.** Some brainstorms need three questions, some need ten. Stop when the user's purpose, constraints, and success criteria are clear enough to generate meaningfully different alternatives.

End-of-phase signal: Claude has enough to propose alternatives, or the user says "I have what I need, let's move on."

**The transition is its own turn.** When the picture seems clear enough to move to alternatives, say so and stop — "I think I have enough to lay out approaches; ready for me to?" — rather than rolling into Phase 2 in the same turn. The judgment that Phase 1 is done is itself a thing for the user to confirm: they may have a constraint not yet surfaced, or want to stay in questioning. Generating alternatives off an unconfirmed picture is how the brainstorm produces answers to the wrong question.

### Phase 2 — Exploration

Goal: surface 2–3 genuinely different approaches the user could take, with trade-offs, so they can choose with the alternatives visible.

Discipline:
- **2–3 alternatives, not a list of variations on one approach.** If all three "alternatives" differ only in tone or in one parameter, they're not really alternatives — they're a single approach with knobs.
- **Per alternative: core idea, what it would look like in practice, trade-offs.** Trade-offs is the load-bearing part — what does this approach give up?
- **Don't recommend; surface.** The user decides. The skill's job is to make the choice visible, not to push a winner.
- **Loop back to Phase 1 when needed.** If during Phase 2 the user reveals a constraint that wasn't surfaced earlier ("oh, this has to fit in 800 words"), return to Phase 1 to absorb it before the alternatives shift accordingly. Linearity is not the goal — clarity is.
- **The alternatives end the turn.** Present the 2–3 alternatives and stop — do not append a recommendation, a lean, a next step, or follow-up questions. The alternatives are a reactable unit and the user's pick is a decision; anything queued after them goes stale the moment they start choosing. "Don't recommend; surface" is not only about withholding a winner, it's about not burying the choice under what comes after it.

End-of-phase signal: the user picks one of the alternatives, asks for a modification, or says "let me think about it" / "I have what I need."

---

## End of the brainstorm: save prompt

The brainstorm ends when one of two things happens:

1. **The user signals completion.** "OK, I think I have my answer," "good, let's move on," "let's draft it now," or similar.
2. **The conversation shifts into actual work that uses the brainstorm's output.** The user moves from exploring to executing — e.g., "let's draft the policy note now," "OK, start writing." Claude pauses **once** before starting the new task to ask the save question.

At this end-of-brainstorm moment, Claude asks: **"Do you want to save this brainstorm?"**

- If **no:** brainstorm ends, nothing is saved, Claude proceeds to whatever the user wants next.
- If **yes:** Claude produces the save artifact (format below) and asks the user where to save it.

The save prompt fires once per session. If the user says no and later changes their mind, they can ask to save explicitly.

---

## Save format

A structured summary, not a transcript. Roughly half a page. Saved as a markdown file with a date-prefixed name.

Filename: `YYYY-MM-DD_<topic>.md` (e.g., `2026-05-13_partner_request_framing.md`), the form the folder's catalog names (`standing_documents_template.md`).

Location: `workspace/brainstorms/`, the universal home (created up front); its catalog (`standing_documents_template.md`) gets the row at the close-out's refresh.

Format:

```markdown
# Brainstorm: [topic]

**Date:** [YYYY-MM-DD]
**Session context:** [one-line description of what triggered the brainstorm]

## Question
[The actual question being brainstormed, in the user's words where possible.]

## Constraints surfaced
- [Constraint 1]
- [Constraint 2]
- [...]

## Success criteria
[How the user will know the chosen approach worked.]

## Alternatives considered

### Alternative 1: [Short label]
**Core idea:** [One or two sentences.]
**In practice:** [What this would actually look like.]
**Trade-offs:** [What this approach gives up.]

### Alternative 2: [Short label]
[Same structure]

### Alternative 3: [Short label]
[Same structure, if a third alternative was explored]

## What the user landed on
[The chosen approach, or "still open" if no decision was made.]

## Why
[the user's reasoning, in their own words where possible.]

## What's still open
- [Loose end 1]
- [Loose end 2]

## Next action
[What happens after this brainstorm — usually a hand-off to a drafting/processing skill, or a follow-up brainstorm.]
```

Sections can be omitted if they don't apply (e.g., no "What's still open" if everything resolved). The format is a guide, not a contract.

---

## Hand-off to other skills

The brainstorm ends; the next thing starts. Common hand-offs:

- **To `writing_skill.md` Protocol 2.** When the brainstorm has produced a rough outline or framing for a draft, Protocol 2 picks up: branch creation, outline refinement, drafting in units. The brainstorm's "alternatives considered" and "the user landed on X" supply the framing that Protocol 2 builds on.
- **To `materials_processing_skill.md` or `document_processing_skill.md`.** When the brainstorm clarified what to do with a source document (process it as a paper vs. as a document? include or exclude from the index?), the relevant pipeline runs next.
- **To `workstream_plan_skill.md`.** When what the brainstorm resolved into is not one deliverable but a **workstream** — multi-artifact work with its own sequence and open decisions — offer the plan file: "this looks like a workstream — open a `<stem>_PLAN.md` for it?" On the user's yes, that skill runs (sketch first; plain mode by default). Offer, don't open — and per the turn discipline, the offer ends the turn.

### The exploration triage (when the brainstorm resolved into an offshoot)

Most brainstorms resolve into a primary deliverable, and the hand-offs above apply. But a brainstorm can instead resolve into an *offshoot* — a side investigation, not the main thing: "let me check whether that result is robust," "what if we ran the alternative specification," "there's a side case worth working up." When the outcome is an offshoot rather than a primary deliverable, run one triage question before handing off:

> **Is this offshoot *testing* whether something on `main` holds, or *adding* to `main`?**

- **Testing** — it puts a `main` claim at risk (a robustness check, an alternative spec, a re-analysis that could move a conclusion). Hand off to **`exploration_branch_skill.md`**: the work belongs on a long-lived, isolated branch so `main` stays truthful while the question is open.
- **Adding** — it is additive by construction and risks no `main` claim (a supplementary descriptive cut, a case study). Hand off to a **folder on `main`** via the folder-creation placement check; no branch.

The triage is by **purpose, not probability**. Whether the offshoot *will* overturn `main` is unknowable at hand-off — not knowing is the whole reason to run it. What is always known is its purpose: is a `main` claim being put at risk, or not? Classifying by purpose isolates the high-cost (overturning) case from the start — testing work is never left sitting on `main` until a bad result lands, and never has to be dug back out of `main` afterward.

This triage is **one reactable unit**: ask the question and stop, per the turn discipline above. The user's answer is the routing decision.

Claude does not auto-invoke the next skill — the user names the next move (or it's named in the brainstorm's "Next action" section). The brainstorming skill's job ends at the hand-off.

---

## Note for future code-project work

`claude_researcher`'s upstream brainstorming skill has two additional phases not ported here: a worktree-setup phase (creates an isolated git workspace) and a planning hand-off phase (switches to a "Writing Plans" skill to produce an implementation plan). Both are code-project infrastructure.

As of v2.1.3, this kit does not include a code-implementation planning skill. When such a skill is added — either by porting `claude_researcher`'s `write-a-plan` skill or by building the user's own — this skill's hand-off section should be extended with a code-project branch:

> **For code projects:** when the brainstorm has produced a design the user wants to implement, the hand-off is to `[implementation-planning skill]` rather than to `writing_skill.md` Protocol 2.

Until that skill exists, this section is a placeholder. The user is the one who would add the code-implementation skill (they're the one who would want to start a code project), so the integration happens when they're ready.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
