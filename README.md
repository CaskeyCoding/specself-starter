# SpecSelf Starter

**A life operating system your AI agent runs *with* you.**

SpecSelf Starter is a clone-and-go template for organizing your whole life —
principles, vision, goals, areas, projects, habits — as plain markdown that an
AI agent (Claude Code or any agent that reads files) can reason over with you.

It applies the rigor of spec-driven development to living: every part of your
life becomes a diffable, dated, falsifiable artifact. The agent surfaces,
connects, and challenges. **You decide and author.** Nothing here ships your
data anywhere — your content lives in `your-life/`, on your machine, in your
own private repo. No server, no account, no keys to lose.

> "Specs for the self." The discipline you'd apply to a system, applied to a life.

---

## The one rule

> **You decide and commit. The agent organizes, connects, surfaces, and
> challenges — but never silently authors your life.**

Every design choice in this kit serves that rule. It is what makes it safe to
hand an agent your whole life. See [`steering/philosophy.md`](steering/philosophy.md).

## The spine: horizons of focus

Your daily actions connect all the way up to who you want to be. The agent's
core job is keeping these layers **coherent** — flagging the project that serves
no goal, the goal that contradicts a principle, the area you've starved all week.

| Horizon | Artifact | Lives in |
|---|---|---|
| **5 — Purpose & Principles** | what you stand for | `your-life/principles/`, `aspirational.md` |
| **4 — Vision** (3–5 yr) | who you're becoming | `your-life/vision.md` |
| **3 — Goals** (6–24 mo) | outcomes with success criteria | `your-life/goals/` |
| **2 — Areas** (ongoing) | roles & standards to maintain | `your-life/areas/` |
| **1 — Projects** (weeks–months) | outcomes with a finish line | `your-life/projects/` |
| **Ground — Actions** | daily capture & plans | `your-life/journal/`, `reviews/` |

See [`steering/coherence.md`](steering/coherence.md) for how the agent checks
alignment across horizons.

## Quickstart (5 minutes)

1. **Use this template** (or clone it) into a new private repo.
2. Open it with your agent. Tell it:
   > "Read `AGENTS.md` and everything in `steering/`, then walk me through `GETTING-STARTED.md`."
3. Do the **foundation session** once — the agent interviews you and seeds the
   stack with your first principles, vision, areas, and goals.
4. Run the loop from there: `/daily` capture, `/weekly` review, monthly+ deep
   sessions. The agent reminds; you reflect.

Your content goes in `your-life/`, which is **gitignored by default**. Commit the
*structure*, keep the *content* private. See [`steering/privacy.md`](steering/privacy.md).

## What's in the box

```
specself-starter/
├── AGENTS.md            The operating contract (works with any agent)
├── CLAUDE.md            Claude Code accelerators (subagents, slash commands)
├── GETTING-STARTED.md   The one-time foundation session
├── steering/            The method — your agent reads this every session
│   ├── philosophy.md    The contract: you decide, the agent organizes
│   ├── methodology.md   Two-axis principles + the horizons model + lifecycle
│   ├── cadence.md       The daily → annual review loop
│   ├── coherence.md     How the agent checks alignment across horizons
│   ├── privacy.md       Keeping your life yours
│   └── tone.md          How the agent challenges without lecturing
├── personas/            Lenses the agent adopts to interview and challenge you
├── templates/           One template per artifact: principle, goal, project, …
├── .claude/             Claude Code extras: persona subagents, /commands, hooks
└── your-life/           YOUR content — gitignored; structure committed
```

## Works with any agent

The kit is plain markdown. `AGENTS.md` is the agent-neutral contract — point any
capable agent at it. If you use **Claude Code**, the `.claude/` directory adds
accelerators: each persona becomes a subagent, each review tier becomes a slash
command (`/daily`, `/weekly`, `/capture`, `/review`, `/coherence-check`), and a
SessionStart hook nudges you when a tier is overdue.

## License & attribution

SpecSelf Starter is offered for you to fork and adapt. Suggested licensing:
MIT for the scaffolding/code, CC-BY for the method docs. Pick what fits before
you publish a fork. The method here is the structure and the prompts — your
principles and your life are entirely your own.
