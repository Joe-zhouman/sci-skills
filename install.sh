#!/usr/bin/env bash
# install.sh — install the sci-skills plugin families (linux)
#
# What this does:
#   Symlinks each family directory (sci-skills/, sci-skills-article/,
#   sci-skills-analysis/) into ~/.claude/skills/<family>/, so CC's
#   @skills-dir mechanism auto-loads each family as a separate plugin
#   and namespaces its skills (e.g. sci-skills:sci-draw,
#   sci-skills-article:sci-story).
#
# Why symlink (not copy): editing the repo updates the plugin immediately.
# Why one plugin per family (not one for the whole repo): CC's plugin loader
#   only scans one level under skills/, so each family must be its own plugin
#   reached via its own symlink. A root-level plugin.json would make the
#   whole repo one plugin and recursively walk all family subdirs —
#   deliberately avoided.
#
# Idempotent: safe to re-run. Repoints existing symlinks, backs up
# non-symlink conflicts. Run from anywhere; resolves repo root from this
# script's location.

set -euo pipefail

# --- locate repo root (this script lives at repo root) ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"

# --- the three family directories (each is a separate plugin) ---
# xps (sci-skills-analysis) 不是谁都要用的：不需要时跳过，只装其余家族：
#   SKIP_FAMILIES=sci-skills-analysis bash install.sh
# （空格分隔多个家族名；跳过仍会 uv sync，依赖与其他家族共享）
FAMILIES=(sci-skills sci-skills-article sci-skills-analysis)
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

echo "Installing sci-skills families from: $REPO_ROOT"
echo

mkdir -p "$SKILLS_DIR"

for fam in "${FAMILIES[@]}"; do
  if skip_fam "$fam"; then
    echo "[skip]    $fam — in SKIP_FAMILIES"
    continue
  fi
  SRC="$REPO_ROOT/$fam"
  LINK="$SKILLS_DIR/$fam"

  if [[ -L "$LINK" ]]; then
    # existing symlink — repoint to current repo (handles repo moved/relocated)
    rm "$LINK"
  elif [[ -e "$LINK" ]]; then
    echo "WARNING: $LINK exists and is not a symlink." >&2
    echo "         Backing it up to ${LINK}.bak and replacing with symlink." >&2
    mv "$LINK" "${LINK}.bak"
  fi
  ln -s "$SRC" "$LINK"
  echo "[plugin]  $LINK -> $SRC"
done

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
echo "  2. Verify plugins:  /skills   (should list the three families above)"
echo
echo "Update later: git pull && bash install.sh   (re-running repoints symlinks + re-syncs env)"
