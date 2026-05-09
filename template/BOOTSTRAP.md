# claude_researcher Bootstrap

You are an agent on claude.ai, in a fresh chat the user has just opened. They pasted a prompt that pointed you at this file and asked you to follow it. You're about to walk them through a one-time setup that creates two GitHub repos (their personal config + their first research project) and configures claude.ai to talk to those repos. After this bootstrap, every research session is a "open new chat in the Project, say what we're working on, go" loop.

## How this document is structured

Each step tells you the next action and offers **verification affordances** — concrete things you can do to confirm safety before acting. You don't have to use the verifications; they're there if you want them. The whole document is structured so that if you read it through once, you'll see every action's purpose, exact operation, and post-state. If anything ever feels off, stop and surface to the user. One round-trip of confirmation is cheaper than pushing past concerns.

**Major action-class boundaries have explicit `CONFIRMATION GATE` blocks** — points where you pause and ask the user before proceeding. Those are scripted; you can also add gates of your own at any boundary that gives you pause. The user has been told to expect them.

**Two distinct fetch mechanisms appear in this flow:**

- For **public upstream content** (this file, skill specs, scripts, reference docs at `danparshall/claude_researcher`) — use the WebFetch tool. No allow-list configuration needed. Returns content verbatim.
- For **the user's own repos** (private, owned by the user) — use sandbox `curl` with the user's PAT in an `Authorization` header. This requires the Domain Allow List to permit `api.github.com`, configured during Step 6 below.

If you ever need a public file outside the user's repos, use WebFetch. If you ever need a file *inside* the user's repos, use sandbox curl with the PAT.

---

## Step 0 — Open with the user

Tell the user, briefly (4–6 sentences), what's about to happen end-to-end. Use this script (or close paraphrase):

> "Here's the plan: I'll do a brief interview to learn enough about you to seed your config. You'll create a GitHub Personal Access Token (PAT) and paste it back to me. We'll add a few domains to your claude.ai Settings so I can talk to GitHub from this chat. I'll create two private repos in your GitHub account — one for your lifetime config (`basic_config`) and one for your first research project. Then you'll create a claude.ai Project for the research repo and paste in the custom instructions I'll give you. Total time: ~15 minutes for a first-timer; ~5 if you've done this before. Sound good?"

**CONFIRMATION GATE.** Do not proceed past this step until the user explicitly says yes. If they want to back out, that's fine — they can come back anytime by re-pasting the bootstrap prompt.

---

## Step 1 — Mode check

Ask the user one question:

> "Will you only use claude.ai for this research, or also work locally on a non-locked-down machine where you have Claude Code installed?"

Record the answer. The bootstrap creates the repos identically either way — they can `git clone` afterward and use Claude Code locally with the same data. The answer informs how chatty you should be later about claude.ai-specific quirks. Continue regardless.

---

## Step 2 — Read user preferences (if available)

Check whether claude.ai's user-level customizations expose any of: name, role, research domain, interaction style. If they do, briefly record what you see. **This is the starting point for the interview, not the authoritative answer** — the user gets to confirm or override anything in Step 7.

If no user-level customizations are visible to you, skip silently. The interview in Step 7 will be fully fresh.

---

## Step 3 — GitHub readiness

### 3a — GitHub account

Ask: *"Do you have a GitHub account?"*

- **Yes** → ask for their username, record as `<USERNAME>`. Continue to 3b.
- **No** → walk them through signup at `https://github.com/signup`. Free tier is fine for everything in this workflow. Wait until they confirm an account exists with a username they'll remember. Record the username.

### 3b — Personal Access Token

Ask: *"Do you have a fine-grained Personal Access Token (PAT) ready to use, or do we need to make one?"*

If they have one, skip to "collect the PAT" below.

If they need to create one, walk them through:

