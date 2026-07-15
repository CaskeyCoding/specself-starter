---
title: Playtest Fridays
status: active
cadence: weekly
serves: [principle:ship-before-its-ready]
created: 2026-02-06
last_reviewed: 2026-02-28
ended_on:
---

> **FICTIONAL EXAMPLE:** not a real person, not real corpus. Part of the `examples/`
> worked corpus (persona: Sam Rivers). See [`examples/README.md`](../../README.md).

# Playtest Fridays: put the latest build in front of a stranger every week

Every Friday, whatever is playable goes in front of someone who isn't me and hasn't
seen it that week. Not "a build exists somewhere," but a stranger's hands on it, the
same week it changed.

## Why it serves principle:ship-before-its-ready

The principle is about shipping rough and letting players teach me; a weekly cadence
is what keeps that from being a one-time act of courage at launch. If the only
exposure to real players is the eventual store release, the principle is aspirational
talk. This habit is the rehearsal.

## What counts

A person outside my own head plays the current build (or the current tutorial
segment, if that's all that's ready) for at least five minutes, and I write down one
concrete moment they hit that I didn't expect. Watching a friend nod along on a call
does not count (it has to be someone who can get stuck without me coaching them
through it).

## Lapse signal

Two consecutive Fridays with nothing playable in front of a stranger moves this to
`lapsed`. One missed Friday because the build was genuinely broken is a rep lost, not
a pattern yet.

## Evidence

- 2026-02-13: kept. Two people from the local dev-meetup Discord played the vertical
  slice; both got stuck on the same jump I'd never noticed was ambiguous.
- 2026-02-20: missed. A touch-input regression broke the build Thursday night; there
  was nothing playable by Friday.
- 2026-02-27: kept. Ran the tutorial past three strangers at the meetup. All three
  took twice as long as intended to reach the first real choice, confirming what the
  project log already suspected: the tutorial is too long.
