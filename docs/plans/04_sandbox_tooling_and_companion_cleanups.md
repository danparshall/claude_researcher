# Plan 04 — Sandbox Tooling Matrix and Companion Cleanups

**Goal:** Empirically verify which document-processing tools (`pypdf`, `pandoc`, `python-docx`) are available in claude.ai's sandbox and write findings to `template/reference/SANDBOX_TOOLING.md`, unblocking Wave 4 / Wave 5 of the skill ports. While there, knock out three small cleanups that surfaced during the 2026-05-11 sessions: terminology sweep on "Custom Instructions" → "Project Instructions", add a `Surface` field to the convo summary template, and extend the §2e convo-name handshake with a human-readable rename suggestion.

**Originating conversation:** [`docs/convos/20260511_clone_first_ship.md`](../convos/20260511_clone_first_ship.md)

**Context:** Two distinct strands converge in this plan. (1) **Sandbox tooling.** STATUS Open Questions has flagged for several sessions that Wave 4 (`branch-document-review`, depends on `pandoc`) and Wave 5 (`document-processing`, may want `python-docx`) need confirmation that the tools are accessible in claude.ai's sandbox before porting effort lands. The 2026-05-09 smoke-test resolved that pip-install works on-the-fly with the "Package Managers Only" egress preset, but each specific package — and the system binary `pandoc` — still needs an actual try. (2) **Companion cleanups.** The 2026-05-11 dogfooding + clone-first ship sessions surfaced three small ergonomic gaps that don't deserve their own plans but should land before more substantive work accumulates on top of them: docs use "Custom Instructions" where the Anthropic UI uses "Project Instructions", convo files don't record which surface (claude.ai vs Claude Code) they were written from, and the §2e handshake names a file slug but doesn't help the user keep the WebUI chat title aligned with it.

**Confidence:** High on Task 2 (terminology sweep is mechanical). High on Task 3 (adding a frontmatter field is structurally trivial). High on Task 4 (one paragraph edit + example update in RESEARCHER.md §2e). Medium on Task 1 — the failure mode is "tool unavailable + workaround unclear", and we don't fully know the answer for `pandoc` specifically until the smoke test runs. If `pandoc` is unavailable and unfixable, Wave 4's `branch-document-review` port needs a design rethink (use `difflib` instead).

**Architecture:** Task 1 is empirical — a single fresh claude.ai chat runs `pip install` / version-check probes and reports results into a new reference file. Tasks 2–4 are doc edits made via the Contents API, each one PUT per file. Task 4 is the only one that changes runtime behavior (it touches the §2e handshake script that every future session executes).

