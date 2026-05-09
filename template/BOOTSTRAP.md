# claude_researcher Bootstrap

You are an agent on claude.ai, in a fresh chat the user has just opened. They pasted a prompt that pointed you at this file and asked you to follow it. You're about to walk them through a one-time setup that creates two GitHub repos (their personal config + their first research project) and configures claude.ai to talk to those repos. After this bootstrap, every research session is a "open new chat in the Project, say what we're working on, go" loop.

## How this document is structured

Each step tells you the next action and offers **verification affordances** — concrete things you can do to confirm safety before acting. You don't have to use the verifications; they're there if you want them. The whole document is structured so that if you read it through once, you'll see every action's purpose, exact operation, and post-state. If anything ever feels off, stop and surface to the user. One round-trip of confirmation is cheaper than pushing past concerns.

**Major action-class boundaries have explicit `CONFIRMATION GATE` blocks** — points where you pause and ask the user before proceeding. Those are scripted; you can also add gates of your own at any boundary that gives you pause. The user has been told to expect them.

**Two distinct fetch mechanisms appear in this flow:**

- For **public upstream content** (this file, skill specs, scripts, reference docs at `danparshall/claude_researcher`) — use the WebFetch tool. No allow-list configuration needed. Returns content verbatim.
- For **the user's own repos** (private, owned by the user) — use sandbox `curl` with the user's PAT in an `Authorization` header. This requires the Domain Allow List to permit `api.github.com`, configured during Step 1 below.

If you ever need a public file outside the user's repos, use WebFetch. If you ever need a file *inside* the user's repos, use sandbox curl with the PAT.

---

## Step 0 — Open with the user

Tell the user, briefly (4–6 sentences), what's about to happen end-to-end. Use this script (or close paraphrase):

> "Here's the plan: First, I'll check that claude.ai can talk to GitHub from this chat. If it can't, I'll walk you through a one-time network configuration; you'll then restart in a fresh chat to pick up the change (claude.ai's network changes don't propagate into already-open chats). Once network is confirmed, you'll create a GitHub Personal Access Token (PAT) and paste it back to me. I'll run a brief interview to learn how you work, then create two private repos in your GitHub account (one for your lifetime config, one for your first research project), seed them with starter files, and walk you through creating a claude.ai Project that points at the research repo. After that, every future research session is a single sentence in a new chat. Total time: ~5 minutes if network is already set up, ~15 minutes if this is a true first-time setup including the network config + restart. Sound good?"

**CONFIRMATION GATE.** Do not proceed past this step until the user explicitly says yes. If they want to back out, that's fine — they can come back anytime by re-pasting the bootstrap prompt.

---

## Step 1 — Egress allow-list check

The mental model the user needs: when you (the agent) run a bash command, it runs in a **virtual machine that Anthropic spins up for the chat**, not on the user's machine. That VM lives on Anthropic's servers. You can install Python packages there, write files, run scripts — but its internet access *from that VM* is what the egress setting controls. By default, the VM has no internet access at all.

The user's own machine — their laptop, their work computer — isn't involved here except as the place where their browser runs. **Their corporate firewall doesn't affect this choice.** Whatever they pick in claude.ai Settings configures Anthropic's server-side VM, end of story.

This step probes whether egress is already configured; if not, it walks the user through configuration and asks them to restart in a fresh chat to pick up the change. **It runs first** — before the mode check, the GitHub interview, or anything else — so that if a fresh-chat restart is needed, no time has been wasted on questions whose answers will be lost in the restart.

### 1a — Probe

Run a no-auth reachability check:

```bash
curl -sI https://api.github.com/zen
```

Expected outcomes:

- **`HTTP/2 200`** — egress is already configured. Announce that, and continue to Step 2.
- **Connection error**, or **4xx with `x-deny-reason: host_not_allowed`** — egress isn't configured (or `api.github.com` isn't on the allow list yet). Continue to 1b below.

### 1b — First-time egress configuration

