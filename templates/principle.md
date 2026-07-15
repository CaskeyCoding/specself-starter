---
title:                      # display title, free text (the filename is the id)
status: draft               # draft | active | contested | retired
kind: revealed              # revealed (evidence-backed) | aspirational (not yet lived)
domain: core                # core | work | relationships | health | money | integrity | learning
confidence: medium          # low | medium | high
serves: []                  # type:slug refs this supports (see templates/README.md); usually empty — H5 is the top
created: YYYY-MM-DD
last_reviewed: YYYY-MM-DD
ended_on:                   # set with a date when status enters a terminal state
supersedes: []              # type:slug refs to principles this replaces (see templates/README.md)
---

Field definitions and enum values are canonical in `schemas/principle.schema.yaml` and `schemas/enums.yaml`; this template does not restate them.

# [The principle as one actionable sentence]

State it as a rule you can follow and fail, not a category. Good: "When someone
asks my opinion on their work, I give the version I'd want if roles were reversed,
even when it costs me." Bad: "Honesty."

## Why

What this principle protects or produces. Why it earns a place in your life.

## Evidence

Concrete, dated instances of you actually living (or failing) this. For a
`revealed` principle this section must be real — not plausible-sounding. For
`aspirational`, note that evidence is still missing.

- YYYY-MM-DD — what happened.

## Falsification

The specific evidence that would force this to `contested` or `retired`. If you
can't name it, this isn't a principle yet — it's a slogan.

## Tensions

Which other principles this can collide with, and how you tend to resolve the
collision under pressure.
