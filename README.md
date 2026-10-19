# Internship-Dash-Applier

A portable, README-first operating system for an agent-assisted internship search: résumé-first intake → parallel verified research → a clean tracker and short-answer bank → daily change monitoring → careful BrowserOS Neo applications.

**This is an agent playbook, not an installed job scraper or an autonomous application bot.** Cloning it does not create a schedule, connect accounts, or submit applications. A compatible coding agent follows the instructions, connects the user's tools, creates private state, tests the workflow, and only then creates the requested schedule. No model API subscription is assumed beyond the chosen agent's own requirements.

## Start in a fresh agent chat

Clone/download this repository, open its folder in your coding agent, and paste:

> Read AGENTS.md and docs/SETUP.md, then set up Internship-Dash-Applier for me. Start by asking for all versions of my résumé. Do not assume you know my background, preferences, availability, or permissions. Use adaptive intake, verify role eligibility and actual application dates, research in parallel where supported, collect exact required and optional short-answer prompts, and create a clean private tracker. Show a dry run before scheduling. Use BrowserOS Neo for applications. Do not submit anything until we establish the application authorization policy and all quality gates pass.

The agent should **ask for your résumé first**, extract what is already known, then ask only useful follow-ups. It should not dump a 50-question form or ask the same question for every employer.

## What you get after setup

- An approved applicant profile, evidence-backed story bank, and selected résumé variants stored privately.
- One **Internships** master list: all active leads and submitted applications, with submitted rows at the bottom in very light green; remaining rows in very light red.
- **Deferred — Closed & Ineligible** for confirmed closed listings and hard eligibility mismatches. Unknown pay or dates are holds, not automatic disqualifications.
- **Application Blockers** containing only unresolved holds, grouped by owner and next action. Resolved responses belong in the private profile/answer bank, not as permanent blocker rows.
- A **Short-Answer Bank** document with exact prompts, company/role labels, limits, required/optional status, drafts, and per-answer approval.
- A daily changes summary: newly opened roles, upcoming openings, verified deadlines, closures, and unknown dates newly resolved.
- An application worker that uses approved information, holds uncertain fields, verifies receipts, and updates the ledger immediately. Speed never outranks accuracy or answer quality.

## Reading order

1. [Setup and migration](docs/SETUP.md)
2. [Résumé-first intake](docs/INTAKE.md)
3. [Parallel research and daily monitoring](docs/RESEARCH.md)
4. [Tracker and private state](docs/TRACKER.md)
5. [Short-answer collection and approval](docs/SHORT_ANSWERS.md)
6. [BrowserOS Neo application worker](docs/APPLY.md)
7. [Scheduling](docs/SCHEDULING.md)
8. [Quality gates and acceptance tests](docs/QUALITY_GATES.md)
9. [Security and sharing](SECURITY.md)

Reusable run prompts live in [prompts/](prompts/BOOTSTRAP.md). Synthetic templates live in [templates/](templates/profile.example.json). The only executable code is an offline repository check: `python3 scripts/check_playbook.py`.

## Important boundaries

- Public GitHub hosts the **method**, not an applicant's résumé, passwords, private answers, contact information, or application history.
- A daily GitHub Actions schedule does not magically control a signed-in browser on a laptop. Use an appropriately configured local agent worker for Neo. See [Scheduling](docs/SCHEDULING.md).
- Research coverage is documented, never claimed to be every internship on the internet. Official dates may remain unknown.
- Applying early can help with rolling review; it does not guarantee selection. Do not infer opening dates from first discovery or treat metadata expiry as a recruiting deadline.
- Required confirmations and human handoffs depend on the agent/platform and employer. This playbook cannot override them.

## Development status

The playbook and example templates are reusable. Live connectors, an applicant's intake, a baseline audit, scheduled runs, and submission authority must be configured and verified per installation. No live scheduler or applicant-data database is bundled.
