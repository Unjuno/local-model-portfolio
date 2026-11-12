"""v19 extraordinary compact model portfolio checks; offline stdlib only."""
import json
import re
import unittest
from pathlib import Path
from scripts.check_parameter_cutoff import validate_model,LOW
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
class V19SmallSpecializationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current=load("catalog/CURRENT.json")
        cls.view=load("catalog/effective-portfolio-2026-11-06-v19.json")
        cls.q=load("queues/proposed-v19-2026-11-06.json")
        cls.r=load("catalog/research/2026-11-06-small-model-r26.json")
    def test_counts_and_queue_identity(self):
        # v19 remains an immutable historical view after CURRENT advances.
        v=self.view; c=self.current
        self.assertEqual(v["revision_id"],"v19-20261106")
        self.assertEqual(self.q["source_revision"],v["revision_id"])
        self.assertEqual(len(v["items"]),150)
        keys=[(x["asset_kind"],x["repo_id"]) for x in v["items"]]
        self.assertEqual(len(keys),len(set(keys)))
        chosen={(x["asset_kind"],x["repo_id"]) for x in v["items"] if x["portfolio_decision"] in ("select","conditional")}
        offered={(x["asset_kind"],x["repo_id"]) for x in self.q["candidates"]}
        self.assertEqual(len(chosen),105)
        self.assertEqual(chosen,offered)
        expected={"v19-20261106":(150,105),"v20-20261106":(154,108),"v21-20261106":(159,112),"v22-20261106":(163,116),"v23-20261106":(165,118),"v24-20261106":(168,121),"v25-20261106":(169,122),"v26-20261106":(172,125),"v27-20261107":(173,126),"v28-20261112":(175,128)}
        self.assertIn(c["revision_id"],expected)
        tracked,active=expected[c["revision_id"]]
        cv=load(c["materialized_catalog_path"])
        cq=load(c["priority_worklist_path"])
        self.assertEqual(cv["revision_id"],c["revision_id"])
        self.assertEqual(cq["source_revision"],c["revision_id"])
        self.assertEqual(c["expected"]["tracked"],tracked)
        self.assertEqual(c["expected"]["active"],active)
        self.assertEqual(len(cv["items"]),tracked)
        ck={(x["asset_kind"],x["repo_id"]) for x in cv["items"]}
        ca={(x["asset_kind"],x["repo_id"]) for x in cv["items"] if x["portfolio_decision"] in ("select","conditional")}
        self.assertEqual(len(ck),tracked)
        self.assertEqual(len(ca),active)
        self.assertEqual(len(cq["candidates"]),active)
        self.assertEqual(ca,{(x["asset_kind"],x["repo_id"]) for x in cq["candidates"]})
        if c["revision_id"]=="v20-20261106":
            self.assertEqual(cv["items"][:150],v["items"])
            self.assertEqual(load("policies/limits.json")["archive_target_bytes"],4000000000000)
    def test_exact_six_new_and_evidence_scope(self):
        rows=self.r["source_weight_evidence"]; self.assertEqual(len(rows),6)
        m={x["repo_id"]:x for x in self.view["items"]}
        for w in rows:
            x=m[w["repo_id"]]
            self.assertEqual(x["portfolio_decision"],"conditional")
            self.assertEqual(x["parameter_gate"]["status"],LOW)
            self.assertEqual(validate_model(x),[])
            self.assertEqual(x["source_weight"]["source_reported_bytes"],w["bytes"])
            self.assertEqual(x["source_weight"]["source_reported_sha256"],w["sha"])
            self.assertRegex(w["sha"],r"^[0-9a-f]{64}$")
            self.assertIsNone(x["fully_pinned_revision_sha"])
            self.assertIsNone(x["selected_file_bytes"])
            self.assertIs(x["download_approved"],False)
            self.assertIs(x["source_weight"]["full_file_local_sha256_verified"],False)
            self.assertIs(x["regulation_evidence"]["human_performance_legal_threshold_verified"],False)
    def test_real_total_parameters_and_pair_dependencies(self):
        m={x["repo_id"]:x for x in self.view["items"]}
        self.assertEqual(m["IFM/K2-Horizon-0.9B"]["parameter_gate"]["total_parameters"],1_078_285_824)
        self.assertEqual(m["LiquidAI/LFM2.5-VL-3B-DSpark"]["parameter_gate"]["total_parameters"],3_403_000_000)
        self.assertEqual(m["LiquidAI/LFM2.5-VL-3B-DSpark"]["draft_parameters"],279_500_000)
        self.assertEqual(m["udgamlabs/Lilavati-Checker"]["parameter_gate"]["total_parameters"],189_400_000)
        for k in ("LiquidAI/LFM2.5-VL-3B-DSpark","udgamlabs/Lilavati-Checker"):
            self.assertEqual(len(m[k]["additional_learned_dependencies"]),1)
    def test_source_weight_storage_not_full_manifest(self):
        r=self.r
        self.assertEqual(sum(w["bytes"] for w in r["source_weight_evidence"]),12_799_213_698)
        self.assertEqual(r["weight_bytes_total_selected_6"],12_799_213_698)
        self.assertIsNone(r["all_selected_files_bytes"])
        self.assertFalse(r["download_authorized"])
        self.assertFalse(r["payloads_downloaded"])
    def test_regulation_not_invented(self):
        sources=self.r["china_regulation_source_register"]
        self.assertGreaterEqual(len(sources),2)
        self.assertTrue(any("2026-04/30" in s["source"] for s in sources))
        self.assertFalse(self.r["risk_prediction"]["verified_official_rule"])
        self.assertIsNone(self.r["risk_prediction"]["likelihood_numeric"])
        self.assertTrue(all(s["binding_specific_human_threshold"] is False for s in sources))
    def test_official_mofcom_proposal_and_open_source_exception(self):
        records=self.r["china_regulation_source_register"]
        primary=next(x for x in records if x.get("type")=="MOFCOM_MOST_ANNOUNCEMENT_48_2026_INTERIM_EXPORT_REGISTRATION_AND_PROPOSED_CATALOGUE")
        self.assertEqual(primary["published"],"2026-10-16")
        self.assertEqual(primary["legal_stage"],"CATALOGUE_PUBLIC_COMMENT_WITH_INTERIM_EXPORT_REGISTRATION")
        self.assertIs(primary["previously_public_opensource_technology_excluded"],True)
        self.assertIs(primary["superhuman_performance_automatic_ban_enacted"],False)
        self.assertIs(primary["blanket_weight_takedown_announced"],False)
        self.assertIs(primary["binding_specific_human_threshold"],False)
    def test_existing_user_protections_and_approvals(self):
        m={x["repo_id"]:x for x in self.view["items"]}
        self.assertEqual(m["Nanbeige/Nanbeige4.3-33B"]["portfolio_decision"],"select")
        exc=["state-spaces/mamba-2.8b","Wigtn/Qwen3-VL-2B-WigtnOCR","Wigtn/KoGovDoc-Bench","qvac/TranscribePsy-250M-EU","nvidia/nemotron-labs-unified-asr-0.6b","PerceptronAI/Isaac-0.2-2B-Preview"]
        self.assertTrue(all(m[rid]["portfolio_decision"]=="excluded" for rid in exc))
        self.assertEqual(load("queues/approved.json")["entries"],[])
        self.assertFalse(self.q["approved"])
        self.assertFalse(self.q["download_enabled"])
        self.assertTrue(all(x["not_authorized"] and x["download_approved"] is False for x in self.q["candidates"]))
    def test_research_alternates_not_falsely_available(self):
        self.assertEqual(len(self.r["alternate_research_only"]),4)
        r=next(x for x in self.r["alternate_research_only"] if x.get("repo_id")=="microsoft/Orchard-GUI-4B")
        self.assertIs(r["model_checkpoint_public"],False)
        active={x["repo_id"] for x in self.view["items"]}
        self.assertNotIn("microsoft/Orchard-GUI-4B",active)
        self.assertNotIn("XHToken/Spark-X2.6-1.7B",active)
    def test_conditional_is_not_superhuman_independent(self):
        for x in self.r["selected"]:
            self.assertFalse(x["legal_human_surpassing_threshold_verified"])
            self.assertFalse(x["full_pinned_manifest"])
if __name__=="__main__":unittest.main()
