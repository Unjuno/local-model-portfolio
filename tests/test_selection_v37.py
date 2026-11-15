"""Verify v37 exact publisher primary source identity and non-executable gates."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def get(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def uid(x):return x["asset_kind"],x["repo_id"]
class V37(unittest.TestCase):
 def test_exact_two_evidence_corrections_and_same_assets(self):
  old=get("catalog/effective-portfolio-2026-11-15-v36.json")
  new=get("catalog/effective-portfolio-2026-11-15-v37.json")
  c=get("catalog/CURRENT.json");o=get("catalog/revisions/v37-2026-11-15.json")
  self.assertEqual(len(new["items"]),191)
  self.assertEqual(len({uid(x) for x in new["items"]}),191)
  self.assertEqual({uid(x):x["portfolio_decision"] for x in old["items"]},
                   {uid(x):x["portfolio_decision"] for x in new["items"]})
  self.assertEqual(new["counts"],old["counts"])
  self.assertEqual(c["revision_id"],"v37-20261115")
  self.assertEqual(len(o["metadata_corrections"]),2)
  self.assertEqual(o["selection_added"],0)
  self.assertTrue(all(not x["download_approved"] for x in new["items"]))
 def test_primary_hashes_and_overfetch_are_exact(self):
  s=get("catalog/research/2026-11-15-r85-v37-kumo-tabular-source-and-policy-facts.json")
  chosen=s["source_file_manifest"]["selected_source_files"];excluded=s["source_file_manifest"]["excluded_alternative_size_files"]
  self.assertEqual(len(chosen),6);self.assertEqual(len(excluded),4)
  self.assertEqual(sum(x["bytes"] for x in chosen),1717765270)
  self.assertEqual(sum(x["bytes"] for x in excluded),720168092)
  self.assertEqual(len([x for x in chosen if x.get("lfs_sha256")]),2)
  self.assertTrue(all(not x["payload_fetched"] and not x["local_sha_verified"] for x in chosen+excluded))
  v=get("catalog/effective-portfolio-2026-11-15-v37.json")
  m=next(x for x in v["items"] if x["repo_id"]=="nvidia/Kumo-Tabular")
  self.assertEqual(m["upstream_revision_sha_observed"],s["revision"])
  self.assertIsNone(m["selected_file_bytes"])
  self.assertIsNone(m["fully_pinned_revision_sha"])
  self.assertFalse(m["download_approved"])
 def test_queue_and_access_match_and_owner_gate_remains_closed(self):
  v=get("catalog/effective-portfolio-2026-11-15-v37.json")
  q=get("queues/proposed-v37-2026-11-15.json")
  p=get("catalog/preparation/2026-11-15-insurance-bundles-v37.json")
  a=get("catalog/access/2026-11-15-v37-conditional-hub-gates.json")
  r=get("catalog/readiness/v37-2026-11-15-r85-all144-gates.json")
  active={uid(x) for x in v["items"] if x["portfolio_decision"] in ("select","conditional")}
  cond={uid(x) for x in v["items"] if x["portfolio_decision"]=="conditional"}
  self.assertEqual(len(active),144);self.assertEqual(len(cond),91)
  self.assertEqual(active,{uid(x) for x in q["candidates"]})
  self.assertEqual(active,{uid(x) for x in p["items"]})
  self.assertEqual(active,{uid(x) for x in r["records"]})
  self.assertEqual(cond,{uid(x) for x in a["entries"]})
  self.assertEqual(a["gated_count"],19)
  self.assertEqual(a["unverified_hub_gate_count"],0)
  pplx=next(x for x in a["entries"] if x["repo_id"]=="perplexity-ai/pplx-decider-flash-v1.3")
  self.assertIs(pplx["hub_gated"],False)
  self.assertIs(pplx["hub_api_private"],False)
  self.assertEqual(pplx["owner_access_permission"],"unknown")
  self.assertTrue(all(not x["download_authorized"] for x in a["entries"]))
  self.assertFalse(q["download_enabled"]);self.assertFalse(p["download_enabled"])
  self.assertEqual(get("queues/approved.json")["entries"],[])
if __name__=="__main__":unittest.main()
