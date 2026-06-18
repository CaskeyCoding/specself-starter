# Privacy — Keeping Your Life Yours

This system holds some of the most personal writing you'll ever do. Its privacy
model is radically simpler than any hosted product because there is **no
backend**: your content is files on your machine. You hold every key by default.

## Where your content lives

Everything you write goes under `your-life/`. By default the kit's `.gitignore`
**commits the structure** (folders, READMEs) and **ignores the content**. This
means you can fork or publish the kit without leaking your corpus.

Two sensible setups:

1. **Private repo (recommended).** Keep your whole life OS in a *private* git
   repo. Delete the `your-life/**` ignore rules so your content is versioned —
   you get the full diffable history the method is built for. Because the repo is
   private, access control is the repo's; encryption at rest is your provider's.
2. **Local only.** Keep `your-life/` untracked entirely. No history, but nothing
   ever leaves the machine.

> **Access control and encryption are different protections.** A private repo
> stops outsiders from reading. It does *not* encrypt content from anyone who can
> read the repo or holds the keys. For most people, a private repo on a reputable
> host is the right balance. If you need more, keep the most sensitive material
> in `.sensitive/` (below) and out of any cloud.

## The `.sensitive/` escape hatch

`your-life/.sensitive/` is for material too raw even for a private repo. It is
**never committed** (hard-coded in `.gitignore`) and the agent is instructed
**never to read it**. Use it for the things you need to write to think clearly
but never want stored or surfaced. It is a one-way scratch pad.

## What the agent sees

Be clear-eyed: **your agent's provider sees whatever you put in the conversation.**
When you run a session, the principles and journal context the agent reads are
sent to that model's API. Choose a provider whose data policy you accept, and:

- Prefer providers/configurations that don't train on your inputs.
- Don't paste material from `.sensitive/` into a session.
- Remember the agent can read your files — scope each session to the tier's needs
  rather than dumping the whole corpus every time.

## What may and may not be committed

- **May:** your principles, goals, journal, reviews, decisions — in your private
  repo.
- **Be careful with:** other people. Use roles, not names, where you can ("my
  manager," not a full name) — it protects them and you, and it's enough for
  reflection. Never commit anyone else's secrets or anything under an NDA.
- **Never:** credentials, account secrets, anything `.sensitive/`, anything that
  would harm someone if the repo leaked.

## Signals (passive context)

If you connect passive signal (calendar exports, health stats, spend summaries)
under `your-life/signals/`, treat it as **read-only context** the agent uses to
ask better questions — never as content it authors principles from. Keep signal
minimal and prune it; old passive data at rest is liability, not insight.
