#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
VALIDATOR="${HOME}/.codex/skills/.system/skill-creator/scripts/quick_validate.py"

python3 -m json.tool "$ROOT/.codex-plugin/plugin.json" >/dev/null
python3 -m json.tool "$ROOT/.claude-plugin/plugin.json" >/dev/null
python3 -m json.tool "$ROOT/.claude-plugin/marketplace.json" >/dev/null
python3 -m json.tool "$ROOT/skills/_shared/agent-execution-defaults.json" >/dev/null

if [[ -f "$VALIDATOR" ]] && python3 -c 'import yaml' >/dev/null 2>&1; then
  python3 "$VALIDATOR" "$ROOT/skills/timeboxed-delivery"
  python3 "$VALIDATOR" "$ROOT/skills/wait-discipline"
  python3 "$VALIDATOR" "$ROOT/skills/batch-concurrency"
else
  python3 - "$ROOT" <<'PY'
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
for skill in ("timeboxed-delivery", "wait-discipline", "batch-concurrency"):
    path = root / "skills" / skill / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise SystemExit(f"{path}: missing YAML frontmatter")
    try:
        frontmatter = text.split("---\n", 2)[1]
    except IndexError as exc:
        raise SystemExit(f"{path}: malformed YAML frontmatter") from exc
    fields = {}
    for line in frontmatter.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    if fields.get("name") != skill:
        raise SystemExit(f"{path}: expected name {skill!r}, got {fields.get('name')!r}")
    if not fields.get("description"):
        raise SystemExit(f"{path}: missing description")
    if not re.fullmatch(r"[a-z0-9-]+", fields["name"]):
        raise SystemExit(f"{path}: invalid skill name")
print("Basic skill validation passed.")
PY
fi

echo "Validation passed."
