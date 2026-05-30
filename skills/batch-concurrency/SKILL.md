---
name: batch-concurrency
description: Use for tasks with many independent samples, remote model API calls, HTTP requests, videos, texts, files, embeddings, evaluations, dataset processing, CPU-heavy loops, multiprocessing, async concurrency, throughput optimization, RPM/TPM limits, or resource utilization. Guides bounded concurrency, multiprocessing, result ordering, retries, and rate-limit-aware remote model calls.
---

# Batch Concurrency

[中文版](SKILL.zh.md)

## Shared Defaults

Read `../_shared/agent-execution-defaults.json` first. Use `remote_model_api`, `parallel_programming`, and `async_programming` defaults unless the user or API provider gives specific limits.

## Core Workflow

1. Prove one item works end to end.
2. Convert to bounded concurrency or multiprocessing.
3. Preserve result order with input indexes.
4. Capture per-item errors without dropping the whole batch.
5. Add bounded retry/backoff.
6. Save partial results for long jobs.
7. Emit progress.

## Remote Model APIs

For LLM/video/text model APIs, follow the FairGamer `Competition.py` pattern: use async tasks, a shared result queue or indexed result array, RPM token bucket gating, and sort or assign results by task id.

Add TPM control too:

- Estimate tokens before each request using tokenizer counts when available.
- Otherwise use `default_prompt_token_estimate + max_tokens`, multiplied by `token_safety_margin`.
- Acquire one request token from an RPM bucket and estimated token units from a TPM bucket before sending.
- On provider responses with actual token usage, record actuals and tune estimates for later calls.
- On 429/rate-limit errors, respect `Retry-After`; otherwise use bounded exponential backoff with jitter.

Skeleton policy:

```python
await rpm_bucket.acquire(1)
await tpm_bucket.acquire(estimated_prompt_tokens + max_tokens)
result = await call_model(item)
results[index] = result
```

## CPU-Bound Local Work

Use multiprocessing for Python CPU-bound work when practical. Default to 16 processes from shared config, then reduce if memory, I/O, or machine load requires it.

Prefer lock-free designs:

- `ProcessPoolExecutor.map` for ordered outputs.
- return `(index, result)` from workers and sort once.
- write per-process temp files and merge after completion.
- avoid shared mutable state and hot locks.

Use locks only for correctness-critical shared resources. A fast parallel program with lock contention is often just a slower serial program wearing a disguise.

## When Not To Parallelize

Stay serial if the item count is tiny, the single-item path is unproven, the API requires serial order, or rate/cost limits make concurrency harmful.
