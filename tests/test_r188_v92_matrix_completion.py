"""R188 metadata-only regression; never fetches or loads model payloads."""
import json
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))
def keys(rows):
    return {(x["asset_kind"], x["repo_id"]) for x in rows}
class MatrixCompletionV92(unittest.TestCase):
    def setUp(self):
        self.old = read("catalog/effective-portfolio-2026-11-28-v91.json")
        self.new = read("catalog/effective-portfolio-2026-11-28-v92.json")
        self.cur = read("catalog/CURRENT.json")
        self.m = read("manifests/drafts/r188-2026-11-28-matrixformer-source.candidate.json")
    def test_additive(self):
        self.assertEqual(self.new["items"][:-1], self.old["items"])
        self.assertEqual(len(keys(self.new["items"])), 286)
        self.assertEqual(self.new["items"][-1]["repo_id"], "Tabimpute/MatrixFormer")
        self.assertEqual(self.new["items"][-1]["portfolio_decision"], "conditional")
        self.assertFalse(self.new["items"][-1]["download_approved"])
        self.assertEqual(read("catalog/revisions/v92-2026-11-28.json")["additions"], self.new["items"][-1:])
    def test_coverage(self):
        active = [x for x in self.new["items"] if x["portfolio_decision"] in ("select", "conditional")]
        conditional = [x for x in active if x["portfolio_decision"] == "conditional"]
        self.assertEqual((len(active), len(conditional)), (230, 174))
        for p,k in [("queues/proposed-v92-2026-11-28.json","candidates"),("catalog/preparation/2026-11-28-insurance-bundles-v92.json","items"),("catalog/readiness/v92-2026-11-28-r188-all230-gates.json","records")]:
            rows=read(p)[k]
            self.assertEqual(len(rows),230)
            self.assertEqual(keys(rows),keys(active))
            self.assertTrue(all(x["download_approved"] is False for x in rows))
        self.assertEqual(keys(read("catalog/access/2026-11-28-v92-conditional-hub-gates.json")["entries"]),keys(conditional))
        self.assertTrue(all(not x["ready_to_acquire"] for x in read("catalog/readiness/v92-2026-11-28-r188-all230-gates.json")["records"]))
    def test_manifest_scope(self):
        self.assertEqual(sum(x["bytes"] for x in self.m["files"]), 624134936)
        self.assertEqual(sum(x["bytes"] for x in self.m["files"] if x["selected_for_research"]),312108648)
        self.assertEqual(sum(x["bytes"] for x in self.m["code_scope"]["files"]),218310)
        self.assertEqual(self.m["model_plus_code_reference_bytes"],312326958)
        self.assertFalse(next(x for x in self.m["files"] if x["path"]=="model.safetensors")["selected_for_research"])
        self.assertTrue(self.m["runtime_pinned_revision_parity"]["git_oid_equal"])
        self.assertIsNone(self.m["dependency_inclusive_bytes"])
        self.assertIsNone(self.m["owner_incremental_bytes"])
        self.assertFalse(self.m["download_enabled"])
    def test_canonical_and_ledger(self):
        if self.cur["revision_id"] == "v92-20261128":
            self.assertEqual(self.cur["materialized_catalog_path"],"catalog/effective-portfolio-2026-11-28-v92.json")
            self.assertEqual(self.cur["ordered_overlays"][-1],"catalog/revisions/v92-2026-11-28.json")
            self.assertEqual(self.cur["expected"]["active"],230)
        else:
            self.assertIn("catalog/revisions/v92-2026-11-28.json",self.cur["ordered_overlays"])
        self.assertEqual(read("queues/approved.json")["entries"],[])
        self.assertGreaterEqual(read("catalog/execution/2026-11-19-acquisition-ledger.json")["summary"]["models_verified"],133)
    def test_prior_sidecars_unchanged(self):
        for old,new,key in [
            ("queues/proposed-v91-2026-11-28.json","queues/proposed-v92-2026-11-28.json","candidates"),
            ("catalog/preparation/2026-11-28-insurance-bundles-v91.json","catalog/preparation/2026-11-28-insurance-bundles-v92.json","items"),
            ("catalog/readiness/v91-2026-11-28-r187-all229-gates.json","catalog/readiness/v92-2026-11-28-r188-all230-gates.json","records"),
            ("catalog/access/2026-11-28-v91-conditional-hub-gates.json","catalog/access/2026-11-28-v92-conditional-hub-gates.json","entries")]:
            self.assertEqual(read(old)[key],read(new)[key][:-1])
if __name__ == "__main__":
    unittest.main()
