# claude_researcher Bootstrap — Thin Slice Test

**Audience:** a Claude session running in a fresh chat on claude.ai. The user has just pasted the bootstrap prompt, which directed you to fetch and follow this file.

**This is a test, not the real bootstrap.** Do **not** create any GitHub repos, write any files, modify any Settings, or take any action beyond what is explicitly listed below. The point is to validate that the orchestration-via-fetched-doc pattern works on claude.ai before the full bootstrap is written. After this test, this file will be replaced with the production bootstrap.

If anything in this file feels like it should require a confirmation prompt to the user — pause and surface that to the user, then continue. Capture friction in the result block at the end. The whole point is to learn where friction appears.

---

## Step 1 — Acknowledge fetch

Tell the user, in 1–2 sentences, that you have successfully fetched and read this thin-slice bootstrap from `raw.githubusercontent.com`. Note any friction in the fetch itself (e.g., did the sandbox block it, did you need a different fetch tool, did the content arrive verbatim or summarized).

## Step 2 — Brief interview (chat only, no API calls)

Ask the user the following questions, **one at a time**, waiting for each answer before moving to the next:

1. *"What's your name?"*
2. *"What's your current role or research domain — in one sentence?"*
3. *"On a 3-tier scale, how would you describe your git fluency — novice, occasional, or fluent?"*

After all three answers, summarize back what they told you in 2–3 sentences. This is purely a chat interaction — do not write anything to GitHub or to any file.

## Step 3 — Chained fetch (verification)

Fetch this second URL and briefly describe (1–2 sentences) what kind of document it is:

`https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/ATTRIBUTION.md`

This step tests whether you will follow a fetch-and-read instruction encoded *inside* the bootstrap file (rather than typed by the user). Note any friction (re-prompts, refusals, summarization).

## Step 4 — Report

Print the following result block to the user, filling in the bracketed fields. Use exact field names so the result is machine-parseable:

```
THIN_SLICE_RESULT
- all_steps_completed: <yes | no>
- consent_reprompts_during_run: <none | list them with which step>
- fetches_blocked_or_summarized: <none | describe>
- user_name: <as reported>
- user_role: <as reported>
- user_git_fluency: <novice | occasional | fluent | other>
- chained_fetch_succeeded: <yes | no>
- chained_fetch_returned_verbatim: <yes | no | unclear>
- friction_worth_flagging: <none | bulleted list>
- model_or_tool_calls_required_user_authorization: <none | list>
```

After printing the result block, **stop**. Do not continue with any further setup actions. Do not ask the user what to do next. The session ends here.

---

**For the developer reviewing the result:** this thin slice is referenced from `docs/convos/20260508_phase1_phase2_initial_build.md` (Phase 3 follow-up). If all four steps complete cleanly with no re-prompts and the chained fetch returned verbatim, the orchestration pattern is validated and the full BOOTSTRAP.md can be written against this design. Any non-`none` field in the result block is design input.