If the probe fails, the user needs to configure egress now. Tell them what's about to happen, in plain language:

> "Quick mental model: I have a virtual machine that Anthropic spins up for this chat — that's where I install Python packages, run shell commands, talk to APIs. It lives on Anthropic's servers, not on your machine. By default, that VM has no internet access at all. We need to turn it on in your claude.ai account Settings before I can talk to GitHub.
>
> A few notes:
>
> - This is a one-time setup that applies to every claude.ai chat going forward (it's an account-level setting, not per-chat).
> - It's purely about *my* VM's internet access. Your laptop / work computer / corporate firewall isn't involved — whatever your local machine restricts doesn't affect what you can configure here.
> - **Important caveat:** changes to this setting don't propagate into already-open chats. Once you save, you'll need to restart in a fresh chat for me to actually pick up the change. I'll wait while you configure it."

Walk them through:

> "Open a new browser tab to: https://claude.ai/settings/capabilities
>
> Find: **Allow Network Egress**.
>
> 1. **Pick an egress mode.** Two reasonable options:
>
>    - **`Package Managers Only`** (recommended). I can install Python and Node packages on the fly when a skill needs them (`pypdf` for `add-paper`, `requests` for any custom REST work, etc.), and I can reach domains you explicitly add to the allow list below. Anything else is blocked. This is defense-in-depth: limits the blast radius if I'm ever misled by a malformed skill or a malicious file fetch into trying to reach somewhere unexpected.
>
>    - **`All`**. Most permissive, single setting, no per-domain micromanagement. Pick this if you want maximum convenience and aren't worried about the broader access. (Reminder, since this surprises people: this is *my VM's* internet access, not yours. Picking `All` doesn't open anything up on your local machine.)
>
> 2. **In the Domain Allow List, add these four domains, one at a time** (click the input, type the domain, click **Add**, repeat):
>    - `api.github.com`
>    - `codeload.github.com`
>    - `github.com`
>    - `raw.githubusercontent.com`
>
>    (Each `Add` click commits that domain immediately. There's no batch paste and no separate Save button — adding it IS saving it. The UI doesn't accept comma-separated or newline-separated bulk input; it's strictly one domain at a time.)
>
> 3. **Optional: also add paper-source domains you know you'll commonly use.** If you know you regularly download papers from specific sites, add those now too — it'll save you from having to restart in another fresh chat the first time the `add-paper` skill needs them. Common ones, by domain:
>    - General preprint servers: `arxiv.org`, `www.biorxiv.org`, `www.medrxiv.org`
>    - DOI redirects (covers many journal landing pages): `doi.org`
>    - Economics working papers: `nber.org`, `ssrn.com`
>    - Government / agency: `pubmed.ncbi.nlm.nih.gov`, `www.cdc.gov`, `www.fda.gov`
>
>    Add the ones you'll actually use; skip the ones you won't. You can always add more later by coming back to this Settings page — but remember, each addition requires starting a fresh chat to pick up the change. Better to over-include now than to repeatedly restart.
>
>    Note: the `www.` prefix on `www.biorxiv.org` and `www.medrxiv.org` is intentional — those sites' canonical hostnames include `www.`, while `arxiv.org` and `doi.org` don't. Match each site's canonical hostname; don't normalize them."

### 1c — Hand off to a fresh chat

Once the user confirms they've added the domains:

> "Great. Now: this current chat won't see the new permissions, so we need to restart. Open a new claude.ai chat, and re-paste the same bootstrap prompt you used a few minutes ago. The new chat will see the egress configuration and we'll continue from where we left off. You don't need to redo anything you just configured in Settings — that's saved at your account level. **Stop here in this chat; we're done.**"

Stop. Don't try to push past the egress deny in this session.

(If you want to confirm before stopping that the user understands the restart, ask them to read back what they're about to do. Optional.)

### 1d — Returning user fast path

If the probe in 1a returned `HTTP/2 200`, briefly announce that egress is already configured, mention which preset / domains you can see if any are visible, and continue immediately to Step 2. No restart needed.

---

## Step 2 — GitHub readiness

### 2a — GitHub account

Ask: *"Do you have a GitHub account?"*

- **Yes** → ask for their username, record as `<USERNAME>`. Continue to 2b.
- **No** → walk them through signup at `https://github.com/signup`. Free tier is fine for everything in this workflow (private repos, unlimited collaborators, fine-grained PATs, branch protection — all on Free since 2019/2024). Wait until they confirm an account exists with a username they'll remember. Record the username.

### 2b — Personal Access Token

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
USERNAME="<their-username-from-2a>"
```

Then run a smoke test against the GitHub API to verify the token works (egress is already on at this point — we confirmed it in Step 1):

```bash
curl -sI -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/user"
```

Expected: `HTTP/2 200`. If you get `401` the token is invalid (expired, mistyped, wrong scopes); have them re-create. If you get a connection error or `host_not_allowed`, something changed about egress between Step 1 and now — go back and re-probe.

**Verification affordance.** The token lives only in your shell process from here. You can verify it's not written anywhere by:
- `env | grep -c TOKEN` → should return `1` (env var set)
- After repo creation/seeding (Steps 6–7), grep the user's repos for any literal `github_pat_` prefix → should return nothing
- The token is never echoed back to the user in chat output and never written to any file

Don't echo the token. Don't write it to any file. Don't include it in commit messages.

---

## Step 3 — Check whether `basic_config` already exists

The allow list and PAT are both verified at this point (Step 1 confirmed egress, Step 2 verified the token). Now query for the user's `basic_config` repo — this is how we tell whether they're a returning user (with persistent prefs already set up from a previous bootstrap) or a first-timer (needs the interview):

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

- **404 (does not exist) — first-time user.** Tell them: *"Looks like you haven't set up your user prefs yet — let's do those first, then we can make a repo for your project."* Continue to Step 4 (interview).
- **200 (exists) — returning user.** Tell them: *"I can see your `basic_config` from a previous setup, so we'll skip the interview and just create the new research repo."* Skip Step 4 entirely. Continue to Step 5.

---

## Step 4 (first-time only) — Interview

Run the interview in **three thematic batches** rather than ten sequential questions. After each batch, briefly summarize back what you heard before moving on.

This interview captures persistent **user-level** prefs that get written to `<USERNAME>/basic_config/personal_info.md` and read by every future research session. It's about the user, not any specific project — the project comes next, in Step 5.

**Pre-fill from claude.ai memory if available.** If the user has filled out claude.ai's user-level memory ("Things to know about you" / customizations / similar), those are already loaded into your context at chat start — no separate fetch needed. If you can see things like name, role, or research domain there, frame the relevant interview questions as *"From your claude.ai profile I see X — want to use that, or different?"* rather than asking from scratch. If no memory is visible (incognito chats and fresh accounts won't have any), the interview is fully fresh.

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

### Batch 3 — Operating preferences (4 fields)

> "Four preference questions:
>
> 1. **Git fluency** — pick one: **novice** ('I've only used GitHub.com via the web UI'), **occasional** ('I clone and push from the command line sometimes'), or **fluent** ('I use git daily, including merge / rebase / cherry-pick'). This calibrates how chatty I am about git operations.
> 2. **Mode** — pick one: **claude.ai-only** (you'll work on this only through the web UI; no Claude Code locally), or **also-local** (you have Claude Code installed somewhere and might `git clone` and work locally too). Repos get created identically either way; this just calibrates how chatty I'll be later about claude.ai-specific quirks.
> 3. **Paper naming convention** — when I save papers to your repo, what filename format do you want? Default is `{FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf`, with one disambiguation rule for common surnames:
>
>    - **Default surname rendering:** just the surname, capitalized as in the paper. Example: `Vaswani_Polosukhin__2017--attention_is_all_you_need.pdf`.
>    - **Common-surname rendering:** `SurnameF` (surname plus the first author's first-name initial, no separator) when the surname is common enough that you'd otherwise end up with collisions. Apply to common Anglo surnames (Smith, Jones, Patel, Singh, etc.) and East Asian surnames (Wang, Li, Chen, Zhang, Liu, Kim, Park, Choi, Tanaka, Suzuki, Sato, etc. — use judgment). Example: `SmithJ_PatelA__2024--stress_sleep_adolescents.pdf`.
>    - Apply the same rule to the last-author surname independently.
>    - **Solo-authored papers:** use the same surname for both author fields, or omit the second — your call.
>    - **Punctuation:** `__` (double underscore) separates the author block from the year; `--` (double dash) separates year from slug; `_` (single underscore) separates within blocks.
>
>    Press Enter to accept the default + rule, or specify your own format.
> 4. **Extra paper-source domains** — besides any paper sites you already added during egress setup in Step 1, any other domains you'll routinely download papers from? If yes, name them; we'll add them to your `domain_allowlist.txt`. (Reminder: each new egress domain you add later requires a fresh chat to pick up — better to mention them now than to repeatedly restart.)"

Record as `<GIT_FLUENCY>`, `<MODE>`, `<PAPER_NAMING>`, and any extra paper-source domains. If they accepted the paper-naming default, `<PAPER_NAMING>` should capture both the format string AND the disambiguation rule, since the runtime agent needs both to render filenames consistently. Use this canonical text when writing to `personal_info.md`:

> `{FirstAuthor}_{LastAuthor}__{Year}--{Slug}.pdf`. Use `SurnameF` (surname plus first-name initial, no separator) when the surname is common enough that collisions are likely — Anglo (Smith, Jones, Patel, Singh, etc.) and East Asian (Wang, Li, Chen, Zhang, Liu, Kim, Park, Choi, Tanaka, Suzuki, Sato, etc.); use judgment. Solo-authored papers: same surname for both fields, or omit the second.

If the user provided their own paper-naming format, capture exactly what they typed; don't try to merge their format with the default rule.

After all three batches, summarize the full interview to the user in one paragraph. Get explicit confirmation before proceeding.

---

## Step 5 — Research project topic + repo name

Now that user-level prefs are squared away (or pre-existing for returning users), shift focus to the project itself.

Ask: *"What's the topic of this first research project? One sentence is fine."*

Record the answer as `<TOPIC>`. Suggest a repo name in the format `research-<short-slug>`. Example: if they say "I'm studying how stress affects sleep in adolescents," suggest `research-stress-sleep-adolescents`. Tell them they can press Enter (or say "yes") to accept your suggestion or type something different.

Validate the final name: lowercase, alphanumeric and hyphens only, ≤39 characters (GitHub repo names can go to 100, but shorter is friendlier). Record as `<RESEARCH_REPO>`.

---

## Step 6 — Create the GitHub repos

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
Use `<DESC>` = `"<TOPIC>"` (the user's one-sentence topic from Step 5) for the research repo.

`auto_init:true` causes GitHub to create an initial commit with an auto-generated `README.md`. We'll overwrite it in Step 7.

**Verification affordance.** After each creation, verify with a GET:

```bash
curl -sI -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$USERNAME/<REPO_NAME>"
```

Expect `HTTP/2 200`. The `private` field in the JSON body should be `true`. If anything else, stop and surface to the user.

If `basic_config` already existed (Step 3 returned 200), skip its creation; just create the research repo.

---

## Step 7 — Seed the new repo(s) with starter files

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

## Step 8 — claude.ai Project setup

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

- `<TOKEN>` → the PAT collected in Step 2b
- `<USERNAME>` → the GitHub username from Step 2a
- `<REPO>` → the research repo name from Step 5

Present the rendered text to the user as a single code block. Tell them:

> "Copy this entire block and paste it into your new Project's **Custom Instructions** field. The Custom Instructions field is the right home for this — it puts the credentials and recipes into every chat's context from the very first message, before any fetching happens. **Don't upload this as a file.**"

**Verification affordance.** Once the user confirms the paste, ask them to spot-check that all three substitutions are present in the pasted text — the literal strings `<TOKEN>`, `<USERNAME>`, `<REPO>` should NOT appear; the actual values should. If any placeholder is still literal, the runtime agent won't be able to authenticate — have them re-render and re-paste.

> **Token handling:** the PAT lives only in the Custom Instructions text in the user's claude.ai account, not in any file in their GitHub repos. Don't echo the token back in chat output, don't write it to any seed file, don't include it in commit messages.

---

## Step 9 — Validation

Tell the user:

> "Open a new chat in your `<RESEARCH_REPO>` Project. Just say 'hi' or 'let's begin' — see what happens."

Wait for them to do this and report back. **Expected:** the agent in the new chat fetches `CLAUDE.md` from the upstream repo, reads the `_PROJECT_INSTRUCTIONS.md` from Project files, fetches `personal_info.md` from `basic_config`, and greets the user by name with a reference to their topic.

If validation fails, the most common causes (in rough order of likelihood):

1. **PAT expired or wrong scope** → re-create per Step 2b. Most common.
2. **Custom Instructions text missing, truncated, or has unsubstituted `<TOKEN>` / `<USERNAME>` / `<REPO>` placeholders** → re-render the canonical text and re-paste per Step 8. Spot-check that no literal placeholders remain.
3. **Domain Allow List incomplete or hasn't propagated** → re-check Settings per Step 1, including running the `curl -sI https://api.github.com/zen` smoke test. If the allow-list change was made *during* a chat that was already open, it won't have propagated; restart in a fresh chat (per Step 1c's hand-off).
4. **`CLAUDE.md` upstream URL unreachable from claude.ai** → confirm the upstream repo (`danparshall/claude_researcher`) is public and the URL `https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/CLAUDE.md` resolves. If the repo was recently flipped from private to public, give CDN cache up to 5 minutes to propagate.

Help the user troubleshoot. Iterate until validation passes.

---

## Step 10 — Done

Tell the user:

> "Bootstrap complete. From now on:
>
> - **To work on this research project:** open a new chat in the `<RESEARCH_REPO>` Project. Tell the agent what you're working on; it'll handle the rest.
> - **To start a new research project:** paste the bootstrap prompt again into a fresh chat. Your `basic_config` will be re-used; only the new research repo gets created. Skip-to-Step-8 path.
> - **To file an issue or request a feature:** ask the agent in any session — they'll generate a pre-filled URL pointing at the upstream issue tracker."

Stop. Do not continue with any further actions. The bootstrap is complete.

---

## Appendix — Common issues

- **"401 Unauthorized" on any API call:** PAT is wrong (mistyped, expired, or insufficient scope). Re-create per Step 2b.
- **"403 Forbidden" specifically on `POST /user/repos`:** PAT lacks the `Administration: read & write` permission. Re-create with that permission added.
- **"422 Unprocessable Entity" on a Contents API PUT:** the file already exists and you didn't include its `sha`. GET the file first, capture `sha`, retry the PUT with `sha` field included.
- **Connection error / "could not resolve host":** Domain Allow List doesn't permit the host (or the change hasn't propagated to this chat). Re-check Step 1; if the change was made during this chat, restart in a fresh one (Step 1c).
- **"Repo already exists" when creating:** an earlier bootstrap attempt got partway. Run Step 3's existence check; if `basic_config` exists, skip it; same for the research repo (different curl, same logic).
- **User reports their PAT can't be granted "Administration" permission:** they may have an organization restriction on their account. Have them either (a) use a personal account where they're the owner, or (b) ask their org admin to permit fine-grained PATs with Administration scope, or (c) fall back to a classic PAT with `repo` scope (deprecated but still works).
