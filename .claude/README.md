# .claude/ — Claude Code Accelerators

Optional conveniences for [Claude Code](https://claude.com/claude-code). None of
this is required — the kit works with any agent via [`../AGENTS.md`](../AGENTS.md).
These just make the loop faster in Claude Code.

```
.claude/
├── agents/         Persona subagents — invoke a lens with @coach, @skeptic, …
├── skills/         Cadence sessions — /foundation /daily /weekly /monthly /quarterly /annual
├── commands/       Any-time helpers — /capture /coherence-check
├── hooks/          Privacy guard (corpus-leak + secrets) for git commit/push
└── settings.json   SessionStart nudge + PreToolUse privacy guard
```

## Personas as subagents

Each file in `agents/` is a thin subagent that loads the matching
[`../personas/`](../personas/) file plus `../steering/` and runs a session through
that lens. All nine lenses ship as subagents (coach, skeptic, journalist,
future-self, intake, therapist, stoic, biographer, forensic-auditor) — the mapping
is 1:1 with `personas/`. To add your own, copy `agents/_template.md` and point it
at a new `personas/` file; keep the body thin so the persona file stays the single
source of truth.

## Skills and commands

The cadence sessions are skills in `skills/` (`/foundation`, `/daily`, `/weekly`,
`/monthly`, `/quarterly`, `/annual`); `commands/` holds the two any-time helpers
(`/capture`, `/coherence-check`). Each loads the right steering + persona +
template and runs the session. See `CLAUDE.md` for the table.

## The hooks

`settings.json` runs a SessionStart hook (`../scripts/overdue.sh`, which computes
per-tier overdue from `your-life/reviews/` filenames and prints one line per
overdue tier — silent when everything is current, and it only prints, never writes
a review) and a `PreToolUse` privacy guard that blocks any `git commit`/`git push`
of `your-life/` corpus or secrets. The guard also runs without Claude via the
`pre-commit` fallback; see `GETTING-STARTED.md`. Edit or remove either freely.

### Windows

The SessionStart hook above (`../scripts/overdue.sh`) and `../bundle-context.sh`
are POSIX shell, so they need Git Bash or WSL on Windows. `../scripts/overdue.ps1`
is the native PowerShell twin of the overdue check, for running it by hand, and
`../bundle-context.ps1` is the native PowerShell twin of the bundler; neither
needs Git Bash or WSL.
