"""Regression tests for typed catalog identity and legacy receipt classification."""
import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / "scripts" / "audit_typed_portfolio_composition.py"
spec = importlib.util.spec_from_file_location("typed_portfolio", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class TypedPortfolioTests(unittest.TestCase):
    def test_dataset_legacy_receipt(self):
        self.assertEqual(mod.receipt_kind({"repo_id":"x"}, {"x":{"dataset"}}), "dataset")
    def test_unregistered(self):
        self.assertEqual(mod.receipt_kind({"repo_id":"x"}, {}), "unresolved")
    def test_ambiguous(self):
        self.assertEqual(mod.receipt_kind({"repo_id":"x"}, {"x":{"model","dataset"}}), "unresolved")
    def test_declared_kind(self):
        self.assertEqual(mod.receipt_kind({"repo_id":"x","asset_kind":"dataset"}, {"x":{"model","dataset"}}), "dataset")
    def test_conflicting_declared_kind(self):
        self.assertEqual(mod.receipt_kind({"repo_id":"x","asset_kind":"model"}, {"x":{"dataset"}}), "unresolved")
    def test_duplicate_typed_identity(self):
        with self.assertRaises(ValueError):
            mod.unique_keys([{"asset_kind":"model","repo_id":"x"}]*2)
    def test_distinct_typed_identities(self):
        self.assertEqual(len(mod.unique_keys([{"asset_kind":"model","repo_id":"x"},{"asset_kind":"dataset","repo_id":"x"}])), 2)

if __name__ == "__main__":
    unittest.main()
