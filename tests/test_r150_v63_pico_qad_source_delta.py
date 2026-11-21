"""Read-only, offline regression for R150: Pico INT8 QAD source delta.

Tests only metadata; never fetches or executes upstream model files.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD_PATH = ROOT / "manifests/drafts/r143-2026-11-22-three-specialists-originals.candidate.json"
NEW_PATH = ROOT / "manifests/drafts/r150-2026-11-22-kitten-pico-int8-qad-source-delta.candidate.json"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


class PicoQADDelta(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = read_json(OLD_PATH)
        cls.new = read_json(NEW_PATH)
        cls.parent = next(
            item for item in cls.old["model_repos"]
            if item["repo_id"] == "KittenML/kitten-tts-2-pico"
        )

    def test_delta_exactly_prior_excluded_files(self):
        historical = {
            x["path"]: x["bytes"] for x in self.parent["excluded_alternative_files"]
        }
        candidate = {
            x["path"]: x["publisher_reference_bytes"]
            for x in self.new["additional_int8_files"]
        }
        self.assertEqual(candidate, historical)
        self.assertEqual(len(candidate), 8)
        self.assertEqual(sum(candidate.values()), 63_628_208)
        for path in candidate:
            self.assertIn(path, {f"kitten_tts_2_pico_{lang}.onnx" for lang in ("de", "en", "es", "fr", "hi", "it", "pt", "ru")})

    def test_source_revision_and_full_scope_reconcile(self):
        self.assertEqual(self.new["publisher_immutable_revision_sha"], self.parent["revision_sha"])
        self.assertEqual(len(self.new["publisher_immutable_revision_sha"]), 40)
        self.assertEqual(self.new["prior_selected_file_count"], self.parent["selected_file_count"])
        self.assertEqual(self.new["prior_selected_publisher_bytes"], self.parent["selected_source_bytes"])
        self.assertEqual(
            self.new["proposed_selected_publisher_reference_bytes"],
            self.new["prior_selected_publisher_bytes"] + self.new["additional_publisher_reference_bytes"],
        )
        self.assertEqual(
            self.new["proposed_selected_publisher_reference_bytes"],
            self.parent["publisher_repo_bytes"],
        )
        self.assertEqual(
            self.new["proposed_selected_file_count"],
            self.parent["publisher_repo_file_count"],
        )

    def test_unknown_publisher_sha_must_not_be_pretended_locked(self):
        self.assertEqual(self.new["publisher_int8_weight_sha256_refs_observed"], 0)
        for entry in self.new["additional_int8_files"]:
            self.assertIsNone(entry["publisher_lfs_sha256"])
            self.assertIsNone(entry["publisher_git_blob_oid"])
            self.assertFalse(entry["final_source_lock_ready"])
            self.assertFalse(entry["local_sha256_verified"])

    def test_no_synthetic_authorization_or_catalog_mutation(self):
        for field in (
            "download_enabled", "download_approved", "approved_by_user",
            "license_text_reviewed_for_owner", "parent_dependency_rights_reviewed",
            "owner_intended_license_acts_verified",
            "owner_windows_D_current_capacity_or_sha_verified",
            "owner_offline_restore_verified",
        ):
            self.assertIs(self.new[field], False, field)
        self.assertTrue(self.new["older_source_manifest_and_canonical_overlay_not_rewritten"])
        self.assertTrue(self.new["existing_conditional_model_selection_unchanged"])
        self.assertEqual(self.new["model_assets_added"], 0)
        self.assertEqual(self.new["new_model_weights_downloaded_this_research_bytes"], 0)

    def test_fixed_publisher_code_and_doc_cited(self):
        evidence = self.new["new_evidence"]
        self.assertEqual(
            evidence["fixed_author_code_revision_sha"],
            "5802f6b956844919ecf210f4e55f4750a6ad7c6f",
        )
        self.assertIn("docs/kitten-tts-2-tiny.md", evidence["fixed_author_technical_doc_url"])
        self.assertIn("kittenml/kittentts2_tiny/model.py", evidence["fixed_runtime_code_url"])


if __name__ == "__main__":
    unittest.main()
