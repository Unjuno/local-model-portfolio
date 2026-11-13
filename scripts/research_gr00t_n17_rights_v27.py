#!/usr/bin/env python3
"""Research-only GR00T N1.7 source, 2026-11-05 publisher license conflict.

All model weights are represented by anonymous Hugging Face metadata only.
Reads only small pinned text, GitHub README and public issue JSON.
Never downloads weights, opens user disks or touches the approved queue.
"""
from __future__ import annotations
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import urllib.request

from scripts.capacity_inventory import snapshot, dump, exact_sum
from scripts import capacity_selection as cap

ROOT=Path(__file__).resolve().parents[1]
OUT=Path("catalog/research/2026-11-07-gr00t-n17-rights")
SRC=OUT/"sources"
N17="nvidia/GR00T-N1.7-3B"
COSMOS="nvidia/Cosmos-Reason2-2B"
N16="nvidia/GR00T-N1.6-3B"
N16_REPO=Path("catalog/capacity/2026-11-06/sources/model--nvidia--GR00T-N1.6-3B.json")
CODE_REPO="NVIDIA/Isaac-GR00T"
CODE_SHA="7b304f95b95790490b79bd263ba57015c3c12dfd"
N16_CODE_SHA="9b37aa1ce69c73c6d165233fa88128283bba4508"
ISSUE_NUMBER=803
MAX_TEXT=260_000

def need(value,msg):
    if not value:raise ValueError(msg)

def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def read_https_bounded(url,allow_prefix):
    need(url.startswith(allow_prefix) and "resolve/" not in url and "git/blobs" not in url,
         "unexpected or model-payload URL")
    req=urllib.request.Request(url,headers={
      "Accept":"application/vnd.github+json" if "api.github.com" in url else "text/plain",
      "User-Agent":"local-model-portfolio-GR00T-rights-archive"})
    if "api.github.com" in url and (token:=os.environ.get("GITHUB_TOKEN")):
        req.add_header("Authorization","Bearer "+token)
    with urllib.request.urlopen(req,timeout=25) as r:
        data=r.read(MAX_TEXT+1)
    need(len(data)<=MAX_TEXT,"text API body too large")
    return data

def github_get(path):
    u=f"https://api.github.com/repos/{CODE_REPO}/{path}"
    return json.loads(read_https_bounded(u,f"https://api.github.com/repos/{CODE_REPO}/"))

def source_text_evidence(src,path):
    repo=src["repo_id"];rev=src["pinned_revision"]
    need(repo==N17 and re.fullmatch("[0-9a-f]{40}",rev),"foreign/unpinned text")
    need(path in ("LICENSE","README.md","config.json","model.safetensors.index.json"),
         "unrecognized document")
    names={f["path"] for f in src["files"]}
    need(path in names,"missing document "+path)
    raw=read_https_bounded(
         f"https://huggingface.co/{repo}/raw/{rev}/{path}",
         f"https://huggingface.co/{repo}/raw/{rev}/")
    need(len(raw)==next(f["bytes"] for f in src["files"] if f["path"]==path),
         "pinned text size mismatch")
    return {"path":path,"immutable_revision":rev,
        "sha256":hashlib.sha256(raw).hexdigest(),
        "bytes":len(raw),"text":raw.decode("utf-8")}

def code_readme():
    ob=github_get(f"contents/README.md?ref={CODE_SHA}")
    need(ob.get("encoding")=="base64" and ob.get("type")=="file",
         "GitHub code README absent")
    raw=base64.b64decode(ob["content"])
    need(len(raw)==ob["size"] and len(raw)<MAX_TEXT,"GitHub README size mismatch")
    return {"revision":CODE_SHA,"sha256":hashlib.sha256(raw).hexdigest(),
        "bytes":len(raw),"text":raw.decode("utf-8")}

def issue_record():
    p=github_get(f"issues/{ISSUE_NUMBER}")
    need(p.get("number")==ISSUE_NUMBER and "licen" in p.get("title","").lower(),
         "wrong issue")
    return {"source":"https://github.com/NVIDIA/Isaac-GR00T/issues/803",
       "number":ISSUE_NUMBER,"state":p["state"],"created_at":p["created_at"],
       "updated_at":p["updated_at"],"closed_at":p.get("closed_at"),
       "issue_author_is_not_licensor":True,"issue_not_an_approval":True,
       "publisher_definitive_resolution_verified":False}

