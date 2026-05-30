# Agent Temporal Superpowers

[English](README.md)

一个类似 Superpowers 的轻量 skill 套件，用于约束三类 Agent 执行行为：

- `timeboxed-delivery`：尊重用户 DDL，在时间耗尽前返回结果或进度。
- `wait-discipline`：避免无意义 sleep，要求有边界、基于条件的等待。
- `batch-concurrency`：为批处理任务使用有界异步、RPM/TPM 感知的远端模型调用，以及多进程处理。

三个 skill 共用：

```text
skills/_shared/agent-execution-defaults.json
```

Agent 应该把这个 JSON 当作默认参数，然后根据用户要求、服务商限制、机器资源和任务风险灵活调整。

## 本地安装

安装到 Codex 风格的 skill 目录：

```bash
./scripts/install-codex-skills.sh
```

安装到 Claude 风格的 skill 目录：

```bash
./scripts/install-claude-skills.sh
```

## Skill 文档

- [timeboxed-delivery](docs/timeboxed-delivery.zh.md)
- [wait-discipline](docs/wait-discipline.zh.md)
- [batch-concurrency](docs/batch-concurrency.zh.md)

## 验证

```bash
./scripts/validate.sh
```

## 插件结构

本仓库包含：

- `.codex-plugin/plugin.json`：Codex 插件 manifest，指向 `./skills/`。
- `.claude-plugin/plugin.json`：Claude 插件元数据。
- `.claude-plugin/marketplace.json`：本地 marketplace 元数据。
- `skills/`：实际 skill。
- `skills/_shared/`：共享 JSON 默认参数。
- `docs/`：每个 skill 的精简用法和配置说明。
- `scripts/`：本地安装和验证脚本。
