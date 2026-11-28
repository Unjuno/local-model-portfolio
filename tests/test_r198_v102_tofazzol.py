import json, unittest
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(p): return json.loads((R/p).read_text(encoding="utf-8"))
def key(x): return x["asset_kind"],x["repo_id"]
class TofazzolFormal(unittest.TestCase):
 def test_formal_addition(self):
  old=load("catalog/effective-portfolio-2026-11-28-v101.json")["items"]
  new=load("catalog/effective-portfolio-2026-11-28-v102.json")["items"]
  self.assertEqual(new[:-1],old)
  self.assertEqual(len(new),297)
  self.assertEqual(len(set(map(key,new))),297)
  self.assertEqual(new[-1],load("catalog/revisions/v102-2026-11-28.json")["additions"][0])
  self.assertEqual(new[-1]["repo_id"],"porkr/Tofazzol-v2.1-1.5B")
  self.assertEqual(new[-1]["parameter_gate"]["total_parameters"],1543714304)
  self.assertFalse(new[-1]["download_approved"])
  self.assertIsNone(new[-1]["selected_file_bytes"])
 def test_source_scope(self):
  m=load("manifests/drafts/r198-2026-11-28-tofazzol-source.candidate.json"); s=m["source_models"][0]
  self.assertEqual(len(s["source_files"]),56)
  self.assertEqual(len(s["candidate_selected_files"]),34)
  self.assertEqual(sum(f["bytes"] for f in s["source_files"]),3100135228)
  self.assertEqual(sum(f["bytes"] for f in s["source_files"] if f["path"] in s["candidate_selected_files"]),3099316333)
  self.assertTrue(s["tree_pagination_complete"])
  for f in s["source_files"]:
   if f["publisher_lfs_sha256"] and f["publisher_SHA256SUMS"]: self.assertEqual(f["publisher_lfs_sha256"],f["publisher_SHA256SUMS"])
  self.assertFalse(m["download_enabled"])
  self.assertIsNone(m["complete_dependency_inclusive_bytes"])
 def test_join_and_stop(self):
  d=load("catalog/effective-portfolio-2026-11-28-v102.json")
  active={key(x) for x in d["items"] if x["portfolio_decision"] in ("select","conditional")}
  conditional={key(x) for x in d["items"] if x["portfolio_decision"]=="conditional"}
  self.assertEqual(len(active),241)
  self.assertEqual(d['items'][-1]['parameter_gate']['status'],'PASS_TOTAL_PARAMS_LT_150B')
  self.assertEqual(len(conditional),185)
  for path,k in [("queues/proposed-v102-2026-11-28.json","candidates"),("catalog/preparation/2026-11-28-insurance-bundles-v102.json","items"),("catalog/readiness/v102-2026-11-28-r198-all241-gates.json","records"),("catalog/access/2026-11-28-v102-conditional-hub-gates.json","entries")]:
   rows=load(path)[k]; expected=conditional if k=="entries" else active
   self.assertEqual(len(rows),len(expected)); self.assertEqual(set(map(key,rows)),expected)
  rd=load("catalog/readiness/v102-2026-11-28-r198-all241-gates.json")
  self.assertTrue(all(not x["ready_to_acquire"] and not x["download_approved"] for x in rd["records"]))
  self.assertEqual(rd["summary"]["blocking_gate_counts"],dict(Counter(g for x in rd["records"] for g in x["blocking_gates"])))
  self.assertEqual(load("queues/approved.json")["entries"],[])
  self.assertEqual(load("catalog/execution/2026-11-19-acquisition-ledger.json")["summary"]["models_verified"],133)
  c=load("catalog/CURRENT.json")
  if c["revision_id"]=="v102-20261128":
   self.assertEqual(c["materialized_catalog_path"],"catalog/effective-portfolio-2026-11-28-v102.json")
   self.assertEqual(c["expected"]["active"],241)
