"""Read-only tests for v16 decision policy."""
import unittest
from scripts.audit_selection_decisions import check_record,audit

ROW={
"key":"HF:sample/model","provider":"huggingface","model_id":"sample/model","portfolio_decision":"conditional",
"in_portfolio":True,"evidence_grade":"B","quality_positive":"reported external comparison",
"quality_negative":"underpowered benchmark",
"publisher_url":"https://huggingface.co/sample/model","license_text_reviewed":False,
"source_revision_sha":None,"selected_file_sha256_complete":False,"download_authorized":False
}

class DecisionAuditTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual([],check_record(ROW,{"sample/model"}))
    def test_no_unverified_download(self):
        r=dict(ROW,download_authorized=True)
        self.assertTrue(check_record(r,{"sample/model"}))
    def test_no_untracked_active(self):
        self.assertTrue(check_record(ROW,set()))
    def test_requires_negative_evidence(self):
        r=dict(ROW,quality_negative="")
        self.assertTrue(check_record(r,{"sample/model"}))
    def test_no_hf_alias_for_civitai(self):
        r=dict(ROW,provider="civitai",model_id=2218365,model_version_id=3411348)
        self.assertTrue(check_record(r,{"sample/model"}))
    def test_current_repository(self):
        self.assertEqual([],audit())

if __name__=="__main__":unittest.main()
