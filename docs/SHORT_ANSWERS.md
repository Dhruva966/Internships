# Short-answer collection and answer library

Collect questions during research so the applicant can answer them once in their own voice, then approve tailored versions. This is not permission to fabricate an answer or complete a hiring assessment on their behalf.

## Safe collection

Read publicly visible application forms without entering or transmitting applicant information. Do not create accounts, invent credentials, upload a résumé, bypass CAPTCHA, or advance a step that sends data just to discover later questions. If questions are behind a login or data-submission step, record `not_accessible_without_user_action` and the precise blocker. Public accessibility does not mean a form is safe to submit during research.

Collect **both required and optional** questions. Record:

- Stable role ID, company, role title, official form URL, observation timestamp, and application section.
- Exact prompt, preserving subquestions; do not silently replace it with a paraphrase.
- Required/optional status, word or character limit and its unit, response type, and any special instructions.
- Relevant context such as team, role, or answer constraints. Store conditional-display rules if visible.
- Collection status and whether a human-owned assessment or artifact is required.

Do not treat an applicant coding challenge, timed test, design exercise, video assessment, or evaluation task as an ordinary reusable short answer. The applicant owns that work; follow the employer's assistance rules and escalate instead of completing it automatically.

## Canonical questions and tailored instances

Maintain two layers:

1. **Canonical question:** a reusable topic such as “technical accomplishment,” “why this company,” or “project you are proud of.” This groups similar prompts; it does not erase their differences.
2. **Question instance:** the employer's exact prompt for a particular requisition, including its limit and required status. Each instance gets an approved response version or an unresolved status.

Two “why us” prompts can share applicant background but require different employer-specific motivation. Do not paste a generic canonical answer blindly. Similar wording with different subquestions or limits still needs an instance-level check.

## Applicant conversation

Compile new questions at the bottom of a question document, grouped by company and role. Put the company in parentheses after each question. Mark required/optional and limits clearly. Keep previously approved responses intact; record revisions instead of silently replacing the user's final wording.

Ask one substantive question at a time when the applicant wants to dictate. Use their own stories, phrasing, and emotional substance; remove filler, clarify sequence, and make the response slightly more formal without replacing their voice. Ask follow-ups only for missing material facts, personal contribution, or an outcome the prompt actually needs. Reuse approved factual answers rather than repeatedly asking availability, authorization, or other already answered questions.

Separate what the applicant personally did from team results. Preserve distinctions between a working prototype, a designed revision, a planned model, a projected result, and a measured outcome. Do not invent metrics, credentials, investor commitments, implementation details, or company enthusiasm. Evidence gaps should become questions, not polished guesses.

## Response lifecycle

Use states such as `unanswered`, `draft`, `needs_user_review`, `approved`, `needs_refresh`, and `not_applicable`. Store response version, approval timestamp, source story IDs, and the exact question instance to which approval applies. Keep sensitive details in private applicant storage, never in the public repository or logs.

Before filling an application:

1. Re-read the current prompt and limit; forms can change.
2. Retrieve an approved response appropriate to that employer and role.
3. Check all subquestions are addressed, names and facts are accurate, and the word/character limit passes mechanically.
4. If tailoring changes the meaning or introduces new claims, request review. Stylistic shortening must preserve the approved substance.
5. Complete optional short answers when the user's policy calls for them. If there is no solid answer, hold the role rather than leave it blank just to submit faster.
6. Save the exact submitted version and its question alongside confirmation evidence after a verified submission.

Routine factual screening answers belong in the approved applicant profile, not repeatedly in the story library. New employer-specific commitments, references, sensitive disclosures, and material legal acknowledgments still require the applicable user confirmation. A broad desire to apply is not a reason to infer unknown facts.

## Quality checks

- Exact prompt and limits have provenance; inaccessible questions are not claimed to be collected.
- No stale employer names, role titles, or mismatched project details.
- No unapproved numerical claims or projected outcomes presented as achieved.
- Every required instance has a valid answer or a blocker; every optional instance has an intentional disposition.
- No assessment content is mislabeled as an ordinary personal statement.
- The user can review the final response and understand what will be sent.
