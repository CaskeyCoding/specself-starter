# your-life/ — Your Content

Everything under this folder is **yours**. By default the kit's `.gitignore`
commits this structure (folders + READMEs) but ignores the content you write, so
you can fork the kit publicly without leaking your corpus. If you keep your life
OS in a *private* repo and want full history, delete the `your-life/**` rules from
the root `.gitignore`. See [`../steering/privacy.md`](../steering/privacy.md).

Don't hand-build files from scratch — run [`../GETTING-STARTED.md`](../GETTING-STARTED.md)
and let your agent seed these with you, using the matching `../templates/`.

## The map

| Folder | Horizon | Holds | Template |
|---|---|---|---|
| `principles/` + `aspirational.md` | H5 | how you act, and who you want to be | `principle.md` |
| `vision.md` | H4 | who you're becoming (3–5 yr) | `vision.md` |
| `goals/` | H3 | outcomes with success criteria (6–24 mo) | `goal.md` |
| `areas/` | H2 | standing roles & standards | `area.md` |
| `projects/` | H1 | finite outcomes you're driving now | `project.md` |
| `habits/` | cross | recurring commitments | `habit.md` |
| `journal/` | ground | dated raw capture (`YYYY-MM-DD.md`) | `journal-entry.md` |
| `reviews/` | ground | weekly/monthly/quarterly/annual reviews | `review-*.md` |
| `reflections/domains/` | — | periodic per-domain synthesis | — |
| `reflections/evidence/` | — | the six evidence types | `evidence.md` |
| `decisions/` | — | life-ADRs (`ADR-NNN-*.md`) | `decision.md` |
| `signals/` | — | optional passive context (read-only) | — |

## The two single files

`vision.md` and `aspirational.md` live at the top of this folder (one each). Your
agent creates them during the foundation session. `aspirational.md` is where
who-you-want-to-be writing lives, kept deliberately separate from the
evidence-backed `revealed` principles — protecting that gap is the point.

## The escape hatch

`your-life/.sensitive/` (create it if you want it) is never committed and the
agent is instructed never to read it. Use it for material too raw even for a
private repo.
