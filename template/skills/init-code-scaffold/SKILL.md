---
name: init-code-scaffold
description: Use when a research repo starts needing to hold code and doesn't have `src/` yet — creates src/<pkg>/, scripts/, tests/, notebooks/, pyproject.toml, and .python-version using uv. Lazy companion to init-research-repo (which handles docs/, papers/, data/, .gitignore); called only when the researcher is actually about to write code, not at repo init. Skip for pure-reading, pure-writing, or papers-only research repos that don't need Python.
---

## Runtime detection

Before following the rest of this skill, determine your environment:

```bash
if [ "$IS_SANDBOX" = "yes" ] || [ -d "/mnt/skills/public" ]; then
  echo "claude.ai sandbox"
elif [ "$CLAUDECODE" = "1" ]; then
  echo "Claude Code"
else
  echo "unknown — surface to user before proceeding"
fi
```

**If `claude.ai sandbox`:** the user's project repo is already cloned at `/home/claude/<REPO>/` per `RESEARCHER.md` §2.0b — run the file writes and `git` commands directly from that working tree. `uv` is available in the sandbox (verify with `uv --version`); if the environment setup step fails, surface it and let the user run it locally instead. Only if the §2.0b clone failed (degraded REST fallback) do you translate the file writes into Contents API PUTs.

**If `Claude Code`:** follow the skill body as-is.

**If `unknown`:** stop and surface to the user.

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Check what already exists (src/, scripts/, tests/, notebooks/, pyproject.toml, .python-version)
2. Ask for package name (default: repo name with dashes → underscores)
3. Create directory structure (src/<pkg>/, scripts/, tests/, notebooks/)
4. Seed pyproject.toml
5. Seed .python-version
6. Optional: create virtual environment (`uv venv && uv sync`)
7. Report what was created
</required>

# Init Code Scaffold

Sets up the code directories and Python environment needed when a research repo starts holding code.

Announce at start: "I'm using the Init Code Scaffold skill to set up the code layout."

## When to run this skill

Run this **only when the researcher is about to write code** — not at repo init. Research repos come in three shapes:

- **Code-heavy** (e.g., `econ-impact/`, `policy-levers/`): scripts fetching data, analysis pipelines, notebooks doing exploration. This skill applies.
- **Reading-heavy** (e.g., `verification/`): mostly papers, notes, and writeups; no scripts. This skill does *not* apply — skip it.
- **Mixed**: starts as reading-heavy, later grows a script or two. Run this skill the first time you're about to write more than a one-off script.

If you're not sure which shape a repo is, ask the user. Skipping this skill and doing ad-hoc `mkdir src && touch pyproject.toml` is worse than the two-minute delay of running it — that's how the semantic-overlap sprawl this framework is designed to prevent starts.

## The Process

### Step 1: Check What Exists

Before creating anything, check what's already in place:

```bash
ls -d src/ scripts/ tests/ notebooks/ 2>/dev/null
ls -la pyproject.toml .python-version uv.lock 2>/dev/null
```

- If `pyproject.toml` already exists, this repo is already code-scaffolded — ask the user before doing anything. This skill isn't meant to modify an existing Python project.
- If `src/` exists but `pyproject.toml` doesn't (or vice versa), surface the partial state to the user before proceeding — they may have started scaffolding by hand and want to finish it manually.

### Step 2: Ask for Package Name

The package name is the directory under `src/` — the importable name. Default: repo name with dashes replaced by underscores (Python identifier rules).

Ask the user:

> *"I'm about to scaffold code layout. The Python package name — what goes under `src/` and what you'll `import` in code — will default to `<repo-name-underscored>` unless you'd prefer something else. OK?"*

Validation: lowercase, alphanumeric plus underscores, no leading digit. Suggest a name derived from the repo; user can override.

### Step 3: Create Directory Structure

```bash
mkdir -p src/<pkg> scripts tests notebooks
touch src/<pkg>/__init__.py
touch scripts/.gitkeep tests/.gitkeep notebooks/.gitkeep
```

