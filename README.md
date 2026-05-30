# Agent Temporal Superpowers

A small Superpowers-style skill suite for three related agent behaviors:

- `timeboxed-delivery`: respect user DDLs and report before time runs out.
- `wait-discipline`: avoid pointless sleeps and require bounded condition-based waits.
- `batch-concurrency`: use bounded async, RPM/TPM-aware remote model calls, and multiprocessing for batch work.

All three skills share:

```text
skills/_shared/agent-execution-defaults.json
```

Agents should treat that JSON as defaults, then adjust per user request, provider limits, machine capacity, and task risk.

## Install Locally

For Codex-style skill directories:

```bash
./scripts/install-codex-skills.sh
```

For Claude-style skill directories:

```bash
./scripts/install-claude-skills.sh
```

Validate:

```bash
./scripts/validate.sh
```

## Plugin Shape

This repo includes:

- `.codex-plugin/plugin.json`: Codex plugin manifest, pointing to `./skills/`.
- `.claude-plugin/plugin.json`: Claude plugin metadata.
- `.claude-plugin/marketplace.json`: local marketplace metadata.
- `skills/`: the actual skills.
- `skills/_shared/`: shared JSON defaults.
- `scripts/`: local install and validation helpers.

This intentionally imitates the useful part of `obra/superpowers` without copying its full release, hook, test, and marketplace infrastructure.
