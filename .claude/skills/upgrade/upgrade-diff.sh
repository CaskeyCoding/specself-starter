#!/usr/bin/env bash
# SpecSelf kit upgrade diff — STRUCTURE ONLY, read-only (SS-15).
#
# Shows what upstream changed in the kit's *structure* (templates/, steering/,
# personas/, .claude/, and the top-level docs) versus your fork — so you can pull
# template and skill improvements after you've diverged, WITHOUT ever touching
# your private `your-life/` corpus. This script never reads, diffs, proposes, or
# writes anything under `your-life/`; it is a dry run that writes nothing at all.
#
# Usage:  bash .claude/skills/upgrade/upgrade-diff.sh [UPSTREAM_REF]
#   UPSTREAM_REF defaults to "upstream/main". Set up the remote once:
#     git remote add upstream <the-starter-repo-url>
#     git fetch upstream
set -euo pipefail

UPSTREAM="${1:-upstream/main}"

# The committed structure the kit ships and upgrades. `your-life/` is DELIBERATELY
# absent: your corpus is never compared, proposed, or touched.
STRUCTURE=(
  templates steering personas .claude
  AGENTS.md CLAUDE.md GETTING-STARTED.md README.md
  CHANGELOG.md UPGRADING.md EXTRACTION.md examples
)

# Hard guard: never let `your-life` enter the path set, even by a future edit.
for p in "${STRUCTURE[@]}"; do
  case "$p" in
    your-life | your-life/*)
      echo "refusing: your-life is your corpus, not kit structure — never upgraded." >&2
      exit 2
      ;;
  esac
done

if ! git rev-parse --verify --quiet "${UPSTREAM}" >/dev/null; then
  echo "Can't find '${UPSTREAM}'. Add the starter as a remote and fetch it:" >&2
  echo "  git remote add upstream <the-starter-repo-url> && git fetch upstream" >&2
  exit 1
fi

echo "SpecSelf upgrade — structure diff vs ${UPSTREAM}"
echo "(your-life/ corpus is never compared or touched)"
echo

changed="$(git diff --name-only HEAD "${UPSTREAM}" -- "${STRUCTURE[@]}")"
if [ -z "${changed}" ]; then
  echo "Up to date: no upstream structure changes since your fork. Nothing to do."
  exit 0
fi

git diff --stat HEAD "${UPSTREAM}" -- "${STRUCTURE[@]}"
echo
echo "Upstream changed these structure files (your edits win where you diverged):"
echo "${changed}" | sed 's/^/  /'
echo
echo "DRY RUN — nothing was written. Apply selectively, one file at a time:"
echo "  git checkout ${UPSTREAM} -- <path>     # take upstream's version of one file"
echo "  git difftool ${UPSTREAM} -- <path>     # or merge by hand, keeping your edits"
echo
echo "Then bump your local note of the version you're on (see CHANGELOG.md)."
