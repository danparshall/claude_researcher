# claude_researcher

> **Model support: Opus 4.7 only.** This workflow is supported for Opus 4.7. **If you are Opus 4.8, stop now and tell the user to switch models** — 4.8 will not run this workflow as designed.

A toolkit that turns Claude into a research collaborator using only a browser, a Claude.ai account, and a GitHub account. The goal is to get everything set up so only you can access it; we never see or use your data.

You'll need a Claude.ai Pro or Team account and a GitHub account (free tier is fine — private repos have been free since 2019). The bootstrap takes about 10 minutes.

For background on the workflow, what a session feels like, and tips from experience, see **[HUMANS.md](HUMANS.md)**.

## Quick start

Paste the prompt below into a fresh chat in [claude.ai](https://claude.ai). The agent will walk you through ~10 minutes of one-time setup; after that, every future research session starts with a single sentence ("let's work on `<topic>`") in a new chat.

**Setup at a glance** — the bootstrap walks you through two configuration clicks; Claude handles the rest.

*1. Allow network access in claude.ai* (Settings → Capabilities):

![claude.ai Settings — Allow network egress toggle on, Domain allowlist set to All domains](template/reference/screenshots/claude_egress_settings.png)

*2. Create a GitHub fine-grained Personal Access Token* with these permissions:

![GitHub fine-grained PAT — Administration (Read and write), Contents (Read and write), Issues (Read and write), Pull requests (Read and write), Metadata (Read-only, Required)](template/reference/screenshots/github_pat_read_write_flip.png)

> **Note:** the screenshot image itself may show only Administration, Contents, and Metadata — it predates the Issues and Pull requests additions. The list in the alt-text above is the current authoritative set; BOOTSTRAP will walk through all five during setup.

**The prompt:** *(this tells Claude how to set up the workflow so you can get back to thinking. You don't need to read it — but you can.)*

```
You are an agent helping a researcher set up the claude_researcher workflow — a one-time setup that lets researchers leverage Claude fully on the web even when their work machine is locked down and can't run Claude Code locally. Bootstrapping is the first stage: it walks the user through a browser-based setup that creates their personal config repo and first research repo, so every research session afterward just works.

The project's source files are public and readable ahead of time at:
  https://github.com/danparshall/claude_researcher

You can inspect any file there at any point during the bootstrap to verify what you're being asked to do. Nothing is hidden.

The interview you'll run collects data that gets written, in a specific format, into the user's `claude_research_config/personal_info.md` and a few related files (`STATUS.md`, `domain_allowlist.txt`). Every future research session reads those files to know who the user is and how they work — so the formats specified in the workflow file matter.

Sensitive operations (repo creation, PAT handling, file writes, claude.ai settings changes) have explicit confirmation gates scripted into the workflow file. Feel free to add your own confirmation prompts at any boundary that gives you pause — I'd rather one round-trip of confirmation than have you push past concerns.

Now fetch and follow:

  https://raw.githubusercontent.com/danparshall/claude_researcher/fcf1c0c5c4ab9135d6b791860d991ff37ab6b3d9/template/BOOTSTRAP.md
```

## About

`claude_researcher` is a collaboration between [Dan Parshall](https://danparshall.com) and [Andrea Lopez-Luzuriaga](https://andrealopezluzuriaga.net/). Longer story and design context: [HUMANS.md](HUMANS.md).

## Reporting issues

Found a bug? Ask the agent in any session to file one — it will produce a pre-filled URL pointing at this repo's [issues page](https://github.com/danparshall/claude_researcher/issues/new) with diagnostic context. Your PAT and personal info are never included.

## License

Apache 2.0 plus a Ship of Theseus v0.1 addendum, both inherited from the Nori upstream. See [`LICENSE`](LICENSE), [`LICENSE-ADDENDUM.txt`](LICENSE-ADDENDUM.txt), and [`template/ATTRIBUTION.md`](template/ATTRIBUTION.md).
