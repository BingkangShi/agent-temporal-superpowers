# Why Superpowers Has Many Folders

`obra/superpowers` is not only a few skill files. It is a multi-agent, multi-platform plugin distribution.

The important folders are:

- `skills/`: the actual reusable skills. This is the core.
- `.codex-plugin/`: Codex plugin manifest. It tells Codex where the skills live and how to display the plugin.
- `.claude-plugin/`: Claude plugin manifest and marketplace metadata.
- `.cursor-plugin/`, `.opencode/`, `gemini-extension.json`: adapters for other agent apps.
- `hooks/`: startup hooks that inject "use skills" instructions into supported agents.
- `scripts/`: release, sync, and marketplace helper scripts.
- `tests/`: regression tests that check triggering, installation, hooks, and platform behavior.
- `docs/`: design notes and platform-specific docs.
- `assets/`: icons and marketplace images.

So the file count is high because Superpowers solves distribution and enforcement across many apps, not because each individual skill needs that much ceremony.

## Installation Model

Superpowers uses two installation styles:

1. Plugin install: the Agent App reads a plugin manifest, then loads skills from the plugin's `skills/` directory.
2. Direct skill install: skills are copied into a local skill directory such as `~/.codex/skills` or `~/.claude/skills`.

The plugin route is better for automatic updates, marketplace discovery, icons, hooks, and cross-platform packaging. Direct copying is simpler and good for local/private skills.

## Usage Model

Each skill has a `SKILL.md` with YAML frontmatter:

```yaml
name: skill-name
description: when the agent should use this skill
```

The description is always visible to the agent. The body is loaded only when the skill triggers. This keeps context small while still allowing detailed workflows on demand.
