"""Regression tests for v38 research access/risk/budget consistency (stdlib only)."""
import unittest
from scripts.verify_v38_r88_access_scope import verify,load,unique_index,EXPECTED_CLASSES
from collections import Counter
class V38R88(unittest.TestCase):
 def test_v38_full_census(self):
  out=verify()
  self.assertEqual(out["result"],"PASS_METADATA_ONLY_NO_HDD_OR_PAYLOADS")
  self.assertEqual((out["tracked"],out["active"],out["conditional_access"],out["gated"]),(193,146,93,20))
  self.assertFalse(out["download_authorized"])
 def test_no_gated_bypass_and_select_not_misclassified(self):
  a=load("catalog/access/2026-11-15-v38-conditional-hub-gates.json")
  t=load("catalog/research/2026-11-15-r88-v38-146-access-risk-and-capacity-triage.json")
  self.assertEqual(t["summary"]["select_records_without_conditional_access_sidecar"],53)
  self.assertEqual(Counter(r["investigation_class"] for r in t["records"]),Counter(EXPECTED_CLASSES))
  self.assertFalse(a["download_authorized"])
  self.assertEqual(a["owner_authorizations_verified"],0)
 def test_source_scope_reuse_is_not_owner_disk_reuse(self):
  m=load("manifests/drafts/v38-haru-praxis-original-selected-source.candidate.json")
  self.assertFalse(m["already_selected_VAE_reference"]["local_hdd_reuse_verified"])
  self.assertEqual(m["publisher_reference_file_count"],43)
  self.assertFalse(m["allow_full_repo_download"])
  self.assertTrue(m["requires_owner_local_HDD_and_checksum"])
if __name__=="__main__":unittest.main()
