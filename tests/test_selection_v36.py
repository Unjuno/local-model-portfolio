"""V36: retain old 189 and verify two distinct Gated original scientific checkpoints."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def j(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def k(x):return x["asset_kind"],x["repo_id"]

class V36(unittest.TestCase):
 def test_append_only_and_no_quantization_duplication(self):
  v35=j("catalog/effective-portfolio-2026-11-15-v35.json")
  v36=j("catalog/effective-portfolio-2026-11-15-v36.json")
  overlay=j("catalog/revisions/v36-2026-11-15.json")
  current={"revision_id":"v36-20261115"}
  self.assertEqual(len(v35["items"]),189)
  self.assertEqual(v36["items"][:189],v35["items"])
  self.assertEqual(v36["items"][189:],overlay["additions"])
  self.assertEqual(len(v36["items"]),191)
  self.assertEqual(len({k(x) for x in v36["items"]}),191)
  self.assertEqual(v36["counts"]["active"],144)
  self.assertEqual(current["revision_id"],"v36-20261115")
  self.assertEqual({x["repo_id"] for x in overlay["additions"]},{
   "nvidia/Ising-Decoder-ColorCode-1-Fast","nvidia/Ising-Decoder-SurfaceCode-1-Fast"})
  for x in overlay["additions"]:
   self.assertEqual(x["portfolio_decision"],"conditional")
   self.assertIsNone(x["selected_file_bytes"])
   self.assertIsNone(x["fully_pinned_revision_sha"])
   self.assertFalse(x["download_approved"])
 def test_gated_permissions_queue_and_dependencies(self):
  v=j("catalog/effective-portfolio-2026-11-15-v36.json")
  q=j("queues/proposed-v36-2026-11-15.json")
  p=j("catalog/preparation/2026-11-15-insurance-bundles-v36.json")
  a=j("catalog/access/2026-11-15-v36-conditional-hub-gates.json")
  ready=j("catalog/readiness/v36-2026-11-15-r83-all144-gates.json")
  active={k(x) for x in v["items"] if x["portfolio_decision"] in ("select","conditional")}
  conditional={k(x) for x in v["items"] if x["portfolio_decision"]=="conditional"}
  self.assertEqual(len(active),144)
  self.assertEqual(active,{k(x) for x in q["candidates"]})
  self.assertEqual(active,{k(x) for x in p["items"]})
  self.assertEqual(conditional,{k(x) for x in a["entries"]})
  self.assertEqual(len(a["entries"]),91)
  self.assertEqual(sum(x["hub_gated"] for x in a["entries"]),19)
  self.assertEqual(len(ready["records"]),144)
  self.assertEqual(ready["summary"]["ready_to_approve"],0)
  self.assertEqual(j("queues/approved.json")["entries"],[])
 def test_source_geometry_and_stop_gates(self):
  a={x["repo_id"]:x for x in j("catalog/revisions/v36-2026-11-15.json")["additions"]}
  self.assertEqual(a["nvidia/Ising-Decoder-ColorCode-1-Fast"]["upstream_model_file"]["bytes_exact"],5899248)
  self.assertEqual(a["nvidia/Ising-Decoder-SurfaceCode-1-Fast"]["upstream_model_file"]["bytes_exact"],1826360)
  self.assertEqual(a["nvidia/Ising-Decoder-ColorCode-1-Fast"]["parameter_gate"]["total_parameters"],2936580)
  self.assertEqual(a["nvidia/Ising-Decoder-SurfaceCode-1-Fast"]["parameter_gate"]["total_parameters"],912772)
  self.assertTrue(all(x["observed_access"].startswith("Gated") and not x["personal_access_verified"] for x in a.values()))
  self.assertEqual(j("catalog/revisions/v36-2026-11-15.json")["selected_publisher_source_candidate_bytes"],7760518)

if __name__=="__main__": unittest.main()
