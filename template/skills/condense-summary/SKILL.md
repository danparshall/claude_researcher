---
name: condense-summary
description: Use when I say "condense this summary", "make the index line for SLUG", "the index row for X is too long", "write the one-liner for X", or "backfill one-liners for section Y". Brings one PAPER_SUMMARIES.md entry up to complete first, then writes its Focus and One-liner fields and regenerates the PAPER_INDEX.md row with paper-index. Works in any paper-collection repo.
---

`{{skills_dir}}` is `~/.claude/skills` on Claude Code and `/home/claude/.claude_researcher_template/template/skills` in the claude.ai sandbox.
Sandbox-specific notes (REST for Issues/Pulls, the post-commit push hook) are in RESEARCHER.md.

<required>
CRITICAL: Add the following steps to your task list:

1. Run condense_check.py on the key; read the whole entry and its index row
2. Decide whether the entry is complete enough to condense from; if not, read the source and enrich the entry first
3. Write the Focus and One-liner fields (and Index label only when the Title parenthetical does not parse)
4. Rename the related-entries field to Related
5. Regenerate the index row with paper_index.py index
6. Re-run condense_check.py; run paper_index.py check
7. Commit with the key(s) in the subject
</required>

Announce at start: "I'm using the condense-summary skill to bring KEY into shape."

The order is the point. PAPER_SUMMARIES.md is the source of truth and the index row is derived from it. The failure this skill exists to prevent is an index row that claims something the entry does not contain — so anything worth saying goes into the entry first, and the ≤50-word version is written last, from the entry alone. A `head -c 300` of the summary is not a one-liner.

## Step 1: Locate

```
python3 {{skills_dir}}/condense-summary/condense_check.py REPO_ROOT KEY
```

`KEY` is the `### ` heading (the slug in slug-anchored repos; in repos without slugs, a unique substring of the heading). The script prints the entry's line range, the fields it already has, word counts with OK/WARN/FAIL against the 50/60-word rule, completeness signals, and every index row it can match — by slug cell first, by filename otherwise. Then read the entry in full (heading to the next `---`) and the row. Do not condense from the script's summary of the entry.

## Step 2: Decide whether the entry can be condensed from

The entry is not ready if any of these hold: the Summary is under ~80 words; an empirical paper's Key findings carry no number; there is no Relevance paragraph; the existing index row makes a claim the entry does not. When it is not ready, open the source — `papers/text/FILE.txt` (or the PDF, or the `.md` capture) — and add what is missing to the entry: the thesis, the one or two numbers that carry it (metric, dataset, baseline), and why it matters for this collection. This is the QA step. Reference-only entries with no local source: condense from what the entry has and say so in the commit message.

<bad-example>
Row says "N=57 novices were 4.16× more accurate"; entry says only "novices did better with LLM help". Agent writes the one-liner from the row.
</bad-example>
<good-example>
Same situation. Agent reads the paper, adds "4.16× more accurate (N=57, 13-hour trial, eight benchmarks)" to Key findings, then writes the one-liner from the entry.
</good-example>

## Step 3: Write the fields

Add two bullets to the entry's metadata list, directly after the File / Files / Text extraction bullet:

```
- **Focus:** Compute governance, verification
- **One-liner:** Verifying that no 10^25-FLOP run occurs anywhere within 30 days at 90% confidence needs ~232 inspectors — IAEA scale — via on-chip weight snapshots, proof-of-training transcripts, and chip tracking.
```

Focus: 2–5 words naming the topic, in the vocabulary the repo's existing Focus column already uses. One-liner: ≤50 words, a thesis (the claim), with the single number that carries it; no hedging clauses, no "this paper examines", no second sentence of caveats. Count with the script (Step 6), not by eye. If the field already exists and is over 50 words, rewrite it; over 60 is a hard fail.

The index row's Paper column (authors, org, year) is derived from the trailing parenthetical of the `**Title:**` line, e.g. `(Shavit — OpenAI, 2023)`. If the Title has no such parenthetical and you are not going to add one, write `- **Index label:** Shavit (OpenAI) (2023)` after the One-liner bullet. Only then — do not add Index label to entries whose Title already parses.

<bad-example>
```
- **One-liner:** This paper examines whether compliance with training-run rules could potentially be verified, finding that it may be feasible under some assumptions, although the authors note several limitations regarding adversarial chips and the political feasibility of inspections, which future work should address.
```
</bad-example>

## Step 4: Rename the related-entries field

