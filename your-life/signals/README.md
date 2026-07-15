# signals/ — Passive Context

Passive exports you connect for context: calendar exports, spend CSVs, health
and training exports, commit logs, time-tracking dumps. Anything that
describes what you did without you having written it.

## Read-only, never authored from

Signal is **context, never content** (`../../steering/cadence.md`). The
Forensic-Auditor persona reads it to ask sharper questions and flag a missing
trail; no session drafts a principle, journal entry, or anything else
directly from a signal file. Ingesting signal can run without you; deciding
what it means never does.

## Same privacy rules as the rest of the corpus

This is your content like everything else under `your-life/`: gitignored by
default, committed structure only. See
[`../../steering/privacy.md`](../../steering/privacy.md): keep signal
minimal and prune it, since old passive data at rest is liability, not
insight.

Note: the `.sensitive/` escape hatch is not a subfolder here. It lives at
`your-life/.sensitive/`, a sibling of this folder, not a child of it.
