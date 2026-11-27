import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))
def keys(xs):
    return sorted((x["asset_kind"],x["repo_id"]) for x in xs)
class GigaEdgeResearch(unittest.TestCase):
    def test_append_only(self):
        old=load("catalog/effective-portfolio-2026-11-28-v82.json")
        new=load("catalog/effective-portfolio-2026-11-28-v83.json")
        overlay=load("catalog/revisions/v83-2026-11-28.json")
        self.assertEqual(new["items"][:-1],old["items"])
        self.assertEqual(new["items"][-1:],overlay["additions"])
        self.assertEqual(len(set(keys(new["items"]))),277)
        self.assertEqual(overlay["replacement_operations"],[])
        self.assertEqual(overlay["removed_assets"],[])
    def test_join_and_stop(self):
        new=load("catalog/effective-portfolio-2026-11-28-v83.json")
        active=[x for x in new["items"] if x["portfolio_decision"] in ("select","conditional")]
        cond=[x for x in active if x["portfolio_decision"]=="conditional"]
        self.assertEqual((len(active),len(cond)),(221,165))
        for path,field,rows in [("queues/proposed-v83-2026-11-28.json","candidates",active),("catalog/preparation/2026-11-28-insurance-bundles-v83.json","items",active),("catalog/readiness/v83-2026-11-28-r180-all221-gates.json","records",active),("catalog/access/2026-11-28-v83-conditional-hub-gates.json","entries",cond)]:
            self.assertEqual(keys(load(path)[field]),keys(rows))
        self.assertTrue(all(not x["download_approved"] and not x["ready_to_acquire"] and x["blocking_gates"] for x in load("catalog/readiness/v83-2026-11-28-r180-all221-gates.json")["records"]))
        self.assertTrue(all(not x["download_approved"] for x in load("queues/proposed-v83-2026-11-28.json")["candidates"]))
        self.assertEqual(load("catalog/CURRENT.json")["revision_id"],"v83-20261128")
    def test_manifest(self):
        m=load("manifests/drafts/r180-2026-11-28-gigaedge-two-profile-source.candidate.json")
        s=m["source_models"][0]
        fs=s["source_files"]
        chosen=[x for x in fs if x["selected_candidate"]]
        self.assertEqual((len(fs),len(chosen)),(13,7))
        self.assertEqual(sum(x["bytes"] for x in fs),39967596)
        self.assertEqual(sum(x["bytes"] for x in chosen),11058505)
        self.assertEqual(sum(x["lfs_sha256"] is not None for x in fs),5)
        self.assertFalse(m["download_enabled"])
        self.assertFalse(m["approved_by_user"])
        self.assertIsNone(s["complete_dependency_inclusive_bytes"])
        self.assertIsNone(s["exact_total_trained_parameters"])
