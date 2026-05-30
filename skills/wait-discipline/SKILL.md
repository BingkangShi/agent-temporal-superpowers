---
name: wait-discipline
description: Use when writing, reviewing, or running code that waits, sleeps, polls, retries, watches services, handles queues, rate limits, dev server startup, async jobs, or mentions sleep 300/sleep 500/不要等待/不要浪费时间. Enforces bounded condition-based waiting using shared JSON defaults.
---

# Wait Discipline

## Shared Defaults

Read `../_shared/agent-execution-defaults.json` first. Use `wait_discipline` defaults unless task context or user instructions require different values.

## Rules

- Do not use hidden multi-minute sleeps in an interactive agent turn.
- Do not add unconditional long sleeps.
- Every wait loop must have an overall timeout.
- Every sleep must sit between condition checks.
- Prefer short local polling intervals, then exit immediately when ready.
- Use API-provided `Retry-After` or rate-limit metadata when available.

Bad:

```bash
sleep 300
```

Good:

```bash
timeout 30s sh -c 'until curl -fsS http://localhost:3000/health; do sleep 1; done'
```

Python pattern:

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

Before preserving any sleep, verify it is necessary for correctness rather than habit.
