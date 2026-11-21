#!/usr/bin/env python3
"""Read-only v38 source/rights/capacity audit. Python >=3.10, standard library.

Run from the Git repository (no GitHub API, weights, model imports, CI, downloads).
The result tests JSON research integrity, NOT actual owner HDD, permissions or model runtime.
"""
from __future__ import annotations
import json
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
ACTIVE={"select","conditional"}
RID="v38-20261115"
TRIAGE="catalog/research/2026-11-15-r88-v38-146-access-risk-and-capacity-triage.json"
ACCESS="catalog/access/2026-11-15-v38-conditional-hub-gates.json"
GATES="catalog/readiness/v38-2026-11-15-r86-all146-selection-gates.json"
SOURCE="manifests/drafts/v38-haru-praxis-original-selected-source.candidate.json"
EXPECTED_CLASSES={
 "A_VERIFY_USER_GATED_RIGHTS":20,
 "B_RESOLVE_ACCESS_CONFLICT":1,
 "C_RESTRICTIVE_OR_NONSTANDARD_USE_TERMS":8,
 "D_CUSTOM_SOURCE_LICENSE_REVIEW":27,
 "E_TRAINED_COMPONENTS_INCOMPLETE":2,
 "F_SOURCE_SCOPE_AND_RUNTIME_RECONCILIATION":88,
}
def load(relative:str):
    p=(ROOT/relative).resolve()
    if not p.is_relative_to(ROOT.resolve()):
        raise ValueError("unsafe path")
    return json.loads(p.read_text(encoding="utf-8"))
def key(x): return x["asset_kind"],x["repo_id"]
def unique_index(rows):
    result={key(r):r for r in rows}
    if len(result)!=len(rows):
        raise AssertionError("duplicate asset_kind/repo_id")
    return result

def verify()->dict:
    c=load("catalog/CURRENT.json")
    assert "catalog/revisions/v38-2026-11-15.json" in c["ordered_overlays"], "Missing historical v38"
    if c["revision_id"]==RID:
        assert c["latest_conditional_access_audit"]["path"]==ACCESS
    v=load("catalog/effective-portfolio-2026-11-15-v38.json")
    q=load("queues/proposed-v38-2026-11-15.json")
    p=load("catalog/preparation/2026-11-15-insurance-bundles-v38.json")
    a=load(ACCESS);r=load(GATES); t=load(TRIAGE);m=load(SOURCE)
    assert v["revision_id"]==RID
    all_items=unique_index(v["items"])
    active=unique_index([x for x in v["items"] if x["portfolio_decision"] in ACTIVE])
    cond={k:x for k,x in active.items() if x["portfolio_decision"]=="conditional"}
    assert len(all_items)==193
    assert len(active)==146 and len(cond)==93
    assert len([x for x in active.values() if x["asset_kind"]=="model"])==128
    assert len([x for x in active.values() if x["asset_kind"]=="dataset"])==18
    assert set(unique_index(q["candidates"]))==set(active)
    assert set(unique_index(p["items"]))==set(active)
    assert set(unique_index(r["records"]))==set(active)
    aud=unique_index(a["entries"])
    assert set(aud)==set(cond)
    assert a["source_revision"]==RID and len(aud)==93
    assert sum(x["hub_gated"] is True for x in a["entries"])==a["gated_count"]==20
    assert aud[("model","higurashi-ai/Haru-4B")]["hub_gated"] is False
    assert aud[("model","runwayml/praxis-1-droid")]["hub_gated"] is True
    assert all(x["owner_access_permission"]=="unknown" and x["download_authorized"] is False for x in a["entries"])
    tri=unique_index(t["records"])
    assert set(tri)==set(active) and len(tri)==146
    assert {row["research_order"] for row in tri.values()}==set(range(1,147))
    assert dict(Counter(x["investigation_class"] for x in tri.values()))==EXPECTED_CLASSES
    assert t["summary"]["select_records_without_conditional_access_sidecar"]==53
    assert t["summary"]["current_parameter_unknown_active"]==9
    assert r["summary"]["observed_gated_conditional"]==20
    assert r["summary"]["ready_to_approve"]==0
    assert t["summary"]["canonical_final_pinned_revision_missing"]==144
    assert t["summary"]["canonical_selected_bytes_missing"]==144
    refs=m["repositories"]
    assert len(refs)==3 and sum(len(x["files"]) for x in refs)==43
    assert sum(sum(f["bytes"] for f in x["files"]) for x in refs)==m["publisher_reference_bytes"]==69_536_354_285
    assert not m["executable"] and not m["download_authorized"] and m["owner_authorized_download_count"]==0
    assert m["wan_vae_not_recounted_in_logical_selection_bytes"] is True
    b=t["budget_stress"]
    assert b["source_only_v32_historical_bytes"]==3_466_070_232_173
    assert b["provisional_incremental_caps_v33_to_v36_bytes"]==94_520_000_000
    assert b["v38_new_originals_and_external_dependency_source_reference_bytes"]==69_536_354_285
    assert b["v38_new_80GB_reservation_cap_bytes"]==80_000_000_000
    assert b["nominal_plan_cap_bytes"]==3_640_590_232_173
    assert b["nominal_source_reference_bytes"]==3_630_126_586_458
    assert b["nominal_cap_scenario_after_floor_margin_bytes"]==(4_000_000_000_000-200_000_000_000-b["nominal_plan_cap_bytes"])==159_409_767_827
    assert b["nominal_source_scenario_after_floor_margin_bytes"]==(4_000_000_000_000-200_000_000_000-b["nominal_source_reference_bytes"])==169_873_413_542
    assert b["physical_disk_total_bytes"] is None and b["physical_free_bytes"] is None and b["complete_offline_archive_bytes"] is None
    assert b["storage_fit_verified"] is False
    assert not any(x["download_approved"] for x in all_items.values())
    assert not q["approved"] and not q["download_enabled"] and not p["download_enabled"]
    assert not a["download_authorized"] and not t["approved"] and not t["download_enabled"]
    assert load("queues/approved.json")["entries"]==[]
    return {"result":"PASS_METADATA_ONLY_NO_HDD_OR_PAYLOADS","revision":RID,"tracked":len(all_items),"active":len(active),"conditional_access":len(aud),"gated":20,"missing_final_source_locks":144,"budget_cap_scenario_margin_bytes":159_409_767_827,"download_authorized":False}
if __name__=="__main__":
    print(json.dumps(verify(),indent=2,ensure_ascii=False))