Four names exist for the same thing: `Relationship to other repo entries`, `Cross-references (in this collection)`, `Cross-references in this collection`, `Companions in this collection`. While you are in the entry, rename it to `- **Related:**` with backticked slugs (`` `catch-a-chinchilla` ``), one bullet. Prose after the slugs may stay. The script flags dangling slugs; fix them.

## Step 5: Regenerate the index row

```
python3 {{skills_dir}}/paper-index/paper_index.py index REPO_ROOT
```

The row is generated from the fields you just wrote — never write it by hand. Paper cell comes from the Title parenthetical or the Index label field; Key Contribution is the One-liner. A repo not yet migrated to the generated format (no `GENERATED` markers in PAPER_INDEX.md) has no `index` to run: leave its row alone; the migration generates it.

## Step 6: Verify

Re-run `condense_check.py` on the key: One-liner must read OK, Focus present, no completeness signals you did not deliberately leave, index row found. Then `python3 {{skills_dir}}/paper-index/paper_index.py check REPO_ROOT` must exit 0.

## Step 7: Commit

One commit per entry or per batch, key(s) in the subject: `condense: catch-a-chinchilla, scher-thiergart-verification — Focus/One-liner + rows`. Stage PAPER_SUMMARIES.md, PAPER_INDEX.md and PAPER_RELATED.md by name.

## Batch mode and fan-out

"Backfill section Y": `python3 {{skills_dir}}/condense-summary/condense_check.py REPO_ROOT --sweep --section "Y"` lists every entry with row/focus/one-liner status; work through the ones marked `row=no` or `one-liner=-:MISSING` or `FAIL`, one at a time, Steps 1–6 each, one commit for the section.

Fanning out across sections with subagents: PAPER_SUMMARIES.md is one file, so parallel agents must not edit it — concurrent writes lose updates. Use the prompt/apply/verify scripts in `paper-index` (its "Condense fan-out" section): each agent writes a whole replacement entry as a fragment, and `fanout_apply.py` splices them serially. Calibrate before fanning out: do five entries by hand and read the five one-liners aloud to me.

## Calibration examples (general-ai-abilities, 2026-09-07)

Five entries, one per case, done by hand before any fan-out; three of the five needed no source read, the text-only one did.

- `martin-spectral-rg` — row was 59 words; entry complete. One-liner (46): Reads layer-wise training as a Wilsonian RG flow on the retained eigenvalue spectrum: well-trained layers converge to a marginal boundary at power-law exponent α ≈ 2, where every logarithmic spectral band carries equal energy; evidence is one three-layer MNIST MLP, and the fixed-point claim is unproved.
- `verbalizable-representations-global-workspace` — no row; entry complete. One-liner (40): The Jacobian lens finds a mid-layer "J-space" in Claude Sonnet 4.5 that behaves like a global workspace — verbal report, directed modulation, internal reasoning, generalization, selectivity — and surfaces deception and hidden objectives before any output; post-training installs the Assistant into it.
- `harack-lawfare-tri-purpose` — text-only; entry had no Key claims or Relevance, and the row carried the two-grade claim the entry only half stated. Read the 2,400-word capture, added eight Key claims and a Relevance paragraph, then wrote the one-liner (46): AI verification is tri-purpose infrastructure — prosperity, peace, safety — each payoff alone justifying it; privacy-preserving computation on shipping confidential-computing hardware (OpenMined × UK AISI × Anthropic demo) suffices for commercial-grade verification today, while state-secret grade needs cryptographic commitments plus a mutually overseen neutral data center, years away.
- `walmart-central-planning` — reference-only, no local source; condensed from the secondary-source entry; fields go after the `Local file: none` bullet. One-liner (48): Walmart, Amazon and the modern firm's interior already run non-market coordination at national-economy scale (Walmart ≈ $500B revenue, planner-set internal prices), so Mises–Hayek "planning is impossible" is empirically refuted and the live question is democratizing planning; critics answer that the firm's inputs and outputs are still market-priced.
- `krishnan-fable-cipher` — X thread; entry complete. One-liner (50): Asked open-endedly to find and solve an unsolved cipher, Fable 5.1 chose one open 373 years and solved it in 44 minutes and 176k tokens; the author's point is problem selection and attention-starved open problems, not the solve — an unverified first-party claim (no cipher named, no plaintext, run count unstated).

The script runs on python3 ≥ 3.9 (stdlib only). Its Key-findings check accepts any `Key ...:` label (claims, results, arguments); an entry whose findings sit under another heading reads as missing until the heading is renamed.
