# Changelog

All notable changes to the **SpecSelf Starter** kit's *structure* — `templates/`,
`steering/`, `personas/`, `.claude/`, and the top-level docs. This is the file a
fork reads to upgrade (see [`UPGRADING.md`](UPGRADING.md)). It tracks the **kit**,
never anyone's `your-life/` corpus.

The format follows [Keep a Changelog](https://keepachangelog.com/); versions are
[SemVer](https://semver.org/) for the structure contract:

- **major** — a breaking change to the artifact contract or directory layout a fork
  must hand-migrate (e.g. a template frontmatter field renamed or removed).
- **minor** — additive, backward-compatible: a new skill, persona, template, or
  steering doc; an existing one improved without breaking the contract.
- **patch** — wording, typos, formatting; no behavior change.

A fork upgrades by pulling **structure** changes here that it wants; its corpus is
never affected.

## [Unreleased]

*Nothing yet.*

## [0.2.1] — 2026-07-15

### Added

- `scripts/coherence.py`: stdlib-only runnable coherence report implementing the
  mechanical checks from `steering/coherence.md` (orphan, starvation, capacity,
  staleness, revealed/aspirational drift) over a `your-life/` or `examples/`
  corpus, with a `--today` flag for reproducible runs. The contradiction check
  is deliberately deferred to persona review; it has no mechanical rule, and the
  script says so rather than inventing one. `steering/coherence.md` gained a
  one-line pointer to the script.

## [0.2.0] — 2026-07-15

The response to the 2026-07-15 external deep review (ADR-008 in the parent
specs repo), plus the app/kit seam alignment (ADR-009). While the kit is
pre-1.0, a breaking structure change bumps the minor version; the breaking
items are flagged below.

### Added

- `templates/README.md`: the schema doc. The file basename is the id; `serves:`
  references are `type:slug`; per-type status enums; life-ADR numbering.
- `templates/aspirational.md`: the scaffold for the `your-life/aspirational.md`
  singleton (principle-shaped entries, promotion bar, graduation log).
- `schemas/` (`enums.yaml`, `principle.schema.yaml`, `persona.schema.yaml`):
  machine-readable single source for enums and artifact/persona contracts.
- `scripts/validate.py`: stdlib-only corpus validator (required fields, enum
  membership, `serves:` resolution, revealed-principle evidence, goal success
  criteria, `ended_on` on terminal states). Opt-in pre-commit hook included,
  commented out.
- `scripts/overdue.sh` + `scripts/overdue.ps1`: the SessionStart nudge now
  computes per-tier overdue from review filenames and stays silent when
  everything is current.
- `scripts/set-privacy-mode.sh`: mechanical public/private switching for the
  `.gitignore` corpus block and the `.specself-allow-corpus` marker;
  `your-life/.sensitive/` stays blocked in both modes (the commit guard now
  refuses it unconditionally).
- `LICENSE` (MIT) ships with the kit instead of being authored at extraction.
- READMEs for `your-life/signals/`, `decisions/`, `reflections/` (+ `domains/`,
  `evidence/`), documenting the ADR numbering convention and the signals
  read-only rule.
- Example corpus extended to every artifact type: aspirational singleton, a
  habit, two journal entries, a monthly review, a life-ADR; it doubles as the
  validator fixture.
- Journal entries gained an optional `## Captures` section: `/capture` appends
  timestamped jots there; `/daily` fills the day-close sections once.

### Changed

- **Breaking (major):** template frontmatter normalized to the schema doc. The
  `id:` field is dropped everywhere (the filename is the id), `title:` is a
  free-text display title, and goal's `met_on:` is replaced by the uniform
  `ended_on:`. A fork migrates by renaming `met_on:` and deleting `id:` lines.
- Status enums standardized per type; `project` gains `contested`/`retired`,
  `area` and `vision` gain `contested`.
- The nine `.claude/agents/` subagents are slimmed to the template shape: the
  persona file is the single source of truth, and every agent reads all of
  `steering/` (no more per-agent drift).
- The Stoic leads a quarterly goal audit (cut-two test, borrowed ambition);
  Biographer and Forensic-Auditor are finished lenses, sketch footers dropped.
- The annual blank-slate-first protocol is stated in the agent-neutral layer
  (`steering/cadence.md`, `personas/future-self.md`), not only in a subagent.
- `/coherence-check` documents that its standalone report is ephemeral by
  design; the persisted trail is the weekly+ review's coherence section.
- `/daily` asks three rotating prompts from a shared pool aligned with the
  hosted app (ADR-009 seam).

## [0.1.0] — 2026-06-30

The first tagged structure baseline — the kit as it stands after the launch epic
(SS-0 … SS-15). Everything below is the structure a fork inherits and can later
upgrade.

### Added

- The agent-neutral contract (`AGENTS.md`) and the horizons method in `steering/`
  (philosophy, methodology, cadence, coherence, privacy, tone).
- One `templates/` file per artifact (principle, evidence, goal, vision, area,
  project, habit, decision, journal-entry, and the four review tiers).
- The `personas/` lenses and their `.claude/agents/` subagents.
- The cadence sessions as `.claude/skills/` (`foundation`, `daily`, `weekly`,
  `monthly`, `quarterly`, `annual`) plus the `capture` / `coherence-check` helpers.
- The deterministic privacy guard (`.claude/hooks/guard-corpus-commit.sh`) wired as
  a Claude Code `PreToolUse` hook and a `pre-commit` fallback (SS-9).
- A clearly-fictional worked corpus under `examples/` so a forker sees the system
  alive before their first session (SS-14).
- **This upgrade path: `CHANGELOG.md`, `UPGRADING.md`, and the `upgrade` skill** that
  diffs a fork's structure against upstream and proposes updates, never touching
  `your-life/` corpus (SS-15).

[Unreleased]: about:blank
[0.2.0]: about:blank
[0.1.0]: about:blank