def classify_license(license_text,model_readme,code_readme_text):
    txt=" ".join(license_text.lower().split())
    need("nvidia license" in txt[:250].lower(),"different LICENSE identity")
    need("3.3 use limitation" in txt and "only may be used" in txt and
         "non-commercially" in txt and "research or evaluation purposes only" in txt,
         "license commercial restriction not established")
    need("nvidia open model license" in model_readme.lower(),
         "no model-card NVIDIA open license statement")
    need(bool(re.search(r"\*\*Model weights:\*\*\s*\[NVIDIA Open Model License\]",code_readme_text,re.I)),
         "GitHub declared model weights license changed")
    need(bool(re.search(r"\*\*Code:\*\*\s*Apache 2\.0",code_readme_text,re.I)),
         "code and weights licensing distinction changed")
    need("fully commercially licensable under apache 2.0" in code_readme_text.lower(),
         "commercial claim changed")
    return {"fixed_HF_license_title":"NVIDIA License",
       "HF_license_section_3_3_noncommercial_research_evaluation_only":True,
       "HF_card_claims_NVIDIA_open_model_license":True,
       "official_source_claims_weight_NVIDIA_open_model_license":True,
       "official_source_claims_code_Apache2":True,
       "official_source_has_additional_Apache_commercial_claim":True,
       "contradictory_first_party_artifacts":True,
       "legal_interpretation":"UNCERTAIN_RESOLVE_WITH_PUBLISHER; plan under most restrictive confirmed wording until corrected",
       "commercial_permission_verified":False,
       "redistribution_permission_for_target_use_verified":False,
       "download_approval_allowed":False}

def weights_and_config(src):
    need(src["asset_kind"]=="model" and src["repo_id"]==N17,"wrong model repo")
    need(src["tree_complete"] and src.get("gated") is False,"GR00T N1.7 public tree absent")
    need(src.get("payload_bytes_downloaded")==0 and src.get("download_authorized") is False,
         "model payload acquisition not authorized")
    need(bool(re.fullmatch("[0-9a-f]{40}",src["pinned_revision"])), "no immutable SHA")
    files=src["files"];paths={f["path"] for f in files}
    need(len(paths)==len(files),"duplicate HF paths")
    need(src["source_scope_bytes"]==exact_sum(f["bytes"] for f in files),
         "publisher source bytes mismatch")
    weights=[f for f in files if f["path"].endswith(".safetensors")]
    need(weights and all(f["bytes"]>0 for f in weights),"missing original weights")
    need({"LICENSE","README.md","config.json","processor_config.json","statistics.json"}.issubset(paths),
         "missing license or embodiment/processor metadata")
    docs={d["path"]:d for d in src.get("documentation",[])
          if isinstance(d.get("json"),dict)}
    need("config.json" in docs,"missing pinned config JSON")
    cfg=docs["config.json"]["json"]
    need(cfg.get("model_type")=="Gr00tN1d7" or "Gr00tN1d7" in cfg.get("architectures",[]),
         "wrong architecture")
    if "model.safetensors.index.json" in paths:
        need("model.safetensors.index.json" in docs,"missing model index")
        mapped=set(docs["model.safetensors.index.json"]["json"]["weight_map"].values())
        need(mapped=={x["path"] for x in weights},"shard index mismatch")
    else:
        need(len(weights)==1,"unindexed weights incomplete")
    chosen=[f for f in files if "/" not in f["path"] and f["path"]!=".gitattributes"]
    need(all(f["bytes"] is not None for f in chosen),"unknown selected byte")
    chosen_b=exact_sum(f["bytes"] for f in chosen)
    return {"repo_id":N17,"revision":src["pinned_revision"],
       "source_repository_bytes":src["source_scope_bytes"],
       "complete_source_repo_tree":True,
       "recommended_original_file_scope_bytes":chosen_b,
       "recommended_selected_files":chosen,
       "original_weight_file_count":len(weights),
       "original_weight_bytes":exact_sum(f["bytes"] for f in weights),
       "selected_file_count":len(chosen),
       "published_model_safetensors_total":(src.get("parameter_metadata") or {}).get("total"),
       "parameter_magnitude_under_150B":(
             (src.get("parameter_metadata") or {}).get("total") or 10**12)<150_000_000_000,
       "model_config_observed":{x:cfg.get(x) for x in (
              "model_name","model_type","backbone_model_type","select_layer",
              "action_horizon","max_action_dim","max_state_dim","transformers_version",
              "model_dtype","load_bf16","use_relative_action")},
       "complete_model_embedded_backbone_verified":False,
       "dependent_backbone_already_embedded_dedup_unverified":True,
       "source_identity_and_bytes_not_local_hash":True,
       "owner_ram_gpu_peak_bytes":None,"owner_approval":False}

