---
title:                      # display title, free text (the filename is the id)
status: active              # draft | active | contested | shipped | abandoned | retired
horizon: weeks-months
serves: []                  # type:slug refs this ladders up to (see templates/README.md)
created: YYYY-MM-DD
target_date: YYYY-MM-DD
last_reviewed: YYYY-MM-DD
last_moved: YYYY-MM-DD       # date of last real progress — feeds the staleness check
ended_on:                   # set with a date when status enters a terminal state
---

# [Project title — the finite outcome]

A concrete outcome with a finish line. If it can't be finished, it's an area
(H2), not a project.

## Definition of done

The specific, checkable condition that means this project is `shipped`.

- [ ] Done when…

## Why it serves [goal/area]

The explicit link up. A project that serves no active goal or area is an orphan —
the coherence check will flag it. Either connect it or question it.

## Next action

The single next physical action. Keep exactly one. If you can't name it, the
project is stalled — say so.

## Log

Dated progress notes. Update `last_moved` in frontmatter when real work happens —
this is what the staleness check reads.

- YYYY-MM-DD — what moved.