**Branch:** `main`. This repo is `main_only` (no feature branches per STATUS's critical-note-for-fresh-agents).

**Tech Stack:** Empirical probing with `pip`, `which`, `python -c "import X"`. Markdown editing for the rest. No code added to the repo.

---

## Task 1 — Sandbox Tooling Matrix

### What changes

Open a fresh claude.ai chat. The chat does NOT need Project context; an unattached chat is fine — the goal is to probe the bare sandbox. (Egress should be configured per the standard `domain_allowlist.txt` with "Package Managers Only" preset so `pip install` works on-the-fly.)

Run these probes in order:

```bash
# pypdf — needed for Phase 5 task 31 (add-paper PDF extraction)
pip install pypdf --break-system-packages 2>&1 | tail -3
python3 -c "import pypdf; print('pypdf', pypdf.__version__)"

# pandoc — needed for Wave 4 branch-document-review (regeneration step)
which pandoc
pandoc --version 2>&1 | head -2
# if not present, try installing:
apt-get install -y pandoc 2>&1 | tail -3 || pip install pypandoc --break-system-packages 2>&1 | tail -3

# python-docx — may be wanted for Wave 5 document-processing
pip install python-docx --break-system-packages 2>&1 | tail -3
python3 -c "from docx import Document; print('python-docx OK')"

# Bonus: confirm git is available for the clone-first architecture
which git && git --version
```

For each tool, record:

- **Name + version target**
- **Install command that worked** (or "not installable in current sandbox configuration")
- **Verify command** (the one-liner that confirms it's importable / executable)
- **Status:** `available`, `available after install`, or `unavailable`
- **Wave dependency:** which skills depend on this

Then write findings to `template/reference/SANDBOX_TOOLING.md` using the schema below.

### Output file schema

```markdown
# Sandbox Tooling Matrix

**Last verified:** YYYY-MM-DD by `<USERNAME>` in fresh chat.

This file records which document-processing and analysis tools are available in claude.ai's sandbox, so skill ports can rely on tested capabilities rather than assumed ones. Re-verify quarterly or whenever a port discovers a discrepancy.

## Tools

### pypdf

- **Status:** available after install
- **Install:** `pip install pypdf --break-system-packages`
- **Verify:** `python3 -c "import pypdf; print(pypdf.__version__)"`
- **Wave dependency:** Phase 5 task 31 (`add-paper` PDF text extraction)
- **Notes:** [any quirks observed]

### pandoc

[same structure]

### python-docx

[same structure]

### git

[same structure — confirms the clone-first architecture is on solid ground]

## Workaround table

| If tool is unavailable | Use this instead |
|---|---|
| `pandoc` | `difflib` (stdlib) + manual prose diff |
| `python-docx` | `mammoth` (already in MCP App env per anthropic_api block) for docx → HTML; raw XML fallback for write |
| `pypdf` | `pdfminer.six` as secondary |
```

### Verification plan

1. After the fresh-chat session, confirm `template/reference/SANDBOX_TOOLING.md` exists in the repo with all four tool blocks filled in.
2. Confirm at least one of {pandoc, pypandoc fallback} is `available`-tier — if both are `unavailable`, Wave 4 `branch-document-review` needs a design rethink before its port can be drafted; surface that finding in STATUS Open Questions immediately.
3. Confirm the Wave 4 / Wave 5 entries in `docs/plans/02_skill_ports.md` cite the new reference file for their tool prerequisites.

### What could change

- `pandoc` might be installable via `pip install pypandoc` even if `apt-get` doesn't work (pypandoc bundles the binary). If so, the install command is `pip install pypandoc --break-system-packages` and the verify is `python3 -c "import pypandoc; print(pypandoc.get_pandoc_version())"`. Document whichever path works.
- If the sandbox egress is in "Allow All" rather than "Package Managers Only", more domains are reachable but installs work the same. The egress posture should not affect this matrix.
- If `--break-system-packages` is gone in a future Ubuntu base, switch to `pipx` or a venv. Document the workaround.

---

## Task 2 — Terminology Sweep: "Custom Instructions" → "Project Instructions"

### What changes

The Anthropic UI uses **"Project Instructions"** (project-level) and **"Instructions for Claude"** (user-level). Our docs have been calling the project-level field "Custom Instructions" — wrong term, propagated through several files. The slim `_PROJECT_INSTRUCTIONS.md.template` shipped in Plan 03 commit `b599058` happens not to say "Custom Instructions" anywhere (luck, not design); everything else needs a sweep.

Files to edit and the rule for each:

- **`template/RESEARCHER.md`** — multiple mentions throughout (§2a, §4, §5, §7, the opening paragraph). Replace every "Custom Instructions" with "Project Instructions". This is the most important file because every future session reads it.
- **`template/BOOTSTRAP.md`** — Step 8 area and possibly elsewhere; replace every "Custom Instructions" with "Project Instructions". Update Step 8 prose (whose subject is exactly "what the user pastes into the Project Instructions field") for clarity.
- **`HUMANS.md`** (root) — check for the term; replace if present.
- **`docs/plans/01_initial_build.md`** — many mentions, but most are historical Phase 4 descriptions. **Decision rule:** leave historical phase descriptions (Phase 4 tracker row, "Phase 4: Write `CLAUDE.md`" section body, etc.) intact — they describe what was named/written at the time. Update forward-looking and Open-Questions mentions only. Same principle Plan 03 used for the rename sweep.
- **`docs/plans/02_skill_ports.md`** — likely no occurrences; check anyway.
- **`docs/convos/*.md`** — leave alone (historical record).

### Verification plan

After the sweep, grep the non-historical files for residual "Custom Instructions" mentions. The only ones that should remain are inside historical phase descriptions in `01_initial_build.md` and inside convo files (left intentionally untouched). Anywhere else is a miss.

### What could change

If Anthropic renames "Project Instructions" to something else in a future UI revision, this sweep buys us nothing. Worth noting in the commit message that the term tracks the Anthropic UI specifically and may need re-sweeping later.

---

## Task 3 — Add `Surface` Field to Convo Summary Template

### What changes

Convo files don't currently record which surface (claude.ai WebUI vs. Claude Code) they were written from. The 2026-05-11 dogfooding session is the pivot point — work before that date was mostly or entirely Claude Code; work after is mostly WebUI. The distinction matters for two downstream uses:

1. **The banner-vs-proper-REST empirical question** (now in RESEARCHER.md §8 Parking Lot). Comparing translation success across surfaces requires being able to tell which is which.
2. **HUMANS.md's multi-surface framing** has actual data behind it instead of just narrative.

The change is one line in the convo summary template inside `template/skills/update-docs/SKILL.md`. The template currently has:

```markdown
# [Convo Name]

**Date:** YYYY-MM-DD
**Branch:** branch-name
```

Add a third field:

```markdown
# [Convo Name]

**Date:** YYYY-MM-DD
**Branch:** branch-name
**Surface:** claude.ai | claude-code
```

The agent picks the surface value automatically per the runtime-detection probe already present in `finish-convo/SKILL.md`'s preamble. No user input needed.

Also check `template/skills/finish-convo/SKILL.md` — if it duplicates the template (which it shouldn't, but verify), update there too.

### What about existing convos?

Leave them. The history is the history; back-filling `Surface:` fields into past convos amounts to claims-by-inference about sessions we can't directly observe. Future convos get the field; past convos can be inferred from context (the same way we just did for `20260510_skill_ports_initial_ship` — `~/.claude/skills/` references gave it away).

### Verification plan

After the edit, open the updated `update-docs/SKILL.md` and confirm the template has the three-field frontmatter. The next session's convo file should pick this up automatically when finish-convo runs.

---

## Task 4 — Human-Readable Rename Slug in §2e Handshake

### What changes

Current §2e handshake in RESEARCHER.md proposes a file slug only:

> Example: *"I'll log this session as `20260511_managed_retreat_planning` — sound right?"*

The user has no easy way to keep the WebUI chat title aligned with this slug, so chat-list scrollback and repo convo files drift. WebUI auto-titles like "Plan 3 continuation" or "Help with template files" don't map to anything findable in the repo.

New version of the handshake: propose **both** the file slug (canonical identifier) AND a human-readable rendering of it (presentation layer for the WebUI title field), in a single line.

> Example: *"I'll log this session as `20260511_managed_retreat_planning` (suggested chat title: 'Managed retreat planning' — paste into the chat's title field if you want them to match) — sound right?"*

The file slug stays canonical. The human-readable title is **derived from the slug** by a deterministic rule, so any agent can reconstruct one from the other.

### Slug → title mapping rule

To go from `YYYYMMDD_<short-slug>` to a human-readable title:

1. Drop the `YYYYMMDD_` date prefix (the WebUI's own metadata carries the timestamp).
2. Replace underscores with spaces.
3. Sentence-case: capitalize the first word and proper nouns/acronyms; everything else lowercase.
4. For compound concepts that previously used `-` inside a single underscore segment (e.g., `clone_first_ship`), use a hyphen between the words that belong together and a space between separate concepts. Result: "Clone-first ship".
5. If the slug contains a phase or plan reference like `plan03_` or `phase4_`, render it as "Plan 03 — " or "Phase 4 — " with an em-dash.

Examples (current convo files in this repo):

| Slug | Suggested chat title |
|---|---|
| `20260508_claude_ai_researcher_design` | "Claude.ai researcher design" |
| `20260508_phase1_phase2_initial_build` | "Phase 1 + Phase 2 initial build" |
| `20260509_phase4_runtime_and_skill_index` | "Phase 4 runtime and skill index" |
| `20260510_skill_ports_initial_ship` | "Skill ports — initial ship" |
| `20260511_dogfooding_session` | "Dogfooding session" |
| `20260511_clone_first_ship` | "Clone-first ship" |

### Where in RESEARCHER.md the edit lands

§2e's "Convo-name handshake" paragraph. Replace the example line and add the mapping rule (compactly — maybe 2-3 sentences citing the rule and 2 illustrative examples; the full table can live in HUMANS.md if it grows further).

This is WebUI-specific in practice. Claude Code doesn't have a comparable chat-title concept the user sees in a list, so the affordance there is "ignore the parenthetical." Note this inline so Claude-Code-session agents don't feel obligated to invent a title.

### Verification plan

Next session that runs the §2e handshake should naturally propose both forms. If the user pastes the suggested title into their chat title field, the WebUI list now serves as an index into `docs/convos/`. Track in HUMANS.md as a tip after a few sessions of empirical evidence that it works.

### What could change

If Anthropic ships an API that lets the agent rename the chat itself (currently the title is set by the user via UI), the parenthetical becomes redundant and the agent does the rename directly. Not worth designing around now — the parenthetical works regardless.

---

## Dependencies and Ordering

1. **Task 1** is independent and benefits from being done in a fresh chat (its findings get re-used by Tasks 2-4 commits indirectly via the next session's STATUS update). Recommended: do Task 1 first or in parallel with Tasks 2-4 in different chats.
2. **Tasks 2, 3, 4** are independent of each other; do them in any order in the same session. Commit message proposals:
   - `template: terminology sweep "Custom Instructions" → "Project Instructions" (Plan 04 Task 2)`
   - `update-docs: add Surface field to convo summary template (Plan 04 Task 3)`
   - `RESEARCHER.md: §2e handshake proposes human-readable chat title alongside file slug (Plan 04 Task 4)`
3. **Task 1's findings**, once written, may motivate small edits to `02_skill_ports.md` Wave 4 / Wave 5 sections — fold those into the same session as Task 1 or queue separately if they're nontrivial.

Estimated total time: 60-90 minutes across one or two sessions. Task 1 is ~20 min of fresh-chat work + ~10 min writing the reference file. Tasks 2-4 combined are ~30-45 min of editing.

## Out of Scope

- **Retroactively adding `Surface` to existing convo files.** Decided against in Task 3 — claims-by-inference about past sessions is worse than just leaving the gap.
- **Cross-Project rename of the "Project Instructions" field in the Anthropic UI.** Not ours to rename; we just match the term they use.
- **API-based chat-title rename.** No such API exists today (Task 4 footnote); revisit if it ships.
- **Wave 0 (provenance + sync infrastructure).** Still deferred; Task 1's findings might motivate a re-evaluation if drift between `~/.claude/skills/` and `template/skills/` becomes visible, but Plan 04 doesn't take it on.
- **Phase 4.5 (collaborator mode v1.1).** Still waits for a real collaborator candidate.
- **Beta-session-driven empirical resolution of banner-vs-proper-REST.** That's in §8 Parking Lot; this plan doesn't substitute for it.

---

**Testing Details:** No code changes, so no test suite. Task 1 is itself a test (an empirical probe of sandbox capabilities). Tasks 2-4 are doc edits whose verification is `grep` of the changed files and one fresh-chat run that exercises the changed prose.

**Implementation Details:**
- Task 1's fresh-chat session needs no Project attachment; an unattached claude.ai chat works because the probes don't need PAT auth or repo access. Just `pip` and `python3`. Once results are gathered, paste into a Project chat (or copy into the repo via Contents API from a follow-on chat) to write `SANDBOX_TOOLING.md`.
- Task 2's reference sweep follows Plan 03's principle: leave historical phase/convo descriptions intact, update forward-looking and current-state references only.
- Task 3's edit is one line in `update-docs/SKILL.md`. Be careful not to also edit the verbatim Claude-Code path examples elsewhere in the skill (those are intentional Code paths that the REST-adaptation banner says to translate).
- Task 4's mapping rule is deterministic but has minor stylistic latitude — pick a convention and stick with it. The mapping table at the top of HUMANS.md (or as part of Task 4's RESEARCHER.md edit) seeds the convention.
- Task 1's findings should also be referenced in §8 Parking Lot if a new open question emerges (e.g., "pandoc unavailable, branch-document-review needs design rethink").

**What could change:** If Task 1 reveals `pandoc` is genuinely unavailable in the claude.ai sandbox with no installable workaround, Wave 4's `branch-document-review` port needs a redesign that uses `difflib` against raw markdown rather than re-rendering markdown→docx for visual diff. That's a meaningful design pivot but tractable; the existing AITaxBID source already has a `difflib` path. Flag in STATUS Open Questions and adjust 02's Wave 4 section.

**Questions:**
- Should `SANDBOX_TOOLING.md` include a row for `pdfminer.six` (the `pypdf` fallback) verified at the same time, or is it premature to test fallbacks before knowing whether the primary works? Lean: test fallbacks only if primaries fail.
- The HUMANS.md / RESEARCHER.md split for the slug → title mapping table: should the full table live in RESEARCHER.md (closer to the handshake rule) or in HUMANS.md (closer to user-facing explanation)? Lean: short version with 2-3 examples in RESEARCHER.md §2e; full table optional in HUMANS.md if it grows useful.
- Is there a fifth small cleanup worth folding in before this plan executes? Currently four feels right; more than that and the plan loses focus.

---
