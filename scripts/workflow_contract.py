"""Offline data contracts and single-host ledger primitives; no browser/network calls."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

APPLICATION_STATES = {"not_started", "draft", "blocked", "ready_for_review", "ready_to_submit",
                      "submitting", "verification_pending", "submitted", "submission_unknown",
                      "interview", "rejected", "offer", "withdrawn"}
POST_SUBMISSION_STATES = {"submitted", "interview", "rejected", "offer", "withdrawn"}
PENDING_STATES = {"submitting", "verification_pending", "submission_unknown"}
MISSING = {"", "unknown", "none", "not_selected", "not_checked", "not_submitted"}


def known(value):
    return value is not None and str(value).strip().lower() not in MISSING


def timestamp(value):
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed if parsed.tzinfo is not None else None
    except (ValueError, TypeError):
        return None


def http_url(value):
    p = urlparse(str(value))
    return p.scheme in {"https", "http"} and bool(p.netloc)


def applied(role):
    """Receipt history, never today's workflow status, determines 'already applied'."""
    return bool(timestamp(role.get("submission_confirmed_at")) and
                known(role.get("confirmation_evidence")))


def validate_role(role):
    errors = []
    for field in ("role_id", "company", "role_title"):
        if not known(role.get(field)):
            errors.append(f"{field}: required")
    if not http_url(role.get("canonical_url", "")):
        errors.append("canonical_url: required HTTP(S) application URL")
    for field, allowed in {
        "opportunity_status": {"open", "not_yet_open", "closed", "unknown"},
        "eligibility_status": {"eligible", "ineligible", "unknown"},
        "assessment_state": {"not_checked", "needs_clarification", "checked"},
        "application_status": APPLICATION_STATES,
        "paid_status": {"paid", "unpaid", "unknown"},
        "question_completeness": {"not_checked", "inaccessible", "incomplete", "complete"},
    }.items():
        if role.get(field) not in allowed:
            errors.append(f"{field}: invalid state {role.get(field)!r}")
    if role.get("eligibility_status") == "eligible" and role.get("assessment_state") != "checked":
        errors.append("eligible role requires checked assessment")
    if role.get("eligibility_status") == "ineligible" and not known(role.get("eligibility_reason")):
        errors.append("ineligible role requires reason")
    for field in ("first_seen_at", "last_checked_at", "next_check_at", "submission_confirmed_at"):
        if known(role.get(field)) and not timestamp(role[field]):
            errors.append(f"{field}: timezone-aware ISO timestamp required")
    if known(role.get("submission_confirmed_at")) != known(role.get("confirmation_evidence")):
        errors.append("submission receipt and timestamp must be supplied together")
    if role.get("application_status") in POST_SUBMISSION_STATES and not applied(role):
        errors.append("post-submission status requires immutable receipt evidence")
    if applied(role) and role.get("application_status") not in POST_SUBMISSION_STATES:
        errors.append("receipt history cannot be reset to unsubmitted status")
    for prefix, date_field in (("opening", "application_opens_at"), ("deadline", "application_deadline_at")):
        if known(role.get(date_field)):
            for suffix in ("evidence_url", "evidence_excerpt", "observed_at", "date_precision" if prefix == "opening" else "precision"):
                if not known(role.get(f"{prefix}_{suffix}")):
                    errors.append(f"{date_field}: missing {prefix}_{suffix}")
            if not http_url(role.get(f"{prefix}_evidence_url", "")):
                errors.append(f"{date_field}: official evidence URL required")
    return errors


def ready_errors(role, profile):
    errors = validate_role(role)
    if applied(role) or role.get("do_not_reapply") is True or role.get("application_status") in PENDING_STATES:
        errors.append("already applied or submission unresolved")
    if role.get("opportunity_status") != "open" or role.get("eligibility_status") != "eligible":
        errors.append("verified open and eligible required")
    if role.get("question_completeness") != "complete" or not known(role.get("resume_version")):
        errors.append("complete approved answers and selected resume required")
    execution = profile.get("execution", {})
    if execution.get("submission_authorized") is not True or execution.get("scope_approved") is not True:
        errors.append("submission scope not approved")
    if profile.get("preferences", {}).get("pay", {}).get("paid_only") is True and role.get("paid_status") != "paid":
        errors.append("paid compensation not verified")
    # Detailed fit, consent, attachments and employer rules still need the live review.
    return errors


def validate_profile(profile):
    errors = []
    if not isinstance(profile, dict) or profile.get("schema_version") != "1.0":
        return ["profile schema_version must be 1.0"]
    execution = profile.get("execution", {})
    if execution.get("mode") not in {"discover_only", "prepare_drafts", "submit_approved"}:
        errors.append("invalid execution mode")
    if execution.get("submission_authorized") is True:
        if execution.get("mode") != "submit_approved" or execution.get("scope_approved") is not True or not known(execution.get("approval_source")):
            errors.append("submission authorization requires approved scope, source and submit_approved mode")
    for fact in profile.get("education", {}).values():
        if isinstance(fact, dict) and fact.get("state") in {"confirmed", "estimated"} and (not known(fact.get("value")) or not known(fact.get("source"))):
            errors.append("confirmed education fact missing value/source")
    gpa = profile.get("education", {}).get("college_gpa", {})
    if gpa.get("state") in {"unknown", "not_yet_available"} and gpa.get("value") is not None:
        errors.append("unknown college GPA cannot carry a numeric value")
    for resume in profile.get("resumes", []):
        if resume.get("approved_for_upload") is True:
            if not (len(str(resume.get("sha256", ""))) == 64 and known(resume.get("approval_source")) and known(resume.get("approved_at"))):
                errors.append("approved resume requires SHA256, approval source and time")
    return errors


