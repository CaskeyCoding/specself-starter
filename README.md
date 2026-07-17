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

"Spec" here means exactly what it means in software: a dated, versioned
statement of intent that reality gets checked against. Your principles and
goals are written as specs; the reviews are the tests.

---

## Test drive it in five minutes

You do not have to tell the system anything about yourself to see what it does.
Clone the repo and run the weekly coherence report over the worked example
corpus:

```bash
python scripts/coherence.py examples/sam-rivers
```

You get the same kind of report the kit gives you after a few weeks of real
use: the orphaned project, the starved area, the principle drifting from its
evidence, and the one question worth sitting with. No account, no personal
input, nothing to set up beyond the clone.

## The one rule

> **You decide and commit. The agent organizes, connects, surfaces, and
> challenges — but never silently authors your life.**

Every design choice in this kit serves that rule. It is what makes it safe to
hand an agent your whole life. See [`steering/philosophy.md`](steering/philosophy.md).

## See it work

This is not an abstract framework. After a few weeks of use, a weekly review
ends like this: a short report that names the gaps you would otherwise miss,
followed by one question worth sitting with.

<!-- source: steering/coherence.md -->

```
Coherence, 2026-05-30 (weekly)

Orphans:       1  (project: redesign-portfolio → no goal)
Contradictions:1  (goal: double-client-load x principle: protect-deep-work)
Starved areas: 1  (health, 0 evidence in 21d)
Over-capacity: yes (7 active projects, 5 stalled)
Stale:         1  (goal: learn-piano, recommend contested)
Drift:         1  (aspirational → revealed candidate: give-feedback-i-d-want)

Top question this week: You have 7 active projects and starved health for
3 weeks. What comes off the list?
```

The agent surfaces and challenges here; it never authors your record.

## The spine: horizons of focus

Your daily actions connect all the way up to who you want to be. The agent's
core job is keeping these layers **coherent** — flagging the project that serves
no goal, the goal that contradicts a principle, the area you've starved all week.

| Horizon | Artifact | Lives in |
|---|---|---|
| **5 — Purpose & Principles** | what you stand for | `your-life/principles/`, `your-life/aspirational.md` |
| **4 — Vision** (3–5 yr) | who you're becoming | `your-life/vision.md` |
| **3 — Goals** (6–24 mo) | outcomes with success criteria | `your-life/goals/` |
| **2 — Areas** (ongoing) | roles & standards to maintain | `your-life/areas/` |
| **1 — Projects** (weeks–months) | outcomes with a finish line | `your-life/projects/` |
| **Ground — Actions** | daily capture & plans | `your-life/journal/`, `reviews/` |

See [`steering/coherence.md`](steering/coherence.md) for how the agent checks
alignment across horizons.

## Get started (setup: about 5 minutes; first sitting: 15-20 minutes)

1. **Use this template** (or clone it) into a new private repo. (about 5 minutes)
2. Open it with your agent. Tell it:
   > "Read `AGENTS.md` and everything in `steering/`, then walk me through `GETTING-STARTED.md`."
3. Do the **first foundation sitting** once (about 15-20 minutes, per
   `GETTING-STARTED.md`): the agent interviews you and drafts your first
   candidate principles. The rest of the foundation (vision, areas, goals,
   projects) spreads across three more short sittings over your first week, so
   the largest ask never lands on day one. Arriving with years of notes
   already? Run `/adopt` instead and draft a first corpus from them.
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
├── CHANGELOG.md         Structure changes, versioned (for upgrading a fork)
├── UPGRADING.md         Pull kit improvements without touching your corpus
├── examples/            A fictional worked corpus — see the system alive
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
accelerators: each persona becomes a subagent, each cadence tier becomes a skill
(`/foundation`, `/daily`, `/weekly`, `/monthly`, `/quarterly`, `/annual`) with
`/capture` and `/coherence-check` as helpers, plus a SessionStart nudge and a
privacy guard that blocks committing your corpus or secrets.

## The hosted companion (optional)

There is a hosted SpecSelf app, and it is deliberately **narrower** than this
kit: a principles + journal engine (the foundation interview, daily capture,
weekly and monthly reviews, principle synthesis, and a principles-scope
coherence report). It does not manage goals, areas, projects, or habits, and
it will not grow those surfaces; this repo layout is the wider system of
record. The app speaks the same contracts this kit defines (the schemas,
personas, prompts, and question bank here are the single source it vendors),
and it exports your corpus in exactly this kit's `your-life/` shape, so you
can start hosted and graduate to your own repo, or ignore the app entirely.
The export includes an `EXPORT-REPORT.md` that names anything you need to
backfill (a revealed principle still missing its dated evidence, say) before
`scripts/validate.py` passes, so graduation is honest about what is left to do
rather than promising a clean round trip. The kit is the whole method; the app
is one convenient engine for part of it.

## Upgrading after you've diverged

The kit is a starting point, not a dependency — but when upstream ships a better
template or a new skill, you can pull those **structure** improvements without
losing your edits and **without ever touching your `your-life/` corpus**. Add the
starter as an `upstream` remote, then run the **`/upgrade`** skill (or
`bash .claude/skills/upgrade/upgrade-diff.sh upstream/main`): it's a dry run that
shows what changed in the structure and lets you apply each file you want, one at a
time. [`CHANGELOG.md`](CHANGELOG.md) tracks what changed; [`UPGRADING.md`](UPGRADING.md)
walks the flow with a worked example.

## License & attribution

SpecSelf Starter is MIT-licensed (see [`LICENSE`](LICENSE)): fork it, adapt
it, build on it, commercially or not. The method here is the structure and
the prompts. Your principles and your life are entirely your own and never
part of this license.
