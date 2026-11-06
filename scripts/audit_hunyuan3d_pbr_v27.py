#!/usr/bin/env python3
"""Read-only Hunyuan3D-2.1 PBR restoration dependency census (2026-11-07).

Only anonymous Hugging Face tree metadata, GitHub source text/tree metadata and
GitHub release-asset metadata. No checkpoint payload download or code execution.
"""
from __future__ import annotations

import base64
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import urllib.request

from scripts.capacity_inventory import snapshot, dump, exact_sum
from scripts import capacity_selection as cap

ROOT=Path(__file__).resolve().parents[1]
OUT=Path("catalog/research/2026-11-07-hunyuan3d-pbr")
PARENT="tencent/Hunyuan3D-2.1"
PARENT_REV="0b94677654c57bb9a6b6845cd7b704ccf551d327"
CODE_REPO="Tencent-Hunyuan/Hunyuan3D-2.1"
CODE_SHA="82920d643c0dc2f7bfd7255f45f62d386edfe60c"
DINO="facebook/dinov2-giant"
REAL_REPO="xinntao/Real-ESRGAN"
REAL_RELEASE_TAG="v0.1.0"
REAL_RELEASE_ASSET_ID=40831506
REAL_RELEASE_NAME="RealESRGAN_x4plus.pth"
REAL_RELEASE_BYTES=67_040_989
REAL_RELEASE_URL="https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
NEEDED_TEXTS=(
    "README.md",
    "LICENSE",
    "requirements.txt",
    "hy3dpaint/README.md",
    "hy3dpaint/LICENSE",
    "hy3dpaint/textureGenPipeline.py",
    "hy3dpaint/utils/multiview_utils.py",
    "hy3dpaint/utils/image_super_utils.py",
    "hy3dpaint/hunyuanpaintpbr/unet/modules.py",
)
def require(x,reason):
    if not x:raise ValueError(reason)
def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def save(path,obj):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
def git_get(url):
    allowed=(f"https://api.github.com/repos/{CODE_REPO}/",
             f"https://api.github.com/repos/{REAL_REPO}/releases/tags/")
    require(url.startswith(allowed),"GitHub operation outside source metadata whitelist")
    require(not any(y in url for y in ("/git/blobs/","/releases/assets/","/zipball","/tarball")),
            "GitHub payload endpoint forbidden")
    headers={"Accept":"application/vnd.github+json","User-Agent":"portfolio-hunyuan3d-source-audit",
            "X-GitHub-Api-Version":"2022-11-28"}
    if os.environ.get("GITHUB_TOKEN"):headers["Authorization"]="Bearer "+os.environ["GITHUB_TOKEN"]
    req=urllib.request.Request(url,headers=headers)
    with urllib.request.urlopen(req,timeout=25) as r:body=r.read(6_000_001)
    require(len(body)<=6_000_000,"unexpected large metadata body")
    return json.loads(body.decode("utf-8"))
def source_tree_and_texts():
    require(bool(re.fullmatch(r"[a-f0-9]{40}",CODE_SHA)),"invalid pinned code")
    tree=git_get(f"https://api.github.com/repos/{CODE_REPO}/git/trees/{CODE_SHA}?recursive=1")
    require(tree.get("truncated") is False,"truncated Github tree")
    files=sorted([x for x in tree["tree"] if x.get("type")=="blob"],key=lambda x:x["path"])
    require(len(files)==len({f["path"] for f in files}) and len(files)>350,"unexpected source tree")
    require(exact_sum(f["size"] for f in files)==173_699_323,"code blob sum changed")
    mapping={f["path"]:f for f in files}
    texts={}
    for path in NEEDED_TEXTS:
        require(path in mapping and mapping[path]["size"]<150_000,"source file missing/oversized: "+path)
        doc=git_get(f"https://api.github.com/repos/{CODE_REPO}/contents/{path}?ref={CODE_SHA}")
        require(doc.get("type")=="file" and doc.get("encoding")=="base64",
                "not expected source text")
        raw=base64.b64decode(doc["content"])
        require(len(raw)==mapping[path]["size"] and len(raw)<150_000,"mismatched text sizes")
        texts[path]=raw.decode("utf-8")
    return files,texts
