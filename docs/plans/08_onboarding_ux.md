# claude_researcher — Plan 08: Onboarding UX cleanup

**Goal:** Apply the 2026-06-03 think-aloud session's prose and structural fixes to README, HUMANS.md, BOOTSTRAP.md (§0/§1/§2b/§4), RESEARCHER.md (project-repo isolation rule), and `personal_info.md.template`. Add screenshots for the two hardest steps (egress + PAT). Three captured task issues (#11 website, #12 add-paper first-save, #13 reminders mechanism) execute separately.

**Status:** Ready for execution. All decisions resolved at design time; this plan is a sequence of mostly-mechanical text edits with the structural calls already made.

**Originating convo:** [`20260603_onboarding_ux_think_aloud.md`](../convos/20260603_onboarding_ux_think_aloud.md). The convo's **Decisions Made** + **Resolutions (2026-06-03 follow-up)** sections are the input. The **Captured Tasks** section (#11/#12/#13) is tracked separately — out of scope here.

**Related prior work:** PR [#8](https://github.com/danparshall/claude_researcher/pull/8) (egress UI-agnostic rewrite, 2026-05-21) is the most relevant recent neighbor — it shipped the §1b prose-by-intent approach that Task 1.4 below extends. The think-aloud session is evidence that prose-only intervention on §1b isn't enough; screenshots (Phase 2) are the harder next step.

**Confidence:** High. Decisions all locked from a single triage conversation that ran through six open questions in a follow-up triage with Dan; nothing left to relitigate. Most edits are mechanical text changes. Two coupling concerns (paper-naming fallback, reminders mechanism) are resolved by deferring to companion issues — no half-mechanism is left exposed.

**Branch:** `onboarding-ux-cleanup`.

**Tracking issue:** none for this plan itself. The deferred surface (#11/#12/#13) already has issue coverage.

---

## Coupling concerns resolved at design time (do NOT re-open)

These were thought through before writing the plan. The implementing agent should not re-derive them.

- **Drop paper-naming from BOOTSTRAP interview without breaking add-paper.** Per Plan 06's ship (commit `454018f`), `add-paper/SKILL.md` reads `paper_naming.academic_format` and `paper_naming.institutional_format` from `personal_info.md` and falls back to hardcoded defaults when the keys are absent. Therefore dropping both the bootstrap question (Task 1.6) and the template fields (Task 1.7) is safe — first-run add-paper uses the existing defaults. Issue [#12](https://github.com/danparshall/claude_researcher/issues/12) ships the UX polish (explicit first-save prompt) later; it's a layer on top, not a precondition.
- **Allow-all egress default does NOT require a `reminders.md` write in this plan.** The convo pairs "lead with allow-all" with "revisit-after-a-week reminder." Plan 08 ships **only the prose change** (Task 1.4). The reminder-writing mechanism (BOOTSTRAP-end write to `basic_config/reminders.md` + RESEARCHER.md session-start check) is tracked at [#13](https://github.com/danparshall/claude_researcher/issues/13) and executes as a unit when that issue ships. Plan 08 does not write any half-mechanism. The forward-reference sentence in Task 1.4 is a UX promise that's harmless even when #13 hasn't shipped (worst case: user revisits manually, which is today's behavior).
- **Website is out of scope.** Tracked at [#11](https://github.com/danparshall/claude_researcher/issues/11). Plan 08 references the issue in Phase 3 below for completeness but executes nothing.

## Decisions confirmed at design time (do NOT re-litigate)

Lifted from the convo's Decisions Made + Resolutions sections. Re-opening these blows scope unboundedly.

- README becomes **very short, humans-only.** Most content moves into BOOTSTRAP or out of the repo. README is roughly: bootstrap prompt + privacy one-liner + pointer to HUMANS.md.
- **Claude.ai = Pro/Team. GitHub free tier = fine.** README phrasing explicit about both.
- **Project ≡ repo, with NDA/IP isolation rule** lands in `RESEARCHER.md` §4 (already about project boundary discipline). NOT in `personal_info.md` or Project Instructions.
- **Allow-all egress default.** BOOTSTRAP §1b leads with allow-all; allow-list framed as "if you have a corporate-style preference for tighter scoping."
- **PAT section becomes affordance-based** ("you don't need to understand this; ask me to explain if you want"). Bootstrap-only; not RESEARCHER.md.
- **Paper-naming dropped from BOOTSTRAP §4 Batch 3** entirely. Templates and add-paper fallback handle the gap. #12 is the use-time UX polish.
- **Git-fluency elicitation reworded** to concept-check, not menu-pick: *"the program used to track all changes in the project is called 'git' — are you familiar with it?"* The agent still classifies internally into `novice` / `occasional` / `fluent` so RESEARCHER.md §1's tier dial keeps working — the elicitation just isn't menu-driven.
- **Per-batch closer added to all three interview batches:** *"It's okay if you don't want to answer right now, and remember you can always ask me for explanations."*
- **Screenshots live at `template/reference/screenshots/`**, referenced from BOOTSTRAP by relative path.
- **Terms to drop from user-facing prose:** orchestration, fork, repo (in narrative), shell commands, "my VM" / "the VM", egress (in narrative only — the literal Settings UI label survives in step-by-step instructions). Plus "token" disambiguation, since the audience hears "Anthropic-billed tokens" first.
- **Sequencing locked:** prose pass + RESEARCHER.md rules first; screenshots second; website (#11) third / separate.

---

## Phase 1 — Prose pass + RESEARCHER.md rules

Text-only changes. Cheap to review as diffs. Should ship in 3-4 logical commits (one per cohesive change area). The §4 interview restructure pairs the BOOTSTRAP edit with the template edit (Tasks 1.6 + 1.7) in a single commit, since they're one logical change.

### Task 1.1 — README slim-down

**File:** `README.md` (currently ~60 lines).

**Current shape:** Quick start (L7-28) → What's in this repo (L30-37) → About (L39-41) → Reporting issues (L43-45) → License (L47-49) → Developer info (L53-60).

**Target shape:**
- 2-3 sentences of what this is, including the **new privacy one-liner**: *"The goal is to get everything set up so only you can access it; we never see or use your data."*
- 1 sentence framing accounts: *"You'll need a Claude.ai Pro or Team account and a GitHub account (free tier is fine)."*
- **Bootstrap prompt block** with a clear `**The prompt:**` header label and a one-line preamble: *"This tells Claude how to set up the workflow so you can get back to thinking. You don't need to read it — but you can."*
- One-line pointer to HUMANS.md for everything else.

**What moves out:**
- "What's in this repo" developer enumeration → drop (it's repo-archaeology; readers who want it can browse `template/`).
- "About" collaboration note → keep a one-liner with links; longer story moves to HUMANS.md if not already there.
- "Reporting issues" → see Question 2 below for placement (likely a one-liner in README pointing at GitHub Issues, since the affordance is structural).
- "License" → tiny footer line is fine; LICENSE file is the canonical home.
- "Developer info" section → drop; this repo is published now.

**Steps:**
1. Open `README.md`.
2. Replace existing content with the target shape. **Preserve the SHA-pinned raw URL exactly** — `tools/repin.py` matches a specific regex (URL with `/main/` or a 40-char SHA in `https://raw.githubusercontent.com/danparshall/claude_researcher/<SHA-or-main>/...` shape). Currently pinned to `2dec9af`.
3. Verify `python3 tools/repin.py --dry-run` (or equivalent inspection) still recognizes the URL pattern after the edit.
4. Commit: `convo: README slim-down per onboarding think-aloud`.

**Don't:** drop or reformat the SHA-pinned URL. Don't drop the prompt block.

---

### Task 1.2 — HUMANS.md durability paragraph

**File:** `HUMANS.md`.

**Change:** insert a new subsection between "## Where this comes from" (currently L23-31) and "## What it isn't" (currently L33-40). Heading: `## Don't worry about the machinery`. Body adapted from the convo's draft:

> "You don't need to care about prompts and config files day-to-day; the bootstrap sets things up so you don't have to. But it's all yours, and you can update any of it whenever you decide you're ready. Every change is recorded and version-controlled in your GitHub repo, so it's almost impossible to break anything permanently — if a change doesn't work out, the old version is one click away."

Light polish for HUMANS.md tone (no all-caps, plain prose).

**Steps:**
1. Open `HUMANS.md`.
2. Insert the new subsection at the boundary between L31 and L33.
3. Commit: `convo: HUMANS.md add durability subsection`.

**Don't:** restructure existing HUMANS.md sections. Insertion only.

---

### Task 1.3 — BOOTSTRAP §0 timing claim

**File:** `template/BOOTSTRAP.md` L24 (inside Step 0's opening script).

**Change:** "~5 minutes if network is already set up, ~15 minutes if this is a true first-time setup" → "~5 minutes if network is already set up, ~10 minutes if this is a true first-time setup." Matches the README's revised 10-minute claim (Task 1.1).

**Steps:**
1. Edit L24 of `template/BOOTSTRAP.md`.
2. (Folded into Task 1.4's commit — both are BOOTSTRAP prose edits in adjacent regions and ship together.)

---

### Task 1.4 — BOOTSTRAP §1b egress: lead with allow-all

**File:** `template/BOOTSTRAP.md` Step 1b (L51-79; specifically L67-79).

**Current shape:** L70-77 enumerates three UI variants (simple toggle / mode-choice / domain-list) and presents the allow-list path before reaching the "simplest path is to allow everything" sentence (L72). The framing is mealy — allow-all reads as one option among three rather than the recommended default.

**Target:** lead with allow-all. Restructure so the user reads "easiest = allow everything" first; the allow-list path is framed as advanced / corporate-tighter-scoping.

**Specific edit pattern:**
1. Open the variant block (after "**Turn it on**") with a single recommended-path sentence: *"The easiest setting is to allow everything — this controls Anthropic's server-side virtual machine (the one Claude uses for this chat), not your computer, so the broad setting doesn't open anything up on your local machine or behind your work firewall."* (Note: this sentence uses the term "virtual machine" once because it's load-bearing for the user's mental model — but does NOT use "my VM," which is the jargon the convo flagged.)
2. Then enumerate the UI variants but with allow-all applied to each:
   - Simple on/off toggle → on.
   - Mode-choice → the broadest option.
   - Domain allow-list → check the "allow all" box if present; otherwise see the minimum-domains list as the advanced alternative.
3. Keep the existing four-GitHub-domain list + the paper-source-domain list, but reframe as: *"If your account or your tier only offers a domain-list UI without an 'allow all' option, you'll need these four at minimum:"* — i.e., these become a fallback for tier-restricted accounts, not the default for everyone.
4. Add one forward-reference sentence: *"After bootstrap I can set up a reminder for you to revisit this setting in a week if you want to tighten it later — for now, the easiest path is to allow everything."* This is a UX promise the user reads; the actual reminder write is part of [#13](https://github.com/danparshall/claude_researcher/issues/13). If #13 hasn't shipped when Plan 08 ships, the worst case is the user revisits manually (today's behavior). No regression.

**Don't:** drop the literal claude.ai Settings UI label "network egress" — that's the actual UI string the user has to find. Don't remove the four-GitHub-domain list. Don't change the 1a probe (L40-50) or the 1c restart logic (L83-92).

**Verify after editing:** read §1b end-to-end as a fresh agent would. Does the first thing the user is told to do read as "allow everything"? Does the allow-list path read as advanced/optional?

---

### Task 1.5 — BOOTSTRAP §2b PAT: affordance-based rewrite

**File:** `template/BOOTSTRAP.md` Step 2b (L108-147), plus "About PAT scope" subsection (L168-170).

**Current shape:** L108-114 frames the PAT prompt. L116-127 lectures the user through each GitHub permission (Administration, Contents, Metadata). L129 has the explicit Administration confirmation gate. L131-147 covers paste, env var, and the smoke test.

**Target:** affordance-based. Replace the lecture with a one-sentence framing + compact action recipe + an explicit "ask me to explain if you want details" line. Move the per-permission detail into a subsection at the end of §2b that the agent only consults on user request.

**Specific edits:**
1. Replace L108's `Ask: ...` framing with a one-sentence intro: *"The PAT is the password Claude uses to talk to GitHub on your behalf. You don't need to understand the details — happy to explain any of this if you want; just ask."*
2. Compress L116-127 into a tight action recipe — five lines, not five paragraphs:
   - URL (`https://github.com/settings/personal-access-tokens/new`)
   - Token name + expiration (compact)
   - **Repository access:** All repositories (with the existing single-line caveat about scoping to non-existent-yet repos)
   - **Permissions to set:** "Use these values — **Administration**: Read and write; **Contents**: Read and write; **Metadata**: Read-only (default)." Single line, action-oriented; the convo specifically asked for "use these values" instead of "Configure."
   - Click **Generate token**, copy the value immediately.
3. **Keep the Administration confirmation gate (L129) exactly as-is.** Load-bearing — without it, Step 6 throws 403.
4. Add a new subsection at the end of §2b: `### Why each permission (ask if you want details)`. Move the current per-permission explanations there, written for the agent to read aloud to the user on request. The user only sees this content if they ask "what does each permission do?" — the agent then reads it back.
5. Reword L121's "repo-scoped" — the term is jargon on first appearance. Replace with "scoped to all your GitHub repos" or similar plain phrasing.
6. Rename the convo's flagged button: L123 says "Click `Add permissions`" implicitly — make the button name explicit if the GitHub UI labels it that way (verify against current GitHub Settings UI; the convo flagged "name the button explicitly" as one of the small copy-edits).

**Don't:** remove the smoke test (L138-147). Don't remove or relax the Administration confirmation gate. Don't drop the `github_pat_` prefix verification cue (it's the user's confirmation that they copied the right thing).

**Commit:** Tasks 1.3 + 1.4 + 1.5 ship together as one commit covering BOOTSTRAP §§0/1b/2b prose changes: `convo: BOOTSTRAP §§0/1b/2b prose pass (allow-all default, PAT affordance, timing claim)`.

---

### Task 1.6 — BOOTSTRAP §4 interview: drop paper-naming + reword git-fluency + per-batch closer

**File:** `template/BOOTSTRAP.md` Step 4 (L197-248).

**Three changes, one structural edit:**

**(a) Drop paper-naming entirely.** Remove L231-237 (the `**Paper naming conventions**` question + its two-protocol enumeration). Renumber Batch 3 from 4 questions to 3 questions (Git fluency, Mode, Extra paper-source domains). Update L240's `Record as` summary to drop `<PAPER_NAMING_ACADEMIC>` + `<PAPER_NAMING_INSTITUTIONAL>`. Remove L242-246 (the canonical-text blockquotes — those existed to capture defaults when the user accepted them; no longer needed). The "After all three batches, summarize" line at L248 stays unchanged.

**(b) Reword git-fluency.** L229's menu-pick question becomes a concept-check.

Replace L229 ("**Git fluency** — pick one: **novice** ... **occasional** ... **fluent** ... This calibrates how chatty I am about git operations.") with:

> "**Git** — the program used to track all changes in your project is called *git*. Are you familiar with it? (If yes, briefly — daily user? occasional? web-UI only? If no, no problem — I'll explain things as we go.)"

The agent classifies the answer into the existing tier values (`novice` / `occasional` / `fluent`) and writes that tier to `personal_info.md` under the existing field. **Downstream RESEARCHER.md §1's tier dial keeps working unchanged** — only the elicitation phrasing changes.

**(c) Per-batch closer.** Append to each of the three batches' question blockquotes (after the last question in each batch, before the `Record as` line):

> "It's okay if you don't want to answer right now, and remember you can always ask me for explanations."

So three insertions:
- After Batch 1's question 3 (L211).
- After Batch 2's question 3 (L221).
- After Batch 3's revised question 3 (the renumbered "Extra paper-source domains" — L238 after paper-naming is removed).

Place the closer **inside the blockquote** so it reads as part of the agent's spoken question, not as an instruction to the agent. (See Question 3 below if the implementing agent wants to verify this call.)

**Steps:**
1. Open `template/BOOTSTRAP.md`.
2. Apply (a): remove paper-naming question + canonical-text blockquotes + summary mentions.
3. Apply (b): git-fluency rewording.
4. Apply (c): per-batch closer in three places.
5. Read the three batches end-to-end as a fresh agent would. Verify the per-batch summarization line (L199) still applies to the revised content.
6. **Bundle with Task 1.7 in the same commit** — interview-side drop and template-side drop are one logical change.

---

### Task 1.7 — personal_info.md.template: drop paper-naming fields

**File:** `template/templates/personal_info.md.template` (currently 40 lines).

**Change:** delete L35-36:

```
- **Paper naming (academic):** `<PAPER_NAMING_ACADEMIC>`
- **Paper naming (institutional):** `<PAPER_NAMING_INSTITUTIONAL>`
```

Result: `## Operating preferences` becomes a 2-item list (Git fluency, Mode). The schema is still extensible — when #12 ships, add-paper writes these keys back to `personal_info.md` on first save with the user-chosen values.

**Why safe:** `add-paper/SKILL.md` reads these keys with fallback to defaults when absent. No regression — first-run add-paper still names papers correctly.

**Steps:**
1. Edit `template/templates/personal_info.md.template`.
2. Delete L35-36.
3. (Folded into Task 1.6's commit.) Commit message: `convo: BOOTSTRAP §4 interview restructure (drop paper-naming, reword git-fluency, per-batch closers)`.

---

### Task 1.8 — RESEARCHER.md: project-repo isolation rule

**File:** `template/RESEARCHER.md` §4 — "Project confusion handling" (L289-298).

**Current shape:** §4 already enforces "don't re-bind to a different repo mid-session" when the user names a repo that doesn't match the Project Instructions binding. The new rule extends with the NDA/IP framing — the principle behind why the gate exists.

**Target:** add a paragraph at the end of §4, after the existing L297 paragraph and before the L299 `---` divider:

> "**Project ≡ repo, NDA/IP isolation.** Each claude.ai Project corresponds to exactly one research repo. Do not let data, code, or context bleed between repos — even when the user asks something like *'remind me what we worked on for ClientX,'* do not auto-bridge into another repo's contents. The motivation is NDA/IP: cross-contamination between, say, a confidential consulting project and a public-policy research project is a real risk, even when both belong to the same user. If the user wants context from another repo, ask them to switch Projects (or open a fresh chat in that Project) rather than reaching across from this Project's session."

**Steps:**
1. Open `template/RESEARCHER.md`.
2. Append the new paragraph at the end of §4 (after L297, before the L299 `---`).
3. Commit: `convo: RESEARCHER.md project-repo isolation rule (NDA/IP)`.

**Don't:** modify §4's existing scripted error-handling (L291-297) — that's the operational gate. The new paragraph extends the principle; the existing gate stays unchanged.

---

### Task 1.9 — Terminology sweep

**Scope:** all four user-facing files (`README.md`, `HUMANS.md`, `template/BOOTSTRAP.md`, `template/RESEARCHER.md`).

**Drop from user-facing prose** (per convo):
- "orchestration"
- "fork" (BOOTSTRAP doesn't fork; it creates new empty repos via the GitHub API)
- "repo" in narrative (use "GitHub project" or "project" — but disambiguate from claude.ai Project where the context is ambiguous)
- "shell commands"
- "my VM" / "the VM" (route around with "Claude needs internet access for this" — "virtual machine" survives where it's load-bearing for the mental model, see Task 1.4 note)
- "egress" in narrative prose. The literal Settings UI label survives in step-by-step instructions ("Look for the **network egress** setting" stays — that's the label the user has to find).

**Handle carefully:**
- "token" — the audience hears "tokens" as "things Anthropic charges you for." First mention of PAT should frame it as "the password Claude uses to talk to GitHub on your behalf" (already handled in Task 1.5). Subsequent uses of "PAT" or "token" are fine because the disambiguation has happened.

**Method:**
1. Run the greps:
   - `grep -n -i -E 'orchestrat|fork|shell command|my VM|the VM' README.md HUMANS.md template/BOOTSTRAP.md template/RESEARCHER.md`
   - `grep -n -i 'egress' README.md HUMANS.md template/BOOTSTRAP.md template/RESEARCHER.md`
2. For each hit, classify: (a) **leave** (literal UI label, code, technical detail in agent-only context); (b) **reword** (user-facing prose); (c) **drop** (just noise).
3. **Surface ambiguous cases to Dan before committing** — `tools/reference-sweep-note.md` (the methodology note from Plan 04) records that find-and-replace-by-inspection has failed twice on this repo. Verify mechanically with greps after each round of edits, not by visual scan.
4. Repeat the greps after edits. Remaining hits should all be intentional (UI labels, code, agent-facing notes).
5. Commit: `convo: terminology sweep per onboarding think-aloud`.

**Reference:** `tools/reference-sweep-note.md` for the verification protocol.

---

### Phase 1 testing

This is documentation work — no automated tests. Verification is by structured read-through and by mechanical grep.

**Testing Plan**

I will verify Phase 1 by:

1. **Self-read-through:** after all Phase 1 commits, read each touched file end-to-end as a fresh agent would. Catch dangling references to dropped concepts (e.g., a leftover mention of `<PAPER_NAMING_ACADEMIC>` somewhere, or "fork" surviving in HUMANS.md). This is the doc analog of an integration check.
2. **Mechanical greps:** the terminology sweep's verification greps from Task 1.9, run after each edit and once more at the end of Phase 1.
3. **Dogfood read-through (recommended, highest-leverage):** open a fresh claude.ai web chat, paste the README's bootstrap prompt, walk through Steps 0-4 *as the agent reads them*. Capture every point where the prose still feels jargon-y, ambiguous, or assumes prior knowledge. Findings go into a follow-up convo on this branch. This is the natural dogfooding moment the convo flagged — running it on web exercises the very flow being fixed.
4. **Repin sanity check:** `tools/repin.py` recognizes the SHA-pinned URL after Task 1.1's README edit (verify by inspection — the URL pattern must stay matchable).

NOTE: this is documentation work, not code, so no TDD applies. The exception clause in the write-a-plan skill covers this: "Pure analysis or exploration tasks do not need TDD."

---

## Phase 2 — Screenshots

Ships after Phase 1's prose is settled and committed — captures are tied to specific Step labels and screen positions, so the wording needs to be stable first.

### Task 2.1 — Create screenshots directory

**Steps:**
1. `mkdir -p template/reference/screenshots/`
2. Add a `.gitkeep` so the directory exists in git before screenshots land.
3. Folded into Task 2.2's commit.

### Task 2.2 — Capture and stage four screenshots

**Targets (per convo):**

| Filename | What it shows | Step it lives near |
|----------|----------------|---------------------|
| `claude_egress_settings.png` | claude.ai Settings → network egress (toggle + dropdown if visible) | BOOTSTRAP §1b |
| `github_pat_create_form.png` | GitHub Settings → fine-grained PAT create form (top of page) | BOOTSTRAP §2b |
| `github_pat_add_permissions.png` | The "Add permissions" button + opened permission selector | BOOTSTRAP §2b |
| `github_pat_read_write_flip.png` | A permission toggled from Read-only to Read/Write | BOOTSTRAP §2b |

**Capture method:**

1. Read `/Users/dan/.claude/skills/using-screenshots/SKILL.md`.
2. Capture each screen. Prefer a fresh-account test if possible (avoid leaking real PATs, usernames, or other personal identifiers).
3. Crop tight to the relevant UI region; redact any identifiers that survived the crop.
4. PNG format. Sub-200 KB per image is fine; smaller is better for `raw.githubusercontent.com` fetches.
5. Save to `template/reference/screenshots/` with the filenames above.
6. Reference each inline in BOOTSTRAP at the relevant Step. Markdown image syntax with relative path: `![claude.ai network egress settings](reference/screenshots/claude_egress_settings.png)`. Path is relative to `template/BOOTSTRAP.md`, so `reference/screenshots/<name>.png` resolves correctly both in GitHub's web view and via `raw.githubusercontent.com`.
7. Commit: `add screenshots for egress + PAT steps`.

**Caveat:** claude.ai's egress UI has changed at least twice in the last six weeks — the egress screenshot in particular will go stale fast. Record the capture date inline in the image filename or a sidecar `.md` note (`template/reference/screenshots/CAPTURED.md` is a reasonable home — one line per image, capture date + UI variant).

**Open question (deferred to execution time):** should screenshot image references in BOOTSTRAP be SHA-pinned the way the prose URLs are? Probably no — BOOTSTRAP itself is SHA-pinned in README, and images are fetched alongside BOOTSTRAP, so the BOOTSTRAP-level pin handles the staleness story. Confirm at execution time.

---

### Phase 2 testing

1. Verify each image renders when previewed from the BOOTSTRAP markdown on GitHub's web view.
2. Verify the relative path resolves via `raw.githubusercontent.com` fetch (not just web view).
3. Optional dogfood: a fresh claude.ai chat fetches BOOTSTRAP via the README's pinned URL — does the rendered version show the images, or just the markdown source? Agent-side image rendering via `WebFetch` may not display images directly even when the markdown references them; confirm acceptable to ship either way.
4. Verify capture-date sidecar (`template/reference/screenshots/CAPTURED.md`) is committed and lists all four images.

---

## Phase 3 — Website (out of scope)

Tracked at [issue #11](https://github.com/danparshall/claude_researcher/issues/11). Not executed by Plan 08. The convo locked the public website as separate scope for the hoi-polloi audience.

When #11 executes, it's its own plan / branch / convo — no edits to `onboarding-ux-cleanup` are required to unblock it. Plan 08's prose changes already reduce the README's burden enough that the website doesn't have to wait on additional README cleanup.

---

## What could change

- **Egress UI churn.** The convo and PR #8 history both confirm the claude.ai network-egress Settings UI has shifted at least twice in the last six weeks. Screenshots will go stale. Task 1.4's prose changes are UI-agnostic by design (extending PR #8's principle), so the prose survives even when the screenshot doesn't. If a churn happens during execution, prioritize the prose; re-capture screenshots after.
- **#12 (add-paper first-use prompt) timing.** If #12 ships before Plan 08, Task 1.6's paper-naming drop is even safer (explicit ask instead of silent default). If #12 stalls, defaults catch users until it ships. Either way, no half-mechanism.
- **#13 (reminders mechanism) timing.** Task 1.4's forward-reference sentence ("I'll set up a reminder for you to revisit in a week") is a UX promise. If #13 doesn't ship for a while, the promise is empty operationally. Two options: (a) keep the sentence as future-tense and accept the temporary gap; (b) drop the sentence and add it back when #13 ships. Recommend (a) — the user's mental model is right either way, and the cost of restoring the sentence later is higher than the cost of leaving it.
- **README slim-down (Task 1.1) ↔ `tools/repin.py` regex.** The SHA-pinned bootstrap-prompt URL must stay matchable. If the slim-down accidentally drops or reformats it, `repin.py` breaks silently. Verify after editing.
- **Per-batch closer placement (Question 3 below).** If a fresh-chat dogfood read shows the closer reads awkwardly inside the blockquote, move it outside. Cheap to change.

---

## Questions

1. **How much "About" should survive in the slimmed README?** The current "About" section names Dan + Andrea as the collaboration and links to their sites. The convo says README becomes "very short, humans-only" but doesn't explicitly say to drop the collaboration framing. **Recommendation:** keep a one-line attribution with links; move the longer collaboration story to HUMANS.md if it's not already there.
2. **Where does "Reporting issues" land if README drops it?** Options: (a) move to HUMANS.md as a small "Reporting issues" subsection; (b) leave a one-line pointer in README (e.g., *"Found a bug? File an issue on the [GitHub Issues page](https://github.com/danparshall/claude_researcher/issues/new) — or ask the agent to file one for you with diagnostic context."*); (c) drop and rely on GitHub Issues being discoverable. **Recommendation:** (b) — the affordance ("ask the agent to file one") is value-add even in a slim README.
3. **Per-batch closer placement: inside the blockquote (reads as agent speech) or outside (reads as instruction to the agent)?** **Recommendation:** inside. The closer is something the user benefits from hearing as part of the agent's actual question, not as a silent calibration cue. But cheap to flip if dogfood reads otherwise.
4. **Screenshot location vs Dan's `basic_config`.** These are bootstrap onboarding artifacts; they belong in the upstream template repo so every user gets them via the bootstrap fetch. `template/reference/screenshots/` is the right home. Confirmed in convo Resolutions.

---

**Testing Details** — see Phase 1 testing and Phase 2 testing sections above. This plan ships documentation, not code; verification is by structured read-through, mechanical grep, and (recommended) a dogfood fresh-chat walk-through.

**Implementation Details (max 10 bullets):**
- Phase 1 ships in roughly 4 commits: README slim-down, HUMANS.md durability paragraph, BOOTSTRAP §§0/1b/2b prose pass, BOOTSTRAP §4 interview + personal_info.md.template, RESEARCHER.md isolation rule, terminology sweep. (Last two can fold into one if the sweep is light.)
- Phase 2 ships as one commit (screenshots dir + four PNGs + BOOTSTRAP inline references + CAPTURED.md sidecar).
- All edits stay on branch `onboarding-ux-cleanup` until Dan asks for the PR.
- The SHA-pinned bootstrap URL in README (`2dec9af`) must stay intact and `repin.py`-matchable after Task 1.1.
- The Administration confirmation gate in §2b (L129) must stay intact after Task 1.5.
- The four-GitHub-domain allow-list must stay listed (as fallback) after Task 1.4.
- The existing `<GIT_FLUENCY>` field name + downstream tier-dial in RESEARCHER.md §1 stay unchanged after Task 1.6; only the elicitation phrasing changes.
- `tools/reference-sweep-note.md` methodology applies to Task 1.9 — verify with greps, not visual scan.
- No `basic_config/reminders.md` write in this plan; #13 owns that.
- No `add-paper/SKILL.md` first-save prompt in this plan; #12 owns that.

**What could change:** see the section above.

**Questions:** see the section above.

---
