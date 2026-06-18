# .claude/ — Claude Code Accelerators

Optional conveniences for [Claude Code](https://claude.com/claude-code). None of
this is required — the kit works with any agent via [`../AGENTS.md`](../AGENTS.md).
These just make the loop faster in Claude Code.

```
.claude/
├── agents/         Persona subagents — invoke a lens with @coach, @skeptic, …
├── commands/       Slash commands — /capture /daily /weekly /review /coherence-check
└── settings.json   SessionStart hook that nudges overdue review tiers
```

## Personas as subagents

Each file in `agents/` is a thin subagent that loads the matching
[`../personas/`](../personas/) file plus `../steering/` and runs a session through
that lens. All nine lenses ship as subagents (coach, skeptic, journalist,
future-self, intake, therapist, stoic, biographer, forensic-auditor) — the mapping
is 1:1 with `personas/`. To add your own, copy `agents/_template.md` and point it
at a new `personas/` file; keep the body thin so the persona file stays the single
source of truth.

## Slash commands

Each file in `commands/` is a tier entry point. They load the right steering +
persona + template and run the session. See `CLAUDE.md` for the table.

## The hook

`settings.json` runs a SessionStart hook that prints which review tiers look
overdue, based on the newest dated files in `your-life/reviews/`. It only nudges —
it never writes a review. Edit or remove it freely; it's illustrative, and the
date logic is intentionally simple so you can adapt it to your setup.
