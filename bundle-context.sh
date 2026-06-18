#!/usr/bin/env bash
#
# bundle-context.sh - concatenate your operating context (the contract + your
# vision + your committed principles) into one file you can paste into a chat or
# add to a Claude Project as knowledge.
#
# Usage:
#   ./bundle-context.sh            # writes context-bundle.md
#   ./bundle-context.sh out.md     # writes to a path you choose
#
# Windows: run from Git Bash.
#
# The output contains YOUR corpus. It is gitignored by default. Never commit it.

set -euo pipefail
cd "$(dirname "$0")"

OUT="${1:-context-bundle.md}"

emit() { printf '%s\n' "$1"; }

{
  emit "# My SpecSelf operating context"
  emit ""
  emit "> This is the contract my agent follows, plus my committed vision and"
  emit "> principles. Read it and hold to it for this conversation. You may question"
  emit "> anything here, but you never rewrite it: I author the record, you challenge it."
  emit ""
  emit "---"
  emit ""
  emit "## The contract (AGENTS.md)"
  emit ""
  cat AGENTS.md

  if [ -f your-life/vision.md ]; then
    emit ""
    emit "---"
    emit ""
    emit "## Vision"
    emit ""
    cat your-life/vision.md
  fi

  if [ -f your-life/aspirational.md ]; then
    emit ""
    emit "---"
    emit ""
    emit "## Aspirational (who I am becoming)"
    emit ""
    cat your-life/aspirational.md
  fi

  emit ""
  emit "---"
  emit ""
  emit "## Principles"
  emit ""

  # Every committed principle file, across all domains; skip scaffolding.
  found=0
  while IFS= read -r f; do
    found=1
    emit "### ${f#your-life/principles/}"
    emit ""
    cat "$f"
    emit ""
  done < <(find your-life/principles -type f -name '*.md' ! -name 'README.md' | sort)

  if [ "$found" -eq 0 ]; then
    emit "_No committed principles yet. Run the foundation session"
    emit "(see GETTING-STARTED.md), then re-run this script._"
  fi
} > "$OUT"

lines=$(wc -l < "$OUT" | tr -d ' ')
echo "Wrote $OUT ($lines lines)."
echo "Paste it into a chat, or add it to a Claude Project as knowledge."
echo "It contains your corpus and is gitignored. Do not commit it."
