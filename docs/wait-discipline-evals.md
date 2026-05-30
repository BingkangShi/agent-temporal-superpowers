# wait-discipline evals

[中文版](wait-discipline-evals.zh.md)

Use these tasks to test whether an agent replaces blind waiting with bounded, condition-based waiting.

## Metrics

- `no_blind_sleep`: no unconditional long sleep is introduced or preserved.
- `overall_timeout`: every polling loop has a total deadline.
- `condition_check`: waits check readiness or external state between intervals.
- `retry_after`: API retry metadata is respected when available.
- `fast_exit`: loop exits immediately when condition is satisfied.
- `interactive_bound`: agent does not hide multi-minute waits in an interactive turn.

## Test Tasks

### 1. Remove `sleep 300`

Prompt:

```text
Review this deployment script and replace sleep 300 with a better readiness wait.
```

Success:

- replaces blind sleep with a condition check,
- adds an overall timeout,
- uses short polling.

Failure:

- keeps `sleep 300`,
- changes it to another blind long sleep,
- adds no timeout.

### 2. Dev Server Startup

Prompt:

```text
Start a local dev server and wait until it is ready without wasting time.
```

Success:

- probes a health endpoint or port,
- uses short polling and timeout,
- stops polling as soon as ready.

Failure:

- uses a fixed large sleep,
- assumes readiness without checking,
- waits silently for minutes.

### 3. API Rate Limit

Prompt:

```text
Handle HTTP 429 responses from an API that returns Retry-After.
```

Success:

- reads and follows `Retry-After`,
- caps retry attempts,
- emits useful retry diagnostics.

Failure:

- ignores `Retry-After`,
- retries in a tight loop,
- sleeps indefinitely.

### 4. Queue Worker Polling

Prompt:

```text
Poll a background job until completion.
```

Success:

- polls job status,
- exits on done/failed states,
- has an overall timeout.

Failure:

- sleeps once for a guessed duration,
- never checks failed state,
- can hang forever.

### 5. Test Timeout Behavior

Prompt:

```text
Write a test for timeout behavior that uses sleep.
```

Success:

- uses the shortest reliable sleep,
- isolates the timing-sensitive test,
- avoids making the whole suite slow.

Failure:

- uses multi-second sleeps where milliseconds would work,
- creates flaky timing assumptions,
- slows unrelated tests.

### 6. Watcher Debounce

Prompt:

```text
Implement a file watcher debounce.
```

Success:

- uses a small debounce interval,
- coalesces events,
- does not block the main loop unnecessarily.

Failure:

- uses large blocking sleep,
- drops events incorrectly,
- prevents shutdown or cancellation.
