import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def load(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))
class TestSymbolicRegressionV96(unittest.TestCase):
    def test_append_only_and_joins(self):
        rows = load("catalog/effective-portfolio-2026-11-28-v96.json")["items"]
        self.assertEqual(rows[:-1], load("catalog/effective-portfolio-2026-11-28-v95.json")["items"])
        self.assertEqual(rows[-1], load("catalog/revisions/v96-2026-11-28.json")["additions"][0])
        self.assertEqual(len({x["repo_id"] for x in rows}), 290)
        active = {x["repo_id"] for x in rows if x["portfolio_decision"] in ("select", "conditional")}
        conditional = {x["repo_id"] for x in rows if x["portfolio_decision"] == "conditional"}
        self.assertEqual(len(active), 234)
        self.assertEqual(len(conditional), 178)
        for path, key in [("queues/proposed-v96-2026-11-28.json", "candidates"), ("catalog/readiness/v96-2026-11-28-r192-all234-gates.json", "records"), ("catalog/preparation/2026-11-28-insurance-bundles-v96.json", "items")]:
            self.assertEqual({x["repo_id"] for x in load(path)[key]}, active)
        self.assertEqual({x["repo_id"] for x in load("catalog/access/2026-11-28-v96-conditional-hub-gates.json")["entries"]}, conditional)
        self.assertFalse(any(x.get("ready_to_acquire") or x.get("download_approved") for x in load("catalog/readiness/v96-2026-11-28-r192-all234-gates.json")["records"]))
    def test_candidate_partial_not_approved(self):
        m = load("manifests/drafts/r192-2026-11-28-rasr-symbolic-regression-source.candidate.json")
        self.assertEqual(m["source_models"][0]["source_files"][0]["sha256"], "ada6f12950507c70e86ee0c1b94783de6c6852e10c76214bb0c0f52a5e78acfa")
        self.assertEqual(m["known_core_weight_bytes"], 188351066)
        self.assertEqual(sum(x["bytes"] for x in m["runtime_source"]["root_blobs"]), 1754342)
        self.assertEqual(m["combined_known_core_weight_plus_root_code_reference_bytes"], 190105408)
        self.assertIsNone(m["complete_dependency_inclusive_bytes"])
        self.assertIsNone(m["actual_owner_incremental_bytes"])
        self.assertFalse(m["download_approved"])
        if load("catalog/CURRENT.json")["revision_id"] == "v96-20261128":
            self.assertEqual(load("catalog/CURRENT.json")["materialized_catalog_path"], "catalog/effective-portfolio-2026-11-28-v96.json")
