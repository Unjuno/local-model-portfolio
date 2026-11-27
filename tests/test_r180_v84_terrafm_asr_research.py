import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding="utf-8"))
def key(x):return x["asset_kind"],x["repo_id"]
class TerraFMResearch(unittest.TestCase):
 def test_append_only_and_counts(self):
  a=load("catalog/effective-portfolio-2026-11-28-v83.json")["items"]; b=load("catalog/effective-portfolio-2026-11-28-v84.json")["items"]; o=load("catalog/revisions/v84-2026-11-28.json")
  self.assertEqual(b[:-1],a); self.assertEqual(len(b),278); self.assertEqual(len({key(x) for x in b}),278)
  self.assertEqual(b[-1],o["additions"][0]); self.assertEqual(b[-1]["repo_id"],"MBZUAI/TerraFM")
  self.assertIsNone(b[-1]["parameter_gate"]["total_parameters"]); self.assertFalse(b[-1]["download_ready"])
 def test_typed_joins_stop(self):
  b=load("catalog/effective-portfolio-2026-11-28-v84.json")["items"]; ac={key(x) for x in b if x["portfolio_decision"] in ("select","conditional")}; co={key(x) for x in b if x["portfolio_decision"]=="conditional"}
  self.assertEqual((len(ac),len(co)),(222,166))
  for new,old,k in [["queues/proposed-v84-2026-11-28.json","queues/proposed-v83-2026-11-28.json","candidates"],["catalog/preparation/2026-11-28-insurance-bundles-v84.json","catalog/preparation/2026-11-28-insurance-bundles-v83.json","items"],["catalog/readiness/v84-2026-11-28-r180-all222-gates.json","catalog/readiness/v83-2026-11-28-r180-all221-gates.json","records"],["catalog/access/2026-11-28-v84-conditional-hub-gates.json","catalog/access/2026-11-28-v83-conditional-hub-gates.json","entries"]]:
   z=load(new)[k]; self.assertEqual(z[:-1],load(old)[k]); self.assertEqual({key(x) for x in z},co if k=="entries" else ac); self.assertEqual(len(z),166 if k=="entries" else 222)
  g=load("catalog/readiness/v84-2026-11-28-r180-all222-gates.json"); self.assertTrue(all(not x["download_approved"] and not x["ready_to_acquire"] for x in g["records"])); self.assertEqual(g["summary"]["blocked_any"],222)
  self.assertEqual(load("queues/approved.json")["entries"],[])
 def test_manifest_and_revision_drift(self):
  m=load("manifests/drafts/r180-2026-11-28-terrafm-and-fluid-asr-source.candidate.json"); t,f=m["source_models"]; z=t["source_files"]
  self.assertEqual((len(z),sum(x["bytes"] for x in z)),(8,453538500)); self.assertEqual(sum(x["bytes"] for x in z if x["selected_candidate"]),451895030); self.assertEqual(sum(x["selected_candidate"] for x in z),4)
  self.assertEqual(next(x["lfs_sha256"] for x in z if x["path"]=="TerraFM-B.pth"),t["older_same_weight_lfs_sha256"]); self.assertFalse(t["older_license_file_present"])
  self.assertEqual((len(f["source_files"]),sum(x["bytes"] for x in f["source_files"])),(17,5139989533)); self.assertFalse(any(x["selected_candidate"] for x in f["source_files"]))
  g=m["existing_granite_revision_drift"]; self.assertEqual(g["weight_lfs_sha256_old"],g["weight_lfs_sha256_new"]); self.assertEqual(g["new_full_repo_bytes"]-g["old_full_repo_bytes"],2894)
  self.assertFalse(m["download_enabled"]); self.assertFalse(m["approved_by_user"]); self.assertIsNone(t["complete_dependency_inclusive_bytes"]); self.assertIsNone(t["owner_incremental_bytes"])
 def test_current_chain_and_decisions(self):
  c=load("catalog/CURRENT.json"); s=load("catalog/snapshots/2026-11-28-v83-current-before-v84.json"); self.assertIn("catalog/revisions/v84-2026-11-28.json",c["ordered_overlays"]); self.assertEqual(s["revision_id"],"v83-20261128")
  self.assertEqual(c["revision_id"],load(c["materialized_catalog_path"])["revision_id"])
  d=load("catalog/decisions/2026-11-28-r180-terrafm-asr-source-adjudication.json"); self.assertEqual([x["decision"] for x in d["decisions"][:3]],["ADD","HOLD","KEEP"]); self.assertEqual(d["owner_approval_added"],0)
  ledger=load("catalog/execution/2026-11-19-acquisition-ledger.json"); self.assertGreaterEqual(sum(x["status"]=="VERIFIED" for x in ledger["models"]),133)
