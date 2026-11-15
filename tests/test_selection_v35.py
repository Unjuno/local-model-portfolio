"""V35 original Muse Glimmer + independent DFlash adoption and hard stops (stdlib)."""
import json, unittest, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def key(x):return x["asset_kind"],x["repo_id"]
class V35(unittest.TestCase):
 def test_append_only_and_publisher_evidence(self):
  o=read("catalog/effective-portfolio-2026-11-15-v34.json")
  n=read("catalog/effective-portfolio-2026-11-15-v35.json")
  d=read("catalog/revisions/v35-2026-11-15.json")
  self.assertEqual(n["items"][:len(o["items"])],o["items"])
  self.assertEqual(len(o["items"]),187)
  self.assertEqual(n["items"][187:],d["additions"])
  self.assertEqual(n["counts"]["tracked"],189)
  self.assertEqual(n["counts"]["models"],163)
  self.assertEqual(n["counts"]["datasets"],26)
  self.assertEqual(n["counts"]["active"],142)
  self.assertEqual(n["counts"]["by_decision"],{"select":53,"conditional":89,"hold":28,"deferred":13,"excluded":6})
  self.assertEqual(len({key(x) for x in n["items"]}),189)
  self.assertEqual([x["repo_id"] for x in d["additions"]],["meta-models/Muse-Glimmer-30B","meta-models/Muse-Glimmer-30B-assistant"])
  self.assertEqual(n["items"][187]["upstream_source_weights"]["source_stored_parameter_count"],29776626688)
  self.assertEqual(n["items"][187]["upstream_source_weights"]["source_index_tensor_payload_bytes"],59553253376)
  self.assertEqual(n["items"][188]["upstream_source_weights"]["publisher_pointer_sha256"],"fd88d337eb84f8d0e6ba33a7684d7efa6722d4460ba4d6badca9699418392a84")
  for x in d["additions"]:
   self.assertEqual(x["portfolio_decision"],"conditional")
   self.assertFalse(x["download_approved"])
   self.assertIsNone(x["selected_file_bytes"])
   self.assertIsNone(x["fully_pinned_revision_sha"])
   self.assertFalse(x["license_text_reviewed"])
   self.assertFalse(x["dependencies_reviewed"])
 def test_all_candidate_id_integrity_and_no_approval(self):
  n=read("catalog/effective-portfolio-2026-11-15-v35.json")
  q=read("queues/proposed-v35-2026-11-15.json")
  p=read("catalog/preparation/2026-11-15-insurance-bundles-v35.json")
  a=read("catalog/access/2026-11-15-v35-conditional-hub-gates.json")
  r=read("catalog/readiness/v35-2026-11-15-r82-all142-gates.json")
  active=[x for x in n["items"] if x["portfolio_decision"] in ("select","conditional")]
  cond=[x for x in active if x["portfolio_decision"]=="conditional"]
  self.assertEqual(len(active),142)
  self.assertEqual({key(x) for x in active},{key(x) for x in q["candidates"]})
  self.assertEqual({key(x) for x in active},{key(x) for x in p["items"]})
  self.assertEqual({key(x) for x in active},{key(x) for x in r["records"]})
  self.assertEqual({key(x) for x in cond},{key(x) for x in a["entries"]})
  self.assertEqual(sum(x["hub_gated"] for x in a["entries"]),17)
  self.assertEqual(len(r["records"]),142)
  self.assertEqual(r["summary"]["unknown_total_active"],9)
  self.assertEqual(r["summary"]["no_final_revision"],140)
  self.assertEqual(r["summary"]["ready_to_approve"],0)
  self.assertTrue(all(not x["download_approved"] for x in n["items"]))
  self.assertFalse(q["approved"]);self.assertFalse(q["download_enabled"])
  self.assertFalse(p["download_enabled"]);self.assertFalse(a["download_authorized"])
  self.assertEqual(read("queues/approved.json")["entries"],[])
 def test_active_pointer_only_after_complete_set(self):
  c={"revision_id":"v35-20261115","expected":{"tracked":189,"active":142},"priority_worklist_path":"queues/proposed-v35-2026-11-15.json","insurance_preparation_worklist_path":"catalog/preparation/2026-11-15-insurance-bundles-v35.json"}
  n=read("catalog/effective-portfolio-2026-11-15-v35.json")
  self.assertEqual(c["revision_id"],"v35-20261115")
  self.assertEqual(n["revision_id"],c["revision_id"])
  self.assertEqual(c["expected"]["tracked"],len(n["items"]))
  self.assertEqual(c["expected"]["active"],142)
  self.assertEqual(c["priority_worklist_path"],"queues/proposed-v35-2026-11-15.json")
  self.assertEqual(c["insurance_preparation_worklist_path"],"catalog/preparation/2026-11-15-insurance-bundles-v35.json")
if __name__=="__main__":unittest.main()
