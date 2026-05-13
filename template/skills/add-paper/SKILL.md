---
name: add-paper
description: Triage skill — routes academic-style papers to `paper-processing-academic`, institutional-style reports to `paper-processing-institutional`, non-paper documents to `document-processing` (deferred). Step 0 triage runs here; the routed per-protocol skill handles Steps 1-6.
nori_researcher_source: nori-skillsets add-paper v1.0.0 (ported to claude_researcher in 0bbd419, 2026-05-10)
aitaxbid_source: ~/code/AITaxBID/skills/paper_processing.md@e0a736d (2026-05-02)
---

## Runtime detection

Before following the rest of this skill, determine your environment:

```bash
if [ "$IS_SANDBOX" = "yes" ] || [ -d "/mnt/skills/public" ]; then
  echo "claude.ai sandbox"
elif [ "$CLAUDECODE" = "1" ]; then
  echo "Claude Code"
else
  echo "unknown — surface to user before proceeding"
fi
```

Both environments set positive markers; the probe checks for either side affirmatively rather than inferring from absence. If neither fires, something is misconfigured (env vars stripped, custom shell, etc.) and silently picking a branch is worse than surfacing the question.

**If `claude.ai sandbox`:** translate every `git add` / `git commit` / `git push` in this skill into the REST `write_update` / `write_new` recipes from your Project Instructions. Translate local paths like `/Users/<user>/.claude/skills/...` into `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/skills/...` URLs (fetched via WebFetch).

**If `Claude Code`:** follow the skill body as-is.

**If `unknown`:** stop and surface to the user. Don't guess which environment you're in — the cost of a wrong guess (running `git push` in a sandbox with no git, or writing REST calls against a local working tree) is higher than the cost of one round-trip clarification.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

0. Triage — Protocol A or Protocol B (Step 0)
1. Load and follow the routed per-protocol skill (Dispatch at end of Step 0)
</required>

## Scope

This skill is a **triage dispatcher**. It runs Step 0, then routes to one of three target skills that do the actual work:

- **Academic-style papers** — research-oriented documents with original empirical or theoretical contribution (journal articles, working papers, dissertations, white papers structured as research). Routed to **`paper-processing-academic`** by Step 0 triage.
- **Institutional-style reports** — substantive analytical documents that synthesize evidence, position a framework, or advise on policy, but do not present the authors' own original research with a stated hypothesis (G20 background notes, IMF/World Bank/OECD/UN flagship reports, multilateral working-group papers, regional development bank policy reports). Routed to **`paper-processing-institutional`** by Step 0 triage.
- **Legislation, government regulatory documents, terms of reference, and consultant deliverables tied to a single project** — routed to **`document-processing`**. (Note: `document-processing` is deferred per Plan 02 Wave 5; the pointer is currently aspirational — if you hit this branch, fall back to manual handling and surface to the user.)

**Where config keys live.** The four `PROJECT_QUESTION` / `CONDITIONAL_SECTION` / `BIB_FILE` / `PAPERS_INDEX` keys live in the research repo's `STATUS.md` under `## Project parameters`. The two `paper_naming` keys (`paper_naming.academic_format`, `paper_naming.institutional_format`) live in the user's `personal_info.md` under "Operating preferences". The `paper_summaries.structure` knob also lives in `STATUS.md` project parameters. The per-protocol skills each reference back to this section for the full schema.

# Adding a Paper

Announce at start: "I'm using the Add Paper skill — first I'll triage the document, then dispatch to the appropriate per-protocol skill."

## Step 0: Triage — academic-style or institutional-style?

Open the document and answer three quick questions:

1. Does it have an **abstract** (vs. an *executive summary*)?
2. Does it pose a **research question or hypothesis**?
3. Does it report **new estimates the authors produced from data they analyzed** (rather than synthesizing others' findings)?

- **Two or more "yes"** → **Protocol A** (academic-style).
- **Two or more "no"** → **Protocol B** (institutional-style).

For borderline cases, exercise judgment and flag the call to the user in the conversation. Common borderline cases:

- Multilateral working papers that have abstracts and methods sections but lean heavily on policy framing — usually Protocol A.
- Institutional monographs with chapter-level empirical work — usually Protocol B at the document level (the value is the synthesis); if a chapter is heavily reused on its own, consider creating a separate Protocol A summary for that chapter and cross-linking.
- Country case studies with descriptive but not causal analysis — usually Protocol B.
- IDB Discussion Papers, Technical Notes, and Working Papers — most have research-paper structure and are Protocol A; monographs and synthesis pieces are Protocol B. Triage on structure, not on the publisher.
- Reports without named individual authors (e.g., OECD secretariat reports, UN agency reports) are unambiguously Protocol B.
- Reports with named authors but commissioned by an institution (e.g., "Prepared by Smith and Jones for the G20") — the cover usually names the institution as the publisher and the individuals as the production team. Treat as Protocol B.

The pipeline shape is identical across protocols. What differs:

| Step | Protocol A | Protocol B |
|---|---|---|
| Filename | `paper_naming.academic_format` | `paper_naming.institutional_format` |
| Summary section (a) | Thesis, research question, contribution | Purpose, commissioning context, position |
| Summary section (b) | Data, sample, identification, effect sizes | Document type, frameworks/databases, headline findings, policy framework |
| Summary section (d) | Standard "relevance" framing | Same plus "what position does this represent" + cross-references |
| BibTeX entry type | `@article` / `@unpublished` | `@techreport` / `@book` / `@inbook` |

For **legislation, government regulatory documents, terms of reference, and consultant deliverables**, route to `document-processing` instead — not the paper-processing skills.

**Dispatch:**

- **Protocol A → academic** → Read `template/skills/paper-processing-academic/SKILL.md` and follow it from Step 1 onward. Step 0 (this skill) is already complete.
- **Protocol B → institutional** → Read `template/skills/paper-processing-institutional/SKILL.md` and follow it from Step 1 onward. Step 0 (this skill) is already complete.
- **Non-paper document** (legislation, regulatory docs, ToRs, consultant deliverables) → use `document-processing` (currently deferred per Plan 02 Wave 5; if you hit this branch, fall back to manual handling and surface to the user).

# Common Mistakes

**Forgetting Step 0 triage**
- Problem: Skipping triage routes the document through the wrong protocol — wrong filename convention, wrong section emphasis in the summary, wrong BibTeX entry type.
- Fix: Always start with Step 0. If borderline, flag the call to the user before proceeding rather than silently picking a branch.

**Trying to do the full workflow in `add-paper`**
- Problem: After Step 0, the agent ignores the Dispatch instruction and tries to execute Steps 1-6 from this file. Those steps no longer live here — they're in the per-protocol skills.
- Fix: After Step 0, read and follow the routed per-protocol skill (`paper-processing-academic` or `paper-processing-institutional`). This skill is intentionally thin; the real work is in the routed file.

**Reading config keys from the wrong file**
- Problem: Schema is split per Tier C — user-level `paper_naming.*` lives in `personal_info.md`; per-project `PROJECT_QUESTION` / `CONDITIONAL_SECTION` / `BIB_FILE` / `PAPERS_INDEX` / `paper_summaries.structure` live in `STATUS.md` `## Project parameters`. The per-protocol skills each point back to this Scope section rather than duplicating the schema.
- Fix: Read user-level keys from `personal_info.md`; read per-project keys from the research repo's `STATUS.md`.
