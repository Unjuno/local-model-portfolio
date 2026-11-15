"""R91 snapshot contract: primary-policy evidence and 148 blocked assets (stdlib only)."""
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = "catalog/research/2026-11-15-r91-v40-148-policy-and-insurance-triage.json"

def read(name):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise ValueError("unsafe path")
    return json.loads(path.read_text(encoding="utf-8"))

def identity(x):
    return x["asset_kind"], x["repo_id"]

class R91V40PolicyCensus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = read(P)
        cls.catalog = read("catalog/effective-portfolio-2026-11-15-v40.json")
        cls.readiness = read("catalog/readiness/v40-2026-11-15-r90-all148-gates.json")
        cls.access = read("catalog/access/2026-11-15-v40-conditional-hub-gates.json")

    def test_unique_and_currently_selected_coverage(self):
        rows = self.audit["entries"]
        active = [x for x in self.catalog["items"] if
                  x["portfolio_decision"] in ("select", "conditional")]
        self.assertEqual(len(self.catalog["items"]), 195)
        self.assertEqual(len(active), 148)
        self.assertEqual(len(rows), 148)
        self.assertEqual(len(set(map(identity, rows))), 148)
        self.assertEqual({identity(x) for x in rows}, {identity(x) for x in active})
        self.assertEqual([x["decision"] for x in rows], [x["portfolio_decision"] for x in active])

    def test_first_blocker_is_exact_and_independent(self):
        rows = self.audit["entries"]
        got = dict(Counter(x["first_blocker"] for x in rows))
        self.assertEqual(got, self.readiness["summary"]["first_blocker_counts"])
        self.assertEqual(got, {
            "OWNER_SPECIFIC_GATED_ENTITLEMENT": 19,
            "OWNER_HDD_ACTUAL_CAPACITY_AND_STAGING": 2,
            "SINGLE_IMMUTABLE_SOURCE_FILE_SET": 118,
            "COMPLETE_TRAINED_TOTAL_PARAMETERS": 9,
        })
        self.assertTrue(all(x["first_blocker"] in x["all_blocking_gates"] for x in rows))
        self.assertEqual(len(self.access["entries"]), 95)
        self.assertEqual(sum(x["hub_gated"] for x in self.access["entries"]), 20)
        self.assertEqual(self.audit["summary"]["unverified_select_access_sidecars"], 53)

    def test_stale_groundingpi_gated_flag_corrected(self):
        research = read("catalog/research/2026-11-15-r88-groundingpi-thinker-original-license-comparison.json")
        record = next(x for x in self.access["entries"] if x["repo_id"] == "GroundingPI/GroundingPI")
        self.assertFalse(record["hub_gated"])
        self.assertFalse(research["ground"]["model_gated"])
        self.assertEqual(research["ground"]["model_gated_correction"]["old_value"], True)
        self.assertEqual(record["owner_access_permission"], "unknown")
        self.assertFalse(record["download_authorized"])

    def test_uncertainty_and_approval_fail_closed(self):
        rows = self.audit["entries"]
        self.assertEqual(sum(x["parameter_gate"] == "UNVERIFIED_BLOCK_FINAL_LOCK" for x in rows), 9)
        self.assertTrue(all(not x["download_approved"] and not x["ready_to_acquire"] and
                            not x["local_payload_sha_verified"] and
                            not x["offline_restore_verified"] for x in rows))
        self.assertFalse(self.audit["capacity_hard_gates"]["final_storage_fit_verified"])
        self.assertIsNone(self.audit["capacity_hard_gates"]["owner_actual_free_bytes"])
        self.assertEqual(read("queues/approved.json")["entries"], [])
        self.assertEqual(self.readiness["summary"]["ready_to_approve"], 0)
        policy = read("policies/limits.json")["total_parameter_policy"]
        self.assertEqual(policy["mode"], "BASELINE_WITH_QUANTIZED_RUNTIME_EXCEPTION")
        self.assertFalse(policy["hard_exclusion_by_parameter_count_alone"])
        self.assertTrue(any(x["license_tag_only"] and "other" in x["license_tag_only"]
                            for x in rows))
        self.assertEqual(len(self.audit["legal_observations"]), 6)

if __name__ == "__main__":
    unittest.main()
