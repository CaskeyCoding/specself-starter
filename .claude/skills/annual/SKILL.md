---
name: annual
description: Annual review (half day) — blank-slate rewrite of your principles FIRST, then diff against last year; retire what you can't re-derive. Supersedes the generic /review annual. Use for the annual tier.
---

Run the SpecSelf **annual** tier as **Future-Self + Biographer + Stoic**. Honor `AGENTS.md`.

**Read first:** `steering/cadence.md` (annual row), `steering/methodology.md`,
`steering/coherence.md`, `steering/tone.md`; personas `future-self.md`, `biographer.md`,
`stoic.md`.

1. **Blank-slate rewrite FIRST.** Re-derive the principles from scratch without looking
   at last year's set (Future-Self holds the long arc; Biographer holds the year's
   story).
2. **Then diff** against the prior set. What you cannot re-derive is a candidate for
   `retired`. The diff between this year and last is the year's real report.
3. Run the six-check coherence pass from `steering/coherence.md` across the rewritten
   stack; produce the ranked report. **Persist it:**
   `python scripts/coherence.py your-life --write your-life/reviews/coherence --tier annual`.
   Read the report's **Trend** section back into the wrap: a finding on a streak
   outranks a fresh one, so let the ONE question come from a streak when the trend
   shows one. The dated report is machine-derived and regenerable; never cite it as
   `Evidence` for a principle.
4. Hydrate `templates/review-annual.md` to `your-life/reviews/`.

Write the rewrite and retirements as `<!-- CANDIDATE - edit or delete -->` blocks;
recommend retirements with evidence, make none. The human authors the final set.
