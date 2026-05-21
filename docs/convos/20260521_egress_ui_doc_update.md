# 20260521 — Egress Step 1 made UI-agnostic

**Date:** 2026-05-21
**Branch:** egress-docs-ui-agnostic
**Surface:** Claude Code (CLI)

## Summary

Immediately after the bootstrap SHA-pin fix (see `20260520_bootstrap_sha_pin.md`)
verified working, Dan reported via screenshot that claude.ai's network-egress
Settings UI had changed. The old `BOOTSTRAP.md` Step 1 walked the user through a
mode selector (`Package Managers Only` / `All`) plus a free-form **Domain Allow
List** into which they typed `api.github.com` and three other GitHub domains. The
screenshot (a free-plan account) showed instead a single **"Allow network egress"**
toggle described as *"access common package managers"*, a "View package manager
domains" link, and **no visible custom domain allow-list**.

Dan's redirect: rather than re-scripting against the new UI, make Step 1
**UI-agnostic** — *"allow all domains for now (if you're given the option to
provide a whitelist later, you'll need to include these four at a minimum)"* — and
he hypothesized the UI variant may depend on account tier (free vs paid). Step 1
was rewritten to guide by intent, not by widget. The 1a probe
(`curl api.github.com/zen`) was already the empirical arbiter, so the doc no
longer needs to know the exact UI.

## Topics Explored

- Screenshot of `claude.ai/settings/capabilities` — new single-toggle egress UI on
  a free-plan account; old mode-selector + custom Domain Allow List not visible
- A `nori-web-search-researcher` agent was dispatched to find Anthropic's current
  egress model + whether GitHub domains count as "package manager domains" — it
  **timed out with no result**; not retried (Dan's redirect made a precise domain
  list moot)
- Grepped `BOOTSTRAP.md` + `RESEARCHER.md` + skills for residual `allow-list` /
  `egress` references

## Provisional Findings

- The egress UI changed and **varies by account type** (Dan's hypothesis; not
  independently confirmed). A doc that scripts exact clicks is inherently fragile
  against this — the same failure mode as the stale-`web_fetch` bug from the prior
  session, in a different layer.
- **Unresolved and load-bearing:** whether enabling the free-tier single toggle
  actually lets the sandbox reach `api.github.com`. If "allow network egress" on a
  free account is genuinely package-managers-only and GitHub is not in that set,
  the kit cannot onboard a free-tier user regardless of doc wording. No doc change
  resolves this — it needs an empirical test (the 1a probe, run on a free account
  after enabling egress).

## Decisions Made

- **Rewrote `BOOTSTRAP.md` Step 1b** to be UI-agnostic: enable network egress, pick
  the most permissive option the UI offers (toggle / mode choice / custom
  allow-list); if a domain allow-list exists, the four GitHub domains are the
  minimum (paper-source domains optional, conditional on a list UI existing).
  Added an agent note that the UI varies and exact-click scripts go stale, plus a
  "stop and surface if unrecognized" escape hatch.
- **§1 header** renamed "Egress allow-list check" → "Network egress check".
- **Terminology sweep** — "Domain Allow List" / "the allow list" → "network egress"
  across the fetch-mechanisms note, Step 3 lead-in, two `BOOTSTRAP.md`
  troubleshooting entries, and `RESEARCHER.md`'s session-start troubleshooting.
- The 1a probe and the 1c fresh-chat hand-off were left intact.
- Shipped in commit
  [`c484f95`](https://github.com/danparshall/claude_researcher/commit/c484f95)
  (2 files, +19 −29). Dan reviewed the §1b wording — "LGTM".

## Results

No analysis artifacts. Result is the egress-doc rewrite on `egress-docs-ui-agnostic`.

## Open Questions

- **Free-tier GitHub reachability** (above) — needs an empirical probe on a free
  account. The single most important open item.
- **`domain_allowlist.txt`'s role.** The bootstrap still seeds a
  `domain_allowlist.txt` into `basic_config`, and the Step 4 interview (Batch 3)
  still asks for paper-source domains "we'll add to your `domain_allowlist.txt`."
  Both assume the user can actively allow-list domains. Under the new model that is
  uncertain. The file could be reframed as exactly what Dan's instruction
  described — *the list of domains to add if/when the UI offers a whitelist* — but
  that is a deliberate reframe, deferred out of this branch. Not yet captured as a
  task/issue.
