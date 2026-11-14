"""Fail-closed research-scope tests; no model downloads, execution or network."""
import copy
import json
import unittest

from scripts.validate_rare_specialist_proposal import (
    APPROVED, CATALOG, PROPOSAL, ROOT, validate
)


class RareSpecialistSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proposal = json.loads((ROOT / PROPOSAL).read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / CATALOG).read_text(encoding="utf-8"))
        cls.approvals = json.loads((ROOT / APPROVED).read_text(encoding="utf-8"))

    def test_five_sources_have_valid_metadata_but_no_acquisition_authorization(self):
        result = validate(self.proposal, self.catalog, self.approvals)
        self.assertEqual(result["status"], "PASS_RESEARCH_METADATA_ONLY")
        self.assertEqual(result["candidates"], 5)
        self.assertEqual(result["gated_without_entitlement"], 2)
        self.assertEqual(result["source_bytes"], 2_805_003_661)
        self.assertFalse(result["formal_selection_changed"])

    def test_pickle_loader_security_hold_cannot_be_bypassed(self):
        x = copy.deepcopy(self.proposal)
        item = next(r for r in x["candidates"] if r["repo_id"] == "nvidia/Kumo-Anomaly")
        item["decision"] = "RECOMMEND_CONDITIONAL_FOR_NEXT_FORMAL_REVIEW"
        with self.assertRaisesRegex(ValueError, "unsafe decision"):
            validate(x, self.catalog, self.approvals)

    def test_ising_gated_metadata_never_implies_entitlement(self):
        x = copy.deepcopy(self.proposal)
        item = next(r for r in x["candidates"]
                    if r["repo_id"] == "nvidia/Ising-Decoder-ColorCode-1-Fast")
        item["anonymous_access_state"] = "public_ungated_metadata"
        with self.assertRaisesRegex(ValueError, "Gated access bypass"):
            validate(x, self.catalog, self.approvals)

    def test_publisher_byte_count_must_match_each_selected_file(self):
        x = copy.deepcopy(self.proposal)
        item = next(r for r in x["candidates"] if r["repo_id"] == "nvidia/Kumo-Relational")
        item["proposed_source_files"][0]["bytes"] += 1
        with self.assertRaisesRegex(ValueError, "publisher file sum mismatch"):
            validate(x, self.catalog, self.approvals)

    def test_local_sha_must_not_be_claimed_without_payload(self):
        x = copy.deepcopy(self.proposal)
        x["candidates"][0]["proposed_source_files"][0]["owner_local_sha_verified"] = True
        with self.assertRaisesRegex(ValueError, "payload claimed verified"):
            validate(x, self.catalog, self.approvals)

    def test_parameter_unsupported_promotion_is_rejected(self):
        x = copy.deepcopy(self.proposal)
        item = next(r for r in x["candidates"] if r["repo_id"] == "nvidia/Kumo-Relational")
        item["parameter_screening"]["observed_model_parameters"] = 123456
        with self.assertRaisesRegex(ValueError, "full count not proved"):
            validate(x, self.catalog, self.approvals)

    def test_final_lock_cannot_be_inferred_from_metadata(self):
        x = copy.deepcopy(self.proposal)
        x["candidates"][0]["final_lock_eligible"] = True
        with self.assertRaisesRegex(ValueError, "approval or entitlement improperly asserted"):
            validate(x, self.catalog, self.approvals)

    def test_owner_approval_queue_must_remain_empty(self):
        with self.assertRaisesRegex(ValueError, "acquisition queue"):
            validate(self.proposal, self.catalog, {"entries": [{"unapproved": True}]})


if __name__ == "__main__":
    unittest.main()
