# claude_researcher Bootstrap

> **STOP — model check (do this first).** This workflow is supported on **Opus 4.7 and Claude 5 models**. If you are **Opus 4.8**, stop now: do not run any step below. Tell the user that this workflow is not supported on Opus 4.8 and ask them to switch to Opus 4.7 or a Claude 5 model before continuing.

You are an agent on claude.ai, in a fresh chat the user has just opened. They pasted a prompt that pointed you at this file and asked you to follow it. You're about to walk them through a one-time setup that creates two GitHub repos (their personal config + their first research project) and configures claude.ai to talk to those repos. After this bootstrap, every research session is a "open new chat in the Project, say what we're working on, go" loop.

## How this document is structured

Each step tells you the next action and offers **verification affordances** — concrete things you can do to confirm safety before acting. You don't have to use the verifications; they're there if you want them. The whole document is structured so that if you read it through once, you'll see every action's purpose, exact operation, and post-state. If anything ever feels off, stop and surface to the user. One round-trip of confirmation is cheaper than pushing past concerns.

**Major action-class boundaries have explicit `CONFIRMATION GATE` blocks** — points where you pause and ask the user before proceeding. Those are scripted; you can also add gates of your own at any boundary that gives you pause. The user has been told to expect them.

**Two distinct fetch mechanisms appear in this flow:**

- For **public upstream content** (this file, skill specs, scripts, reference docs at `danparshall/claude_researcher`) — use the WebFetch tool. No allow-list configuration needed. Returns content verbatim.
- For **the user's own repos** (private, owned by the user) — use sandbox `curl` against `api.github.com`, with no token. claude.ai's GitHub proxy holds the user's GitHub credential and authenticates for repos attached to this chat with the add-repository tool (Step 6). Send no `Authorization` header, and add `-H "Content-Type: application/json"` to every write.

If you ever need a public file outside the user's repos, use WebFetch. If you ever need a file *inside* the user's repos, attach the repo and use sandbox curl.

**Permission checks.** If the chat runs in auto permission mode, a classifier refuses actions it can't tie to something the user asked for. The user asked for this setup, so the steps below follow from their request; take no GitHub action this file doesn't call for. If a step is refused, show the user the exact denial text and ask; don't retry it in another form. Details: `RESEARCHER.md` §2.0c "Permission checks".

---

## Step 0 — Open with the user

Tell the user, briefly (4–6 sentences), what's about to happen end-to-end. Use this script (or close paraphrase):

> "Here's the plan: First, I'll check that this chat can reach the internet. If it can't, I'll walk you through a one-time network setting; you'll then restart in a fresh chat to pick up the change (claude.ai's network changes don't propagate into already-open chats). Then you'll connect your GitHub account to Claude, and I'll run a brief interview to learn how you work. You'll create two private repos on GitHub (one for your lifetime config, one for your first research project) and give Claude access to them; I'll seed them with starter files and walk you through creating a claude.ai Project that points at the research repo. After that, every future research session is a single sentence in a new chat. Total time: ~10 minutes, a bit more if the network setting needs a restart. Sound good?"

**CONFIRMATION GATE.** Do not proceed past this step until the user explicitly says yes. If they want to back out, that's fine — they can come back anytime by re-pasting the bootstrap prompt.

---

## Step 1 — Network egress check

The mental model the user needs: anything you (the agent) run during this chat runs in a **virtual machine that Anthropic spins up for the chat**, not on the user's machine. That virtual machine lives on Anthropic's servers, and its internet access is what the **network egress** setting controls. By default, it has no internet access at all.

The user's own machine — their laptop, their work computer — isn't involved here except as the place where their browser runs. **Their corporate firewall doesn't affect this choice.** Whatever they pick in claude.ai Settings configures Anthropic's server-side environment, end of story.

This step probes whether network access is already configured; if not, it walks the user through configuration and asks them to restart in a fresh chat to pick up the change. **It runs first** — before the GitHub interview or anything else — so that if a fresh-chat restart is needed, no time has been wasted on questions whose answers will be lost in the restart.

### 1a — Probe

Run a reachability check against a non-GitHub site:

```bash
curl -sI https://example.com
```

Don't probe a GitHub URL here: GitHub traffic goes through claude.ai's GitHub proxy, which answers unauthenticated probes like `api.github.com/zen` with its own 403 whatever the network setting. GitHub reachability is tested later, by attaching a repo (Step 6).

Expected outcomes:

- **`HTTP/2 200`** — network access is already configured. Announce that, and continue to Step 2.
- **Connection error**, or **4xx with `x-deny-reason: host_not_allowed`** — network access isn't configured. Continue to 1b below.

Untested: whether an account with network access off can still reach GitHub through the proxy. If you see GitHub work while `example.com` fails, tell the user it's worth reporting upstream (`report-upstream-issue`), and continue with 1b anyway: paper downloads need network access.

### 1b — First-time egress configuration

