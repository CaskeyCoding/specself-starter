# decisions/ — Life-ADRs

Real forks in your life, captured the way a software ADR captures one in a
system: what you chose, what you rejected, and why. Hydrate every entry from
[`../../templates/decision.md`](../../templates/decision.md).

## Numbering

Sequential, zero-padded to three digits, **global** across your whole corpus
(not per domain): the next number is max + 1. Filename
`ADR-NNN-kebab-title.md`. Other artifacts reference a decision as
`decision:ADR-NNN` (see [`../../templates/README.md`](../../templates/README.md)).

## Status

`proposed | accepted | superseded`. A decision is never edited after
acceptance, it is superseded: the old file moves to `superseded` and lists
`superseded_by:`, the new one lists `supersedes:`. Nothing is deleted.

## When to write one

Pair any significant principle or goal revision with a life-ADR
(`../../steering/methodology.md`, Supersession section). Not every change
needs one, a real fork does.
