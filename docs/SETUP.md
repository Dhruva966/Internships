# Set up or move to another computer

This is an installation procedure for an agent, not evidence that installation has happened.

## 1. Establish tools and private storage

Ask the user to open this repository in their preferred coding agent. Explain any product/account costs before enabling paid services. No particular model or API key is required by this playbook; use the agent they already have and verify its capabilities.

Ask them to install BrowserOS Neo from the [official BrowserOS website](https://browseros.com/) and follow its current connection instructions. Confirm the domain and current documentation rather than installing a random extension, package, or copied MCP endpoint. Connect the agent through the browser's supported MCP connection flow. Test a harmless page read, session naming, fresh snapshot, and compact result. If tools are missing/disconnected, report that; never silently switch browsers.

Connect the user's chosen spreadsheet/document provider with the minimum required permissions. Prefer native Google Sheets/Docs connectors if available. If unavailable, use private local CSV/Markdown initially and report the limitation instead of inventing cloud links. Sharing defaults are private unless that user specifies otherwise.

Choose an absolute private runtime directory outside this checkout, accessible to the scheduled worker. Record it in the private setup manifest, not a public README. Store:

- approved profile and résumé inventory with hashes;
- roles and evidence, company scan queue, application event ledger;
- question instances, approved answer versions, story bank;
- checkpoints, worker ownership/leases, consent scope, receipts and blockers.

Choose JSON/CSV for a single coordinator or SQLite if concurrent durable writers are actually implemented. The provided single-host lock, atomic JSON writer and append-only ledger are described in [STATE_AND_RECOVERY.md](STATE_AND_RECOVERY.md). They do not implement a browser worker or distributed database.

## 2. Intake before searching

Follow [INTAKE.md](INTAKE.md). First ask a new applicant for **all résumé versions**. For an existing applicant, reuse their confirmed résumé/profile and ask only for changes or missing facts. Extract facts with provenance, then ask 1–3 useful questions at a time. Confirm hard filters and application authorization. Never inherit another person's answers from an example.

## 3. Import prior applications, if any

Ask for an existing tracker and the smallest relevant confirmation evidence. Merge by employer/requisition, not title similarity alone. Preserve submissions even when a listing closes. Uncertain submission becomes `submission_unknown`; don't reapply until reconciled. Select one canonical tracker and map old views into it. Avoid repeatedly scanning full history.

## 4. Baseline research and short answers

Follow [RESEARCH.md](RESEARCH.md), [TRACKER.md](TRACKER.md), and [SHORT_ANSWERS.md](SHORT_ANSWERS.md). Partition independent research among supported subagents; otherwise run the same bounded partitions sequentially. A coordinator validates and merges evidence. Collect public form prompts without transmitting applicant data. An inaccessible form is logged as unknown, not declared essay-free.

## 5. Dry run and application authorization

After initial research, start short-answer preparation with the applicant while processing eligible roles with no substantive written questions. Research continues incrementally. Optional substantive essays belong in the answer lane, and one writer owns all application actions. Do not wait for the entire research inventory or every essay to be finished before progressing an independently ready role.

Follow [QUALITY_GATES.md](QUALITY_GATES.md). Start in review-only mode. Show the user a small, high-fit queue and one fully reviewed draft. Establish exact data destinations, permitted application classes, employer caps, required confirmations, and answer approvals. A cap is a maximum, not a target. Do not turn on submissions merely because discovery is enabled.

## 6. Schedule, verify, and hand over

Follow [SCHEDULING.md](SCHEDULING.md). Ask timezone, cadence, daily work/token budget and notification preference. Avoid creating a duplicate schedule. Test a manual run, create the supported schedule only when requested, and verify the saved schedule plus a run record. Record host, schedule ID, private state location, next run and how to disable it. A laptop/browser-dependent application worker needs the configured host available.

## Migration checklist

1. Clone this documentation repository on the new host.
2. Transfer the user's approved **private** state through a separately approved secure method; never commit it to make migration convenient.
3. Reconnect accounts and Neo locally; browser cookies and passwords do not travel in Git.
4. Revalidate file paths, résumé hashes, available tools, timezone and sharing settings.
5. Disable the old worker/schedule or transfer exclusive ownership. Prevent two computers applying to the same role.
6. Reconcile any `submitting` or `submission_unknown` ledger entries before retrying anything.
7. Run the dry-run acceptance suite, then enable one scheduler. Verify a real run and the next scheduled run.
