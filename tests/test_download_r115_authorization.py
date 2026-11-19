"""Offline regression tests for the R115 downloader's explicit-acquisition gate.

Does not access Hugging Face, import model code, or download model payloads.
Run: python3 -m unittest tests/test_download_r115_authorization.py -v
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "download_r115_windows.py"
spec = importlib.util.spec_from_file_location("r115_download", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(mod)


def sample_model():
    return {
        "source_repo_id": "owner/model",
        "source_revision": "a" * 40,
        "files": [
            {"path": "README.md", "bytes": 7, "sha256": None, "git_blob_sha1": "c" * 40},
            {"path": "model.safetensors", "bytes": 123, "sha256": "b" * 64, "git_blob_sha1": None},
        ],
    }


def approval(model):
    return {
        "source_repo_id": model["source_repo_id"],
        "source_revision": model["source_revision"],
        "source_scope_sha256": mod.source_fingerprint(model),
        "approved": True,
        "user_explicit_manifest_consent": True,
        "license_and_parent_rights_reviewed": True,
        "owner_archive_volume_verified": True,
    }


class R115ApprovalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "approved.json"
        self.model = sample_model()

    def write(self, entries):
        self.path.write_text(json.dumps({"schema_version": 1, "entries": entries}), encoding="utf-8")

    def test_empty_approved_queue_blocks_all_transfers(self):
        self.write([])
        with self.assertRaisesRegex(ValueError, "No explicitly approved"):
            mod.assert_explicit_approved_sources([self.model], self.path)

    def test_missing_queue_blocks_all_transfers(self):
        with self.assertRaisesRegex(ValueError, "not present"):
            mod.assert_explicit_approved_sources([self.model], self.path)

    def test_user_consent_cannot_be_inferred_from_public_candidate(self):
        entry = approval(self.model)
        entry["user_explicit_manifest_consent"] = False
        self.write([entry])
        with self.assertRaisesRegex(ValueError, "Missing exact"):
            mod.assert_explicit_approved_sources([self.model], self.path)

    def test_rights_and_disk_verification_are_independent_gates(self):
        for flag in ("license_and_parent_rights_reviewed", "owner_archive_volume_verified"):
            entry = approval(self.model)
            entry[flag] = False
            self.write([entry])
            with self.subTest(flag=flag), self.assertRaisesRegex(ValueError, "Missing exact"):
                mod.assert_explicit_approved_sources([self.model], self.path)

    def test_revision_or_file_scope_change_invalidates_prior_approval(self):
        self.write([approval(self.model)])
        for field, replacement in (("source_revision", "d" * 40),):
            modified = dict(self.model)
            modified[field] = replacement
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "Missing exact"):
                mod.assert_explicit_approved_sources([modified], self.path)
        new_model = sample_model()
        new_model["files"][1]["bytes"] += 1
        with self.assertRaisesRegex(ValueError, "Missing exact"):
            mod.assert_explicit_approved_sources([new_model], self.path)

    def test_explicit_matching_manifest_is_accepted(self):
        self.write([approval(self.model)])
        mod.assert_explicit_approved_sources([self.model], self.path)

    def test_scope_fingerprint_not_changed_by_file_list_order(self):
        reordered = sample_model()
        reordered["files"].reverse()
        self.assertEqual(mod.source_fingerprint(self.model), mod.source_fingerprint(reordered))


if __name__ == "__main__":
    unittest.main()
