# batch-concurrency evals

[中文版](batch-concurrency-evals.zh.md)

Use these tasks to test whether an agent chooses efficient bounded concurrency, preserves correctness, and respects API/resource limits.

## Metrics

- `single_item_first`: one item is proven before scaling.
- `bounded_concurrency`: concurrency is limited and configurable.
- `order_preserved`: output order matches input order.
- `per_item_errors`: individual failures are captured without losing the batch.
- `rpm_respected`: requests-per-minute limit is enforced.
- `tpm_respected`: tokens-per-minute limit is estimated and enforced.
- `partial_results`: long jobs save checkpoints.
- `multiprocessing_used`: CPU-bound Python uses process-based parallelism when suitable.
- `lock_contention_avoided`: design avoids hot shared locks.

## Test Tasks

### 1. 200 Remote Text Samples

Prompt:

```text
Process 200 text samples with a remote model API. Preserve order and respect 100 RPM.
```

Success:

- runs or sketches one-sample proof,
- uses bounded async concurrency,
- uses RPM token bucket,
- returns ordered results.

Failure:

- writes only serial loop,
- launches unbounded tasks,
- loses ordering.

### 2. Add TPM Limit

Prompt:

```text
Use an API with 100 RPM and 200k TPM. Each request has variable prompt length.
```

Success:

- estimates prompt and completion tokens,
- applies TPM bucket before sending,
- adjusts estimates from actual usage if available.

Failure:

- only handles RPM,
- ignores max completion tokens,
- treats all requests as equal token cost.

### 3. Partial Result Recovery

Prompt:

```text
Run a 5,000-item model evaluation that may take hours.
```

Success:

- saves partial results periodically,
- can resume or skip completed items,
- records per-item error state.

Failure:

- stores everything only in memory,
- loses all progress on interruption,
- retries the whole batch after one failure.

### 4. CPU-Bound Local Work

Prompt:

```text
Compute CPU-heavy features for 20,000 files.
```

Success:

- uses multiprocessing by default,
- starts from 16 processes or config default,
- avoids shared hot locks,
- preserves output association with input files.

Failure:

- uses Python threads for CPU-bound work without reason,
- writes lock-heavy shared state,
- gives nondeterministic output order without indexes.

### 5. Mixed Pipeline

Prompt:

```text
Upload files, call a remote model, then run local CPU post-processing.
```

Success:

- separates network/API and CPU stages,
- bounds each resource independently,
- uses queues/backpressure if needed.

Failure:

- uses one global unbounded concurrency value,
- overloads memory or API,
- blocks CPU workers on network waits.

### 6. Provider 429 Storm

Prompt:

```text
The provider starts returning frequent 429 errors during a batch run.
```

Success:

- respects `Retry-After`,
- lowers effective concurrency or waits through buckets,
- keeps completed results,
- reports rate-limit state.

Failure:

- retries immediately,
- increases concurrency,
- discards successful work.

### 7. Tiny Batch

Prompt:

```text
Process 3 tiny local files.
```

Success:

- keeps implementation simple,
- does not add unnecessary multiprocessing,
- still preserves error handling.

Failure:

- over-engineers a worker pool,
- adds complex rate-limit machinery with no benefit.
