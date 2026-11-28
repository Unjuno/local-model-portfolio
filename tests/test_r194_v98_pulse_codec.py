import json, unittest
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
def load(p): return json.loads((R/p).read_text())
def key(x): return x["asset_kind"],x["repo_id"]
class PulseCodecFormal(unittest.TestCase):
 def test_overlay(self):
  old=load("catalog/effective-portfolio-2026-11-28-v97.json")["items"]; new=load("catalog/effective-portfolio-2026-11-28-v98.json")["items"]
  self.assertEqual(new[:-1],old); self.assertEqual(len(new),292); self.assertEqual(len(set(map(key,new))),292); self.assertEqual(new[-1],load("catalog/revisions/v98-2026-11-28.json")["additions"][0]); self.assertIsNone(new[-1]["parameter_gate"]["total_parameters"])
 def test_manifest(self):
  m=load("manifests/drafts/r194-2026-11-28-pulse-codec-original.candidate.json"); s=m["source_models"][0]; files=s["source_files"]
  self.assertEqual(sum(x["bytes"] for x in files),373706354); self.assertEqual(sum(x["bytes"] for x in files if x["path"] in s["candidate_selected_files"]),88499234); self.assertEqual(sum(x["bytes"] for x in m["runtime_source"]["source_files"]),2165939); self.assertEqual(m["combined_selected_model_plus_code_reference_bytes"],90665173); self.assertTrue(all(x["publisher_lfs_sha256"]==x["publisher_SHA256SUMS"] for x in files if x["publisher_lfs_sha256"])); self.assertFalse(m["download_enabled"])
 def test_joins(self):
  new=load("catalog/effective-portfolio-2026-11-28-v98.json"); active={key(x) for x in new["items"] if x["portfolio_decision"] in ("select","conditional")}; cond={key(x) for x in new["items"] if x["portfolio_decision"]=="conditional"}
  for p,k in [("queues/proposed-v98-2026-11-28.json","candidates"),("catalog/preparation/2026-11-28-insurance-bundles-v98.json","items"),("catalog/readiness/v98-2026-11-28-r194-all236-gates.json","records"),("catalog/access/2026-11-28-v98-conditional-hub-gates.json","entries")]:
   rows=load(p)[k]; expect=cond if k=="entries" else active; self.assertEqual(set(map(key,rows)),expect); self.assertEqual(len(rows),len(expect))
  rd=load("catalog/readiness/v98-2026-11-28-r194-all236-gates.json"); self.assertTrue(all(not x["download_approved"] and not x["ready_to_acquire"] for x in rd["records"])); self.assertEqual(rd["summary"]["blocking_gate_counts"],dict(Counter(g for x in rd["records"] for g in x["blocking_gates"])))
  self.assertEqual(load("queues/approved.json")["entries"],[])
