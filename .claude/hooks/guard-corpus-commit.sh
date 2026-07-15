#!/usr/bin/env bash
# SpecSelf privacy guard — deterministic corpus-leak + secrets protection.
#
# Refuses to commit (a) private your-life/ corpus content or (b) secret-shaped
# strings. It checks file PATHS directly, NOT git's ignore status, so editing
# .gitignore to un-ignore your-life/ does not defeat it (the gitignore-was-edited
# case). No agent in the loop: this is enforcement, so it is a hook, not a skill.
#
# Used two ways (same logic): the Claude Code PreToolUse wrapper
# (guard-corpus-commit-hook.sh) and the pre-commit framework
# (.pre-commit-config.yaml). Exit 0 = clean, exit 1 = blocked.
set -uo pipefail

# Private-repo escape hatch. By default the guard assumes a public remote and
# refuses your-life/ corpus (the safe default). A forker who has DELIBERATELY
# chosen a private repo (GETTING-STARTED.md "Before you start") opts in to
# versioning their corpus by creating .specself-allow-corpus at the repo root, or
# exporting SPECSELF_ALLOW_CORPUS=1. Secrets stay blocked either way. This is what
# keeps the guard from firing on an INTENTIONAL private repo while still catching
# the accidental gitignore-was-edited leak on a public one.
allow_corpus=0
if [ -f ".specself-allow-corpus" ] || [ "${SPECSELF_ALLOW_CORPUS:-}" = "1" ]; then
  allow_corpus=1
fi

# File list: pre-commit passes staged paths as args; otherwise read the staged set.
if [ "$#" -gt 0 ]; then
  files=$(printf '%s\n' "$@")
else
  files=$(git diff --cached --name-only 2>/dev/null || true)
fi

corpus_hits=""
secret_hits=""

while IFS= read -r f; do
  [ -z "$f" ] && continue
  # (a) The escape hatch is NEVER committed, allow_corpus notwithstanding
  # (this is what keeps --private mode from accidentally versioning it).
  case "$f" in
    */.sensitive/*|.sensitive/*)
      corpus_hits="${corpus_hits}  ${f}"$'\n'
      continue
      ;;
  esac
  # (b) Private corpus: anything under your-life/ that is not committed structure
  # (the kit commits only README.md + .gitkeep there; everything else is yours).
  if [ "$allow_corpus" -eq 0 ]; then
    case "$f" in
      your-life/*)
        base="${f##*/}"
        if [ "$base" != ".gitkeep" ] && [ "$base" != "README.md" ]; then
          corpus_hits="${corpus_hits}  ${f}"$'\n'
        fi
        ;;
    esac
  fi
  # (c) Secret shapes in the staged content.
  if [ -f "$f" ] && LC_ALL=C grep -EqI \
    '(AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|aws_secret_access_key[[:space:]]*=)' \
    "$f"; then
    secret_hits="${secret_hits}  ${f}"$'\n'
  fi
done <<EOF
${files}
EOF

if [ -n "$corpus_hits" ] || [ -n "$secret_hits" ]; then
  echo "------------------------------------------------------------" >&2
  echo "SpecSelf privacy guard BLOCKED this commit. Your life stays yours." >&2
  if [ -n "$corpus_hits" ]; then
    echo "Private corpus must never be committed:" >&2
    printf '%s' "$corpus_hits" >&2
  fi
  if [ -n "$secret_hits" ]; then
    echo "Secret-shaped content detected:" >&2
    printf '%s' "$secret_hits" >&2
  fi
  echo "This guard checks PATHS, so editing .gitignore does not bypass it." >&2
  echo "Intentional (a private repo)? See steering/privacy.md and the guard" >&2
  echo "section in GETTING-STARTED.md." >&2
  echo "------------------------------------------------------------" >&2
  exit 1
fi
exit 0