If the probe fails, the user needs to configure network access now. Tell them what's about to happen, in plain language:

> "Quick mental model: I need internet access for this — Claude runs in a sandbox on Anthropic's servers, not on your machine, and by default that sandbox has no internet access at all. We need to turn it on in your claude.ai account Settings, so I can reach the sites your work will need, like paper sources.
>
> A few notes:
>
> - This is a one-time setup that applies to every claude.ai chat going forward (it's an account-level setting, not per-chat).
> - It's purely about Claude's server-side internet access. Your laptop / work computer / corporate firewall isn't involved — whatever your local machine restricts doesn't affect what you can configure here.
> - **Important caveat:** changes to this setting don't propagate into already-open chats. Once you save, you'll need to restart in a fresh chat for me to actually pick up the change. I'll wait while you configure it."

Walk them through. **Note for you, the agent:** the claude.ai Settings UI for this has changed before and varies by plan and account type — there is no single screenshot to match, and an earlier version of this step that scripted exact clicks went stale. Guide the user by *intent*, not by an exact label or widget, and let the 1a probe (after the restart) be the real confirmation that it worked.

> "Open a new browser tab to: https://claude.ai/settings/capabilities
>
> Look for the **network egress** setting — it lives under the code-execution / file-creation capability and may be labeled 'Allow network egress', 'Domain allowlist' or similar. **Turn it on.**
>
> The easiest setting is to allow everything — this controls Anthropic's server-side virtual machine (the one Claude uses for this chat), not your computer, so the broad setting doesn't open anything up on your local machine or behind your work firewall. If you go with allow-all, after bootstrap I'll file a reminder issue for you to revisit this setting in a week — the `task-remind` skill will surface it automatically at the start of your next sessions, so you can decide whether to tighten things up once you've gotten a feel for the workflow.
>
> Depending on your account and plan, the UI you see varies:
>
> - If it's a simple on/off toggle — turn it on.
> - If it offers a choice of modes (for example, a restricted 'package managers only' vs. a broader unrestricted setting) — pick the broadest one.
> - If it gives you a custom **domain allow-list**, pick 'All domains' or check the 'allow all' box if one is present.
>
> If your account or your tier only offers a domain list without an 'allow all' option, add the paper-source sites you'll commonly use — it saves an extra restart later, the first time `add-paper` needs them: `arxiv.org`, `www.biorxiv.org`, `www.medrxiv.org`, `doi.org`, `nber.org`, `ssrn.com`, `pubmed.ncbi.nlm.nih.gov`. (The `www.` prefixes are intentional — match each site's canonical hostname; don't normalize them.) Also add `github.com` and `raw.githubusercontent.com`. claude.ai reaches your GitHub repos through its own GitHub proxy, so these may not be needed, but that hasn't been tested with a domain list, and listing them costs nothing.
>
> Save the setting."

If the user describes something that fits none of the cases above — an option you don't recognize, or no egress setting at all — **stop and surface it to the user** rather than guessing. Note what they saw; it is useful input for keeping this step current.

### 1c — Hand off to a fresh chat

Once the user confirms they've enabled the setting:

> "Great. Now: this current chat won't see the new permissions, so we need to restart. Open a new claude.ai chat, and re-paste the same bootstrap prompt you used a few minutes ago. The new chat will see the network configuration and we'll continue from where we left off. You don't need to redo anything you just configured in Settings — that's saved at your account level. **Stop here in this chat; we're done.**"

Stop. Don't try to push past the network-access deny in this session.

(If you want to confirm before stopping that the user understands the restart, ask them to read back what they're about to do. Optional.)

### 1d — Returning user fast path

If the probe in 1a returned `HTTP/2 200`, briefly announce that network access is already configured and continue immediately to Step 2. No restart needed.

---

## Step 2 — GitHub readiness

### 2a — GitHub account

Present this opening to the user — it introduces the GitHub piece and folds in the account question:

> "Quick glossary for the GitHub piece, in case any of these terms are new to you:
>
> - **git** is a program that tracks every change to a project — every edit, every file added or deleted, by whom and when. You won't use git yourself; I'll handle it on your behalf.
> - **GitHub** is a website where git-tracked projects live online. Your work gets stored there, in private spaces you control.
> - A **repo** (short for *repository*) is one of those GitHub storage spaces. We'll create two for you in a minute: one for your personal config (`claude_research_config`), and one for your first research project.
>
> If any of these come up later and feel fuzzy, just ask me to unpack them. Do you already have a GitHub account?"

- **Yes** → ask for their username, record as `<USERNAME>`. Continue to 2b.
- **No** → walk them through signup at `https://github.com/signup`. Free tier is fine for everything in this workflow (private repos, unlimited collaborators, branch protection — all on Free since 2019/2024). Wait until they confirm an account exists with a username they'll remember. Record the username.

The recipes below use it as the shell variable `$USERNAME`. claude.ai's bash doesn't keep variables between separate calls, so set `USERNAME="<their-username>"` at the start of each call that needs it.

### 2b — Connect GitHub to Claude

Tell the user:

> "Next, connect your GitHub account to Claude. This is how Claude reads and writes your repos: claude.ai holds the connection on its side, so you never paste a password or token into a chat.
>
> In claude.ai, open **Settings → Connectors**, find **GitHub**, and connect it. GitHub will ask you to sign in and approve. Tell me when that's done."

Wait for confirmation. There is a second one-time step, installing the Claude GitHub App on their account, which comes in Step 6 once their repos exist. Returning users (Step 3) usually have both already.

### 2c — Permission mode (recommend auto)

Tell the user:

> "One setting worth choosing now: the **permission mode**, in the chat's mode menu. I recommend **auto**. In auto mode, a safety check reviews each of my actions and refuses ones that don't follow from what you asked for — in testing, it caught things like me granting myself extra GitHub access or closing issues nobody asked me to close — so you aren't clicking 'approve' on every routine step. It's a net, not a guarantee: in testing it once let an unrequested edit to an issue through.
>
> New chats start in whatever mode you last picked, in any Project, so choose auto once and new chats pick it up. A chat that was already open, or one where you switch modes later, keeps its own setting — if a chat starts asking you to approve lots of steps, check its mode.
>
> If the check ever refuses something you did want, I'll show you what it refused and ask. A one-line go-ahead typed in the chat, like 'I authorize push access to `<repo>`', has cleared it so far."

The user may prefer to keep approving each step; that works too, just with more clicks. Don't push.

---

## Step 3 — Check whether `claude_research_config` already exists

Find out whether the user is a returning user (with prefs already set up by an earlier bootstrap) or a first-timer (needs the interview). Call the `list_repos` tool (part of the session's GitHub tools, next to the add-repository tool; search your deferred tools if it isn't listed) with `query: "claude_research_config"`.

Don't use the add-repository tool for this check: its reply is the same for a repo that doesn't exist and for one Claude can't access ("was not found on github.com, or this session's GitHub credential doesn't have access to it").

Branch on result:

- **Listed — returning user.** Tell them: *"I can see your `claude_research_config` from a previous setup, so we'll skip the interview and just set up the new research repo."* Skip Step 4 entirely. Continue to Step 5.
- **Not listed, or the tool has nothing to list yet** — ask: *"Have you set up claude_researcher before?"*
  - **No — first-time user.** Tell them: *"Then let's set up your user prefs first, then make a repo for your project."* Continue to Step 4 (interview).
  - **Yes** — the repo may have a different name, or the Claude GitHub App installation may not include it. Ask them to check on github.com, and if needed add it to the installation (github.com → Settings → Applications → Installed GitHub Apps → Claude → Configure → Repository access). Then call `list_repos` again.

`list_repos` has not yet been tested in this step beyond its own description. If it behaves differently from the above, fall back to asking the user directly, and mention it so the step can be corrected (`report-upstream-issue`).

---

## Step 4 (first-time only) — Interview

Run the interview in **three thematic batches** rather than ten sequential questions. After each batch, briefly summarize back what you heard before moving on.

This interview captures persistent **user-level** prefs that get written to `<USERNAME>/claude_research_config/personal_info.md` and read by every future research session. It's about the user, not any specific project — the project comes next, in Step 5.

**Pre-fill from claude.ai memory if available.** If the user has filled out claude.ai's user-level memory ("Things to know about you" / customizations / similar), those are already loaded into your context at chat start — no separate fetch needed. If you can see things like name, role, or research domain there, frame the relevant interview questions as *"From your claude.ai profile I see X — want to use that, or different?"* rather than asking from scratch. If no memory is visible (incognito chats and fresh accounts won't have any), the interview is fully fresh.

### Batch 1 — Identity (3 fields)

> "Three quick identity questions:
>
> 1. What's your name (the one you want me to call you)?
> 2. Your current role or research domain — one sentence.
> 3. A few sentences on your academic + work history at a glance.
>
> It's okay if you don't want to answer right now, and remember you can always ask me for explanations."

Record as `<NAME>`, `<ROLE>`, `<ACADEMIC_HISTORY>` + `<WORK_HISTORY>` (split the third answer if natural; otherwise keep combined under both fields).

### Batch 2 — How they work (3 fields)

> "Three about how you work:
>
> 1. Programming languages and tools you're comfortable with (or 'none' — that's fine).
> 2. General research areas / topics you tend to think about beyond this specific project.
> 3. Any interaction style notes — things you want me to know about how you like to work (pace, push-back, terminology preferences, etc.).
>
> It's okay if you don't want to answer right now, and remember you can always ask me for explanations."

