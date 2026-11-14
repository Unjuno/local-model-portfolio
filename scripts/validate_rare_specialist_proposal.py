#!/usr/bin/env python3
"""Validate pinned rare specialist research only; stdlib, no network, no payload fetch.

Python >= 3.10. This cannot approve acquisition or prove local payload identity.
"""
from __future__ import annotations
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = "catalog/proposals/07-rare-specialist-2026-11-15.json"
CATALOG = "catalog/effective-portfolio-2026-11-14-v32.json"
APPROVED = "queues/approved.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
EXPECTED = {
    "nvidia/Kumo-Relational": "RECOMMEND_CONDITIONAL_FOR_NEXT_FORMAL_REVIEW",
    "nvidia/Kumo-Anomaly": "HOLD_UNTIL_SECURE_PICKLE_DESERIALIZATION_AND_OFFLINE_RUNTIME",
    "nvidia/Ising-Decoder-ColorCode-1-Fast": "P0_RESEARCH_PERSONAL_GATED_ENTITLEMENT_FIRST",
    "nvidia/Ising-Decoder-SurfaceCode-1-Fast": "P0_RESEARCH_PERSONAL_GATED_ENTITLEMENT_FIRST",
    "nvidia/Nemotron-3.5-Parse": "HOLD_PENDING_OCR_DISTINCTNESS_AND_RUNTIME_COMPARISON",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(proposal: dict, catalog: dict, approved: dict) -> dict:
    require(catalog.get("revision_id") == "v32-20261114", "unexpected canonical revision")
    require(len(catalog.get("items", [])) == 182, "canonical asset count drifted")
    require(sum(x.get("portfolio_decision") in ("select", "conditional")
                for x in catalog["items"]) == 135, "canonical active count drifted")
    require(not approved.get("entries"), "acquisition queue must remain empty")
    require(proposal.get("selection_state_unchanged") is True, "formal adoption asserted")
    records = proposal.get("candidates")
    require(isinstance(records, list) and len(records) == 5, "expected five candidates")
    byid = {r["repo_id"]: r for r in records}
    require(len(byid) == len(records) and set(byid) == set(EXPECTED),
            "candidate ID set or uniqueness mismatch")
    canonical_ids = {x["repo_id"] for x in catalog["items"]}
    totals, gated = 0, 0
    for ident, item in byid.items():
        require(ident not in canonical_ids, f"candidate already in canonical: {ident}")
        require(item["decision"] == EXPECTED[ident], f"unsafe decision: {ident}")
        require(bool(HEX40.fullmatch(item["source_revision"])), f"missing 40hex pin: {ident}")
        require(item["download_authorized"] is False and
                item["formal_catalog_change_approved"] is False and
                item["anonymous_metadata_not_user_entitlement"] is True,
                f"approval or entitlement improperly asserted: {ident}")
        files = item["proposed_source_files"]
        require(isinstance(files, list) and files, f"empty file scope: {ident}")
        require(len(files) == item["candidate_selected_file_count"],
                f"file count inconsistent: {ident}")
        require(len({f["path"] for f in files}) == len(files),
                f"repeated source path: {ident}")
        total = 0
        for f in files:
            require(isinstance(f["bytes"], int) and not isinstance(f["bytes"], bool)
                    and f["bytes"] > 0, f"bad file bytes: {ident}/{f['path']}")
            require(bool(HEX40.fullmatch(f["publisher_git_blob_sha1"])),
                    f"bad Git blob identity: {ident}/{f['path']}")
            sha = f.get("publisher_lfs_sha256")
            require(sha is None or bool(HEX64.fullmatch(sha)),
                    f"bad LFS SHA256: {ident}/{f['path']}")
            if f["path"].endswith((".pt", ".pth", ".safetensors")):
                require(sha is not None, f"trained weight missing publisher SHA: {ident}")
            require(f["file_payload_fetched"] is False and
                    f["owner_local_sha_verified"] is False, f"payload claimed verified: {ident}")
            total += f["bytes"]
        require(total == item["candidate_selected_source_bytes"],
                f"publisher file sum mismatch: {ident}")
        if ident in ("nvidia/Ising-Decoder-ColorCode-1-Fast",
                     "nvidia/Ising-Decoder-SurfaceCode-1-Fast"):
            require(item["anonymous_access_state"] == "gated_auto_metadata" and
                    item["decision"].startswith("P0_RESEARCH_PERSONAL_GATED"),
                    f"Gated access bypass: {ident}")
            gated += 1
        totals += total
    kumo = byid["nvidia/Kumo-Relational"]["publisher_tag_compatibility"]
    require(kumo["torch_load_weights_only"] is True and
            kumo["will_download_missing_config_or_checkpoint_by_default"] is True and
            bool(HEX40.fullmatch(kumo["revision_alias_observed_resolves_to"])),
            "Kumo relational offline safety gate lost")
    anomaly = byid["nvidia/Kumo-Anomaly"]["security_and_code_evidence"]
    require(anomaly["pytorch_flag"] == "torch.load(...,weights_only=False)" and
            anomaly["unsafe_pickle_calls_observed_in_inference_ad"] >= 1 and
            anomaly["unsafe_pickle_in_worker"] is True,
            "Kumo Anomaly unsafe-loader stop not recorded")
    require(byid["nvidia/Nemotron-3.5-Parse"]["candidate_selected_file_count"] == 6,
            "Nemotron deliberately incomplete source set changed")
    require(totals == 2_805_003_661, "unexpected source reference scope sum")
    require(gated == 2, "Gated candidate count changed")
    return {"status": "PASS_RESEARCH_METADATA_ONLY", "candidates": 5,
            "gated_without_entitlement": 2, "source_bytes": totals,
            "formal_selection_changed": False, "downloads_authorized": 0}


def main() -> None:
    data = json.loads((ROOT / PROPOSAL).read_text(encoding="utf-8"))
    cat = json.loads((ROOT / CATALOG).read_text(encoding="utf-8"))
    approval = json.loads((ROOT / APPROVED).read_text(encoding="utf-8"))
    print(json.dumps(validate(data, cat, approval), indent=2))


if __name__ == "__main__":
    main()
