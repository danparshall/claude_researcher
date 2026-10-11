---
name: own-document-verification
description: "Use this skill to verify a document written by the user or a collaborator — claim by claim — against the sources the repo holds and has processed. Covers documents co-produced in the repo and documents arriving from outside; produces a verification document with per-claim verdicts, a tiered change list that never touches the draft, and a first-class coverage report listing every claim the repo cannot check and why. Does NOT cover verifying deep-research agent outputs — that is `agent_research_verification_skill.md` — and is not a review round on a branch, which is `writing_branch_skill.md`: this skill checks a draft against sources, not against the user's editorial judgment."
triggers: >-
  "verify this document against the repo," "check what I wrote against the sources," "verify my
  draft." Not for agent outputs (`skills/agent_research_verification_skill.md`) or review rounds
  (`skills/writing_branch_skill.md`)
---

# Own-Document Verification

Verifies a document written by the user or a collaborator against the repo's processed sources, claim by claim. Two outputs matter equally: the **verdicts** on the claims the repo can check, and the **coverage report** on the claims it cannot — every unverifiable claim listed with its repo-side reason, so the user can decide per claim whether to retrieve the source, accept the claim on their own authority, or soften the draft. A verification run that silently checks only what it can check gives false comfort; the coverage report is what makes the run honest.

The claim-verification core — verdict vocabulary, the whole-document rule, escalation mechanics — is inherited from `agent_research_verification_skill.md`, not restated here. What is different: the document under verification is *ours*, not an agent's, so the output is a correction instrument rather than a citability gate; the insulation problem is inverted (a do-not-read list over repo files, not header-not-body over a prompt); and there is no dive machinery — no retrieval pass, no raw output, no INDEX tracker.

## When to use this skill

- The user says "verify this document against the repo," "check the correctness of something I wrote against the sources," "verify my draft," or asks whether a document's claims hold up against what the repo has processed.
- A deliverable drafted in the repo is approaching submission and its load-bearing claims need an independent check against the extracts and originals.
- A document arrives from outside — written by a collaborator, or by the user elsewhere — and needs checking against the repo's holdings.
- The user asks to check one document against a **companion document** — a response-to-reviewers letter against the revised manuscript, an executive summary the user wrote against the report it fronts, a cover note against the deliverable it covers: the **companion-document mode** (after Step 6). The ground truth is the companion, not the repo's sources. (The kit's own `SUMMARY_` files are not this mode's object: they re-verify by the processing skills' optional step, `document_processing_skill.md` Step 7, which edits them; this skill never edits.)

**Do not use this skill for:**

- **Deep-research agent outputs.** Those go through `agent_research_verification_skill.md`, whose output is a citability gate (the verification document becomes the only citable artifact). Here the draft is already ours; the output is a list of corrections and a coverage map, and the draft's citability is the user's call.
- **Review rounds.** A branch review per `writing_branch_skill.md` checks a draft against the user's judgment — structure, argument, voice. This skill checks it against sources only. The two can run on the same document; they are different operations.
- **Verifying against unprocessed material.** The ground truth is the repo's extracts and originals. A source that is in the repo but has no extract is a coverage finding (`held-not-processed`), not something the verifier reads ad hoc mid-pass.

## Prerequisites

- A repo with processed sources: originals with extracts (and summaries) under the repo's source folders, registered in the repo's indexes.
- `agent_research_verification_skill.md` at v4.0.0 or later, for the inherited claim-verification core (Step 4 below). Where that skill is not shipped in the repo, the fallback paragraph in Step 4 carries the minimum; the run is still valid, just thinner on the mechanics.
- The document to verify, in a readable format. For a co-produced document, it lives in the repo already; for an external one, it enters through the repo's normal intake and sits wherever the user places it.

## The workflow

### Step 0 — Intake fork: co-produced or external?

Ask (or confirm from context) which of two cases this is. The answer sets the insulation and whether Step 2 runs.

- **Repo-co-produced.** The document was drafted in this repo with Claude. Drafting artifacts exist — working conversations, decision records, outlines, matrices, the drafting sessions' notes — and the verifier must be insulated from all of them, because they carry what the draft *needs* its sources to say. The do-not-read list (Step 3) is the mechanism.
- **External.** The document was written outside the repo (by a collaborator, or by the user without Claude). No drafting artifacts exist here, so the extractor and verifier are fresh by construction — but the extraction rules (Step 1) carry the entire load, with no drafting-session record to fall back on for what a sentence was meant to assert. The document is read as it is written, full stop. Step 2 (citation mapping) runs on this branch.

