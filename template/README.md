# claude_researcher

Browser-only research workflow for [claude.ai](https://claude.ai). A downstream port of the Nori `researcher` Skillset, adapted so collaborators on locked-down work machines (no shell, no git, no Claude Code) can use a research-first workflow with nothing but a browser, a Claude.ai Pro account, and a GitHub PAT.

The agent reads its instructions from this repo at runtime, and reads/writes your research artifacts via the GitHub REST API from claude.ai's sandbox.

## Quick start

If a colleague pointed you here, paste the prompt below into a fresh chat in claude.ai. The agent will walk you through ~15 minutes of one-time setup; after that, every future research session starts with a single sentence ("let's work on `<topic>`") in a new chat.

```
You are running the claude_researcher bootstrap. Fetch and follow the
instructions at:

https://raw.githubusercontent.com/danparshall/claude_researcher/main/BOOTSTRAP.md

Read that file end-to-end, then begin. Do not skip steps.
```

> **You will need:** a GitHub account (free tier is fine), a Claude.ai Pro or Team account, and ~15 minutes for setup. The bootstrap will help you create a fine-grained GitHub PAT and configure your first research project.

## What this repo provides

- **[`BOOTSTRAP.md`](BOOTSTRAP.md)** — one-time setup orchestration the agent follows during your first chat.
- **[`CLAUDE.md`](CLAUDE.md)** — runtime instructions every working session loads.
- **[`skills/`](skills/)** — Markdown skill specs the agent fetches on demand (`finish-convo`, `add-paper`, `audit-docs`, etc.).
- **[`scripts/`](scripts/)** — Python helpers (REST wrappers, repo creation, PDF extraction) the agent runs in claude.ai's sandbox.
- **[`reference/`](reference/)** — human-readable docs (PAT setup, claude.ai Project setup, why this uses REST).
- **[`templates/`](templates/)** — starter files the bootstrap copies into your repos (e.g., `domain_allowlist.txt`).

## Reporting issues

If something breaks, ask the agent to file an issue — it will produce a pre-filled URL pointing at this repo's [issues page](https://github.com/danparshall/claude_researcher/issues/new) with diagnostic context. Your PAT and personal info are never included in the report.

## License

Apache 2.0 plus a Ship of Theseus v0.1 addendum, both inherited from the Nori upstream. See [`LICENSE`](LICENSE), [`LICENSE-ADDENDUM.txt`](LICENSE-ADDENDUM.txt), and [`ATTRIBUTION.md`](ATTRIBUTION.md).
