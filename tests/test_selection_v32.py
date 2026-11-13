"""Verify v32 compact trained-state selection, retention, and nonexecution."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def key(row):
    return row["asset_kind"], row["repo_id"].lower()

class V32(unittest.TestCase):
    def setUp(self):
        self.old=load("catalog/effective-portfolio-2026-11-13-v31.json")
        self.view=load("catalog/effective-portfolio-2026-11-14-v32.json")
        self.current=load("catalog/CURRENT.json")
        self.overlay=load("catalog/revisions/v32-2026-11-14.json")

    def test_exact_three_unique_outcomes_and_history(self):
        self.assertEqual(self.view["items"][:179],self.old["items"])
        self.assertEqual(len(self.view["items"]),182)
        self.assertEqual(len({key(v) for v in self.view["items"]}),182)
        self.assertEqual({v["repo_id"] for v in self.view["items"][-3:]},{
            "tencent/Qwen3.8-27B-DSpine-b16",
            "nvidia/Nemotron-3-Diarization",
            "nvidia/RFD4-Proteina"})
        self.assertEqual(self.current["revision_id"],"v32-20261114")
        self.assertEqual((self.current["expected"]["tracked"],
                          self.current["expected"]["active"],
                          self.current["expected"]["models"],
                          self.current["expected"]["datasets"]),(182,135,156,26))
        self.assertEqual(self.current["expected"]["by_decision"],{
            "select":53,"conditional":82,"hold":28,"deferred":13,"excluded":6})
        self.assertEqual(self.current["expected"]["parameter_gate"],{
            "PASS_TOTAL_PARAMS_LT_150B":134,
            "UNVERIFIED_BLOCK_FINAL_LOCK":20,
            "OVER_150B_QUANT_REVIEW_REQUIRED":2})

    def test_nonexecutable_queue_and_dependencies(self):
        q=load("queues/proposed-v32-2026-11-14.json")
        plan=load("catalog/preparation/2026-11-14-insurance-bundles-v32.json")
        active={key(v) for v in self.view["items"]
                if v["portfolio_decision"] in ("select","conditional")}
        self.assertEqual(len(active),135)
        self.assertEqual(len(q["candidates"]),135)
        self.assertEqual(len(plan["items"]),135)
        self.assertEqual({key(v) for v in q["candidates"]},active)
        self.assertEqual({key(v) for v in plan["items"]},active)
        self.assertFalse(q["approved"])
        self.assertFalse(q["download_enabled"])
        self.assertFalse(plan["download_enabled"])
        self.assertEqual(load("queues/approved.json")["entries"],[])
        self.assertTrue(all(v["not_authorized"] and v["download_approved"] is False
                            for v in q["candidates"]))

    def test_three_model_hashes_and_distinct_file_selection(self):
        rows={v["repo_id"]:v for v in self.overlay["additions"]}
        self.assertEqual(len(rows),3)
        self.assertEqual(rows["nvidia/RFD4-Proteina"]["upstream_model_file"]["bytes_exact"],1742660596)
        self.assertEqual(rows["nvidia/RFD4-Proteina"]["parameter_gate"]["total_parameters"],435622465)
        self.assertEqual(rows["nvidia/Nemotron-3-Diarization"]["parameter_gate"]["total_parameters"],99200000)
        self.assertEqual(rows["tencent/Qwen3.8-27B-DSpine-b16"]["parameter_gate"]["total_parameters"],2025900000)
        self.assertEqual(sum(v["selection_budget_cap_bytes"] for v in rows.values()),9700000000)
        for v in rows.values():
            self.assertRegex(v["upstream_model_file"]["sha256"],r"^[a-f0-9]{64}$")
            self.assertIsNone(v["selected_file_bytes"])
            self.assertIsNone(v["fully_pinned_revision_sha"])
            self.assertFalse(v["download_approved"])
            self.assertFalse(v["preservation_bundle"]["fixed_manifest_complete"])
        self.assertFalse(self.overlay["download_authorizations_created"])
        self.assertFalse(any(v["asset_kind"]=="dataset" for v in rows.values()))

    def test_gated_metadata_coverage_no_permission(self):
        a=load("catalog/access/2026-11-14-v32-conditional-hub-gates.json")
        cond={key(v) for v in self.view["items"] if v["portfolio_decision"]=="conditional"}
        self.assertEqual(a["source_revision"],"v32-20261114")
        self.assertEqual(len(a["entries"]),82)
        self.assertEqual({key(v) for v in a["entries"]},cond)
        self.assertEqual(a["gated_count"],17)
        self.assertEqual(sum(v["hub_gated"] for v in a["entries"]),17)
        self.assertTrue(a["fail_closed_if_missing"])
        self.assertTrue(all(v["owner_access_permission"]=="unknown"
                            and v["download_authorized"] is False for v in a["entries"]))

if __name__=="__main__":
    unittest.main()
