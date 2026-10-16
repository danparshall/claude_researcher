# The `.gitignore` kit block

The floor promises that package binaries are gitignored (`structure_conventions.md`, the
outbound-packages home) and, until v6.4, nothing shipped the rule. This file is the seed. A repo's
`.gitignore` is project-owned; the block below is kit-owned, written verbatim between its two
marker lines by Part A step 2 and Part B Step 2b, and regenerated at every propagation by Part
C Step 7.5 (the repo's own rules outside the markers are never touched). The audit reads the
block against this text (`repo_audit_skill.md` Check 14). Kit metadata, always-active group;
not read at session start.

```gitignore
# --- kit block: begin (structure_conventions.md; regenerated at every propagation) ---
# Outbound packages: the build script is tracked, the copied binaries and zips are not
workspace/packages/**/*.zip
workspace/packages/**/*.docx
workspace/packages/**/*.pptx
workspace/packages/**/*.pdf
workspace/packages/**/*.xlsx
# Python and script residue
__pycache__/
*.pyc
node_modules/
# Operating-system files
.DS_Store
Thumbs.db
desktop.ini
# --- kit block: end ---
```

---
*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
