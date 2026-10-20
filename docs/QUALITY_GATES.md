# Quality gates and acceptance tests

No gate is satisfied by intent, a plausible summary, or a checkbox in a README. Keep actual evidence in the private run record.

## Before research publication

- Profile is applicant-approved; every hard filter has a value or an explicit unknown.
- Résumé variants have hashes and purpose. Built, in-progress, planned, projected and measured claims are distinguished.
- Official role ID, current availability, location, term, pay and hard requirements are verified or visibly unknown. Preferred requirements are not treated as mandatory.
- Dates are labelled by meaning and source. Discovery time, posting time and metadata expiry never become invented opening/deadline dates.
- All records pass canonical-ID dedupe against current and historical applications.
- Coverage log lists sources searched, failures and gaps; there is no unsupported claim of exhaustive coverage.

## Before each submission

1. Applicant authorizes this application/data destination and required platform confirmations are satisfied.
2. Exact role is open and eligible; unresolved hard-filter facts hold the application.
3. No prior submitted/unknown/in-flight record; stricter employer/user company limits respected.
4. Correct approved résumé is actually attached, not merely selected in a file chooser.
5. All factual answers are supported and apply to this wording; no invented GPA, date, credential, reference or sponsorship answer.
6. Required **and substantive optional** essays are specific, truthful, within limits and approved for this use. Unknown prompts/assessment assistance hold the application.
7. Final retained values, dropdowns and uploads are reviewed. No stale auto-filled values or silent resets remain.
8. Final action is authorized; official receipt is verified before `submitted` is written. Email verification is pending, not success.

## Acceptance scenarios (run on synthetic fixtures / safe dry runs)

| Scenario | Required result |
| --- | --- |
| Fresh applicant, no context | First question requests all résumé versions; subsequent questions reuse extracted facts. |
| No college GPA | Record unknown/not yet available; never use high-school GPA or zero as a substitute. |
| Junior-only role, freshman | Deferred/ineligible with evidence; no submission. |
| Pay or start date missing | Hold for research, not automatically eligible or ineligible. |
| First seen today; datePosted last month; expiry next year | Keep three distinct facts; no fabricated opening date/deadline. |
| Previously unknown deadline becomes published | Update source/timestamp and surface one meaningful change. |
| Unchanged unknown source | Preserve unknown; advance next check; no repeated alert. |
| One source fails to load | Log failure; don't claim no new roles or mark postings closed. |
| Same requisition with application/confirmation URLs | One role record, merged evidence, no duplicate application. |
| Company cap reached | Hold further roles, even if easy to submit. |
| Required or optional substantive essay has no solid answer | Block and collect it in the question bank; don't omit for speed. |
| User dictation says projected result | Polished answer still says projected; no invented measured outcome. |
| New password / CAPTCHA / binding consent appears | Follow platform-specific handoff/confirmation; no bypass. |
| Résumé chooser runs but attachment absent | Not ready; no submission. |
| Dropdown resets after another field | Detect final value mismatch and repair before Submit. |
| Crash after clicking Submit | `submission_unknown`; reconcile receipt before any retry. |
| Two scheduled workers select the same role | Exactly one role owner; second worker skips/exits. |
| Submitted role later closes | Preserve application history; don't reclassify as never applied. |
| Resolved blocker / old no-essay instruction | Remove active blocker; approved answer bank/current policy wins. |
| Move to new computer | Reconnect privately, transfer one worker owner, reconcile ledger; no secrets in Git. |

## Completion report

Run `python3 scripts/check_playbook.py` for package/schema checks and `python3 -m unittest discover -s tests -v` for synthetic state, two-lane, duplicate and restart tests. These are offline tests, not proof that every acceptance scenario or live ATS interaction has passed. Use [STATE_AND_RECOVERY.md](STATE_AND_RECOVERY.md) for a private manifest, ledger, checkpoint and single-host lock. Verify live connectors separately with harmless reads; final-form attachment/consent/receipt gates still apply to every real application.

Report verified counts, unresolved holds with owners, source gaps, actual scheduler state, and next action. Separate `prepared`, `scheduled`, `attempted`, `verification_pending` and `confirmed submitted`. Do not say "running daily" until a saved enabled schedule and test execution have been verified. Do not claim offline fixture checks prove live connectors or submission quality.
