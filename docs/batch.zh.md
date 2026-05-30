# batch

[English](batch.md)

## 用途

用于大量相互独立的任务：远端模型 API 调用、文本/视频样本、embedding、HTTP 请求、文件批处理、评测、CPU 密集循环或多进程任务。

## 用法

典型提示：

```text
Process these 200 samples with bounded concurrency and preserve order.
```

```text
用 Gemini/OpenAI API 处理这个数据集，不要超过 RPM 或 TPM 限制。
```

Agent 应该：

- 先跑通单个样本，
- 再改成有界并发或多进程，
- 用 index 保持输出顺序，
- 捕获单项错误而不中断整个批次，
- 使用有界 retry/backoff，
- 长任务保存 partial results，
- 输出进度。

## JSON 参数

配置位置：`skills/_shared/agent-execution-defaults.json`。

### `remote_model_api`

- `default_concurrency`：远端 API 默认并发请求数。
- `max_concurrency_without_user_approval`：未获得用户明确同意前的并发上限。
- `default_rpm_limit`：默认每分钟请求数 bucket 大小。
- `default_tpm_limit`：默认每分钟 token 数 bucket 大小。
- `token_bucket_interval_seconds`：bucket refill 窗口。
- `default_prompt_token_estimate`：没有 tokenizer 时的 prompt token 估算值。
- `default_completion_token_estimate`：completion token 估算值。
- `token_safety_margin`：避免低估 TPM 的安全倍率。
- `retry.max_attempts`：每个 item 最大尝试次数。
- `retry.initial_backoff_seconds`：首次重试延迟。
- `retry.max_backoff_seconds`：重试延迟上限。
- `retry.jitter_fraction`：随机抖动，避免同步重试。
- `persist_partial_results_every_n_items`：保存 checkpoint 的频率。
- `preserve_order`：输出顺序与输入顺序保持一致。

### `parallel_programming`

- `default_processes`：CPU-bound 多进程默认进程数。
- `prefer_multiprocessing_for_cpu_bound_python`：Python CPU-bound 任务优先使用多进程而非线程。
- `prefer_lock_free_result_collection`：避免共享可变状态和高频锁竞争。
- `leave_cpu_headroom_processes`：为系统和其他工具保留 CPU 余量。
- `chunk_size_strategy`：默认 chunk size 策略。

### `async_programming`

- `default_concurrency`：非模型异步 I/O 的默认并发数。
- `preserve_order_with_indexes`：用输入 index 保存结果。
- `capture_per_item_errors`：单项失败不影响整个批次继续执行。
- `emit_progress`：长批处理过程中输出进度。

服务商实际 RPM/TPM 限制和用户指令优先于默认值。
