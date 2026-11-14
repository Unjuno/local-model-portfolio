"""V34 historical Kumo trained-state selection, frozen separately from later CURRENT."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def key(x):return x["asset_kind"],x["repo_id"]
class V34(unittest.TestCase):
 def test_exact_two_kumo_learned_outcomes(self):
  old=read("catalog/effective-portfolio-2026-11-15-v33.json")
  v=read("catalog/effective-portfolio-2026-11-15-v34.json")
  ov=read("catalog/revisions/v34-2026-11-15.json")
  self.assertEqual(len(old["items"]),185)
  self.assertEqual(v["items"][:185],old["items"])
  self.assertEqual(len(v["items"]),187)
  self.assertEqual(v["items"][185:],ov["additions"])
  self.assertEqual({key(x) for x in v["items"]}.__len__(),187)
  self.assertEqual(v["counts"]["active"],140)
  self.assertEqual({x["repo_id"] for x in ov["additions"]},{"nvidia/Kumo-Tabular","nvidia/Kumo-Anomaly"})
  self.assertTrue(all(x["portfolio_decision"]=="conditional" and x["selected_file_bytes"] is None and x["fully_pinned_revision_sha"] is None and not x["download_approved"] for x in ov["additions"]))
 def test_historical_queue_consistent_and_nonexecutable(self):
  v=read("catalog/effective-portfolio-2026-11-15-v34.json")
  q=read("queues/proposed-v34-2026-11-15.json")
  p=read("catalog/preparation/2026-11-15-insurance-bundles-v34.json")
  a=read("catalog/access/2026-11-15-v34-conditional-hub-gates.json")
  active={key(x) for x in v["items"] if x["portfolio_decision"] in ("select","conditional")}
  cond={key(x) for x in v["items"] if x["portfolio_decision"]=="conditional"}
  self.assertEqual(len(active),140)
  self.assertEqual(active,{key(x) for x in q["candidates"]})
  self.assertEqual(active,{key(x) for x in p["items"]})
  self.assertEqual(cond,{key(x) for x in a["entries"]})
  self.assertEqual(len(a["entries"]),87)
  self.assertEqual(sum(x["hub_gated"] for x in a["entries"]),17)
  self.assertFalse(q["approved"]);self.assertFalse(q["download_enabled"])
  self.assertEqual(read("queues/approved.json")["entries"],[])
 def test_unknown_parameter_blocks_kumo_anomaly(self):
  v=read("catalog/effective-portfolio-2026-11-15-v34.json")
  m={x["repo_id"]:x for x in v["items"]}
  self.assertEqual(m["nvidia/Kumo-Anomaly"]["parameter_gate"]["status"],"UNVERIFIED_BLOCK_FINAL_LOCK")
  self.assertTrue(not m["nvidia/Kumo-Anomaly"]["download_approved"])
  self.assertNotIn("nvidia/Nemotron-3.5-Parse",m)
if __name__=="__main__":unittest.main()
