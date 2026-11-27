import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
class R174Test(unittest.TestCase):
    def test_preserve_and_add(self):
        old=load("catalog/effective-portfolio-2026-11-28-v76.json")["items"]; new=load("catalog/effective-portfolio-2026-11-28-v77.json")["items"]
        self.assertEqual(old,new[:267]); self.assertEqual(len(new),269)
        self.assertEqual({x["repo_id"] for x in new[267:]},{"tencent/WePocketModel1.0-4B","nvidia/Nemotron-3.5-Parse"})
        self.assertTrue(all(x["research_only_nonexecutable"] and not x["download_approved"] and x["selected_file_bytes"] is None for x in new[267:]))
    def test_join(self):
        m=load("catalog/effective-portfolio-2026-11-28-v77.json")["items"]; active={(x["asset_kind"],x["repo_id"]) for x in m if x["portfolio_decision"] in ("select","conditional")}; cond={(x["asset_kind"],x["repo_id"]) for x in m if x["portfolio_decision"]=="conditional"}
        self.assertEqual(len(active),213); self.assertEqual(len(cond),157)
        for p,k in [("catalog/readiness/v77-2026-11-28-r174-all213-gates.json","records"),("catalog/preparation/2026-11-28-insurance-bundles-v77.json","items"),("queues/proposed-v77-2026-11-28.json","candidates")]:
            rows=load(p)[k]; self.assertEqual(len(rows),213); self.assertEqual({(x["asset_kind"],x["repo_id"]) for x in rows},active); self.assertTrue(all(x["download_approved"] is False for x in rows))
        self.assertEqual({(x["asset_kind"],x["repo_id"]) for x in load("catalog/access/2026-11-28-v77-conditional-hub-gates.json")["entries"]},cond)
        self.assertTrue(all(not x["ready_to_acquire"] for x in load("catalog/readiness/v77-2026-11-28-r174-all213-gates.json")["records"]))
        self.assertEqual(load("queues/approved.json")["entries"],[])
    def test_pinned_sources(self):
        m=load("manifests/drafts/r174-2026-11-28-wepm-and-nemotron-immutable-source.candidate.json"); self.assertEqual(sum(x["all_files_bytes"] for x in m["source_repositories"]),16380934947)
        self.assertEqual(sum(x["all_files_count"] for x in m["source_repositories"]),263)
        for s in m["source_repositories"]:
            self.assertRegex(s["revision"],r"^[0-9a-f]{40}$"); f=s["file_refs"]; self.assertEqual(len({x["path"] for x in f}),s["all_files_count"]); self.assertEqual(sum(x["bytes"] for x in f),s["all_files_bytes"])
            self.assertEqual(sum(bool(x["lfs_sha256"]) for x in f),s["lfs_sha256_count"])
            for x in f:
                self.assertRegex(x["git_blob_oid"],r"^[0-9a-f]{40}$")
                if x["lfs_sha256"]: self.assertRegex(x["lfs_sha256"],r"^[0-9a-f]{64}$")
        self.assertFalse(m["download_approved"]); self.assertFalse(m["executable"]); self.assertIsNone(m["physical_archive_delta_bytes"])
    def test_budget(self):
        c=load("catalog/snapshots/2026-11-28-v76-current-before-v77.json"); self.assertEqual(c["revision_id"],"v76-20261128")
        b=load("catalog/effective-portfolio-2026-11-28-v77.json")["budget"]; self.assertEqual(b["r174_source_repo_proxy_delta_bytes"],11888223977); self.assertEqual(b["r174_active_source_repo_proxy_bytes"],3934993704769); self.assertIsNone(b["final_selected_total_bytes"])
if __name__=="__main__": unittest.main()
