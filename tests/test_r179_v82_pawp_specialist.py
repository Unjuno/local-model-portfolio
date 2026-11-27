"""R179: metadata-only regression for PAWP and v81 concurrent preservation."""
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))
def key(x):
    return (x["asset_kind"], x["repo_id"])
class PawpRegression(unittest.TestCase):
    def test_selection_and_joins(self):
        old = load("catalog/effective-portfolio-2026-11-28-v81.json")
        new = load("catalog/effective-portfolio-2026-11-28-v82.json")
        self.assertEqual(new["items"][:-1], old["items"])
        self.assertEqual(len(new["items"]), 276)
        self.assertEqual(len({key(x) for x in new["items"]}), 276)
        active = {key(x) for x in new["items"] if x["portfolio_decision"] in ("select","conditional")}
        conditional = {key(x) for x in new["items"] if x["portfolio_decision"] == "conditional"}
        self.assertEqual(len(active), 220)
        self.assertEqual(len(conditional), 164)
        for path, field, expected in [("queues/proposed-v82-2026-11-28.json","candidates",active),("catalog/preparation/2026-11-28-insurance-bundles-v82.json","items",active),("catalog/access/2026-11-28-v82-conditional-hub-gates.json","entries",conditional),("catalog/readiness/v82-2026-11-28-r179-all220-gates.json","records",active)]:
            rows = load(path)[field]
            self.assertEqual(len(rows),len(expected))
            self.assertEqual({key(x) for x in rows}, expected)
        self.assertTrue(all(not x["ready_to_acquire"] and not x["download_approved"] for x in load("catalog/readiness/v82-2026-11-28-r179-all220-gates.json")["records"]))
        self.assertEqual(new["items"][-1], load("catalog/revisions/v82-2026-11-28.json")["additions"][0])
        self.assertIsNone(new["items"][-1]["selected_file_bytes"])
        self.assertFalse(new["items"][-1]["download_approved"])
    def test_source_scope(self):
        m = load("manifests/drafts/r179-2026-11-28-pawp-300k-two-states-source.candidate.json")
        self.assertEqual(len(m["source_files"]),23)
        self.assertEqual(sum(x["bytes"] for x in m["source_files"]),7130007)
        selected = [x for x in m["source_files"] if x["selected"]]
        self.assertEqual(len(selected),8)
        self.assertEqual(sum(x["bytes"] for x in selected),2306237)
        self.assertEqual({x["path"] for x in selected if x["path"].endswith(".safetensors")},{"model.safetensors","variants/dense_300k_v3.safetensors"})
        self.assertFalse(m["download_approved"])
        self.assertFalse(m["executable"])
        self.assertIsNone(m["complete_dependency_inclusive_bytes"])
if __name__ == "__main__":
    unittest.main()
