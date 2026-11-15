"""v42 audit of observed gated LTX parent, public child access, and noncompensatory source rights."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(x):return json.loads((ROOT/x).read_text(encoding="utf-8"))
IDS={"Lightricks/LTX-2.5","ChrisColeTech/LTX-2.5-uncensored-v1.1-FP8","Stuubs/Stubelius_Remix_Ltx2.5"}
GATE="LTX_TRAINED_SHARED_COMPONENTS_AND_DERIVATIVE_LICENCE_UNRESOLVED"
class V42(unittest.TestCase):
 def test_same_asset_ids_and_decisions(self):
  a=read("catalog/effective-portfolio-2026-11-15-v41.json")["items"]
  b=read("catalog/effective-portfolio-2026-11-15-v42.json")["items"]
  self.assertEqual(len(a),195);self.assertEqual(len(b),195)
  self.assertEqual([(x["asset_kind"],x["repo_id"],x["portfolio_decision"]) for x in a],[(x["asset_kind"],x["repo_id"],x["portfolio_decision"]) for x in b])
  self.assertEqual({x["repo_id"] for x,y in zip(a,b) if x!=y},IDS)
 def test_blocked_source_and_owner_rights(self):
  a=read("catalog/access/2026-11-15-v42-conditional-hub-gates.json")
  r=read("catalog/readiness/v42-2026-11-15-r94-all148-gates.json")
  self.assertEqual(r["summary"]["blocking_gate_counts"][GATE],3)
  self.assertEqual(r["summary"]["unknown_total_active"],9)
  self.assertEqual(a["gated_count"],20)
  for repo in IDS:
   x=next(x for x in r["records"] if x["repo_id"]==repo)
   y=next(x for x in a["entries"] if x["repo_id"]==repo)
   self.assertIn(GATE,x["blocking_gates"])
   self.assertTrue(y["underlying_parent_hub_gated"])
   self.assertFalse(y["download_authorized"])
  self.assertTrue(next(x for x in a["entries"] if x["repo_id"]=="Lightricks/LTX-2.5")["hub_gated"])
  for repo in IDS-{"Lightricks/LTX-2.5"}:
   self.assertFalse(next(x for x in a["entries"] if x["repo_id"]==repo)["hub_gated"])
 def test_status_and_sidecars(self):
  c=read("catalog/CURRENT.json")
  self.assertEqual(read("catalog/effective-portfolio-2026-11-15-v42.json")["revision_id"],"v42-20261115")
  self.assertEqual(read("catalog/readiness/CURRENT.json")["catalog_revision"],c["revision_id"])
  self.assertEqual(read("catalog/estimates/CURRENT.json")["portfolio_revision"],c["revision_id"])
  self.assertEqual(read("queues/approved.json")["entries"],[])
  self.assertEqual(read(c["latest_active_readiness_audit"]["summary_path"])["summary"]["ready_to_approve"],0)
if __name__=="__main__":unittest.main()
