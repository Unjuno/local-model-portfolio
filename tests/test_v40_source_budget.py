"""R91 regression: v40 budget is an estimate, not owner-verified archive or legal authorization."""
import unittest
from scripts.validate_v40_source_budget import validate

class V40Budget(unittest.TestCase):
    def test_revisions_and_decimal_bytes(self):
        r = validate()
        self.assertEqual(r["revision"], "v40-20261115")
        self.assertEqual((r["tracked"], r["active"]), (195, 148))
        self.assertEqual(r["revision_cap_total_bytes"], 204_520_000_000)
        self.assertEqual(r["nominal_total_bytes"], 3_670_590_232_173)
        self.assertEqual(r["nominal_after_floor_margin_bytes"], 129_409_767_827)

    def test_fail_closed_owner_runtime(self):
        r = validate()
        self.assertFalse(r["real_disk_measured"])
        self.assertFalse(r["download_authorized"])
        self.assertFalse(r["full_offline_dependencies_verified"])

if __name__ == "__main__":
    unittest.main()
