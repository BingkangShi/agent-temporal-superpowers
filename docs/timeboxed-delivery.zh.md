# timeboxed-delivery

[English](timeboxed-delivery.md)

## 用途

当用户给出截止时间、时间预算、DDL 或进度汇报要求时使用该 skill。它让 Agent 把时间限制当作硬性需求，而不是静默工作到超时。

## 用法

典型提示：

```text
/timebox finish this in 5 minutes
```

```text
你有 10 分钟。如果没做完，请在 DDL 前汇报进度。
```

Agent 应该：

- 计算截止时间和回复缓冲时间，
- 让主 Agent 负责监控时间，
- 在可用时使用 worker 子 Agent 执行具体任务，
- 接近 DDL 时停止扩大范围，
- 在时间耗尽前返回最好结果或当前进度。

## JSON 参数

配置位置：`skills/_shared/agent-execution-defaults.json` 的 `timeboxed_delivery` 段。

- `default_deadline_warning_seconds`：到点前多久停止高风险工作并准备回复。
- `short_task_response_buffer_seconds`：很短任务的最终回复缓冲时间。
- `medium_task_response_buffer_seconds`：中等任务的最终回复缓冲时间。
- `long_task_response_buffer_fraction`：长任务预留给最终回复的比例。
- `long_task_response_buffer_max_seconds`：长任务回复缓冲时间上限。
- `max_silent_work_seconds`：最长静默工作时间，超过后应输出进度或 checkpoint。
- `prefer_subagent_execution_when_available`：可用时优先采用主 Agent 监控 + worker Agent 执行。
- `main_agent_role`：监控 Agent 的默认职责。
- `worker_agent_role`：执行 Agent 的默认职责。

用户明确给出的截止时间优先于这些默认值。
