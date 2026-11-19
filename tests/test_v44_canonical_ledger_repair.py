"""V44 repaired canonical source worklists follow one exact 149/96 ID set, not stale v43 metadata."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(path): return json.loads((ROOT/path).read_text(encoding="utf-8"))
def k(x):return x["asset_kind"],x["repo_id"].lower()
class TestV44CanonicalLedgerRepair(unittest.TestCase):
 def test_v44_current_and_149_96_id_joins(self):
  c={"revision_id":"v44-20261115"};v=read("catalog/effective-portfolio-2026-11-15-v44.json")
  q=read("queues/proposed-v44-2026-11-18.json");p=read("catalog/preparation/2026-11-18-insurance-bundles-v44.json")
  a=read("catalog/access/2026-11-18-v44-conditional-hub-gates.json")
  r=read("catalog/readiness/v44-2026-11-15-r101-all149-gates.json")
  self.assertEqual(c["revision_id"],"v44-20261115")
  self.assertEqual((len(v["items"]),len({k(x) for x in v["items"]})),(196,196))
  active={k(x) for x in v["items"] if x["portfolio_decision"] in ("select","conditional")}
  cond={k(x) for x in v["items"] if x["portfolio_decision"]=="conditional"}
  self.assertEqual((len(active),len(cond)),(149,96))
  self.assertEqual(active,{k(x) for x in q["candidates"]})
  self.assertEqual(active,{k(x) for x in p["items"]})
  self.assertEqual(active,{k(x) for x in r["records"]})
  self.assertEqual(cond,{k(x) for x in a["entries"]})
  self.assertEqual(sum(x["hub_gated"] is True for x in a["entries"]),20)
  self.assertEqual(q["source_revision"],c["revision_id"])
  self.assertEqual(p["source_revision"],c["revision_id"])
  self.assertEqual(a["source_revision"],c["revision_id"])
  self.assertEqual(r["summary"]["ready_to_approve"],0)
  self.assertTrue(all(x["download_approved"] is False for x in v["items"]))
  self.assertTrue(all(x["not_authorized"] and x["download_approved"] is False for x in q["candidates"]))
  self.assertEqual(read("queues/approved.json")["entries"],[])
 def test_external_sov_not_autoselected(self):
  v=read("catalog/effective-portfolio-2026-11-15-v44.json")
  s=read("catalog/research/2026-11-18-r102-sov-transcribe-original-and-dflash.json")
  self.assertNotIn("salesforce-sovereign-intelligence/SOV-Transcribe-1",{x["repo_id"] for x in v["items"]})
  self.assertEqual(s["formal_selection"],"HOLD_RESEARCH_NOT_ADDED_TO_CANONICAL")
  self.assertEqual(s["subject"]["publisher_weight_shards_count"],16)
  self.assertEqual(s["subject"]["metadata_selected_file_count"],34)
  self.assertEqual(s["subject"]["metadata_selected_source_bytes"],53315653534)
  self.assertEqual(s["subject"]["model_configuration"]["weight_index_reported_tensors"],1147)
  self.assertEqual(s["optional_acceleration"]["full_repo_files"],6)
  self.assertFalse(s["download_enabled"])
if __name__=="__main__":unittest.main()
