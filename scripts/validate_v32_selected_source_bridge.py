#!/usr/bin/env python3
"""Validate the v32 135-asset historical selected-byte provenance bridge.

Offline, read-only, standard-library only. No downloads, no model execution, no
permission mutation. Run from any working directory with:
    python3 scripts/validate_v32_selected_source_bridge.py
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))

def active_by_id(document):
    records = [row for row in document["items"]
               if row["portfolio_decision"] in ("select", "conditional")]
    index = {(row["asset_kind"], row["repo_id"]): row for row in records}
    assert len(index) == len(records), "Duplicate active ID"
    return index

def main():
    current = read("catalog/CURRENT.json")
    assert current["revision_id"] == "v32-20261114", "V32 historical bridge is stale"
    canonical = read(current["materialized_catalog_path"])
    assert len(canonical["items"]) == current["expected"]["tracked"] == 182
    active = active_by_id(canonical)
    assert len(active) == current["expected"]["active"] == 135

    source = read("catalog/capacity/2026-11-07/v27/selected-file-capacity.json")
    r64 = read("manifests/drafts/r64-eight-source-scopes.candidate.json")
    r48 = read("catalog/research/2026-11-12-r48-pinned-scopes.json")
    r73 = read("catalog/research/2026-11-15-r73-nine-v27-v32-revision-payload-identity.json")
    bridge = read("catalog/research/2026-11-15-r72-v32-active135-selected-source-byte-bridge.json")
    assert bridge["research_only"] and not bridge["approved"] and not bridge["download_enabled"]
    assert bridge["catalog_revision"] == current["revision_id"]
    assert bridge["canonical_catalog"] == current["materialized_catalog_path"]
    assert not any(row["download_approved"] for row in canonical["items"])
    assert len(bridge["items"]) == len(active)
    assert len(source["items"]) == 126
    old = {(x["asset_kind"], x["repo_id"]): x for x in source["items"]}
    assert len(old) == 126 and set(old).issubset(active)

    nine = {x["repo_id"]: x for x in r73["rows"]}
    assert len(nine) == r73["counts"]["repositories"] == 9
    assert r73["counts"]["selected_file_references"] == 233
    assert r73["counts"]["new_selected_weight_changed_references"] == 0
    assert r73["counts"]["new_absent_support_files"] == 4
    assert r73["counts"]["modified_support_files"] == 8
    assert r73["counts"]["unchanged_selected_file_references"] == 221
    assert r73["legal_access_approved"] is False and r73["download_enabled"] is False
    assert r73["checkpoint_payloads_downloaded"] == 0

    r64_repos = {x["repo_id"]: x for x in r64["repositories"]}
    assert len(r64_repos) == len(r64["repositories"]) == 9
    zonos = next(x for x in r48["sources"] if x["repo_id"] == "Zyphra/ZONOS3-Mini")
    zonos_profile = next(x for x in r48["profiles"]
                         if x["id"] == "zonos_native_keep2_reference_scope")

    checks = Counter()
    sums = Counter()
    seen = set()
    for item in bridge["items"]:
        key = item["asset_kind"], item["repo_id"]
        assert key in active and key not in seen
        seen.add(key)
        orig = active[key]
        assert item["decision"] == orig["portfolio_decision"]
        assert item["risk_tier"] == orig["risk_tier"]
        assert item["v32_observed_revision"] == (orig.get("upstream_revision_sha_observed") or None)
        assert item["final_pinned_revision"] == (orig.get("fully_pinned_revision_sha") or None)
        assert item["canonical_selected_file_bytes"] == orig.get("selected_file_bytes")
        assert not item["download_approved"] and not item["final_acquisition_approved"]
        checks[item["revision_relation"]] += 1

        if key in old:
            x = old[key]
            assert item["source_evidence_path"] == "catalog/capacity/2026-11-07/v27/selected-file-capacity.json"
            assert item["publisher_source_revision"] == x["source_revision"]
            assert len(x["files"]) == item["publisher_selected_file_count"]
            file_sum = sum(f["bytes"] for f in x["files"])
            assert file_sum == x["primary_file_bytes"] == item["publisher_selected_file_bytes"]
            assert item["publisher_full_source_scope_bytes"] == x["source_scope_bytes"]
            assert item["publisher_package_bytes"] == x["package_bytes"]
            assert item["publisher_file_sha256_count"] == sum(bool(f.get("sha256")) for f in x["files"])
            assert item["publisher_git_blob_sha1_count"] == sum(bool(f.get("git_blob_sha1")) for f in x["files"])
            assert item["historical_unknown_or_masked_payload_identity_count"] == (
                x.get("masked_or_unknown_payload_identity_files") or 0
            )
            sums["selected"] += file_sum
            sums["upstream_scope"] += x["source_scope_bytes"]
            sums["package"] += x["package_bytes"]
            sums["files"] += len(x["files"])
            sums["sha256"] += item["publisher_file_sha256_count"]
            sums["git_sha1"] += item["publisher_git_blob_sha1_count"]
            sums["masked"] += item["historical_unknown_or_masked_payload_identity_count"]
            sums["different_scope"] += (x["source_scope_bytes"] != file_sum)

            obs = orig.get("upstream_revision_sha_observed")
            status = ("OLD_CANONICAL_REVISION_MISSING" if not obs
                      else "OLD_REVISION_MATCH" if obs == x["source_revision"]
                      else "OLD_REVISION_DIFFERENT_SELECTED_WEIGHT_IDENTITY_PROVEN_SAME")
            assert item["revision_relation"] == status, key
            if status.endswith("IDENTITY_PROVEN_SAME"):
                claim = nine[item["repo_id"]]
                assert claim["new_revision_selected_weight_blobs_identity_unchanged"] is True
                assert claim["old_selected_revision"] == x["source_revision"]
                assert claim["v32_observed_revision"] == obs
                assert claim["old_selected_file_count"] == len(x["files"])
                paths = {f["path"] for f in x["files"]}
                for missing in claim["missing_support_paths_at_new_revision"]:
                    assert missing in paths
                for modified in claim["changed_support_files_at_new_revision"]:
                    assert modified["path"] in paths

        elif item["repo_id"] in r64_repos:
            x = r64_repos[item["repo_id"]]
            assert item["source_evidence_path"] == "manifests/drafts/r64-eight-source-scopes.candidate.json"
            assert item["publisher_source_revision"] == x["revision"]
            assert item["publisher_selected_file_count"] == len(x["files"]) == x["file_count"]
            amount = sum(f["bytes"] for f in x["files"])
            assert amount == x["selected_bytes"] == item["publisher_selected_file_bytes"]
            sums["new_r64"] += amount
        else:
            assert key == ("model", "Zyphra/ZONOS3-Mini")
            assert item["publisher_source_revision"] == zonos["revision"]
            assert item["publisher_selected_file_count"] == zonos_profile["file_count"] == 14
            assert item["publisher_selected_file_bytes"] == zonos_profile["known_scope_bytes"]
            sums["zonos"] += item["publisher_selected_file_bytes"]

    assert seen == set(active), "Bridge does not cover current 135 active identities"
    expected_counts = {
        "OLD_REVISION_MATCH": 85,
        "OLD_CANONICAL_REVISION_MISSING": 32,
        "OLD_REVISION_DIFFERENT_SELECTED_WEIGHT_IDENTITY_PROVEN_SAME": 9,
        "NEW_CANONICAL_REVISION_MISSING": 5,
        "NEW_CANONICAL_REVISION_MISSING_OR_DIFFERENT": 1,
        "NEW_REVISION_MATCH": 2,
        "NEW_REVISION_DIFFERENT_SUPPORT_REVIEW_REQUIRED": 1,
    }
    assert dict(checks) == expected_counts
    assert dict(checks) == bridge["counts"]["revision_statuses"]
    assert sums["selected"] == bridge["bytes"]["historical_v27_126_selected_primary_file_sum"] == 3413612735064
    assert sums["upstream_scope"] == bridge["bytes"]["historical_v27_126_full_source_scopes_sum"] == 6399135485511
    assert sums["package"] == bridge["bytes"]["historical_v27_126_parent_referenced_package_sum"] == 3569207077684
    assert sums["files"] == 59938
    assert sums["sha256"] == 50314 and sums["git_sha1"] == 59938
    assert sums["different_scope"] == 66
    assert sums["new_r64"] == 33219541806
    assert sums["zonos"] == 11076560635
    assert sum(x["selected_bytes"] for x in r64["repositories"]) == 38519866446
    assert bridge["bytes"]["r64_additional_external_ace_step_source"] == 5300324640
    assert sums["selected"] + sums["new_r64"] + sums["zonos"] == 3457908837505
    assert bridge["bytes"]["all135_arithmetic_selected_primary_and_zonos_reference_without_missing_deps"] == 3457908837505
    assert bridge["bytes"]["physical_disk_free"] is None
    assert bridge["bytes"]["final_full_offline_bytes"] is None
    assert bridge["counts"]["canonical_final_bytes_missing"] == 133
    assert bridge["counts"]["canonical_final_pin_missing"] == 133

    print(json.dumps({
        "result": "PASS_RESEARCH_SOURCE_METADATA_ONLY",
        "catalog_revision": current["revision_id"],
        "active_ids": len(active),
        "old_profile_files": sums["files"],
        "old_source_scope_divergences": sums["different_scope"],
        "revision_relation": dict(checks),
        "research_profile_bytes": 3457908837505,
        "download_authorized": False,
        "local_hash_verified": False,
        "owner_disk_verified": False
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
