---
name: adopt
description: Turn an existing body of notes (an Obsidian vault, a Notion export, journals, a docs folder) into a first corpus of candidates. Read-only over a source directory you name; drafts bounded principle, area, goal, project, and habit candidates through the kit templates, never copying your notes wholesale. Use once, if you arrive with years of notes instead of a blank your-life/.
---

Run the SpecSelf **adopt** pass: read a body of notes the human already has and
draft their first corpus as candidates, so someone arriving with years of notes
does not have to author a foundation from scratch. Synthesize in the
**Journalist** lens (`personas/journalist.md`). Honor `AGENTS.md`.

**Read first:** `AGENTS.md` (the one rule and the hard boundaries), then
`steering/` (methodology, privacy, tone), then the `templates/` you will write
into (`principle.md`, `aspirational.md`, `area.md`, `goal.md`, `project.md`,
`habit.md`).

Adopt does not interview. It reads what already exists and proposes candidates.
The stories behind a value rarely live in notes, so adopt is a head start, not a
replacement for the foundation sitting. Say so in the closing report.

## The contract (read this before touching anything)

- **The human names a source directory.** Ask for it, and ask for any paths
  inside it that are off-limits.
- **The source directory is READ-ONLY, always.** List, stat, and read its files.
  Never write, edit, move, rename, or delete anything inside it. It is not yours
  to change.
- **You write only into `your-life/`.** Every candidate artifact lands under
  `your-life/`, through the templates, as a `<!-- CANDIDATE - edit or delete -->`
  block. That is the one place adopt writes.
- **Never read `your-life/.sensitive/`** (a standing boundary), and never read
  any source path the human marked off-limits.
- **Never copy the notes wholesale.** Adopt drafts a bounded set of candidates
  with citations. It does not import a vault into `your-life/`.

## Steps

1. **Get the source and the off-limits list.** Ask the human for the source
   directory and for any files or subfolders within it that are private and must
   not be read. Record the off-limits list; you will name it in the report.

2. **Bound the sample.** Do not read the whole directory. Sample the **50 most
   recently modified files** plus any specific files the human names as worth
   reading. This keeps a giant vault from blowing the session. Skip anything
   under an off-limits path and skip `your-life/.sensitive/` entirely. If a file
   cannot be read (binary, encoding, permissions), skip it and note it for the
   report.

3. **Read read-only and gather evidence.** Read the sampled files. For each
   theme, role, outcome, or routine that recurs, note where it appears (the file
   path) and any date you can derive from the note content (a dated entry, a
   heading date, a logged event). A date written **in the note** is what lets a
   principle be `revealed`; a file's modified timestamp is provenance for the
   citation, not evidence of when something happened.

4. **Draft candidates through the templates.** Write each candidate into
   `your-life/` as a `<!-- CANDIDATE - edit or delete -->` block, hydrating the
   matching template, and cite its source in the block (the file path, plus a
   date where one is derivable from the content). Draft, in bounds:

   | Candidate | Template | Where it comes from | Bound |
   |---|---|---|---|
   | Revealed principles | `templates/principle.md` | recurring stances the notes show dated evidence for | 3-5 |
   | Aspirational entries | `templates/aspirational.md` | stances the notes state but do not back with a dated instance | 0-3 |
   | Areas | `templates/area.md` | standing roles the notes maintain (health, money, a craft, a relationship) | 2-5 |
   | Goals | `templates/goal.md` | finite outcomes the notes are working toward, each with a success criterion and a `serves:` link | 2-4 |
   | Projects | `templates/project.md` | concrete efforts the notes show in flight now | at most 3 |
   | Habits | `templates/habit.md` | routines the notes track or repeat | at most 3 |

   - **The bounds are ceilings, not quotas.** Fewer is fine. Drafting three thin
     principles to hit the floor flatters the human with volume and violates the
     `AGENTS.md` boundary against fabricated evidence. Draft only what the notes
     actually support.
   - **`revealed` requires a dated instance from the notes.** A principle
     candidate is `kind: revealed` only when you can cite at least one concrete,
     dated instance from the sampled notes under its `## Evidence` section.
     Without that, it is not revealed. Propose it for `aspirational.md` instead,
     with its promotion bar, or skip it. Never invent a date to clear the bar,
     and never collapse the gap between who the notes show the human to be and
     who they want to be.
   - **Do not draft a vision.** The five-year portrait is exactly what notes do
     not contain; leave it for the foundation sitting and name it in the report.

5. **Write the adopt report.** Close with a short report (in chat, not a corpus
   file) covering:
   - **Drawn from where.** Which candidates came from which files, so the human
     can trace every draft back to its source.
   - **Skipped and why.** What was left out and the reason: out of the sample
     (older than the 50 most recent, not named), marked off-limits, or unreadable.
   - **What the notes could not cover.** Which foundation phases have no material
     here. The vision and the lived stories behind the load-bearing values almost
     never live in notes, so those phases stay empty until the human does them.
   - **The recommendation.** Sitting 1 of `/foundation` (Operating System +
     Load-Bearing Values) is still worth running, because it captures exactly the
     decision-making and value stories the notes lack. Say this plainly.

## Placement

`/adopt` can run **before** `/foundation` (turn the notes into a starting draft,
then let the sittings deepen it), **after sitting 1** (keep the value stories from
sitting 1, let adopt fill areas, goals, and projects from the notes), or **instead
of sittings 2-4** (adopt covers the horizons that live in notes; you still want
sitting 1 for the stories). GETTING-STARTED carries this as its "Already have
notes?" section.

## Hard boundaries

- **The source directory is read-only.** No write, edit, move, rename, or delete
  inside it, ever. If a step seems to call for changing a source file, it is
  wrong; stop and re-read this section.
- **`your-life/.sensitive/` and off-limits paths are never read.**
- **No wholesale import.** Adopt drafts bounded candidates with citations; it
  never copies a vault into `your-life/`.
- **Never fabricate evidence** and never manufacture a date to promote a
  candidate to `revealed`.

## The never-authors rule

Write every proposed principle, area, goal, project, or habit as a
`<!-- CANDIDATE - edit or delete -->` block, never committed text. Each candidate
is something the human rewrites in their own words or discards; adopt surfaces and
drafts from the notes, the human edits and commits. Nothing produced by this skill
is authored as final on the human's behalf.
