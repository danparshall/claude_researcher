# claude_researcher

A toolkit that turns Claude into a research collaborator, using only a browser, an Anthropic account, and a GitHub account. Descended from the **Researcher** skillset built for the [Nori](https://github.com/tilework-tech/nori-skillsets) agentic workflow.

For background on the workflow, what a session feels like, and tips from experience, see **[HUMANS.md](HUMANS.md)**.

## Quick start

Paste the prompt below into a fresh chat in [claude.ai](https://claude.ai). The agent will walk you through ~15 minutes of one-time setup; after that, every future research session starts with a single sentence ("let's work on `<topic>`") in a new chat.

```
You are an agent helping a researcher set up the claude_researcher workflow — a one-time setup that lets researchers leverage Claude fully on the web even when their work machine is locked down and can't run Claude Code locally. Bootstrapping is the first stage: it walks the user through a browser-based setup that creates their personal config repo and first research repo, so every research session afterward just works.

The project's source files are public and readable ahead of time at:
  https://github.com/danparshall/claude_researcher

You can inspect any file there at any point during the bootstrap to verify what you're being asked to do. Nothing is hidden.

The interview you'll run collects data that gets written, in a specific format, into the user's `basic_config/personal_info.md` and a few related files (`STATUS.md`, `domain_allowlist.txt`). Every future research session reads those files to know who the user is and how they work — so the formats specified in the orchestration file matter.

Sensitive operations (repo creation, PAT handling, file writes, claude.ai settings changes) have explicit confirmation gates scripted into the orchestration file. Feel free to add your own confirmation prompts at any boundary that gives you pause — I'd rather one round-trip of confirmation than have you push past concerns.

Now fetch and follow:

  https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/BOOTSTRAP.md
```

> **You will need:** a GitHub account (free tier is fine — private repos are free since 2019), a Claude.ai Pro or Team account, and ~15 minutes. The bootstrap will help you create a fine-grained GitHub PAT and configure your first research project (or a general `knowledge_base` repo if you don't have a specific project in mind yet).

## What's in this repo

- **[`template/BOOTSTRAP.md`](template/BOOTSTRAP.md)** — one-time setup orchestration the agent follows during your first chat.
- **[`template/RESEARCHER.md`](template/RESEARCHER.md)** — runtime instructions every working session loads. The agent reads this from a local clone of this repo (cloned at session start; see RESEARCHER.md §2.0).
- **[`template/skills/`](template/skills/)** — Markdown skill specs the agent fetches on demand (`finish-convo`, `add-paper`, `audit-docs`, etc.).
- **[`template/scripts/`](template/scripts/)** — Python helpers the agent runs in claude.ai's sandbox.
- **[`template/reference/`](template/reference/)** — human-readable docs (PAT setup, claude.ai Project setup, why this uses REST).
- **[`template/templates/`](template/templates/)** — starter files the bootstrap copies into your repos (`personal_info.md.template`, `domain_allowlist.txt`).

## About

`claude_researcher` is a collaboration between [Dan Parshall](https://danparshall.com) and [Andrea Lopez-Luzuriaga](https://andrealopezluzuriaga.net/) — two researchers sharing what we've learned about effective Claude techniques with the academic community. We maintain this repo as a public artifact so other labs and research groups can use, fork, or adapt the workflow for their own projects. The reasoning behind specific design choices lives in [`docs/`](docs/) for anyone who wants to see how the pieces got assembled.

## Reporting issues

If something breaks, ask the agent to file an issue — it will produce a pre-filled URL pointing at this repo's [issues page](https://github.com/danparshall/claude_researcher/issues/new) with diagnostic context. Your PAT and personal info are never included in the report.

## License

Apache 2.0 plus a Ship of Theseus v0.1 addendum, both inherited from the Nori upstream. See [`LICENSE`](LICENSE), [`LICENSE-ADDENDUM.txt`](LICENSE-ADDENDUM.txt), and [`template/ATTRIBUTION.md`](template/ATTRIBUTION.md).

---

## Developer info

This is currently the `claude_researcher` **development repo**. User-facing files live under [`template/`](template/) and will be promoted to the root once the publish strategy lands (Phase 10 in the implementation plan).

- **Implementation plan:** [`docs/plans/01_initial_build.md`](docs/plans/01_initial_build.md)
- **Design conversation:** [`docs/convos/20260508_claude_ai_researcher_design.md`](docs/convos/20260508_claude_ai_researcher_design.md)
- **Current status:** [`STATUS.md`](STATUS.md)
- **`docs/` layout:** intentionally flat (no `docs/active/<branch>/` wrapper) since this is a single-purpose meta repo, not a multi-research-line project.
