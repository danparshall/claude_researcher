# claude_researcher (dev repo)

Development repo for `claude_researcher` — a downstream fork of the [Nori researcher Skillset](https://github.com/tilework-tech/nori-skillsets) adapted for the claude.ai web UI. The eventual public repo will let non-CLI-savvy collaborators (scientists, professors, economists) on locked-down work machines use a research-first workflow with browser-only setup, via claude.ai Project + GitHub PAT + REST API.

## Structure

- `template/` — content destined for the public repo (CLAUDE.md, BOOTSTRAP.md, skills, scripts, references, license).
- `docs/convos/` — design and progress conversations.
- `docs/plans/` — implementation plans.

The `docs/` layout is intentionally **flat** (no `docs/active/<branch>/` wrapper) since this is a single-purpose meta repo, not a multi-research-line project.

## Where to start

- **Implementation plan:** [`docs/plans/01_initial_build.md`](docs/plans/01_initial_build.md)
- **Design conversation:** [`docs/convos/20260508_claude_ai_researcher_design.md`](docs/convos/20260508_claude_ai_researcher_design.md)
- **Current status:** [`STATUS.md`](STATUS.md)

## License

Apache 2.0 + Ship of Theseus v0.1 addendum, both inherited from Nori upstream. See [`LICENSE`](LICENSE) and [`LICENSE-ADDENDUM.txt`](LICENSE-ADDENDUM.txt). Copyright + Nori chain attribution lands in `template/ATTRIBUTION.md` (Phase 2 task 4).
