#!/usr/bin/env bash
# uninstall.sh — remove the sci-skills plugin-family symlinks (linux)
#
# Removes ONLY the symlinks that install.sh created under ~/.claude/skills/.
# The repo itself is left untouched (so git pull && bash install.sh can
# re-activate it). Idempotent: safe to re-run; missing symlinks are skipped.
#
# This does NOT touch: ~/.claude/agents/, settings.json, installed_plugins.json,
# or any user-project output directories (sci-skills/ within a manuscript
# project). Those are separate concerns.

set -euo pipefail

FAMILIES=(sci-skills sci-skills-article sci-skills-analysis)
CLAUDE_HOME="${HOME}/.claude"
SKILLS_DIR="$CLAUDE_HOME/skills"

echo "Removing sci-skills family symlinks from: $SKILLS_DIR"
echo

removed=0
skipped=0
for fam in "${FAMILIES[@]}"; do
  LINK="$SKILLS_DIR/$fam"
  if [[ -L "$LINK" ]]; then
    rm "$LINK"
    echo "[removed] $LINK"
    removed=$((removed + 1))
  elif [[ -e "$LINK" ]]; then
    echo "[skipped] $LINK exists but is NOT a symlink (not touching it — resolve manually)" >&2
    skipped=$((skipped + 1))
  else
    echo "[absent]  $LINK (nothing to do)"
  fi
done

echo
echo "Done. Removed $removed symlink(s), skipped $skipped non-symlink(s)."
echo "The repo is still on disk — re-activate anytime with: bash install.sh"
