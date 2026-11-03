"""Offline deterministic unit tests for the hard 150B parameter gate.

No model execution, network access, file downloads, or third-party dependencies.
Run: python -m unittest discover -s tests -p "test_parameter_cutoff.py"
"""
import unittest

from scripts.check_parameter_cutoff import validate_model

CAP = 150_000_000_000


def record(count, gate, decision="select", tier="R1"):
    return {
        "repo_id": "unit/fake",
        "asset_kind": "model",
        "risk_tier": tier,
        "portfolio_decision": decision,
        "parameter_gate": {"total_parameters": count, "status": gate},
    }


class ParameterCapTests(unittest.TestCase):
    def test_under_150b_passes_parameter_gate(self):
        self.assertEqual([], validate_model(record(80_000_000_000, "PASS_TOTAL_PARAMS_LT_150B"), CAP))

    def test_exactly_150b_requires_exclusion(self):
        r = record(150_000_000_000, "EXCLUDED_TOTAL_PARAMS_GE_150B", "excluded", "EXCLUDED")
        self.assertEqual([], validate_model(r, CAP))
        self.assertNotEqual([], validate_model(record(150_000_000_000, "PASS_TOTAL_PARAMS_LT_150B"), CAP))

    def test_1t_moe_active_52b_cannot_bypass_total(self):
        r = record(1_050_000_000_000, "PASS_TOTAL_PARAMS_LT_150B")
        r["active_parameters"] = 52_000_000_000
        self.assertNotEqual([], validate_model(r, CAP))

    def test_unknown_does_not_pass(self):
        self.assertEqual([], validate_model(record(None, "UNVERIFIED_BLOCK_FINAL_LOCK"), CAP))
        self.assertNotEqual([], validate_model(record(None, "PASS_TOTAL_PARAMS_LT_150B"), CAP))

    def test_invalid_count_does_not_pass(self):
        self.assertNotEqual([], validate_model(record(-1, "PASS_TOTAL_PARAMS_LT_150B"), CAP))
        self.assertNotEqual([], validate_model(record(150.0, "EXCLUDED_TOTAL_PARAMS_GE_150B"), CAP))



    def test_just_below_150b_passes(self):
        self.assertEqual([], validate_model(record(149_999_999_999, "PASS_TOTAL_PARAMS_LT_150B"), CAP))

    def test_qwen_flash_180b_includes_ngrams_mtp(self):
        total = 125_000_000_000 + 51_000_000_000 + 4_000_000_000
        self.assertEqual(total, 180_000_000_000)
        self.assertNotEqual([], validate_model(record(total, "PASS_TOTAL_PARAMS_LT_150B"), CAP))
        self.assertEqual([], validate_model(record(total, "EXCLUDED_TOTAL_PARAMS_GE_150B", "excluded", "EXCLUDED"), CAP))

    def test_excluded_but_missing_decision_is_fail(self):
        self.assertNotEqual([], validate_model(record(180_000_000_000, "EXCLUDED_TOTAL_PARAMS_GE_150B"), CAP))

if __name__ == "__main__":
    unittest.main()
