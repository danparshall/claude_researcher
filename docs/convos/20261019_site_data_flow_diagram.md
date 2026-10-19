# 20261019_site_data_flow_diagram

**Date:** 2026-10-19
**Branch:** convo-20261019-site-data-flow-diagram (site work on `site-claude-researcher` branch `data-flow-diagram`, fast-forwarded to its `main`)
**Surface:** claude-code
**Machine:** Dans-MacBook-Air
**Session:** Dan (air, claude_researcher, 20261019T1127, opus-5.5) · /Users/dan/.claude/projects/-Users-dan-code-claude-researcher/a288786e-b602-42ac-8eba-27ec70fa6f8e.jsonl · —

## Summary

Dan asked whether the latest work had reached clauderesearch.ai. It had: the Oct 13 proxy-only setup commits (`d65e1cb`, `b8b5d5a`, pushed from `pro`) were built by GitHub Pages, and the live `index.html` matched `origin/main` byte for byte. The local clone on `air` was two commits behind and was fast-forwarded.

The session-start reminder check surfaced #36, a July grab-bag of onboarding observations. Going through it, several items had been made moot by the token-free setup. One ("Claude knows what the script says without knowing the file contents") was rejected as a user-facing claim: printed output, such as `head()`, summaries or tracebacks, enters the chat, so it is not a privacy guarantee. The rest became a privacy-section update on the site: a data-flow diagram, a model-training Q&A, and an encryption-at-rest Q&A.

The diagram went through several versions: a vertical stack of boxes, then a triangle (You at the top, the AI provider at the lower left, GitHub at the lower right). The Anthropic corner was the sticking point. After a subagent's legal research and a check of the primary sources, real Anthropic marks were kept off the page. Dan then decided the corner should be the provider-neutral "AI provider", with Lucide's `bot` icon. Shipped as `site-claude-researcher` `c449119`, and confirmed live.

## Topics Explored

- Deploy verification for clauderesearch.ai (Pages build list, live-vs-repo diff, a screenshot asset check).
- Triage of #36's items against the current token-free setup.
- Diagram design: boxes → triangle; phone fallback (the SVG labels are too small at about 343px, so phones get the vertical stack); icon choices.
- US trademark law on logo use (subagent research): nominative fair use, dilution exclusions, *Jack Daniel's*, copyright in simple marks, contract terms, lookalike marks.
- Whether the toolkit is provider-neutral: the workflow content plausibly is, but the setup and data flow are claude.ai-specific.

## Provisional Findings

- **GitHub encryption at rest:** confirmed on the page. GitHub's changelog (2019-05-23): "Source code stored on GitHub.com will be encrypted at rest, by default." This is disk-level encryption, and GitHub can still read the data. The realistic risks are account compromise, accidental publishing, and legal demands.
- **Logo law (research summary, not legal advice):**
  - Nominative fair use favors the plain word over the stylized logo. *New Kids* (9th Cir. 1992) n.7 on Coca-Cola's "distinctive lettering", attached to the second factor ("only so much … as is reasonably necessary").
  - *Toyota v. Tabari* (9th Cir. 2010): the "Lexus L" logo was "more use of the mark than necessary … visual trappings".
  - *Century 21 v. LendingTree* (3d Cir. 2005, "block letters") and *ISC2 v. Security University* (2d Cir. 2016) point the same way.
  - Deliberate lookalikes (an "A\" typed in another font) are still judged as imitations; redrawing only escapes copyright.
- **Anthropic consumer terms, "Use of our brand" (read on the page, effective 2025-10-08):** "You may not, without our prior written permission, use our name, logos, or other trademarks in connection with products or services other than the Services, or in any other way that implies our affiliation, endorsement, or sponsorship."
  - The terms have a severability clause and are governed by English law. That is the version served to this fetch; it may be geo-dependent, so this is unverified for US users.
  - Dan's view: the "name" part is unenforceable against plain reference and isn't expected to be honored. The agent agreed on practical enforceability but noted that the clause severs rather than voiding the contract.
- **The orange starburst is Claude's official logo, not a community variant.** Simple Icons and Lobe Icons redraw official marks (their MIT license covers the SVG code, not trademark rights).
- **Reported, secondary source only:** Anthropic v. Abnormal AI, N.D. Cal. 3:26-cv-06754 (filed 2026-07-01), over the slash logo. Not verified on a court record.

## Decisions Made

- **Diagram corners:**
  - "You" uses a generic person icon.
  - "AI provider" uses Lucide `bot` (ISC, with the notice kept inline), in the site's accent blue.
  - "GitHub" uses the official mark, in black and unaltered, as permitted for showing integration.
- **No Anthropic marks and no lookalikes on the site.** The intermediate versions (the "A\" badge, a 4-lobed orbital) were dropped when the corner went provider-neutral.
- **No OpenAI or Gemini logos** until other providers actually work. Showing them would imply an integration that doesn't exist.
- **Training Q&A wording, from Dan:** governed by "your model provider's terms of service"; ask an agent to translate it from lawyer to English.
- **Accepted wording debt:** the site text still says "Claude" throughout, while the diagram says "AI provider". Dan chose not to rework the text now; this is tracked in #102.
- **#36 closed** with a per-item disposition comment.

## Results

- Shipped: `danparshall/site-claude-researcher` `c449119`, "Privacy section: data-flow diagram, training and encryption Q&As". Verified live on clauderesearch.ai, identical to the committed `index.html`.

## Open Questions

- Should the natural-recall example from #36 ("remember the woman we spoke about last week? … the one with the blue hair?") become copy in HUMANS.md or on the site?
- The phone layout has no icons. Add them?
- The SVG label positions were computed rather than checked visually on several browsers or fonts.
- If the logo question comes back, the route is to ask marketing@anthropic.com for permission.

## Captured Tasks

- [#101: Add AGENTS.md entry point for non-Claude agents](https://github.com/danparshall/claude_researcher/issues/101) — captured 2026-10-19
- [#102: Test the workflow with non-Claude AI providers](https://github.com/danparshall/claude_researcher/issues/102) — captured 2026-10-19
- [#103: Synth-data pseudofile tool for sensitive datasets](https://github.com/danparshall/claude_researcher/issues/103) — captured 2026-10-19 (split from #36)
