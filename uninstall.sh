#!/usr/bin/env bash
# uninstall.sh — remove the sci-skills symlink installs (linux)
#
# Removes the flat per-skill symlinks that install.sh created under
# ~/.claude/skills/ and ~/.zcode/skills/ (plus any older family-level or
# per-skill symlinks from earlier install styles). Only symlinks actually
# pointing into this repo are removed. The repo itself is untouched.
# Idempotent.
#
# This does NOT touch: ~/.claude/agents/, settings.json, installed_plugins.json,
# marketplace installs (/plugin uninstall <name>@sci-skills), or any
# user-project output directories (sci-skills/ within a manuscript
# project). Those are separate concerns.

set -euo pipefail

FAMILIES=(sci-skills sci-skills-article sci-skills-thesis sci-skills-analysis)
CLAUDE_HOME="${HOME}/.claude"
REPO_URL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# every skill name this repo can provide, plus the family names from older
# install styles — all checked against both harness skills dirs
NAMES=()
for fam in "${FAMILIES[@]}"; do
  NAMES+=("$fam")
  for skill_dir in "$REPO_URL/$fam/skills/"*/; do
    [[ -f "$skill_dir/SKILL.md" ]] && NAMES+=("$(basename "$skill_dir")")
  done
done

remove_from() {
  local dest="$1" label="$2" removed=0 skipped=0
  for name in "${NAMES[@]}"; do
    local LINK="$dest/$name"
    if [[ -L "$LINK" ]]; then
      if [[ "$(readlink "$LINK")" == "$REPO_URL"* ]]; then
        rm "$LINK"
        echo "[$label]  removed $LINK"
        removed=$((removed + 1))
      else
        echo "[$label]  $LINK points outside this repo — not touching it" >&2
        skipped=$((skipped + 1))
      fi
    fi
  done
  [[ $removed -eq 0 && $skipped -eq 0 ]] && echo "[$label]  nothing to remove"
  return 0
}

echo "Removing sci-skills symlinks (only links pointing into $REPO_URL)"
echo

remove_from "$CLAUDE_HOME/skills" "claude"

if [[ -d "${HOME}/.zcode/skills" && "${SKIP_ZCODE:-}" != "1" ]]; then
  remove_from "${HOME}/.zcode/skills" "zcode"
fi

echo
echo "Done. The repo is still on disk — re-activate anytime with: bash install.sh"
echo "(Marketplace installs are separate: /plugin uninstall <name>@sci-skills)"
