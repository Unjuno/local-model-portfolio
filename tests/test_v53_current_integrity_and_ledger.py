"""Current v53 canonical integrity and 61-ledger delta audit; no network or weights."""
from __future__ import annotations
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def read(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))


class CurrentV53Integrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = read("catalog/CURRENT.json")
        cls.prev = read("catalog/effective-portfolio-2026-11-19-v52.json")
        cls.eff = read("catalog/effective-portfolio-2026-11-20-v53.json")
        cls.q = read("queues/proposed-v53-2026-11-20.json")
        cls.access = read("catalog/access/2026-11-20-v53-conditional-hub-gates.json")
        cls.prep = read("catalog/preparation/2026-11-20-insurance-bundles-v53.json")
        cls.ready = read("catalog/readiness/v53-2026-11-20-r125-all159-gates.json")
        cls.delta = read("queues/proposed-v52-r125-ledger61-delta-next15.json")
        cls.new = read("queues/proposed-v53-r126-aion-bf16-first-public-source.json")
        cls.oldlog = read("catalog/execution/2026-11-19-acquisition-ledger.json")

    def test_current_points_to_existing_materialized_v53(self):
        self.assertEqual(self.c["revision_id"], "v53-20261120")
        self.assertEqual(self.c["materialized_catalog_path"],
                         "catalog/effective-portfolio-2026-11-20-v53.json")
        self.assertEqual(self.c["ordered_overlays"][-1], "catalog/revisions/v53-2026-11-20.json")
        self.assertEqual(self.c["priority_worklist_path"], "queues/proposed-v53-2026-11-20.json")
        self.assertEqual(self.c["latest_conditional_access_audit"]["path"],
                         "catalog/access/2026-11-20-v53-conditional-hub-gates.json")

    def test_prior_205_immutable_and_new_asset_unique(self):
        self.assertEqual(len(self.prev["items"]), 205)
        self.assertEqual(self.prev["items"], self.eff["items"][:205])
        self.assertEqual(len(self.eff["items"]), 206)
        refs = [(x["asset_kind"], x["repo_id"]) for x in self.eff["items"]]
        self.assertEqual(len(refs), len(set(refs)))
        self.assertEqual(self.eff["items"][-1]["repo_id"], "microsoft/Aion-1.0-Instruct-2.3B")

    def test_counts_from_assets_not_just_published_headers(self):
        items = self.eff["items"]
        actual = {
            "tracked": len(items),
            "active": sum(x["portfolio_decision"] in ("select", "conditional") for x in items),
            "models": sum(x["asset_kind"] == "model" for x in items),
            "datasets": sum(x["asset_kind"] == "dataset" for x in items),
        }
        for k, val in actual.items():
            self.assertEqual(val, self.c["expected"][k])
            self.assertEqual(val, self.eff["counts"][k])
        self.assertEqual(actual, {"tracked": 206, "active": 159,
                                  "models": 180, "datasets": 26})

    def test_active_worklist_exact_id_coverage(self):
        active = {(x["asset_kind"], x["repo_id"]) for x in self.eff["items"]
                  if x["portfolio_decision"] in ("select", "conditional")}
        work = {(x["asset_kind"], x["repo_id"]) for x in self.q["candidates"]}
        self.assertEqual(len(work), 159)
        self.assertEqual(active, work)
        self.assertFalse(self.q["download_enabled"])
        self.assertFalse(self.q["approved"])

    def test_conditional_access_and_owner_auth(self):
        conditional = {x["repo_id"] for x in self.eff["items"]
                       if x["portfolio_decision"] == "conditional"}
        self.assertEqual(conditional, {x["repo_id"] for x in self.access["entries"]})
        self.assertEqual(len(conditional), 106)
        self.assertEqual(self.access["gated_count"], 21)
        self.assertEqual(sum(bool(x["hub_gated"]) for x in self.access["entries"]), 21)
        self.assertEqual(self.access["owner_authorizations_verified"], 0)

    def test_readiness_and_preparation_all_still_blocked(self):
        self.assertEqual(len(self.ready["records"]), 159)
        self.assertEqual(len(self.prep["items"]), 159)
        self.assertEqual(self.ready["summary"]["blocked_any"], 159)
        self.assertFalse(any(x["ready_to_acquire"] for x in self.ready["records"]))
        self.assertFalse(any(x["download_approved"] for x in self.prep["items"]))
        self.assertEqual(read("queues/approved.json")["entries"], [])

    def test_delta_and_new_source_byte_reconciliation(self):
        self.assertEqual(len(self.delta["entries"]), 15)
        self.assertEqual(self.delta["go_scope_bytes"], 327549073014)
        self.assertEqual(self.delta["source_difference"]
                         ["reported_matching_weight_source_bytes_not_retransferred"], 47152036163)
        self.assertEqual(len(self.new["entries"]), 1)
        self.assertEqual(self.new["go_scope_bytes"], 4593276272)
        self.assertEqual(self.delta["go_scope_bytes"] + self.new["go_scope_bytes"], 332142349286)
        self.assertEqual(self.c["latest_r126_windows_aion_original"]
                         ["combined_r125_plus_r126_source_bytes"], 332142349286)

    def test_ledger_report_not_offline_owner_verification(self):
        self.assertEqual(self.oldlog["summary"]["models_verified"], 61)
        self.assertEqual(self.oldlog["summary"]["files_verified_total"], 708)
        self.assertEqual(self.oldlog["summary"]["bytes_verified_total"], 409835119252)
        self.assertTrue(self.c["latest_r126_windows_aion_original"]
                        ["owner_local_preflight_unverified"])


if __name__ == "__main__":
    unittest.main()
