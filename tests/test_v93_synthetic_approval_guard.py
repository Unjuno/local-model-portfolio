import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestV93SyntheticApprovalGuard(unittest.TestCase):
    def test_plan_is_review_only(self):
        s=(ROOT/"scripts/build_v93_plan.py").read_text(encoding="utf-8")
        self.assertIn("review-v93-UNAPPROVED.json",s)
        self.assertNotIn("APPROVAL.write_text",s)
        for key in ("approved","download_enabled","approved_by_user","license_text_reviewed","parent_dependency_rights_reviewed","nonstandard_license_permission_verified"):
            self.assertNotIn(f'"{key}": True',s)
        self.assertIn('"approval_ref": None',s)
    def test_legacy_rejected(self):
        s=(ROOT/"scripts/preserve_execute.py").read_text(encoding="utf-8")
        self.assertIn('or review_ref.startswith("v73-remaining-pinned-")',s)
        self.assertIn('"v73 permissive public assets, pinned via publisher api" in source',s)
        self.assertIn('"v93 metadata-only review" in source',s)
