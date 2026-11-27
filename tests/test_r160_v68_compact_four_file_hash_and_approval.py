"""R160/v68 immutable publisher source and selection regression, stdlib only; no models loaded."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rd(path):return json.loads((ROOT/path).read_text(encoding="utf8"))
def key(x):return (x["asset_kind"],x["repo_id"])
from scripts.ledger_history_r168 import historical_117_ledger

class V68(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=rd("catalog/CURRENT.json");cls.v=rd("catalog/effective-portfolio-2026-11-25-v68.json")
  cls.o=rd("catalog/effective-portfolio-2026-11-24-v67.json")
  cls.m=rd("manifests/drafts/r160-2026-11-25-four-small-trained-states-75file-publisher-frozen.candidate.json");cls.ledger=historical_117_ledger(rd("catalog/execution/2026-11-19-acquisition-ledger.json"))
  cls.queue=rd("queues/proposed-v68-2026-11-25.json");cls.a=rd("catalog/access/2026-11-25-v68-conditional-hub-gates.json")
  cls.g=rd("catalog/readiness/v68-2026-11-25-r160-all203-gates.json");cls.p=rd("catalog/preparation/2026-11-25-insurance-bundles-v68.json")
 def test_canonical_and_old_items_unchanged(self):
  self.assertIn(self.c["revision_id"],("v68-20261125","v69-20261125","v70-20261125", "v71-20261125", "v72-20261125", "v73-20261125"))
  self.assertEqual(self.v["items"][:248],self.o["items"])
  self.assertEqual(len(self.v["items"]),252)
  self.assertEqual(len({key(x) for x in self.v["items"]}),252)
  self.assertEqual((self.v["counts"]["active"],self.v["counts"]["models"],self.v["counts"]["datasets"]),(203,226,26))
  self.assertEqual((self.v["counts"]["by_decision"]["select"],self.v["counts"]["by_decision"]["conditional"],self.v["counts"]["by_decision"]["hold"]),(56,147,30))
 def test_116_receipts_and_75_publisher_files(self):
  self.assertEqual(sum(x["status"]=="VERIFIED" for x in self.ledger["models"]),116)
  self.assertTrue(all(x["repo_id"] in {v["repo_id"] for v in self.v["items"]} for x in self.ledger["models"] if x["status"]=="VERIFIED"))
  files=self.m["model_sources"]
  self.assertEqual(len(files),4)
  self.assertEqual(sum(len(x["files"]) for x in files),75)
  self.assertEqual(sum(sum(z["bytes"] for z in x["files"]) for x in files),17608061719)
  self.assertEqual(self.m["publisher_source_aggregates"]["exact_duplicate_excess_file_bytes"],20076087)
  self.assertTrue(all(len(x["immutable_revision_sha"])==40 for x in files))
  self.assertTrue(all(not x["download_approved"] for x in files))
  self.assertTrue(all(not z["owner_local_sha256_verified"] for x in files for z in x["files"]))
 def test_joined_stop_gates(self):
  active={key(x) for x in self.v["items"] if x["portfolio_decision"] in ("select","conditional")}
  conditional={key(x) for x in self.v["items"] if x["portfolio_decision"]=="conditional"}
  for collection in (self.queue["candidates"],self.g["records"],self.p["items"]):
   self.assertEqual({key(x) for x in collection},active)
  self.assertEqual({key(x) for x in self.a["entries"]},conditional)
  self.assertEqual(self.a["gated_count"],21)
  self.assertEqual(self.g["summary"]["blocked_any"],203)
  self.assertEqual(self.g["summary"]["ready_to_approve"],0)
  self.assertEqual(rd("queues/approved.json")["entries"],[])
  self.assertFalse(self.queue["approved"] or self.queue["download_enabled"])
  self.assertTrue(all(not x["download_approved"] for x in self.v["items"]))
  self.assertEqual(rd("catalog/readiness/CURRENT.json")["catalog_revision"],self.c["revision_id"])
  self.assertEqual(rd("catalog/estimates/CURRENT.json")["portfolio_revision"],self.c["revision_id"])
if __name__=="__main__":unittest.main()
