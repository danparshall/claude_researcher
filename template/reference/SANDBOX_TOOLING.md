# Sandbox Tooling Matrix

**Last verified:** 2026-05-11 by `danparshall` in a claude.ai Project chat (the probes are sandbox-level — package availability and system binaries don't depend on Project attachment — so the result generalizes to unattached chats).

This file records which document-processing and analysis tools are available in claude.ai's sandbox, so skill ports can rely on tested capabilities rather than assumed ones. **Re-verify quarterly or whenever a port discovers a discrepancy.**

## Environment baseline

- **OS:** Ubuntu 24.04
- **Python:** 3.12.3
- **`pip` install posture:** `--break-system-packages` required for system-wide installs (PEP 668). The "Package Managers Only" egress preset makes `pip install` work on-the-fly.

## Tools

### pypdf

- **Status:** available (pre-installed)
- **Version observed:** 5.9.0
- **Install:** not required; `pip install pypdf --break-system-packages` if a fresh install is ever needed
- **Verify:** `python3 -c "import pypdf; print(pypdf.__version__)"`
- **Wave dependency:** Phase 5 task 31 (`add-paper` PDF text extraction)
- **Notes:** none — pre-installed in `/usr/local/lib/python3.12/dist-packages`.

### pandoc

- **Status:** available (pre-installed as a system binary)
- **Version observed:** 3.1.3 (features: `-server +lua`)
- **Install:** not required; `apt-get install -y pandoc` if ever absent (root access in sandbox makes this work)
- **Verify:** `which pandoc && pandoc --version | head -1`
- **Wave dependency:** Wave 4 (`branch-document-review` regeneration step in `docs/plans/02_skill_ports.md`)
- **Notes:** This was the medium-confidence item in Plan 04 — turned out to be a non-issue. The `pypandoc` Python wrapper fallback documented in the plan is therefore unnecessary on the primary path; keep it in the workaround table below in case of future regressions.

### python-docx

- **Status:** available (pre-installed)
- **Version observed:** 1.2.0 (with `lxml` 6.0.2)
- **Install:** not required; `pip install python-docx --break-system-packages` if ever needed
- **Verify:** `python3 -c "from docx import Document; import docx; print(docx.__version__)"`
- **Wave dependency:** Wave 5 (`document-processing` in `docs/plans/02_skill_ports.md`)
- **Notes:** import path is `from docx import Document` (the PyPI package name `python-docx` does not match the import name `docx` — a common gotcha).

### git

- **Status:** available (pre-installed as a system binary)
- **Version observed:** 2.43.0
- **Install:** not required
- **Verify:** `which git && git --version`
- **Architectural dependency:** the clone-first session start (RESEARCHER.md §2.0) — `git clone --depth 1` of the upstream template at session start. Empirically benchmarked at ~335ms for the 896K template repo during the 2026-05-11 dogfooding session.
- **Notes:** none.

## Workaround table

These workarounds are documented for completeness. None are needed today; every primary tool above is `available` (pre-installed). Re-check on quarterly re-verification.

| If primary is unavailable | Use instead | Notes |
|---|---|---|
| `pandoc` (system binary) | `pip install pypandoc --break-system-packages` | Bundles its own pandoc binary; install command is `pip install pypandoc --break-system-packages`; verify with `python3 -c "import pypandoc; print(pypandoc.get_pandoc_version())"`. |
| `pandoc` (no install path works) | `difflib` (stdlib) | Wave 4 `branch-document-review` redesign — diff raw markdown directly instead of rendering to docx for visual diff. Existing AITaxBID source already has a `difflib` path. |
| `python-docx` | `mammoth` | docx → HTML conversion (read-only); raw OOXML write fallback if write needed. |
| `pypdf` | `pdfminer.six` | secondary PDF text-extraction library. |
| `--break-system-packages` removed in future Ubuntu base | `pipx` install, or per-project venv | document the new posture in this file when it happens. |

## Probe script

For re-verification:

```bash
echo "=== Environment ==="
python3 --version
cat /etc/os-release | grep -E '^(NAME|VERSION_ID)='

echo "=== git ==="
which git && git --version

echo "=== pypdf ==="
pip install pypdf --break-system-packages 2>&1 | tail -3
python3 -c "import pypdf; print('pypdf', pypdf.__version__)"

echo "=== pandoc ==="
which pandoc && pandoc --version | head -2

echo "=== python-docx ==="
pip install python-docx --break-system-packages 2>&1 | tail -3
python3 -c "from docx import Document; import docx; print('python-docx', docx.__version__)"
```

## Verification history

| Date | Verifier | Surface | Findings summary |
|---|---|---|---|
| 2026-05-11 | danparshall | claude.ai Project chat | All four tools pre-installed; no workarounds needed. |
