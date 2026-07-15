#!/usr/bin/env bash
# SpecSelf Claude Code PreToolUse wrapper for the corpus guard.
#
# Claude Code runs this before every Bash tool call, passing the event JSON on
# stdin. When the command commits or pushes, we run the deterministic guard and
# BLOCK (exit 2, whose stderr Claude surfaces) on a violation. On anything else
# we no-op (exit 0). The guard itself only blocks on a real corpus/secret hit, so
# a coarse git-commit/push match here is safe.
#
# This is the convenience layer. The authoritative, agent-independent gate is the
# pre-commit hook (.pre-commit-config.yaml) — both call the same guard.
input=$(cat 2>/dev/null || true)

if printf '%s' "$input" | grep -q 'git' && \
   printf '%s' "$input" | grep -Eq '(commit|push)'; then
  here="$(cd "$(dirname "$0")" && pwd)"
  if ! bash "$here/guard-corpus-commit.sh"; then
    echo "SpecSelf guard: refused this commit/push (see the reason above)." >&2
    echo "Unstage the flagged corpus/secret and retry." >&2
    exit 2
  fi
fi
exit 0
