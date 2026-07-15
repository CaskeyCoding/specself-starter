---
name: upgrade
description: Pull SpecSelf kit STRUCTURE improvements (templates, steering, personas, .claude) from upstream after your fork has diverged — proposing each change, never touching your-life/ corpus. Use when the starter has shipped updates you want.
---

Run a **structure-only** upgrade of this SpecSelf fork against the upstream
starter. Honor `AGENTS.md` and the one rule: you **propose**, the human decides
and applies. **Never** read, diff, propose, or write anything under `your-life/` —
that is the human's corpus, not kit structure (`steering/privacy.md`).

**Read first:** `UPGRADING.md` (the full flow + the dry-run example), `CHANGELOG.md`
(what changed upstream), `steering/privacy.md` (why corpus is out of scope).

## Steps

1. **Confirm the upstream remote.** Check `git remote -v` for an `upstream`. If it's
   missing, tell the human the one-time setup and stop until they run it:
   `git remote add upstream <starter-url> && git fetch upstream`. Otherwise
   `git fetch upstream` to refresh.
2. **Diff structure only.** Run the bundled script — it is the deterministic, corpus-safe
   diff (it hard-excludes `your-life/`):
   `bash .claude/skills/upgrade/upgrade-diff.sh upstream/main`
   Do not hand-roll a `git diff` that could include `your-life/`; use the script.
3. **Read CHANGELOG.md** for the upstream releases between the human's version and
   `upstream/main`, so each file change has a *why*, not just a diff.
4. **Propose, ranked.** For each changed structure file, present: what changed, why
   (from CHANGELOG), and whether the human likely diverged on it (their edits should
   win). Rank by value: new/renamed skills and steering fixes first, cosmetic last.
   Recommend one of `take upstream` / `merge by hand` / `skip — you diverged here`.
5. **Apply only what the human accepts**, one file at a time, with the commands the
   script prints (`git checkout upstream/main -- <path>` or a hand-merge). Make no
   change they did not confirm. Touch nothing under `your-life/`.
6. **Record the upgrade.** After applying, suggest the human note which CHANGELOG
   version they're now on (a line in their own notes or a fork CHANGELOG entry).

## Hard boundaries

- `your-life/**` is **out of scope, always** — not compared, not proposed, not
  written. The script enforces this; you reinforce it.
- Never force-overwrite a diverged file. Where the human edited a template or steering
  doc to taste, default to `merge by hand` and keep their intent.
- This skill writes nothing on its own. Every apply is a human-confirmed command.
