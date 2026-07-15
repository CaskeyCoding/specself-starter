---
title:                      # display title, free text (the filename is the id)
status: active              # draft | active | contested | met | retired
horizon: 6-24mo
serves: [vision]            # type:slug refs this advances (see templates/README.md)
created: YYYY-MM-DD
target_date: YYYY-MM-DD
last_reviewed: YYYY-MM-DD
ended_on:                   # set with a date when status enters a terminal state
---

# [Goal title — the outcome, not the activity]

State the outcome you're committed to, not the tasks. "Ship v1 of the side
business with 10 paying customers" — not "work on the side business."

## Success criteria (falsifiable)

A measure and a date. You must be able to look at this on `target_date` and say
plainly whether it was met or failed. Vague criteria mean a goal you can't fail,
which is a mood, not a goal.

- [ ] Measurable criterion, by `target_date`.

## Failure criteria

What would mark this `contested` before the target date — the early signal that
it's drifting or was wrong. (e.g., "no paying customer by month 6.")

## Why this serves the vision

The explicit link up. If you can't articulate how this goal serves the vision or
a principle, question whether it belongs.

## Projects under this goal

The H1 projects that ladder up to this goal (the agent maintains these `serves:`
links from the project side).
