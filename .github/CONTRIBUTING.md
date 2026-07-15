# Contributing to SpecSelf Starter

Thanks for looking at this. A few things before you open an issue or a PR.

## What contributions target

This repo is a template. Contributions here should improve the **structure**:
`templates/`, `steering/`, `personas/`, `.claude/`, the top-level docs
(`AGENTS.md`, `GETTING-STARTED.md`, `CHANGELOG.md`, `UPGRADING.md`), and any
tooling that ships to every fork.

Contributions should **never** target `your-life/` content. That directory is
gitignored by design and holds each user's private corpus (their principles,
goals, journal). A PR that adds sample content, "fixes" someone's life data,
or otherwise touches `your-life/` outside the empty `.gitkeep` scaffolding
is out of scope. If you want a worked example, look at `examples/` (clearly
labeled fictional data), not `your-life/`.

## Good contributions

- A template that's missing a field real usage needs.
- A steering doc that's ambiguous or contradicts another steering doc.
- A persona that behaves inconsistently with its own file.
- A `.claude/` skill or hook bug.
- Docs fixes: broken links, stale instructions, typos.

## Before you open a PR

1. Keep the change scoped to the structure, not to any one person's use of it.
2. If you're adding a new template or skill, follow the shape of an existing
   one in the same directory.
3. Don't commit anything that looks like real personal data, even as an
   example. Fabricated example content belongs under `examples/`, clearly
   marked as fiction.

## After you fork

Once you use this template (or clone it), this repo's whole `.github/`
directory (this file, the issue templates, the PR template) is inherited
into your fork. They're aimed at contributions back to the shared template,
not at your private life OS. If they don't make sense for a personal,
single-user fork, delete them. Nothing else in the kit depends on
`.github/` being present.
