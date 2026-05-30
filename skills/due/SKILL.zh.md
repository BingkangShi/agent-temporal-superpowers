# Timeboxed Delivery

[English](SKILL.md)

## 共享默认值

先读取 `../_shared/agent-execution-defaults.json`。除非用户给出更严格或更宽松的参数，否则使用 `timeboxed_delivery` 默认值。

## 执行模型

如果 Agent App 支持子 Agent 或后台 worker：

1. 主 Agent 负责计时器、DDL 检查、进度收集和最终回复。
2. 派发 worker 子 Agent 执行具体实现、调查或批处理任务。
3. 要求 worker 在 `max_silent_work_seconds` 之前输出 checkpoint。
4. 在距离 DDL `default_deadline_warning_seconds` 时停止扩大范围，并收集当前最好结果。
5. 在截止时间前回复结果、进度或 blocker。

如果没有子 Agent，则模拟同样行为：内部跟踪 DDL，使用短工具调用，并在回复缓冲时间前停止新的高风险工作。

## 工作策略

- 把时间限制当作硬性需求。
- 先选择最小有用交付物。
- 避免大范围探索和可选重构。
- 优先使用有边界的命令和目标明确的测试。
- 如果未完成，返回当前状态、具体产物、blocker、下一步和预计额外时间。

不要为了追求更好看的结果而静默超过用户 DDL。
