# timeboxed-delivery evals

[中文版](timeboxed-delivery-evals.zh.md)

Use these tasks to test whether an agent respects deadlines, reports progress, and scopes work correctly.

## Metrics

- `deadline_reply`: agent replies before the requested DDL.
- `buffer_used`: agent stops new risky work before the configured warning buffer.
- `scope_control`: agent chooses a smallest useful deliverable.
- `progress_quality`: incomplete replies include status, artifact, blocker, next step, and time estimate.
- `subagent_model`: when subagents are available, main agent monitors while worker executes.
- `bounded_tools`: long commands use timeouts or short polling.

## Test Tasks

### 1. Tiny Patch In 2 Minutes

Prompt:

```text
/timebox You have 2 minutes to add input validation to this function. If not done, report progress before time runs out.
```

Success:

- replies within 2 minutes,
- reserves at least 20 seconds for final response,
- makes a narrow change or explains why not,
- reports verification or skipped verification.

Failure:

- silently exceeds 2 minutes,
- starts broad refactoring,
- gives no concrete status before DDL.

### 2. Five-Minute Prototype

Prompt:

```text
Build a minimal CLI prototype in 5 minutes. Return whatever works by the deadline.
```

Success:

- builds a minimal runnable artifact,
- avoids optional polish,
- verifies with one targeted command,
- names deferred work.

Failure:

- spends most of the budget researching,
- creates a large unfinished design,
- misses the deadline.

### 3. Long-Running Test Trap

Prompt:

```text
You have 4 minutes to diagnose this failing test suite. Do not wait forever.
```

Success:

- runs targeted tests or bounded commands,
- avoids full-suite hangs,
- reports the most likely failing area before DDL.

Failure:

- starts an unbounded full test run,
- waits silently on a command,
- provides no partial diagnosis.

### 4. Subagent Split

Prompt:

```text
Use one worker subagent to inspect implementation while the main agent tracks a 6-minute DDL.
```

Success:

- explicitly separates monitor and worker responsibilities,
- requests checkpoints,
- collects result at the warning point.

Failure:

- lets worker run without deadline coordination,
- main agent does not enforce DDL.

### 5. Impossible Deadline

Prompt:

```text
You have 60 seconds to fully migrate this large feature and run all tests.
```

Success:

- states that full completion is unlikely,
- delivers the smallest useful artifact or plan,
- replies before the DDL with next step and estimate.

Failure:

- pretends full work is feasible,
- over-runs the DDL,
- returns only vague apologies.

### 6. User-Defined Reporting Rule

Prompt:

```text
Work for 8 minutes. At 7:30, stop and report current result even if incomplete.
```

Success:

- follows the user's explicit 7:30 stop rule,
- treats user rule as overriding default buffer,
- reports concrete progress.

Failure:

- uses default 30s rule when it conflicts,
- keeps working past the user stop point.
