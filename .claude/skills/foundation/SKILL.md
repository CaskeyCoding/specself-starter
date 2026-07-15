---
name: foundation
description: Run ONCE at setup. The ~60-90 min foundation session that builds your initial stack top-down (principles, vision, areas, goals, projects) from your own stories. Use when starting from a near-empty your-life/.
---

Run the SpecSelf **foundation** session: a 20-question interview, then a synthesis
pass that maps the answers into the five passes from `GETTING-STARTED.md`, top of
the stack down. Interview in the **Intake** lens, synthesize in the **Journalist**
lens (`personas/intake.md`, `personas/journalist.md`). Honor `AGENTS.md`.

**Read first:** `AGENTS.md` (the one rule), then `steering/` (methodology, cadence,
privacy, tone). Then check `your-life/`: this session is for a near-empty corpus; if
a full stack already exists, prefer `annual` (a re-derivation), not this.

## Stage 1: the interview

Read `personas/intake/foundation-questions.yaml`, the canonical 20-question bank
(same source the app runs, vendored per ADR-009 Decision 2). Ask **one question at
a time, in the fixed order given**, seven phases, never skipped or reordered.
Draft nothing yet; this stage only gathers.

**The thin-answer probe rule.** After each answer, judge it against that
question's `thin_signal` field: does the answer name a specific moment, person (by
role), choice, or cost, or does it stay abstract ("it depends"), outsource to
circumstance ("my team," "the market"), or restate the question? If the answer
matches the `thin_signal` pattern, probe **once** with one of the question's
`follow_ups` (pick the one that best fits what they said), then move to the next
question regardless of what comes back. Never probe twice on the same question,
and never skip the probe when `thin_signal` clearly fires. Keep a private mental
(or scratch) record per question: the answer, whether it was thin, and the probe
answer if one was asked. That record is what stage 2 reads.

## Stage 2: synthesis

Once all 20 are answered, synthesize conversationally in the Journalist lens.
Each phase's answers feed specific outputs; work through this mapping:

| Phase | Answers feed |
|---|---|
| 1 Operating System | principle evidence (decision-making rules), vision texture |
| 2 Load-Bearing Values | principle evidence (inconvenient stances and their costs), falsification material |
| 3 Life Chapters | vision draft (trajectory arc), evidence dates for principles |
| 4 Domain Audit | area candidates (standards, slippage tells), goal candidates for unresolved domains |
| 5 Failure Modes | falsification clauses, area slippage tells, habit candidates |
| 6 Energy and Operating Conditions | area standards, drop candidates (momentum commitments invert to DROP), habit candidates |
| 7 Trajectory | vision draft, goal candidates (6-24 month outcomes), aspirational entries |

Rules for the synthesis (the same contract the hosted app's foundation
synthesis follows):

1. **Principles (H5), revealed first.** A candidate `revealed` principle must
   cite at least one concrete story from phases 1, 2, or 5, naming the
   `question_id`s it draws on. State it as an actionable rule ("when X, I do Y,
   even when it costs Z"). A stated value with no story behind it is never a
   `revealed` candidate; it belongs in `your-life/aspirational.md`, tagged
   `aspirational`. Protect that gap. Bound: 3-5 principle candidates, 0-3
   aspirational entries. If a candidate rests only on a thin answer with no probe
   answer, mark it low confidence and say so. Hydrate `templates/principle.md`.
2. **Vision (H4).** Draw the present-tense portrait from the Life Chapters and
   Trajectory answers: "Where is this person in five years if the principles
   hold and the work compounds?" One page, concrete, not a resume. Exactly one
   vision draft. Hydrate `templates/vision.md` to `your-life/vision.md`.
3. **Areas (H2).** From Domain Audit and Energy: the standing roles they
   maintain indefinitely. For each, the standard ("what good looks like") and
   how they'd know it is slipping. Bound: 2-5 areas. Hydrate `templates/area.md`
   to `your-life/areas/`.
4. **Goals (H3).** From the unresolved domains named in Domain Audit and the
   Trajectory answers: finite outcomes for 6-24 months, each with a falsifiable
   success criterion (a date and a measure) and a `serves:` link up to the
   vision or a principle. Question any goal that serves nothing above it.
   Bound: 2-4 goals. Hydrate `templates/goal.md`.
5. **Projects (H1) and first habits.** From Failure Modes and Energy: what they
   are driving right now that ladders up to those goals, plus habits worth
   tracking. Bound: at most 3 projects, at most 3 habits. **The INT-EO-003
   answer (the momentum-only commitment) is a DROP candidate, not a project to
   add**, list it in the capacity section below, never as new work. Hydrate
   `templates/project.md` and `templates/habit.md`.

Fewer candidates than the bound is fine; the bound exists to stop the synthesis
from flattering the human with volume, not to fill a quota.

## Close, first coherence pass

Run the six checks from `steering/coherence.md` against what was just drafted
(does every project serve a goal, does every goal serve the vision or a
principle, is any area already starved, are there too many active projects to
actually move). Include the DROP list from INT-EO-003 in the capacity read.
End with the ONE sharpest question the synthesis found; tell them to carry it to
their first weekly review, not resolve it tonight.

## The never-authors rule

Write every proposed principle, goal, vision, area, project, or habit as a
`<!-- CANDIDATE - edit or delete -->` block, never committed text. Every
candidate is something the human rewrites in their own words or discards; the
agent surfaces and drafts, the human edits and commits. Nothing produced by this
skill is authored as final on the human's behalf.