def view(role):
    if applied(role):
        return "Internships", "applied", "#F0FAF0"
    if role.get("opportunity_status") == "closed" or role.get("eligibility_status") == "ineligible":
        return "Deferred — Closed & Ineligible", "deferred", None
    return "Internships", "unsubmitted", "#FFF6F6"


def atomic_json(path, value):
    path = Path(path)
    temp = path.with_name(path.name + f".{os.getpid()}.tmp")
    try:
        with temp.open("x", encoding="utf-8") as handle:
            os.chmod(temp, 0o600)
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


class WorkerLock:
    """Single-host exclusive lock. Never auto-steal: inspect/reconcile dead owners."""
    def __init__(self, root, owner, now):
        self.path = Path(root) / "worker.lock.json"
        self.owner, self.now = owner, now
        self.acquired = False

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        try:
            with self.path.open("x", encoding="utf-8") as handle:
                os.chmod(self.path, 0o600)
                json.dump({"owner": self.owner, "pid": os.getpid(), "acquired_at": self.now}, handle)
        except FileExistsError as exc:
            raise RuntimeError("Worker already locked; do not steal or submit") from exc
        self.acquired = True
        return self

    def __exit__(self, *_):
        record = json.loads(self.path.read_text())
        if record.get("owner") == self.owner:
            self.path.unlink()
        self.acquired = False


class Ledger:
    """Call under WorkerLock. Receipt confirmation is append-only, exactly once."""
    def __init__(self, root, lock):
        if not lock.acquired:
            raise RuntimeError("Active WorkerLock required")
        self.path = Path(root) / "ledger.json"
        self.lock = lock
        self.data = json.loads(self.path.read_text()) if self.path.exists() else {"schema_version": "1.0", "events": []}

    def events(self, role_id):
        return [e for e in self.data["events"] if e["role_id"] == role_id]

    def record(self, role_id, status, at, evidence=None):
        if not self.lock.acquired:
            raise RuntimeError("Lock no longer held")
        if status not in APPLICATION_STATES or not timestamp(at):
            raise ValueError("Invalid status or timestamp")
        if self.path.exists():
            self.data = json.loads(self.path.read_text())
        past = self.events(role_id)
        receipt = next((e for e in past if e["status"] == "submitted"), None)
        if receipt and status not in {"interview", "rejected", "offer", "withdrawn"}:
            raise ValueError("Receipt is permanent; duplicate/reset forbidden")
        if not receipt and status in {"interview", "rejected", "offer", "withdrawn"}:
            raise ValueError("Cannot create post-submission event without receipt")
        if status == "submitting" and past and past[-1]["status"] in PENDING_STATES:
            raise ValueError("Reconcile unresolved submission before retry")
        if past and past[-1]["status"] in PENDING_STATES and status not in PENDING_STATES | {"submitted"}:
            if status != "draft" or not known(evidence):
                raise ValueError("Authoritative non-receipt reconciliation required")
        if status == "submitted" and (not known(evidence) or not past or past[-1]["status"] not in PENDING_STATES):
            raise ValueError("Submission requires prior attempt and official receipt")
        event = {"role_id": role_id, "status": status, "at": at, "evidence": evidence}
        event["event_id"] = hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()
        self.data["events"].append(event)
        atomic_json(self.path, self.data)
        return event

    def reconcile_not_received(self, role_id, at, evidence):
        """Only after authoritative evidence establishes that no app was received."""
        past = self.events(role_id)
        if not past or past[-1]["status"] not in PENDING_STATES or not known(evidence):
            raise ValueError("Reconciliation evidence required")
        if any(e["status"] == "submitted" for e in past):
            raise ValueError("Cannot erase confirmed submission")
        return self.record(role_id, "draft", at, evidence)


def validate_manifest(manifest):
    required = {"schema_version", "installation_id", "private_root", "owner_host", "files",
                "tracker", "question_bank", "schedule", "limits", "tools"}
    errors = [f"manifest missing {key}" for key in required - manifest.keys()]
    files = manifest.get("files", {})
    for key in ("profile", "roles", "ledger", "checkpoint", "lock"):
        if not files.get(key):
            errors.append(f"manifest files.{key} required")
    schedule = manifest.get("schedule", {})
    if schedule.get("enabled") is True:
        if not schedule.get("id") or not schedule.get("timezone") or not schedule.get("dry_run_passed_at"):
            errors.append("enabled schedule requires ID, timezone and dry-run evidence")
        if not known(manifest.get("owner_host")) or "<" in manifest.get("private_root", "<"):
            errors.append("enabled schedule requires concrete host/private root")
    return errors
