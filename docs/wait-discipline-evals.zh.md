# wait-discipline 评估

[English](wait-discipline-evals.md)

用这些任务测试 Agent 是否能把盲目等待替换为有边界、基于条件的等待。

## 指标

- `no_blind_sleep`：不引入或保留无条件长 sleep。
- `overall_timeout`：每个轮询循环都有总 deadline。
- `condition_check`：等待间隔之间检查 readiness 或外部状态。
- `retry_after`：可用时遵守 API retry 元数据。
- `fast_exit`：条件满足后立刻退出循环。
- `interactive_bound`：交互回合中不隐藏多分钟等待。

## 测试任务

### 1. 移除 `sleep 300`

提示：

```text
Review this deployment script and replace sleep 300 with a better readiness wait.
```

成功：

- 用条件检查替代盲目 sleep，
- 添加整体 timeout，
- 使用短轮询。

失败：

- 保留 `sleep 300`，
- 改成另一个盲目长 sleep，
- 没有 timeout。

### 2. 开发服务器启动

提示：

```text
Start a local dev server and wait until it is ready without wasting time.
```

成功：

- 探测 health endpoint 或端口，
- 使用短轮询和 timeout，
- ready 后立即停止轮询。

失败：

- 使用固定长 sleep，
- 不检查就假设 ready，
- 静默等待数分钟。

### 3. API 限流

提示：

```text
Handle HTTP 429 responses from an API that returns Retry-After.
```

成功：

- 读取并遵守 `Retry-After`，
- 限制 retry 次数，
- 输出有用的 retry 诊断。

失败：

- 忽略 `Retry-After`，
- 紧密循环重试，
- 无限 sleep。

### 4. 队列 worker 轮询

提示：

```text
Poll a background job until completion.
```

成功：

- 轮询 job 状态，
- 在 done/failed 状态退出，
- 有整体 timeout。

失败：

- 按猜测时长 sleep 一次，
- 不检查 failed 状态，
- 可能永远挂住。

### 5. Timeout 行为测试

提示：

```text
Write a test for timeout behavior that uses sleep.
```

成功：

- 使用尽可能短且可靠的 sleep，
- 隔离 timing-sensitive 测试，
- 不拖慢整个测试套件。

失败：

- 毫秒可行时却使用多秒 sleep，
- 制造脆弱 timing 假设，
- 拖慢无关测试。

### 6. Watcher debounce

提示：

```text
Implement a file watcher debounce.
```

成功：

- 使用较小 debounce 间隔，
- 合并事件，
- 不无谓阻塞主循环。

失败：

- 使用大段阻塞 sleep，
- 错误丢弃事件，
- 阻止 shutdown 或 cancellation。
