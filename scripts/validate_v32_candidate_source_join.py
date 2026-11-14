#!/usr/bin/env python3
"""Offline, read-only audit of v32 candidate source byte/revision joins (R72/R73).

Usage, from repository root:
    python3 scripts/validate_v32_candidate_source_join.py

No network requests, model downloads, local file mutations, or approval changes.
Only verifies research evidence, NOT a lawful or runnable archive lock.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def require(cond: bool, message: str) -> None:
    if not cond:
        raise AssertionError(message)


def main() -> None:
    cur = read("catalog/CURRENT.json")
    require(cur["revision_id"] == "v32-20261114", "Canonical revision changed: regenerate R72/R73")
    v32 = read(cur["materialized_catalog_path"])
    v27 = read("catalog/preparation/2026-11-09-v27-manifest-readiness.json")
    v27cap = read("catalog/capacity/2026-11-07/v27/capacity-summary.json")
    r64 = read("manifests/drafts/r64-eight-source-scopes.candidate.json")
    r48 = read("catalog/research/2026-11-12-r48-pinned-scopes.json")
    r71 = read("catalog/research/2026-11-15-r71-rfd4-revision-file-identity.json")
    r72 = read("catalog/research/2026-11-15-r72-v32-135-candidate-scope-byte-revision-join.json")
    r73 = read("catalog/research/2026-11-15-r73-14-upstream-head-observations.json")

    assets = v32["items"]
    require(len(assets) == cur["expected"]["tracked"] == 182, "v32 record count")
    require(len({(a["asset_kind"], a["repo_id"]) for a in assets}) == len(assets),
            "Duplicate v32 asset ID")
    active = {(a["asset_kind"], a["repo_id"]): a for a in assets
              if a["portfolio_decision"] in ("select", "conditional")}
    require(len(active) == cur["expected"]["active"] == 135, "v32 active count")
    require(all(not a["download_approved"] for a in assets), "Unapproved catalog change")
    require(r72["approved"] is False and r72["download_enabled"] is False, "R72 is executable")
    require(r73["download_authorized"] is False and r73["weights_fetched"] is False,
            "R73 is executable")
    require(r72["canonical_revision"] == r73["canonical_revision"] == cur["revision_id"],
            "Wrong source version")

    old = {(a["asset_kind"], a["repo_id"]): a for a in v27["assets"]}
    cand = {a["repo_id"]: a for a in r64["repositories"]}
    require(len(old) == 126 and len(cand) == 9, "Old catalog or R64 changed")
    profile = next(p for p in r48["profiles"]
                   if p["id"] == "zonos_native_keep2_reference_scope")
    zonos = next(s for s in r48["sources"] if s["repo_id"] == "Zyphra/ZONOS3-Mini")
    require(len(profile["file_indices"]) == profile["file_count"] == 14,
            "ZONOS profile count")
    require(sum(r48["files"][i][2] for i in profile["file_indices"])
            == profile["known_scope_bytes"], "ZONOS profile bytes")

    rows = r72["rows"]
    keys = [(r["asset_kind"], r["repo_id"]) for r in rows]
    require(len(keys) == len(set(keys)) == 135 and set(keys) == set(active),
            "R72 active set mismatch")
    classes = Counter()
    relations = Counter()
    candidate_sum = 0
    for row in rows:
        key = (row["asset_kind"], row["repo_id"])
        a = active[key]
        require(row["portfolio_decision"] == a["portfolio_decision"]
                and row["risk_tier"] == a["risk_tier"], f"Status drift: {key}")
        require(row["canonical_observed_revision"] == (a["upstream_revision_sha_observed"] or None),
                f"Observed revision changed: {key}")
        require(row["canonical_final_revision"] == (a["fully_pinned_revision_sha"] or None),
                f"Final revision changed: {key}")
        require(row["canonical_final_selected_file_bytes"] == a["selected_file_bytes"],
                f"Final bytes changed: {key}")
        require(row["download_approved"] is False
                and row["candidate_is_final_approved_lock"] is False,
                f"Acquisition flag unexpectedly enabled: {key}")
        if key in old:
            item = old[key]
            cclass = "V27_READINESS_PRIMARY_SCOPE"
            b = item["selected_source_primary_bytes"]
            rev = item["candidate_publisher_revision"] or None
            evidence = "catalog/preparation/2026-11-09-v27-manifest-readiness.json"
            nfiles = None
        elif row["repo_id"] in cand:
            item = cand[row["repo_id"]]
            cclass = "R64_PINNED_CANDIDATE_SOURCE"
            b = item["selected_bytes"]
            require(b == sum(f["bytes"] for f in item["files"]), "R64 file sum")
            rev = item["revision"]
            evidence = "manifests/drafts/r64-eight-source-scopes.candidate.json"
            nfiles = item["file_count"]
        else:
            require(row["repo_id"] == zonos["repo_id"], f"Uncovered ID: {key}")
            cclass = "R48_ZONOS_KEEP2_PINNED_REFERENCE_NOT_MINIMAL"
            b = profile["known_scope_bytes"]
            rev = zonos["revision"]
            evidence = "catalog/research/2026-11-12-r48-pinned-scopes.json"
            nfiles = profile["file_count"]
        require(isinstance(b, int) and b >= 0, f"Invalid source bytes: {key}")
        require(row["source_scope_evidence"] == cclass, f"Wrong evidence class: {key}")
        require(row["source_evidence_path"] == evidence, f"Wrong evidence path: {key}")
        require(row["source_candidate_bytes"] == b
                and row["source_candidate_revision"] == rev
                and row["source_candidate_file_count"] == nfiles,
                f"Stale source candidate: {key}")
        obs = a["upstream_revision_sha_observed"] or None
        if obs and rev:
            relation = ("MATCHES_CANONICAL_OBSERVED" if obs == rev
                        else "DIVERGENT_REVISIONS_NEEDS_CONTENT_IDENTITY")
        elif rev:
            relation = "CANDIDATE_REVISION_ONLY_CANONICAL_EMPTY"
        elif obs:
            relation = "CANONICAL_REVISION_ONLY_CANDIDATE_EMPTY"
        else:
            relation = "BOTH_REVISION_FIELDS_MISSING"
        if relation == "DIVERGENT_REVISIONS_NEEDS_CONTENT_IDENTITY":
            require(row["repo_id"] == "nvidia/RFD4-Proteina", "Other revision conflict")
            require(r71["statistics"]["root_model_payload_identical_by_publisher_sha"]
                    is True, "RFD4 identity evidence vanished")
            relation = "RFD4_MAIN_WEIGHT_IDENTICAL_BY_LFS_SHA_SUPPORT_FILES_DIFFER"
        require(row["revision_relation"] == relation, f"Stale revision relation: {key}")
        candidate_sum += b
        classes[cclass] += 1
        relations[relation] += 1

    require(dict(classes) == r72["counts"]["by_source_evidence"], "Group counts drift")
    require(dict(relations) == r72["counts"]["revision_relations"], "Relation count drift")
    require(classes["V27_READINESS_PRIMARY_SCOPE"] == 126
            and classes["R64_PINNED_CANDIDATE_SOURCE"] == 8
            and classes["R48_ZONOS_KEEP2_PINNED_REFERENCE_NOT_MINIMAL"] == 1,
            "136? Wrong historical/candidate source coverage")
    require(relations["MATCHES_CANONICAL_OBSERVED"] == 96
            and relations["BOTH_REVISION_FIELDS_MISSING"] == 32
            and relations["CANDIDATE_REVISION_ONLY_CANONICAL_EMPTY"] == 6
            and relations["RFD4_MAIN_WEIGHT_IDENTICAL_BY_LFS_SHA_SUPPORT_FILES_DIFFER"] == 1,
            "Revision accounting wrong")
    require(sum(r["source_candidate_revision"] is not None for r in rows) == 103,
            "Source pinned coverage drift")
    require(candidate_sum == r72["capacity"]["sum_135_candidate_primary_source_bytes"]
            == 3457908837505, "Source candidate byte sum changed")
    require(v27cap["known_primary_file_bytes_sum"]
            == sum(x["selected_source_primary_bytes"] for x in v27["assets"])
            == r72["capacity"]["v27_126_primary_sum"], "v27 evidence sum changed")
    extras = [r for r in r64["repositories"] if
              ("model", r["repo_id"]) not in active and
              ("dataset", r["repo_id"]) not in active]
    require(len(extras) == 1 and extras[0]["repo_id"] == "ACE-Step/Ace-Step1.5",
            "External R64 dependency changed")
    require(extras[0]["selected_bytes"] == r72["capacity"]["r64_external_bytes"],
            "External dependency source bytes changed")

    # A publisher's mutable HEAD is NOT an immutable selected-file lock.
    current_heads = r73["records"]
    checked = set()
    for x in current_heads:
        key = (x["asset_kind"], x["repo_id"])
        require(key in active and key not in checked, "R73 duplicate or unknown")
        checked.add(key)
        parent = next(r for r in rows if (r["asset_kind"], r["repo_id"]) == key)
        require(parent["revision_relation"] == "BOTH_REVISION_FIELDS_MISSING",
                "R73 overwrote a historical pin")
        require(re.fullmatch("[0-9a-f]{40}", x["upstream_sha_at_check"]) is not None,
                "Invalid observed SHA")
        require(x["historical_source_candidate_bytes"] == parent["source_candidate_bytes"],
                "Historical byte record edited")
        require(x["source_bytes_verified_at_new_sha"] is False
                and x["revalidated_selected_file_manifest"] is False
                and x["download_approved"] is False, "Unjustified source promotion")
    require(len(checked) == r73["checked_total"] == 14, "R73 head count drift")
    require(r73["remaining_without_new_live_head_observation"] == 18,
            "Remaining source head count drift")
    print(json.dumps({
        "result": "PASS_RESEARCH_METADATA_ONLY",
        "v32_active": len(active),
        "v27_reused_source_candidates": 126,
        "r64_active_candidates": 8,
        "r48_zonos_reference_candidates": 1,
        "candidate_bytes_reported": candidate_sum,
        "source_candidate_revisions_known": 103,
        "publisher_head_only_rechecked": len(checked),
        "final_acquisition_approvals": 0,
        "offline_runtime_verified": False,
    }, indent=2))


if __name__ == "__main__":
    main()
