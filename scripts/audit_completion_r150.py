#!/usr/bin/env python3
"""Read-only R150 completeness map for the latest immutable portfolio.

Input: canonical CURRENT, active readiness and the reported acquisition ledger.
Output: machine-readable all-asset status, WITHOUT downloads or ownership claims.
The ledger's VERIFIED is a tool receipt, not an owner-drive independent rehash.
"""
from __future__ import annotations
from collections import Counter
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ("select", "conditional")


def load(root: Path, relative: str):
    p = (root / relative).resolve()
    if not p.is_relative_to(root.resolve()):
        raise ValueError("unsafe repository path")
    return json.loads(p.read_text(encoding="utf-8"))


def build(root: Path = ROOT) -> dict:
    c = load(root, "catalog/CURRENT.json")
    view = load(root, c["materialized_catalog_path"])
    ledger = load(root, "catalog/execution/2026-11-19-acquisition-ledger.json")
    ready = load(root, c["latest_active_readiness_audit"]["summary_path"])
    access = load(root, c["latest_conditional_access_audit"]["path"])
    approved = load(root, "queues/approved.json")
    revdiff = load(root, "catalog/research/2026-11-22-r148-ledger99-immutable-revision-drift.json")
    rfd4 = load(root, "catalog/research/2026-11-22-r150-rfd4-core-weight-same-auxiliary-diff.json")
    if len(view["items"]) != c["expected"]["tracked"] or view["revision_id"] != c["revision_id"]:
        raise ValueError("canonical tracked/revision mismatch")
    if approved.get("entries") != []:
        raise ValueError("explicit user-approved queue is not empty; stop and review")
    if ready.get("summary", {}).get("ready_to_approve") != 0:
        raise ValueError("unexpected ready-to-approve status in catalogue")
    acquired = {}
    for model in ledger["models"]:
        if model["repo_id"] in acquired:
            raise ValueError("duplicate reported acquisition repo id: " + model["repo_id"])
        acquired[model["repo_id"]] = model
    sidecars = {(x["asset_kind"], x["repo_id"]):x for x in ready["records"]}
    if len(sidecars) != len(ready["records"]):
        raise ValueError("duplicate readiness identity")
    active = [x for x in view["items"] if x["portfolio_decision"] in ACTIVE]
    if len(active) != c["expected"]["active"]:
        raise ValueError("canonical active count mismatch")
    if len(sidecars) != len(active):
        raise ValueError("readiness active count mismatch")
    if {(x["asset_kind"],x["repo_id"]) for x in active} != set(sidecars):
        raise ValueError("missing active readiness identity")
    if len(access["entries"]) != c["expected"]["by_decision"]["conditional"]:
        raise ValueError("conditional access scope mismatch")
    if len({(x["asset_kind"],x["repo_id"]) for x in view["items"]}) != len(view["items"]):
        raise ValueError("duplicate canonical identity")
    extra = set(acquired) - {x["repo_id"] for x in view["items"]}
    if extra:
        raise ValueError("reported acquired repositories unrepresented: "+repr(sorted(extra)))

    changed = {x["repo_id"]:x for x in revdiff["revision_comparisons"]}
    rows=[]
    for x in view["items"]:
        rid, kind = x["repo_id"],x["asset_kind"]
        rep=acquired.get(rid)
        rr=sidecars.get((kind,rid))
        status = rep["status"] if rep else "NO_ACQUISITION_REPORT_FOR_REPO"
        observation = str(x.get("upstream_revision_sha_observed") or "")
        variant = ("NO_REPORTED_ACQUISITION" if not rep else
                   "RECEIPT_REVISION_SAME_AS_CATALOG_OBSERVED" if observation and observation == rep["revision_sha"] else
                   "RFD4_MAIN_ROOT_WEIGHT_SAME_AUXILIARY_VARIANT_DIFFERENT"
                       if rid=="nvidia/RFD4-Proteina" else
                   "PUBLISHER_WEIGHT_IDENTICAL_BUT_RUNTIME_METADATA_MAY_DIFFER"
                       if rid in changed and changed[rid]["status"]=="WEIGHTS_IDENTICAL_METADATA_OR_CONFIG_ONLY" else
                   "RECEIPT_REVISION_DIFFERENCE_NOT_FULLY_RECONCILED"
                       if observation else "NO_HISTORIC_40HEX_REVISION_CATALOG_OBSERVATION")
        if rep and rr is None and x["portfolio_decision"] in ACTIVE:
            raise ValueError("missing readiness for acquired active id")
        rows.append({
            "asset_kind":kind,"repo_id":rid,"decision":x["portfolio_decision"],
            "active":x["portfolio_decision"] in ACTIVE,
            "risk_tier":x.get("risk_tier"),
            "regulatory_forecast_scenario_not_probability":(x.get("forecast_priority") or {}).get("wave"),
            "parameter_gate":(x.get("parameter_gate") or {}).get("status"),
            "publisher_revision_observed":observation or None,
            "reported_receipt_status":status,
            "reported_receipt_revision":rep.get("revision_sha") if rep else None,
            "reported_verified_files":rep.get("files_verified") if rep and rep.get("status")=="VERIFIED" else None,
            "reported_verified_source_bytes":rep.get("source_bytes") if rep and rep.get("status")=="VERIFIED" else None,
            "acquired_identity_relation":variant,
            "readiness_status": "BLOCKED_AND_UNAPPROVED" if rr else "INACTIVE_NOT_IN_ACTIVE_READINESS",
            "owner_HDD_full_SHA_independently_reverified_in_this_study":False,
            "complete_offline_inference_or_training_restore_verified_in_this_study":False,
            "owner_license_per_act_verified_in_this_study":False,
            "new_transfer_authorized":False,
            "next_step":"NO_REDOWNLOAD; OWNER_LOCAL_HASH_AND_DEPENDENCY_RESTORE" if rep and rep.get("status")=="VERIFIED" else
                        "GATED_OR_PRIVATE_USER_ENTITLEMENT_HOLD" if rep else
                        "SOURCE_SELECTION_RIGHTS_AND_PRESENT_OWNER_DISK_EXISTENCE_CHECK_BEFORE_ANY_TRANSFER"
        })
    cnt=Counter(x["reported_receipt_status"] for x in rows)
    active_cnt=Counter(x["reported_receipt_status"] for x in rows if x["active"])
    if cnt.get("VERIFIED")!=ledger["summary"]["models_verified"]:
        raise ValueError("VERIFIED count does not match source ledger")
    if cnt.get("HOLD_GATED_OR_PRIVATE")!=ledger["summary"]["models_held"]:
        raise ValueError("HOLD count does not match source ledger")
    if not rfd4["core_identity"]["old_and_acquired_equal"]:
        raise ValueError("RFD4 core cannot be treated identical")
    return {
        "schema_version":1,
        "kind":"R150_ALL_235_ASSET_SOURCE_REPORT_AND_OFFLINE_RESTORE_COMPLETENESS_MAP",
        "observed_jst":"2026-11-22",
        "catalog_revision":c["revision_id"],
        "source_canonical_current":"catalog/CURRENT.json",
        "source_ledger":"catalog/execution/2026-11-19-acquisition-ledger.json",
        "source_rfd4_core_check":"catalog/research/2026-11-22-r150-rfd4-core-weight-same-auxiliary-diff.json",
        "registered_assets":len(rows),
        "active_assets":len(active),
        "registered_models":c["expected"]["models"],
        "registered_datasets":c["expected"]["datasets"],
        "decisions":c["expected"]["by_decision"],
        "reported_ledger":{
            "verified_repos":ledger["summary"]["models_verified"],
            "verified_file_refs":ledger["summary"]["files_verified_total"],
            "verified_bytes":ledger["summary"]["bytes_verified_total"],
            "held_gated_repos":ledger["summary"]["models_held"],
            "historical_minimum_free_bytes_reported":ledger["summary"]["minimum_free_bytes_observed"],
            "not_independently_rehashed_at_owner_current_drive":True,
        },
        "source_receipt_status_counts":dict(cnt),
        "active_source_receipt_status_counts":dict(active_cnt),
        "active_unknown_total_parameter_count":ready["summary"]["unknown_total_active"],
        "active_conditional_gated_count":access["gated_count"],
        "active_ready_for_new_acquisition":ready["summary"]["ready_to_approve"],
        "recorded_explicit_download_approvals":len(approved["entries"]),
        "number_of_independently_verified_owner_offline_restores_this_study":0,
        "not_reported_acquired_does_not_mean_absent_from_user_disk":True,
        "all_represented_reported_verified_ids":True,
        "rfd4_central_root_same_while_auxiliary_differs":True,
        "next_priority":"Known acquired checksum/reconstruction > selected-only source/rights closure; RFD4 core no retransfer, others conditional",
        "assets":rows
    }


if __name__ == "__main__":
    result=build()
    print(json.dumps(result,ensure_ascii=False,indent=2))
