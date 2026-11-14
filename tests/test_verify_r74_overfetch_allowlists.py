"""R75: regression tests for read-only, fail-closed R74 allowlist verifier.

Use 'python -m unittest tests.test_verify_r74_overfetch_allowlists' from repository root.
No network access, weight download, model import or model execution.
"""
import copy
import unittest

from scripts import verify_r74_overfetch_allowlists as audit


class R74AllowlistTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = audit.load()

    def data(self):
        return copy.deepcopy(self.original)

    def test_actual_metadata_invariants(self):
        result = audit.validate(*self.data())
        self.assertEqual("PASS_METADATA_CROSSCHECK_ONLY", result["status"])
        self.assertEqual(66, result["asset_count"])
        self.assertEqual(1425, result["file_refs"])
        self.assertEqual(2_985_522_750_447, result["overfetch_scope_difference_bytes"])
        self.assertEqual(80, result["hash_identity_counts"]["unverifiable_payload_hash"])
        self.assertFalse(result["approved_download"])
        self.assertEqual(
            [{"repo_id": "Qwen/Qwen-Image-2.1", "unattributed_bytes": 3333149}],
            result["unattributed_excess"],
        )

    def test_path_traversal_and_glob_refused(self):
        for filename in ("../LICENSE", "weights/*.safetensors", "a//b", "/tmp/a", "a\\b"):
            draft, source, approvals = self.data()
            draft["records"][0]["files"][0]["path"] = filename
            with self.subTest(filename=filename), self.assertRaisesRegex(ValueError, "unsafe filename"):
                audit.validate(draft, source, approvals)

    def test_duplicate_file_ref_refused(self):
        draft, source, approvals = self.data()
        draft["records"][0]["files"][1]["path"] = draft["records"][0]["files"][0]["path"]
        with self.assertRaisesRegex(ValueError, "duplicate filename"):
            audit.validate(draft, source, approvals)

    def test_payload_sha_cannot_be_substituted_by_pointer_blob_sha(self):
        draft, source, approvals = self.data()
        record = next(
            r for r in draft["records"]
            if any(f["identity_kind"] == "unverifiable_payload_hash" for f in r["files"])
        )
        f = next(f for f in record["files"] if f["identity_kind"] == "unverifiable_payload_hash")
        f["publisher_payload_sha256"] = f["git_blob_sha1_reference"]
        with self.assertRaisesRegex(ValueError, "masked payload must remain blocked"):
            audit.validate(draft, source, approvals)

    def test_publisher_sha_mismatch_refused(self):
        draft, source, approvals = self.data()
        f = next(f for f in draft["records"][0]["files"] if f["identity_kind"] == "lfs_payload_sha256")
        f["publisher_payload_sha256"] = "not-a-valid-sha"
        with self.assertRaisesRegex(ValueError, "bad LFS payload identity"):
            audit.validate(draft, source, approvals)

    def test_cross_index_revision_mismatch_refused(self):
        draft, source, approvals = self.data()
        draft["records"][0]["revision_sha"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "R73/R74 mismatch"):
            audit.validate(draft, source, approvals)

    def test_unapproved_manifest_flag_must_stay_false(self):
        draft, source, approvals = self.data()
        draft["download_authorized"] = True
        with self.assertRaisesRegex(ValueError, "unsafe draft flag"):
            audit.validate(draft, source, approvals)

    def test_single_asset_approval_must_stay_false(self):
        draft, source, approvals = self.data()
        draft["records"][0]["download_approved"] = True
        with self.assertRaisesRegex(ValueError, "unexpectedly approved"):
            audit.validate(draft, source, approvals)

    def test_owner_approval_queue_nonempty_refused(self):
        draft, source, approvals = self.data()
        approvals["entries"] = [{"asset": "mutated"}]
        with self.assertRaisesRegex(ValueError, "approved queue is not empty"):
            audit.validate(draft, source, approvals)

    def test_selected_file_byte_mutation_refused(self):
        draft, source, approvals = self.data()
        draft["records"][0]["files"][0]["bytes"] += 1
        with self.assertRaisesRegex(ValueError, "selected byte total mismatch"):
            audit.validate(draft, source, approvals)


    def test_historical_source_blob_provenance_required(self):
        draft, source, approvals = self.data()
        draft["historical_source_blob_sha"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "historical source blob provenance mismatch"):
            audit.validate(draft, source, approvals)

    def test_three_legitimate_zero_byte_git_blobs(self):
        draft, source, approvals = self.data()
        blanks = [(r["repo_id"], f["path"]) for r in draft["records"]
                  for f in r["files"] if f["bytes"] == 0]
        self.assertEqual(
            [("ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8", "samples/nul"),
             ("ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8", "workflow_examples/nul"),
             ("KlingTeam/LivePortrait", ".gitkeep")],
            blanks,
        )
        self.assertEqual("PASS_METADATA_CROSSCHECK_ONLY",
                         audit.validate(draft, source, approvals)["status"])

    def test_empty_file_requires_exact_git_empty_blob(self):
        draft, source, approvals = self.data()
        row = next(r for r in draft["records"] if r["repo_id"] ==
                   "ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8")
        file = next(f for f in row["files"] if f["path"] == "samples/nul")
        file["git_blob_sha1_reference"] = "a" * 40
        with self.assertRaisesRegex(ValueError, "invalid zero-byte Git blob identity"):
            audit.validate(draft, source, approvals)

    def test_windows_colon_filename_refused(self):
        draft, source, approvals = self.data()
        draft["records"][0]["files"][0]["path"] = "C:weights.safetensors"
        with self.assertRaisesRegex(ValueError, "unsafe filename"):
            audit.validate(draft, source, approvals)


if __name__ == "__main__":
    unittest.main()
