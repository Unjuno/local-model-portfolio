"""Static evidence-contract tests for R32. No network and no weight acquisition."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "catalog/research/2026-11-07-r32-ltx-donor-chain.json"


class TestR32ResearchProvenance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(FILE.read_text(encoding="utf-8"))
        cls.files = cls.data["file_manifest"]

    def test_six_distinct_source_files(self):
        self.assertEqual(len(self.files), 6)
        self.assertEqual(len({x["id"] for x in self.files}), 6)
        self.assertEqual(len({(x["repo_id"], x["file"]) for x in self.files}), 6)

    def test_publisher_sha256_metadata_only(self):
        for x in self.files:
            self.assertRegex(x["sha256"], r"^[a-f0-9]{64}$")
            self.assertTrue(x["url"].startswith("https://huggingface.co/"))
            self.assertGreater(x["displayed_gb"], 0)
        self.assertIn("NOT recomputed", self.data["integrity"])

    def test_stuubs_quant_does_not_create_a_new_trained_state(self):
        files = {x["id"]: x for x in self.files}
        self.assertEqual(files["stuubs_v1_bf16"]["repo_id"], files["stuubs_v1_int8"]["repo_id"])
        self.assertIn("SAME_STUUBS_V1", files["stuubs_v1_int8"]["role"])
        self.assertNotEqual(files["stuubs_v1_bf16"]["sha256"], files["stuubs_v1_int8"]["sha256"])

    def test_omninft_separate_adapters_and_compatibility_not_assumed(self):
        files = {x["id"]: x for x in self.files}
        self.assertNotEqual(files["omninft_ltx23"]["sha256"], files["omninft_ltx2"]["sha256"])
        omni = self.data["classification"]["omni"]
        self.assertTrue(omni["two_different_parent_checkpoints"])
        self.assertFalse(omni["direct_LTX2_3_to_LTX2_5_compatibility_proven"])

    def test_original_chris_mirror_not_hash_proven(self):
        chris = self.data["classification"]["chris"]
        self.assertTrue(chris["mirror_explicitly_says_duplicated_from_original"])
        self.assertFalse(chris["original_sha_matched_to_mirror"])
        self.assertFalse(chris["actual_complete_bytes_verified"])

    def test_license_and_runtime_evidence_not_overclaimed(self):
        omni = self.data["classification"]["omni"]
        self.assertTrue(omni["rights_conflict_requires_resolution"])
        self.assertIsNone(omni["full_repo_revision"])
        self.assertIsNone(self.data["classification"]["stuubs"]["full_repo_commit"])

    def test_no_selection_or_download_mutation(self):
        current = json.loads((ROOT / "catalog/CURRENT.json").read_text(encoding="utf-8"))
        self.assertEqual(current["expected"]["tracked"], 150)
        self.assertEqual(current["expected"]["active"], 105)
        self.assertTrue(self.data["all_existing_150_still_intact"])
        self.assertEqual(self.data["formal_changes"], 0)
        self.assertEqual(self.data["new_download_approvals"], 0)
        self.assertFalse(self.data["weight_downloaded"])
        self.assertEqual(self.data["user_cap_bytes"], 4_000_000_000_000)


if __name__ == "__main__":
    unittest.main()
