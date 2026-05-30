# wait-discipline

## Purpose

Use this skill when code or agent actions involve waiting, sleeping, polling, retries, queue checks, service startup, or rate-limit delays. It prevents pointless long waits such as `sleep 300` without a condition.

## Usage

Typical prompts:

```text
Review this script and remove pointless sleeps.
```

```text
Start the dev server, but do not wait blindly.
```

The agent should:

- avoid unconditional long sleeps,
- use condition-based polling,
- set an overall timeout,
- check readiness between sleeps,
- respect provider `Retry-After` headers when present.

## JSON Parameters

Configured in `skills/_shared/agent-execution-defaults.json` under `wait_discipline`.

- `max_unconditional_sleep_seconds`: maximum acceptable unconditional sleep.
- `max_sleep_seconds_without_user_or_api_reason`: longer sleeps need a clear user/API reason.
- `default_local_poll_interval_seconds`: normal local polling interval.
- `max_local_poll_interval_seconds`: maximum local polling interval.
- `default_wait_timeout_seconds`: default total timeout for wait loops.
- `require_condition_check_between_sleeps`: every repeated sleep must check state.
- `require_overall_timeout_for_polling`: polling must have a total deadline.
- `ban_hidden_multi_minute_sleep`: disallow hidden multi-minute waits in interactive work.

Task-specific service startup times or API rate limits may override these defaults.
