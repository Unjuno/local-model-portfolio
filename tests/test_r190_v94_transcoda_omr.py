import json, unittest
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
def load(p): return json.loads((R/p).read_text())
def key(x): return x["asset_kind"], x["repo_id"]
class TranscodaFormal(unittest.TestCase):
 def test_overlay(self):
  old=load("catalog/effective-portfolio-2026-11-28-v93.json")["items"]; new=load("catalog/effective-portfolio-2026-11-28-v94.json")["items"]
  self.assertEqual(new[:-1],old); self.assertEqual(len(set(map(key,new))),288); self.assertEqual(new[-1],load("catalog/revisions/v94-2026-11-28.json")["additions"][0]); self.assertTrue(new[-1]["research_only_nonexecutable"]); self.assertIsNone(new[-1]["selected_file_bytes"])
 def test_scope(self):
  m=load("manifests/drafts/r190-2026-11-28-transcoda-omr-publisher-scope.candidate.json"); self.assertEqual(sum(x["bytes"] for x in m["runtime_source"]["source_files"]),9456925); self.assertEqual(m["source_models"][0]["source_files"][0]["bytes"]+9456925,m["combined_known_weight_plus_code_reference_bytes"]); self.assertFalse(m["download_enabled"]); self.assertIsNone(m["complete_dependency_inclusive_bytes"])
 def test_join(self):
  new=load("catalog/effective-portfolio-2026-11-28-v94.json"); active={key(x) for x in new["items"] if x["portfolio_decision"] in ("select","conditional")}; conditional={key(x) for x in new["items"] if x["portfolio_decision"]=="conditional"}
  self.assertEqual(len(active),232); self.assertEqual(len(conditional),176)
  for path,k in [("queues/proposed-v94-2026-11-28.json","candidates"),("catalog/preparation/2026-11-28-insurance-bundles-v94.json","items"),("catalog/readiness/v94-2026-11-28-r190-all232-gates.json","records"),("catalog/access/2026-11-28-v94-conditional-hub-gates.json","entries")]:
   rows=load(path)[k]; expected=conditional if k=="entries" else active; self.assertEqual(set(map(key,rows)),expected); self.assertEqual(len(rows),len(expected))
  rd=load("catalog/readiness/v94-2026-11-28-r190-all232-gates.json"); self.assertTrue(all(not x["download_approved"] and not x["ready_to_acquire"] for x in rd["records"])); self.assertEqual(rd["summary"]["blocking_gate_counts"],dict(Counter(g for x in rd["records"] for g in x["blocking_gates"])))
  self.assertEqual(load("queues/approved.json")["entries"],[]); self.assertGreaterEqual(load("catalog/execution/2026-11-19-acquisition-ledger.json")["summary"]["models_verified"],133)
  c=load("catalog/CURRENT.json")
  if c["revision_id"]=="v94-20261128": self.assertEqual(c["materialized_catalog_path"],"catalog/effective-portfolio-2026-11-28-v94.json"); self.assertEqual(c["expected"]["tracked"],288); self.assertEqual(c["expected"]["active"],232)
