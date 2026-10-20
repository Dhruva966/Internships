"""Synthetic offline tests: never contact an employer or submit a real form."""
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from workflow_contract import Ledger, WorkerLock, applied, ready_errors, validate_role, validate_profile, view

NOW = "2030-01-01T09:00:00+00:00"


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        with (ROOT / "templates/roles.example.csv").open() as f:
            self.role = next(csv.DictReader(f))
        self.profile = json.loads((ROOT / "templates/profile.example.json").read_text())

    def test_invalid_role_rejected(self):
        self.role.update(eligibility_status="INVALID_STATE", canonical_url="")
        errors = validate_role(self.role)
        self.assertTrue(any("canonical_url" in x for x in errors))
        self.assertTrue(any("eligibility_status" in x for x in errors))

    def test_unknown_gpa_not_high_school_gpa(self):
        self.profile["education"]["college_gpa"]["value"] = 4.0
        self.assertTrue(validate_profile(self.profile))

    def test_unapproved_submission_blocked(self):
        self.assertTrue(ready_errors(self.role, self.profile))

    def test_receipt_survives_status_and_closure(self):
        self.role.update(submission_confirmed_at=NOW, confirmation_evidence="Mock receipt 123", application_status="rejected", opportunity_status="closed")
        self.assertTrue(applied(self.role))
        self.assertEqual(view(self.role), ("Internships", "applied", "#F0FAF0"))
        self.assertTrue(ready_errors(self.role, self.profile))

    def test_second_writer_cannot_acquire(self):
        with tempfile.TemporaryDirectory() as root:
            with WorkerLock(root, "first", NOW):
                with self.assertRaises(RuntimeError):
                    with WorkerLock(root, "second", NOW):
                        pass

    def test_restart_pending_and_receipt(self):
        with tempfile.TemporaryDirectory() as root:
            with WorkerLock(root, "first", NOW) as lock:
                ledger = Ledger(root, lock)
                ledger.record("mock-1", "submitting", NOW)
                ledger.record("mock-1", "verification_pending", NOW)
            with WorkerLock(root, "restart", NOW) as lock:
                ledger = Ledger(root, lock)
                with self.assertRaises(ValueError):
                    ledger.record("mock-1", "submitting", NOW)
                ledger.record("mock-1", "submitted", NOW, "Mock ATS receipt 123")
                ledger.record("mock-1", "interview", NOW)
                with self.assertRaises(ValueError):
                    ledger.record("mock-1", "submitting", NOW)

    def test_two_lanes_mock_end_to_end(self):
        self.profile["execution"].update(mode="submit_approved", scope_approved=True, submission_authorized=True, approval_source="Synthetic user")
        self.role.update(opportunity_status="open", eligibility_status="eligible", assessment_state="checked", paid_status="paid", resume_version="mock-approved", question_completeness="complete")
        essay_role = dict(self.role, role_id="mock-essay", question_completeness="incomplete")
        self.assertTrue(ready_errors(essay_role, self.profile))
        self.assertEqual(ready_errors(self.role, self.profile), [])
        with tempfile.TemporaryDirectory() as root:
            with WorkerLock(root, "mock-worker", NOW) as lock:
                ledger = Ledger(root, lock)
                ledger.record(self.role["role_id"], "submitting", NOW)
                # Synthetic ATS confirmation, not a live browser test.
                ledger.record(self.role["role_id"], "submitted", NOW, "Mock ATS receipt")
                self.role.update(application_status="submitted", submission_confirmed_at=NOW, confirmation_evidence="Mock ATS receipt")
                self.assertEqual(view(self.role)[1], "applied")
                self.assertTrue(ready_errors(self.role, self.profile))
                with self.assertRaises(ValueError):
                    ledger.record(self.role["role_id"], "submitting", NOW)

    def test_unknown_requires_authoritative_reconciliation(self):
        with tempfile.TemporaryDirectory() as root:
            with WorkerLock(root, "mock", NOW) as lock:
                ledger = Ledger(root, lock)
                ledger.record("mock", "submitting", NOW)
                ledger.record("mock", "submission_unknown", NOW)
                with self.assertRaises(ValueError):
                    ledger.reconcile_not_received("mock", NOW, None)
                ledger.reconcile_not_received("mock", NOW, "Mock employer confirms no application received")
                ledger.record("mock", "submitting", NOW)


if __name__ == "__main__":
    unittest.main()
