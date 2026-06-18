# CLAUDE.md — Claude Code Accelerators

This file is for [Claude Code](https://claude.com/claude-code). It layers
tool-specific conveniences on top of the agent-neutral contract.

**Read [`AGENTS.md`](AGENTS.md) first — it is the source of truth.** Everything
there applies. This file only adds Claude Code mechanics.

## Always-on context

At the start of every session, load:

- [`AGENTS.md`](AGENTS.md) — the operating contract
- [`steering/`](steering/) — the method (philosophy, methodology, cadence,
  coherence, privacy, tone)

Then load the human's current state from `your-life/` as the tier requires.

## Slash commands

Defined in [`.claude/commands/`](.claude/commands/):

| Command | Tier | What it does |
|---|---|---|
| `/capture` | any time | Quick journal capture — 1 decision, 1 friction, 1 surprise |
| `/daily` | daily (~2 min) | Today's intent + yesterday's evidence; writes a dated journal entry |
| `/weekly` | weekly (~20 min) | Cluster the week's entries, run the coherence check, surface candidates |
| `/review` | monthly+ | Deep session: synthesize candidate principles/goals, falsification sweep |
| `/coherence-check` | any time | Vertical alignment audit across all horizons (read-only report) |

## Personas as subagents

Each lens in [`personas/`](personas/) has a matching subagent in
[`.claude/agents/`](.claude/agents/). Invoke one to run a session through that
lens — e.g. the **Skeptic** to stress-test a principle, the **Coach** for a
tactical execution review, the **Future-Self** for an annual rewrite. Respect the
pairing rules in each persona file (some pair poorly in the same session).

## SessionStart hook

[`.claude/settings.json`](.claude/settings.json) wires a SessionStart hook that
reminds you which review tiers are overdue (based on the dates of the latest
entries in `your-life/reviews/`). It only *nudges* — it never authors a review.

## Claude-Code-specific guardrails

- Treat `your-life/.sensitive/` as off-limits — do not read or grep it, even if
  asked to "search everything."
- This repo is the human's private life. Do not run commands that would push
  `your-life/` content to any remote unless they explicitly direct it.
- When proposing candidate principles/goals, write them to the target file as a
  clearly-marked `<!-- CANDIDATE - edit or delete -->` block, never as committed
  text.
