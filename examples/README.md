# Examples — A Worked Corpus (Fiction)

> **FICTIONAL EXAMPLE — not a real person, not real corpus.** Everything under
> `examples/` is an invented persona ("Sam Rivers") used to show the SpecSelf
> system alive before your first session. Nothing here is real data about anyone.
> Passes the kit's privacy gate (ADR-002): zero real corpus, fiction labeled as
> fiction. Delete this whole directory whenever you like — your own life lives in
> `your-life/`, never here.

## Why this is here

The templates in `templates/` show you the *shape* of each artifact. This shows you
the *system* — one small life, worked top of the stack down, with the layers
actually connected so you can see the **coherence check** do its job. Read it once,
then build your own under `your-life/` (which the privacy guard keeps private).

## The persona

**Sam Rivers** — a fictional indie game developer, ~18 months into going solo,
trying to ship a first *paid* game without polishing it to death. Small on purpose,
but now covers **every artifact type** the templates define: one vision, one
aspirational entry, one principle (with its evidence), one goal, one project, one
area, one habit, two journal entries, one decision, and both a weekly and a monthly
review, connected, not just individually valid. This corpus doubles as
`scripts/validate.py`'s fixture (see `templates/README.md` § Validating), so every
file here also has to pass the schema check, not just read well.

## The corpus, top of the stack down (H5 → H1 → reviews)

| Horizon | File | Serves |
|---|---|---|
| H5 principle | [`sam-rivers/principles/work/ship-before-its-ready.md`](sam-rivers/principles/work/ship-before-its-ready.md) | — (top of stack) |
| evidence | [`sam-rivers/reflections/evidence/2026-02-15-jam-game-shipped.md`](sam-rivers/reflections/evidence/2026-02-15-jam-game-shipped.md) | backs the principle |
| aspirational | [`sam-rivers/aspirational.md`](sam-rivers/aspirational.md) | (the not-yet-evidenced counterpart to `revealed`) |
| H4 vision | [`sam-rivers/vision.md`](sam-rivers/vision.md) | — |
| H3 goal | [`sam-rivers/goals/launch-paid-game-v1.md`](sam-rivers/goals/launch-paid-game-v1.md) | vision + the principle |
| decision | [`sam-rivers/decisions/ADR-001-launch-paid-not-free.md`](sam-rivers/decisions/ADR-001-launch-paid-not-free.md) | reaffirms the goal's paid model |
| H2 area | [`sam-rivers/areas/health.md`](sam-rivers/areas/health.md) | a standard to hold |
| H1 project | [`sam-rivers/projects/build-demo-and-wishlist-page.md`](sam-rivers/projects/build-demo-and-wishlist-page.md) | the goal |
| habit | [`sam-rivers/habits/playtest-fridays.md`](sam-rivers/habits/playtest-fridays.md) | the principle |
| journal | [`sam-rivers/journal/2026-02-24.md`](sam-rivers/journal/2026-02-24.md), [`sam-rivers/journal/2026-02-26.md`](sam-rivers/journal/2026-02-26.md) | raw evidence feeding the weekly review below |
| review (weekly) | [`sam-rivers/reviews/2026-W09-weekly.md`](sam-rivers/reviews/2026-W09-weekly.md) | runs the six coherence checks over the above |
| review (monthly) | [`sam-rivers/reviews/2026-02-monthly.md`](sam-rivers/reviews/2026-02-monthly.md) | synthesizes the month, including the weekly above |

## What to notice

- **The ladder connects.** The project `serves:` the goal, the goal `serves:` the
  vision *and* the principle. The weekly **coherence check** walks exactly those
  `serves:` links (see `steering/coherence.md`).
- **A real finding.** The weekly review honestly flags the `health` area as
  **starved** (zero evidence that week) — surfaced as a *question*, never an edit.
  That is the whole point of the system: make the entropy visible; you decide.
- **Revealed vs aspirational.** The one principle is `revealed` because it has dated
  evidence behind it. A value you *want* but can't back with a story would be
  `aspirational` — the kit keeps the two honestly separate. The aspirational entry
  here was surfaced *by* the weekly review's starvation finding, then held to a
  promotion bar the monthly review checks and declines to clear: you can trace a
  candidate from a coherence finding, to a draft, to a synthesis pass that says
  "not yet," in the files themselves.
- **The bottom of the stack feeds the top.** The two journal entries land inside the
  same week the weekly review summarizes, and their skipped runs are the raw material
  the review's health-starvation finding is built from. The habit's evidence log runs
  on its own weekly cadence alongside the same week.
