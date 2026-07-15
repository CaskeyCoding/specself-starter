# Methodology — The Model

How every artifact in the system is organized: the horizons stack, the two-axis
framework for principles, the status lifecycle, and the rules that keep the
corpus honest. This is the system itself, independent of any tool or schedule.

## The horizons stack

Six levels, top to ground. Each artifact type lives at one horizon and points
*up* (what it serves) and *down* (what serves it).

| Horizon | Artifact | Question it answers | Template |
|---|---|---|---|
| **H5 — Purpose & Principles** | `principle` | How do I act, and why? | `templates/principle.md` |
| **H4 — Vision** | `vision` | Who am I becoming over 3–5 years? | `templates/vision.md` |
| **H3 — Goals** | `goal` | What outcome am I committed to in 6–24 months? | `templates/goal.md` |
| **H2 — Areas** | `area` | What role/standard do I maintain indefinitely? | `templates/area.md` |
| **H1 — Projects** | `project` | What finite outcome am I driving now? | `templates/project.md` |
| **Ground — Actions** | journal / review | What did I do, intend, learn today/this week? | `templates/journal-entry.md`, `review-*.md` |

Supporting (cross-horizon): `habit` (recurring commitment), `decision` (life-ADR),
`evidence` (raw material for reflection), `signal` (passive context, read-only).

Every non-ground artifact carries a `serves:` frontmatter field naming the
higher-horizon artifact(s) it ladders up to. That field is what makes the
[coherence check](coherence.md) possible. An artifact that serves nothing is
either a mistake or a missing link — the agent flags it. References are
`type:slug` and resolve to a file basename (see `templates/README.md`).

## The two-axis framework (principles)

Principles — the top horizon — are positioned on two orthogonal axes.

### Kind axis — revealed vs aspirational

- **revealed** — a rule backed by evidence of how you have *actually behaved*
  under pressure. Extracted from journal entries, sessions, or observed signal.
- **aspirational** — a rule you *want* to live by but can't yet demonstrate.
  Inherited or chosen, not yet tested.

**The gap between the two sets is the most useful signal this system produces.**
Never collapse an aspirational principle into the revealed set without evidence;
doing so launders a wish into a fact and defeats the project. The axis lives in
the `kind:` frontmatter field. Aspirational principles collect in the singleton
`your-life/aspirational.md` (scaffold: `templates/aspirational.md`) until
evidence graduates them into their own file under `principles/<domain>/`.

### Domain axis

`core | work | relationships | health | money | integrity | learning`

Canonical values live in `schemas/enums.yaml#domain`; this section explains the axis, the schema is the machine-readable source.

These seven are sensible defaults, **not law** — edit them in your own corpus to
fit your life. `core` is reserved for cross-domain principles. Keep `core`
small (a cap of ~10 is a good forcing function): if you can't name your handful
of load-bearing principles, you haven't found them yet. Recorded in `domain:`.

## Status lifecycle

Most artifacts share a four-state lifecycle. The agent may *recommend* a
transition with evidence; **you** make it.

```
draft ──► active ──► contested ──► retired
              ▲           │
              └───────────┘  (review clears the challenge)
```

| Status | Meaning |
|---|---|
| `draft` | Captured, not yet committed to |
| `active` | Currently lived / being pursued; reviewed on cadence |
| `contested` | Evidence has emerged that challenges it; pending falsification |
| `retired` | Replaced or falsified; kept in the corpus for the audit trail |

All types share this base cycle. Goal adds one terminal state, **`met`** (the
success criteria were satisfied). Project adds **`shipped`** and
**`abandoned`**. Habit replaces `contested` with **`lapsed`**: the lapse
itself is the challenging evidence, so there's no separate contested state to
pass through. Decisions keep their own vocabulary, `proposed | accepted |
superseded`, mirroring software ADRs rather than this lifecycle. Every
terminal transition (`met`, `shipped`, `abandoned`, `retired`, `superseded`)
is dated in the `ended_on:` field. The full per-type enum table lives in
`templates/README.md`.

## Falsification is required

Every principle and every goal must state **what evidence would force its
retirement or failure**. A principle you can't falsify is a slogan; a goal you
can't fail is a mood. This single requirement does most of the work of keeping
the corpus honest, because it forces specificity:

- Not "I value health" but "I train 3×/week; two consecutive months under that
  marks this `contested`."
- Not "honesty" but "I give the version of feedback I'd want if roles were
  reversed, even when it costs me — falsified if I go quiet to keep the peace
  twice in a quarter."

## Supersession, not deletion

When a new artifact replaces an old one, the old one moves to `retired` and lists
the replacement; the new one lists `supersedes:`. Nothing is deleted. You should
be able to reconstruct how your thinking changed and why. Pair significant
revisions with a `decision/` life-ADR.
