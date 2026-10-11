---
name: agent-research-verification
description: "Codifies the workflow for delegating literature searches or evidence synthesis to external deep-research agents (Claude Research, ChatGPT Deep Research, or similar) so their outputs become trustworthy inputs to deliverables. Core principle: agent outputs are NEVER directly citable. Only the verification document — produced by cross-checking agent claims against retrieved originals — is citable. The skill orchestrates: prompt drafting (consulting LESSONS.md for known agent failure modes), filing the raw output, the sources table the agent produces, handing off to the project's papers protocol for retrieved originals, verification against those originals, and discipline around LESSONS.md so prompt engineering compounds across dives. Does NOT replace the project's papers protocol — Step 6 hands off to it explicitly."
triggers: >-
  "I'm going to run a deep dive," "let's draft a research prompt," "I have an agent output to
  file," "verify this dive"; any Claude Research or Deep Research output. Agent outputs are
  never citable; only the verification document is
---

# Agent Research Verification Skill

This skill defines the workflow for handling output from external deep-research agents (Claude Research, ChatGPT Deep Research, or similar tools). It exists because agent outputs look authoritative but are not. They contain fabricated citations, misattributed claims, overstated magnitudes, and silently dropped counter-evidence. Using them directly in deliverables is unsafe.

The workflow's core principle: **agent outputs are never directly citable. Only the verification document — produced by cross-checking agent claims against retrieved originals — is citable.** The raw agent output remains in the project as an audit trail.

The workflow has a second purpose beyond per-dive verification: **patterns in agent errors accumulate in a `LESSONS.md` file, and that file is consulted before drafting any new deep-research prompt.** Prompt engineering compounds across dives rather than starting from scratch each time.

**What this skill is, and what it is not.** This skill defines (a) the folder structure for agent outputs, (b) the per-dive file set and naming convention, (c) the eight-step workflow from prompt to citable verification, (d) the verification-document structure, (e) the INDEX.md workflow tracker for dives, plus the archetype-blind registration of verified dives into the repo's own deep-dives catalog, (f) the LESSONS.md discipline for prompt engineering, (g) the hand-off rules to the project's papers protocol for retrieved originals, and (h) the workflow-skip logging discipline that keeps gaps from compounding silently.

It is **not** the papers protocol itself — Step 6 hands off to the project's `materials_processing_skill.md` family and, when non-paper sources are present, to `document_processing_skill.md`. It is also **not** a brainstorming or thinking-notes skill — for rough-idea work upstream of running a dive, use `brainstorming_skill.md`. And it is **not** a substitute for reading and engaging with the papers it surfaces — the verification step requires retrieving and reading the originals, not just trusting the agent's summary.

---

## When to use this skill

Read this skill when:
- The user says "I'm going to run a deep dive on X," "let's draft a research prompt," "let's set up an agent dive," or similar.
- The user returns from running a deep-research dive with output to file ("I have the output," "let me share what the agent produced").
- The user asks "what dives have I done on X?", "have I already researched this?", or any retrieval question about past agent work.
- The user asks to verify an existing raw agent output ("verify this," "let's check the agent's claims," "do the second pass").
- Any reference to Claude Research, ChatGPT Deep Research, Perplexity Deep Research, or similar agent platforms in the context of literature search or evidence synthesis.

