# Pure metadata regression; no network, no model weights.
import json,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
class R131(unittest.TestCase):
 def test_files_equal(self):
  x=load("manifests/drafts/r130-2026-11-20-frostwolf-and-phala-originals-fixed.candidate.json")["models"];y=load("manifests/drafts/r130-2026-11-20-frostwolf-and-phala-uncensored-originals.candidate.json")["original_outcomes"]
  self.assertEqual(len(x),len(y))
  n=0
  for a in x:
   b=next(v for v in y if v["repo_id"]==a["repo_id"])
   self.assertEqual(a["revision"],b["publisher_revision_sha"])
   self.assertEqual(a["bytes"],b["publisher_source_bytes"])
   canon={i["path"]:i for i in a["selected_source_files"]}
   other={i["path"]:i for i in b["all_files"]}
   self.assertEqual(canon.keys(),other.keys())
   for p,z in canon.items():
    t=other[p]
    self.assertEqual(z["bytes"],t["bytes"])
    self.assertEqual(z.get("sha256"),t.get("publisher_lfs_sha256"))
    self.assertEqual(z.get("git_blob_sha1"),t.get("publisher_git_blob_sha1"))
    n+=1
  self.assertEqual(n,20)
 def test_v56_snapshot_immutable_and_live_current_consistent(self):
  # The R131 v56 files stay immutable when CURRENT advances to v57+.
  old=load("catalog/effective-portfolio-2026-11-20-v56.json")
  self.assertEqual(old["revision_id"],"v56-20261120")
  self.assertEqual(len(old["items"]),211)
  self.assertEqual(len({(x["asset_kind"],x["repo_id"]) for x in old["items"]}),211)
  self.assertEqual(sum(x["portfolio_decision"] in ("select","conditional") for x in old["items"]),164)
  self.assertEqual(len(load("queues/proposed-v56-2026-11-20.json")["candidates"]),164)
  self.assertEqual(len(load("catalog/readiness/v56-2026-11-20-r130-all164-gates.json")["records"]),164)
  self.assertEqual(len(load("catalog/access/2026-11-20-v56-conditional-hub-gates.json")["entries"]),111)
  self.assertEqual(len(load("catalog/preparation/2026-11-20-insurance-bundles-v56.json")["items"]),164)
  c=load("catalog/CURRENT.json")
  eff=load(c["materialized_catalog_path"])
  self.assertEqual(eff["revision_id"],c["revision_id"])
  self.assertEqual(len(eff["items"]),c["expected"]["tracked"])
  self.assertEqual(len({(x["asset_kind"],x["repo_id"]) for x in eff["items"]}),c["expected"]["tracked"])
  self.assertEqual(sum(x["portfolio_decision"] in ("select","conditional") for x in eff["items"]),c["expected"]["active"])
  self.assertEqual(len(load(c["priority_worklist_path"])["candidates"]),c["expected"]["active"])
  self.assertEqual(len(load(c["insurance_preparation_worklist_path"])["items"]),c["expected"]["active"])
  self.assertEqual(len(load(c["latest_conditional_access_audit"]["path"])["entries"]),c["expected"]["by_decision"]["conditional"])
  self.assertEqual(len(load(c["latest_active_readiness_audit"]["summary_path"])["records"]),c["expected"]["active"])
  self.assertEqual(c["latest_v56_uncensored_model_additions"]["overlay"],"catalog/revisions/v56-2026-11-20.json")
  self.assertTrue({(x["asset_kind"],x["repo_id"]) for x in old["items"]}.issubset(
      {(x["asset_kind"],x["repo_id"]) for x in eff["items"]}))
  self.assertEqual(load("queues/approved.json")["entries"],[])
if __name__=="__main__":unittest.main()
