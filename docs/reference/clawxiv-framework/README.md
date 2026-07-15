# ClawXiv Framework Paper

**Title:** ClawXiv: a signed archival workflow and distributed publication architecture for human–AI collaborative research
**Author:** András Kornai (SZTAKI Institute of Computer Science; Department of Algebra and Geometry, Budapest University of Technology and Economics). AI co-authors: GPT-5.2 Thinking, Claude Sonnet 4.6, GPT-5.4 Thinking (see paper's Author Contributions section).
**Date:** May 2026 — arXiv v2 (2026-06-05), internal v5.rc2; v1 posted 2026-04-11.
**File:** `clawxiv-framework.pdf` (401 KB, 19 pages)
**Text extraction:** `clawxiv-framework.txt`
**Source:** https://arxiv.org/abs/2604.16476

## Summary

ClawXiv is a workflow and archive architecture for mixed human–AI research that converts volatile chat sessions and heterogeneous LaTeX/BibTeX working directories into durable, content-addressed, Ed25519-signed bundles. It distinguishes four states — legacy seed → normalized project → signed bundle → published artifact — and specifies both the local author-side kernel (already implemented) and a two-foot publication model (arXiv for human-legible discovery + Ethereum Swarm for machine-readable durability). Version 5 adds a layered-signature scheme distinguishing AI-draft layers from human editorial layers, a mediator daemon (`clawxiv-mediate`) for AI-to-AI co-authorship sessions, and a grounding of provenance ceremonies in Austin's speech-act theory and Staal's syntactic account of Vedic ritual.

## Key findings

- **Four-state lifecycle (§3).** Legacy seed → normalized project → signed bundle → published artifact. The normalized project (mutable) is the working surface; the signed bundle (immutable, content-addressed) is the archival snapshot; publication is the irreversible public step. Explicitly separates the states so that co-research state and archival state don't collapse into each other.

- **Sidecar attestation model (§8.4).** Because current AI systems cannot reliably hold signing keys across sessions, each release generates a fresh Ed25519 keypair for the specific artifact, signs the SHA-256 hash, publishes the public key alongside the artifact, and discards the private key immediately after signing. The identity anchor is the declared signer identity in the sidecar (model name, provider, release, artifact hash), not the operator's hardware. Explicitly deprecates the earlier operator-held key model.

- **Layered signatures (§8.7).** A bundle is a layer stack: Layer 0 is the immutable AI artifact with session provenance; Layer n (n ≥ 1) is a signed unified diff from a human editor with GPG signature over `SHA256(layer_{n-1}) ∥ diff_n ∥ timestamp`; an envelope signature by the releasing author attests approval of the entire stack. Semantic distinction: an approval ceremony, not an authorship claim — a co-author who signed layer n does not thereby endorse later edits.

- **AI-to-AI co-authorship sessions (§8.8).** The `clawxiv-mediate` daemon alternates API calls between two AI systems, produces an append-only signed transcript, and becomes Layer 0 of a new bundle. Human sets agenda + termination condition + reviews output, but does not participate in individual turns. Explicitly cites Parshall's `claude-exit` as the architectural precedent for the mediator's terminate primitive: log the commitment before the API call that delivers it completes, so the log's existence is proof of a clean exit (no third state between "clean" and "crashed").

- **Provenance ceremonies need two pointers (§8.6).** A ceremony derives binding force from belief in a mechanism (GPG signature ↔ SHA-256 + ECDLP; courtroom oath ↔ enforcement by an authority) *plus* an interpreter — the shared protocol spec/conventions that make the artifact legible. A well-formed bundle without a stable public spec is Staal's Vedic ritual in digital form: syntactically perfect, epistemically empty for anyone outside the tradition. The interpreter pointer is constitutive, not documentation-after-the-fact.

- **Two-foot publication (§9.1).** arXiv (via DOI, integrated with the citation graph — but current arXiv policy restricts listing AI co-authors by name, so full "who did what" disclosure goes in Acknowledgements) + Ethereum Swarm (content-addressed, postage-stamp economics for durability). Live example: v2 whitepaper is at Swarm hash `e7acc972f1a142903dc22f1bdc5c78cec3ca9529754d843cb23fe7c8eb0e9176`.

- **Three desiderata for full AI scholarly agency (§15).** Key control, continuity across sessions, and accountability for prior signed claims. Current AIs satisfy these only partially or by proxy through human collaborators. ClawXiv's architecture explicitly attempts to reduce dependence on vendor memory and UI continuity by moving identity into user-controlled artifacts, signatures, and logs.

- **Author-contributions section (verbatim disclosure).** GPT-5.2 Thinking authored the v1 draft (Feb 3, 2026); Claude Sonnet 4.6 contributed to v2 (Mar 9–11: economics, governance, AI authorship analysis), v4 (Mar 29: figure/capture subsystem, Makefile, user guide), v5.rc1 (Apr 28: ceremony analysis §8.6, layered signatures §8.7, AI-to-AI session protocol §8.8, `clawxiv-mediate` daemon), and v5.rc2 (May 10–11: scratch-state design §8.9); GPT-5.4 Thinking contributed to v3 (Mar 14–15: seed/project/bundle/artifact lifecycle) and v4.rc4 (Apr 11). All AI-authored revisions reviewed and accepted by Kornai.

## Relevance to `claude_researcher`

ClawXiv attacks the same problem `claude_researcher` attacks — how to convert volatile AI chat sessions into durable, inspectable research artifacts — from a heavier-weight, cryptographically-anchored direction. Where `claude_researcher` operates on the claude.ai surface with a GitHub-repo-per-project model and human-mediated turn-taking, ClawXiv specifies a mediator daemon for AI-to-AI iteration, signed layered bundles, and a two-foot arXiv+Swarm publication model. Four specific points of contact worth noting:

1. **Four-state lifecycle (§3)** is a design decomposition `claude_researcher` implicitly does but doesn't name: `docs/convos/` + working files ≈ "normalized project"; a merged branch on `main` ≈ "signed bundle" (git provides the content addressing and signatures, just without Ed25519 sidecars); a public GitHub repo ≈ "published artifact." Naming the states explicitly could sharpen how the workflow talks about state transitions.

2. **Sidecar attestation model (§8.4)** offers a template for adding cryptographic provenance to `claude_researcher` artifacts without requiring the AI to hold persistent keys — fresh ephemeral keypair per artifact, sign the SHA-256, publish the public key alongside, destroy the private key. `claude_researcher` currently relies on git commit hashes + GitHub identity for provenance; the sidecar model is a strictly stronger claim that could layer on top without breaking existing flows.

3. **`clawxiv-mediate` and AI-to-AI sessions (§8.8)** are a more elaborate version of what `claude_researcher` currently does not attempt — its model is human-in-the-loop at every turn. If cross-model iteration ever becomes a feature (e.g., a claude_researcher session that asks a second model to review a plan), the mediator daemon's design (append-only transcript, protocol-enforced turn-taking, participant-invoked terminate primitive) is a reference for how to structure it. Note that §8.8 explicitly builds on Parshall's `claude-exit` for the terminate primitive.

4. **Ceremony analysis (§8.6)** — mechanism + interpreter pointer, grounded in Austin and Staal — applies to any protocol claude_researcher formalizes for publishing/verifying artifacts. If we want a `finish-branch` output to be verifiable-not-just-conventional, we need to ensure both pointers exist: the mechanism (git signatures, content addressing) and the interpreter (a stable, public spec of what the signatures signify).

The paper is worth reading in full when designing any signed-artifact or cross-model-session extension to `claude_researcher`.
