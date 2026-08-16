# PreCompact hook probes — empirical results

**Sidecar to:** [`20260813_precompact_update_docs_hook.md`](20260813_precompact_update_docs_hook.md) (session convo; this file is the raw-findings record so the convo doc can stay narrative).
**Context:** [Issue #42](https://github.com/danparshall/claude_researcher/issues/42) — wire PreCompact to auto-run `update-docs` before context compaction.
**Environment:** Claude Code **2.1.233**, macOS (darwin-x64, `Dans-MacBook-Pro`), 2026-08-16. Sacrificial sessions: `claude -p`, model haiku, fresh project dirs under `/tmp/precompact-probes/` (probe designs, hook scripts, and logs preserved there; filler corpus regenerable via seeded `gen_bigfiles.py`). Raw hook logs are NOT vendored into this public repo — PostCompact payloads embed compaction summaries quoting the operator's private CLAUDE.md; redacted excerpts only.

## Probe designs

| Probe | Config | Workload | Question |
|---|---|---|---|
| 1-control | PreCompact command hook, logs stdin, exit 0; `autoCompactWindow: 100000` | 5 filler files ≈150k tok | Does auto-compact fire in print mode? What does PreCompact receive? |
| 1-block | Same but exit 2 | 10 reads ≈300k tok | Is the veto honored? Retry? Wedge? Does the model see the veto? |
| 2 | `{"type":"agent"}` hook on UserPromptSubmit | trivial | Is the undocumented agent-hook schema accepted? What tools does it get? |
| 3/3b | PreCompact `[command, agent]` + PostCompact command | 5 files / 10 paginated | Does the agent hook fire on PreCompact? Does compaction wait? |
| 3c | PreCompact `[agent]` alone | 7 files | Bisect: was 3b's agent-skip caused by being second in the array? |

## Findings

**F1 — Auto-compaction fires in print mode (`claude -p`).** Undocumented. Level progression in debug log: `ok → warn → compact`, then `routing through reactive (thresholdSource=env)`.

**F2 — `autoCompactWindow` / `CLAUDE_CODE_AUTO_COMPACT_WINDOW` works, with a 20% margin.** Setting 100000 yields `effectiveWindow=80000` (debug log). Threshold-crossing is workload-sensitive to within one Read call (probe 3 null: 6 reads stayed under; control's 7 crossed).

**F3 — PreCompact stdin schema (undocumented).** Captured verbatim (values redacted):
```json
{"session_id": "…", "transcript_path": "…/.claude/projects/<slug>/<session>.jsonl",
 "cwd": "…", "prompt_id": "…", "hook_event_name": "PreCompact",
 "trigger": "auto", "custom_instructions": null}
```
The field is `trigger` (not the matcher name); `custom_instructions` exists (presumably `/compact <text>`; manual path untested). `transcript_path` points at the live full-fidelity JSONL → **deterministic pre-loss salvage is possible from a plain command hook.**

**F4 — Compaction WAITS for the PreCompact command hook** (synchronous). Hook dispatch → ~41s summarization turn → PostCompact dispatch, three clean cycles in probe 3b.

**F5 — Blocking auto-compact: retry storm, then silent surrender; model never informed.** Exit-2 veto produced 8 PreCompact fires in 21s (~3s apart, same `prompt_id`), then the harness stopped attempting compaction entirely. Session continued un-compacted to ≈260k tokens (within haiku's true window) and exited 0. The blocked session's model reported earlier context as "FULL ORIGINAL CONTENT" (vs. control's "appears as a SUMMARY") and never saw the hook's stderr marker. **Design consequence: block-and-nudge architectures are dead** — the veto is invisible to the model, and behavior at the true context ceiling with compaction forfeited remains untested (wedge risk).

**F6 — Agent hooks (`{"type":"agent","prompt":"…"}`) work and are near-fully tooled — but NOT on PreCompact.** On UserPromptSubmit the spawned agent executed Write and Bash (artifacts on disk) and inventoried its tools: Bash, Edit, Read, Write, **Skill**, WebFetch, WebSearch, Task*, SendMessage, ListAgents, ToolSearch, MCP tools. On PreCompact the same hook config is **silently skipped** — no dispatch line in the debug log, no error, three compaction cycles with only the sibling command hook running (probe 3b). Probe 3c bisects the only-first-in-array confound; result recorded below.

**F7 — `PostCompact` exists in 2.1.233 and its stdin carries the full `compact_summary`.** Undocumented and design-changing: a plain command hook receives the complete compaction summary text (`<analysis>` + `<summary>` blocks) after every compaction. Deterministic persistence of every compaction summary is therefore free — no model, no agent hook.

**F8 — Compaction is itself a model turn.** The harness injects a "CRITICAL: Respond with TEXT ONLY … `<analysis>`/`<summary>`" instruction into the *session model*; the response becomes the replacement context (and the PostCompact payload). The in-context state is fully available at compaction time — the stock pipeline just discards the distillation after swapping it in.

**F9 — Auto-compact has a thrash-breaker.** "Autocompact is thrashing: the context refilled to the limit within 3 turns of the previous compact, 3 times in a row" → session killed (exit 1). Guards any design that lets context refill fast post-compaction.

**F10 — probe 3c: agent-only hook on PreCompact also silently skipped.** Multiple compaction cycles (thrash-breaker killed the run, as in 3b), artifacts dir empty, debug log shows zero PreCompact dispatch lines (vs. 3b where the command hook logged a dispatch line per cycle). Rules out the only-first-in-array confound. **Conclusion: agent-type hooks are silently ignored on the PreCompact event in CC 2.1.233** — accepted by config, never dispatched, no error anywhere. (Also: 7 sequential ~25k-token reads re-trigger the F9 thrash-breaker even without pagination — any future probe needs interleaved low-token turns.)

## Design implications for #42

1. **Architecture C (block-and-nudge): eliminated** (F5).
2. **Agent-hook-on-PreCompact: eliminated** (F6 + F10) — silently unsupported on this event in 2.1.233. Worth re-probing after CC upgrades (the type is marked experimental; per-event support may expand), but not designable-against today.
3. **The A+B hybrid strengthens into A+B′:**
   - **A (pre-loss salvage):** PreCompact command hook copies/derives from `transcript_path` (F3, F4 — synchronous window confirmed).
   - **B′ (summary capture):** PostCompact command hook persists `compact_summary` to disk (F7) — strictly better than reconstructing from the compacted context.
   - **Trigger (model-side distillation):** SessionStart(`compact`) stdout → instructs the model to run `update-docs` against A's raw salvage + B′'s summary. (Stdout-to-context confirmed by docs; end-to-end untested — next probe.)
4. Threshold knob (F2) makes all of this testable cheaply; thrash-breaker (F9) is the guardrail to respect in any test harness.
