"""R40 regressions for cross-manifest checksum reuse and partial 4TB evidence."""
import json
import unittest
from pathlib import Path

from scripts.audit_candidate_manifest_union import (
    DEFAULT_REPORT, ROOT, aggregate, verify_report,
)

def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class TestR40SHAUnion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = read(DEFAULT_REPORT)
        cls.core = cls.r["core_packages"]
        cls.opt = cls.r["optional_special_packages"]
        cls.check = verify_report()

    def test_fifteen_cores_and_two_optional_specials(self):
        self.assertEqual(len(self.core), 15)
        self.assertEqual(len(self.opt), 2)
        self.assertEqual(len({x["package_id"] for x in self.core+self.opt}), 17)
        self.assertEqual(self.r["core_statistics"]["file_references"], 181)
        self.assertEqual(self.r["with_optional_special_statistics"]["file_references"], 186)

    def test_all_pinned_source_metadata_is_verified_against_each_manifest(self):
        self.assertEqual(self.check["status"], "PASS_PUBLISHER_METADATA_ONLY")
        self.assertEqual(self.check["source_manifests"], len(self.r["source_manifests"]))
        self.assertFalse(self.check["archive_complete"])
        self.assertFalse(self.check["download_authorized"])
        for p in self.core+self.opt:
            self.assertFalse(p["download_approved"])
            self.assertFalse(p["fully_runtime_executable"])
            for f in p["files"]:
                self.assertRegex(f["revision"], r"^[a-f0-9]{40}$")
                self.assertFalse(f["body_downloaded"])
                self.assertFalse(f["local_full_sha_verified"])

    def test_core_fifteen_packages_sum_and_only_known_shared_vae(self):
        calc = aggregate(self.core)
        self.assertEqual(calc["publisher_file_bytes_before_sha_reuse"],392_782_078_397)
        self.assertEqual(calc["publisher_sha_reusable_bytes"],507_591_892)
        self.assertEqual(calc["publisher_sha_unique_bytes"],392_274_486_505)
        repeats = calc["publisher_sha_identical_repeated_files"]
        self.assertEqual(len(repeats),1)
        self.assertEqual(repeats[0]["sha256"],
                         "d6e524b3fffede1787a74e81b30976dce5400c4439ba64222168e607ed19e793")
        self.assertEqual(repeats[0]["first_package"],"R23/wan-animate2")
        self.assertEqual(repeats[0]["later_package"],"R23/longcat-avatar15")
        self.assertEqual(repeats[0]["first_path"],"vae/diffusion_pytorch_model.safetensors")

    def test_two_distinct_video_models_share_exact_original_vae_file(self):
        wan = next(x for x in self.core if x["package_id"] == "R23/wan-animate2")
        cat = next(x for x in self.core if x["package_id"] == "R23/longcat-avatar15")
        wv = next(f for f in wan["files"] if f["path"]=="vae/diffusion_pytorch_model.safetensors")
        cv = next(f for f in cat["files"] if f["path"]=="vae/diffusion_pytorch_model.safetensors")
        self.assertNotEqual(wv["repo_id"],cv["repo_id"])
        self.assertEqual(wv["bytes"],507_591_892)
        self.assertEqual(wv["bytes"],cv["bytes"])
        self.assertEqual(wv["source_sha256"],cv["source_sha256"])
        self.assertNotEqual(wan["classification"],"ORDINARY_QUANTIZATION_DUPLICATE")
        self.assertNotEqual(cat["classification"],"ORDINARY_QUANTIZATION_DUPLICATE")

    def test_with_optional_ltx_specials_preserves_training_states(self):
        calc=aggregate(self.core+self.opt)
        self.assertEqual(calc["publisher_file_bytes_before_sha_reuse"],471_259_070_013)
        self.assertEqual(calc["publisher_sha_reusable_bytes"],507_591_892)
        self.assertEqual(calc["publisher_sha_unique_bytes"],470_751_478_121)
        self.assertEqual({x["package_id"] for x in self.opt},
                         {"OPTIONAL/Chris-LTX25-FP8","OPTIONAL/Stubelius-v1-BF16"})
        self.assertTrue(all(x["classification"].startswith("SEPARATE_SPECIAL_") for x in self.opt))

    def test_exact_sha_also_deduplicates_prior_evidence_not_extra_asset(self):
        x=self.r["cross_round_source_evidence"]
        self.assertTrue(x["round19_chatr_original_vs_r21_same_sha"])
        self.assertTrue(x["round19_chatr_source_reported_bytes_equal_r21"])
        self.assertTrue(x["round19_media_evidence_not_separate_download"])

    def test_93_missing_sha_cannot_be_counted_as_verified_duplicate(self):
        self.assertEqual(aggregate(self.core)["sha_unknown_file_references"],93)
        self.assertEqual(aggregate(self.core+self.opt)["sha_unknown_file_references"],93)
        self.assertFalse(self.r["policy"]["existing_local_shas_examined"])
        self.assertTrue(self.r["policy"]["unverified_sha_support_not_falsely_deduped"])

    def test_alt_formats_and_special_history_not_pruned(self):
        options=self.r["not_included_alt_formats"]
        self.assertTrue(any("mistral4-native" in s for s in options))
        self.assertTrue(any("gptoss120-original" in s for s in options))
        self.assertTrue(any("Stubelius intermediate" in s for s in options))
        self.assertTrue(self.r["policy"]["optional_derived_special_states_preserved_not_pruned"])

    def test_budget_and_user_selected_unaffected(self):
        limits=read("policies/limits.json")
        current=read("catalog/effective-portfolio-2026-11-06-v19.json")
        queue=read("queues/approved.json")
        portfolio=current
        self.assertEqual(limits["archive_target_bytes"],4_000_000_000_000)
        self.assertEqual(limits["minimum_free_bytes"],200_000_000_000)
        self.assertEqual(current["counts"]["tracked"],150)
        self.assertEqual(current["counts"]["active"],105)
        self.assertEqual(len(portfolio["items"]),150)
        self.assertEqual(next(x for x in portfolio["items"] if x["repo_id"]=="Nanbeige/Nanbeige4.3-33B")["portfolio_decision"],"select")
        self.assertEqual(queue["entries"],[])
        self.assertEqual(self.r["policy"]["queue_approvals_added"],0)
        self.assertEqual(self.r["policy"]["model_weights_downloaded"],0)
        self.assertIsNone(self.r["policy"]["physical_disk_free_bytes"])

if __name__=="__main__":
    unittest.main()
