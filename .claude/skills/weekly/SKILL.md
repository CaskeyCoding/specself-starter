---
name: weekly
description: Weekly review (~20 min) — cluster the week, run the six-check coherence pass, surface candidate updates, write the weekly review. Use for the weekly tier.
---

Run the SpecSelf **weekly** tier as **Coach + Journalist**. Honor `AGENTS.md`.

**Read first:** `steering/cadence.md` (weekly row), `steering/coherence.md`,
`steering/methodology.md`, `steering/tone.md`; personas `coach.md` + `journalist.md`.

1. **Facts (Journalist).** Read this week's `your-life/journal/` entries; build the
   timeline.
2. **Execution vs intent (Coach).** Where the week matched stated priorities; which
   project moved, which did not. Fact-check commitments.
3. **Coherence check.** Run all six checks from `steering/coherence.md` against
   `your-life/` (orphans, contradictions, starved areas, over-capacity, staleness,
   drift) and produce the compact **ranked** coherence report, not a flat dump.
   **Persist it** so this week remembers the last one:
   `python scripts/coherence.py your-life --write your-life/reviews/coherence --tier weekly`.
   Read the written report's **Trend** section back into the wrap: a finding on a
   streak ("starved: area:health, 3rd consecutive report") outranks a fresh one, so
   let the ONE question come from a streak when the trend shows one. The dated report
   is machine-derived and regenerable; never cite it as `Evidence` for a principle.
4. **Candidates.** Surface candidate principles/habits/edits. Write each into its
   target file as a `<!-- CANDIDATE - edit or delete -->` block, clearly labeled, never
   committed.
5. Hydrate `templates/review-weekly.md` to `your-life/reviews/<YYYY-Www>.md`.
6. End with the ONE sharpest question and ask for next week's short commitments.

Recommend status transitions with their evidence; make none. The human confirms each.
