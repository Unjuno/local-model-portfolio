#!/usr/bin/env python3
"""Offline, read-only v32 research blocker census validation.

Run from repository root:
    python3 scripts/validate_v32_acquisition_blockers.py

Does not fetch model weights, contact Hub, or modify files.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKLIST = ROOT / "catalog/research/2026-11-15-v32-active-acquisition-blockers.json"
CURRENT = ROOT / "catalog/CURRENT.json"

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> None:
    current = load(CURRENT)
    manifest = load(ROOT / current["materialized_catalog_path"])
    work = load(WORKLIST)
    assert current["revision_id"] == work["canonical_revision"], "Stale research worklist"
    assert work["source_catalog"] == current["materialized_catalog_path"], "Source mismatch"
    assert work["approved"] is False and work["download_enabled"] is False
    all_items = manifest["items"]
    assert len(all_items) == current["expected"]["tracked"]
    ids = [(x["asset_kind"], x["repo_id"]) for x in all_items]
    assert len(ids) == len(set(ids)), "Duplicate canonical ID"
    active = [x for x in all_items if x["portfolio_decision"] in ("select", "conditional")]
    assert len(active) == current["expected"]["active"]
    assert len(work["items"]) == len(active) == work["active_count"]
    actual = {(x["asset_kind"], x["repo_id"]): x for x in active}
    assert len({(x["asset_kind"], x["repo_id"]) for x in work["items"]}) == len(active)
    expected_counts = Counter()
    for row in work["items"]:
        key = (row["asset_kind"], row["repo_id"])
        assert key in actual, f"Unexpected worklist record {key}"
        source = actual[key]
        assert row["decision"] == source["portfolio_decision"]
        assert row["tier"] == source["risk_tier"]
        assert row["parameter_gate"] == source["parameter_gate"]["status"]
        blockers = []
        if source["parameter_gate"]["status"] == "UNVERIFIED_BLOCK_FINAL_LOCK":
            blockers.append("TOTAL_PARAMETERS_UNKNOWN")
        if source["parameter_gate"]["status"] == "OVER_150B_QUANT_REVIEW_REQUIRED":
            blockers.append("OVER_BASELINE_EXCEPTION_UNPROVEN")
        if source["selected_file_bytes"] is None:
            blockers.append("SELECTED_FILE_BYTES_UNKNOWN")
        if not source["fully_pinned_revision_sha"]:
            blockers.append("REVISION_NOT_PINNED")
        if not source["license_text_reviewed"]:
            blockers.append("LICENSE_TEXT_NOT_REVIEWED")
        if not source["dependencies_reviewed"]:
            blockers.append("DEPENDENCIES_NOT_REVIEWED")
        if not source["download_approved"]:
            blockers.append("ACQUISITION_NOT_APPROVED")
        assert row["blockers"] == blockers, f"Stale blocker flags: {key}"
        expected_counts.update(blockers)
    assert dict(expected_counts) == work["counts"], "Stale blocker totals"
    assert not any(x["download_approved"] for x in all_items), "Unauthorized approval"
    print(json.dumps({"result": "PASS", "revision": current["revision_id"],
                      "tracked": len(all_items), "active": len(active),
                      "blockers": dict(expected_counts)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
