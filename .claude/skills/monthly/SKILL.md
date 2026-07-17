---
name: monthly
description: Monthly deep review (~60 min) — synthesize candidate principles from the month's evidence, pressure borrowed ones, run a full-stack coherence pass. Supersedes the generic /review monthly. Use for the monthly tier.
---

Run the SpecSelf **monthly** tier as **Skeptic + Therapist**. Honor `AGENTS.md`.

**Read first:** `steering/cadence.md` (monthly row), `steering/methodology.md`,
`steering/coherence.md`, `steering/tone.md`; personas `skeptic.md` + `therapist.md`.

1. Synthesize the month's reviews and evidence into candidate principles. Pressure any
   that sound borrowed rather than lived (Skeptic); make room for what is hard to say
   (Therapist).
2. For each candidate principle: rate confidence and write a falsification criterion.
3. Run the full six-check coherence pass from `steering/coherence.md` across the whole
   stack; produce the ranked report. **Persist it:**
   `python scripts/coherence.py your-life --write your-life/reviews/coherence --tier monthly`.
   Read the report's **Trend** section back into the wrap: a finding on a streak
   outranks a fresh one, so let the ONE question come from a streak when the trend
   shows one. The dated report is machine-derived and regenerable; never cite it as
   `Evidence` for a principle.
4. Hydrate `templates/review-monthly.md` to `your-life/reviews/`.

Write candidates as `<!-- CANDIDATE - edit or delete -->` blocks. Promote nothing
without the human's sign-off; recommend transitions with evidence, make none.
