import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def key(rows): return {(x["asset_kind"],x["repo_id"]) for x in rows}
class HorizonResearch(unittest.TestCase):
 def test_catalog_and_joins(self):
  old=load("catalog/effective-portfolio-2026-11-28-v90.json")["items"]; new=load("catalog/effective-portfolio-2026-11-28-v91.json")["items"]
  self.assertEqual(new[:-1],old); self.assertEqual(len(key(new)),285); self.assertEqual(new[-1]["repo_id"],"Horizon-Labs/multilingual-reranker-small")
  active=[x for x in new if x["portfolio_decision"] in ("select","conditional")]; conditional=[x for x in active if x["portfolio_decision"]=="conditional"]
  self.assertEqual(len(active),229); self.assertEqual(len(conditional),173)
  for p,k in [("queues/proposed-v91-2026-11-28.json","candidates"),("catalog/readiness/v91-2026-11-28-r187-all229-gates.json","records"),("catalog/preparation/2026-11-28-insurance-bundles-v91.json","items")]: self.assertEqual(key(load(p)[k]),key(active))
  self.assertEqual(key(load("catalog/access/2026-11-28-v91-conditional-hub-gates.json")["entries"]),key(conditional))
  self.assertFalse(any(x["ready_to_acquire"] or x["download_approved"] for x in load("catalog/readiness/v91-2026-11-28-r187-all229-gates.json")["records"]))
 def test_manifest(self):
  m=load("manifests/drafts/2026-11-28-horizon-reranker-source.candidate.json"); self.assertEqual(len(m["files"]),31); self.assertEqual(sum(x["bytes"] for x in m["files"]),1428709912); self.assertEqual(sum(x["bytes"] for x in m["files"] if x["selected"]),597202061); self.assertEqual(sum(x["selected"] for x in m["files"]),28); self.assertFalse(m["download_approved"]); self.assertIsNone(m["actual_owner_incremental_bytes"]); self.assertIn("catalog/revisions/v91-2026-11-28.json",load("catalog/CURRENT.json")["ordered_overlays"])
