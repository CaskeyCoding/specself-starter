---
name: foundation
description: Run ONCE at setup. Builds your initial stack top-down (principles, vision, areas, goals, projects) from your own stories. Default flow is three or four short sittings across week one, each ending with real drafts; one long session stays available. Use when starting from a near-empty your-life/.
---

Run the SpecSelf **foundation** session: the same 20-question interview
(`personas/intake/foundation-questions.yaml`, seven phases), staged so every
sitting ends with visible output instead of asking for a single long block up
front. Interview in the **Intake** lens, synthesize in the **Journalist** lens
(`personas/intake.md`, `personas/journalist.md`). Honor `AGENTS.md`.

**Read first:** `AGENTS.md` (the one rule), then `steering/` (methodology,
cadence, privacy, tone). Then check `your-life/`: this session is for a
near-empty corpus; if a full stack already exists, prefer `annual` (a
re-derivation), not this.

## Default flow: four short sittings across week one

The 20 questions split into four sittings on the phase boundaries. Each sitting
runs 15-20 minutes, interviews its phases, then drafts that sitting's candidate
outputs before you stop. This is the default because a first honest draft you
actually finish beats a 90-minute session you bounce off of.

| Sitting | Phases (questions) | Time | Ends with |
|---|---|---|---|
| 1 | 1 Operating System + 2 Load-Bearing Values (6 q) | 15-20 min | 1-3 candidate revealed principles drafted; tomorrow's `/daily` wired |
| 2 | 3 Life Chapters + 4 Domain Audit (6 q) | ~20 min | vision draft + area candidates |
| 3 | 5 Failure Modes + 6 Energy (6 q) | ~20 min | falsification clauses, habit candidates, the DROP list |
| 4 | 7 Trajectory (2 q) + synthesis wrap | ~15 min | goal candidates + the assembled foundation outputs |

The candidates each sitting draws from its phases are the phase-to-output
mapping in `projects/specself-starter/feature/foundation-synthesis/requirements.md`,
mirrored in the reference table near the bottom of this file. Some outputs cross
sitting boundaries on purpose (a principle drafted in sitting 1 gets its
mandatory falsifier in sitting 3); each sitting below says what to carry
forward.

**One-sitting path stays.** If the human says they want to run all four passes
now, do that: work sittings 1 through 4 back to back in one session, still
drafting each sitting's output as you reach it, and finish with the full close.
The sitting plan is the default, not a cap.

## Resume state

The session records progress in `your-life/reflections/foundation-progress.md`
(corpus territory, so gitignored with everything else; it is not a validated
artifact, just a dated checklist you read and update in prose). It is the only
state that carries between sittings.

**On every invocation, before asking anything:**

1. Read `your-life/reflections/foundation-progress.md` if it exists.
2. If it exists and shows incomplete phases, say which sittings are done and
   resume at the next unanswered phase. Do not re-ask completed phases.
3. If every phase is complete, say so and point at the drafted candidates for
   review (do not restart the interview silently). Foundation runs once; from
   here the human edits the candidates and moves into the weekly loop.
4. If the file is absent, this is sitting 1: create it after the first sitting.

The file is a plain markdown checklist. Keep this shape:

```markdown
# Foundation progress

Started: <YYYY-MM-DD>

## Sitting 1, Operating System + Load-Bearing Values (phases 1-2)
- Completed: <YYYY-MM-DD>
- Questions answered: INT-OS-001, INT-OS-002, INT-OS-003, INT-LV-001, INT-LV-002, INT-LV-003
- Candidates drafted: your-life/principles/<domain>/<slug>.md, ...
- Next: sitting 2 (Life Chapters + Domain Audit)

## Sitting 2, Life Chapters + Domain Audit (phases 3-4)
- Not yet run
```

At the end of each sitting, append or update that sitting's block with the date,
the `question_id`s answered, and the candidate file paths drafted, then note the
next sitting. Never overwrite an earlier sitting's record.

