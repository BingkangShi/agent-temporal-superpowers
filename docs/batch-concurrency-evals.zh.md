# batch-concurrency 评估

[English](batch-concurrency-evals.md)

用这些任务测试 Agent 是否会选择高效的有界并发，在保证正确性的同时遵守 API 和资源限制。

## 指标

- `single_item_first`：扩展前先跑通单项。
- `bounded_concurrency`：并发有上限且可配置。
- `order_preserved`：输出顺序与输入顺序一致。
- `per_item_errors`：单项失败被记录，不丢失整个批次。
- `rpm_respected`：执行 RPM 限制。
- `tpm_respected`：估算并执行 TPM 限制。
- `partial_results`：长任务保存 checkpoint。
- `multiprocessing_used`：适合时 CPU-bound Python 使用进程并行。
- `lock_contention_avoided`：避免高频共享锁竞争。

## 测试任务

### 1. 200 个远端文本样本

提示：

```text
Process 200 text samples with a remote model API. Preserve order and respect 100 RPM.
```

成功：

- 跑通或设计单样本 proof，
- 使用有界 async 并发，
- 使用 RPM token bucket，
- 返回有序结果。

失败：

- 只写串行循环，
- 启动无界任务，
- 丢失顺序。

### 2. 添加 TPM 限制

提示：

```text
Use an API with 100 RPM and 200k TPM. Each request has variable prompt length.
```

成功：

- 估算 prompt 和 completion token，
- 请求前应用 TPM bucket，
- 可用时从真实 usage 调整估算。

失败：

- 只处理 RPM，
- 忽略 max completion tokens，
- 把所有请求视为同等 token 成本。

### 3. Partial result 恢复

提示：

```text
Run a 5,000-item model evaluation that may take hours.
```

成功：

- 定期保存 partial results，
- 可恢复或跳过已完成 item，
- 记录单项错误状态。

失败：

- 所有结果只存在内存，
- 中断后丢失全部进度，
- 一个失败后重跑整个批次。

### 4. CPU-bound 本地工作

提示：

```text
Compute CPU-heavy features for 20,000 files.
```

成功：

- 默认使用多进程，
- 从 16 进程或配置默认值开始，
- 避免共享热锁，
- 保持输出和输入文件的对应关系。

失败：

- 无理由使用 Python 线程处理 CPU-bound 工作，
- 写出锁竞争严重的共享状态，
- 不用 index 导致输出顺序不确定。

### 5. 混合 pipeline

提示：

```text
Upload files, call a remote model, then run local CPU post-processing.
```

成功：

- 分离网络/API 和 CPU 阶段，
- 分别限制每类资源，
- 需要时使用队列/backpressure。

失败：

- 使用一个全局无界并发值，
- 压爆内存或 API，
- 让 CPU worker 阻塞在网络等待上。

### 6. 服务商 429 风暴

提示：

```text
The provider starts returning frequent 429 errors during a batch run.
```

成功：

- 遵守 `Retry-After`，
- 降低有效并发或通过 bucket 等待，
- 保留已完成结果，
- 报告 rate-limit 状态。

失败：

- 立即重试，
- 增加并发，
- 丢弃成功结果。

### 7. 很小批次

提示：

```text
Process 3 tiny local files.
```

成功：

- 保持实现简单，
- 不添加不必要的多进程，
- 仍保留错误处理。

失败：

- 过度设计 worker pool，
- 添加没有收益的复杂限流机制。
