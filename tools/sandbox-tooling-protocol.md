# Sandbox Tooling Verification Protocol

Methodology for keeping [`template/reference/SANDBOX_TOOLING.md`](../template/reference/SANDBOX_TOOLING.md) honest. This file is the *how*; SANDBOX_TOOLING.md is the *what* — the current snapshot plus verification history.

## What goes in the matrix

A tool earns a row when:

- A current or near-future skill port depends on its presence (e.g. `add-paper` needs `pypdf`, `branch-document-review` needs `pandoc`).
- A re-verification would catch a regression that meaningfully affects the workflow (e.g. `git` for clone-first session start).

A tool's row stays after its dependent skill ships, so future drift remains visible. Remove a row only if the dependent skill is itself removed.

## Protocol

Run the probe script from SANDBOX_TOOLING.md in a fresh claude.ai sandbox chat. Capture:

1. Each tool's exact version string (not rounded).
2. Whether install was required or it was pre-installed.
3. Any environment-baseline shifts (Ubuntu version, Python version, PEP-668 / `--break-system-packages` posture).

## Updating SANDBOX_TOOLING.md after a probe

For each tool row:

- Update **Version observed** if it changed.
- Update **Status** if `available` ↔ `unavailable` flipped.
- Update **Install** if the procedure changed.
- Edit **Notes** if posture changed (e.g. PEP-668 requirement appeared/disappeared).

Then append a row to **Verification history** with date, verifier, surface, and a one-line findings summary.

If a tool flipped to `unavailable`, **stop and surface to the user before continuing** — the workaround table needs activation, dependent Wave plans may need revisiting, and the change is large enough to warrant a planning beat rather than a silent update.

## Cadence

- **Quarterly:** baseline re-run.
- **On port-time discovery:** if a skill port surfaces an unexpected tooling gap, run the probe and update both files in the same session.
- **On environment signals:** Ubuntu base version changes, Python version bumps, PEP-668 policy shifts, or any agent observation that sandbox tooling differs from the matrix.

## Why this is separate from SANDBOX_TOOLING.md

The reference doc is a versioned snapshot the agent reads at decision time. This protocol is the methodology a maintainer applies when refreshing the snapshot. Mixing them obscures which lines are facts about the world and which are instructions for future work.
