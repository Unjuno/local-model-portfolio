"""R96 snapshot regression: publisher gate metadata is not download approval.

Reads historical v41 JSON only; never queries HF or loads model code/weights.
"""
import copy
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))
def key(x):
    return (x["asset_kind"], x["repo_id"])

def validate(catalog, conditional_access, snapshot, approved):
    if snapshot["canonical_revision"] != "v41-20261115":
        raise ValueError("wrong canonical revision")
    if len(catalog["items"]) != 195 or len(conditional_access["entries"]) != 95:
        raise ValueError("wrong historical catalog count")
    records = snapshot["records"]
    if len(records) != 38 or len({key(x) for x in records}) != 38:
        raise ValueError("HF sample not unique or complete")
    canonical = {key(x): x for x in catalog["items"]}
    access = {key(x): x for x in conditional_access["entries"]}
    for record in records:
        k = key(record)
        if k not in canonical:
            raise ValueError("source not in canonical catalog")
        if record["live_repository_metadata_gated_marker"] not in (
            "GATED_MARKER", "NO_GATED_MARKER"
        ):
            raise ValueError("unknown HF gate state")
        if not record["live_metadata_license_tag"]:
            raise ValueError("missing publisher license tag")
        if not record["live_metadata_updated_date_text"]:
            raise ValueError("missing timestamp")
        if record["owner_specific_entitlement_proven"] or record["download_approved"]:
            raise ValueError("public listing must never imply owner approval")
        if record["license_full_text_reviewed_by_this_refresh"]:
            raise ValueError("license tag cannot certify full legal text")
        if record["source_snapshot_immutable_sha_verified_by_this_refresh"]:
            raise ValueError("current repository listing cannot certify SHA")
        if k in access:
            observed = record["live_repository_metadata_gated_marker"] == "GATED_MARKER"
            if observed != access[k]["hub_gated"]:
                raise ValueError("HF access state conflicts with archived v41 ledger")
    gated = [x for x in records if x["review_group"] == "v41_conditional_gated"]
    if len(gated) != 20 or any(x["live_repository_metadata_gated_marker"] != "GATED_MARKER" for x in gated):
        raise ValueError("Gated 20/20 regression")
    if sum(x["asset_kind"] == "dataset" for x in gated) != 1:
        raise ValueError("gated dataset not included")
    unknown = {
        key(x) for x in catalog["items"]
        if x["asset_kind"] == "model" and x["portfolio_decision"] in ("select","conditional")
        and x["parameter_gate"]["status"] == "UNVERIFIED_BLOCK_FINAL_LOCK"
    }
    if len(unknown) != 9 or not unknown.issubset({key(x) for x in records}):
        raise ValueError("nine unknown-total assets not covered")
    selects = [x for x in records if x["active_selection"] == "select"]
    if len(selects) != 10:
        raise ValueError("selected non-Gated control scope")
    if any(x["live_repository_metadata_gated_marker"] != "NO_GATED_MARKER" for x in selects):
        raise ValueError("control not ungated")
    if approved["entries"]:
        raise ValueError("unexpected approved model acquisition")
    if snapshot["acquisition_approved"] or snapshot["download_enabled"]:
        raise ValueError("new access observation promoted to download")
    if snapshot["summary"]["unique_repos_checked"] != len(records):
        raise ValueError("incorrect declared sample count")
    return True

class R96LiveHuggingFaceSnapshot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat = load("catalog/effective-portfolio-2026-11-15-v41.json")
        cls.ac = load("catalog/access/2026-11-15-v41-conditional-hub-gates.json")
        cls.snapshot = load("catalog/access/2026-11-15-r96-v41-live-hf38-sample.json")
        cls.approved = load("queues/approved.json")

    def test_source_scope_counts_and_all_access_gates(self):
        self.assertTrue(validate(self.cat, self.ac, self.snapshot, self.approved))

    def test_changed_gated_marker_must_fail(self):
        s = copy.deepcopy(self.snapshot)
        row = next(x for x in s["records"] if x["review_group"] == "v41_conditional_gated")
        row["live_repository_metadata_gated_marker"] = "NO_GATED_MARKER"
        with self.assertRaisesRegex(ValueError, "conflicts|Gated"):
            validate(self.cat, self.ac, s, self.approved)

    def test_unknown_license_tag_must_fail(self):
        s = copy.deepcopy(self.snapshot)
        s["records"][0]["live_metadata_license_tag"] = None
        with self.assertRaisesRegex(ValueError, "license tag"):
            validate(self.cat, self.ac, s, self.approved)

    def test_inferred_personal_permission_must_fail(self):
        s = copy.deepcopy(self.snapshot)
        s["records"][0]["owner_specific_entitlement_proven"] = True
        with self.assertRaisesRegex(ValueError, "approval"):
            validate(self.cat, self.ac, s, self.approved)

    def test_unapproved_queue_cannot_change(self):
        a = {"entries": [{"repo_id": "fabricated"}]}
        with self.assertRaisesRegex(ValueError, "approved"):
            validate(self.cat, self.ac, self.snapshot, a)

if __name__=="__main__":
    unittest.main()