def budget(v27,n17):
    need(v27["source_revision"]=="v27-20261107" and len(v27["items"])==126,
         "wrong baseline")
    need(v27["known_scope_content_union_bytes"]==3_417_685_712_585,
         "baseline logical size changed")
    entries=[(r["repo_id"]+"@"+r["source_revision"],f) for r in v27["items"] for f in r["files"]]
    entries.extend((d["repo_id"]+"@"+d["revision"],f) for d in v27["dependencies"] for f in d["files"])
    need(cap.union_bytes(entries)==v27["known_scope_content_union_bytes"],
         "baseline hash-aware union mismatch")
    added=[(N17+"@"+n17["revision"],f) for f in n17["recommended_selected_files"]]
    union=cap.union_bytes(entries+added)
    delta=union-v27["known_scope_content_union_bytes"]
    need(0<=delta<=n17["recommended_original_file_scope_bytes"],"invalid union")
    return {"baseline_v27_logical_bytes":v27["known_scope_content_union_bytes"],
       "N17_original_source_files_gross_bytes":n17["recommended_original_file_scope_bytes"],
       "N17_hash_identity_aware_logical_increment_bytes":delta,
       "research_hold_scenario_logical_bytes":union,
       "scenario_within_nominal_4TB_target":union<4_000_000_000_000,
       "capacity_difference_is_not_owner_free_disk_bytes":4_000_000_000_000-union,
       "selected_model_scope_is_not_approved":True,
       "dependent_gated_backbone_not_double_counted_or_verified":True,
       "fully_restorable_archive_bytes":None,
       "owner_disk_free_bytes":None,
       "acquisition_peak_bytes":None,"model_payloads_downloaded":0}