Do not use this skill for:
- One-off web searches Claude does inline in a working chat (that's just normal work).
- Reading and processing a paper the user found on their own (that's `materials_processing_skill.md`).
- Brainstorming what to research (that's `brainstorming_skill.md` upstream).
- Writing the deliverable that uses verified findings (that's `writing_skill.md` Protocol 2).

---

## Repo-specific parameters

The repo's `CLAUDE.md` provides project-specific values for the parameters below. If `CLAUDE.md` does not define a parameter, use the default given here.

| Parameter | Description | Default |
|---|---|---|
| `AGENT_OUTPUTS_FOLDER` | Where agent-research artifacts live | `workspace/agent_outputs/` |
| `AGENT_OUTPUTS_INDEX` | Topic-grouped tracker for all dives | `workspace/agent_outputs/INDEX.md` |
| `AGENT_OUTPUTS_LESSONS` | Cross-dive error patterns and prompt-engineering responses | `workspace/agent_outputs/LESSONS.md` |
| `AGENT_OUTPUTS_SKIPS` | Cross-dive register of workflow skip events | `workspace/agent_outputs/WORKFLOW_SKIPS.md` |
| `PAPERS_PROTOCOL_SKILL` | Project's paper-processing skill (used at Step 6 hand-off) | `materials_processing_skill.md` |
| `DOCUMENT_PROTOCOL_SKILL` | Project's document-processing skill (used at Step 6 hand-off for non-paper sources) | `document_processing_skill.md` |

If `CLAUDE.md` does not define these parameters, use the defaults — but flag to the user that the parameters should be added to `CLAUDE.md` so future sessions don't have to re-infer them.

---

## Folder structure

```
workspace/agent_outputs/
├── INDEX.md                          ← topic-grouped tracker for all dives
├── LESSONS.md                        ← cross-dive error patterns + prompt-engineering responses
├── WORKFLOW_SKIPS.md                 ← cross-dive register of workflow skip events (created up front with INDEX and LESSONS, the skill's triple; a pass creates the three or none, never one of three)
├── <topic_slug_1>/
│   ├── YYYYMMDD_HHMM_prompt.md
│   ├── YYYYMMDD_HHMM_raw.md
│   ├── YYYYMMDD_HHMM_retrieval.md        ← source table (table 1, immutable) + worked-down pass tables + residual not-retrieved list
│   ├── YYYYMMDD_HHMM_workflow_notes.md   ← lazy; only when something was skipped
│   └── YYYYMMDD_HHMM_verification.md
└── <topic_slug_2>/
    └── ...
```

**Folder-per-topic.** A topic is a substantive research question that the user might run multiple dives on over time. Topic slugs are lowercase, snake_case, descriptive (`remote_work_productivity`, `school_meal_costs`, not `topic_1`).

**Files inside a topic carry the dive's date-and-time stamp.** Multiple dives on the same topic coexist without overwriting. All files for one dive share the same `YYYYMMDD_HHMM_` prefix so they sort adjacent when the folder is listed. The timestamp is the *dive identifier*, not a per-file modification date — verification done a week later still carries the dive's original timestamp.

**File set per dive:**

| File | Naming | Produced by | Purpose | Citable? |
|---|---|---|---|---|
| Prompt | `YYYYMMDD_HHMM_prompt.md` | Drafter chat (Step 1) | The prompt that was run, plus filing instructions for the researcher | N/A — input artifact |
| Raw output | `YYYYMMDD_HHMM_raw.md` | Researcher chat (Step 3) | Unedited agent synthesis | **No** — audit trail only |
| Retrieval doc | `YYYYMMDD_HHMM_retrieval.md` | Researcher files table 1 (Step 3); retriever appends the held and completeness checks (Step 4), then passes + residual (Step 5) | One kept, accumulating document: **table 1** = every source × every candidate link (the researcher's verbatim record, append-only below it); the held and completeness checks; the per-pass "still missing" tables; the residual "not retrieved + reason" list at the foot | **No** — kept backlog + input to verification; never deleted |
| Workflow notes | `YYYYMMDD_HHMM_workflow_notes.md` | Any chat (lazy — only when a skip happens) | Narrative of skips and overrides for this dive | **No** — audit/bookkeeping |
| Verification | `YYYYMMDD_HHMM_verification.md` | Verifier chat (Step 7) | Two-table claim-by-claim cross-check against the dive's declared source folders | **Yes** — the only citable artifact |

Plus: raw retrieved originals first land in `workspace/staging/` (the repo's intake funnel, defined in `structure_conventions.md`); the project's papers protocol and (when applicable) document-processing protocol then file the processed outputs into the dive's **declared source folders** — wherever the repo's `FOLDER_MAP`s place literature and non-paper material — never in `agent_outputs/`, emptying staging as they go.

**The retrieval doc is the dive's kept backlog — never deleted.** It is not scratch. Table 1 preserves the agent's full candidate list verbatim; the pass tables show the narrowing; the residual list records what was *not* retrieved and why (paywalled / broken link / not found). That residual is what you return to when a paywalled source later becomes reachable — so the document is retained for the life of the dive, and beyond as audit trail, never pruned. The classic failure — the candidate list deleted before retrieval finished, losing the not-yet-retrieved backlog — is exactly what keeping one accumulating document prevents.

**A dive may stop at raw.** If the user decides the agent output is exploratory and won't be used for a deliverable, verification is optional. INDEX.md marks the dive as `raw only — not for citation`. The audit trail is still preserved.

---

## The eight-step workflow

The workflow is described below as eight numbered steps. Before the steps themselves, two pieces of structural discipline that frame how the steps are run:

### Operating pattern: five chats, five roles

The workflow is run across **five separate chat sessions**, each owning a distinct role and a distinct file output. This is the recommended pattern; the step descriptions below name which chat owns each step.

| Chat | Role | Owns | Produces |
|---|---|---|---|
| 1 | **Drafter** | Step 1 (prompt drafting and filing the prompt) | `YYYYMMDD_HHMM_prompt.md` |
| 2 | **Researcher** (the deep-research agent — Claude Research in this project) | Steps 2 and 3 (running the dive, filing the raw output and the source table) | `YYYYMMDD_HHMM_raw.md` and `YYYYMMDD_HHMM_retrieval.md` (table 1) |
| 3 | **Retriever** | Steps 4 and 5 (the held and completeness checks on table 1 as its first action, then iterative-pass web retrieval with the user, run in the browser, claude.ai web) | appends the check, the pass tables + residual list to `YYYYMMDD_HHMM_retrieval.md` (no separate file) |
| 4 | **Source processor** | Step 6 (papers protocol on academic sources first, then document-processing protocol on non-paper sources) | per-paper outputs (papers protocol) and per-document outputs (document-processing protocol) |
| 5 | **Verifier** | Step 7 (writing the two-table verification against the dive's declared source folders) | `YYYYMMDD_HHMM_verification.md` — the only citable artifact |

The separation is not a workaround; it is the discipline. Each chat sees only the information it needs to do its job, and crucially, **the verifier in chat 5 does not know what the drafter in chat 1 expected to find.** Co-locating drafting and verification in one chat biases the verification toward "did the agent answer the prompt" rather than "do the claims hold against primary sources." The five-chat split forecloses that bias by construction.

**The file system is the contract between chats.** Each chat opens fresh, reads what its predecessors filed, and writes what its successors need. No chat depends on remembered context from another chat.

For the avoidance of doubt: this project's researcher chat is always Claude Research. The pattern is platform-agnostic in principle (any deep-research agent could play the role); in this project, Claude Research is the standing choice.

**The research tool locks the chat.** With Advanced Research switched on in claude.ai, the researcher chat can use the research tool and nothing else: no GitHub, no `CLAUDE.md`, no skill read, no look at the literature home. So chat 2 runs in two moves, in the project that has access to the repo: with research **on**, it launches the dive from the prompt the drafter finished at Step 1, reading nothing first (everything the dive needs is in the prompt and its handoff packet); when the dive closes, research goes **off** so the chat can reach the repo and file the raw output and the retrieval doc (Step 3). Two consequences run through the steps below. The prompt the agent runs assumes no repo access, so it carries nothing the agent would have to look up there (Step 1: no exclusion list). And everything that needs the repo, the duplicate check included, happens in a chat that can read it (Step 4, the retriever).
### Session-start ritual: check what's filed before doing your step

Each chat (chats 2–5) opens fresh and depends on prior chats having filed their artifacts. The session-start ritual is: read what should be there, name what's missing, and complain before doing anything else. The ritual is **not a block** — the user can override — but the override is logged (see Workflow notes and Cross-dive register sections below), not waved through.

**Per-chat expectations:**

| Chat opening | Should already exist in the repo | Reads from prompt header | Must not read |
|---|---|---|---|
| Researcher (chat 2) — checked at the filing moment, after research is switched off, never before the launch | `_prompt.md` filed by drafter; INDEX row at `prompt drafted — not yet run` | Dive ID, Topic | — (the researcher consumes the full prompt; it runs the dive) |
| Retriever (chat 3) | All researcher artifacts: `_raw.md` and `_retrieval.md` (with table 1 filed); INDEX row at `raw only — not for citation` | Source folders (the eventual homes; retrieved originals are staged in workspace/staging/ first) | The prompt body (header fields only); `INDEX.md` beyond the dive's Status cell |
| Source processor (chat 4) | The worked `_retrieval.md` (table 1, the held check, pass tables, residual list); the retrieved originals staged in workspace/staging/ (the repo's intake funnel) | Source folders (knows which folders to process and in what order — papers first, documents second) | `_raw.md`, ever; the prompt body (header fields only) — see Step 6; `INDEX.md` beyond the dive's Status cell |
| Verifier (chat 5) | All of the above, plus papers processed (papers protocol) and documents processed (document-processing protocol) | Source folders (knows which folders define the verification universe); Dive type (knows which Step 7 synthesis template applies) | The prompt body (header fields only); `INDEX.md` beyond the dive's Status cell (it updates that cell and reads nothing else in the row) |

The "Must not read" column states each chat's insulation positionally, so a fresh chat can see what is off-limits in the same place it sees what should exist — a list of files it must not open, not guidance about approach.

**Header, not body.** The "reads from prompt header" column is exact. Downstream chats read the prompt file's **metadata block** — the workflow configuration the pipeline needs to run — and never the prompt **body**, which carries the research question, the decomposition, and everything else that says what the drafter was hoping to find. **The header's bound is mechanical:** read from the top of the file to the first `---` divider and stop there, never by a line count (a fixed line count can run past the metadata block into the research question). That line is what lets the verifier read `Source folders` and `Dive type` without breaching the insulation Step 7 depends on: both are facts about how this dive is wired, not about what it expected. A chat that finds itself reading the prompt body to work out what the drafter was looking for has crossed the line, and should stop and log the crossing rather than continue.

**Header-versus-body is a channel rule, not just a layout rule.** In practice a second channel exists between chats: the user relays a handoff brief, written by the chat that is finishing, into the chat that follows — and that prose arrives before any repo read. Whatever reaches a downstream chat, by file or by relay, is subject to the same split. A relayed handoff may carry **workflow configuration** (dive type, source folders, which artifacts exist, which files not to read, standing operator rulings) and may **point** at cross-dive evidence ("read the cross-dive findings file, adjudicate what it records"); it must not carry the *reading* of that evidence, an expected direction, a prediction about which lesson will promote, or a nomination of the dive's likely problem. **The chat that writes a downstream chat's handoff writes configuration and pointers, never findings.** And where the operator relays the header's fields verbatim, the downstream chat need not open the prompt file at all — strictly better than positional protection, and the preferred arrangement; reading the header in place is the fallback where no relay happened.

**The ritual, step by step:**

1. The chat reads its expected prior artifacts from the repo.
2. If everything is present → proceed normally with the chat's step.
3. If something is missing → the chat **complains**, names exactly what's missing, and asks the user: *deliberate override, or accident?*
   - **Accident** → the user goes back to the missing step (or another chat) and completes it. This chat does not proceed.
   - **Deliberate override** → the user explicitly signals the override (e.g., "yes, override, I want to start the verifier with partial papers"). The chat proceeds, **and** triggers the workflow-notes-and-to-do logging (see the Workflow notes section below).

**The user-side override marker (optional shortcut).** The user can pre-empt the complaint by including a phrase like `[override: <reason>]` in their first message. The chat skips the complaint step, but **still does the bookkeeping** — the override marker reduces the prompt friction, not the logging discipline. The whole point is that overrides are visible later, not invisible.

**Why complain rather than block.** The user has legitimate reasons to do steps out of order — a quick verifier read against partial papers, a retriever run started before the researcher's filing has fully landed, etc. Blocking would be paternalistic and would push them to work around the chat. Complaining-and-logging makes the cost of the skip visible without removing their authority.

### Step 1 — Prompt drafting

**Owned by the drafter chat (chat 1).** Claude and the user co-draft the deep-research prompt iteratively. A clean prompt has:

- **A clear research question** (one sentence, no compound questions).
- **A declared dive type** — `evidence synthesis` or `discovery (inventory)`. An evidence-synthesis dive asks the agent what the literature or the record *shows*; a discovery dive asks it what *exists*. The two produce different verification work and different syntheses, and Steps 7 and 8 fork on the declared type. **The drafter declares it in two places:** the prompt file's header block, where chats 2–5 read it, and the prompt body, where the agent reads it. Neither substitutes for the other. The header declaration is what lets every downstream chat read the dive the same way; without it the verifier has to infer the type from the raw output's opening lines, which is a small insulation breach and an avoidable one. If a dive is genuinely both, declare the **dominant** type and note the mix in one line — the fork runs on the declared type.
- **Scoped geography or scope** (which countries, which time period, which type of evidence).
- **Explicit quality criteria** (peer-reviewed journals, working papers from a defined list of institutions, etc.).
- **No exclusion list.** The prompt does not list the papers already held. The agent cannot read the repo, so a list written as a pointer does nothing, and a list written out in full anchors the agent: it reads the excluded cluster as a region to avoid and under-surfaces in-scope material next to it. Duplicate avoidance runs after the dive instead, as the retriever's held check on table 1 (Step 4), which also stops anything held from being retrieved twice. *(Documented predecessor, to kit v6.9: the prompt carried an exclusion list stated as duplicate-avoidance only.)*
- **An honest-picture instruction** ("Report counter-evidence and null results as prominently as supporting evidence. Where evidence is mixed or weak, say so explicitly. Do not pad the response to make findings appear more conclusive than they are.").
- **Mitigations for known failure modes**, drawn from two registers read together: the kit's **Known agent failure modes** table (the hoisted, cross-project set; "Cross-project hoisting" below), and the repo's own `LESSONS.md` (see below). The kit table is what a lesson learned in one repo looks like when it reaches every other; a pattern in both is cited once.
- **A window defined on the date that answers the question.** A publication window ("published since 1 January 2024") and an evidence window ("reporting on the period since 1 January 2024") are different filters, and a document can pass one while failing the other — a report published inside the window on fieldwork conducted two years earlier is *new* by publication and *stale* by evidence. Where the dive's question is about **currency** — what the state of things is now — either define the window on evidence date, or define it on publication **and** require every entry to carry its fieldwork or data-collection date alongside its publication date. An agent that applies a publication window correctly will still return stale evidence if a publication window is what it was given; this is a prompt-design failure, not an agent failure, and no verification pass will catch it as the latter.
- **Two physically separate lists wherever a category must not collapse into its neighbour.** An instruction of the form "list these separately, marked as such" asks the agent to hold a convention across a long output, and conventions get applied to the first case and dropped by the tenth. Where the distinction is load-bearing — found versus referenced-but-not-located, published versus forthcoming, retrieved versus inferred — specify it in the Deliverables section as **two separately-headed lists**, not as a marker inside one list. This is the same reasoning the verification body already runs on (see "Body — claim-by-claim tables"): two visibly-separate tables make absences visible, where a merged table with a type column can look complete while silently dropping a category. The prompt end of the pipeline needs the same structural guard as the verification end, and for the same reason.
- **A Deliverables section specifying two outputs and a multi-candidate sources table.** The agent is instructed to produce (a) its synthesis report and (b) a "Sources cited" table with one row per source. The table has at least these columns: claim supported (which part of the research question the source backs) · citation (author, year, title) · link candidate 1 (journal / DOI) · link candidate 2 (working paper) · link candidate 3 (institutional repository) · link candidate 4 (other — preprint server, archived PDF, blog post). The agent provides *all* link candidates it can find for each source, not just one. The multi-candidate format is what the retriever chat (chat 3) needs to work the table in passes when paywalls block the first-choice link.

**Read `LESSONS.md` before drafting.** This is the load-bearing read. Every accumulated lesson from past dives is a prompt-engineering response to a known agent failure mode. Open the file, surface any patterns relevant to the current topic or to the agent platform being used, and bake the mitigations into the prompt being drafted. If the same pattern has surfaced repeatedly, the mitigation may need strengthening — flag that to the user.

**Also read `WORKFLOW_SKIPS.md` before drafting.** Same session-start moment as the `LESSONS.md` read; see the Cross-dive register section below for how patterns get surfaced.

Iterate on the prompt with the user until they approve it. The approved prompt gets filed at the end of Step 1 (not at Step 3, despite what older one-operator versions of this workflow assumed — in the five-chat pattern, the drafter files its own output before handing off).

**Source folders question (workflow-configuration, not prompt content).** Before filing the prompt, the drafter chat asks the user which folders this dive's sources will be processed into and verified against. The skill does **not** assume a folder: it reads the repo's `FOLDER_MAP`s — the per-folder purpose index every repo carries regardless of archetype — and proposes the home they indicate for academic sources (where the repo keeps literature) plus any non-paper folder, then confirms. Phrasing: *"This dive's academic sources will go to the repo's literature home, which the `FOLDER_MAP`s put at `<suggested>`; any non-paper sources to `<suggested>`. Confirm or correct."* This is a one-question check, answered per dive. The answer goes in the prompt file's header `Source folders` field (see header template below). It does **not** go into the prompt body the agent sees — the agent doesn't need to know about the repo's folder structure; the question exists so downstream chats know where to put files and where to check. Reading the `FOLDER_MAP`s keeps this skill blind to the archetype: do **not** hardcode a folder, do **not** scan the raw tree to guess, and do **not** read the archetype layer (`archetype_conventions.md` or an archetype spec) at runtime.

If the repo's maps are thin or empty (a new or migration-gap repo) and don't show where literature or non-paper material lives, the suggestion degrades to asking the user outright — flag the gap, never silently hardcode a home. A declared folder that doesn't yet exist is created when the retriever (or source processor) first writes to it; if a needed home isn't represented in the maps at all, surface that rather than inventing structure.

#### Prompt file header template

The prompt file (`<YYYYMMDD_HHMM>_prompt.md`) starts with a metadata block that downstream chats read at session start:

```markdown
# Deep-Research Prompt — <one-line dive title>

**Dive ID:** <YYYYMMDD_HHMM>
**Topic:** <topic_slug>
**Dive type:** <evidence synthesis | discovery (inventory)> — declared per Step 1; Steps 7 and 8 fork on it
**Agent platform:** Claude Research
**Drafted:** <YYYY-MM-DD> (drafter chat)
**Skill:** `skills/agent_research_verification_skill.md` Step 1
**Source folders:** <comma-separated list of the folders this dive's sources are processed into and verified against — the repo's literature home plus any non-paper folders, as declared per Step 1's source-folders question; read from the repo's `FOLDER_MAP`s, not assumed>

---

[prompt body — research question, decomposition, deliverables, etc.]

---

[Filing instructions for the researcher chat — see Step 2 handoff packet]
```

**The metadata block carries workflow configuration and nothing else.** Every field above is a fact about how the dive is *wired* — which folders, which type, which platform, which stamp — and that is precisely what makes it safe for chats 2–5 to read (see "Header, not body" above). **Do not put the drafter's reasoning in it**, however it is labelled: not the hypothesis the dive is testing, not the ladder of prior findings the question sits on, not a "why this dive exists" note addressed to downstream chats. Those belong below the divider with the prompt body, and nowhere a downstream chat reads: not in the dive's `INDEX.md` row either, whose Angle, Notes and topic description carry scope and workflow facts only (INDEX.md structure below), because the verifier updates that row at Step 7.

The failure this prevents is quiet and it lands on the last chat in the pipeline. A block explaining what the drafter expects the answer to be, sitting above the divider and marked as context for downstream chats, reads as something the verifier is *supposed* to consume — so it gets read, and the clean-room property Step 7 depends on is gone before the first claim is checked. Labelling the block as non-prompt context does not help: the verifier's protection is positional, not a matter of intent, which is the whole reason the rule is stated as header-versus-body rather than as a judgment call.
**INDEX.md gets a row added in the same commit** as filing the prompt. Status: `prompt drafted — not yet run`. See INDEX.md structure below for the row format.

### Step 2 — Run the dive

**Owned by the researcher chat (chat 2 — Claude Research in this project).** The user opens the chat in the project that has access to the repo, switches Advanced Research **on** and pastes the prompt (with the handoff packet appended, see below) to launch the dive; nothing is read before the launch, since the prompt was finished at Step 1. When the dive closes they switch research **off**, and the chat files (Step 3). This happens **outside** the drafter chat; the drafter does not run dives.

#### Drafter → Researcher handoff packet

Because the researcher chat runs as a separate session and files its own output, the drafter chat hands the researcher a packet of filing instructions appended to the prompt itself. The packet specifies the shared dive timestamp, the destination paths, the header to prepend, and the INDEX.md update.

The timestamp is set by the drafter chat at the time of prompt filing (`YYYYMMDD_HHMM`), and the researcher chat **reuses that exact stamp** for both files it produces, so the prompt, raw output, and retrieval doc all sort adjacent in the topic folder. The researcher does not stamp the files with its own run time.

**Template (paste at the end of the prompt before handing it off):**

````markdown
**Filing instructions (for the researcher chat).**

While Advanced Research is on, this chat can reach nothing but the research tool: run the dive, then file with research switched off. Before filing, check that `<YYYYMMDD_HHMM>_prompt.md` is in the topic folder and the `INDEX.md` row reads `prompt drafted — not yet run`; if either is missing, say so to the user, and on their word file the prompt from this chat and add the row in the same commit as the output. When you produce the output, file two documents at the topic folder, both stamped with this dive's ID:

- `workspace/agent_outputs/<topic_slug>/<YYYYMMDD_HHMM>_raw.md` — the synthesis report.
- `workspace/agent_outputs/<topic_slug>/<YYYYMMDD_HHMM>_retrieval.md` — the **source table (table 1)**: the Sources cited table, every source × every candidate link (multi-candidate links per source; see the Deliverables section of this prompt for the column spec). This is the first, immutable section of the dive's retrieval doc — the retriever appends the pass tables and the residual list *below* it. Do not edit or delete table 1 later; only append beneath it.

Prepend this header to the raw file (the body below it is the untouched synthesis):

```markdown
---
**Source:** Claude Research
**Date run:** YYYY-MM-DD HH:MM
**Prompt:** [<YYYYMMDD_HHMM>_prompt.md](<YYYYMMDD_HHMM>_prompt.md)
**Retrieval doc:** [<YYYYMMDD_HHMM>_retrieval.md](<YYYYMMDD_HHMM>_retrieval.md)
**Status:** raw — not for citation in deliverables. Verification produces the citable input.
---
```

In the same commit, update `workspace/agent_outputs/INDEX.md` under the `<topic_slug>` topic: change Status from `prompt drafted — not yet run` to `raw only — not for citation`.

**Completion checklist — you are not done until all four hold:** (1) `_raw.md` filed with its header; (2) `_retrieval.md` filed with table 1 and the append-only notice; (3) the `INDEX.md` status flipped; (4) all of it in one commit. Producing the synthesis in chat and stopping there is the standing failure this checklist exists to prevent — the dive is not filed until the files are in the repo.

Repo access mechanics per `github_api_workflow_skill.md` (the repo-access authority): a claude.ai web chat uses the GitHub REST API (git push is blocked; the recipes per `github_api_workflow_skill.md`'s web branch); a Cowork session uses plain git.
````

When the user returns to a new working chat to start the retriever (chat 3) phase, advance to Step 4, the retriever's first action. (Step 3 is owned by the researcher chat and has already happened by then.)

### Step 3 — File the raw output

**Owned by the researcher chat (chat 2).** The unedited synthesis is filed at `<AGENT_OUTPUTS_FOLDER>/<topic_slug>/<YYYYMMDD_HHMM>_raw.md`, with the header block from the handoff packet prepended. INDEX.md is updated to status `raw only — not for citation` in the same commit.

If this is a re-dive on a topic that already has earlier dives, the researcher chat (or the drafter chat returning to review) considers whether INDEX.md should mark any earlier dive as `superseded`. Propose the supersession to the user — don't apply silently. Sometimes the new dive is a different angle, not a replacement.

### Step 4 — Table 1 arrives with the raw; the retriever checks it first

**Table 1 is produced by the researcher (chat 2); the two checks on it are the retriever's (chat 3) first action.** The source table is filed as **table 1** of the dive's retrieval doc (`<YYYYMMDD_HHMM>_retrieval.md`). There is no separate extract-links step performed by the drafter — the link list is part of the researcher's deliverable, specified in the prompt's Deliverables section (per Step 1's checklist).

The retriever opens with two checks, before any link is tried, and appends both below table 1 (never inside it):

1. **The held check.** Every table-1 row is checked against what the project already holds, and the rows already held are recorded (which row, where it is held), so none is retrieved again. **A work is held when its PDF is in the literature home, or when it is on a shared literature library's list, if you keep one** (a `PAPERS_INDEX.md` in another repo of yours). A cite key in a `.bib` file or a mention in a summary is not holding; anything not held is retrieved. Where the session cannot reach that list, the check says so and names the rows the user checks by hand.
2. **The completeness check.** The retriever scans the raw output for every work it cites that has no row in table 1 (a "cited in text, no table row" note from the researcher counts). Each one is run through the held check, and **every work not held joins the pass 1 list**. A claim with no source at all is a candidate for the `fabricated` or `unverifiable` verdict at Step 7 and is noted so no pass is spent on a source that does not exist.

*(Documented predecessor, to kit v6.9: the duplicate check sat in the prompt as an exclusion list, and the completeness check had no route into retrieval, so a work it found was noted and dropped.)*

### Step 5 — Retrieve originals

**Owned by the retriever chat (chat 3) in the five-chat pattern.** This is iterative work between the user and a fresh chat dedicated to retrieval, after Step 4's two checks; see the retrieval pass workflow below. The retrieval runs in the browser (claude.ai web), where the user downloads the files.

Paywalled items, broken links, and "no link found" entries are flagged as unretrievable but are **not blockers**. The verification step (Step 7) will mark claims from unretrievable sources as `unverifiable` — that is honest accounting, not failure.

#### The retrieval pass workflow

Retrieval proceeds in **passes**, working **table 1** (the multi-candidate source table) of the dive's retrieval doc (`_retrieval.md`), less the rows the held check found held and plus the works the completeness check added. Each pass appends a new "still missing" table *below* the last, so the doc accumulates the whole narrowing — never overwrite table 1 or a prior pass table.

**Pass 1:** The user attempts to retrieve every source on the pass 1 list using its **first link** (column 1, journal / DOI; for a work the completeness check added, the first link the retriever finds). Whatever they get they drop into workspace/staging/ (the repo's intake funnel — the retriever does not file into the literature home or documents folder itself; the source processor does that at Step 6). They return to the retriever chat and report back: *"I tried column 1, here's what I got."* The chat checks workspace/staging/ against table 1 and **appends a fresh "still missing" table** to `_retrieval.md`, with the column-1 links struck through.

**Pass 2 and later:** The user attempts each still-missing source using **its next available link**, whichever column that is, not a fixed column for all: a source that carries link 1 only has no column 2, and a strict column pass skips it. They return to the chat. Chat builds the next fresh table. The passes continue until either everything retrievable is in the destination folders or every remaining source has run out of links and is confirmed unretrievable. *(Documented predecessor, to kit v6.9: pass N used column N for every source, which skipped any source carrying link 1 only.)*

**The chat is the delivery surface; the doc is the record.** At the start of each pass, the retriever presents the pass's links **in chat** — one per source, as clickable links, flagging which are expected to be open-access — rather than leaving the user to copy URLs out of table 1's cells. `_retrieval.md` records the pass; it is not how the pass reaches them. The deliverable of a link pass is a link that downloads a file, and a hand-off that requires the reader to hunt is a hand-off of work.

**A bibliographic record page is a valid link candidate.** A record page in a working-paper archive is not the destination, but it holds the download: on a working-paper record follow its full-text link, which resolves to the PDF on the series host; on an article record use the publisher link or the listed open versions of the same work. The retriever states in the row which link on the record page serves the file, so the reader clicks once. An archive handle is often the most stable route to a working paper: series hosts move and the handle does not. A record treated as the destination yields no file.

**Substitution decisions during the passes.** Sometimes the user retrieves a working paper version and decides to **cite the published version** anyway (e.g., the working paper has the same content but the deliverable's audience expects the journal citation). This is a legitimate choice and goes into the retrieval doc as a substitution note (in the pass table or the residual list): *retrieved working paper, cited as journal version*. The verifier (chat 5) reads this and accounts for it in the verification table — a verdict of `confirmed` against a working-paper retrieval is still a confirmation of the cited claim, as long as the working paper and the journal version match on the verified point.

**End of retrieval.** The retriever closes the doc with a **residual list** at the foot of `YYYYMMDD_HHMM_retrieval.md`: one row per source that was *not* retrieved, with its reason (`paywalled` / `broken link` / `not found`), plus, for the sources that were retrieved, which column's link succeeded, which version was retrieved (held in workspace/staging/ pending Step-6 processing), and which version will be cited if different (substitution notes). The full doc — table 1, the pass tables, the residual list — is what the verifier reads in Step 7 to know *what kind of unverifiability* a missing source represents, and is the kept backlog the user returns to when a paywalled source later becomes reachable.

### Step 6 — Process retrieved sources through the project's protocols

**Owned by the source-processor chat (chat 4) in the five-chat pattern.** A fresh chat opens, sees the retrieval doc and the retrieved originals in workspace/staging/ (the repo's intake funnel), and runs each through the project's protocols on its own terms — the protocols file each source out of staging into the dive's declared source folders — without exposure to the dive's prompt or framing. This insulation is deliberate: sources are processed on their content, not on whether the agent's claim about them was right.

**Do-not-read list for this chat: `_raw.md`, ever; `_prompt.md`, metadata header only.** These are files not to open, not guidance about approach. The topic folder puts both alongside the `_retrieval.md` this chat needs, and the insulation here matters as much as at Step 7, for a compounding reason: the per-source summaries this chat writes become the ground truth the verifier checks the agent against, so a processor that has read the agent's framing first turns the verification into a check of the agent against a mirror of itself — and the breach is invisible afterwards, because a contaminated summary looks exactly like a clean one.

**The topic slug is framing too.** A slug names what the dive is about, so it steers whoever reads it. Any note in a per-source summary that records how the source reached the repo carries the **dive ID only** (`<YYYYMMDD_HHMM>`), never the topic slug; a brief this chat gives a drafting subagent names no topic; and where this chat's prompt (or chat 5's) asks for the STATUS check, it names the STATUS entry that states the dive's question as one to skip.
**Sequential, not interleaved — papers first, documents second.**

1. The chat first runs the project's papers protocol (`<PAPERS_PROTOCOL_SKILL>`, default `materials_processing_skill.md`) on every new academic source the retriever filed in the dive's declared literature home. (That protocol is itself archetype-blind — it reads the repo's `FOLDER_MAP`s to place and index each paper — so this skill names no folder.) This pass completes fully before the next protocol starts.
2. If the dive has non-paper sources, the chat then runs the project's document-processing protocol (`<DOCUMENT_PROTOCOL_SKILL>`, default `document_processing_skill.md`) on every new non-paper source in the dive's declared documents folder.

Sequencing matters because the two protocols have different outputs (different summary structures, different indexes, different BibTeX entry types). Running them sequentially keeps the chat's working memory clean and avoids cross-contamination of output formats.

This is a **hand-off, not duplication**. This skill does not re-describe how papers or documents are processed. Read the relevant project protocol and follow it.

When the sources are processed and in their destination folders (with index entries and per-source outputs in place), advance to Step 7.

### Step 7 — Verification (second pass)

**Owned by the verifier chat (chat 5) in the five-chat pattern.** The verifier opens fresh against the repo state: it reads `_raw.md`, `_retrieval.md` (table 1, the pass tables, and the residual list), and the dive's processed sources in the declared source folders. It does **not** see the prompt and is **not** told what the drafter expected to find. The verification is a clean-room read against primary sources.

**The verifier checks claims only against the dive's declared source folders.** A claim whose source is not in those folders is `unverifiable` — even if the source exists on the open web. The verifier does not retrieve sources mid-verification; retrieval and protocol-processing happen at Steps 5 and 6, in chats 3 and 4, before the verifier chat opens. By the time the verifier sits down, the ground-truth library is closed.

The retrieval doc's residual list distinguishes *kinds* of unverifiability — paywalled, broken link, not found, working-paper-substituted-for-journal — so when the verifier marks a claim `unverifiable`, the synthesis section names which kind. "Unverifiable because the source was paywalled" is different from "unverifiable because no source was retrievable for this claim" and the deliverable downstream may care about the distinction.

**Verifier's session-start confirmation.** Even though the prompt header carries the `Source folders` field, the verifier chat explicitly confirms with the user at session start which folder holds the non-paper documents for this dive. The header is the default; the confirmation is the discipline. Fresh chats don't assume.

**The verifier reads the dive type from the prompt header** (see "Header, not body" above) and applies the matching synthesis template. It does not infer the type from the raw output. If the header carries no dive type — an older dive, or a drafter who skipped the declaration — the verifier asks the user rather than inferring, and logs the gap per the session-start ritual.

For each **headline claim** in the agent's raw output — a finding, a magnitude, a causal statement, anything that could appear in a deliverable — the verification asks:

- Did the agent represent the source accurately?
- Are magnitudes (effect sizes, sample sizes, time periods) correct?
- Is the identification strategy described correctly?
- Are claims about "no evidence exists" defensible?

**Headline claims only.** The verification tables are not exhaustive. Background context, definitions, and framing don't need rows. The principle: if a claim isn't worth a row in the verification table, it isn't worth citing in a deliverable.

Where a claim cannot be verified because the source wasn't retrievable (or wasn't processed into the dive's declared folders), mark it `unverifiable`. That is honest accounting — not confirmation.

**The whole-document rule (contested readings escalate; the operator adjudicates).** Two triggers, either sufficient: the source appears to contradict itself across passages, or the passage the claim list points at reads **narrower** than the claim cited to it. Both are the same signal — the passage does not sit comfortably under the claim. When either fires, the verifier does **not** record a verdict from the pointed-at passage. Instead:

- **Read the whole source** — the full extract, or the original where the extract is partial. Some extracts are deliberately operative-provisions-only; a whole read of a partial extract reproduces the narrow-reading failure this rule exists to prevent, so check the extract's own stated coverage before trusting it as "the whole document."
- **A garbled table is not a silent source.** Before recording a figure as absent from a source whose extraction has lost or mangled a table — the commonest way an extraction goes partial without announcing it, because the surrounding narrative survives and the document reads complete — attempt to **reconstruct the row from the source's own prose**: where the other values in the same row are stated narratively and match, the row's identity is fixed and the figure is verifiable. Where reconstruction fails, the cell says the absence is an **extraction limit, not a source silence** — `unverifiable` on an extraction limit, a different kind of unverifiability from "not retrieved." A verifier that cannot see a figure otherwise concludes the figure is absent, and "absent from the source" reads as "invented by the agent" — the same over-reporting failure this rule exists to prevent, arriving through extraction quality rather than passage selection.
- **Weigh the readings by independent structural positions**, not by which passage the claim list pointed at: executive summary, body treatment, recommendations, footnotes, annexes. A reading carried in one subordinate clause and contradicted by the summary, the body and the recommendations is not a genuine ambiguity — it is a concessive outlier, recorded as such rather than as an inconsistent source. Count positions by their physical place in the document, never by the labels a derived layer gives them: two labels can name one paragraph, and a double-count can invert the weighing.
- **Escalate, don't decide.** The verifier records both readings in the claim's row, states which reading the whole document carries and why (the structural weighing), and leaves the verdict cell blank. Escalations are batched and put to the user at the end of the pass, not claim by claim.
- **The user adjudicates on citability, not preference.** The question they answer is what the source, read whole, actually supports and what can honestly be cited — the same honesty standard the whole workflow runs on, applied by the operator. The verdict they set is one of the existing six values; the cell keeps the two readings and gains an adjudication note (*escalated per whole-document rule; adjudicated by the user, <date>, on <stated basis>*), so a later reader can distinguish verifier-recorded verdicts from adjudicated ones. Provenance, not restriction, is what protects the clean-room property here.

Why the rule exists: a pass tuned to catch dropped qualifiers systematically **over-reports when it reads narrowly** — a narrow passage always makes a claim look inflated — and the verifier's own weighing can fail too. Escalation answers both failure modes at once.

See the **Verification document structure** section below for the full template, including the two-table body structure.

After the verification document is produced:
- **INDEX.md status flipped** to `verified` in the same commit. (`INDEX.md` here is this skill's own workflow tracker — see below.)
- **The verified dive is registered in the repo's deep-dives catalog** in the same commit — see "Registering the verified dive in the repo's catalog" below. Only verified dives register; a raw dive earns no catalog row.
- **LESSONS.md updated** if a new error pattern surfaces, or if an existing pattern accumulates a third instance. See the LESSONS.md discipline section below.

### Step 8 — The verification document is the citable input

After Step 7, the verification document is the **only** artifact from this dive that can be cited in deliverables. The raw output remains as audit trail.

When drafting a deliverable that uses findings from this dive:
- **On an evidence-synthesis dive, cite the verification doc as the synthesis source.** On a **discovery dive there is no synthesis to cite** — the verification doc is a finding aid, establishing which documents are real, correctly described and reachable, not what they show. Citing it for an empirical claim is a category error. Point at it to explain where the originals came from and what could not be established; cite the originals for everything else.
- Cite the underlying papers (from the repo's literature home) and documents (from the dive's declared documents folder) for the empirical claims themselves, using the project's normal citation conventions.
- Never cite the raw agent output. If you find yourself wanting to ("the agent said X"), the right move is to verify the claim against the original source and write the verified version.

### Registering the verified dive in the repo's catalog

There are **two index surfaces**, and this skill writes to both at different moments. Keeping them distinct is the point:

- **This skill's workflow tracker** — `<AGENT_OUTPUTS_INDEX>` (default `workspace/agent_outputs/INDEX.md`). The skill **owns** this file (it lives in the skill's own `workspace/agent_outputs/` folder). It tracks **every dive at every status** — `prompt drafted`, `raw only`, `verification in progress`, `verified`, `superseded` — and is the operational ledger for running the workflow. It is *not* part of the repo's by-subject catalog, and it holds rows (raw, prompt-drafted) that the catalog must not.
- **The repo's deep-dives catalog** — the repo's own by-subject index of **verified** deep-research runs, which the rest of the repo's retrieval points at, so a verified dive is findable by subject alongside the repo's papers, notes, and other materials rather than buried inside `agent_outputs/`. This is **not** owned or named by this skill.

On verification completion, register the verified dive in that repo catalog. **Do this archetype-blind, exactly as the papers protocol places papers:** read the repo's `FOLDER_MAP`s to find the existing deep-dives / verified-output index (the root map's root-documents block names it), add the dive in the header row that index carries (`typed_index_template.md`: `Dive · About · Verified · Verification` — the dive id, the question in Claude's words with a subject already named in a row keeping its words, the verification date, the verification document's path), in the section its head says it takes, and confirm placement before writing. **Never name a specific index file and never read the archetype layer (`archetype_conventions.md` or an archetype spec) at runtime** — repo types carry this differently (a research repo carries a named deep-dives index; a NONE repo names the catalog it uses; the skill stays blind to which). Register **only verified dives** — the citability rule and the catalog's "verified only" rule are the same line. The registration is batched into the **same commit** as the verification doc and the workflow-tracker status flip.

If the repo's maps show no deep-dives catalog at all (a thin/new repo, or a repo whose type doesn't carry one), **degrade to asking the user** and flag the gap — do not invent a catalog or hardcode one. The skill's own workflow tracker still records the dive regardless; what's missing in that case is only the repo-catalog cross-reference, which is a setup/migration gap to surface, not to paper over.

---

## Workflow notes and to-do logging (lazy artifact)

When a chat detects a skip and the user overrides (per the session-start ritual above), or when any step is done out of order, the chat creates or appends to a dive-specific **workflow notes** file:

`workspace/agent_outputs/<topic_slug>/<YYYYMMDD_HHMM>_workflow_notes.md`

This file is **lazy**: it exists only for dives where something was skipped or done out of order. Dives that ran cleanly have no workflow notes file. Its presence in the topic folder is itself a signal that the dive has bookkeeping that needs attention later.

**Format** — one entry per skip event:

```markdown
## <ISO timestamp> — <chat that detected the skip>

**What was skipped:** [The artifact or step that was missing when this chat opened.]

**Override or accident:** [Deliberate override / the user proceeded after being prompted / chat proceeded after explicit override marker.]

**Reason given (if any):** [the user's stated reason, if they gave one.]

**Follow-up to-do:** [What needs to happen to close the gap — e.g., "complete the retrieval log retroactively from chat history," "re-run papers processor against the missing sources."]

**Queue entry:** [Pointer to the corresponding row in `workdesk/INDEX.md`.]
```

**Paired queue entry.** In the same write, the chat adds a row to `workdesk/INDEX.md`, the pending-actions queue (`structure_conventions.md`):

```markdown
| [Topic slug / dive timestamp] — [what was skipped, one line] | do | workspace/agent_outputs/<topic_slug>/<YYYYMMDD_HHMM>_workflow_notes.md | YYYY-MM-DD | session | waiting |
```

The queue row is the durable surface — it lives where everything else waiting on the user lives, so the gap doesn't get lost in `agent_outputs/`'s structure.

**When the follow-up is closed.** The row clears at the session close-out's queue reconciliation (`project_tracker_skill.md`) once the gap is resolved; the user either (a) leaves the workflow_notes entry as audit trail, or (b) adds a closing note to the workflow_notes file describing how the gap was resolved. Either is fine.

---

## Cross-dive pattern detection: WORKFLOW_SKIPS.md

A single register at `<AGENT_OUTPUTS_SKIPS>` (default `workspace/agent_outputs/WORKFLOW_SKIPS.md`) aggregates every skip event across every dive. The dive-level `_workflow_notes.md` files are the human-readable narrative; this register is the structured cross-dive data.

**Why a separate register.** Pattern detection — "have I skipped this step on three or more dives?" — should be a single file-read, not a scan across N dives' workflow notes. The register mirrors how `LESSONS.md` works for prompt-engineering patterns: one file collecting cross-dive signal. **It is created up front with `INDEX.md` and `LESSONS.md`** (the skill's triple, `structure_conventions.md`'s standing-documents table; the conformance pass creates it where missing), so the session-start read below always finds the file, with no rows until the first skip. *(Documented predecessor, to v6.5: born on use at the first skip's commit.)*

**Format:**

```markdown
# Workflow Skips Register

*Cross-dive register of every workflow skip event. Patterns surface here (same step skipped on 3+ dives) before they show up as habits.*

---

| Dive | Chat | Step skipped | Reason | Resolved? | Workflow notes link |
|---|---|---|---|---|---|
| <topic> / <YYYY-MM-DD HH:MM> | <chat name> | <step skipped> | <one-line reason> | <✓ date / open> | [link](<topic>/<YYYYMMDD_HHMM>_workflow_notes.md) |
```

**When the register is written to.** Same commit as the workflow_notes file creation/append. The chat that's logging the skip writes both files atomically.

**Pattern surfacing — done at session start by any chat.**

When a chat reads `LESSONS.md` at session start (per Step 1's discipline), it **also** reads `WORKFLOW_SKIPS.md` and counts skip events per step. If any step has been skipped on **three or more dives**, the chat surfaces this to the user at the start of the session, before doing anything else:

> "Heads up — the retrieval log has been skipped on 4 dives now (<topic_1> / <date_1>, <topic_2> / <date_2>, …). This is a pattern, not a one-off. Worth looking at why this keeps happening: is the retrieval log harder to produce than the workflow assumes, or is it the kind of step that always gets skipped under time pressure? Either is fixable, but the fix is different."

The surfacing is **not a complaint** about the specific dive in front of the chat — it's a meta-observation about the workflow. The chat names the pattern and asks the user what to do; it doesn't refuse to proceed.

**What "the fix is different" means in practice:**
- *Step is harder than the workflow assumes* → revise the skill / the artifact format / the prompt so the step is cheaper to do.
- *Step gets skipped under time pressure* → strengthen the session-start complaint, or build a stricter pre-commit check, or accept the gap and adjust the verifier's expectations.

Both are legitimate responses. The register exists so the user has the data to choose between them rather than guessing.

The threshold of three matches the project-level "codify after the third repetition" rule (see Working Conventions in CLAUDE.md): recurrence beats triviality, and the third instance is when a one-off becomes a pattern.

---

## INDEX.md structure

`<AGENT_OUTPUTS_INDEX>` is a topic-grouped tracker for every dive in the project. It is **this skill's own workflow tracker** — the operational ledger that follows each dive through every status — and is distinct from the repo's by-subject deep-dives catalog (see "Registering the verified dive in the repo's catalog" above): the tracker holds all dives at all statuses; the catalog holds verified dives only.

### Top of file

```markdown
# Agent Research Index

*Audit trail and citability ledger for all deep-research dives in this project.*

**Citability rule:** Only `verified` dives are usable as sources in deliverables. Raw agent output is audit trail only.

**Status values:**
- `verified` — verification document exists; citable in deliverables.
- `raw only — not for citation` — prompt + raw output exist; no verification yet.
- `verification in progress` — verification started; not yet citable.
- `superseded` — a later dive replaces this one; kept for audit trail.
- `prompt drafted — not yet run` — prompt filed; agent dive pending (no raw output yet).

---

<!-- slot: catalog -->
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->
```

The per-topic sections below sit inside the `catalog` slot; the header above it is kit form,
regenerated at every propagation, and the file exists from the repo's birth as the folder's
standing document (`standing_documents_template.md`; the markers are
`structure_conventions.md`, "Slots and markers, one notation").

### Per topic

Each topic gets a `## <topic_slug>` heading, a one-sentence description, and a four-column table:

```markdown
## remote_work_productivity

*Evidence on how remote work affects productivity, and on employer responses.*

| Date | Angle | Status | Notes |
|---|---|---|---|
| 2026-09-20 09:00 | Refresh focused on two countries, studies published since 2024 | verified | Claude Research. Supersedes 2026-05-13 dive (narrower geographic scope). |
| 2026-05-13 14:30 | Initial dive — cross-country evidence on productivity effects | superseded | Claude Research. |
```

**Column conventions:**

- **Date:** `YYYY-MM-DD HH:MM`, human-readable, matches the timestamp on the dive's files.
- **Angle:** one sentence on the dive's **scope** (geography, period, kind of evidence), especially how it differs from prior dives on the same topic. This is the load-bearing column for finding the right past dive. It never states what the drafter expects to find, a hypothesis, or the channel the plan hopes for.
- **Status:** one of the five legend values.
- **Notes:** workflow facts only: the agent platform; if superseding an earlier dive, which one and why; any major retrieval gaps. Never the drafter's reasoning.

**Topic description.** One sentence above the table per topic, stating scope under the same rule as Angle. Cheap; disambiguates short slugs. If the scope of a topic drifts across dives, revise the description.

**Why the tracker is kept neutral.** The verifier updates the dive's row at Step 7, and every downstream chat sees the tracker while doing its bookkeeping, so whatever the row says is read. Chats 3 to 5 read the tracker by the dive's Status cell only (the session-start table), and the row carries nothing that would steer them if they read more.
### Discipline

- **Add a row when the prompt is filed (end of Step 1).** Status: `prompt drafted — not yet run`.
- **Update the row's status when the raw output is filed (Step 3).** Status: `raw only — not for citation`.
- **Update the row's status when verification is in progress (Step 7 started).** Status: `verification in progress`.
- **Update the row's status when verification completes (Step 7 done).** Status: `verified`.
- **Mark earlier rows `superseded`** when a new dive replaces them. Always propose to the user — don't apply silently. The Notes column on the new row names what it supersedes and why.

**INDEX updates are batched with the dive's file commits**, not separate commits. Every state change in the workflow updates INDEX in the same commit as the corresponding file write.

---

## LESSONS.md structure

`<AGENT_OUTPUTS_LESSONS>` accumulates cross-dive patterns in agent errors and the prompt-engineering responses that mitigate them. **It is consulted at Step 1 of every new dive.**

### Top of file

```markdown
# Agent Research — Lessons Learned

Cross-dive patterns in agent errors, and the prompt-engineering responses that
mitigate them. Consult this file when drafting any new deep-research prompt
(Step 1 of agent_research_verification_skill.md). Each entry is a pattern
observed across at least two dives, or a drafting principle admitted on the
user's word (its Provenance line says so); entries marked `Cross-project
candidate? Y` are flagged for possible hoisting into the skill itself in a
future skills-maintenance session.

---

<!-- slot: catalog -->
<!-- /slot -->

<!-- slot: unplaced -->
<!-- /slot -->
```

The entries sit inside the `catalog` slot; the header is kit form, regenerated at every
propagation; the file exists from birth as a standing document (`standing_documents_template.md`).

### Per entry

```markdown
## <pattern_name>

**Description:** [What the agent does wrong, in one paragraph.]

**Surfaced in:**
- [Topic slug / dive date — link to the verification doc that surfaced it]
- [Topic slug / dive date — link]

**Prompt response:** [The engineering fix — concrete language to bake into future prompts.]

**Cross-project candidate?** [Y / N — Y when the pattern is generic enough to apply beyond this project's domain.]

**Last updated:** YYYY-MM-DD
```

**Example:**

```markdown
## magnitude_overstatement

**Description:** The agent reports headline effect sizes (treatment effects, elasticities, response coefficients) without confidence intervals or comparison to the null hypothesis. Reported magnitudes have been roughly 2x the published values in two verified cases.

**Surfaced in:**
- remote_work_productivity / 2026-05-13 — [verification](remote_work_productivity/20260513_1430_verification.md)
- school_meal_costs / 2026-06-01 — [verification](school_meal_costs/20260601_1100_verification.md)

**Prompt response:** Include in the methodology section of every prompt: "Report effect sizes with confidence intervals or standard errors. Explicitly compare each headline finding against the null hypothesis or a no-effect baseline. Where a finding has been challenged in subsequent literature, report the challenge."

**Cross-project candidate?** Y — magnitude overstatement is a generic agent failure mode, not specific to this project's domain.

**Last updated:** 2026-06-01
```

### Discipline

- **A pattern earns an entry when it has been observed in two or more dives.** A single-dive observation lives in that verification doc's "patterns in the agent's errors" section, not yet in LESSONS.md. Promote to LESSONS.md when the second instance appears.
- **A drafting principle is the one entry exempt from the dive count.** A load-bearing rule about how a prompt frames the agent's task, learned from drafting rather than from an observed error (for example, a rule that the prompt must not hand the agent the project's own taxonomy to confirm), enters on the user's word as its own entry type: the entry form above with `**Provenance:** drafting principle, not dive-observed` in place of the Surfaced-in list, the rest unchanged. It is never given a dive it did not have, and a dive that later shows the error it guards against is added as Surfaced-in without changing the provenance.
- **At verification completion (Step 7),** Claude reviews the new verification's error-patterns section against existing LESSONS.md entries. If a new pattern surfaces (second instance of something), propose an entry to the user. If an existing entry accumulates a third instance, propose strengthening the prompt response.
- **The `Cross-project candidate?` field is set at write time, and a Y is logged to the kit channel in the same commit.** The user (or Claude with the user's approval) judges whether the pattern is generic or domain-specific. A pattern flagged Y gets, in the same commit, a `[SKILL-FEEDBACK] — agent_research_verification_skill.md — <date> — <model>` entry in the repo's `skills/CHANGELOG.md` naming the lesson and quoting its prompt response (the entry form is `structure_conventions.md`, "The skills CHANGELOG and the `[SKILL-FEEDBACK]` channel"); a sweep run from your canonical skills repo, if you keep one, reads that channel, and the lesson is hoisted into Step 1 there (see "Cross-project hoisting"). Strengthening a flagged entry logs a new one.
- **`Last updated`** is bumped whenever the entry is revised — new dive surfaces it, prompt response is strengthened, cross-project status reconsidered.

---

## Verification document structure

The verification doc at `<topic_slug>/<YYYYMMDD_HHMM>_verification.md` follows this template.

### Header

```markdown
# Verification — <topic_slug> — <dive date>

**Prompt:** [<YYYYMMDD_HHMM>_prompt.md](<YYYYMMDD_HHMM>_prompt.md)
**Raw output:** [<YYYYMMDD_HHMM>_raw.md](<YYYYMMDD_HHMM>_raw.md)
**Retrieval doc:** [<YYYYMMDD_HHMM>_retrieval.md](<YYYYMMDD_HHMM>_retrieval.md)
**Agent platform:** Claude Research
**Verification date:** YYYY-MM-DD
**Dive type:** <evidence synthesis | discovery (inventory)> — copied from the prompt header; determines which synthesis template below applies
**Source folders for this dive:** [the repo's literature home] and [non-paper folder name, or "none — academic sources only"]
**Retrieval coverage (required):** [State totals AND enumerate every source that was *not* retrieved, each with its reason (paywalled / broken link / not found), copied from the residual list at the foot of `_retrieval.md`. This is the durable record of the backlog in the citable artifact — e.g., "12 of 18 cited sources retrieved (8 in the literature folder, 4 in <documents folder>). Not retrieved: Author A 2019 (paywalled); Author B 2021 (broken link); Author C 2022 (not found); Author D 2020 (paywalled). Unverifiable claims marked below."]
```

### Body — claim-by-claim tables (two tables, by source type)

The verification body has **two tables**, one for academic paper sources and one for non-paper document sources. The two tables exist whether or not the dive has both source types — if a source type has no claims, the table is empty with a one-line "no [academic / non-paper] sources for this dive" note. Two visibly-separate tables make absences visible; a merged table with a source-type column can look complete while silently dropping a category. Verdicts adjudicated under Step 7's whole-document rule carry their adjudication note in the verdict cell, alongside the two readings.

**Part 1: Academic paper sources** *(verified against the dive's declared literature folder)*

| Claim from agent output | Agent's cited source | What the original (in the literature folder) actually says | Verdict |
|---|---|---|---|
| [Verbatim claim] | [Author, year + how the agent cited it] | [What the retrieved original actually says] | [verdict] |

**Part 2: Non-paper document sources** *(verified against the dive's declared documents folder)*

| Claim from agent output | Agent's cited source | What the original (in the documents folder) actually says | Verdict |
|---|---|---|---|
| [Verbatim claim] | [Document title, institution, date + how the agent cited it] | [What the retrieved original actually says] | [verdict] |

**Verdict values (same vocabulary across both tables):**

- `confirmed` — original says what the agent claimed.
- `partially confirmed` — original supports part of the claim but not all of it (e.g., magnitude is roughly right but scope is narrower than the agent implied).
- `contradicted` — original says something materially different from what the agent claimed.
- `unverifiable` — original is not in the dive's declared source folders. Not confirmation; do not cite. The retrieval log names the reason (paywalled, broken link, not found, etc.).
- `fabricated` — the claim doesn't appear in any retrieved source. The agent invented it.
- `misattributed` — the claim appears somewhere, but not in the source the agent cited. (Common with research agents; they mash findings together and attach them to nearby citations.)

**Existence claims (mostly a discovery-dive case).** Where the claim is that a document exists, the document's presence in the dive's declared source folders **is** the evidence, and the verdict answers the claim as stated. Two consequences. A retrieved but unreadable file — an image-only scan with no text layer — **confirms existence and leaves content unverifiable**: record it as `confirmed` with the content limit stated in the "what the original actually says" cell, rather than reaching for a sixth verdict value that would cost every dive to serve one. And the reverse holds strictly: a claim that a document exists, where the document was never retrieved, is `unverifiable` and not `confirmed`, however plausible the document is and however many other sources refer to it.

**Escalated claims (the whole-document rule).** Where a Step 7 whole-document trigger fires, *escalated* is a **transient state within the pass, not a seventh verdict value** — the same reasoning as the existence-claim note above: don't grow the vocabulary to serve a state that resolves before the document is finished. The verdict cell stays blank until the user adjudicates; the final verdict is always one of the six values, and the cell carries the two readings plus the adjudication note so the provenance is visible in the citable artifact.

**Headline claims only.** A row is justified only if the claim could appear in a deliverable. Background framing, definitions, and connective tissue do not need rows in either table.

### Synthesis section

```markdown
## Synthesis

### Claims that survive

[The verified, citable findings, restated in the user's own words — paste-ready
for deliverables. Each survival should reference its row in the table(s) above.]

### Claims to retire

[What the agent said that didn't hold up, and why. Worth recording so the
same claim doesn't get re-introduced in a later session.]

### Patterns in the agent's errors

[If specific failure modes showed up in this dive — magnitude overstatement,
counter-evidence dropped, fabricated citations, identification strategy
mischaracterized — note them here. At verification completion, Claude reviews
this section against LESSONS.md to decide whether a new entry or update is
warranted.]

### <fourth sub-section — forks on dive type; see below>
```

The first three sub-sections are the same for every dive. **The fourth forks on the dive type declared in the prompt header**, because the two kinds of dive have different things to be honest about. An evidence-synthesis dive asks what the evidence supports; a discovery dive has no evidence base to summarise — its claims were about which documents exist — so the same template applied to it produces either an empty paragraph or, worse, a fabricated one.

Whichever branch applies, the fourth sub-section is the **load-bearing output**. The tables are the work; the synthesis is the use.

#### Fork A — evidence-synthesis dive

```markdown
### Updated honest-picture summary

[The "what does the evidence actually support" paragraph, replacing the
agent's framing with what survives the second pass. This is what the user
hands to themselves when starting a deliverable a month later.]
```

#### Fork B — discovery (inventory) dive

A discovery dive's verification establishes which documents are **real, correctly described, and reachable**. It does not establish findings about the world. Its fourth sub-section is therefore not a summary of evidence but a **map to the originals** — a finding aid.

```markdown
### Map to the originals

**[Opening finding-aid line — required.] This document is a finding aid, not an
evidence base. It establishes which documents exist, whether they are described
correctly, and whether they can be reached. It establishes nothing about
[the subject matter]. Cite the originals in [source folders], never this
document, for any empirical claim.**

[The map, organised on the dive's own structure — the topics or categories the
prompt asked the agent to report on, in the prompt's order, so a reader who
knows the question can find the answer. For each:

  · **What exists and is held** — named, with where it sits.
  · **What is confirmed absent** — an established negative, which is a finding
    in its own right and often the most durable thing a discovery dive produces.
  · **What could not be established either way** — and *why not*, because the
    kinds of unreachability have different fixes:
      – host-protected / server failure → worth retrying, the document is real
      – not found / no working path → needs a different route, not a repeat
      – not attempted by decision → deliberate, not a gap
      – unfixable by any retrieval → publisher ID collision, image-only scan
        with no text layer; no future pass resolves these
]

[**The retrieval-pass caveat — required where the unverifiable count is high.**
For an existence claim the document *is* the source, so an unretrieved row
leaves nothing to verify against. A discovery dive with many `unverifiable`
verdicts is making a statement about the retrieval pass, not about the
documents. Say so explicitly, so a later reader does not mistake an
unworked backlog for an established absence.]
```

**The residual list is the input to the next dive.** A discovery dive's unreached rows are not failure; they are the scope of the follow-up. Where the prompt declared the dive part of a sequence, say so here.

---

## Cross-project hoisting

The `Cross-project candidate? Y` flag in LESSONS.md entries exists because some agent failure modes are generic across projects (magnitude overstatement, counter-evidence drop, fabricated citations) while others are domain-specific (e.g., conflation of two neighboring categories in one field's data).

**The channel.** A flagged lesson reaches the kit through the channel the discovery sweep already reads: the `[SKILL-FEEDBACK]` entry the writing session logs in the repo's `skills/CHANGELOG.md` in the same commit as the lesson (the Discipline bullet above). The sweep (your canonical skills repo, if you keep one, and its discovery workflow) collects the entries; consolidation reads them as feedback on this skill and hoists the pattern — **one row added to the Known agent failure modes table below**, the table Step 1 reads beside the repo's `LESSONS.md` — once it has appeared in two or more projects, or once when the failure mode is plainly platform-general. The project-local `LESSONS.md` entries stay as the record of how the lesson was learned; future projects meet the hoisted version before they meet the pattern. *(Documented predecessor, to v6.5: detection was user-driven — the user was to open a session in the canonical skills repo and search the content repos for the flag.)*

**The backfill.** A repo whose `LESSONS.md` carries flagged entries with no matching CHANGELOG entry gets them written at the conformance pass (`PROJECT_SETUP.md` Step 7.5 part 2, the standing-documents bullet), so the next sweep brings them in.

**Claude in a content-repo session** has a smaller role here: when reading LESSONS.md at Step 1, if a pattern looks generic and isn't yet flagged `Cross-project candidate? Y`, suggest to the user that the flag may be appropriate. Don't apply silently.

### Known agent failure modes — the hoisted set (kit-side)

The landing place of the loop above: one row per pattern hoisted at a consolidation, written only there (a content-repo session never adds a row; it flags a lesson). Step 1 reads this table at every dive beside the repo's `LESSONS.md`; the prompt response is the text the drafter carries into the prompt. `Hoisted from` names the repos and the consolidation that hoisted it, so the row's evidence is traceable to the `LESSONS.md` entries that stay in their repos. Born empty: the loop had a channel, a sweep and a consolidation step, and no place in the kit for a lesson to land; the first rows come from the first consolidation that receives flagged entries.

| Pattern | What the agent does | Prompt response (carried into Step 1) | Hoisted from |
|---|---|---|---|

---

## Common pitfalls

- **Don't cite the raw output, ever.** The whole skill exists to prevent this. If a deliverable cites "the agent said," roll back and verify against the original.
- **Don't let the drafter chat do the verification.** The drafter knows what the prompt was looking for, which biases the second pass toward "did the agent answer my question" rather than "do the claims hold against primary sources." The five-chat pattern (drafter / researcher / retriever / source processor / verifier) exists precisely to enforce this separation — collapsing drafter and verifier into one chat collapses the discipline.
- **Don't skip verification because the dive "looks fine."** Agent output is most dangerous when it looks coherent and authoritative. Coherence is not accuracy.
- **Don't process unretrieved sources as `confirmed`.** If the source wasn't retrieved and processed into the dive's declared folders, the verdict is `unverifiable`, not `confirmed`. This is the most consequential discipline rule in the skill.
- **Don't let INDEX.md fall behind.** Every state change in the workflow updates INDEX in the same commit. If INDEX doesn't reflect reality, the citability rule degrades to "trust whoever last spoke."
- **Don't skip the LESSONS.md and WORKFLOW_SKIPS.md reads at Step 1.** Prompt engineering compounds only if past lessons are actually consulted, and workflow patterns surface only if the skips register is actually read. Reading both files before drafting is the load-bearing discipline.
- **Don't merge raw output into a verification doc to save time.** They are different artifacts with different epistemic status. The verification doc is your synthesis; the raw output is what the agent produced. Merging them collapses the provenance.
- **Don't run a topic twice without checking INDEX first.** The "did I already run this?" check is what INDEX exists for. A new dive on a topic that already has dives should either explicitly supersede the prior one, or carry a different angle. Both should be reflected in INDEX's Notes column.
- **Don't delete the retrieval doc, or treat it as scratch.** It is the dive's kept backlog — table 1 (every source × every candidate link), the pass tables, and the residual not-retrieved-with-reasons list. It's how you pick up a paywalled source weeks later. Pruning it loses the backlog silently. The verification doc's required coverage field copies the residual list, so the backlog also lands in the citable artifact.
- **Don't record a verdict from the pointed-at passage alone when a whole-document trigger fires.** A source that seems to contradict itself, or a passage that reads narrower than the claim cited to it, obliges the whole-source read and the escalation under Step 7's whole-document rule — verdict blank, both readings recorded, the user adjudicates. A pass tuned to catch dropped qualifiers over-reports when it reads narrowly.
- **Don't waive away the session-start ritual.** The ritual exists because gaps in prior steps are invisible to a fresh chat. Complaining-and-logging is cheap; silent drift across chats is expensive.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
