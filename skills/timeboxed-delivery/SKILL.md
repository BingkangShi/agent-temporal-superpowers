---
name: timeboxed-delivery
description: Use when the user gives a deadline, time budget, impatience constraint, or phrases like /timebox, /timeboxed, within N minutes, report progress by, ddl, 限定时间, 限时完成, N分钟内完成, 不要超时. Guides the agent to finish or report progress before the deadline, ideally with a main-agent monitor and a worker subagent when the app supports subagents.
---

# Timeboxed Delivery

## Shared Defaults

Read `../_shared/agent-execution-defaults.json` first. Use `timeboxed_delivery` defaults unless the user gives stricter or looser parameters.

## Execution Model

If the Agent App supports subagents or background workers:

1. Keep the main agent responsible for the timer, deadline checks, progress collection, and final user reply.
2. Dispatch a worker subagent for the concrete implementation, investigation, or batch task.
3. Require checkpoints from the worker before `max_silent_work_seconds`.
4. At `default_deadline_warning_seconds` before the DDL, stop expanding scope and collect the best available result.
5. Reply before the deadline with result, progress, or blocker.

If subagents are unavailable, simulate the same behavior: track the DDL internally, use short tool calls, and stop new risky work before the response buffer.

## Work Strategy

- Treat the time limit as a hard requirement.
- Pick the smallest useful deliverable first.
- Avoid broad exploration and optional refactors.
- Prefer bounded commands and targeted tests.
- If incomplete, return current status, concrete artifact, blocker, next step, and estimated extra time.

Do not silently exceed the user's DDL to chase a nicer answer.
