# Wait Discipline

[English](SKILL.md)

## 共享默认值

先读取 `../_shared/agent-execution-defaults.json`。除非任务上下文或用户指令要求不同值，否则使用 `wait_discipline` 默认值。

## 规则

- 不要在交互式 Agent 回合里隐藏多分钟 sleep。
- 不要添加无条件长 sleep。
- 每个等待循环都必须有整体 timeout。
- 每次 sleep 都必须位于条件检查之间。
- 本地等待优先使用短轮询，条件满足后立刻退出。
- 如果 API 提供 `Retry-After` 或限流元数据，应优先使用。

坏例子：

```bash
sleep 300
```

好例子：

```bash
timeout 30s sh -c 'until curl -fsS http://localhost:3000/health; do sleep 1; done'
```

Python 模式：

```python
import time

deadline = time.monotonic() + 30
while time.monotonic() < deadline:
    if ready():
        break
    time.sleep(1)
else:
    raise TimeoutError("condition was not met within 30s")
```

保留任何 sleep 前，都要确认它是正确性所需，而不是习惯。
