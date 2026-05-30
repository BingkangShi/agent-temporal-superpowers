#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
DEST="${CLAUDE_HOME:-$HOME/.claude}/skills"

mkdir -p "$DEST"
rm -rf "$DEST/timeboxed-delivery" "$DEST/wait-discipline" "$DEST/batch-concurrency"
rsync -a --delete "$ROOT/skills/due/" "$DEST/due/"
rsync -a --delete "$ROOT/skills/wait/" "$DEST/wait/"
rsync -a --delete "$ROOT/skills/batch/" "$DEST/batch/"
rsync -a --delete "$ROOT/skills/_shared/" "$DEST/_shared/"

echo "Installed Tempo skills to $DEST"
