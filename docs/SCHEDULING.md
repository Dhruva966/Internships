# Scheduled discovery and application work

**This repository does not install a cron job or enable a live schedule.** A setup agent creates one only after intake, authorization and dry-run tests. Ask the user's timezone, cadence, allowed hours, per-run time/token budget, application limits and notification preference; record them privately.

## Choose the execution environment honestly

| Option | Appropriate use | Prerequisites / limits |
| --- | --- | --- |
| Codex/ChatGPT desktop scheduled task | Agent research plus local Neo browser work | Confirm available scheduling features, tools, local folder access and an available configured host. |
| Local cron / OS scheduler | Invoke an installed, tested agent runner | Verify that runner's current documented command, authentication, MCP and private-state access. No runner is bundled here. |
| GitHub Actions | Documentation validation; separately implemented public discovery code | Hosted jobs do not inherit the laptop's Neo session or local résumé. A YAML schedule alone is not an application worker. |
| Dedicated remote host | A deliberately deployed worker | Separate browser/agent setup, secure private state, permissions, monitoring and a single active owner are required. |

The included GitHub workflow validates this playbook on pushes/PRs. It is **not** a daily search or application workflow. Don't rename its green check as a successful live dry run.

## Recommended initial schedule

After the user chooses times: one daily discovery/change-monitor pass and a bounded application pass using the same private queue. A same-chat recurring task can preserve context; a standalone task must load the private manifest and state each time. Do not let two schedules independently submit the same role. Use a shared lease and one write coordinator.

Faster checks can be limited to a small watchlist around explicitly published opening dates. Don't promise first-hour coverage from a once-daily run. An unknown opening date remains unknown. Respect site limits and back off on failures.

## Create through the host's supported scheduler

1. Inspect existing schedules so this isn't a duplicate.
2. Manually run [the daily prompt](../prompts/DAILY_RUN.md) in dry-run mode using the actual connected tools.
3. Verify gates and a durable checkpoint, and obtain the user's requested cadence and scope.
4. Use the scheduling mechanism exposed by the agent product, not invented tool calls or hand-written internal config. Adapt to the current UI/API. If only an OS scheduler is available, test its documented agent command first and present the exact proposed schedule before installation.
5. Verify the saved prompt, timezone, enabled state, next run, destination and scheduler ID. Review the first real run. Record how to pause/disable it.
6. Stay quiet when nothing actionable changes. Notify on newly eligible/opened roles, meaningful deadlines, successful submissions, failures or genuinely new user actions. Do not repeatedly notify for the same unresolved blocker.

## Required run behavior

- Load and validate private profile/answer versions, queue and checkpoint.
- Acquire exclusive worker ownership and enforce per-run budget; if locked, exit without a second browser writer.
- Recheck due sources, discover new ones within the coverage plan, classify dates precisely, merge deltas, and refresh the tracker/question bank.
- Apply only if enabled and all gates pass. Otherwise prepare reviewed drafts or blockers.
- Persist `last_successful_check`, changed records, next due sources and receipt reconciliation work. A failed check is not a successful empty scan and does not turn a role into closed.
- When time/budget expires, checkpoint and stop. A long outage should produce one meaningful failure notice, not a flood. No busy-wait polling.

## Portability

Git transports the instructions and synthetic templates. The new host needs fresh authenticated connections and approved access to private state. Do not copy browser cookies into the repository. Disable the previous host before enabling submissions on the new host. Test reconciliation and duplicate prevention after migration.

## Official product reference

Read the current [OpenAI scheduled-task documentation](https://learn.chatgpt.com/docs/automations?surface=app) during setup. As checked October 19, 2026, local-file tasks require the computer and desktop app to be running; web tasks don't directly operate a local folder. Verify current product availability rather than hard-coding assumptions. Other agents have their own scheduler requirements.