## Running a sitting

For every sitting, the interview mechanics are identical:

- Ask **one question at a time, in the fixed order** from
  `personas/intake/foundation-questions.yaml`, only the phases that belong to
  this sitting. Never skip or reorder.
- Apply **the thin-answer probe rule** (below) to each answer.
- Keep a per-question record (answer, whether it was thin, the probe answer if
  asked). That record is what the sitting's synthesis reads.

Then draft that sitting's outputs, state what the next sitting covers, and update
the progress file.

### Sitting 1, Operating System + Load-Bearing Values (phases 1-2)

Interview INT-OS-001..003 and INT-LV-001..003. Then draft **1-3 candidate
revealed principles** in the Journalist lens, hydrating `templates/principle.md`
into `your-life/principles/<domain>/`.

- A `revealed` candidate must cite at least one concrete story from these phases
  as its Evidence, naming the `question_id`s. State it as an actionable rule
  ("when X, I do Y, even when it costs Z").
- A stated value with no story behind it is never a `revealed` candidate; it
  goes to `your-life/aspirational.md`, tagged `aspirational`. Protect that gap.
- The principle template's falsification section is mandatory (ADR-009 Decision
  3), but its raw material is phase 5, which arrives in sitting 3. Draft each
  principle with a placeholder falsification note ("falsifier to be set in
  sitting 3 from the failure-mode answers") rather than inventing one now, and
  record these candidates in the progress file so sitting 3 can find them.
- Bound: 1-3 principle candidates here (the full run reaches 3-5 across the
  failure-mode evidence too); 0-3 aspirational entries. If a candidate rests
  only on a thin answer with no probe answer, mark it low confidence and say so.

Close sitting 1 by **wiring tomorrow's `/daily`**: tell the human their first
daily entry is tomorrow, that `/daily` takes about two minutes, and that the
week's dailies become evidence later sittings can cite. Then say sitting 2
(Life Chapters + Domain Audit) drafts their vision and area candidates.

### Sitting 2, Life Chapters + Domain Audit (phases 3-4)

Interview INT-LC-001..003 and INT-DA-001..003. Then draft:

- **A vision draft** (H4) from the Life Chapters answers, present-tense, one
  page, concrete, not a resume: "Where is this person in five years if the
  principles hold and the work compounds?" Hydrate `templates/vision.md` to
  `your-life/vision.md`. This is a first pass; sitting 4 tightens it with the
  Trajectory answers, so mark it as a draft to revisit.
- **Area candidates** (H2) from the Domain Audit: the standing roles the human
  maintains indefinitely, each with a standard ("what good looks like") and a
  slippage tell. Hydrate `templates/area.md` to `your-life/areas/`. Bound: 2-5
  areas. Their slippage tells and standards get sharpened in sitting 3 from the
  failure-mode and energy answers, so leave room.

Close by saying sitting 3 (Failure Modes + Energy) sets the falsifiers on the
sitting-1 principles and surfaces habits and the drop list.

### Sitting 3, Failure Modes + Energy (phases 5-6)

Interview INT-FM-001..003 and INT-EO-001..003. Then:

- **Set the falsification clauses.** Revisit the candidate principles drafted in
  sitting 1 (find them via the progress file) and fill each one's mandatory
  falsification section from these failure-mode answers: the human's own named
  failure pattern is usually the falsifier ("this principle is false if
  <failure mode> shows up in <context> again"). Do not draft fresh principles in
  isolation here; complete the existing ones. If the failure-mode evidence
  supports a new revealed principle, you may add it (staying within the 3-5
  total bound), with its falsifier set now.
- **Sharpen the areas.** Add slippage tells (from Failure Modes) and best-work
  standards (from Energy) to the sitting-2 area candidates.
- **Habit candidates.** From Failure Modes and Energy, the counter-patterns
  worth tracking. Hydrate `templates/habit.md`. Bound: at most 3 habits.
- **The DROP list.** The INT-EO-003 answer (a commitment honored out of
  momentum, not choice) is a candidate to DROP, not a project to add. Record it
  for the capacity read in sitting 4's close; never draft it as new work.

Close by saying sitting 4 (Trajectory + wrap) drafts the goals, adds any
projects, completes the vision, and runs the first coherence check.

### Sitting 4, Trajectory + synthesis wrap (phase 7)

Interview INT-TR-001..002. Then assemble the foundation:

- **Goal candidates** (H3) from the unresolved domains named in the Domain Audit
  (sitting 2) and the Trajectory answers: finite outcomes for 6-24 months, each
  with a falsifiable success criterion (a date and a measure) and a `serves:`
  link up to the vision or a principle. Question any goal that serves nothing
  above it. Hydrate `templates/goal.md`. Bound: 2-4 goals.
- **Project candidates** (H1) from Failure Modes and Energy: what the human is
  driving right now that ladders up to those goals. Hydrate
  `templates/project.md`. Bound: at most 3 projects.
- **Complete the vision** with the Trajectory answers: tighten the sitting-2
  draft so the five-year portrait reflects the shot the human named.
- **Aspirational entries** for the Trajectory wants with no backing story.

Then run the close below.

## Close: first coherence pass

At the end of sitting 4 (or the single session), run the six checks from
`steering/coherence.md` against everything drafted: does every project serve a
goal, does every goal serve the vision or a principle, is any area already
starved, are there too many active projects to actually move. Include the DROP
list from INT-EO-003 in the capacity read. End with the ONE sharpest question
the synthesis found; tell the human to carry it to their first weekly review
(day 7), not resolve it tonight. Mark every phase complete in the progress file.

## The thin-answer probe rule

After each answer, judge it against that question's `thin_signal` field: does the
answer name a specific moment, person (by role), choice, or cost, or does it stay
abstract ("it depends"), outsource to circumstance ("my team," "the market"), or
restate the question? If the answer matches the `thin_signal` pattern, probe
**once** with one of the question's `follow_ups` (pick the one that best fits
what they said), then move to the next question regardless of what comes back.
Never probe twice on the same question, and never skip the probe when
`thin_signal` clearly fires. When a candidate later rests only on a thin answer
with no probe answer, mark it low confidence and flag it as resting on a
deflected question.

## The phase-to-output mapping (reference)

The full mapping each sitting draws from (canonical source:
`projects/specself-starter/feature/foundation-synthesis/requirements.md`):

| Phase | Answers feed |
|---|---|
| 1 Operating System | principle evidence (decision-making rules), vision texture |
| 2 Load-Bearing Values | principle evidence (inconvenient stances and their costs), falsification material |
| 3 Life Chapters | vision draft (trajectory arc), evidence dates for principles |
| 4 Domain Audit | area candidates (standards, slippage tells), goal candidates for unresolved domains |
| 5 Failure Modes | falsification clauses, area slippage tells, habit candidates |
| 6 Energy and Operating Conditions | area standards, drop candidates (momentum commitments invert to DROP), habit candidates |
| 7 Trajectory | vision draft, goal candidates (6-24 month outcomes), aspirational entries |

Bounds across the whole foundation, not per sitting: 3-5 revealed principle
candidates, 0-3 aspirational entries, exactly 1 vision, 2-5 areas, 2-4 goals, at
most 3 projects and 3 habits. Fewer than the bound is fine; the bound exists to
stop the synthesis from flattering the human with volume, not to fill a quota.

## The never-authors rule

Write every proposed principle, goal, vision, area, project, or habit as a
`<!-- CANDIDATE - edit or delete -->` block, never committed text. Every
candidate is something the human rewrites in their own words or discards; the
agent surfaces and drafts, the human edits and commits. Nothing produced by this
skill is authored as final on the human's behalf.
