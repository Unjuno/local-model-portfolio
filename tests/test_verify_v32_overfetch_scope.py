"""R75 read-only regression tests: R74 selected-file allowlists must fail closed."""
from __future__ import annotations

import copy
import json
import unittest

from scripts import verify_v32_overfetch_scope as audit


class OverfetchScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = audit.ROOT
        cls.allowlist = json.loads((root / audit.ALLOWLIST).read_text(encoding="utf-8"))
        cls.identities = json.loads((root / audit.IDENTITIES).read_text(encoding="utf-8"))
        cls.approved = json.loads((root / audit.APPROVED).read_text(encoding="utf-8"))

    def test_original_66_sources_and_real_metadata(self):
        report = audit.verify()
        self.assertEqual("PASS_PUBLISHER_SOURCE_SCOPE_ONLY", report["status"])
        self.assertEqual(66, report["source_allowlist_repos"])
        self.assertEqual(1425, report["selected_file_refs"])
        self.assertEqual(80, report["masked_payload_sha256_refs"])
        self.assertEqual(2_985_522_750_447, report["observed_extra_source_bytes"])
        self.assertEqual(1_782_172_555_461, report["selected_file_bytes"])
        self.assertFalse(report["download_authorized"])
        self.assertFalse(report["safe_as_download_authorization"])
        self.assertEqual(
            [{"repo_id": "Qwen/Qwen-Image-2.1",
              "observed_scope_delta_bytes": 3_333_149,
              "source_excluded_file_count": 0,
              "finding": "UNEXPLAINED_SOURCE_SCOPE_DELTA_NOT_INFERRED_FILES"}],
            report["scope_delta_without_excluded_files"],
        )

    def _bad(self, edit, error):
        obj = copy.deepcopy(self.allowlist)
        edit(obj)
        with self.assertRaisesRegex(ValueError, error):
            audit.validate(obj, self.identities, self.approved)

    def test_reject_wildcard_allow_pattern(self):
        self._bad(lambda x: x["records"][0]["files"][0].update(path="**/*.safetensors"),
                  "unsafe/glob")

    def test_reject_parent_directory_escape(self):
        self._bad(lambda x: x["records"][0]["files"][0].update(path="../secret"),
                  "unsafe/glob")

    def test_reject_duplicate_file(self):
        def change(x):
            x["records"][0]["files"][1]["path"] = x["records"][0]["files"][0]["path"]
        self._bad(change, "duplicate literal file path")

    def test_reject_invalid_payload_sha(self):
        def change(x):
            file = next(f for f in x["records"][0]["files"]
                        if f["identity_kind"] == "lfs_payload_sha256")
            file["publisher_payload_sha256"] = "x" * 64
        self._bad(change, "invalid publisher payload SHA")

    def test_reject_false_verified_masked_payload(self):
        def change(x):
            row = next(r for r in x["records"] if any(
                f["identity_kind"] == "unverifiable_payload_hash" for f in r["files"]))
            f = next(f for f in row["files"] if f["identity_kind"] == "unverifiable_payload_hash")
            f["publisher_payload_sha256_unverified"] = False
        self._bad(change, "masked payload must stay unverified")

    def test_reject_revision_mismatch(self):
        self._bad(lambda x: x["records"][0].update(revision_sha="a" * 40),
                  "R73 immutable source identity mismatch")

    def test_reject_unauthorized_flag(self):
        obj = copy.deepcopy(self.allowlist)
        obj["download_authorized"] = True
        with self.assertRaisesRegex(ValueError, "non-executable"):
            audit.validate(obj, self.identities, self.approved)

    def test_reject_nonempty_approved_queue(self):
        with self.assertRaisesRegex(ValueError, "approved queue not empty"):
            audit.validate(self.allowlist, self.identities, {"entries": [{"repo_id": "x/y"}]})

    def test_reject_extra_source_size_mismatch(self):
        def change(x):
            x["records"][0]["observed_publisher_repo_scope_bytes"] += 1
        self._bad(change, "R73 immutable source identity mismatch")

    def test_exact_empty_git_blobs_are_allowed(self):
        empties = [
            (row["repo_id"], f["path"])
            for row in self.allowlist["records"]
            for f in row["files"] if f["bytes"] == 0
        ]
        self.assertEqual(
            [("ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8", "samples/nul"),
             ("ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8", "workflow_examples/nul"),
             ("KlingTeam/LivePortrait", ".gitkeep")],
            empties,
        )

    def test_reject_unexpected_zero_byte_git_identity(self):
        def change(x):
            row = next(r for r in x["records"]
                       if r["repo_id"] == "ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8")
            f = next(f for f in row["files"] if f["path"] == "samples/nul")
            f["git_blob_sha1_reference"] = "a" * 40
        self._bad(change, "empty file must be an exact Git empty blob")

    def test_reject_source_blob_mismatch(self):
        self._bad(lambda x: x.update(historical_source_blob_sha="a" * 40),
                  "historical publisher source reference mismatch")


if __name__ == "__main__":
    unittest.main()