### Step 1 — Claims extraction, by a fresh session

Extraction is its own session, separate from both the drafting sessions (if any) and the verification session. A session that drafted the document decomposes it as intended rather than as written; a session that will verify it decomposes toward what it can check. Fresh extraction protects against both.

The extractor reads the document and produces the **claims file**: one row per headline claim, in document order. Rules, each of which exists because its violation has already caused a verification failure:

- **Claim text is the draft's verbatim sentence.** Never a paraphrase, never a tightening. A paraphrase at extraction can drop a qualifier before verification starts — the identical dropped-qualifier failure the verification exists to catch, moved upstream where no source-side rule can reach it.
- **The unit is the full qualified assertion.** If a sentence's qualifier lives in the adjacent prose — a scope condition in the sentence before, a "since 2024" in the sentence after — the qualifier travels into the row alongside the verbatim sentence. A claim row that strips its qualifiers manufactures overstatements for the verifier to find.
- **The cited source is a pointer, not a boundary.** Record what the draft cites for the claim, but the citation does not limit where the verifier may look. Treating each row's citation as the boundary of the check is exactly how narrow-reading failures happen.
- **Draft-governs, stated at extraction.** The claims file opens with one line: *claims are verified as the draft states them, not as the author intended them.* The verifier holds the draft to its own words; intent is invisible and not the standard.
- **Headline claims only.** A row is justified if the claim is load-bearing — a fact, magnitude, legal or institutional statement, or characterization of a source that the document's argument rests on. Background framing and connective tissue do not get rows.

The claims file is saved unregistered (see Step 6) and handed to the verifier session as its input.

### Step 2 — Citation mapping (external branch only)

For an external document, before verification, resolve the document's citations against the repo's holdings — the indexes and source folders. Each cited source lands in one of:

- **Held and processed** — verification proceeds against the extract or original.
- **Held, not processed** — the file is in the repo but has no extract. A coverage finding, not a mid-pass processing job.
- **Identifiable, not held** — the citation is precise enough to name a retrievable document the repo does not have.
- **Citation too vague to resolve** — "a multilateral's report," an author-year with no matching entry. Distinct from identifiable-not-held because the fix is different: the user clarifies the citation before anyone retrieves anything.

Optionally, and bounded by the user's instruction: a sweep for **uncited claims the repo can still speak to** — the document asserts something without citation, but a held source confirms or contradicts it. These are verified normally but flagged with their distinct status (*uncited; checked against repo holdings*), because a verdict on an uncited claim says something about the repo's knowledge, not about the document's sourcing.

For a co-produced document this step is unnecessary as a separate pass — the drafting already cited repo sources — but its vocabulary (the four statuses) is used by Step 5 regardless of branch.

### Step 3 — Insulation: the fresh verifier session and the do-not-read list

The verifier is a **fresh session** that opens against the repo and reads only: the claims file, the document under verification, and the repo's processed sources. It does not read the drafting artifacts.

The **do-not-read list** is a per-run parameter, assembled by the user (or the session preparing the run) before the verifier opens, naming the files and folders the verifier must not open. Standing members, every run:

- The working conversations and decision records behind the document (`workspace/claude_conversations/`, brainstorms, carryovers, drafting-session outputs) — co-produced branch.
- **`FOLDER_MAP.md` files are named explicitly on the list wherever they carry contaminating content.** Folder maps accumulate findings, prior results, and settled positions; a verifier that opens one to orient itself can learn what the answer is supposed to be. If the verifier needs to locate a source, it uses the repo's indexes' file-path columns, or asks the user, rather than browsing maps.
- Anything else the user names for the run.

**Precedence rule:** for the duration of a verification run, the do-not-read list overrides any `CLAUDE.md` or skills-table instruction to read a file. A skills-table row saying "read this skill when X arrives" does not license the verifier to open a file on the list; the collision resolves in the list's favor, and the verifier notes in its output that the file was skipped under this rule. Without this stated, every future verifier meets the collision fresh and resolves it ad hoc.

