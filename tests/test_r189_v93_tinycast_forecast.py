import json, unittest
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text())
def key(x):return x["asset_kind"],x["repo_id"]
class TinyCastFormal(unittest.TestCase):
 def test_overlay(self):
  old=load("catalog/effective-portfolio-2026-11-28-v92.json")["items"];new=load("catalog/effective-portfolio-2026-11-28-v93.json")["items"]
  self.assertEqual(new[:-1],old);self.assertEqual(len(new),287);self.assertEqual(len(set(map(key,new))),287)
  self.assertEqual(new[-1],load("catalog/revisions/v93-2026-11-28.json")["additions"][0]);self.assertTrue(new[-1]["research_only_nonexecutable"]);self.assertIsNone(new[-1]["selected_file_bytes"])
 def test_scope(self):
  m=load("manifests/drafts/r189-2026-11-28-tinycast-forecast-originals.candidate.json");s=m["source_models"][0]
  self.assertEqual(s["safetensors_total"],146505);self.assertEqual(sum(x["bytes"] for x in s["source_files"]),720964);self.assertEqual(sum(x["bytes"] for x in s["source_files"] if x["path"] in s["candidate_selected_files"]),613278)
  self.assertEqual(sum(x["bytes"] for x in m["runtime_source"]["source_files"]),2795416);self.assertEqual(m["combined_selected_model_plus_code_reference_bytes"],3408694);self.assertFalse(m["download_enabled"]);self.assertIsNone(m["complete_dependency_inclusive_bytes"])
 def test_join(self):
  new=load("catalog/effective-portfolio-2026-11-28-v93.json");active={key(x) for x in new["items"] if x["portfolio_decision"] in ("select","conditional")};conditional={key(x) for x in new["items"] if x["portfolio_decision"]=="conditional"}
  self.assertEqual(len(active),231);self.assertEqual(len(conditional),175);self.assertEqual(new["counts"]["active"],231)
  for path,k in [("queues/proposed-v93-2026-11-28.json","candidates"),("catalog/preparation/2026-11-28-insurance-bundles-v93.json","items"),("catalog/readiness/v93-2026-11-28-r189-all231-gates.json","records"),("catalog/access/2026-11-28-v93-conditional-hub-gates.json","entries")]:
   rows=load(path)[k];expect=conditional if k=="entries" else active
   self.assertEqual(set(map(key,rows)),expect);self.assertEqual(len(rows),len(expect))
  rd=load("catalog/readiness/v93-2026-11-28-r189-all231-gates.json");self.assertTrue(all(not x["download_approved"] and not x["ready_to_acquire"] for x in rd["records"]));self.assertEqual(rd["summary"]["blocking_gate_counts"],dict(Counter(g for x in rd["records"] for g in x["blocking_gates"])))
  self.assertEqual(load("queues/approved.json")["entries"],[]);self.assertEqual(load("catalog/execution/2026-11-19-acquisition-ledger.json")["summary"]["models_verified"],133)
  c=load("catalog/CURRENT.json")
  if c["revision_id"]=="v93-20261128":
   self.assertEqual(c["materialized_catalog_path"],"catalog/effective-portfolio-2026-11-28-v93.json");self.assertEqual(c["expected"]["tracked"],287);self.assertEqual(c["expected"]["active"],231)
