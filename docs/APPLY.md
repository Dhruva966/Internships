# BrowserOS Neo application worker

The worker applies consistently within explicit user authority; it does not maximize submission count at the expense of quality. Default to review-only until the user approves the application policy and a successful dry run.

## Prerequisites

Read the private approved profile, résumé manifest, answer bank, current queue, ledger and consent scope. Read the current Neo skill/tool descriptions. Confirm the browser is connected. If not, log a single browser blocker and stop browser work; don't silently substitute a different browser.

## Per-role transaction

1. Select a high-fit eligible open role, respecting dates, company caps and the user's approved scope. Recheck exact current posting and form; a cached search result is insufficient.
2. Resolve role aliases and prior submissions. An immutable receipt means previously applied even after `interview`, `rejected`, `offer` or `withdrawn`; never reapply. Imported claims of prior submission remain duplicate holds until reconciled, never fresh leads. Skip unresolved `submitting`, `verification_pending` and `submission_unknown`. Acquire exclusive ownership before acting; see [state and recovery](STATE_AND_RECOVERY.md).
3. Inspect the actual form before sending data. Extract missing short-answer prompts and update the question bank. If eligibility, pay, timing or answers are unresolved, create a concise blocker and release/move on.
4. Confirm the specific permitted data and destination. Select the approved résumé variant by hash/version, not a similar filename. Never attach an agent-generated replacement unless approved.
5. Fill factual fields from provenance-backed profile entries. Respect exact form wording: current versus permanent address, pursuing versus completed degree, college versus high-school GPA, current versus future sponsorship. An empty numeric GPA field does not justify entering zero or high-school GPA.
6. Fill every substantive required/optional essay using an approved, genuinely matching answer instance. Do not reuse a company motivation answer for another employer merely by replacing its name. Preserve the applicant's voice and truthful built/planned distinctions. Human-owned technical assessments remain held if assistance is not explicitly allowed.
7. Review the **retained** values, attachments and word/character limits after the form settles. Some ATS controls silently reset other fields. Avoid recursive full-form re-filling; correct the actual failing field.
8. Follow the current platform's action-time confirmation and handoff rules for agreements, new credentials, sensitive data, CAPTCHA, identity checks or other protected actions. A user's general desire for automation is not permission to bypass those rules.
9. Before Submit, run every gate in QUALITY_GATES.md and recheck company caps. Mark the ledger `submitting`, perform only an authorized final action, and verify an employer success page or confirmation identifying the role. A pending email challenge is not success.
10. Record timestamp, role ID, résumé/answer versions and private receipt evidence. Update the master tracker immediately, clear that role's resolved blockers and release its lease. If success is ambiguous, mark `submission_unknown` and reconcile before another attempt.

## Token-efficient Neo pattern

- Use `name_session` early with a short PII-free label. List tabs after reconnect; derive fresh handles and work in owned tabs. Keep no more than five independent tabs unless the user approves more.
- Prefer Neo `run` for a bounded multi-step snapshot → act → settled diff loop. Use a fresh snapshot's refs; don't carry stale refs across navigation.
- Batch independent research reads, but keep each form's actions sequential. Keep each run within the current tool's time limit. Wait on a specific expected selector/text, not polling sleeps.
- Use compact diffs and narrow extracts, not repeated full screenshots or whole-sheet reads. Retain one useful proof screenshot/receipt when needed; don't drop verification to save tokens.
- Cache stable company/ATS knowledge and approved answer versions in private state. Revalidate changed facts and the actual final form.
- Save a tested reusable helper only if current Neo tools support it. It must contain no applicant data, cookies or credentials. Cached helpers are hints, not evidence that today's form is unchanged.
- Ask once per genuinely new fact. Reuse approved shared answers, with employer-specific applicability checks. Don't keep retrying login failures, CAPTCHA or missing answers.

## Stop and resume

Hold the affected role, store the exact missing action with an owner, and continue another eligible role. For Neo human-help workflows, respect its ownership/handback protocol; never act on a page while the user controls it. If all work is blocked, report the smallest set of decisions that unblocks it. Do not create an endless agent loop merely to appear active.

Scheduled access cannot guarantee no interruptions: new terms, login expiry, site changes, CAPTCHA and new factual questions may require human involvement.
