#!/usr/bin/env python3
"""TRELLIS.2 offline restore source evidence; anonymous metadata/code, no weights.

Records mandatory gated DINOv3 ViT-L and cross-repo sparse-structure decoder,
and distinguish default RMBG 2.0 preprocessing from required 3D inference.
"""
from __future__ import annotations
import base64
from datetime import datetime, timezone
import hashlib
import json
import re
import urllib.request
from pathlib import Path

from scripts.capacity_inventory import snapshot, dump, exact_sum
from scripts import capacity_selection as cap

ROOT=Path(__file__).resolve().parents[1]
OUT=Path("catalog/research/2026-11-07-trellis2-closure")
SRC=OUT/"sources"
PARENT="microsoft/TRELLIS.2-4B"
PARENT_SHA="af44b45f2e35a493886929c6d786e563ec68364d"
CODE_REPO="microsoft/TRELLIS.2"
CODE_SHA="75fbf0183001ed9876c8dbb35de6b68552ee08bd"
DECODER="microsoft/TRELLIS-image-large"
DINO="facebook/dinov3-vitl16-pretrain-lvd1689m"
RMBG="briaai/RMBG-2.0"
DEPENDENTS=(DECODER,DINO,RMBG)
DECODER_STEM="ckpts/ss_dec_conv3d_16l8_fp16"
API_ROOT="https://api.github.com/repos/microsoft/TRELLIS.2"
TEXTS=("trellis2/pipelines/base.py","trellis2/pipelines/trellis2_image_to_3d.py",
       "trellis2/modules/image_feature_extractor.py","trellis2/pipelines/rembg/BiRefNet.py",
       "LICENSE","README.md")
def need(v,msg):
    if not v:raise ValueError(msg)
def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def git_get(url):
    need(url.startswith(API_ROOT+"/") and "/git/blobs/" not in url
         and "/zipball/" not in url and "/tarball/" not in url,"unapproved GitHub URL")
    req=urllib.request.Request(url,headers={
      "Accept":"application/vnd.github+json","User-Agent":"local-model-portfolio-TRELLIS-source-audit",
      "X-GitHub-Api-Version":"2022-11-28"})
    with urllib.request.urlopen(req,timeout=25) as q:raw=q.read(2_000_001)
    need(len(raw)<=2_000_000,"GitHub source response oversized")
    return json.loads(raw.decode("utf-8"))
def git_code_evidence():
    need(bool(re.fullmatch("[a-f0-9]{40}",CODE_SHA)),"bad code revision")
    tree=git_get(f"{API_ROOT}/git/trees/{CODE_SHA}?recursive=1")
    need(tree.get("truncated") is False,"GitHub source tree truncated")
    rows=sorted((x for x in tree["tree"] if x["type"]=="blob"),key=lambda x:x["path"])
    need(len(rows)>120,"unexpected TRELLIS source footprint")
    bypath={x["path"]:x for x in rows}
    need(len(bypath)==len(rows),"duplicate code filenames")
    bytext={}
    for path in TEXTS:
        need(path in bypath and bypath[path]["size"]<160_000,"missing short source "+path)
        obj=git_get(f"{API_ROOT}/contents/{path}?ref={CODE_SHA}")
        need(obj.get("type")=="file" and obj.get("encoding")=="base64","not short text")
        raw=base64.b64decode(obj["content"])
        need(len(raw)==bypath[path]["size"] and len(raw)<160_000,"code text length mismatch")
        bytext[path]=raw.decode("utf-8")
    return rows,bytext
def pipeline_json():
    import urllib.error
    url=f"https://huggingface.co/{PARENT}/raw/{PARENT_SHA}/pipeline.json"
    req=urllib.request.Request(url,headers={"User-Agent":"local-model-portfolio-TRELLIS-manifest-audit"})
    # Only an explicitly whitelisted tiny JSON document is permitted.
    with urllib.request.urlopen(req,timeout=25) as r:
        need(r.url==url or r.url.endswith("/pipeline.json"),"unexpected HF redirect")
        body=r.read(100_001)
    need(len(body)<=100_000,"unexpected large pipeline metadata")
    data=json.loads(body)
    need(data.get("name")=="Trellis2ImageTo3DPipeline","unknown pipeline")
    return data,hashlib.sha256(body).hexdigest(),len(body)
