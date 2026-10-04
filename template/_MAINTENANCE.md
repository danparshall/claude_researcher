# Maintenance note — RESEARCHER.md has a CLI sibling

The rules in this profile (`RESEARCHER.md`) also live in a CLI-agent sibling
profile:
[`danparshall/dotfiles → nori-researcher/AGENTS.md`](https://github.com/danparshall/dotfiles/blob/main/nori-researcher/AGENTS.md).
The two share a persona + workflow core but target different substrates:
claude.ai web (this file) vs Claude Code CLI.

**If you are the profile maintainer** — Dan, or a fork maintainer keeping both
sides in sync — before adding or changing a rule in `RESEARCHER.md`, check the
decision rubric in
[`danparshall/dotfiles`](https://github.com/danparshall/dotfiles/blob/main/notes/researcher_profile_maintenance.md)
(`notes/researcher_profile_maintenance.md`, section "Rubric — which file does a
rule belong in?"). It classifies the change (persona / universal discipline /
substrate-specific / user-facing calibration / session ceremony) and tells you
which file(s) it lands in. Skip the rubric only when the change is unambiguously
one-substrate (e.g., the §2 clone-first fetch sequence has no CLI analog).

**The persona text in §0 is generated — do not edit it here.** Everything
between the `<!-- PERSONA:START … -->` and `<!-- PERSONA:END -->` markers in
`RESEARCHER.md` is copied from the `# Persona` section of
`nori-researcher/AGENTS.md` in dotfiles by the skill exporter, and any hand
edit between the markers is overwritten on the next export. Make persona
changes in `AGENTS.md`. The §0 heading and the "Tier-independent…" line above
the start marker stay hand-written here, as does everything after the end
marker.

**If you're a downstream user** of `claude_researcher` (an academic running the
profile via bootstrap): you can ignore this file. It's a maintainer's aid;
nothing in `RESEARCHER.md` depends on it. Downstream forkers who intend to
maintain their own CLI sibling may find the rubric useful.
