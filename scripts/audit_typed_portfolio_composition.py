#!/usr/bin/env python3
"""Read-only composition/receipt audit. No model loads, network or authorization."""
import argparse
from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path

ACTIVE = {"select", "conditional"}

def key(row):
    return row["asset_kind"], row["repo_id"]

def unique_keys(rows):
    keys = [key(row) for row in rows]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate typed identity")
    return set(keys)

def receipt_kind(row, by_id):
    # Legacy ledger has no asset_kind; infer ONLY a unique catalog identity.
    kinds = by_id.get(row["repo_id"], set())
    declared = row.get("asset_kind")
    if declared:
        return declared if declared in kinds else "unresolved"
    return next(iter(kinds)) if len(kinds) == 1 else "unresolved"

def audit(catalog, ledger, readiness, prep, proposed, access, approved):
    rows = catalog["items"]
    unique_keys(rows)
    active = [r for r in rows if r["portfolio_decision"] in ACTIVE]
    models = [r for r in active if r["asset_kind"] == "model"]
    active_keys = unique_keys(active)
    conditional_keys = unique_keys([r for r in active if r["portfolio_decision"] == "conditional"])
    for name, entries, target in (
        ("readiness", readiness["records"], active_keys),
        ("preparation", prep["items"], active_keys),
        ("proposed", proposed["candidates"], active_keys),
        ("access", access["entries"], conditional_keys),
    ):
        if unique_keys(entries) != target:
            raise ValueError(name + " identity mismatch")
    if approved["entries"] or proposed["approved"] or proposed["download_enabled"]:
        raise ValueError("approval boundary changed; manual review required")
    if any(r["download_approved"] or r["ready_to_acquire"] for r in readiness["records"]):
        raise ValueError("readiness authorization boundary changed")
    if any(r["download_approved"] for r in rows):
        raise ValueError("catalog authorization boundary changed")
    by_id = defaultdict(set)
    for row in rows:
        by_id[row["repo_id"]].add(row["asset_kind"])
    verified = [r for r in ledger["models"] if r["status"] == "VERIFIED"]
    breakdown = defaultdict(lambda: {"reports": 0, "source_bytes": 0, "files": 0})
    for row in verified:
        bucket = breakdown[receipt_kind(row, by_id)]
        bucket["reports"] += 1
        bucket["source_bytes"] += row["source_bytes"]
        bucket["files"] += row["files_verified"]
    summary = ledger["summary"]
    for metric, expected in (("reports", summary["models_verified"]), ("source_bytes", summary["bytes_verified_total"]), ("files", summary["files_verified_total"])):
        if sum(v[metric] for v in breakdown.values()) != expected:
            raise ValueError("ledger total mismatch: " + metric)
    hashes = [{f["sha256"] for f in r.get("weight_files_sha256", []) if f.get("sha256")} for r in verified]
    groups = Counter(r.get("group") or "UNCLASSIFIED" for r in models)
    legacy = [r for r in models if r.get("group") == "言語・高性能・Base"]
    params = Counter()
    for row in models:
        n = row["parameter_gate"].get("total_parameters")
        params["unknown" if n is None else "at_most_100M" if n <= 100_000_000 else "over_100M_to_3B" if n <= 3_000_000_000 else "over_3B"] += 1
    return {
        "catalog_revision": catalog["revision_id"],
        "tracked": len(rows), "active": len(active), "active_models": len(models),
        "active_datasets": len(active)-len(models),
        "decisions": dict(Counter(r["portfolio_decision"] for r in rows)),
        "exact_typed_sidecar_joins": {"readiness": len(active_keys), "preparation": len(active_keys), "proposed": len(active_keys), "access": len(conditional_keys)},
        "reported_verified_by_catalog_kind": dict(breakdown),
        "reported_verified_total": len(verified),
        "reported_held_total": sum(r["status"].startswith("HOLD") or r["status"] == "HELD" for r in ledger["models"]),
        "receipt_kind_is_catalog_match_not_owner_artifact_verification": True,
        "nonempty_reported_weight_hash_sets": sum(bool(s) for s in hashes),
        "exact_nonempty_hash_set_pairs": sum(bool(a) and a == b for a,b in combinations(hashes,2)),
        "partial_hash_overlap_pairs": sum(bool(a & b) and a != b for a,b in combinations(hashes,2)),
        "active_model_missing_group": groups["UNCLASSIFIED"],
        "legacy_language_base_group_count": len(legacy),
        "legacy_group_whole_repo_reference_bytes": sum(r["resource_screen"]["source_all_repo_bytes"] for r in legacy) if all(r["resource_screen"].get("source_all_repo_bytes") is not None for r in legacy) else None,
        "legacy_group_not_exhaustive_and_includes_specialists": True,
        "recorded_model_parameter_bands": dict(params),
        "both_explicit_quality_fields": sum(bool(r.get("quality_positive")) and bool(r.get("quality_negative")) for r in models),
        "explicit_incumbent_comparison_field": sum(bool(r.get("incumbent_comparison")) for r in models),
        "active_primary_selected_bytes_present": sum(r.get("selected_file_bytes") is not None for r in active),
        "active_final_lock_bytes_unknown": sum(r.get("final_selected_file_bytes") is None for r in readiness["records"]),
        "owner_disk_rehashed": False, "physical_savings_bytes": None, "ready_to_acquire": 0, "download_approved": 0,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    def load(path):
        return json.loads((args.root / path).read_text(encoding="utf-8"))
    current = load("catalog/CURRENT.json")
    report = audit(
        load(current["materialized_catalog_path"]),
        load("catalog/execution/2026-11-19-acquisition-ledger.json"),
        load(current["latest_active_readiness_audit"]["summary_path"]),
        load(current["insurance_preparation_worklist_path"]),
        load(current["priority_worklist_path"]),
        load(current["latest_conditional_access_audit"]["path"]),
        load("queues/approved.json"),
    )
    if report["catalog_revision"] != current["revision_id"]:
        raise ValueError("CURRENT revision mismatch")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
