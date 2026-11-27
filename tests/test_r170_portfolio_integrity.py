import json
import unittest
from pathlib import Path
from scripts.audit_portfolio_integrity import audit, AUTH_GATES

ROOT = Path(__file__).resolve().parents[1]

class PortfolioIntegrity(unittest.TestCase):
    def test_current_read_only_audit(self):
        report = audit(ROOT)
        self.assertEqual(report["errors"], [])
        self.assertFalse(report["acquisition_authorized"])
        self.assertFalse(report["physical_deletion_authorized"])

    def test_v74_correction_preserves_stops(self):
        p = ROOT / "catalog/readiness/v74-2026-11-27-r169-all210-gates.json"
        r = json.loads(p.read_text(encoding="utf-8"))
        self.assertEqual(len(r["records"]), 210)
        self.assertEqual(len(r["r170_metadata_only_correction"]["record_corrections"]), 2)
        self.assertTrue(all(AUTH_GATES.intersection(i["blocking_gates"]) and not i["download_approved"] for i in r["records"]))
        self.assertTrue(all(i["first_blocker"] in i["blocking_gates"] for i in r["records"]))

if __name__ == "__main__":
    unittest.main()
