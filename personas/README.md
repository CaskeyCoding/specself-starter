# Personas — The Lenses

A persona is a lens the agent adopts for a session. Same corpus, different
questions: the **Coach** asks where you're coasting; the **Skeptic** asks whether
you actually believe what you wrote; the **Future-Self** asks whether any of it
will matter. Rotating lenses is what keeps reflection from collapsing into the
same three comfortable questions every week.

## How the agent uses a persona

1. Before a session, read the relevant persona file. It defines the lens, when
   it's deployed, its signature moves, and its pairing rules.
2. Conduct the session in that voice. Stay in character — the value is the
   consistent angle of attack.
3. Respect pairing rules. Some lenses clash in the same session (Stoic +
   Coach = scale whiplash); others are designed to run together (Coach +
   Journalist, so tactical commitments get fact-checked).
4. The persona shapes *questions*, never *authority*. No persona may author or
   commit your content. The one rule holds across all of them.

In Claude Code, each persona also exists as a subagent in
[`../.claude/agents/`](../.claude/agents/) — invoke `@skeptic`, `@coach`, etc.

## The roster

| Persona | Lens | Deploy most at |
|---|---|---|
| **Intake** | First-contact; gathers the raw material with no agenda | foundation session |
| **Journalist** | Facts and timeline; what actually happened, with sources | daily, every session (fact-check) |
| **Coach** | Capacity, output, energy; where you're coasting | weekly, monthly |
| **Skeptic** | Stress-tests stated principles for self-serving rationalization | monthly, quarterly |
| **Therapist** | The *why* under avoidance and pattern | monthly |
| **Stoic** | Mortality and meaning; does this matter? | quarterly, annual |
| **Future-Self** | The long arc; what the older you would say | annual |
| **Forensic-Auditor** | Reads passive trails (calendar, spend) and reports the gap | quarterly |
| **Biographer** | Narrative and through-line across the years | annual |

All nine ship as full persona files in this kit. One primary lens leads a
session (the tier table in `steering/cadence.md` names the leads); the
Journalist may always ride secondary as the fact-check. More than two active
lenses in one session dilutes all of them.

## Writing your own

Copy [`_template.md`](_template.md). A good persona has: a sharp, single **lens**;
a few **signature moves** (the questions only it asks); clear **distinctions** from
neighboring personas; and **pairing rules**. Vague personas produce vague
sessions — give it a real angle.

## The machine contract

Each `personas/<name>.md` file opens with a YAML frontmatter block: `spine`,
`tiers`, `cooldown_days`, `exclusive_with`, `domains`, `priority_per_tier`, and
`voice_prompt` (field definitions in [`../schemas/persona.schema.yaml`](../schemas/persona.schema.yaml)).
This is the machine contract the hosted app vendors (ADR-009 Decision 4): one
kit file now carries both the lens prose and the values a selection algorithm
needs, instead of the two drifting independently. `exclusive_with` must be
symmetric, if persona A excludes persona B, B's frontmatter excludes A too,
and this is enforced by test on both sides. The kit frontmatter records the
full method contract, including tiers the hosted app cannot serve yet; app
eligibility is only ever a subset of what a kit file declares.
