# Canonical tracker and state

Use one authoritative store and render views from it. A spreadsheet row number is a location, not a role ID. A native Sheet can be authoritative for a single coordinator; if a private database is authoritative, declare it and sync the Sheet through one writer. Do not independently edit two competing masters.

## Core visible tabs

| Tab | Contents |
| --- | --- |
| Internships | Active leads, held-but-not-disqualified roles, and all previously submitted applications. Unsubmitted first; submitted at bottom. |
| Deferred — Closed & Ineligible | Confirmed closed/unavailable unsubmitted postings and hard eligibility mismatches, with reason/evidence and possible recheck trigger. |
| Application Blockers | Only unresolved holds: role ID, category, owner, exact missing answer/action, evidence, next step, and last checked date. |
| Short-Answer Bank | Exact company/role question instances and approval states, or a linked native document if that is easier to dictate into. |

Optional deadline views should reference canonical IDs, not copied application rows that drift out of sync. Hide old queue snapshots as recoverable archives after reconciling unique roles; do not delete user records just to simplify tabs. Submitted records stay in Internships even if the employer later closes the posting.

## Row presentation

- Submitted: full row **very light green**, e.g. `#F0FAF0`.
- Not submitted: full row **very light red**, e.g. `#FFF6F6`.
- Base grouping and colors on immutable prior-submission history, not only the current workflow status. Interview/rejected/offer/withdrawn records with receipts remain green at the bottom and count toward employer limits. Imported prior-submission claims block reapplication until reconciled. Color is supplementary; keep an explicit status column.
- Keep filters, frozen headers, wrapped notes, usable links and dropdown validation. Verify the actual native rendering after edits. Preserve supporting notes, formulas, and links during moves.

## Minimum role record

Employer, requisition ID, canonical URL, title, focus, location, work mode, internship term, pay/currency/unit/source, required degree/class year/GPA/authorization, opening-date value and evidence, deadline value/timezone and evidence, review mode, first seen, last checked, availability status, eligibility status/reason, fit, application status, selected résumé version, question-completeness status, blocker owner, receipt evidence.

Opening date, `datePosted`, first seen and structured-data expiry must be separate. A deadline without a timezone stays timezone-unknown. Do not invent local midnight. Use `unknown`, not a blank that could mean "not applicable."

## Separate state axes

- Availability: `open`, `not_yet_open`, `closed`, `unknown`.
- Eligibility: `eligible`, `ineligible`, `unknown`. Assessment state separately records `not_checked`, `needs_clarification`, or `checked`.
- Application: `not_started`, `draft`, `blocked`, `ready_for_review`, `ready_to_submit`, `submitting`, `verification_pending`, `submitted`, `submission_unknown`, `interview`, `rejected`, `offer`, `withdrawn`.
- Fit/priority: a ranking, never evidence of eligibility.

`blocked` is not `ineligible`. Unknown pay, an account gate, a missing transcript or an unanswered essay stays a hold. A preferred qualification is not a hard cutoff. A closing deadline is not the internship start date.

## Identity, deduplication and atomic submission

Prefer `(employer, requisition_id)`; use canonical URL and documented aliases when no ID exists. Normalize ATS application/confirmation suffixes without merging different requisitions or terms. Generic talent pools may differ from specific jobs. Merge exact duplicate records, retaining all notes and receipt evidence, and keep an alias mapping.

Before applying, atomically claim the role in a private ledger. Record `submitting` before the final action; then store the exact receipt and mark `submitted`. If the browser crashes or a request times out after submission, leave `submission_unknown` until receipt/portal evidence resolves it. Never blindly retry Submit. Record company caps, employer-specific windows and exact role history.

One coordinator writes Sheets. Workers return proposed deltas with canonical IDs, evidence and timestamps. Compare the current row/version before writing; reject conflicts. Native row copies/moves should retain formats and validations. Repair dependent links after sorting.

## Blocker hygiene

Close/remove resolved blockers from the active tab and retain their answer/provenance privately. Remove blockers for confirmed ineligible/closed roles and for already-submitted applications. Keep a user-skipped role on hold without repeatedly asking about it. Distinguish `user_answer`, `user_login`, `human_challenge`, `approval`, `agent_research`, `browser_issue`, `duplicate_reconciliation`, and `company_cap`. Historical failure notes are not proof that the same browser problem exists today.

Never put passwords or OTPs into a blocker row. A pay/timing fact is normally the agent's research work, not a question the applicant should guess.