def check_pipeline(texts):
    config=texts["hy3dpaint/textureGenPipeline.py"]
    multi=texts["hy3dpaint/utils/multiview_utils.py"]
    modules=texts["hy3dpaint/hunyuanpaintpbr/unet/modules.py"]
    superres=texts["hy3dpaint/utils/image_super_utils.py"]
    require('self.dino_ckpt_path = "facebook/dinov2-giant"' in config,"default DINO changed")
    require('self.realesrgan_ckpt_path = "ckpt/RealESRGAN_x4plus.pth"' in config,"super-res ckpt changed")
    require("self.use_dino = True" in modules,"DINO enabled for original PBR UNet changed")
    require("self.dino_v2 = Dino_v2(config.dino_ckpt_path)" in multi,"DINO runtime load changed")
    require('AutoModel.from_pretrained(dino_v2_path)' in modules,"DINO pretrained load changed")
    require('allow_patterns=["hunyuan3d-paintpbr-v2-1/*"]' in multi,"PBR native subfolder changed")
    require("model_path=config.realesrgan_ckpt_path" in superres,"RealESRGAN model loader changed")
    require(REAL_RELEASE_URL in texts["hy3dpaint/README.md"],"original release required URL changed")
    require("torch==2.5.1" in texts["README.md"],"publisher torch support statement changed")
    require("transformers==4.46.0" in texts["requirements.txt"],"Python dependency changed")
    require("diffusers==0.30.0" in texts["requirements.txt"],"diffusers dependency changed")
    rootlic=texts["LICENSE"]
    for term in ("EUROPEAN UNION","UNITED KINGDOM","SOUTH KOREA","Territory"):
        require(term in rootlic,"publisher's restricted license wording changed: "+term)
    header=texts["hy3dpaint/textureGenPipeline.py"].splitlines()[:10]
    require(any("NON-COMMERCIAL LICENSE" in x for x in header),
            "code header non-commercial warning changed")
    require("TENCENT HUNYUAN 3D 2.1 COMMUNITY LICENSE AGREEMENT" in texts["hy3dpaint/LICENSE"],
            "paint license text changed")
    return {
        "DINOv2_giant_required_by_default_pbr_checkpoint":True,
        "external_super_resolution_checkpoint_required_for_default_paint_pipeline":True,
        "DINOv2_giant_not_substitutable_with_DINOv3":True,
        "pbr_model_weights_already_in_parent_repo":True,
        "file_claim_only_not_runtime_test":True,
        "root_community_license_excludes_EU_UK_South_Korea":True,
        "source_header_says_noncommercial_but_actual_root_license_is_community":True,
        "source_and_weight_licenses_must_be_reviewed_separately":True,
        "environment_candidate":{"python":"3.10","torch":"2.5.1+cu124",
                                "transformers":"4.46.0","diffusers":"0.30.0",
                                "custom_cuda":["custom_rasterizer","DifferentiableRenderer"],
                                "tested_on_owner_hardware":False},
        "official_vram_recommendation_gb":{"shape":10,"texture":21,"combined":29,
                           "publisher_claim_not_measured":True,
                           "clock":None,"batch":None},
    }
def official_release():
    x=git_get(f"https://api.github.com/repos/{REAL_REPO}/releases/tags/{REAL_RELEASE_TAG}")
    matches=[a for a in x.get("assets",[]) if a.get("name")==REAL_RELEASE_NAME]
    require(len(matches)==1,"RealESRGAN release target missing")
    a=matches[0]
    require(a["id"]==REAL_RELEASE_ASSET_ID and a["size"]==REAL_RELEASE_BYTES,
            "RealESRGAN release asset mutable; abort rather than assume old byte count")
    require(a["browser_download_url"]==REAL_RELEASE_URL,"release URL changed")
    return {
       "repo":REAL_REPO,"release_tag":REAL_RELEASE_TAG,"release_id":x["id"],
       "release_asset_id":a["id"],"asset_name":a["name"],"bytes":a["size"],
       "digest_from_github_release_api":a.get("digest"),
       "payload_sha256_verified":False,
       "source_repo_license_spdx":"BSD-3-Clause (not independent pretrained checkpoint rights clearance)",
       "download_url_for_later_authorized_acquisition_only":REAL_RELEASE_URL,
       "first_published_at":a["created_at"],
       "downloaded_this_audit":False,
    }
