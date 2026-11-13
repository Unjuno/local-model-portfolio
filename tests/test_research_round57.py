"""R57 metadata-only audit invariants: no network/payload loading."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
class R57(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=read("catalog/research/2026-11-14-r57-v32-frozen-source-scopes.json"); cls.d=read("manifests/drafts/r57-v32-three-source-scopes.candidate.json")
    def test_current_selected_portfolio_unchanged(self):
        c=read("catalog/CURRENT.json")
        self.assertEqual(c["revision_id"],"v32-20261114")
        self.assertEqual((c["expected"]["tracked"],c["expected"]["active"]),(182,135))
        self.assertEqual(read("queues/approved.json")["entries"],[])
        self.assertFalse(self.a["acquisition_gates"]["model_files_locally_downloaded"])
        self.assertFalse(self.d["download_enabled"])
    def test_three_exact_pinned_source_scopes(self):
        a=self.a;d=self.d
        self.assertEqual(a["statistics"]["source_file_references"],23)
        self.assertEqual(a["statistics"]["partial_upstream_bytes"],6191586316)
        self.assertEqual(len(a["files"]),3)
        self.assertEqual({z["repo_id"] for z in a["files"]},{"tencent/Qwen3.8-27B-DSpine-b16","nvidia/Nemotron-3-Diarization","nvidia/RFD4-Proteina"})
        self.assertEqual(len(d["selected_file_subsets"]),3)
        self.assertFalse(d["download_enabled"])
        self.assertFalse(d["approved"])
        for z in a["files"]:
            self.assertEqual(len(z["files"]),z["source_file_count"])
            self.assertEqual(z["source_scope_bytes"],sum(f["size_bytes"] for f in z["files"]))
            self.assertEqual(len({f["path"] for f in z["files"]}),len(z["files"]))
            self.assertRegex(z["revision"],"^[0-9a-f]{40}$")
            for f in z["files"]:
                self.assertGreater(f["size_bytes"],0)
                self.assertFalse(f["local_sha_verified"])
                if f["source_sha256"] is not None:self.assertRegex(f["source_sha256"],"^[0-9a-f]{64}$")
            self.assertEqual(sum(f["source_sha256"] is not None for f in z["files"]),1)
            self.assertFalse(z["download_authorized"])
            self.assertFalse(z["full_offline_package_complete"])
        self.assertEqual(sum(z["total_source_subset_bytes"] for z in d["selected_file_subsets"]),6191586316)
        self.assertTrue(all(not x["can_enter_approved_queue"] and not x["download_authorized"] for x in d["selected_file_subsets"]))
    def test_no_qwen_redundancy_and_rfd_release_consistency(self):
        q=self.a["qwen_parent_reuse"];r=self.a["rfd4_revision_identity"]
        self.assertEqual(q["same_weight_shard_sha256_and_bytes"],18)
        self.assertEqual(q["same_tokenizer_sha256_and_bytes"],1)
        self.assertEqual(q["additional_parent_bytes_to_acquire_for_dspine"],0)
        self.assertFalse(q["actual_dspine_target_runtime_tested"])
        self.assertTrue(r["root_model_sha_and_size_equal_between_recipe_and_latest"])
        self.assertTrue(r["root_config_git_blob_equal_between_recipe_and_latest"])
        self.assertTrue(r["readme_git_blob_changed"])
        self.assertTrue(r["provenance_git_blob_changed"])
        self.assertEqual(r["selected_source_snapshot"],"a06e2509c7033b010fc43614e9fd840303588502")
        pan=self.a["large_holds"][0]
        self.assertNotEqual(pan["vae_lfs_sha256"],pan["different_from_r40_common_wan_avatar_vae_sha256"])
    def test_sha_missing_for_text_is_not_invented(self):
        x=self.a["files"][0]
        self.assertIsNone(next(t for t in x["files"] if t["path"]=="README.md")["source_sha256"])
        self.assertTrue(self.d["external_dependencies_not_included"])
        self.assertTrue(self.d["sha256_of_text_files_not_claimed_from_git_blob_sha1"])
if __name__=="__main__":unittest.main()
