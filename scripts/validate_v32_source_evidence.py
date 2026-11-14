#!/usr/bin/env python3
"""Offline, read-only audit of the v32 135-active source-evidence join.

Usage (from repository root):
  python3 scripts/validate_v32_source_evidence.py

This validates publisher *metadata references*, not local file integrity,
model functionality, legal entitlement, or download permission. No network.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "catalog/research/2026-11-15-r70-v32-all135-source-evidence-reconciliation.json"


def load(path: str | Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def active_ids(catalog: dict) -> dict:
    assets = [
        item
        for item in catalog["items"]
        if item["portfolio_decision"] in {"select", "conditional"}
    ]
    keys = [(item["asset_kind"], item["repo_id"]) for item in assets]
    assert len(keys) == len(set(keys)), "Duplicate active portfolio identity"
    return dict(zip(keys, assets))


def main() -> None:
    current = load("catalog/CURRENT.json")
    assert current["revision_id"] == "v32-20261114", "Stale v32 audit; regenerate before reuse"
    assert current["materialized_catalog_path"] == "catalog/effective-portfolio-2026-11-14-v32.json"

    v32 = load(current["materialized_catalog_path"])
    v27 = load("catalog/effective-portfolio-2026-11-07-v27.json")
    capacity = load("catalog/capacity/2026-11-07/v27/capacity-summary.json")
    r64 = load("manifests/drafts/r64-eight-source-scopes.candidate.json")
    r48 = load("catalog/research/2026-11-12-r48-pinned-scopes.json")
    report = load(RESEARCH.relative_to(ROOT))

    assert report["research_only"] is True
    assert report["approved"] is False and report["download_enabled"] is False
    assert report["weights_downloaded"] is False
    assert len(v32["items"]) == current["expected"]["tracked"] == 182

    old = active_ids(v27)
    now = active_ids(v32)
    assert len(old) == capacity["exact_primary_file_scope_count"] == 126
    assert len(now) == current["expected"]["active"] == 135
    assert set(old).issubset(now), "Old active ID missing from v32"

    sources = {repo["repo_id"]: repo for repo in r64["repositories"]}
    assert len(sources) == len(r64["repositories"]) == 9
    new = {key: item for key, item in now.items() if key not in old}
    assert len(new) == 9
    assert len([key for key in new if key[1] in sources]) == 8
    assert len([repo_id for repo_id in sources if not any(k[1] == repo_id for k in now)]) == 1

    profile = next(p for p in r48["profiles"] if p["id"] == "zonos_native_keep2_reference_scope")
    zonos = next(s for s in r48["sources"] if s["repo_id"] == "Zyphra/ZONOS3-Mini")
    assert len(profile["file_indices"]) == profile["file_count"] == 14
    assert len(set(profile["file_indices"])) == profile["file_count"]
    assert sum(r48["files"][i][2] for i in profile["file_indices"]) == profile["known_scope_bytes"]

    source_sum = 0
    source_files = 0
    for repo in sources.values():
        assert re.fullmatch(r"[a-fA-F0-9]{40}", repo["revision"])
        assert len(repo["files"]) == repo["file_count"]
        assert all(isinstance(f["bytes"], int) and f["bytes"] >= 0 for f in repo["files"])
        assert sum(f["bytes"] for f in repo["files"]) == repo["selected_bytes"]
        for f in repo["files"]:
            assert re.fullmatch(r"[0-9a-fA-F]{40}", f["git_blob_sha1"])
            if f.get("source_sha256") is not None:
                assert re.fullmatch(r"[0-9a-fA-F]{64}", f["source_sha256"])
        source_sum += repo["selected_bytes"]
        source_files += repo["file_count"]

    rows = report["rows"]
    identifiers = [(item["asset_kind"], item["repo_id"]) for item in rows]
    assert len(rows) == len(set(identifiers)) == len(now)
    assert set(identifiers) == set(now)
    counts = {"historical": 0, "r64": 0, "zonos": 0, "revision_conflicts": []}
    for row in rows:
        key = row["asset_kind"], row["repo_id"]
        asset = now[key]
        assert row["decision"] == asset["portfolio_decision"]
        assert row["tier"] == asset["risk_tier"]
        assert row["download_approved"] is False
        assert row["canonical_observed_revision"] == (asset["upstream_revision_sha_observed"] or None)
        assert row["canonical_final_revision"] == (asset["fully_pinned_revision_sha"] or None)
        assert row["canonical_selected_file_bytes"] == asset["selected_file_bytes"]
        if key in old:
            counts["historical"] += 1
            assert row["source_evidence_class"] == "V27_HISTORICAL_CENSUS_NEEDS_V32_SOURCE_REVALIDATION"
            assert row["source_scope_bytes"] is None
        elif key[1] in sources:
            counts["r64"] += 1
            evidence = sources[key[1]]
            assert row["source_revision"] == evidence["revision"]
            assert row["source_scope_bytes"] == evidence["selected_bytes"]
            assert row["source_file_count"] == evidence["file_count"]
            assert row["source_evidence_class"] == "R64_PINNED_CANDIDATE_SOURCE_SCOPE"
            observed = asset["upstream_revision_sha_observed"]
            expected_status = (
                "CANONICAL_OBSERVED_REVISION_MISSING" if not observed
                else "OBSERVED_REVISION_MATCH" if observed == evidence["revision"]
                else "REVISION_MISMATCH_NEEDS_CONTENT_DIFF"
            )
            assert row["revision_relation"] == expected_status
            if expected_status == "REVISION_MISMATCH_NEEDS_CONTENT_DIFF":
                counts["revision_conflicts"].append(key[1])
        else:
            counts["zonos"] += 1
            assert key[1] == zonos["repo_id"]
            assert row["source_revision"] == zonos["revision"]
            assert row["source_scope_bytes"] == profile["known_scope_bytes"]
            assert row["source_evidence_class"] == "R48_PINNED_REFERENCE_SCOPE_NOT_MINIMAL"

    assert (counts["historical"], counts["r64"], counts["zonos"]) == (126, 8, 1)
    assert counts["revision_conflicts"] == ["nvidia/RFD4-Proteina"]
    assert source_files == report["counts"]["r64_source_file_references"] == 91
    assert report["counts"]["active_missing_any_historical_or_candidate_source_evidence"] == 0
    assert sum(asset["selected_file_bytes"] is None for asset in now.values()) == 133
    assert sum(not asset["fully_pinned_revision_sha"] for asset in now.values()) == 133
    assert all(not item["download_approved"] for item in v32["items"])

    scenario = report["storage_scenario_bytes"]
    assert scenario["v27_historical_sha_aware_union"] == capacity["known_scope_content_union_bytes"]
    assert scenario["r64_nine_source_repo_file_sum"] == source_sum
    assert scenario["r48_zonos_reference_scope"] == profile["known_scope_bytes"]
    assert scenario["illustrative_additive_source_only_not_complete"] == (
        capacity["known_scope_content_union_bytes"] + source_sum + profile["known_scope_bytes"]
    )
    assert scenario["illustrative_source_only_difference_if_empty_true_4tb"] == (
        scenario["nominal_policy_cap"]
        - scenario["mandatory_minimum_free_floor"]
        - scenario["illustrative_additive_source_only_not_complete"]
    )
    assert scenario["source_only_not_strict_upper_or_lower_bound"] is True

    # Publisher OID evidence for the RFD4 revision difference, without payload downloads.
    r71 = load("catalog/research/2026-11-15-r71-rfd4-revision-file-identity.json")
    identity = report["source_identity_followup_2026_11_15"]
    assert r71["repo_id"] == "nvidia/RFD4-Proteina"
    assert r71["approved"] is False and r71["download_enabled"] is False
    assert r71["payload_downloaded"] is False and r71["local_hash_verified"] is False
    assert identity["verified_evidence"] == "catalog/research/2026-11-15-r71-rfd4-revision-file-identity.json"
    assert r71["statistics"]["selected_files"] == 7
    assert r71["statistics"]["identical_files"] == 3
    assert r71["statistics"]["changed_support_files"] == 4
    root = next(x for x in r71["files"] if x["path"] == "model.safetensors")
    assert root["content_identical"] is True
    assert root["old"]["lfs_sha256"] == root["new"]["lfs_sha256"]
    assert root["new"]["lfs_sha256"] == r71["statistics"]["root_model_payload_sha256"]
    assert root["new"]["bytes"] == 1742660596
    r64_rfd4 = sources["nvidia/RFD4-Proteina"]
    assert r64_rfd4["revision"] == r71["source_revision_candidate"]
    assert r71["source_revision_old"] == now[("model", "nvidia/RFD4-Proteina")]["upstream_revision_sha_observed"]
    for entry in r71["files"]:
        candidate = next(f for f in r64_rfd4["files"] if f["path"] == entry["path"])
        assert entry["new"]["bytes"] == candidate["bytes"]
        assert entry["new"]["git_blob_oid"] == candidate["git_blob_sha1"]
        if candidate["source_sha256"]:
            assert entry["new"]["lfs_sha256"] == candidate["source_sha256"]
    assert sum(x["old"]["bytes"] for x in r71["files"]) == r71["statistics"]["old_selected_scope_bytes"]
    assert sum(x["new"]["bytes"] for x in r71["files"]) == r71["statistics"]["new_selected_scope_bytes"]
    assert r71["statistics"]["new_minus_old_selected_scope_bytes"] == 2233
    assert sum(x["content_identical"] for x in r71["files"]) == 3
    assert sorted(x["path"] for x in r71["files"] if not x["content_identical"]) == sorted(
        ["README.md", "inference.yaml", "provenance.json", "release-checkpoints.json"]
    )

    # R64 internal dedup is NOT a claim of global v27+v32 dedup or HDD free space.
    by_hash = {}
    r64_file_rows = 0
    for repo in sources.values():
        for file in repo["files"]:
            digest = ("sha256:" + file["source_sha256"] if file["source_sha256"]
                      else "git_blob_sha1:" + file["git_blob_sha1"])
            r64_file_rows += 1
            if digest in by_hash:
                assert by_hash[digest] == file["bytes"]
            else:
                by_hash[digest] = file["bytes"]
    unique_bytes = sum(by_hash.values())
    assert r64_file_rows == 91
    assert source_sum - unique_bytes == identity["r64_internal_digest_deduplicated_bytes"] == 4451775
    assert len(by_hash) == identity["r64_unique_git_blob_or_lfs_identity_entries"] == 87
    assert identity["v27_plus_r64_internal_unique_plus_r48_scenario_bytes"] == (
        capacity["known_scope_content_union_bytes"] + unique_bytes + profile["known_scope_bytes"]
    )
    assert report["hard_gates"]["rfd4_model_payload_revision_difference_unverified"] is False
    assert report["hard_gates"]["rfd4_supporting_material_and_selected_revision_still_need_final_lock"] is True

    print(json.dumps({
        "result": "PASS_SOURCE_METADATA_JOIN_ONLY",
        "rfd4_root_model_oid_equivalent": True,
        "r64_verified_internal_duplicate_reference_bytes": 4451775,
        "revision": current["revision_id"],
        "active": len(now),
        "v27_historical": counts["historical"],
        "r64_new": counts["r64"],
        "zonos_new": counts["zonos"],
        "r64_file_rows": source_files,
        "unresolved_revision_conflicts": counts["revision_conflicts"],
        "nominal_source_only_bytes": scenario["illustrative_additive_source_only_not_complete"],
        "local_file_checks": 0,
        "download_approvals": 0,
    }, indent=2))


if __name__ == "__main__":
    main()