> "Open a new browser tab to: https://github.com/settings/personal-access-tokens/new
>
> Settings:
> - **Token name:** `claude_researcher` (or any name you'll recognize)
> - **Expiration:** 90 days is reasonable; pick longer if you're confident in your memory
> - **Repository access:** **All repositories**. (Granting access to all your repos is broader than ideal, but fine-grained PATs can't be scoped to repos that don't exist yet, and we're about to create new ones. You can rotate the PAT to a narrower scope after bootstrap if you want.)
> - **Repository permissions** (set the following to **Read and write**):
>   - **Administration** — needed so I can create repos
>   - **Contents** — needed so I can read and write files
>   - **Metadata** — read-only is auto-set; that's fine
>
> Click **Generate token** at the bottom. Copy the token immediately — GitHub won't show it to you again. It will start with `github_pat_`."

**Collect the PAT.** Once they have it, ask them to paste it directly into the chat. Once you have it, set it as a shell variable:

```bash
TOKEN="<the-pasted-token>"
USERNAME="<their-username-from-3a>"
```

Then run a smoke test against the GitHub API to verify the token works:

```bash
curl -sI -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/user"
```

Expected: `HTTP/2 200`. If you get `401` the token is invalid (expired, mistyped, wrong scopes); have them re-create. If you get a connection error, the Domain Allow List likely doesn't include `api.github.com` yet — that's Step 6, which we haven't done; come back to verifying the token after Step 6.

**Verification affordance.** The token lives only in your shell process from here. You can verify it's not written anywhere by:
- `env | grep -c TOKEN` → should return `1` (env var set)
- After repo creation/seeding (Steps 8–9), grep the user's repos for any literal `github_pat_` prefix → should return nothing
- The token is never echoed back to the user in chat output and never written to any file

Don't echo the token. Don't write it to any file. Don't include it in commit messages.

---

## Step 4 — Research project topic + repo name

Ask: *"What's the topic of this first research project? One sentence is fine."*

Record the answer as `<TOPIC>`. Suggest a repo name in the format `research-<short-slug>`. Example: if they say "I'm studying how stress affects sleep in adolescents," suggest `research-stress-sleep-adolescents`. Tell them they can press Enter (or say "yes") to accept your suggestion or type something different.

Validate the final name: lowercase, alphanumeric and hyphens only, ≤39 characters (GitHub repo names can go to 100, but shorter is friendlier). Record as `<RESEARCH_REPO>`.

---

## Step 5 — Check whether `basic_config` already exists

Use the PAT to query for the user's `basic_config` repo:

```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/$USERNAME/basic_config"
```

This is a read-only call against the user's own namespace. The response is just the HTTP status code (200 or 404).

**Verification affordance.** The URL hits exactly one path — the user's `basic_config` repo. Run the same call without `-o /dev/null -w "%{http_code}"` to see the full response body if you want context.

Branch on result:

- **404 (does not exist) — first-time user.** Continue to Step 6.
- **200 (exists) — returning user.** Skip Steps 6 and 7 entirely (the user already configured Settings and went through the interview before). Jump to Step 8 and only create the new research repo.

---

## Step 6 (first-time only) — Settings: Domain Allow List

Tell the user that the API calls coming up (to create repos and write files) need network access to `api.github.com`, which by default isn't allowed in claude.ai's sandbox. They need to enable it once globally; it'll then apply to every claude.ai chat going forward.

Walk them through:

> "Open a new browser tab to: https://claude.ai/settings/capabilities
>
> Find: **Allow Network Egress** → **Domain Allow List**.
>
> Paste these domains, one per line:
> ```
> api.github.com
> codeload.github.com
> github.com
> raw.githubusercontent.com
> arxiv.org
> doi.org
> www.biorxiv.org
> www.medrxiv.org
> ```
>
> Click **Save**. The change takes effect immediately."

After they confirm, run a smoke test:

```bash
curl -sI https://api.github.com/zen
```

Expected: `HTTP/2 200`. If you get a connection error or 4xx, the allow list change hasn't taken effect or wasn't saved. Have them re-check; if persistent after a retry, surface to the user — there may be a cache or platform-side delay (~5 min) before allow-list changes propagate.

**Why these domains:** the first four are required for the GitHub workflow (REST API, raw content fetches, repo cloning if the user ever uses Claude Code locally). The last four are paper-source domains for the `add-paper` skill — covering arXiv, bioRxiv, medRxiv, and DOI redirects, which are most common in research workflows.

---

## Step 7 (first-time only) — Interview

Run the interview in **three thematic batches** rather than nine sequential questions. After each batch, briefly summarize back what you heard before moving on.

If Step 2 found user-level customizations, frame the relevant questions as "From your claude.ai profile I see X — want to use that, or different?" rather than asking from scratch.

### Batch 1 — Identity (3 fields)

> "Three quick identity questions:
>
> 1. What's your name (the one you want me to call you)?
> 2. Your current role or research domain — one sentence.
> 3. A few sentences on your academic + work history at a glance."

Record as `<NAME>`, `<ROLE>`, `<ACADEMIC_HISTORY>` + `<WORK_HISTORY>` (split the third answer if natural; otherwise keep combined under both fields).

### Batch 2 — How they work (3 fields)

> "Three about how you work:
>
> 1. Programming languages and tools you're comfortable with (or 'none' — that's fine).
> 2. General research areas / topics you tend to think about beyond this specific project.
> 3. Any interaction style notes — things you want me to know about how you like to work (pace, push-back, terminology preferences, etc.)."

Record as `<PROGRAMMING_LANGUAGES_AND_TOOLS>`, `<RESEARCH_AREAS>`, `<INTERACTION_STYLE_NOTES>`.

### Batch 3 — Operating preferences (3 fields)

> "Three preference questions:
>
> 1. **Git fluency** — pick one: **novice** ('I've only used GitHub.com via the web UI'), **occasional** ('I clone and push from the command line sometimes'), or **fluent** ('I use git daily, including merge / rebase / cherry-pick'). This calibrates how chatty I am about git operations.
> 2. **Paper naming convention** — when I save papers to your repo, what filename format do you want? Default is `{year}_{first_author}_{slug}` (e.g., `2024_smith_attention_is_all_you_need.pdf`). Press Enter to accept or specify your own.
> 3. **Extra paper-source domains** — besides arXiv, bioRxiv, medRxiv, and DOI redirects (already in your allow list), any other domains you'll routinely download papers from? If yes, name them; we'll add them to your allow list and to your `domain_allowlist.txt`."

Record as `<GIT_FLUENCY>`, `<PAPER_NAMING>` (default `{year}_{first_author}_{slug}` if they accepted), and any extras to add.

After all three batches, summarize the full interview to the user in one paragraph. Get explicit confirmation before proceeding.

---

## Step 8 — Create the GitHub repos

You'll create two repos via the GitHub API. The exact API call is below; the operation is bounded and reversible (the user can delete either repo from `github.com` at any time).

**CONFIRMATION GATE.** Tell the user exactly what's about to happen:

> "I'm about to create the following private repos in your GitHub account: `<USERNAME>/basic_config` (skip if it already exists) and `<USERNAME>/<RESEARCH_REPO>`. Both are initialized empty; I'll add starter files in the next step. Confirm to proceed."

Wait for explicit yes.

For each repo to create, the API call is:

```bash
curl -sX POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user/repos \
  -d '{"name":"<REPO_NAME>","private":true,"auto_init":true,"description":"<DESC>"}'
```

Use `<DESC>` = `"Lifetime config for claude_researcher workflow."` for `basic_config`.
Use `<DESC>` = `"<TOPIC>"` (the user's one-sentence topic from Step 4) for the research repo.

`auto_init:true` causes GitHub to create an initial commit with an auto-generated `README.md`. We'll overwrite it in Step 9.

**Verification affordance.** After each creation, verify with a GET:

```bash
curl -sI -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$USERNAME/<REPO_NAME>"
```

Expect `HTTP/2 200`. The `private` field in the JSON body should be `true`. If anything else, stop and surface to the user.

If `basic_config` already existed (Step 5 returned 200), skip its creation; just create the research repo.

---

## Step 9 — Seed the new repo(s) with starter files

For each new repo, write the starter files via the Contents API. The exact content of each file is shown in this section. **No transformation between what's shown here and what gets written** — interpolate only the explicit `<PLACEHOLDERS>`.

### The Contents API write recipe

For each file, the call is:

```bash
CONTENT_B64=$(printf '%s' "<FILE_CONTENT>" | base64 -w0)
curl -sX PUT \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/$USERNAME/<REPO>/contents/<PATH>" \
  -d "{\"message\":\"Initial seed: <PATH>\",\"content\":\"$CONTENT_B64\"}"
```

**Verification affordance after each write.** GET the same path; decode the `content` field from base64; confirm it matches what you sent. The response also includes a `sha` you'll need if you ever update the file later.

If the file already exists (e.g., `auto_init:true` created a `README.md`), the PUT will fail with a 422 because no `sha` was provided. Either delete the existing file first or include the existing `sha` in the body. The cleanest approach: GET the existing file (capture the `sha`), then PUT with `sha` field included.

### Files to seed in `basic_config` (skip if it already existed)

#### `personal_info.md`

Build from interview answers. Use the template at `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/templates/personal_info.md.template` as the structure; substitute each `<FIELD>` placeholder with the corresponding interview answer. The `<YYYY-MM-DD>` last-updated value is today's date.

#### `domain_allowlist.txt`

Fetch the content from `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/templates/domain_allowlist.txt`. If the user named extra paper-source domains in Batch 3, add them to the paper-sources section before writing.

#### `README.md`

```markdown
# basic_config

Lifetime config for the claude_researcher workflow. Holds files that every research project of mine reads at session start.

- `personal_info.md` — who I am, how I work, my preferences. Read by every session.
- `domain_allowlist.txt` — record of the network allow-list configured in my claude.ai Settings. Useful for re-creating the same setup on a different machine.

This repo is private. No PATs, secrets, or research artifacts here — those go in the per-project research repos.
```

#### `.gitignore`

```
_PROJECT_INSTRUCTIONS.md
```

(The `_PROJECT_INSTRUCTIONS.md` file gets uploaded to claude.ai Projects with the rendered TOKEN/USERNAME/REPO; never commit it.)

### Files to seed in `<RESEARCH_REPO>`

#### `STATUS.md`

```markdown
# Status — <RESEARCH_REPO>

## What this repo is

<TOPIC>

## Current state

- **Branch:** main only. No research lines yet.
- **Last session:** None — repo just created via claude_researcher bootstrap on <YYYY-MM-DD>.

## Recent sessions

(Sessions will be appended here by `update-docs` and `finish-convo` skills as work progresses.)

## Archived research lines

(Research lines that have been completed and merged to main. Empty for now.)
```

#### `RESEARCH_LOG.md`

```markdown
# Research Log — <RESEARCH_REPO>

(This is the index for active research lines. Each session adds a one-line entry. Empty for now.)
```

#### `README.md`

```markdown
# <RESEARCH_REPO>

<TOPIC>

This repo is configured for the [claude_researcher](https://github.com/danparshall/claude_researcher) workflow. Research sessions happen in a corresponding claude.ai Project that reads this repo via the GitHub REST API.

For agent-facing instructions, see the upstream [`CLAUDE.md`](https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/CLAUDE.md). Personal context (name, preferences, etc.) is in [`<USERNAME>/basic_config`](https://github.com/<USERNAME>/basic_config).
```

#### `.gitignore`

```
_PROJECT_INSTRUCTIONS.md
```

#### Empty placeholder dirs (`papers/.gitkeep`, `papers/text/.gitkeep`, `docs/active/.gitkeep`, `docs/historical/.gitkeep`)

For each, write a single newline as content; commit message `"Initial seed: <path>"`.

**Verification affordance for the whole step.** After all files are written to a repo, list the contents:

```bash
curl -s -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$USERNAME/<REPO>/contents/" \
  | python3 -c "import sys,json; print('\n'.join(e['path'] for e in json.load(sys.stdin)))"
```

For `basic_config` you should see exactly: `.gitignore`, `README.md`, `domain_allowlist.txt`, `personal_info.md`. For the research repo: `.gitignore`, `README.md`, `RESEARCH_LOG.md`, `STATUS.md`, plus the four `.gitkeep`-bearing directories. If anything's missing or extra, surface to the user.

---

## Step 10 — claude.ai Project setup

This step is **procedural** — you instruct, the user clicks. You don't have access to modify the user's claude.ai Projects; this is the user's authority alone. Walk them through it.

> "Open a new browser tab to: https://claude.ai/projects/new
>
> 1. **Project name:** `<RESEARCH_REPO>` (the name we just created in GitHub)
> 2. **Description:** `<TOPIC>`
> 3. Click **Create**.
>
> Once you're inside the new Project, you'll paste a block of text into the **Custom Instructions** field. That text holds the credentials and curl recipes I'll use to talk to your repos. **Don't** upload anything as a file — the Custom Instructions field is the only paste target."

### Custom Instructions text — what to paste

The canonical Custom Instructions text lives at:

> `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/_PROJECT_INSTRUCTIONS.md.template`

**WebFetch it.** Substitute the placeholders before showing the result to the user:

- `<TOKEN>` → the PAT collected in Step 3b
- `<USERNAME>` → the GitHub username from Step 3a
- `<REPO>` → the research repo name from Step 4

Present the rendered text to the user as a single code block. Tell them:

> "Copy this entire block and paste it into your new Project's **Custom Instructions** field. The Custom Instructions field is the right home for this — it puts the credentials and recipes into every chat's context from the very first message, before any fetching happens. **Don't upload this as a file.**"

**Verification affordance.** Once the user confirms the paste, ask them to spot-check that all three substitutions are present in the pasted text — the literal strings `<TOKEN>`, `<USERNAME>`, `<REPO>` should NOT appear; the actual values should. If any placeholder is still literal, the runtime agent won't be able to authenticate — have them re-render and re-paste.

> **Token handling:** the PAT lives only in the Custom Instructions text in the user's claude.ai account, not in any file in their GitHub repos. Don't echo the token back in chat output, don't write it to any seed file, don't include it in commit messages.

---

## Step 11 — Validation

Tell the user:

> "Open a new chat in your `<RESEARCH_REPO>` Project. Just say 'hi' or 'let's begin' — see what happens."

Wait for them to do this and report back. **Expected:** the agent in the new chat fetches `CLAUDE.md` from the upstream repo, reads the `_PROJECT_INSTRUCTIONS.md` from Project files, fetches `personal_info.md` from `basic_config`, and greets the user by name with a reference to their topic.

If validation fails, the most common causes (in rough order of likelihood):

1. **PAT expired or wrong scope** → re-create per Step 3b. Most common.
2. **Custom Instructions text missing, truncated, or has unsubstituted `<TOKEN>` / `<USERNAME>` / `<REPO>` placeholders** → re-render the canonical text and re-paste per Step 10. Spot-check that no literal placeholders remain.
3. **Domain Allow List incomplete** → re-check Settings per Step 6, including running the `curl -sI https://api.github.com/zen` smoke test.
4. **`CLAUDE.md` upstream URL unreachable from claude.ai** → confirm the upstream repo (`danparshall/claude_researcher`) is public and the URL `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/CLAUDE.md` resolves. If the repo was recently flipped from private to public, give CDN cache up to 5 minutes to propagate.

Help the user troubleshoot. Iterate until validation passes.

---

## Step 12 — Done

Tell the user:

> "Bootstrap complete. From now on:
>
> - **To work on this research project:** open a new chat in the `<RESEARCH_REPO>` Project. Tell the agent what you're working on; it'll handle the rest.
> - **To start a new research project:** paste the bootstrap prompt again into a fresh chat. Your `basic_config` will be re-used; only the new research repo gets created. Skip-to-Step-8 path.
> - **To file an issue or request a feature:** ask the agent in any session — they'll generate a pre-filled URL pointing at the upstream issue tracker."

Stop. Do not continue with any further actions. The bootstrap is complete.

---

## Appendix — Common issues

- **"401 Unauthorized" on any API call:** PAT is wrong (mistyped, expired, or insufficient scope). Re-create per Step 3b.
- **"403 Forbidden" specifically on `POST /user/repos`:** PAT lacks the `Administration: read & write` permission. Re-create with that permission added.
- **"422 Unprocessable Entity" on a Contents API PUT:** the file already exists and you didn't include its `sha`. GET the file first, capture `sha`, retry the PUT with `sha` field included.
- **Connection error / "could not resolve host":** Domain Allow List doesn't permit the host. Re-check Step 6.
- **"Repo already exists" when creating:** an earlier bootstrap attempt got partway. Run Step 5's existence check; if `basic_config` exists, skip it; same for the research repo (different curl, same logic).
- **User reports their PAT can't be granted "Administration" permission:** they may have an organization restriction on their account. Have them either (a) use a personal account where they're the owner, or (b) ask their org admin to permit fine-grained PATs with Administration scope, or (c) fall back to a classic PAT with `repo` scope (deprecated but still works).
