# Attribution

Copyright 2026 Dan Parshall, downstream of Nori (`tilework-tech/nori-skillsets`) under Apache 2.0 + Ship of Theseus v0.1 addendum.

## Provenance chain

1. **Upstream:** [Nori Skillsets](https://github.com/tilework-tech/nori-skillsets) — the original `researcher` Skillset for Claude Code on a developer's local machine.
2. **This work:** `claude_researcher` — a port of the researcher workflow to claude.ai's web UI, so collaborators on locked-down machines can use the research-first workflow with browser-only setup.
3. **Downstream:** Each collaborator's `<USERNAME>/claude_research_config` (their lifetime config) and `<USERNAME>/research-<topic>` repos (their research artifacts). Those are their work; this project neither claims nor licenses their content.

## License terms

Both [`LICENSE`](LICENSE) (Apache 2.0) and [`LICENSE-ADDENDUM.txt`](LICENSE-ADDENDUM.txt) (Ship of Theseus v0.1) apply in full. The addendum specifically defeats the LLM-cleanroom dodge: using AI tools to produce functionally equivalent software while referencing this code or its abstractions creates a derivative work subject to the full license terms. Both files must travel with any derivative work.

## What's preserved verbatim from upstream

- `LICENSE` (Apache 2.0)
- `LICENSE-ADDENDUM.txt` (Ship of Theseus v0.1)
- The structure and intent of the carried-over skills (see [`skills/`](skills/) for which were carried verbatim and which were REST-adapted).

## What's new in this work

- Bootstrap orchestration ([`BOOTSTRAP.md`](BOOTSTRAP.md)) for one-time browser-based setup.
- Runtime [`RESEARCHER.md`](RESEARCHER.md) adapted for claude.ai's session model (Project Instructions bootstrap + REST API access via PAT).
- REST API adaptations of git-CLI-using skills (`finish-convo`, `update-docs`, `add-paper`, `init-research-repo`, `audit-docs`, `audit-papers`).
- Python helpers in [`scripts/`](scripts/) for the REST workflow and PDF text extraction.
- `_PROJECT_INSTRUCTIONS.md` template + Domain Allow List baseline.
