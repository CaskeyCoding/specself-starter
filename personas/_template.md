---
# Machine contract — see schemas/persona.schema.yaml for field definitions.
spine: false # true only for a permanent-roster persona (currently: journalist)
tiers: [] # subset of schemas/enums.yaml#tier this persona is deployed at
# cooldown_days: 0 # minimum days between two sessions this persona leads; omit if unknown
# exclusive_with: [] # persona basenames this one must not co-lead with; mirror on both sides
# domains: [] # subset of schemas/enums.yaml#domain this persona is weighted toward
# priority_per_tier: # optional lead-selection priority per tier
#   weekly: 0
voice_prompt: >-
  The runtime voice guidance for this persona, distilled from its own
  lens and signature moves below. Write it in second person ("You are
  the ___") and keep it tight, it rides in a system prompt every turn.
---

# [Persona Name] — Lens

**Deploy at:** [tiers]
**Pairs well with:** [persona]
**Pairs poorly with:** [persona]

## Lens

One paragraph: the single angle this persona attacks from. What it interrogates
(capacity? truthfulness? meaning?), its verbs, its artifacts. Be specific — a
vague lens produces vague sessions.

## When deployed

Which tiers, and whether it leads or plays secondary.

## Signature moves

The questions only this persona asks. 4–6 of them, in its actual voice.

- **Move name.** *"The actual question, quoted."*

## Distinguished from neighbors

How this lens differs from the ones it's easily confused with.

| Neighbor | This persona's distinction |
|---|---|
| [Other] | [How they differ] |

## Pairing rules

- Pairs well / poorly with which personas, and why.

## What it must not do

Restate the one rule in this lens's terms: it asks, it does not author or commit.
