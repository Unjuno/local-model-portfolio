"""R33 immutable donor-lineage and representation audit; metadata-only, no downloads."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R32 = ROOT / "catalog/research/2026-11-07-r32-ltx-donor-chain.json"
R33 = ROOT / "catalog/research/2026-11-07-r33-ltx-exact-donor-and-adapter-conversion.json"


class R33ArchiveEvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r33 = json.loads(R33.read_text(encoding="utf-8"))
        cls.r32 = json.loads(R32.read_text(encoding="utf-8"))
        cls.files = {row["role"]: row for row in cls.r33["primary_files"]}

    def test_full_sha_and_exact_lfs_bytes(self):
        self.assertEqual(len(self.files), 3)
        for x in self.files.values():
            self.assertRegex(x["source_git_commit"], r"^[0-9a-f]{40}$")
            self.assertRegex(x["sha256"], r"^[0-9a-f]{64}$")
            self.assertGreater(x["bytes"], 0)
            self.assertTrue(x["source"].startswith("https://huggingface.co/"))

    def test_tenstrip_stubelius_donor_is_v15_not_v1(self):
        x = self.files["STUUBS_ACTUAL_10EROS_V15_DONOR"]
        self.assertEqual(x["file"], "10Eros_v1.5_bf16.safetensors")
        self.assertEqual(x["bytes"], 46_139_886_366)
        self.assertEqual(x["sha256"], "2383d87bc1eea4fc00b73a52eb177bea868c2c46da621511acf9e54b92309f24")
        self.assertEqual(self.r33["corrected_lineage"]["stuubs_merges_10Eros_version"], "v1.5")
        self.assertTrue(self.r32["r33_mandatory_erratum"]["preserve_historical_v1_metadata_but_not_donor"])

    def test_original_lora_and_bf16_conversion_are_same_training(self):
        orig = self.files["OMNINFT_LTX23_ORIGINAL_FP32_SOURCE"]
        conv = self.files["OMNINFT_LTX23_KIJAI_BF16_RUNTIME_CONVERSION"]
        self.assertEqual(orig["bytes"], 1_233_512_728)
        self.assertEqual(conv["bytes"], 616_948_520)
        self.assertNotEqual(orig["sha256"], conv["sha256"])
        self.assertTrue(self.r33["original_rl_conversion"]["same_learned_adapter"])
        self.assertTrue(self.r33["original_rl_conversion"]["quantization_only_copy"])
        self.assertEqual(self.r33["original_rl_conversion"]["ui_strength_needed_for_kijai"], 2.0)

    def test_multiple_quant_files_not_counted_as_special_trained_states(self):
        x = self.r33["additional_quant_quality_counterexample"]
        self.assertEqual(len(x["variants"]), 2)
        self.assertEqual(x["variants"][0]["bytes"], 16_641_963_302)
        self.assertEqual(x["variants"][1]["bytes"], 19_107_895_342)
        self.assertIn("NOT", x["decision"])
        self.assertEqual(x["hiss_evidence"], "QUANTIZER_CREATOR_LISTENING_TEST_NOT_INDEPENDENT")

    def test_chris_historical_mirror_not_equated_to_current_weights(self):
        x = self.r33["chris_mirror_caveat"]
        self.assertRegex(x["mirror_creation_commit"], r"^[a-f0-9]{40}$")
        self.assertFalse(x["original_mirror_current_weight_sha_matched"])
        self.assertTrue(x["original_repo_changed_after_mirror"])

    def test_portfolio_and_approvals_unchanged(self):
        d = self.r33["decision"]
        self.assertEqual(d["new_select"], 0)
        self.assertEqual(d["new_formal_conditional"], 0)
        self.assertEqual(d["download_queue_changes"], 0)
        self.assertEqual(d["model_downloads"], 0)
        self.assertEqual(d["archive_target_bytes"], 4_000_000_000_000)
        c = json.loads((ROOT / "catalog/CURRENT.json").read_text(encoding="utf-8"))
        self.assertEqual(c["expected"]["tracked"], 150)
        self.assertEqual(c["expected"]["active"], 105)


if __name__ == "__main__":
    unittest.main()
