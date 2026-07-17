# CLAUDE.md — Claude Code Accelerators

This file is for [Claude Code](https://claude.com/claude-code) (and Fable). It is
the fast path for running the kit in Claude Code; it adds tool mechanics on top of
the agent-neutral contract and **never restates a rule**.

**Read [`AGENTS.md`](AGENTS.md) first — it is the source of truth.** The one rule,
the standing jobs, the hard boundaries, and the tone all live there and all apply.
This file points at them; it does not copy them. Delete this file and the kit still
runs from `AGENTS.md`.

## Always-on context

At the start of every session, load:

- [`AGENTS.md`](AGENTS.md) — the operating contract
- [`steering/`](steering/) — the method (philosophy, methodology, cadence,
  coherence, privacy, tone)

Then load the human's current state from `your-life/` as the tier requires.

## Cadence sessions are skills

The reflection tiers ship as skills in [`.claude/skills/`](.claude/skills/). Invoke
one by name; each reads `steering/` first, hydrates the matching `templates/` file,
runs the coherence check on weekly+, and writes only `<!-- CANDIDATE -->` drafts
(see [`.claude/skills/README.md`](.claude/skills/README.md)).

| Skill | When | Lead lens |
|---|---|---|
| `/foundation` | once, at setup (first sitting 15-20 min; rest across week one) | Intake / Journalist |
| `/daily` | daily (~2 min) | Journalist |
| `/weekly` | weekly (~20 min) | Coach + Journalist |
| `/monthly` | monthly (~60 min) | Skeptic + Therapist |
| `/quarterly` | quarterly (~90 min) | Skeptic + Forensic-Auditor |
| `/annual` | yearly (half day) | Future-Self + Biographer + Stoic |

Two any-time helpers stay as slash commands in [`.claude/commands/`](.claude/commands/):
`/capture` (a quick journal jot) and `/coherence-check` (a standalone read-only
alignment audit; the weekly+ skills run this inline).

## Personas are subagents

Each lens in [`personas/`](personas/) has a matching subagent in
[`.claude/agents/`](.claude/agents/). Spawn one to run through that lens — the
**Skeptic** to stress-test a principle, the **Coach** for a tactical review, the
**Future-Self** for the annual rewrite. The subagent reads its persona file at
runtime (single source of truth). Respect the pairing rules in each persona file
(some pair poorly in one session). The cadence skills already name their lead lenses.

## The privacy guard

[`.claude/settings.json`](.claude/settings.json) wires a `PreToolUse` hook that
**blocks any `git commit`/`git push`** which would include private `your-life/`
corpus or a secret, and a `SessionStart` hook that nudges you when a review tier is
overdue (it only prints; it never authors a review). The same guard runs without
Claude via the `pre-commit` fallback. See the privacy-guard section of
[`GETTING-STARTED.md`](GETTING-STARTED.md) (including the `.specself-allow-corpus`
opt-in for a deliberate private repo).

## Memory

Your corpus is the `your-life/` files, not Claude Code memory. Do **not** persist
corpus content (journal entries, principles, anything personal) into Claude Code's
saved memory — it is not the human's authored file and can outlive the session.
Memory is fine for tool preferences; the life OS state lives only in `your-life/`.

## Plan mode and the foundation session

The `/foundation` session is generative — it writes candidate drafts under
`your-life/` — so run it in normal mode, not plan mode (plan mode is read-only and
would block the drafting). If you want to preview the five passes first, use plan
mode to outline them, then exit plan mode to run the interview for real.

## Guardrails

The behavioral rules are in [`AGENTS.md`](AGENTS.md) § Hard boundaries and § The one
rule — honor them, do not re-derive them here. Two Claude Code mechanics implement
them:

- The privacy guard above now **enforces** "never push the corpus" (AGENTS.md hard
  boundary) at commit time, so it no longer depends on remembering.
- When you propose a candidate principle/goal, write it to the target file as a
  `<!-- CANDIDATE - edit or delete -->` block, never as committed text. That is how
  AGENTS.md's "draft candidates, never author" rule looks in a file.

`your-life/.sensitive/` is off-limits (AGENTS.md): do not read or grep it, even if
asked to "search everything."
