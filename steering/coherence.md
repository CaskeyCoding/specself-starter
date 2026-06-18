# Coherence — The Vertical Alignment Check

**This is the core feature of the system, not a nicety.** No ordinary life tool
does it, because no tool had a reasoning agent reading the whole stack at once.
Yours does. On every weekly+ session, run this check and report the gaps as
**questions**, never as edits.

## What coherence means

The horizons stack is only valuable if the layers connect. Coherence is the
property that:

- every **project** ladders up to at least one **goal**,
- every **goal** serves the **vision** and respects the **principles**,
- every **area** has enough attention to hold its standard,
- and your **actions** this week actually moved the things you say matter.

Incoherence is the normal entropy of a life: you take on projects that serve
nothing, set goals that quietly betray a principle, and starve an area for a
month without noticing. The agent's job is to make that entropy *visible* so you
can decide what to do about it. **You** resolve it; the agent only surfaces it.

## The `serves:` links

Every non-ground artifact declares what it serves in frontmatter:

```yaml
# in a project file
serves: [goal:ship-side-business-v1]      # this project ladders up to a goal

# in a goal file
serves: [vision, principle:bias-to-shipping]   # this goal serves the vision + a principle
```

These links are the graph the check walks. An artifact with an empty `serves:`
is either a mistake or a deliberate orphan — flag it either way.

## The six checks

Run these in order. Each produces findings, never edits.

### 1. Orphan check (upward)
For every `active` **project**, is there a `serves:` link to an `active` goal?
For every `active` **goal**, does it serve the vision or a principle?

> *Finding:* "Project `redesign-portfolio` serves no active goal. Is it
> load-bearing, or is it a hobby that's crowding out goal work?"

### 2. Contradiction check
Does any `active` goal or project conflict with an `active` `revealed` principle?

> *Finding:* "Your goal `double-client-load` pushes against your principle
> `protect-deep-work-mornings`. Which gives?"

### 3. Starvation check (downward)
For each `area`, how much evidence/action did it get this period? Flag any area
with none.

> *Finding:* "`health` has had no journal evidence in 3 weeks while `work` has 14
> entries. Intentional season, or drift?"

### 4. Capacity check
Count `active` projects and goals against realistic bandwidth. Too many `active`
items is a coherence failure — nothing actually moves.

> *Finding:* "7 projects are `active`. Last week 5 of them saw zero movement.
> Which three are real right now?"

### 5. Staleness check (the pruning loop)
Any artifact past its cadence with no new evidence is a candidate for
`contested`. This is where breadth gets pruned back to what's alive.

> *Finding:* "Goal `learn-piano` has no evidence in 2 quarters. Recommend
> `contested`. Retire, revive, or re-scope?"

### 6. Revealed/aspirational drift
Has new evidence promoted an `aspirational` principle to `revealed` — or
contradicted a `revealed` one? Surface the candidate transition; never make it.

> *Finding:* "Three journal entries this month show you giving costly honest
> feedback. `give-feedback-i-d-want` (aspirational) may have earned `revealed`."

## Output format

Produce a short **coherence report**, not a wall of text:

```
Coherence — 2026-05-30 (weekly)

Orphans:       1  (project: redesign-portfolio → no goal)
Contradictions:1  (goal: double-client-load ✗ principle: protect-deep-work)
Starved areas: 1  (health — 0 evidence in 21d)
Over-capacity: yes (7 active projects, 5 stalled)
Stale:         1  (goal: learn-piano — recommend contested)
Drift:         1  (aspirational → revealed candidate: give-feedback-i-d-want)

Top question this week: You have 7 active projects and starved health for
3 weeks. What comes off the list?
```

End with **one** sharp question — the most important tension for them to resolve.
Don't dump all six findings as equally urgent; rank them.

## What you must not do

- Do not rewrite goals/projects/principles to "fix" coherence. Resolution is the
  human's act of will.
- Do not auto-flip statuses. Recommend, with the evidence, and wait.
- Do not treat every gap as a problem. A deliberately starved area during a known
  season (new baby, crunch) is a *choice*, not a failure. Ask before judging.