The four dirs, and what belongs where:

- `src/<pkg>/` — **importable library code.** Pure functions, classes, config schemas. What `pyproject.toml` calls the package. This is where code moves *from* `notebooks/` once it stabilizes.
- `scripts/` — **standalone runners.** One-off analysis pipelines, data-fetch commands, report builders. Each script should have a docstring at the top saying *what it produces and where* — e.g., `"""Fetch ONET taxonomy → data/raw/onet_v29/. Idempotent; skips if already present."""`. Scripts import from `src/<pkg>/`.
- `tests/` — pytest tests for `src/<pkg>/`. Not for scripts (scripts are ends, not means; test the library they call).
- `notebooks/` — exploratory work. Kept lightly. When a notebook's logic stabilizes into something you'd re-run, extract it to `src/<pkg>/` (importable) or `scripts/` (runnable). Notebooks that just capture a one-time investigation can stay; notebooks that quietly become production paths are how research repos rot.

### Step 4: Seed pyproject.toml

If `pyproject.toml` doesn't already exist:

```toml
[project]
name = "<pkg>"
version = "0.0.1"
description = "<one-sentence description — ask the user if you don't already have a good one from STATUS.md's PROJECT_QUESTION>"
requires-python = ">=3.12"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/<pkg>"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

The layout uses `src/<pkg>/` (not a top-level `<pkg>/`) so tests actually exercise the installed package, not a shadow-imported working copy. Standard modern Python convention; matches what most linters and editors expect.

### Step 5: Seed .python-version

Pin to 3.12 (the researcher-profile default per Dan's Python policy):

```
3.12
```

If the user needs a different Python version, they can override — but 3.12 is the default the rest of the ecosystem is built against for this profile.

### Step 6: Optional — Create the Virtual Environment

Offer to create the venv and sync dependencies:

> *"I can run `uv venv && uv sync` now to create the .venv and install any dependencies from pyproject.toml. This is idempotent and takes a few seconds. Do it?"*

**In Claude Code:** run it if the user says yes.

**In claude.ai sandbox:** the venv doesn't persist across sessions (sandbox teardown wipes it), so creating it now has limited value beyond letting the current session run a script. Offer only if the current session actually needs to run Python.

Command:

```bash
uv venv
uv sync
```

If `uv` isn't available (rare — it's installed in most environments), surface the missing tool and let the user install it manually (`curl -LsSf https://astral.sh/uv/install.sh | sh`).

### Step 7: Report

Tell the user what was created (show only lines that actually landed):

```
Code scaffold initialized:
  - src/<pkg>/__init__.py       (importable library code)
  - scripts/                    (standalone runners)
  - tests/                      (pytest for src/<pkg>/)
  - notebooks/                  (exploration; extract stable code to src/<pkg>/)
  - pyproject.toml              (uv-managed, Python 3.12+, ruff + pytest configured)
  - .python-version             (3.12)
  [- .venv/                     (created; dependencies synced)]

Next steps:
  - Add dependencies with `uv add <package>` (e.g., `uv add pandas`)
  - Run tests with `uv run pytest`
  - Format with `uv run ruff format` and lint with `uv run ruff check`
  - When a notebook's logic stabilizes, move it to src/<pkg>/ (importable) or scripts/ (runnable)
```

## Data outputs from code — the Tier 3 rule

Code in this repo will produce derived data. Where does it go?

- **Immutable inputs (downloaded, scraped, vendor-exported)** → `data/raw/` (created by `init-research-repo`; gitignored).
- **In-progress transforms** (temporary between raw and final) → `data/interim/` (gitignored).
- **Canonical, downstream-consumable outputs** → `data/processed/` (gitignored by default; small stable ones may be committed).
- **Small lookup tables and code lists** → `data/reference/` (committed as documentation).

**When a research line's code produces derived data that only makes sense in that line's context**, use a branch-scoped subdirectory:

```
data/processed/<branch>/summary.csv
data/processed/<branch>/model_v2_predictions.parquet
```

