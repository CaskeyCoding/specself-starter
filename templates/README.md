# Templates — The Schema

Every artifact in `your-life/` is hydrated from one of these templates. This
file is the schema they share: what identifies an artifact, what `serves:`
references point at, which statuses each type can hold, and when dates get set.
The coherence check and any validator run against these rules.

## Identity: the basename is the id

The file's basename (minus `.md`) is the artifact's identifier and slug, in
kebab-case. There is no `id:` frontmatter field. `title:` is the human-readable
display title, free text.

| Artifact | Lives at | Identified by |
|---|---|---|
| principle | `your-life/principles/<domain>/<slug>.md` | basename |
| aspirational entries | `your-life/aspirational.md` (singleton) | `aspirational` |
| vision | `your-life/vision.md` (singleton) | `vision` |
| goal | `your-life/goals/<slug>.md` | basename |
| area | `your-life/areas/<slug>.md` | basename |
| project | `your-life/projects/<slug>.md` | basename |
| habit | `your-life/habits/<slug>.md` | basename |
| decision | `your-life/decisions/ADR-NNN-<slug>.md` | `ADR-NNN` |
| evidence | `your-life/reflections/evidence/<date>-<slug>.md` | basename |
| journal entry | `your-life/journal/<YYYY-MM-DD>.md` | `date:` |
| review | `your-life/reviews/<period>.md` | `period:` |

## References: `serves:` uses `type:slug`

Every non-ground artifact declares what it ladders up to:

```yaml
serves: [goal:double-client-load]          # -> your-life/goals/double-client-load.md
serves: [vision, principle:bias-to-shipping]   # singletons are referenced bare
supersedes: [decision:ADR-003]             # decisions by their ADR number
```

A reference that resolves to no file is a broken link; the coherence check
flags it and a validator fails on it.

## Status: one base lifecycle, explicit terminals

The shared lifecycle is `draft -> active -> contested -> retired` (contested
can clear back to active). Per-type enums:

| Type | Statuses |
|---|---|
| principle, area, vision | `draft \| active \| contested \| retired` |
| goal | `draft \| active \| contested \| met \| retired` |
| project | `draft \| active \| contested \| shipped \| abandoned \| retired` |
| habit | `draft \| active \| lapsed \| retired` |
| decision | `proposed \| accepted \| superseded` |
| evidence, journal, reviews | none (immutable records) |

Notes:

- **Terminal states** are `met`, `shipped`, `abandoned`, `retired`, and
  `superseded`. Where steering says "retire," read "move to the type's
  terminal state."
- A habit's `lapsed` plays the contested role: the lapse itself is the
  challenging evidence. A lapsed habit either restarts (back to `active`) or
  gets retired honestly.
- Decisions deliberately keep their own vocabulary (mirroring software ADRs):
  a decision is never "active," it is accepted until superseded.

## Dates: every terminal transition is dated

Every status-bearing template carries `ended_on:` — set it to the date the
artifact enters any terminal state (the `status:` value says which one). The
audit trail is the point: the diff between years cannot be reconstructed from
undated transitions. Alongside it:

- `created:` — when the artifact was first committed.
- `last_reviewed:` — touched at every session that examined it; the staleness
  check reads this.
- `last_moved:` (projects only) — date of last real progress, which is not the
  same as last reviewed.

## Numbering: life-ADRs

Decisions are numbered sequentially and zero-padded to three digits, globally
(not per domain): the next ADR is max + 1. Filename `ADR-NNN-kebab-title.md`.

## Validating

`scripts/validate.py` (stdlib only) checks a corpus against every rule on this
page: required frontmatter per type, status enum membership, `serves:` /
`supersedes:` / `related:` refs that resolve, a `kind: revealed` principle
carrying dated evidence, a goal carrying a success-criteria checkbox, and
`ended_on` set if and only if the status is terminal. Run it from
`specself-starter/`:

```bash
python scripts/validate.py                              # your-life/, the default
python scripts/validate.py --corpus examples/sam-rivers  # the worked example
```

Errors exit 1, one line each. Warnings (empty `serves:` on a goal/project/
habit, a `last_reviewed` older than 90 days) print but exit 0. A clean run
prints a one-line OK summary with the file count.
