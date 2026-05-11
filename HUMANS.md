# HUMANS.md

The long-form companion to the README. If the README is "how to start," this is "why this exists, what to expect, and how to get the most out of it."

## What this is

If you've used Claude.ai for research conversations, you've probably noticed how much gets lost between chats. Every new session is a blank slate: the agent doesn't remember the paper you discussed last week, the framing you settled on, the half-formed hypothesis you wanted to come back to. You end up either pasting context every time or simply re-doing thinking you've already done.

`claude_researcher` adds persistent memory of your work to claude.ai — a record of your projects, the papers you've read, the conversations you've had, and the reasoning that came out of them. Each session starts from where you left off. Nothing installs on your machine; everything lives in a private GitHub repository you own, and the agent reads and writes it on your behalf when you start a new chat.

## What a session feels like

Suppose you're a researcher working on coastal adaptation policy, and you've been at it for a few months. You open Claude.ai, navigate to your `claude_researcher` Project, and start a new chat with: *"Let's pick up on the managed retreat work."*

The agent reads its runtime instructions, your researcher profile (it knows you're an economist at a public policy school, you prefer Python, you talk to it as a colleague rather than a tool), and the status of your repository (it sees an active research line called `managed-retreat`). It pulls up the conversation log from your last session and picks up where you left off: *"Last time we ended on the tension between federal buyout efficiency and state-level political feasibility. You wanted to look at how the Hurricane Sandy programs were structured — did you have time to find the GAO report?"*

You paste a PDF. The agent saves it to your repo with a clean filename, extracts the text, and writes a summary indexed against your reading notes. You discuss for an hour. When you're done, you say *"good stopping point."* The agent writes a permanent record of the conversation into your repo, updates the status log, and notes what's open for next time.

Next week, in a fresh chat, the cycle starts again — but everything from the prior session is there.

## Where this comes from

Anthropic ships a CLI tool called Claude Code for developers. It introduced a convention that's been quietly powerful: at the root of any project, you put a file called `CLAUDE.md` containing standing rules and context — what the project is, how you work, what conventions matter. The agent auto-discovers it. Separately, in a `~/.claude/skills/` folder, you keep reusable workflow recipes — "how to add a paper to my reading list," "how to wrap up a conversation," "how to write a plan." The agent loads these on demand when their triggers fire. The combination is closer to a working environment than a chatbot: persistent memory, opinionated workflows, an agent that comes to you already knowing what your project is about.

Around this pattern, ecosystems grew. **Nori** is an open-source bundle of skills built by [tilework-tech](https://github.com/tilework-tech/nori-skillsets), oriented primarily toward software engineering — test-driven development, debugging, code review, plan-writing, large-task handling. A Claude Code user installs Nori and instantly has a curated set of opinionated working styles backed by the agent. It's been formative for how a lot of people think about agent-assisted work.

Nori has a sub-skillset called **Researcher**, aimed at researchers using Claude Code locally for paper triage, multi-session reasoning, and writing. That's where the design DNA of this project comes from. We took Researcher's patterns — `STATUS.md`, `RESEARCH_LOG.md`, on-demand skills, the convention of capturing conversations and plans as durable artifacts — and rebuilt them for an environment where the user doesn't have a terminal. The Project Instructions field on a Claude.ai Project plays the role of the Code `CLAUDE.md` convention; a public GitHub repo (this one) plays the role of `~/.claude/skills/`; the sandbox's network access plays the role of local filesystem reads.

The result is the same working pattern, ported to the browser. The web is the immediately-available surface — no install, no terminal, just a claude.ai Project — and it's enough on its own for research workflows. Claude Code is an option that opens up later if you install it locally: full Nori SWE skillset, offline access, code-friendly tools. This project's conventions carry across both surfaces (skill names match, file conventions are the same, mental model carries over), so Code adds to what you have rather than replacing it.

## What it isn't

This project is scoped on purpose. It's trying to be very good at *one thing*: making Claude a useful research collaborator for someone who works entirely in a browser. A few things it deliberately doesn't try to be:

- **A full Nori replacement.** Skills around UI testing, worktrees, agentic software development, and decision-doc maintenance aren't included. If you find yourself wanting these, install Claude Code locally and use Nori directly.
- **A collaboration platform.** v1 assumes a solo researcher owns the research repo. Multi-person teams (a professor sharing a repo with a grad student, say) are planned for v1.1 but aren't here yet.
- **A coding environment.** You can do small amounts of analysis or scripting through the agent, but the design center is research conversation, paper management, and durable notes — not building software.
- **A perfect abstraction.** The Project Instructions field is one place where you have to paste a small block of text to bootstrap each Project. It's a one-time setup per Project, but it's not invisible.

## Where instructions to Claude live

If you've used Claude Code, you've encountered a small ecosystem of files where instructions to the agent can live — `~/.claude/CLAUDE.md` for user-level rules across all projects, a `CLAUDE.md` in each repo for project-level rules, a skills folder for reusable workflows. The web has direct analogs:

- **Personal preferences** in claude.ai Settings — the web analog of `~/.claude/CLAUDE.md`. Applies to all your claude.ai chats, regardless of Project.
- **Project Instructions** — the per-Project field; the analog of a local repo's `CLAUDE.md`. In our bootstrap, the only thing this field does is pass the credentials and bootstrap recipes the agent needs to read the real workflow doc.
- **`RESEARCHER.md` in the upstream `danparshall/claude_researcher` repo** — the actual workflow rules. At session start, the agent clones the upstream template into its sandbox (a "clone" is just a copy of the repo's files), then reads `RESEARCHER.md` from there. Keeping the workflow doc in the upstream repo — rather than copied into each user's research repo at bootstrap — means every session reads the same canonical version, upstream fixes propagate automatically, and a web-only user still has a real repo-level instructions doc they can read on GitHub.

And then there's the surface this project actually leans on:

- **`personal_info.md` in your `basic_config` repo** (on GitHub, private) — your name, role, git fluency tier, interaction style, paper-naming convention, anything else you want the agent to know across all your research projects.

The deliberate choice: `personal_info.md` is the canonical home for your preferences in this project. Three reasons. First, it works for users with no local machine access, which is the whole design center. Second, it's one place — your personal context applies to every research project you spin up, not a separate setting per Project. Third, you can ask the agent to update it during any session: *"add to my personal_info that I prefer Python over R,"* *"update my interaction style to be terser,"* *"note that I've moved fields."* The agent edits the file, commits it, and the next session reads the new version. It's a real file you can read and edit yourself on GitHub.com — not a black-box memory the agent owns.

The other surfaces still exist and still work. If you have something genuinely universal you want applied to every claude.ai chat regardless of project, the Settings preferences field is the right home. If you eventually install Claude Code locally, the local `CLAUDE.md` files matter again. But for the day-to-day of working in this project, `personal_info.md` is the only surface you need to think about.

## Tips and notes

### Treat the agent like a colleague — including in your writing about it

This is the most counter-intuitive thing to learn, and it's load-bearing. Language model agents form working mental models of the role they've been cast into, and behave according to that model. If your standing instructions, your project notes, and your in-conversation prompts treat the agent as a careless intern who needs to be hemmed in by aggressive guardrails — *"DO NOT under any circumstances..."* — the agent reads itself as that careless intern, and produces the kinds of mistakes a careless intern would make. If instead the same documents frame the agent as a responsible collaborator whose judgment is trusted within bounds, you get back work that reflects that trust.

The mechanism is closer to acting than to instruction-following. The agent isn't reading your guardrails as constraints to navigate around; it's reading them as evidence about who it's playing. The word "persona" in our `personal_info.md` setup is deliberate. Being warm and direct with the agent, telling it what you want rather than what you don't want, treating it as someone whose work you respect — these aren't politeness for politeness's sake. Being nice to the agent produces better work, for entirely self-interested reasons.

The corollary: if a session starts going badly — the agent feels confused, defensive, or sloppy — the fastest fix is usually to wrap the conversation cleanly and start fresh, rather than to push harder. A frustrated session compounds; a fresh session reads the same notes and starts again from neutral.

### Don't fight the session-start fetches

Each fresh chat begins with the agent loading half a dozen files — your profile, your project status, the upstream workflow instructions, the skill manifest. It's noisier than chatting with a clean Claude window. But that orientation is what produces the continuity. If you skip it ("just answer the question, don't load anything"), you get the equivalent of a temp worker who's never seen the project — accurate-sounding output that misses the actual context.

The agent uses your research repo's `STATUS.md` and `RESEARCH_LOG.md` as the canonical record of your work, not claude.ai's chat-history surface. Two reasons. First, claude.ai's chat-history summaries aren't visible to you and can drift in ways neither of you can audit; the markdown files in your repo are version-controlled and you read the same text the agent does. Second, you can edit those files when something is wrong — try editing a chat-history summary. If the agent ever does search past chats during a session, it should be because you explicitly asked for something not reflected in the repo records.

### Pick research-line names with future-you in mind

Each research line gets a short hyphenated name — `managed-retreat`, `cap-and-trade-microeconomics`. Pick ones you'll recognize months later. `temp` and `working` are tempting in the moment but unhelpful when you have a dozen lines accumulated.

### Why you'll be asked to name the conversation

Within the first message or two, the agent will propose a name for this session — something like `20260511_managed_retreat_planning`. Accept it or counter-propose; the exact name matters less than the fact that one gets established early.

The reason is structural: the agent cannot see the title of the claude.ai chat from inside the chat. That title — the one you can edit in the sidebar — is invisible from the agent's side. So without a user-confirmed name established by handshake, there's no stable identifier connecting the various artifacts the agent might create this session: the conversation summary in `docs/convos/`, any plan documents in `docs/plans/`, any results files, the STATUS recent-sessions entry. The handshake creates that join key. Later, when you or a future agent wants to ask "what was the reasoning behind that decision?", the trail leads back through the convo name to the recorded reasoning.

If you don't expect to produce durable artifacts in a session — a quick lookup, a short chat — just tell the agent "no need to log this one" when it asks. The handshake is fast and easy to opt out of.

### Use `add-paper` for PDFs you actually want engaged with

Dropping a PDF into chat just shows it to the current conversation. The `add-paper` skill — invoked by saying "add this paper" or similar — does something more useful: renames the file to your canonical format, extracts the text, writes a summary, indexes it against your reading list. The next session can ask about that paper without you re-uploading anything. If you're going to do real work with a paper, run it through `add-paper` once at the start.

### Update `personal_info.md` as your work evolves

The agent calibrates to it — your role, your tools, your interaction style. If you've shifted fields, picked up a new methodology, or just noticed the agent's tone is wrong for you, update the file. A line edit takes seconds and changes a lot.

### When in doubt, wrap and start fresh

Context windows are finite, and a long session accumulates entropy. If the agent feels off, the conversation has wandered, or you're about to start a meaningfully different topic — say "let's wrap." The `finish-convo` skill writes a permanent record of the conversation; the next chat picks up cleanly from there. The wrap is cheap, the long-session drift isn't.
