# .claude/skills/ — Cadence sessions

The SpecSelf cadence sessions, as Claude Code skills. Per the SS-6 design and
the determinism test, the cadence sessions are **skills** (fixed multi-step +
light judgment); the personas are subagents (`../agents/`); corpus protection
is a hook (`../settings.json` + a pre-commit fallback, SS-9).

| Skill | Tier | Lead lens |
|---|---|---|
| `foundation` | once, in 3-4 short sittings across week one (or one long session) | Intake / Journalist |
| `adopt` | once, if you arrive with existing notes | Journalist |
| `daily` | daily (~2 min) | Journalist |
| `weekly` | weekly (~20 min) | Coach + Journalist |
| `monthly` | monthly (~60 min) | Skeptic + Therapist |
| `quarterly` | quarterly (~90 min) | Skeptic + Forensic-Auditor |
| `annual` | yearly (half day) | Future-Self + Biographer + Stoic |

Every skill:

- reads `steering/` first (it never inlines a rule — `AGENTS.md` and `steering/` are
  the single source of truth);
- hydrates the matching `templates/` file;
- runs the six-check coherence pass from `steering/coherence.md` on weekly+ (and the
  `foundation` close);
- writes candidates as `<!-- CANDIDATE - edit or delete -->` blocks and never promotes
  them. The human authors and commits.

Delete `.claude/` entirely and the system still runs from `AGENTS.md` — these are
accelerators, never dependencies.

## The `upgrade` skill (kit maintenance, not a cadence tier)

`upgrade` (SS-15) is different in kind: it maintains the **fork itself**, not the
human's life. It diffs the kit's *structure* (`templates/`, `steering/`, `personas/`,
`.claude/`, top-level docs) against upstream and proposes updates, so a diverged fork
can pull improvements — **never** comparing or touching `your-life/` corpus. It pairs
the deterministic [`upgrade/upgrade-diff.sh`](upgrade/upgrade-diff.sh) (a dry-run diff
that hard-excludes corpus) with the judgment to rank and explain each change. See
[`../../UPGRADING.md`](../../UPGRADING.md) and [`../../CHANGELOG.md`](../../CHANGELOG.md).

> **Transitional note.** The older `../commands/{daily,weekly,review}.md` slash commands
> still exist and overlap these skills. SS-10 (the Fable-first CLAUDE.md pass) is where
> CLAUDE.md is reconciled and the duplicate commands are retired. `capture` and
> `coherence-check` remain slash commands (any-time helpers); the weekly+ skills run the
> coherence check inline.
