# Research and daily monitoring

This workflow creates an evidence-backed opportunity queue. It does not treat discovery as permission to apply, and it never turns missing information into a guessed date or qualification.

## Baseline research

1. Complete the intake and obtain the user's existing tracker and application history before starting. Import prior applications first, so discovery cannot produce accidental reapplications.
2. Split the agreed search scope into bounded, non-overlapping research assignments: for example robotics companies, semiconductor employers, university programs, and energy hardware. Each parallel agent receives the same applicant constraints, schema, evidence rules, and assigned source list. Agents return candidate records; one coordinator validates and merges them.
3. Start with official employer career sites and their linked applicant-tracking systems. Use portfolios, VC lists, search engines, and aggregators for discovery, not as a substitute for verifying the actual posting. Record an unofficial lead as unverified until checked.
4. Inspect the role, dates, compensation, location, onsite requirements, duration, class-year rules, work authorization, sponsorship, degree requirements, and any GPA requirement. Distinguish a preference from a mandatory qualification.
5. Inspect publicly visible application forms for required and optional short answers using [SHORT_ANSWERS.md](SHORT_ANSWERS.md). Do not enter applicant data, create an account, upload a file, or submit a form during research.
6. Merge and deduplicate records; run the gates below; publish only verified changes to the user's tracker. Maintain explicit unknowns and unresolved questions.

Parallelism improves coverage, not certainty. A coordinator must resolve conflicting evidence and check evidence freshness before recommending an application. Agents must not race to edit the same spreadsheet rows or submit applications concurrently.

## Date meanings: never substitute one for another

| Field | Meaning |
| --- | --- |
| `application_opens_at` | Explicitly published time when this application opens. |
| `application_deadline_at` | Explicitly published final application cutoff for this role. |
| `date_posted` | Posting publication date stated by the source; not necessarily its opening date. |
| `posting_expires_at` | Stated posting expiry, including structured-data expiry; not automatically an application deadline. |
| `first_seen_at` | When this monitor first discovered the record. |
| `last_checked_at` | Last successful verification, not the last attempted fetch. |
| `next_check_at` | Next planned check based on urgency and uncertainty. |

Each published date needs its source URL, the exact supporting text or short excerpt, observation timestamp, precision, and timezone when given. Keep date-only values date-only; do not invent midnight or a timezone. Preserve ambiguity such as “applications close in November” as text and unknown exact date. A historical program window is not a confirmed future opening. A related job's deadline is not this job's deadline. Internship work dates are not application dates.

`Unknown` is a valid result. Distinguish it from `not applicable`, `not checked`, and a temporary `verification failed`. An unavailable source must not cause a previously open role to become closed automatically.

## Identity, history, and duplicates

Use the official employer plus requisition ID as the primary identity. Keep canonical URL, alternate URLs, and source role ID. When no ID exists, use a normalized employer/title/location key and flag uncertain merges for review. Do not merge distinct requisitions merely because titles match. Treat reposts and replacement requisitions as linked records; do not assume they authorize a second application.

Before adding or applying, check all tracker tabs, the durable submission ledger, and confirmed employer records where available. A prior confirmed application wins over a stale “not started” row. A click on Submit, an email-verification screen, and a draft are not confirmed submissions. The user sets a company cap; any stricter employer limit takes precedence. Count across all role categories and tabs, not only the current queue.

## Eligibility and application states

Keep opportunity status separate from application status:

- Opportunity: `open`, `not_yet_open`, `closed`, `unknown`.
- Eligibility: `eligible`, `ineligible`, `unknown`.
- Eligibility assessment progress: `not_checked`, `needs_clarification`, `checked`. This is a separate field, not a fourth eligibility outcome.
- Application: `not_started`, `draft`, `blocked`, `ready_for_review`, `ready_to_submit`, `submitting`, `verification_pending`, `submitted`, `submission_unknown`, `interview`, `rejected`, `offer`, `withdrawn`.

Record the reason and supporting requirement for ineligibility. Do not invent a GPA, substitute high-school GPA for college GPA, or assume a degree preference is a hard cutoff. Unknown eligibility requires review, not a false “eligible.” Location, paid status, work dates, and employer commitments must match the intake. Roles outside the user's interests should be excluded with a reason, not misclassified as legally ineligible.

## Core spreadsheet views

The canonical role record appears once. Derived views must refer to its stable ID, not duplicate independently editable copies.

- **Internships:** actionable or unresolved roles plus the user's application history. Keep unsubmitted roles above submitted roles; submitted rows go to the bottom. Use very light red across unsubmitted rows and pale green across confirmed submitted rows. Keep a text status so color is not the only signal.
- **Deferred — Closed & Ineligible:** only confirmed closed or hard-ineligible unsubmitted roles, with distinct reason codes and evidence. Submitted records stay in Internships even after closure. Deliberately held, user-skipped, and unknown roles also stay in Internships with an unresolved blocker where applicable. A login blocker alone does not make a role ineligible.
- **Application Blockers:** only unresolved blockers, linked to the canonical role. Record the exact needed action, owner, last verification, and resolution. Remove resolved items from this active view while preserving resolution history.
- **Changes:** newly opened roles, upcoming openings, deadlines, newly resolved unknowns, closures, and material eligibility changes.

Before restructuring an existing workbook, snapshot it, inspect headers/validation/formulas, and identify existing canonical records. Move whole records without detaching notes or dates, preserve stable IDs, reconcile counts and links, and verify formatting after changes. Never delete application history to make the view cleaner.

## Daily change monitor

Revisit known sources and discover new roles. Checking only unknown dates misses closures, changed deadlines, and new requisitions.

Use a bounded daily budget with fair scheduling: urgent deadlines and known upcoming openings first; new roles next; then stale unknowns and a rotating share of all other active sources. Ensure every active source gets a scheduled revisit. Stable unknowns may use a longer interval, but do not disappear indefinitely. Apply retry/backoff for failures and respect source limits; do not repeatedly reload the same unknown page every few minutes.

Compare normalized records against the previous successful snapshot. Surface material changes rather than redisplaying the whole tracker. An unchanged unknown produces no repeated alert. A newly confirmed opening/deadline includes evidence and the previous value. A closure requires direct evidence, not just a fetch error or missing search result.

The daily output is a concise action queue: new eligible roles, upcoming openings, near deadlines, newly confirmed facts, changed/closed roles, and user decisions required. Keep a machine-readable change ledger. Discovery and application execution are separate scheduled stages; a GitHub schedule alone cannot control a signed-in local browser. See the repository setup/scheduling instructions for the actual worker and handoff.

## Deterministic quality gates

Reject a record from the application queue unless these checks pass:

1. **Identity:** stable role identity, canonical application link, no unresolved duplicate, no prior submission, company cap respected.
2. **Evidence:** official posting verified recently enough for the agreed cadence; every claimed date is tied to this role and source; failed checks retain their error state.
3. **Fit:** paid/location/dates/interests match; hard eligibility requirements satisfied or explicitly escalated.
4. **Answers:** every required field has an approved truthful answer; optional short answers are handled under the user's quality preference; no fabricated experience or metrics.
5. **Execution boundary:** account access, CAPTCHA, assessments, missing facts, and required confirmations are not bypassed. Record a blocker and move to another eligible role.
6. **Outcome:** only employer-confirmed submissions become `submitted`; store confirmation evidence and timestamp, update the tracker immediately, and resolve obsolete blockers.

Prioritization should combine fit, explicit deadlines, and rolling-review evidence. Posting age alone is not evidence of urgency or a reason to delay. Never compromise answer quality merely to increase submission count.