def main():
    current=load("catalog/CURRENT.json")
    need(current["revision_id"]=="v27-20261107" and
         current["expected"]["tracked"]==173 and current["expected"]["active"]==126,
         "catalog unexpectedly changed")
    need(load("queues/approved.json")["entries"]==[],"downloads already approved")
    view=load(current["materialized_catalog_path"])
    need(N17 not in {x["repo_id"] for x in view["items"]},"N1.7 already formally selected")
    old=load(N16_REPO)
    need(old["repo_id"]==N16 and old["pinned_revision"]==
         "d0814e7ecb19202e7c8468b46098b0b7ef3a6d61","N1.6 parent baseline changed")
    need(old["source_scope_bytes"]==6_573_788_038,"N1.6 source size changed")
    oldconfig=next(d["json"] for d in old["documentation"] if d.get("path")=="config.json")
    need(oldconfig["model_type"]=="Gr00tN1d6" and oldconfig["model_name"]==
         "nvidia/Eagle-Block2A-2B-v2","prior Eagle backbone assumption changed")
    first=snapshot({"asset_kind":"model","repo_id":N17,"portfolio_decision":"research_hold"})
    dump(ROOT/SRC/(N17.replace("/","--")+".json"),first)
    need(not first.get("error"),"N17 source snapshot failed: "+str(first.get("error")))
    n17=weights_and_config(first)
    cosine=snapshot({"asset_kind":"model","repo_id":COSMOS,"portfolio_decision":"potential_external_gated_backbone"})
    dump(ROOT/SRC/(COSMOS.replace("/","--")+".json"),cosine)
    need(not cosine.get("error"),"gated Cosmos snapshot metadata unavailable: "+str(cosine.get("error")))
    license_text=source_text_evidence(first,"LICENSE")
    hf_card=source_text_evidence(first,"README.md")
    github=code_readme()
    issue=issue_record()
    contradictory=classify_license(license_text["text"],hf_card["text"],github["text"])
    need(issue["state"]=="open","issue resolved: review new rights before continuing")
    cp=budget(load("catalog/capacity/2026-11-07/v27/selected-file-capacity.json"),n17)
    facts={"schema_version":1,"observation_utc":datetime.now(timezone.utc).isoformat(),
       "baseline_revision":"v27-20261107","current_tracked":173,"current_active":126,
       "candidate":n17,
       "source_code":{"repo":CODE_REPO,"sha":CODE_SHA,"n1d6_code_branch_revision":N16_CODE_SHA,
             "n1d7_runtime_verified":False,"n1d6_and_n1d7_code_abi_different":True},
       "source_license_texts":{
           "HF_MODEL_LICENSE":{"sha256":license_text["sha256"],"bytes":license_text["bytes"],
                "url":f"https://huggingface.co/{N17}/blob/{n17['revision']}/LICENSE"},
           "HF_MODEL_README":{"sha256":hf_card["sha256"],"bytes":hf_card["bytes"]},
           "NVIDIA_GITHUB_README":{"sha256":github["sha256"],"bytes":github["bytes"]}},
       "rights_conflict":contradictory,"license_issue":issue,
       "predecessor":{"repo_id":N16,"revision":old["pinned_revision"],
           "source_repo_bytes":old["source_scope_bytes"],
           "pretrained_VLM_reference_from_config":"nvidia/Eagle-Block2A-2B-v2",
           "external_backbone_weight_required_for_runtime_confirmed":False},
       "successor":{"repo_id":N17,"publisher_train_data_claim":
          "20k hours EgoScale egocentric human video, relative end-effector controls, GR00T N1d7 action representation",
          "code_verifiable_justifications":["new Cosmos-Reason2-2B Qwen3VL backbone",
                 "different 132D action/state and extended horizon in N1d7 source",
                 "separate action policy training outcomes"],
          "independent_robothardware_quality_validation":False,
          "official_benchmark_reported_but_not_reproduced":True,
          "original_release_not_new_on_Nov7_2026":True},
       "potential_external_backbone":{"repo_id":COSMOS,"revision":cosine["pinned_revision"],
           "gated":cosine.get("gated"),"license_metadata":cosine.get("license_metadata"),
           "source_repo_bytes":cosine.get("source_scope_bytes"),
           "source_tree_complete":cosine.get("tree_complete"),
           "required_separate_runtime_weight_download_verified":False,
           "do_not_double_count_as_mandatory_before_model_init_static_review":True},
       "capacity":cp,
       "decision":"RESEARCH_HOLD_RIGHTS_CONFLICT_AND_BACKBONE_CLOSURE",
       "new_models_selected":0,"new_models_removed":0,
       "new_download_authorizations":0,"model_payloads_downloaded":0,
       "owner_disk_measured":False,
       "source_urls":[f"https://huggingface.co/{N17}",
         "https://github.com/NVIDIA/Isaac-GR00T/issues/803",
         f"https://github.com/NVIDIA/Isaac-GR00T/tree/{CODE_SHA}",
         f"https://huggingface.co/{COSMOS}"],
       "next_action":["Ask NVIDIA to reconcile the conflicting immutable LICENSE file and claimed open model terms",
           "inspect N1d7 original tensor index to determine whether Cosmos vision-language checkpoint is already embedded",
           "audit N1d6 exact Eagle configuration and offline tokenizer/embodiment stats",
           "compare policies on real robot data with frozen HW/backend/context/action horizon/batch",
           "measure owner physical free space, RAM and actual acquisition peak before any download"],
       "source_only_metadata_not_access_permission":True}
    dump(ROOT/OUT/"audit.json",facts)
    print(json.dumps({"new_selection":0,"n17_sha":n17["revision"],
      "n17_repo_bytes":n17["source_repository_bytes"],
      "n17_original_bytes":n17["recommended_original_file_scope_bytes"],
      "n17_count":n17["original_weight_file_count"],
      "base_model_elements":n17["published_model_safetensors_total"],
      "gated_parent":facts["potential_external_backbone"]["gated"],
      "legal_conflict":contradictory["contradictory_first_party_artifacts"],
      "issue_open":issue["state"],"research_union":cp["research_hold_scenario_logical_bytes"],
      "payload_download_bytes":0},ensure_ascii=False))
if __name__=="__main__":main()