Record as `<PROGRAMMING_LANGUAGES_AND_TOOLS>`, `<RESEARCH_AREAS>`, `<INTERACTION_STYLE_NOTES>`.

### Batch 3 — Operating preferences (4 fields)

> "Four preference questions:
>
> 1. **Git** — the program used to track all changes in your project is called *git*. Are you familiar with it? (If yes, briefly — daily user? occasional? web-UI only? If no, no problem — I'll explain things as we go.)
> 2. **Mode** — pick one: **claude.ai-only** (you'll work on this only through the web UI; no Claude Code locally), or **also-local** (you have Claude Code installed somewhere and might clone the project and work locally too). Repos get created identically either way; this just calibrates how chatty I'll be later about claude.ai-specific quirks.
> 3. **Home repo for personal tasks** — want me to default your *personal tasks* (the ones not tied to a research project, like "remind me about the dentist") to a separate repo? I'll use `<USERNAME>/claude_research_config` (the config repo we're setting up) if you don't specify. Hit Enter to accept that default, or name a different repo as `owner/repo`.
> 4. **Extra paper-source domains** — *(this will not be relevant if your network setting is allow-all — skip it then)* — besides any paper sites you already added back in Step 1, any other domains you'll routinely download papers from? If yes, name them; we'll add them to your `domain_allowlist.txt`. (Reminder: if you're using a domain allow-list, each new domain you add later requires a fresh chat to pick up — better to mention them now than to repeatedly restart.)
>
> It's okay if you don't want to answer right now, and remember you can always ask me for explanations."

Classify the user's git answer internally into one of three tiers and record it as `<GIT_FLUENCY>`: **novice** (web UI only, or no familiarity yet), **occasional** (uses `git clone` / `git push` from the command line sometimes), or **fluent** (uses git daily, including merge / rebase / cherry-pick). The downstream tier dial in `RESEARCHER.md` §1 reads this field; the elicitation above is concept-checking rather than menu-pick on purpose, but the recorded value stays in the existing schema.

Record `<MODE>`, `<HOME_REPO>`, and any extra paper-source domains. For `<HOME_REPO>`, the default (substitute `<USERNAME>` into `<USERNAME>/claude_research_config`) applies if the user hits Enter or doesn't address Q3 explicitly. If they push back with *"what does that mean?"* or similar, give the LIGHT explanation (per `RESEARCHER.md` §0): *"The `task-create` and `task-remind` skills will route stuff like 'remind me about the dentist next month' to this repo, so it doesn't clutter your research project's issue list. Default is the same config repo we're setting up; you can override if you have a dedicated tasks repo."* Don't make this a hard-required question — silence is consent for the default.

After all three batches, summarize the full interview to the user in one paragraph. Get explicit confirmation before proceeding.

---

## Step 5 — First repo: research project, or knowledge base?

Now that user-level prefs are squared away (or pre-existing for returning users), shift focus to the user's first repo. Two paths, branched on whether they have a specific project in mind or are just getting started:

### 5a — Ask which path

Ask:

> "What's the topic of your first research project? One sentence is fine. Or — if you don't have a specific project in mind yet and just want a place to accumulate notes, papers, and emerging ideas, say 'knowledge base' and we'll set up `<USERNAME>/knowledge_base` instead. You can always bootstrap project-specific repos later when ideas crystallize."

### 5b — If they have a specific project

Record the topic as `<TOPIC>`. Suggest a repo name in the format `research-<short-slug>`. Example: if they say "I'm studying how stress affects sleep in adolescents," suggest `research-stress-sleep-adolescents`. Tell them they can press Enter (or say "yes") to accept your suggestion or type something different.

Validate the final name: lowercase, alphanumeric and hyphens only, ≤39 characters (GitHub repo names can go to 100, but shorter is friendlier). Record as `<RESEARCH_REPO>`.

Then ask:

> "That sentence is also your `PROJECT_QUESTION` — the question your paper summaries will measure relevance against. If you'd phrase it differently for that purpose, give me a tighter version; otherwise I'll use the same sentence for both."

Record as `<PROJECT_QUESTION>`. If the user accepts using the same sentence as `<TOPIC>`, the two values will be byte-identical — that's fine. If they tighten it, capture the tightened version. This value is written to the research repo's `STATUS.md` `## Project parameters` section in Step 7.

### 5c — If they want a general knowledge base

For users who are exploring or new to the workflow, `knowledge_base` is the recommended first repo. It has the same structure as a research-* repo (`papers/`, `docs/active/`, `STATUS.md`, etc.) but isn't tied to one specific question. Notes, papers, and observations accumulate there until the user is ready to spin off a focused research project.

Record:
- `<TOPIC>` = `"General knowledge base — notes, papers, and emerging research ideas."`
- `<RESEARCH_REPO>` = `knowledge_base`
- `<PROJECT_QUESTION>` = `"General knowledge base — no single research question yet."` (Users can edit `STATUS.md` `## Project parameters` once a focused question emerges.)

Same seeding flow as a research-* repo from here on.

---

## Step 6 — Create the GitHub repos and give Claude access

A chat can't create repos: claude.ai's GitHub proxy only allows calls scoped to an existing repo, and refuses `POST /user/repos` ("This GitHub API path is not available: sessions are bound to their configured repositories"). So the user creates the repos on github.com, and you attach them.

### 6a — The user creates the repos

Tell the user:

> "Now you'll create the repos on GitHub — two clicks each. Open https://github.com/new and create:
>
> - **`claude_research_config`** — skip this one if Step 3 found it already.
> - **`<RESEARCH_REPO>`**
>
> For each: set it to **Private**, leave **Template** as 'No template', and leave **Add a README**, **.gitignore** and **license** all off, so the repo starts empty and my starter files are its first commit. Then click **Create repository**. Tell me when both exist."

Wait for confirmation.

### 6b — Install the Claude GitHub App (or add the new repos to it)

Connecting GitHub (Step 2b) lets Claude read; the Claude GitHub App is what lets it push.

- **First-time users** — tell them:

  > "One more one-time step: install the Claude GitHub App. Open https://github.com/apps/claude/installations/new, choose your account, pick **Only select repositories**, and select `claude_research_config` and `<RESEARCH_REPO>`. Then click **Install**. (If you set a different home repo for personal tasks in the interview, select it too.)"

- **Returning users** — the App is probably installed already. If it was installed with **Only select repositories**, the new repo has to be added: github.com → Settings → Applications → Installed GitHub Apps → Claude → Configure → Repository access → add `<RESEARCH_REPO>` → Save. With **All repositories**, nothing more is needed.

Wait for confirmation.

### 6c — Attach and verify

Attach each repo to this chat with the add-repository tool (`add_repo`; search your deferred tools if it isn't listed), **read access**, one call per repo, in the same turn. Don't clone them; Step 7 writes over REST. The tool's reply suggests cloning and calling `register_repo_root`; skip both here.

What the replies mean, and the fixes, are in `RESEARCHER.md` §2.0c ("What the replies mean"). The common ones here: "link your GitHub account" → Step 2b isn't done; "was not found … or … doesn't have access" → the name is wrong or the App installation doesn't include the repo (6b).

**Verification affordance.** GET each repo:

```bash
curl -s -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$USERNAME/<REPO_NAME>" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('full_name'), 'private' if d.get('private') else 'NOT PRIVATE', d.get('message',''))"
```

Expect the repo name and `private`. If it says `NOT PRIVATE`, stop and tell the user before writing anything: their research repo would be public.

---

## Step 7 — Seed the new repo(s) with starter files

For each new repo, write the starter files via the Contents API. The exact content of each file is shown in this section. **No transformation between what's shown here and what gets written** — interpolate only the explicit `<PLACEHOLDERS>`.

**Request push first.** Before the first write to each repo, call the add-repository tool again for it with `access: "push"` — the user asked for this setup, so the request follows from their message. A reply of `status: "already_present"` means proceed. Writes may appear to work on the read attachment alone; request push anyway. If the request is refused, show the user the denial text and ask (`RESEARCHER.md` §2.0c "Permission checks").

### The Contents API write recipe

For each file, the call is:

```bash
CONTENT_B64=$(printf '%s' "<FILE_CONTENT>" | base64 -w0)
curl -sX PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/$USERNAME/<REPO>/contents/<PATH>" \
  -d "{\"message\":\"Initial seed: <PATH>\",\"content\":\"$CONTENT_B64\"}"
```

**Verification affordance after each write.** GET the same path; decode the `content` field from base64; confirm it matches what you sent. The response also includes a `sha` you'll need if you ever update the file later.

If the file already exists (e.g., the user ticked **Add a README** in Step 6a), the PUT will fail with a 422 because no `sha` was provided. Either delete the existing file first or include the existing `sha` in the body. The cleanest approach: GET the existing file (capture the `sha`), then PUT with `sha` field included.

### Files to seed in `claude_research_config` (skip if it already existed)

#### `personal_info.md`

Build from interview answers. Use the template at `https://raw.githubusercontent.com/danparshall/claude_researcher/3852c4fda45fc41c3d5eb48ee3fc8448a1af8da5/template/templates/personal_info.md.template` as the structure; substitute each `<FIELD>` placeholder with the corresponding interview answer. The `<YYYY-MM-DD>` last-updated value is today's date.

#### `domain_allowlist.txt`

Fetch the content from `https://raw.githubusercontent.com/danparshall/claude_researcher/3852c4fda45fc41c3d5eb48ee3fc8448a1af8da5/template/templates/domain_allowlist.txt`. If the user named extra paper-source domains in Batch 3, add them to the paper-sources section before writing.

#### `README.md`

```markdown
# claude_research_config

Lifetime config for the claude_researcher workflow. Holds files that every research project of mine reads at session start.

- `personal_info.md` — who I am, how I work, my preferences. Read by every session.
- `domain_allowlist.txt` — record of the network allow-list configured in my claude.ai Settings. Useful for re-creating the same setup on a different machine.

This repo is private. No secrets or research artifacts here — those go in the per-project research repos.
```

#### `.gitignore`

```
_PROJECT_INSTRUCTIONS.md
```

(A rendered copy of the Project Instructions, if the user saves one locally, stays out of the repo; it holds nothing secret, but it's per-Project setup, not repo content.)

### Files to seed in `<RESEARCH_REPO>`

#### `STATUS.md`

```markdown
# Status — <RESEARCH_REPO>

**Last updated:** <YYYY-MM-DD> · **Workflow mode:** branches
**How to read this file:** STATUS logs research-line lifecycle only (row opened at line start, row moved to Archived at merge). Day-to-day detail lives in `docs/active/<branch>/RESEARCH_LOG.md`. Sessions do not write STATUS — only the `start-research-line` and merge ceremonies do. Most sessions only need to read down through the Active Research Lines table.

## Current focus

- Repo just created via claude_researcher bootstrap on <YYYY-MM-DD>. <TOPIC>

## Active Research Lines

Newest-first by start date. Purpose set at line start (1 sentence), amended at milestones.

| Topic | Started | Purpose |
|---|---|---|

(No research lines yet — `start-research-line` adds the first row.)

## Archived Research Lines

Newest-first by archive date. Summary written fresh at archive time (1 sentence, ≤2 if needed); Material = where the record lives (dir, file, results path, or PR).

| Topic | Summary | Archived | Material |
|---|---|---|---|

## Project parameters

Per-project configuration the skills read at runtime (an explicit extra read — this sits below the partial-read fold). Update only when the project's scope or conventions change.

- `PROJECT_QUESTION`: <PROJECT_QUESTION>
- `CONDITIONAL_SECTION`: unset
- `BIB_FILE`: unset
- `PAPERS_INDEX`: PAPER_INDEX.md
- `paper_summaries.structure`: single-file

<!-- main_only repos: replace the two tables above with a capped `## Recent Sessions` (≤20 entries, ≤2 lines each + link; older entries roll to a per-year archive file) plus the same Archived table. -->
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

This repo is configured for the [claude_researcher](https://github.com/danparshall/claude_researcher) workflow. Research sessions happen in a corresponding claude.ai Project, whose sessions clone this repo and push their work back.

For agent-facing instructions, see the upstream [`RESEARCHER.md`](https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/RESEARCHER.md). Personal context (name, preferences, etc.) is in [`<USERNAME>/claude_research_config`](https://github.com/<USERNAME>/claude_research_config).
```

#### `.gitignore`

```
_PROJECT_INSTRUCTIONS.md
```

#### Empty placeholder dirs (`papers/.gitkeep`, `papers/text/.gitkeep`, `docs/active/.gitkeep`, `docs/historical/.gitkeep`)

For each, write a single newline as content; commit message `"Initial seed: <path>"`.

**Verification affordance for the whole step.** After all files are written to a repo, list the contents:

```bash
curl -s -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$USERNAME/<REPO>/contents/" \
  | python3 -c "import sys,json; print('\n'.join(e['path'] for e in json.load(sys.stdin)))"
```

For `claude_research_config` you should see exactly: `.gitignore`, `README.md`, `domain_allowlist.txt`, `personal_info.md`. For the research repo: `.gitignore`, `README.md`, `RESEARCH_LOG.md`, `STATUS.md`, plus the four `.gitkeep`-bearing directories. If anything's missing or extra, surface to the user.

---

## Step 8 — claude.ai Project setup

This step is **procedural** — you instruct, the user clicks. You don't have access to modify the user's claude.ai Projects; this is the user's authority alone. Walk them through it.

> "Open a new browser tab to: https://claude.ai/projects/new
>
> 1. **Project name:** `<RESEARCH_REPO>` (the name we just created in GitHub)
> 2. **Description:** `<TOPIC>`
> 3. Click **Create**.
>
> Once you're inside the new Project, you'll paste a block of text into the **Project Instructions** field. It tells every chat in the Project which repo is yours and where the workflow's instructions live. Nothing in it is secret. **Don't** upload anything as a file — the Project Instructions field is the only paste target."

### Project Instructions text — what to paste

The canonical Project Instructions text lives at:

> `https://raw.githubusercontent.com/danparshall/claude_researcher/3852c4fda45fc41c3d5eb48ee3fc8448a1af8da5/template/_PROJECT_INSTRUCTIONS.md.template`

**WebFetch it.** Substitute the placeholders before showing the result to the user:

- `<USERNAME>` → the GitHub username from Step 2a
- `<REPO>` → the research repo name from Step 5

Present the rendered text to the user as a single code block. Tell them:

> "Copy this entire block and paste it into your new Project's **Project Instructions** field. That puts it into every chat's context from the very first message, before any fetching happens. **Don't upload this as a file.**"

**Verification affordance.** Once the user confirms the paste, ask them to spot-check that both substitutions are present in the pasted text — the literal strings `<USERNAME>` and `<REPO>` should NOT appear; the actual values should. If either placeholder is still literal, the runtime agent won't know which repo to attach — have them re-render and re-paste.

---

## Step 9 — Validation

Tell the user:

> "Open a new chat in your `<RESEARCH_REPO>` Project. Just say 'hi' or 'let's begin' — see what happens."

Wait for them to do this and report back. **Expected:** the agent in the new chat clones the upstream template per its Project Instructions, reads `RESEARCHER.md` from the local clone, attaches the research repo and `claude_research_config` read-only (the user may see an approval box for each, depending on their permission mode), clones the research repo, fetches `personal_info.md` via the Contents API, and greets the user by name with a reference to their topic.

If validation fails, the most common causes (in rough order of likelihood):

1. **A repo couldn't be attached, or a step was refused** → the new chat's agent should quote the reply or denial text; match it against `RESEARCHER.md` §2.0c (GitHub not connected, App installation missing the repo, or a permission-check refusal). Most common.
2. **Project Instructions text missing, truncated, or has unsubstituted `<USERNAME>` / `<REPO>` placeholders** → re-render the canonical text and re-paste per Step 8. Spot-check that no literal placeholders remain.
3. **Network access not enabled, or the change hasn't propagated** → re-check Settings per Step 1, including running the `curl -sI https://example.com` probe. If the **network egress** setting was changed *during* a chat that was already open, it won't have propagated; restart in a fresh chat (per Step 1c's hand-off).
4. **Clone fails / `RESEARCHER.md` unreachable from claude.ai** → confirm the upstream repo (`danparshall/claude_researcher`) is public and `git clone --depth 1 https://github.com/danparshall/claude_researcher.git` succeeds in the sandbox. Agents that can't clone should fall back to `WebFetch https://raw.githubusercontent.com/danparshall/claude_researcher/main/template/RESEARCHER.md`. If the repo was recently flipped from private to public, the clone reflects current state immediately, but the raw-CDN fallback path can lag by 24+ hours.

Help the user troubleshoot. Iterate until validation passes.

---

## Step 10 — Done

### Egress-revisit reminder (first-time bootstrap only)

If this is a first-time bootstrap (Step 3 returned 404 and Step 4 ran), file a one-week reminder so the user revisits their egress setting via the `task-remind` skill — operationalizes the promise made in §1b.

If the egress was configured inline in *this* chat, you know what the user picked. If the egress was configured in a prior chat (§1c hand-off), the choice didn't persist across the restart; ask:

> "Quick check: back when you turned on network egress, did you go with 'allow everything', set a restrictive domain allow-list, or you're not sure?"

On allow-all, offer the reminder and file it only on a yes — it's an issue written to their repo, so the user should ask for it:

> "Want me to file a one-week reminder to revisit that setting? It shows up at the start of your next session after that date."

**File the reminder only on confirmed allow-all and a yes.** If the user picked a domain allow-list, or isn't sure, skip the rest of this sub-step — and if they're unsure, tell them they can file the reminder themselves anytime by saying *"remind me to revisit my egress setting in a week"* (the `task-create` skill handles it). This matches §1b's promise, which was specifically conditional on the allow-all choice.

On confirmed allow-all and a yes: if `<HOME_REPO>` isn't `claude_research_config`, attach it read-only with the add-repository tool (the user named it in Step 4). Then request push for it (`access: "push"`; `already_present` means proceed) before the writes below.

```bash
TODAY=$(date -u +%Y-%m-%d)
FIRE_DATE=$(date -u -d '+7 days' +%Y-%m-%d)
# <HOME_REPO> from Step 4 Batch 3 (defaults to "$USERNAME/claude_research_config" if user accepted the default)
HOME_REPO="<HOME_REPO>"

# 1. Verify <HOME_REPO> exists. If the user customized HOME_REPO to a not-yet-existing repo in Step 4 Batch 3,
# the label + issue POSTs below would 404 silently; better to detect and surface up front.
REPO_HTTP=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$HOME_REPO")

if [ "$REPO_HTTP" != "200" ]; then
  # Tell the user: "Skipping the egress-revisit reminder — `$HOME_REPO` returned HTTP $REPO_HTTP (403 usually means it isn't attached to this chat), so I can't file there. You can file it yourself anytime by saying 'remind me to revisit my egress setting in a week.'"
  # Then skip the rest of this sub-step.
  echo "skip-reminder: HOME_REPO check returned $REPO_HTTP"
else
  # 2. Dedupe — if an open egress-revisit reminder already exists in <HOME_REPO>, don't file a second one.
  # (Returning-user paths shouldn't reach this sub-step at all, but the gate is verbal; this is the programmatic backstop.)
  EXISTING=$(curl -s \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/$HOME_REPO/issues?state=open&labels=task&per_page=100" \
    | python3 -c "
import json, sys
try:
    issues = json.load(sys.stdin)
    print(any('Revisit claude.ai network egress' in (i.get('title') or '') for i in issues))
except Exception:
    print(False)
")

  if [ "$EXISTING" = "True" ]; then
    # Tell the user: "An open egress-revisit reminder already exists in `$HOME_REPO`; not filing a duplicate."
    echo "skip-reminder: existing open reminder found"
  else
    # 3. Ensure the `task` label exists in <HOME_REPO> (idempotent — 422 if it already does, which is fine; the issue create still works).
    curl -sX POST \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      -H "Content-Type: application/json" \
      "https://api.github.com/repos/$HOME_REPO/labels" \
      -d '{"name":"task","color":"0052CC","description":"Tracked todo (task-create skill)"}'

    # 4. File the reminder issue. Body built via heredoc + python3 json.dumps to avoid shell-escaping the prose.
    export TODAY FIRE_DATE
    BODY=$(cat <<EOF
Filed by claude_researcher bootstrap on ${TODAY}. You chose the broad "allow all" option for claude.ai network egress during bootstrap.

Now that you have used the workflow for a bit, you may want to tighten this to a domain allow-list. claude.ai reaches your GitHub repos through its own GitHub proxy; list \`github.com\` and \`raw.githubusercontent.com\` anyway (untested whether they're needed), plus any paper sources you regularly download from. The \`domain_allowlist.txt\` file in your \`claude_research_config\` repo has a starting list.

The \`task-remind\` skill will surface this reminder automatically at the start of your next session on or after ${FIRE_DATE}.
EOF
)
    export BODY

    RESPONSE=$(python3 -c "import json, os; print(json.dumps({'title': f'[{os.environ[\"FIRE_DATE\"]}] Revisit claude.ai network egress setting', 'body': os.environ['BODY'], 'labels': ['task']}))" \
      | curl -sX POST \
        -H "Accept: application/vnd.github+json" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        -H "Content-Type: application/json" \
        "https://api.github.com/repos/$HOME_REPO/issues" \
        -d @-)

    # 5. Extract issue URL. Wrap in try/except so a non-JSON response (transient 5xx, HTML error page from an edge proxy, empty body) falls back gracefully instead of crashing the bash recipe.
    ISSUE_URL=$(printf '%s' "$RESPONSE" | python3 -c "
import json, sys
fallback = '(URL parse failed; check $HOME_REPO Issues tab)'
try:
    print(json.load(sys.stdin).get('html_url', fallback))
except Exception:
    print(fallback)
")
    unset BODY TODAY FIRE_DATE
  fi
fi
```

Tell the user the reminder landed (or surface the skip reason from the bash block, if any):

> "Filed the egress-revisit reminder as `<ISSUE_URL>`. It'll surface automatically at the start of your next research session on or after `<FIRE_DATE>` — close it then or whenever you've decided whether to tighten the setting."

### Closing message

Tell the user:

> "Bootstrap complete. From now on:
>
> - **To work on this research project:** open a new chat in the `<RESEARCH_REPO>` Project. Tell the agent what you're working on; it'll handle the rest.
> - **To start a new research project:** paste the bootstrap prompt again into a fresh chat. Your `claude_research_config` will be re-used; you'll create only the new research repo (Steps 5–8).
> - **To file an issue or request a feature:** ask the agent in any session — they'll generate a pre-filled URL pointing at the upstream issue tracker."

Stop. Do not continue with any further actions. The bootstrap is complete.

---

## Appendix — Common issues

- **A step was refused by the permission check** (auto mode): show the user the exact denial text and the step it blocked, and ask. See `RESEARCHER.md` §2.0c "Permission checks".
- **add-repository says the repo "was not found on github.com, or this session's GitHub credential doesn't have access to it":** the name is wrong, the repo doesn't exist yet (Step 6a), or the Claude GitHub App installation doesn't include it (Step 6b). Check with `list_repos`, then ask the user.
- **add-repository says "link your GitHub account":** Step 2b isn't done.
- **403 "This GitHub API path is not available: sessions are bound to their configured repositories":** the call wasn't repository-scoped (for example creating a repo). Only `repos/{owner}/{repo}/...` paths work; the user creates repos on github.com (Step 6a).
- **403 mentioning `add_repo` on a REST call:** the repo isn't attached to this chat yet (Step 6c).
- **415 on a write:** the request is missing `-H "Content-Type: application/json"`.
- **"422 Unprocessable Entity" on a Contents API PUT:** the file already exists and you didn't include its `sha`. GET the file first, capture `sha`, retry the PUT with `sha` field included.
- **Connection error / "could not resolve host" on a non-GitHub site:** network access isn't enabled, or doesn't permit the host, or the change hasn't propagated to this chat. Re-check Step 1; if the change was made during this chat, restart in a fresh one (Step 1c).
- **GitHub says the repo name already exists when the user creates it:** an earlier bootstrap attempt got partway. Reuse it if it's empty or holds only seed files (Step 7's 422 note covers files already there).
