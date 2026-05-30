# batch-concurrency

[中文版](batch-concurrency.zh.md)

## Purpose

Use this skill for many independent items: remote model API calls, text/video samples, embeddings, HTTP requests, file batches, evaluations, CPU-heavy loops, or multiprocessing tasks.

## Usage

Typical prompts:

```text
Process these 200 samples with bounded concurrency and preserve order.
```

```text
Use Gemini/OpenAI API for this dataset without exceeding RPM or TPM limits.
```

The agent should:

- prove one item works first,
- switch to bounded concurrency or multiprocessing,
- preserve output order with indexes,
- capture per-item errors,
- retry with bounded backoff,
- save partial results for long jobs,
- emit progress.

## JSON Parameters

Configured in `skills/_shared/agent-execution-defaults.json`.

### `remote_model_api`

- `default_concurrency`: default concurrent remote API calls.
- `max_concurrency_without_user_approval`: upper bound before asking or requiring explicit user/provider support.
- `default_rpm_limit`: default requests-per-minute bucket size.
- `default_tpm_limit`: default tokens-per-minute bucket size.
- `token_bucket_interval_seconds`: bucket refill window.
- `default_prompt_token_estimate`: fallback prompt token estimate when no tokenizer is available.
- `default_completion_token_estimate`: fallback completion estimate.
- `token_safety_margin`: multiplier to avoid undercounting TPM usage.
- `retry.max_attempts`: maximum attempts per item.
- `retry.initial_backoff_seconds`: first retry delay.
- `retry.max_backoff_seconds`: retry delay cap.
- `retry.jitter_fraction`: randomization to avoid synchronized retries.
- `persist_partial_results_every_n_items`: checkpoint frequency.
- `preserve_order`: keep output aligned with input order.

### `parallel_programming`

- `default_processes`: default process count for CPU-bound multiprocessing.
- `prefer_multiprocessing_for_cpu_bound_python`: prefer processes over threads for Python CPU-bound work.
- `prefer_lock_free_result_collection`: avoid shared mutable state and hot locks.
- `leave_cpu_headroom_processes`: keep some CPU capacity free.
- `chunk_size_strategy`: default chunk sizing guidance.

### `async_programming`

- `default_concurrency`: default concurrency for non-model async I/O.
- `preserve_order_with_indexes`: store results by input index.
- `capture_per_item_errors`: keep batch running when one item fails.
- `emit_progress`: report progress during long batches.

Provider-specific RPM/TPM limits and user instructions override defaults.
