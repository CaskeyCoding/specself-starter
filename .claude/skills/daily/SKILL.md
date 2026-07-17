---
name: daily
description: Close the day (~2 min) in the Journalist lens, reflect yesterday's intent vs reality, ask today's three rotating prompts, write a dated journal entry. Use for the daily tier.
---

Run the SpecSelf **daily** tier in the **Journalist** lens. Honor `AGENTS.md`.

**Read first:** `steering/cadence.md` (daily row) and `steering/tone.md`; persona
`personas/journalist.md`; `templates/daily-prompts.yaml` (the prompt pool).

1. Reflect yesterday's entry back: did intent match what happened? Fact, not judgment.
2. If today's entry already has a `## Captures` section, read its jots as raw
   material for this close, don't rewrite them.
3. Pick today's three prompts from `templates/daily-prompts.yaml` using its
   documented deterministic date-window rule, keyed to the user's local
   calendar date (the same rule the app uses, so kit and app users in the
   same timezone get the same prompts on the same day). Ask them one at a
   time, plus one line on what would make tomorrow count.
4. Write to `your-life/journal/<today>.md` via `templates/journal-entry.md`
   (create if absent, append if present), filling the `## Responses` list once
   with the three prompt/answer pairs.
5. ~2 minutes. No synthesis, that is for weekly+. End by noting if a weekly review is
   overdue.

Capture only: do not interpret or propose principles here. Nothing is committed that
the human did not write.
