"""v34 exact identities and no authorization; read-only unittest."""
import json, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def get(p): return json.loads((R/p).read_text())
def key(x): return (x["asset_kind"],x["repo_id"].lower())
class TestV34(unittest.TestCase):
 def test_append_and_views(self):
  v33=get("catalog/effective-portfolio-2026-11-15-v33.json")
  v=get("catalog/effective-portfolio-2026-11-15-v34.json")
  c=get("catalog/CURRENT.json")
  q=get("queues/proposed-v34-2026-11-15.json")
  p=get("catalog/preparation/2026-11-15-insurance-bundles-v34.json")
  a=get("catalog/access/2026-11-15-v34-conditional-hub-gates.json")
  self.assertEqual(v["items"][:185],v33["items"])
  self.assertEqual((len(v["items"]),len(set(map(key,v["items"])))),(187,187))
  self.assertEqual((c["revision_id"],v["revision_id"]),("v34-20261115","v34-20261115"))
  active={key(x) for x in v["items"] if x["portfolio_decision"] in ("select","conditional")}
  conditional={key(x) for x in v["items"] if x["portfolio_decision"]=="conditional"}
  self.assertEqual((len(active),len(conditional)),(140,87))
  self.assertEqual({key(x) for x in q["candidates"]},active)
  self.assertEqual({key(x) for x in p["items"]},active)
  self.assertEqual({key(x) for x in a["entries"]},conditional)
  self.assertTrue(all(not x["download_approved"] for x in v["items"]))
  self.assertTrue(all(x.get("not_authorized") and not x["download_approved"] for x in q["candidates"]))
  self.assertEqual(get("queues/approved.json")["entries"],[])
 def test_new_two_without_formats(self):
  o=get("catalog/revisions/v34-2026-11-15.json")
  rows={x["repo_id"]:x for x in o["additions"]}
  self.assertEqual(set(rows),{"nvidia/Kumo-Tabular","nvidia/Kumo-Anomaly"})
  self.assertEqual(rows["nvidia/Kumo-Tabular"]["upstream_model_file"]["paths"],["large/classifier.pt","large/regressor.pt"])
  self.assertTrue(rows["nvidia/Kumo-Anomaly"]["preservation_bundle"]["runtime_execution_hold"])
  self.assertEqual(rows["nvidia/Kumo-Anomaly"]["parameter_gate"]["status"],"UNVERIFIED_BLOCK_FINAL_LOCK")
  self.assertEqual(o["planning_cap_bytes"],3000000000)
if __name__=="__main__":unittest.main()