The list travels in the verification document's header, so a later reader can see what the verifier could and could not see.

**Running the verifier as a scoped/blind session.** The insulation this step builds by hand — a fresh session with a controlled reading scope — is exactly what `workstream_plan_skill.md`'s **scoped mode** formalizes, with `BLIND_SESSION.md` as the session-side companion. Where the verification run is a step in a workstream plan, or the user wants the stronger machinery, run the verifier as a scoped session: the do-not-read list becomes the session's reading-scope specification, and the contamination rule and report-inbox mechanics come for free. The list and precedence rule above stand either way — they are this skill's requirements, however the session is launched.
### Step 4 — Claim verification (inherited core)

Verification of each claim follows **`agent_research_verification_skill.md` (v4.0.0 or later), Step 7**: the six-value verdict vocabulary (`confirmed` · `partially confirmed` · `contradicted` · `unverifiable` · `fabricated` · `misattributed`), the **whole-document rule** with operator adjudication, and *escalated* as a transient state rather than a seventh verdict value. Read that skill's Step 7 and its verification-document structure before the pass; do not work from memory of it, and do not restate it here — point, don't restate, or the two drift.

Two adaptations for this skill's context:

- `fabricated` reads as *the claim appears in no held source and cites none* — for our own document this is usually a drafting error or a memory-sourced assertion, not invention, but the verdict vocabulary is not softened for it. `misattributed` reads as *the claim is supported by a held source, but not the one the draft cites*.
- `unverifiable` is never a dead end here: every `unverifiable` verdict must carry its repo-side reason from Step 5's taxonomy, because the coverage report is built from these rows.

