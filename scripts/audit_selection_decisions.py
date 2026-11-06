#!/usr/bin/env python3
"""Audit current v19 selection and historic v17 evidence without downloading weights.

Python >=3.10; standard library only. Read-only.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
STATES={"select","conditional","hold","deferred","excluded","research_only"}
GRADES={"A","B","C","U"}
PROVIDERS={"huggingface","civitai"}

def load(root: Path, path: str):
    target=(root/path).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError("path escapes repository")
    return json.loads(target.read_text(encoding="utf-8"))

def is_url(value):
    if not isinstance(value,str): return False
    parsed=urlparse(value)
    return parsed.scheme=="https" and bool(parsed.netloc)

def check_record(row:dict, ids:set[str])->list[str]:
    errors=[]
    key=row.get("key","<missing>")
    if row.get("provider") not in PROVIDERS: errors.append(f"{key}: invalid provider")
    if row.get("portfolio_decision") not in STATES: errors.append(f"{key}: invalid decision")
    if row.get("evidence_grade") not in GRADES: errors.append(f"{key}: invalid grade")
    if not isinstance(row.get("quality_positive"),str) or not row["quality_positive"].strip(): errors.append(f"{key}: missing positive evidence")
    if not isinstance(row.get("quality_negative"),str) or not row["quality_negative"].strip(): errors.append(f"{key}: missing negative evidence")
    if not is_url(row.get("publisher_url")): errors.append(f"{key}: invalid primary url")
    for url_field in ("quality_url","download_page"):
        if url_field in row and not is_url(row[url_field]): errors.append(f"{key}: invalid {url_field}")
    if row.get("download_authorized") is not False: errors.append(f"{key}: research record cannot grant download")
    if row.get("license_text_reviewed") is not False: errors.append(f"{key}: unreviewed license marked reviewed")
    if row.get("source_revision_sha") is not None or row.get("selected_file_sha256_complete") is not False: errors.append(f"{key}: fabricated pin/file verification")
    if row.get("in_portfolio") is True:
        if row.get("provider")!="huggingface": errors.append(f"{key}: non-HF portfolio ID requires dedicated source schema")
        if row.get("model_id") not in ids: errors.append(f"{key}: missing portfolio model")
        if row.get("portfolio_decision")=="research_only": errors.append(f"{key}: tracked model cannot be research_only")
    elif row.get("in_portfolio") is False:
        if row.get("portfolio_decision")!="research_only": errors.append(f"{key}: untracked candidate must be research_only")
    else: errors.append(f"{key}: in_portfolio not boolean")
    if row.get("provider")=="civitai":
        if not isinstance(row.get("model_id"),int) or not isinstance(row.get("model_version_id"),int):
            errors.append(f"{key}: Civitai requires numeric model/version")
        if row.get("in_portfolio") is True: errors.append(f"{key}: Civitai mirrored as HF")
    return errors

def audit(root:Path=ROOT)->list[str]:
    errors=[]
    current=load(root,"catalog/CURRENT.json")
    if current.get("revision_id") not in ("v19-20261106", "v20-20261106", "v21-20261106", "v22-20261106", "v23-20261106", "v24-20261106", "v25-20261106"): return ["unexpected CURRENT revision"]
    if current.get("decision_method_path")!="policies/selection-decision-v17.json": return ["decision policy not current"]
    model=load(root,current["materialized_catalog_path"])
    if model.get("revision_id")!=current["revision_id"]: errors.append("view revision differs from current")
    items=model.get("items")
    if not isinstance(items,list): return errors+["invalid items"]
    known={x.get("repo_id"):x for x in items if isinstance(x,dict) and x.get("asset_kind")=="model"}
    active=[x for x in items if x.get("portfolio_decision") in ("select","conditional")]
    if len(items)!=current.get("expected",{}).get("tracked") or len(active)!=current.get("expected",{}).get("active"): errors.append("current tracked/active count mismatch")
    dossier=load(root,current["decision_research_path"])
    if dossier.get("source_revision")!="v17-20261104": errors.append("dossier revision mismatch")
    rules=load(root,current["decision_method_path"])
    if rules.get("policy_id")!=dossier.get("policy_id"): errors.append("policy id mismatch")
    if rules.get("hard_boundaries",{}).get("never_auto_download_or_seed") is not True: errors.append("auto-download protection absent")
    if rules.get("hard_boundaries",{}).get("unknown_total_blocks_final_lock") is not True: errors.append("unknown-total protection absent")
    rows=dossier.get("evidence_rows")
    if not isinstance(rows,list) or len(rows)!=5: return errors+["expected 5 research records"]
    if len({r.get("key") for r in rows})!=len(rows): errors.append("duplicate candidate key")
    for row in rows:
        errors+=check_record(row,set(known))
        if row.get("in_portfolio"):
            model_record=known.get(row.get("model_id"))
            if model_record and model_record.get("portfolio_decision")!=row.get("portfolio_decision"): errors.append(f"{row.get('key')}: decision mismatch")
            if row.get("portfolio_decision") in ("select","conditional") and model_record and model_record.get("parameter_gate",{}).get("status")!="PASS_TOTAL_PARAMS_LT_150B" and not model_record.get("research_only_unknown_total_allow_conditional"): errors.append(f"{row.get('key')}: active unknown total")
    for x in active:
        if x.get("asset_kind")=="model" and x.get("parameter_gate",{}).get("status") not in ("PASS_TOTAL_PARAMS_LT_150B","OVER_150B_QUANT_RUNTIME_VERIFIED") and not (x.get("portfolio_decision")=="conditional" and x.get("research_only_unknown_total_allow_conditional") is True and x.get("parameter_gate",{}).get("status")=="UNVERIFIED_BLOCK_FINAL_LOCK" and x.get("download_approved") is False): errors.append(f"{x.get('repo_id')}: unverified active gate")
    q=load(root,current["priority_worklist_path"])
    a={(x["asset_kind"],x["repo_id"]) for x in active}
    b={(x["asset_kind"],x["repo_id"]) for x in q.get("candidates",[])}
    if a!=b or len(q.get("candidates",[]))!=len(active): errors.append("active queue ids differ")
    if q.get("approved") is not False or q.get("download_enabled") is not False: errors.append("queue executable")
    for candidate in q.get("candidates",[]):
        item=known.get(candidate.get("repo_id"))
        if item and item.get("parameter_gate",{}).get("status")=="UNVERIFIED_BLOCK_FINAL_LOCK":
            if candidate.get("research_only") is not True or candidate.get("can_enter_approved_queue") is not False or candidate.get("download_approved") is not False:
                errors.append("unknown-total conditional candidate not blocked: "+candidate.get("repo_id","missing"))
    rights=load(root,"policies/personal-research-rights-v17.json")
    if rights.get("downloads_approved")!=0 or rights.get("seed_approved") is not False:
        errors.append("rights policy accidentally authorizes payload")
    return errors

if __name__=="__main__":
    errors=audit()
    if errors:
        print("FAIL current selection and v17 evidence audit")
        for err in errors: print(" -",err)
        raise SystemExit(1)
    print("PASS current selection, historic v17 evidence, and non-executable queue")