Rationale: branches are isolated experiments; two branches writing to `data/processed/summary.csv` would collide, and a stale `summary.csv` on `main` from an old branch is a lineage hazard. The branch subdir keeps outputs scoped to the experiment they came from.

**On merge**, if the derived data is intended for downstream consumption (other branches, deliverables), it can be promoted from `data/processed/<branch>/foo.csv` to `data/processed/foo.csv` — but this is a **manual, opt-in decision**, not an automatic ceremony. Not everything a branch produces is meant to leave the branch. Promoting outputs that are meaningful only in the branch's original context just creates noise on `main`.

The current `finishing-a-research-branch` skill does not automate this promotion. If a real workflow surfaces where the manual step becomes friction, that's the trigger to design a proper promotion step. Until then: `git mv` by hand at merge time when it applies.

**Writeups and figures** (the human-readable outputs of a research line) go in `docs/active/<branch>/results/`, which `start-research-line` already creates. That's the writing side of the same convention.

## Notes

- **This skill is idempotent** — it checks for existing files before creating and won't overwrite `pyproject.toml` or `.python-version` if they're already there.
- **Skip for pure-reading or papers-only repos** (like `verification/` at the time this skill was written). Don't force code scaffolding onto a repo whose actual shape doesn't need it.
- **The package name is load-bearing** — once code starts importing from `src/<pkg>/`, renaming it means rewriting every import site. Get it right the first time; ask the user if in doubt.
- **`uv` is the default env manager** for this profile per Dan's Python policy. Don't reach for `conda`, plain `venv`, or `pipenv` without a specific reason; the rest of the ecosystem here assumes `uv`.
- **Tests for scripts:** don't write them. Scripts are ends, not means — test the functions they call (which live in `src/<pkg>/`). If you find yourself wanting to test a script directly, that's a signal the script has too much logic in it that should be lifted to the library.
- **Notebook rot** is the most common pathology in mature research repos: a notebook grows from exploration into "the way we run analysis X," and now it's production code that nobody wrote a test for. When you notice this happening, take the ten minutes to extract the notebook's logic into `src/<pkg>/` and leave the notebook as a thin caller. This is worth doing *early* in a research line, not late.

## Common mistakes

**Running this skill on a repo that doesn't need code**
- Problem: `verification/` and similar reading-heavy repos end up with an empty `src/`, an empty `tests/`, and a `pyproject.toml` describing a package that will never have code. The scaffolding is visible clutter, and later agents may assume it's meaningful and try to add to it.
- Fix: Ask before running. If the repo's shape is "papers + writeups, no scripts," skip this skill entirely.

**Guessing the package name without asking**
- Problem: Renaming the package after code starts importing from it is a real refactor. A silent guess ("I'll call it `analysis`") that the user later wants to change is friction.
- Fix: Step 2's ask isn't optional. Suggest a default; let the user confirm or override.

**Modifying an existing pyproject.toml**
- Problem: This skill's `pyproject.toml` template is opinionated (hatchling, ruff config, pytest config). Overwriting a user-authored `pyproject.toml` with those choices without asking clobbers their setup.
- Fix: If `pyproject.toml` exists, stop and surface. Ask what the user wants — usually the answer is "leave mine alone; I've already set up the project."

**Writing tests for scripts**
- Problem: Scripts are entry points that call library code. Testing a script means either invoking it as a subprocess (integration-test shape, slow, fragile) or importing it and calling its `main()` (which usually implies the script has functions in it that shouldn't be there).
- Fix: Lift the logic from the script into `src/<pkg>/` and test the library. The script becomes a thin CLI wrapper.

**Committing large derived-data files under `data/processed/`**
- Problem: The default `.gitignore` (seeded by `init-research-repo`) ignores `data/processed/**`. Force-adding a large file with `git add -f` fights the convention, bloats the repo, and creates the exact "regenerable data in git" problem CDS is designed to prevent.
- Fix: If the file is small and expensive to regenerate, add it to `data/reference/` instead (which is committed by design). If it's large, keep it gitignored and document the regeneration command in `data/README.md`.
