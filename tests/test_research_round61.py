"""R61: Pruna archival original vs compressed Comfy: static exact source checks."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):
    q=(ROOT/p).resolve()
    if not q.is_relative_to(ROOT.resolve()):raise ValueError("path escapes repo")
    return json.loads(q.read_text(encoding="utf-8"))
class R61(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=read("catalog/research/2026-11-14-r61-pruna-source-curve-capacity.json")
        cls.d=read("manifests/drafts/r61-pruna-original-and-comfy-comparators.candidate.json")
    def test_fixed_44_original_files_and_dedup(self):
        o=self.a["preservation_original"]
        self.assertEqual(o["file_reference_count"],44)
        self.assertEqual(o["learned_safetensors_count"],15)
        self.assertEqual(o["logical_source_bytes"],99840428064)
        self.assertEqual(o["unique_content_bytes_under_sha_and_gitblob_dedup"],99828998036)
        self.assertEqual(o["logical_source_bytes"]-o["unique_content_bytes_under_sha_and_gitblob_dedup"],11430028)
        self.assertEqual(len(o["duplicate_path_groups"]),5)
        self.assertEqual(sum(x["bytes"] for x in o["source_files"]),o["logical_source_bytes"])
        self.assertFalse(o["complete_offline_rebuild_proven"])
        self.assertFalse(o["owner_authorized_download"])
        self.assertEqual(len({x["path"] for x in o["source_files"]}),44)
    def test_three_execution_profiles_are_alternatives(self):
        a=self.a["runtime_representation_alternatives"]["comfy_component_profiles"]
        for name,base,full in [("bf16",55165475664,74471781216),
                               ("int8",29480935784,39229053508),
                               ("w4a8",20084601325,26808697441)]:
            self.assertEqual(a[name]["core"]["exact_bytes"],base)
            self.assertEqual(a[name]["full"]["exact_bytes"],full)
            self.assertEqual(sum(f["bytes"] for f in a[name]["core"]["files"]),base)
            self.assertEqual(sum(f["bytes"] for f in a[name]["full"]["files"]),full)
            self.assertEqual(len(a[name]["core"]["files"]),3)
            self.assertEqual(len(a[name]["full"]["files"]),4)
        self.assertEqual(a["w4a8"]["publisher_documentation_example"]["exact_bytes"],39390906877)
        self.assertTrue(self.d["disallow_simultaneous_download_of_all_formats"])
    def test_diffusers_638_keys_are_not_lossless_comfy_claim(self):
        r=self.a["implementation_and_structural_evidence"]
        self.assertEqual(r["pruna_diffusers"]["original_index_tensor_name_count"],638)
        self.assertEqual(r["pruna_diffusers"]["original_index_tensor_data_bytes"],66280430080)
        self.assertEqual(r["comfy"]["code_commit"],"eee59185ff4f43ae2d9ad122b245619d27d9daad")
        self.assertFalse(r["pruna_diffusers"]["exact_safetensors_tensor_value_parity_with_comfy_verified"])
        self.assertFalse(r["comfy"]["local_runtime_abi_checked"])
        self.assertTrue(self.a["conclusions"]["v32_total_135_assets_source_union_finalized"] is False)
    def test_nonexecuting_main_unchanged(self):
        c=read("catalog/CURRENT.json")
        self.assertEqual((c["revision_id"],c["expected"]["tracked"],c["expected"]["active"]),("v32-20261114",182,135))
        self.assertEqual(c["latest_pruna_original_source_scope_audit"]["path"],"catalog/research/2026-11-14-r61-pruna-source-curve-capacity.json")
        self.assertEqual(read("queues/approved.json")["entries"],[])
        self.assertFalse(self.d["download_enabled"])
        self.assertFalse(self.d["approved"])
        self.assertFalse(self.d["preferred_archival_candidate"]["can_enter_approved_queue"])
if __name__=="__main__":unittest.main()