def verify_identifiers(config,text):
    args=config["args"]
    need(args["models"]["sparse_structure_decoder"]==
         f"{DECODER}/{DECODER_STEM}","different sparse structure dependency")
    need(args["image_cond_model"]["name"]=="DinoV3FeatureExtractor","wrong vision encoder")
    need(args["image_cond_model"]["args"]["model_name"]==DINO,"wrong DINOv3 variant")
    need(args["rembg_model"]["name"]=="BiRefNet","unexpected background remover")
    need(args["rembg_model"]["args"]["model_name"]==RMBG,"wrong RMBG reference")
    need("pipeline.rembg_model = getattr(rembg" in text["trellis2/pipelines/trellis2_image_to_3d.py"],
         "default loader does not initialize background removal")
    need("pipeline.image_cond_model = getattr(image_feature_extractor" in text["trellis2/pipelines/trellis2_image_to_3d.py"],
         "default loader does not initialize DINOv3")
    need('DINOv3ViTModel.from_pretrained(model_name)' in text["trellis2/modules/image_feature_extractor.py"],
         "DINO loader changed")
    need("AutoModelForImageSegmentation.from_pretrained" in text["trellis2/pipelines/rembg/BiRefNet.py"],
         "background segmentation loader changed")
    need("models.from_pretrained(v)" in text["trellis2/pipelines/base.py"],
         "foreign model fallback changed")
    need("if has_alpha" in text["trellis2/pipelines/trellis2_image_to_3d.py"],
         "preprocessing alpha control changed")
    return {"required_sparse_decoder_repo":DECODER,"required_sparse_decoder_stem":DECODER_STEM,
        "required_vision_model":DINO,"default_loader_rembg_model":RMBG,
        "DINOv3_is_always_constructed_by_default_loader":True,
        "RMBG_is_always_constructed_by_default_loader":True,
        "RMBG_is_functionally_replaceable_with_different_background_preprocessor":True,
        "RMBG_is_not_proven_mandatory_for_rgba_geometry_without_source_modification":True,
        "external_decoder_is_loaded_by_foreign_repo_fallback":True,
        "offlinedemo_executed":False}
def source_select(repo,src):
    need(src["repo_id"]==repo and src["asset_kind"]=="model","different HF repo")
    need(src["payload_bytes_downloaded"]==0 and src["download_authorized"] is False,"payload access detected")
    evidence={"repo_id":repo,"source_revision":src.get("pinned_revision"),
      "source_tree_complete":bool(src.get("tree_complete")),
      "source_tree_error":src.get("error"),
      "source_all_repo_bytes":src.get("source_scope_bytes"),
      "gated":src.get("gated"),"source_license_metadata":src.get("license_metadata"),
      "source_snapshot_path":str(SRC/(repo.replace("/","--")+".json")),
      "selected_file_bytes":None,"selected_files":None,
      "personal_access_verified":False,"license_body_cleared":False,
      "read_only_source_metadata":True,"payload_identity_verified_on_owner_disk":False,
      "reconstruction_tested":False}
    if not src.get("tree_complete"):return evidence
    files={f["path"]:f for f in src["files"]}
    need(len(files)==len(src["files"]),"duplicate filenames")
    need(exact_sum(x["bytes"] for x in src["files"])==src["source_scope_bytes"],
         "full source tree byte mismatch")
    if repo==DECODER:
        names=[DECODER_STEM+".json",DECODER_STEM+".safetensors"]
        need(set(names).issubset(files),"external sparse decoder missing")
        # Keep named original learned weights and its architecture metadata only.
    elif repo in (DINO,RMBG):
        original=[x for x in ("model.safetensors","pytorch_model.bin") if x in files]
        # No artificial zero: if source tree lacks the expected original tensor, remain unknown.
        if not original:
            evidence["unresolved_weight_layout"]="Original model.safetensors / pytorch_model.bin not in public tree"
            return evidence
        weight="model.safetensors" if "model.safetensors" in original else "pytorch_model.bin"
        names=[weight]
        # Root config/processor/code and source rights; never duplicate other serialized weights.
        for path in files:
            if "/" in path:continue
            if path in ("LICENSE","LICENSE.md","LICENSE.txt","README.md","NOTICE","config.json",
                         "preprocessor_config.json","processor_config.json","tokenizer_config.json") or path.endswith(".py"):
                names.append(path)
        names=list(dict.fromkeys(names))
        need("config.json" in names,"vision model config missing")
    else:raise ValueError("unknown dependency")
    selected=[files[p] for p in names]
    size=exact_sum(x["bytes"] for x in selected)
    evidence.update(
       selected_file_bytes=size,
       selected_files=selected,
       masked_lfs_payload_files=sum(x.get("payload_hash_masked",False) for x in selected),
       selected_files_missing_sha256=sum(x.get("identity_kind")=="unverifiable_payload_hash" for x in selected),
       original_tensor_layout="BF16 or publisher format: do not infer real RAM from file extension",
       selection_is_only_a_research_profile=True)
    return evidence
