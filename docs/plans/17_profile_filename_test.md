# Plan 17 — Does the profile filename trigger the web permission check?

Branch: `profile-filename-test` (test-only; not for merge as-is). Issue: #79 (profile rename).

## Question

On the web sandbox, the auto-mode permission check refused the §2b read of `personal_info.md` in 4 of 5 attempts on 2026-10-11, mostly as [PII Data Handling] (once [Third-Party Attack]), even after a go-ahead naming the file (`docs/convos/20261011_plan14_web_runs.md`). The check sees the command, so the word "personal" in the URL may be part of the trigger. The 2026-10-10 test that "ruled out" the filename had both names pass, so it had nothing to compare and couldn't tell either way.

Competing explanation: a fetched public repo's instructions (RESEARCHER.md) telling the agent to read private data looks injection-like, whatever the file is called. If so, a rename won't help.

## Setup

- `danparshall/claude_research_config` has `researcher_config.md`, made byte-identical to `personal_info.md` on 2026-10-29 (blob `9adfe38`). Only the name differs.
- This branch replaces every `personal_info.md` mention a web session reads (`template/RESEARCHER.md` and `template/skills/**`, 21 mentions) with `researcher_config.md`, i.e. the rename as it would ship.

## Arms

- **A (control):** Project Instructions as now; the clone gets `main`.
- **B (test):** same Project Instructions with two edits:
  1. Clone line: `git clone --depth 1 --branch profile-filename-test https://github.com/danparshall/claude_researcher.git /home/claude/.claude_researcher_template`
  2. Prose: `personal_info.md` → `researcher_config.md` (two mentions).

## Protocol

- Run 10 fresh sessions, alternating A, B, A, B, … in the same Project, swapping the instructions between runs. Alternating spreads drift in the checker across both arms.
- Same opening message every time, neutral and with no authorization wording: "Start a session and tell me where the work stands."
- Don't type any go-ahead. Record only the first attempt at the profile read.
- Record per run: arm, profile read (ok / refused + label), and any other refusal at startup.

## Reading the result

- B is OK in ≥4 of 5 while A is refused in ≥3 of 5: the filename matters; ship the rename (new name first, fall back to `personal_info.md` for existing users).
- Both arms refused at similar rates: the filename is not the trigger; drop the rename and look at the injection-like explanation.
- Both arms mostly OK: the checker has changed since 2026-10-11; no rename needed for now.
- Five per arm only detects a large effect. A mixed result means more runs, not a decision.

## Results

| Run | Arm | Profile read | Other startup refusals |
|---|---|---|---|
| 1 | A | | |
| 2 | B | | |
| 3 | A | | |
| 4 | B | | |
| 5 | A | | |
| 6 | B | | |
| 7 | A | | |
| 8 | B | | |
| 9 | A | | |
| 10 | B | | |