def dino_profile(src):
    require(src["repo_id"]==DINO and src["asset_kind"]=="model","wrong DINO source")
    require(src.get("tree_complete") is True and src.get("payload_bytes_downloaded")==0
            and src.get("download_authorized") is False,"no complete public source tree")
    require(src.get("gated") is False,"DINOv2 source unexpectedly gated")
    require(src.get("license_metadata")=="apache-2.0","DINOv2 license changed")
    require(re.fullmatch("[a-f0-9]{40}",src.get("pinned_revision","")),"missing pinned DINO hash")
    require(src["source_scope_bytes"]==exact_sum(f["bytes"] for f in src["files"]),"DINO source sum changed")
    files={x["path"]:x for x in src["files"]}
    require("model.safetensors" in files and "config.json" in files and
            "preprocessor_config.json" in files,"DINOv2 required original/config missing")
    keep={"model.safetensors","config.json","preprocessor_config.json","README.md",
          "LICENSE","LICENSE.md","NOTICE",".gitattributes"}
    selected=[f for f in src["files"] if f["path"] in keep]
    require(len({x["path"] for x in selected})==len(selected),"duplicate selected DINO file")
    require(all("pytorch_model.bin"!=x["path"] for x in selected),"duplicate DINO serialization")
    require(files["model.safetensors"]["bytes"]>1_000_000_000,"DINOv2 giant unexpectedly tiny")
    return {
       "id":DINO,"pinned_revision":src["pinned_revision"],
       "source_repository_gross_bytes":src["source_scope_bytes"],
       "source_files":len(src["files"]),"selected_original_files_bytes":exact_sum(x["bytes"] for x in selected),
       "selected_original_files":selected,
       "not_chosen_alternative_weight_files":[x["path"] for x in src["files"] if
                     x["path"].endswith((".bin",".safetensors")) and x not in selected],
       "gated":src["gated"],"license_metadata":src["license_metadata"],
       "locally_verified_source_hashes":False,
       "publisher_snapshot_path":str(OUT/"sources/facebook--dinov2-giant.json"),
       "license_specific_use_cleared":False,
       "original_pretrained_weights_required":True,
       "selected_file_scope_only_not_execution":True,
    }
def dedup_v27(old,dino,real,codefiles):
    require(old["source_revision"]=="v27-20261107"
            and old["exact_primary_file_scope_count"]==126
            and old["known_scope_content_union_bytes"]==3_417_685_712_585,"v27 baseline changed")
    require(any(x["repo_id"]==PARENT for x in old["items"]),"parent Hunyuan selection missing")
    require(all(x["repo_id"]!=DINO for x in old["items"]),"DINOv2 already selected, review duplicate")
    entries=[(x["repo_id"]+"@"+x["source_revision"],f) for x in old["items"] for f in x["files"]]
    entries += [(x["repo_id"]+"@"+x["revision"],f) for x in old["dependencies"] for f in x["files"]]
    baseline=cap.union_bytes(entries)
    require(baseline==old["known_scope_content_union_bytes"],"stale dedup source")
    new=[(DINO+"@"+dino["pinned_revision"],f) for f in dino["selected_original_files"]]
    asset={"path":REAL_RELEASE_NAME,"bytes":real["bytes"],"sha256":None,
           "identity_kind":"unverified_release_asset",
           "asset_id":real["release_asset_id"],"sha256_verified":False}
    new.append((f"githubrelease:{REAL_REPO}@{REAL_RELEASE_TAG}:{real['release_asset_id']}",asset))
    git_files=[{"path":x["path"],"bytes":x["size"],"git_blob_sha1":x["sha"],"identity_kind":"git_blob_sha1"} for x in codefiles]
    new.extend((f"github:{CODE_REPO}@{CODE_SHA}",f) for f in git_files)
    new_gross=exact_sum(f["bytes"] for _,f in new)
    union=cap.union_bytes(entries+new)
    require(baseline<=union<=baseline+new_gross,"invalid logical union")
    return {
      "baseline_known_logical_bytes":baseline,
      "new_source_file_gross_bytes":new_gross,
      "new_source_hash_aware_logical_increment_bytes":union-baseline,
      "new_source_only_logical_union_bytes":union,
      "newly_required_model_bytes_not_part_of_v27_selected_primary_scopes":True,
      "real_esrgan_release_digest_unverified_not_sha256_deduplicated":True,
      "exact_primary_scopes_unchanged":126,
      "owner_real_disk_capacity_bytes":None,
      "owner_real_disk_free_bytes":None,
      "acquisition_peak_bytes":None,
      "complete_offline_archive_bytes":None,
      "no_model_downloads":True,
      "archive_budget_bytes":4_000_000_000_000,
      "minimum_free_space_bytes":200_000_000_000,
      "hypothetical_4TB_difference_not_physical_available_bytes":4_000_000_000_000-union,
    }
