#!/bin/sh
# SpecSelf privacy-mode switcher (ADR-008 D14).
#
# The one irreversible-if-wrong setup step is hand-editing the .gitignore
# rules that decide whether your-life/ corpus gets committed. This makes it
# mechanical: manages the fenced block in .gitignore between the "specself
# privacy mode" markers, plus the .specself-allow-corpus marker the commit
# guard reads (.claude/hooks/guard-corpus-commit.sh). Manual fallback and the
# reasoning: GETTING-STARTED.md "Before you start", steering/privacy.md.
#
# Usage: scripts/set-privacy-mode.sh --status | --private | --public
# Locates the kit root from its own path, so it runs from anywhere.
# --private and --public are idempotent: running either twice changes
# nothing the second time.

set -eu

script_dir=$(cd -- "$(dirname -- "$0")" >/dev/null 2>&1 && pwd)
kit_root=$(cd -- "$script_dir/.." >/dev/null 2>&1 && pwd)
cd "$kit_root"

GITIGNORE=".gitignore"
ALLOW_MARKER=".specself-allow-corpus"
BEGIN_MARKER="# >>> specself privacy mode — managed by scripts/set-privacy-mode.sh"
END_MARKER="# <<< specself privacy mode"

PUBLIC_BLOCK='your-life/**
!your-life/
!your-life/**/
!your-life/**/README.md
!your-life/**/.gitkeep
!your-life/README.md'

# The escape hatch stays uncommittable even when the rest of your-life/ is
# versioned in private mode.
PRIVATE_BLOCK='your-life/.sensitive/**'

usage() {
  echo "Usage: $0 --status | --private | --public" >&2
  echo "  --status   print the current privacy mode" >&2
  echo "  --private  version your-life/ corpus (private remote only)" >&2
  echo "  --public   restore the default: your-life/ corpus stays uncommitted" >&2
}

markers_present() {
  [ -f "$GITIGNORE" ] && grep -qF "$BEGIN_MARKER" "$GITIGNORE" && grep -qF "$END_MARKER" "$GITIGNORE"
}

# Lines strictly between the markers, or empty if the markers are missing.
current_block() {
  [ -f "$GITIGNORE" ] || return 0
  awk -v b="$BEGIN_MARKER" -v e="$END_MARKER" \
    '$0==b{inside=1;next} $0==e{inside=0;next} inside{print}' "$GITIGNORE"
}

block_is_public() { [ "$(current_block)" = "$PUBLIC_BLOCK" ]; }

replace_block() {
  # $1 = the new block content (may be multiple lines).
  if ! markers_present; then
    echo "set-privacy-mode: markers not found in $GITIGNORE." >&2
    echo "Expected '$BEGIN_MARKER' and '$END_MARKER'. Not touching the file." >&2
    exit 1
  fi
  tmp=$(mktemp)
  awk -v b="$BEGIN_MARKER" -v e="$END_MARKER" -v new="$1" \
    '$0==b{print;print new;inside=1;next} $0==e{inside=0;print;next} inside{next} {print}' \
    "$GITIGNORE" > "$tmp"
  mv "$tmp" "$GITIGNORE"
}

do_status() {
  if markers_present && block_is_public && [ ! -f "$ALLOW_MARKER" ]; then
    echo "public"
    echo "your-life/ corpus is gitignored; only README.md and .gitkeep commit."
  else
    echo "private"
    echo "your-life/ corpus is versioned in this repo; your-life/.sensitive/** still ignored."
  fi
}

do_private() {
  replace_block "$PRIVATE_BLOCK"
  if [ -f "$ALLOW_MARKER" ]; then
    echo "$ALLOW_MARKER already present."
  else
    : > "$ALLOW_MARKER"
    echo "Created $ALLOW_MARKER."
  fi
  echo "Private mode set: your-life/ corpus will now be tracked by git."
  echo "your-life/.sensitive/** stays ignored, no exceptions."
  echo "The commit guard now allows corpus commits (private remote only —"
  echo "see steering/privacy.md)."
}

do_public() {
  replace_block "$PUBLIC_BLOCK"
  if [ -f "$ALLOW_MARKER" ]; then
    rm -f "$ALLOW_MARKER"
    echo "Removed $ALLOW_MARKER."
  else
    echo "$ALLOW_MARKER already absent."
  fi
  echo "Public mode restored: your-life/ corpus is gitignored again."

  if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    tracked=$(git ls-files your-life 2>/dev/null | grep -vE '(README\.md|\.gitkeep)$' || true)
    if [ -n "$tracked" ]; then
      echo "------------------------------------------------------------" >&2
      echo "WARNING: these your-life/ files are already tracked by git and" >&2
      echo "will STAY tracked (restoring .gitignore does not untrack them):" >&2
      echo "$tracked" | sed 's/^/  /' >&2
      echo "To remove them from git (your local copies are kept):" >&2
      echo "  git rm --cached -r <path>   # for each path above, then commit" >&2
      echo "------------------------------------------------------------" >&2
    fi
  fi
}

case "${1:-}" in
  --status) do_status ;;
  --private) do_private ;;
  --public) do_public ;;
  *) usage; exit 2 ;;
esac
