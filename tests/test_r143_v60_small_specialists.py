"""Offline metadata-only v60 selection, source freeze, STOP gate test."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))

class V60Specialists(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=load("catalog/CURRENT.json")
        cls.old=load("catalog/effective-portfolio-2026-11-21-v59.json")
        cls.e=load("catalog/effective-portfolio-2026-11-22-v60.json")
        cls.d=load("catalog/revisions/v60-2026-11-22.json")
        cls.m=load("manifests/drafts/r143-2026-11-22-three-specialists-originals.candidate.json")
        cls.q=load("queues/proposed-v60-2026-11-22.json")
        cls.a=load("catalog/access/2026-11-22-v60-conditional-hub-gates.json")
        cls.r=load("catalog/readiness/v60-2026-11-22-r143-all177-gates.json")
        cls.p=load("catalog/preparation/2026-11-22-insurance-bundles-v60.json")
        cls.decision=load("catalog/decisions/2026-11-22-r143-v60-three-small-specialists.json")

    def test_canonical_and_old_immutable(self):
        self.assertIn(self.c["revision_id"],("v60-20261122","v61-20261122","v62-20261122","v63-20261122", "v64-20261122","v65-20261122", "v66-20261124", "v67-20261124","v68-20261125","v69-20261125","v70-20261125"))
        self.assertIn("catalog/revisions/v60-2026-11-22.json",self.c["ordered_overlays"])
        self.assertIn(self.c["materialized_catalog_path"],("catalog/effective-portfolio-2026-11-22-v60.json","catalog/effective-portfolio-2026-11-22-v61.json","catalog/effective-portfolio-2026-11-22-v62.json","catalog/effective-portfolio-2026-11-22-v63.json","catalog/effective-portfolio-2026-11-22-v64.json", "catalog/effective-portfolio-2026-11-22-v65.json", "catalog/effective-portfolio-2026-11-24-v66.json", "catalog/effective-portfolio-2026-11-24-v67.json","catalog/effective-portfolio-2026-11-25-v68.json","catalog/effective-portfolio-2026-11-25-v69.json","catalog/effective-portfolio-2026-11-25-v70.json"))
        self.assertEqual(self.old["items"],self.e["items"][:221])
        self.assertEqual(self.d["previous_asset_count"],221)
        self.assertEqual(self.d["previous_active_count"],174)
        self.assertEqual([x["repo_id"] for x in self.e["items"][-3:]],
                         [x["repo_id"] for x in self.d["additions"]])
        self.assertEqual(self.e["counts"]["tracked"],224)
        self.assertEqual(self.e["counts"]["active"],177)
        self.assertEqual(self.e["counts"]["models"],198)
        self.assertEqual(self.e["counts"]["datasets"],26)
        self.assertEqual(self.e["counts"]["by_decision"]["conditional"],124)
        self.assertEqual(self.e["counts"]["by_decision"]["select"],53)
        self.assertEqual(self.e["counts"]["parameter_gate"]["UNVERIFIED_BLOCK_FINAL_LOCK"],23)
        self.assertEqual(self.e["counts"]["parameter_gate"]["PASS_TOTAL_PARAMS_LT_150B"],173)
        for k in ("tracked","active","models","datasets","by_decision","by_tier","by_forecast_wave","parameter_gate","resource_screen"):
            if self.c["revision_id"] == "v60-20261122":
                self.assertEqual(self.c["expected"][k],self.e["counts"][k])
            else:
                self.assertIn("catalog/revisions/v60-2026-11-22.json",self.c["ordered_overlays"])
        self.assertEqual(len({(x["asset_kind"],x["repo_id"]) for x in self.e["items"]}),224)

    def test_source_59_and_int8_avoidance(self):
        self.assertEqual((self.m["source_repos"],self.m["publisher_total_file_refs"],self.m["publisher_total_repo_bytes"]), (3,67,2_195_546_493))
        self.assertEqual((self.m["selected_source_file_refs"],self.m["selected_source_bytes"],self.m["selected_lfs_sha256_refs"]), (59,2_131_918_285,30))
        self.assertEqual((self.d["publisher_source_files_selected"],self.d["publisher_selected_bytes"]), (59,2_131_918_285))
        count=bytes_=sha=0
        for m in self.m["model_repos"]:
            self.assertEqual(len(m["revision_sha"]),40)
            self.assertFalse(m["observed_access"]["gated"])
            self.assertFalse(m["observed_access"]["private"])
            self.assertEqual(len(m["selected_files"]),m["selected_file_count"])
            count+=m["selected_file_count"]
            bytes_+=m["selected_source_bytes"]
            sha+=m["selected_lfs_sha256_refs"]
            self.assertEqual(sum(f["bytes"] for f in m["selected_files"]),m["selected_source_bytes"])
            for f in m["selected_files"]:
                self.assertFalse(f["local_sha256_verified"])
                self.assertEqual(len(f["git_blob_sha1"]),40)
                if f["publisher_lfs_sha256"]:
                    self.assertEqual(len(f["publisher_lfs_sha256"]),64)
        self.assertEqual((count,bytes_,sha),(59,2_131_918_285,30))
        pico=next(x for x in self.m["model_repos"] if x["repo_id"]=="KittenML/kitten-tts-2-pico")
        self.assertEqual((len(pico["selected_files"]),len(pico["excluded_alternative_files"])),(33,8))
        self.assertEqual(sum(x["bytes"] for x in pico["excluded_alternative_files"]),63_628_208)
        self.assertEqual(sum(x["path"].endswith(".safetensors") and "kitten_tts_2_pico_" in x["path"] for x in pico["selected_files"]),8)
        self.assertEqual(sum(x["path"].endswith("_int4.onnx") for x in pico["selected_files"]),8)

    def test_all_sidecars_stop(self):
        ids={(x["asset_kind"],x["repo_id"]) for x in self.e["items"] if x["portfolio_decision"] in ("select","conditional")}
        self.assertEqual(len(ids),177)
        self.assertEqual({(x["asset_kind"],x["repo_id"]) for x in self.q["candidates"]},ids)
        self.assertEqual({(x["asset_kind"],x["repo_id"]) for x in self.r["records"]},ids)
        self.assertEqual({(x["asset_kind"],x["repo_id"]) for x in self.p["items"]},ids)
        self.assertEqual(len(self.a["entries"]),124)
        self.assertEqual(self.r["summary"]["blocked_any"],177)
        self.assertEqual(self.r["summary"]["ready_to_approve"],0)
        self.assertEqual(self.r["summary"]["unknown_total_active"],10)
        self.assertEqual(self.r["summary"]["downloads_approved"],0)
        self.assertFalse(self.r["ready_to_acquire"])
        self.assertFalse(self.q["approved"])
        self.assertFalse(self.q["download_enabled"])
        self.assertFalse(self.p["download_enabled"])
        self.assertEqual(load("queues/approved.json")["entries"],[])
        for x in self.r["records"]:
            self.assertFalse(x["ready_to_acquire"])
            self.assertFalse(x["download_approved"])

    def test_three_trainings_and_96_existing_report(self):
        repo_ids=[x["repo_id"] for x in self.d["additions"]]
        self.assertEqual(repo_ids,["mistralai/Timestral-28M","internlm/Intern-Decision-0.8B","KittenML/kitten-tts-2-pico"])
        self.assertEqual(self.d["additions"][0]["parameter_gate"]["total_parameters"],27_821_184)
        self.assertEqual(self.d["additions"][1]["parameter_gate"]["total_parameters"],852_985_920)
        self.assertIsNone(self.d["additions"][2]["parameter_gate"]["total_parameters"])
        self.assertEqual(self.d["additions"][2]["parameter_gate"]["status"],"UNVERIFIED_BLOCK_FINAL_LOCK")
        self.assertTrue(all(x["research_only_nonexecutable"] and not x["download_approved"] for x in self.d["additions"]))
        self.assertEqual(len(self.decision["decisions"]),3)
        self.assertEqual(self.decision["execution"]["ledger_reported_verified_models_now"],96)
        ledger=load("catalog/execution/2026-11-19-acquisition-ledger.json")
        self.assertGreaterEqual(ledger["summary"]["models_verified"],96)
        self.assertEqual(self.decision["execution"]["approved_queue_entries_added"],0)

if __name__=="__main__":
    unittest.main()