def account(old,codetree,rows):
    need(old["source_revision"]=="v27-20261107" and old["exact_primary_file_scope_count"]==126,
        "v27 source records moved")
    need(old["known_scope_content_union_bytes"]==3_417_685_712_585,"v27 baseline logical bytes changed")
    entries=[(f"{x['repo_id']}@{x['source_revision']}",f) for x in old["items"] for f in x["files"]]
    entries += [(f"{x['repo_id']}@{x['revision']}",f) for x in old["dependencies"] for f in x["files"]]
    need(cap.union_bytes(entries)==old["known_scope_content_union_bytes"],"prior source SHA dedup differs")
    new=[]
    for row in rows:
        if row["selected_files"] is not None:
            new.extend((f"{row['repo_id']}@{row['source_revision']}",f) for f in row["selected_files"])
    code=[{"path":x["path"],"bytes":x["size"],"git_blob_sha1":x["sha"],"identity_kind":"git_blob_sha1"}
           for x in codetree]
    new.extend((f"github:{CODE_REPO}@{CODE_SHA}",f) for f in code)
    gross=exact_sum(x["bytes"] for _,x in new)
    extended=cap.union_bytes(entries+new)
    return {"baseline_known_logical_bytes":old["known_scope_content_union_bytes"],
      "new_source_selected_files_reported_gross_bytes":gross,
      "new_source_hash_identity_deduplicated_increment_bytes":extended-old["known_scope_content_union_bytes"],
      "new_source_partial_union_bytes":extended,
      "research_only_not_complete_archive_bytes":True,
      "required_dependency_profiles_all_complete":all(row["selected_file_bytes"] is not None for row in rows[:2]),
      "default_pipeline_three_dependencies_complete":all(row["selected_file_bytes"] is not None for row in rows),
      "remaining_archive_budget_if_all_scopes_cleared_not_computable":True,
      "owner_disk_free_bytes":None,"physical_archive_used_bytes":None,"download_peak_bytes":None,
      "model_payload_downloads":0,"approved_queue_unchanged":True}
