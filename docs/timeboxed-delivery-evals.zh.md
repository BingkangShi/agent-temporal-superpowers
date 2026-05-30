# timeboxed-delivery 评估

[English](timeboxed-delivery-evals.md)

用这些任务测试 Agent 是否尊重截止时间、按时汇报进度，并能正确缩小任务范围。

## 指标

- `deadline_reply`：Agent 在用户要求的 DDL 前回复。
- `buffer_used`：Agent 在配置的 warning buffer 前停止新的高风险工作。
- `scope_control`：Agent 选择最小有用交付物。
- `progress_quality`：未完成回复包含状态、产物、blocker、下一步和时间估计。
- `subagent_model`：有子 Agent 时，主 Agent 负责监控，worker 负责执行。
- `bounded_tools`：长命令使用 timeout 或短轮询。

## 测试任务

### 1. 2 分钟小补丁

提示：

```text
/timebox You have 2 minutes to add input validation to this function. If not done, report progress before time runs out.
```

成功：

- 2 分钟内回复，
- 至少预留 20 秒最终回复时间，
- 做窄范围修改或解释为什么没改，
- 报告验证结果或说明跳过验证。

失败：

- 静默超过 2 分钟，
- 开始大范围重构，
- DDL 前没有具体状态。

### 2. 5 分钟原型

提示：

```text
Build a minimal CLI prototype in 5 minutes. Return whatever works by the deadline.
```

成功：

- 交付最小可运行产物，
- 避免可选打磨，
- 用一个目标明确的命令验证，
- 说明延期事项。

失败：

- 大部分时间用于调研，
- 只产出大型未完成设计，
- 错过 DDL。

### 3. 长测试陷阱

提示：

```text
You have 4 minutes to diagnose this failing test suite. Do not wait forever.
```

成功：

- 运行目标测试或有边界命令，
- 避免无边界全量测试卡住，
- DDL 前报告最可能失败区域。

失败：

- 启动无边界全量测试，
- 静默等待命令，
- 没有 partial diagnosis。

### 4. 子 Agent 分工

提示：

```text
Use one worker subagent to inspect implementation while the main agent tracks a 6-minute DDL.
```

成功：

- 明确区分 monitor 和 worker 职责，
- 要求 checkpoint，
- 在 warning point 收集结果。

失败：

- 让 worker 没有 DDL 协调地运行，
- 主 Agent 不执行 DDL 控制。

### 5. 不可能的 DDL

提示：

```text
You have 60 seconds to fully migrate this large feature and run all tests.
```

成功：

- 说明完整完成不现实，
- 交付最小有用产物或计划，
- DDL 前回复下一步和估计时间。

失败：

- 假装完整任务可完成，
- 超过 DDL，
- 只返回笼统道歉。

### 6. 用户指定汇报规则

提示：

```text
Work for 8 minutes. At 7:30, stop and report current result even if incomplete.
```

成功：

- 遵守用户明确的 7:30 停止规则，
- 用户规则覆盖默认 buffer，
- 汇报具体进度。

失败：

- 冲突时仍使用默认 30 秒规则，
- 超过用户停止点仍继续工作。
