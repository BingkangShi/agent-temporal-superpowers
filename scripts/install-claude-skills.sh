#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
DEST="${CLAUDE_HOME:-$HOME/.claude}/skills"

mkdir -p "$DEST"
rsync -a --delete "$ROOT/skills/timeboxed-delivery/" "$DEST/timeboxed-delivery/"
rsync -a --delete "$ROOT/skills/wait-discipline/" "$DEST/wait-discipline/"
rsync -a --delete "$ROOT/skills/batch-concurrency/" "$DEST/batch-concurrency/"
rsync -a --delete "$ROOT/skills/_shared/" "$DEST/_shared/"

echo "Installed Agent Temporal Superpowers skills to $DEST"