def main():
    c=load("catalog/CURRENT.json")
    need(c["revision_id"]=="v27-20261107" and c["expected"]["tracked"]==173
         and c["expected"]["active"]==126,"catalog changed; review first")
    need(load("queues/approved.json")["entries"]==[],"approval queue changed")
    old=load("catalog/capacity/2026-11-07/v27/selected-file-capacity.json")
    base=load("catalog/capacity/2026-11-06/sources/model--microsoft--TRELLIS.2-4B.json")
    need(base["repo_id"]==PARENT and base["pinned_revision"]==PARENT_SHA
         and base["source_scope_bytes"]==16_237_485_044,"parent source changed")
    need(base["tree_complete"] and base["gated"] is False,"TRELLIS parent unexpectedly private")
    need(all(DECODER_STEM not in f["path"] for f in base["files"]),"external decoder already in parent")
    config,digest,config_bytes=pipeline_json()
    tree,text=git_code_evidence()
    depfacts=verify_identifiers(config,text)
    recs=[]
    for id in DEPENDENTS:
        snap=snapshot({"asset_kind":"model","repo_id":id,"portfolio_decision":"dependency_research_only"})
        dump(ROOT/SRC/(id.replace("/","--")+".json"),snap)
        rec=source_select(id,snap)
        recs.append(rec)
        print(json.dumps({"id":id,"revision":rec["source_revision"],
             "source_bytes":rec["source_all_repo_bytes"],
             "profile_bytes":rec["selected_file_bytes"],
             "gated":rec["gated"],"error":rec["source_tree_error"]},ensure_ascii=False),flush=True)
    need(recs[0]["selected_file_bytes"] is not None,"critical Microsoft sparse decoder missing")
    summary=account(old,tree,recs)
    result={"schema_version":1,"source_revision":"v27-20261107",
      "observed_at_utc":datetime.now(timezone.utc).isoformat(),
      "parent":{"id":PARENT,"immutable_revision":PARENT_SHA,"source_repo_bytes":base["source_scope_bytes"],
        "source_file_count":len(base["files"]), "model_pipeline_sha256":digest,
        "model_pipeline_json_bytes":config_bytes, "published_mit_metadata_not_rights_for_dependencies":True},
      "microsoft_source":{"repo":CODE_REPO,"git_revision":CODE_SHA,
        "code_tree_complete":True,"blob_file_count":len(tree),
        "gross_git_blob_bytes":exact_sum(x["size"] for x in tree),
        "source_license":"MIT","weight_payload_in_code_repo_not_downloaded":True},
      "dependency_facts_from_pinned_code":depfacts,
      "dependent_source_profiles":recs,
      "capacity_research_scenario":summary,
      "current_DINOv3_variants_in_portfolio_not_substitutes":[
        "facebook/dinov3-vit7b16-pretrain-lvd1689m",
        "facebook/dinov3-vith16plus-pretrain-lvd1689m"],
      "prerequisites_for_storage":["owner authenticates each gated HF repository individually",
        "no unofficial mirror as alternative to license approval",
        "confirm license terms for DINOv3 and RMBG; commercial/full pipeline terms distinct",
        "verify immutable LFS payload SHA256 after lawful acquisition",
        "pin torch/transformers/custom DINOv3 extractor ABI, NVIDIA rendering libraries",
        "test RGBA-only path if opting out of default RMBG model without bypassing licensing"],
      "research_only":True,"new_assets_selected":0,"new_download_authorizations":0,
      "model_payload_bytes_downloaded":0,"owner_hardware_tested":False,
      "full_offline_restoration_tested":False,"main_branch_not_modified":True,
      "source_urls":{
        "trellis_code":f"https://github.com/{CODE_REPO}/tree/{CODE_SHA}",
        "model_pipeline":f"https://huggingface.co/{PARENT}/blob/{PARENT_SHA}/pipeline.json",
        "microsoft_decoder":f"https://huggingface.co/{DECODER}",
        "dino":f"https://huggingface.co/{DINO}",
        "rembg":f"https://huggingface.co/{RMBG}",
        "licensing_issue":"https://github.com/microsoft/TRELLIS.2/issues/22",
        "reported_dino_compatibility_issue":"https://github.com/microsoft/TRELLIS.2/issues/161"}}
    dump(ROOT/OUT/"audit.json",result)
    print("SUMMARY",json.dumps({"revision":"v27-20261107","selected_assets_added":0,
       "source_dependency_profile_bytes":[{x["repo_id"]:x["selected_file_bytes"]} for x in recs],
       "source_only_partial_dedup_bytes":summary["new_source_partial_union_bytes"],
       "all_mandatory_repos_censused":summary["required_dependency_profiles_all_complete"]},
       ensure_ascii=False),flush=True)
if __name__=="__main__":main()
