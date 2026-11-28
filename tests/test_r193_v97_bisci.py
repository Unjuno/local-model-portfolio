import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
class BiSCI(unittest.TestCase):
 def test_immutable_prior_and_add(self):
  old=read("catalog/effective-portfolio-2026-11-28-v96.json"); new=read("catalog/effective-portfolio-2026-11-28-v97.json"); o=read("catalog/revisions/v97-2026-11-28.json")
  self.assertEqual(new["items"][:-1],old["items"]); self.assertEqual(new["items"][-1],o["additions"][0]); self.assertEqual(len(new["items"]),291); x=new["items"][-1]; self.assertEqual(x["repo_id"],"CaiYuanhao/BiSCI"); self.assertEqual(x["parameter_gate"]["status"],"UNVERIFIED_BLOCK_FINAL_LOCK"); self.assertIsNone(x["parameter_gate"]["total_parameters"]); self.assertFalse(x["download_approved"])
 def test_manifest(self):
  m=read("manifests/drafts/r193-2026-11-28-bisci-simulation-source.candidate.json"); self.assertEqual(m["source_commit"],"d7c8aaac7c5180dd6334edc602120b43afa5817c"); self.assertEqual(sum(x["bytes"] for x in m["candidate_model_source_files"]),2854346); self.assertEqual(sum(x["bytes"] for x in m["code_source_files"]),301186); self.assertEqual(m["model_plus_code_reference_bytes"],3155532); self.assertEqual([x["path"] for x in m["candidate_model_source_files"] if x["path"].endswith(".pth")],["Simu_models/bisrnet.pth"]); self.assertIsNone(m["dependency_inclusive_bytes"]); self.assertIsNone(m["owner_incremental_bytes"]); self.assertFalse(m["download_approved"]); self.assertFalse(m["executable"])
 def test_readiness(self):
  r=read("catalog/readiness/v97-2026-11-28-r193-all235-gates.json"); q=read("queues/proposed-v97-2026-11-28.json"); a=read("catalog/access/2026-11-28-v97-conditional-hub-gates.json"); p=read("catalog/preparation/2026-11-28-insurance-bundles-v97.json"); new=read("catalog/effective-portfolio-2026-11-28-v97.json"); key=lambda x:(x["asset_kind"],x["repo_id"]); active={key(x) for x in new["items"] if x["portfolio_decision"] in ("select","conditional")}
  self.assertEqual(len(active),235); self.assertEqual(active,{key(x) for x in r["records"]}); self.assertEqual(active,{key(x) for x in q["candidates"]}); self.assertEqual(active,{key(x) for x in p["items"]}); self.assertEqual(len(a["entries"]),179); self.assertTrue(all(not x["download_approved"] for x in r["records"])); self.assertEqual(r["records"][-1]["first_blocker"],"COMPLETE_TRAINED_TOTAL_PARAMETERS"); self.assertEqual(r["summary"]["ready_to_approve"],0); self.assertEqual(r["summary"]["unknown_total_active"],32)
