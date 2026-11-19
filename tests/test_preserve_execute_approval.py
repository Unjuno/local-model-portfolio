"""Offline regression tests for fail-closed acquisition approval and license gates.

No network, downloads, model execution, or D: drive writes are performed.
Run: python -m unittest discover -s tests -p test_preserve_execute_approval.py -v
"""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "preserve_execute.py"
SPEC = importlib.util.spec_from_file_location("preserve_execute", SCRIPT)
preserve = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preserve)


def task(path="model.safetensors", size=11, revision="a" * 40):
    return {
        "repo_id": "Publisher/Original",
        "rev": revision,
        "files": [{"path": path, "bytes": size, "sha256": "b" * 64}],
        "license": "apache-2.0",
        "gated_hint": False,
        "group": "research",
    }


def approval(t):
    return {
        "repo_id": t["repo_id"],
        "revision_sha": t["rev"],
        "approved": True,
        "download_enabled": True,
        "approved_by_user": True,
        "license_text_reviewed": True,
        "parent_dependency_rights_reviewed": True,
        "approval_ref": "explicit-review-record-001",
        "files": [
            {"path": t["files"][0]["path"],
             "bytes": t["files"][0]["bytes"],
             "sha256": "b" * 64},
        ],
    }


class SourceGateTests(unittest.TestCase):
    def _approve(self, t, entry):
        with tempfile.TemporaryDirectory() as td:
            f = Path(td) / "approved.json"
            f.write_text(json.dumps({"schema_version": 1, "entries": [entry]}),
                         encoding="utf-8")
            return preserve.approval_for(t, approval_path=f)

    def test_exact_model_file_scope_approved(self):
        t = task()
        self.assertIsNotNone(self._approve(t, approval(t)))

    def test_no_permission_field_is_not_approved(self):
        t = task()
        a = approval(t)
        del a["approved_by_user"]
        self.assertIsNone(self._approve(t, a))

    def test_revision_mismatch_is_not_approved(self):
        t = task()
        a = approval(t)
        a["revision_sha"] = "c" * 40
        self.assertIsNone(self._approve(t, a))

    def test_file_scope_mismatch_is_not_approved(self):
        t = task()
        a = approval(t)
        a["files"][0]["bytes"] += 1
        self.assertIsNone(self._approve(t, a))

    def test_size_only_wildcard_approval_is_not_accepted(self):
        t = task()
        a = approval(t)
        a["files"][0].pop("sha256")
        self.assertIsNone(self._approve(t, a))

    def test_path_traversal_rejected(self):
        t = task("../private/secret")
        self.assertIsNone(self._approve(t, approval(t)))

    def test_unapproved_does_not_even_call_hub(self):
        t = task()
        with mock.patch.object(preserve, "approval_for", return_value=None), \
             mock.patch.object(preserve, "log"), \
             mock.patch.object(preserve, "api_model") as api:
            r = preserve.process_task(t, "candidate.json")
        self.assertEqual(r["status"], "HOLD_NO_EXPLICIT_APPROVED_MANIFEST")
        api.assert_not_called()

    def test_license_other_never_automatically_permissive(self):
        self.assertNotIn("other", preserve.PERMISSIVE)
        t = task()
        with mock.patch.object(preserve, "approval_for", return_value=approval(t)), \
             mock.patch.object(preserve, "log"), \
             mock.patch.object(preserve, "api_model", return_value={
                 "cardData": {"license": "other"},
                 "gated": False, "private": False, "disabled": False,
                 "siblings": [],
             }), mock.patch.object(preserve, "free_bytes") as free:
            r = preserve.process_task(t, "candidate.json")
        self.assertEqual(r["status"], "HOLD_LICENSE_REVIEW_REQUIRED")
        free.assert_not_called()

    def test_incomplete_hash_does_not_verify(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "data"
            p.write_bytes(b"x")
            ok, how, value = preserve.verify_file(p, {"bytes": 1})
        self.assertFalse(ok)
        self.assertEqual(how, "NO_PUBLISHER_HASH")


if __name__ == "__main__":
    unittest.main()
