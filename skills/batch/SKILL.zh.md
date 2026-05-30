# Batch Concurrency

[English](SKILL.md)

## 共享默认值

先读取 `../_shared/agent-execution-defaults.json`。除非用户或 API 服务商给出具体限制，否则使用 `remote_model_api`、`parallel_programming` 和 `async_programming` 默认值。

## 核心流程

1. 先跑通单个 item。
2. 转成有界并发或多进程。
3. 用输入 index 保持结果顺序。
4. 捕获单项错误，避免一个失败拖垮整个批次。
5. 添加有界 retry/backoff。
6. 长任务保存 partial results。
7. 输出进度。

## 远端模型 API

对 LLM、视频、文本模型 API，参考 FairGamer `Competition.py` 的模式：使用 async tasks、共享结果队列或按 index 写入的结果数组、RPM token bucket 限流，并按 task id 排序或赋值保序。

同时补充 TPM 控制：

- 请求前尽量用 tokenizer 估算 token。
- 没有 tokenizer 时使用 `default_prompt_token_estimate + max_tokens`，再乘以 `token_safety_margin`。
- 发送请求前，同时从 RPM bucket 获取 1 个 request token，并从 TPM bucket 获取估算 token 数。
- 如果服务商响应里有真实 token usage，记录真实值并调整后续估算。
- 遇到 429 或 rate-limit 错误时，优先遵守 `Retry-After`；否则使用带 jitter 的有界指数退避。

策略骨架：

```python
await rpm_bucket.acquire(1)
await tpm_bucket.acquire(estimated_prompt_tokens + max_tokens)
result = await call_model(item)
results[index] = result
```

## CPU-bound 本地工作

Python CPU-bound 任务可行时使用多进程。默认使用共享配置中的 16 个进程，然后根据内存、I/O 或机器负载降低。

优先采用少锁或无锁设计：

- 用 `ProcessPoolExecutor.map` 获得有序输出。
- worker 返回 `(index, result)`，最后统一排序。
- 每个进程写自己的临时文件，完成后合并。
- 避免共享可变状态和高频锁竞争。

只有正确性确实需要共享资源时才使用锁。锁竞争严重的并行程序往往只是慢一点的串行程序。

## 什么时候不要并行

如果 item 数量很小、单样本路径还没跑通、API 要求串行顺序，或者 rate/cost 限制让并发有害，就保持串行。
