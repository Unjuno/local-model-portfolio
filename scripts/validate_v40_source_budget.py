#!/usr/bin/env python3
"""V40 deterministic source-budget reconciliation, read-only and fail-closed.

Python >=3.10, standard library. No network, model downloads or execution.
This is *not* a measurement of the owner's disk or a finished archive.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_REVISION = "v40-20261115"
EVIDENCE = "catalog/estimates/2026-11-15-v40-r91-source-reservation-correction.json"
FIELDS = (
    ("v33-2026-11-15.json", "planning_reservation_cap_bytes"),
    ("v34-2026-11-15.json", "planning_cap_bytes"),
    ("v35-2026-11-15.json", "planning_reservation_cap_bytes"),
    ("v36-2026-11-15.json", "planning_reservation_cap_bytes"),
    ("v37-2026-11-15.json", None),
    ("v38-2026-11-15.json", "planning_reservation_cap_bytes"),
    ("v39-2026-11-15.json", "planned_new_budget_bytes"),
    ("v40-2026-11-15.json", "reservation_cap_not_actual_bytes"),
)

def load(path: str) -> dict:
    rel = Path(path)
    target = (ROOT / rel).resolve()
    if rel.is_absolute() or ".." in rel.parts or not target.is_relative_to(ROOT):
        raise ValueError("Unsafe path: " + path)
    return json.loads(target.read_text(encoding="utf-8"))

def validate() -> dict:
    c = load("catalog/CURRENT.json")
    est = load("catalog/estimates/CURRENT.json")
    ready = load("catalog/readiness/CURRENT.json")
    policy = load("policies/limits.json")
    ledger = load(EVIDENCE)
    portfolio = load("catalog/effective-portfolio-2026-11-15-v40.json")
    live = load(c["materialized_catalog_path"])
    assert "catalog/revisions/v40-2026-11-15.json" in c["ordered_overlays"], "Historical v40 overlay missing"
    assert portfolio["revision_id"] == EXPECTED_REVISION
    assert est["portfolio_revision"] == c["revision_id"] == ready["catalog_revision"]
    assert len(portfolio["items"]) == 195 and sum(
        x["portfolio_decision"] in ("select","conditional") for x in portfolio["items"]) == 148
    assert c["expected"]["tracked"] == len(live["items"])
    assert c["expected"]["active"] == sum(
        x["portfolio_decision"] in ("select","conditional") for x in live["items"])
    assert ready["tracked_assets"] == len(live["items"])
    assert ready["active_assets"] == c["expected"]["active"]
    assert policy["archive_target_bytes"] == ledger["math"]["archive_limit_bytes"] == 4_000_000_000_000
    assert policy["minimum_free_bytes"] == ledger["math"]["minimum_free_bytes"] == 200_000_000_000
    assert ledger["canonical_revision"] == EXPECTED_REVISION
    assert est["estimate_path"] == EVIDENCE
    assert "catalog/revisions/v40-2026-11-15.json" in c["ordered_overlays"]
    ids = {(x["asset_kind"], x["repo_id"]) for x in portfolio["items"]}
    assert len(ids) == 195, "Duplicate asset identity"
    assert not any(x["download_approved"] for x in portfolio["items"])
    active = [x for x in portfolio["items"] if x["portfolio_decision"] in ("select", "conditional")]
    assert len(active) == 148
    cap_total = 0
    for i, (basename, field) in enumerate(FIELDS):
        path = f"catalog/revisions/{basename}"
        r = load(path)
        assert path in c["ordered_overlays"], "Missing applied revision: " + path
        cap = r[field] if field is not None else 0
        assert isinstance(cap, int) and not isinstance(cap, bool) and cap >= 0
        assert cap == ledger["planning_incremental_revisions"][i]["planning_cap_bytes"]
        assert r["revision_id"] == ledger["planning_incremental_revisions"][i]["revision"]
        cap_total += cap
    assert cap_total == ledger["math"]["sum_post_v32_planning_reservations_bytes"] == 204_520_000_000
    v32 = load("catalog/estimates/2026-11-14-v32-runtime-contingency-r63.json")
    base = v32["capacity_bytes"]["prior_R62"]
    assert base == ledger["source_baseline_bytes"] == 3_466_070_232_173
    total = base + cap_total
    margin = policy["archive_target_bytes"] - policy["minimum_free_bytes"] - total
    assert total == ledger["math"]["nominal_plan_total_bytes"] == 3_670_590_232_173
    assert margin == ledger["math"]["nominal_plan_margin_after_minimum_free_bytes"] == 129_409_767_827
    assert margin > 0, "Even the incomplete planning proxy would exceed the declared limit"

    rev38 = load("catalog/revisions/v38-2026-11-15.json")
    rev39 = load("catalog/revisions/v39-2026-11-15.json")
    rev40 = load("catalog/revisions/v40-2026-11-15.json")
    comp = ledger["math"]["nominal_model_only_source_components"]
    assert comp["v32_historical_source_only_reference_bytes"] == base
    assert comp["v33_through_v36_mixed_planning_caps_bytes"] == sum(
        ledger["planning_incremental_revisions"][i]["planning_cap_bytes"] for i in range(4))
    assert comp["v38_publisher_model_plus_qwen_source_reference_bytes"] == (
        rev38["new_model_original_source_bytes"] + rev38["external_qwen_source_dependency_bytes"])
    assert comp["v39_publisher_model_plus_vq_source_reference_bytes"] == rev39["publisher_source_references_bytes"]
    assert comp["v40_publisher_selected_groundingpi_scope_bytes"] == rev40["publisher_candidate_bytes"]
    source_total = sum(comp.values())
    assert source_total == ledger["math"]["nominal_mixed_source_scenario_total_bytes"] == 3_651_822_129_270
    assert policy["archive_target_bytes"] - policy["minimum_free_bytes"] - source_total == 148_177_870_730

    assert est["physical_HDD_capacity_verified"] is False
    assert est["external_runtime_dependency_closure_complete"] is False
    assert ready["owner_HDD_verified"] is False and ready["download_approved"] is False
    assert ledger["math"]["full_archive_real_bytes"] is None
    assert ledger["math"]["physical_owner_disk_free_bytes"] is None
    assert ledger["risk_status"]["download_approved"] is False
    return {
        "result": "PASS_DETERMINISTIC_SOURCE_BUDGET_NOT_ARCHIVE_APPROVAL",
        "revision": EXPECTED_REVISION,
        "tracked": len(ids),
        "active": len(active),
        "revision_cap_total_bytes": cap_total,
        "nominal_total_bytes": total,
        "nominal_after_floor_margin_bytes": margin,
        "real_disk_measured": False,
        "download_authorized": False,
        "full_offline_dependencies_verified": False,
    }

if __name__ == "__main__":
    print(json.dumps(validate(), ensure_ascii=False, indent=2))
