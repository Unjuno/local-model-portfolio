"""R162/v69: pure-stdlib static status and Publisher LFS core checks."""
import unittest,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text(encoding="utf8"))
def key(x):return x["asset_kind"],x["repo_id"]
class R162(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=read("catalog/CURRENT.json");cls.e=read("catalog/effective-portfolio-2026-11-25-v69.json");cls.old=read("catalog/effective-portfolio-2026-11-25-v68.json")
  cls.tts=read("manifests/drafts/r162-2026-11-25-paradee13-tihon100k-core-weight-pins.candidate.json");cls.ink=read("manifests/drafts/r162-2026-11-25-electroglyph-inkling-heretic-v22-adapter-core.candidate.json");cls.ledger=read("catalog/execution/2026-11-19-acquisition-ledger.json")
  cls.queue=read("queues/proposed-v69-2026-11-25.json");cls.access=read("catalog/access/2026-11-25-v69-conditional-hub-gates.json")
  cls.ready=read("catalog/readiness/v69-2026-11-25-r162-all206-gates.json");cls.prep=read("catalog/preparation/2026-11-25-insurance-bundles-v69.json")
 def test_same_252_and_counts(self):
  self.assertIn(self.c["revision_id"],("v69-20261125","v70-20261125", "v71-20261125", "v72-20261125", "v73-20261125"))
  self.assertEqual(self.e["items"][:252],self.old["items"])
  self.assertEqual(len(self.e["items"]),255)
  self.assertEqual(len({key(x) for x in self.e["items"]}),255)
  self.assertEqual((self.e["counts"]["active"],self.e["counts"]["models"],self.e["counts"]["datasets"]),(206,229,26))
  self.assertEqual((self.e["counts"]["by_decision"]["select"],self.e["counts"]["by_decision"]["conditional"],self.e["counts"]["by_decision"]["hold"]),(56,150,30))
 def test_pinned_weight_files_exact(self):
  x=self.tts["model_sources"];self.assertEqual(len(x),2)
  self.assertEqual(sum(len(s["weights"]) for s in x)+len(self.ink["core_weight_files"]),5)
  self.assertEqual(sum(sum(f["bytes"] for f in s["weights"]) for s in x)+sum(f["bytes"] for f in self.ink["core_weight_files"]),92138387)
  for src in x:
   self.assertEqual(len(src["revision"]),40)
   self.assertFalse(src["full_repo_file_census_frozen"])
   for f in src["weights"]:self.assertEqual(len(f["sha256"]),64)
  self.assertEqual(self.ink["publisher_repo_file_count"],10)
  self.assertEqual(self.ink["core_weight_files"][0]["bytes"],51617184)
  self.assertFalse(self.ink["source_file_scope_complete"])
 def test_derived_sets_and_blocked_authorization(self):
  active={key(x) for x in self.e["items"] if x["portfolio_decision"] in ("select","conditional")}
  conditional={key(x) for x in self.e["items"] if x["portfolio_decision"]=="conditional"}
  for rows in (self.queue["candidates"],self.ready["records"],self.prep["items"]):
   self.assertEqual({key(x) for x in rows},active)
  self.assertEqual({key(x) for x in self.access["entries"]},conditional)
  self.assertEqual(self.access["gated_count"],21)
  self.assertEqual(self.ready["summary"]["blocked_any"],206)
  self.assertEqual(self.ready["summary"]["ready_to_approve"],0)
  self.assertEqual(read("queues/approved.json")["entries"],[])
  self.assertFalse(self.queue["approved"] or self.queue["download_enabled"])
  self.assertTrue(all(not x["download_approved"] for x in self.e["items"]))
  self.assertEqual(sum(x["status"]=="VERIFIED" for x in self.ledger["models"]),116)
  self.assertTrue(all(z["repo_id"] in {x["repo_id"] for x in self.e["items"]} for z in self.ledger["models"] if z["status"]=="VERIFIED"))
  self.assertEqual(read("catalog/readiness/CURRENT.json")["catalog_revision"],self.c["revision_id"])
  self.assertEqual(read("catalog/estimates/CURRENT.json")["portfolio_revision"],self.c["revision_id"])
if __name__=="__main__":unittest.main()
