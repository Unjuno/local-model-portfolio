"""R58 fail-closed audit, all seven active unresolved source-weight identities."""
import json
import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(p): return json.loads((R/p).read_text(encoding="utf-8"))
class R58(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=read("catalog/research/2026-11-14-r58-seven-active-unknown-dependency-and-format.json")
    def test_exact_seven_active_parameter_unknown(self):
        current=read("catalog/CURRENT.json");view=read(current["materialized_catalog_path"])
        self.assertEqual(current["revision_id"],"v32-20261114")
        self.assertEqual((current["expected"]["tracked"],current["expected"]["active"]),(182,135))
        unknown={x["repo_id"] for x in view["items"] if x["asset_kind"]=="model"
                 and x["portfolio_decision"] in ("select","conditional")
                 and x.get("parameter_gate",{}).get("status")=="UNVERIFIED_BLOCK_FINAL_LOCK"}
        self.assertEqual(len(unknown),7)
        self.assertEqual({x["repo_id"] for x in self.data["records"]},unknown)
        self.assertFalse(read("queues/approved.json")["entries"])
        self.assertEqual(self.data["parameter_gate_changes"],0)
        self.assertEqual(self.data["download_approvals_created"],0)
    def test_publisher_sha_and_subset_not_approved(self):
        self.assertEqual(len(self.data["records"]),7)
        self.assertTrue(self.data["source_metadata_observed_complete_7_of_7"])
        for x in self.data["records"]:
            self.assertRegex(x["publisher_revision_sha"],r"^[a-f0-9]{40}$")
            self.assertIs(x["full_trained_pipeline_parameters_verified"],False)
            self.assertIs(x["owner_entitlement_verified"],False)
            self.assertIs(x["download_authorized"],False)
            self.assertEqual(x["weight_like_file_count"],len(x["all_publisher_weight_file_options"]))
            self.assertEqual(x["chosen_source_subset_weight_bytes"],
                             sum(f["size_bytes"] for f in x["chosen_source_subset_nonexecuting"]) or None)
            for f in x["all_publisher_weight_file_options"]:
                self.assertIs(f["local_file_sha256_verified"],False)
                if f["publisher_lfs_sha256"] is not None: self.assertRegex(f["publisher_lfs_sha256"],r"^[a-f0-9]{64}$")
    def test_no_semantic_quant_dedupe_of_trained_stages(self):
        by={x["repo_id"]:x for x in self.data["records"]}
        l=by["ausboss/Qwen-Image-2.1-Consistency-LoRA"]["chosen_source_subset_nonexecuting"]
        self.assertEqual(len(l),2)
        self.assertEqual(l[0]["size_bytes"],159436496)
        self.assertEqual(l[1]["size_bytes"],159436496)
        self.assertNotEqual(l[0]["publisher_lfs_sha256"],l[1]["publisher_lfs_sha256"])
        f=by["fishaudio/drama-3"]["chosen_source_subset_nonexecuting"]
        self.assertEqual(len(f),16)
        self.assertEqual(next(x["size_bytes"] for x in f if x["path"]=="codec.pth"),1871099728)
        self.assertEqual(len(by["PrunaAI/P-H3-Image"]["chosen_source_subset_nonexecuting"]),15)
        self.assertEqual(len(by["maya-research/maya2-native"]["chosen_source_subset_nonexecuting"]),2)
        s=by["Stuubs/Stubelius_Remix_Ltx2.5"]
        self.assertTrue(s["revision_drift_since_r51"])
        self.assertEqual(len(s["chosen_source_subset_nonexecuting"]),1)
        self.assertEqual(s["chosen_source_subset_nonexecuting"][0]["size_bytes"],42008732600)
    def test_gated_and_missing_legal_status_blocked(self):
        steer=next(x for x in self.data["records"] if x["repo_id"]=="WhissleAI/steer-tts")
        self.assertEqual(steer["public_hub_gated"],"auto")
        self.assertEqual(steer["hub_license_tag"],"cc-by-nc-4.0")
        self.assertEqual(self.data["full_offline_archive_capacity_bytes"],None)
        self.assertEqual(self.data["source_git_revision_drift"][0]["id"],"Stuubs/Stubelius_Remix_Ltx2.5")
if __name__=="__main__":
    unittest.main()