**Fallback where the sibling skill is not shipped in this repo:** on either of two triggers — the source appears to contradict itself, or the pointed-at passage reads narrower than the claim — the verifier records no verdict from the pointed-at passage; it reads the whole extract or original (checking the extract's stated coverage first — a whole read of a deliberately partial extract reproduces the narrow-reading failure), weighs readings by independent structural positions (summary, body, recommendations, annexes) counted by physical place in the document rather than by derived-layer labels, records both readings with the weighing, leaves the verdict blank, and batches escalations to the user at pass end. The user adjudicates on what the source, read whole, supports and can honestly be cited — citability, not preference — choosing one of the six verdict values, with an adjudication provenance note in the cell. This paragraph is the minimum; the sibling skill is the canonical statement.

**Language rule.** Where a verdict rests on a source in a language the user does not read (their reading languages are declared in the repo's `CLAUDE.md`; default English), the verification row carries the source's verbatim words inline with an English rendering beside them, per `document_processing_skill.md` (v3.0.0) — so the exact words a verdict rests on are auditable by the user without opening the source-language extract. Verification always runs against the source-language extract or the original, never against an English reading copy (those are marked audit-only and are not verification targets).

### Step 5 — Coverage: the first-class second output

Every claim the repo could not check is listed in the **coverage report**, with its repo-side reason:

- **`cited-not-held`** — the draft cites a source the repo does not have. (External branch splits this via Step 2 into *identifiable-not-held* and *citation-too-vague*.) Natural action: retrieve, or clarify the citation.
- **`held-not-processed`** — the source is in the repo but has no extract; the ground-truth library does not cover it. Natural action: process it through the repo's materials protocols, then re-verify the claim.
- **`held-but-silent`** — the cited source is held and processed, but says nothing on the claim's point. Natural action: soften the draft, or find the claim's real source.
- **`no citation`** — the claim cites nothing and no held source speaks to it. Natural action: the user decides whether it stands on their authority or needs a source.

The reasons matter because each implies a different fix; a flat "unverifiable" list would leave the user re-deriving the triage the verifier already knows.

**The user's triage.** The coverage report goes to the user, who rules per claim: **retrieve** (the source enters the repo through normal intake and the claim is re-verified in a later run), **accept on own authority** (the claim stands; the ruling is recorded), or **soften** (the draft is edited to what the held evidence supports). **Rulings are recorded in the verification document**, in the claim's row — *ruled by the user, <date>: <ruling>* — so a re-verification of the same document does not reopen settled claims: a later run checks new and changed claims, and claims whose ruling was *retrieve* once the source is in, but does not re-litigate an *accept on own authority*.

### Step 6 — Outputs

Three artifacts, all read-only on the draft:

- **The verification document.** Header (document verified, date, intake branch, do-not-read list, claims-file pointer, sources consulted), the claims table with verdicts and escalation/adjudication notes per the inherited structure, and the coverage report with the user's rulings as they land.
- **The change list, tiered.** Every finding that implies an edit, sorted **must-fix** (the draft states something a held source contradicts, or overstates what its source supports — wrong as written) above **minor** (imprecise, improvable, not wrong). The verifier **never edits the draft**. The user applies, rejects, or delegates each item; the draft changes only by their hand or on their explicit instruction in a separate session.
- **The claims file** (Step 1), kept as the record of what was checked.

**Registration is deferred to a following session.** The verifier session does not register its outputs — no index rows, no `FOLDER_MAP.md` entries — because opening those files is itself a contamination risk (folder maps and indexes carry findings and settled results; this is how a prior verification session contaminated itself). The outputs exist unregistered until a later, ordinary session registers them. This is a deliberate, bounded exception to the repo rule that a file is not in the repo until it carries an index row: the exception lasts exactly one session boundary, and the following session's first job on the document is the registration. State the pending registration at close-out (STATUS or the session hand-off) so it is not lost.

## Companion-document mode

One document checked against another: a response-to-reviewers letter against the revised manuscript ("we added the robustness check in section 4"), an executive summary the user wrote against the report it fronts, a cover note against the deliverable. The workflow above runs with three substitutions. **The ground truth is the companion**, not the repo's sources: the do-not-read list (Step 3) covers the drafting artifacts of both documents, and the verifier reads the companion whole. **The claims are the document's claims about the companion**: Step 1 extracts every sentence that asserts what the companion contains, says or does, verbatim, with its location claim ("section 4", "Table 2") carried into the row; Step 2 maps each to the companion's actual location. **The coverage report lists what the companion does not show** — a claimed change with no trace, a section renumbered — and a claim the companion supports only partly is a must-fix, since the reader of the letter will look. Outputs, registration and the rules are unchanged. *(If one kind of companion check keeps recurring, give it a skill of its own.)*

## Key rules

- **Coverage is an output, not an apology.** The run is not finished until every claim has either a verdict or a reasoned coverage row.
- **Verbatim at extraction, draft-governs throughout.** No paraphrase in the claims file; the draft is held to its own words.
- **The citation is a pointer, not a boundary.** The verifier may find a claim's support — or its contradiction — in any held source.
- **The do-not-read list wins.** Over skills-table triggers, over orientation habits, for the length of the run.
- **Never verify against a derived layer when the ground truth is held.** Extract or original; summaries are for finding, not for verdicts. An English reading copy is never a verification target.
- **The verifier never edits the draft.** Corrections travel as a change list; the draft changes only by the user.
- **No registration by the verifier session.** Outputs are registered by a following session; the pending registration is stated at close-out.
- **Rulings persist.** A recorded triage ruling is not reopened by re-verification unless the user reopens it.

## Edge cases

- **Mixed provenance.** A document partly drafted in the repo and partly written outside runs the co-produced branch (the stricter insulation), with Step 2's citation mapping run on the externally-written parts.
- **A claim about a source the repo holds only as an image-only scan.** Existence is checkable; content may not be. Follow the sibling skill's existence-claim note: record what can be established, state the content limit in the row, do not stretch a verdict.
- **The document cites the repo's own derived artifacts** (a summary, a prior verification document). The claim is verified against the underlying original, not the derived layer; if the derived layer misled the draft, that is a finding about the derived layer worth flagging alongside the verdict.
- **Very small documents.** For a short document (an email, a one-pager) the fresh-extraction session and the verifier session may be collapsed into one fresh session with the user's approval — the insulation that matters most is from the *drafting* sessions, which is preserved. Record the collapse in the verification document's header.

## Setting up for a new project

This skill assumes the repo has: processed sources (extracts registered in indexes), a conversations/drafting-artifacts home to insulate against, and `FOLDER_MAP.md`-style per-folder records (whose contaminating role Step 3 names). Where a repo names these differently, map them once at first use and note the mapping in the verification document's header. If `agent_research_verification_skill.md` is not shipped, Step 4's fallback paragraph governs.

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