def main():
    c=load("catalog/CURRENT.json")
    require(c["revision_id"]=="v27-20261107" and c["expected"]["tracked"]==173
            and c["expected"]["active"]==126,"catalog revision changed; manual rebase")
    require(load("queues/approved.json")["entries"]==[],"approved queue changed")
    old=load("catalog/capacity/2026-11-07/v27/selected-file-capacity.json")
    parent=load("catalog/capacity/2026-11-06/sources/model--tencent--Hunyuan3D-2.1.json")
    require(parent["repo_id"]==PARENT and parent["pinned_revision"]==PARENT_REV
            and parent["source_scope_bytes"]==14_909_683_275,"parent source changed")
    tree,texts=source_tree_and_texts()
    findings=check_pipeline(texts)
    r=official_release()
    src=snapshot({"asset_kind":"model","repo_id":DINO,"portfolio_decision":"dependency_research_only"})
    require(not src.get("error"),"DINO hub metadata error: "+str(src.get("error")))
    dump(ROOT/OUT/"sources/facebook--dinov2-giant.json",src)
    dino=dino_profile(src)
    logical=dedup_v27(old,dino,r,tree)
    data={
       "schema_version":1,"audited_on":"2026-11-07",
       "observed_at_utc":datetime.now(timezone.utc).isoformat(),
       "baseline_revision":"v27-20261107","baseline_active_assets":126,
       "parent":{"id":PARENT,"source_revision":PARENT_REV,"source_gross_bytes":14_909_683_275,
                 "selected_in_portfolio":True},
       "code":{"repo":CODE_REPO,"revision":CODE_SHA,"complete_git_tree":True,
               "code_and_examples_blob_count":len(tree),
               "git_blob_gross_bytes":exact_sum(x["size"] for x in tree),
               "source_files":[{"path":x["path"],"bytes":x["size"],"git_blob_sha1":x["sha"]}
                               for x in tree],
               "no_source_payload_download":True},
       "checked_pbr_code_dependencies":findings,
       "dino_model":dino,
       "realesrgan_checkpoint":r,
       "capacity_scenario":logical,
       "rights_and_reproducibility_gaps":[
          "Tencent Community License territory excludes EU/UK/Korea, commercial MAU/Notice conditions need personal review",
          "Legacy Tencent source header labels NON-COMMERCIAL and differs from modern community license header; reconcile rights",
          "Meta DINOv2 Apache2 license metadata does not imply Tencent license grants third-party resale",
          "RealESRGAN_x4plus.pth GitHub release digest is null; SHA256 identity and pretrained-weight-specific rights not verified",
          "Python 3.10, PyTorch2.5.1+cu124, Diffusers0.30.0, Transformers4.46.0 and compiled CUDA extensions need ABI lock/test",
          "Storage for original Python wheelhouse, compile toolchain, mesh renderers, staging remains UNKNOWN",
          "Hunyuan3D PBR and DINOv2 full offline output has not been executed",
       ],
       "newly_selected_portfolio_assets":0,"newly_approved_downloads":0,
       "downloaded_model_payload_bytes":0,"owner_device_measured":False,
       "complete_offline_restoration_verified":False,
       "source_urls":{
         "parent":f"https://huggingface.co/{PARENT}/tree/{PARENT_REV}",
         "code":f"https://github.com/{CODE_REPO}/tree/{CODE_SHA}",
         "dino":"https://huggingface.co/"+DINO,
         "real":REAL_RELEASE_URL,
         "paper":"https://arxiv.org/abs/2506.15442",
       }
    }
    save(OUT/"audit.json",data)
    print(json.dumps({
      "DINO_sha":dino["pinned_revision"],"dino_selected_bytes":dino["selected_original_files_bytes"],
      "dino_gated":dino["gated"],"real_asset_id":REAL_RELEASE_ASSET_ID,
      "real_bytes":r["bytes"],"code_gross_bytes":data["code"]["git_blob_gross_bytes"],
      "source_only_logical_union":logical["new_source_only_logical_union_bytes"],
      "new_models_selected":0,"weights_downloaded":0},ensure_ascii=False))
if __name__=="__main__":main()
