# Upgrading your fork

You forked SpecSelf Starter, then made it yours — you tuned templates and steering
to taste, and you filled `your-life/` with your corpus. Later, upstream ships
improvements: a sharper template, a new skill, a better steering doc. This is how
you pull those **structure** improvements **without losing your edits and without
ever touching your corpus**.

## The one guarantee

**`your-life/` is never upgraded.** It is yours — not compared, not proposed, not
written, ever. The upgrade only ever touches the kit's *structure*: `templates/`,
`steering/`, `personas/`, `.claude/`, and the top-level docs. Your principles,
journal, goals, and reviews are out of scope by construction (the
[`upgrade-diff` script](.claude/skills/upgrade/upgrade-diff.sh) hard-excludes
`your-life/`, and the privacy guard would block a commit that included it anyway).

## One-time setup

Point your fork at the starter as a remote named `upstream`:

```bash
git remote add upstream <the-starter-repo-url>
git fetch upstream
```

## Run the upgrade

In Claude Code, invoke the **`/upgrade`** skill — it reads `CHANGELOG.md` for the
*why*, runs the diff, and proposes each change for you to accept or skip (it applies
nothing on its own). Or run the diff yourself:

```bash
git fetch upstream
bash .claude/skills/upgrade/upgrade-diff.sh upstream/main
```

It is a **dry run**: it writes nothing. It shows only what changed in the structure,
then prints the commands to apply each file *you* choose. Read
[`CHANGELOG.md`](CHANGELOG.md) alongside it so each change has a reason.

## Worked dry-run (a fixture fork)

A fixture fork that diverged — the forker dropped the `Tensions` section from
`templates/principle.md` and has private corpus in `your-life/` — run against an
upstream that added the `upgrade` skill and improved `steering/philosophy.md` and the
`weekly` skill:

```text
$ bash .claude/skills/upgrade/upgrade-diff.sh upstream/main
SpecSelf upgrade — structure diff vs upstream/main
(your-life/ corpus is never compared or touched)

 .claude/skills/upgrade/SKILL.md | 1 +
 .claude/skills/weekly/SKILL.md  | 2 +-
 steering/philosophy.md          | 2 +-
 templates/principle.md          | 2 +-
 4 files changed, 4 insertions(+), 3 deletions(-)

Upstream changed these structure files (your edits win where you diverged):
  .claude/skills/upgrade/SKILL.md
  .claude/skills/weekly/SKILL.md
  steering/philosophy.md
  templates/principle.md

DRY RUN — nothing was written. Apply selectively, one file at a time:
  git checkout upstream/main -- <path>     # take upstream's version of one file
  git difftool upstream/main -- <path>     # or merge by hand, keeping your edits

Then bump your local note of the version you're on (see CHANGELOG.md).
```

Notice what is **not** in that list: the fork's `your-life/principles/honesty.md`
corpus. It is never compared, even though it lives right there in the fork.

## Deciding per file

- **A skill/persona/steering doc you never touched** → `git checkout upstream/main --
  <path>`: just take upstream's version.
- **A template or doc you edited to taste** (like `templates/principle.md` above) →
  `git difftool upstream/main -- <path>` and merge by hand. **Your edits win**; fold
  in the upstream improvement you actually want.
- **A change you don't want** → skip it. Divergence is allowed; the kit is a starting
  point, not a dependency.

After applying, note which `CHANGELOG.md` version you're now on (a line in your own
notes, or your fork's own changelog) so the next upgrade starts from the right place.

## What this deliberately is NOT

Not an auto-merge and not a package manager. There is no lockfile and no forced
update — a life OS you can't diverge from would defeat the point. The kit gives you a
**safe, corpus-free, dry-run-first** way to cherry-pick upstream improvements, and
leaves every decision with you. See `steering/privacy.md` and `AGENTS.md` § the one
rule.
