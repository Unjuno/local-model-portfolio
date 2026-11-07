"""R37 Chatterbox immutable source-state and shared decoder audit; metadata only."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class R37ChatterboxArchiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = load("catalog/research/2026-11-08-r37-chatterbox-versioned-source-manifest.json")
        cls.current = load("catalog/CURRENT.json")
        cls.queue = load("queues/approved.json")
        cls.pack = cls.r["language_packs"]["entries"]

    def test_nine_pinned_repos_include_single_language_variants(self):
        rs = self.r["source_repositories"]
        self.assertEqual(len(rs), 9)
        self.assertEqual(len({x["id"] for x in rs}), 9)
        for x in rs:
            self.assertRegex(x["sha"], r"^[a-f0-9]{40}$")
            self.assertGreater(x["source_repo_bytes"], 0)
        self.assertEqual(self.r["source_repositories"][0]["source_repo_bytes"], 13_866_212_931)

    def test_official_v3_loader_is_explicit_not_default_v2(self):
        code = self.r["reference_implementation"]
        self.assertIn('t3_model="v3"', code["v3_explicit_argument"])
        self.assertTrue(code["default_without_argument"].startswith("v2"))
        self.assertEqual(code["standard_decoder_path"], "s3gen.pt")
        self.assertTrue(code["loader_rev_immutable_pinned"])
        self.assertEqual(code["source_commit_sha"],
                         "ab55923c27757c90cfcc407baa57dc25a7d25217")
        self.assertIn(code["source_commit_sha"], code["pinned_multilingual_loader_url"])
        self.assertIn(code["source_commit_sha"], code["pinned_turbo_nano_loader_url"])

    def test_v3_six_files_match_pinned_source_and_total(self):
        v3 = self.r["multilingual_v3"]
        files = v3["selected_files"]
        self.assertEqual(len(files), 6)
        self.assertEqual(sum(f["bytes"] for f in files), 3_208_951_924)
        self.assertEqual(v3["selected_six_file_bytes"], 3_208_951_924)
        self.assertIn("t3_mtl23ls_v3.safetensors", [x["path"] for x in files])
        self.assertIn("s3gen.pt", [x["path"] for x in files])
        self.assertNotIn("s3gen_v3.safetensors", [x["path"] for x in files])
        self.assertRegex(v3["main_v3_t3"]["sha256"], r"^[a-f0-9]{64}$")
        self.assertEqual(v3["v2_alternative"]["additional_bytes_to_keep_v2_with_v3_source"], 2_143_989_752)

    def test_six_language_t3_are_different_trained_finetunes(self):
        self.assertEqual(len(self.pack), 6)
        self.assertTrue(self.r["language_packs"]["different_t3_sha"])
        self.assertEqual(len({x["unique_t3"]["sha256"] for x in self.pack}), 6)
        self.assertTrue(all(x["kind"] == "SPECIAL_LANGUAGE_FINETUNE_NOT_QUANTIZED_BASE" for x in self.pack))
        self.assertFalse(self.r["language_packs"]["contains_dedicated_japanese_model"])

    def test_s3gen_v3_is_exactly_shared_across_language_packs(self):
        pt = self.pack[0]["common_s3gen_v3_pt"]
        safe = self.pack[0]["common_s3gen_v3_safetensors"]
        self.assertTrue(all(x["common_s3gen_v3_pt"]["sha256"] == pt["sha256"] for x in self.pack))
        self.assertTrue(all(x["common_s3gen_v3_safetensors"]["sha256"] == safe["sha256"] for x in self.pack))
        self.assertRegex(pt["sha256"], r"^[a-f0-9]{64}$")
        self.assertRegex(safe["sha256"], r"^[a-f0-9]{64}$")
        self.assertNotEqual(pt["sha256"], safe["sha256"])
        z = self.r["totals"]
        self.assertEqual(z["six_language_unique_t3_files_bytes"], 12_863_941_240)
        self.assertEqual(z["six_pack_one_shared_s3gen_v3_pt_plus_six_t3_bytes"], 13_920_844_934)
        self.assertGreater(z["six_pack_entire_repo_download_bytes"],
                           z["six_pack_one_shared_s3gen_v3_pt_plus_six_t3_bytes"])

    def test_turbo_nano_are_separate_t3_but_one_meanflow_decoder(self):
        a,b = self.r["turbo_and_nano"]["entries"]
        self.assertNotEqual(a["unique_t3"]["sha256"], b["unique_t3"]["sha256"])
        self.assertEqual(a["shared_meanflow"]["sha256"], b["shared_meanflow"]["sha256"])
        self.assertEqual(a["shared_ve"]["sha256"], b["shared_ve"]["sha256"])
        self.assertEqual(self.r["totals"]["turbo_nano_unique_t3_and_one_meanflow_bytes"],
                         3_850_254_292)
        self.assertIn("S3Gen(meanflow=True)", self.r["turbo_and_nano"]["loader_behavior"])

    def test_archive_risk_is_maintenance_not_unverified_takedown(self):
        self.assertIn("retired research", self.r["first_party_status"]["as_of_august_2026"].lower())
        self.assertIn("NOT evidence", self.r["first_party_status"]["as_of_august_2026"])
        self.assertFalse(self.r["quality_and_scope"]["independent_claim_v3_better_not_verified"] is False)
        self.assertFalse(self.r["rights_and_security"]["source_revision_for_loader_unpinned"])

    def test_source_code_pin_explains_actual_v3_and_meanflow_file_choice(self):
        source = self.r["reference_implementation"]["verified_pinned_loader_behavior"]
        self.assertEqual(source["multilingual_default"], "t3_mtl23ls_v2.safetensors")
        self.assertEqual(source["v3_opt_in"], "t3_mtl23ls_v3.safetensors")
        self.assertEqual(source["standard_s3gen_loaded"], "s3gen.pt")
        self.assertEqual(source["turbo_nano_decoder_loaded"], "s3gen_meanflow.safetensors")
        self.assertFalse(self.r["reference_implementation"]["runtime_quality_user_measured"])

    def test_existing_selection_and_queue_unchanged(self):
        self.assertEqual(self.current["expected"]["tracked"], 150)
        self.assertEqual(self.current["expected"]["active"], 105)
        self.assertEqual(self.current["expected"]["archive_limit_bytes"], 4_000_000_000_000)
        self.assertTrue(self.r["decision"]["existing_chatterbox_select_unchanged"])
        self.assertEqual(self.r["decision"]["downloads"], 0)
        self.assertEqual(self.queue["entries"], [])

if __name__ == "__main__":
    unittest.main()
