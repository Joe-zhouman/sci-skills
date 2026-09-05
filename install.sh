#!/usr/bin/env bash
# install.sh — install the sci-skills skills for live development (linux)
#
# What this does:
#   Symlinks every <family>/skills/<skill>/ directory flat into the user
#   skills dirs of both harnesses (~/.claude/skills/ and, unless SKIP_ZCODE=1,
#   ~/.zcode/skills/). Both harnesses scan those dirs flat
#   (<skills-dir>/<skill>/SKILL.md), and because these are symlinks, edits in
#   the repo show up in every new session immediately — no reinstall step.
#
# Dev vs distribution:
#   - This script = DEV install (live symlinks, plain skill names).
#   - .claude-plugin/marketplace.json = DISTRIBUTION (frozen copies under
#     ~/.claude/plugins/cache/, plugin-namespaced names like
#     sci-skills:sci-draw). Use one or the other for the same skills —
#     installing both double-loads them.
#
# Idempotent: safe to re-run. Repoints existing symlinks, leaves
# non-symlink conflicts untouched. Run from anywhere; resolves repo root
# from this script's location.

set -euo pipefail

# --- locate repo root (this script lives at repo root) ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"

# --- the four family directories (each is a separate plugin) ---
# xps (sci-skills-analysis) 不是谁都要用的：不需要时跳过，只装其余家族：
#   SKIP_FAMILIES=sci-skills-analysis bash install.sh
# （空格分隔多个家族名；跳过仍会 uv sync，依赖与其他家族共享）
FAMILIES=(sci-skills sci-skills-article sci-skills-thesis sci-skills-analysis)
SKIP_FAMILIES="${SKIP_FAMILIES:-}"

# returns 0 (true) if the family is in SKIP_FAMILIES
skip_fam() { [[ " $SKIP_FAMILIES " == *" $1 "* ]]; }

# --- sanity: every installed family must have .claude-plugin/plugin.json + skills/ ---
for fam in "${FAMILIES[@]}"; do
  if skip_fam "$fam"; then continue; fi
  if [[ ! -f "$REPO_ROOT/$fam/.claude-plugin/plugin.json" ]] || [[ ! -d "$REPO_ROOT/$fam/skills" ]]; then
    echo "ERROR: $REPO_ROOT/$fam does not look like a sci-skills family plugin" >&2
    echo "       (expected $fam/.claude-plugin/plugin.json and $fam/skills/)" >&2
    exit 1
  fi
done

# --- platform guard (win/mac deferred) ---
OS="$(uname -s)"
if [[ "$OS" != "Linux" ]]; then
  echo "ERROR: this install.sh is for Linux (got $OS)." >&2
  exit 1
fi

CLAUDE_HOME="${HOME}/.claude"
SKILLS_DIR="$CLAUDE_HOME/skills"

# --- flat per-skill symlinks (dev live-sync install) ---
# Each skill is symlinked individually into the harness's user skills dir, so
# repo edits show up immediately in every new session. Both CC and ZCode scan
# these dirs flat (<skills-dir>/<skill>/SKILL.md). This is the DEV install —
# the marketplace (.claude-plugin/marketplace.json) is the DISTRIBUTION path
# (frozen copies, plugin-namespaced); use one or the other, not both, for the
# same skills.
link_skills_into() {
  local dest="$1" label="$2" count=0
  mkdir -p "$dest"
  for fam in "${FAMILIES[@]}"; do
    if skip_fam "$fam"; then continue; fi
    for skill_dir in "$REPO_ROOT/$fam/skills/"*/; do
      [[ -f "$skill_dir/SKILL.md" ]] || continue
      local name LINK
      name="$(basename "$skill_dir")"
      LINK="$dest/$name"
      if [[ -L "$LINK" ]]; then
        rm "$LINK"    # repoint (repo may have moved)
      elif [[ -e "$LINK" ]]; then
        echo "  WARNING: $LINK exists and is not a symlink — left untouched" >&2
        continue
      fi
      ln -s "${skill_dir%/}" "$LINK"
      count=$((count + 1))
    done
  done
  echo "[$label]  $count skill symlink(s) live in $dest (edits sync immediately)"
}

echo "Installing sci-skills skills (flat live symlinks) from: $REPO_ROOT"
echo

link_skills_into "$SKILLS_DIR" "claude"

# --- ZCode side (optional) ---
# Opt out with SKIP_ZCODE=1 (e.g. if you manage ZCode skills another way).
ZCODE_SKILLS_DIR="${HOME}/.zcode/skills"
if [[ "${SKIP_ZCODE:-}" == "1" || ! -d "${HOME}/.zcode" ]]; then
  echo "[zcode]   skipped (SKIP_ZCODE=1 or no ~/.zcode)"
else
  link_skills_into "$ZCODE_SKILLS_DIR" "zcode"
fi

# --- Python env for bundled scripts (XPS analysis etc.) ---
# A pyproject.toml at repo root declares the deps the skill scripts run in.
# `uv sync` creates .venv/ and installs them; scripts self-activate it via a
# transparent launcher in _cli.py (re-exec under .venv), so agents just call
# `python scripts/foo.py` with no env bookkeeping.
# The XPS-only deps (lmfit/lmfitxps/pyarrow) are the optional `xps` extra —
# skipped together with the sci-skills-analysis family (SKIP_FAMILIES).
sync_env() {
  ( cd "$REPO_ROOT" && "$@" ) || echo "  WARNING: uv sync failed — scripts will fall back to the caller's interpreter (deps may be missing). Install uv: https://docs.astral.sh/uv/"
}
if command -v uv >/dev/null 2>&1; then
  if skip_fam "sci-skills-analysis"; then
    echo "[env]     uv found — syncing .venv (base deps only, no xps extra)"
    sync_env uv sync
  else
    echo "[env]     uv found — syncing .venv (base deps + xps extra)"
    sync_env uv sync --extra xps
  fi
else
  echo "[env]     uv NOT found — skipping .venv setup." >&2
  echo "          Skill scripts self-activate .venv when present; without uv they fall back to the caller's interpreter." >&2
  echo "          Install uv (recommended):  https://docs.astral.sh/uv/" >&2
  echo "          Then re-run:  bash install.sh" >&2
fi

echo
echo "Done. To activate:"
echo "  1. Start a NEW Claude Code session (skills load at session start)."
echo "  2. Verify plugins:  /skills   (should list the families above)"
echo
echo "Update later: git pull && bash install.sh   (re-running repoints symlinks + re-syncs env)"
echo
echo "Alternative — install as marketplace plugins instead of dev symlinks:"
echo "  /plugin marketplace add Joe-zhouman/sci-skills"
echo "  /plugin install sci-skills@sci-skills        # and the other families as needed"
echo "  (marketplace installs COPY the plugin dir; for xps deps run 'uv sync'"
echo "   inside the installed sci-skills-analysis plugin dir)"
