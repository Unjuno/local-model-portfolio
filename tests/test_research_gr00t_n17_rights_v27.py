"""Research-only GR00T N1.7 new learned stage and noncommercial LICENSE conflict."""
import copy
import unittest
from scripts import research_gr00t_n17_rights_v27 as m

def examples():
    license = ("NVIDIA License\n1. Definitions\n"
               "3.3 Use Limitation. The Work and any derivative works thereof only may be used "
               "or intended for use non-commercially. As used herein, non-commercially "
               "means for research or evaluation purposes only.")
    card="This model is released under the NVIDIA Open Model License Agreement."
    code=("GR00T N1.7 is fully commercially licensable under Apache 2.0.\n"
          "- **Code:** Apache 2.0 — see LICENSE\n- **Model weights:** [NVIDIA Open Model License](https://www.nvidia.com/...)\n")
    return (license,card,code)

class GR00T_N17_RightAudit(unittest.TestCase):
    def test_unchanged_model_catalog(self):
        c=m.load("catalog/CURRENT.json")
        self.assertEqual(c["revision_id"],"v27-20261107")
        self.assertEqual((c["expected"]["tracked"],c["expected"]["active"]),(173,126))
        self.assertFalse(m.load("queues/approved.json")["entries"])
        v=m.load(c["materialized_catalog_path"])
        ids={x["repo_id"] for x in v["items"]}
        self.assertIn(m.N16,ids)
        self.assertNotIn(m.N17,ids)
    def test_first_party_license_conflict_blocks_approval(self):
        o=m.classify_license(*examples())
        self.assertTrue(o["HF_license_section_3_3_noncommercial_research_evaluation_only"])
        self.assertTrue(o["contradictory_first_party_artifacts"])
        multiline=list(examples())
        multiline[0]=multiline[0].replace("research or evaluation purposes only",
                                       "research or\n evaluation purposes only")
        self.assertTrue(m.classify_license(*multiline)["contradictory_first_party_artifacts"])
        self.assertFalse(o["commercial_permission_verified"])
        self.assertFalse(o["download_approval_allowed"])
        s=list(examples())
        s[0]=s[0].replace("non-commercially","commercially")
        with self.assertRaises(ValueError):m.classify_license(*s)
        s=list(examples())
        s[2]=s[2].replace("[NVIDIA Open Model License]","[NVIDIA License]")
        with self.assertRaises(ValueError):m.classify_license(*s)
    def test_research_budget_not_a_physical_device(self):
        a=m.load("catalog/capacity/2026-11-07/v27/selected-file-capacity.json")
        original=copy.deepcopy(a)
        test={"revision":"e"*40,
            "recommended_original_file_scope_bytes":13579,
            "recommended_selected_files":[
              {"path":"model.safetensors","bytes":13579,
                "sha256":"d"*64,"identity_kind":"lfs_payload_sha256"}]}
        x=m.budget(a,test)
        self.assertEqual(a,original)
        self.assertEqual(x["N17_hash_identity_aware_logical_increment_bytes"],13579)
        self.assertEqual(x["research_hold_scenario_logical_bytes"],3_417_685_712_585+13579)
        self.assertIsNone(x["owner_disk_free_bytes"])
        self.assertIsNone(x["fully_restorable_archive_bytes"])
        self.assertEqual(x["model_payloads_downloaded"],0)
    def test_zero_or_duplicate_payload_bytes_fail_closed(self):
        base={"asset_kind":"model","repo_id":m.N17,"tree_complete":True,"gated":False,
             "pinned_revision":"e"*40,"payload_bytes_downloaded":0,"download_authorized":False,
             "files":[{"path":"model.safetensors","bytes":100,"sha256":"a"*64},
                      {"path":"LICENSE","bytes":40},
                      {"path":"README.md","bytes":40},
                      {"path":"config.json","bytes":40},
                      {"path":"processor_config.json","bytes":40},
                      {"path":"statistics.json","bytes":40}],
             "source_scope_bytes":300,"documentation":[
             {"path":"config.json","json":{"model_type":"Gr00tN1d7"}}]}
        got=m.weights_and_config(base)
        self.assertEqual(got["original_weight_bytes"],100)
        self.assertFalse(got["complete_model_embedded_backbone_verified"])
        bad=copy.deepcopy(base);bad["gated"]="manual"
        with self.assertRaises(ValueError):m.weights_and_config(bad)
        bad=copy.deepcopy(base);bad["files"].append(copy.deepcopy(bad["files"][0]))
        with self.assertRaises(ValueError):m.weights_and_config(bad)
        bad=copy.deepcopy(base);bad["files"][0]["bytes"]=0
        with self.assertRaises(ValueError):m.weights_and_config(bad)
if __name__=="__main__":unittest.main()
