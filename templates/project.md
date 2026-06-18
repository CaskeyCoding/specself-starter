---
id:
title:                      # kebab-case-slug
status: active              # draft | active | shipped | abandoned | contested
horizon: weeks-months
serves: []                  # goal:<id> and/or area:<id> this project ladders up to
created: YYYY-MM-DD
target_date: YYYY-MM-DD
last_moved: YYYY-MM-DD       # date of last real progress — feeds the staleness check
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
