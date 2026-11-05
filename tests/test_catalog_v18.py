"""Read-only tests for v18 source-pinned candidate promotion. Standard library only."""
import json, unittest
from pathlib import Path
from scripts.check_parameter_cutoff import validate_model,LOW

ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
class V18Promotions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current=load("catalog/CURRENT.json")
        cls.view=load("catalog/effective-portfolio-2026-11-05-v18.json")
        cls.queue=load("queues/proposed-v18-2026-11-05.json")
        cls.census=load("catalog/preparation/2026-11-05-component-census.json")
        cls.r21=load("manifests/drafts/round21-pinned-preservation.candidate.json")
    def test_144_unique_and_99_active(self):
        items=self.view["items"]
        self.assertEqual(self.view["revision_id"],"v18-20261105")
        self.assertEqual(len(items),144)
        keys={(x["asset_kind"],x["repo_id"]) for x in items}
        self.assertEqual(len(keys),144)
        active={(x["asset_kind"],x["repo_id"]) for x in items if x["portfolio_decision"] in ("select","conditional")}
        self.assertEqual(len(active),99)
        self.assertEqual(active,{(x["asset_kind"],x["repo_id"]) for x in self.queue["candidates"]})
        self.assertEqual(len(self.view["items"]),144)
        self.assertEqual(len(active),99)
    def test_exact_two_new_identity_and_pinned_revisions(self):
        repos={x["repo_id"]:x for x in self.view["items"]}
        ids=["chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1","InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF"]
        for id in ids:
            r=repos[id]
            self.assertEqual(r["portfolio_decision"],"conditional")
            self.assertEqual(r["parameter_gate"]["status"],LOW)
            self.assertEqual([],validate_model(r))
            self.assertFalse(r["download_approved"])
            self.assertTrue(r["license_text_reviewed"])
            self.assertTrue(r["dependencies_reviewed"])
            self.assertRegex(r["fully_pinned_revision_sha"],r"^[0-9a-f]{40}$")
            self.assertFalse(r["reproducibility_package"]["local_weights_hash_verified"])
        self.assertEqual(repos[ids[0]]["fully_pinned_revision_sha"],"aa213272180d6ad0d03f5fb3d597f0f0322647c5")
        self.assertEqual(repos[ids[1]]["fully_pinned_revision_sha"],"e6924b3a08765341e01546308ccf2683d43e880b")
        self.assertEqual(repos[ids[0]]["source_relation"].count("Qwen/Qwen-Image-2.1")>0,True)
    def test_r22_full_pipeline_census_is_pinned(self):
        repos={x["repo_id"]:x for x in self.view["items"]}
        self.assertEqual(repos["chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1"]["parameter_gate"]["total_parameters"],self.census["packages"]["chatr-image"]["serialized_scalar_total"])
        self.assertEqual(repos["InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF"]["parameter_gate"]["total_parameters"],self.census["packages"]["interpretic-q4"]["serialized_scalar_total"])
        self.assertLess(self.census["packages"]["chatr-image"]["serialized_scalar_total"],150_000_000_000)
        self.assertLess(self.census["packages"]["interpretic-q4"]["serialized_scalar_total"],150_000_000_000)
        self.assertEqual(self.census["adapter_compatibility"]["matched_pairs"],224)
    def test_r21_exact_storage_and_no_false_disk_savings(self):
        repos={x["repo_id"]:x for x in self.view["items"]}
        self.assertEqual(repos["chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1"]["reproducibility_package"]["complete_pinned_package_bytes"],33802789787)
        self.assertEqual(repos["InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF"]["reproducibility_package"]["complete_pinned_package_bytes"],17738357352)
        self.assertEqual(33802789787+17738357352,51541147139)
        self.assertIsNone(repos["chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1"]["reproducibility_package"]["actual_incremental_bytes"])
        self.assertFalse(self.r21["download_authorized"])
    def test_no_acquisition_or_reuse_assertion(self):
        self.assertIs(self.queue["approved"],False)
        self.assertIs(self.queue["download_enabled"],False)
        for x in self.queue["candidates"]:
            self.assertIs(x["not_authorized"],True)
            self.assertIs(x["download_approved"],False)
        approved=load("queues/approved.json")
        self.assertEqual(approved["entries"],[])
        r={x["repo_id"]:x for x in self.view["items"]}
        for id in ["chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1","InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF"]:
            self.assertFalse(r[id]["reproducibility_package"]["hardware_tested_on_user_machine"])
            self.assertFalse(r[id]["reproducibility_package"]["explicit_acquisition_approval"])
            self.assertIsNone(r[id]["reproducibility_package"]["measured_user_peak_ram_bytes"] if "measured_user_peak_ram_bytes" in r[id]["reproducibility_package"] else None)
    def test_protect_user_choices_and_historic_research(self):
        repos={x["repo_id"]:x for x in self.view["items"]}
        self.assertEqual(repos["Nanbeige/Nanbeige4.3-33B"]["portfolio_decision"],"select")
        excluded=["state-spaces/mamba-2.8b","Wigtn/Qwen3-VL-2B-WigtnOCR","Wigtn/KoGovDoc-Bench","qvac/TranscribePsy-250M-EU","nvidia/nemotron-labs-unified-asr-0.6b","PerceptronAI/Isaac-0.2-2B-Preview"]
        self.assertTrue(all(repos[x]["portfolio_decision"]=="excluded" for x in excluded))
        self.assertFalse(self.r21["packages"][0]["formal_catalog_member_added"]) # historical pre-v18 snapshot preserved
    def test_checksum_discrepancies_not_hidden(self):
        repos={x["repo_id"]:x for x in self.view["items"]}
        a=repos["chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1"]
        self.assertEqual(set(a["reproducibility_package"]["checksum_discrepancy_files"]),{"README.md","inference.py"})
        self.assertFalse(a["reproducibility_package"]["checksum_discrepancy_is_proof_of_model_corruption"])
        self.assertEqual(len(self.census["publisher_checksum_discrepancies"]),2)
if __name__=="__main__":unittest.main()
