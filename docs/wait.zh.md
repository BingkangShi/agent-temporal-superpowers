# wait

[English](wait.md)

## 用途

当代码或 Agent 行为涉及等待、sleep、轮询、重试、队列检查、服务启动或限流延迟时使用该 skill。它用于避免没有条件检查的长时间等待，例如 `sleep 300`。

## 用法

典型提示：

```text
Review this script and remove pointless sleeps.
```

```text
启动开发服务器，但不要盲目等待。
```

Agent 应该：

- 避免无条件长 sleep，
- 使用基于条件的轮询，
- 设置整体 timeout，
- 每次 sleep 之间检查状态，
- 服务商提供 `Retry-After` 时优先遵守。

## JSON 参数

配置位置：`skills/_shared/agent-execution-defaults.json` 的 `wait_discipline` 段。

- `max_unconditional_sleep_seconds`：允许的无条件 sleep 上限。
- `max_sleep_seconds_without_user_or_api_reason`：超过该时长的 sleep 必须有用户或 API 层面的明确理由。
- `default_local_poll_interval_seconds`：本地轮询默认间隔。
- `max_local_poll_interval_seconds`：本地轮询最大间隔。
- `default_wait_timeout_seconds`：等待循环默认总 timeout。
- `require_condition_check_between_sleeps`：重复 sleep 之间必须检查条件。
- `require_overall_timeout_for_polling`：轮询必须有总截止时间。
- `ban_hidden_multi_minute_sleep`：禁止交互任务中的隐藏多分钟等待。

具体服务启动时间或 API 限流规则可以覆盖这些默认值。
