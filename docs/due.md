# due

[中文版](due.zh.md)

## Purpose

Use this skill when the user gives a deadline, time budget, DDL, or progress-report requirement. It helps the agent treat time as a hard requirement instead of silently working past the user's limit.

## Usage

Typical prompts:

```text
/timebox finish this in 5 minutes
```

```text
You have 10 minutes. If unfinished, report progress before the DDL.
```

The agent should:

- compute the deadline and response buffer,
- keep the main agent responsible for monitoring time,
- use a worker subagent when available,
- stop expanding scope near the DDL,
- return the best result or progress before time runs out.

## JSON Parameters

Configured in `skills/_shared/agent-execution-defaults.json` under `timeboxed_delivery`.

- `default_deadline_warning_seconds`: when to stop risky work and prepare the reply.
- `short_task_response_buffer_seconds`: final reply buffer for very short tasks.
- `medium_task_response_buffer_seconds`: final reply buffer for medium tasks.
- `long_task_response_buffer_fraction`: fraction reserved for long tasks.
- `long_task_response_buffer_max_seconds`: maximum long-task reply buffer.
- `max_silent_work_seconds`: maximum time before emitting progress/checkpoint.
- `prefer_subagent_execution_when_available`: prefer main-agent monitor plus worker-agent execution.
- `main_agent_role`: default responsibility of the monitoring agent.
- `worker_agent_role`: default responsibility of the task execution agent.

User-provided deadlines override these defaults.
