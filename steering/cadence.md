# Cadence — The Review Loop

Five reflection tiers, from daily to annual. Each consumes specific inputs and
produces specific artifacts. The cadence is what keeps the system alive: it
forces falsification, drives the [coherence check](coherence.md), and runs the
pruning loop that stops breadth from becoming bloat.

## Schedule reminders, not reflection

The governing rule: **the system reminds you to reflect; it never reflects on
your behalf.** Anything that runs without you — ingest, hydration, coverage
computation — produces *context*, never *content*.

| Allowed without you | Forbidden without you |
|---|---|
| Ingesting passive signal as context | Authoring journal entries or principles |
| Hydrating a session template with prompts | Deciding a goal is met or a project done |
| Computing coverage / coherence gaps | Marking anything `contested` / `retired` |
| Surfacing that a tier is overdue | Resolving a contradiction a review exists to find |

## The tiers

| Tier | Frequency | Duration | Consumes | Produces | Lead personas |
|---|---|---|---|---|---|
| **Daily** | daily | ~2 min | yesterday's actions, today's intent | one journal entry | Journalist |
| **Weekly** | weekly | ~20 min | the week's entries | weekly review + candidate updates | Journalist + Coach |
| **Monthly** | monthly | ~60 min | the month's reviews & evidence | candidate principles/goals, coherence pass | Skeptic, Therapist, rotating |
| **Quarterly** | quarterly | ~90 min | the quarter's artifacts | falsification sweep, status transitions | Skeptic, Forensic-Auditor |
| **Annual** | yearly | half day | the year's corpus | blank-slate rewrite, retirements | Future-Self, Biographer |

## What each tier does

### Daily (~2 min)
Capture, don't analyze. One decision you made, one friction you hit, one
surprise. Fixed template, no persona pressure. This is the raw material
everything else is synthesized from. Use `/capture` any time; `/daily` to close
the day.

### Weekly (~20 min)
Cluster the week's entries by theme. The agent (as Coach + Journalist) asks where
execution matched intent, audits the calendar against stated priorities, and runs
a **coherence check**: which area got starved, which project didn't move, which
goal saw no action. Output: a weekly review and clearly-labeled *candidate*
updates you accept or reject.

### Monthly (~60 min)
Synthesis. The agent surfaces candidate principles from the month's evidence and
pushes back on borrowed-sounding ones (Skeptic). Rate confidence, write
falsification criteria. Re-check coherence across the full stack. Promote
nothing without your sign-off.

### Quarterly (~90 min)
Falsification sweep across all `active` principles and goals. Any artifact with
no new supporting evidence this quarter is auto-flagged `contested` (a
recommendation — you confirm). Transition statuses. This is the primary pruning
tier.

### Annual (half day)
Blank-slate rewrite. Re-derive your principles from scratch without looking at
last year's; *then* diff against the prior set. What you can't re-derive gets
retired. The agent (as Future-Self + Biographer) holds the long arc. The diff
between this year and last is the year's real report.

## Overdue handling

The agent surfaces overdue tiers at session start (the Claude Code SessionStart
hook automates the nudge). Missing a tier is data, not failure — note it in the
next session: a skipped weekly for a month is itself a signal about the period.
