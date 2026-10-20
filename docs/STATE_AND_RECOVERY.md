# Private state and recovery contract

These templates make setup deterministic without publishing applicant data. Copy the example manifest, profile, empty ledger and checkpoint into a **private directory outside this repository**, replace examples, and create `roles.json` from the canonical tracker using role IDs. Do not copy the worker-lock example into the active lock path.

## Required files

| File | Required contents |
| --- | --- |
| manifest.json | Installation ID, one owner host, absolute private root, the five file paths, canonical tracker/question-bank IDs, tool readiness, sharing policy, budgets and saved schedule ID/timezone/cadence/test evidence. |
| profile.json | Approved facts with provenance, résumé hashes/selection rules, shared answers, submission scope and company caps. |
| roles.json | Role records matching `roles.example.csv` fields. Keep exact IDs, aliases, sources and confirmed receipts. |
| ledger.json | Append-only event list. Each event has event_id, role_id, status, at and evidence. Keep résumé/answer versions in the linked private receipt. |
| checkpoint.json | Run attempts/success/failure separately, source cursor, due sources, pending roles, reconciliation IDs, unsynced tracker IDs and notified change IDs. |
| worker.lock.json | Created exclusively at run start: owner run ID, process ID and acquired_at. Existence blocks a second worker. Never synthesize this from the example. |

JSON dates/timestamps are ISO8601 with timezone for instants. Unknown private JSON fields are null; CSVs use documented `unknown` sentinels. The empty example is not a completed installation. `validate_manifest` verifies minimum structure, not account readiness.

## Permanent application history

An authoritative `submitted` event and the role's `submission_confirmed_at` plus `confirmation_evidence` establish **ever applied**. Those facts are immutable. `interview`, `rejected`, `offer` and `withdrawn` are later workflow events, not permission to reapply. Views, green highlighting, company counts and duplicate checks use receipt history, never equality with the current status string alone. Submitted records remain green/bottom even after the listing closes.

Import verified historic receipts before starting the worker. Ambiguous historical submissions become `submission_unknown`; never fabricate a receipt date. Resolve them before retrying.

## Single-host writer protocol

`scripts/workflow_contract.py` provides `WorkerLock`, `Ledger` and `atomic_json` reference primitives. One coordinator owns all application and tracker writes. Acquire WorkerLock before creating Ledger or editing private state; lock acquisition uses exclusive file creation. A second owner exits without touching the browser. Ledger writes use a temporary file, flush/fsync and atomic replacement. These primitives do not implement Google Sheets transactions or multi-host distributed locks.

Before the browser's final action, persist `submitting` and exact role/answer/résumé context. When the employer returns a verified receipt, persist `submitted`, synchronize role receipt fields and then update the spreadsheet. If the Sheet write fails, keep the receipt and add the role to `tracker_sync_pending_role_ids`. Retry only the tracker write, never Submit. Mark success only after read-back.

An email code or pending challenge becomes `verification_pending`. If a browser/network failure makes the result uncertain, persist `submission_unknown`. Both block a new attempt. Only authoritative employer evidence of **non-receipt** permits `reconcile_not_received` back to draft; retain that evidence in the event list. Merely not seeing an email is insufficient.

## Failure and stale lock recovery

1. Stop this installation's scheduling or establish that no scheduled/browser writer is active.
2. Inspect the recorded host/process and current process state. A timestamp or timeout alone does not prove the owner stopped. Never auto-steal a lock because it is old.
3. Preserve the lock and ledger for diagnosis. If the ledger is malformed, stop; recover from a verified backup rather than replacing it with an empty file.
4. Inspect every `submitting`, `verification_pending` and `submission_unknown` role against employer/receipt evidence. Keep unresolved ones blocked.
5. Only after the owner is confirmed inactive, archive the stale lock to a private recovery folder and acquire a new exclusive lock. Record who recovered it and why.
6. Reconcile tracker-sync work before new applications. Advance the source cursor only for completed checks; failed checks keep a retry/backoff entry and must not silently mark roles closed.
7. Run a bounded dry run, checkpoint the result and re-enable the single scheduler.

For a new computer, disable the old scheduler and browser writer before transferring approved private state. A local lock does not coordinate two different disks; one-host ownership is required until a genuine shared transactional store is implemented.

## Parallel lanes, not parallel submission writers

After résumé/profile approval and initial research, begin two lanes immediately: (A) extract and discuss required/optional short answers; (B) process verified roles with **no substantive written prompts**, including optional prompts. Do not wait for every research partition or answer to finish before lane B starts. Researchers may run in parallel; the single application writer consumes ready records from either lane. An unanswered optional essay belongs in lane A, not a fast-lane omission.
